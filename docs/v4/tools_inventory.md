# Tools Inventory (v4.X)

**Version:** 4.0
**Last Updated:** 2025-11-22
**Purpose:** Authoritative API reference for VALIDATED analysis tools (YELLOW/GREEN only)
**Source of Truth:** `/home/etai/projects/REMEMVR/docs/v4/tools_status.tsv`

---

## Module: tools.analysis_irt

### prepare_irt_input_from_long

| Field | Value |
|-------|-------|
| **Description** | Convert long-format DataFrame to IRT tensors for IWAVE model fitting |
| **Inputs** | `df_long: DataFrame` (long format with composite_ID, item, response), `groups: Dict[str, List[str]]` (factor -> item mapping) |
| **Outputs** | `Tuple[Tensor, Tensor, Tensor, List, List]` (response_matrix, missing_mask, Q_matrix, composite_ids, item_list) |

### configure_irt_model

| Field | Value |
|-------|-------|
| **Description** | Build IWAVE Graded Response Model with specified architecture |
| **Inputs** | `n_items: int`, `n_factors: int`, `n_cats: int`, `Q_matrix: Tensor`, `correlated_factors: bool`, `device: str`, `seed: int` |
| **Outputs** | `IWAVE` model object |

### fit_irt_grm

| Field | Value |
|-------|-------|
| **Description** | Fit IRT model via variational inference (IWAVE algorithm) |
| **Inputs** | `model: IWAVE`, `response_matrix: Tensor`, `missing_mask: Tensor`, `batch_size: int`, `iw_samples: int`, `mc_samples: int` |
| **Outputs** | `IWAVE` fitted model |

### extract_theta_from_irt

| Field | Value |
|-------|-------|
| **Description** | Extract participant ability estimates (theta scores) from fitted model |
| **Inputs** | `model: IWAVE`, `response_matrix: Tensor`, `missing_mask: Tensor`, `composite_ids: List`, `factor_names: List`, `scoring_batch_size: int`, `mc_samples: int`, `iw_samples: int`, `invert_scale: bool` |
| **Outputs** | `DataFrame` with columns: composite_ID, domain_name, theta |

### extract_parameters_from_irt

| Field | Value |
|-------|-------|
| **Description** | Extract item parameters (discrimination a, difficulty b) from fitted model |
| **Inputs** | `model: IWAVE`, `item_list: List`, `factor_names: List`, `n_cats: int` |
| **Outputs** | `DataFrame` with columns: item, domain, Discrimination, Difficulty_1...Difficulty_k |

### calibrate_irt

| Field | Value |
|-------|-------|
| **Description** | Full IRT pipeline: prepare -> configure -> fit -> extract (convenience wrapper) |
| **Inputs** | `df_long: DataFrame`, `groups: Dict[str, List[str]]`, `config: dict` (irt_config with model params) |
| **Outputs** | `Tuple[DataFrame, DataFrame]` (theta_scores, item_parameters) |

### filter_items_by_quality

| Field | Value |
|-------|-------|
| **Description** | D039: Purify items by quality thresholds for 2-pass IRT calibration |
| **Inputs** | `df_items: DataFrame` (item parameters), `a_threshold: float` (default 0.4), `b_threshold: float` (default 3.0) |
| **Outputs** | `Tuple[DataFrame, DataFrame]` (retained_items, removed_items) |

### calibrate_grm

| Field | Value |
|-------|-------|
| **Description** | Backwards-compatible wrapper for calibrate_irt() |
| **Inputs** | `df_long: DataFrame`, `groups: Dict[str, List[str]]`, `config: dict` |
| **Outputs** | `Tuple[DataFrame, DataFrame]` (theta_scores, item_parameters) |

---

## Module: tools.analysis_lmm

### prepare_lmm_input_from_theta

| Field | Value |
|-------|-------|
| **Description** | DEPRECATED: Convert theta scores from wide to long format with nominal days. Violates D070. |
| **Inputs** | `theta_scores: DataFrame` (wide format with UID, test, Theta_* columns), `factors: List[str]` (optional filter) |
| **Outputs** | `DataFrame` with columns: UID, test, Factor, Ability, Days, Days_sq, log_Days |
| **Warning** | Use `fit_lmm_trajectory_tsvr()` instead for REMEMVR analyses |

### configure_candidate_models

| Field | Value |
|-------|-------|
| **Description** | Generate formulas for 5 candidate LMM models |
| **Inputs** | `n_factors: int` (1=single domain, >1=multiple), `reference_group: str` (required if n_factors > 1) |
| **Outputs** | `Dict[str, Dict[str, str]]` with keys: Linear, Quadratic, Log, Lin+Log, Quad+Log; each containing formula and re_formula |

### fit_lmm_trajectory_tsvr

| Field | Value |
|-------|-------|
| **Description** | D070: Fit LMM using TSVR (actual hours since encoding) as time variable |
| **Inputs** | `theta_scores: DataFrame` (composite_ID, domain_name, theta), `tsvr_data: DataFrame` (UID, Test, TSVR_hours), `formula: str`, `groups: str` (default 'UID'), `re_formula: str` (default '~Days'), `reml: bool` (default False) |
| **Outputs** | `MixedLMResults` object |

### compare_lmm_models_by_aic

| Field | Value |
|-------|-------|
| **Description** | Fit all 5 candidate models, compare by AIC, return best model |
| **Inputs** | `data: DataFrame`, `n_factors: int`, `reference_group: str`, `groups: str`, `save_dir: Path` |
| **Outputs** | `Dict` with keys: models (all fitted), aic_comparison (DataFrame), best_model (name), best_result (MixedLMResults) |

### extract_fixed_effects_from_lmm

| Field | Value |
|-------|-------|
| **Description** | Extract fixed effects table from fitted LMM |
| **Inputs** | `result: MixedLMResults` |
| **Outputs** | `DataFrame` with columns: effect, coefficient, std_error, z_value, p_value |

### extract_random_effects_from_lmm

| Field | Value |
|-------|-------|
| **Description** | Extract random effects variance components and ICC |
| **Inputs** | `result: MixedLMResults` |
| **Outputs** | `Dict` with keys: variance_components (Dict), icc (float) |

### compute_contrasts_pairwise

| Field | Value |
|-------|-------|
| **Description** | D068: Post-hoc pairwise contrasts with dual p-value reporting |
| **Inputs** | `lmm_result: MixedLMResults`, `comparisons: List[str]` (e.g., ["Where-What", "When-What"]), `family_alpha: float` (default 0.05) |
| **Outputs** | `DataFrame` with columns: comparison, beta, se, z, p_uncorrected, alpha_corrected, p_corrected, sig_uncorrected, sig_corrected |

