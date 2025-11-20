# analysis.py
import pandas as pd
import numpy as np
import os
from statsmodels.regression.mixed_linear_model import MixedLMResults
from statsmodels.stats.outliers_influence import variance_inflation_factor
import statsmodels.formula.api as smf
import sys
import traceback
from params import ANALYSIS_LIST
import plots
from box import Box
import json

df_data = pd.read_csv('dfData.csv')
df_data.rename(columns={'test': 'Test'}, inplace=True)

RECOMPUTE = False
# List all the folder names in the results directory
MODEL_TYPE = 'Lin+Log'
MIN_DISCRIM_THRESHOLD = 0.25
MAX_DISCRIM_THRESHOLD = 4


UTIL_PLOT_PARAMS = {
    'title': 'Utility',
    'x_axis': {
        'label': 'Days Since Encoding',
        'range': [0, 6],
        'tick_gap': 1,
    },
    'y_axis': {
        'label': 'Predicted Utility',
        'range': [-1, 1],
        'tick_gap': 1,
    },
    'legend': {
        'show': True,
        'location': 'upper right',
        'title': None,
        'fontsize': 'small',
        'framealpha': 0.8,  # Transparency of the legend frame
    },
    'output': {
        'show': True,  # Show the plot interactively
        'save': True,  # Save the plot to disk
        'dpi': 300,  # DPI for saved plots
        'filename': 'utility.png',
    }
}
blue    = '#1f77b4'
orange  = '#ff7f0e'
green   = '#2ca02c'
red     = '#d62728'
purple  = '#9467bd'
brown   = '#8c564b'
pink    = '#e377c2'
grey    = '#7f7f7f'
mustard = '#bcbd22'
cyan    = '#17becf'
black   = '#000000'

COLORS_UTIL = [
    blue,
    orange,
    green,
    brown
]

def get_factors(name):
    for analysis in ANALYSIS_LIST:
        if analysis['label'] == name:
            return analysis['groups']

def prep_ctt_df_long(name, factors):
    # --- Prep Confidence Data ---

    corr = 'corr'
    if len(factors) == 1:
        corr = 'uncorr'
    
    # Get the raw data
    df_conf = pd.read_csv(f'results/{name}/TC_{corr}_noroom_5cats_data.csv')

    # Get a list of item names so we can map them to factors
    item_names = df_conf['item_name'].to_list()
    factors_list = []
    for item in item_names:
        for factor, regex_list in factors.items():
            if any(regex in item for regex in regex_list):
                factors_list.append(factor)
                break
        else:
            # If no factor matches, this is a critical error in the data
            sys.exit(f"Error: Item '{item}' does not match any factor in {factors.keys()}. Please check the factors configuration.")

    # Add the factors to the DataFrame
    df_conf['Factor'] = factors_list

    # Group by UID, test, and Factor, and calculate the mean score
    df_conf.rename(columns={'score': 'Data'}, inplace=True)
    df_conf.rename(columns={'test': 'Test'}, inplace=True)
    df_conf['Data'] = df_conf['Data'] / 4.0 # Normalize the score to a 0-1 range
    df_conf = (
        df_conf
        .groupby(['UID', 'Test', 'Factor'], as_index=False)['Data']
        .mean()
        )
    # Add the Measure column
    df_conf['Measure'] = 'conf'


    # --- Prep Score Data ---
    # Get the raw data
    df_scor = pd.read_csv(f'results/{name}/TQ_{corr}_noroom_2cats_data.csv')

    # Get a list of df_scor names so we can map them to factors
    item_names = df_scor['item_name'].to_list()
    factors_list = []
    for item in item_names:
        for factor, regex_list in factors.items():
            if any(regex in item for regex in regex_list):
                factors_list.append(factor)
                break
        else:
            # If no factor matches, this is a critical error in the data
            sys.exit(f"Error: Item '{item}' does not match any factor in {factors.keys()}. Please check the factors configuration.")

    # Add the factors to the DataFrame
    df_scor['Factor'] = factors_list

    df_scor.rename(columns={'score': 'Data'}, inplace=True)
    df_scor.rename(columns={'test': 'Test'}, inplace=True)
    df_scor = (
        df_scor
        .groupby(['UID', 'Test', 'Factor'], as_index=False)['Data']
        .mean()
        )
    df_scor['Measure'] = 'scor'

    # Combine DataFrames
    df_long = pd.concat([df_conf, df_scor], ignore_index=True)
    df_long.rename(columns={'test': 'Test'}, inplace=True)

    df_long['Source'] = 'ctt'
    
    return df_long

