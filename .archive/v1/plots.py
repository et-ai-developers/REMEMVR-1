# plots.py

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy.stats as stats
import patsy # Required for creating design matrices to calculate CIs
import sys
from matplotlib.lines import Line2D # Needed for custom legend

from torch import sub

RESIDUAL_OFFSET_DISTANCE = .03
RESIDUAL_SCATTER_POINT_ALPHA = 0.2
MEAN_CI_ALPHA = 0.2
DIFF_HIST_ALPHA = 0.5
CTT_LINE_STYLE = 'solid'
IRT_LINE_STYLE = 'dashed'
PROB_LINE_STYLE = 'dotted'
UTIL_LINE_STYLE = 'dashdot'

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


def save_or_show_plot(fig, save_path=None, dpi=300):
    """Helper function to either save the plot to a file or show it interactively."""
    if save_path:
        # Saves the figure with high resolution and a tight bounding box
        fig.savefig(save_path, dpi=dpi, bbox_inches='tight')
        plt.close(fig) # Close the figure to free up memory
    else:
        plt.show()



def get_offsets(num_factors):
    """
    Returns a list of offsets based on the number of factors.
    This is used to adjust the x-coordinates of residuals in plots.
    """
    if num_factors == 1:
        return [0]  # No offset for single factor
    elif num_factors == 2:
        return [-RESIDUAL_OFFSET_DISTANCE, RESIDUAL_OFFSET_DISTANCE]
    elif num_factors == 3:
        return [-2 * RESIDUAL_OFFSET_DISTANCE, 0, 2 * RESIDUAL_OFFSET_DISTANCE]
    elif num_factors == 4:
        return [-1.5 * RESIDUAL_OFFSET_DISTANCE, -0.5 * RESIDUAL_OFFSET_DISTANCE, 0.5 * RESIDUAL_OFFSET_DISTANCE, 1.5 * RESIDUAL_OFFSET_DISTANCE]
    elif num_factors == 5:
        return [-2 * RESIDUAL_OFFSET_DISTANCE, -1 * RESIDUAL_OFFSET_DISTANCE, 0, 1 * RESIDUAL_OFFSET_DISTANCE, 2 * RESIDUAL_OFFSET_DISTANCE]
    elif num_factors == 6:
        return [-2.5 * RESIDUAL_OFFSET_DISTANCE, -1.5 * RESIDUAL_OFFSET_DISTANCE, -0.5 * RESIDUAL_OFFSET_DISTANCE, 0.5 * RESIDUAL_OFFSET_DISTANCE, 1.5 * RESIDUAL_OFFSET_DISTANCE, 2.5 * RESIDUAL_OFFSET_DISTANCE]
    else:
        raise ValueError("Unsupported number of factors: {}".format(num_factors))

# --- Other plotting functions remain the same ---

