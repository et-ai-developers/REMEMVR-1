# REMEMVR Tools Catalog (Lightweight)

**Purpose:** Quick reference for tool discovery - "What exists and what does it do?"
**Audience:** rq_planner agent (planning phase), main claude when browsing available tools
**Last Updated:** 2025-11-22
**Size:** ~300 lines (96% lighter than tools_inventory.md)

**For detailed API specs:** See `docs/tools_inventory.md` (full signatures, parameters, examples)

---

## Design Philosophy

**This catalog answers ONE question:** "Which tools exist for which tasks?"

- **One line per function:** Name + purpose + basic I/O
- **No parameter details:** Use tools_inventory.md for full signatures
- **No examples:** Use tools_inventory.md for usage patterns
- **No implementation notes:** Use tools_inventory.md for caveats

---

## Analysis Tools: IRT Calibration

### Pipeline Wrappers (High-Level)

```
calibrate_irt: End-to-end IRT calibration | df_long + groups + config -> theta_scores + item_params
calibrate_grm: Alias for calibrate_irt (backwards compatibility) | df_long + groups + config -> theta_scores + item_params
```

### Atomic Components (Low-Level)

```
prepare_irt_input_from_wide: Convert long-format data to IRT tensors | df_long + groups -> response_matrix + Q_matrix + missing_mask + item_list + composite_ids
configure_irt_model: Build unfitted deepirtools IWAVE GRM model | Q_matrix + n_cats + config -> model
fit_irt_grm: Fit GRM model via variational inference | model + response_matrix + missing_mask -> fitted_model
extract_theta_from_irt: Extract ability estimates (theta scores) | fitted_model + response_matrix + composite_ids + groups -> theta_df
extract_parameters_from_irt: Extract item parameters (discrimination + difficulty) | fitted_model + item_list -> params_df
filter_items_by_quality: 2-pass IRT purification (Decision D039) | item_params + thresholds -> purified_items + excluded_items
```

**Decision D039:** `filter_items_by_quality` implements 2-pass purification (|b| > 3.0 OR a < 0.4)

---

## Analysis Tools: LMM Trajectory Analysis

### Pipeline Wrappers (High-Level)

```
run_lmm_analysis: Complete LMM pipeline (prep + fit 5 models + compare + extract) | theta_scores + output_dir -> best_model + comparison + effects
```

### Atomic Components (Low-Level)

```
prepare_lmm_input_from_theta: Reshape wide to long + add time variables | theta_scores + factors -> df_long (with Days, Days_sq, log_Days)
configure_candidate_models: Generate 5 candidate model formulas | reference_level -> formulas (linear, quadratic, log, linear+log, quadratic+log)
fit_lmm_trajectory: Fit single LMM model via statsmodels | data + formula + groups -> MixedLMResults
fit_lmm_trajectory_tsvr: Fit LMM using TSVR as time variable (Decision D070) | data + candidate_models + output_dir -> best_model + comparison
compare_lmm_models_by_aic: Compare models via AIC with weights | model_results -> comparison_table (AIC, delta_AIC, weights)
extract_fixed_effects_from_lmm: Extract fixed effects table | MixedLMResults -> fixed_effects_df (coef, SE, z, p, CI)
extract_random_effects_from_lmm: Extract random effects variances + ICC | MixedLMResults -> random_effects_dict
compute_contrasts_pairwise: Post-hoc contrasts with dual reporting (Decision D068) | MixedLMResults + contrasts -> contrasts_df (uncorrected + Bonferroni)
compute_effect_sizes_cohens: Compute Cohen's f² for fixed effects | MixedLMResults -> effect_sizes_df
```

**Decision D068:** `compute_contrasts_pairwise` reports BOTH uncorrected (α=0.05) AND Bonferroni-corrected p-values
**Decision D070:** `fit_lmm_trajectory_tsvr` uses TSVR (actual hours since encoding) NOT nominal days (0,1,3,6)

---

## Plotting Tools

### Plot Generation

```
plot_trajectory: Trajectory plot with fitted curves + observed data | time_pred + fitted_curves + observed_data -> fig + ax
plot_trajectory_probability: Plot trajectory with theta->probability transformation (Decision D069) | df_thetas + item_params_path + factors -> fig + ax + prob_data
plot_diagnostics: 2x2 diagnostic grid (residuals vs fitted, QQ, scale-location, leverage) | residuals + fitted_values -> fig + axes
plot_histogram_by_group: Grouped histogram with overlapping distributions | data + value_col + group_col -> fig + ax
```

**Decision D069:** `plot_trajectory_probability` creates dual-scale plots (theta + probability) for interpretability