def prep_irt_df_long(name, factors):
    
    corr = 'corr'
    if len(factors) == 1:
        corr = 'uncorr'
    
    # --- Prep Confidence Data ---
    # Get the raw data
    df_conf = pd.read_csv(f'results/{name}/TC_{corr}_noroom_5cats_p2_high_data_ability.csv')
    df_conf.rename(columns={'test': 'Test'}, inplace=True)
    
    # Get a list of columns that start with 'Theta_'
    value_vars = [col for col in df_conf.columns if col.startswith('Theta_')]

    # Melt the dataframe into long format
    df_conf = df_conf.melt(id_vars=['UID', 'Test'], value_vars=value_vars,
                    var_name='Factor', value_name='Data')

    # Extract the part after 'Theta_' in the Factor column
    df_conf['Factor'] = df_conf['Factor'].str.replace(r'^Theta_', '', regex=True)

    df_conf.reset_index(drop=True, inplace=True)
    df_conf['Measure'] = 'conf'

    # --- Prep Score Data ---
    # Get the raw data
    df_scor = pd.read_csv(f'results/{name}/TQ_{corr}_noroom_2cats_p2_high_data_ability.csv')
    df_scor.rename(columns={'test': 'Test'}, inplace=True)
    
    # Get a list of columns that start with 'Theta_'
    value_vars = [col for col in df_scor.columns if col.startswith('Theta_')]

    # Melt the dataframe into long format
    df_scor = df_scor.melt(id_vars=['UID', 'Test'], value_vars=value_vars,
                    var_name='Factor', value_name='Data')

    # Extract the part after 'Theta_' in the Factor column
    df_scor['Factor'] = df_scor['Factor'].str.replace(r'^Theta_', '', regex=True)

    df_scor.reset_index(drop=True, inplace=True)
    df_scor['Measure'] = 'scor'

    # Combine DataFrames
    df_long = pd.concat([df_conf, df_scor], ignore_index=True)

    df_long['Source'] = 'irt'

    return df_long

def prep_prob_df_long(name, factors, irt_df_long):

    corr = 'corr'
    if len(factors) == 1:
        corr = 'uncorr'

    logit_data = {}
    for factor in factors.keys():
        logit_data[factor] = {
            'scor': {
                'mean_discrimination': None,
                'mean_difficulty': None,
            },
            'conf': {
                'mean_discrimination': None,
                'mean_difficulty': None,
            }
        }

    for measure in ['conf', 'scor']:
        if measure == 'conf':
            df = pd.read_csv(f'results/{name}/TC_{corr}_noroom_5cats_p2_high_data_difficulty.csv')
        else:
            df = pd.read_csv(f'results/{name}/TQ_{corr}_noroom_2cats_p2_high_data_difficulty.csv')

        for factor in factors.keys():
            # --- Filter items for the current factor ---
            discrim_col_name = f'Discrim_{factor}'
            acceptable_items = df[
                (df[discrim_col_name] >= MIN_DISCRIM_THRESHOLD) & 
                (df[discrim_col_name] <= MAX_DISCRIM_THRESHOLD)
            ]

            # # --- Calculate average parameters from ONLY the filtered set ---
            avg_discrimination = acceptable_items['Overall_Discrimination'].mean()
            avg_difficulty = acceptable_items['Difficulty'].mean()

            # --- Store the average parameters ---
            logit_data[factor][measure]['mean_discrimination'] = avg_discrimination
            logit_data[factor][measure]['mean_difficulty'] = avg_difficulty

    prob_df_long = irt_df_long.copy()

    probabilities = []
    for row in prob_df_long.itertuples():
        factor = row.Factor
        measure = row.Measure
        discrimination = logit_data[factor][measure]['mean_discrimination']
        difficulty = logit_data[factor][measure]['mean_difficulty']
        if discrimination is None or difficulty is None:
            print(f"Warning: Missing discrimination or difficulty for factor '{factor}' and measure '{measure}'. Skipping this row.")
            continue
        probability = 1 / (1 + np.exp(-(discrimination * (row.Data - difficulty))))
        probabilities.append(probability)
        
    prob_df_long.drop(columns=['Data'], inplace=True)

    prob_df_long['Data'] = probabilities  # Keep the original Data for reference

    prob_df_long['Source'] = 'prob'

    return prob_df_long

