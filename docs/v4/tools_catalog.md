# Tools Catalog (v4.X)

**Version:** 4.0
**Last Updated:** 2025-11-22
**Purpose:** Lightweight tool discovery for rq_planner (YELLOW/GREEN tools only)
**Format:** One-line descriptions for quick scanning

## IRT Analysis Tools

| Function | Description |
|----------|-------------|
| `prepare_irt_input_from_long` | Convert long DataFrame to IRT tensors (response matrix, missing mask, composite IDs) |
| `configure_irt_model` | Build IWAVE GRM model with Q-matrix and factor structure |
| `fit_irt_grm` | Fit IRT model via variational inference (IWAVE algorithm) |
| `extract_theta_from_irt` | Extract participant ability estimates (theta scores) from fitted model |
| `extract_parameters_from_irt` | Extract item parameters (discrimination a, difficulty b) from fitted model |
| `calibrate_irt` | Full IRT pipeline: prepare -> configure -> fit -> extract (convenience wrapper) |
| `filter_items_by_quality` | D039: Purify items by quality thresholds (a >= 0.4, \|b\| <= 3.0) |
| `calibrate_grm` | Backwards-compatible wrapper for calibrate_irt() |

---

## LMM Analysis Tools

| Function | Description |
|----------|-------------|
| `prepare_lmm_input_from_theta` | DEPRECATED: Convert theta wide -> long format with nominal days (use fit_lmm_trajectory_tsvr) |
| `configure_candidate_models` | Generate 5 candidate LMM formulas (Linear, Quadratic, Log, Lin+Log, Quad+Log) |
| `fit_lmm_trajectory_tsvr` | D070: Fit LMM using TSVR (actual hours) as time variable |
| `compare_lmm_models_by_aic` | Fit all 5 candidate models, compare by AIC, return best |
| `compare_lmm_models_kitchen_sink` | **NEW (2025-12-08)**: Comprehensive model selection testing 70+ time transformations (polynomial, logarithmic, power-law, root, reciprocal, exponential, trigonometric, hyperbolic, hybrids). Supports 0/1/2-way interactions. Requires continuous TSVR. **NOTE:** `re_formula` parameter affects absolute AICs but preserves rankings; use `'~1'` for complex interactions, `'~log_TSVR'` or `'~TSVR'` for simple trajectories. Validated on RQ 5.1.1 (bit-exact match with existing results when using same re_formula). Returns AIC comparison, best model, Log model benchmark, top 10 models. |
| `extract_fixed_effects_from_lmm` | Extract fixed effects table (coefficients, SE, z, p-values) |
| `extract_random_effects_from_lmm` | Extract random effects variance components and ICC |
| `compute_contrasts_pairwise` | D068: Post-hoc pairwise contrasts with dual p-values (uncorrected + Bonferroni) |
| `compute_effect_sizes_cohens` | Compute Cohen's f-squared effect sizes for fixed effects |
| `select_lmm_random_structure_via_lrt` | Compare 3 random structures via LRT (Full, Uncorrelated, Intercept-only), select parsimoniously |
| `prepare_age_effects_plot_data` | Create age tertiles (Young/Middle/Older), aggregate observed means + predictions for Age × Domain × Time plot |
| `compute_icc_from_variance_components` | Compute 3 ICC estimates (intercept, slope_simple, slope_conditional) with interpretation thresholds |
| `test_intercept_slope_correlation_d068` | D068: Pearson correlation between random intercepts/slopes with dual p-values (uncorrected + Bonferroni) |
| `extract_segment_slopes_from_lmm` | Extract Early/Late slopes + ratio from piecewise LMM with delta method SE propagation (RQ 5.8 two-phase test) |
| `extract_marginal_age_slopes_by_domain` | Extract domain-specific marginal age effects from 3-way Age×Domain×Time interaction LMM with delta method SEs (RQ 5.10) |
| `compute_model_averaged_variance_decomposition` | **NEW (2025-12-09)**: Model-averaged variance decomposition for stratified LMMs when functional form uncertainty is high. Integrates with `compare_lmm_models_kitchen_sink` to identify competitive models (ΔAIC < 2), fits stratified LMMs for each level (e.g., Common/Congruent/Incongruent) × model, then Akaike-averages variance components (var_int, var_slope, cov, var_resid), ICCs (intercept, slope_simple, slope_conditional), and random effects (participant-specific intercepts/slopes). Returns both model-specific AND averaged results (transparency). Handles convergence failures gracefully. Use when best model has <30% Akaike weight (Burnham & Anderson, 2002 threshold). **Reusable:** RQ 5.4.6 (congruence), RQ 5.2.6 (domain), RQ 5.3.7 (paradigm), any variance decomposition with model uncertainty. Parametric design: `delta_aic_threshold=2.0`, `min_models=3`, `max_models=10`. |

