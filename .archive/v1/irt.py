# irt.py

import os
import sys
import shutil
import multiprocessing as mp
import pandas as pd
import numpy as np
import torch
import deepirtools
import statsmodels.formula.api as smf
from box import Box
import json
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
import traceback
from statsmodels.regression.mixed_linear_model import MixedLMResults

# ─── MAX OUT YOUR CPU THREADS ────────────────────────────────────────────────
torch.set_num_threads(mp.cpu_count())           # one thread per core
torch.set_num_interop_threads(mp.cpu_count())   # for parallel kernels

# ─── TUNE cuDNN FOR BEST PERF ───────────────────────────────────────────────
torch.backends.cudnn.benchmark = True           # autotune best kernels
torch.backends.cudnn.enabled   = True           # ensure cuDNN is on

# Custom module imports
import data.data as loadData
import tools as tools
import plots as plots
import params as p

OVERWRITE = False
RUN_IRT = True
RUN_LMM = True
WORKERS_PER_GPU = 1  # Number of workers per GPU

class Logger:
    """A simple logger to write stdout to both terminal and a file,
    but skip any lines that start with 'Epoch =' in the log output."""
    def __init__(self, filepath):
        # Save original stdout
        self.terminal = sys.stdout
        # Open the logfile for writing (UTF-8)
        self.logfile = open(filepath, "w", encoding='utf-8')
        # Buffer to accumulate partial writes until a newline
        self._buffer = ""

    def write(self, message):
        # Accumulate into buffer so we can detect full lines
        self._buffer += message
        # While there's at least one newline, process complete lines
        while "\n" in self._buffer:
            line, self._buffer = self._buffer.split("\n", 1)
            # Re-add the newline we split off
            full_line = line + "\n"
            # Write to both terminal and logfile
            self.terminal.write(full_line)
            self.logfile.write(full_line)
        # Flush after handling any complete lines
        self.flush()

    def flush(self):
        # Ensure both streams are flushed
        self.terminal.flush()
        if self.logfile:
            self.logfile.flush()

    def close(self):
        # Close logfile cleanly when done
        if self.logfile:
            self.logfile.close()
            self.logfile = None