def plot_ctt_regression(
        lmm_results: pd.DataFrame, 
        df_long: pd.DataFrame,
        save_path: str,
        params: dict,
        colors: list,
    ):
    """
    Plots the model-predicted regression lines (in terms of theta) with 95% confidence intervals.
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    day_range = np.linspace(df_long['Days'].min(), df_long['Days'].max(), 100)
    
    is_multi_factor = 'Factor' in df_long.columns and df_long['Factor'].nunique() > 1
    factors = df_long['Factor'].unique()
    
    pred_grid = pd.DataFrame([(day, factor) for factor in factors for day in day_range], columns=['Days', 'Factor'])
    
    model_terms = lmm_results.fe_params.index
    if any('Days_sq' in term for term in model_terms): pred_grid['Days_sq'] = pred_grid['Days'] ** 2
    if any('log_Days' in term for term in model_terms): pred_grid['log_Days'] = np.log(pred_grid['Days'] + 1)
        
    formula_rhs = lmm_results.model.formula.split('~')[1].strip()
    design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
    
    pred_grid['mean'] = lmm_results.predict(pred_grid)
    fe_cov = lmm_results.cov_params().loc[lmm_results.fe_params.index, lmm_results.fe_params.index]
    design_matrix = design_matrix[fe_cov.columns]
    
    pred_var = np.sum((design_matrix @ fe_cov) * design_matrix, axis=1)
    pred_se = np.sqrt(pred_var)
    pred_grid['mean_ci_lower'] = pred_grid['mean'] - 1.96 * pred_se
    pred_grid['mean_ci_upper'] = pred_grid['mean'] + 1.96 * pred_se
    
    df_temp = df_long.copy()
    df_temp['Residual'] = lmm_results.resid

    # Determine which covariates are in the model
    use_sq = any('Days_sq' in term for term in lmm_results.fe_params.index)
    use_log = any('log_Days' in term for term in lmm_results.fe_params.index)

    offsets = get_offsets(len(factors))

    # For each factor, plot the scattered residuals
    for i, factor in enumerate(factors):
        sub = df_temp[df_temp['Factor'] == factor] if is_multi_factor else df_temp
        x_vals = []
        y_vals = []

        for day in [0, 1, 3, 6]:
            row = {'Factor': factor, 'Days': day}
            if use_sq: row['Days_sq'] = day**2
            if use_log: row['log_Days'] = np.log(day + 1)
            mu = lmm_results.predict(pd.DataFrame([row]))[0]
            for uid in sub['UID'].unique():
                # Get the mean residual for this UID and day
                mean_residual = sub[(sub['UID'] == uid) & (sub['Days'] == day)]['Residual'].mean()
                if not np.isnan(mean_residual):
                    x_vals.append(day + offsets[i])
                    y_vals.append(mean_residual + mu)

        ax.scatter(
            x_vals,
            y_vals,
            color=colors[i],
            alpha=RESIDUAL_SCATTER_POINT_ALPHA,
            s=10
        )

    # --- Plot the main LMM trajectory with confidence intervals ---

    for i, factor in enumerate(factors):
        factor_df = pred_grid[pred_grid['Factor'] == factor]
        ax.plot(factor_df['Days'], factor_df['mean'], color=colors[i], linewidth=2.5, label=factor, linestyle=CTT_LINE_STYLE)
        ax.fill_between(factor_df['Days'], factor_df['mean_ci_lower'], factor_df['mean_ci_upper'], color=colors[i], alpha=MEAN_CI_ALPHA)

    ax.set_xlabel(params.x_axis.label)
    ax.set_ylabel(params.y_axis.label)
    ax.set_title(f"{save_path}\n{params.title}\n")

    if params.y_axis.range:
        ax.set_ylim(bottom=params.y_axis.range[0], top=params.y_axis.range[1])

    if params.legend.show:
        ax.legend(loc=params.legend.location, title=params.legend.title, fontsize=params.legend.fontsize, framealpha=params.legend.framealpha)

    ax.grid(True, linestyle='--', alpha=0.6)
    
    save_or_show_plot(fig, save_path=save_path, dpi=params.output.dpi)

def plot_item_difficulty(
    item_params_df: pd.DataFrame, 
    save_path: str,
    params: dict,
    colors: list,
):
    """
    Plots overlapping histograms of item difficulties for each factor.
    
    This version uses a fixed range of -5 to +5 with a bin width of 0.25.
    Items with difficulties outside this range are collected into two "overflow"
    bins at the extremes of the plot for better visualization.
    """
    if 'Difficulty' not in item_params_df.columns:
        return

    fig, ax = plt.subplots(figsize=(14, 7))

    # --- 1. Define the fixed histogram bins and plot range ---
    BIN_WIDTH = 0.25
    X_MIN, X_MAX = -5, 5
    
    # Create bins for the central distribution from -5 to +5
    central_bins = np.arange(X_MIN, X_MAX + BIN_WIDTH, BIN_WIDTH)
    
    # Define positions for the extreme overflow bins
    extreme_low_pos = X_MIN - BIN_WIDTH * 2
    extreme_high_pos = X_MAX + BIN_WIDTH

    # Dynamically find the discrimination factor columns
    discrim_cols = [col for col in item_params_df.columns if col.startswith('Discrim_')]
    group_names = [col.replace('Discrim_', '') for col in discrim_cols]
    
    # --- 2. Loop through each factor and plot its distribution ---
    for i, (group, discrim_col) in enumerate(zip(group_names, discrim_cols)):
        # Select items that are supposed to load on this factor
        group_items = item_params_df[item_params_df[discrim_col] > 0]
        if group_items.empty:
            continue
        
        difficulties = group_items['Difficulty'].dropna()
        color = colors[i]

        # --- 3. Partition the data into central and extreme values ---
        central_difficulties = difficulties[(difficulties >= X_MIN) & (difficulties <= X_MAX)]
        extreme_low_count = np.sum(difficulties < X_MIN)
        extreme_high_count = np.sum(difficulties > X_MAX)

        # --- 4. Manually calculate and plot the histogram bars ---
        
        # A. Plot the central distribution
        if not central_difficulties.empty:
            counts, _ = np.histogram(central_difficulties, bins=central_bins)
            # Use the center of the bins for the x-position of the bars
            bin_centers = central_bins[:-1] + BIN_WIDTH / 2
            ax.bar(bin_centers, counts, width=BIN_WIDTH, color=color, alpha=0.6, 
                   edgecolor='white', label=f'{group} (n={len(difficulties)})')

        # B. Plot the extreme "overflow" bins if they contain any items
        if extreme_low_count > 0:
            ax.bar(extreme_low_pos, extreme_low_count, width=BIN_WIDTH * 1.5, 
                   color=color, alpha=0.6, edgecolor='white')
        if extreme_high_count > 0:
            ax.bar(extreme_high_pos, extreme_high_count, width=BIN_WIDTH * 1.5, 
                   color=color, alpha=0.6, edgecolor='white')

        # --- 5. Overlay the normal distribution curve for the CENTRAL data ---
        if not central_difficulties.empty:
            mu, std = stats.norm.fit(central_difficulties)
            x_curve = np.linspace(X_MIN, X_MAX, 200)
            p_curve = stats.norm.pdf(x_curve, mu, std)
            
            # Scale the PDF to match the histogram
            scaled_p = p_curve * len(central_difficulties) * BIN_WIDTH
            ax.plot(x_curve, scaled_p, color=color, linewidth=2.5)

    # --- 6. Final plot formatting ---
    ax.set_title(f"{save_path}\n{params['title']}\n", fontsize=16)
    ax.set_xlabel(params['x_axis']['label'], fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)

    # Set custom x-axis ticks to label the overflow bins
    tick_positions = [extreme_low_pos] + list(np.arange(X_MIN, X_MAX + 1, 1)) + [extreme_high_pos]
    tick_labels = [f'< {X_MIN}'] + [str(int(p)) for p in np.arange(X_MIN, X_MAX + 1, 1)] + [f'> {X_MAX}']
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels)
    ax.set_xlim(X_MIN - BIN_WIDTH * 4, X_MAX + BIN_WIDTH * 3)

    if params['legend']['show']:
        ax.legend(loc=params['legend']['location'], title=params['legend']['title'], 
                  fontsize=params['legend']['fontsize'], framealpha=params['legend']['framealpha'])

    ax.grid(True, axis='y', linestyle='--', alpha=0.6)
    
    save_or_show_plot(fig, save_path=save_path, dpi=params['output']['dpi'])

def plot_lmm_diagnostics(
        lmm_results: pd.DataFrame,
        save_path: str,
        params: dict,
    ):

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f"{save_path}\n{params.title}\n", fontsize=16)
    
    fitted, residuals = lmm_results.fittedvalues, lmm_results.resid
    std_resid = residuals / np.sqrt(lmm_results.scale)

    axes[0, 0].scatter(fitted, residuals, alpha=0.5, edgecolors='k', lw=0.5)
    axes[0, 0].axhline(0, color='red', linestyle='--'); axes[0, 0].set_title('Residuals vs. Fitted')
    axes[0, 0].set_xlabel('Fitted values'); axes[0, 0].set_ylabel('Residuals')

    axes[0, 1].hist(residuals, bins='auto', edgecolor='black', alpha=0.7)
    axes[0, 1].set_title('Histogram of Residuals'); axes[0, 1].set_xlabel('Residuals')

    stats.probplot(residuals, dist="norm", plot=axes[1, 0])
    axes[1, 0].get_lines()[0].set_markerfacecolor('C0'); axes[1, 0].get_lines()[0].set_markeredgecolor('C0')
    axes[1, 0].get_lines()[1].set_color('red'); axes[1, 0].set_title('Normal Q-Q Plot')

    axes[1, 1].scatter(fitted, np.sqrt(np.abs(std_resid)), alpha=0.5, edgecolors='k', lw=0.5)
    axes[1, 1].set_title('Scale-Location Plot'); axes[1, 1].set_xlabel('Fitted values')
    axes[1, 1].set_ylabel('√|Standardized Residuals|')

    fig.tight_layout(rect=[0, 0.03, 1, 0.95])
    save_or_show_plot(fig, save_path=save_path, dpi=params.output.dpi)

def plot_lmm_trajectory(
        lmm_results: pd.DataFrame, 
        df_long: pd.DataFrame,
        save_path: str,
        params: dict,
        colors: list
    ):
    """
    Plots the model-predicted regression lines (in terms of theta) with 95% confidence intervals.
    """
    
    fig, ax = plt.subplots(figsize=(10, 6))
    day_range = np.linspace(df_long['Days'].min(), df_long['Days'].max(), 100)
    
    is_multi_factor = 'Factor' in df_long.columns and df_long['Factor'].nunique() > 1
    factors = df_long['Factor'].unique()
    
    pred_grid = pd.DataFrame([(day, factor) for factor in factors for day in day_range], columns=['Days', 'Factor'])
    
    model_terms = lmm_results.fe_params.index
    if any('Days_sq' in term for term in model_terms): pred_grid['Days_sq'] = pred_grid['Days'] ** 2
    if any('log_Days' in term for term in model_terms): pred_grid['log_Days'] = np.log(pred_grid['Days'] + 1)
        
    formula_rhs = lmm_results.model.formula.split('~')[1].strip()
    design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
    
    pred_grid['mean'] = lmm_results.predict(pred_grid)
    fe_cov = lmm_results.cov_params().loc[lmm_results.fe_params.index, lmm_results.fe_params.index]
    design_matrix = design_matrix[fe_cov.columns]
    
    pred_var = np.sum((design_matrix @ fe_cov) * design_matrix, axis=1)
    pred_se = np.sqrt(pred_var)
    pred_grid['mean_ci_lower'] = pred_grid['mean'] - 1.96 * pred_se
    pred_grid['mean_ci_upper'] = pred_grid['mean'] + 1.96 * pred_se

    # Copy residuals
    day_positions = sorted(df_long['Days'].unique())
    df_temp = df_long.copy()
    df_temp['Residual'] = lmm_results.resid

    # Determine which covariates are in the model
    use_sq = any('Days_sq' in term for term in lmm_results.fe_params.index)
    use_log = any('log_Days' in term for term in lmm_results.fe_params.index)

    offsets = get_offsets(len(factors))

    # For each factor, plot violin of residuals + model mean at each discrete day
    for i, factor in enumerate(factors):
        sub = df_temp[df_temp['Factor'] == factor] if is_multi_factor else df_temp
        means_at = []
        for d in day_positions:
            # build a one-row DataFrame to predict mean
            row = {'Factor': factor, 'Days': d}
            if use_sq: row['Days_sq'] = d**2
            if use_log: row['log_Days'] = np.log(d + 1)
            mu = lmm_results.predict(pd.DataFrame([row]))[0]
            means_at.append(mu)

        # scatter actual residual+mean
        for d, mu in zip(day_positions, means_at):
            ys = sub.loc[sub['Days'] == d, 'Residual'] + mu
            x = sub.loc[sub['Days'] == d, 'Days'].values + offsets[i]

            ax.scatter(
                x,
                ys,
                color=colors[i],
                alpha=RESIDUAL_SCATTER_POINT_ALPHA,
                s=10
            )

    # --- Plot the main LMM trajectory with confidence intervals ---

    for i, factor in enumerate(factors):
        factor_df = pred_grid[pred_grid['Factor'] == factor]
        ax.plot(factor_df['Days'], factor_df['mean'], color=colors[i], linewidth=2.5, label=factor, linestyle=IRT_LINE_STYLE)
        ax.fill_between(factor_df['Days'], factor_df['mean_ci_lower'], factor_df['mean_ci_upper'], color=colors[i], alpha=MEAN_CI_ALPHA)

    ax.set_xlabel(params.x_axis.label)
    ax.set_ylabel(params.y_axis.label)
    ax.set_title(f"{save_path}\n{params.title}\n")

    if params.y_axis.range:
        ax.set_ylim(bottom=params.y_axis.range[0], top=params.y_axis.range[1])

    if params.legend.show:
        ax.legend(loc=params.legend.location, title=params.legend.title, fontsize=params.legend.fontsize, framealpha=params.legend.framealpha)

    ax.grid(True, linestyle='--', alpha=0.6)
    
    save_or_show_plot(fig, save_path=save_path, dpi=params.output.dpi)

def plot_predicted_probabilities(
    lmm_results,
    df_items,
    df_long,
    groups,
    save_path: str,
    params: dict,
    colors: list,
    min_discrim_threshold: float = 0.25,
    max_discrim_threshold: float = 4.0
):
    """
    Plots the model-predicted probability of a correct response for an average person.
    The shaded area represents the 95% confidence interval for the mean predicted trend,
    showing our confidence in the model's estimate.
    """

    def plot_individual_deviations(
        df_lmm_long, 
        df_items, 
        groups, 
        lmm_results, 
        ax=None,
        colors=None,
        # Pass the discrimination thresholds to the function
        min_discrim_threshold=0.5,
        max_discrim_threshold=4.0
    ):
        """
        Overlays violins, scattered dots, and spaghetti lines representing individual trajectories.
        This version filters items to match the main trend line, using only items
        with acceptable discrimination parameters.
        """
        
        # Create a copy of the data to avoid modifying the original DataFrame
        df = df_lmm_long.copy()

        offsets = get_offsets(len(groups))
        
        color_count = 0
        for factor in groups:
            # --- Filter items for the current factor ---
            discrim_col_name = f'Discrim_{factor}'
            if discrim_col_name not in df_items.columns:
                discrim_cols = [c for c in df_items.columns if c.startswith('Discrim_')]
                discrim_col_name = discrim_cols[0] if len(discrim_cols) == 1 else None

            if discrim_col_name:
                acceptable_items = df_items[
                    (df_items[discrim_col_name] >= min_discrim_threshold) & 
                    (df_items[discrim_col_name] <= max_discrim_threshold)
                ]
            else:
                acceptable_items = df_items

            if acceptable_items.empty:
                color_count += 1
                continue

            # --- Calculate average parameters from ONLY the filtered set ---
            avg_discrimination = acceptable_items['Overall_Discrimination'].mean()
            avg_difficulty = acceptable_items['Difficulty'].mean()

            # Get the subset of data for the current factor
            sub = df[df['Factor']==factor].copy()
            
            # Calculate the probability for each individual data point
            sub.loc[:, 'P_i'] = 1 / (1 + np.exp(-(avg_discrimination * (sub['Ability'] - avg_difficulty))))

            sub.to_csv(f"{save_path}_factor_{factor}_filtered.csv", index=False)

            # --- Pre-calculate jittered x-coordinates for all points ---
            jittered_coords = []
            days = sorted(sub['Days'].unique())
            for d in days:
                day_data = sub.loc[sub['Days'] == d]
                y = day_data['P_i']
                if y.empty or y.isna().all():
                    jittered_coords.append(pd.Series([np.nan] * len(day_data), index=day_data.index))
                    continue
                
                x_jitter = abs(y - y.mean())
                x_jitter = (x_jitter.max() - x_jitter) if x_jitter.max() > 0 else x_jitter
                x_jitter = x_jitter + np.random.normal(loc=0, scale=x_jitter + 1e-9, size=len(x_jitter))
                x_jitter = x_jitter * 0.1
                x_jitter = (x_jitter - x_jitter.mean()) + d
                jittered_coords.append(x_jitter)
            
            if jittered_coords:
                sub['x_jittered'] = pd.concat(jittered_coords)
            else:
                color_count += 1
                continue

            # --- Plotting ---

            # 4. Plot the scattered dots
            ax.scatter(sub['Days'] + offsets[color_count], sub['P_i'], s=18, alpha=RESIDUAL_SCATTER_POINT_ALPHA, color=colors[color_count], edgecolor='none')
            
            color_count += 1
            
        return ax

    # --- Main function starts here ---
    fig, ax = plt.subplots(figsize=(10, 6))
    day_range = np.linspace(df_long['Days'].min(), df_long['Days'].max(), 100)
    factors = df_long['Factor'].unique()
    
    # Build pred_grid for LMM prediction
    pred_grid = pd.DataFrame([
        (d, f) for f in factors for d in day_range
    ], columns=['Days', 'Factor'])
    
    # Add any extra terms your model needs
    terms = lmm_results.fe_params.index
    if any('Days_sq' in t for t in terms):
        pred_grid['Days_sq'] = pred_grid['Days']**2
    if any('log_Days' in t for t in terms):
        pred_grid['log_Days'] = np.log(pred_grid['Days'] + 1)

    # Predict mean theta
    pred_grid['mean_theta'] = lmm_results.predict(pred_grid)

    # --- NEW: Calculate the standard error and CI for the mean theta prediction ---
    formula_rhs = lmm_results.model.formula.split('~')[1].strip()
    design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
    fe_cov = lmm_results.cov_params().loc[lmm_results.fe_params.index, lmm_results.fe_params.index]
    design_matrix = design_matrix[fe_cov.columns] # Ensure column order matches
    
    pred_var = np.sum((design_matrix @ fe_cov) * design_matrix, axis=1)
    pred_se = np.sqrt(pred_var)
    pred_grid['theta_lower'] = pred_grid['mean_theta'] - 1.96 * pred_se
    pred_grid['theta_upper'] = pred_grid['mean_theta'] + 1.96 * pred_se
    
    for i, factor in enumerate(factors):

        # 1. Define the acceptable discrimination range.
        min_d, max_d = min_discrim_threshold, max_discrim_threshold

        # 2. Find the name of the discrimination column for the current factor.
        #    This handles both single-factor ('Discrim_All') and multi-factor models.
        discrim_col_name = f'Discrim_{factor}'
        if discrim_col_name not in df_items.columns:
            # Fallback for single factor models where the name might not match exactly.
            discrim_cols = [c for c in df_items.columns if c.startswith('Discrim_')]
            if len(discrim_cols) == 1:
                discrim_col_name = discrim_cols[0]
            else:
                # If we can't be sure which column to use, skip filtering for this factor.
                print(f"Warning: Could not uniquely identify discrimination column for factor '{factor}'. Plot will be based on all items.")
                discrim_col_name = None
        
        # 3. Filter the items based on the acceptable discrimination range.
        if discrim_col_name:
            acceptable_items = df_items[
                (df_items[discrim_col_name] >= min_d) & 
                (df_items[discrim_col_name] <= max_d)
            ]
        else:
            acceptable_items = df_items # Use all items if column not found

        # Check if any items remain after filtering
        if acceptable_items.empty:
            print(f"Warning: No items found for factor '{factor}' within the acceptable discrimination range. Skipping plot for this factor.")
            continue

        # For the mean trend, we use the average item parameters for that factor
        regex = '|'.join(groups[factor])
        factor_items = df_items[df_items.index.str.contains(regex)]
        if factor_items.empty: continue
            
        avg_discrimination = acceptable_items['Overall_Discrimination'].mean()
        avg_difficulty = acceptable_items['Difficulty'].mean()
        
        factor_df = pred_grid[pred_grid['Factor'] == factor]
        
        # Define the logistic function (with the correct sign)
        def to_prob(theta):
            logit = avg_discrimination * (theta - avg_difficulty)
            return 1 / (1 + np.exp(-logit))
        
        # Apply the transformation to the mean and the CI bounds
        prob_mean = to_prob(factor_df['mean_theta'])
        prob_lower = to_prob(factor_df['theta_lower'])
        prob_upper = to_prob(factor_df['theta_upper'])
        
        # Plot the results
        
        ax.plot(factor_df['Days'], prob_mean, color=colors[i], linewidth=2.5, label=factor, linestyle=PROB_LINE_STYLE)
        ax.fill_between(factor_df['Days'], prob_lower, prob_upper, color=colors[i], alpha=MEAN_CI_ALPHA)

    ax.set_xlabel(params['x_axis']['label'])
    ax.set_ylabel(params['y_axis']['label'])

    ax.set_title(f"{save_path}\n{params['title']}\n")
    if params['y_axis']['range']:
        ax.set_ylim(params['y_axis']['range'])
    if params['legend']['show']:
        ax.legend(loc=params['legend']['location'],
                  title=params['legend']['title'],
                  fontsize=params['legend']['fontsize'],
                  framealpha=params['legend']['framealpha'])
    ax.grid(True, linestyle='--', alpha=0.6)

    ax = plot_individual_deviations(
        df_lmm_long = df_long, 
        df_items = df_items, 
        groups = groups, 
        lmm_results = lmm_results, 
        ax=ax,
        colors=colors,
    )

    save_or_show_plot(fig, save_path=save_path, dpi=params.output.dpi)

def plot_utility(
    lmm_results: pd.DataFrame, 
    df_long: pd.DataFrame,
    save_path: str,
    params: dict,
    colors: list,
    # Define some constants for plotting aesthetics
    RESIDUAL_SCATTER_POINT_ALPHA = 0.1,
    MEAN_CI_ALPHA = 0.15
):
    """
    Plots the model-predicted utility over time, separating trends by
    data source (e.g., 'ctt' vs. 'prob') and factor. Individual data points
    are shown as residuals centered around the predicted mean.
    """
    
    fig, ax = plt.subplots(figsize=(12, 8))
    day_range = np.linspace(df_long['Days'].min(), df_long['Days'].max(), 100)
    
    # Get unique sources and factors from the data
    sources = df_long['Source'].unique()
    factors = df_long['Factor'].unique()
    
    # Define line styles for different sources to make the plot clear
    line_styles = {'ctt': '-', 'prob': '--'}
    
    # --- 1. Calculate the LMM's predicted mean and confidence interval ---
    pred_grid = pd.DataFrame(
        [(day, source, factor) for day in day_range for source in sources for factor in factors],
        columns=['Days', 'Source', 'Factor']
    )
    
    model_terms = lmm_results.fe_params.index
    if any('Days_sq' in term for term in model_terms): pred_grid['Days_sq'] = pred_grid['Days'] ** 2
    if any('log_Days' in term for term in model_terms): pred_grid['log_Days'] = np.log(pred_grid['Days'] + 1)
        
    formula_rhs = lmm_results.model.formula.split('~')[1].strip()
    design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
    
    pred_grid['mean'] = lmm_results.predict(pred_grid)
    fe_cov = lmm_results.cov_params().loc[lmm_results.fe_params.index, lmm_results.fe_params.index]
    design_matrix = design_matrix[fe_cov.columns]
    
    pred_var = np.sum((design_matrix @ fe_cov) * design_matrix, axis=1)
    pred_se = np.sqrt(pred_var)
    pred_grid['mean_ci_lower'] = pred_grid['mean'] - 1.96 * pred_se
    pred_grid['mean_ci_upper'] = pred_grid['mean'] + 1.96 * pred_se

    # --- 2. Plot Individual Data Points (as Residuals) ---
    # This new section replicates the logic from your lmm_trajectory plot.
    
    df_temp = df_long.copy()
    df_temp['Residual'] = lmm_results.resid

    df_temp.to_clipboard()
    input("Check the copied DataFrame in your clipboard to verify the data structure.")

    day_positions = sorted(df_long['Days'].unique())
    offsets = get_offsets(len(factors))

    for i, factor in enumerate(factors):
        for source in sources:
            # Correctly filter the data for the specific source and factor
            sub = df_temp[(df_temp['Factor'] == factor) & (df_temp['Source'] == source)]
            if sub.empty:
                continue

            color = colors[i]
            
            # Loop through each day to plot the points for that day
            for d in day_positions:
                day_data = sub[sub['Days'] == d]
                if day_data.empty:
                    continue

                # Predict the mean for this specific point in time, source, and factor
                row = {'Source': source, 'Factor': factor, 'Days': d}
                if 'Days_sq' in pred_grid.columns: row['Days_sq'] = d**2
                if 'log_Days' in pred_grid.columns: row['log_Days'] = np.log(d + 1)
                
                mu = lmm_results.predict(pd.DataFrame([row]))[0]

                # Y values are the residuals centered around the predicted mean
                ys = day_data['Residual'] + mu
                # X values are the day positions with a horizontal offset for each factor
                xs = day_data['Days'] + offsets[i]

                ax.scatter(xs, ys, color=color, alpha=RESIDUAL_SCATTER_POINT_ALPHA, s=15, edgecolor='none')

    # --- 3. Plot the Main Trend Lines on Top ---
    for i, factor in enumerate(factors):
        for source in sources:
            sub_pred = pred_grid[(pred_grid['Factor'] == factor) & (pred_grid['Source'] == source)]
            if sub_pred.empty:
                continue

            color = colors[i]
            linestyle = line_styles.get(source, '-')

            ax.plot(
                sub_pred['Days'], 
                sub_pred['mean'], 
                color=color, 
                linewidth=2.5, 
                linestyle=linestyle,
                label=f"{factor}" # Keep legend clean, source is shown by line style
            )
            ax.fill_between(
                sub_pred['Days'], 
                sub_pred['mean_ci_lower'], 
                sub_pred['mean_ci_upper'], 
                color=color, 
                alpha=MEAN_CI_ALPHA
            )

    # --- 4. Final Formatting and Custom Legend ---
    ax.set_xlabel(params['x_axis']['label'])
    ax.set_ylabel("Memory Utility")
    ax.set_title(f"{params['title']}\n(Mean Trend ±95% CI)")

    if params['y_axis']['range']:
        ax.set_ylim(bottom=params['y_axis']['range'][0], top=params['y_axis']['range'][1])

    # Create a more informative legend
    handles, labels = ax.get_legend_handles_labels()
    # Remove duplicate labels if any
    by_label = dict(zip(labels, handles))
    
    # style_handles = [
    #     Line2D([0], [0], color='gray', linestyle='-', label='Raw Scores (CTT)'),
    #     Line2D([0], [0], color='gray', linestyle='--', label='IRT Probability')
    # ]
    ax.legend(handles=list(by_label.values()), loc='best', title=params['legend']['title'])

    ax.grid(True, linestyle='--', alpha=0.6)
    
    save_or_show_plot(fig, save_path=save_path, dpi=params['output']['dpi'])

def plot_analysis(
    lmm_results: pd.DataFrame,
    df_data: pd.DataFrame,
    title: str,
    save_path: str,
):
    try:
        """ Plots the model-predicted regression lines (in terms of theta) with 95% confidence intervals."""
        
        print(f"Plotting analysis for {title}...")

        fig, ax = plt.subplots(figsize=(12, 8))
        time_range = np.linspace(df_data['Time'].min(), df_data['Time'].max(), 200)

        # Get unique sources and factors from the data
        sources = df_data['Source'].unique()
        factors = df_data['Factor'].unique()
        measures = df_data['Measure'].unique()

        # --- 1. Calculate the LMM's predicted mean and confidence interval ---
        # pred_grid = df_data.copy()
        pred_grid = pd.DataFrame(
            [(time, source, factor, measure) for time in time_range for source in sources for factor in factors for measure in measures],
            columns=['Time', 'Source', 'Factor', 'Measure']
        )

        print(pred_grid)
        # input()
        
        model_terms = lmm_results.fe_params.index
        if any('Time_sq' in term for term in model_terms): pred_grid['Time_sq'] = pred_grid['Time'] ** 2
        if any('log_Time' in term for term in model_terms): pred_grid['log_Time'] = np.log(pred_grid['Time'] + 1)
        # if any('Time_post_consolidation' in term for term in model_terms): 
        #     pred_grid['Time_post_consolidation'] = np.maximum(0, pred_grid['Time'] - 24)

        formula_rhs = lmm_results.model.formula.split('~')[1].strip()
        design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
        
        pred_grid['mean'] = lmm_results.predict(pred_grid)
        fe_cov = lmm_results.cov_params().loc[lmm_results.fe_params.index, lmm_results.fe_params.index]
        design_matrix = design_matrix[fe_cov.columns]
        
        pred_var = np.sum((design_matrix @ fe_cov) * design_matrix, axis=1)
        pred_se = np.sqrt(pred_var)
        pred_grid['mean_ci_lower'] = pred_grid['mean'] - 1.96 * pred_se
        pred_grid['mean_ci_upper'] = pred_grid['mean'] + 1.96 * pred_se

        # --- 2. Plot Individual Data Points (as Residuals) ---

        time_positions = sorted(df_data['Time'].unique())

        legend = []

        for source in sources:

            if source == 'ctt':
                line_style = 'dotted'
                ax.set_ylim(bottom=0, top=1)

            elif source == 'irt':
                line_style = 'dashed'
                ax.set_ylim(bottom=-1, top=1)

            elif source == 'prob':
                line_style = 'solid'
                ax.set_ylim(bottom=0, top=1)

            for measure in measures:
                if measure == 'scor':
                    colours = [blue, green, orange]
                    # ax.set_ylabel("Probability of Correct Response / High Confidence", fontsize=14)
                elif measure == 'conf':
                    colours = [cyan, purple, red]
                    # ax.set_ylabel("Probability of Correct Response / High Confidence", fontsize=14)
                elif measure == 'util':
                    ax.set_ylim(bottom=-1, top=1)
                    colours = [pink, brown, grey]

                for i, factor in enumerate(factors):


                    # Correctly filter the data for the specific source and factor
                    sub = df_data[(df_data['Factor'] == factor) & (df_data['Source'] == source) & (df_data['Measure'] == measure)]
                    if sub.empty:
                        continue

                    # Loop through each time to plot the points for that time
                    for t in time_positions:
                        time_data = sub[sub['Time'] == t]
                        if time_data.empty:
                            continue

                        # Predict the mean for this specific point in time, source, and factor
                        row = {'Source': source, 'Factor': factor, 'Time': t, 'Measure': measure}
                        if 'Time_sq' in pred_grid.columns: row['Time_sq'] = t**2
                        if 'log_Time' in pred_grid.columns: row['log_Time'] = np.log(t + 1)
                        if 'Time_post_consolidation' in pred_grid.columns:
                            row['Time_post_consolidation'] = np.maximum(0, t - 24)

                        mu = lmm_results.predict(pd.DataFrame([row]))[0]

                        # Y values are the residuals centered around the predicted mean
                        ys = time_data['Resid'] + mu
                        # X values are the time positions with a horizontal offset for each factor
                        xs = time_data['Time']

                        ax.scatter(xs, ys, color=colours[i], alpha=RESIDUAL_SCATTER_POINT_ALPHA, s=15, edgecolor='none')

                        # --- 3. Plot the Main Trend Lines on Top ---
                    sub_pred = pred_grid[(pred_grid['Factor'] == factor) & (pred_grid['Source'] == source) & (pred_grid['Measure'] == measure)]
                    if sub_pred.empty:
                        continue
                    ax.plot(
                        sub_pred['Time'], 
                        sub_pred['mean'], 
                        color=colours[i], 
                        linewidth=2.5, 
                        linestyle=line_style,
                        label=f"{factor}" # Keep legend clean, source is shown by line style
                    )
                    ax.fill_between(
                        sub_pred['Time'], 
                        sub_pred['mean_ci_lower'], 
                        sub_pred['mean_ci_upper'], 
                        color=colours[i], 
                        alpha=MEAN_CI_ALPHA
                    )

                    factor_temp = factor
                    factor_temp = factor_temp.replace("All ", "")
                    factor_temp = factor_temp.replace("Items ", "")
                    
                    legend.append({
                        'factor': factor_temp,
                        'source': source,
                        'measure': measure,
                        'color': colours[i],
                        'linestyle': line_style,
                        'intercept': sub_pred['mean'].iloc[0],  # Use the first mean as intercept for sorting
                    })


        # # --- 3. Plot the Main Trend Lines on Top ---
        # for i, factor in enumerate(factors):
        #     for source in sources:
        #         sub_pred = pred_grid[(pred_grid['Factor'] == factor) & (pred_grid['Source'] == source)]
        #         if sub_pred.empty:
        #             continue

        #         linestyle = 'solid'

        #         ax.plot(
        #             sub_pred['Time'], 
        #             sub_pred['mean'], 
        #             color=colors[i], 
        #             linewidth=2.5, 
        #             linestyle=linestyle,
        #             label=f"{factor}" # Keep legend clean, source is shown by line style
        #         )
        #         ax.fill_between(
        #             sub_pred['Time'], 
        #             sub_pred['mean_ci_lower'], 
        #             sub_pred['mean_ci_upper'], 
        #             color=colors[i], 
        #             alpha=MEAN_CI_ALPHA
        #         )

        # --- 4. Final Formatting and Custom Legend ---

        fontsize_axes = 14
        fontsize_title = 16

        ax.set_xlabel("Time since encoding (hours)", fontsize=fontsize_axes)
        ax.tick_params(axis='both', labelsize=fontsize_axes)
        ax.set_xlim(left=-5, right=200)
        # ax.set_title("", fontsize=fontsize_title)
        # if "1.1" in title:
        #     # ax.set_ylabel("Probability of Correct Response", fontsize=fontsize_axes)
        #     # ax.set_title("Probability of Correct REMEMVR Responses over Time", fontsize=fontsize_title)
        #     ax.set_xlim(left=-5, right=200)
        # elif "5." in title:
        #     # ax.set_ylabel("(Accuracy Ability - Confidence Ability)", fontsize=fontsize_axes)
        #     # ax.set_title("Utility of Correct REMEMVR Responses over Time", fontsize=fontsize_title)
        #     ax.set_xlim(left=-5, right=200)

        # else:
        #     # ax.set_ylabel("Label")
        #     # ax.set_title(title)
        #     pass
        
        if len(factors) > 0:
            # Sort legend by descending factor[intercept]
            # legend = sorted(legend, key=lambda x: x['intercept'], reverse=True)
            print(legend)
            ax.legend(
                handles=[Line2D([0], [0], color=leg['color'], linestyle=leg['linestyle'], label=f"{leg['factor']} ({leg['measure']})") for leg in legend],
                loc='best',
                title=None,
                fontsize=12,
                framealpha=0.8
            )

        ax.grid(True, linestyle='--', alpha=0.6)
        
        save_or_show_plot(fig, save_path=save_path, dpi=300)

    except:
        pass










def plot_model_evolution(
        all_lmm_results: list, 
        df_long_final: pd.DataFrame,
        pass_num: int,
        save_folder: str,
        params: dict,
    ):
    fig, ax = plt.subplots(figsize=(10, 6))
    n_results = len(all_lmm_results)
    
    for i, lmm_results in enumerate(all_lmm_results):
        is_final_pass = (i == n_results - 1)
        alpha = 1.0 if is_final_pass else 0.3
        linewidth = 2.5 if is_final_pass else 1.5
        linestyle = '-' if is_final_pass else '--'
        day_range = np.linspace(df_long_final['Days'].min(), df_long_final['Days'].max(), 100)
        is_multi_factor = 'Factor' in df_long_final.columns and df_long_final['Factor'].nunique() > 1
        # factors = df_long_final['Factor'].unique() if is_multi_factor else ['Overall']
        factors = df_long_final['Factor'].unique()
        
        pred_grid = pd.DataFrame([(day, factor) for factor in factors for day in day_range], columns=['Days', 'Factor'])
        
        model_terms = lmm_results.fe_params.index
        if any('Days_sq' in term for term in model_terms): pred_grid['Days_sq'] = pred_grid['Days'] ** 2
        if any('log_Days' in term for term in model_terms): pred_grid['log_Days'] = np.log(pred_grid['Days'] + 1)
        formula_rhs = lmm_results.model.formula.split('~')[1].strip()
        design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
        # pred_grid['mean'] = lmm_results.predict(exog=design_matrix)
        pred_grid['mean'] = lmm_results.predict(pred_grid)

        # colors = plt.cm.get_cmap('viridis', len(factors))
        colors = params.colors if 'colors' in params else plt.cm.get_cmap('viridis', len(factors))

        for j, factor in enumerate(factors):
            factor_df = pred_grid[pred_grid['Factor'] == factor]
            # color = colors(j / (len(factors)-1)) if len(factors) > 1 else colors(0.5)
            color = colors[j] if 'colors' in params else colors(j / (len(factors)-1)) if len(factors) > 1 else colors(0.5)

            label = factor if is_final_pass else None
            ax.plot(factor_df['Days'], factor_df['mean'], color=color, linewidth=linewidth, alpha=alpha, linestyle=linestyle, label=label)

    ax.set_xlabel(params.x_axis.label)
    ax.set_ylabel(params.y_axis.label)
    ax.set_title(f"{params.title} 1 - {pass_num})")
    if params.y_axis.range:
        ax.set_ylim(bottom=params.y_axis.range[0], top=params.y_axis.range[1])
    
    if params.legend.show:
        ax.legend(loc=params.legend.location, title=params.legend.title, fontsize=params.legend.fontsize, framealpha=params.legend.framealpha)
    ax.grid(True, linestyle='--', alpha=0.6)
    save_or_show_plot(fig, save_path=f"{save_folder}{params.output.filename}", dpi=params.output.dpi)



# def plot_item_difficulty(
#         item_params_df: pd.DataFrame, 
#         pass_num: int,
#         save_folder: str,
#         params: dict,
#         colors: list,
#     ):

#     """
#     Plots overlapping histograms of item difficulties for each factor,
#     with a normal distribution curve overlaid for each.
#     """
#     if 'Difficulty' not in item_params_df.columns: return
#     fig, ax = plt.subplots(figsize=(12, 7))

