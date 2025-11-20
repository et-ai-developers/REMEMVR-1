# utility.py
import pandas as pd
import numpy as np
import os
from statsmodels.regression.mixed_linear_model import MixedLMResults
import statsmodels.formula.api as smf
import sys
import traceback
from params import ANALYSIS_LIST
import plots
from box import Box
import json

# List all the folder names in the results # directory
MODEL_TYPE = 'Lin+Log'
MIN_DISCRIM_THRESHOLD = 0.25
MAX_DISCRIM_THRESHOLD = 4
dfData = pd.read_csv('dfData.csv')

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
    # Add the Type column
    df_conf['Type'] = 'conf'


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
    df_scor['Type'] = 'scor'

    # Combine DataFrames
    df_long = pd.concat([df_conf, df_scor], ignore_index=True)
    # day_map = {1: 0, 2: 1, 3: 3, 4: 6}
    # df_long['Days']    = df_long['Test'].map(day_map)
    # df_long['Days_sq'] = df_long['Days'] ** 2
    # df_long['log_Days']= np.log(df_long['Days'] + 1)
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
    df_conf['Type'] = 'conf'

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
    df_scor['Type'] = 'scor'

    # Combine DataFrames
    df_long = pd.concat([df_conf, df_scor], ignore_index=True)
    # day_map = {1: 0, 2: 1, 3: 3, 4: 6}
    # df_long['Days']    = df_long['Test'].map(day_map)
    # df_long['Days_sq'] = df_long['Days'] ** 2
    # df_long['log_Days']= np.log(df_long['Days'] + 1)

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

    for outcome_type in ['conf', 'scor']:
        if outcome_type == 'conf':
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
            logit_data[factor][outcome_type]['mean_discrimination'] = avg_discrimination
            logit_data[factor][outcome_type]['mean_difficulty'] = avg_difficulty

    prob_df_long = irt_df_long.copy()

    # print("prob_df_long:\n", prob_df_long)
    # input("Press Enter to continue...")

    probabilities = []
    for row in prob_df_long.itertuples():
        factor = row.Factor
        outcome_type = row.Type
        discrimination = logit_data[factor][outcome_type]['mean_discrimination']
        difficulty = logit_data[factor][outcome_type]['mean_difficulty']
        if discrimination is None or difficulty is None:
            print(f"Warning: Missing discrimination or difficulty for factor '{factor}' and outcome type '{outcome_type}'. Skipping this row.")
            continue
        probability = 1 / (1 + np.exp(-(discrimination * (row.Data - difficulty))))
        probabilities.append(probability)
        

    # prob_df_long.loc[:, 'Probability'] = 1 / (1 + np.exp(-(logit_data[factor][outcome_type]['mean_discrimination'] * (irt_df_long['Data'] - logit_data[factor][outcome_type]['mean_difficulty']))))
    # Remove the 'Data' column as it is not needed in the final DataFrame
    prob_df_long.drop(columns=['Data'], inplace=True)
    # Rename the Probability column to 'Data'
    # prob_df_long.rename(columns={'Probability': 'Data'}, inplace=True)
    prob_df_long['Data'] = probabilities  # Keep the original Data for reference

    # print("prob_df_long:\n", prob_df_long)
    # input("Press Enter to continue...")


    prob_df_long['Source'] = 'prob'

    return prob_df_long

def compute_utility(name, df_long):

    
    df_util = df_long.pivot(index=['UID', 'Test', 'Source', 'Factor'],
                   columns='Type',
                   values='Data').reset_index()
    df_util.rename(columns={'conf': 'Pc'}, inplace=True)
    df_util.rename(columns={'scor': 'Ps'}, inplace=True)

    # Calculate the utility ORIGINAL
    # df_util['Utility'] = (df_util['Ps'] * df_util['Pc']) - ((1 - df_util['Ps']) * df_util['Pc'])  
    
    # Calculate the utility
    # df_util['Utility'] = (2 * df_util['Ps'] - 1) * df_util['Pc']  # Base formula

    # --- ALTERNATIVES BELOW ---

    # 1. Add nonlinear confidence correction: boosts confident beliefs (positive or negative)
    # lambda_val = 0.2
    # df_util['Utility'] = (2 * df_util['Ps'] - 1) * df_util['Pc'] + lambda_val * (df_util['Pc'] - 0.5)**3

    # 2. Apply a sigmoid-like transformation: spreads out values, suppresses zero peak
    alpha = 2
    df_util['Utility'] = np.tanh((2 * df_util['Ps'] - 1) * df_util['Pc'] * alpha)

    # 3. Weight by belief strength (how far Ps is from 0.5): emphasizes certainty
    # beta = 1
    # df_util['Utility'] = (2 * df_util['Ps'] - 1) * df_util['Pc'] * np.abs(df_util['Ps'] - 0.5) ** beta

    # 4. Shift utility baseline with a fixed offset
    # delta = 0.1
    # df_util['Utility'] = (2 * df_util['Ps'] - 1) * df_util['Pc'] + delta


    day_map = {1: 0, 2: 1, 3: 3, 4: 6}
    df_util['Days']    = df_util['Test'].map(day_map)
    df_util['Days_sq'] = df_util['Days'] ** 2
    df_util['log_Days']= np.log(df_util['Days'] + 1)

    # Remove the Factor column
    # if 'Factor' in df_util.columns:
    #     df_util.drop(columns=['Factor'], inplace=True)

    # df_util.rename(columns={'Source': 'Factor'}, inplace=True)

    # df_util = df_util[df_util['Source'] == 'prob']

    formulas = {
        "Linear":      "Utility ~ Days * Source * Factor",
        "Quadratic":   "Utility ~ (Days + Days_sq) * Source * Factor",
        "Log":         "Utility ~ (log_Days) * Source * Factor",
        "Lin+Log":     "Utility ~ (Days + log_Days) * Source * Factor",
        "Quad+Log":    "Utility ~ (Days + Days_sq + log_Days) * Source * Factor",
        "Spline":      "Utility ~ bs(Days, df=3) * Source * Factor"
    }

    for model_name, formula in formulas.items():

        print(f"Fitting model: {model_name} with formula: {formula}")
            
        re_term = "~log_Days" if "log" in model_name.lower() else "~Days"
        mdl = smf.mixedlm(
            formula,
            data=df_util,
            groups=df_util["UID"],
            re_formula=re_term
        )
        fit = mdl.fit(method=["lbfgs"], reml=False, warn_convergence=False)

        # df_long.to_clipboard()
        # input("Data copied to clipboard. Press Enter to continue...")

        # # Put the model residuals into the clipboard including the UID
        # fit.resid.to_clipboard()
        # input("Model fitted. Residuals copied to clipboard. Press Enter to continue...")

        plots.plot_utility(
            lmm_results= fit,
            df_long= df_util,
            save_path= f"utility/plots/{name}_{model_name}_utility.png",
            params= Box(UTIL_PLOT_PARAMS),
            colors= COLORS_UTIL
        )

    # input()

