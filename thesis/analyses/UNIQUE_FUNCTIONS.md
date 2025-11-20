# UNIQUE STATISTICAL FUNCTIONS FOR CHAPTERS 5, 6, AND 7
## CLI-Based Architecture for Agent Execution

**Purpose:** This document specifies all statistical functions needed to execute analyses across Chapters 5-7. Each function is designed for command-line invocation by analysis agents.

**Date:** 2025-11-04
**Author:** Ronan Ronayne
**Status:** REVISED for CLI architecture

---

## ARCHITECTURE OVERVIEW

### Execution Pattern:
```bash
python theme.py \
  -function=function_name \
  -input=path/to/input.csv \
  -output=path/to/output.csv \
  -params=[param1=value1,param2=value2]
```

### Workflow:
1. **Data Selection Agent** → Uses data.py + variables.xlsx to generate analysis-specific datasets
2. **IRT Agent** → Runs IRT pipeline, produces theta scores CSV files
3. **Analysis Agent** → Runs statistical functions step-by-step via CLI
4. **Inspector Agent** → Validates outputs after each step before proceeding

### Key Principles:
- All input/output via file paths (CSV, pickle, JSON)
- Functions are stateless and idempotent
- Each function returns exit code (0=success, 1=error)
- Results saved to structured folders (results/CH{N}/RQ{N}/step{N}_output.csv)

---

## THEME 1: DATA PREPARATION TOOLS
**Module:** `data_prep.py`

### 1.1 `load_irt_theta_scores`
**Purpose:** Load IRT theta scores from saved CSV files
**CLI:**
```bash
python data_prep.py \
  -function=load_irt_theta_scores \
  -input=results/All/TQ_corr_noroom_2cats_p1_med_data_ability.csv \
  -output=data/temp/theta_scores.csv \
  -params=[subset_columns=['Theta_All']]
```
**Input:** Path to IRT theta scores CSV
**Output:** CSV with columns [UID, Test, Composite_ID, Theta_*, Days]
**Parameters:**
- `subset_columns`: List of theta columns to extract (default=all)
- `add_days`: Boolean, compute Days from Composite_ID (default=True)

**Used by RQs:** 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 5.11, 5.12, 5.13, 5.14, 5.15, 6.1, 6.2, 6.5, 6.6, 6.7, 6.12, 6.13, 6.14, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.16, 7.17, 7.18, 7.19, 7.20

---

### 1.2 `reshape_wide_to_long`
**Purpose:** Reshape wide-format theta scores to long format for LMM
**CLI:**
```bash
python data_prep.py \
  -function=reshape_wide_to_long \
  -input=data/temp/theta_scores.csv \
  -output=data/temp/theta_long.csv \
  -params=[id_vars=['UID','Test','Days'],value_vars=['Theta_What','Theta_Where','Theta_When'],var_name='Domain',value_name='Theta']
```
**Input:** Wide-format CSV (one row per UID×Test, multiple theta columns)
**Output:** Long-format CSV with factor column and single theta column
**Parameters:**
- `id_vars`: Columns to keep as identifiers
- `value_vars`: Theta columns to stack
- `var_name`: Name for new factor column
- `value_name`: Name for outcome column

**Used by RQs:** 5.1, 5.2, 5.3, 5.5, 5.6, 5.9, 5.10, 6.1, 6.2, 6.6, 6.7

---

### 1.3 `compute_time_transformations`
**Purpose:** Create time variables for LMM (linear, quadratic, logarithmic)
**CLI:**
```bash
python data_prep.py \
  -function=compute_time_transformations \
  -input=data/temp/theta_long.csv \
  -output=data/temp/theta_long_with_time.csv \
  -params=[transformations=['linear','quadratic','log'],log_constant=1]
```
**Input:** CSV with 'Days' column
**Output:** Same CSV with added columns: Days², log(Days+1)
**Parameters:**
- `transformations`: List of transformations ['linear','quadratic','log']
- `log_constant`: Constant to add before log (default=1)

**Used by RQs:** 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 6.1, 6.2, 6.4, 6.5, 6.6, 6.7, 6.10, 6.12

---

### 1.4 `merge_accuracy_confidence`
**Purpose:** Merge TQ (accuracy) and TC (confidence) theta scores
**CLI:**
```bash
python data_prep.py \
  -function=merge_accuracy_confidence \
  -input=data/temp/theta_tq.csv,data/temp/theta_tc.csv \
  -output=data/temp/theta_merged.csv \
  -params=[merge_keys=['UID','Test'],suffixes=['_TQ','_TC']]
```
**Input:** Two CSV paths (comma-separated): accuracy, confidence
**Output:** Merged CSV with both accuracy and confidence thetas
**Parameters:**
- `merge_keys`: Columns to merge on (default=['UID','Test'])
- `suffixes`: Suffixes for overlapping columns (default=['_TQ','_TC'])

**Used by RQs:** 6.1, 6.2, 6.5, 6.12, 6.13, 6.14, 7.12

---

### 1.5 `standardize_cognitive_tests`
**Purpose:** Convert cognitive test raw scores to T-scores (M=50, SD=10)
**CLI:**
```bash
python data_prep.py \
  -function=standardize_cognitive_tests \
  -input=data/cognitive_tests.csv \
  -output=data/cognitive_tests_standardized.csv \
  -params=[test_columns=['RAVLT','BVMT','NART','RPM'],use_sample_norms=True]
```
**Input:** CSV with cognitive test scores
**Output:** CSV with T-scored columns
**Parameters:**
- `test_columns`: Columns to standardize
- `use_sample_norms`: Boolean, use sample M/SD vs population norms (default=True)
- `normative_file`: Optional path to norms CSV (columns: test, M, SD)

**Used by RQs:** 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.10, 7.11, 7.15, 7.16, 7.17, 7.19, 7.20

---

### 1.6 `compute_mean_theta`
**Purpose:** Compute mean theta scores per participant (across time points or domains)
**CLI:**
```bash
python data_prep.py \
  -function=compute_mean_theta \
  -input=data/temp/theta_scores.csv \
  -output=data/temp/theta_means.csv \
  -params=[group_by=['UID'],theta_columns=['Theta_All']]
```
**Input:** CSV with theta scores (multiple rows per UID)
**Output:** CSV with one row per UID, mean theta columns
**Parameters:**
- `group_by`: Variables to group by (e.g., ['UID'] or ['UID','Domain'])
- `theta_columns`: Theta columns to average

**Used by RQs:** 7.1, 7.2, 7.4, 7.7, 7.8, 7.11, 7.12, 7.13, 7.14, 7.15, 7.16, 7.17

---

### 1.7 `extract_item_level_data`
**Purpose:** Load item-level accuracy and confidence responses (not aggregated thetas)
**CLI:**
```bash
python data_prep.py \
  -function=extract_item_level_data \
  -input=data/master.xlsx \
  -output=data/temp/item_level_responses.csv \
  -params=[analysis_set='All',response_type='accuracy',add_days=True]
```
**Input:** Path to master.xlsx or preprocessed item-level CSV
**Output:** Long-format CSV with one row per item response [UID, Test, Item, Response, Days]
**Parameters:**
- `analysis_set`: Which items to include (uses data.py logic)
- `response_type`: 'accuracy' or 'confidence'
- `add_days`: Boolean, compute Days from Test number

**Used by RQs:** 6.3, 6.4, 6.8, 6.9, 6.15, 7.13

---