#     # Dynamically find the discrimination factor columns
#     discrim_cols = [col for col in item_params_df.columns if col.startswith('Discrim_')]
#     group_names = [col.replace('Discrim_', '') for col in discrim_cols]
    
#     # Define a shared bin range for all histograms
#     sane_difficulties_all = item_params_df['Difficulty'].clip(-8, 8)
#     bins = np.linspace(sane_difficulties_all.min(), sane_difficulties_all.max(), 30)

#     for i, (group, discrim_col) in enumerate(zip(group_names, discrim_cols)):
#         # Select items where the loading on this factor is > 0
#         group_items = item_params_df[item_params_df[discrim_col] > 0]
#         if group_items.empty: continue
        
#         if params.clip:
#             sane_difficulties = group_items['Difficulty'].clip(params.clip[0], params.clip[1])
#         else:
#             sane_difficulties = group_items['Difficulty']

#         ax.hist(sane_difficulties, bins=bins, edgecolor='black', alpha=DIFF_HIST_ALPHA, 
#                 label=f'{group} (n={len(sane_difficulties)})', color=colors[i])

#         # Overlay the normal distribution curve
#         mu, std = stats.norm.fit(sane_difficulties)
#         x = np.linspace(sane_difficulties.min(), sane_difficulties.max(), 100)
#         p = stats.norm.pdf(x, mu, std)
        
