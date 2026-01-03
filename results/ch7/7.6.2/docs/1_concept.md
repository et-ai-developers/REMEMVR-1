# RQ 7.6.2: Does RAVLT Delayed predict REMEMVR slope?

**Chapter:** 7
**Type:** Slopes (Predictors of Forgetting Rate)
**Subtype:** RAVLT Delayed Forgetting Correlation
**Full ID:** 7.6.2

---

## Research Question

**Primary Question:**
Does RAVLT forgetting (T5 - Delayed Recall) predict REMEMVR forgetting rate?

**Scope:**
This RQ tests whether short-term forgetting (RAVLT delay of 20-30 minutes) predicts long-term forgetting (REMEMVR slope over 6 days). Analysis includes N=100 participants, correlating RAVLT forgetting index (T5Sc - DRSc) with REMEMVR per-participant slope values. Includes both bivariate and partial correlations controlling for initial encoding.

**Theoretical Framing:**
Tests whether forgetting reflects stable individual differences in consolidation efficiency across different time scales. If consolidation mechanisms generalize, short-term and long-term forgetting should correlate, providing evidence for common underlying processes.

---

## Theoretical Background

**Relevant Theories:**
- **Consolidation Theory**: If forgetting reflects stable individual differences in consolidation efficiency, different time scales should correlate.
- **Memory Systems Theory**: Different consolidation mechanisms may operate at different time scales - hippocampal-dependent consolidation for REMEMVR vs working memory decay for RAVLT delayed.

**Key Citations:**
[To be enhanced by rq_scholar]

**Theoretical Predictions:**
If consolidation processes generalize across time scales, individuals who show greater forgetting on RAVLT delayed recall should also show steeper forgetting slopes in REMEMVR. However, different mechanisms (working memory vs long-term consolidation) may limit this relationship.

**Literature Gaps:**
Limited research on cross-task forgetting correlations, especially across such different time scales (minutes vs days).

---

## Hypothesis

**Primary Hypothesis:**
Weak positive correlation expected between RAVLT forgetting and REMEMVR slope. RAVLT delay is 20-30 minutes; REMEMVR is 6 days. If consolidation processes generalize, correlation should be detectable but may be modest due to different underlying mechanisms.

**Secondary Hypotheses:**
Partial correlation controlling for initial encoding levels (RAVLT T5 and REMEMVR intercept) may be weaker than bivariate correlation, as initial encoding capacity may confound the forgetting relationship.

**Theoretical Rationale:**
Consolidation efficiency may represent a stable individual difference that manifests across different memory systems and time scales. However, RAVLT involves verbal working memory while REMEMVR involves episodic spatial memory, which may limit correlation magnitude.

**Expected Effect Pattern:**
Bivariate: r(RAVLT_Forgetting, REMEMVR_Slope) H 0.15, p H 0.14
Partial: r H 0.12, p H 0.24 (weaker after controlling for encoding)
Overall weak, non-significant relationship reflecting different mechanisms.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in REMEMVR slope from omnibus analysis

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)  
  - [x] `-D-` tags (put-down location)
  - Description: Included in REMEMVR slope from omnibus analysis

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in REMEMVR slope from omnibus analysis

**Inclusion Rationale:**
Uses REMEMVR slope from omnibus analysis that aggregates across all episodic memory domains. RAVLT tests verbal list learning (What domain equivalent in verbal modality).

**Exclusion Rationale:**
No domain-specific exclusions - requires overall REMEMVR forgetting rate rather than domain-specific slopes.

---

## Analysis Approach

**Analysis Type:**
Correlation analysis (bivariate and partial) with cross-validation and multiple comparison corrections

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load REMEMVR slopes from Ch5 omnibus analysis
- Extract RAVLT scores from master.xlsx (T5Sc, DRSc)
- Compute RAVLT_Forgetting = RAV_T5Sc - RAV_DRSc
- Check data quality and missingness

