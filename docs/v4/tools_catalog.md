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
| `extract_fixed_effects_from_lmm` | Extract fixed effects table (coefficients, SE, z, p-values) |
| `extract_random_effects_from_lmm` | Extract random effects variance components and ICC |
| `compute_contrasts_pairwise` | D068: Post-hoc pairwise contrasts with dual p-values (uncorrected + Bonferroni) |
| `compute_effect_sizes_cohens` | Compute Cohen's f-squared effect sizes for fixed effects |
| `select_lmm_random_structure_via_lrt` | Compare 3 random structures via LRT (Full, Uncorrelated, Intercept-only), select parsimoniously |
| `prepare_age_effects_plot_data` | Create age tertiles (Young/Middle/Older), aggregate observed means + predictions for Age × Domain × Time plot |
| `compute_icc_from_variance_components` | Compute 3 ICC estimates (intercept, slope_simple, slope_conditional) with interpretation thresholds |
| `test_intercept_slope_correlation_d068` | D068: Pearson correlation between random intercepts/slopes with dual p-values (uncorrected + Bonferroni) |
| `assign_piecewise_segments` | Assign Early/Late segments and compute Days_within for piecewise LMM |
| `extract_segment_slopes_from_lmm` | Extract segment-factor slopes from piecewise LMM via delta method |

---

## Plotting Tools

| Function | Description |
|----------|-------------|
| `convert_theta_to_probability` | Transform theta to probability scale via IRT 2PL formula |
| `prepare_piecewise_plot_data` | Aggregate observed means + model predictions for two-panel piecewise plots |

---

## Validation Tools

| Function | Description |
|----------|-------------|
| `check_file_exists` | Validate file exists and optionally meets minimum size requirement |
| `validate_irt_convergence` | Check IRT model convergence (loss stability, parameter bounds) |
| `validate_irt_parameters` | Validate item quality against thresholds (a >= min, \|b\| <= max) |
| `validate_lmm_convergence` | Check LMM convergence status and warnings |
| `validate_lmm_residuals` | Test residuals normality via Kolmogorov-Smirnov test |
| `validate_hypothesis_tests` | Validate hypothesis test format and p-value bounds |
| `validate_contrasts` | Validate contrast results format and Decision D068 compliance (dual p-values) |
| `validate_probability_transform` | Validate theta→probability transformation (bounds, monotonicity) |
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
| `run_lmm_sensitivity_analyses` | Compare 7 alternative models (piecewise vs continuous, knots, weighted) |

---

## CTT Analysis Tools

| Function | Description |
|----------|-------------|
| `compute_cronbachs_alpha` | Cronbach's alpha internal consistency with bootstrap 95% CIs (1000+ iterations, KR-20 equivalent for binary) |
| `compare_correlations_dependent` | Steiger's z-test for dependent correlations (tests if r13 differs from r12 when sharing variable 1) |

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

**End of Tools Catalog**