#         # Scale the PDF to match the histogram
#         bin_width = bins[1] - bins[0]
#         scaled_p = p * len(sane_difficulties) * bin_width
#         ax.plot(x, scaled_p, color=colors[i], linewidth=2)

#     ax.set_title(f"{save_folder}{params.output.filename}\n{params.title} - (Pass {pass_num})")
#     ax.set_xlabel(params.x_axis.label)
#     ax.set_ylabel('Frequency')

#     if params.x_axis.range:
#         ax.set_xlim(left=params.x_axis.range[0], right=params.x_axis.range[1])

#     if params.legend.show:
#         ax.legend(loc=params.legend.location, title=params.legend.title, fontsize=params.legend.fontsize, framealpha=params.legend.framealpha)

#     ax.grid(True, linestyle='--', alpha=0.6)
    
#     save_or_show_plot(fig, save_path=f"{save_folder}{params.output.filename}", dpi=params.output.dpi)

# def plot_lmm_trajectory(
#     lmm_results: pd.DataFrame, 
#     df_long: pd.DataFrame,
#     model_name: str,
#     pass_num: int,
#     save_folder: str,
#     params: dict,
# ):
#     """
#     Plots the model-predicted regression lines (in terms of theta) with 95% 
#     confidence intervals and overlays individual participant spaghetti lines.
#     """
#     # Define plotting aesthetics
#     point_alpha = 0.1
#     violin_alpha = 0.05
#     line_alpha = 0.1
    
