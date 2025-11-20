# RQ X.Y: [Research Question Title]

**Last Updated:** YYYY-MM-DD HH:MM
**Chapter:** X
**RQ Number:** Y

---

<!--
IMPORTANT: UNIVERSAL TEMPLATE
This template shows IRT + LMM pipeline as an EXAMPLE only
Adapt sections based on your RQ's analysis type:
- IRT: Item Response Theory (ability estimates)
- LMM: Linear Mixed Models (trajectories, longitudinal)
- CTT: Classical Test Theory (reliability, item analysis)
- Correlation: Pearson/Spearman correlations
- ANOVA: Between/within-subjects designs
- Regression: Linear/logistic regression
- Descriptive: Descriptive statistics only

Delete irrelevant sections and adapt Method/Validation/Plots accordingly
-->

---

## Status

| **Phase** | **Status** | **Score** | **Date** |
|-----------|-----------|----------|----------|
| Specification | complete / in_progress / not_started | - | YYYY-MM-DD |
| Scholar Validation | passed / failed / not_started | 9.5/10 | YYYY-MM-DD |
| Statistics Validation | passed / failed / not_started | 9.3/10 | YYYY-MM-DD |
| Safety Audit | proceed / block / not_started | - | YYYY-MM-DD |
| Data Preparation | success / failure / not_started | - | YYYY-MM-DD |
| Output Verification | clean / contaminated / not_started | - | YYYY-MM-DD |
| Analysis Execution | success / failure / not_started | - | YYYY-MM-DD |
| Results Validation | complete / not_started | - | YYYY-MM-DD |

**Notes:** [Any critical issues, decisions, or blockers]

---

## 1. Research Question

[Verbatim research question from thesis]

**Example:**
Are there domain-specific differences in the rate and pattern of episodic forgetting over 6 days?

---

## 2. Hypotheses

[Expected outcomes with theoretical grounding]

**Hypothesis 1:** [Main hypothesis]
- **Theoretical Basis:** [Theory name and key principle]
- **References:** [Citations provided by scholar-agent]

**Hypothesis 2:** [Secondary hypothesis, if applicable]
- **Theoretical Basis:** [Theory name and key principle]
- **References:** [Citations provided by scholar-agent]

**Example:**
**Hypothesis 1:** Person items will show slower forgetting than Place items
- **Theoretical Basis:** Self-reference effect and schema congruence theory suggest person-related information benefits from richer encoding and stronger consolidation
- **References:**
  - Symons & Johnson (1997) - Self-reference effect enhances episodic memory encoding
  - Maguire et al. (2016) - Schema congruence predicts long-term retention in spatial memory tasks

---

## 3. Input Data

**Purpose:** Executable specifications for data-prep agent

### A. Data Sources (RAW DATA ONLY - Extractable from master.xlsx)

**Primary Source:** master.xlsx

**Variables Required:**

| **Variable** | **Tag(s) in master.xlsx** | **Description** | **Type** |
|-------------|--------------------------|-----------------|----------|
| UID | UID | Participant identifier | string |
| Test | Test | Test session (1-4) | int |
| VR_Person_T1 | RVR-i1PO-T1, RVR-i2PO-T1, ..., RVR-i9PO-T1 | VR Person items Test 1 | binary (0/1) |
| VR_Place_T1 | RVR-i10PL-T1, RVR-i11PL-T1, ..., RVR-i18PL-T1 | VR Place items Test 1 | binary (0/1) |
| [Continue for all tests and domains] | | | |

**Tag Format Rules:**
- Pattern: `RVR-{item_code}-T{test}`
- Item codes from docs/data_structure.md
- Tests: T1, T2, T3, T4
- Dichotomous scoring: 1 = correct, 0 = incorrect/missing

**Filters:**
- Exclude participants with <3 test sessions
- Exclude items with >70% missing values across all participants

**Expected Dimensions:**
- **Rows:** 400 (100 participants × 4 tests)
- **Columns:** 37 (1 UID + 1 Test + 9 Person items + 9 Place items + 9 Object items + 8 covariates)
- **File Size:** ~25-35 KB CSV

### B. Files Data-Prep Should Create

| **Filename** | **Purpose** | **Companion Doc** |
|-------------|-----------|-------------------|
| irt_input.csv | RAW VR items in wide format for IRT calibration | irt_input.md |

### C. Files Data-Prep Should NOT Create

❌ **theta_scores.csv** - Derived from IRT (created by analysis-executor in Step 2)
❌ **lmm_input.csv** - Derived from theta scores (created by analysis-executor in Step 3)
❌ Any file containing IRT/LMM outputs

---

## 4. Method

**Purpose:** Tool-by-tool procedure for analysis-executor agent

### Step 1: IRT Calibration (Primary Analysis)

**Input:** data/irt_input.csv

**Tool:** `tools.analysis_irt.calibrate_grm()`

**Parameters:** (see config.yaml for exact values)
- Model: 2PL-C (two-parameter logistic, constrained)
- Dimensions: 3 (Person, Place, Object)
- Purification: 2-pass with thresholds |b|>3.0, a<0.4
- Estimation: IWAVE algorithm via deepirtools

