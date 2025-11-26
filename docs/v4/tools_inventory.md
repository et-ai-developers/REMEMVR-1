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

---

## Module: tools.plotting

### convert_theta_to_probability

| Field | Value |
|-------|-------|
| **Description** | Transform theta scores to probability scale via IRT 2PL formula |
| **Inputs** | `theta: ndarray`, `discrimination: float` (default 1.0), `difficulty: float` (default 0.0) |
| **Outputs** | `ndarray` of probabilities in range [0, 1] |

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

---

### validate_lmm_assumptions_comprehensive

| Field | Value |
|-------|-------|
| **Description** | Comprehensive LMM assumption validation with 7 diagnostics: (1) Residual normality (Shapiro-Wilk + Q-Q plot), (2) Homoscedasticity (Breusch-Pagan + residuals vs fitted), (3) Random effects normality (Shapiro-Wilk + separate Q-Q plots for intercepts/slopes), (4) Autocorrelation (ACF plot + Lag-1 test), (5) Linearity (partial residual CSVs for rq_plots), (6) Outliers (Cook's distance), (7) Convergence diagnostics. Includes remedial action recommendations. |
| **Inputs** | `lmm_result: MixedLMResults` (fitted model), `data: DataFrame` (original data), `output_dir: Path` (plot save directory), `acf_lag1_threshold: float = 0.1` (ACF threshold), `alpha: float = 0.05` (significance level) |
| **Outputs** | `Dict[valid: bool, diagnostics: Dict, plot_paths: List[Path], message: str]` |
| **Reference** | RQ 5.8 1_concept.md Step 3.5, Schielzeth et al. 2020 (LMM diagnostics) |
| **Notes** | Complete rewrite of v3.0 minimal implementation. Generates 6 diagnostic plots: qq_residuals.png, residuals_vs_fitted.png, qq_random_intercepts.png, qq_random_slopes.png, acf.png, cooks_distance.png. Generates partial residual CSVs for ALL predictors. Configurable thresholds per RQ requirements. Returns `valid=True` only if ALL 7 diagnostics pass. |

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

**End of Tools Inventory**