#     fig, ax = plt.subplots(figsize=(10, 6))
    
#     # --- 1. Calculate the Main Trend Line (Fixed Effect) ---
#     day_range = np.linspace(df_long['Days'].min(), df_long['Days'].max(), 100)
#     factors = df_long['Factor'].unique()
    
#     pred_grid = pd.DataFrame([(day, factor) for factor in factors for day in day_range], columns=['Days', 'Factor'])
    
#     model_terms = lmm_results.fe_params.index
#     if any('Days_sq' in term for term in model_terms): pred_grid['Days_sq'] = pred_grid['Days'] ** 2
#     if any('log_Days' in term for term in model_terms): pred_grid['log_Days'] = np.log(pred_grid['Days'] + 1)
        
#     formula_rhs = lmm_results.model.formula.split('~')[1].strip()
#     design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
    
#     pred_grid['mean'] = lmm_results.predict(pred_grid)
#     fe_cov = lmm_results.cov_params().loc[lmm_results.fe_params.index, lmm_results.fe_params.index]
#     design_matrix = design_matrix[fe_cov.columns]
    
#     pred_var = np.sum((design_matrix @ fe_cov) * design_matrix, axis=1)
#     pred_se = np.sqrt(pred_var)
#     pred_grid['mean_ci_lower'] = pred_grid['mean'] - 1.96 * pred_se
#     pred_grid['mean_ci_upper'] = pred_grid['mean'] + 1.96 * pred_se

#     colors = params['colors'] if 'colors' in params else plt.cm.get_cmap('viridis', len(factors))
    
#     # --- 2. Plot Individual Data (Violins, Dots, and Spaghetti Lines) ---
#     day_positions = sorted(df_long['Days'].unique())

#     for i, factor in enumerate(factors):
#         # Get the color for the current factor
#         color = colors[i] if isinstance(colors, list) and i < len(colors) else 'gray'
        
