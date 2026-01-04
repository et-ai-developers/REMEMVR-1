# Analysis Plan: RQ 7.6.2 - Does RAVLT Delayed predict REMEMVR slope?

**Research Question:** Does RAVLT forgetting (T5 - Delayed Recall) predict REMEMVR forgetting rate?
**Created:** 2026-01-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ tests whether short-term forgetting (RAVLT delay of 20-30 minutes) predicts long-term forgetting (REMEMVR slope over 6 days). Analysis correlates RAVLT forgetting index (T5Sc - DRSc) with REMEMVR per-participant slope values from Ch5 5.1.1 omnibus analysis. Includes both bivariate and partial correlations controlling for initial encoding levels.

The analysis pipeline uses correlation methods with cross-validation and bootstrap confidence intervals. No IRT or LMM modeling required - this is a correlation analysis between derived variables from existing sources.

**Pipeline:** Correlation analysis (bivariate and partial)
**Steps:** 8 total analysis steps
**Estimated Runtime:** Medium (30-60 minutes total)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + Bonferroni corrected)
- No D039 (no IRT analysis)
- No D069 (no trajectory plots)  
- No D070 (no LMM with TSVR)

---

## Analysis Plan

### Step 0: Load Participant Data

**Dependencies:** None (first step)
**Complexity:** Low (data loading only)

**Purpose:** Load participant demographic and cognitive test data from prepared dataset

**Input:**
- File: ./data/dfnonvr.csv (prepared participant dataset)
- Format: CSV with 100 rows (participants) x demographics/cognitive columns
- Required columns: UID, RAV_T5Sc, RAV_DRSc (RAVLT scores)
- Data types: UID (string), RAV_T5Sc (float), RAV_DRSc (float)

**Processing:**
- Load participant data using load_participant_data function
- Verify all 100 participants present with required RAVLT scores
- Check for missing values in T5Sc and DRSc columns

**Output:**
- File: data/step00_participant_data.csv
- Format: CSV with participant-level data
- Columns: UID, RAV_T5Sc, RAV_DRSc, plus other demographics
- Expected Rows: 100 participants

**Validation Requirement:**
Validation tools MUST be used after data loading tool execution. Specific validation tools will be determined by rq_tools based on data loading requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_participant_data.csv: 100 rows x minimum 3 columns (UID, RAV_T5Sc, RAV_DRSc)

*Value Ranges:*
- RAV_T5Sc in [0, 15] (RAVLT T5 word count range)
- RAV_DRSc in [0, 15] (RAVLT delayed recall word count range)  
- UID format: string participant identifiers

*Data Quality:*
- All 100 participants present (no data loss)
- No NaN values in RAV_T5Sc or RAV_DRSc columns
- No duplicate UIDs

*Log Validation:*
- Required: "Data loaded successfully: 100 participants"
- Forbidden: "ERROR", "Missing values in RAVLT"
- Acceptable warnings: None expected for data loading

### Step 1: Extract Cognitive Test Scores

**Dependencies:** Step 0 (requires participant data)  
**Complexity:** Low (data extraction only)

**Purpose:** Extract RAVLT scores and compute forgetting index

**Input:**
- File: data/step00_participant_data.csv (from Step 0)
- Required columns: UID, RAV_T5Sc, RAV_DRSc

**Processing:**
- Extract RAVLT scores using extract_cognitive_tests function
- Compute RAVLT_Forgetting = RAV_T5Sc - RAV_DRSc (higher = more forgetting)
- Standardize forgetting scores for effect size interpretation

**Output:**
- File: data/step01_ravlt_scores.csv
- Format: CSV with RAVLT data
- Columns: UID, RAV_T5Sc, RAV_DRSc, RAVLT_Forgetting, RAVLT_Forgetting_z
- Expected Rows: 100 participants

**Validation Requirement:**
Validation tools MUST be used after cognitive test extraction tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_ravlt_scores.csv: 100 rows x 5 columns (UID, RAV_T5Sc, RAV_DRSc, RAVLT_Forgetting, RAVLT_Forgetting_z)