def main(name):

    try:

        # --- Create our master DataFrame ---
        factors = get_factors(name)
        ctt_df_long = prep_ctt_df_long(name, factors)
        irt_df_long = prep_irt_df_long(name, factors)
        prob_df_long = prep_prob_df_long(name, factors, irt_df_long)
        df_master = pd.concat([ctt_df_long, irt_df_long, prob_df_long], ignore_index=True)
        df_master = df_master.sort_values(by=['UID', 'Test', 'Source', 'Factor', 'Type']).reset_index(drop=True)
        df_master = df_master[['UID', 'Test', 'Source', 'Factor', 'Type', 'Data']]
        day_map = {1: 0, 2: 1, 3: 3, 4: 6}
        df_master['Days']    = df_master['Test'].map(day_map)
        df_master['Days_sq'] = df_master['Days'] ** 2
        df_master['log_Days']= np.log(df_master['Days'] + 1)

        # compute_utility(name, df_master[df_master['Source'] != 'irt'])

        # Drop any rows where Source is 'irt' and reset the index
        df_master = df_master[df_master['Source'] != 'irt']
        df_master = df_master[df_master['Source'] != 'ctt']
        # df_master = df_master[df_master['Type'] != 'scor']
        print(df_master)
        df_master.reset_index(drop=True, inplace=True)

        print("n_sources:", df_master['Source'].nunique())
        print("n_factors:", df_master['Factor'].nunique())
        print("n_types:", df_master['Type'].nunique())

        results = {}

        for m, t in (('Model 1', 'Type'), ('Model 2', 'Type')):

            formulas = {
                # "Linear":      f"Data ~ (Days) * Source * {t}",
                # "Quadratic":   f"Data ~ (Days + Days_sq) * Source * {t}",
                # "Log":         f"Data ~ (log_Days) * Source * {t}",
                "Lin+Log":     f"Data ~ (Days + log_Days) * Factor * Type",
                # "Quad+Log":    f"Data ~ (Days + Days_sq + log_Days) * Source * {t}",
                # "Spline":      f"Data ~ (bs(Days, df=3)) * Source * {t}"
                # "Linear":       f"Data ~ Days * Factor",
            }

            
            # models = {}
            # summaries = {}
            # aics   = {}
            for model_name, formula in formulas.items():

                print(f"Fitting model: {model_name} with formula: {formula}")
                model_path = f"utility\pkl\{name}_{model_name}_{t}.pkl"
                # if os.path.exists(model_path):        
                #     fit = MixedLMResults.load(model_path)
                # else:
                    
                re_term = "~log_Days" if "log" in model_name.lower() else "~Days"
                mdl = smf.mixedlm(
                    formula,
                    data=df_master,
                    groups=df_master["UID"],
                    re_formula=re_term
                )
                fit = mdl.fit(method=["lbfgs"], reml=False, warn_convergence=False)
                fit.save(model_path)

                results[model_name] = {
                    "Formula": formula,
                    "Sources": df_master['Source'].unique().tolist(),
                    "Factors": df_master['Factor'].unique().tolist(),
                    "Types": df_master['Type'].unique().tolist(),
                    # "Analysis": m,
                    
                    "Fit": fit,
                }

                # models[model_name] = fit
                # aics[model_name] = fit.aic
                # summaries[model_name] = f"\n\n{m}\nName: {name}\nSources: {df_master['Source'].unique().tolist()}\nFactors: {df_master['Factor'].unique().tolist()}\nTypes: {df_master['Type'].unique().tolist()}\nModel: {model_name}\nFormula:\n{formula}\nAIC: {fit.aic}\nSummary:\n{fit.summary()}"

            # best_model = min(aics, key=aics.get)
            # results.append(summaries[best_model])

        return results
    
    except Exception as e:
        print(f"Error processing {name}: {e} \n{traceback.format_exc()}")
        return " "

if __name__ == "__main__":
    all_results = {}
    for name in os.listdir('results'):
        if name == 'All':
            continue
        all_results[name] = main(name)
        break
    
    for name in all_results:
        for model_name in all_results[name]:
            temp_results = all_results[name][model_name]
            summary = temp_results['Fit'].summary()
            # Delete the Fit object to save memory
            del temp_results['Fit']

            print(json.dumps(temp_results, indent=4))
            print(summary)