#         # Get the subset of data for the current factor
#         sub = df_long[df_long['Factor'] == factor].copy()
        
#         # --- A. Plot Spaghetti Lines (Corrected Logic) ---
#         # We loop through each participant and plot their actual ability scores over time.
#         for uid in sub['UID'].unique():
#             participant_data = sub[sub['UID'] == uid].sort_values('Days')
#             if len(participant_data) > 1:
#                 ax.plot(
#                     participant_data['Days'], 
#                     participant_data['Ability'], 
#                     color=color, 
#                     alpha=line_alpha,
#                     linewidth=0.7,
#                     label='_nolegend_' # Prevents legend clutter
#                 )

#         # --- B. Plot Violins ---
#         # The violins show the distribution of raw ability scores at each time point.
#         violin_data = [sub.loc[sub['Days'] == d, 'Ability'].dropna().values for d in day_positions]
#         valid_days = [d for d, v in zip(day_positions, violin_data) if len(v) > 0]
#         valid_violins = [v for v in violin_data if len(v) > 0]
        
#         if valid_violins:
#             vp = ax.violinplot(
#                 valid_violins,
#                 positions=valid_days,
#                 widths=0.6,
#                 showmeans=False, showmedians=False, showextrema=False
#             )
#             for pc in vp['bodies']:
#                 pc.set_facecolor(color)
#                 pc.set_edgecolor('none')
#                 pc.set_alpha(violin_alpha)

#     # --- 3. Plot the Main Trend Line on Top ---
#     for i, factor in enumerate(factors):
#         factor_df = pred_grid[pred_grid['Factor'] == factor]
#         color = colors[i] if isinstance(colors, list) and i < len(colors) else 'gray'
#         ax.plot(factor_df['Days'], factor_df['mean'], color=color, linewidth=2.5, label=factor)
#         ax.fill_between(factor_df['Days'], factor_df['mean_ci_lower'], factor_df['mean_ci_upper'], color=color, alpha=params['alpha'])

#     # --- 4. Final Formatting ---
#     ax.set_xlabel(params['x_axis']['label'])
#     ax.set_ylabel(params['y_axis']['label'])
#     ax.set_title(f"{params['title']} - ({model_name} Model, Pass {pass_num})")

#     if params['y_axis']['range']:
#         ax.set_ylim(bottom=params['y_axis']['range'][0], top=params['y_axis']['range'][1])

#     if params['legend']['show']:
#         ax.legend(loc=params['legend']['location'], title=params['legend']['title'], fontsize=params['legend']['fontsize'], framealpha=params['legend']['framealpha'])

#     ax.grid(True, linestyle='--', alpha=0.6)
    
#     save_or_show_plot(fig, save_path=f"{save_folder}{params['output']['filename']}", dpi=params['output']['dpi'])

# def plot_predicted_probabilities2(
#     lmm_results,
#     df_items,
#     df_long,
#     groups,
#     model_name: str,
#     pass_num: int,
#     save_folder: str,
#     params: dict,
# ):
#     """
#     Plots the model-predicted probability of a correct response for an average person.
#     The trend line and its confidence interval are now based only on items within the
#     acceptable discrimination range (0.5 to 4.0).
#     """

#     # This helper function can remain exactly as it is.
#     def plot_individual_deviations(
#         df_lmm_long, 
#         df_items, 
#         groups, 
#         lmm_results, 
#         ax=None,
#         colors=None,
#     ):
#         # 1) pre-compute a_bar, b_bar per factor
#         bars = {
#             k: (
#                 df_items.loc[df_items.index.str.contains('|'.join(v)), 'Overall_Discrimination'].mean(),
#                 df_items.loc[df_items.index.str.contains('|'.join(v)), 'Difficulty'].mean()
#             )
#             for k,v in groups.items()
#         }
#         # 2) for every row in df_lmm_long, compute P_i and P_mean
#         df = df_lmm_long.copy()
#         df['a_bar'] = df['Factor'].map(lambda k: bars[k][0])
#         df['b_bar'] = df['Factor'].map(lambda k: bars[k][1])
#         # individual P_i
#         df['P_i'] = 1/(1 + np.exp(-(df['a_bar']*(df['Ability']-df['b_bar']))))
#         # mean theta at each row
#         df['mean_theta'] = lmm_results.predict(df)
#         # mean probability at each row
#         df['P_mean'] = 1/(1 + np.exp(-(df['a_bar']*(df['mean_theta']-df['b_bar']))))
#         # 3) now group by factor & day to plot violins on df['P_i']
#         color_count = 0
#         for factor in groups:
#             sub = df[df['Factor']==factor]
#             days = sorted(sub['Days'].unique())
#             violins = [sub.loc[sub['Days']==d, 'P_i'].values for d in days]
#             vp = ax.violinplot(violins, positions=days, widths=0.6,
#                             showmeans=False, showmedians=False, showextrema=False)
#             for body in vp['bodies']:
#                 body.set_alpha(0.05)
#                 body.set_facecolor(colors[color_count])
#                 body.set_edgecolor('none')
#             # scatter points
#             for d in days:
#                 y = sub.loc[sub['Days']==d, 'P_i']
#                 x = (abs(y - sub.loc[sub['Days']==d, 'P_mean']))
#                 x = (x.max() - x)
#                 x = x + np.random.normal(loc=0, scale=x, size=len(x))
#                 x = x * 0.1
#                 x = (x - x.mean()) + d
#                 ax.scatter(
#                     x, y, s=8, alpha=0.1, color=colors[color_count], edgecolor='none', label=None
#                 )
#             color_count += 1
#         return ax

#     # This helper function can also remain as it is.
#     def safe_logistic(x):
#         x_clamped = np.clip(x, -10, 10)
#         return 1.0 / (1.0 + np.exp(-x_clamped))

#     # --- Main function starts here ---
#     fig, ax = plt.subplots(figsize=(10, 6))
#     day_range = np.linspace(df_long['Days'].min(), df_long['Days'].max(), 100)
#     factors = df_long['Factor'].unique()
    
#     # --- Calculate the LMM's predicted mean theta and its standard error ---
#     pred_grid = pd.DataFrame([
#         (d, f) for f in factors for d in day_range
#     ], columns=['Days', 'Factor'])
    
#     terms = lmm_results.fe_params.index
#     if any('Days_sq' in t for t in terms):
#         pred_grid['Days_sq'] = pred_grid['Days']**2
#     if any('log_Days' in t for t in terms):
#         pred_grid['log_Days'] = np.log(pred_grid['Days'] + 1)

#     pred_grid['mean_theta'] = lmm_results.predict(pred_grid)

#     formula_rhs = lmm_results.model.formula.split('~')[1].strip()
#     design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
#     fe_cov = lmm_results.cov_params().loc[lmm_results.fe_params.index, lmm_results.fe_params.index]
#     design_matrix = design_matrix[fe_cov.columns]
    
#     pred_var = np.sum((design_matrix @ fe_cov) * design_matrix, axis=1)
#     pred_se = np.sqrt(pred_var)
#     pred_grid['theta_lower'] = pred_grid['mean_theta'] - 1.96 * pred_se
#     pred_grid['theta_upper'] = pred_grid['mean_theta'] + 1.96 * pred_se
    
#     # --- Plotting Loop ---
#     cmap = params['colors'] if 'colors' in params else plt.cm.get_cmap('viridis', len(factors))
#     for i, factor in enumerate(factors):
        
#         # ============================ NEW CODE BLOCK ================================
#         # This new block filters the items before calculating the average parameters.

#         # 1. Define the acceptable discrimination range.
#         min_d, max_d = 0.5, 4.0

#         # 2. Find the name of the discrimination column for the current factor.
#         #    This handles both single-factor ('Discrim_All') and multi-factor models.
#         discrim_col_name = f'Discrim_{factor}'
#         if discrim_col_name not in df_items.columns:
#             # Fallback for single factor models where the name might not match exactly.
#             discrim_cols = [c for c in df_items.columns if c.startswith('Discrim_')]
#             if len(discrim_cols) == 1:
#                 discrim_col_name = discrim_cols[0]
#             else:
#                 # If we can't be sure which column to use, skip filtering for this factor.
#                 print(f"Warning: Could not uniquely identify discrimination column for factor '{factor}'. Plot will be based on all items.")
#                 discrim_col_name = None
        
#         # 3. Filter the items based on the acceptable discrimination range.
#         if discrim_col_name:
#             acceptable_items = df_items[
#                 (df_items[discrim_col_name] >= min_d) & 
#                 (df_items[discrim_col_name] <= max_d)
#             ]
#         else:
#             acceptable_items = df_items # Use all items if column not found

#         # Check if any items remain after filtering
#         if acceptable_items.empty:
#             print(f"Warning: No items found for factor '{factor}' within the acceptable discrimination range. Skipping plot for this factor.")
#             continue

#         # 4. Calculate average parameters using ONLY the acceptable items.
#         avg_discrimination = acceptable_items['Overall_Discrimination'].mean()
#         avg_difficulty = acceptable_items['Difficulty'].mean()
#         # ==============================================================================
        
#         # The rest of the plotting logic uses these new, filtered averages.
#         factor_df = pred_grid[pred_grid['Factor'] == factor]
        
#         def to_prob(theta):
#             logit = avg_discrimination * (theta - avg_difficulty)
#             return 1 / (1 + np.exp(-logit))
        
#         prob_mean = to_prob(factor_df['mean_theta'])
#         prob_lower = to_prob(factor_df['theta_lower'])
#         prob_upper = to_prob(factor_df['theta_upper'])
        