*Value Ranges:*
- RAV_T5Sc in [0, 15]
- RAV_DRSc in [0, 15] 
- RAVLT_Forgetting in [-15, 15] (difference score range)
- RAVLT_Forgetting_z approximately in [-3, 3] (standardized)

*Data Quality:*
- All 100 participants present
- No NaN values in computed scores
- RAVLT_Forgetting_z has mean approximately 0, SD approximately 1

*Log Validation:*
- Required: "RAVLT scores extracted: 100 participants"
- Required: "Forgetting index computed successfully"
- Forbidden: "ERROR", "NaN values detected"

### Step 2: Extract REMEMVR Slopes

**Dependencies:** Step 1 (requires RAVLT data for merge validation)
**Complexity:** Medium (cross-RQ data extraction)

**Purpose:** Extract participant-specific slopes from Ch5 5.1.1 LMM results

**Input:**
- File: results/ch5/5.1.1/data/step05_lmm_model_summary.txt (LMM results from Ch5)
- Alternative: Use extract_random_effects_from_lmm function to get slopes directly

**Processing:**
- Extract random slopes (participant-specific forgetting rates) from LMM
- Use extract_random_effects_from_lmm function 
- Ensure slopes represent individual differences in forgetting rate

**Output:**
- File: data/step02_rememvr_slopes.csv  
- Format: CSV with slope data
- Columns: UID, REMEMVR_Slope, REMEMVR_Intercept
- Expected Rows: 100 participants

**Validation Requirement:**
Validation tools MUST be used after slope extraction tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_rememvr_slopes.csv: 100 rows x 3 columns (UID, REMEMVR_Slope, REMEMVR_Intercept)

*Value Ranges:*
- REMEMVR_Slope in [-2, 0] (negative slopes expected for forgetting)
- REMEMVR_Intercept in [-2, 2] (IRT ability scale)

*Data Quality:*
- All 100 participants present
- No NaN values in slope estimates
- No duplicate UIDs

*Log Validation:*
- Required: "Random effects extracted: 100 participants"
- Forbidden: "ERROR", "Missing slopes"

### Step 3: Merge Analysis Dataset

**Dependencies:** Steps 1, 2 (requires both RAVLT and slope data)
**Complexity:** Low (data merging only)

**Purpose:** Create complete analysis dataset merging RAVLT and REMEMVR data

**Input:**
- File: data/step01_ravlt_scores.csv (RAVLT data)
- File: data/step02_rememvr_slopes.csv (slope data)

**Processing:**
- Merge datasets on UID
- Verify all participants have both RAVLT and slope data
- Create final analysis dataset

**Output:**
- File: data/step03_analysis_input.csv
- Format: CSV with merged data
- Columns: UID, RAV_T5Sc, RAV_DRSc, RAVLT_Forgetting, RAVLT_Forgetting_z, REMEMVR_Slope, REMEMVR_Intercept
- Expected Rows: 100 participants

**Validation Requirement:**
Validation tools MUST be used after data merging tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_analysis_input.csv: 100 rows x 7 columns (complete merged dataset)

*Value Ranges:*
- All ranges as specified in Steps 1-2

*Data Quality:*
- All 100 participants present (no data loss in merge)
- No NaN values in any analysis columns
- UIDs unique

*Log Validation:*
- Required: "Data merged successfully: 100 participants"
- Forbidden: "ERROR", "Merge failed"

### Step 4: Compute Bivariate Correlation

**Dependencies:** Step 3 (requires merged analysis dataset)
**Complexity:** Medium (correlation with bootstrap CI)

**Purpose:** Test primary hypothesis - correlation between RAVLT forgetting and REMEMVR slope

**Input:**
- File: data/step03_analysis_input.csv (merged dataset)
- Variables: RAVLT_Forgetting, REMEMVR_Slope

**Processing:**
- Compute Pearson correlation using bootstrap_correlation_ci function
- Random seed = 42, bootstrap iterations = 1000
- Calculate 95% confidence interval
- Apply Decision D068: Report BOTH uncorrected AND Bonferroni-corrected p-values
- Bonferroni correction factor: 28 (total Chapter 7 primary hypotheses)