def prep_util_df_long(df_master):
    """
    Compute utility (score - confidence) for each UID/Test/Factor for each source,
    and return as a long-format dataframe.
    """

    # Create empty list to accumulate result rows
    util_rows = []

    # Iterate over each scoring source
    for source in ['ctt', 'irt', 'prob']:
        # Filter score and confidence data for the current source
        df_scor = df_master[(df_master['Source'] == source) & (df_master['Measure'] == 'scor')].reset_index(drop=True)
        df_conf = df_master[(df_master['Source'] == source) & (df_master['Measure'] == 'conf')].reset_index(drop=True)

        # Extract score and confidence arrays
        scores = df_scor['Data'].to_numpy()
        confidences = df_conf['Data'].to_numpy()

        # Compute utility
        utility = scores - confidences

        # Construct new dataframe using original UID/Test/Factor info with utility values
        df_util_chunk = pd.DataFrame({
            'UID': df_scor['UID'],
            'Test': df_scor['Test'],
            'Factor': df_scor['Factor'],
            'Data': utility,
            'Measure': 'util',
            'Source': source
        })

        util_rows.append(df_util_chunk)

    # Combine all utility chunks into final dataframe
    df_util = pd.concat(util_rows, ignore_index=True)

    # Invert all the utility values by multiplying by -1
    df_util['Data'] *= -1

    return df_util

def run_lmm(set_name, data, formula_suffix, covariates):

    lmm_results = {}

    sources = data['Source'].unique().tolist()
    factors = data['Factor'].unique().tolist()
    measures = data['Measure'].unique().tolist()

    # --- NEW: Step 1 - Merge Covariate Data ---
    if covariates:

        # Select only the UID and the requested covariate columns from the master data
        covariate_data = df_data[['UID'] + covariates].drop_duplicates()
        
        # Merge the covariate data into the analysis dataframe
        data = pd.merge(data, covariate_data, on='UID', how='left')

        # --- NEW: Step 2 - Check for Multicollinearity (VIF) ---
        # Select only numeric covariates for the VIF check
        numeric_covariates = data[covariates].select_dtypes(include=np.number)
        
        if not numeric_covariates.empty:
            print(f"\n--- Checking for Multicollinearity in: {', '.join(numeric_covariates.columns)} ---")
            # Add a constant for VIF calculation
            vif_data = pd.concat([numeric_covariates, pd.Series(1, index=numeric_covariates.index, name='const')], axis=1)
            
            for i, col in enumerate(numeric_covariates.columns):
                vif = variance_inflation_factor(vif_data.values, i)
                print(f"VIF for {col}: {vif:.2f}")
                if vif > 5.0:
                    print(f"  -> WARNING: High VIF detected for '{col}'. Results may be unstable.")
            print("----------------------------------------------------")

    base_formula = f"Data ~ (Time + log_Time) * {formula_suffix}"
    
    if covariates:
        # Add the covariates as main effects to the formula
        covariate_string = " + ".join(covariates)
        final_formula = f"{base_formula} + {covariate_string}"
    else:
        final_formula = base_formula

    formulas = {
        "Lin+Log": final_formula,
    }

    # formulas = {
    #     # Your existing models
    #     # "Linear":     f"Data ~ (Time) * {formula_suffix}",
    #     # "Quadratic":  f"Data ~ (Time + Time_sq) * {formula_suffix}",
    #     # "Log":        f"Data ~ (log_Time) * {formula_suffix}",
    #     "Lin+Log":    f"Data ~ (Time + log_Time) * {formula_suffix}",
    #     # "Quad+Log":   f"Data ~ (Time + Time_sq + log_Time) * {formula_suffix}",
    #     # "Spline":     f"Data ~ (bs(Time, df=3)) * {formula_suffix}",
        
    #     # New, theoretically-motivated models
    #     # "Power":      f"Data ~ (I(Time**-0.5)) * {formula_suffix}", # A simple power law approximation
    #     # "Piecewise":  f"Data ~ (Time + Time_post_consolidation) * {formula_suffix}",
    # }

    print(data)
    # input()

    for model_name, formula in formulas.items():

        print(f"Fitting model: {model_name} with formula: {formula}")
        analysis_name = f'src-{"-".join(sources)}_fac-{"-".join(factors)}_typ-{"-".join(measures)}_for-{formula_suffix}_cov-{"-".join(covariates)}_mdl-{model_name}'
        analysis_name = analysis_name.replace(" ", "").replace("*", "_x_")
        model_path = f"analysis/{set_name}/pkl/{analysis_name}.pkl"
        if os.path.exists(model_path) and not RECOMPUTE:
            fit = MixedLMResults.load(model_path)
        else:
            re_term = "~log_Time" if "log" in model_name.lower() else "~Time"
            mdl = smf.mixedlm(
                formula,
                data=data,
                groups=data["UID"],
                re_formula=re_term
            )
            fit = mdl.fit(method=["lbfgs"], reml=False)
            fit.save(model_path)
            # print(fit.summary())
            # input("Press Enter to continue...")

        df_plot = data.copy()
        # df_plot = pd.DataFrame(columns=['UID', 'Time', 'Source', 'Factor', 'Measure', 'Predict', 'Resid'])
        # df_plot['UID'] = data['UID']
        # df_plot['Time'] = data['Time']
        # # df_plot['Time_sq'] = data['Time_sq'] if 'Time_sq' in data else None
        # df_plot['log_Time'] = data['log_Time'] if 'log_Time' in data else None
        # # df_plot['Time_post_consolidation'] = data['Time_post_consolidation'] if 'Time_post_consolidation' in data else None
        # df_plot['Source'] = data['Source']
        # df_plot['Factor'] = data['Factor']
        # df_plot['Measure'] = data['Measure']
        df_plot['Predict'] = fit.predict()
        df_plot['Resid'] = fit.resid

        lmm_results[analysis_name] = {
            "Sources": sources,
            "Factors": factors,
            "Measures": measures,
            "Covariates": covariates,
            "Formula": formula,
            "Model": model_name,
            "Fit": fit,
            "Plot": df_plot,
        }

    return lmm_results