### 1.8 `filter_participants`
**Purpose:** Exclude participants by age, UID, or other criteria
**CLI:**
```bash
python data_prep.py \
  -function=filter_participants \
  -input=data/temp/theta_scores.csv \
  -output=data/temp/theta_filtered.csv \
  -params=[age_range=[20,70],exclude_uids=[],min_complete_tests=4]
```
**Input:** CSV with participant data
**Output:** Filtered CSV
**Parameters:**
- `age_range`: Tuple [min, max] or None
- `exclude_uids`: List of UIDs to exclude or empty list
- `min_complete_tests`: Minimum number of completed tests (default=4)

**Used by RQs:** 5.9, 5.10, 7.8, 7.9, 7.10, 7.12

---

### 1.9 `create_piecewise_time_structure`
**Purpose:** Create piecewise time segments for consolidation analysis
**CLI:**
```bash
python data_prep.py \
  -function=create_piecewise_time_structure \
  -input=data/temp/theta_long.csv \
  -output=data/temp/theta_piecewise.csv \
  -params=[breakpoint=1,segments=['Early','Late'],center_time=True]
```
**Input:** CSV with Days column
**Output:** CSV with added columns: Segment, Days_within
**Parameters:**
- `breakpoint`: Day to split segments (default=1)
- `segments`: Names for segments (default=['Early','Late'])
- `center_time`: Boolean, center Days_within at 0 for each segment

**Used by RQs:** 5.2, 5.6, 5.8

---

### 1.10 `validate_data_structure`
**Purpose:** Check data completeness and structure before analysis
**CLI:**
```bash
python data_prep.py \
  -function=validate_data_structure \
  -input=data/temp/theta_scores.csv \
  -output=data/temp/validation_report.json \
  -params=[expected_n_obs=400,required_columns=['UID','Test','Theta_All']]
```
**Input:** CSV to validate
**Output:** JSON file with validation results
**Parameters:**
- `expected_n_obs`: Expected number of observations (e.g., 400)
- `required_columns`: List of columns that must be present

**Used by RQs:** All RQs (as pre-check step)

---

## THEME 2: IRT TOOLS (WRAPPERS)
**Module:** `irt_tools.py`

**Note:** Full IRT pipeline is already implemented in irt.py. These are wrapper functions for CLI access.

### 2.1 `run_irt_pipeline`
**Purpose:** Execute full IRT analysis pipeline
**CLI:**
```bash
python irt_tools.py \
  -function=run_irt_pipeline \
  -input=data/master.xlsx \
  -output=results/All/TQ_corr_noroom_2cats_p1_med \
  -params=[analysis_set='All',factors=1,correlated_factors=False,categories=2,iteration_level='med']
```
**Input:** Path to master.xlsx
**Output:** Directory with theta scores CSV, item params CSV, model pickle, summary txt
**Parameters:**
- `analysis_set`: Name from params.py (e.g., 'All', 'All by Domain')
- `factors`: Number of factors or factor names
- `correlated_factors`: Boolean
- `categories`: 2 (TQ) or 5 (TC)
- `iteration_level`: 'low', 'med', 'high'

**Used by RQs:** All RQs that require IRT theta scores (executed once per analysis set at start of chapter)

---

### 2.2 `extract_item_parameters`
**Purpose:** Extract item difficulty and discrimination from saved IRT model
**CLI:**
```bash
python irt_tools.py \
  -function=extract_item_parameters \
  -input=results/All/TQ_corr_noroom_2cats_p1_med_model.pkl \
  -output=data/temp/item_params.csv \
  -params=[item_names=None]
```
**Input:** Path to pickled IRT model
**Output:** CSV with columns [Item, Difficulty, Discrimination, Factor]
**Parameters:**
- `item_names`: List of items to extract (None=all)

**Used by RQs:** 5.15, 6.14

---

### 2.3 `compute_irt_reliability`
**Purpose:** Compute IRT marginal reliability from theta SEs
**CLI:**
```bash
python irt_tools.py \
  -function=compute_irt_reliability \
  -input=results/All/TQ_corr_noroom_2cats_p1_med_data_ability.csv \
  -output=data/temp/reliability_report.json \
  -params=[]
```
**Input:** CSV with Theta and SE_Theta columns
**Output:** JSON with {'reliability': float, 'mean_SE': float, 'SE_range': [min, max]}
**Parameters:** None

**Used by RQs:** 7.17

---

## THEME 3: LMM (LINEAR MIXED MODELS) TOOLS
**Module:** `lmm_tools.py`

### 3.1 `fit_lmm`
**Purpose:** Fit single linear mixed model
**CLI:**
```bash
python lmm_tools.py \
  -function=fit_lmm \
  -input=data/temp/theta_long.csv \
  -output=results/CH5/RQ1/model_linlog.pkl \
  -params=[formula='Theta ~ Days + np.log(Days+1)',groups='UID',re_formula='~ Days',reml=False]
```
**Input:** Long-format CSV
**Output:** Pickled MixedLM result object
**Parameters:**
- `formula`: R-style formula string
- `groups`: Grouping variable column name
- `re_formula`: Random effects formula (default='~ Days')
- `reml`: Boolean (default=False for AIC comparison)

**Used by RQs:** 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7, 5.8, 5.9, 5.10, 6.1, 6.2, 6.4, 6.5, 6.6, 6.7, 6.10, 6.11, 6.12

---

### 3.2 `fit_multiple_lmms`
**Purpose:** Fit multiple LMM specifications and compare via AIC
**CLI:**
```bash
python lmm_tools.py \
  -function=fit_multiple_lmms \
  -input=data/temp/theta_long.csv \
  -output=results/CH5/RQ1/aic_comparison.csv \
  -params=[formulas=['Linear:Theta~Days','Quad:Theta~Days+I(Days**2)','Log:Theta~np.log(Days+1)'],groups='UID',re_formula='~Days',save_models=True,model_dir='results/CH5/RQ1/models/']
```
**Input:** Long-format CSV
**Output:** CSV with columns [Model, AIC, ΔAIC, Akaike_Weight, Converged]
**Parameters:**
- `formulas`: List of 'name:formula' strings
- `groups`: Grouping variable
- `re_formula`: Random effects formula
- `save_models`: Boolean, save each model as pickle (default=True)
- `model_dir`: Directory to save models

**Used by RQs:** 5.1, 5.3, 5.5, 5.7

---

### 3.3 `extract_lmm_fixed_effects`
**Purpose:** Extract fixed effects table from fitted LMM
**CLI:**
```bash
python lmm_tools.py \
  -function=extract_lmm_fixed_effects \
  -input=results/CH5/RQ1/model_linlog.pkl \
  -output=results/CH5/RQ1/fixed_effects.csv \
  -params=[alpha=0.05]
```
**Input:** Pickled LMM model
**Output:** CSV with columns [Term, β, SE, z, p, CI_lower, CI_upper]
**Parameters:**
- `alpha`: Confidence level (default=0.05 for 95% CI)

**Used by RQs:** 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.9, 5.10, 6.1, 6.2, 6.4, 6.5, 6.6, 6.7, 6.10, 6.12

---

### 3.4 `extract_lmm_random_effects`
**Purpose:** Extract random effects variances and correlation
**CLI:**
```bash
python lmm_tools.py \
  -function=extract_lmm_random_effects \
  -input=results/CH5/RQ1/model_linlog.pkl \
  -output=results/CH5/RQ1/random_effects_summary.json \
  -params=[]
```
**Input:** Pickled LMM model
**Output:** JSON with {'σ²_intercept', 'σ²_slope', 'ρ', 'σ²_residual'}
**Parameters:** None