#         color = cmap[i] if isinstance(cmap, list) else cmap(i)
#         ax.plot(factor_df['Days'], prob_mean, color=color, linewidth=2.5, label=factor)
#         ax.fill_between(factor_df['Days'], prob_lower, prob_upper, color=color, alpha=params['alpha'])

#     # --- Formatting and Saving ---
#     ax.set_xlabel(params['x_axis']['label'])
#     ax.set_ylabel(params['y_axis']['label'])
#     ax.set_title(f"{params['title']} (Mean Trend ±95% CI) — ({model_name}, pass {pass_num})")
#     if params['y_axis']['range']:
#         ax.set_ylim(params['y_axis']['range'])
#     if params['legend']['show']:
#         ax.legend(loc=params['legend']['location'],
#                   title=params['legend']['title'],
#                   fontsize=params['legend']['fontsize'],
#                   framealpha=params['legend']['framealpha'])
#     ax.grid(True, linestyle='--', alpha=0.6)

#     ax = plot_individual_deviations(
#         df_lmm_long = df_long, 
#         df_items = df_items, 
#         groups = groups, 
#         lmm_results = lmm_results, 
#         ax=ax,
#         colors=cmap,
#     )

#     save_or_show_plot(fig, save_path=f"{save_folder}{params['output']['filename']}", dpi=params['output']['dpi'])

    # def plot_individual_deviations(
    #     df_lmm_long, 
    #     df_items, 
    #     groups, 
    #     lmm_results, 
    #     ax=None,
    #     colors=None,
    #     # Pass the discrimination thresholds to the function
    #     # min_discrim_threshold=min_discrim_threshold,
    #     # max_discrim_threshold=max_discrim_threshold
    # ):
    #     """
    #     Overlays violins and scattered dots representing individual deviations.
    #     This version filters items to match the main trend line, using only items
    #     with acceptable discrimination parameters.
    #     """
        
    #     # Create a copy of the data to avoid modifying the original DataFrame
    #     df = df_lmm_long.copy()
        
    #     # Pre-calculate mean theta for all rows once to be efficient
    #     df['mean_theta'] = lmm_results.predict(df)

    #     color_count = 0
    #     for factor in groups:
    #         # --- NEW: Filter items for the current factor ---
    #         # This logic now mirrors the filtering used for the main trend line.
            
    #         # 1. Find the name of the discrimination column for the current factor.
    #         discrim_col_name = f'Discrim_{factor}'
    #         if discrim_col_name not in df_items.columns:
    #             discrim_cols = [c for c in df_items.columns if c.startswith('Discrim_')]
    #             if len(discrim_cols) == 1:
    #                 discrim_col_name = discrim_cols[0]
    #             else:
    #                 discrim_col_name = None # Cannot determine column

    #         # 2. Filter the items dataframe.
    #         if discrim_col_name:
    #             acceptable_items = df_items[
    #                 (df_items[discrim_col_name] >= min_discrim_threshold) & 
    #                 (df_items[discrim_col_name] <= max_discrim_threshold)
    #             ]
    #         else:
    #             acceptable_items = df_items # Fallback to all items

    #         if acceptable_items.empty:
    #             # If no items are left after filtering, skip this factor for the deviation plot.
    #             color_count += 1
    #             continue

    #         # --- Calculate average parameters from ONLY the filtered set ---
    #         avg_discrimination = acceptable_items['Overall_Discrimination'].mean()
    #         avg_difficulty = acceptable_items['Difficulty'].mean()

    #         # Calculate probabilities for each individual using these filtered average parameters
    #         sub = df[df['Factor']==factor].copy() # Use .copy() to avoid SettingWithCopyWarning
    #         sub.loc[:, 'P_i'] = 1 / (1 + np.exp(-(avg_discrimination * (sub['Ability'] - avg_difficulty))))
    #         sub.loc[:, 'P_mean'] = 1 / (1 + np.exp(-(avg_discrimination * (sub['mean_theta'] - avg_difficulty))))

    #         # --- The rest of the plotting logic remains the same ---
    #         days = sorted(sub['Days'].unique())
    #         violins = [sub.loc[sub['Days']==d, 'P_i'].dropna().values for d in days]
            
    #         valid_days = [d for d, v in zip(days, violins) if len(v) > 0]
    #         valid_violins = [v for v in violins if len(v) > 0]

    #         if not valid_violins: 
    #             color_count += 1
    #             continue

    #         vp = ax.violinplot(valid_violins, positions=valid_days, widths=0.6,
    #                         showmeans=False, showmedians=False, showextrema=False)
            
    #         # Determine the color safely for the current factor
    #         color = colors[color_count] if isinstance(colors, list) and color_count < len(colors) else 'gray'

    #         for body in vp['bodies']:
    #             body.set_alpha(0.05)
    #             body.set_facecolor(color)
    #             body.set_edgecolor('none')
                
    #         for d in valid_days:
    #             y = sub.loc[sub['Days']==d, 'P_i']
    #             p_mean_val = sub.loc[sub['Days']==d, 'P_mean']
    #             if y.empty or p_mean_val.isna().all(): continue

    #             x = (abs(y - p_mean_val))
    #             x = (x.max() - x)
    #             # Add a small epsilon to scale to avoid scale=0 error if all values are the same
    #             x = x + np.random.normal(loc=0, scale=x + 1e-9, size=len(x))
    #             x = x * 0.1
    #             x = (x - x.mean()) + d
    #             ax.scatter(
    #                 x, y, s=8, alpha=0.1, color=color, edgecolor='none', label=None
    #             )

    #         # Here's my added code to plot spaghetti lines between individual deviations across days
            
    #         for d in valid_days:
    #             y = sub.loc[sub['Days'] == d, 'P_i']
    #             p_mean_val = sub.loc[sub['Days'] == d, 'P_mean']
    #             if y.empty or p_mean_val.isna().all(): continue

    #             # Calculate x positions with jitter
    #             x = (abs(y - p_mean_val))
    #             x = (x.max() - x)
    #             x = x + np.random.normal(loc=0, scale=x + 1e-9, size=len(x))
    #             x = x * 0.1
    #             x = (x - x.mean()) + d
    #             # Plot spaghetti lines
    #             ax.plot(x, y, color=color, alpha=0.1)

    #         color_count += 1
    #     return ax

    
    # def plot_individual_deviations(
    #     df_lmm_long, 
    #     df_items, 
    #     groups, 
    #     lmm_results, 
    #     ax=None,
    #     colors=None,
    # ):
    #     # 1) pre-compute a_bar, b_bar per factor
    #     bars = {
    #         k: (
    #             df_items.loc[df_items.index.str.contains('|'.join(v)), 'Overall_Discrimination'].mean(),
    #             df_items.loc[df_items.index.str.contains('|'.join(v)), 'Difficulty'].mean()
    #         )
    #         for k,v in groups.items()
    #     }
    #     # 2) for every row in df_lmm_long, compute P_i and P_mean
    #     df = df_lmm_long.copy()
    #     df['a_bar'] = df['Factor'].map(lambda k: bars[k][0])
    #     df['b_bar'] = df['Factor'].map(lambda k: bars[k][1])
    #     # individual P_i
    #     df['P_i'] = 1/(1 + np.exp(-(df['a_bar']*(df['Ability']-df['b_bar']))))
    #     # mean theta at each row
    #     df['mean_theta'] = lmm_results.predict(df)
    #     # mean probability at each row
    #     df['P_mean'] = 1/(1 + np.exp(-(df['a_bar']*(df['mean_theta']-df['b_bar']))))
    #     # 3) now group by factor & day to plot violins on df['P_i']
    #     color_count = 0
    #     for factor in groups:
    #         sub = df[df['Factor']==factor]
    #         days = sorted(sub['Days'].unique())
    #         violins = [sub.loc[sub['Days']==d, 'P_i'].values for d in days]
    #         vp = ax.violinplot(violins, positions=days, widths=0.6,
    #                         showmeans=False, showmedians=False, showextrema=False)
    #         for body in vp['bodies']:
    #             body.set_alpha(0.05)
    #             body.set_facecolor(colors[color_count])
    #             body.set_edgecolor('none')
    #         # scatter points
    #         for d in days:
    #             y = sub.loc[sub['Days']==d, 'P_i']
    #             x = (abs(y - sub.loc[sub['Days']==d, 'P_mean']))
    #             x = (x.max() - x)
    #             x = x + np.random.normal(loc=0, scale=x, size=len(x))
    #             x = x * 0.1
    #             x = (x - x.mean()) + d
    #             ax.scatter(
    #                 x, y, s=8, alpha=0.1, color=colors[color_count], edgecolor='none', label=None
    #             )
    #         color_count += 1
    #     return ax

    # def safe_logistic(x):
    #     x_clamped = np.clip(x, -10, 10)
    #     return 1.0 / (1.0 + np.exp(-x_clamped))

    # def plot_predicted_probabilities(
#         lmm_results: pd.DataFrame, 
#         df_items: pd.DataFrame, 
#         df_long: pd.DataFrame, 
#         groups: dict,
#         model_name: str,
#         pass_num: int,
#         save_folder: str,
#         params: dict,
#     ):

#     """
#     Plots the model-predicted probability of a correct response for an average
#     person on an average item for each factor, now including confidence intervals.
#     """