class DeepIrt:
    """Performs a confirmatory multidimensional IRT analysis,
    handling both dichotomous and polytomous (≥3 categories) data."""
    def __init__(self, params):
        print("\n--- Initializing DeepIrt ---\n")
        deepirtools.manual_seed(123)
        self.params     = params
        self.categories = params.data.categories
        self.device     = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(f"→ Running on {self.device.type.upper()}")

    def run(self, dfIRT, groups, items_summary, iteration):
        print("\n--- Running Confirmatory MIRT Analysis ---\n")

        # 1) Prepare stacked response matrix
        df = dfIRT.copy()
        df['Composite_ID'] = df['UID'].astype(str) + '_T' + df['test'].astype(str)
        resp = df.pivot(index='Composite_ID', columns='item_name', values='score')

        pt_ids    = resp.index.tolist()
        all_items = resp.columns.tolist()
        n_items   = len(all_items)

        # 2) Build CPU tensors for data & mask
        data_cpu = torch.from_numpy(np.nan_to_num(resp.values)).float()
        mask_cpu = torch.from_numpy(~np.isnan(resp.values)).float()

        # 3) Build the Q-matrix on CPU
        Q_cpu = torch.zeros((n_items, len(groups)), dtype=torch.float32)
        for i, item in enumerate(all_items):
            for gi, regexes in enumerate(groups.values()):
                if any(rx in item for rx in regexes):
                    Q_cpu[i, gi] = 1
                    break

        # 4) Report group membership counts
        print("Items Summary:")
        for gi, name in enumerate(groups.keys()):
            items_summary[name]['current'] = int(Q_cpu[:, gi].sum().item())
            items_summary[name]['percent'] = int(
                items_summary[name]['current'] / items_summary[name]['initial'] * 100
            )
        print(json.dumps(items_summary, indent=4))

        # 5) Determine the category count per item based on test design
        n_cats = []
        for it in all_items:
            if 'TC_' in it:
                n_cats.append(5)
            elif 'TQ_' in it:
                if len(self.categories) == 2:
                    n_cats.append(2)
                elif len(self.categories) == 3:
                    if "-O-" in it:
                        n_cats.append(3)
                    else:
                        n_cats.append(2)
        
        print(f"device: {self.device}, factors: {len(groups)}, Q shape: {Q_cpu.shape}")

        if self.params.analysis.correlated_factors:
            correlated_factors = list(range(len(groups)))
        else:
            correlated_factors = []

        # 6) Instantiate and move the model to device
        model = deepirtools.IWAVE(
            model_type         = "grm",
            latent_size        = len(groups),
            n_cats             = n_cats,
            Q                  = Q_cpu,
            device             = self.device,
            correlated_factors = correlated_factors,
        )

        # 7) Move data → GPU
        data = data_cpu.to(self.device, non_blocking=True)
        mask = mask_cpu.to(self.device, non_blocking=True)

        # 8) Fit
        print("Fitting the Confirmatory MIRT model...")
        model.fit(
            data         = data,
            missing_mask = mask,
            batch_size   = iteration['model_fit']['batch_size'],
            iw_samples   = iteration['model_fit']['iw_samples'],
            mc_samples   = iteration['model_fit']['mc_samples'],
        )
        print("Model fitting complete.")
        torch.cuda.empty_cache()

        # ============================ CORRECTED SECTION =============================
        # 9) Extract item parameters, handling both 1D and 2D intercept tensors

        with torch.no_grad():
            loadings   = model.loadings.detach().cpu()      # [n_items, n_factors]
            intercepts = model.intercepts.detach().cpu()    # Shape is either [n_items] or [n_items, max_thresholds]
            discr      = torch.linalg.norm(loadings, dim=1) # [n_items]

            # Build difficulties by averaging only over each item's real thresholds
            diffs = []
            
            # Check the dimensionality of the intercepts tensor ONCE.
            is_dichotomous_case = intercepts.dim() == 1

            for j, k in enumerate(n_cats):
                # each item j has k categories ⇒ k–1 thresholds
                if k <= 1:
                    diffs.append(float('nan'))
                else:
                    if is_dichotomous_case:
                        # If all items are dichotomous, intercepts is a 1D tensor.
                        # We simply take the j-th element.
                        alpha_j = intercepts[j]
                    else:
                        # Otherwise, it's a 2D tensor.
                        # Take the first (k–1) intercepts for item j.
                        alpha_j = intercepts[j, : (k-1)]
                    
                    # The rest of the calculation is the same.
                    # threshold difficulties = –α_j / a_j
                    b_j = -alpha_j / discr[j]
                    diffs.append(b_j.mean().item())

            diffs = np.array(diffs, dtype=float)
        # ==============================================================================

        item_params = {
            'Difficulty':               diffs,
            'Overall_Discrimination':   discr.numpy(),
        }
        for fi, fname in enumerate(groups.keys()):
            item_params[f'Discrim_{fname}'] = loadings[:, fi].numpy()

        df_items = pd.DataFrame(item_params, index=all_items)
        df_items.index.name = 'item_name'

        # 10) Score all person-timepoints in small batches
        theta_cols = [f"Theta_{g}" for g in groups.keys()]
        all_thetas = []
        batch_sz   = iteration['model_scores']['scoring_batch_size']
        N          = data.size(0)
        with torch.no_grad():
            for i in range(0, N, batch_sz):
                Xb = data[i:i+batch_sz]
                Mb = mask[i:i+batch_sz]
                th = model.scores(
                    data         = Xb,
                    missing_mask = Mb,
                    mc_samples   = iteration['model_scores']['mc_samples'],
                    iw_samples   = iteration['model_scores']['iw_samples']
                )
                all_thetas.append(th.cpu())

        thetas = torch.cat(all_thetas, dim=0).numpy()
        torch.cuda.empty_cache()

        # build df_thetas
        df_thetas = pd.DataFrame(thetas, columns=theta_cols, index=pt_ids)
        df_thetas.index.name = 'Composite_ID'
        df_thetas.reset_index(inplace=True)
        df_thetas[['UID','test']] = df_thetas['Composite_ID'].str.split('_T', n=1, expand=True)
        df_thetas['test'] = pd.to_numeric(df_thetas['test'])
        
        # --- Invert theta scale for interpretability ---
        theta_cols = [c for c in df_thetas.columns if c.startswith('Theta_')]
        df_thetas[theta_cols] = df_thetas[theta_cols] * 1
        
        df_thetas = df_thetas[['UID','test'] + theta_cols]

        print("Parameter extraction complete.\n")
        return df_thetas, df_items