**Used by RQs:** 5.1, 5.13, 7.3

---

### 3.5 `extract_lmm_blups`
**Purpose:** Extract subject-specific random intercepts and slopes (BLUPs)
**CLI:**
```bash
python lmm_tools.py \
  -function=extract_lmm_blups \
  -input=results/CH5/RQ1/model_linlog.pkl \
  -output=results/CH5/RQ1/blups.csv \
  -params=[groups_col='UID']
```
**Input:** Pickled LMM model
**Output:** CSV with columns [UID, Intercept, Slope_Days, Slope_Log]
**Parameters:**
- `groups_col`: Name of grouping variable (default='UID')

**Used by RQs:** 5.13, 5.14, 7.3

---

### 3.6 `compute_lmm_predictions`
**Purpose:** Generate model-predicted values from fitted LMM
**CLI:**
```bash
python lmm_tools.py \
  -function=compute_lmm_predictions \
  -input=results/CH5/RQ1/model_linlog.pkl,data/temp/theta_long.csv \
  -output=results/CH5/RQ1/predictions.csv \
  -params=[level='population']
```
**Input:** Two paths (comma-separated): pickled model, data for prediction
**Output:** CSV with original data plus 'Predicted' column
**Parameters:**
- `level`: 'population' (fixed only) or 'subject' (fixed + random)

**Used by RQs:** 5.1, 5.3, 5.5, 6.1, 6.2, 6.5, 6.6, 6.7

---

### 3.7 `test_random_slopes_necessity`
**Purpose:** Likelihood ratio test comparing intercepts-only vs random slopes
**CLI:**
```bash
python lmm_tools.py \
  -function=test_random_slopes_necessity \
  -input=results/CH5/RQ1/model_intercepts.pkl,results/CH5/RQ1/model_slopes.pkl \
  -output=results/CH5/RQ1/lrt_slopes.json \
  -params=[]
```
**Input:** Two pickled models (comma-separated): intercepts-only, with-slopes
**Output:** JSON with {'χ²', 'df', 'p', 'conclusion'}
**Parameters:** None

**Used by RQs:** 5.1, 5.13

---

### 3.8 `compute_icc`
**Purpose:** Compute intraclass correlation from LMM
**CLI:**
```bash
python lmm_tools.py \
  -function=compute_icc \
  -input=results/CH5/RQ1/model_linlog.pkl \
  -output=results/CH5/RQ1/icc.json \
  -params=[]
```
**Input:** Pickled LMM model
**Output:** JSON with {'ICC': float}
**Parameters:** None

**Used by RQs:** 5.13, 7.3

---

### 3.9 `compute_lmm_diagnostics`
**Purpose:** Generate diagnostic plots and statistics for LMM
**CLI:**
```bash
python lmm_tools.py \
  -function=compute_lmm_diagnostics \
  -input=results/CH5/RQ1/model_linlog.pkl \
  -output=results/CH5/RQ1/diagnostics/ \
  -params=[diagnostics=['residuals','qq','influential','random_effects']]
```
**Input:** Pickled LMM model
**Output:** Directory with diagnostic plots (PNG) and summary JSON
**Parameters:**
- `diagnostics`: List of diagnostics to compute

**Used by RQs:** All RQs using LMM (for validation)

---

## THEME 4: MODEL COMPARISON TOOLS
**Module:** `model_comparison.py`

### 4.1 `compute_aic_table`
**Purpose:** Create AIC comparison table from multiple models
**CLI:**
```bash
python model_comparison.py \
  -function=compute_aic_table \
  -input=results/CH5/RQ1/models/ \
  -output=results/CH5/RQ1/aic_comparison.csv \
  -params=[model_pattern='*.pkl']
```
**Input:** Directory containing pickled models
**Output:** CSV with columns [Model, AIC, ΔAIC, Akaike_Weight]
**Parameters:**
- `model_pattern`: Glob pattern to match model files (default='*.pkl')

**Used by RQs:** 5.1, 5.3, 5.5, 5.7

---

### 4.2 `compute_akaike_weights`
**Purpose:** Compute Akaike weights from AIC values
**CLI:**
```bash
python model_comparison.py \
  -function=compute_akaike_weights \
  -input=results/CH5/RQ1/aic_table.csv \
  -output=results/CH5/RQ1/aic_table_weighted.csv \
  -params=[]
```
**Input:** CSV with AIC column
**Output:** CSV with added Akaike_Weight column
**Parameters:** None

**Used by RQs:** 5.1, 5.3, 5.5, 5.7

---

### 4.3 `likelihood_ratio_test`
**Purpose:** LRT between nested models
**CLI:**
```bash
python model_comparison.py \
  -function=likelihood_ratio_test \
  -input=results/CH5/RQ1/model_restricted.pkl,results/CH5/RQ1/model_full.pkl \
  -output=results/CH5/RQ1/lrt_result.json \
  -params=[]
```
**Input:** Two pickled models (comma-separated): restricted, full
**Output:** JSON with {'LR', 'df', 'p'}
**Parameters:** None

**Used by RQs:** 5.1, 5.13, 7.3

---

## THEME 5: REGRESSION TOOLS
**Module:** `regression_tools.py`

### 5.1 `fit_multiple_regression`
**Purpose:** Fit OLS multiple regression
**CLI:**
```bash
python regression_tools.py \
  -function=fit_multiple_regression \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ1/regression_model.pkl \
  -params=[formula='Theta_All ~ RAVLT + BVMT + NART + RPM',standardize=False]
```
**Input:** CSV with outcome and predictors
**Output:** Pickled OLS result object
**Parameters:**
- `formula`: R-style formula
- `standardize`: Boolean, standardize predictors (default=False)

**Used by RQs:** 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.11, 7.12, 7.13, 7.16, 7.19, 7.20

---

### 5.2 `extract_regression_summary`
**Purpose:** Extract regression summary table
**CLI:**
```bash
python regression_tools.py \
  -function=extract_regression_summary \
  -input=results/CH7/RQ1/regression_model.pkl \
  -output=results/CH7/RQ1/regression_summary.csv \
  -params=[alpha=0.05]
```
**Input:** Pickled OLS model
**Output:** CSV with [Term, β, SE, t, p, CI_lower, CI_upper, R², Adj_R², F, p_F]
**Parameters:**
- `alpha`: Confidence level (default=0.05)

**Used by RQs:** 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7, 7.8, 7.9, 7.11, 7.12, 7.13, 7.16, 7.19, 7.20

---

### 5.3 `compute_vif`
**Purpose:** Compute variance inflation factors
**CLI:**
```bash
python regression_tools.py \
  -function=compute_vif \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ1/vif.csv \
  -params=[predictor_cols=['RAVLT','BVMT','NART','RPM']]
```
**Input:** CSV with predictor variables
**Output:** CSV with columns [Variable, VIF]
**Parameters:**
- `predictor_cols`: List of predictor column names

**Used by RQs:** 7.1, 7.2, 7.4, 7.8, 7.10, 7.16, 7.17

---

### 5.4 `compute_semi_partial_correlations`
**Purpose:** Compute unique variance per predictor
**CLI:**
```bash
python regression_tools.py \
  -function=compute_semi_partial_correlations \
  -input=results/CH7/RQ1/regression_model.pkl \
  -output=results/CH7/RQ1/sr2.csv \
  -params=[]
```
**Input:** Pickled regression model
**Output:** CSV with columns [Predictor, sr²]
**Parameters:** None

**Used by RQs:** 7.1, 7.4