**Output:**
- File: data/step04_bivariate_correlation.csv
- Format: CSV with correlation results
- Columns: correlation, CI_lower, CI_upper, p_uncorrected, p_bonferroni, N
- Expected Rows: 1 (single correlation)

**Validation Requirement:**
Validation tools MUST be used after correlation analysis tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_bivariate_correlation.csv: 1 row x 6 columns (correlation results)

*Value Ranges:*
- correlation in [-1, 1] (correlation coefficient bounds)
- CI_lower in [-1, 1], CI_upper in [-1, 1]
- p_uncorrected in [0, 1], p_bonferroni in [0, 1] 
- N = 100

*Data Quality:*
- No NaN values in correlation results
- CI_lower <= correlation <= CI_upper
- p_bonferroni = p_uncorrected x 28 (Decision D068 correction)

*Log Validation:*
- Required: "Bootstrap correlation complete: 1000 iterations"
- Required: "Dual p-values computed" (Decision D068)
- Forbidden: "ERROR", "Correlation failed"

### Step 5: Compute Partial Correlation

**Dependencies:** Step 4 (requires bivariate results for comparison)
**Complexity:** Medium (partial correlation analysis)

**Purpose:** Test secondary hypothesis - correlation controlling for initial encoding levels

**Input:**
- File: data/step03_analysis_input.csv (merged dataset)
- Variables: RAVLT_Forgetting, REMEMVR_Slope (primary)
- Controls: RAV_T5Sc, REMEMVR_Intercept (encoding levels)

**Processing:**
- Compute partial correlation controlling for encoding variables
- Use compute_pearson_correlations_with_correction function for dual p-values
- Apply same bootstrap procedure (seed=42, iterations=1000)
- Decision D068: Report uncorrected and Bonferroni-corrected p-values

**Output:**
- File: data/step05_partial_correlation.csv
- Format: CSV with partial correlation results  
- Columns: partial_r, CI_lower, CI_upper, p_uncorrected, p_bonferroni, N
- Expected Rows: 1 (single partial correlation)

**Validation Requirement:**
Validation tools MUST be used after partial correlation analysis tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_partial_correlation.csv: 1 row x 6 columns (partial correlation results)

*Value Ranges:*
- partial_r in [-1, 1]
- CI bounds in [-1, 1] 
- p-values in [0, 1]
- N = 100

*Data Quality:*
- No NaN values
- CI_lower <= partial_r <= CI_upper
- Dual p-values present (Decision D068)

*Log Validation:*
- Required: "Partial correlation computed successfully"
- Required: "Dual p-values reported"
- Forbidden: "ERROR", "Computation failed"

### Step 6: Model Diagnostics

**Dependencies:** Step 5 (requires correlation results)
**Complexity:** Medium (assumption testing)

**Purpose:** Check correlation assumptions and identify potential issues

**Input:**
- File: data/step03_analysis_input.csv (for diagnostic plots)
- Variables: RAVLT_Forgetting, REMEMVR_Slope

**Processing:**
- Test linearity assumption (scatterplot inspection)
- Test normality (Kolmogorov-Smirnov tests)
- Identify outliers using Cook's D < 4/N = 0.04 threshold
- Test homoscedasticity
- Generate diagnostic plots

**Output:**
- File: data/step06_diagnostics.csv
- Format: CSV with diagnostic results
- Columns: test_type, statistic, p_value, conclusion
- Expected Rows: Multiple (one per diagnostic test)

**Validation Requirement:**
Validation tools MUST be used after diagnostic analysis tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_diagnostics.csv: Multiple rows x 4 columns (diagnostic results)

*Value Ranges:*
- statistic values depend on test type
- p_value in [0, 1]
- conclusion: categorical text

*Data Quality:*
- All diagnostic tests completed
- No NaN values in test statistics
- Clear Pass/Fail conclusions

*Log Validation:*
- Required: "Diagnostic tests completed"
- Required: "Assumptions checked"
- Forbidden: "ERROR", "Test failed to run"

### Step 7: Cross-Validation Analysis

**Dependencies:** Step 6 (requires diagnostic results)
**Complexity:** Medium (bootstrap resampling)

**Purpose:** Assess stability of correlation estimates through resampling