def extract_lmm_summary(fit):
    # Extract fixed effects
    fixed_tbl = fit.summary().tables[1]

    # Handle either SimpleTable or DataFrame directly
    if hasattr(fixed_tbl, 'as_html'):
        fixed_df = pd.read_html(fixed_tbl.as_html(), header=0, index_col=0)[0]
    else:
        fixed_df = fixed_tbl.copy()
        fixed_df.index.name = 'Var'
        fixed_df.reset_index(inplace=True)

    fixed_df = fixed_df.rename(columns={
        'Coef.': 'Coef',
        'Std.Err.': 'SE',
        'z': 'Z',
        'P>|z|': 'P',
        '[0.025': 'CI025',
        '0.975]': 'CI975'
    })

    # Try to extract random effects
    try:
        random_tbl = fit.summary().tables[2]
        if hasattr(random_tbl, 'as_html'):
            random_df = pd.read_html(random_tbl.as_html(), header=0, index_col=0)[0]
        else:
            random_df = random_tbl.copy()
            random_df.index.name = 'var'
            random_df.reset_index(inplace=True)

        random_df = random_df.rename(columns={
            'Coef.': 'Coef',
            'Std.Err.': 'SE'
        })
        random_df['Z'] = None
        random_df['P'] = None
        random_df['CI025'] = None
        random_df['CI975'] = None

        return pd.concat([fixed_df, random_df], ignore_index=True)

    except Exception:
        return fixed_df