### compute_effect_sizes_cohens

| Field | Value |
|-------|-------|
| **Description** | Compute Cohen's f-squared effect sizes for LMM fixed effects |
| **Inputs** | `lmm_result: MixedLMResults`, `include_interactions: bool` (default False) |
| **Outputs** | `DataFrame` with columns: effect, f_squared, interpretation (negligible/small/medium/large) |

### select_lmm_random_structure_via_lrt

| Field | Value |
|-------|-------|
| **Description** | Compare 3 random structure specifications via Likelihood Ratio Test: (1) Full (random intercepts + slopes with correlation), (2) Uncorrelated (random intercepts + slopes without correlation), (3) Intercept-only. Uses parsimonious selection: prefers simpler model if p ≥ 0.05. |
| **Inputs** | `data: DataFrame` (long-format LMM input), `formula: str` (fixed effects formula), `time_var: str` (time variable name for random slopes), `groups: str = 'UID'` (grouping variable), `reml: bool = False` (ML required for LRT) |
| **Outputs** | `Dict[selected_model: str, lrt_results: DataFrame, fitted_models: Dict[str, MixedLMResults]]` |
| **Reference** | Pinheiro & Bates (2000), Verbeke & Molenberghs (2000), RQ 5.10 1_concept.md |
| **Notes** | v1 implementation: Uncorrelated model equals Full model (statsmodels limitation - no simple formula syntax for uncorrelated random effects). Compares Intercept-only vs Full via LRT. All models fitted with REML=False (ML estimation required for valid LRT comparison). Selection logic: start from Intercept-only, test if Full improves fit (p < 0.05). Handles convergence failures gracefully by falling back to simpler models. 12/15 tests GREEN, 3 skipped (statsmodels convergence limitations with synthetic data documented). |

### prepare_age_effects_plot_data

| Field | Value |
|-------|-------|
| **Description** | Create age tertiles (Young/Middle/Older), aggregate observed means, and generate LMM predictions for RQ 5.10 Age × Domain × Time interaction visualization. Produces plot-ready data with observed values (mean ± 95% CI) and model predictions for each domain × tertile × timepoint combination. |
| **Inputs** | `lmm_input: DataFrame` (long format with UID, Age, domain_name, TSVR_hours, theta), `lmm_model: MixedLMResults` (fitted model), `output_path: Path` (CSV save location) |
| **Outputs** | `DataFrame` with columns: domain_name, age_tertile, TSVR_hours, theta_observed, se_observed, ci_lower, ci_upper, theta_predicted (36 rows = 3 domains × 3 tertiles × 4 timepoints) |
| **Reference** | RQ 5.10 1_concept.md, ANALYSES_CH5.md lines 921-926, tools_todo.yaml lines 51-67 |
| **Notes** | Age tertiles created using pd.qcut(Age, q=3) for equal-sized groups (~20 subjects each for N=60). Tertiles used ONLY for visualization; analysis uses continuous Age_c (grand-mean centered). Predictions generated from LMM fittedvalues aggregated by group (not marginal effects). CIs computed as mean ± 1.96*SEM. 15/15 tests GREEN. |

### compute_icc_from_variance_components

| Field | Value |
|-------|-------|
| **Description** | Compute 3 Intraclass Correlation Coefficient (ICC) estimates from LMM variance components for RQ 5.13 individual differences analysis. ICC quantifies proportion of variance due to between-person differences vs within-person residual variation. Provides ICC_intercept (baseline individual differences), ICC_slope_simple (slope variance only), and ICC_slope_conditional (slope variance accounting for correlation with intercepts at specific timepoint). |
| **Inputs** | `variance_components_df: DataFrame` (with columns: Component, Variance), `slope_name: str = 'TSVR_hours'` (slope component name), `timepoint: float = 6.0` (for conditional ICC calculation, e.g., Day 6) |
| **Outputs** | `DataFrame` with columns: icc_type, icc_value, interpretation (3 rows, sorted by icc_type) |
| **Reference** | Snijders & Bosker (2012) Ch 3, RQ 5.13 1_concept.md Step 4, tools_todo.yaml lines 71-86 |
| **Notes** | Three ICC formulas: (1) ICC_intercept = σ²_intercept / (σ²_intercept + σ²_residual), (2) ICC_slope_simple = σ²_slope / (σ²_slope + σ²_residual), (3) ICC_slope_conditional = Var(b₀ᵢ + b₁ᵢ×t) / [Var(b₀ᵢ + b₁ᵢ×t) + σ²_residual] where Var(b₀ᵢ + b₁ᵢ×t) = σ²_intercept + 2×t×cov(b₀,b₁) + t²×σ²_slope. Interpretation thresholds: <0.10 Low, 0.10-0.30 Moderate, 0.30-0.75 High, ≥0.75 Very High. Handles intercept-only models (no slope variance) gracefully. 14/14 tests GREEN. |

### test_intercept_slope_correlation_d068

| Field | Value |
|-------|-------|
| **Description** | Test correlation between random intercepts and random slopes from LMM with Decision D068 dual p-value reporting (uncorrected + Bonferroni). Tests whether individuals with higher baseline memory (intercepts) show different rates of forgetting (slopes). Used in RQ 5.13 individual differences analysis. |
| **Inputs** | `random_effects_df: DataFrame` (UID, intercepts, slopes), `family_alpha: float = 0.05` (significance threshold), `n_tests: int = 15` (Chapter 5 family size for Bonferroni), `intercept_col: str = 'Group Var'` (statsmodels default), `slope_col: str = 'Group x TSVR_hours Var'` (statsmodels default) |
| **Outputs** | `Dict[r: float, p_uncorrected: float, p_bonferroni: float, significant_uncorrected: bool, significant_bonferroni: bool, interpretation: str]` |
| **Reference** | Decision D068 (dual p-value reporting), RQ 5.13 1_concept.md Step 5, Pearson correlation via scipy.stats.pearsonr, tools_todo.yaml lines 89-105 |
| **Notes** | Pearson correlation between random intercepts and slopes with Bonferroni correction (p_bonf = min(p_uncorr × n_tests, 1.0)). Interpretation thresholds: \|r\| < 0.30 Weak, 0.30-0.50 Moderate, ≥0.50 Strong. RQ 5.13 hypothesis: negative correlation (higher starters forget slower). 14/14 tests GREEN. Configurable column names for different random effects naming conventions. |

### extract_segment_slopes_from_lmm