class Analysis:
    def __init__(self, dfData, params, gpu_id=None):
        print("\n--- Initializing Analysis ---\n")
        self.params = params
        self.dfData = dfData
        self.dfIRT_initial = None
        self.items_summary = {}
        self.gpu_id = gpu_id    
        self.save_path = os.path.join(self.params.general.save_folder, f"{self.params.general.file_header}")

    def _prepare_data(self):
        """Prepares the initial IRT data frame."""

        px_data = tools.select_px(
            self.dfData, 
            self.params.px.exclude, 
            self.params.px.age_range
        )

        self.dfIRT_initial, self.items_summary = tools.select_data(
            df=px_data,
            tests=self.params.data.tests,
            all_tags=self.params.data.all_tags,
            groups=self.params.data.groups,
            categories=self.params.data.categories,
            specify_room=self.params.analysis.specify_room
        )

        self.dfIRT_raw = self.dfIRT_initial.copy()
        self.dfIRT_initial.to_csv(f"{self.save_path}data.csv", index=False)

        self.dfIRT_initial = tools.remove_invariant_items(self.dfIRT_initial)

        print(f"IRT data prepared with {len(self.dfIRT_initial['item_name'].unique())} items and {len(self.dfIRT_initial['UID'].unique())} participants.")

        self.dfIRT_initial.to_csv(f"{self.save_path}data2.csv", index=False)

    def _run_ctt_lmm_comparison(self, file_header):
        """Fits competing LMMs (linear, quadratic, log, combinations, spline) and returns the best model."""

        print("CTT LMM comparison complete.")
        print("File header:", file_header)

        df_ctt_long = self.dfIRT_raw
        # Rename score column to Score for consistency
        df_ctt_long.rename(columns={'score': 'Score'}, inplace=True)
        df_ctt_long.rename(columns={'test': 'Test'}, inplace=True)

        factors = []
        item_names = df_ctt_long['item_name']
        for item in item_names:
            for group_name, regexes in self.params.data.groups.items():
                if any(rx in item for rx in regexes):
                    factors.append(group_name)
                    break

        df_ctt_long['Factor'] = factors


        if "TC_" in self.params.data.all_tags_keys:
            # We need to remap the confidence scores from a 0-4 scale to a 0-1 scale
            df_ctt_long['Score'] = df_ctt_long['Score'] / 4.0

        df_ctt_long = (
            df_ctt_long
            .groupby(['UID', 'Test', 'Factor'], as_index=False)['Score']
            .mean()
            # .rename(columns={'Score': 'meanScore'})
        )

        factor_names = list(self.params.data.groups.keys())
        # print("#######################")
        # print("Factor names:", factor_names)
        # print(df_ctt_long)

        # Set Factor as ordered categorical
        df_ctt_long['Factor'] = pd.Categorical(df_ctt_long['Factor'], categories=factor_names, ordered=True)

        # Now sort by that column
        df_ctt_long = df_ctt_long.sort_values('Factor').reset_index(drop=True)

        # print(df_ctt_long)
        # print("#######################")

        # 2) Create time covariates
        day_map = {1: 0, 2: 1, 3: 3, 4: 6}
        df_ctt_long['Days']    = df_ctt_long['Test'].map(day_map)
        df_ctt_long['Days_sq'] = df_ctt_long['Days'] ** 2
        df_ctt_long['log_Days']= np.log(df_ctt_long['Days'] + 1)

        # 3) Determine whether we have multiple factors
        n_groups = len(self.params.data.groups)
        
        # 4) Build our formula set
        if n_groups == 1:
            # Single‐factor: no Factor interaction
            formulas = {
                "Linear":      "Score ~ Days",
                "Quadratic":   "Score ~ Days + Days_sq",
                "Log":         "Score ~ log_Days",
                "Lin+Log":     "Score ~ Days + log_Days",
                "Quad+Log":    "Score ~ Days + Days_sq + log_Days",
                # "Spline":      "score ~ bs(Days, df=3)"
            }
        else:
            # Multi‐factor: include treatment‐coded Factor
            rg = self.params.analysis.lmm_reference_group
            wrap = f"C(Factor, Treatment('{rg}'))"
            formulas = {
                "Linear":      f"Score ~ Days * {wrap}",
                "Quadratic":   f"Score ~ (Days + Days_sq) * {wrap}",
                "Log":         f"Score ~ log_Days * {wrap}",
                "Lin+Log":     f"Score ~ (Days + log_Days) * {wrap}",
                "Quad+Log":    f"Score ~ (Days + Days_sq + log_Days) * {wrap}",
                # "Spline":      f"score ~ bs(Days, df=3) * {wrap}"
            }

        # Dump the model summary to file
        with open(f"{file_header}data_ctt_summary.txt", 'w') as f:
            f.write("")

        # print("df_ctt_long:\n", df_ctt_long)
        # sys.exit()


        # 5) Fit each candidate and record AIC
        models = {}
        aics   = {}
        for model_name, formula in formulas.items():

            print(f"Fitting model: {model_name} with formula: {formula}")

            model_path = f"{file_header}data_ctt_{model_name}.pkl"

            if os.path.exists(model_path):
            
                fit = MixedLMResults.load(model_path)
                
            else:
                # choose random‐slope matching the formula
                re_term = "~log_Days" if "log" in model_name.lower() else "~Days"
                mdl = smf.mixedlm(
                    formula,
                    data=df_ctt_long,
                    groups=df_ctt_long["UID"],
                    re_formula=re_term
                )
                fit = mdl.fit(method=["lbfgs"], reml=False)

                fit.save(f"{file_header}data_ctt_{model_name}.pkl")

            models[model_name] = fit
            aics[model_name]   = fit.aic

            # Dump the model summary to file
            with open(f"{file_header}data_ctt_summary.txt", 'a') as f:
                f.write(f"\n\nModel: {model_name}\n")
                f.write(fit.summary().as_text())

            plots.plot_ctt_regression(
                lmm_results = fit,
                df_long     = df_ctt_long,
                save_path   = f"{file_header}plot_ctt_scor_{model_name}.png",
                params      = self.params.plots.ctt_regression,
                colors      = self.params.data.colors
            )

            plots.plot_lmm_diagnostics(
                lmm_results = fit,
                save_path   = f"{file_header}plot_ctt_diag_{model_name}.png",
                params      = self.params.plots.lmm_diagnostics,
            )

        # 6) Rank the models by AIC from best to worst
        model_ranking = sorted(aics.items(), key=lambda x: x[1])
        with open(f"{file_header}data_ctt_summary.txt", 'a') as f:
            f.write("\n\nModel Ranking by AIC:\n")
            for name, aic in model_ranking:
                while len(name) < 12:
                    name += " "
                f.write(f"{name}: AIC = {aic:.2f}\n")

        return

    def _run_irt_lmm_comparison(self, df_thetas, file_header, pass_num, df_items):
        """Fits competing LMMs (linear, quadratic, log, combinations, spline) and returns the best model."""
        
        # 1) Melt into long format
        df_lmm_long = df_thetas.melt(
            id_vars=['UID', 'test'],
            value_vars=[c for c in df_thetas.columns if c.startswith('Theta_')],
            var_name='Factor', value_name='Ability'
        )
        df_lmm_long['Factor'] = df_lmm_long['Factor'].str.replace('Theta_', '')
        
        # 2) Create time covariates
        day_map = {1: 0, 2: 1, 3: 3, 4: 6}
        df_lmm_long['Days']    = df_lmm_long['test'].map(day_map)
        df_lmm_long['Days_sq'] = df_lmm_long['Days'] ** 2
        df_lmm_long['log_Days']= np.log(df_lmm_long['Days'] + 1)
        
        # 3) Determine whether we have multiple factors
        n_groups = len(self.params.data.groups)
        
        # 4) Build our formula set
        if n_groups == 1:
            # Single‐factor: no Factor interaction
            formulas = {
                "Linear":      "Ability ~ Days",
                "Quadratic":   "Ability ~ Days + Days_sq",
                "Log":         "Ability ~ log_Days",
                "Lin+Log":     "Ability ~ Days + log_Days",
                "Quad+Log":    "Ability ~ Days + Days_sq + log_Days",
                # "Spline":      "Ability ~ bs(Days, df=3)"
            }
        else:
            # Multi‐factor: include treatment‐coded Factor
            rg = self.params.analysis.lmm_reference_group
            wrap = f"C(Factor, Treatment('{rg}'))"
            formulas = {
                "Linear":      f"Ability ~ Days * {wrap}",
                "Quadratic":   f"Ability ~ (Days + Days_sq) * {wrap}",
                "Log":         f"Ability ~ log_Days * {wrap}",
                "Lin+Log":     f"Ability ~ (Days + log_Days) * {wrap}",
                "Quad+Log":    f"Ability ~ (Days + Days_sq + log_Days) * {wrap}",
                # "Spline":      f"Ability ~ bs(Days, df=3) * {wrap}"
            }

                # Dump the model summary to file
        with open(f"{file_header}data_irt_summary.txt", 'w') as f:
            f.write("")
        
        # 5) Fit each candidate and record AIC
        models = {}
        aics   = {}
        for model_name, formula in formulas.items():

            model_path = f"{file_header}data_irt_{model_name}.pkl"
            if os.path.exists(model_path):
                fit = MixedLMResults.load(model_path)
            else:
                re_term = "~log_Days" if "log" in model_name.lower() else "~Days"
                mdl = smf.mixedlm(
                    formula,
                    data=df_lmm_long,
                    groups=df_lmm_long["UID"],
                    re_formula=re_term
                )
                fit = mdl.fit(method=["lbfgs"], reml=False)
                fit.save(f"{file_header}data_irt_{model_name}.pkl")

            models[model_name] = fit
            aics[model_name]   = fit.aic

            # Dump the model summary to file
            with open(f"{file_header}data_irt_summary.txt", 'a') as f:
                f.write(f"\n\nModel: {model_name}\n")
                f.write(fit.summary().as_text())

            self._plots(
                model_name  = model_name,
                file_header = file_header,
                df_items    = df_items,
                lmm_results = fit,
                df_lmm_long = df_lmm_long
            )

        # 6) Rank the models by AIC from best to worst
        model_ranking = sorted(aics.items(), key=lambda x: x[1])
        with open(f"{file_header}data_irt_summary.txt", 'a') as f:
            f.write("\n\nModel Ranking by AIC:\n")
            for name, aic in model_ranking:
                while len(name) < 12:
                    name += " "
                f.write(f"{name}: AIC = {aic:.2f}\n")

        return

    def _plots(self, model_name, file_header, df_items, lmm_results, df_lmm_long):
        
        plots.plot_lmm_diagnostics(
            lmm_results = lmm_results,
            save_path   = f"{file_header}plot_irt_diag_{model_name}.png",
            params      = self.params.plots.lmm_diagnostics,
        )
        
        plots.plot_lmm_trajectory(
            lmm_results = lmm_results,
            df_long     = df_lmm_long,
            save_path   = f"{file_header}plot_irt_abil_{model_name}.png",
            params      = self.params.plots.lmm_trajectory,
            colors      = self.params.data.colors
        )
        
        plots.plot_predicted_probabilities(
            lmm_results = lmm_results,
            df_items    = df_items,
            df_long     = df_lmm_long,
            groups      = self.params.data.groups,
            save_path   = f"{file_header}plot_irt_prob_{model_name}.png",
            params      = self.params.plots.predicted_probabilities,
            colors      = self.params.data.colors
        )

    def _run_pass_analysis(self, df_thetas, df_items, pass_num, file_header):
        """
        Runs the full LMM and plotting pipeline for a single pass of the
        iterative filtering process. Also saves the dataframes for this pass.
        """
        print(f"\n--- Running Full Analysis for Pass {pass_num} ---")

        plots.plot_item_difficulty(
            item_params_df  = df_items, 
            save_path       = f"{file_header}plot_irt_itemDifficulty.png",
            params          = self.params.plots.item_difficulty,
            colors          = self.params.data.colors
        )

        # --- LMM Model Comparison ---
        if pass_num == 1:
            self._run_ctt_lmm_comparison(file_header)
        
        self._run_irt_lmm_comparison(df_thetas, file_header, pass_num, df_items)        
            
        return

    def run(self):
        """Main execution function for the iterative analysis."""
        self._prepare_data()
        dirt = DeepIrt(self.params)
        df_irt_current = self.dfIRT_initial.copy()
        n_initial_items = len(df_irt_current['item_name'].unique())
        
        pass_results_lmm = []
        excluded_items = set()

        pass_num = 0

        for iteration in self.params.analysis.iterations:

            pass_num += 1

            # Use existing data if it exists, otherwise prepare new data
            if os.path.exists(f"{self.save_path}p{pass_num}_{iteration['label']}_data_ability.csv") and os.path.exists(f"{self.save_path}p{pass_num}_{iteration['label']}_data_difficulty.csv"):
                print(f"Using existing data for Pass {iteration['label']}...")
                df_thetas = pd.read_csv(f"{self.save_path}p{pass_num}_{iteration['label']}_data_ability.csv")
                df_items = pd.read_csv(f"{self.save_path}p{pass_num}_{iteration['label']}_data_difficulty.csv", index_col='item_name')

            else:
                if self.gpu_id is None:
                    print(f"\n--- WARNING: GPU ID is None. Skipping Pass {pass_num} ---")
                    continue
                print(f"\n--- Starting Pass {iteration['label']} Analysis ---")
                df_thetas, df_items = dirt.run(df_irt_current, self.params.data.groups, self.items_summary.copy(), iteration)
                df_thetas.to_csv(f"{self.save_path}p{pass_num}_{iteration['label']}_data_ability.csv", index=False)
                df_items.to_csv(f"{self.save_path}p{pass_num}_{iteration['label']}_data_difficulty.csv")
                print(f"Saved theta scores and item parameters for Pass {iteration['label']}.")

            min_d, max_d = iteration['min_discrim_threshold'], iteration['max_discrim_threshold']
            print(f"Excluding items with Overall_Discrimination < {min_d} or > {max_d} for Pass {iteration['label']}...")
            # newly_excluded = set(df_items[(df_items['Overall_Discrimination'] < min_d) | (df_items['Overall_Discrimination'] > max_d)].index)
            # 1. Dynamically find all discrimination columns
            discrim_cols = [col for col in df_items.columns if col.startswith('Discrim_')]

            # 2. Build the filtering condition for all of them.
            #    This removes items if their discrimination on a factor they load on is bad.
            is_bad_item = pd.Series(False, index=df_items.index)
            for col in discrim_cols:
                # Get the discrimination values for the current factor
                discrim_values = df_items[col]

                is_bad_for_this_factor = (
                    (discrim_values > max_d) | 
                    ((discrim_values < min_d) & (discrim_values != 0))
                )
                
                # Update the master list: if an item is bad on ANY factor, it's out.
                is_bad_item |= is_bad_for_this_factor

            newly_excluded = set(df_items[is_bad_item].index)

            if RUN_LMM:

                self._run_pass_analysis(df_thetas, df_items, pass_num, f"{self.save_path}p{pass_num}_{iteration['label']}_")
                # pass_results_lmm.append(best_lmm)
                
                # plots.plot_model_evolution(
                #     all_lmm_results = pass_results_lmm, 
                #     df_long_final   = df_lmm_long,
                #     save_folder     = f"{self.save_path}pass-{pass_num}_{iteration['label']}_",
                #     params          = self.params.plots.model_evolution,
                # )

            print(f"\n--- Pass {iteration['label']} Summary: Found {len(newly_excluded)} new items to exclude for the next pass ---")
            for item in sorted(list(newly_excluded)): print(f"  - {item}")
            
            excluded_items.update(newly_excluded)
            n_remaining = n_initial_items - len(excluded_items)
            percent_rem = (n_remaining / n_initial_items) * 100
            print(f"Total items excluded so far: {len(excluded_items)}. Remaining: {n_remaining}/{n_initial_items} ({percent_rem:.1f}%)")
            df_irt_current = self.dfIRT_initial[~self.dfIRT_initial['item_name'].isin(excluded_items)]
        
        print("\n--- Analysis Complete ---")
        return
        # print(f"\n--- WARNING: Max iterations reached. Using results from last pass. ---")

