# RQ 7.4.2: BVMT predicts Where more than What

**Chapter:** 7
**Type:** Process-Specific Prediction
**Subtype:** Domain-Specific Prediction
**Full ID:** 7.4.2

---

## Research Question

**Primary Question:**
Does BVMT (visuospatial memory test) show stronger prediction for Where (spatial location) than What (object identity)?

**Scope:**
This RQ examines domain-specificity in cognitive test prediction using bivariate correlations between BVMT Total Recall (BVMT_TotR) and REMEMVR theta scores for Where and What domains. Analysis includes 100 participants with mean theta scores derived from Ch5 domain-specific analyses (5.2.x). Uses Steiger's Z-test to compare dependent correlations with hypothesis r(BVMT, Where) > r(BVMT, What).

**Theoretical Framing:**
Tests domain-specificity hypothesis that visuospatial tests should preferentially predict visuospatial memory domains. BVMT requires spatial configuration memory which should transfer to REMEMVR Where domain more than What domain, which may rely more on verbal encoding.

---

## Theoretical Background

**Relevant Theories:**
- **Domain-Specificity Theory**: Cognitive abilities show domain-specific transfer where visuospatial tests predict visuospatial memory performance more than verbal/semantic memory
- **Dual-Coding Theory** (Paivio, 1986): Spatial information (Where) processed in visuospatial system while object identity (What) may engage both verbal and visual codes
- **Transfer-Appropriate Processing**: Performance is enhanced when the cognitive processes required during testing match those required during encoding/retrieval

**Key Citations:**

**Theoretical Predictions:**
BVMT requires spatial configuration memory, visual pattern recognition, and spatial working memory. These processes should overlap more with REMEMVR Where domain (spatial location memory) than What domain (object identity), leading to stronger correlation with Where.

**Literature Gaps:**
Domain-specificity in episodic memory prediction using immersive VR paradigms has been understudied. Most research examines global memory measures rather than domain-specific transfer.

---

## Hypothesis

**Primary Hypothesis:**
r(BVMT, Where) > r(BVMT, What). BVMT requires spatial configuration memory, which should transfer to REMEMVR Where domain more strongly than What domain.

**Secondary Hypotheses:**
Both correlations expected to be positive and significant, but the difference in magnitude demonstrates domain-specific transfer.

**Theoretical Rationale:**
BVMT and REMEMVR Where domain both require spatial memory processes including visual pattern recognition, spatial configuration memory, and spatial working memory. What domain may rely more on verbal labeling and semantic memory, showing weaker correlation with visuospatial BVMT.

**Expected Effect Pattern:**
Expected: r(BVMT, Where) = 0.42, r(BVMT, What) = 0.28. Steiger's Z-test should show significant difference (p < 0.05) supporting domain-specificity hypothesis.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object naming/identity memory from Ch5 domain-specific theta scores

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)  
  - [x] `-D-` tags (put-down location)
  - Description: Spatial location memory aggregated across location subtypes

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Not examined in this RQ

**Inclusion Rationale:**
Examines What vs Where domains to test domain-specificity of visuospatial prediction. Where domain includes all spatial location subtypes (general, pick-up, put-down) as they all require spatial memory processes theoretically related to BVMT.

**Exclusion Rationale:**
When domain excluded as this RQ specifically tests spatial (Where) vs object (What) domain-specificity. Temporal order may engage different cognitive processes not central to visuospatial domain-specificity hypothesis.

---

## Analysis Approach

**Analysis Type:**
Bivariate correlation analysis with dependent correlations comparison (Steiger's Z-test)

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load Where and What theta scores from Ch5 5.2.x domain analyses
- Extract BVMT_TotR scores from master.xlsx
- Compute mean theta scores per participant per domain
- Check data quality and missing values

**Step 2:** Compute bivariate correlations
- r1 = cor(BVMT_TotR, Mean_Theta_Where)  
- r2 = cor(BVMT_TotR, Mean_Theta_What)
- Report correlation coefficients with 95% confidence intervals

**Step 3:** Test domain-specificity hypothesis
- Steiger's Z-test for dependent correlations: H1: r1 > r2
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Chapter-level alpha = 0.00179
- Secondary: FDR correction for comparison

**Step 4:** Effect sizes and descriptive statistics
- Cohen's d for correlation difference
- Descriptive statistics for all variables
- Semi-partial correlations for unique variance

**Step 5:** Model diagnostics
- Check assumptions: normality, linearity, homoscedasticity
- Identify potential outliers and influential points
- Bootstrap confidence intervals (1000 iterations)

**Step 6:** Visualization
- Scatter plots with regression lines for both correlations
- Visual comparison of slopes
- Difference in correlations clearly apparent

**Step 7:** Sensitivity analyses
- Exclude potential outliers, rerun analysis
- Alternative BVMT scoring (if available)
- Robustness check with different correlation methods

**Expected Outputs:**
- data/step01_domain_theta_scores.csv (Where and What means per participant)
- data/step02_bvmt_scores.csv (BVMT_TotR per participant)
- data/step03_analysis_input.csv (merged dataset for analysis)
- data/step04_correlation_results.csv (correlation coefficients, CIs, dual p-values)
- data/step05_steiger_test.csv (dependent correlation comparison results)
- data/step06_effect_sizes.csv (Cohen's d, bootstrap CIs)
- data/step07_sensitivity_analysis.csv (robustness checks)
- results/domain_specificity_summary.md (text summary for thesis)
- plots/domain_specificity_scatterplots.png (correlation visualization)

**Success Criteria:**
- Both correlations significant at uncorrected alpha
- r_Where > r_What in expected direction
- Steiger's Z-test p-value reported (significance not required)
- Effect sizes with confidence intervals calculated
- Visual difference in slopes apparent in scatter plots
- Assumptions checked and reported
- Sensitivity analyses confirm main findings

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.2.x domain outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.2.x (Domain-specific analyses - What/Where/When)

**File Paths:**
- results/ch5/5.2.1/data/step03_theta_scores.csv (or appropriate domain RQ)
- results/ch5/5.2.2/data/step03_theta_scores.csv (if separate What/Where analyses)
- data/cache/master.xlsx (BVMT cognitive test scores)

**Dependencies:**
Ch5 5.2.x domain analyses must complete before this RQ can run. Requires domain-specific theta scores rather than omnibus scores.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- Must have both BVMT scores and domain theta scores

**Items:**
- [x] What domain: All `-N-` tagged items from domain analysis
- [x] Where domain: All `-L-`, `-U-`, `-D-` tagged items from domain analysis
- Domain theta scores already aggregated from Ch5 analyses

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from Ch5 domain analyses
- BVMT: Total Recall score (not T-scored, use raw score)

---