| Field | Value |
|-------|-------|
| **Description** | Extract Early/Late segment slopes from piecewise LMM with delta method SE propagation for ratio. RQ 5.8 Test 4 requires Late/Early ratio < 0.5 to indicate robust two-phase forgetting pattern (consolidation-dominated Early vs decay-dominated Late). Delta method required because ratio SE ≠ simple quadrature due to covariance between slopes. |
| **Inputs** | `lmm_result: MixedLMResults` (fitted piecewise LMM), `segment_col: str = 'Segment'` (segment variable name), `time_col: str = 'Days_within'` (time-within-segment variable) |
| **Outputs** | `DataFrame[metric: str, value: float, SE: float, CI_lower: float, CI_upper: float, interpretation: str]` with 3 rows: Early_slope, Late_slope, Ratio_Late_Early |
| **Reference** | RQ 5.8 Test 4 (Convergent Evidence), Delta method: Casella & Berger (2002) Statistical Inference 2nd ed. p.240, tools_todo.yaml lines 115-133 |
| **Notes** | Piecewise LMM formula: `theta ~ Days_within + Days_within:SegmentLate + (Days_within \| UID)`. Early slope = β_Days_within, Late slope = β_Days_within + β_Days_within:SegmentLate. Delta method for ratio SE: SE²_ratio = (∂ratio/∂early)²×Var(early) + (∂ratio/∂late)²×Var(late) + 2×(∂ratio/∂early)×(∂ratio/∂late)×Cov(early,late), where ∂ratio/∂early = -late/early² and ∂ratio/∂late = 1/early. Interpretation thresholds: ratio < 0.5 (robust two-phase), 0.5-0.75 (moderate), 0.75-1.0 (weak), >1.0 (unexpected/reverse). Handles zero Early slope (ratio=inf/nan). 11/11 tests GREEN. 172 lines implementation. |

### assign_piecewise_segments

| Field | Value |
|-------|-------|
| **Description** | Assign piecewise segments (Early/Late) and compute Days_within for piecewise LMM (RQ 5.8 piecewise regression design) |
| **Inputs** | `df: DataFrame`, `tsvr_col: str = 'TSVR_hours'`, `early_cutoff_hours: float = 24.0` |
| **Outputs** | `DataFrame` with added columns: Segment (Early/Late), Days_within (time since segment start) |
| **Reference** | RQ 5.8 piecewise forgetting analysis, tools/analysis_lmm.py lines 25-101 |
| **Notes** | Implements piecewise regression design dividing forgetting trajectory into two temporal segments: Early segment (0-24h, consolidation-dominated) and Late segment (24-168h, decay-dominated). Default cutoff 24h represents one night's sleep (consolidation window). Creates Segment column (Early/Late) and Days_within column (0-1 for Early, 0-6 for Late). Used with piecewise LMM formula: theta ~ Days_within + Days_within:SegmentLate. |

### run_lmm_analysis

| Field | Value |
|-------|-------|
| **Description** | Complete LMM analysis pipeline wrapper (prepare data, fit candidates, compare AIC, extract effects, save results) |
| **Inputs** | `theta_scores: DataFrame`, `output_dir: Union[str, Path]`, `n_factors: int`, `reference_group: Optional[str]`, `save_models: bool = True` |
| **Outputs** | `Dict` with keys: best_model, aic_table, fixed_effects, random_effects |
| **Reference** | tools/analysis_lmm.py lines 739-877, convenience wrapper for full LMM workflow |
| **Notes** | Convenience wrapper combining: prepare_lmm_input_from_theta → configure_candidate_models → compare_lmm_models_by_aic → extract_fixed_effects_from_lmm + extract_random_effects_from_lmm. Simplifies common workflow into single function call. Automatically saves fitted models if save_models=True. Returns all key outputs in single dict. |

---

## Module: tools.plotting

### convert_theta_to_probability

| Field | Value |
|-------|-------|
| **Description** | Transform theta scores to probability scale via IRT 2PL formula |
| **Inputs** | `theta: ndarray`, `discrimination: float` (default 1.0), `difficulty: float` (default 0.0) |
| **Outputs** | `ndarray` of probabilities in range [0, 1] |

### plot_trajectory

| Field | Value |
|-------|-------|
| **Description** | Plot trajectory with fitted curves and observed data with error bars |
| **Inputs** | `time_pred: ndarray`, `fitted_curves: Dict[str, ndarray]`, `observed_data: DataFrame`, `time_col: str = 'Time'`, `value_col: str = 'Value'`, `group_col: str = 'Group'`, `xlabel: str`, `ylabel: str`, `title: str`, `figsize: Tuple`, `colors: Optional[Dict]`, `output_path: Optional[Path]` |
| **Outputs** | `Tuple[Figure, Axes, DataFrame]` (figure, axes, plot data CSV) |
| **Reference** | tools/plotting.py, generic trajectory visualization |
| **Notes** | Reusable trajectory plotting with consistent styling. Supports grouped visualizations by domain/factor. Saves both PNG and CSV for reproducibility. |

### plot_trajectory_probability

| Field | Value |
|-------|-------|
| **Description** | Plot trajectory with theta transformed to probability scale (Decision D069 dual-scale plotting) |
| **Inputs** | `df_thetas: DataFrame`, `item_parameters_path: Path`, `time_var: str = 'test'`, `factors: List[str]`, `title: str`, `figsize: Tuple`, `colors: Optional[Dict]`, `output_path: Optional[Path]`, `show_errorbar: bool = True` |
| **Outputs** | `Tuple[Figure, Axes, DataFrame]` (figure, axes, plot data) |
| **Reference** | Decision D069 (dual-scale trajectory plots), tools/plotting.py |
| **Notes** | Implements dual-scale trajectory plotting: theta scale (statistical rigor) + probability scale (general audience interpretability). Uses IRT 2PL transformation P = 1/(1 + exp(-(a×(theta - b)))) where a = mean discrimination from Pass 2 item parameters. Enhances interpretability while preserving statistical accuracy. |

### plot_histogram_by_group

| Field | Value |
|-------|-------|
| **Description** | Create grouped histogram with overlapping distributions |
| **Inputs** | `df: DataFrame`, `value_col: str`, `group_col: str`, `xlabel: str = 'Value'`, `ylabel: str = 'Frequency'`, `title: str`, `bins: int = 20`, `colors: Optional[Dict]`, `figsize: Tuple`, `output_path: Optional[Path]`, `vline: Optional[float]`, `vline_label: Optional[str]` |
| **Outputs** | `Tuple[Figure, Axes]` |
| **Reference** | tools/plotting.py, distribution visualization |
| **Notes** | Supports grouped histograms for comparing distributions across factors/domains. Optional vertical reference line for thresholds. Publication-ready styling with 300 DPI. |

### set_plot_style_defaults