**Input:**
- File: data/step03_analysis_input.csv (merged dataset)

**Processing:**
- Bootstrap resampling stability analysis (1000 iterations, seed=42)
- Sensitivity analysis: exclude outliers identified in Step 6, recompute
- Compare Pearson vs Spearman if normality violated
- Generate stability metrics

**Output:**
- File: data/step07_bootstrap_results.csv
- Format: CSV with bootstrap stability results
- Columns: metric, mean_estimate, CI_lower, CI_upper, stability_index
- Expected Rows: Multiple (one per stability metric)

**Validation Requirement:**
Validation tools MUST be used after cross-validation analysis tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_bootstrap_results.csv: Multiple rows x 5 columns

*Value Ranges:*
- mean_estimate in [-1, 1] for correlations
- CI bounds in [-1, 1]
- stability_index in [0, 1] (higher = more stable)

*Data Quality:*
- Bootstrap completed with 1000 iterations  
- No NaN values in stability estimates
- Confidence intervals well-formed

*Log Validation:*
- Required: "Bootstrap analysis complete: 1000 iterations"
- Required: "Stability metrics computed"
- Forbidden: "ERROR", "Resampling failed"

### Step 8: Effect Size and Power Analysis

**Dependencies:** Step 7 (requires final correlation estimates)
**Complexity:** Medium (power calculations)

**Purpose:** Interpret effect size magnitude and assess statistical power

**Input:**
- File: data/step04_bivariate_correlation.csv (primary correlation)
- File: data/step05_partial_correlation.csv (partial correlation)

**Processing:**
- Interpret effect sizes using Cohen's guidelines (r = 0.10 small, 0.30 medium, 0.50 large)
- Post-hoc power analysis for observed effect sizes
- Sensitivity analysis: smallest detectable correlation at 80% power with N=100
- Compare to encoding-to-encoding correlations from RQ 7.1.1 if available

**Output:**
- File: data/step08_power_analysis.csv
- Format: CSV with power analysis results
- Columns: analysis_type, effect_size, power, min_detectable_r, interpretation  
- Expected Rows: 2 (bivariate and partial correlations)

**Validation Requirement:**
Validation tools MUST be used after power analysis tool execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_power_analysis.csv: 2 rows x 5 columns

*Value Ranges:*
- effect_size in [-1, 1] 
- power in [0, 1]
- min_detectable_r in [0, 1]
- interpretation: categorical text

*Data Quality:*
- Power analysis completed for both correlations
- No NaN values in power estimates
- Interpretations consistent with effect size guidelines

*Log Validation:*
- Required: "Power analysis completed"
- Required: "Effect size interpretation generated"
- Forbidden: "ERROR", "Power calculation failed"

---

## Expected Data Formats

### Primary Analysis Variables

**RAVLT_Forgetting:**
- Computation: RAV_T5Sc - RAV_DRSc  
- Interpretation: Higher values = more forgetting
- Range: [-15, 15] (theoretical range)
- Distribution: Expected approximately normal

**REMEMVR_Slope:**
- Source: Random slopes from Ch5 5.1.1 LMM
- Interpretation: Rate of forgetting over 6 days
- Range: [-2, 0] (negative slopes expected)
- Units: Theta change per day

**Control Variables:**
- RAV_T5Sc: RAVLT Trial 5 score (initial encoding)
- REMEMVR_Intercept: Initial REMEMVR ability level

### Data Transformation Pipeline

**Step 0 -> Step 1:**
- Format: Wide participant data (no transformation)
- Key: UID (participant identifier)

**Step 1 -> Step 2:**
- Format: Add computed RAVLT forgetting variables
- New columns: RAVLT_Forgetting, RAVLT_Forgetting_z

**Step 2 -> Step 3:**
- Format: Merge operation (left join on UID)
- Combine: RAVLT data + REMEMVR slope data

**Step 3 -> Steps 4-8:**
- Format: Analysis-ready dataset (no further transformation)
- Use: Direct input to correlation functions

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQs

