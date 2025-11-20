"""
Generic plotting functions for REMEMVR analysis pipeline.

Provides reusable, configurable plotting functions with consistent styling
for trajectory plots, diagnostics, histograms, and IRT probability conversions.

Key Features:
- Loads styling from config/plotting.yaml
- Publication-ready defaults (300 DPI, clear fonts)
- Saves both PNG and CSV data for reproducibility
- Supports grouped visualizations by domain/factor

Functions:
    setup_plot_style() - Apply consistent matplotlib/seaborn styling
    plot_trajectory() - Trajectory with fitted curves + observed errorhars
    plot_diagnostics() - 2x2 diagnostic grid for regression validation
    plot_histogram_by_group() - Grouped histograms
    theta_to_probability() - IRT response function
    save_plot_with_data() - Save PNG + CSV simultaneously

Author: Claude (REMEMVR Project)
Date: 2025-01-08
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from scipy import stats
from typing import List, Optional, Dict, Tuple, Any

from tools.config import load_config


# =============================================================================
# Style Setup
# =============================================================================

def setup_plot_style(config_path: Optional[Path] = None) -> None:
    """
    Apply consistent matplotlib and seaborn styling from config.

    Loads plotting parameters from config/plotting.yaml and applies them
    to matplotlib rcParams. If config not found, uses sensible defaults.

    Args:
        config_path: Optional path to plotting.yaml. If None, uses default.

    Raises:
        None - gracefully falls back to defaults if config missing

    Example:
        >>> setup_plot_style()  # Uses config/plotting.yaml
        >>> plt.plot([0, 1], [0, 1])  # Will use configured style
    """
    # Set seaborn style first (base style)
    sns.set_style("whitegrid")

    # Try to load config
    try:
        if config_path is None:
            config = load_config('plotting')
        else:
            import yaml
            with open(config_path, 'r') as f:
                config = yaml.safe_load(f)
    except (FileNotFoundError, KeyError, Exception):
        # Use defaults if config not found
        config = {
            'dpi': 300,
            'font_size': 11,
            'axes_labelsize': 12,
            'axes_titlesize': 13,
            'legend_fontsize': 10,
            'line_width': 2.5,
            'marker_size': 8
        }

    # Apply matplotlib rcParams
    plt.rcParams['figure.dpi'] = config.get('dpi', 300)
    plt.rcParams['font.size'] = config.get('font_size', 11)
    plt.rcParams['axes.labelsize'] = config.get('axes_labelsize', 12)
    plt.rcParams['axes.titlesize'] = config.get('axes_titlesize', 13)
    plt.rcParams['legend.fontsize'] = config.get('legend_fontsize', 10)


# =============================================================================
# Trajectory Plotting
# =============================================================================

def plot_trajectory(
    time_pred: np.ndarray,
    fitted_curves: Dict[str, np.ndarray],
    observed_data: pd.DataFrame,
    time_col: str = 'Time',
    value_col: str = 'Value',
    group_col: str = 'Group',
    xlabel: str = 'Time',
    ylabel: str = 'Value',
    title: str = 'Trajectory Plot',
    colors: Optional[Dict[str, str]] = None,
    figsize: Tuple[int, int] = (10, 6),
    output_path: Optional[Path] = None,
    show_errorbar: bool = True,
    annotation: Optional[str] = None
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Create trajectory plot with fitted curves and observed data points.

    Plots smooth fitted trajectories (lines) alongside observed data points
    with error bars (mean ± SEM). Useful for visualizing forgetting curves,
    growth curves, or any longitudinal data.

    Args:
        time_pred: Time points for fitted curve (1D array, e.g., np.linspace(0, 6, 100))
        fitted_curves: Dict mapping group names to fitted values {group: array}
        observed_data: DataFrame with observed data (long format)
        time_col: Column name for time variable in observed_data
        value_col: Column name for observed values
        group_col: Column name for grouping variable (e.g., 'Domain', 'Factor')
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Plot title
        colors: Optional dict mapping groups to colors {group: hex_color}
        figsize: Figure size (width, height) in inches
        output_path: Optional path to save plot
        show_errorbar: Whether to show error bars (default True)
        annotation: Optional text annotation (placed bottom-left)

    Returns:
        fig: Matplotlib figure
        ax: Matplotlib axes

    Example:
        >>> time_pred = np.linspace(0, 6, 100)
        >>> fitted = {'What': 0.5 - 0.1*time_pred, 'Where': 0.4 - 0.08*time_pred}
        >>> observed = pd.DataFrame({'Time': [0,1,3,6]*2, 'Value': [...], 'Group': [...]})
        >>> fig, ax = plot_trajectory(time_pred, fitted, observed)
    """
    # Calculate observed statistics (mean ± SEM per group × time)
    observed_stats = observed_data.groupby([group_col, time_col]).agg(
        mean=( value_col, 'mean'),
        sem=(value_col, lambda x: x.std() / np.sqrt(len(x))),
        n=(value_col, 'count')
    ).reset_index()

    # Get default colors if not provided
    if colors is None:
        try:
            config = load_config('plotting')
            colors = config.get('colors', {
                'What': '#E74C3C',
                'Where': '#3498DB',
                'When': '#2ECC71'
            })
        except:
            # Fallback colors
            colors = {
                'What': '#E74C3C',
                'Where': '#3498DB',
                'When': '#2ECC71'
            }

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot each group
    for group, fitted_values in fitted_curves.items():
        color = colors.get(group, None)  # None uses default matplotlib color cycle

        # Plot fitted trajectory (smooth curve)
        ax.plot(time_pred, fitted_values,
                color=color, linewidth=2.5, label=f'{group} (fitted)',
                alpha=0.9)

        # Plot observed data points (mean ± SEM)
        group_data = observed_stats[observed_stats[group_col] == group]

        if show_errorbar and len(group_data) > 0:
            ax.errorbar(group_data[time_col], group_data['mean'],
                        yerr=group_data['sem'],
                        fmt='o', color=color, markersize=8,
                        capsize=5, capthick=2, alpha=0.7,
                        label=f'{group} (observed)')

    # Formatting
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)
    ax.legend(loc='upper right', framealpha=0.95)
    ax.grid(True, alpha=0.3)

    # Add annotation if provided
    if annotation:
        ax.text(0.02, 0.02, annotation,
                transform=ax.transAxes,
                fontsize=9, style='italic',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.3),
                verticalalignment='bottom')

    plt.tight_layout()

    # Save if output path provided
    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')

    return fig, ax