### Plot Utilities

```
set_plot_style_defaults: Apply consistent matplotlib/seaborn styling | config_path -> None (sets global style)
save_plot_with_data: Save PNG + associated CSV for reproducibility | fig + output_path + data -> None (saves files)
convert_theta_to_probability: IRT response function (theta to probability) | theta + discrimination + difficulty -> probability
```

---

## Validation Tools

### Data Quality

```
check_missing_data: Check for missing data in DataFrame | df -> missing_report (has_missing, percent, by_column)
validate_data_columns: Validate required columns exist | df + required_columns -> validation_report
validate_numeric_range: Check numeric data within expected range | data + min_val + max_val -> validation_report
check_file_exists: Check file exists before loading | file_path -> exists_report
```

### Statistical Validation

```
validate_irt_convergence: Validate IRT model converged properly | results -> convergence_report
validate_irt_parameters: Validate IRT item parameters (psychometric quality) | params_df + thresholds -> validation_report
validate_lmm_convergence: Validate LMM converged without warnings | MixedLMResults -> convergence_report
validate_lmm_residuals: Test residuals for normality + homoscedasticity | residuals + alpha -> validation_report
```

### Lineage Tracking (Provenance)

```
create_lineage_metadata: Create metadata for data transformation | source_file + output_file + operation + params -> metadata_dict
save_lineage_to_file: Save lineage metadata to JSON | metadata + file_path -> None (saves JSON)
load_lineage_from_file: Load lineage metadata from JSON | file_path -> metadata_dict
validate_lineage: Validate data comes from expected source | actual_source + expected_source -> validation_report
```

### Reporting

```
generate_validation_report: Aggregate multiple validation results | validation_checks + report_title -> report_dict
save_validation_report: Save validation report to JSON | report + report_file -> None (saves JSON)
```

---

## Configuration Tools

### Config Loading

```
load_config_from_file: Load YAML config by name | config_name (paths/plotting/irt/lmm) -> config_dict
load_config_from_yaml: Get config value by dot-notation path | config_name + key_path -> value
load_rq_config_merged: Load RQ-specific config with overrides | chapter + rq -> rq_config_dict
```

### Specialized Getters

```
load_irt_config_from_yaml: Shortcut for IRT config | key_path -> value
load_lmm_config_from_yaml: Shortcut for LMM config | key_path -> value
load_plot_config_from_yaml: Shortcut for plotting config | key_path -> value
resolve_path_from_config: Get path from config with env var expansion | key_path + kwargs -> Path
```

### Config Utilities

```
merge_config_dicts: Merge nested dicts (RQ-specific overrides) | base_dict + override_dict -> merged_dict
expand_env_vars_in_path: Expand environment variables in path strings | path_str -> expanded_str
validate_irt_params: Validate IRT config structure | config -> validation_report
validate_paths_exist: Validate paths in config exist | config_name -> validation_report
reset_config_cache: Reset config cache (testing helper) | None -> None
```

---

## Standard Library Functions (NOT in tools/ - no tool inventory documentation needed)

**Note:** The following standard library functions are used directly in analysis scripts and do NOT require tools_inventory.md documentation:

### pandas Operations

```
pd.read_csv: Load CSV data
pd.DataFrame.melt: Reshape wide to long
pd.DataFrame.merge: Join dataframes
pd.DataFrame.pivot: Reshape long to wide
pd.DataFrame.groupby: Group aggregations
pd.DataFrame.to_csv: Save dataframe to CSV
```

### numpy Operations

```
np.linspace: Generate evenly spaced values
np.log: Natural logarithm
np.array: Create numpy array
np.mean, np.std, np.median: Basic statistics
```

### pathlib Operations

```
Path.mkdir: Create directory
Path.exists: Check path exists
Path.read_text, Path.write_text: File I/O
```

**Why stdlib exempt?** These are well-documented in official Python/pandas/numpy docs. rq_tools agent has explicit exemption rule for stdlib functions (see agents/rq_tools.md Step 10).

---

## Tool Organization by Use Case

### IRT Calibration Workflow

1. **Data preparation:** `prepare_irt_input_from_wide` (or standard pandas operations)
2. **Model building:** `configure_irt_model`
3. **Model fitting:** `fit_irt_grm`
4. **Extract results:** `extract_theta_from_irt` + `extract_parameters_from_irt`
5. **Item purification:** `filter_items_by_quality` (2-pass, Decision D039)
6. **Validation:** `validate_irt_convergence` + `validate_irt_parameters`

**OR use pipeline wrapper:** `calibrate_irt` (all steps in one call)

### LMM Trajectory Workflow