def main(set_name):

    try:

        # --- Create our master DataFrame ---
        factors = get_factors(set_name)
        ctt_df_long = prep_ctt_df_long(set_name, factors)
        irt_df_long = prep_irt_df_long(set_name, factors)
        prob_df_long = prep_prob_df_long(set_name, factors, irt_df_long)
        df_master = pd.concat([ctt_df_long, irt_df_long, prob_df_long], ignore_index=True)
        util_df_long = prep_util_df_long(df_master)
        df_master = pd.concat([df_master, util_df_long], ignore_index=True)
        df_master = df_master.sort_values(by=['UID', 'Test', 'Source', 'Factor', 'Measure']).reset_index(drop=True)
        df_master = df_master.merge(
            df_data[['UID', 'Test', 'Time_SVR']],
            on=['UID', 'Test'],
            how='left'
        )
        df_master.rename(columns={'Time_SVR': 'Time'}, inplace=True)
        df_master['Time_sq'] = df_master['Time'] ** 2
        df_master['log_Time']= np.log(df_master['Time'] + 1)
        df_master['Time_post_consolidation'] = np.maximum(0, df_master['Time'] - 24)
        df_master = df_master[['UID', 'Test', 'Time', 'Time_sq', 'log_Time', 'Time_post_consolidation', 'Source', 'Factor', 'Measure', 'Data']]
        # df_master = df_master[['UID', 'Test', 'Time', 'log_Time', 'Source', 'Factor', 'Measure', 'Data']]


        if not os.path.exists(f'analysis/{set_name}'):
            os.makedirs(f'analysis/{set_name}')
        if not os.path.exists(f'analysis/{set_name}/pkl'):
            os.makedirs(f'analysis/{set_name}/pkl')
        df_master.to_csv(f'analysis/{set_name}/df_master.csv', index=False)

        # Get the 'age' and UID columns from df_data
        if 'age' in df_data.columns:
            df_master = df_master.merge(df_data[['UID', 'age']], on='UID', how='left')
        else:
            print("Warning: 'age' column not found in df_data. Covariate analysis will not include age.")

        print(df_master)
        input("Press Enter to continue...")

        all_lmm_results = {}

        # covariates = ['age']
        covariates = []

        for analysis_name, source, measure, formula_interactions, covariates in [

            # # --- Question 1: What is the basic shape of forgetting? ---
            ['1.1_IRT_Scores',    ['prob'], ['scor'], 'Factor', covariates],
            ['1.2_IRT_Confidence',  ['prob'], ['conf'], 'Factor', covariates],
            ['1.3_CTT_Scores',    ['ctt'], ['scor'], 'Factor', covariates],
            ['1.4_CTT_Confidence',  ['ctt'], ['conf'], 'Factor', covariates],


            # # # # --- Question 2: Does IRT change the story vs. CTT? ---
            # ['2.1_CTT_vs_IRT_Scores',      ['ctt', 'prob'], ['scor'], 'Factor * Source', covariates],
            # ['2.2_CTT_vs_IRT_Confidence',  ['ctt', 'prob'], ['conf'], 'Factor * Source', covariates],
            # ['2.3_CTT_vs_IRT_Both',  ['ctt', 'prob'], ['scor', 'conf'], 'Factor * Source', covariates],

            # # # # --- Question 3: What is the relationship between accuracy and confidence? ---
            # ['3.1_CTT_Score_vs_Conf',   ['ctt'], ['scor', 'conf'], 'Factor * Measure', covariates],
            # ['3.2_IRT_Score_vs_Conf',   ['prob'],['scor', 'conf'], 'Factor * Measure', covariates],

            # # # # --- Question 4: Do findings hold for raw theta scores? (Sensitivity Analysis) ---
            ['4.1_IRT_Ability_Scores',      ['irt'], ['scor'], 'Factor', covariates],
            ['4.2_IRT_Ability_Confidence',  ['irt'], ['conf'], 'Factor',  covariates],
            # ['4.3_IRT_Ability_Score_vs_Conf', ['irt'], ['scor', 'conf'], 'Factor * Measure', covariates],

            # # # # --- Question 5: How does utility look? ---
            # ['5.1_CTT_Utility', ['ctt'], ['util'], 'Factor', covariates],
            # ['5.2_IRT_Utility', ['irt'], ['util'], 'Factor', covariates],
            # ['5.3_Prob_Utility', ['prob'], ['util'], 'Factor', covariates],

            # # --- NEW: Question 6: What explains individual differences in utility? ---
            # # ['6.1_Prob_Utility_vs_Age_Gender', ['prob'], ['util'], 'Factor', ['age', 'sex']],
            # ['6.1_Prob_Utility', ['prob'], ['util'], 'Factor',  covariates],
            # ['5.3_Utility_vs_Age', ['prob'], ['util'], 'Factor', covariates],


        ]:
            df_subset = df_master[(df_master['Source'].isin(source)) & (df_master['Measure'].isin(measure))].reset_index(drop=True)
            if df_subset.empty:
                print(f"No data for Source: {source}, Measure: {measure}. Skipping.")
                continue

            all_lmm_results[analysis_name] = run_lmm(
                set_name, 
                df_subset,
                formula_interactions,
                covariates
            )

        return all_lmm_results

    except Exception as e:
        print(f"Error processing {set_name}: {e} \n{traceback.format_exc()}")
        return " "