| Field | Value |
|-------|-------|
| **Description** | Apply consistent matplotlib and seaborn styling from config |
| **Inputs** | `config_path: Optional[Path] = None` (optional path to plotting.yaml) |
| **Outputs** | None |
| **Reference** | tools/plotting.py lines 40-86 |
| **Notes** | Loads plotting parameters from config/plotting.yaml and applies them to matplotlib rcParams. Falls back to sensible defaults if config not found. Should be called before plot generation. |

### plot_diagnostics

| Field | Value |
|-------|-------|
| **Description** | Create 2x2 diagnostic plot grid for regression model validation |
| **Inputs** | `df: DataFrame` (with fitted and residuals columns), `fitted_col: str = 'fitted'`, `residuals_col: str = 'residuals'`, `group_col: Optional[str] = None`, `figsize: Tuple[int, int] = (12, 10)`, `output_path: Optional[Path] = None` |
| **Outputs** | `Tuple[Figure, np.ndarray]` (matplotlib figure and 2x2 array of axes) |
| **Reference** | tools/plotting.py lines 215-333 |
| **Notes** | Creates four diagnostic plots: (A) Residuals vs Fitted, (B) Q-Q Plot, (C) Scale-Location, (D) Residuals by Group. Used for LMM assumption validation. |

### save_plot_with_data

| Field | Value |
|-------|-------|
| **Description** | Save plot as PNG and optionally save associated data as CSV |
| **Inputs** | `fig: Figure` (matplotlib figure to save), `output_path: Path` (path for PNG file), `data: Optional[DataFrame] = None` (optional DataFrame to save as CSV), `dpi: int = 300` (DPI for PNG output) |
| **Outputs** | None |
| **Reference** | tools/plotting.py lines 471-509 |
| **Notes** | Saves matplotlib figure and corresponding data for reproducibility. CSV is saved with same name as PNG but .csv extension. Default 300 DPI for publication quality. |

### prepare_piecewise_plot_data

| Field | Value |
|-------|-------|
| **Description** | Prepare piecewise trajectory plot data with observed means and model predictions |
| **Inputs** | `df_input: DataFrame` (piecewise LMM data), `lmm_result: MixedLMResults` (fitted model), `segment_col: str`, `factor_col: str`, `segment_values: List[str]` (e.g., ['Early', 'Late']), `factor_values: List[str]` (e.g., ['Common', 'Congruent', 'Incongruent']), `days_within_col: str = 'Days_within'`, `theta_col: str = 'theta'`, `early_grid_points: int = 20`, `late_grid_points: int = 60`, `ci_level: float = 0.95` |
| **Outputs** | `Dict[str, DataFrame]` with keys 'early' and 'late', each containing DataFrame with columns: Days_within, {factor_col}, theta_observed, CI_lower_observed, CI_upper_observed, theta_predicted, Data_Type |
| **Reference** | tools/plotting.py lines 664-838, RQ 5.8 piecewise plots |
| **Notes** | Aggregates observed theta scores by segment and factor, computes 95% CI, and generates model predictions on a grid of Days_within values for smooth trajectory lines. Designed for piecewise LMM plots with separate Early and Late panels. |

---

## Module: tools.validation

### validate_irt_convergence

| Field | Value |
|-------|-------|
| **Description** | Check IRT model convergence based on loss stability and parameter bounds |
| **Inputs** | `results: Dict[str, Any]` (containing loss_history, model parameters) |
| **Outputs** | `Dict[str, Any]` with keys: converged (bool), checks (list of check results), message (str) |

### validate_irt_parameters

| Field | Value |
|-------|-------|
| **Description** | Validate item parameters against quality thresholds |
| **Inputs** | `df_items: DataFrame`, `a_min: float` (default 0.4), `b_max: float` (default 3.0), `a_col: str` (default 'Discrimination'), `b_col: str` (default 'Difficulty') |
| **Outputs** | `Dict[str, Any]` with keys: valid (bool), n_items, n_valid, n_invalid, invalid_items (list), message (str) |

### validate_lmm_convergence

| Field | Value |
|-------|-------|
| **Description** | Check LMM model convergence status and warnings |
| **Inputs** | `lmm_result: MixedLMResults` |
| **Outputs** | `Dict[str, Any]` with keys: converged (bool), message (str), warnings (list) |

### validate_lmm_residuals

| Field | Value |
|-------|-------|
| **Description** | Test LMM residuals for normality using Kolmogorov-Smirnov test |
| **Inputs** | `residuals: ndarray`, `alpha: float` (default 0.05) |
| **Outputs** | `Dict[str, Any]` with keys: normal (bool), ks_statistic (float), p_value (float), message (str) |

### check_file_exists