def main(params, dfData, gpu_id=None):
    """Main entry point for the script."""

    if gpu_id is not None:
        if torch.cuda.is_available():
            torch.cuda.set_device(gpu_id)
            print(f"Using GPU {gpu_id} for this run.")
        else:
            print(f"GPU {gpu_id} not available. Running on CPU instead.")
            gpu_id = None

    params = Box(params)

    # --- Parameter Setup ---
    # Get our all_tags list from the DataFrame columns
    for tag_key in params.data.all_tags_keys:
        params.data.all_tags.extend([tag for tag in dfData.columns if tag_key in tag])
    # Remove duplicates and sort the tags
    params.data.all_tags = sorted(set(params.data.all_tags))

    # Set the reference group for LMMs if not already set
    if not params.analysis.lmm_reference_group:
        if params.data.groups:
            params.analysis.lmm_reference_group = list(params.data.groups.keys())[0]
        else:
            raise ValueError("No groups defined for LMM analysis. Please set 'lmm_reference_group' in params.")
        
    if not os.path.exists(params.general.save_folder): os.makedirs(params.general.save_folder)
    else:
        if OVERWRITE:
            print(f"Warning: Save folder '{params.general.save_folder}' already exists. Overwriting contents.")
            remove = True
            start_time = time.time()
            while start_time + 5 > time.time():
                response = input("Press Enter to cancel...")
                if response == "":
                    remove = False
                    break
            if remove:
                shutil.rmtree(params.general.save_folder)
                os.makedirs(params.general.save_folder)

    logger = Logger(os.path.join(params.general.save_folder, f"{params.general.file_header}.txt"))
    sys.stdout = logger
    
    logger.logfile.write("--- Analysis Configuration ---\n")
    logger.logfile.write(f"params = {json.dumps(params, indent=4)}\n")

    try:
        irt = Analysis(dfData, params, gpu_id)
        irt.run()

    except KeyboardInterrupt:
        print("\n--- Analysis interrupted by user. Exiting gracefully. ---")
        sys.exit(0)

    except Exception as e:
        print(f"\n--- AN UNEXPECTED ERROR OCCURRED ---")
        print(f"Error: {e}")
        print(traceback.format_exc())
    
    finally:
        if isinstance(sys.stdout, Logger):
            sys.stdout.close(); sys.stdout = sys.stdout.terminal

