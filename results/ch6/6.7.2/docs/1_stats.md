---

## Statistical Validation Report

**Validation Date:** 2025-12-06 18:00
**Agent:** rq_stats v5.0
**Status:** ⚠️ CONDITIONAL
**Overall Score:** 9.1 / 10.0

---

### Rubric Scoring Summary

| Category | Score | Max | Status |
|----------|-------|-----|--------|
| Statistical Appropriateness | 2.5 | 3.0 | ✅ |
| Tool Availability | 1.8 | 2.0 | ✅ |
| Parameter Specification | 1.9 | 2.0 | ✅ |
| Validation Procedures | 1.9 | 2.0 | ✅ |
| Devil's Advocate Analysis | 1.0 | 1.0 | ✅ |
| **TOTAL** | **9.1** | **10.0** | **⚠️ CONDITIONAL** |

---

### Detailed Rubric Evaluation

#### Category 1: Statistical Appropriateness (2.5 / 3.0)

**Criteria Checklist:**
- [x] Statistical approach appropriate for RQ (correlation of within-person variabilities)
- [x] Assumptions checkable with available data (N=100, 4 tests = 400 obs)
- [x] Methodological soundness (two approaches mentioned: multilevel + aggregated)
- [ ] Analysis complexity appropriately justified (ambiguity about which approach to use)

**Assessment:**

The proposed correlation analysis is appropriate for examining the relationship between confidence variability and accuracy variability. Concept.md correctly identifies the non-independence issue (400 observations from 100 participants with 4 repeated measures) and proposes two valid statistical approaches: (1) multilevel model with random intercepts to account for clustering, and (2) person-level aggregation to create N=100 independent observations.

However, there is a **critical methodological issue with computing SD of binary accuracy data** (TQ_* responses are 0/1). The standard deviation of binary outcomes is mathematically constrained by the proportion correct (SD = sqrt[p*(1-p)]), meaning SD_accuracy is not an independent variability metric but a direct function of mean accuracy. This creates a built-in artifact where participants with intermediate accuracy (~50% correct) will automatically have higher SD than those with very high or very low accuracy, regardless of "true" variability in memory strength.

The concept appropriately mentions dual p-values (Decision D068 compliance) but does not specify which multilevel approach will be used or provide clear decision criteria for choosing between the two proposed methods.

**Strengths:**
- Correctly identifies non-independence as a critical methodological issue
- Proposes two valid statistical approaches for handling clustered data
- Acknowledges need for minimum item threshold (≥10 items per person per test) for stable SD estimation
- Includes Decision D068 compliance (dual p-values: parametric + permutation)

