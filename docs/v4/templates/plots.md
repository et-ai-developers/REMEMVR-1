# plots.md - Plotting Specifications Template (v4.X)

**Version:** 1.0.0
**Last Updated:** 2025-11-17
**Purpose:** Plotting specifications and requirements for rq_plots agent
**Audience:** rq_plots agent when generating plots.py
**Template Type:** Comprehensive (function catalog + D069 validation + TDD naming)

---

## OVERVIEW

This template provides the **plotting specifications** for the rq_plots agent. The agent generates `results/chX/rqY/plots/plots.py` that **ONLY calls existing functions** from `tools/plotting.py` - NEVER creates new plotting functions.

**v4.X Design Philosophy:**
- **Consistency across 50 RQs:** All plots use same themes, colors, styles
- **Source code reading:** Agent reads `tools/plotting.py` directly (step 5) to learn function APIs
- **Fail-fast validation:** If required function missing from tools/plotting.py → FAIL immediately (no code generation)
- **User adds missing functions:** Master and user manually add to tools/plotting.py, then retry

**Purpose of This Template:**
- Document available plotting functions (summary + key parameters)
- Specify Decision D069 requirements (MANDATORY dual-scale trajectory plots)
- Define output format standards (PNG, DPI, dimensions, colors)
- Provide file naming guidance (TDD - conventions emerge from RQ 5.1)

**NOTE:** Agent reads `tools/plotting.py` source code for complete function signatures. This template provides essential guidance + critical requirements (D069).

---

## RQ_PLOTS AGENT WORKFLOW INTEGRATION

**How rq_plots uses this template:**

```
Step 1: Read docs/v4/agent_best_practices.md
Step 2: Read results/chX/rqY/status.yaml
Step 3: Check prior steps = success, this step = pending
Step 4: Read docs/v4/templates/plots.md (THIS FILE)
Step 5: Read tools/plotting.py (SOURCE CODE - learns full signatures)
Step 6: Read/Bash specified data files (pandas.head to inspect)
Step 7: Ultrathink - generate plots.py using ONLY existing functions
Step 8: Check all required functions exist in tools/plotting.py (else FAIL)
Step 9-10: Create and write plots.py
Step 11: Update status.yaml
Step 12: Report success
```

**Critical Step 8: Function Existence Validation**

IF any required function missing from tools/plotting.py:
- **FAIL immediately** with missing function list
- **DO NOT generate code** (no hallucinated alternatives)
- **Master invokes user:** Add missing function to tools/plotting.py manually
- **Retry rq_plots:** Succeeds with complete function set