---

### 5.5 `fit_hierarchical_regression`
**Purpose:** Fit hierarchical regression with ΔR² tests
**CLI:**
```bash
python regression_tools.py \
  -function=fit_hierarchical_regression \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ4/hierarchical_results.csv \
  -params=[blocks=[['Age','Sex'],['RAVLT','BVMT'],['DASS']],dv='Theta_All',cumulative=True]
```
**Input:** CSV with outcome and all predictors
**Output:** CSV with columns [Step, Predictors, R², ΔR², F_ΔR², p_ΔR²]
**Parameters:**
- `blocks`: List of predictor sets
- `dv`: Dependent variable name
- `cumulative`: Boolean, blocks are cumulative (default=True)

**Used by RQs:** 7.4, 7.8, 7.11, 7.17

---

### 5.6 `stepwise_selection`
**Purpose:** Forward/backward stepwise variable selection
**CLI:**
```bash
python regression_tools.py \
  -function=stepwise_selection \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ16/stepwise_results.json \
  -params=[dv='Theta_All',candidate_predictors=['Age','RAVLT','BVMT','NART','RPM'],direction='both',criterion='AIC']
```
**Input:** CSV with outcome and candidates
**Output:** JSON with {'final_model': model info, 'selected_predictors': list, 'steps': DataFrame as dict}
**Parameters:**
- `dv`: Dependent variable name
- `candidate_predictors`: List of predictor names
- `direction`: 'forward', 'backward', 'both'
- `criterion`: 'AIC' or 'BIC'

**Used by RQs:** 7.16

---

### 5.7 `fit_multivariate_regression`
**Purpose:** Fit multivariate regression (multiple DVs)
**CLI:**
```bash
python regression_tools.py \
  -function=fit_multivariate_regression \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ18/multivariate_results.json \
  -params=[dvs=['Theta_What','Theta_Where','Theta_When'],predictors=['RAVLT','BVMT','RPM']]
```
**Input:** CSV with multiple outcomes and predictors
**Output:** JSON with model summaries and multivariate statistics
**Parameters:**
- `dvs`: List of dependent variable names
- `predictors`: List of predictor names

**Used by RQs:** 7.18

---

### 5.8 `test_regression_coefficients_equality`
**Purpose:** Wald test for coefficient equality across models
**CLI:**
```bash
python regression_tools.py \
  -function=test_regression_coefficients_equality \
  -input=results/CH7/RQ2/model_what.pkl,results/CH7/RQ2/model_where.pkl,results/CH7/RQ2/model_when.pkl \
  -output=results/CH7/RQ2/wald_test.json \
  -params=[coefficient_name='RAVLT']
```
**Input:** Multiple pickled models (comma-separated)
**Output:** JSON with {'χ²', 'df', 'p'}
**Parameters:**
- `coefficient_name`: Which coefficient to test

**Used by RQs:** 7.2, 7.18

---

### 5.9 `compute_partial_correlations`
**Purpose:** Partial correlation controlling for covariates
**CLI:**
```bash
python regression_tools.py \
  -function=compute_partial_correlations \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ9/partial_corr.json \
  -params=[x='Age',y='Theta_All',covariates=['RAVLT','BVMT']]
```
**Input:** CSV with variables
**Output:** JSON with {'r_partial', 'p'}
**Parameters:**
- `x`: Variable 1 name
- `y`: Variable 2 name
- `covariates`: List of covariate names

**Used by RQs:** 7.9

---

### 5.10 `fit_interaction_model`
**Purpose:** Fit regression with interaction
**CLI:**
```bash
python regression_tools.py \
  -function=fit_interaction_model \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ10/interaction_model.pkl \
  -params=[formula='Theta ~ Age * RAVLT',center_predictors=True]
```
**Input:** CSV with outcome and predictors
**Output:** Pickled regression model
**Parameters:**
- `formula`: Formula with interaction
- `center_predictors`: Boolean, mean-center (default=True)

**Used by RQs:** 7.10

---

### 5.11 `probe_interaction`
**Purpose:** Compute simple slopes at moderator levels
**CLI:**
```bash
python regression_tools.py \
  -function=probe_interaction \
  -input=results/CH7/RQ10/interaction_model.pkl \
  -output=results/CH7/RQ10/simple_slopes.csv \
  -params=[moderator='Age',levels=[-1,0,1]]
```
**Input:** Pickled interaction model
**Output:** CSV with columns [Moderator_Level, Slope, SE, t, p]
**Parameters:**
- `moderator`: Name of moderator variable
- `levels`: Values to probe (default=[-1,0,1] SD units)

**Used by RQs:** 7.10

---

## THEME 6: CORRELATION & ASSOCIATION TOOLS
**Module:** `correlation_tools.py`

### 6.1 `compute_correlation_matrix`
**Purpose:** Correlation matrix with significance tests
**CLI:**
```bash
python correlation_tools.py \
  -function=compute_correlation_matrix \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ20/correlation_matrix.csv \
  -params=[variables=['Theta_Free','Theta_Cued','Theta_Recognition','RAVLT','BVMT'],method='pearson']
```
**Input:** CSV with variables to correlate
**Output:** Two CSVs: correlations.csv and pvalues.csv
**Parameters:**
- `variables`: List of variable names
- `method`: 'pearson', 'spearman', 'kendall'

**Used by RQs:** 7.20, 6.13

---

### 6.2 `steiger_z_test`
**Purpose:** Compare two dependent correlations
**CLI:**
```bash
python correlation_tools.py \
  -function=steiger_z_test \
  -input=data/temp/correlations.csv \
  -output=results/CH7/RQ2/steiger_test.json \
  -params=[r12=0.45,r13=0.28,r23=0.62,n=100]
```
**Input:** CSV with correlation matrix OR individual r values as params
**Output:** JSON with {'z', 'p'}
**Parameters:**
- `r12`: Correlation between var1 and var2
- `r13`: Correlation between var1 and var3
- `r23`: Correlation between var2 and var3
- `n`: Sample size

**Used by RQs:** 7.2, 7.5, 7.6, 7.20

---

### 6.3 `goodman_kruskal_gamma`
**Purpose:** Compute gamma for ordinal association
**CLI:**
```bash
python correlation_tools.py \
  -function=goodman_kruskal_gamma \
  -input=data/temp/item_level_responses.csv \
  -output=results/CH6/RQ4/gamma_per_subject.csv \
  -params=[x_col='confidence',y_col='accuracy',group_by=['UID','Days']]
```
**Input:** CSV with ordinal variables
**Output:** CSV with columns [GroupVars, gamma, SE, p]
**Parameters:**
- `x_col`: Confidence/predictor column
- `y_col`: Accuracy/outcome column
- `group_by`: Variables to compute gamma within (e.g., per participant per day)

**Used by RQs:** 6.4, 6.6

---

### 6.4 `compute_contingency_table`
**Purpose:** Create contingency table and test independence
**CLI:**
```bash
python correlation_tools.py \
  -function=compute_contingency_table \
  -input=data/temp/profile_data.csv \
  -output=results/CH7/RQ15/contingency_table.csv \
  -params=[row_var='CogProfile',col_var='REMEMVRProfile',test='chi2']
```
**Input:** CSV with categorical variables
**Output:** CSV (contingency table) + JSON with test results
**Parameters:**
- `row_var`: Row variable name
- `col_var`: Column variable name
- `test`: 'chi2' or 'fisher'

**Used by RQs:** 7.15

---