def select_best_model(all_results):
    """
    Analyzes a dictionary of LMM results to find the most consistently
    best-fitting model across all analyses using three different metrics:
    1. Mean Z-Score of AICs (lower is better)
    2. Mean Ordinal Rank of AICs (lower is better)
    3. Mean Akaike Weight (higher is better)

    Args:
        all_results: A nested dictionary with the structure:
                     {set_name: {analysis_name: {model_name: {'Fit': lmm_results}}}}

    Returns:
        A pandas DataFrame summarizing the performance of each model type.
    """
    
    # Initialize a dictionary to store the performance metrics for each model type
    model_performance = {
        'Linear':    {'z_scores': [], 'ranks': [], 'weights': []},
        'Quadratic': {'z_scores': [], 'ranks': [], 'weights': []},
        'Log':       {'z_scores': [], 'ranks': [], 'weights': []},
        'Lin+Log':   {'z_scores': [], 'ranks': [], 'weights': []},
        'Quad+Log':  {'z_scores': [], 'ranks': [], 'weights': []},
        'Spline':    {'z_scores': [], 'ranks': [], 'weights': []},
        'Power':     {'z_scores': [], 'ranks': [], 'weights': []},
        'Piecewise': {'z_scores': [], 'ranks': [], 'weights': []},
    }

    # --- Step 1: Iterate through each analysis set and calculate metrics ---
    for set_name in all_results:
        for analysis_name in all_results[set_name]:
            
            # --- A. Gather AICs for the current analysis set ---
            aics = []
            for model_name_key in all_results[set_name][analysis_name]:
                model_info = all_results[set_name][analysis_name][model_name_key]
                model_type = model_info['Model']
                aic_value = float(model_info['Fit'].aic)
                aics.append({'model_type': model_type, 'aic': aic_value})
            
            if not aics:
                continue

            # --- B. Calculate Z-Scores ---
            aic_values = np.array([m['aic'] for m in aics])
            mean_aic = np.mean(aic_values)
            std_aic = np.std(aic_values)
            
            # Avoid division by zero if all AICs are identical
            if std_aic > 0:
                z_scores = (aic_values - mean_aic) / std_aic
            else:
                z_scores = np.zeros_like(aic_values)

            for i, model_data in enumerate(aics):
                model_performance[model_data['model_type']]['z_scores'].append(z_scores[i])

            # --- C. Calculate Ordinal Ranks ---
            # Sort models by AIC value (lower is better)
            aics_sorted = sorted(aics, key=lambda x: x['aic'])
            for rank, model_data in enumerate(aics_sorted, 1): # Ranks start at 1
                model_performance[model_data['model_type']]['ranks'].append(rank)

            # --- D. Calculate Akaike Weights ---
            min_aic = aic_values.min()
            # Calculate delta AICs to prevent numerical overflow with exp()
            delta_aics = aic_values - min_aic
            # Calculate the relative likelihood of each model
            relative_likelihoods = np.exp(-0.5 * delta_aics)
            # The sum of likelihoods is the denominator for the weights
            sum_likelihoods = np.sum(relative_likelihoods)
            
            if sum_likelihoods > 0:
                akaike_weights = relative_likelihoods / sum_likelihoods
            else:
                # Handle the rare case where all likelihoods are zero
                akaike_weights = np.zeros_like(aic_values)

            for i, model_data in enumerate(aics):
                model_performance[model_data['model_type']]['weights'].append(akaike_weights[i])

    # --- Step 2: Aggregate the results and create a summary DataFrame ---
    summary_data = []
    for model_type, metrics in model_performance.items():
        if not metrics['z_scores']: # Skip models that were never run
            continue
        summary_data.append({
            'Model Type': model_type,
            'Mean Z-Score': np.mean(metrics['z_scores']),
            'Mean Rank': np.mean(metrics['ranks']),
            'Mean Akaike Weight': np.mean(metrics['weights']),
            'N Runs': len(metrics['z_scores'])
        })
        
    summary_df = pd.DataFrame(summary_data)
    
    # --- Step 3: Print the formatted results ---
    print("\n--- Comprehensive Model Selection Summary ---")
    print("Lower Z-Score/Rank is better. Higher Akaike Weight is better.\n")
    
    # Sort by each metric to easily see the winner
    print("--- Sorted by Mean Z-Score (Lower is Better) ---")
    print(summary_df.sort_values('Mean Z-Score').to_string(index=False))
    
    print("\n--- Sorted by Mean Rank (Lower is Better) ---")
    print(summary_df.sort_values('Mean Rank').to_string(index=False))
    
    print("\n--- Sorted by Mean Akaike Weight (Higher is Better) ---")
    print(summary_df.sort_values('Mean Akaike Weight', ascending=False).to_string(index=False))
    
    # --- Step 4: Determine and announce the overall winner ---
    z_winner = summary_df.loc[summary_df['Mean Z-Score'].idxmin()]
    rank_winner = summary_df.loc[summary_df['Mean Rank'].idxmin()]
    weight_winner = summary_df.loc[summary_df['Mean Akaike Weight'].idxmax()]
    
    print("\n--- Conclusion ---")
    print(f"Best Model by Z-Score:       {z_winner['Model Type']}")
    print(f"Best Model by Rank:          {rank_winner['Model Type']}")
    print(f"Best Model by Akaike Weight: {weight_winner['Model Type']}")

    # Check for consensus
    if z_winner['Model Type'] == rank_winner['Model Type'] == weight_winner['Model Type']:
        print(f"\n>> All three methods converge on the '{z_winner['Model Type']}' model as the best overall fit. <<")
    else:
        print("\n>> The methods do not converge on a single best model. Careful consideration is needed. <<")
    
    summary_df.to_csv('analysis/model_selection_summary.csv', index=False)

    return z_winner['Model Type']

