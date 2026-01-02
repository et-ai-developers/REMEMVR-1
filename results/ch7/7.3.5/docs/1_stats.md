## Statistical Validation Report

**Validation Date:** 2026-01-02 21:50
**Agent:** rq_stats v5.0
**Status:** ❌ REJECTED
**Overall Score:** 5.8 / 10.0

---

### Rubric Scoring Summary

| Category | Score | Max | Status |
|----------|-------|-----|--------|
| Statistical Appropriateness | 2.4 | 3.0 | ⚠️ |
| Tool Availability | 0.9 | 2.0 | ❌ |
| Parameter Specification | 1.4 | 2.0 | ⚠️ |
| Validation Procedures | 0.5 | 2.0 | ❌ |
| Devil's Advocate Analysis | 0.6 | 1.0 | ⚠️ |
| **TOTAL** | **5.8** | **10.0** | **❌ REJECTED** |

---

### Detailed Rubric Evaluation

#### Statistical Appropriateness (2.4 / 3.0)

**Criteria Checklist:**
- [x] ANOVA appropriate for comparing calibration groups on continuous outcomes (education, RPM, age)
- [x] Correlation analysis appropriate for examining calibration-reserve relationships
- [x] Analysis complexity appropriate for exploratory research question
- [ ] Comprehensive justification of methodological choices missing

**Assessment:**
The proposed ANOVA and correlation approach is methodologically sound for comparing calibration groups on cognitive reserve indicators. The analysis is appropriately simple for the exploratory nature of the research question. Multiple testing correction via Decision D068 dual reporting shows good statistical practice.

**Strengths:**
- Standard statistical methods appropriate for research question
- Multiple testing correction acknowledged (Decision D068)
- Bootstrap confidence intervals for correlations show good practice
- Sensitivity analyses planned (outlier exclusion, alternative grouping)

**Concerns / Gaps:**
- Calibration group creation method (correlation residuals) needs more theoretical justification
- No discussion of alternatives like ANCOVA to control for confounders
- Limited consideration of non-parametric alternatives if assumptions violated

**Score Justification:**
Strong methodological foundation with minor gaps in justification. Methods match RQ requirements and data structure, with good attention to multiple testing issues.

#### Tool Availability (0.9 / 2.0)

**Criteria Checklist:**
- [ ] Most required analysis tools missing from REMEMVR tools package
- [ ] Low tool reuse rate (~10-20%)
- [x] Missing tools clearly identified with specifications possible

**Assessment:**
Major tool availability gaps for the proposed statistical analysis. The REMEMVR tools package is optimized for IRT/LMM analyses, not basic statistical comparisons.

**Source:** `docs/v4/tools_inventory.md`

**Analysis Pipeline Steps:**

| Step | Tool Function | Status | Notes |
|------|---------------|--------|-------|
| Step 1: Data Preparation | Basic data loading | ✅ Available | Generic tools.data functions |
| Step 2: Calibration Groups | Residual-based grouping | ⚠️ Missing | Needs custom implementation |
| Step 3: One-way ANOVA | Group comparisons | ⚠️ Missing | scipy.stats available but not REMEMVR tools |
| Step 4: Correlation Analysis | Pearson correlations | ⚠️ Missing | Basic stats, not specialized tools |
| Step 5: Bootstrap CIs | Bootstrap confidence intervals | ⚠️ Missing | No bootstrap infrastructure |
| Step 6: Effect Sizes | Cohen's d for groups | ⚠️ Missing | tools.analysis_lmm has f-squared only |
| Step 7: Multiple Testing | Bonferroni correction | ⚠️ Missing | D068 in LMM tools only |

**Tool Reuse Rate:** 2/7 tools (29%) - mostly data handling functions

**Missing Tools:**
1. **Tool Name:** `tools.analysis_stats.one_way_anova_d068`
   - **Required For:** Step 3 - Group comparisons with dual p-value reporting
   - **Priority:** High (core analysis method)
   - **Specifications:** ANOVA with assumption checks, effect sizes, dual reporting per D068

2. **Tool Name:** `tools.analysis_stats.correlations_bootstrap`
   - **Required For:** Step 4 - Correlation analysis with bootstrap CIs
   - **Priority:** High (core analysis method)
   - **Specifications:** Pearson correlations with 1000-iteration bootstrap confidence intervals

3. **Tool Name:** `tools.analysis_stats.create_calibration_groups`
   - **Required For:** Step 2 - Create well-calibrated/over/underconfident groups
   - **Priority:** High (novel grouping method)
   - **Specifications:** Correlation residuals with configurable SD cutoffs, group validation