**This RQ requires outputs from:**
- **RQ 5.1.1** (General Functional Form Analysis)
  - File: results/ch5/5.1.1/data/step05_lmm_model_summary.txt
  - Alternative: Use extract_random_effects_from_lmm on fitted LMM model
  - Used in: Step 2 (extract participant-specific slopes)
  - Rationale: RQ 5.1.1 establishes omnibus forgetting trajectories with participant-specific random slopes. This RQ correlates those individual slope estimates with RAVLT forgetting.

**Execution Order Constraint:**
1. RQ 5.1.1 must complete through Step 5 (LMM fitting with random slopes)
2. This RQ can execute once random slopes available

**Data Source Boundaries:**
- **DERIVED data:** REMEMVR slopes from RQ 5.1.1 LMM random effects  
- **RAW data:** RAVLT scores from ./data/dfnonvr.csv (prepared cognitive dataset)

**Validation:**
- Step 2: Check RQ 5.1.1 completion status (rq_results: success required)
- If dependency missing -> quit with error -> user must execute RQ 5.1.1 first

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This prevents correlation analysis errors from cascading through interpretation and plotting steps. Per v4.X architecture, validation failures trigger immediate error handling and g_debug invocation.

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will specify BOTH analysis tool + validation tool per step
- rq_analysis (Step 12 workflow) will embed validation tool calls in analysis recipes  
- g_code (Step 14 workflow) will generate scripts with validation function calls
- bash execution will run analysis -> validation -> error on validation failure

### Validation Requirements By Step

#### Step 0: Load Participant Data
**Analysis Tool:** load_participant_data
**Validation Focus:** Data loading completeness, required columns present, participant count

#### Step 1: Extract Cognitive Test Scores  
**Analysis Tool:** extract_cognitive_tests
**Validation Focus:** RAVLT score ranges, computed variables, standardization

#### Step 2: Extract REMEMVR Slopes
**Analysis Tool:** extract_random_effects_from_lmm  
**Validation Focus:** Slope extraction success, value ranges, participant matching

#### Step 3: Merge Analysis Dataset
**Analysis Tool:** pandas merge operations
**Validation Focus:** Merge completeness, no data loss, UIDs matched

#### Step 4: Compute Bivariate Correlation
**Analysis Tool:** bootstrap_correlation_ci
**Validation Focus:** Correlation bounds, bootstrap completion, dual p-values (D068)

#### Step 5: Compute Partial Correlation  
**Analysis Tool:** compute_pearson_correlations_with_correction
**Validation Focus:** Partial correlation validity, control variable effects, dual p-values

#### Step 6: Model Diagnostics
**Analysis Tool:** assumption testing functions
**Validation Focus:** Diagnostic test completion, outlier identification, assumption results

#### Step 7: Cross-Validation Analysis
**Analysis Tool:** bootstrap_correlation_ci (stability)
**Validation Focus:** Bootstrap stability, resampling success, sensitivity analysis

#### Step 8: Effect Size and Power Analysis
**Analysis Tool:** power analysis functions  
**Validation Focus:** Power calculation validity, effect size interpretation, detectability

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message
- Log failure to logs/stepNN_name.log  
- Quit script immediately (do NOT proceed to next step)
- g_debug invoked by master to diagnose root cause

---

## Summary

**Total Steps:** 8 (plus Step 0 extraction = 9 total)
**Estimated Runtime:** 30-60 minutes (Medium complexity overall)
**Cross-RQ Dependencies:** RQ 5.1.1 (REMEMVR slopes required)
**Primary Outputs:** Bivariate and partial correlations with bootstrap CIs and dual p-values
**Validation Coverage:** 100% (all 9 steps have validation requirements)

**Key Statistical Features:**
- Bootstrap confidence intervals (1000 iterations, seed=42)
- Dual p-value reporting per Decision D068
- Partial correlation controlling for encoding levels
- Comprehensive assumption testing and diagnostics
- Power analysis and effect size interpretation

**Expected Results:**
- Weak positive correlation between RAVLT and REMEMVR forgetting (r ~ 0.15, p ~ 0.14)
- Partial correlation weaker than bivariate after controlling for encoding
- Adequate power for medium effects but limited for small effects with N=100

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml  
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2026-01-04): Initial plan created by rq_planner agent