# =============================================================================
# Diagnostic Plotting
# =============================================================================

def plot_diagnostics(
    df: pd.DataFrame,
    fitted_col: str = 'fitted',
    residuals_col: str = 'residuals',
    group_col: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 10),
    output_path: Optional[Path] = None
) -> Tuple[plt.Figure, np.ndarray]:
    """
    Create 2x2 diagnostic plot grid for regression model validation.

    Creates four diagnostic plots:
    - (A) Residuals vs Fitted: Check linearity and homoscedasticity
    - (B) Q-Q Plot: Check normality of residuals
    - (C) Scale-Location: Check homoscedasticity with sqrt(|residuals|)
    - (D) Residuals by Group: Check group-level distributions

    Args:
        df: DataFrame with fitted values and residuals
        fitted_col: Column name for fitted values
        residuals_col: Column name for residuals
        group_col: Optional column name for grouping (e.g., 'Domain')
        figsize: Figure size (width, height) in inches
        output_path: Optional path to save plot

    Returns:
        fig: Matplotlib figure
        axes: 2x2 array of axes

    Example:
        >>> df = pd.DataFrame({'fitted': [...], 'residuals': [...], 'group': [...]})
        >>> fig, axes = plot_diagnostics(df)
    """
    fig, axes = plt.subplots(2, 2, figsize=figsize)

    # (A) Residuals vs Fitted
    ax = axes[0, 0]
    ax.scatter(df[fitted_col], df[residuals_col], alpha=0.4, s=10)
    ax.axhline(y=0, color='red', linestyle='--', linewidth=1.5)
    ax.set_xlabel('Fitted Values')
    ax.set_ylabel('Residuals')
    ax.set_title('(A) Residuals vs Fitted', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Add lowess smooth
    try:
        sorted_idx = np.argsort(df[fitted_col])
        fitted_sorted = df[fitted_col].iloc[sorted_idx]
        resid_sorted = df[residuals_col].iloc[sorted_idx]

        window = min(51, len(fitted_sorted) // 10 * 2 + 1)  # Ensure odd
        if window >= 3:
            smooth = pd.Series(resid_sorted).rolling(window=window, center=True).mean()
            ax.plot(fitted_sorted, smooth, color='blue', linewidth=2, alpha=0.8)
    except Exception:
        pass  # Skip smooth if it fails

    # (B) Q-Q Plot (Normality of residuals)
    ax = axes[0, 1]
    stats.probplot(df[residuals_col], dist="norm", plot=ax)
    ax.set_title('(B) Normal Q-Q Plot', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # (C) Scale-Location (Homoscedasticity)
    ax = axes[1, 0]
    sqrt_abs_resid = np.sqrt(np.abs(df[residuals_col]))
    ax.scatter(df[fitted_col], sqrt_abs_resid, alpha=0.4, s=10)
    ax.set_xlabel('Fitted Values')
    ax.set_ylabel('√|Residuals|')
    ax.set_title('(C) Scale-Location', fontweight='bold')
    ax.grid(True, alpha=0.3)

    # Add smooth
    try:
        window = min(51, len(fitted_sorted) // 10 * 2 + 1)
        if window >= 3:
            sorted_idx = np.argsort(df[fitted_col])
            fitted_sorted = df[fitted_col].iloc[sorted_idx]
            sqrt_resid_sorted = sqrt_abs_resid.iloc[sorted_idx]
            smooth = pd.Series(sqrt_resid_sorted).rolling(window=window, center=True).mean()
            ax.plot(fitted_sorted, smooth, color='red', linewidth=2, alpha=0.8)
    except Exception:
        pass

    # (D) Residuals by Group (if group_col provided)
    ax = axes[1, 1]
    if group_col and group_col in df.columns:
        # Get colors
        try:
            config = load_config('plotting')
            colors = config.get('colors', {})
        except:
            colors = {}

        for group in df[group_col].unique():
            group_resid = df[df[group_col] == group][residuals_col]
            color = colors.get(group, None)
            ax.hist(group_resid, alpha=0.5, bins=30, label=str(group), color=color)

        ax.set_xlabel('Residuals')
        ax.set_ylabel('Frequency')
        ax.set_title('(D) Residuals Distribution by Group', fontweight='bold')
        ax.legend()
    else:
        # Overall histogram if no groups
        ax.hist(df[residuals_col], bins=30, alpha=0.7, edgecolor='black')
        ax.set_xlabel('Residuals')
        ax.set_ylabel('Frequency')
        ax.set_title('(D) Residuals Distribution', fontweight='bold')

    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')

    return fig, axes


# =============================================================================
# Histogram Plotting
# =============================================================================

def plot_histogram_by_group(
    df: pd.DataFrame,
    value_col: str,
    group_col: str,
    xlabel: str = 'Value',
    ylabel: str = 'Frequency',
    title: str = 'Histogram by Group',
    bins: int = 20,
    colors: Optional[Dict[str, str]] = None,
    figsize: Tuple[int, int] = (10, 6),
    output_path: Optional[Path] = None,
    vline: Optional[float] = None,
    vline_label: Optional[str] = None
) -> Tuple[plt.Figure, plt.Axes]:
    """
    Create grouped histogram with overlapping distributions.

    Args:
        df: DataFrame with values and groups
        value_col: Column name for values to histogram
        group_col: Column name for grouping variable
        xlabel: X-axis label
        ylabel: Y-axis label
        title: Plot title
        bins: Number of histogram bins
        colors: Optional dict mapping groups to colors
        figsize: Figure size (width, height)
        output_path: Optional path to save plot
        vline: Optional x-coordinate for vertical reference line
        vline_label: Optional label for vertical line

    Returns:
        fig: Matplotlib figure
        ax: Matplotlib axes

    Example:
        >>> df = pd.DataFrame({'Value': [...], 'Group': ['What', 'Where', 'When']})
        >>> fig, ax = plot_histogram_by_group(df, 'Value', 'Group')
    """
    # Get default colors if not provided
    if colors is None:
        try:
            config = load_config('plotting')
            colors = config.get('colors', {})
        except:
            colors = {}

    # Create figure
    fig, ax = plt.subplots(figsize=figsize)

    # Plot histogram for each group
    for group in df[group_col].unique():
        group_data = df[df[group_col] == group][value_col]
        color = colors.get(group, None)

        ax.hist(group_data, alpha=0.6, bins=bins,
                label=f'{group} (n={len(group_data)})',
                color=color)

    # Formatting
    ax.set_xlabel(xlabel, fontweight='bold')
    ax.set_ylabel(ylabel, fontweight='bold')
    ax.set_title(title, fontweight='bold', pad=15)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # Add vertical line if specified
    if vline is not None:
        ax.axvline(x=vline, color='black', linestyle='--', linewidth=1, alpha=0.5)
        if vline_label:
            ax.text(vline + 0.1, ax.get_ylim()[1] * 0.95, vline_label,
                    fontsize=9, style='italic')

    plt.tight_layout()

    if output_path:
        fig.savefig(output_path, dpi=300, bbox_inches='tight')

    return fig, ax


# =============================================================================
# IRT Utilities
# =============================================================================

def theta_to_probability(
    theta: np.ndarray,
    discrimination: float,
    difficulty: float
) -> np.ndarray:
    """
    Convert IRT ability (theta) to probability of correct response.

    Uses the 2-parameter logistic (2PL) IRT response function:
        P(correct) = 1 / (1 + exp(-(a * (θ - b))))

    where:
        θ (theta) = ability
        a = discrimination (how well item differentiates ability levels)
        b = difficulty (ability level at which P=0.5)

    Args:
        theta: Ability parameter (scalar or array)
        discrimination: Item discrimination parameter (a > 0)
        difficulty: Item difficulty parameter (b, can be any real number)

    Returns:
        prob: Probability of correct response (0 to 1)

    Example:
        >>> theta = np.array([-2, -1, 0, 1, 2])
        >>> prob = theta_to_probability(theta, discrimination=1.5, difficulty=0.0)
        >>> print(prob)  # [0.047, 0.18, 0.5, 0.82, 0.953]

    Note:
        - When θ = b, P ≈ 0.5
        - Higher discrimination = steeper response curve
        - This function is vectorized (works with numpy arrays)
    """
    # Ensure numpy array for vectorization
    theta = np.asarray(theta)

    # IRT 2PL response function
    prob = 1 / (1 + np.exp(-(discrimination * (theta - difficulty))))

    return prob


# =============================================================================
# Save Utilities
# =============================================================================

def save_plot_with_data(
    fig: plt.Figure,
    output_path: Path,
    data: Optional[pd.DataFrame] = None,
    dpi: int = 300
) -> None:
    """
    Save plot as PNG and optionally save associated data as CSV.

    Saves matplotlib figure and corresponding data for reproducibility.
    CSV is saved with same name as PNG but .csv extension.

    Args:
        fig: Matplotlib figure to save
        output_path: Path for PNG file (e.g., "trajectory.png")
        data: Optional DataFrame to save as CSV
        dpi: DPI for PNG output (default 300 for publication quality)

    Example:
        >>> fig, ax = plt.subplots()
        >>> ax.plot([0, 1, 2], [0, 1, 4])
        >>> data = pd.DataFrame({'x': [0,1,2], 'y': [0,1,4]})
        >>> save_plot_with_data(fig, Path("plot.png"), data)
        # Saves: plot.png and plot.csv
    """
    # Ensure Path object
    output_path = Path(output_path)

    # Create output directory if needed
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # Save figure
    fig.savefig(output_path, dpi=dpi, bbox_inches='tight')

    # Save data if provided
    if data is not None:
        csv_path = output_path.with_suffix('.csv')
        data.to_csv(csv_path, index=False)


def plot_trajectory_probability(
    df_thetas: pd.DataFrame,
    item_parameters_path: Path,
    time_var: str = 'test',
    factors: List[str] = None,
    title: str = "Memory Trajectory (Probability Scale)",
    **kwargs
) -> Tuple[plt.Figure, plt.Axes, pd.DataFrame]:
    """
    Plot trajectory with theta transformed to probability scale (Decision D069).

    Implements dual-scale trajectory plotting:
    - Theta scale: Statistical rigor, psychometrician-interpretable
    - Probability scale: General audience interpretable, reviewer-friendly

    Uses IRT 2PL transformation: P = 1 / (1 + exp(-(a * (θ - b))))
    where:
    - a = mean discrimination from Pass 2 item parameters
    - b = 0 (reference difficulty)
    - θ = theta scores

    Args:
        df_thetas: DataFrame with theta scores (long format)
                   Must contain: UID, {time_var}, {factor}_Theta columns
        item_parameters_path: Path to item_parameters.csv (Pass 2 output)
        time_var: Time variable column name (default: 'test')
        factors: List of factor names to plot (default: infer from columns)
        title: Plot title
        **kwargs: Additional arguments passed to plot_trajectory()

    Returns:
        Tuple of:
        - fig: Matplotlib figure
        - ax: Matplotlib axes
        - prob_data: DataFrame with probability-transformed scores

    Example:
        ```python
        fig, ax, prob_data = plot_trajectory_probability(
            df_thetas=df_thetas,
            item_parameters_path=Path("data/item_parameters.csv"),
            time_var='Days',
            factors=['What', 'Where', 'When']
        )
        ```

    Decision D069 Context:
        Dual-scale reporting enhances interpretability without sacrificing rigor.
        Theta scale preserves statistical properties (IRT estimates), while probability
        scale provides intuitive metric (0-100% correct) for general audience.
    """
    print("\n" + "=" * 60)
    print("PROBABILITY-SCALE TRAJECTORY PLOT (Decision D069)")
    print("=" * 60)

    # Read item parameters to get mean discrimination
    df_items = pd.DataFrame(pd.read_csv(item_parameters_path))

    # Calculate mean discrimination across all items
    mean_a = df_items['a'].mean()
    print(f"Mean item discrimination: {mean_a:.3f}")

    # Infer factors if not provided
    if factors is None:
        factors = [col.replace('_Theta', '') for col in df_thetas.columns if col.endswith('_Theta')]

    print(f"Transforming factors: {factors}")

    # Transform theta to probability
    prob_data = df_thetas.copy()

    for factor in factors:
        theta_col = f'{factor}_Theta'
        prob_col = f'{factor}_Probability'

        if theta_col not in df_thetas.columns:
            print(f"  Warning: {theta_col} not found in data. Skipping.")
            continue

        # IRT 2PL transformation: P = 1 / (1 + exp(-(a * (θ - b))))
        # Using b=0 (reference difficulty)
        theta = df_thetas[theta_col]
        probability = 1 / (1 + np.exp(-(mean_a * theta)))

        # Convert to percentage scale (0-100%)
        prob_data[prob_col] = probability * 100

        print(f"  {factor}: θ range [{theta.min():.2f}, {theta.max():.2f}] → P% range [{prob_data[prob_col].min():.1f}%, {prob_data[prob_col].max():.1f}%]")

    # Rename Probability columns to match plot_trajectory expectations
    # plot_trajectory expects columns like {factor}_Theta
    prob_data_renamed = prob_data.copy()
    for factor in factors:
        prob_col = f'{factor}_Probability'
        theta_col = f'{factor}_Theta'
        if prob_col in prob_data.columns:
            prob_data_renamed[theta_col] = prob_data[prob_col]

    # Call plot_trajectory with probability-transformed data
    fig, ax = plot_trajectory(
        df_long=prob_data_renamed,
        time_var=time_var,
        factors=factors,
        title=title,
        ylabel="Probability Correct (%)",
        ylim=(0, 100),
        **kwargs
    )

    print("=" * 60 + "\n")

    return fig, ax, prob_data