**Tool Availability Assessment:**
❌ Insufficient (<90% tool reuse): Multiple core statistical tools missing, significant implementation required

#### Parameter Specification (1.4 / 2.0)

**Criteria Checklist:**
- [x] Key parameters specified (0.5 SD cutoffs, 1000 bootstrap iterations)
- [ ] Some parameter choices need better justification
- [x] Multiple testing correction method specified (Decision D068)

**Assessment:**
Basic parameter specifications present but some methodological choices need stronger justification. The 0.5 SD cutoffs for calibration grouping and 1000 bootstrap iterations are reasonable but not literature-supported.

**Strengths:**
- Calibration group cutoffs specified (0.5 SD from correlation residuals)
- Bootstrap iteration count specified (1000)
- Decision D068 dual p-value reporting referenced
- Effect size interpretation ranges mentioned

**Concerns / Gaps:**
- 0.5 SD cutoff not justified from calibration literature
- Group size validation mentioned but criteria not specified
- No justification for Pearson vs Spearman correlations
- Bootstrap CI percentile method not specified

**Score Justification:**
Parameters adequately specified for implementation but lack strong methodological rationale. Some key choices (group cutoffs) need literature support.

#### Validation Procedures (0.5 / 2.0)

**Criteria Checklist:**
- [ ] No ANOVA assumption testing specified
- [ ] No correlation assumption checking mentioned  
- [x] Some sensitivity analyses planned

**Assessment:**
Major gaps in statistical assumption validation procedures. The concept specifies sensitivity analyses but lacks comprehensive assumption testing framework required for rigorous analysis.

**Strengths:**
- Sensitivity analysis planned (outlier exclusion)
- Alternative grouping methods considered (tertiles vs SD cutoffs)
- Data quality checks mentioned