### 6.5 `cramers_v`
**Purpose:** Compute Cramér's V effect size
**CLI:**
```bash
python correlation_tools.py \
  -function=cramers_v \
  -input=results/CH7/RQ15/contingency_table.csv \
  -output=results/CH7/RQ15/cramers_v.json \
  -params=[]
```
**Input:** CSV contingency table
**Output:** JSON with {'cramers_v': float}
**Parameters:** None

**Used by RQs:** 7.15

---

### 6.6 `compute_odds_ratio`
**Purpose:** Odds ratio with CI for 2×2 table
**CLI:**
```bash
python correlation_tools.py \
  -function=compute_odds_ratio \
  -input=results/CH7/RQ15/contingency_2x2.csv \
  -output=results/CH7/RQ15/odds_ratio.json \
  -params=[alpha=0.05]
```
**Input:** 2×2 CSV contingency table
**Output:** JSON with {'OR', 'CI_lower', 'CI_upper', 'p'}
**Parameters:**
- `alpha`: Confidence level (default=0.05)

**Used by RQs:** 7.15

---

## THEME 7: METACOGNITION METRICS TOOLS
**Module:** `metacognition.py`

### 7.1 `compute_brier_score`
**Purpose:** Compute Brier score per day
**CLI:**
```bash
python metacognition.py \
  -function=compute_brier_score \
  -input=data/temp/item_level_responses.csv \
  -output=results/CH6/RQ3/brier_scores.csv \
  -params=[accuracy_col='accuracy',confidence_col='confidence',group_by=['Days']]
```
**Input:** CSV with item-level accuracy and confidence
**Output:** CSV with columns [Days, Brier_Score, N_Items]
**Parameters:**
- `accuracy_col`: Binary outcome column (0/1)
- `confidence_col`: Confidence column (0-1)
- `group_by`: Variables to compute Brier score within (e.g., per day)

**Used by RQs:** 6.3

---

### 7.2 `compute_calibration_curve`
**Purpose:** Create calibration curve (binned)
**CLI:**
```bash
python metacognition.py \
  -function=compute_calibration_curve \
  -input=data/temp/item_level_responses.csv \
  -output=results/CH6/RQ3/calibration_curves.csv \
  -params=[accuracy_col='accuracy',confidence_col='confidence',group_by=['Days'],n_bins=5,strategy='uniform']
```
**Input:** CSV with item-level data
**Output:** CSV with columns [Days, Bin, Mean_Confidence, Mean_Accuracy, N_Items]
**Parameters:**
- `accuracy_col`, `confidence_col`: Column names
- `group_by`: Variables to compute curves within
- `n_bins`: Number of bins (default=5)
- `strategy`: 'uniform' or 'quantile'

**Used by RQs:** 6.3

---

### 7.3 `compute_ece`
**Purpose:** Expected Calibration Error
**CLI:**
```bash
python metacognition.py \
  -function=compute_ece \
  -input=data/temp/item_level_responses.csv \
  -output=results/CH6/RQ3/ece.csv \
  -params=[accuracy_col='accuracy',confidence_col='confidence',group_by=['Days'],n_bins=5]
```
**Input:** CSV with item-level data
**Output:** CSV with columns [Days, ECE]
**Parameters:**
- `accuracy_col`, `confidence_col`, `group_by`, `n_bins`: Same as 7.2

**Used by RQs:** 6.3

---

### 7.4 `compute_utility`
**Purpose:** Metacognitive utility (accuracy - confidence, inverted)
**CLI:**
```bash
python metacognition.py \
  -function=compute_utility \
  -input=data/temp/theta_merged.csv \
  -output=data/temp/theta_with_utility.csv \
  -params=[accuracy_col='Theta_TQ',confidence_col='Theta_TC',invert=True]
```
**Input:** CSV with accuracy and confidence columns
**Output:** Same CSV with added 'Utility' column
**Parameters:**
- `accuracy_col`, `confidence_col`: Column names
- `invert`: Boolean, multiply by -1 (default=True, so higher=better)

**Used by RQs:** 6.5, 6.14

---

### 7.5 `identify_high_confidence_errors`
**Purpose:** Extract high-confidence errors
**CLI:**
```bash
python metacognition.py \
  -function=identify_high_confidence_errors \
  -input=data/temp/item_level_responses.csv \
  -output=results/CH6/RQ8/high_conf_errors.csv \
  -params=[accuracy_col='accuracy',confidence_col='confidence',confidence_threshold=0.75]
```
**Input:** CSV with item-level data
**Output:** Filtered CSV (accuracy=0, confidence>threshold)
**Parameters:**
- `accuracy_col`, `confidence_col`: Column names
- `confidence_threshold`: Minimum confidence (default=0.75)

**Used by RQs:** 6.8, 6.9

---

### 7.6 `compute_confidence_bias_correction`
**Purpose:** Within-person z-score normalization of confidence
**CLI:**
```bash
python metacognition.py \
  -function=compute_confidence_bias_correction \
  -input=data/temp/item_level_responses.csv \
  -output=data/temp/item_level_zscore.csv \
  -params=[confidence_col='confidence',group_by=['UID']]
```
**Input:** CSV with confidence ratings
**Output:** Same CSV with added 'confidence_zscore' column
**Parameters:**
- `confidence_col`: Column name
- `group_by`: Variable to compute z-scores within (typically 'UID')

**Used by RQs:** 6.1, 6.2, 6.3 (as sensitivity check)

---

## THEME 8: LATENT VARIABLE TOOLS
**Module:** `latent_variable.py`

### 8.1 `fit_latent_profile_analysis`
**Purpose:** Fit LPA models with 1-k classes
**CLI:**
```bash
python latent_variable.py \
  -function=fit_latent_profile_analysis \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ14/lpa_results/ \
  -params=[indicators=['Theta_What','Theta_Where','Theta_When'],n_classes_range=[1,5],covariance_type='full',n_init=100]
```
**Input:** CSV with indicator variables
**Output:** Directory with model pickles + summary CSV (BIC, AIC, entropy per k)
**Parameters:**
- `indicators`: List of column names
- `n_classes_range`: [min, max] classes to test
- `covariance_type`: 'spherical', 'tied', 'diag', 'full'
- `n_init`: Random initializations

**Used by RQs:** 5.14, 7.14, 7.15

---

### 8.2 `extract_lpa_class_membership`
**Purpose:** Extract most likely class per observation
**CLI:**
```bash
python latent_variable.py \
  -function=extract_lpa_class_membership \
  -input=results/CH7/RQ14/lpa_results/model_k3.pkl \
  -output=results/CH7/RQ14/class_membership.csv \
  -params=[include_probabilities=True]
```
**Input:** Pickled LPA model
**Output:** CSV with columns [ObsID, Class, Prob_Class1, Prob_Class2, ...]
**Parameters:**
- `include_probabilities`: Boolean (default=True)

**Used by RQs:** 5.14, 7.14, 7.15

---

### 8.3 `compute_lpa_entropy`
**Purpose:** Compute classification entropy
**CLI:**
```bash
python latent_variable.py \
  -function=compute_lpa_entropy \
  -input=results/CH7/RQ14/class_membership.csv \
  -output=results/CH7/RQ14/entropy.json \
  -params=[]
```
**Input:** CSV with posterior probabilities
**Output:** JSON with {'entropy': float}
**Parameters:** None

**Used by RQs:** 5.14, 7.14, 7.15

---