if __name__ == "__main__":

    mp.set_start_method('spawn', force=True)

    dfMaster, dfVariables, dfData = loadData.startup()
    dfData = tools.calculateDays(dfData)

    # dfData.to_csv("results/dfData.csv", index=False)

    print("\n--- Starting IRT Analysis ---\n")
    
    params_list = p.params_list

    params_list = params_list[:4]
    
    n_gpus      = torch.cuda.device_count()
    max_workers = min(len(params_list), n_gpus)
    if max_workers == 0:
        print("No GPUs available. Running on CPU with 1 worker.")
        max_workers = 1

    max_workers = 1
        
    print(f"Using {n_gpus} GPUs, running {len(params_list)} parameter sets with up to {max_workers} workers.")
    input("Press Enter to start the analysis...")

    with ProcessPoolExecutor(max_workers=max_workers) as exe:
        futures = {}
        for idx, params in enumerate(params_list):
            gpu_id = idx % n_gpus if n_gpus > 0 else None
            futures[exe.submit(main, params, dfData.copy(), gpu_id)] = (idx, gpu_id)

        for fut in as_completed(futures):
            idx, gpu_id = futures[fut]
            try:
                fut.result()
                print(f"✓ Run #{idx} finished on GPU {gpu_id}")
                
            except Exception as e:
                print(f"✗ Run #{idx} on GPU {gpu_id} failed:", e)
                print(traceback.format_exc())