---

## Plotting Tools

| Function | Description |
|----------|-------------|
| `convert_theta_to_probability` | Transform theta to probability scale via IRT 2PL formula |
| `plot_trajectory` | Trajectory with fitted curves + observed error bars (reusable with consistent styling) |
| `plot_trajectory_probability` | D069: Dual-scale trajectory plotting (theta + probability scales for interpretability) |
| `plot_histogram_by_group` | Grouped histograms with overlapping distributions |
| `set_plot_style_defaults` | Apply consistent matplotlib/seaborn styling from config |
| `plot_diagnostics` | Create 2x2 diagnostic plot grid (residuals vs fitted, Q-Q, scale-location, residuals by group) |
| `save_plot_with_data` | Save plot as PNG and associated data as CSV for reproducibility |
| `prepare_piecewise_plot_data` | Aggregate observed means + model predictions for two-panel piecewise plots |
| `assign_piecewise_segments` | Assign Early/Late segments + compute Days_within for RQ 5.8 piecewise LMM |
| `run_lmm_analysis` | Complete LMM pipeline wrapper (prepare → fit → compare → extract → save) |

---

## Validation Tools

| Function | Description |
|----------|-------------|
| `check_file_exists` | Validate file exists and optionally meets minimum size requirement |
| `create_lineage_metadata` | Create lineage metadata for data transformation (prevents Pass 1/2 mix-ups) |
| `save_lineage_to_file` | Save lineage metadata to JSON file |
| `load_lineage_from_file` | Load lineage metadata from JSON file |
| `validate_lineage` | Validate data provenance (source file and pass number) |
| `check_missing_data` | Check for missing data in DataFrame (total, percent, by column) |
| `validate_data_columns` | Validate required columns exist in DataFrame (case-sensitive) |
| `validate_irt_convergence` | Check IRT model convergence (loss stability, parameter bounds) |
| `validate_irt_parameters` | Validate item quality against thresholds (a >= min, \|b\| <= max) |
| `validate_lmm_convergence` | Check LMM convergence status and warnings |
| `validate_lmm_residuals` | Test residuals normality via Kolmogorov-Smirnov test |
| `validate_lmm_assumptions_comprehensive` | 7 LMM diagnostics (normality, homoscedasticity, Q-Q, ACF, linearity, outliers, convergence) with plots and remedial recommendations |
| `validate_contrasts_d068` | D068: Validate contrast results have dual p-values (uncorrected + bonferroni/tukey/holm) |
| `validate_hypothesis_test_dual_pvalues` | D068: Validate hypothesis tests have required terms AND dual p-values (uncorrected + correction) |
| `validate_contrasts_dual_pvalues` | D068: Validate post-hoc contrasts have required comparisons AND dual p-values (uncorrected + tukey/bonferroni/holm) |
| `validate_correlation_test_d068` | D068: Validate correlation tests have dual p-values (uncorrected + bonferroni/holm/fdr) |
| `validate_numeric_range` | Validate numeric values within range [min, max], detect NaN/inf violations |
| `validate_data_format` | Validate DataFrame has all required columns (case-sensitive) |
| `validate_effect_sizes` | Validate Cohen's f² non-negative, warn if >1.0 (very large) |
| `validate_probability_range` | Validate probabilities in [0,1] across multiple columns, no NaN/inf |
| `validate_model_convergence` | Validate statsmodels LMM converged successfully |
| `validate_standardization` | Validate z-score standardization (mean ≈ 0, SD ≈ 1) with configurable tolerance for sampling variation |
| `validate_variance_positivity` | Validate all LMM variance components > 0 (detects collinearity/convergence issues) |
| `validate_icc_bounds` | Validate ICC values in [0,1] range (detects computation errors) |
| `validate_dataframe_structure` | Generic DataFrame validator (rows exact/range, columns present, types match) |
| `validate_plot_data_completeness` | Verify all domains/groups present in plot data (complete factorial design) |
| `validate_cluster_assignment` | Validate K-means clusters (consecutive IDs 0...K-1, minimum cluster size enforced) |
| `validate_bootstrap_stability` | Validate clustering stability via Jaccard coefficient (mean, 95% CI, threshold check) |
| `validate_cluster_summary_stats` | Validate cluster summaries (min <= mean <= max, SD >= 0, N > 0) |