### 8.4 `characterize_lpa_profiles`
**Purpose:** Compute profile means per class
**CLI:**
```bash
python latent_variable.py \
  -function=characterize_lpa_profiles \
  -input=data/temp/theta_means.csv,results/CH7/RQ14/class_membership.csv \
  -output=results/CH7/RQ14/profile_means.csv \
  -params=[indicators=['Theta_What','Theta_Where','Theta_When']]
```
**Input:** Two CSVs (comma-separated): data, class membership
**Output:** CSV with columns [Class, n, Mean_Theta_What, Mean_Theta_Where, ...]
**Parameters:**
- `indicators`: Variable names to summarize

**Used by RQs:** 5.14, 7.14, 7.15

---

### 8.5 `predict_profile_membership`
**Purpose:** Multinomial logistic regression for profile membership
**CLI:**
```bash
python latent_variable.py \
  -function=predict_profile_membership \
  -input=data/temp/theta_means.csv,results/CH7/RQ14/class_membership.csv \
  -output=results/CH7/RQ14/profile_prediction.json \
  -params=[dv='Class',predictors=['Age','RAVLT','BVMT'],reference_class=1]
```
**Input:** Two CSVs: data, class membership
**Output:** JSON with model summary (ORs, p-values per predictor per class)
**Parameters:**
- `dv`: Class membership column name
- `predictors`: List of predictor names
- `reference_class`: Reference class (default=largest)

**Used by RQs:** 7.14, 7.15

---

### 8.6 `correspondence_analysis`
**Purpose:** Correspondence analysis on contingency table
**CLI:**
```bash
python latent_variable.py \
  -function=correspondence_analysis \
  -input=results/CH7/RQ15/contingency_table.csv \
  -output=results/CH7/RQ15/correspondence_analysis.json \
  -params=[n_components=2]
```
**Input:** Contingency table CSV
**Output:** JSON with {'row_coords', 'col_coords', 'inertia', 'explained_variance'}
**Parameters:**
- `n_components`: Number of dimensions (default=2)

**Used by RQs:** 7.15

---

### 8.7 `hierarchical_clustering`
**Purpose:** Hierarchical clustering on correlation matrix
**CLI:**
```bash
python latent_variable.py \
  -function=hierarchical_clustering \
  -input=results/CH7/RQ20/correlation_matrix.csv \
  -output=results/CH7/RQ20/dendrogram.pkl \
  -params=[method='average',metric='euclidean']
```
**Input:** Correlation matrix CSV or data CSV
**Output:** Pickle with {'linkage_matrix', 'dendrogram_dict', 'cophenetic_corr'}
**Parameters:**
- `method`: 'single', 'complete', 'average', 'ward'
- `metric`: Distance metric

**Used by RQs:** 7.20

---

## THEME 9: EFFECT SIZE TOOLS
**Module:** `effect_sizes.py`

### 9.1 `compute_cohens_d`
**Purpose:** Cohen's d for mean difference
**CLI:**
```bash
python effect_sizes.py \
  -function=compute_cohens_d \
  -input=data/temp/theta_long.csv \
  -output=results/CH5/RQ1/cohens_d.csv \
  -params=[group_var='Domain',value_var='Theta',groups_to_compare=[['What','Where'],['What','When']],pooled_sd=True]
```
**Input:** CSV with grouping variable and continuous outcome
**Output:** CSV with columns [Comparison, d, Group1_M, Group2_M]
**Parameters:**
- `group_var`: Grouping variable name
- `value_var`: Continuous variable name
- `groups_to_compare`: List of [group1, group2] pairs
- `pooled_sd`: Boolean (default=True)

**Used by RQs:** 5.1, 5.3, 5.5, 6.1

---

### 9.2 `compute_cohens_f2`
**Purpose:** Cohen's f² for incremental R²
**CLI:**
```bash
python effect_sizes.py \
  -function=compute_cohens_f2 \
  -input=results/CH7/RQ4/hierarchical_results.csv \
  -output=results/CH7/RQ4/cohens_f2.csv \
  -params=[]
```
**Input:** CSV with R²_full and R²_restricted columns
**Output:** CSV with added 'f²' column
**Parameters:** None

**Used by RQs:** 7.4, 7.8

---

### 9.3 `compute_eta_squared`
**Purpose:** η² for ANOVA
**CLI:**
```bash
python effect_sizes.py \
  -function=compute_eta_squared \
  -input=results/CH7/RQ11/anova_results.json \
  -output=results/CH7/RQ11/eta_squared.json \
  -params=[]
```
**Input:** JSON with SS_effect and SS_total
**Output:** JSON with {'η²': float}
**Parameters:** None

**Used by RQs:** 7.11

---

## THEME 10: VISUALIZATION TOOLS
**Module:** `visualization.py`

### 10.1 `plot_lmm_trajectory`
**Purpose:** Trajectory plot from LMM
**CLI:**
```bash
python visualization.py \
  -function=plot_lmm_trajectory \
  -input=data/temp/theta_long.csv,results/CH5/RQ1/predictions.csv \
  -output=results/CH5/RQ1/trajectory_plot.png \
  -params=[x_var='Days',y_var='Theta',group_var='Domain',show_ci=True,show_observed=True]
```
**Input:** Two CSVs (comma-separated): observed data, predictions
**Output:** PNG figure
**Parameters:**
- `x_var`, `y_var`, `group_var`: Column names
- `show_ci`: Boolean (default=True)
- `show_observed`: Boolean (default=True)

**Used by RQs:** 5.1, 5.2, 5.3, 5.5, 5.9, 5.10, 6.1, 6.2, 6.5, 6.6, 6.7

---

### 10.2 `plot_calibration_curve`
**Purpose:** Calibration curve plot
**CLI:**
```bash
python visualization.py \
  -function=plot_calibration_curve \
  -input=results/CH6/RQ3/calibration_curves.csv \
  -output=results/CH6/RQ3/calibration_plot.png \
  -params=[days_to_plot=[0,6],show_perfect_line=True,annotate_bins=True]
```
**Input:** CSV from compute_calibration_curve()
**Output:** PNG figure
**Parameters:**
- `days_to_plot`: List of days to plot (default=[0,6])
- `show_perfect_line`: Boolean
- `annotate_bins`: Boolean

**Used by RQs:** 6.3

---

### 10.3 `plot_diagnostics`
**Purpose:** Diagnostic plots (Q-Q, residuals vs fitted)
**CLI:**
```bash
python visualization.py \
  -function=plot_diagnostics \
  -input=results/CH5/RQ1/model_linlog.pkl \
  -output=results/CH5/RQ1/diagnostics/ \
  -params=[plots=['qq','residuals','scale_location','leverage']]
```
**Input:** Pickled model (LMM or OLS)
**Output:** Directory with PNG figures
**Parameters:**
- `plots`: List of diagnostic types

**Used by RQs:** All RQs (validation step)

---

### 10.4 `plot_correlation_matrix`
**Purpose:** Heatmap of correlation matrix
**CLI:**
```bash
python visualization.py \
  -function=plot_correlation_matrix \
  -input=results/CH7/RQ20/correlation_matrix.csv \
  -output=results/CH7/RQ20/correlation_heatmap.png \
  -params=[annotate=True,cmap='coolwarm',vmin=-1,vmax=1]
```
**Input:** Correlation matrix CSV
**Output:** PNG figure
**Parameters:**
- `annotate`: Boolean
- `cmap`: Colormap name
- `vmin`, `vmax`: Color limits

**Used by RQs:** 7.20

---