1. **Data preparation:** `prepare_lmm_input_from_theta` (reshape + add time vars)
2. **Define candidates:** `configure_candidate_models` (5 models)
3. **Fit models:** `fit_lmm_trajectory` or `fit_lmm_trajectory_tsvr` (Decision D070)
4. **Model selection:** `compare_lmm_models_by_aic`
5. **Extract effects:** `extract_fixed_effects_from_lmm` + `extract_random_effects_from_lmm`
6. **Post-hoc tests:** `compute_contrasts_pairwise` (Decision D068 dual reporting)
7. **Effect sizes:** `compute_effect_sizes_cohens`
8. **Validation:** `validate_lmm_convergence` + `validate_lmm_residuals`

**OR use pipeline wrapper:** `run_lmm_analysis` (steps 1-5 in one call)

### Plotting Workflow

1. **Style setup:** `set_plot_style_defaults` (once at start)
2. **Generate plots:** `plot_trajectory` (theta scale) + `plot_trajectory_probability` (Decision D069, probability scale)
3. **Diagnostics:** `plot_diagnostics` (residuals, QQ plot, etc.)
4. **Save with data:** `save_plot_with_data` (PNG + CSV for reproducibility)

### Data Validation Workflow

1. **File checks:** `check_file_exists`
2. **Column checks:** `validate_data_columns`
3. **Missing data:** `check_missing_data`
4. **Range checks:** `validate_numeric_range`
5. **Lineage tracking:** `create_lineage_metadata` + `save_lineage_to_file` (every output file)
6. **Generate report:** `generate_validation_report` + `save_validation_report`

---

## Quick Reference by Module

**tools.analysis_irt (8 functions):** calibrate_irt, calibrate_grm, prepare_irt_input_from_wide, configure_irt_model, fit_irt_grm, extract_theta_from_irt, extract_parameters_from_irt, filter_items_by_quality

**tools.analysis_lmm (10 functions):** run_lmm_analysis, prepare_lmm_input_from_theta, configure_candidate_models, fit_lmm_trajectory, fit_lmm_trajectory_tsvr, compare_lmm_models_by_aic, extract_fixed_effects_from_lmm, extract_random_effects_from_lmm, compute_contrasts_pairwise, compute_effect_sizes_cohens

**tools.plotting (7 functions):** set_plot_style_defaults, plot_trajectory, plot_trajectory_probability, plot_diagnostics, plot_histogram_by_group, save_plot_with_data, convert_theta_to_probability

**tools.validation (14 functions):** check_missing_data, validate_data_columns, validate_numeric_range, check_file_exists, validate_irt_convergence, validate_irt_parameters, validate_lmm_convergence, validate_lmm_residuals, create_lineage_metadata, save_lineage_to_file, load_lineage_from_file, validate_lineage, generate_validation_report, save_validation_report

**tools.config (12 functions):** load_config_from_file, load_config_from_yaml, load_rq_config_merged, load_irt_config_from_yaml, load_lmm_config_from_yaml, load_plot_config_from_yaml, resolve_path_from_config, merge_config_dicts, expand_env_vars_in_path, validate_irt_params, validate_paths_exist, reset_config_cache

**Total:** 51 functions across 5 modules

---

## Decision-Specific Tools (Cross-Reference)

**Decision D039 (2-pass IRT purification):**
- `filter_items_by_quality` - Implements purification with |b| > 3.0 OR a < 0.4 thresholds

**Decision D068 (Dual reporting p-values):**
- `compute_contrasts_pairwise` - Reports BOTH uncorrected (α=0.05) AND Bonferroni-corrected p-values

**Decision D069 (Dual-scale trajectory plots):**
- `plot_trajectory_probability` - Generates plots with theta AND probability scales for interpretability

**Decision D070 (TSVR as LMM time variable):**
- `fit_lmm_trajectory_tsvr` - Uses TSVR (actual hours since encoding) instead of nominal days (0,1,3,6)

---

## Missing Tools (Not Yet Implemented)

**Classical Test Theory (CTT):**
- CTT scoring functions currently in legacy `utility.py` (not in tools/)
- If needed: agent should report as blocked with missing_tool error

**If you need a tool not listed here:** Report to rq_tools agent, which will either:
1. Find it in tools_inventory.md (you missed it in this catalog)
2. Confirm it's missing → trigger TDD workflow for implementation

---

**End of Tools Catalog**

**For detailed API specifications:** See [docs/tools_inventory.md](tools_inventory.md)
**For naming conventions:** See [docs/v4/tools_naming.md](v4/tools_naming.md)
**For tool status tracking:** See [docs/tools_status.csv](tools_status.csv)