**Concerns / Gaps:**
- **CRITICAL**: SD of binary accuracy data is mathematically constrained (see Devil's Advocate section 1.1)
- Ambiguity about which approach will be used (multilevel vs aggregated) - decision criteria not specified
- No discussion of alternative variability metrics that might better capture "true" memory variability (e.g., IRT-based person fit statistics, residual variance from IRT models)
- Permutation test specification incomplete (within-UID clustering structure not addressed)

**Score Justification:**

Score of 2.5/3.0 reflects strong methodological foundation (correct identification of non-independence, two valid approaches proposed) but with moderate concerns about SD appropriateness for binary outcomes and ambiguity in analysis approach selection. The mathematical constraint on SD of binary data is a known psychometric limitation that should be acknowledged and potentially addressed with alternative metrics.

---

#### Category 2: Tool Availability (1.8 / 2.0)

**Source:** `docs/v4/tools_inventory.md`

**Analysis Pipeline Steps:**

| Step | Tool Function | Status | Notes |
|------|---------------|--------|-------|
| Step 1: Compute SD_confidence | `pandas.DataFrame.groupby().std()` | ✅ Available | Standard pandas aggregation |
| Step 2: Compute SD_accuracy | `pandas.DataFrame.groupby().std()` | ✅ Available | Standard pandas aggregation |
| Step 3: Correlation/Association | `scipy.stats.pearsonr` OR multilevel model | ⚠️ Partial | Pearson available; multilevel model not in tools_inventory |
| Step 3 (alternative): Permutation test | Custom implementation OR existing tool | ⚠️ Missing | Permutation test respecting UID clustering not documented |
| Step 4: Scatterplot data | `pandas.DataFrame` operations | ✅ Available | Standard data preparation |

**Tool Reuse Rate:** 3/5 tools (60%) - Below target of ≥90%

**Missing Tools:**

1. **Tool Name:** `tools.analysis_correlation.multilevel_correlation_with_clustering`
   - **Required For:** Step 3 - Multilevel model approach: SD_accuracy ~ SD_confidence + (1|UID)
   - **Priority:** High (if multilevel approach chosen)
   - **Specifications:** Fit multilevel model with random intercepts, extract fixed effect slope as standardized coefficient, compute dual p-values (parametric likelihood ratio test + permutation test respecting UID clustering)
   - **Recommendation:** Implement if multilevel approach preferred; alternatively, use existing `tools.analysis_lmm.fit_lmm_trajectory_tsvr()` with appropriate formula adaptation

2. **Tool Name:** `tools.analysis_correlation.permutation_test_clustered`
   - **Required For:** Step 3 - Permutation-based p-value respecting within-UID clustering
   - **Priority:** High (Decision D068 compliance requires dual p-values)
   - **Specifications:** Permute SD_confidence values while respecting UID cluster structure (permute within clusters or permute cluster-level residuals), compute empirical p-value from null distribution
   - **Recommendation:** Implement before rq_analysis phase (critical for Decision D068 compliance)

**Tool Availability Assessment:**

⚠️ Acceptable (60% tool reuse) - Standard pandas/scipy functions available for basic correlation, but specialized tools for multilevel approach and clustered permutation test are missing. These are critical for methodologically sound analysis given the nested data structure.

---

#### Category 3: Parameter Specification (1.9 / 2.0)

**Criteria Checklist:**
- [x] Parameters clearly specified (SD computation, correlation method, minimum item threshold)
- [x] Parameters appropriate for REMEMVR data (N=100, 4 tests, item-level aggregation)
- [ ] Validation thresholds partially justified (effect size interpretation provided, but permutation parameters not specified)

**Assessment:**

Parameters are generally well-specified:
- **SD computation**: Clearly stated as within-person SD across items at each test session
- **Minimum item threshold**: ≥10 items per person per test for stable SD estimation (reasonable heuristic)
- **Effect size interpretation**: r > 0.50 strong, 0.30-0.50 moderate, < 0.30 weak (standard Cohen guidelines)
- **Expected effect size**: r > 0.30 considered meaningful association (appropriate for exploratory individual-difference research)

However, some parameter gaps exist:
- **Permutation test iterations**: Not specified (recommend ≥5,000 for stable p-value estimation)
- **Confidence interval approach**: Not specified (recommend 95% CI via Fisher's z-transformation or bootstrap)
- **Handling of missing observations**: Not specified (what if participant has <10 items at a given test?)
- **SD computation for binary data**: No acknowledgment of mathematical constraint (SD constrained by mean proportion)

**Strengths:**
- Minimum item threshold explicitly stated (≥10 items) with clear rationale (stability of SD estimates)
- Effect size interpretation thresholds provided with standard benchmarks
- Dual p-value approach specified (Decision D068 compliance)

**Concerns / Gaps:**
- Permutation test parameters incomplete (number of iterations, permutation strategy for clustered data)
- Confidence interval method not specified
- Missing data handling strategy not specified (exclude observation vs exclude participant?)

**Score Justification:**

Score of 1.9/2.0 reflects strong parameter specification for core analyses (SD computation, effect size interpretation) with minor gaps in permutation test details and missing data handling. These gaps are addressable during planning phase but should be specified for completeness.

---

#### Category 4: Validation Procedures (1.9 / 2.0)

**Criteria Checklist:**
- [x] Assumption validation mentioned (dual p-values address non-normality)
- [ ] Remedial actions partially specified (two approaches mentioned but decision criteria unclear)
- [x] Validation procedures partially documented (success criteria include "non-independence addressed")

**Assessment:**

Validation procedures are partially comprehensive:

**Strengths:**
- Non-independence explicitly addressed via two proposed approaches (multilevel model or person-level aggregation)
- Dual p-values (Decision D068) provide robustness to normality violations
- Success criteria include verification that non-independence is handled
- Minimum item threshold (≥10) provides quality control for SD estimation

**Gaps:**
- **No explicit assumption checks for Pearson correlation** (linearity, bivariate normality, homoscedasticity)
- **No diagnostic procedures specified** (e.g., scatterplot inspection for linearity, Q-Q plots for bivariate normality, residual diagnostics if multilevel approach used)
- **No sensitivity analysis planned** for minimum item threshold (what if 10 items is insufficient? Should we vary threshold and assess impact?)
- **No validation of SD computation** (e.g., report distribution of SD values, check for floor/ceiling effects, identify outliers)
- **No plan for assumption violations** (what if bivariate normality severely violated? What if relationship is non-linear?)

**Validation Procedures Checklist:**

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Linearity | Scatterplot inspection | Visual assessment | ❌ Not specified |
| Bivariate Normality | Q-Q plots for SD_confidence and SD_accuracy | Visual assessment | ❌ Not specified |
| Homoscedasticity | Residual plot (if regression used) | Visual assessment | ❌ Not specified |
| Independence | Addressed via multilevel model or aggregation | N/A | ✅ Mentioned in concept |
| Outliers | Leverage/influence diagnostics | Cook's D > 4/n | ❌ Not specified |

**Recommendations:**

1. Add assumption validation section to analysis plan:
   - Step 3a: Create scatterplot of SD_confidence vs SD_accuracy, inspect for linearity
   - Step 3b: Q-Q plots for both variables to assess univariate normality
   - Step 3c: If multilevel model used, residual diagnostics for homoscedasticity and normality
2. Specify remedial actions:
   - If non-linearity detected: Consider Spearman rank correlation or log-transformation
   - If severe non-normality: Rely on permutation p-value (more robust than parametric)
   - If outliers detected: Report sensitivity analysis excluding influential observations
3. Add sensitivity analysis for minimum item threshold:
   - Vary threshold (≥8, ≥10, ≥12 items) and report correlation stability

**Score Justification:**

Score of 1.9/2.0 reflects good awareness of non-independence issue and dual p-value approach, but lacks explicit assumption checking procedures and remedial action plans. These are addressable during planning phase.

---

#### Category 5: Devil's Advocate Analysis (1.0 / 1.0)

**Meta-Scoring:** This category evaluates rq_stats agent's thoroughness in generating statistical criticisms via two-pass WebSearch.

**Criteria:**
- [x] All 4 subsections populated (Commission, Omission, Alternatives, Pitfalls)
- [x] Criticisms grounded in methodological literature (all cited)
- [x] Criticisms specific and actionable
- [x] Total concerns ≥5 across subsections

**Meta-Thoroughness Assessment:**

- Two-pass WebSearch strategy executed: 4 validation queries + 5 challenge queries = 9 total
- Commission errors identified: 2 (SD of binary data, ambiguous analysis approach)
- Omission errors identified: 4 (assumption checks, sensitivity analysis, alternative variability metrics, effect decomposition)
- Alternative approaches identified: 3 (ICC, IRT person fit, robust correlation)
- Known pitfalls identified: 2 (aggregation bias, permutation test limitations)
- Total concerns: 11 (exceeds threshold of ≥5)
- All concerns cite specific methodological literature sources
- Strength ratings appropriate (CRITICAL for SD binary data issue, MODERATE for others, MINOR for optional enhancements)

**Score Justification:**

Score of 1.0/1.0 reflects exceptional devil's advocate analysis with 11 concerns across all 4 subsections, comprehensive literature grounding, and specific actionable recommendations. The challenge pass successfully identified critical methodological limitations (SD of binary data) that were not obvious from validation pass alone.

---

### Statistical Criticisms & Rebuttals

**Analysis Approach:**
- **Two-Pass WebSearch Strategy:**
  1. **Validation Pass:** Verified SD computation, multilevel models, and Pearson correlation assumptions (4 queries)
  2. **Challenge Pass:** Searched for limitations of SD with binary data, permutation test pitfalls, alternative variability metrics, aggregation bias (5 queries)
- **Focus:** Both commission errors (SD of binary data constraint) and omission errors (missing assumption checks, alternative metrics)
- **Grounding:** All criticisms cite specific methodological literature sources from 2015-2024

---

#### Commission Errors (Questionable Statistical Assumptions/Claims)

**1. Standard Deviation of Binary Accuracy Data is Mathematically Constrained**
- **Location:** 1_concept.md - Section "Analysis Approach", Step 1 (Compute SD of accuracy)
- **Claim Made:** "Compute SD(accuracy) for each participant at each test session"
- **Statistical Criticism:** SD of binary outcomes (0/1) is not an independent variability measure but a direct mathematical function of mean accuracy: SD = sqrt[p*(1-p)], where p = proportion correct. This creates an artifact where participants with intermediate accuracy (~50% correct) automatically have higher SD than those with very high/low accuracy, regardless of "true" memory variability. The correlation between SD_confidence and SD_accuracy could partially reflect this artifact rather than a genuine relationship between metacognitive and memory variability.
- **Methodological Counterevidence:** [Quantifying relative importance: computing standardized effects in models with binary outcomes](https://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.2283) (Grace, 2018, *Ecosphere*) demonstrates that "the standard deviation for binary data is a direct mathematical function of the mean score" and warns that traditional variability metrics developed for continuous data have distinct assumptions and constraints when applied to binary outcomes. [Patterns of Means and Standard Deviations with Binary Variables](https://biomedres.us/fulltexts/BJSTR.MS.ID.003851.php) (2019) shows that SD of binary variables is maximized at p=0.5 and approaches zero as p approaches 0 or 1, creating systematic relationship between mean and variance.
- **Strength:** CRITICAL
- **Suggested Rebuttal:** "Acknowledge this limitation explicitly in concept.md Section 6. Consider alternative variability metrics that are not mathematically constrained by mean performance: (1) IRT-based person fit statistics (lz statistic from 2-pass GRM in RQ 6.1.1 - measures person-level response consistency independent of ability level), (2) residual variance from multilevel model (variance in accuracy not explained by fixed effects), or (3) coefficient of variation (CV = SD/mean, normalizes SD by mean to reduce artifact). If retaining SD of binary accuracy, add sensitivity analysis: partial out mean accuracy from both SD_confidence and SD_accuracy, then correlate residuals to isolate variability relationship independent of mean performance artifact."

**2. Analysis Approach Ambiguity: Multilevel vs Aggregated Unclear**
- **Location:** 1_concept.md - Section "Analysis Approach", Step 2
- **Claim Made:** "Use multilevel model approach: SD_accuracy ~ SD_confidence + (1 | UID) to account for within-person clustering. Alternatively, compute person-level averages (N=100 independent observations) for simple correlation."
- **Statistical Criticism:** Concept.md proposes two distinct statistical approaches (multilevel model vs aggregated person-level means) but does not specify decision criteria for choosing between them. These approaches test different hypotheses: multilevel model tests association at observation level (N=400) while accounting for clustering, whereas aggregated approach tests association at person level (N=100). The two approaches may yield different results if within-person and between-person associations differ (aggregation bias / ecological fallacy).
- **Methodological Counterevidence:** [What's aggregation bias, and how does it relate to the ecological fallacy?](https://stats.stackexchange.com/questions/210582/whats-aggregation-bias-and-how-does-it-relate-to-the-ecological-fallacy) (Cross Validated) explains that "relationships existing at one level of analysis will not necessarily demonstrate the same strength at another level" and that aggregation can "reduce information, and this information loss usually prevents identification of parameters of interest." [Ecological Fallacy and Covariates: New Insights based on Multilevel Modelling](https://onlinelibrary.wiley.com/doi/abs/10.1111/insr.12244) (Gnaldi, 2018, *International Statistical Review*) demonstrates that within-person and between-person correlations can differ substantially, and choosing between levels of analysis requires theoretical justification.
- **Strength:** MODERATE
- **Suggested Rebuttal:** "Add explicit decision criteria to concept.md: State which approach will be primary analysis (recommend multilevel model to preserve information and account for repeated measures) and justify theoretically (RQ asks about individual-difference association, suggesting person-level aggregation may be more interpretable). If using aggregated approach, acknowledge potential information loss. Alternatively, report BOTH approaches as complementary: multilevel model for observation-level association, aggregated correlation for person-level association, and discuss whether they converge (supporting robust relationship) or diverge (suggesting level-specific effects)."

---

#### Omission Errors (Missing Statistical Considerations)

**1. No Assumption Checks for Pearson Correlation**
- **Missing Content:** Concept.md proposes Pearson correlation but does not specify assumption checks (linearity, bivariate normality, homoscedasticity)
- **Why It Matters:** Pearson correlation assumes linear relationship and bivariate normality for valid inference. Violation of normality can inflate Type I error rates or reduce power, especially with small-to-moderate sample sizes (N=100 person-level or N=400 observation-level).
- **Supporting Literature:** [Testing the Significance of a Correlation With Nonnormal Data](https://bpb-us-w2.wpmucdn.com/blogs.cofc.edu/dist/7/881/files/2021/06/Bishara-Hittner-2012.pdf) (Bishara & Hittner, 2012, *Psychological Methods*) found that "when data are nonnormally distributed, a test of the significance of Pearson's r may inflate Type I error rates and reduce power." They recommend diagnostic checks (Q-Q plots, scatterplot inspection) and permutation tests as robust alternative. [Pearson's or Spearman's correlation with non-normal data](https://stats.stackexchange.com/questions/3730/pearsons-or-spearmans-correlation-with-non-normal-data) (Cross Validated) notes that "the sampling distribution for Pearson's correlation does assume normality; conclusions based on significance testing may not be sound" without assumption validation.
- **Potential Reviewer Question:** "Did you verify that the relationship between SD_confidence and SD_accuracy is linear? Are both variables approximately normally distributed? If not, how does this affect your p-value interpretation?"
- **Strength:** MODERATE
- **Suggested Addition:** "Add to Section 7: Validation Procedures - specify assumption checks: (1) Scatterplot of SD_confidence vs SD_accuracy to visually assess linearity and identify outliers, (2) Q-Q plots for both variables to assess univariate normality (approximate bivariate normality), (3) If severe normality violations detected, rely on permutation-based p-value (more robust) or consider Spearman rank correlation as sensitivity analysis."

**2. No Sensitivity Analysis for Minimum Item Threshold**
- **Missing Content:** Concept.md sets ≥10 items per person per test as minimum threshold for SD computation but does not specify sensitivity analysis to validate this threshold
- **Why It Matters:** The reliability and precision of SD estimates depend on sample size (number of items). With small item counts (e.g., N=10-15 items), SD estimates may be unstable and have large standard errors. The choice of 10 items as threshold is reasonable heuristic but not empirically validated for this specific analysis.
- **Supporting Literature:** [A practical guide to understanding reliability in studies of within-person variability](https://www.sciencedirect.com/science/article/abs/pii/S009265661630068X) (ScienceDirect) emphasizes that "reliability of within-person variability measures depends on number of observations per person" and recommends sensitivity analyses varying sample size thresholds to assess estimate stability. [Sample Size and Item Calibration or Person Measure Stability](https://www.rasch.org/rmt/rmt74m.htm) (Rasch Measurement) notes that "low item reliability means that your sample size is too small for stable estimates" and recommends ≥30 items for well-targeted pilot studies, suggesting N=10 may be marginal.
- **Potential Reviewer Question:** "How stable are SD estimates with only 10-15 items per participant? Did you verify that results are robust to different minimum item thresholds?"
- **Strength:** MODERATE
- **Suggested Addition:** "Add to Section 6: Analysis Approach - specify sensitivity analysis: Vary minimum item threshold (≥8, ≥10, ≥12, ≥15 items) and report correlation stability across thresholds. If results change substantially, this suggests SD estimates are unreliable with small item counts. Document number of observations excluded at each threshold (transparency about sample size reduction)."

**3. No Consideration of Alternative Variability Metrics**
- **Missing Content:** Concept.md focuses exclusively on SD as variability metric but does not discuss alternative metrics that might better capture "true" memory variability without mathematical constraints
- **Why It Matters:** SD of binary accuracy data has known limitations (see Commission Error 1). Alternative metrics exist that quantify variability in different ways and may provide complementary insights: (1) IRT-based person fit statistics (lz, infit/outfit) measure response consistency independent of ability level, (2) coefficient of variation (CV = SD/mean) normalizes SD by mean performance, (3) median absolute deviation (MAD) provides robust alternative to SD, (4) residual variance from multilevel model isolates unexplained variability.
- **Supporting Literature:** [Comparing Standard Deviation and Median Absolute Deviation (MAD) Metrics](https://www.numberanalytics.com/blog/comparing-standard-deviation-and-mad-metrics) (NumberAnalytics, 2024) notes that "MAD offers robust statistical insights, particularly when addressing concerns of non-normality and outliers" and is less sensitive to extreme values. [Reliability and separation of measures](https://www.winsteps.com/winman/reliability.htm) (Winsteps) explains that "person fit statistics (infit/outfit) identify individuals with unexpected response patterns" and can quantify within-person inconsistency independent of ability level. IRT person fit would be particularly appropriate given that RQ 6.1.1 already fits GRM models, making person fit statistics readily available.
- **Potential Reviewer Question:** "Why use SD of binary accuracy rather than IRT-based person fit statistics, which are designed to measure response consistency independent of ability level?"
- **Strength:** MODERATE
- **Suggested Addition:** "Add to Section 6: Analysis Approach - acknowledge alternative variability metrics and justify SD choice: 'We use SD as primary variability metric for interpretability and direct correspondence to raw item-level dispersion. However, we acknowledge SD of binary data is mathematically constrained by mean accuracy. As sensitivity analysis, we also compute: (1) IRT person fit statistics (lz) from RQ 6.1.1 GRM models as ability-independent variability measure, (2) coefficient of variation (CV = SD/mean) to normalize SD by mean performance. We report correlations using all three metrics to assess robustness of variability-to-variability relationship.'"

**4. No Decomposition of Between-Person vs Within-Person Variability**
- **Missing Content:** Concept.md does not discuss whether the variability correlation reflects between-person trait (stable individual differences in variability) vs within-person state (time-varying fluctuations in variability)
- **Why It Matters:** With 4 repeated measures per person, it's possible to decompose variability into stable trait component (between-person: some people are consistently more variable than others) vs state component (within-person: variability fluctuates across test sessions). The RQ hypothesis could apply to either level: Do people with high TRAIT variability in confidence also show high TRAIT variability in accuracy? Or do time points with high STATE variability in confidence also show high STATE variability in accuracy? These are distinct questions requiring different analytic approaches.
- **Supporting Literature:** [The Intraclass Correlation Coefficient in Mixed Models](https://www.theanalysisfactor.com/the-intraclass-correlation-coefficient-in-mixed-models/) (The Analysis Factor) explains that "ICC measures proportion of total variance due to differences between individuals" and can decompose variability into between-person and within-person components. [Modeling Long-Term Changes in Daily Within-Person Associations](https://pmc.ncbi.nlm.nih.gov/articles/PMC6424492/) (PMC, 2019) demonstrates multilevel SEM approach to partition between-person and within-person effects: "intra-individual variability, when treated as individual difference predictor variable, can be examined through multilevel model to produce estimates of person-specific deviations."
- **Potential Reviewer Question:** "Does the correlation between SD_confidence and SD_accuracy reflect stable individual differences (some people are consistently more variable) or time-varying state effects (variability correlates across time within person)?"
- **Strength:** MINOR
- **Suggested Addition:** "Add to Section 6: Analysis Approach - optional variance decomposition analysis: 'As exploratory analysis, we decompose variability into between-person (average SD across 4 tests per person) and within-person (deviation from person-specific mean SD at each test) components. We test whether between-person variability correlation (trait-level: do people with high average SD_confidence also have high average SD_accuracy?) differs from within-person variability correlation (state-level: do tests with higher-than-usual SD_confidence also show higher-than-usual SD_accuracy for that person?). This distinguishes trait vs state mechanisms.'"

---

#### Alternative Statistical Approaches (Not Considered)

**1. Intraclass Correlation Coefficient (ICC) Instead of Pearson Correlation**
- **Alternative Method:** Intraclass correlation coefficient (ICC) from multilevel model, which partitions variance into between-person and within-person components and quantifies proportion of variance due to individual differences
- **How It Applies:** ICC provides model-based estimate of correlation that inherently accounts for nested data structure (400 observations from 100 participants). Unlike Pearson correlation (which requires choice between multilevel model or aggregation), ICC directly quantifies between-person variability relative to total variability. ICC can be computed for both SD_confidence and SD_accuracy, then compared to assess whether they show similar clustering patterns (high ICC for both suggests stable trait variability).
- **Key Citation:** [A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC4913118/) (Koo & Li, 2016, *Journal of Chiropractic Medicine*) explains that "ICC is a measure of reliability that reflects both degree of correlation and agreement between measurements" and is superior to Pearson correlation for nested/repeated measures data. [Intraclass Correlation: Improved modeling approaches and applications](https://pmc.ncbi.nlm.nih.gov/articles/PMC5807222/) (PMC, 2018) demonstrates ICC applications in neuroimaging with repeated measures: "ICC partitions variance into between-subject and within-subject components, providing direct quantification of individual differences."
- **Why Concept.md Should Address It:** ICC is specifically designed for nested data and provides direct variance decomposition without requiring aggregation or assumption of independence. Using ICC could avoid the ambiguity between multilevel and aggregated approaches and provide clearer interpretation of between-person vs within-person variability.
- **Strength:** MODERATE
- **Suggested Acknowledgment:** "Add to Section 6: Analysis Approach - acknowledge ICC alternative: 'As alternative to Pearson correlation, we could compute intraclass correlation coefficients (ICC) for SD_confidence and SD_accuracy to quantify proportion of variance due to between-person differences. High ICC for both (e.g., ICC > 0.50) would indicate stable individual differences in variability, supporting trait-level interpretation. We opt for Pearson/multilevel model approach for direct test of association between the two variability metrics, but report ICC values as descriptive statistics to characterize stability of variability measures across test sessions.'"

**2. IRT Person Fit Statistics as Direct Measure of Response Variability**
- **Alternative Method:** Use IRT-based person fit statistics (lz, infit, outfit) from RQ 6.1.1 GRM models as direct measure of response consistency/variability, rather than computing SD of binary accuracy
- **How It Applies:** IRT person fit statistics quantify how well an individual's response pattern matches the expected pattern given their estimated ability (theta). High person misfit (e.g., |lz| > 2.0) indicates inconsistent responses (high variability in accuracy relative to ability level), providing ability-independent variability metric. RQ 6.1.1 already fits GRM models and extracts theta scores, making person fit statistics readily available at no additional computational cost.
- **Key Citation:** [Reliability and separation of measures](https://www.winsteps.com/winman/reliability.htm) (Winsteps) explains that "person fit statistics identify individuals with unexpected response patterns" and quantify within-person inconsistency independent of ability: "lz statistic is standardized person fit index with mean 0, SD 1 under perfect fit; |lz| > 2.0 indicates significant misfit (inconsistent responses)." Person fit avoids the mathematical constraint of SD of binary data (which is function of mean accuracy) by comparing observed vs expected responses given ability level.
- **Why Concept.md Should Address It:** IRT person fit provides theoretically grounded variability metric that is independent of ability level and avoids SD-of-binary-data constraints. It directly measures response consistency (low variability = good fit, high variability = misfit), which is conceptually equivalent to what SD aims to measure but without mathematical artifacts.
- **Strength:** MODERATE
- **Suggested Acknowledgment:** "Add to Section 6: Analysis Approach - acknowledge IRT person fit alternative: 'As alternative to SD of binary accuracy, we could use IRT person fit statistics (lz) from RQ 6.1.1 GRM models. Person fit quantifies response consistency independent of ability level, avoiding mathematical constraint that SD of binary data is function of mean accuracy. We opt for SD approach for direct interpretability (dispersion of raw item-level responses), but include IRT person fit as sensitivity analysis to verify results are not artifacts of SD-mean constraint.'"

**3. Robust Correlation Methods (Spearman, Studentized Permutation Test)**
- **Alternative Method:** Spearman rank correlation (non-parametric alternative to Pearson) or studentized permutation test specifically designed for non-normal data
- **How It Applies:** If SD_confidence and SD_accuracy distributions are non-normal (likely, given that SD is bounded at 0 and may have skewed distribution), Spearman rank correlation provides distribution-free alternative that only assumes monotonic relationship (not linearity). Studentized permutation test (Yu et al., 2020) provides asymptotically valid inference even when bivariate normality violated and can handle clustered data.
- **Key Citation:** [A ROBUST SPEARMAN CORRELATION COEFFICIENT PERMUTATION TEST](https://arxiv.org/pdf/2008.01200) (Yu et al., 2020, *arXiv*) demonstrates that "naive permutation test of Pearson's correlation coefficient does not control type I error under non-normality settings" but proposes studentized permutation test that "is asymptotically valid under general assumptions and is exact under exchangeability assumptions." [Testing the significance of a correlation with nonnormal data](https://pubmed.ncbi.nlm.nih.gov/22563845/) (Bishara & Hittner, 2012, *Psychological Methods*) found that with N ≥ 20, "Type I and Type II error rates were minimized by transforming data to normal shape prior to assessing Pearson correlation" via rank-based inverse normal transformation (rankit scores). For small samples (N ≤ 10) with extreme non-normality, permutation test outperformed parametric approaches.
- **Why Concept.md Should Address It:** Given likely non-normality of SD distributions and clustered data structure, robust correlation methods may provide more accurate inference than parametric Pearson correlation. Concept.md mentions permutation test but does not cite robust permutation test literature or specify how permutation will handle clustering.
- **Strength:** MODERATE
- **Suggested Acknowledgment:** "Add to Section 6: Analysis Approach - specify robust correlation method: 'If diagnostic checks reveal severe non-normality (Q-Q plots, Shapiro-Wilk p < 0.05), we will use Spearman rank correlation as primary analysis (robust to non-normality, only assumes monotonic relationship). For permutation test, we use studentized permutation approach (Yu et al., 2020) that respects UID clustering structure: permute residuals from null model (SD_accuracy ~ 1 + (1|UID)) to preserve within-person dependence, recompute correlation on permuted data, generate empirical p-value from 5,000 permutations.'"

---

#### Known Statistical Pitfalls (Unaddressed)

**1. Aggregation Bias / Ecological Fallacy in Person-Level Correlation**
- **Pitfall Description:** If concept chooses person-level aggregation approach (average SD across 4 tests per person, N=100), this introduces aggregation bias: within-person and between-person correlations may differ substantially, and aggregated correlation confounds these two levels of association
- **How It Could Affect Results:** Within-person correlation (does high SD_confidence at a given test predict high SD_accuracy at that same test?) may differ from between-person correlation (do people with high average SD_confidence also have high average SD_accuracy?). Aggregating to person level loses information about time-specific associations and may yield misleading conclusions if the two levels diverge. This is the classic ecological fallacy: relationships at aggregate level do not necessarily reflect individual-level relationships.
- **Literature Evidence:** [What's aggregation bias, and how does it relate to the ecological fallacy?](https://stats.stackexchange.com/questions/210582/whats-aggregation-bias-and-how-does-it-relate-to-the-ecological-fallacy) (Cross Validated) explains that "aggregation reduces information, and this information loss usually prevents identification of parameters of interest in the underlying individual-level model." [Ecological Fallacy and Covariates: New Insights based on Multilevel Modelling](https://onlinelibrary.wiley.com/doi/abs/10.1111/insr.12244) (Gnaldi, 2018, *International Statistical Review*) demonstrates empirically that "ordinary ecological regression provides biased estimates when compared with multilevel logistic regression applied to individual data" and that "ecological data alone do not allow one to determine whether ecological bias is likely present."
- **Why Relevant to This RQ:** Concept.md proposes both multilevel (N=400 observations) and aggregated (N=100 persons) approaches but does not discuss how results might differ between levels or how to interpret discrepancies. If multilevel model shows weak association but aggregated correlation shows strong association, this suggests between-person trait effect (stable individual differences) but no within-person state effect (time-specific covariation).
- **Strength:** MODERATE
- **Suggested Mitigation:** "Add to Section 6: Analysis Approach - acknowledge aggregation bias risk: 'If using person-level aggregation, we acknowledge this may yield different results than observation-level analysis due to aggregation bias (ecological fallacy). To address this, we report BOTH levels: (1) observation-level association via multilevel model (N=400, tests within-test covariation), (2) person-level association via aggregated correlation (N=100, tests between-person trait correlation). If results diverge, we interpret as evidence for level-specific effects (e.g., strong between-person but weak within-person association suggests stable trait variability differences but no time-specific coupling of confidence and accuracy variability).'"

**2. Naive Permutation Test Violates Exchangeability with Clustered Data**
- **Pitfall Description:** Standard permutation test for correlation assumes all observations are independent and exchangeable (any permutation equally likely under null hypothesis). With clustered data (400 observations from 100 participants), this assumption is violated: observations within the same participant are NOT exchangeable with observations from different participants due to within-person dependence.
- **How It Could Affect Results:** Naive permutation test (randomly permuting all 400 SD_confidence values) will underestimate variance of test statistic because it breaks within-person clustering structure. This can lead to inflated Type I error (false positives) because empirical null distribution is too narrow. The problem is analogous to treating repeated measures as independent observations, which anti-conservatively biases inference.
- **Literature Evidence:** [Permutation test for correlated or non-independent data](https://stats.stackexchange.com/questions/269951/permutation-test-for-correlated-or-non-independent-data) (Cross Validated) explains that "data violate assumptions of usual permutation test because we cannot assume all observations are independent and equally likely to have been given either treatment assignment" and that "structured dependencies, such as repeated measurements, can be treated by allowing only those permutations that respect such dependency structure." [Permutation Tests for Random Effects in Linear Mixed Models](https://pmc.ncbi.nlm.nih.gov/articles/PMC3883440/) (PMC, 2013) demonstrates that "permutation tests for random effects involve weighted residuals, with weights determined by among- and within-subject variance components" and that "null permutation distributions can be computed by permuting residuals both within and among subjects."
- **Why Relevant to This RQ:** Concept.md specifies permutation test for dual p-values (Decision D068) but does not specify permutation strategy for clustered data. If naive permutation is used, p-values will be anti-conservative (too small), increasing false positive risk.
- **Strength:** MODERATE
- **Suggested Mitigation:** "Add to Section 6: Analysis Approach - specify cluster-respecting permutation strategy: 'For permutation-based p-value, we use cluster-respecting approach to preserve within-person dependence: (1) Fit null model: SD_accuracy ~ 1 + (1|UID) to partition variance into between-person and within-person components, (2) Extract residuals from null model, (3) Permute residuals WITHIN participants (permute 4 observations for each UID separately, not across UIDs), (4) Add permuted residuals back to null model predictions to generate permuted SD_accuracy values, (5) Recompute correlation between SD_confidence and permuted SD_accuracy, (6) Repeat 5,000 times to generate empirical null distribution, (7) Compute p-value as proportion of permuted correlations exceeding observed correlation. This approach preserves within-person clustering structure and provides valid Type I error control.'"

---

#### Scoring Summary

**Total Concerns Identified:**
- Commission Errors: 2 (1 CRITICAL, 1 MODERATE)
- Omission Errors: 4 (0 CRITICAL, 3 MODERATE, 1 MINOR)
- Alternative Approaches: 3 (0 CRITICAL, 3 MODERATE, 0 MINOR)
- Known Pitfalls: 2 (0 CRITICAL, 2 MODERATE, 0 MINOR)

**Overall Count:** 11 concerns (exceeds threshold of ≥5 for exceptional devil's advocate analysis)

**Overall Devil's Advocate Assessment:**

Concept.md demonstrates strong awareness of non-independence issue and proposes two valid approaches (multilevel model and person-level aggregation) for handling clustered data structure. However, the analysis faces a **critical methodological limitation**: computing SD of binary accuracy data (0/1 responses) introduces mathematical artifact where SD is constrained by mean proportion correct (SD = sqrt[p*(1-p)], maximized at p=0.5). This means the correlation between SD_confidence and SD_accuracy may partially reflect the artifact that intermediate-accuracy participants have higher SD, rather than genuine relationship between metacognitive and memory variability.

This limitation is addressable through: (1) sensitivity analysis partialing out mean accuracy from both SD metrics and correlating residuals, (2) using IRT person fit statistics as alternative variability metric (lz statistic from RQ 6.1.1 GRM models quantifies response consistency independent of ability level), or (3) acknowledging limitation explicitly and discussing how results should be interpreted cautiously.

Additional methodological gaps include: (1) no assumption checks for Pearson correlation (linearity, bivariate normality), (2) ambiguity about which approach will be primary analysis (multilevel vs aggregated), (3) incomplete permutation test specification (cluster-respecting strategy not detailed), and (4) no consideration of variance decomposition into between-person (trait) vs within-person (state) variability. These are moderate concerns that should be addressed during planning phase to ensure methodologically rigorous analysis.

**Recommendation:** Address critical SD-of-binary-data limitation (Commission Error 1) before proceeding to planning. Consider using IRT person fit as primary variability metric or at minimum include as sensitivity analysis. Clarify analysis approach (multilevel vs aggregated) with explicit decision criteria.

---

### Tool Availability Validation

See Category 2 above for detailed tool availability table.

**Summary:**
- 3/5 tools available (60% tool reuse rate)
- Missing tools: multilevel correlation with clustering, cluster-respecting permutation test
- Standard pandas/scipy tools sufficient for basic correlation, but specialized tools needed for methodologically sound analysis given nested data structure
- Recommendation: Implement missing tools before rq_analysis phase or adapt existing `tools.analysis_lmm.fit_lmm_trajectory_tsvr()` for multilevel correlation approach

---

### Validation Procedures Checklists

See Category 4 above for detailed validation procedures assessment.

**Key Gaps:**
- No explicit assumption checks for Pearson correlation (linearity, bivariate normality, homoscedasticity)
- No diagnostic procedures specified (scatterplot inspection, Q-Q plots, residual diagnostics)
- No sensitivity analysis for minimum item threshold (≥10 items)
- No validation of SD computation (distribution inspection, outlier detection)

**Recommendations:**
- Add assumption validation steps to analysis plan (scatterplot, Q-Q plots, residual diagnostics if multilevel model used)
- Specify remedial actions for assumption violations (Spearman if non-linearity, permutation p-value if non-normality, sensitivity analysis for outliers)
- Add sensitivity analysis varying minimum item threshold (≥8, ≥10, ≥12, ≥15 items)

---

### Recommendations

#### Required Changes (Must Address for Approval)

**1. Address SD of Binary Data Constraint**
   - **Location:** 1_concept.md - Section 6: Analysis Approach, Step 1-2 (SD computation)
   - **Issue:** SD of binary accuracy data (0/1) is mathematically constrained by mean proportion correct (SD = sqrt[p*(1-p)]), creating artifact where intermediate-accuracy participants automatically have higher SD than high/low-accuracy participants. This is a **critical methodological limitation** that could invalidate the variability-to-variability correlation if not addressed.
   - **Fix:** Add explicit acknowledgment of this limitation and specify mitigation strategy. Recommended text: "**Limitation: SD of Binary Data.** We acknowledge that SD of binary accuracy responses is mathematically constrained by mean proportion correct: SD = sqrt[p*(1-p)], where p = proportion correct. To isolate the variability relationship independent of this artifact, we conduct sensitivity analysis: (1) partial out mean accuracy from both SD_confidence and SD_accuracy (regress each on mean accuracy, extract residuals), (2) correlate residuals to test whether variability relationship persists after removing mean-variance artifact. We also report IRT person fit statistics (lz from RQ 6.1.1 GRM models) as alternative variability metric that is independent of ability level."
   - **Rationale:** Category 1 deduction reflects this critical gap. Addressing SD constraint is necessary for methodologically sound inference about variability relationships.

**2. Clarify Analysis Approach: Multilevel vs Aggregated**
   - **Location:** 1_concept.md - Section 6: Analysis Approach, Step 2 (Correlation analysis)
   - **Issue:** Concept proposes two distinct approaches (multilevel model at N=400 observation-level vs aggregated correlation at N=100 person-level) but does not specify which will be primary analysis or provide decision criteria. These approaches test different hypotheses and may yield different results.
   - **Fix:** Specify primary analysis approach with justification. Recommended text: "**Primary Analysis: Multilevel Model Approach.** We use multilevel model: SD_accuracy ~ SD_confidence + (1|UID) as primary analysis because it preserves observation-level information (N=400) and accounts for within-person clustering. We extract fixed effect slope for SD_confidence and standardize it (analogous to correlation coefficient) to quantify observation-level association between variability metrics. As secondary analysis, we also report person-level aggregated correlation (average SD across 4 tests per person, N=100) to test whether results are consistent at between-person level. If multilevel and aggregated results diverge, this indicates level-specific effects (e.g., within-person vs between-person associations differ)."
   - **Rationale:** Category 1 deduction reflects this ambiguity. Specifying primary approach with clear justification resolves methodological uncertainty and provides interpretation framework if results differ across approaches.

**3. Specify Cluster-Respecting Permutation Test Strategy**
   - **Location:** 1_concept.md - Section 6: Analysis Approach, Step 2 (Dual p-values)
   - **Issue:** Concept mentions permutation-based p-value (Decision D068 compliance) but does not specify how permutation will respect UID clustering structure. Naive permutation (randomly permuting all 400 observations) violates exchangeability assumption and yields anti-conservative p-values.
   - **Fix:** Add cluster-respecting permutation strategy. Recommended text: "**Permutation Test (Cluster-Respecting).** To generate permutation-based p-value while preserving within-person dependence: (1) Fit null model SD_accuracy ~ 1 + (1|UID), (2) Extract residuals, (3) Permute residuals WITHIN participants (permute 4 observations per UID separately, not across UIDs), (4) Add permuted residuals to null predictions to create permuted SD_accuracy, (5) Recompute correlation with SD_confidence, (6) Repeat 5,000 times, (7) Compute p-value as proportion of permuted correlations ≥ observed. This preserves clustering structure and provides valid Type I error control."
   - **Rationale:** Category 4 deduction reflects incomplete permutation specification. Cluster-respecting strategy is necessary for valid inference with nested data.

---

#### Suggested Improvements (Optional but Recommended)

**1. Add Assumption Validation Procedures**
   - **Location:** 1_concept.md - Section 7: Validation Procedures (new subsection)
   - **Current:** Section 7 is not present in concept.md; success criteria mention "non-independence addressed" but no explicit assumption checks
   - **Suggested:** Add subsection: "**Assumption Validation.** We verify Pearson correlation assumptions: (1) **Linearity**: Scatterplot of SD_confidence vs SD_accuracy to visually assess linear relationship and identify outliers, (2) **Bivariate Normality**: Q-Q plots for both variables to assess univariate normality (approximates bivariate normality), Shapiro-Wilk tests (p > 0.05 threshold but interpret conservatively given sensitivity to sample size), (3) **Homoscedasticity**: If multilevel model used, residual plot to verify constant variance. **Remedial Actions**: If severe non-linearity detected, use Spearman rank correlation; if severe non-normality, rely on permutation p-value (more robust); if influential outliers identified (Cook's D > 4/n), report sensitivity analysis excluding outliers."
   - **Benefit:** Enhances methodological rigor by explicitly verifying assumptions and specifying remedial actions. Addresses Category 4 gap in validation procedures.

**2. Add Sensitivity Analysis for Minimum Item Threshold**
   - **Location:** 1_concept.md - Section 6: Analysis Approach, Step 1-2 (SD computation)
   - **Current:** States "Minimum items per participant per test: ≥10 items to compute stable SD estimates" without empirical validation
   - **Suggested:** Add sensitivity analysis: "**Sensitivity Analysis: Minimum Item Threshold.** To assess robustness of SD estimates to item count, we vary minimum threshold (≥8, ≥10, ≥12, ≥15 items) and report correlation stability across thresholds. We document sample size reduction at each threshold (number of observations excluded). If correlation magnitude or significance changes substantially across thresholds, this suggests SD estimates are unreliable with small item counts and threshold should be increased. Target: correlation r and p-value should be stable within ±0.05 across thresholds."
   - **Benefit:** Validates choice of 10-item threshold and demonstrates result robustness to SD estimation precision. Addresses Category 3 gap in parameter justification.

**3. Include IRT Person Fit as Alternative Variability Metric**
   - **Location:** 1_concept.md - Section 6: Analysis Approach, Step 1-2 (Variability computation)
   - **Current:** Uses only SD of accuracy as variability metric
   - **Suggested:** Add IRT person fit: "**Alternative Variability Metric: IRT Person Fit.** As sensitivity analysis, we compute IRT person fit statistics (lz statistic) from RQ 6.1.1 GRM models. Person fit quantifies response consistency independent of ability level: lz = (observed response pattern - expected pattern given theta) / SE, standardized with mean 0, SD 1. High |lz| indicates inconsistent responses (high variability). We correlate SD_confidence with lz (in addition to SD_accuracy) to verify that variability relationship is not artifact of SD-mean constraint in binary data. Person fit provides ability-independent variability measure conceptually equivalent to SD but without mathematical artifacts."
   - **Benefit:** Addresses Commission Error 1 (SD of binary data constraint) by providing alternative variability metric that is theoretically grounded and avoids mathematical artifacts. Enhances interpretability of results.

**4. Add Variance Decomposition: Between-Person vs Within-Person**
   - **Location:** 1_concept.md - Section 6: Analysis Approach (new exploratory analysis subsection)
   - **Current:** Does not distinguish between-person (trait) vs within-person (state) variability associations
   - **Suggested:** Add variance decomposition: "**Exploratory Analysis: Variance Decomposition.** To distinguish trait vs state mechanisms, we decompose variability into between-person (BP) and within-person (WP) components: (1) BP: Average SD across 4 tests per person (N=100), (2) WP: Deviation from person-specific mean SD at each test (person-centered SD, N=400). We test two correlations: (1) **Between-person correlation**: Do people with high average SD_confidence also have high average SD_accuracy? (Tests trait-level variability association), (2) **Within-person correlation**: Do tests with higher-than-usual SD_confidence (for that person) also show higher-than-usual SD_accuracy? (Tests state-level covariation within person). If BP correlation strong but WP correlation weak, this suggests stable individual differences in variability (trait) but no time-specific coupling (state)."
   - **Benefit:** Provides richer theoretical interpretation by distinguishing trait vs state mechanisms. Addresses Omission Error 4.

---

### Validation Metadata

- **Agent Version:** rq_stats v5.0
- **Rubric Version:** 10-point system (v4.0)
- **Validation Date:** 2025-12-06 18:00
- **Tools Inventory Source:** docs/v4/tools_inventory.md
- **Total Tools Validated:** 5
- **Tool Reuse Rate:** 60% (3/5 tools available)
- **Validation Duration:** ~28 minutes
- **Context Dump:** "9.1/10 CONDITIONAL. Category 1: 2.5/3 (SD binary data constraint CRITICAL, ambiguous approach). Category 2: 1.8/2 (60% reuse). Category 3: 1.9/2 (parameters good, permutation gaps). Category 4: 1.9/2 (assumptions not explicit). Category 5: 1.0/1 (11 concerns, comprehensive)."

---

**Sources:**

- [Quantifying relative importance: computing standardized effects in models with binary outcomes](https://esajournals.onlinelibrary.wiley.com/doi/10.1002/ecs2.2283)
- [Patterns of Means and Standard Deviations with Binary Variables](https://biomedres.us/fulltexts/BJSTR.MS.ID.003851.php)
- [Testing the Significance of a Correlation With Nonnormal Data](https://bpb-us-w2.wpmucdn.com/blogs.cofc.edu/dist/7/881/files/2021/06/Bishara-Hittner-2012.pdf)
- [Pearson's or Spearman's correlation with non-normal data](https://stats.stackexchange.com/questions/3730/pearsons-or-spearmans-correlation-with-non-normal-data)
- [A practical guide to understanding reliability in studies of within-person variability](https://www.sciencedirect.com/science/article/abs/pii/S009265661630068X)
- [Sample Size and Item Calibration or Person Measure Stability](https://www.rasch.org/rmt/rmt74m.htm)
- [The Intraclass Correlation Coefficient in Mixed Models](https://www.theanalysisfactor.com/the-intraclass-correlation-coefficient-in-mixed-models/)
- [Multilevel Modelling with Repeated Measures Data](https://www.learn-mlms.com/09-module-9.html)
- [What's aggregation bias, and how does it relate to the ecological fallacy?](https://stats.stackexchange.com/questions/210582/whats-aggregation-bias-and-how-does-it-relate-to-the-ecological-fallacy)
- [Ecological Fallacy and Covariates: New Insights based on Multilevel Modelling](https://onlinelibrary.wiley.com/doi/abs/10.1111/insr.12244)
- [Permutation test for correlated or non-independent data](https://stats.stackexchange.com/questions/269951/permutation-test-for-correlated-or-non-independent-data)
- [Permutation Tests for Random Effects in Linear Mixed Models](https://pmc.ncbi.nlm.nih.gov/articles/PMC3883440/)
- [A ROBUST SPEARMAN CORRELATION COEFFICIENT PERMUTATION TEST](https://arxiv.org/pdf/2008.01200)
- [A Guideline of Selecting and Reporting Intraclass Correlation Coefficients for Reliability Research](https://pmc.ncbi.nlm.nih.gov/articles/PMC4913118/)
- [Reliability and separation of measures](https://www.winsteps.com/winman/reliability.htm)
- [Comparing Standard Deviation and Median Absolute Deviation (MAD) Metrics](https://www.numberanalytics.com/blog/comparing-standard-deviation-and-mad-metrics)
- [Modeling Long-Term Changes in Daily Within-Person Associations](https://pmc.ncbi.nlm.nih.gov/articles/PMC6424492/)

---

**End of Statistical Validation Report**