**Process:**
1. Load irt_input.csv
2. Pass 1: Calibrate 2PL-C model with all items
3. Flag items exceeding thresholds (|b|>3.0 OR a<0.4)
4. Pass 2: Re-calibrate without flagged items
5. Extract theta scores for all participants × tests × dimensions

**Outputs:**
- data/item_parameters.csv (item discrimination a, difficulty b, flagged status)
- data/item_parameters.md (companion documentation)
- data/theta_scores.csv (ability estimates for each participant × test × dimension)
- data/theta_scores.md (companion documentation)

**Quality Checks:**
- Verify convergence (max iterations <200, gradient <0.001)
- Check item parameter ranges: 0.4 ≤ a ≤ 3.0, -3.0 ≤ b ≤ 3.0
- Document flagged items (expect 5-15% flagging rate)

---

### Step 2: Data Reshaping (Data Preparation for LMM)

**Input:** data/theta_scores.csv

**Tool:** `tools.data.reshape_wide_to_long()`

**Parameters:** (see config.yaml)
- ID variable: UID
- Time variable: Test (1-4)
- Value variables: Theta_Person, Theta_Place, Theta_Object

**Process:**
1. Load theta_scores.csv (wide format: 1 row per participant × test)
2. Reshape to long format: 1 row per participant × test × domain
3. Create domain factor variable (Person, Place, Object)
4. Add session timing variable (Day: 0, 0, 1, 7)

**Outputs:**
- data/lmm_input.csv (long format for LMM analysis)
- data/lmm_input.md (companion documentation)

**Expected Dimensions:**
- **Rows:** 1,200 (100 participants × 4 tests × 3 domains)
- **Columns:** 4 (UID, Test, Domain, Theta, Day)

---

### Step 3: Linear Mixed Model Analysis (Trajectory Analysis)

**Input:** data/lmm_input.csv

**Tool:** `tools.analysis_lmm.fit_lmm()`

**Parameters:** (see config.yaml for exact formula)
- Formula: `Theta ~ Domain * Day + (1 + Day | UID)`
- Fixed effects: Domain (3 levels), Day (continuous), Domain×Day interaction
- Random effects: Random intercept + random slope for Day
- Estimation: REML via statsmodels.MixedLM