**Concerns / Gaps:**
- No normality tests specified for ANOVA
- No homogeneity of variance testing (Levene's test)
- No linearity checks for correlations
- Missing assumption violation remedial actions
- No diagnostic plots planned

**Recommendations:**
- Add Shapiro-Wilk normality tests for each group
- Include Levene's test for homogeneity of variance  
- Specify Q-Q plots for visual normality assessment
- Plan non-parametric alternatives (Kruskal-Wallis, Spearman) if assumptions violated

**Score Justification:**
Insufficient validation procedures for methodological rigor. Lacks comprehensive assumption testing that reviewers would expect for ANOVA/correlation analyses.

#### Devil's Advocate Analysis (0.6 / 1.0)

**Meta-Scoring:** Evaluating thoroughness of statistical criticism generation (WebSearch skipped per instruction)

**Coverage Assessment:**
Generated concerns across 4 required subsections with moderate depth. Identified key methodological gaps but could be more comprehensive with literature support.

**Criticism Summary:**
- Commission Errors: 2 concerns (residual-based grouping, validation methods)
- Omission Errors: 3 concerns (power analysis, assumption testing, group imbalances)  
- Alternative Approaches: 2 concerns (continuous vs categorical, regression vs ANOVA)
- Known Pitfalls: 3 concerns (small groups, meaningless grouping, multiple testing)

**Total concerns:** 10 across all subsections

**Quality Assessment:**
Criticisms are methodologically sound but lack specific literature citations (due to skipped WebSearch). Concerns address real statistical issues that reviewers would likely raise.

**Meta-thoroughness:**
Adequate coverage of statistical criticism types. Without literature search, criticisms are based on general statistical principles rather than specific methodological papers.

**Score Justification:**
Adequate devil's advocate analysis given constraints. Generated sufficient concerns across all categories but limited by lack of literature grounding due to skipped WebSearch.

---

### Tool Availability Validation

**Source:** `docs/v4/tools_inventory.md`

**Analysis Pipeline Requirements:**

| Step | Required Functionality | REMEMVR Tools Status | Standard Library |
|------|----------------------|-------------------|----------------|
| One-way ANOVA | Group comparisons with effect sizes | ❌ Missing | scipy.stats.f_oneway |
| Correlation Analysis | Pearson r with significance | ❌ Missing | scipy.stats.pearsonr |
| Bootstrap CIs | Resampling confidence intervals | ❌ Missing | scipy.stats.bootstrap |
| Multiple Testing | Bonferroni correction | ❌ Missing | statsmodels.stats |
| Effect Sizes | Cohen's d for group comparisons | ❌ Missing | Custom calculation |
| Assumption Testing | Normality, homogeneity tests | ❌ Missing | scipy.stats |

**Tool Reuse Assessment:**
- REMEMVR-specific tools: 2/7 (29%) - data loading and validation only
- Standard library coverage: 6/7 (86%) - most functionality available in scipy/statsmodels
- Implementation gap: REMEMVR lacks basic statistical analysis infrastructure

**Missing Tool Specifications:**

1. **tools.analysis_stats.one_way_anova_comprehensive**
   - **Purpose:** Complete ANOVA pipeline with assumption testing
   - **Inputs:** data (DataFrame), grouping_var (str), outcome_vars (List[str]), alpha (float)
   - **Outputs:** ANOVA results with effect sizes, assumption tests, dual p-values per D068
   - **Features:** Shapiro-Wilk normality, Levene homogeneity, Brown-Forsythe robustness

2. **tools.analysis_stats.bootstrap_correlations**
   - **Purpose:** Correlation analysis with bootstrap confidence intervals  
   - **Inputs:** x (Series), y (Series), n_bootstrap (int), ci_level (float)
   - **Outputs:** r, p-value, bootstrap CI, assumption diagnostics
   - **Features:** Pearson/Spearman options, outlier detection, linearity assessment

---

### Validation Procedures Checklists

#### ANOVA Validation Checklist

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Normality | Shapiro-Wilk per group | p>0.05 | ❌ Not specified in concept |
| Homogeneity of Variance | Levene's test | p>0.05 | ❌ Not specified in concept |
| Independence | Design review | Study structure | ✅ Between-subjects design appropriate |
| Outliers | Box plots + IQR rule | >1.5×IQR | ❌ Only mentions "outlier exclusion" |

**ANOVA Validation Assessment:**
Major gaps in assumption testing procedures. Concept mentions sensitivity analysis for outliers but lacks systematic assumption validation that would be required for publication.

**Required Additions:**
- Shapiro-Wilk normality tests for each calibration group
- Levene's test for equal variances across groups
- Box plot visualization for outlier identification
- Remedial actions: Kruskal-Wallis if normality violated, Welch ANOVA if variances unequal

---

#### Correlation Validation Checklist

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Linearity | Scatterplot inspection | Visual assessment | ❌ Not specified in concept |
| Normality | Shapiro-Wilk | p>0.05 | ❌ Not specified in concept |
| Outliers | Cook's distance | D > 4/n | ❌ Limited outlier procedures |
| Independence | Design review | Study structure | ✅ Independent participants |

**Correlation Validation Assessment:**
Insufficient assumption checking for correlation analyses. Bootstrap CIs mentioned but underlying assumptions not validated.

**Required Additions:**
- Scatterplot matrix for linearity assessment
- Normality testing for bivariate distributions
- Outlier detection using leverage and influence measures
- Alternative: Spearman correlation if assumptions violated

---

### Statistical Criticisms & Rebuttals

**Analysis Approach:**
- **WebSearch Strategy:** Skipped per user instruction for Ch7 standard regression methods
- **Focus:** Commission errors (questionable assumptions) and omission errors (missing procedures)
- **Limitation:** Without literature search, criticisms based on general statistical principles

---

#### Commission Errors (Questionable Statistical Assumptions/Claims)

**1. Calibration Group Creation Method Not Validated**
- **Location:** 1_concept.md - Section 4: Analysis Approach, Step 2
- **Claim Made:** "Compute confidence-accuracy correlation residuals" and "Define groups: Overconfident (residual > 0.5 SD)"
- **Statistical Criticism:** Method assumes correlation residuals provide meaningful psychological groupings, but 0.5 SD cutoff is arbitrary. No validation that resulting groups represent distinct calibration phenotypes vs statistical artifacts.
- **Methodological Counterevidence:** Standard practice in calibration research uses confidence-accuracy difference scores or bias measures (overconfidence = confidence - accuracy), not residuals from correlation which may not preserve ordinal relationships.
- **Strength:** MODERATE
- **Suggested Rebuttal:** "Add methodological justification for residual approach vs difference scores. Cite calibration literature supporting this grouping method. Include validation showing groups differ meaningfully on calibration measures beyond just statistical cutoffs."

**2. Group Size Validation Criteria Unspecified**
- **Location:** 1_concept.md - Section 4: Analysis Approach, Step 2
- **Claim Made:** "Validate group sizes and distributions"
- **Statistical Criticism:** No criteria specified for minimum group sizes or distributional requirements. With N=100 and 3 groups, risk of severely unbalanced groups that violate ANOVA assumptions.
- **Methodological Counterevidence:** ANOVA requires roughly equal group sizes (largest/smallest ratio <1.5) and minimum n>20 per group for adequate power. Residual-based grouping may create 20/60/20 or worse imbalances.
- **Strength:** MODERATE  
- **Suggested Rebuttal:** "Specify minimum group size requirements (n≥20 per group). Plan alternative grouping methods (e.g., forced tertiles) if residual approach creates severe imbalances. Include group balance assessment in validation procedures."

---

#### Omission Errors (Missing Statistical Considerations)

**1. No Power Analysis for Group Comparisons**
- **Missing Content:** Concept proposes ANOVA group comparisons but provides no power analysis for detecting meaningful differences with N=100 across 3 groups
- **Why It Matters:** Without power analysis, risk of Type II error (failing to detect true group differences) or conducting underpowered study. Effect size expectations (F > 3.0, F > 4.0) suggest medium effects but no sample size justification.
- **Supporting Literature:** Standard practice requires power analysis for group comparison studies. Cohen (1988) guidelines suggest n≥26 per group for medium effects (f=0.25) at 80% power.
- **Potential Reviewer Question:** "What is the statistical power to detect the expected group differences with your sample size?"
- **Strength:** CRITICAL
- **Suggested Addition:** "Add power analysis to Section 4 showing 80% power to detect medium effects (f≥0.25) with α=0.05. If underpowered, acknowledge limitation or consider reducing groups to increase power."

**2. Missing Comprehensive Assumption Testing**
- **Missing Content:** No specification of normality tests, homogeneity of variance tests, or diagnostic procedures for ANOVA and correlation assumptions
- **Why It Matters:** ANOVA and correlation analyses have specific assumptions. Violation without detection leads to invalid statistical inference. Reviewers expect assumption validation.
- **Supporting Literature:** Field (2013) and other statistical texts require assumption testing before parametric analyses. Shapiro-Wilk, Levene's test, and diagnostic plots are standard procedures.
- **Potential Reviewer Question:** "How will you test whether your data meet the assumptions for ANOVA and correlation analyses?"
- **Strength:** CRITICAL
- **Suggested Addition:** "Add comprehensive assumption testing procedures to Section 7: Validation. Include Shapiro-Wilk normality tests, Levene homogeneity test, and diagnostic plots. Specify remedial actions (non-parametric alternatives) if assumptions violated."

**3. No Discussion of Confounding Variables**
- **Missing Content:** Analysis compares groups on education, RPM, and age but doesn't consider controlling for potential confounders (e.g., overall memory performance)
- **Why It Matters:** Groups defined by memory performance characteristics may differ systematically on variables that could confound relationships with cognitive reserve indicators.
- **Supporting Literature:** ANCOVA designs commonly used in cognitive research to control for baseline differences between groups.
- **Potential Reviewer Question:** "Should you control for overall memory performance when comparing groups on cognitive reserve indicators?"
- **Strength:** MODERATE
- **Suggested Addition:** "Consider ANCOVA controlling for overall theta scores when comparing groups on education/RPM. Alternatively, acknowledge this limitation in discussion section."

---

#### Alternative Statistical Approaches (Not Considered)

**1. Continuous Calibration Measures Instead of Groups**
- **Alternative Method:** Use calibration quality as continuous predictor in regression models instead of categorical groups
- **How It Applies:** Linear regression of education/RPM/age on continuous calibration measures avoids arbitrary grouping and preserves information
- **Why Concept.md Should Address It:** Categorical grouping loses information and statistical power compared to continuous approaches
- **Strength:** MODERATE
- **Suggested Acknowledgment:** "Acknowledge trade-off between interpretability (groups) and statistical power (continuous). Consider supplemental analyses using continuous calibration predictors to maximize power."

**2. Non-parametric Alternatives for Robust Analysis**
- **Alternative Method:** Kruskal-Wallis test for group comparisons, Spearman correlations for associations
- **How It Applies:** Provides robust alternatives if normality or other parametric assumptions violated
- **Why Concept.md Should Address It:** Small group sizes and cognitive data often violate normality assumptions
- **Strength:** MINOR
- **Suggested Acknowledgment:** "Include non-parametric alternatives (Kruskal-Wallis, Spearman) as backup if parametric assumptions violated during analysis."

---

#### Known Statistical Pitfalls (Unaddressed)

**1. Multiple Comparisons Without Family-Wise Error Control**
- **Pitfall Description:** Testing 3 outcomes (education, RPM, age) across 3 groups creates multiple comparison problem even with Bonferroni correction within each test
- **How It Could Affect Results:** Inflated Type I error rate across the family of 9 pairwise comparisons (3 groups × 3 outcomes)
- **Why Relevant to This RQ:** Concept mentions "dual p-value reporting" but unclear if family-wise error controlled across all comparisons
- **Strength:** MODERATE
- **Suggested Mitigation:** "Clarify family-wise error control strategy. Consider Holm-Bonferroni across all 9 comparisons or accept higher Type I risk with clear acknowledgment of exploratory nature."

**2. Small Effect Sizes May Not Be Meaningful**
- **Pitfall Description:** Expected correlations (r=0.25-0.40) are small-to-medium effects that may not represent practically significant relationships
- **How It Could Affect Results:** Statistically significant but practically meaningless findings, especially with multiple testing
- **Why Relevant to This RQ:** Small effects in exploratory research may not replicate or have real-world significance
- **Strength:** MINOR
- **Suggested Mitigation:** "Include effect size interpretation guidelines and discuss practical significance thresholds. Acknowledge exploratory nature requiring replication."

**3. Calibration Group Validity Concerns**  
- **Pitfall Description:** Groups based on statistical residuals may not represent psychologically meaningful calibration types
- **How It Could Affect Results:** Finding group differences that reflect statistical artifacts rather than true metacognitive phenotypes
- **Why Relevant to This RQ:** Novel grouping method without established validity in calibration literature
- **Strength:** MODERATE
- **Suggested Mitigation:** "Include calibration group validation: compare groups on direct calibration measures (confidence-accuracy bias) to confirm psychological meaningfulness beyond statistical definition."

---

#### Scoring Summary for Devil's Advocate Analysis

**Count concerns across all 4 subsections:**
- Commission Errors: 2 (0 CRITICAL, 2 MODERATE, 0 MINOR)
- Omission Errors: 3 (2 CRITICAL, 1 MODERATE, 0 MINOR)  
- Alternative Approaches: 2 (0 CRITICAL, 1 MODERATE, 1 MINOR)
- Known Pitfalls: 3 (0 CRITICAL, 2 MODERATE, 1 MINOR)

**Total concerns:** 10 (2 CRITICAL, 6 MODERATE, 2 MINOR)

**Overall Devil's Advocate Assessment:**
Concept.md adequately describes the general analytical approach but lacks sufficient methodological detail to anticipate common statistical criticisms. Key gaps include assumption testing procedures, power analysis, and validation of novel calibration grouping method. The exploratory nature of the research question is appropriate, but stronger methodological foundation required for publication readiness.

---

### Recommendations

#### Required Changes (Must Address for Approval)

1. **Add Comprehensive Statistical Assumption Testing**
   - **Location:** 1_concept.md - Add new Section 7: Validation Procedures  
   - **Issue:** No assumption testing specified for ANOVA (normality, homogeneity) or correlations (linearity, normality)
   - **Fix:** Add detailed assumption testing protocol: "Validate ANOVA assumptions using Shapiro-Wilk normality tests per group (p>0.05), Levene's test for homogeneity of variance (p>0.05), and box plots for outlier detection. For correlations, assess linearity via scatterplots and bivariate normality. Plan non-parametric alternatives (Kruskal-Wallis, Spearman) if assumptions violated."
   - **Rationale:** Essential for methodological rigor - reviewers expect comprehensive assumption validation for parametric tests

2. **Conduct Power Analysis for Group Comparisons**
   - **Location:** 1_concept.md - Section 4: Analysis Approach, add subsection after Step 2
   - **Issue:** No justification that N=100 across 3 groups provides adequate power for expected effect sizes
   - **Fix:** Add power analysis: "Power analysis using G*Power: With α=0.05, n≥26 per group provides 80% power to detect medium effects (f=0.25) in one-way ANOVA. Current N=100 across 3 groups exceeds this requirement. However, if groups become severely unbalanced (e.g., 20/60/20), power may decrease substantially."
   - **Rationale:** Required to demonstrate study is adequately powered to detect meaningful effects and avoid Type II error

3. **Validate Calibration Grouping Method**
   - **Location:** 1_concept.md - Section 4: Analysis Approach, Step 2
   - **Issue:** Residual-based grouping method not validated as psychologically meaningful
   - **Fix:** Add validation step: "Validate calibration groups by confirming they differ on direct calibration measures (confidence-accuracy bias scores). Groups should show expected ordering: well-calibrated (bias ≈ 0), overconfident (bias > 0), underconfident (bias < 0). If validation fails, switch to bias-score based grouping using established calibration metrics."
   - **Rationale:** Novel grouping method requires validation to ensure psychological rather than purely statistical meaning

4. **Specify Missing Statistical Analysis Tools**
   - **Location:** 1_concept.md - Add tool specifications section
   - **Issue:** Required statistical tools missing from REMEMVR package (ANOVA, correlations, bootstrap CIs)
   - **Fix:** "Note: Analysis requires implementation of basic statistical tools currently missing from REMEMVR package: (1) One-way ANOVA with assumption testing and effect sizes, (2) Correlation analysis with bootstrap confidence intervals, (3) Calibration group creation and validation functions. These will be implemented using scipy.stats and statsmodels prior to analysis."
   - **Rationale:** Transparent acknowledgment of tool gaps and implementation plan required for realistic project planning

#### Suggested Improvements (Optional but Recommended)

1. **Consider ANCOVA to Control for Confounders**
   - **Location:** 1_concept.md - Section 4: Analysis Approach, Step 3
   - **Current:** One-way ANOVA comparing groups on education/RPM/age  
   - **Suggested:** "Consider ANCOVA controlling for overall theta scores when comparing groups on cognitive reserve indicators, as calibration groups are defined by memory-related measures"
   - **Benefit:** Controls for potential confounding by overall memory ability, strengthening causal inferences about calibration-reserve relationships

2. **Add Continuous Calibration Analysis for Maximum Power**
   - **Location:** 1_concept.md - Section 4: Analysis Approach, add Step 4b
   - **Current:** Only categorical group comparisons
   - **Suggested:** "Supplement group comparisons with continuous analyses: linear regression of education/RPM/age on continuous calibration quality measures to maximize statistical power"
   - **Benefit:** Avoids information loss from categorization and increases statistical power to detect relationships

3. **Specify Effect Size Interpretation Guidelines**  
   - **Location:** 1_concept.md - Section 4: Analysis Approach, Step 5
   - **Current:** Basic Cohen's d computation mentioned
   - **Suggested:** "Add interpretation framework: Cohen's d effect sizes (0.2 small, 0.5 medium, 0.8 large) and practical significance thresholds (d≥0.3 for meaningful group differences)"
   - **Benefit:** Provides framework for interpreting statistical vs practical significance, enhancing result interpretation

#### Missing Tools (For Implementation Before Analysis)

1. **tools.analysis_stats.one_way_anova_comprehensive**
   - **Required For:** Group comparisons with full assumption testing
   - **Priority:** High (core analysis method)
   - **Specifications:** Input: DataFrame with grouping variable and outcomes. Output: ANOVA table, effect sizes, assumption test results, dual p-values per D068. Features: Shapiro-Wilk per group, Levene's test, post-hoc comparisons with multiple correction.

2. **tools.analysis_stats.bootstrap_correlations** 
   - **Required For:** Correlation analysis with robust confidence intervals
   - **Priority:** High (core analysis method)
   - **Specifications:** Input: two continuous variables, bootstrap parameters. Output: correlation coefficient, p-value, bootstrap CI, assumption diagnostics. Features: 1000-iteration bootstrap, outlier detection, linearity assessment.

3. **tools.analysis_stats.create_calibration_groups**
   - **Required For:** Novel residual-based calibration grouping
   - **Priority:** Medium (novel methodology)  
   - **Specifications:** Input: confidence and accuracy scores, grouping parameters. Output: group assignments, validation metrics. Features: Correlation residuals computation, configurable SD cutoffs, group balance validation, bias-score validation.

---

### Validation Metadata

- **Agent Version:** rq_stats v5.0
- **Rubric Version:** 10-point system (v5.0)  
- **Validation Date:** 2026-01-02 21:50
- **Tools Inventory Source:** docs/v4/tools_inventory.md
- **Total Tools Validated:** 7
- **Tool Reuse Rate:** 29% (2/7 tools available in REMEMVR package)
- **Validation Duration:** ~25 minutes
- **Context Dump:** "5.8/10 REJECTED. Category 1: 2.4/3 (appropriate methods). Category 2: 0.9/2 (29% tool reuse). Category 3: 1.4/2 (parameters need justification). Category 4: 0.5/2 (missing assumption testing). Category 5: 0.6/1 (10 concerns, adequate coverage)."

---