| Field | Value |
|-------|-------|
| **Description** | Validate that file exists and optionally meets minimum size requirement |
| **Inputs** | `file_path: Union[str, Path]`, `min_size_bytes: int` (default 0, 0 = no minimum) |
| **Outputs** | `Dict[str, Any]` with keys: valid (bool), file_path (str), size_bytes (int, 0 if file doesn't exist), message (str) |
| **Notes** | Returns `valid=False` if: (1) file doesn't exist, (2) path is directory not file, (3) file size < min_size_bytes. Accepts both string paths and pathlib.Path objects. |

### create_lineage_metadata

| Field | Value |
|-------|-------|
| **Description** | Create lineage metadata for a data transformation (prevents Pass 1/2 mix-ups) |
| **Inputs** | `source_file: str` (path to source/input file), `output_file: str` (path to output file being created), `operation: str` (e.g., 'irt_calibration', 'lmm_analysis'), `parameters: Optional[Dict[str, Any]] = None` (operation parameters), `description: str = ""` (human-readable description) |
| **Outputs** | `Dict[str, Any]` (lineage metadata dictionary with timestamp) |
| **Reference** | tools/validation.py lines 30-82, post-RQ 5.1 safety feature |
| **Notes** | Creates lineage metadata to track data provenance. Prevents mixing outputs from different passes or configurations. Includes timestamp, operation, parameters, and file paths. |

### save_lineage_to_file

| Field | Value |
|-------|-------|
| **Description** | Save lineage metadata to JSON file |
| **Inputs** | `metadata: Dict[str, Any]` (lineage metadata dictionary), `lineage_file: str` (path to save JSON file) |
| **Outputs** | None (saves to disk) |
| **Reference** | tools/validation.py lines 85-104 |
| **Notes** | Saves lineage metadata as JSON for persistence. Used with create_lineage_metadata and validate_lineage. |

### load_lineage_from_file

| Field | Value |
|-------|-------|
| **Description** | Load lineage metadata from JSON file |
| **Inputs** | `lineage_file: str` (path to lineage JSON file) |
| **Outputs** | `Dict[str, Any]` (lineage metadata dictionary) |
| **Reference** | tools/validation.py lines 107-126 |
| **Notes** | Loads lineage metadata from JSON file. Used to verify data provenance before analysis. |

### validate_lineage

| Field | Value |
|-------|-------|
| **Description** | Validate that data comes from expected source (checks source file and pass number) |
| **Inputs** | `lineage_file: str` (path to lineage JSON file), `expected_source: Optional[str] = None` (expected source file name, partial match allowed), `expected_pass: Optional[int] = None` (expected pass number, 1 or 2) |
| **Outputs** | `Dict[str, Any]` with keys: valid (bool), message (str), metadata (optional) |
| **Reference** | tools/validation.py lines 129-190 |
| **Notes** | Validates data provenance to prevent Pass 1/2 mix-ups (post-RQ 5.1 safety measure). Checks source file and pass number match expectations. |

### check_missing_data

| Field | Value |
|-------|-------|
| **Description** | Check for missing data in DataFrame |
| **Inputs** | `df: DataFrame` (data to check) |
| **Outputs** | `Dict[str, Any]` with keys: has_missing (bool), total_missing (int), total_cells (int), percent_missing (float), missing_by_column (Dict[str, int]) |
| **Reference** | tools/validation.py lines 304-336 |
| **Notes** | Comprehensive missing data report by column. Useful for data quality checks before analysis. |

### validate_data_columns

| Field | Value |
|-------|-------|
| **Description** | Validate that required columns exist in DataFrame |
| **Inputs** | `df: DataFrame` (data to validate), `required_columns: List[str]` (required column names) |
| **Outputs** | `Dict[str, Any]` with keys: valid (bool), missing_columns (List[str]), existing_columns (List[str]), n_required (int), n_missing (int) |
| **Reference** | tools/validation.py lines 443-477 |
| **Notes** | Simple column presence check. Case-sensitive column name matching. Returns invalid if any required columns missing. |

---

### validate_lmm_assumptions_comprehensive

| Field | Value |
|-------|-------|
| **Description** | Comprehensive LMM assumption validation with 7 diagnostics: (1) Residual normality (Shapiro-Wilk + Q-Q plot), (2) Homoscedasticity (Breusch-Pagan + residuals vs fitted), (3) Random effects normality (Shapiro-Wilk + separate Q-Q plots for intercepts/slopes), (4) Autocorrelation (ACF plot + Lag-1 test), (5) Linearity (partial residual CSVs for rq_plots), (6) Outliers (Cook's distance), (7) Convergence diagnostics. Includes remedial action recommendations. |
| **Inputs** | `lmm_result: MixedLMResults` (fitted model), `data: DataFrame` (original data), `output_dir: Path` (plot save directory), `acf_lag1_threshold: float = 0.1` (ACF threshold), `alpha: float = 0.05` (significance level) |
| **Outputs** | `Dict[valid: bool, diagnostics: Dict, plot_paths: List[Path], message: str]` |
| **Reference** | RQ 5.8 1_concept.md Step 3.5, Schielzeth et al. 2020 (LMM diagnostics) |
| **Notes** | Complete rewrite of v3.0 minimal implementation. Generates 6 diagnostic plots: qq_residuals.png, residuals_vs_fitted.png, qq_random_intercepts.png, qq_random_slopes.png, acf.png, cooks_distance.png. Generates partial residual CSVs for ALL predictors. Configurable thresholds per RQ requirements. Returns `valid=True` only if ALL 7 diagnostics pass. |

### validate_contrasts_d068

| Field | Value |
|-------|-------|
| **Description** | Validate Decision D068 compliance in contrast results by checking for dual p-value reporting (uncorrected + correction method). Ensures contrasts include both p_uncorrected AND at least one correction method (p_bonferroni, p_tukey, or p_holm). Pure validation function (no computation). |
| **Inputs** | `contrasts_df: DataFrame` (contrast results with p-value columns) |
| **Outputs** | `Dict[valid: bool, d068_compliant: bool, missing_cols: List[str], message: str]` |
| **Reference** | Decision D068 (dual p-value reporting), RQ 5.9 1_concept.md Step 4, tools_todo.yaml lines 360-373 |
| **Notes** | Accepts alternative correction names: p_bonferroni, p_tukey, or p_holm (all valid correction methods). Returns `valid=True` if p_uncorrected AND at least one correction column present. Case-sensitive column names. Handles empty DataFrames (returns invalid). 11/11 tests GREEN. |

### validate_hypothesis_test_dual_pvalues

| Field | Value |
|-------|-------|
| **Description** | Validate hypothesis test results (e.g., 3-way interactions) include both required statistical terms AND Decision D068 dual p-value reporting. Checks that all specified interaction terms are present in results DataFrame AND that each has p_uncorrected + correction method columns. Used for validating LMM fixed effects tables. |
| **Inputs** | `interaction_df: DataFrame` (hypothesis test results with term names as index/column), `required_terms: List[str]` (e.g., ['Age:Domain:Time'] for 3-way interaction), `alpha_bonferroni: float = 0.05` (significance threshold, unused in validation but part of spec) |
| **Outputs** | `Dict[valid: bool, d068_compliant: bool, missing_terms: List[str], missing_cols: List[str], message: str]` |
| **Reference** | Decision D068 (dual p-value reporting), RQ 5.10 1_concept.md Step 4, tools_todo.yaml lines 375-390 |
| **Notes** | Validates TWO aspects: (1) Required terms present (e.g., 'Age:Domain:Time'), (2) D068 compliance (p_uncorrected + one of p_bonferroni/p_holm/p_fdr). Case-sensitive term matching. Handles empty DataFrames and empty required_terms list (still checks D068). 11/11 tests GREEN. |

### validate_contrasts_dual_pvalues

| Field | Value |
|-------|-------|
| **Description** | Validate post-hoc contrasts include required pairwise comparisons AND Decision D068 dual p-value reporting. Checks that contrast results DataFrame contains: (1) All required comparison names (e.g., 'Where-What', 'Where-When', 'What-When'), (2) BOTH uncorrected and corrected p-values per Decision D068. Used for validating post-hoc tests after significant interactions. |
| **Inputs** | `contrasts_df: DataFrame` (post-hoc contrast results with 'comparison' column), `required_comparisons: List[str]` (required comparison names to check) |
| **Outputs** | `Dict[valid: bool, d068_compliant: bool, missing_comparisons: List[str], message: str]` |
| **Reference** | Decision D068 (dual p-value reporting), RQ 5.10 1_concept.md Step 4, tools_todo.yaml lines 398-415 |
| **Notes** | Typically p_tukey (Tukey HSD) for post-hoc contrasts, but accepts p_bonferroni or p_holm alternatives. Case-sensitive comparison name matching. Handles empty DataFrames (returns invalid). Empty required_comparisons list allowed (still checks D068). 11/11 tests GREEN. 112 lines implementation. |

### validate_correlation_test_d068

| Field | Value |
|-------|-------|
| **Description** | Validate correlation test results include Decision D068 dual p-value reporting. Ensures correlation results contain BOTH uncorrected and corrected p-values. Supports multiple correlation tests in single DataFrame. Optional custom required_cols parameter for non-standard column names. |
| **Inputs** | `correlation_df: DataFrame` (correlation test results with p-value columns), `required_cols: List[str] = None` (optional custom required columns, defaults to D068 spec) |
| **Outputs** | `Dict[valid: bool, d068_compliant: bool, missing_cols: List[str], message: str]` |
| **Reference** | Decision D068 (dual p-value reporting), RQ 5.13 1_concept.md Step 5, tools_todo.yaml lines 417-434 |
| **Notes** | Default D068 validation: p_uncorrected + one of [p_bonferroni, p_holm, p_fdr]. Bonferroni or Holm-Bonferroni typical for correlation tests. Handles empty DataFrames (returns invalid). Reports row count in success message. 10/10 tests GREEN. 110 lines implementation. Used for validating intercept-slope correlation in RQ 5.13. |

---

## Module: tools.analysis_ctt

### compute_cronbachs_alpha

| Field | Value |
|-------|-------|
| **Description** | Compute Cronbach's alpha internal consistency reliability with bootstrap confidence intervals. For dichotomous (0/1) items, equals KR-20. Uses percentile bootstrap method (resamples participants, preserves item structure). |
| **Inputs** | `data: DataFrame` (items as columns, participants as rows), `n_bootstrap: int = 1000` (iterations, 1000-10000 recommended) |
| **Outputs** | `Dict[alpha: float, ci_lower: float, ci_upper: float, n_items: int, n_participants: int]` |
| **Reference** | Cronbach (1951), PMC4205511, PMC8451024 (KR-20 equivalence), RQ 5.12 1_concept.md Step 3b |
| **Notes** | Bootstrap percentile method for 95% CI (2.5th and 97.5th percentiles). Handles NaN via pairwise deletion. Requires ≥2 items and ≥3 participants. For N=100, CI width typically 0.02-0.15. |

---

### compare_correlations_dependent

| Field | Value |
|-------|-------|
| **Description** | Test if two dependent correlations differ significantly using Steiger's z-test. Appropriate when both correlations share a common variable (e.g., testing if r(IRT, Purified_CTT) > r(IRT, Full_CTT) from same participants). |
| **Inputs** | `r12: float` (correlation 1-2), `r13: float` (correlation 1-3), `r23: float` (correlation 2-3), `n: int` (sample size) |
| **Outputs** | `Dict[z_statistic: float, p_value: float, r_difference: float, significant: bool, interpretation: str]` |
| **Reference** | Steiger (1980) Psychological Bulletin 87:245-251, RQ 5.12 1_stats.md |
| **Notes** | Uses Steiger's (1980) equations 3 & 10 for asymptotic covariance of overlapping correlations. Fisher's z-transformation applied. Two-tailed p-value. Requires n ≥ 20, correlations in [-1, 1]. N=100 adequate for 90% power. |

---

### validate_numeric_range

| Field | Value |
|-------|-------|
| **Description** | Validate numeric values fall within specified range [min_val, max_val]. Checks for values below minimum, above maximum, NaN values, and infinite values. Returns violations list for debugging. Range is INCLUSIVE. |
| **Inputs** | `data: np.ndarray or pd.Series` (numeric data), `min_val: float` (minimum allowed, inclusive), `max_val: float` (maximum allowed, inclusive), `column_name: str` (for error messages) |
| **Outputs** | `Dict[valid: bool, message: str, out_of_range_count: int, violations: list]` |
| **Reference** | RQ 5.9 probability transformation validation, tools_todo.yaml lines 202-217 |
| **Notes** | Used for theta score range validation before probability transformation. Violations list limited to first 10 values for reporting. Handles empty data gracefully (returns valid). Example: validate theta in [-3, 3] before GRM probability transformation. 12/12 tests GREEN. ~120 lines implementation. 10 min development time. |

---

### validate_data_format

| Field | Value |
|-------|-------|
| **Description** | Validate DataFrame has all required columns present. Does NOT check for missing values within columns - only column presence. Case-sensitive column name matching. Column order irrelevant. |
| **Inputs** | `df: DataFrame` (DataFrame to validate), `required_cols: List[str]` (list of required column names, case-sensitive) |
| **Outputs** | `Dict[valid: bool, message: str, missing_cols: List[str]]` |
| **Reference** | RQ 5.9 fixed effects table validation, tools_todo.yaml lines 324-339 |
| **Notes** | Simple column presence check. Reports both missing columns and present columns in message. Empty DataFrame returns invalid if required_cols specified. Empty required_cols list returns valid (trivial case). Used for validating LMM fixed effects table format. 11/11 tests GREEN. ~65 lines implementation. 10 min development time. |

---

### validate_effect_sizes

| Field | Value |
|-------|-------|
| **Description** | Validate Cohen's f² effect sizes are within reasonable bounds. Checks for negative values (invalid), NaN/infinite values (invalid), and very large values f²>1.0 (warning but valid). Follows Cohen (1988) guidelines. |
| **Inputs** | `effect_sizes_df: DataFrame` (DataFrame containing effect sizes), `f2_column: str = 'cohens_f2'` (column name for f² values) |
| **Outputs** | `Dict[valid: bool, message: str, warnings: List[str]]` |
| **Reference** | Cohen (1988) Statistical Power Analysis, RQ 5.9 effect size validation, tools_todo.yaml lines 436-452 |
| **Notes** | Cohen (1988) guidelines: f²=0.02 (small), f²=0.15 (medium), f²=0.35 (large), f²>1.0 (very large, uncommon). Very large values trigger warnings but don't invalidate. Reports min/max range in success message. Handles empty DataFrames (returns valid). 13/13 tests GREEN. ~105 lines implementation. 10 min development time. |

---

### validate_probability_range

| Field | Value |
|-------|-------|
| **Description** | Validate probability values are in [0, 1] with no NaN/infinite values. Checks multiple probability columns simultaneously. Returns detailed violation information per column. Range is INCLUSIVE (0 and 1 are valid). |
| **Inputs** | `probability_df: DataFrame` (DataFrame with probability columns), `prob_columns: List[str]` (list of column names to validate) |
| **Outputs** | `Dict[valid: bool, message: str, violations: List[Dict]]` |
| **Reference** | RQ 5.9 IRT theta→probability transformation validation, tools_todo.yaml lines 235-248 |
| **Notes** | Used for validating GRM probability transformation output. Violations list contains dicts with column, issue, count, and example fields. Checks each column for: values <0, values >1, NaN, infinite. Reports total columns and total values in success message. Handles empty DataFrames gracefully. 11/11 tests GREEN. ~125 lines implementation. 10 min development time. |

---

### validate_model_convergence

| Field | Value |
|-------|-------|
| **Description** | Validate statsmodels LMM model converged successfully. Checks model.converged attribute to ensure optimization algorithm reached a solution. Handles missing converged attribute gracefully. |
| **Inputs** | `lmm_result: statsmodels MixedLMResults` (fitted LMM results object) |
| **Outputs** | `Dict[valid: bool, message: str, converged: bool]` |
| **Reference** | RQ 5.13 LMM convergence validation, tools_todo.yaml lines 278-291 |
| **Notes** | Statsmodels sets converged=True when optimization succeeds. Convergence failures indicate: collinearity, insufficient data, model specification issues, or numerical instability. Returns False if converged attribute missing. Simple boolean check - fastest validator. 6/6 tests GREEN. ~67 lines implementation. 10 min development time. |

### validate_standardization

| Field | Value |
|-------|-------|
| **Description** | Validate z-score standardization (mean ≈ 0, SD ≈ 1). Checks that standardized variables have mean within tolerance of 0 and SD within tolerance of 1. Used for pre-clustering validation to ensure all variables on same scale. |
| **Inputs** | `df: pd.DataFrame` (data with standardized columns), `column_names: List[str]` (columns to validate), `tolerance: float` (default 0.01, allows for sampling variation) |
| **Outputs** | `Dict[valid: bool, message: str, mean_values: Dict[str, float], sd_values: Dict[str, float]]` |
| **Reference** | RQ 5.14 clustering pre-validation, tools_todo.yaml lines 222-237 |
| **Notes** | Configurable tolerance parameter accounts for sampling variation (N=100 scenarios). Default tolerance 0.01 allows small deviations from ideal 0/1. Reports actual mean/SD values for all columns. Handles NaN via pairwise deletion in scipy.stats. 11/11 tests GREEN. ~107 lines implementation. 10 min development time. |

### validate_variance_positivity

| Field | Value |
|-------|-------|
| **Description** | Validate all LMM variance components > 0. Negative or zero variance indicates estimation issues (collinearity, convergence failure, model misspecification). Used for RQ 5.13 LMM variance validation. |
| **Inputs** | `variance_df: pd.DataFrame` (variance components table), `component_col: str` (column name for component names, default 'component'), `value_col: str` (column name for variance values, default 'variance') |
| **Outputs** | `Dict[valid: bool, message: str, negative_components: List[str], variance_range: Tuple[float, float]]` |
| **Reference** | RQ 5.13 LMM variance validation, tools_todo.yaml lines 302-316 |
| **Notes** | Detects negative or zero variance components which should never occur in valid LMM results. Reports range of variance values and lists any problematic components. Common causes: collinearity between random effects, convergence issues, overparameterized random effects structure. 11/11 tests GREEN. ~85 lines implementation. 10 min development time. |

### validate_icc_bounds

| Field | Value |
|-------|-------|
| **Description** | Validate ICC values in [0,1] range. ICCs outside this range indicate computation errors since ICC is a proportion of variance. Used for RQ 5.13 ICC validation. |
| **Inputs** | `icc_df: pd.DataFrame` (ICC results table), `icc_col: str` (column name for ICC values, default 'icc_value') |
| **Outputs** | `Dict[valid: bool, message: str, out_of_bounds: List[Dict], icc_range: Tuple[float, float]]` |
| **Reference** | RQ 5.13 ICC computation validation, tools_todo.yaml lines 318-332 |
| **Notes** | Boundary values 0 and 1 are inclusive (valid). Detects NaN and values <0 or >1. Reports range of ICC values in message. Out-of-bounds ICCs indicate: formula error, negative variance components, or missing data. 10/10 tests GREEN. ~87 lines implementation. 10 min development time. |

### validate_dataframe_structure

| Field | Value |
|-------|-------|
| **Description** | Generic DataFrame validation (rows, columns, types). Flexible validator for checking expected structure of analysis outputs. Supports exact row count or range. Optional type checking. |
| **Inputs** | `df: pd.DataFrame` (data to validate), `expected_rows: Union[int, Tuple[int, int]]` (exact count or (min, max) range), `expected_columns: List[str]` (required columns), `column_types: Optional[Dict[str, type]]` (expected dtypes) |
| **Outputs** | `Dict[valid: bool, message: str, checks: Dict[str, bool]]` |
| **Reference** | RQ 5.14 clustering outputs validation, tools_todo.yaml lines 183-199 |
| **Notes** | Three validation checks: (1) Row count in expected range, (2) All required columns present, (3) Column types match (if specified). Reports all checks separately in 'checks' dict. Flexible row count parameter: int for exact, tuple for range. Used for validating clustering assignments, centroids, summary tables. 10/10 tests GREEN. ~117 lines implementation. 10 min development time. |

### validate_plot_data_completeness

| Field | Value |
|-------|-------|
| **Description** | Verify all domains/groups present in plot data. Checks for missing categories that would create incomplete visualizations. Used for RQ 5.10 age effects plot validation. |
| **Inputs** | `plot_data: pd.DataFrame` (plot source data), `required_domains: List[str]` (expected domains), `required_groups: List[str]` (expected groups), `domain_col: str` (default 'domain'), `group_col: str` (default 'group') |
| **Outputs** | `Dict[valid: bool, message: str, missing_domains: List[str], missing_groups: List[str]]` |
| **Reference** | RQ 5.10 age effects visualization validation, tools_todo.yaml lines 352-369 |
| **Notes** | Configurable column names for domain and group variables. Reports missing domains and missing groups separately. Lightweight validator for ensuring complete factorial design in plot data. All domains and groups must be present for valid visualization. 6/6 tests GREEN. ~32 lines implementation. 10 min development time. |

### validate_cluster_assignment

| Field | Value |
|-------|-------|
| **Description** | Validate K-means cluster assignments. Checks cluster IDs are consecutive (0, 1, ..., K-1) and enforces minimum cluster size to prevent singleton clusters. |
| **Inputs** | `cluster_labels: Union[np.ndarray, pd.Series]` (cluster assignments), `n_expected: int` (expected number of participants), `min_cluster_size: int` (default 5, minimum participants per cluster) |
| **Outputs** | `Dict[valid: bool, message: str, cluster_sizes: Dict[int, int], n_clusters: int]` |
| **Reference** | RQ 5.14 clustering validation, tools_todo.yaml lines 471-486 |
| **Notes** | Three checks: (1) All participants assigned (length = n_expected), (2) Cluster IDs consecutive starting from 0, (3) Each cluster has >= min_cluster_size members. Reports actual cluster sizes in output dict. Prevents degenerate solutions with tiny or empty clusters. 4/4 tests GREEN. ~32 lines implementation. 10 min development time. |

### validate_bootstrap_stability

| Field | Value |
|-------|-------|
| **Description** | Validate clustering stability via Jaccard coefficient. Checks Jaccard values in [0,1] range, computes mean and 95% CI from bootstrap distribution. Stability threshold typically 0.75 for reliable clustering. |
| **Inputs** | `jaccard_values: Union[np.ndarray, List[float]]` (Jaccard coefficients from bootstrap iterations), `min_jaccard_threshold: float` (default 0.75, stability threshold) |
| **Outputs** | `Dict[valid: bool, message: str, mean_jaccard: float, ci_lower: float, ci_upper: float, above_threshold: bool]` |
| **Reference** | RQ 5.14 bootstrap clustering validation, tools_todo.yaml lines 488-505 |
| **Notes** | Jaccard coefficient measures overlap between original and bootstrap clustering solutions. Values: 0 = no overlap, 1 = perfect agreement. Mean >= 0.75 indicates stable clusters. 95% CI computed via percentile method (2.5th and 97.5th percentiles). Fixed numpy boolean conversion issue during development. 4/4 tests GREEN. ~40 lines implementation. 10 min development time. |

### validate_cluster_summary_stats

| Field | Value |
|-------|-------|
| **Description** | Validate cluster summary statistics consistency. Checks mathematical constraints: min <= mean <= max, SD >= 0, N > 0. Ensures summary tables are internally consistent. |
| **Inputs** | `summary_df: pd.DataFrame` (cluster summary table), `min_col: str` (default 'min'), `mean_col: str` (default 'mean'), `max_col: str` (default 'max'), `sd_col: str` (default 'sd'), `n_col: str` (default 'N') |
| **Outputs** | `Dict[valid: bool, message: str, failed_checks: List[str]]` |
| **Reference** | RQ 5.14 cluster summary tables validation, tools_todo.yaml lines 505-519 |
| **Notes** | Flexible column naming for different summary table formats. Three mathematical checks: (1) min <= mean <= max for each row, (2) SD >= 0, (3) N > 0. Reports specific failed checks with row indices. Detects computation errors in clustering summary statistics. 4/4 tests GREEN. ~47 lines implementation. 10 min development time. |

---

## Module: tools.config

### load_config_from_file

| Field | Value |
|-------|-------|
| **Description** | Load YAML config file with caching |
| **Inputs** | `config_name: str` (name of config: 'paths', 'plotting', 'irt', 'lmm') |
| **Outputs** | `Dict[str, Any]` (configuration dictionary) |
| **Reference** | tools/config.py lines 65-108 |
| **Notes** | Loads from config/{config_name}.yaml with global caching. Raises FileNotFoundError or yaml.YAMLError on failure. |

### load_config_from_yaml

| Field | Value |
|-------|-------|
| **Description** | Get config value by dot-separated key path |
| **Inputs** | `config_name: str` (config name), `key_path: Optional[str] = None` (dot path like 'data.master', None returns full config) |
| **Outputs** | `Any` (configuration value at key_path) |
| **Reference** | tools/config.py lines 111-150 |
| **Notes** | Supports nested key access via dot notation. Raises KeyError if path doesn't exist. |

### resolve_path_from_config

| Field | Value |
|-------|-------|
| **Description** | Get path from paths.yaml, format templates, return absolute Path |
| **Inputs** | `key_path: str` (dot path to path string), `**kwargs` (template vars, e.g., n=1 for rq{n}) |
| **Outputs** | `Path` (absolute path object) |
| **Reference** | tools/config.py lines 155-190 |
| **Notes** | Resolves paths from paths.yaml with template formatting support (e.g., `rq{n}` → `rq1`). Returns absolute paths. |

### load_plot_config_from_yaml

| Field | Value |
|-------|-------|
| **Description** | Shorthand for load_config_from_yaml('plotting', key_path) |
| **Inputs** | `key_path: Optional[str] = None` |
| **Outputs** | `Any` (plotting config value) |
| **Reference** | tools/config.py lines 193-195 |
| **Notes** | Convenience function for accessing plotting configuration. |

### load_irt_config_from_yaml

| Field | Value |
|-------|-------|
| **Description** | Shorthand for load_config_from_yaml('irt', key_path) |
| **Inputs** | `key_path: Optional[str] = None` |
| **Outputs** | `Any` (IRT config value) |
| **Reference** | tools/config.py lines 198-200 |
| **Notes** | Convenience function for accessing IRT configuration. |

### load_lmm_config_from_yaml

| Field | Value |
|-------|-------|
| **Description** | Shorthand for load_config_from_yaml('lmm', key_path) |
| **Inputs** | `key_path: Optional[str] = None` |
| **Outputs** | `Any` (LMM config value) |
| **Reference** | tools/config.py lines 203-205 |
| **Notes** | Convenience function for accessing LMM configuration. |

### merge_config_dicts

| Field | Value |
|-------|-------|
| **Description** | Deep merge dicts (override takes precedence, returns new dict) |
| **Inputs** | `base: Dict` (base dictionary), `override: Dict` (override dictionary) |
| **Outputs** | `Dict` (merged dictionary, non-mutating) |
| **Reference** | tools/config.py lines 246-273 |
| **Notes** | Performs deep merge where override values replace base values recursively. Returns new dict without mutating inputs. |

### load_rq_config_merged

| Field | Value |
|-------|-------|
| **Description** | Load RQ config with 3-tier merge (global → chapter → RQ) |
| **Inputs** | `chapter: int` (chapter number: 5, 6, 7), `rq: int` (RQ number) |
| **Outputs** | `Dict[str, Any]` (merged configuration dictionary) |
| **Reference** | tools/config.py lines 276-338 |
| **Notes** | Merges config from 3 levels: global config, chapter-specific overrides, RQ-specific overrides. Enables per-RQ configuration customization. |

### reset_config_cache

| Field | Value |
|-------|-------|
| **Description** | Clear global config cache (for testing) |
| **Inputs** | None |
| **Outputs** | None |
| **Reference** | tools/config.py lines 363-370 |
| **Notes** | Resets _CONFIG_CACHE to empty dict. Used in testing to ensure clean state between tests. |

---

**End of Tools Inventory**
