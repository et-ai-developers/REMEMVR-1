# RQ 7.2.4: VR Scaffolding Validation

**Chapter:** 7
**Type:** Cross-Sectional Prediction
**Subtype:** VR Scaffolding Hypothesis Test
**Full ID:** 7.2.4

---

## Research Question

**Primary Question:**
Does REMEMVR show age-invariance while RAVLT shows age decline in the same sample? This formally tests the VR scaffolding hypothesis.

**Scope:**
This RQ compares age correlations between traditional episodic memory testing (RAVLT) and VR-based episodic memory testing (REMEMVR) within the same sample of 100 participants. Uses bivariate correlations and Steiger's Z-test for dependent correlation comparison. Tests the critical prediction that VR context provides compensatory scaffolding that traditional tests lack.

**Theoretical Framing:**
Traditional cognitive tests consistently show robust age decline (r = -0.40 to -0.50 for RAVLT in literature). Chapter 5 found AgeTime interaction p = 0.96 for REMEMVR forgetting trajectories. If the same participants show age decline on RAVLT but not REMEMVR, it validates that the VR context (not sample characteristics) provides age-invariance.

---

## Theoretical Background

**Relevant Theories:**
- **Scaffolding Theory of Aging and Cognition (STAC)**: Proposes that aging brain adaptively recruits additional neural resources to maintain cognitive performance. VR environment may provide external scaffolding that supports this compensatory process.
- **Cognitive Reserve Theory**: Individual differences in ability to cope with age-related neural changes. VR may reduce reliance on declining neural systems by providing alternative processing routes.
- **Episodic Memory and Aging**: Traditional episodic memory tests show consistent age-related decline (r = -0.30 to -0.50) across multiple studies. RAVLT specifically shows r H -0.40 with age in healthy adults.

**Key Citations:**
Park & Reuter-Lorenz (2009) - STAC theory
Stern (2002) - Cognitive reserve framework
Schmidt (1996) - RAVLT age norms

**Theoretical Predictions:**
STAC theory predicts that VR scaffolding should attenuate age-related decline by providing environmental support for compensatory processing. Traditional tests lack such scaffolding and should show typical age-related decline patterns.

**Literature Gaps:**
Direct comparison of age effects between traditional and VR episodic memory tests within the same participants is lacking. Most studies compare different samples or use different task designs, confounding age effects with sample or methodological differences.

---

## Hypothesis

**Primary Hypothesis:**
RAVLT should show significant age decline (r < -0.30, consistent with literature) while REMEMVR should show minimal age decline (r H 0, consistent with Ch5 AgeTime p = 0.96). The difference between these correlations should be statistically significant via Steiger's Z-test.

**Secondary Hypotheses:**
The magnitude of age-related decline should be significantly larger for RAVLT than REMEMVR, supporting the VR scaffolding hypothesis. Effect size difference should be medium to large (Cohen's d > 0.5).

**Theoretical Rationale:**
VR provides rich environmental context, spatial navigation cues, and immersive encoding that may compensate for age-related hippocampal decline. Traditional list learning (RAVLT) lacks these scaffolding elements and relies primarily on declining verbal episodic memory systems.

**Expected Effect Pattern:**
RAVLT: r(Age) < -0.30, p < 0.05
REMEMVR: r(Age) H 0, p > 0.10  
Steiger's Z > 2.0, p < 0.05 for correlation difference

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in omnibus REMEMVR theta_all scores from Ch5

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)  
  - [x] `-D-` tags (put-down location)
  - Description: Included in omnibus REMEMVR theta_all scores from Ch5

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in omnibus REMEMVR theta_all scores from Ch5

**Inclusion Rationale:**
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains (What/Where/When) to provide comprehensive REMEMVR performance measure. This omnibus approach parallels RAVLT's overall memory score.

**Exclusion Rationale:**
Individual domain scores not examined here to maintain focus on overall episodic memory performance comparison. Domain-specific age effects are examined in separate RQs.

---

## Analysis Approach

**Analysis Type:**
Correlation analysis with dependent correlation comparison (Steiger's Z-test)

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load REMEMVR theta_all means per participant from Ch5 5.1.1
- Extract RAVLT_Total scores from dfnonvr.csv  
- Standardize both measures for comparison
- Check data quality and missing values

**Step 2:** Compute bivariate correlations
- r(Age, RAVLT_Total) with 95% confidence interval
- r(Age, REMEMVR_Theta) with 95% confidence interval
- Report both uncorrected and Bonferroni-corrected p-values (Decision D068)

**Step 3:** Test correlation difference
- Steiger's Z-test for comparing dependent correlations
- H0: |r_RAVLT| = |r_REMEMVR|
- H1: |r_RAVLT| > |r_REMEMVR| (directional test)
- Compute effect size: d = (|r_RAVLT| - |r_REMEMVR|) / pooled SE

**Step 4:** Model diagnostics
- Check linearity assumptions via scatterplots
- Identify potential outliers (standardized residuals > 3)
- Test normality of residuals (Shapiro-Wilk test)

**Step 5:** Sensitivity analyses
- Exclude outliers and recompute correlations
- Bootstrap confidence intervals (1000 iterations)
- Compare Pearson vs Spearman correlations

**Step 6:** Visualization
- Side-by-side scatterplots: Age vs RAVLT and Age vs REMEMVR
- Include regression lines with 95% confidence bands
- Highlight correlation coefficients and p-values

**Step 7:** Power analysis
- Post-hoc power for observed correlations
- Sensitivity: smallest detectable correlation difference at 80% power

**Expected Outputs:**
- data/step01_age_ravlt_data.csv (RAVLT data with demographics)
- data/step02_age_rememvr_data.csv (REMEMVR theta scores with demographics)
- data/step03_merged_analysis_data.csv (combined dataset for analysis)
- data/step04_correlation_results.csv (correlations, CIs, p-values)
- data/step05_steiger_test_results.csv (dependent correlation test results)
- data/step06_sensitivity_analysis.csv (outlier-excluded results)
- data/step07_bootstrap_cis.csv (bootstrap confidence intervals)
- results/scaffolding_validation_summary.md (text summary for thesis)
- plots/age_ravlt_scatter.png (RAVLT age correlation plot)
- plots/age_rememvr_scatter.png (REMEMVR age correlation plot)  
- plots/scaffolding_comparison.png (side-by-side comparison)

**Success Criteria:**
- [ ] RAVLT shows significant age decline (p < 0.05, uncorrected)
- [ ] REMEMVR shows non-significant age decline (p > 0.10)
- [ ] Steiger's Z-test p < 0.05 (correlation difference significant)
- [ ] Effect size d > 0.5 (medium to large difference)
- [ ] Consistent with Ch5 age-invariance finding (r H 0 for REMEMVR)
- [ ] Results robust to outlier exclusion
- [ ] Bootstrap CIs exclude zero for correlation difference
- [ ] Power > 0.80 for detecting medium correlation difference

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison - provides omnibus theta_all scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (REMEMVR theta estimates)
- data/cache/master.xlsx (RAVLT scores and demographics)

**Dependencies:**
Ch5 5.1.1 must complete Steps 1-3 (IRT calibration, purification, final theta estimation) before this RQ can run.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from Ch5 sample
- [x] Must have both REMEMVR theta scores and RAVLT scores
- [ ] Exclude: Participants missing either RAVLT or age data

**Items:**
- N/A (uses aggregated theta scores, not item-level data)

**Tests:**
- [x] REMEMVR: Omnibus theta_all (aggregated across T1-T4)
- [x] RAVLT: Total score across all trials (T1-T5 + Delayed Recall)

---