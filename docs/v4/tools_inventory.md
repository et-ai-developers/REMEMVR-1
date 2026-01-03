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

---

## Module: tools.model_selection

### compare_lmm_models_kitchen_sink

| Field | Value |
|-------|-------|
| **Status** | ✅ VALIDATED (2025-12-08) |
| **Description** | Comprehensive LMM model selection testing 70+ time transformations across 9 families (polynomial, logarithmic, power-law, root, reciprocal, exponential, trigonometric, hyperbolic, hybrids). Kitchen-sink approach to identify best functional form for forgetting trajectories. **CRITICAL: Requires continuous TSVR** (not categorical session indicators). |
| **Inputs** | `data: DataFrame` (with outcome, TSVR_hours, groups, optional factors), `outcome_var: str`, `tsvr_var: str` (continuous time in hours), `groups_var: str` (e.g., 'UID'), `factor1_var: str = None` (categorical or continuous), `factor1_type: str = 'categorical'`, `factor1_reference: str = None` (required if categorical), `factor2_var: str = None` (for 2-way interactions), `factor2_type: str = 'categorical'`, `factor2_reference: str = None`, `re_formula: str = '~TSVR'` (random effects specification), `reml: bool = False` (ML for model comparison), `return_models: bool = False`, `save_dir: Path = None`, `log_file: Path = None`, `min_converged_models: int = 10`, `aic_tolerance: float = 0.001` |
| **Outputs** | `Dict` with keys: `comparison` (DataFrame with model_name, AIC, delta_AIC, akaike_weight, cumulative_weight, BIC, log_likelihood, n_params, converged), `best_model` (dict with name, AIC, weight, weight_pct, uncertainty ['Very strong'\|'Strong'\|'Moderate'\|'High'], interpretation, rank), `log_model_info` (dict with rank, AIC, delta_AIC, weight, weight_pct for theoretical benchmark), `top_10` (DataFrame), `failed_models` (List[str]), `transformations` (Dict[str, str] of all time transforms created), `summary_stats` (dict with n_models_tested, n_models_converged, n_models_failed, best_model, best_aic, aic_range, n_competitive_models), `fitted_models` (Dict[str, MixedLMResults] if return_models=True) |
| **Model Suite** | **Polynomial (6):** Linear, Quadratic, Cubic, Quartic, Quadratic_pure, Cubic_pure<br>**Logarithmic (8):** Log, Log2, Log10, LogLog, Lin+Log, Quad+Log, Log+LogLog, Lin+Quad+Log<br>**Power Law (12):** PowerLaw_01 through PowerLaw_10 (α=0.1 to 1.0), PowerLaw_Log, PowerLaw_Lin<br>**Root (9):** SquareRoot, CubeRoot, FourthRoot, Root_033, Root_067, SquareRoot+Log, CubeRoot+Log, SquareRoot+Lin, Root_Multi<br>**Reciprocal (6):** Reciprocal, Recip+Log, Recip+Lin, Recip+Quad, Recip_sq, Recip+PowerLaw<br>**Exponential (7):** Exponential_proxy, Exp+Log, Exp+Lin, Exp_fast, Exp_slow, Exp+PowerLaw, Exp+Recip<br>**Trigonometric (4):** Sin, Cos, Sin+Cos, Sin+Log<br>**Hyperbolic (4):** Tanh, Tanh+Log, Arctanh, Sinh<br>**Hybrids (10):** Log+PowerLaw05, Log+SquareRoot, Log+Recip, SquareRoot+PowerLaw, SquareRoot+Recip, Recip+PowerLaw05, Lin+Log+PowerLaw, Quad+Log+SquareRoot, PowerLaw+Recip+Log, Ultimate (6-term kitchen sink)<br>**TOTAL: ~66 models** |
| **Interactions** | Supports 0-way (simple trajectory), 1-way (time × factor1), 2-way (time × factor1 × factor2). **No 3-way** (insufficient data). Categorical factors use Treatment coding with explicit reference. Continuous factors automatically mean-centered. |
| **Validation** | Enforces continuous TSVR (>10 unique values, numeric dtype). Range warning if TSVR >300h. Akaike weights sum to 1.0 ± tolerance. All weights in (0,1). Best model delta_AIC = 0. Cumulative weights monotonic. Warns (not errors) if <10 models converge. |
| **Use Cases** | **ROOT RQs:** 5.1.1 (general forgetting), 5.2.1 (domain trajectories), 5.3.1 (paradigm trajectories), 5.4.1 (congruence trajectories), 5.5.1 (source-destination), 6.1.1+ (confidence trajectories)<br>**Replaces:** step05 + step06 (446 lines → 20 lines per RQ)<br>**Benefits:** Standardized, comprehensive, discovers power-law/root models missed by basic 5-model suite |
| **Example** | `results = compare_lmm_models_kitchen_sink(data=lmm_input, outcome_var='theta', tsvr_var='TSVR_hours', groups_var='UID', factor1_var='domain', factor1_type='categorical', factor1_reference='What', re_formula='~log_TSVR')`<br>`print(results['best_model'])` → `{'name': 'PowerLaw_05', 'AIC': 866.74, 'weight': 0.1524, 'uncertainty': 'Moderate', ...}` |
| **Important Notes** | (1) **TSVR must be continuous** - Tool rejects categorical session indicators (T1/T2/T3/T4). (2) **Random effects specification CRITICAL:** The `re_formula` parameter affects absolute AIC values but preserves model rankings (ΔAIC unchanged). Use `'~log_TSVR'` or `'~TSVR'` for simple trajectories (allows individual forgetting rates to vary), `'~1'` for complex interactions (aids convergence). **Random slopes add ~4 AIC penalty** (2 parameters: slope variance + slope-intercept covariance) vs intercept-only models - this is expected and correct. To match existing analyses, use same `re_formula` specification. (3) **Numerical precision validated:** When using same `re_formula` as existing step05b, produces bit-exact identical AICs (validated on RQ 5.1.1: 11/11 models matched perfectly). (4) **Log model benchmark:** Always reports Log model rank/weight for theoretical comparison (Ebbinghaus vs Wixted debate). (5) **Time unit:** Expects TSVR in hours, converts to days internally. (6) **Execution time:** ~5-10 minutes for 70 models (7 seconds on RQ 5.1.1 with 400 observations). (7) **Output files:** If save_dir specified, writes `model_comparison.csv` and `best_model_summary.txt`. |
| **References** | RQ 5.1.1 extended comparison (PowerLaw α=0.5 wins, Log ranked #10), RQ 5.4.1 (Recip+Log wins decisively), MODEL_SELECTION_SUMMARY.md (complete Ch5/Ch6 findings) |

---

## Module: tools.variance_decomposition

### compute_model_averaged_variance_decomposition

| Field | Value |
|-------|-------|
| **Status** | ✅ VALIDATED (2025-12-09) |
| **Description** | Model-averaged variance decomposition for stratified LMMs when functional form uncertainty is high (best model weight <30%). Implements Burnham & Anderson (2002) multi-model inference for variance component analysis. Integrates with `compare_lmm_models_kitchen_sink` to identify competitive models, fits stratified LMMs for each level × model combination, then Akaike-averages variance components, ICCs, and random effects. Returns both model-specific AND averaged results for complete transparency. **Addresses critical gap:** When Log vs PowerLaw vs Recip+Log are all competitive, variance decomposition results depend on chosen functional form - model averaging provides robust estimates acknowledging this uncertainty. |
| **Inputs** | `data: DataFrame` (with outcome, TSVR_hours, groups, stratify_var), `outcome_var: str` (e.g., 'theta'), `tsvr_var: str` (continuous time in hours), `groups_var: str` (e.g., 'UID'), `stratify_var: str` (categorical variable for stratification, e.g., 'congruence'), `stratify_levels: List[str]` (levels to analyze, e.g., ['Common', 'Congruent', 'Incongruent']), `delta_aic_threshold: float = 2.0` (only average models with ΔAIC < threshold), `min_models: int = 3` (minimum models to average, warning if less), `max_models: int = 10` (maximum models to average, caps computational cost), `re_intercept: bool = True` (include random intercepts), `re_slope: bool = True` (include random slopes on time variable), `save_dir: Path = None` (if provided, save outputs), `log_file: Path = None` (detailed execution log), `return_fitted_models: bool = False` (return model objects, large memory), `reml: bool = False` (ML for model comparison), `handle_convergence_failures: str = 'warn'` ('warn', 'skip', or 'error') |
| **Outputs** | `Dict` with keys: `model_comparison` (DataFrame from kitchen_sink with all models), `competitive_models` (List[str] of models used for averaging), `stratified_results` (Dict mapping stratify_level → level_results), `averaged_variance_components` (DataFrame with model-averaged var_int, var_slope, cov, var_resid per level), `averaged_ICCs` (DataFrame with model-averaged ICC_intercept, ICC_slope_simple, ICC_slope_conditional per level), `averaged_random_effects` (DataFrame with model-averaged participant-specific intercepts/slopes, N_UID × N_levels rows), `summary_stats` (Dict with n_models_competitive, n_stratify_levels, total_lmm_fits, total_converged, convergence_rate, effective_n_models, cumulative_weight, best_model, best_model_weight).<br><br>**level_results structure:** Each stratify_level contains: `variance_components_by_model` (DataFrame showing variance components for each model), `ICCs_by_model` (DataFrame showing ICCs for each model), `random_effects_by_model` (Dict mapping model_name → DataFrame with UID-specific effects), `variance_components_averaged` (Series with Akaike-weighted averages), `ICCs_averaged` (Series with Akaike-weighted ICC averages), `random_effects_averaged` (DataFrame with Akaike-weighted participant effects), `convergence_status` (Dict mapping model_name → bool), `n_models_converged` (int) |
| **Workflow** | **Step 1:** Run `compare_lmm_models_kitchen_sink` on FULL dataset (unstratified) to identify competitive functional forms (ΔAIC < threshold). **Rationale:** Functional form uncertainty is global property, not level-specific. **Step 2:** Select top competitive models, cap at `max_models`, renormalize Akaike weights to sum to 1.0. **Step 3:** For EACH stratified level: (a) Subset data to level, (b) For EACH competitive model: fit stratified LMM, extract variance components (var_int, var_slope, cov, var_resid), compute ICCs (3 types), extract random effects (participant-specific intercepts/slopes), record convergence status. **Step 4:** For EACH stratified level: model-average variance components using renormalized weights, model-average ICCs, model-average random effects via weighted sum across models. **Step 5:** Aggregate results across levels into summary DataFrames. **Step 6:** Save outputs if `save_dir` specified (model comparison, competitive models, averaged components, averaged ICCs, averaged random effects, model-specific results per level). |
| **Variance Averaging** | For each variance component c and stratify level L: `var_c_avg[L] = Σ(w[m] × var_c[m,L]) / Σ(w[m])` where w[m] = renormalized Akaike weight for model m (converged models only). Same formula for ICCs. |
| **Random Effects Averaging** | For each participant p, stratify level L, and effect type (intercept/slope): `RE_avg[p,L] = Σ(w[m] × RE[m,p,L]) / Σ(w[m])`. Direct averaging (not BLUPs from averaged model). **Output structure:** N_UID × N_levels rows with columns: UID, stratify_var, intercept_avg, slope_avg (if re_slope=True). Compatible with clustering analyses (RQ X.X.7 derivatives). |
| **Use Cases** | **RQ 5.4.6:** Schema congruence variance decomposition (3 stratified levels: Common, Congruent, Incongruent). Feeds RQ 5.4.7 clustering with 300 random effects (100 UID × 3 congruence).<br>**RQ 5.2.6:** Domain variance decomposition (2 stratified levels: What, Where; When excluded due to floor effect). Feeds RQ 5.2.7 clustering with 200 random effects.<br>**RQ 5.3.7:** Paradigm variance decomposition (3 stratified levels: IFR, ICR, IRE). Feeds RQ 5.3.8 clustering with 300 random effects.<br>**Any RQ testing:** "Is forgetting rate trait-like within X category?" when ROOT RQ shows high model uncertainty (effective N > 10 models). |
| **Convergence Handling** | Stratified LMMs may fail to converge when ICC_slope ≈ 0 (variance too small to estimate). Tool handles gracefully via `handle_convergence_failures` parameter: 'warn' logs warning and skips failed model (default), 'skip' silently continues, 'error' raises exception. Failed models excluded from averaging; weights renormalized over converged models only. Reports convergence status per level and overall convergence rate. |
| **Validation** | Unit tests (13 functions, 5 passing helper tests + integration tests): (1) Time transformations correctness, (2) Formula building, (3) Time variable identification, (4) Single model fit and extract, (5) Invalid input rejection, (6) Akaike weights sum to 1.0, (7) Model-averaged ICCs bounded in [0,1], (8) Random effects centered at zero, (9) RQ 5.4.6 output structure (300 rows for 100 UID × 3 congruence), (10) File saving, (11) Convergence failure handling, (12) Random-intercepts-only mode (no slopes), (13) Statistical validity checks. |
| **Performance** | **Computational cost:** N_models × N_levels × N_participants LMM fits. Example: 6 models × 3 congruence levels × 100 UID = 18 LMM fits (~2-5 minutes). Cap at `max_models=10` to limit runtime. **Memory:** ~10 MB per fitted model; set `return_fitted_models=False` to reduce memory usage. **Parallelization:** Sequential (statsmodels LMM not thread-safe); future versions may parallelize across models. |
| **Important Notes** | (1) **Model selection runs ONCE** on full dataset, not per level (functional form is global). (2) **Random effects averaging is DIRECT:** weighted sum of participant-specific effects, not BLUPs from averaged model. Alternative approaches (e.g., fit single model with averaged predictions) not supported. (3) **Transparency priority:** Returns both model-specific AND averaged results; model-specific results saved to `level_{L}/` subdirectories for auditing. (4) **When NOT to use:** Single best model has >30% weight (no uncertainty), random-intercepts-only sufficient (no slopes), stratification not needed (e.g., omnibus forgetting rate). (5) **Burnham & Anderson threshold:** <30% weight mandates model averaging (their recommendation from Ch 2). (6) **Effective N models:** Shannon diversity index H = exp(-Σ w_i log w_i), indicates uncertainty distribution (low = concentrated, high = diffuse). |
| **Example** | `results = compute_model_averaged_variance_decomposition(data=lmm_input, outcome_var='theta', tsvr_var='TSVR_hours', groups_var='UID', stratify_var='congruence', stratify_levels=['Common', 'Congruent', 'Incongruent'], delta_aic_threshold=2.0, max_models=6, save_dir=Path('results/ch5/5.4.6/data'))`<br>`print(results['averaged_ICCs'])` → DataFrame with 3 rows (Common, Congruent, Incongruent) × 4 columns (congruence, ICC_intercept, ICC_slope_simple, ICC_slope_conditional)<br>`random_effects = results['averaged_random_effects']` → 300 rows (100 UID × 3 congruence) for RQ 5.4.7 clustering |
| **References** | Burnham & Anderson (2002) "Model Selection and Multimodel Inference" Ch 2 (Akaike weights), Ch 4 (model averaging), Burnham & Anderson (2004) "Multimodel inference: Understanding AIC and BIC", RQ 5.4.6 1_concept.md, RQ 5.4.1 extended model selection (15 competitive models, effective N=13.96 motivates model averaging) |

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

### extract_marginal_age_slopes_by_domain

| Field | Value |
|-------|-------|
| **Description** | Extract domain-specific marginal age effects on forgetting rate from 3-way Age×Domain×Time interaction LMM. Computes marginal effect of age at specific timepoint using delta method for SE propagation through linear combinations. RQ 5.10 quantifies domain-specific age-related memory decline. |
| **Inputs** | `lmm_result: MixedLMResults` (fitted 3-way interaction model), `eval_timepoint: float = 72.0` (TSVR hours for slope evaluation, default Day 3), `domain_var: str = "domain"`, `age_var: str = "Age_c"` (centered age), `time_linear: str = "TSVR_hours"`, `time_log: str = "log_TSVR"` |
| **Outputs** | `DataFrame[domain: str, age_slope: float, se: float, z: float, p: float, CI_lower: float, CI_upper: float]` with 3 rows (What, Where, When) |
| **Reference** | RQ 5.10 Step 4, tools/analysis_lmm.py lines 1988-2190, Delta method: Casella & Berger (2002) Statistical Inference p.240 |
| **Notes** | **Model structure**: `theta ~ TSVR + log_TSVR + Age_c + Domain + TSVR:Age_c + log_TSVR:Age_c + TSVR:Domain + log_TSVR:Domain + Age_c:Domain + TSVR:Age_c:Domain + log_TSVR:Age_c:Domain`. **Marginal age slope formula**: For reference domain (What): β(TSVR:Age_c) + β(log_TSVR:Age_c) × 1/(TSVR+1). For non-reference domains (Where/When): Reference slope + β(TSVR:Age_c:Domain[X]) + β(log_TSVR:Age_c:Domain[X]) × 1/(TSVR+1). **Delta method SE**: Uses 4-term gradient [∂slope/∂β_linear_ref, ∂slope/∂β_log_ref, ∂slope/∂β_linear_3way, ∂slope/∂β_log_3way] = [1, 1/(TSVR+1), 1, 1/(TSVR+1)] with full variance-covariance matrix. **Auto-detection**: Identifies reference domain by absence of [T.] prefix in coefficient names (treatment coding). **Derivative**: ∂log(TSVR+1)/∂TSVR = 1/(TSVR+1). **Default eval_timepoint**: 72h = Day 3 (midpoint of 0-168h observation window). **15/15 tests GREEN** using real RQ 5.10 data. 203 lines implementation. |

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

### compute_ctt_mean_scores_by_factor

| Field | Value |
|-------|-------|
| **Description** | Compute CTT mean scores (proportion correct) per UID × test × factor. Core CTT computation for IRT-CTT convergence analyses. Works with any factor type: domain (What/Where/When), paradigm (IFR/ICR/IRE), or congruence (Common/Congruent/Incongruent). |
| **Inputs** | `df_wide: DataFrame` (wide format with UID, TEST, composite_ID, item columns), `item_factor_df: DataFrame` (item-to-factor mapping), `factor_col: str = 'factor'`, `item_col: str = 'item_name'`, `include_factors: Optional[List[str]] = None` (filter to subset of factors) |
| **Outputs** | `DataFrame[composite_ID, UID, test, factor, CTT_score, n_items]` |
| **Reference** | RQ 5.2.4 step01_compute_ctt_mean_scores.py, RQ 5.3.5, RQ 5.4.4 |
| **Notes** | CTT_score is proportion correct (0-1 range). n_items counts items per factor. Handles missing items gracefully (uses available items). Raises ValueError on empty data. 27/27 tests GREEN. |

---

### compute_pearson_correlations_with_correction

| Field | Value |
|-------|-------|
| **Description** | Compute Pearson correlations between IRT and CTT scores with Holm-Bonferroni correction. Implements Decision D068 dual p-value reporting (p_uncorrected + p_holm). Computes correlations per factor plus overall (all factors pooled). |
| **Inputs** | `df: DataFrame` (with IRT and CTT score columns), `irt_col: str = 'IRT_score'`, `ctt_col: str = 'CTT_score'`, `factor_col: str = 'factor'`, `thresholds: Optional[List[float]] = [0.70, 0.90]` |
| **Outputs** | `DataFrame[factor, r, CI_lower, CI_upper, p_uncorrected, p_holm, n, threshold_X.XX]` |
| **Reference** | Decision D068 (dual p-value reporting), Holm (1979), RQ 5.2.4 step02_correlations.py |
| **Notes** | Uses Fisher z-transform for 95% CI. Holm-Bonferroni is less conservative than Bonferroni but maintains FWER control. Includes 'Overall' row (all factors pooled). Threshold columns are boolean. 27/27 tests GREEN. |

---

### compute_cohens_kappa_agreement

| Field | Value |
|-------|-------|
| **Description** | Compute Cohen's kappa for agreement between two significance classifications. Assesses agreement between IRT and CTT models on which effects are statistically significant. Accounts for chance agreement. |
| **Inputs** | `classifications_1: List[bool]` (e.g., IRT model significance), `classifications_2: List[bool]` (e.g., CTT model significance), `labels: Optional[List[str]] = None` (effect names for reporting) |
| **Outputs** | `Dict[kappa: float, agreement_percent: float, interpretation: str, n_effects: int, substantial_agreement: bool, confusion_matrix: Dict]` |
| **Reference** | Cohen (1960), Landis & Koch (1977), RQ 5.2.4 step05 |
| **Notes** | Interpretation thresholds per Landis & Koch: <0.20 slight, 0.20-0.40 fair, 0.40-0.60 moderate, 0.60-0.80 substantial, ≥0.80 almost perfect. substantial_agreement is True when kappa > 0.60. 27/27 tests GREEN. |

---

### compare_lmm_fit_aic_bic

| Field | Value |
|-------|-------|
| **Description** | Compare model fit between two LMMs using AIC and BIC. Computes delta (model2 - model1) and interprets per Burnham & Anderson (2002). |
| **Inputs** | `aic_model1: float`, `bic_model1: float`, `aic_model2: float`, `bic_model2: float`, `model1_name: str = 'Model1'`, `model2_name: str = 'Model2'` |
| **Outputs** | `DataFrame[metric, {model1_name}, {model2_name}, delta, interpretation]` (2 rows: AIC, BIC) |
| **Reference** | Burnham & Anderson (2002), RQ 5.2.4 step06 |
| **Notes** | Interpretation thresholds: \|delta\|<2 equivalent, 2-4 weak evidence, 4-7 moderate evidence, >7 strong evidence. Negative delta = model2 better. 27/27 tests GREEN. |

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

## Module: tools.analysis_regression

### fit_multiple_regression

| Field | Value |
|-------|-------|
| **Description** | Fit multiple linear regression with comprehensive diagnostics including VIF, R², adjusted R², F-statistic |
| **Inputs** | `X: Union[np.ndarray, pd.DataFrame]` (predictor variables), `y: Union[np.ndarray, pd.Series]` (response variable), `add_constant: bool = True` (add intercept term), `return_diagnostics: bool = True` (compute VIF and other diagnostics) |
| **Outputs** | `Dict` with keys: model (fitted OLS results), coefficients (DataFrame), r2, adj_r2, f_statistic, p_value, aic, bic, diagnostics (optional Dict with VIF, condition_number, breusch_pagan, durbin_watson) |

### fit_hierarchical_regression

| Field | Value |
|-------|-------|
| **Description** | Fit hierarchical regression with block-wise variable entry and incremental R² calculation |
| **Inputs** | `X_blocks: List[Union[np.ndarray, pd.DataFrame]]` (predictor blocks in order), `y: Union[np.ndarray, pd.Series]` (response), `block_names: List[str] = None` (names for each block), `add_constant: bool = True` |
| **Outputs** | `Dict` with keys: models (list of fitted models per block), incremental_r2 (change in R² per block), summary (DataFrame with cumulative R², ΔR², F-change, p-value per block) |

### compute_regression_diagnostics

| Field | Value |
|-------|-------|
| **Description** | Compute comprehensive regression diagnostics including VIF, Cook's D, leverage, studentized residuals |
| **Inputs** | `model: sm.regression.linear_model.RegressionResultsWrapper` (fitted model), `X: Union[np.ndarray, pd.DataFrame]` (predictors), `return_dataframe: bool = True` (return as DataFrame) |
| **Outputs** | `Dict` with keys: vif (variance inflation factors), cooks_d (Cook's distance per observation), leverage (hat matrix diagonal), studentized_residuals, condition_number, breusch_pagan (heteroscedasticity test), durbin_watson (autocorrelation) |

### cross_validate_regression

| Field | Value |
|-------|-------|
| **Description** | Perform k-fold cross-validation for regression with reproducible splits |
| **Inputs** | `X: Union[np.ndarray, pd.DataFrame]` (predictors), `y: Union[np.ndarray, pd.Series]` (response), `n_folds: int = 5` (number of folds), `random_state: int = 42` (seed for reproducibility), `scoring_metrics: List[str] = ['mse', 'r2']` |
| **Outputs** | `Dict` with keys: scores (per-fold metrics), mean_scores (averaged across folds), std_scores (standard deviation), predictions (out-of-fold predictions) |

### bootstrap_regression_ci

| Field | Value |
|-------|-------|
| **Description** | Compute bootstrap confidence intervals for regression coefficients |
| **Inputs** | `X: Union[np.ndarray, pd.DataFrame]` (predictors), `y: Union[np.ndarray, pd.Series]` (response), `n_bootstrap: int = 1000` (bootstrap iterations), `confidence_level: float = 0.95`, `random_state: int = 42` |
| **Outputs** | `pd.DataFrame` with columns: coefficient, mean, std, ci_lower, ci_upper (one row per predictor) |

### compute_cohens_f2

| Field | Value |
|-------|-------|
| **Description** | Compute Cohen's f² effect size for comparing nested regression models |
| **Inputs** | `r2_full: float` (R² of full model), `r2_reduced: float` (R² of reduced model) |
| **Outputs** | `float` (Cohen's f² value, interpretation: 0.02=small, 0.15=medium, 0.35=large) |

### compute_post_hoc_power

| Field | Value |
|-------|-------|
| **Description** | Compute post-hoc power analysis for regression using non-central F distribution |
| **Inputs** | `n: int` (sample size), `k: int` (number of predictors), `r2: float` (observed R²), `alpha: float = 0.05` (significance level) |
| **Outputs** | `Dict` with keys: power (statistical power), f2 (Cohen's f²), non_centrality (parameter), critical_f |

### variance_decomposition

| Field | Value |
|-------|-------|
| **Description** | Decompose total variance into components attributable to each predictor |
| **Inputs** | `X: Union[np.ndarray, pd.DataFrame]` (predictors), `y: Union[np.ndarray, pd.Series]` (response), `method: str = 'commonality'` (decomposition method) |
| **Outputs** | `pd.DataFrame` with columns: predictor, unique_variance, shared_variance, total_variance |

---

## Module: tools.data

### load_participant_data

| Field | Value |
|-------|-------|
| **Description** | Load participant-level data from dfnonvr.csv (single timepoint variables) |
| **Inputs** | `path: str = './data/dfnonvr.csv'` (file path) |
| **Outputs** | `pd.DataFrame` with 100 rows (participants) × ~100 columns (demographics, cognitive tests, etc.) |

### load_test_data

| Field | Value |
|-------|-------|
| **Description** | Load test-level data from dfdata.csv (per-test variables) |
| **Inputs** | `path: str = './data/dfdata.csv'` (file path) |
| **Outputs** | `pd.DataFrame` with 400 rows (4 tests × 100 participants) × ~377 columns |

### extract_cognitive_tests

| Field | Value |
|-------|-------|
| **Description** | Extract cognitive test scores (RAVLT, BVMT, NART, RPM) with derived metrics |
| **Inputs** | `df: pd.DataFrame` (participant data), `tests: List[str] = None` (subset of tests to extract) |
| **Outputs** | `pd.DataFrame` with columns: UID, RAVLT_T1-T5, RAVLT_total, RAVLT_learning, RAVLT_delayed, RAVLT_forgetting, BVMT_T1-T3, BVMT_total, BVMT_delayed, NART, RPM |

### standardize_to_t_scores

| Field | Value |
|-------|-------|
| **Description** | Convert raw cognitive scores to T-scores (M=50, SD=10) |
| **Inputs** | `scores: Union[pd.Series, pd.DataFrame]` (raw scores), `population_mean: float = None`, `population_sd: float = None` |
| **Outputs** | `Union[pd.Series, pd.DataFrame]` (T-scores with same shape as input) |

### extract_domain_theta_scores

| Field | Value |
|-------|-------|
| **Description** | Load theta scores from Ch5 IRT calibration results |
| **Inputs** | `path: str = None` (path to theta scores CSV), `domains: List[str] = ['What', 'Where', 'When']` |
| **Outputs** | `pd.DataFrame` with columns: composite_ID, UID, test, domain_name, theta |

### merge_theta_cognitive

| Field | Value |
|-------|-------|
| **Description** | Merge theta scores with cognitive test data by UID |
| **Inputs** | `theta_df: pd.DataFrame` (theta scores), `cognitive_df: pd.DataFrame` (cognitive tests) |
| **Outputs** | `pd.DataFrame` (merged data with both theta and cognitive measures) |

### extract_dass_scores

| Field | Value |
|-------|-------|
| **Description** | Extract DASS anxiety and stress subscale scores (depression not available) |
| **Inputs** | `df: pd.DataFrame` (participant data), `subscales: List[str] = ['anxiety', 'stress']` |
| **Outputs** | `pd.DataFrame` with columns: UID, DASS_anxiety, DASS_stress |

### extract_sleep_per_test

| Field | Value |
|-------|-------|
| **Description** | Extract per-test sleep data (hours slept before each test) |
| **Inputs** | `df: pd.DataFrame` (test-level data) |
| **Outputs** | `pd.DataFrame` with columns: composite_ID, UID, test, sleep_hours |

### extract_discrepancy_scores

| Field | Value |
|-------|-------|
| **Description** | Compute VR-traditional memory test discrepancy scores |
| **Inputs** | `vr_scores: pd.DataFrame` (VR theta scores), `traditional_scores: pd.DataFrame` (RAVLT/BVMT scores) |
| **Outputs** | `pd.DataFrame` with columns: UID, test, vr_score, traditional_score, discrepancy, z_discrepancy |

### prepare_regression_data

| Field | Value |
|-------|-------|
| **Description** | Prepare complete dataset for regression analysis with all predictors and outcomes |
| **Inputs** | `participant_path: str = None`, `test_path: str = None`, `theta_path: str = None`, `include_interactions: bool = False` |
| **Outputs** | `pd.DataFrame` (analysis-ready dataset with merged participant, test, and theta data) |

---

## Module: tools.analysis_lpa

### fit_lpa_models

| Field | Value |
|-------|-------|
| **Description** | Fit multiple Gaussian Mixture Models for Latent Profile Analysis |
| **Inputs** | `data: Union[np.ndarray, pd.DataFrame]` (input features), `n_components_range: Union[List[int], range] = range(2, 6)` (number of profiles to test), `covariance_type: str = 'full'` (full/tied/diag/spherical), `n_init: int = 10` (random initializations), `random_state: int = 42` |
| **Outputs** | `Dict[int, GaussianMixture]` (mapping n_components -> fitted model) |

### extract_profile_membership

| Field | Value |
|-------|-------|
| **Description** | Extract profile assignments and posterior probabilities from fitted LPA model |
| **Inputs** | `model: GaussianMixture` (fitted model), `data: Union[np.ndarray, pd.DataFrame]` (input data), `uid_column: str = None` (participant ID column if DataFrame) |
| **Outputs** | `pd.DataFrame` with columns: UID (optional), profile, probability_0, probability_1, ..., entropy |

### compare_lpa_models

| Field | Value |
|-------|-------|
| **Description** | Compare LPA models using BIC, AIC, and entropy for model selection |
| **Inputs** | `models: Dict[int, GaussianMixture]` (fitted models), `data: Union[np.ndarray, pd.DataFrame]` (input data) |
| **Outputs** | `pd.DataFrame` with columns: n_components, BIC, AIC, log_likelihood, entropy, n_parameters (sorted by BIC) |

### characterize_profiles

| Field | Value |
|-------|-------|
| **Description** | Compute profile means, standard deviations, and sizes for interpretation |
| **Inputs** | `model: GaussianMixture` (fitted model), `data: pd.DataFrame` (input data with variable names), `profile_labels: pd.Series` (profile assignments) |
| **Outputs** | `Dict` with keys: means (DataFrame), stds (DataFrame), sizes (Series), proportions (Series) |

### validate_lpa_solution

| Field | Value |
|-------|-------|
| **Description** | Validate LPA solution using internal validity metrics (silhouette, Davies-Bouldin) |
| **Inputs** | `data: Union[np.ndarray, pd.DataFrame]` (input data), `labels: Union[np.ndarray, pd.Series]` (profile assignments), `metric: str = 'euclidean'` |
| **Outputs** | `Dict` with keys: silhouette_score, davies_bouldin_score, silhouette_by_profile (mean per profile) |

### plot_profile_means

| Field | Value |
|-------|-------|
| **Description** | Create visualization of profile characteristics across variables |
| **Inputs** | `profile_means: pd.DataFrame` (means per profile), `profile_sizes: pd.Series` (n per profile), `variable_names: List[str] = None`, `output_path: str = None` |
| **Outputs** | `Tuple[Figure, Axes]` (matplotlib figure and axes objects) |

### perform_external_validation

| Field | Value |
|-------|-------|
| **Description** | Validate profiles against external criteria using ANOVA or chi-square tests |
| **Inputs** | `profile_labels: pd.Series` (profile assignments), `external_variables: pd.DataFrame` (validation variables), `test_type: str = 'auto'` (auto/anova/chi2) |
| **Outputs** | `pd.DataFrame` with columns: variable, test_statistic, p_value, effect_size, significant |

---

## Module: tools.analysis_stats

### one_way_anova_d068

| Field | Value |
|-------|-------|
| **Description** | One-way ANOVA with Decision D068 dual p-value reporting (uncorrected + Bonferroni/Holm) |
| **Inputs** | `data: pd.DataFrame` (long format), `group_col: str` (grouping variable), `value_col: str` (dependent variable), `correction_method: str = 'bonferroni'` (bonferroni/holm), `n_comparisons: int = None` (for correction), `post_hoc: bool = True` (run Tukey HSD) |
| **Outputs** | `Dict` with keys: f_statistic, p_uncorrected, p_corrected, df_between, df_within, eta_squared, post_hoc_results (if requested) |

### chi_square_test_d068

| Field | Value |
|-------|-------|
| **Description** | Chi-square test with Decision D068 dual p-value reporting and optional Yates correction |
| **Inputs** | `contingency_table: Union[pd.DataFrame, np.ndarray]` (observed frequencies), `correction: bool = False` (Yates continuity correction), `n_comparisons: int = None` (for Bonferroni) |
| **Outputs** | `Dict` with keys: chi2_statistic, p_uncorrected, p_corrected, df, expected_frequencies, cramers_v |

### compute_cramers_v

| Field | Value |
|-------|-------|
| **Description** | Compute Cramér's V effect size for contingency tables |
| **Inputs** | `chi2: float` (chi-square statistic), `n: int` (total sample size), `k: int` (minimum of rows-1 or cols-1) |
| **Outputs** | `float` (Cramér's V, interpretation: 0.1=small, 0.3=medium, 0.5=large) |

---

## Module: tools.bootstrap

### bootstrap_correlation_ci

| Field | Value |
|-------|-------|
| **Description** | Bootstrap confidence intervals for Pearson or Spearman correlations |
| **Inputs** | `x: Union[np.ndarray, pd.Series]` (first variable), `y: Union[np.ndarray, pd.Series]` (second variable), `n_bootstrap: int = 1000`, `confidence_level: float = 0.95`, `method: str = 'pearson'` (pearson/spearman), `random_state: int = None` |
| **Outputs** | `Dict` with keys: correlation, ci_lower, ci_upper, bootstrap_distribution |

### bootstrap_mean_ci

| Field | Value |
|-------|-------|
| **Description** | Bootstrap confidence intervals for mean with percentile or BCa method |
| **Inputs** | `data: Union[np.ndarray, pd.Series]` (input data), `n_bootstrap: int = 1000`, `confidence_level: float = 0.95`, `method: str = 'percentile'` (percentile/bca), `paired: bool = False` (for paired samples), `random_state: int = None` |
| **Outputs** | `Dict` with keys: mean, ci_lower, ci_upper, se_bootstrap, bootstrap_distribution |

### bootstrap_median_ci

| Field | Value |
|-------|-------|
| **Description** | Bootstrap confidence intervals for median (robust to outliers) |
| **Inputs** | `data: Union[np.ndarray, pd.Series]` (input data), `n_bootstrap: int = 1000`, `confidence_level: float = 0.95`, `random_state: int = None` |
| **Outputs** | `Dict` with keys: median, ci_lower, ci_upper, bootstrap_distribution |

### bootstrap_statistic

| Field | Value |
|-------|-------|
| **Description** | General bootstrap for any custom statistic function |
| **Inputs** | `data: Union[np.ndarray, pd.DataFrame]` (input data), `statistic_func: Callable` (function to compute statistic), `n_bootstrap: int = 1000`, `confidence_level: float = 0.95`, `method: str = 'percentile'`, `random_state: int = None` |
| **Outputs** | `Dict` with keys: statistic, ci_lower, ci_upper, bootstrap_distribution |

---

## Module: tools.clinical

### compute_sensitivity_specificity

| Field | Value |
|-------|-------|
| **Description** | Compute full diagnostic metrics including sensitivity, specificity, PPV, NPV, accuracy |
| **Inputs** | `y_true: Union[np.ndarray, pd.Series]` (true labels 0/1), `y_pred: Union[np.ndarray, pd.Series]` (predictions 0/1 or probabilities), `threshold: float = 0.5` (for probability predictions) |
| **Outputs** | `Dict` with keys: sensitivity, specificity, ppv, npv, accuracy, balanced_accuracy, f1_score, confusion_matrix |

### compute_roc_auc

| Field | Value |
|-------|-------|
| **Description** | Compute ROC curve and AUC with bootstrap confidence intervals |
| **Inputs** | `y_true: Union[np.ndarray, pd.Series]` (true labels), `y_scores: Union[np.ndarray, pd.Series]` (probability scores), `n_bootstrap: int = 1000` (for CI), `confidence_level: float = 0.95` |
| **Outputs** | `Dict` with keys: auc, ci_lower, ci_upper, fpr (false positive rates), tpr (true positive rates), thresholds |

### compute_diagnostic_odds_ratio

| Field | Value |
|-------|-------|
| **Description** | Compute diagnostic odds ratio (DOR) with Haldane correction for zero cells |
| **Inputs** | `tp: int` (true positives), `tn: int` (true negatives), `fp: int` (false positives), `fn: int` (false negatives), `correction: float = 0.5` (Haldane correction) |
| **Outputs** | `Dict` with keys: dor, log_dor, se_log_dor, ci_lower, ci_upper |

### compute_youden_index

| Field | Value |
|-------|-------|
| **Description** | Compute Youden's J statistic for optimal threshold selection |
| **Inputs** | `y_true: Union[np.ndarray, pd.Series]` (true labels), `y_scores: Union[np.ndarray, pd.Series]` (probability scores) |
| **Outputs** | `Dict` with keys: optimal_threshold, youden_j, sensitivity_at_optimal, specificity_at_optimal |

### compute_likelihood_ratios

| Field | Value |
|-------|-------|
| **Description** | Compute positive and negative likelihood ratios with clinical interpretation |
| **Inputs** | `sensitivity: float` (test sensitivity), `specificity: float` (test specificity) |
| **Outputs** | `Dict` with keys: lr_positive, lr_negative, lr_positive_interpretation, lr_negative_interpretation |

---

## Module: tools.analysis_extensions

### extract_random_effects

| Field | Value |
|-------|-------|
| **Description** | Extract random effects (BLUPs) from fitted LMM - wrapper for existing functionality |
| **Inputs** | `model: MixedLMResults` (fitted LMM) |
| **Outputs** | `pd.DataFrame` with columns: UID, random_intercept, random_slope (if applicable) |

### fit_interaction_model

| Field | Value |
|-------|-------|
| **Description** | Fit LMM with interaction terms - thin wrapper for statsmodels MixedLM |
| **Inputs** | `formula: str` (model formula with interactions), `data: pd.DataFrame` (input data), `groups: str` (grouping variable) |
| **Outputs** | `MixedLMResults` (fitted model object) |

### compute_cohens_q_effect_size

| Field | Value |
|-------|-------|
| **Description** | Cohen's q effect size for comparing two correlations |
| **Inputs** | `r1: float` (first correlation), `r2: float` (second correlation) |
| **Outputs** | `float` (Cohen's q, interpretation: 0.1=small, 0.3=medium, 0.5=large) |

### compare_correlations_dependent

| Field | Value |
|-------|-------|
| **Description** | Steiger's Z-test for comparing dependent correlations sharing one variable |
| **Inputs** | `r12: float` (correlation between vars 1-2), `r13: float` (correlation between vars 1-3), `r23: float` (correlation between vars 2-3), `n: int` (sample size) |
| **Outputs** | `Dict` with keys: z_statistic, p_value, significant (at α=0.05), interpretation |

### compute_discrepancy_scores

| Field | Value |
|-------|-------|
| **Description** | Calculate standardized discrepancy scores between VR and traditional assessments |
| **Inputs** | `vr_scores: pd.Series` (VR test scores), `traditional_scores: pd.Series` (traditional test scores), `standardize: bool = True` (z-score standardization) |
| **Outputs** | `pd.DataFrame` with columns: vr_score, traditional_score, discrepancy, z_discrepancy (if standardized) |

### validate_regression_assumptions

| Field | Value |
|-------|-------|
| **Description** | Comprehensive validation of regression assumptions with diagnostic tests |
| **Inputs** | `model: RegressionResultsWrapper` (fitted regression), `X: pd.DataFrame` (predictors), `return_plots: bool = False` |
| **Outputs** | `Dict` with keys: normality (Shapiro-Wilk test), homoscedasticity (Breusch-Pagan test), multicollinearity (VIF values), autocorrelation (Durbin-Watson), outliers (Cook's D > 4/n), all_assumptions_met (bool) |

### standardize_scores

| Field | Value |
|-------|-------|
| **Description** | Z-score standardization with optional reference population parameters |
| **Inputs** | `scores: Union[pd.Series, pd.DataFrame]` (raw scores), `reference_mean: float = None` (population mean), `reference_sd: float = None` (population SD) |
| **Outputs** | `Union[pd.Series, pd.DataFrame]` (standardized scores, same shape as input) |

### cross_validate_lmm

| Field | Value |
|-------|-------|
| **Description** | K-fold cross-validation for Linear Mixed Models with subject-wise splitting |
| **Inputs** | `formula: str` (model formula), `data: pd.DataFrame` (input data), `groups: str` (subject grouping variable), `n_folds: int = 5`, `random_state: int = 42` |
| **Outputs** | `Dict` with keys: mae_scores (per fold), rmse_scores, r2_scores, mean_mae, mean_rmse, mean_r2, predictions (out-of-fold) |

---

## Module: tools.analysis_ctt

### compute_ctt_mean_scores_by_factor

| Field | Value |
|-------|-------|
| **Description** | Compute CTT mean scores (proportion correct) per UID × test × factor for IRT-CTT convergence analyses |
| **Inputs** | `df_wide: DataFrame` (wide format with item columns), `item_factor_df: DataFrame` (item-to-factor mapping), `factor_col: str = 'factor'`, `item_col: str = 'item_name'`, `include_factors: List[str] = None` |
| **Outputs** | `DataFrame` with columns: composite_ID, UID, test, factor, CTT_score, n_items |

### compute_pearson_correlations_with_correction

| Field | Value |
|-------|-------|
| **Description** | Compute Pearson correlations with Holm-Bonferroni correction (Decision D068 compliance) |
| **Inputs** | `df: DataFrame` (with score columns), `irt_col: str = 'IRT_score'`, `ctt_col: str = 'CTT_score'`, `factor_col: str = 'factor'`, `thresholds: List[float] = [0.70, 0.90]` |
| **Outputs** | `DataFrame` with columns: factor, r, CI_lower, CI_upper, p_uncorrected, p_holm, n, threshold_met |

### compute_cohens_kappa_agreement

| Field | Value |
|-------|-------|
| **Description** | Compute Cohen's kappa for agreement between two significance classifications |
| **Inputs** | `classifications_1: List[bool]` (first model results), `classifications_2: List[bool]` (second model results), `labels: List[str] = None` |
| **Outputs** | `Dict` with keys: kappa, agreement_percent, interpretation, n_effects, substantial_agreement, confusion_matrix |

### compare_lmm_fit_aic_bic

| Field | Value |
|-------|-------|
| **Description** | Compare model fit between two LMMs using AIC and BIC differences |
| **Inputs** | `aic_model1: float`, `bic_model1: float`, `aic_model2: float`, `bic_model2: float`, `model1_name: str = 'Model1'`, `model2_name: str = 'Model2'` |
| **Outputs** | `DataFrame` with columns: metric, model1_value, model2_value, delta, interpretation |

---
## Module: tools.analysis_stats (Additional Functions)

### apply_correction

| Field | Value |
|-------|-------|
| **Description** | Apply multiple comparison correction to p-value (Bonferroni, Holm, FDR) |
| **Inputs** | `p_value: float` (uncorrected p-value), `method: str = 'bonferroni'` (correction method), `n_comparisons: int` (number of comparisons) |
| **Outputs** | `float` (corrected p-value) |

### calculate_omega_squared

| Field | Value |
|-------|-------|
| **Description** | Calculate omega-squared effect size for ANOVA |
| **Inputs** | `F: float` (F-statistic), `df_between: int` (between groups df), `df_within: int` (within groups df), `n: int` (total sample size) |
| **Outputs** | `float` (omega-squared value, interpretation: 0.01=small, 0.06=medium, 0.14=large) |

### compute_effect_sizes

| Field | Value |
|-------|-------|
| **Description** | Compute various effect sizes (Cohen's d, Hedges' g, Glass's delta) for group comparisons |
| **Inputs** | `group1: np.ndarray` (first group data), `group2: np.ndarray` (second group data), `test_type: str = 'independent'` (independent/paired) |
| **Outputs** | `Dict` with keys: cohens_d, hedges_g, glass_delta, interpretation |

### friedman_test_d068

| Field | Value |
|-------|-------|
| **Description** | Friedman test for repeated measures with D068 dual p-value reporting |
| **Inputs** | `measurements: np.ndarray` (n_subjects × n_conditions), `correction: str = 'bonferroni'`, `n_comparisons: int = None` |
| **Outputs** | `Dict` with keys: chi2_statistic, p_uncorrected, p_corrected, df, kendall_w |

### kruskal_wallis_d068

| Field | Value |
|-------|-------|
| **Description** | Kruskal-Wallis H test with D068 dual p-value reporting |
| **Inputs** | `*groups: np.ndarray` (variable number of group arrays), `correction: str = 'bonferroni'`, `n_comparisons: int = None` |
| **Outputs** | `Dict` with keys: H_statistic, p_uncorrected, p_corrected, df, eta_squared |

### mann_whitney_d068

| Field | Value |
|-------|-------|
| **Description** | Mann-Whitney U test with D068 dual p-value reporting |
| **Inputs** | `group1: np.ndarray` (first group), `group2: np.ndarray` (second group), `correction: str = 'bonferroni'`, `n_comparisons: int = None` |
| **Outputs** | `Dict` with keys: U_statistic, p_uncorrected, p_corrected, effect_size_r |

### t_test_d068

| Field | Value |
|-------|-------|
| **Description** | T-test with D068 dual p-value reporting (independent or paired) |
| **Inputs** | `group1: np.ndarray` (first group), `group2: np.ndarray` (second group), `paired: bool = False`, `correction: str = 'bonferroni'`, `n_comparisons: int = None` |
| **Outputs** | `Dict` with keys: t_statistic, p_uncorrected, p_corrected, df, cohens_d, mean_diff, ci_lower, ci_upper |

---

## Module: tools.analysis_lmm (Additional Functions)

### fit_lmm_trajectory

| Field | Value |
|-------|-------|
| **Description** | Fit Linear Mixed Model for trajectory analysis with flexible time specification |
| **Inputs** | `data: pd.DataFrame` (long format), `formula: str` (model formula), `groups: str = 'composite_ID'`, `method: str = 'REML'` |
| **Outputs** | `MixedLM` fitted model object |

### compute_days_within

| Field | Value |
|-------|-------|
| **Description** | Compute days within segment for piecewise LMM analysis |
| **Inputs** | `df: pd.DataFrame` (with Segment and Day columns), `segment_col: str = 'Segment'`, `day_col: str = 'Day'` |
| **Outputs** | `pd.Series` (days within segment, reset at segment boundaries) |

### find_coef_name

| Field | Value |
|-------|-------|
| **Description** | Find coefficient name in model that matches pattern (case-insensitive) |
| **Inputs** | `model: MixedLM` (fitted model), `pattern: str` (search pattern) |
| **Outputs** | `str` (matching coefficient name or None) |

---

## Module: tools.model_averaging

### compute_model_averaged_predictions

| Field | Value |
|-------|-------|
| **Description** | Compute model-averaged predictions using Akaike weights |
| **Inputs** | `models: List[MixedLM]` (fitted models), `data: pd.DataFrame` (prediction data), `aic_values: List[float]` (model AICs) |
| **Outputs** | `np.ndarray` (weighted average predictions) |

### compute_model_averaged_random_effects

| Field | Value |
|-------|-------|
| **Description** | Average random effects across models using Akaike weights |
| **Inputs** | `models: List[MixedLM]` (fitted models), `weights: np.ndarray` (Akaike weights) |
| **Outputs** | `pd.DataFrame` (averaged random effects per participant) |

### compute_unconditional_variance

| Field | Value |
|-------|-------|
| **Description** | Compute unconditional variance of model parameters accounting for model uncertainty |
| **Inputs** | `estimates: List[float]` (parameter estimates), `variances: List[float]` (parameter variances), `weights: np.ndarray` (Akaike weights) |
| **Outputs** | `float` (unconditional variance) |

### identify_competitive_models

| Field | Value |
|-------|-------|
| **Description** | Identify models within delta AIC threshold as competitive |
| **Inputs** | `aic_values: List[float]` (model AICs), `delta_threshold: float = 2.0`, `max_models: int = 10` |
| **Outputs** | `List[int]` (indices of competitive models) |

### run_model_averaging_pipeline

| Field | Value |
|-------|-------|
| **Description** | Complete model averaging pipeline from model selection to averaged results |
| **Inputs** | `data: pd.DataFrame` (input data), `formulas: List[str]` (model formulas), `groups: str = 'composite_ID'`, `delta_aic: float = 2.0` |
| **Outputs** | `Dict` with keys: averaged_predictions, averaged_variance, model_weights, selected_models |

---

## Module: tools.model_selection

### build_formula

| Field | Value |
|-------|-------|
| **Description** | Build model formula string from components |
| **Inputs** | `outcome: str` (dependent variable), `predictors: List[str]` (independent variables), `random: str = None` (random effects) |
| **Outputs** | `str` (complete model formula) |

### log

| Field | Value |
|-------|-------|
| **Description** | Logarithm transformation for model selection (natural log) |
| **Inputs** | `x: Union[float, np.ndarray]` (input value(s)) |
| **Outputs** | `Union[float, np.ndarray]` (log-transformed value(s)) |

---

## Module: tools.sem_calibration

### compute_difference_score_reliability

| Field | Value |
|-------|-------|
| **Description** | Compute reliability of difference scores for confidence-accuracy calibration |
| **Inputs** | `reliability_x: float` (confidence reliability), `reliability_y: float` (accuracy reliability), `correlation: float` (confidence-accuracy correlation) |
| **Outputs** | `float` (difference score reliability) |

### quick_sem_calibration

| Field | Value |
|-------|-------|
| **Description** | Quick structural equation model for calibration analysis |
| **Inputs** | `confidence: np.ndarray` (confidence ratings), `accuracy: np.ndarray` (accuracy scores), `method: str = 'ml'` (estimation method) |
| **Outputs** | `Dict` with keys: calibration_coefficient, standard_error, p_value, model_fit |

### fit_latent_difference

| Field | Value |
|-------|-------|
| **Description** | Fit latent difference score model for calibration |
| **Inputs** | `data: pd.DataFrame` (with confidence and accuracy), `indicators_conf: List[str]`, `indicators_acc: List[str]` |
| **Outputs** | `SEMResults` object with latent calibration estimates |

### fit_residualized

| Field | Value |
|-------|-------|
| **Description** | Fit residualized calibration model (confidence regressed on accuracy) |
| **Inputs** | `confidence: np.ndarray`, `accuracy: np.ndarray` |
| **Outputs** | `Dict` with keys: residual_variance, r_squared, calibration_index |

### get_latent_calibration

| Field | Value |
|-------|-------|
| **Description** | Extract latent calibration scores from SEM model |
| **Inputs** | `model: SEMResults` (fitted SEM), `data: pd.DataFrame` (input data) |
| **Outputs** | `np.ndarray` (latent calibration factor scores) |

### get_model_fit

| Field | Value |
|-------|-------|
| **Description** | Extract model fit indices from SEM results |
| **Inputs** | `model: SEMResults` (fitted model) |
| **Outputs** | `Dict` with keys: chi2, df, p_value, CFI, TLI, RMSEA, SRMR |

### compare_approaches

| Field | Value |
|-------|-------|
| **Description** | Compare different calibration measurement approaches |
| **Inputs** | `data: pd.DataFrame` (calibration data), `approaches: List[str] = ['difference', 'residual', 'latent']` |
| **Outputs** | `pd.DataFrame` (comparison of reliability, validity, and model fit across approaches) |

### save_results

| Field | Value |
|-------|-------|
| **Description** | Save SEM calibration results to file |
| **Inputs** | `results: Dict` (analysis results), `filepath: str` (output path) |
| **Outputs** | `None` (writes to file) |

---

## Module: tools.plotting

### plot_comparison_bars

| Field | Value |
|-------|-------|
| **Description** | Create bar plot comparing groups or conditions |
| **Inputs** | `data: pd.DataFrame` (plot data), `x: str` (x-axis variable), `y: str` (y-axis variable), `hue: str = None` (grouping variable) |
| **Outputs** | `matplotlib.figure.Figure` object |

### plot_panel

| Field | Value |
|-------|-------|
| **Description** | Create multi-panel plot grid for complex visualizations |
| **Inputs** | `data: pd.DataFrame`, `panels: List[Dict]` (panel specifications), `ncols: int = 2` |
| **Outputs** | `matplotlib.figure.Figure` object |

### plot_piecewise_trajectory

| Field | Value |
|-------|-------|
| **Description** | Plot piecewise linear trajectories with segment boundaries |
| **Inputs** | `data: pd.DataFrame` (trajectory data), `x: str` (time variable), `y: str` (outcome), `segment: str` (segment indicator) |
| **Outputs** | `matplotlib.figure.Figure` object |

---

## Module: tools.validation (Additional Functions)

### generate_validation_report

| Field | Value |
|-------|-------|
| **Description** | Generate comprehensive validation report for analysis results |
| **Inputs** | `results: Dict` (analysis results), `checks: List[str]` (validation checks to perform) |
| **Outputs** | `Dict` with keys: passed_checks, failed_checks, warnings, report_text |

### run_lmm_sensitivity_analyses

| Field | Value |
|-------|-------|
| **Description** | Run sensitivity analyses for LMM assumptions and specifications |
| **Inputs** | `model: MixedLM` (fitted model), `data: pd.DataFrame` (input data), `analyses: List[str] = ['outliers', 'normality', 'heteroscedasticity']` |
| **Outputs** | `Dict` with sensitivity analysis results per check |

### save_validation_report

| Field | Value |
|-------|-------|
| **Description** | Save validation report to file with timestamp |
| **Inputs** | `report: Dict` (validation report), `filepath: str` (output path) |
| **Outputs** | `None` (writes to file) |

### validate_contrasts

| Field | Value |
|-------|-------|
| **Description** | Validate contrast specifications and results |
| **Inputs** | `contrasts: pd.DataFrame` (contrast results), `expected_comparisons: List[str]` |
| **Outputs** | `Dict` with keys: all_present, missing_comparisons, valid_statistics |

### validate_hypothesis_tests

| Field | Value |
|-------|-------|
| **Description** | Validate hypothesis test results meet requirements |
| **Inputs** | `tests: pd.DataFrame` (test results), `alpha: float = 0.05`, `require_dual_p: bool = True` |
| **Outputs** | `Dict` with keys: valid_tests, invalid_tests, dual_p_compliance |

### validate_lmm_assumptions_comprehensive_v3

| Field | Value |
|-------|-------|
| **Description** | Comprehensive LMM assumption validation (version 3 with enhanced diagnostics) |
| **Inputs** | `model: MixedLM` (fitted model), `data: pd.DataFrame` (input data), `create_plots: bool = True` |
| **Outputs** | `Dict` with assumption test results, plots, and remedial action recommendations |

### validate_probability_transform

| Field | Value |
|-------|-------|
| **Description** | Validate probability transformation preserves ordering and bounds |
| **Inputs** | `original: np.ndarray` (original scale), `transformed: np.ndarray` (probability scale) |
| **Outputs** | `Dict` with keys: ordering_preserved, bounds_valid, correlation |

---

## Module: tools.config

### expand_env_vars_in_path

| Field | Value |
|-------|-------|
| **Description** | Expand environment variables in file paths |
| **Inputs** | `path: str` (path with potential env vars like $HOME) |
| **Outputs** | `str` (expanded path) |

### validate_irt_params

| Field | Value |
|-------|-------|
| **Description** | Validate IRT parameter configuration |
| **Inputs** | `params: Dict` (IRT parameters) |
| **Outputs** | `Dict` with keys: valid, errors, warnings |

### validate_paths_exist

| Field | Value |
|-------|-------|
| **Description** | Validate that required file paths exist |
| **Inputs** | `paths: List[str]` (file paths to check) |
| **Outputs** | `Dict` with keys: all_exist, missing_paths |

---

## Module: tools.variance_decomposition (Additional Functions)

### log

| Field | Value |
|-------|-------|
| **Description** | Natural logarithm transformation (wrapper for variance decomposition) |
| **Inputs** | `x: Union[float, np.ndarray]` (input value(s)) |
| **Outputs** | `Union[float, np.ndarray]` (log-transformed value(s)) |

---
**End of Tools Inventory**