---

## CTT Analysis Tools

| Function | Description |
|----------|-------------|
| `compute_cronbachs_alpha` | Cronbach's alpha internal consistency with bootstrap 95% CIs (1000+ iterations, KR-20 equivalent for binary) |
| `compare_correlations_dependent` | Steiger's z-test for dependent correlations (tests if r13 differs from r12 when sharing variable 1) |

---

## Config Management Tools

| Function | Description |
|----------|-------------|
| `load_config_from_file` | Load YAML config file with caching (paths, plotting, irt, lmm) |
| `load_config_from_yaml` | Get config value by dot-separated key path (e.g., 'data.master') |
| `resolve_path_from_config` | Get path from paths.yaml, format templates, return absolute Path |
| `load_plot_config_from_yaml` | Shorthand for loading plotting configuration |
| `load_irt_config_from_yaml` | Shorthand for loading IRT configuration |
| `load_lmm_config_from_yaml` | Shorthand for loading LMM configuration |
| `merge_config_dicts` | Deep merge dicts (override takes precedence, non-mutating) |
| `load_rq_config_merged` | Load RQ config with 3-tier merge (global → chapter → RQ) |
| `reset_config_cache` | Clear global config cache (for testing) |

---

## Standard Library Functions (Always Available)

**Note:** The following standard library functions are used directly in analysis scripts and do NOT require tools_inventory.md documentation:

### pandas Operations
```
pd.read_csv, pd.DataFrame.melt, pd.DataFrame.merge, pd.DataFrame.pivot, pd.DataFrame.groupby, pd.DataFrame.to_csv
```

### numpy Operations
```
np.linspace, np.log, np.array, np.mean, np.std, np.median
```

### pathlib Operations
```
Path.mkdir, Path.exists, Path.read_text, Path.write_text
```

**Why stdlib exempt?** These are well-documented in official Python/pandas/numpy docs.

---

## Regression Analysis Tools

| Function | Description |
|----------|-----------|
| `fit_multiple_regression` | Fit multiple linear regression with VIF, R², F-statistic, and comprehensive diagnostics |
| `fit_hierarchical_regression` | Hierarchical regression with block-wise entry and incremental R² calculation |
| `compute_regression_diagnostics` | VIF, Cook's D, leverage, studentized residuals, heteroscedasticity tests |
| `cross_validate_regression` | K-fold cross-validation with reproducible splits and multiple scoring metrics |
| `bootstrap_regression_ci` | Bootstrap confidence intervals for regression coefficients (1000+ iterations) |
| `compute_cohens_f2` | Cohen's f² effect size for nested model comparison (0.02=small, 0.15=medium, 0.35=large) |
| `compute_post_hoc_power` | Post-hoc power analysis using non-central F distribution |
| `variance_decomposition` | Decompose variance into unique and shared components per predictor |

---

## Data Extraction Tools  

| Function | Description |
|----------|-----------|
| `load_participant_data` | Load participant-level data from dfnonvr.csv (100 rows × demographics/cognitive) |
| `load_test_data` | Load test-level data from dfdata.csv (400 rows × per-test variables) |
| `extract_cognitive_tests` | Extract RAVLT, BVMT, NART, RPM scores with derived metrics (totals, learning, forgetting) |
| `standardize_to_t_scores` | Convert raw cognitive scores to T-scores (M=50, SD=10) |
| `extract_domain_theta_scores` | Load theta scores from Ch5 IRT calibration results |
| `merge_theta_cognitive` | Merge theta scores with cognitive test data by UID |
| `extract_dass_scores` | Extract DASS anxiety and stress subscales (depression not available) |
| `extract_sleep_per_test` | Extract per-test sleep hours from test-level data |
| `extract_discrepancy_scores` | Compute VR-traditional test discrepancy scores with z-standardization |
| `prepare_regression_data` | Prepare complete merged dataset for regression analysis |