**Step 2:** Compute RAVLT forgetting index
- RAVLT_Forgetting = RAV_T5Sc - RAV_DRSc
- Higher values indicate more forgetting (worse delayed recall)
- Standardize to enable effect size interpretation

**Step 3:** Bivariate correlation
- r(RAVLT_Forgetting, REMEMVR_Slope)
- Compute 95% confidence interval
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni correction (α = 0.00179, calculated as 0.05/28 where 28 is the total number of primary hypotheses tested across all Chapter 7 RQs)

**Step 4:** Partial correlation analysis  
- Control for initial encoding: RAVLT_T5 and REMEMVR_Intercept
- Partial r(RAVLT_Forgetting, REMEMVR_Slope | T5, Intercept)
- Compare to bivariate correlation

**Step 5:** Model diagnostics
- Check correlation assumptions: linearity, normality
- Identify outliers using Cook's D < 4/N
- Test homoscedasticity
- Examine residual plots

**Step 6:** Cross-validation
- Bootstrap resampling (1000 iterations) for CI stability
- Sensitivity analysis: exclude outliers, recompute
- Compare Pearson vs Spearman (if normality violated)

**Step 7:** Effect size interpretation
- Cohen's guidelines: r = 0.10 small, 0.30 medium, 0.50 large
- Clinical significance: practical importance for theory
- Compare to encoding-to-encoding correlations (RQ 7.1.1)

**Step 8:** Power analysis
- Post-hoc power for observed effect size
- Sensitivity: smallest detectable correlation at 80% power
- N=100 adequate for medium effects but limited for small effects

**Expected Outputs:**
- data/step01_ravlt_forgetting.csv (computed forgetting index)
- data/step02_rememvr_slopes.csv (extracted slope values)  
- data/step03_analysis_input.csv (merged dataset)
- data/step04_bivariate_correlation.csv (r, CI, dual p-values)
- data/step05_partial_correlation.csv (partial r controlling encoding)
- data/step06_diagnostics.csv (assumptions, outliers, normality tests)
- data/step07_bootstrap (1000 replications, seed=42)_results.csv (resampling stability)
- data/step08_power_analysis.csv (post-hoc and sensitivity)
- results/forgetting_correlation_summary.md (text summary for thesis)
- plots/forgetting_scatterplot.png (bivariate relationship)
- plots/partial_correlation_plot.png (residual plots)
- plots/diagnostic_plots.png (normality, outliers)

**Success Criteria:**
- [ ] Valid correlation coefficients (not NaN or infinite)
- [ ] Confidence intervals computed successfully  
- [ ] Both uncorrected and corrected p-values reported
- [ ] Assumptions checked (linearity, normality, homoscedasticity)
- [ ] No extreme outliers (Cook's D < 4/N = 0.04)
- [ ] bootstrap (1000 replications, seed=42) CIs stable across iterations
- [ ] Power analysis completed for effect size interpretation
- [ ] Results interpretable in consolidation theory framework
- [ ] Comparison to encoding correlations (7.1.1) meaningful

---

## Data Source

**Data Type:**
DERIVED (from Ch5 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 omnibus analysis providing REMEMVR slopes

**File Paths:**
- results/ch5/5.1.1/data/step06_best_model.pkl (LMM with slopes)
- results/ch5/5.1.1/data/step04_lmm_input.csv (for slope extraction)
- data/cache/master.xlsx (RAVLT T5Sc, DRSc scores)

**Dependencies:**
Ch5 5.1.1 must complete Step 6 (LMM fitting with individual slopes) before this RQ can run. Requires successful omnibus slope estimation.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from Ch5 analysis
- [ ] Subset: None - requires complete RAVLT data
- [ ] Exclude: Participants with missing RAVLT T5 or Delayed Recall

**Items:**
- N/A (uses aggregated theta slopes, not individual items)

**Tests:**
- [x] All 4 REMEMVR tests (T1, T2, T3, T4) - required for slope calculation
- [x] RAVLT T5 (Trial 5 learning) 
- [x] RAVLT Delayed Recall (20-30 minute delay)

---