### 10.5 `plot_forest`
**Purpose:** Forest plot of regression coefficients
**CLI:**
```bash
python visualization.py \
  -function=plot_forest \
  -input=results/CH7/RQ1/regression_summary.csv \
  -output=results/CH7/RQ1/forest_plot.png \
  -params=[sort_by='effect_size',show_reference_line=True]
```
**Input:** CSV with columns [Term, β, CI_lower, CI_upper]
**Output:** PNG figure
**Parameters:**
- `sort_by`: 'effect_size' or 'alphabetical'
- `show_reference_line`: Boolean (line at β=0)

**Used by RQs:** 7.1, 7.2, 7.4

---

### 10.6 `plot_interaction`
**Purpose:** Interaction plot (simple slopes)
**CLI:**
```bash
python visualization.py \
  -function=plot_interaction \
  -input=results/CH7/RQ10/simple_slopes.csv \
  -output=results/CH7/RQ10/interaction_plot.png \
  -params=[x_var='RAVLT',moderator='Age',moderator_levels=[-1,0,1]]
```
**Input:** CSV from probe_interaction()
**Output:** PNG figure
**Parameters:**
- `x_var`: Focal predictor name
- `moderator`: Moderator variable name
- `moderator_levels`: Values plotted

**Used by RQs:** 7.10

---

## THEME 11: RESAMPLING & CROSS-VALIDATION TOOLS
**Module:** `resampling.py`

### 11.1 `bootstrap_ci`
**Purpose:** Bootstrap confidence interval for any statistic
**CLI:**
```bash
python resampling.py \
  -function=bootstrap_ci \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ4/bootstrap_r2_ci.json \
  -params=[statistic='r2',formula='Theta~RAVLT+BVMT',n_bootstrap=10000,alpha=0.05,method='percentile']
```
**Input:** CSV with data
**Output:** JSON with {'CI_lower', 'CI_upper', 'statistic_value'}
**Parameters:**
- `statistic`: 'r2', 'mean', 'correlation', etc.
- `formula`: Model formula (if statistic='r2')
- `n_bootstrap`: Number of samples
- `alpha`: Confidence level
- `method`: 'percentile' or 'bca'

**Used by RQs:** 7.2, 7.3, 7.4, 7.9

---

### 11.2 `cross_validate_model`
**Purpose:** k-fold cross-validation for regression
**CLI:**
```bash
python resampling.py \
  -function=cross_validate_model \
  -input=data/temp/theta_means.csv \
  -output=results/CH7/RQ16/cv_results.json \
  -params=[formula='Theta~RAVLT+BVMT+RPM',n_folds=5,shuffle=True,random_state=42]
```
**Input:** CSV with data
**Output:** JSON with {'cv_r2_mean', 'cv_r2_sd', 'cv_r2_folds', 'shrinkage'}
**Parameters:**
- `formula`: Model formula
- `n_folds`: Number of folds
- `shuffle`: Boolean
- `random_state`: Random seed

**Used by RQs:** 7.16, 7.19

---

### 11.3 `permutation_test`
**Purpose:** Permutation test for any statistic
**CLI:**
```bash
python resampling.py \
  -function=permutation_test \
  -input=data/temp/theta_long.csv \
  -output=results/CH5/RQ4/permutation_test.json \
  -params=[statistic='linear_trend',group_col='Paradigm',n_permutations=10000]
```
**Input:** CSV with data
**Output:** JSON with {'observed_statistic', 'p', 'null_distribution': array as list}
**Parameters:**
- `statistic`: Name of test statistic function
- `group_col`: Column to permute
- `n_permutations`: Number of permutations

**Used by RQs:** 5.4 (optional)

---

## THEME 12: SPECIALIZED ANALYSIS TOOLS
**Module:** `specialized.py`

### 12.1 `test_linear_trend`
**Purpose:** Test monotonic ordering across ordered groups
**CLI:**
```bash
python specialized.py \
  -function=test_linear_trend \
  -input=results/CH5/RQ4/slopes_by_paradigm.csv \
  -output=results/CH5/RQ4/linear_trend_test.json \
  -params=[x_col='Paradigm',y_col='Slope',order=['Free','Cued','Recognition']]
```
**Input:** CSV with group variable and continuous outcome
**Output:** JSON with {'slope_of_trend', 'R²', 'p'}
**Parameters:**
- `x_col`: Grouping variable (ordered factor)
- `y_col`: Outcome variable
- `order`: List specifying group order

**Used by RQs:** 5.4

---

### 12.2 `compute_trajectory_dissociation`
**Purpose:** Test and quantify divergence between two trajectories
**CLI:**
```bash
python specialized.py \
  -function=compute_trajectory_dissociation \
  -input=results/CH6/RQ2/predictions.csv \
  -output=results/CH6/RQ2/dissociation_summary.json \
  -params=[measure1='Accuracy',measure2='Confidence',time_var='Days']
```
**Input:** CSV with predicted values for two measures over time
**Output:** JSON with {'dissociation': bool, 'direction': str, 'gap_trajectory': DataFrame as dict}
**Parameters:**
- `measure1`, `measure2`: Column names for two trajectories
- `time_var`: Time variable name

**Used by RQs:** 6.2

---

### 12.3 `decompose_forgetting_types`
**Purpose:** Classify item-level responses into forgetting types (RQ6.15)
**CLI:**
```bash
python specialized.py \
  -function=decompose_forgetting_types \
  -input=data/temp/item_level_responses.csv \
  -output=results/CH6/RQ15/forgetting_types.csv \
  -params=[accuracy_col='accuracy',confidence_col='confidence',baseline_day=0,later_day=6]
```
**Input:** CSV with item-level accuracy and confidence across days
**Output:** CSV with columns [Item, UID, Type] where Type = {Genuine_Remember, Lucky_Guess, Genuine_Forget, False_Memory}
**Parameters:**
- `accuracy_col`, `confidence_col`: Column names
- `baseline_day`, `later_day`: Days to compare

**Used by RQs:** 6.15

---

### 12.4 `variance_partitioning`
**Purpose:** Partition explained/unexplained variance with IRT reliability
**CLI:**
```bash
python specialized.py \
  -function=variance_partitioning \
  -input=results/CH7/RQ17/regression_model.pkl,results/All/TQ_corr_noroom_2cats_p1_med_data_ability.csv \
  -output=results/CH7/RQ17/variance_partition.json \
  -params=[]
```
**Input:** Two paths: pickled regression model, theta scores with SEs
**Output:** JSON with {'var_explained', 'var_error', 'var_true_residual', 'reliability', 'r2_corrected'}
**Parameters:** None

**Used by RQs:** 7.17

---

## THEME 13: UTILITY & ORCHESTRATION TOOLS
**Module:** `utils.py`

### 13.1 `save_results`
**Purpose:** Save analysis results to structured folder
**CLI:**
```bash
python utils.py \
  -function=save_results \
  -input=results/CH5/RQ1/ \
  -output=results/CH5/RQ1/ \
  -params=[results_dict_file='results/CH5/RQ1/temp_results.json',include_figures=True,include_models=True]
```
**Input:** Directory + JSON file with results dictionary
**Output:** Organized folder structure with saved files
**Parameters:**
- `results_dict_file`: Path to temporary JSON with results to save
- `include_figures`: Boolean
- `include_models`: Boolean

**Used by RQs:** All RQs (final step)

---

### 13.2 `generate_summary_table`
**Purpose:** Create publication-ready table
**CLI:**
```bash
python utils.py \
  -function=generate_summary_table \
  -input=results/CH5/RQ1/fixed_effects.csv \
  -output=results/CH5/RQ1/fixed_effects_formatted.md \
  -params=[format='markdown',round_digits=3,add_stars=True]
```
**Input:** CSV with results
**Output:** Formatted table file (markdown/latex/html)
**Parameters:**
- `format`: 'markdown', 'latex', 'html'
- `round_digits`: Decimal places
- `add_stars`: Boolean, add significance stars