if __name__ == "__main__":

    all_results = {}

    for set_name in os.listdir('results'):

        if set_name in [
            # 'All',
            # 'All by Domain',
            # 'All by Paradigm',
            # 'All Items',
            # 'Interaction vs Observation',
            'Items by Congruence',
            # 'Items by Domain',
            # 'Items by Paradigm',
            # 'Items Up v Down',
            # 'Portraits vs Landscapes'
        ]:
            
            all_results[set_name] = main(set_name)

        

    results_df_template = pd.DataFrame(columns=['Set', 'Analysis', 'Model', 'AIC', 'Var', 'Coef', 'SE', 'Z', 'P', 'CI025', 'CI975'])
    final_results_df = results_df_template.copy()

    # best_model = select_best_model(all_results)
    # input("Press Enter to continue...")

    for set_name in all_results:

        # if set_name in [
        #     # 'All',
        #     # 'All by Domain',
        #     # 'All by Paradigm',
        #     # 'All Items',
        #     # 'Interaction vs Observation',
            # 'Items by Congruence',
        #     'Items by Domain',
        #     # 'Items by Paradigm',
        #     'Items Up v Down',
        #     # 'Portraits vs Landscapes'
        # ]:
        #     continue

        set_results_df = results_df_template.copy()
        try:
            for analysis_name in all_results[set_name]:
                print(f"Processing set: {set_name}, analysis: {analysis_name}")
        
                aics = {}
                for model_name in all_results[set_name][analysis_name]:
                    aics[model_name] = all_results[set_name][analysis_name][model_name]['Fit'].aic
                    print(f"Model: {model_name}, AIC: {aics[model_name]}")

                best_model = min(aics, key=aics.get)

                if best_model:
                    temp_results = all_results[set_name][analysis_name][best_model]
                    fit = temp_results['Fit']
                    print(fit.summary())
                    
                    results_df = extract_lmm_summary(fit)
                    print(results_df)
                    # input("Press Enter to continue...")
                    results_df['Analysis'] = analysis_name
                    results_df['Model'] = temp_results['Model']
                    results_df['Set'] = set_name
                    results_df['AIC'] = fit.aic
                    
                    set_results_df = pd.concat([set_results_df, results_df], ignore_index=True)

                    print(temp_results['Plot'])
                    # temp_results['Plot'].to_clipboard(index=False)
                    plots.plot_analysis(
                        lmm_results=fit,
                        df_data=temp_results['Plot'],
                        title=f"{set_name} - {analysis_name} - {temp_results['Model']}",
                        save_path=f"analysis/{set_name}/{analysis_name} - {temp_results['Model']}.png",
                    )

        except Exception as e:
            print(f"Error processing set {set_name} for analysis {analysis_name}: {e}")
            traceback.print_exc()
            continue

        print(set_results_df)

        # set_results_df.to_csv(f'analysis/{set_name}/results.csv', index=False, float_format='%.4f')
        # final_results_df = pd.concat([final_results_df, set_results_df], ignore_index=True)

    final_results_df.to_csv(f'analysis/final_results.csv', index=False)