---

## Latent Profile Analysis Tools

| Function | Description |
|----------|-----------|
| `fit_lpa_models` | Fit Gaussian Mixture Models for LPA with multiple component numbers |
| `extract_profile_membership` | Get profile assignments, probabilities, and entropy from fitted LPA |
| `compare_lpa_models` | Compare models by BIC, AIC, entropy for optimal profile number selection |
| `characterize_profiles` | Compute profile means, SDs, sizes for interpretation |
| `validate_lpa_solution` | Internal validity via silhouette score and Davies-Bouldin index |
| `plot_profile_means` | Visualize profile characteristics across variables |
| `perform_external_validation` | Validate profiles against external criteria (ANOVA/chi-square) |

---

## Statistical Testing Tools (D068 Compliant)

| Function | Description |
|----------|-----------|
| `one_way_anova_d068` | One-way ANOVA with dual p-values (uncorrected + Bonferroni/Holm), Tukey post-hoc |
| `chi_square_test_d068` | Chi-square test with dual p-values, optional Yates correction, Cramér's V |
| `compute_cramers_v` | Cramér's V effect size for contingency tables (0.1=small, 0.3=medium, 0.5=large) |

---

## Bootstrap Tools

| Function | Description |
|----------|-----------|
| `bootstrap_correlation_ci` | Bootstrap CIs for Pearson/Spearman correlations with seed control |
| `bootstrap_mean_ci` | Bootstrap CIs for mean with percentile or BCa method, paired samples support |
| `bootstrap_median_ci` | Robust bootstrap CIs for median (outlier-resistant) |
| `bootstrap_statistic` | General bootstrap for any custom statistic function |

---

## Clinical Metrics Tools

| Function | Description |
|----------|-----------|
| `compute_sensitivity_specificity` | Full diagnostic metrics (sens, spec, PPV, NPV, accuracy, F1) |
| `compute_roc_auc` | ROC curve and AUC with bootstrap confidence intervals |
| `compute_diagnostic_odds_ratio` | DOR with Haldane correction for zero cells |
| `compute_youden_index` | Optimal threshold selection via Youden's J statistic |
| `compute_likelihood_ratios` | LR+ and LR- with clinical interpretation |

---

## Analysis Extensions Tools

| Function | Description |
|----------|-----------|
| `extract_random_effects` | Extract BLUPs from fitted LMM (wrapper for existing functionality) |
| `fit_interaction_model` | Fit LMM with interaction terms (thin wrapper for statsmodels) |
| `compute_cohens_q_effect_size` | Cohen's q for correlation comparison (0.1=small, 0.3=medium, 0.5=large) |
| `compare_correlations_dependent` | Steiger's Z-test for dependent correlations sharing one variable |
| `compute_discrepancy_scores` | VR vs traditional assessment discrepancy with z-standardization |
| `validate_regression_assumptions` | Comprehensive assumption checking (normality, homoscedasticity, VIF, outliers) |
| `standardize_scores` | Z-score standardization with optional reference population parameters |
| `cross_validate_lmm` | K-fold CV for LMMs with subject-wise splitting |

## Additional Analysis Stats Tools

| Function | Description |
|----------|-------------|
| `apply_correction` | Apply multiple comparison correction (Bonferroni/Holm/FDR) to p-value |
| `calculate_omega_squared` | Calculate omega-squared effect size for ANOVA (0.01=small, 0.06=medium, 0.14=large) |
| `compute_effect_sizes` | Compute Cohen's d, Hedges' g, Glass's delta for group comparisons |
| `friedman_test_d068` | D068: Friedman test for repeated measures with dual p-value reporting |
| `kruskal_wallis_d068` | D068: Kruskal-Wallis H test with dual p-value reporting |
| `mann_whitney_d068` | D068: Mann-Whitney U test with dual p-value reporting |
| `t_test_d068` | D068: T-test (independent/paired) with dual p-value reporting |

---

## Additional LMM Tools

| Function | Description |
|----------|-------------|
| `fit_lmm_trajectory` | Fit LMM for trajectory analysis with flexible time specification |
| `compute_days_within` | Compute days within segment for piecewise LMM analysis |
| `find_coef_name` | Find coefficient name in model matching pattern (case-insensitive) |