**Used by RQs:** All RQs (reporting step)

---

### 13.3 `create_draft_writeup`
**Purpose:** Generate draft thesis text from results
**CLI:**
```bash
python utils.py \
  -function=create_draft_writeup \
  -input=results/CH5/RQ1/ \
  -output=results/CH5/RQ1/draft.md \
  -params=[rq_number='5.1',template='templates/rq_writeup_template.md']
```
**Input:** Results directory
**Output:** Markdown file with draft text
**Parameters:**
- `rq_number`: RQ identifier (e.g., '5.1')
- `template`: Optional template file path

**Used by RQs:** All RQs (final reporting step)

---

### 13.4 `bonferroni_correction`
**Purpose:** Apply Bonferroni correction to p-values
**CLI:**
```bash
python utils.py \
  -function=bonferroni_correction \
  -input=results/CH5/RQ1/fixed_effects.csv \
  -output=results/CH5/RQ1/fixed_effects_corrected.csv \
  -params=[p_col='p',alpha=0.05,n_tests=3]
```
**Input:** CSV with p-value column
**Output:** CSV with added 'p_corrected' and 'significant_corrected' columns
**Parameters:**
- `p_col`: P-value column name
- `alpha`: Family-wise error rate
- `n_tests`: Number of tests (for correction factor)

**Used by RQs:** All RQs with multiple comparisons

---

### 13.5 `format_p_value`
**Purpose:** Format p-values for publication
**CLI:**
```bash
python utils.py \
  -function=format_p_value \
  -input=results/CH5/RQ1/fixed_effects.csv \
  -output=results/CH5/RQ1/fixed_effects_formatted.csv \
  -params=[p_col='p',threshold=0.001,digits=3]
```
**Input:** CSV with p-value column
**Output:** CSV with added 'p_formatted' column
**Parameters:**
- `p_col`: P-value column name
- `threshold`: Minimum to report exactly (default=0.001)
- `digits`: Decimal places

**Used by RQs:** All RQs (reporting step)

---

### 13.6 `check_assumptions`
**Purpose:** Check regression/LMM assumptions
**CLI:**
```bash
python utils.py \
  -function=check_assumptions \
  -input=results/CH5/RQ1/model_linlog.pkl \
  -output=results/CH5/RQ1/assumptions/ \
  -params=[tests=['normality','homoscedasticity','multicollinearity']]
```
**Input:** Pickled model
**Output:** Directory with test results JSON + diagnostic plots
**Parameters:**
- `tests`: List of assumptions to check

**Used by RQs:** All RQs using regression/LMM (validation step)

---

### 13.7 `validate_output`
**Purpose:** Validate that analysis output matches expected structure
**CLI:**
```bash
python utils.py \
  -function=validate_output \
  -input=results/CH5/RQ1/fixed_effects.csv \
  -output=results/CH5/RQ1/validation_report.json \
  -params=[expected_columns=['Term','β','SE','p'],expected_n_rows=None,check_missing=True]
```
**Input:** Any CSV output file
**Output:** JSON validation report {'valid': bool, 'errors': list}
**Parameters:**
- `expected_columns`: List of required columns
- `expected_n_rows`: Expected row count (None=don't check)
- `check_missing`: Boolean, check for missing values

**Used by RQs:** All RQs (inspector agent uses this after each step)

---

## WORKFLOW SUMMARY

### Typical RQ Execution Sequence:

**Example: RQ 5.1 (Domain Forgetting Trajectories)**

```bash
# Step 1: Data Selection Agent prepares data
python data.py -generate_variables -analysis_set="All by Domain"

# Step 2: IRT Agent runs pipeline (if not already done)
python irt_tools.py -function=run_irt_pipeline \
  -input=data/master.xlsx \
  -output=results/All_by_Domain/TQ_corr_noroom_2cats_p1_med \
  -params=[analysis_set='All by Domain',factors=3,correlated_factors=True,categories=2,iteration_level='med']

# Step 3: Load theta scores
python data_prep.py -function=load_irt_theta_scores \
  -input=results/All_by_Domain/TQ_corr_noroom_2cats_p1_med_data_ability.csv \
  -output=results/CH5/RQ1/step1_theta_scores.csv \
  -params=[subset_columns=['Theta_What','Theta_Where','Theta_When']]

# Inspector validates output
python utils.py -function=validate_output \
  -input=results/CH5/RQ1/step1_theta_scores.csv \
  -output=results/CH5/RQ1/step1_validation.json \
  -params=[expected_columns=['UID','Test','Theta_What','Theta_Where','Theta_When'],check_missing=True]

# Step 4: Reshape to long
python data_prep.py -function=reshape_wide_to_long \
  -input=results/CH5/RQ1/step1_theta_scores.csv \
  -output=results/CH5/RQ1/step2_theta_long.csv \
  -params=[id_vars=['UID','Test','Days'],value_vars=['Theta_What','Theta_Where','Theta_When'],var_name='Domain',value_name='Theta']

# Step 5: Add time transformations
python data_prep.py -function=compute_time_transformations \
  -input=results/CH5/RQ1/step2_theta_long.csv \
  -output=results/CH5/RQ1/step3_theta_long_time.csv \
  -params=[transformations=['linear','quadratic','log']]

# Step 6: Fit multiple LMMs
python lmm_tools.py -function=fit_multiple_lmms \
  -input=results/CH5/RQ1/step3_theta_long_time.csv \
  -output=results/CH5/RQ1/step4_aic_comparison.csv \
  -params=[formulas=['Linear:Theta~Days*C(Domain,Treatment("What"))','LinLog:Theta~(Days+np.log(Days+1))*C(Domain,Treatment("What"))'],groups='UID',save_models=True,model_dir='results/CH5/RQ1/models/']

# Step 7: Extract fixed effects from best model
python lmm_tools.py -function=extract_lmm_fixed_effects \
  -input=results/CH5/RQ1/models/LinLog.pkl \
  -output=results/CH5/RQ1/step5_fixed_effects.csv

# Step 8: Compute Cohen's d
python effect_sizes.py -function=compute_cohens_d \
  -input=results/CH5/RQ1/step3_theta_long_time.csv \
  -output=results/CH5/RQ1/step6_cohens_d.csv \
  -params=[group_var='Domain',value_var='Theta',groups_to_compare=[['What','Where'],['What','When']]]

# Step 9: Generate trajectory plot
python visualization.py -function=plot_lmm_trajectory \
  -input=results/CH5/RQ1/step3_theta_long_time.csv,results/CH5/RQ1/predictions.csv \
  -output=results/CH5/RQ1/trajectory_plot.png \
  -params=[x_var='Days',y_var='Theta',group_var='Domain']

# Step 10: Create draft writeup
python utils.py -function=create_draft_writeup \
  -input=results/CH5/RQ1/ \
  -output=results/CH5/RQ1/draft.md \
  -params=[rq_number='5.1']
```

---

## EXIT CODES

All functions return standardized exit codes:
- **0**: Success
- **1**: General error
- **2**: Invalid input format
- **3**: Missing required parameters
- **4**: Convergence failure (models)
- **5**: Validation failure (assumptions violated)

Stderr contains error messages; stdout contains success messages.

---

**END OF DOCUMENT**