**Why This Works:**
- Prevents inconsistent plot themes (all RQs use same functions)
- Prevents API hallucination (agent can't guess parameters)
- Maintains code quality (functions in tools/ are tested, production-ready)
- Enables systematic improvement (add function once, use in all 50 RQs)

---

## SECTION 1: AVAILABLE PLOTTING FUNCTIONS

**Source:** `tools/plotting.py` (Production-ready, tested functions)

**NOTE:** This section provides **summary + key parameters**. For complete function signatures with all parameters, types, and defaults, see:
1. `tools/plotting.py` source code (agent reads this in step 5)
2. `docs/tools_inventory.md` lines 342-421 (complete API documentation)

---

### Function 1.1: setup_plot_style()

**Purpose:** Apply consistent matplotlib/seaborn styling to all plots

**Signature Summary:**
```python
def setup_plot_style(config_path: Optional[Path] = None) -> None
```

**Key Parameters:**
- `config_path` (Optional[Path]): Path to plotting config YAML. Default: `config/plotting.yaml`

**Behavior:**
- Loads styling parameters from config/plotting.yaml
- Sets DPI=300 (publication quality)
- Configures font sizes, line widths, marker sizes
- Applies seaborn theme for consistent aesthetics

**Usage Pattern:**
```python
# Call ONCE at start of plots.py
from tools.plotting import setup_plot_style
setup_plot_style()  # Loads defaults from config/plotting.yaml

# Then generate all plots with consistent styling
```

**Returns:** None (configures global matplotlib/seaborn settings)

**Source Reference:** tools/plotting.py lines 40-86

---

### Function 1.2: plot_trajectory()

**Purpose:** PRIMARY trajectory plotting function (theta-scale or general trajectories)

**Signature Summary:**
```python
def plot_trajectory(
    time_pred: np.ndarray,
    fitted_curves: Dict[str, np.ndarray],
    observed_data: pd.DataFrame,
    # ... plus 10 optional parameters (xlabel, ylabel, title, colors, etc.)
) -> Tuple[plt.Figure, plt.Axes]
```

**Key Parameters:**
- `time_pred` (np.ndarray): X-axis values for fitted curves (e.g., TSVR hours or nominal days)
- `fitted_curves` (Dict[str, np.ndarray]): {group_name: predicted_values} for each trajectory curve
- `observed_data` (pd.DataFrame): Raw data with time, value, and group columns
- `time_col` (str): Column name for time variable (default: "Time")
- `value_col` (str): Column name for outcome variable (default: "Value")
- `group_col` (str): Column name for grouping (default: "Group")
- `xlabel`, `ylabel`, `title` (str): Axis labels and plot title
- `colors` (Optional[Dict[str, str]]): {group_name: hex_color} mapping
- `figsize` (Tuple[int, int]): Figure dimensions in inches (default: (10, 6))
- `output_path` (Optional[Path]): Where to save PNG (if None, returns figure without saving)
- `show_errorbar` (bool): Show error bars for observed data (default: True)

**Behavior:**
- Plots fitted curves (smooth lines from LMM predictions)
- Overlays observed data points with error bars (mean ± SEM)
- Applies color scheme per group
- Saves PNG at output_path if specified

**Usage Context:**
- **General trajectories:** Use for any time-series plotting
- **Theta-scale trajectories:** Use for IRT theta outcome (y-axis: -3 to +3)
- **NOTE:** For probability-scale trajectories, use `plot_trajectory_probability()` (Decision D069)

**Returns:** (plt.Figure, plt.Axes) - figure and axes objects

**Source Reference:** tools/plotting.py lines 92-208

**Used By RQs:** 5.2.1, 5.2.2, 5.3.1, 5.3.2, 5.4.1, 5.4.2, 5.1.2, 5.2.4, 5.1.6 (9 RQs documented in tools_inventory.md)

---

### Function 1.3: plot_trajectory_probability() ⚠️ DECISION D069

**Purpose:** Dual-scale trajectory plotting - transforms theta to probability scale

**Signature Summary:**
```python
def plot_trajectory_probability(
    df_thetas: pd.DataFrame,
    item_parameters_path: Path,
    time_var: str = 'test',
    factors: List[str] = None,
    title: str = "Memory Trajectory (Probability Scale)",
    **kwargs  # Additional args passed to plot_trajectory()
) -> Tuple[plt.Figure, plt.Axes, pd.DataFrame]
```

**Key Parameters:**
- `df_thetas` (pd.DataFrame): Theta scores with time variable and grouping factors
- `item_parameters_path` (Path): Path to Pass 2 IRT item_parameters.csv (for discrimination parameter)
- `time_var` (str): Time column name (default: "test", can be "TSVR" per D070)
- `factors` (List[str]): Grouping factor columns (e.g., ["domain", "condition"])
- `title` (str): Plot title
- `**kwargs`: Additional args passed to `plot_trajectory()` (xlabel, ylabel, figsize, colors, etc.)

**Behavior:**
- Reads Pass 2 item parameters to extract mean discrimination
- Transforms theta → probability using IRT 2PL formula: P = 1/(1 + exp(-(a*(θ-b))))
  - a = mean discrimination from item_parameters.csv
  - b = 0 (reference difficulty)
  - θ = theta scores
- Calls `plot_trajectory()` with probability-transformed data
- Y-axis scaled 0% to 100% (interpretability for non-psychometricians)

**CRITICAL - Decision D069:**
This function implements **Decision D069: Dual-Scale Trajectory Plotting**.

**MANDATORY** for RQs with LMM trajectory analyses (~40 of 50 RQs). See Section 2 for complete D069 specification.

**Returns:** (plt.Figure, plt.Axes, pd.DataFrame) - figure, axes, and probability-transformed dataframe

**Source Reference:** tools/plotting.py lines 511-622

**See Also:** Section 2 (Decision D069 dedicated section with validation checklist)

---

### Function 1.4: plot_diagnostics()

**Purpose:** 2x2 diagnostic grid for regression model validation

**Signature Summary:**
```python
def plot_diagnostics(
    df: pd.DataFrame,
    fitted_col: str = 'fitted',
    residuals_col: str = 'residuals',
    group_col: Optional[str] = None,
    figsize: Tuple[int, int] = (12, 10),
    output_path: Optional[Path] = None
) -> Tuple[plt.Figure, np.ndarray]
```

**Key Parameters:**
- `df` (pd.DataFrame): DataFrame with fitted values and residuals
- `fitted_col` (str): Column name for fitted values (default: "fitted")
- `residuals_col` (str): Column name for residuals (default: "residuals")
- `group_col` (Optional[str]): Column for grouping in distributions subplot
- `figsize` (Tuple[int, int]): Figure dimensions (default: (12, 10) for 2x2 grid)
- `output_path` (Optional[Path]): Where to save PNG

**Behavior:**
Creates 2x2 diagnostic subplot grid:
1. **Top-left:** Residuals vs Fitted (homoscedasticity check)
2. **Top-right:** Q-Q Plot (normality check)
3. **Bottom-left:** Scale-Location Plot (variance homogeneity)
4. **Bottom-right:** Residuals by Group (if group_col specified)

**Usage Context:**
- Validate LMM assumptions (normality, homoscedasticity)
- Identify outliers or model misspecification
- Required for publication-quality regression analyses

**Returns:** (plt.Figure, np.ndarray) - figure and array of 4 axes objects

**Source Reference:** tools/plotting.py lines 215-332

---

### Function 1.5: plot_histogram_by_group()

**Purpose:** Grouped histograms with optional reference line

**Signature Summary:**
```python
def plot_histogram_by_group(
    df: pd.DataFrame,
    value_col: str,
    group_col: str,
    # ... plus 8 optional parameters
) -> Tuple[plt.Figure, plt.Axes]
```

**Key Parameters:**
- `df` (pd.DataFrame): Data to plot
- `value_col` (str): Column for histogram values
- `group_col` (str): Column for grouping (overlaid histograms per group)
- `xlabel`, `ylabel`, `title` (str): Axis labels and title
- `bins` (int): Number of histogram bins (default: 20)
- `colors` (Optional[Dict[str, str]]): {group_name: hex_color} mapping
- `figsize` (Tuple[int, int]): Figure dimensions (default: (10, 6))
- `output_path` (Optional[Path]): Where to save PNG
- `vline` (Optional[float]): X-coordinate for vertical reference line (e.g., chance level)
- `vline_label` (Optional[str]): Label for vline

**Behavior:**
- Overlays histograms per group with transparency
- Color-codes by group (uses default color scheme or custom colors)
- Adds vertical reference line if vline specified (useful for chance-level marking)

**Usage Context:**
- Compare distributions across groups (What/Where/When domains)
- Visualize theta score distributions
- Show effect size distributions with reference lines

**Returns:** (plt.Figure, plt.Axes)

**Source Reference:** tools/plotting.py lines 339-417

---

### Function 1.6: theta_to_probability()

**Purpose:** Convert IRT theta scores to probability scale (utility function)

**Signature Summary:**
```python
def theta_to_probability(
    theta: np.ndarray,
    discrimination: float,
    difficulty: float
) -> np.ndarray
```

**Key Parameters:**
- `theta` (np.ndarray): Theta scores from IRT calibration
- `discrimination` (float): IRT discrimination parameter (a)
- `difficulty` (float): IRT difficulty parameter (b)

**Behavior:**
- Applies 2PL IRT response function: P = 1/(1 + exp(-(a*(θ-b))))
- Vectorized operation (handles arrays efficiently)

**Usage Context:**
- Used internally by `plot_trajectory_probability()` for D069 implementation
- Can be called directly for custom probability transformations
- Enables interpretability of theta-scale results

**Returns:** np.ndarray of probability values (0 to 1)

**Source Reference:** tools/plotting.py lines 424-464

**See Also:** `plot_trajectory_probability()` (primary usage context)

---

### Function 1.7: save_plot_with_data()

**Purpose:** Save plot as PNG + accompanying CSV for reproducibility

**Signature Summary:**
```python
def save_plot_with_data(
    fig: plt.Figure,
    output_path: Path,
    data: Optional[pd.DataFrame] = None,
    dpi: int = 300
) -> None
```

**Key Parameters:**
- `fig` (plt.Figure): Matplotlib figure object to save
- `output_path` (Path): PNG output path (CSV saved with .csv extension)
- `data` (Optional[pd.DataFrame]): Plot data to save as CSV
- `dpi` (int): PNG resolution (default: 300 for publication quality)

**Behavior:**
- Saves PNG: `output_path` (e.g., `plots/trajectory_theta.png`)
- Saves CSV: `output_path.with_suffix('.csv')` (e.g., `plots/trajectory_theta.csv`)
- CSV contains raw plot data for reproducibility and replotting

**Usage Context:**
- Publication-quality plots (300 DPI)
- Reproducibility requirement (data + visualization)
- Enables replotting without re-running analysis

**Returns:** None (saves files to disk)

**Source Reference:** tools/plotting.py lines 471-508

**Best Practice:** Use for ALL plots to ensure reproducibility

---

## SECTION 2: DECISION D069 - DUAL-SCALE TRAJECTORY PLOTS ⚠️ MANDATORY

**Decision Date:** 2025-11-14
**Scope:** ALL RQs with LMM trajectory analyses (~40 of 50 RQs)
**Status:** MANDATORY (rejection criteria if missing)
**Source:** `docs/project_specific_stats_insights.md` lines 410-649

---

### 2.1 Decision Summary

**Problem:**
- IRT theta scale (-3 to +3) is abstract for non-psychometricians
- Thesis audience includes clinicians, neuroscientists, general psychologists
- Probability scale (0% to 100% correct) more interpretable
- Mixed audience requires BOTH statistical rigor AND accessibility

**Solution: Dual-Scale Trajectory Plotting**

**MANDATORY Requirements:**
1. **BOTH plots required:**
   - Theta-scale plot: `plot_trajectory()` with y-axis: -3 to +3
   - Probability-scale plot: `plot_trajectory_probability()` with y-axis: 0% to 100%

2. **Identical trajectory patterns:**
   - Both plots show same trajectory shape
   - Only y-axis scaling differs
   - X-axis identical (TSVR or nominal days per D070)

3. **File naming:**
   - Theta plot: `{prefix}_theta.png` (e.g., `trajectory_theta.png`)
   - Probability plot: `{prefix}_probability.png` (e.g., `trajectory_probability.png`)

4. **Config.yaml specification:**
   ```yaml
   trajectory_plots:
     probability_scale:
       enabled: true
       discrimination_source: "Pass 2 IRT item parameters (mean a)"
       difficulty_reference: 0  # b = 0 reference
   ```

---

### 2.2 IRT Transformation Formula

**From theta (θ) to probability P(correct):**

```
P(correct) = 1 / (1 + exp(-(a * (θ - b))))

where:
  θ = theta score (from IRT calibration)
  a = discrimination parameter (mean from Pass 2 item_parameters.csv)
  b = difficulty reference (typically 0 for standardized theta)
```

**Implementation:**
- Use `plot_trajectory_probability()` function (Section 1.3)
- Reads `item_parameters_path` to extract mean discrimination
- Automatically applies transformation and plots

---

### 2.3 Validation Checklist (7 Items) ⚠️ MANDATORY

**For rq_plots agent and master:**

When generating plots.py for RQs with LMM trajectory analyses, verify:

- [ ] **Both plots specified:** Theta-scale AND probability-scale plots included in plots.py
- [ ] **Transformation formula documented:** Config.yaml or code comments explain P = 1/(1 + exp(-(a*(θ-b))))
- [ ] **Discrimination parameter sourced:** Mean discrimination from Pass 2 IRT item_parameters.csv
- [ ] **Difficulty reference specified:** b = 0 or mean from Pass 2 (documented)
- [ ] **Config.yaml compliance:** trajectory_plots.probability_scale.enabled = true
- [ ] **File naming consistent:** {prefix}_theta.png and {prefix}_probability.png
- [ ] **Interpretation includes probability scale:** Results summary.md Section 3 (Interpretation) has dedicated "Dual-Scale Trajectory Interpretation" subsection per results.md template with:
  - Theta scale findings (SD units, effect sizes, statistical interpretation)
  - Probability scale findings (percentage points, performance likelihood, practical interpretation)
  - Clinical significance discussion (real-world impact, accessibility for non-psychometricians)
  - Justification for both scales (rigor + interpretability balance)

**Rejection Criterion:**
- IF probability-scale plot missing → **REJECT specification** (incomplete D069 compliance)
- IF transformation formula not documented → **CONDITIONAL** (add documentation)
- IF config.yaml missing probability settings → **CONDITIONAL** (add config)

---

### 2.4 Example Usage (plots.py)

```python
# Dual-scale trajectory plotting per Decision D069

from pathlib import Path
import pandas as pd
from tools.plotting import setup_plot_style, plot_trajectory, plot_trajectory_probability

# Setup consistent styling
setup_plot_style()

# Load data
df_thetas = pd.read_csv("data/theta_scores_with_tsvr.csv")
item_params_path = Path("data/pass2_item_parameters.csv")

# Plot 1: Theta-scale trajectory
# (Standard IRT theta scale: -3 to +3)
fig_theta, ax_theta = plot_trajectory(
    time_pred=time_pred_array,  # From LMM predictions
    fitted_curves={"What": what_pred, "Where": where_pred, "When": when_pred},
    observed_data=df_thetas,
    time_col="TSVR",  # Decision D070: Use TSVR not nominal days
    value_col="theta",
    group_col="domain",
    xlabel="Hours Since Encoding (TSVR)",
    ylabel="Memory Ability (Theta)",
    title="Memory Trajectory - Theta Scale",
    figsize=(10, 6),
    output_path=Path("plots/trajectory_theta.png")
)

# Plot 2: Probability-scale trajectory (Decision D069)
# (Interpretable probability scale: 0% to 100%)
fig_prob, ax_prob, df_prob = plot_trajectory_probability(
    df_thetas=df_thetas,
    item_parameters_path=item_params_path,  # Extracts mean discrimination
    time_var="TSVR",
    factors=["domain"],
    title="Memory Trajectory - Probability Scale",
    xlabel="Hours Since Encoding (TSVR)",
    ylabel="Probability Correct (%)",
    figsize=(10, 6),
    output_path=Path("plots/trajectory_probability.png")
)

# BOTH plots now saved: trajectory_theta.png + trajectory_probability.png
# D069 compliance achieved
```

---

### 2.5 When D069 Applies

**MANDATORY for:**
- RQs with LMM trajectory analyses (theta as outcome over time)
- Estimated: ~40 of 50 RQs (Chapters 5, 6, 7 trajectory-focused)

**NOT required for:**
- RQs without trajectory analyses (e.g., cross-sectional comparisons)
- RQs using CTT outcomes (not theta-based)
- Diagnostic plots (plot_diagnostics)
- Histograms (plot_histogram_by_group)

**Check 2_plan.md:**
- IF plan.md specifies "LMM trajectory" or "theta over time" → D069 applies
- IF plan.md mentions "plot_trajectory()" → check if probability-scale also needed

---

### 2.6 Rationale (Why Both Scales Mandatory)

**Theta Scale:**
- Statistical rigor preserved
- LMM coefficients interpretable (standardized effect sizes)
- Psychometrically sound (latent variable modeling)
- Required for technical audience (psychometricians, methodologists)

**Probability Scale:**
- Interpretability enhanced (% correct is intuitive)
- Clinical significance clearer (e.g., "memory drops from 80% to 60%")
- Accessible to non-psychometricians (clinicians, neuroscientists)
- Publication requirement (mixed-audience journals)

**Both Required:**
- Thesis committee has mixed expertise (psychometrics + neuroscience)
- Publication targets mixed-audience journals
- Reproducibility (other researchers can interpret results)
- Comprehensive reporting (statistical rigor + practical significance)

---

## SECTION 3: OUTPUT FORMAT SPECIFICATIONS

### 3.1 File Format

**Standard:** PNG (Portable Network Graphics)
- **Why PNG:** Lossless compression, high quality, universally compatible
- **NOT JPEG:** Lossy compression unsuitable for scientific figures
- **NOT SVG:** Vector format not standard for publications (PNG preferred)

**Resolution:** 300 DPI (dots per inch)
- Publication quality standard
- Suitable for both print and digital media
- Configured via `setup_plot_style()` or `dpi` parameter in save functions

**Bounding Box:** `bbox_inches='tight'`
- Trims whitespace around figure
- Ensures consistent margins
- Applied automatically by plotting functions

---

### 3.2 Figure Dimensions (Default)

**Trajectory Plots:** (10, 6) inches
- Width: 10 inches (supports wide x-axis labels, multiple curves)
- Height: 6 inches (standard aspect ratio for time-series)

**Diagnostic Plots:** (12, 10) inches
- Width: 12 inches (2x2 grid requires more space)
- Height: 10 inches (square subplots)

**Histograms:** (10, 6) inches
- Width: 10 inches (multiple overlaid distributions)
- Height: 6 inches (standard histogram aspect)

**Override:** Use `figsize` parameter if custom dimensions needed per plan.md

---

### 3.3 Color Scheme (REMEMVR Domains)

**What Domain:** `#E74C3C` (red)
- Semantic memory (objects, facts)
- RGB: (231, 76, 60)

**Where Domain:** `#3498DB` (blue)
- Spatial memory (locations, navigation)
- RGB: (52, 152, 219)

**When Domain:** `#2ECC71` (green)
- Temporal memory (order, sequence)
- RGB: (46, 204, 113)

**Source:** `config/plotting.yaml`

**Usage:**
```python
colors = {
    "What": "#E74C3C",
    "Where": "#3498DB",
    "When": "#2ECC71"
}

plot_trajectory(..., colors=colors)
```

**Consistency:** Same colors used across all 50 RQs (visual consistency in thesis)

---

### 3.4 Styling Parameters (from config/plotting.yaml)

**Font Sizes:**
- Base: 11pt
- Axes labels: 12pt
- Title: 13pt bold
- Legend: 10pt

**Line Widths:**
- Trajectories: 2.5pt (thick for visibility)
- Error bars: 1.5pt
- Reference lines: 1.0pt dashed

**Marker Sizes:**
- Observed data points: 8pt
- Legend markers: 6pt

**Applied Via:** `setup_plot_style()` (call once at start of plots.py)

---

## SECTION 2.5: OPTION B ARCHITECTURE - PLOT SOURCE CSV PREPARATION ⚠️ CRITICAL

**CRITICAL DESIGN:** Plot source CSVs are created DURING ANALYSIS (by g_code), NOT during plotting (by rq_plots).

**READ THIS SECTION FIRST** before understanding rq_plots workflow - it defines the separation of concerns between data manipulation (analysis phase) and visualization (plotting phase).

**Two-Phase Approach:**

**Phase 1: Analysis Pipeline (g_code generates plot source CSVs)**
```python
# In stepN_prepare_trajectory_plot_data.py (generated by g_code):

# 1. Load multiple analysis outputs
theta_df = pd.read_csv("data/theta_scores.csv")
observed_df = pd.read_csv("data/observed_means.csv")
tsvr_df = pd.read_csv("data/tsvr_mapping.csv")

# 2. Aggregate/merge for plotting
plot_data = theta_df.merge(observed_df, on=['composite_ID', 'test'])
plot_data = plot_data.merge(tsvr_df, on='test')
plot_data = plot_data[['time', 'theta', 'CI_lower', 'CI_upper', 'domain']]

# 3. Save plot source CSV
plot_data.to_csv("plots/trajectory_theta_data.csv", index=False)

# 4. Validate
validate_plot_data("plots/trajectory_theta_data.csv", required_columns=[...])
```

**Phase 2: Plotting (rq_plots generates plots.py)**
```python
# In plots/plots.py (generated by rq_plots):

from pathlib import Path
import pandas as pd
from tools.plotting import setup_plot_style, plot_trajectory

setup_plot_style()

# Read pre-aggregated source CSV
df = pd.read_csv("plots/trajectory_theta_data.csv")

# Plot from source CSV
fig, ax = plot_trajectory(
    observed_data=df,
    time_col='time',
    value_col='theta',
    group_col='domain',
    xlabel='Time Since VR (hours)',
    ylabel='Memory Ability (Theta)',
    title='RQ 5.1: Trajectory',
    output_path=Path("plots/trajectory_theta.png")
)
```

**Why This Design (Option B):**
- **Separation of concerns:** Data manipulation (g_code) vs visualization (rq_plots)
- **Atomic agents:** Each agent single responsibility (v4.X philosophy)
- **Built-in validation:** Missing source CSV → rq_plots FAILS → signals analysis incomplete
- **Less complexity:** rq_plots doesn't need data schema knowledge or ETL logic
- **Tool migration:** prepare_*_plot_data functions added to tools/ with TDD

**File Structure Per Plot:**
```
plots/
├── trajectory_theta_data.csv    ← Created by g_code (analysis phase)
├── trajectory_theta.png          ← Created by plots.py (plotting phase)
├── trajectory_prob_data.csv      ← Created by g_code
└── trajectory_prob.png           ← Created by plots.py
```

**Benefits:**
- Reproducibility: Source CSVs document exact data plotted
- Validation: Can inspect plots/*.csv before plotting
- Debugging: If plot wrong, check source CSV first
- Transparency: Data + visualization separated
- Reusability: Source CSVs available for replotting with different styles

---

## SECTION 4: FILE NAMING CONVENTIONS

### 4.1 Naming Convention Source

**Primary Source:** `docs/v4/names.md`

**Current Status (v4.X v1.0.0):** EMPTY (TDD approach)

**Philosophy:** Naming conventions emerge from RQ 5.1 execution, not speculation.

---

### 4.2 Generic TDD Guidance

**When names.md EMPTY (current state):**

1. **Consult plan.md:** Check `results/chX/rqY/docs/2_plan.md` for plot naming specifications
2. **Use descriptive names:** `{analysis_type}_{variant}.png` (e.g., `trajectory_theta.png`)
3. **Propose conventions during RQ 5.1:** When generating first plots, suggest naming patterns to master and user
4. **Document in names.md:** Master and user add discovered conventions to `docs/v4/names.md` plot_names section
5. **Retry if needed:** If naming unclear, rq_plots may fail at step 8 (master clarifies, agent retries)

**Principle:** Use clear, self-documenting names that convey plot purpose.

---

### 4.3 Expected Convention Evolution (TDD Prediction)

**After RQ 5.1 execution, names.md likely to contain:**

```yaml
plot_names:
  - name: trajectory_theta
    pattern: trajectory_theta.png
    example: trajectory_theta.png
    introduced: RQ 5.1
    notes: "Theta-scale trajectory plot (y-axis: -3 to +3)"

  - name: trajectory_probability
    pattern: trajectory_probability.png
    example: trajectory_probability.png
    introduced: RQ 5.1
    notes: "Probability-scale trajectory plot (y-axis: 0-100%, Decision D069)"

  - name: diagnostics
    pattern: diagnostics.png
    example: diagnostics.png
    introduced: RQ 5.1
    notes: "2x2 regression diagnostic grid"

  # Additional patterns discovered during RQ 5.1...
```

**NOTE:** This is PREDICTION not prescription. Actual conventions emerge from implementation.

---

### 4.4 Decision D069 Naming Requirement

**For dual-scale trajectory plots:**

**Requirement:** Theta and probability plots MUST have distinguishable names

**Suggested Pattern (not mandatory until names.md populated):**
- Theta plot: `{prefix}_theta.png`
- Probability plot: `{prefix}_probability.png`

**Example:**
- `trajectory_theta.png` (theta scale)
- `trajectory_probability.png` (probability scale)

**Rationale:** Prevents confusion, enables systematic validation, clarifies which scale in use

---

## SECTION 5: COMMON PATTERNS

### 5.1 Standard Import Structure

```python
from pathlib import Path
import pandas as pd
import numpy as np
from tools.plotting import (
    setup_plot_style,
    plot_trajectory,
    plot_trajectory_probability,
    plot_diagnostics,
    plot_histogram_by_group,
    save_plot_with_data
)

# Setup consistent styling FIRST
setup_plot_style()

# Then generate plots...
```

**Best Practice:** Import only functions needed for THIS RQ (not all 6 every time)

---

### 5.2 Style Setup Pattern

**ALWAYS call `setup_plot_style()` at start of plots.py:**

```python
# Apply consistent styling from config/plotting.yaml
setup_plot_style()
```

**Why First:**
- Configures global matplotlib/seaborn settings
- Ensures all subsequent plots use consistent theme
- Loads config/plotting.yaml defaults (DPI, fonts, colors)

**Only Once:** Called once per script, affects all plots in session

---

### 5.3 Data Loading Pattern

**From analysis outputs:**

```python
# Load theta scores with TSVR
df_thetas = pd.read_csv("data/theta_scores_with_tsvr.csv")

# Load LMM predictions
df_predictions = pd.read_csv("code/lmm_predictions.csv")

# Load IRT item parameters (for D069 probability transformation)
item_params_path = Path("data/pass2_item_parameters.csv")
```

**Best Practice:**
- Use Path objects for cross-platform compatibility
- Verify files exist before plotting (circuit breaker if missing)
- Use relative paths from RQ root (plots.py runs from results/chX/rqY/)

---

### 5.4 Saving Plots Pattern

**Option 1: Direct saving (output_path parameter)**

```python
fig, ax = plot_trajectory(
    ...,
    output_path=Path("plots/trajectory_theta.png")
)
# PNG saved automatically, no CSV
```

**Option 2: Reproducibility (save_plot_with_data)**

```python
fig, ax = plot_trajectory(
    ...,
    output_path=None  # Don't save automatically
)

# Save PNG + CSV for reproducibility
save_plot_with_data(
    fig=fig,
    output_path=Path("plots/trajectory_theta.png"),
    data=df_plot_data,
    dpi=300
)
# Creates: trajectory_theta.png + trajectory_theta.csv
```

**Recommendation:** Option 2 (reproducibility) for ALL plots

---

## SECTION 6: ERROR HANDLING

### 6.1 Missing Function in tools/plotting.py

**Trigger:** rq_plots step 8 validation fails (required function doesn't exist)

**Agent Behavior:**
- **FAIL immediately** with circuit breaker: `PLOTTING_FUNCTION_MISSING`
- **DO NOT generate code** (no hallucinated alternatives, no custom implementations)
- **Report missing functions:** List all functions needed but not found in tools/plotting.py

**Example Error Report:**
```markdown
CIRCUIT BREAKER: PLOTTING_FUNCTION_MISSING

Required functions NOT FOUND in tools/plotting.py:
- plot_effect_sizes() (needed for effect size visualization per plan.md)
- plot_correlation_matrix() (needed for correlation heatmap per plan.md)

Action Required:
1. Master and user manually add missing functions to tools/plotting.py
2. Write tests for new functions (pytest tests/test_plotting.py)
3. Update tools_inventory.md with new function documentation
4. Retry rq_plots agent
```

**Master Actions:**
1. Review plan.md to confirm function actually needed
2. Implement missing function in tools/plotting.py (TDD: test first)
3. Update tools_inventory.md with function API
4. Retry rq_plots invocation

**Rationale:** Prevents inconsistent plotting code, maintains tools/ quality, enables reuse across RQs

---

### 6.2 Missing Data File

**Trigger:** rq_plots step 6 data loading fails (file doesn't exist)

**Agent Behavior:**
- **FAIL immediately** with circuit breaker: `DATA_FILE_MISSING`
- **Report missing file:** Path that doesn't exist
- **DO NOT proceed to plotting**

**Example Error Report:**
```markdown
CIRCUIT BREAKER: DATA_FILE_MISSING

Required data file NOT FOUND:
  Expected: data/theta_scores_with_tsvr.csv

Action Required:
1. Check if prior analysis steps completed successfully
2. Verify file created by expected step (check logs/)
3. If file missing, re-run prior analysis step
4. If path wrong, update 2_plan.md with correct path
5. Retry rq_plots agent
```

**Master Actions:**
1. Check status.yaml - are all prior steps = success?
2. Verify expected file exists: `ls results/chX/rqY/data/`
3. If missing, re-run analysis step that should create it
4. If path mismatch, update plan.md and retry

---

### 6.3 Invalid Parameters

**Trigger:** Function call has wrong parameter types or values

**Agent Behavior:**
- **FAIL during code generation** (detected in step 7 ultrathink)
- **Report parameter mismatch:** Expected vs actual types
- **Reference source code:** "See tools/plotting.py lines X-Y for signature"

**Prevention:**
- Agent reads tools/plotting.py source code (step 5) to learn correct signatures
- Agent cross-references plan.md requirements with function APIs
- Agent validates parameter types before generating code

**Example Error Report:**
```markdown
PARAMETER MISMATCH DETECTED

Function: plot_trajectory()
Parameter: time_pred
  Expected: np.ndarray
  Found in plan.md: List[float]

Action Required:
1. Convert List[float] to np.ndarray before calling plot_trajectory()
2. Update plots.py generation logic
3. Verify data types match function signature from tools/plotting.py lines 92-208
```

**Rationale:** Agent reads source code to prevent API mismatches (v3.0 lesson learned)

---

## SECTION 7: INTEGRATION WITH RQ_PLOTS WORKFLOW

### 7.1 Template Usage in Agent Workflow

**rq_plots agent workflow (summary from Section Overview):**

```
Step 4: Read docs/v4/templates/plots.md (THIS FILE)
  - Learn available functions (Section 1)
  - Understand D069 requirements (Section 2)
  - Note output format specs (Section 3)
  - Check naming conventions (Section 4 - TDD guidance)

Step 5: Read tools/plotting.py (SOURCE CODE)
  - Get complete function signatures
  - Understand implementation details
  - Learn parameter types and defaults
  - Inspect docstrings and usage patterns

Step 7: Ultrathink - Generate plots.py
  - Use ONLY functions from tools/plotting.py
  - Apply D069 if trajectory RQ (both theta + probability)
  - Follow output format specs (PNG 300 DPI)
  - Use TDD naming guidance (propose conventions if names.md empty)

Step 8: Validate - Check all required functions exist
  - IF missing function → FAIL (circuit breaker)
  - ELSE → Proceed to code generation
```

**Template Provides:**
- Essential guidance (what functions available, D069 requirements)
- Output standards (format, dimensions, colors)
- Naming guidance (TDD approach)

**Source Code Provides:**
- Complete signatures (all parameters, types, defaults)
- Implementation details (how functions work)
- Usage patterns (docstring examples)

**Together:** Template + source code = complete specification for rq_plots

---

### 7.2 Status.yaml Integration

**After rq_plots completes, status.yaml updated:**

```yaml
rq_plots:
  status: success
  context_dump: |
    **rq_plots:**
    - Plots generated: 3 (trajectory_theta, trajectory_probability, diagnostics)
    - Data sources: theta_scores_with_tsvr.csv, lmm_predictions.csv, pass2_item_parameters.csv
    - D069 compliance: YES (dual-scale trajectory plots included)
```

**Context dump content:**
- Plots generated count (how many PNG files created)
- Data sources used (which CSV files loaded)
- D069 compliance (if trajectory RQ, confirm both scales generated)

**Used By:**
- rq_inspect: Validates plots created as expected
- rq_results: Summarizes visualization approach
- Master: Tracks progress across workflow steps

---

### 7.3 Validation (rq_inspect Step)

**After plots generated, master invokes rq_inspect:**

**rq_inspect checks:**
1. **Files created:** All expected PNG files exist in plots/
2. **Format valid:** PNG files readable, non-corrupted
3. **D069 compliance:** If trajectory RQ, BOTH theta and probability plots present
4. **Naming conventions:** Files follow names.md patterns (if populated)
5. **Reproducibility:** CSV files paired with PNG files (if save_plot_with_data used)

**Validation checklist (from inspect_criteria.md):**
- [ ] All plots specified in plots.py created successfully
- [ ] PNG files valid format (300 DPI, readable)
- [ ] D069 compliance (trajectory_theta.png + trajectory_probability.png both exist)
- [ ] File naming consistent with names.md (or TDD proposals if names.md empty)
- [ ] CSV data files paired with PNG files (reproducibility requirement)

**IF validation fails:**
- rq_inspect reports failure to master
- Master invokes g_debug to identify root cause
- User and master fix issue (add missing plot, correct naming, etc.)
- Re-run plots.py script
- Retry rq_inspect validation

---

## SECTION 8: VERSION HISTORY

### v1.0.0 (2025-11-17)

**Initial template creation**

**Includes:**
- Section 1: 6 plotting functions (summary + key parameters)
  - setup_plot_style, plot_trajectory, plot_trajectory_probability, plot_diagnostics, plot_histogram_by_group, theta_to_probability, save_plot_with_data
- Section 2: Decision D069 dedicated section (MANDATORY dual-scale trajectory plots)
  - Validation checklist (7 items)
  - IRT transformation formula
  - Rejection criteria
- Section 3: Output format specifications (PNG 300 DPI, dimensions, colors)
- Section 4: File naming conventions (Generic TDD guidance, names.md currently empty)
- Section 5: Common patterns (imports, style setup, data loading, saving)
- Section 6: Error handling (missing functions, missing data, invalid parameters)
- Section 7: rq_plots workflow integration (status.yaml, validation)

**Design Decisions (from user AskUserQuestion):**
- **Function documentation:** Summary + key parameters (hybrid, not full duplication)
- **D069 prominence:** Dedicated major section (ensures visibility and compliance)
- **Naming guidance:** Generic TDD only (pure emergent, no prescriptive examples)

**Status:** Production-ready for RQ 5.1 testing

**Next:** RQ 5.1 will populate names.md plot_names section with discovered conventions

---

**End of plots.md Template**