---

## Model Averaging Tools

| Function | Description |
|----------|-------------|
| `compute_model_averaged_predictions` | Compute Akaike-weighted average predictions across models |
| `compute_model_averaged_random_effects` | Average random effects using Akaike weights |
| `compute_unconditional_variance` | Compute unconditional variance accounting for model uncertainty |
| `identify_competitive_models` | Identify models within delta AIC threshold as competitive |
| `run_model_averaging_pipeline` | Complete pipeline from model selection to averaged results |

---

## Model Selection Tools

| Function | Description |
|----------|-------------|
| `build_formula` | Build model formula string from outcome, predictors, random effects |
| `log` | Natural logarithm transformation for model selection |

---

## SEM Calibration Tools

| Function | Description |
|----------|-------------|
| `compute_difference_score_reliability` | Compute reliability of confidence-accuracy difference scores |
| `quick_sem_calibration` | Quick SEM for calibration analysis with ML estimation |
| `fit_latent_difference` | Fit latent difference score model for calibration |
| `fit_residualized` | Fit residualized calibration model (confidence on accuracy) |
| `get_latent_calibration` | Extract latent calibration factor scores from SEM |
| `get_model_fit` | Extract fit indices (chi2, CFI, TLI, RMSEA, SRMR) from SEM |
| `compare_approaches` | Compare difference/residual/latent calibration approaches |
| `save_results` | Save SEM calibration results to file |

---

## Additional Plotting Tools

| Function | Description |
|----------|-------------|
| `plot_comparison_bars` | Bar plot comparing groups or conditions with optional hue |
| `plot_panel` | Multi-panel plot grid for complex visualizations |
| `plot_piecewise_trajectory` | Plot piecewise linear trajectories with segment boundaries |

---

## Additional Validation Tools

| Function | Description |
|----------|-------------|
| `generate_validation_report` | Generate comprehensive validation report for analysis results |
| `run_lmm_sensitivity_analyses` | Run outlier/normality/heteroscedasticity sensitivity analyses |
| `save_validation_report` | Save timestamped validation report to file |
| `validate_contrasts` | Validate contrast specifications and presence of comparisons |
| `validate_hypothesis_tests` | Validate hypothesis tests meet alpha and dual p requirements |
| `validate_lmm_assumptions_comprehensive_v3` | Enhanced LMM assumption validation with plots and remedies |
| `validate_probability_transform` | Validate probability transformation preserves ordering/bounds |

---

## Config Tools

| Function | Description |
|----------|-------------|
| `expand_env_vars_in_path` | Expand environment variables like $HOME in file paths |
| `validate_irt_params` | Validate IRT parameter configuration for errors/warnings |
| `validate_paths_exist` | Check that required file paths exist before analysis |

---

## Additional Variance Decomposition Tools

| Function | Description |
|----------|-------------|
| `log` | Natural log transformation wrapper for variance decomposition |

---## Additional D068-Compliant Statistical Tools

| Function | Description |
|----------|-------------|
| `chi_square_test_d068` | D068: Chi-square test with dual p-values and optional Yates correction |
| `one_way_anova_d068` | D068: One-way ANOVA with dual p-values and optional Tukey HSD post-hoc |
| `test_intercept_slope_correlation_d068` | D068: Test correlation between random intercepts/slopes with dual p-values |
| `validate_contrasts_d068` | D068: Validate contrast results have dual p-values (uncorrected + corrected) |
| `validate_correlation_test_d068` | D068: Validate correlation tests have dual p-values with corrections |

## Additional CTT Analysis Tools

| Function | Description |
|----------|-------------|
| `compute_ctt_mean_scores_by_factor` | Compute CTT mean scores (proportion correct) per UID × test × factor |
| `compute_pearson_correlations_with_correction` | Pearson correlations with Holm-Bonferroni correction (D068 compliance) |
| `compute_cohens_kappa_agreement` | Cohen's kappa for agreement between two significance classifications |
| `compare_lmm_fit_aic_bic` | Compare model fit between two LMMs using AIC and BIC differences |

## Additional Regression Tools

| Function | Description |
|----------|-------------|
| `compute_cohens_f2` | Compute Cohen's f² effect size for nested regression models (0.02=small, 0.15=medium, 0.35=large) |

---