**Process:**
1. Load lmm_input.csv
2. Fit LMM with random intercepts and slopes
3. Extract fixed effect coefficients (Domain, Day, Domain×Day)
4. Calculate effect sizes (Cohen's f² for interaction)
5. Generate predictions for plotting

**Outputs:**
- data/lmm_coefficients.csv (fixed effects with SE, t, p-values)
- data/lmm_coefficients.md (companion documentation)
- data/lmm_random_effects.csv (participant-level intercepts and slopes)
- data/lmm_random_effects.md (companion documentation)

**Quality Checks:**
- Verify model convergence
- Check residual normality (Q-Q plot, Shapiro-Wilk test)
- Check homoscedasticity (residuals vs fitted plot)
- Calculate ICC (intraclass correlation)

---

### Step 4: Sensitivity Analysis (Robustness Check)

[Optional step if specified in RQ]

---

## 5. Validation

**Purpose:** Validation procedures + results (analysis-executor appends results after execution)

### Validation Procedures (For Analysis-Executor)

**IRT Assumptions:**
- **Local Independence:** Calculate Q3 statistic for all item pairs (threshold <0.2)
- **Unidimensionality:** Check eigenvalue ratio (1st/2nd eigenvalue >3.0)
- **Model Fit:** Calculate M2 statistic with RMSEA (<0.08) and CFI (>0.95)
- **Item Fit:** Calculate S-X² for each item (p > 0.01 after Bonferroni correction)

**LMM Assumptions:**
- **Residual Normality:** Shapiro-Wilk test (p > 0.05) + Q-Q plot
- **Homoscedasticity:** Levene's test (p > 0.05) + residuals vs fitted plot
- **Independence:** Durbin-Watson statistic (1.5-2.5)
- **Linearity:** Check Day effect via polynomial comparisons (linear vs quadratic)

**Effect Size Thresholds:**
- Cohen's f² for Domain×Day interaction: small (0.02), medium (0.15), large (0.35)
- Only interpret interactions with f² ≥ 0.02

---

### Validation Results (Appended by Analysis-Executor)

[Analysis-executor writes validation results here after Step 8]

**IRT Validation Results:**
- [Results of Q3, eigenvalue ratio, M2, S-X² tests]
- [Any assumption violations and how they were handled]

**LMM Validation Results:**
- [Results of Shapiro-Wilk, Levene's, Durbin-Watson tests]
- [Plots: Q-Q plot, residuals vs fitted]
- [Any assumption violations and how they were handled]

**Effect Sizes:**
- Domain×Day interaction: f² = [value], 95% CI [lower, upper]
- Interpretation: [small/medium/large effect]

---

## 6. Plots

**Purpose:** Specifications for plotting agent (future implementation) or analysis-executor

### Plot 1: Item Characteristic Curves (IRT)

**Type:** ICC plot (Item Characteristic Curves)
**Tool:** `tools.plotting.plot_icc()`
**Input:** data/item_parameters.csv
**Output:** plots/irt_icc_by_domain.png, plots/irt_icc_by_domain_data.csv
**Specifications:**
- 3 subplots (Person, Place, Object domains)
- X-axis: Theta (ability) from -3 to +3
- Y-axis: P(correct) from 0 to 1
- Lines: One curve per item (color by discrimination parameter a)
- Annotations: Flag items with difficulty |b|>3.0 or discrimination a<0.4

---

### Plot 2: Forgetting Trajectories (LMM)

**Type:** Line plot with 95% CI ribbons
**Tool:** `tools.plotting.plot_lmm_trajectories()`
**Input:** data/lmm_coefficients.csv + data/lmm_input.csv (for observed data)
**Output:** plots/lmm_trajectories_by_domain.png, plots/lmm_trajectories_by_domain_data.csv
**Specifications:**
- X-axis: Day (0, 0, 1, 7) - note two Test 1 sessions on Day 0
- Y-axis: Theta (ability estimate)
- Lines: 3 trajectories (Person, Place, Object) with 95% CI ribbons
- Points: Observed means (semi-transparent) overlaid on predicted trajectories
- Annotations: Mark significant Domain×Day interaction if p<0.05

---

### Plot 3: Random Effects Distribution (LMM)

**Type:** Scatter plot with marginal histograms
**Tool:** `tools.plotting.plot_random_effects()`
**Input:** data/lmm_random_effects.csv
**Output:** plots/lmm_random_effects.png, plots/lmm_random_effects_data.csv
**Specifications:**
- X-axis: Random intercept (baseline ability)
- Y-axis: Random slope (forgetting rate)
- Points: One per participant, color by domain
- Marginal histograms: Distribution of intercepts (top) and slopes (right)
- Annotations: Identify outliers (>3 SD from mean)

---

## 7. Statistical Audit Number 2

**Purpose:** Placeholder for post-analysis statistics-expert validation

[Statistics-expert agent appends second validation report here after analysis complete]

**Second Audit Date:** YYYY-MM-DD
**Validator:** statistics_expert agent
**Audit Scope:**
- Verify IRT convergence and item flagging procedures
- Check LMM assumption testing completeness
- Validate effect size calculations
- Confirm interpretation aligns with results

**Findings:**
[Statistics-expert writes findings here]

**Recommendations:**
[Statistics-expert writes recommendations here]

**Approval Status:** approved / conditional / rejected
**Conditions (if any):**
[List any required changes before results can be used]

---

## 8. Results

**Purpose:** Summary of findings (added by results-inspector agent)

[Results-inspector agent writes comprehensive results here after Step 9]

### IRT Results

**Item Parameters:**
- [Summary of discrimination and difficulty by domain]
- [Flagged items and purification results]

**Theta Scores:**
- [Descriptive statistics by domain and test]
- [Distribution characteristics]

---

### LMM Results

**Fixed Effects:**

| **Effect** | **Coefficient** | **SE** | **t** | **p** | **95% CI** |
|-----------|----------------|--------|-------|-------|------------|
| Intercept | | | | | |
| Domain_Place | | | | | |
| Domain_Object | | | | | |
| Day | | | | | |
| Domain_Place × Day | | | | | |
| Domain_Object × Day | | | | | |

**Random Effects:**
- Intercept variance: [value] (SD = [value])
- Slope variance: [value] (SD = [value])
- Intercept-Slope correlation: [value]

**Model Fit:**
- AIC: [value]
- BIC: [value]
- Log-likelihood: [value]
- ICC: [value]

**Effect Sizes:**
- Domain×Day interaction: f² = [value], 95% CI [lower, upper]
- Interpretation: [small/medium/large]

---

### Answer to Research Question

[1-2 paragraph scholarly answer to the RQ]

**Example:**
Yes, there are significant domain-specific differences in forgetting trajectories over 6 days (Domain×Day: β = [value], p = [p-value], f² = [value]). Person items showed slower forgetting (slope = [value]) compared to Place items (slope = [value]) and Object items (slope = [value]). This pattern supports the self-reference effect hypothesis, suggesting that person-related episodic memories benefit from richer encoding and stronger consolidation processes.

---

## 9. Theoretical Implications

**Purpose:** Broader interpretation (added by scholar agent after verified results)

[Scholar agent writes theoretical implications here after results validated]

**Date:** YYYY-MM-DD
**Validator:** scholar agent

### Alignment with Episodic Memory Theory

[How results support or challenge existing theories]

### Contribution to Literature

[What new insights these results provide]

### Implications for REMEMVR Assessment Tool

[How findings inform the clinical/research application]

### Future Research Directions

[Open questions raised by results]

### References

[Full citations for all theoretical frameworks mentioned]

---

**End of RQ Specification**