#     def plot_individual_deviations(
#             df_lmm_long, 
#             df_items, 
#             groups, 
#             lmm_results, 
#             ax=None,
#             colors=None,
#             ):
        

#         # 1) pre-compute a_bar, b_bar per factor
#         bars = {
#         k: (
#             df_items.loc[df_items.index.str.contains('|'.join(v)), 'Overall_Discrimination'].mean(),
#             df_items.loc[df_items.index.str.contains('|'.join(v)), 'Difficulty'].mean()
#         )
#         for k,v in groups.items()
#         }

#         # 2) for every row in df_lmm_long, compute P_i and P_mean
#         df = df_lmm_long.copy()
#         df['a_bar'] = df['Factor'].map(lambda k: bars[k][0])
#         df['b_bar'] = df['Factor'].map(lambda k: bars[k][1])

#         # individual P_i
#         df['P_i'] = 1/(1 + np.exp(-df['a_bar']*(df['Ability']-df['b_bar'])))

#         # mean theta at each row
#         df['mean_theta'] = lmm_results.predict(df)

#         # mean probability at each row
#         df['P_mean'] = 1/(1 + np.exp(-df['a_bar']*(df['mean_theta']-df['b_bar'])))

#         # 3) now group by factor & day to plot violins on df['P_i']
#         #    (which will naturally center on df['P_mean'])
#         color_count = 0
#         for factor in groups:
#             sub = df[df['Factor']==factor]
#             days = sorted(sub['Days'].unique())
#             violins = [sub.loc[sub['Days']==d, 'P_i'].values for d in days]

#             vp = ax.violinplot(violins, positions=days, widths=0.6,
#                             showmeans=False, showmedians=False, showextrema=False)
#             for body in vp['bodies']:
#                 body.set_alpha(0.05)
#                 body.set_facecolor(colors[color_count])
#                 body.set_edgecolor('none')

#             # scatter points, optionally weighted by closeness…
#             for d in days:
#                 y = sub.loc[sub['Days']==d, 'P_i']
#                 x = (abs(y - sub.loc[sub['Days']==d, 'P_mean']))
#                 x = (x.max() - x)
#                 x = x + np.random.normal(loc=0, scale=x, size=len(x))  # Add some jitter
#                 x = x * 0.1
#                 x = (x - x.mean()) + d
#                 ax.scatter(
#                     x,
#                     y,
#                     s=8, alpha=0.1, color=colors[color_count], edgecolor='none', label=None
#                 )
#             color_count += 1

#         return ax

#     fig, ax = plt.subplots(figsize=(10, 6))
#     day_range = np.linspace(df_long['Days'].min(), df_long['Days'].max(), 100)
    
#     # 1. Get the predicted ability (theta) trajectories and their CIs from the LMM
#     is_multi_factor = 'Factor' in df_long.columns and df_long['Factor'].nunique() > 1
#     # factors = df_long['Factor'].unique() if is_multi_factor else list(groups.keys())
#     factors = df_long['Factor'].unique()
    
#     pred_grid = pd.DataFrame([(day, factor) for factor in factors for day in day_range], columns=['Days', 'Factor'])
    
#     model_terms = lmm_results.fe_params.index
#     if any('Days_sq' in term for term in model_terms): pred_grid['Days_sq'] = pred_grid['Days'] ** 2
#     if any('log_Days' in term for term in model_terms): pred_grid['log_Days'] = np.log(pred_grid['Days'] + 1)
        
#     formula_rhs = lmm_results.model.formula.split('~')[1].strip()
#     design_matrix = patsy.dmatrix(formula_rhs, pred_grid, return_type='dataframe')
    
#     # pred_grid['mean_theta'] = lmm_results.predict(exog=design_matrix)
#     pred_grid['mean_theta'] = lmm_results.predict(pred_grid)

#     fe_cov = lmm_results.cov_params().loc[lmm_results.fe_params.index, lmm_results.fe_params.index]
#     design_matrix = design_matrix[fe_cov.columns]
#     pred_var = np.sum((design_matrix @ fe_cov) * design_matrix, axis=1)
#     pred_se = np.sqrt(pred_var)
#     pred_grid['theta_ci_lower'] = pred_grid['mean_theta'] - 1.96 * pred_se
#     pred_grid['theta_ci_upper'] = pred_grid['mean_theta'] + 1.96 * pred_se

#     # 2. Calculate and plot probability for each factor
#     # colors = plt.cm.get_cmap('viridis', len(factors))
#     colors = params.colors if 'colors' in params else plt.cm.get_cmap('viridis', len(factors))

#     for i, factor in enumerate(factors):
#         factor_items = df_items[df_items.index.str.contains('|'.join(groups[factor]))]
#         if factor_items.empty: continue
            
#         avg_discrimination = factor_items['Overall_Discrimination'].mean()
#         avg_difficulty = factor_items['Difficulty'].mean()
        
#         factor_df = pred_grid[pred_grid['Factor'] == factor]
        
#         # Define a function for the logistic transformation
#         def to_prob(theta):
#             logit = -avg_discrimination * (theta - avg_difficulty)
#             return 1 / (1 + np.exp(logit))
        
#         # Apply the transformation to the mean and the CI bounds
#         prob_mean = to_prob(factor_df['mean_theta'])
#         prob_lower = to_prob(factor_df['theta_ci_lower'])
#         prob_upper = to_prob(factor_df['theta_ci_upper'])
#         pred_grid.loc[pred_grid['Factor']==factor, 'P_mean']   = prob_mean
#         pred_grid.loc[pred_grid['Factor']==factor, 'P_lower']  = prob_lower
#         pred_grid.loc[pred_grid['Factor']==factor, 'P_upper']  = prob_upper
        
#         # color = colors(i / (len(factors)-1)) if len(factors) > 1 else colors(0.5)
#         color = colors[i] if 'colors' in params else colors(i / (len(factors)-1)) if len(factors) > 1 else colors(0.5)

#         ax.plot(factor_df['Days'], prob_mean, color=color, linewidth=2.5, label=factor)
#         ax.fill_between(factor_df['Days'], prob_lower, prob_upper, color=color, alpha=params.alpha)

#     ax.set_xlabel(params.x_axis.label)
#     ax.set_ylabel(params.y_axis.label)
#     ax.set_title(f"{params.title} - ({model_name} Model, Pass {pass_num})")

#     if params.y_axis.range:
#         ax.set_ylim(bottom=params.y_axis.range[0], top=params.y_axis.range[1])

#     if params.legend.show:
#         ax.legend(loc=params.legend.location, title=params.legend.title, fontsize=params.legend.fontsize, framealpha=params.legend.framealpha)

#     ax = plot_individual_deviations(
#         df_lmm_long = df_long, 
#         df_items = df_items, 
#         groups = groups, 
#         lmm_results = lmm_results, 
#         ax=ax,
#         colors=colors,
#     )

#     ax.grid(True, linestyle='--', alpha=0.6)
    
#     save_or_show_plot(fig, save_path=f"{save_folder}{params.output.filename}", dpi=params.output.dpi)

# def plot_ability_violins(
#         results_df: pd.DataFrame, 
#         groups: dict, 
#         pass_num: int,
#         save_folder: str,
#         params: dict,
#     ):

#     fig, ax = plt.subplots(figsize=(10, 6))
#     group_labels = list(groups.keys())
#     n_groups = len(group_labels)
#     day_map = {1: 0, 2: 1, 3: 3, 4: 6}
#     day_positions = sorted(day_map.values())
#     total_width = 0.8
#     colors = params.colors if 'colors' in params else plt.cm.get_cmap('viridis', n_groups)

#     width = total_width / n_groups if n_groups > 0 else total_width

#     for i, label in enumerate(group_labels):
#         theta_col = f"Theta_{label}"
#         if theta_col not in results_df.columns: continue
#         all_data = [results_df[results_df['test'] == t][theta_col].dropna().values for t in sorted(day_map.keys())]
#         # positions = [d - total_width/2 + width/2 + i*width for d in day_positions]
#         positions = day_positions # Overlay violins at the same positions
#         valid_data = [d for d in all_data if len(d) > 0]
#         valid_pos = [p for d, p in zip(all_data, positions) if len(d) > 0]
#         if not valid_data: continue
#         vp = ax.violinplot(valid_data, positions=valid_pos, widths=width, showmeans=False, showmedians=False, showextrema=False)
#         color = colors[i] if 'colors' in params else colors(i / (n_groups-1)) if n_groups > 1 else colors(0.5)
#         for pc in vp['bodies']: pc.set_alpha(params.alpha); pc.set_facecolor(color); pc.set_edgecolor('black')
#         ax.plot(valid_pos, [np.mean(d) for d in valid_data], 'o-', color=color, label=label)

#     ax.set_xlabel(params.x_axis.label)
#     ax.set_ylabel(params.y_axis.label)
#     ax.set_title(f"{params.title} - (Pass {pass_num})")
    
#     if params.y_axis.range:
#         ax.set_ylim(bottom=params.y_axis.range[0], top=params.y_axis.range[1])
    
#     ax.set_xticks(day_positions); ax.set_xticklabels([str(d) for d in day_positions])
#     ax.grid(True, linestyle='--', alpha=0.6)
    
#     if params.legend.show:
#         ax.legend(loc=params.legend.location, title=params.legend.title, fontsize=params.legend.fontsize, framealpha=params.legend.framealpha)
    
#     save_or_show_plot(
#         fig, 
#         save_path=f"{save_folder}{params.output.filename}",
#         dpi=params.output.dpi
#     )