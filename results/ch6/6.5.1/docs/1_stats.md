---

## Statistical Validation Report

**Validation Date:** 2025-12-06 18:15
**Agent:** rq_stats v5.0
**Status:** ⚠️ CONDITIONAL
**Overall Score:** 9.1 / 10.0

---

### Rubric Scoring Summary

| Category | Score | Max | Status |
|----------|-------|-----|--------|
| Statistical Appropriateness | 2.8 | 3.0 | ✅ |
| Tool Availability | 2.0 | 2.0 | ✅ |
| Parameter Specification | 1.8 | 2.0 | ⚠️ |
| Validation Procedures | 1.7 | 2.0 | ⚠️ |
| Devil's Advocate Analysis | 0.8 | 1.0 | ⚠️ |
| **TOTAL** | **9.1** | **10.0** | **⚠️ CONDITIONAL** |

---

### Detailed Rubric Evaluation

#### Category 1: Statistical Appropriateness (2.8 / 3.0)

**Criteria Checklist:**
- [x] Statistical approach appropriate for RQ (GRM for ordinal confidence, LMM for trajectories)
- [x] Assumptions checkable with N=100, 4 time points (though sample size marginal for multidimensional GRM)
- [x] Methodologically sound with appropriate complexity (3-factor GRM + interaction LMM justified)
- [ ] Sample size adequacy explicitly justified for multidimensional GRM (missing power analysis)

**Assessment:**

The concept proposes a methodologically rigorous two-stage approach: (1) multidimensional GRM (3 factors: Common/Congruent/Incongruent) to derive theta_confidence scores from 5-category ordinal Likert confidence ratings, followed by (2) LMM with Schema × Time interaction to test trajectory differences. This approach is appropriate for the research question and data structure.

**Strengths:**
- GRM correctly chosen for ordinal confidence data (NOT 2PL binary model - appropriate for 5-category Likert scale)
- Multidimensional IRT structure (3 factors) aligns with theoretical schema congruence framework
- LMM with interaction term directly addresses primary hypothesis (schema effects on confidence trajectories)
- Two-pass purification workflow (Decision D039) appropriate for ensuring item quality before Pass 2
- TSVR time variable (actual hours) more precise than nominal days (Decision D070)
- Complexity justified: 3-factor structure theoretically motivated by schema congruence levels, not exploratory fishing

**Concerns / Gaps:**
- **Sample size marginal for multidimensional GRM:** Literature indicates N=500+ recommended for 3-dimensional GRM with adequate parameter recovery ([Frontiers in Psychology, 2016](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.00109/full)). With N=100 participants × 4 tests = 400 observations total (but only 100 independent units), discrimination parameters may show poor estimation, especially for weaker items. Convergence issues documented for multidimensional GRM with N<200 ([Frontiers in Education, 2021](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2021.721963/full)).
- No explicit acknowledgment of small-sample limitations for 3-factor GRM calibration
- Power analysis not mentioned for LMM interaction test (N=100, 4 time points, 3-level schema factor)

**Score Justification:**

Strong methodological approach with appropriate model selection and justified complexity. GRM for ordinal data is correct choice, and 3-factor structure is theoretically motivated. Deduction from perfect score due to missing explicit justification for sample size adequacy in multidimensional GRM context and lack of power analysis for interaction test. Score: 2.8/3.0 (Strong category, 93%).

---

#### Category 2: Tool Availability (2.0 / 2.0)

**Source:** `docs/v4/tools_catalog.md`

**Analysis Pipeline Steps:**

| Step | Tool Function | Status | Notes |
|------|---------------|--------|-------|
| Step 0: Extract TC_* Data | `tools.data.extract_from_dfData` | ✅ Available | Standard extraction, filters TC_* tags with i1-i6 patterns |
| Step 1: IRT Pass 1 (GRM) | `tools.analysis_irt.calibrate_irt` | ✅ Available | 3-factor GRM with Q-matrix, p1_med prior |
| Step 2: Purify Items | `tools.analysis_irt.filter_items_by_quality` | ✅ Available | Decision D039: |b| ≤ 3.0, a ≥ 0.4 thresholds |
| Step 3: IRT Pass 2 (GRM) | `tools.analysis_irt.calibrate_irt` | ✅ Available | Re-calibration on purified items |
| Step 4: Merge TSVR | `tools.lmm.fit_lmm_trajectory_tsvr` | ✅ Available | Decision D070: TSVR time variable support |
| Step 5: Fit LMM | `tools.lmm.fit_lmm_trajectory_tsvr` | ✅ Available | Schema × Time interaction, random slopes |
| Step 6: Post-hoc Contrasts | `tools.lmm.compute_contrasts_pairwise` | ✅ Available | Decision D068: dual p-values (uncorrected + Bonferroni) |
| Step 7: Compare to Ch5 | Manual comparison | ⚠️ Manual | Comparison to RQ 5.4.1 accuracy findings (no tool needed) |

**Tool Reuse Rate:** 6/7 analysis steps (86%)

**Missing Tools:**
None. Step 7 is conceptual comparison (manual documentation), not automated tool requirement.

**Tool Availability Assessment:**

All required analysis tools exist in `tools/` package with appropriate API signatures verified in tools_catalog.md. GRM calibration supports multidimensional models via Q-matrix specification. LMM tools support TSVR time variable (Decision D070) and dual p-value reporting (Decision D068). Purification thresholds align with Decision D039. Tool reuse rate of 86% is acceptable (just below 90% target, but Step 7 is manual comparison not requiring tool).

**Score:** 2.0 / 2.0 (Exceptional - 100% of required analysis tools available)

---

#### Category 3: Parameter Specification (1.8 / 2.0)

**Criteria Checklist:**
- [x] GRM parameters specified (3-factor Q-matrix, p1_med prior, 5-category ordinal)
- [x] Purification thresholds stated (|b| ≤ 3.0, a ≥ 0.4)
- [x] LMM structure specified (Schema × Time interaction, random slopes)
- [ ] IRT prior distribution justification missing (why p1_med chosen?)
- [ ] Sensitivity analysis for purification thresholds not mentioned
- [ ] LMM random structure selection strategy not specified (maximal vs parsimonious?)

**Assessment:**

Key parameters are explicitly stated: 3-factor GRM with Common/Congruent/Incongruent factors mapped via Q-matrix, purification thresholds from Decision D039 (|b| ≤ 3.0, a ≥ 0.4), LMM with Schema × Time interaction and random slopes by UID, TSVR time variable, dual p-value reporting (Decision D068).

**Strengths:**
- GRM structure clearly specified: 3 factors with i1-i6 tag mapping to factors
- 5-category ordinal response format explicitly stated (0, 0.25, 0.5, 0.75, 1.0 values)
- Purification thresholds cited from Decision D039 (project-wide standard)
- Time variable specification clear: TSVR (actual hours) per Decision D070, not nominal days
- Post-hoc correction method specified: Bonferroni per Decision D068

**Concerns / Gaps:**
- **IRT prior not justified:** Concept states "p1_med prior" for GRM but provides no rationale for this choice over alternatives (weakly informative, empirical Bayes, etc.)
- **No sensitivity analysis planned:** Purification thresholds (|b| ≤ 3.0, a ≥ 0.4) are stated but no plan to test sensitivity to these cutoffs (e.g., what if a ≥ 0.3 or a ≥ 0.5?)
- **Random structure selection ambiguous:** Concept proposes "random slopes by UID" but doesn't specify selection strategy. Will maximal model (random intercepts + random slopes for Schema + Time) be attempted first, or parsimonious model-building approach? Literature recommends parsimonious selection via LRT when N<200 ([Stack Exchange discussion](https://stats.stackexchange.com/questions/524599/what-are-the-arguments-in-favor-and-against-using-random-slopes)).
- **No convergence contingency:** What if 3-factor GRM fails to converge with N=100? No fallback plan stated (reduce to 2-factor model? Increase prior informativeness?).

**Score Justification:**

Parameters are well-specified with clear documentation of Decision D039/D068/D070 compliance. Deduction for missing justification of IRT prior choice, lack of sensitivity analysis plans, and ambiguous random structure selection strategy. These gaps prevent full exceptional rating. Score: 1.8/2.0 (Strong category, 90%).

---

#### Category 4: Validation Procedures (1.7 / 2.0)

**Criteria Checklist:**
- [x] IRT convergence checks mentioned (theta in [-4,4], SE in [0.1,1.5])
- [x] Item purification validation specified (30-70% retention expected)
- [x] LMM convergence requirement stated
- [x] Dual p-value reporting specified (Decision D068)
- [ ] Specific IRT assumption tests not detailed (local independence Q3, unidimensionality, model fit)
- [ ] LMM assumption validation procedures missing (residual normality, homoscedasticity, ACF)
- [ ] No remedial actions specified for assumption violations

**Assessment:**

Concept specifies high-level validation requirements (IRT convergence, LMM convergence, dual p-values) but lacks detailed assumption testing procedures and remedial action plans.

**Strengths:**
- IRT convergence thresholds specified: theta ∈ [-4,4], SE ∈ [0.1,1.5]
- Item purification retention target stated: 30-70% per factor (realistic expectation)
- Success criteria include: 1200 observations expected (100 UID × 4 tests × 3 schema levels)
- Dual p-value reporting ensures Decision D068 compliance (Bonferroni correction documented)
- Output files clearly specified for validation (step02_purified_items.csv documents retained items)

**Concerns / Gaps:**

**IRT Validation Gaps:**
- **Local independence not tested:** No mention of Q3 statistic to detect item pairs with residual correlation after conditioning on theta. Q3 > 0.2 threshold recommended ([Christensen et al., 2017](https://www.sciencedirect.com/topics/psychology/graded-response-model)).
- **Unidimensionality per factor not validated:** 3-factor model assumes each factor (Common/Congruent/Incongruent) is unidimensional, but no eigenvalue ratio check or scree plot analysis mentioned.
- **Model fit indices missing:** No RMSEA, CFI, or TLI thresholds specified for GRM fit. Literature recommends RMSEA < 0.08 for acceptable fit.
- **No remedial actions:** What if local independence violated? Purify problem items? Re-specify Q-matrix? No contingency plan.

**LMM Validation Gaps:**
- **Residual diagnostics not specified:** No mention of Q-Q plots for normality, residual vs fitted plots for homoscedasticity, ACF plots for autocorrelation in repeated measures.
- **Outlier detection missing:** No Cook's distance threshold (D > 4/n) or leverage analysis mentioned.
- **Assumption violation handling unclear:** If residual normality fails, will robust standard errors be used? Transformation considered? No plan stated.
- **Random effects normality not checked:** Concept proposes random slopes but doesn't mention Q-Q plots for random effects to validate normality assumption.

**Literature Support for Gaps:**

[Accessible analysis of longitudinal data with LME models (PMC, 2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9092652/) emphasizes comprehensive assumption checking for LMM: "residual normality, homoscedasticity, independence, and linearity should all be validated with diagnostic plots before interpreting fixed effects."

**Score Justification:**

High-level validation requirements present (convergence, retention rates, dual p-values) but lacks granular assumption testing procedures and remedial action plans. IRT local independence, unidimensionality, and model fit checks missing. LMM diagnostic procedures not specified. These gaps prevent strong rating despite good coverage of basic requirements. Score: 1.7/2.0 (Adequate to Strong boundary, 85%).

---

#### Category 5: Devil's Advocate Analysis (0.8 / 1.0)

**Meta-Scoring Criteria:**
- Coverage: 4/4 subsections populated (Commission, Omission, Alternatives, Pitfalls) ✅
- Quality: 8 total concerns with 6 literature citations (good, but could be more comprehensive)
- Thoroughness: Challenge pass conducted, but some criticisms lack specific citations

**Total Concerns Identified:**
- Commission Errors: 1 (0 CRITICAL, 1 MODERATE, 0 MINOR)
- Omission Errors: 3 (1 CRITICAL, 2 MODERATE, 0 MINOR)
- Alternative Approaches: 2 (0 CRITICAL, 1 MODERATE, 1 MINOR)
- Known Pitfalls: 2 (0 CRITICAL, 2 MODERATE, 0 MINOR)

**Overall Devil's Advocate Assessment:**

Generated 8 concerns across all 4 subsections with literature grounding for methodological criticisms. Identified key omissions (multiple testing correction strategy, LMM assumption validation, GRM sample size limitations) and known pitfalls (overfitting risk, convergence issues). Quality is strong with specific actionable recommendations and appropriate strength ratings. However, some criticisms (especially in Alternatives subsection) could benefit from more targeted methodological citations rather than general reviews. Thoroughness is good but not exceptional - could have explored more GRM-specific convergence remedies or Bayesian IRT alternatives.

**Score Justification:**

Strong devil's advocate coverage with 8 concerns well-distributed across subsections. All concerns are specific, actionable, and appropriately rated. Literature citations support key criticisms (sample size requirements, LMM assumptions, random slopes convergence). Deduction from exceptional rating due to: (1) some criticisms lack specific citations (e.g., "GRM prior selection not justified" lacks direct methodological reference), (2) could have generated more GRM-specific concerns (e.g., threshold parameter ordering constraints, response category collapse issues), (3) Bayesian IRT alternative mentioned but not deeply explored with specific citations. Score: 0.8/1.0 (Strong category, 80%).

---

### Tool Availability Validation

**Source:** `docs/v4/tools_catalog.md`

**Analysis Pipeline Steps:**

| Step | Tool Function | Status | Notes |
|------|---------------|--------|-------|
| Step 0: Extract TC_* | Standard extraction | ✅ Available | Filters TC_* tags with i1-i6 congruence patterns |
| Step 1: IRT Pass 1 | `calibrate_irt` | ✅ Available | 3-factor GRM, Q-matrix, p1_med prior |
| Step 2: Purify | `filter_items_by_quality` | ✅ Available | D039: |b| ≤ 3.0, a ≥ 0.4 |
| Step 3: IRT Pass 2 | `calibrate_irt` | ✅ Available | Re-calibration on purified items |
| Step 4: Merge TSVR | `fit_lmm_trajectory_tsvr` | ✅ Available | D070: TSVR time variable |
| Step 5: Fit LMM | `fit_lmm_trajectory_tsvr` | ✅ Available | Schema × Time interaction |
| Step 6: Post-hoc | `compute_contrasts_pairwise` | ✅ Available | D068: dual p-values |
| Step 7: Compare Ch5 | Manual comparison | N/A | Conceptual task, no tool needed |

**Tool Reuse Rate:** 6/6 automated steps (100% for analysis tools)

**Missing Tools:**
None. All required analysis tools available.

**Tool Availability Assessment:**

Exceptional tool coverage. All analysis steps use existing tools from `tools/` package. GRM calibration supports multidimensional models, purification enforces Decision D039 thresholds, LMM tools support TSVR and dual p-values per Decisions D070/D068.

---

### Validation Procedures Checklists

#### IRT Validation Checklist (GRM 3-Factor Ordinal)

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Local Independence | Q3 statistic | Q3 < 0.2 | ⚠️ NOT MENTIONED - should be added to validate item pairs |
| Unidimensionality (per factor) | Eigenvalue ratio | λ1/λ2 > 3.0 | ⚠️ NOT MENTIONED - should validate each factor separately |
| Model Fit | RMSEA / CFI / TLI | RMSEA < 0.08, CFI > 0.95 | ⚠️ NOT MENTIONED - critical for GRM validation |
| Item Fit | Item fit statistics | Model-dependent | ⚠️ NOT MENTIONED - should check item-level fit |
| Convergence | Theta bounds, SE | θ ∈ [-4,4], SE ∈ [0.1,1.5] | ✅ SPECIFIED in success criteria |
| Item Quality | Purification | |b| ≤ 3.0, a ≥ 0.4 | ✅ SPECIFIED per Decision D039 |
| Response Category Use | Category frequencies | Min 10 responses per category | ⚠️ NOT MENTIONED - ensure all 5 Likert levels used |

**IRT Validation Assessment:**

Concept specifies convergence checks and purification thresholds but lacks comprehensive assumption validation. Critical gaps: local independence testing (Q3 statistic), unidimensionality checks per factor (eigenvalue ratios), global model fit indices (RMSEA/CFI/TLI), and response category frequency checks for ordinal data. With 5-category Likert scale, should verify all categories are endorsed sufficiently to estimate thresholds. Literature recommends minimum 10 observations per category per item ([Getting started with the GRM, PMC 2024](https://pmc.ncbi.nlm.nih.gov/articles/PMC11626089/)).

**Concerns:**
- Local independence violations could inflate theta estimates if item pairs share residual variance after conditioning on latent trait
- Without unidimensionality validation per factor, 3-factor structure may be misspecified (factors not truly unidimensional)
- Missing global fit indices prevent assessment of whether GRM adequately represents ordinal response data

**Recommendations:**
- Add Section 7: Validation Procedures subsection for IRT with specific tests: Q3 < 0.2, eigenvalue ratio > 3.0 per factor, RMSEA < 0.08
- Specify remedial actions if assumptions violated (e.g., drop items with Q3 > 0.2, collapse adjacent response categories if insufficient endorsements)

---

#### LMM Validation Checklist

| Assumption | Test | Threshold | Assessment |
|------------|------|-----------|------------|
| Residual Normality | Shapiro-Wilk + Q-Q plot | p > 0.05 (visual primary) | ⚠️ NOT MENTIONED - critical for small N |
| Homoscedasticity | Residual vs fitted plot | Visual inspection | ⚠️ NOT MENTIONED - should check variance constancy |
| Random Effects Normality | Q-Q plot (random intercepts/slopes) | Visual inspection | ⚠️ NOT MENTIONED - assumption for random slopes |
| Independence | ACF plot | Lag-1 ACF < 0.1 | ⚠️ NOT MENTIONED - repeated measures may have autocorrelation |
| Linearity | Partial residual plots | Visual inspection | ⚠️ NOT MENTIONED - verify Schema × Time linearity |
| Outliers | Cook's distance | D > 4/n (n=100, D > 0.04) | ⚠️ NOT MENTIONED - detect influential cases |
| Convergence | Model convergence status | No warnings | ✅ MENTIONED in success criteria |

**LMM Validation Assessment:**

Concept states "LMM converges with random slopes" as success criterion but provides no diagnostic validation procedures. Critical gaps: residual diagnostics (normality, homoscedasticity), random effects normality checks, autocorrelation testing (critical for repeated measures), outlier detection. With N=100 and random slopes, convergence issues likely ([Mixed models Stack Exchange](https://stats.stackexchange.com/questions/524599/what-are-the-arguments-in-favor-and-against-using-random-slopes)), and comprehensive assumption checks essential before interpreting interaction effects.

**Concerns:**
- Without residual normality checks, Type I error rates may be inflated if normality violated with small N
- Homoscedasticity violations could bias standard errors and p-values for interaction test
- ACF not tested: repeated measures (4 tests per participant) may exhibit temporal autocorrelation, violating independence assumption
- No outlier detection: influential cases could drive Schema × Time interaction finding

**Recommendations:**
- Add comprehensive LMM diagnostics section: Shapiro-Wilk test + Q-Q plots (residuals + random effects), residual vs fitted plot, ACF plot for lag-1 autocorrelation, Cook's D > 0.04 outlier detection
- Specify remedial actions: if normality violated, use robust standard errors or log-transform theta; if heteroscedasticity detected, use variance structure modeling; if outliers found, sensitivity analysis excluding influential cases

---

#### Decision Compliance Validation

| Decision | Requirement | Implementation | Compliance |
|----------|-------------|----------------|------------|
| D039: 2-Pass IRT | Purify items before Pass 2 | Step 2: `filter_items_by_quality()` with |b| ≤ 3.0, a ≥ 0.4 | ✅ FULLY COMPLIANT |
| D068: Dual Reporting | Report uncorrected + Bonferroni p-values | Step 6: `compute_contrasts_pairwise()` dual p-values | ✅ FULLY COMPLIANT |
| D069: Dual-Scale Plots | Plot theta + probability scales | Step 7: `plot_trajectory_probability()` dual y-axes | ✅ EXPECTED (not yet in 1_concept.md, should be in planning) |
| D070: TSVR Pipeline | Use TSVR (hours) not nominal days | Step 4-5: `fit_lmm_trajectory_tsvr()` time variable | ✅ FULLY COMPLIANT |

**Decision Compliance Assessment:**

Concept demonstrates full compliance with project-wide statistical decisions D039, D068, D070. Two-pass purification workflow explicitly described. Dual p-value reporting specified for post-hoc contrasts. TSVR time variable clearly stated. Decision D069 (dual-scale plots) not mentioned in 1_concept.md but this is appropriate at concept stage (plotting details belong in planning/plotting phase).

---

### Statistical Criticisms & Rebuttals

**Analysis Approach:**
- **Two-Pass WebSearch Strategy:**
  1. **Validation Pass (4 queries):** Verified GRM appropriateness for ordinal confidence ratings, LMM for longitudinal schema congruence effects, purification thresholds, fluency heuristic theoretical foundation
  2. **Challenge Pass (4 queries):** Searched for GRM convergence issues with small N, LMM random slopes pitfalls, Bonferroni correction limitations, ordinal IRT assumption violations
- **Focus:** Both commission errors (questionable assumptions) and omission errors (missing methodological considerations)
- **Grounding:** All criticisms cite specific methodological literature sources from WebSearch

---

#### Commission Errors (Questionable Statistical Assumptions/Claims)

**1. Implicit Assumption of Adequate Sample Size for Multidimensional GRM**
- **Location:** 1_concept.md - Analysis Approach section, Step 1 (IRT Pass 1 calibration)
- **Claim Made:** "Step 1: IRT Pass 1 calibration with 3-factor GRM (Common/Congruent/Incongruent factors) on all items, using p1_med prior."
- **Statistical Criticism:** Concept proceeds with 3-factor GRM without acknowledging that N=100 participants (400 total observations across 4 tests) is substantially below recommended sample size for multidimensional GRM parameter estimation. No justification provided for why this sample size is adequate despite methodological guidelines.
- **Methodological Counterevidence:** Reise & Yu (1990) and Frontiers in Psychology (2016) research on multidimensional GRM found that **minimum N=500 required for adequate parameter recovery**, with discrimination parameter estimation particularly sensitive to sample size. Study states: "a sample size of 500 provided accurate parameter estimates with an instrument length of 90 or shorter" for 3-dimensional GRM. With N=100, "parameter recovery as reflected in correlations between estimated and true discrimination parameters" may fall well below 0.85 threshold for acceptable recovery. Additional concern: Frontiers in Education (2021) documented that "with such a small sample size [N=100 or N=50], either of the models might not even converge and return any results with MML estimation." ([Sample Size Requirements for MGRM](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2016.00109/full), [Performance of Polytomous IRT Models](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2021.721963/full))
- **Strength:** MODERATE
- **Suggested Rebuttal:** "Add to Analysis Approach section: 'Sample size considerations: While N=100 participants provides 400 total observations (4 tests × 100 UID), this is below the recommended N=500 for multidimensional GRM (Reise & Yu, 1990). We proceed with 3-factor model based on: (1) strong theoretical rationale for schema congruence structure, (2) use of informative priors (p1_med) to stabilize estimation, (3) variational inference (IWAVE algorithm) which may perform better than MML with smaller samples. Discrimination parameters will be monitored for poor recovery (biased estimates, large SEs), and if convergence fails, we will consider: (a) reducing to 2-factor model (collapsing Common+Congruent vs Incongruent), (b) unidimensional model with congruence as observed covariate in LMM, or (c) increasing prior informativeness. Sensitivity analyses will compare 3-factor vs 2-factor vs 1-factor solutions to ensure multidimensional structure is empirically supported.'"

---

#### Omission Errors (Missing Statistical Considerations)

**1. No Multiple Testing Correction Strategy Beyond Post-Hoc Contrasts**
- **Missing Content:** Concept specifies Bonferroni correction for post-hoc pairwise contrasts (Step 6, Decision D068) but doesn't address family-wise error rate across the entire RQ. If primary Schema × Time interaction is non-significant (NULL hypothesis expected), but post-hoc tests are conducted anyway, this represents exploratory analysis without stated correction strategy.
- **Why It Matters:** Conducting post-hoc tests after non-significant omnibus test inflates Type I error rate. If primary interaction p > 0.05 but three pairwise contrasts tested (Congruent vs Common, Congruent vs Incongruent, Common vs Incongruent), family-wise error rate increases. Bonferroni correction for post-hoc tests doesn't account for testing both omnibus interaction AND pairwise contrasts in same analysis family.
- **Supporting Literature:** Bender & Lange (2001, BMJ) and Statistics by Jim ([Bonferroni Correction guide](https://statisticsbyjim.com/hypothesis-testing/bonferroni-correction/)) recommend defining family of tests a priori. "Whether or not to use the Bonferroni correction depends on the circumstances of the study. It should not be used routinely and should be considered if: (1) a single test of the 'universal null hypothesis' that all tests are not significant is required." Concept doesn't clarify: If Schema × Time p > 0.05, will post-hoc contrasts still be conducted? If Schema main effect significant, will contrasts be tested within each time point separately (further multiplying comparisons)?
- **Potential Reviewer Question:** "You expect NULL interaction (paralleling Ch5 5.4.1 accuracy findings). If interaction is indeed non-significant, on what basis will you conduct post-hoc contrasts? Aren't you fishing for significant pairwise differences after failing to reject the NULL for the primary hypothesis? How do you control family-wise error rate across omnibus interaction test + conditional post-hoc tests?"
- **Strength:** CRITICAL
- **Suggested Addition:** "Add to Analysis Approach section: 'Multiple testing strategy: Post-hoc pairwise contrasts (Step 6) will be conducted ONLY if at least one omnibus effect is significant: (a) if Schema × Time interaction p < 0.05, test pairwise contrasts for slope differences (Congruent vs Common, etc.) with Bonferroni correction for k=3 comparisons (α = 0.05/3 = 0.017), OR (b) if Schema main effect p < 0.05 (baseline differences), test pairwise contrasts for intercept differences with same Bonferroni correction. If both interaction AND main effect non-significant (consistent with NULL expectation), post-hoc contrasts will NOT be conducted to avoid inflating Type I error from exploratory testing. This decision rule protects against false positives while allowing exploration of significant omnibus effects.' Reference Decision D068 dual reporting: even if post-hoc tests conducted, both uncorrected and Bonferroni-corrected p-values reported for transparency."

**2. GRM Assumption Validation Procedures Not Specified**
- **Missing Content:** Concept states IRT convergence criteria (theta ∈ [-4,4], SE ∈ [0.1,1.5]) but provides no procedures for validating core GRM assumptions: local independence (item pairs conditionally independent given theta), unidimensionality per factor (each of 3 factors measures single latent trait), model fit to ordinal response data.
- **Why It Matters:** Local independence violations (Q3 > 0.2 for item pairs) inflate theta estimates and bias standard errors. If items within Common/Congruent/Incongruent factors share residual covariance after conditioning on latent trait, multidimensional structure may be misspecified. Unidimensionality violations mean each factor doesn't represent coherent construct. Without global fit indices (RMSEA, CFI), no evidence that GRM adequately represents 5-category ordinal response data.
- **Supporting Literature:** Getting started with the GRM tutorial (PMC, 2024) emphasizes: "The first key assumption of a GRM is that θ is monotonically correlated with the probability of endorsing a response category. The second key assumption pertains to the unidimensionality of θ. This implies that the item pool tested using a GRM analysis should represent only one latent trait." For 3-factor model, each factor must be unidimensional. Christensen et al. (2017) recommend Q3 < 0.2 threshold for local independence. ([GRM tutorial](https://pmc.ncbi.nlm.nih.gov/articles/PMC11626089/), [GRM overview](https://www.sciencedirect.com/topics/psychology/graded-response-model))
- **Potential Reviewer Question:** "How do you validate that Common/Congruent/Incongruent factors are each unidimensional? What if items within a factor cluster into subfactors (e.g., Common items split by paradigm IFR vs ICR vs IRE)? How do you test local independence - are any item pairs locally dependent after conditioning on theta? What model fit indices demonstrate GRM adequately represents 5-category ordinal data?"
- **Strength:** MODERATE
- **Suggested Addition:** "Add Section 7: Validation Procedures - IRT Assumptions subsection: '(1) Local Independence: Compute Q3 statistic for all item pairs within each factor. Flag pairs with Q3 > 0.2 as potentially locally dependent. If violations detected, re-examine item content for shared specific variance (e.g., both items from same paradigm). Consider dropping one item from locally dependent pairs or re-specifying Q-matrix. (2) Unidimensionality per factor: Conduct factor analysis separately for Common, Congruent, Incongruent items. Check eigenvalue ratio λ1/λ2 > 3.0 (first to second eigenvalue) as evidence of dominant single factor. Plot scree plots to visualize dimensionality. If multidimensional structure within factor, consider splitting into subfactors or collapsing to 2-factor or 1-factor model. (3) Model Fit: Compute global fit indices for 3-factor GRM: RMSEA < 0.08 (acceptable fit), CFI > 0.95, TLI > 0.95. Compare 3-factor vs 2-factor vs 1-factor models via AIC/BIC to empirically justify multidimensional structure. (4) Response Category Use: Check endorsement frequencies for all 5 Likert levels per item. Ensure minimum 10 observations per category to estimate threshold parameters. If categories rarely endorsed, consider collapsing adjacent levels (e.g., combine "Guess" + "Not Sure" into single low-confidence category).'"

**3. LMM Assumption Validation and Remedial Actions Missing**
- **Missing Content:** Concept states "LMM converges with random slopes" as success criterion but provides no diagnostic procedures for validating LMM assumptions (residual normality, homoscedasticity, random effects normality, independence/autocorrelation, linearity) or remedial actions if assumptions violated.
- **Why It Matters:** With N=100 and repeated measures (4 tests per participant), assumption violations likely. Residual normality critical for accurate p-values with small N. Homoscedasticity violations bias standard errors for Schema × Time interaction test. Autocorrelation in repeated measures violates independence assumption. Without diagnostics, significant interaction finding could be artifact of violated assumptions.
- **Supporting Literature:** Accessible analysis of longitudinal data with LME models (PMC, 2022) emphasizes comprehensive diagnostics: "residual normality, homoscedasticity, independence, and linearity should all be validated with diagnostic plots before interpreting fixed effects." For small samples, Shapiro-Wilk test p > 0.05 recommended but visual Q-Q plot inspection primary. Repeated measures designs require ACF plot to check lag-1 autocorrelation < 0.1. ([LME longitudinal analysis guide](https://pmc.ncbi.nlm.nih.gov/articles/PMC9092652/))
- **Potential Reviewer Question:** "How do you validate residual normality for LMM with N=100? What if heteroscedasticity detected across Schema levels or Time points? Repeated measures with 4 tests per participant - did you check for autocorrelation in residuals? If normality violated, will you use robust standard errors or transform theta scores? What outlier detection threshold will you use to identify influential cases?"
- **Strength:** MODERATE
- **Suggested Addition:** "Add Section 7: Validation Procedures - LMM Assumptions subsection: '(1) Residual Normality: Shapiro-Wilk test (p > 0.05) + Q-Q plot visual inspection. If violated, consider: (a) robust standard errors, (b) log-transform theta scores, (c) report violation in limitations. (2) Homoscedasticity: Residual vs fitted plot. If variance increases/decreases systematically, use variance structure modeling or weighted least squares. (3) Random Effects Normality: Q-Q plots for random intercepts and random slopes. If violated, consider simpler random structure (intercepts only). (4) Independence: ACF plot for lag-1 autocorrelation in repeated measures. If ACF > 0.1, model temporal correlation structure (AR1, compound symmetry). (5) Linearity: Partial residual plots for Schema × Time interaction. Verify linear relationship. (6) Outliers: Cook's distance D > 4/n (n=100, D > 0.04). Identify influential cases, conduct sensitivity analysis excluding outliers. If Schema × Time interaction significant only with outliers included, report as fragile finding.'"

---

#### Alternative Statistical Approaches (Not Considered)

**1. Bayesian IRT Instead of Frequentist GRM**
- **Alternative Method:** Bayesian multidimensional IRT with weakly informative or informative priors instead of frequentist GRM with maximum likelihood estimation (or variational inference)
- **How It Applies:** Bayesian IRT provides more stable parameter estimates with small sample sizes (N=100) by incorporating prior information. Avoids convergence issues common in frequentist MML/variational inference with underpowered samples. Provides uncertainty quantification via posterior distributions instead of point estimates. Allows direct probability statements about parameters (e.g., "95% probability that discrimination for Congruent items is higher than Common items").
- **Key Citation:** Alternative Approaches to Addressing Non-Normal Distributions in IRT (PubMed, 2017) discusses Bayesian IRT as remedy when sample size insufficient for frequentist estimation. Bayesian approaches "incorporate prior information to stabilize estimation when data are sparse." With N=100 for 3-factor GRM, priors can regularize discrimination parameters and prevent boundary estimates. ([Bayesian IRT for non-normal distributions](https://pubmed.ncbi.nlm.nih.gov/29087217/))
- **Why Concept.md Should Address It:** Methodological reviewers familiar with Bayesian IRT may question why frequentist approach chosen when sample size marginal for multidimensional GRM. Bayesian IRT could reduce convergence risk and provide more accurate parameter recovery with N=100. Concept states "p1_med prior" but doesn't justify frequentist framework over fully Bayesian estimation.
- **Strength:** MODERATE
- **Suggested Acknowledgment:** "Add to Analysis Approach section: 'IRT framework justification: We use variational inference (IWAVE algorithm) with informative priors (p1_med) rather than fully Bayesian MCMC estimation for computational efficiency and alignment with prior REMEMVR analyses. While Bayesian IRT could provide more stable estimates with N=100, variational inference with strong priors offers similar regularization benefits (shrinkage toward prior means for discrimination parameters) with faster computation. If convergence issues arise, we will consider switching to Bayesian MCMC as fallback. Acknowledge in limitations: Bayesian IRT with MCMC sampling could provide better uncertainty quantification for multidimensional model with marginal sample size, recommended for future replication studies.'"

**2. Proportional Odds Ordinal Regression Instead of GRM + LMM Pipeline**
- **Alternative Method:** Proportional odds cumulative logit model (ordinal regression) with Schema × Time interaction directly on 5-category Likert confidence ratings, instead of two-stage GRM -> theta extraction -> LMM pipeline
- **How It Applies:** Ordinal regression models 5-category Likert responses directly without IRT calibration step. Tests whether Schema and Time affect probability of higher vs lower confidence categories. Simpler workflow (one model instead of IRT + LMM), may be more robust with small N, avoids IRT convergence issues. Proportional odds assumption requires that Schema × Time effect is consistent across all category thresholds (e.g., effect on P(Confidence ≥ 2) same as effect on P(Confidence ≥ 4)).
- **Key Citation:** Frontiers in Education (2020) discusses "Why Ordinal Variables Can (Almost) Always Be Treated as Continuous Variables" but notes this applies to factor analysis, not necessarily trajectory modeling where ordinal categories should be respected. Proportional Odds Logistic Regression handbook chapter emphasizes testing proportional odds assumption: "if this assumption is violated, the coefficients cannot be reduced to a single set across all outcome categories, and this modeling approach fails." ([Ordinal variables as continuous](https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2020.589965/full), [Proportional Odds Regression](https://peopleanalytics-regression-book.org/ord-reg.html))
- **Why Concept.md Should Address It:** Ordinal regression is simpler, avoids IRT sample size issues, and may be more appropriate if GRM fails to converge. Reviewers might ask: "Why use complex two-stage GRM + LMM pipeline when ordinal regression directly models Likert categories with fewer assumptions?" Concept doesn't justify IRT-derived theta over raw ordinal scores.
- **Strength:** MINOR
- **Suggested Acknowledgment:** "Add to Analysis Approach section: 'GRM + LMM pipeline justification: We use IRT-derived theta scores rather than raw Likert ordinal categories because: (1) theta provides interval-scale metric (raw Likert assumes equal intervals between categories, which may not hold), (2) IRT separates measurement error from true confidence ability (theta SEs quantify precision), (3) allows multidimensional structure to capture schema congruence effects at measurement level (3 factors in GRM). Alternative: proportional odds ordinal regression on raw Likert could avoid IRT convergence issues but would not account for measurement error or test multidimensional congruence structure. If GRM fails to converge, ordinal regression is fallback option.'"

---

#### Known Statistical Pitfalls (Unaddressed)

**1. Random Slopes Convergence Failure with N=100**
- **Pitfall Description:** Complex LMM with random intercepts + random slopes for Schema × Time interaction may fail to converge or produce singular fit with N=100 participants. Random slopes require estimating variance-covariance matrix for random effects, which is data-hungry. With only 100 independent units and 4 time points, insufficient information to reliably estimate random slopes, especially for categorical predictor (Schema) with 3 levels.
- **How It Could Affect Results:** If random slopes don't converge, forced to use simpler model (random intercepts only), which may be misspecified if true heterogeneity in Schema × Time slopes exists across participants. Singular fit (random slope variance estimated as zero) indicates overfitted model, and hypothesis tests may be anticonservative (inflated Type I error). Concept states "LMM converges with random slopes" as success criterion but provides no contingency plan if convergence fails.
- **Literature Evidence:** Stack Exchange discussion on random slopes (2021) notes: "The problem is that in practice, random slopes often lead to an overfitted model, which means that if the model converges, it is often to a singular fit. Even if the random structure is not over-specified, the more complex the model, the more likely it is for the software to have problems finding a/the solution." Bates et al. (2014) advice: "only include random slopes that contribute significantly to model likelihood, using a likelihood ratio test." With N=100, maximal random effects structure (intercepts + slopes for Schema, Time, Schema×Time) likely overparameterized. ([Random slopes arguments](https://stats.stackexchange.com/questions/524599/what-are-the-arguments-in-favor-and-against-using-random-slopes))
- **Why Relevant to This RQ:** Concept proposes "random slopes by UID" but doesn't specify which slopes (Time only? Schema + Time? Schema × Time?). With 3-level Schema factor and continuous Time, full random structure would estimate: random intercept variance, random slope variance for Time, random slope variance for Schema, random slope covariance. This may exceed data capacity with N=100. If convergence fails, no plan stated for model simplification.
- **Strength:** MODERATE
- **Suggested Mitigation:** "Add to Analysis Approach section: 'Random effects selection strategy: Start with maximal random structure justified by design: random intercepts + random slopes for Time (continuous) by UID. Do NOT include random slopes for Schema (categorical between-items factor) as this would require estimating variance across 3 schema levels, which is overparameterized. Test random slope for Time via likelihood ratio test comparing: (Model 1) random intercept + random slope for Time vs (Model 2) random intercept only. Retain random slope only if LRT p < 0.05 AND model converges without warnings. If singular fit detected (random slope variance near zero), report in results and interpret fixed effects cautiously. If convergence fails with random slopes, use random intercepts only model and acknowledge limitation that individual heterogeneity in Time slopes not modeled. This parsimonious approach follows Bates et al. (2014) recommendation to include random slopes only when justified by data, especially critical with N=100.'"

**2. IRT Threshold Parameter Ordering Constraints May Be Violated**
- **Pitfall Description:** GRM for ordinal data assumes ordered threshold parameters (b1 < b2 < b3 < b4 for 5-category Likert). If participants use response categories illogically (e.g., endorse "Very Confident" more often than "Mildly Confident" for low-ability items), thresholds may be disordered, causing GRM calibration to fail or produce nonsensical parameters.
- **How It Could Affect Results:** Disordered thresholds indicate response category collapse: adjacent Likert levels are not psychologically distinct for participants. For example, if "Not Sure" (category 2) and "Mildly Confident" (category 3) used interchangeably, threshold separation (b2 - b1) may be near zero or negative. GRM may not converge or may estimate boundary parameters (b → ±∞). Concept doesn't mention checking threshold ordering or collapsing categories if disordering detected.
- **Literature Evidence:** Getting started with the GRM (PMC, 2024) notes: "For 5 response categories, the model would estimate 4 threshold/boundary parameters plus 1 discrimination parameter per item." Thresholds must be ordered for GRM to be identifiable. If categories not sufficiently distinct, "collapse adjacent response categories if insufficient endorsements" recommended. With 5-category confidence Likert, middle categories ("Not Sure", "Mildly Confident") may overlap psychologically. ([GRM tutorial](https://pmc.ncbi.nlm.nih.gov/articles/PMC11626089/))
- **Why Relevant to This RQ:** Confidence ratings are subjective metacognitive judgments, not objective performance. Participants may interpret Likert labels idiosyncratically. For example, some participants may rarely use middle categories (response style: mostly "Guess" or "Absolutely Certain"), creating sparse data for estimating b2, b3 thresholds. Concept doesn't address response category frequency checks or threshold ordering diagnostics.
- **Strength:** MODERATE
- **Suggested Mitigation:** "Add to Section 7: Validation Procedures: 'Response category diagnostics: (1) Check endorsement frequencies for all 5 Likert levels (0, 0.25, 0.5, 0.75, 1.0) per item. Flag items with categories endorsed <10 times (insufficient data for threshold estimation). (2) After GRM Pass 1, inspect estimated threshold parameters (b1, b2, b3, b4) per item. Check ordering: b1 < b2 < b3 < b4. If thresholds disordered for >20% of items, indicates response category collapse. (3) Remedial action: Collapse adjacent categories with low separation. For example, if b1 ≈ b2, combine "Guess/No Memory" + "Not Sure" into single low-confidence category (0-0.25 -> 0), reducing to 4-category model. Re-calibrate GRM with collapsed categories. (4) Report category collapsing decision in results with justification (psychological distinctiveness of original categories not empirically supported).'"

---

#### Scoring Summary

**Total Concerns Identified:**
- Commission Errors: 1 (0 CRITICAL, 1 MODERATE, 0 MINOR)
- Omission Errors: 3 (1 CRITICAL, 2 MODERATE, 0 MINOR)
- Alternative Approaches: 2 (0 CRITICAL, 1 MODERATE, 1 MINOR)
- Known Pitfalls: 2 (0 CRITICAL, 2 MODERATE, 0 MINOR)

**Total:** 8 concerns (1 CRITICAL, 6 MODERATE, 1 MINOR)

**Overall Devil's Advocate Assessment:**

Concept.md demonstrates strong methodological foundation with appropriate GRM for ordinal confidence data and LMM for trajectory analysis. However, lacks explicit acknowledgment of sample size limitations for multidimensional GRM (N=100 << recommended N=500), comprehensive assumption validation procedures (IRT local independence, unidimensionality, model fit; LMM residual diagnostics), and contingency plans for convergence failures or assumption violations.

**Key Strengths:**
- GRM correctly chosen for 5-category ordinal data (NOT 2PL binary)
- Two-pass purification workflow appropriate (Decision D039)
- TSVR time variable and dual p-values comply with Decisions D070/D068
- Schema × Time interaction directly tests primary hypothesis
- Theoretical grounding in fluency heuristic and schema processing literature

**Key Gaps Requiring Attention:**
1. **CRITICAL:** Multiple testing strategy incomplete - unclear if post-hoc contrasts conducted after non-significant omnibus interaction (expected NULL hypothesis). Risk of exploratory fishing without family-wise error control.
2. **MODERATE:** Sample size justification missing for 3-factor GRM with N=100 (well below N=500 recommendation). No sensitivity analysis or fallback plan if convergence fails.
3. **MODERATE:** IRT assumption validation procedures not specified (local independence, unidimensionality per factor, model fit indices, threshold ordering).
4. **MODERATE:** LMM diagnostic procedures missing (residual normality, homoscedasticity, ACF, outliers). No remedial actions if assumptions violated.
5. **MODERATE:** Random slopes selection strategy ambiguous - maximal vs parsimonious approach not stated. Convergence risk with N=100 not addressed.
6. **MODERATE:** Bayesian IRT alternative could reduce convergence risk but not discussed. Frequentist GRM with informative priors chosen but not justified over fully Bayesian approach.

**Recommendations:**
Address CRITICAL omission (multiple testing strategy) and MODERATE concerns (sample size justification, assumption validation procedures, remedial action plans) to strengthen methodological rigor and preempt reviewer questions. Concept has strong foundation but needs explicit acknowledgment of small-sample limitations and comprehensive diagnostic planning.

---

### Recommendations

#### Required Changes (Must Address for Approval)

**1. Specify Multiple Testing Correction Strategy for Omnibus + Post-Hoc Tests**
   - **Location:** 1_concept.md - Analysis Approach section, Step 6 (Post-hoc contrasts)
   - **Issue:** Concept states Bonferroni correction for post-hoc pairwise contrasts but doesn't clarify decision rule: Will post-hoc tests be conducted if primary Schema × Time interaction is non-significant (NULL expected per hypothesis)? Current wording allows exploratory testing after failing to reject NULL, inflating family-wise error rate across omnibus test + conditional post-hoc tests.
   - **Fix:** Add decision rule: "Post-hoc pairwise contrasts (Step 6) will be conducted ONLY if at least one omnibus effect is significant: (a) if Schema × Time interaction p < 0.05, test pairwise contrasts for slope differences (Congruent vs Common, Congruent vs Incongruent, Common vs Incongruent) with Bonferroni correction for k=3 comparisons (α = 0.017), OR (b) if Schema main effect p < 0.05 (baseline differences), test pairwise contrasts for intercept differences with same Bonferroni correction. If both interaction AND main effect non-significant (consistent with NULL expectation paralleling Ch5 5.4.1), post-hoc contrasts will NOT be conducted to protect against Type I error from exploratory testing. Reference Decision D068: both uncorrected and Bonferroni-corrected p-values reported for transparency."
   - **Rationale:** Category 5 CRITICAL concern (Omission Error #1). Protects against false positives from exploratory testing after non-significant omnibus result. Aligns with Bender & Lange (2001) and Statistics by Jim guidance on Bonferroni use. Essential for methodological rigor with NULL hypothesis expectation.

**2. Add Sample Size Justification for Multidimensional GRM**
   - **Location:** 1_concept.md - Analysis Approach section, Step 1 (IRT Pass 1 calibration) OR Data Source section
   - **Issue:** Concept proceeds with 3-factor GRM without acknowledging that N=100 participants (400 total observations) is substantially below recommended N=500 for multidimensional GRM parameter recovery. No justification provided, creating vulnerability to reviewer criticism about underpowered IRT analysis.
   - **Fix:** Add paragraph: "Sample size considerations: While N=100 participants provides 400 total observations (4 tests × 100 UID), this is below the recommended N=500 for multidimensional GRM with adequate discrimination parameter recovery (Reise & Yu, 1990; Frontiers in Psychology, 2016). We proceed with 3-factor model based on: (1) strong theoretical rationale for Common/Congruent/Incongruent schema structure, (2) informative priors (p1_med) to regularize estimation and prevent boundary parameters, (3) variational inference (IWAVE algorithm) which may perform better than MML with smaller samples. Discrimination parameters will be monitored for poor recovery (biased estimates, large SEs > 1.5). If convergence fails or parameter quality poor, fallback options: (a) reduce to 2-factor model (Common+Congruent vs Incongruent), (b) unidimensional model with congruence as LMM covariate, or (c) increase prior informativeness. Sensitivity analyses will compare 3-factor vs 2-factor vs 1-factor solutions via AIC/BIC to empirically justify multidimensional structure."
   - **Rationale:** Category 5 MODERATE concern (Commission Error #1). Addresses implicit assumption that N=100 is adequate without justification. Demonstrates awareness of methodological limitation and provides contingency plans. Preempts reviewer question: "Why use 3-factor GRM when sample size inadequate per published guidelines?"

---

#### Suggested Improvements (Optional but Recommended)

**1. Add Comprehensive IRT Assumption Validation Procedures**
   - **Location:** 1_concept.md - Section 7: Analysis Approach, create new subsection "IRT Assumption Validation"
   - **Current:** Concept states convergence criteria (theta ∈ [-4,4], SE ∈ [0.1,1.5]) but no assumption testing procedures
   - **Suggested:** "Add subsection: 'IRT Assumption Validation: (1) Local Independence: Compute Q3 statistic for all item pairs within each factor (Common, Congruent, Incongruent). Flag pairs with Q3 > 0.2 as potentially locally dependent. If violations detected, drop one item from dependent pairs or re-specify Q-matrix. (2) Unidimensionality per factor: Conduct exploratory factor analysis separately for each schema level. Check eigenvalue ratio λ1/λ2 > 3.0 as evidence of dominant single factor. If multidimensional structure within factor, consider subfactor splitting or model simplification. (3) Model Fit: Compute RMSEA < 0.08, CFI > 0.95, TLI > 0.95 for 3-factor GRM. Compare 3-factor vs 2-factor vs 1-factor models via AIC/BIC. (4) Response Category Use: Check endorsement frequencies for all 5 Likert levels per item (minimum 10 observations per category for stable threshold estimation). If categories rarely endorsed, collapse adjacent levels and re-calibrate with reduced categories.'"
   - **Benefit:** Demonstrates comprehensive methodological rigor. Preempts reviewer questions about local independence violations, within-factor dimensionality, and model fit. Provides remedial action plans for assumption violations. Addresses Category 5 MODERATE concern (Omission Error #2).

**2. Add LMM Assumption Validation and Remedial Actions**
   - **Location:** 1_concept.md - Section 7: Analysis Approach, create new subsection "LMM Assumption Validation"
   - **Current:** States "LMM converges with random slopes" but no diagnostic procedures
   - **Suggested:** "Add subsection: 'LMM Assumption Validation: (1) Residual Normality: Shapiro-Wilk test (p > 0.05) + Q-Q plot visual inspection. If violated, consider robust standard errors or log-transform theta. (2) Homoscedasticity: Residual vs fitted plot. If variance non-constant, use variance structure modeling. (3) Random Effects Normality: Q-Q plots for random intercepts/slopes. (4) Independence: ACF plot for lag-1 autocorrelation (threshold < 0.1). If violated, model temporal correlation (AR1). (5) Linearity: Partial residual plots for Schema × Time interaction. (6) Outliers: Cook's distance D > 4/n (n=100, D > 0.04). Conduct sensitivity analysis excluding influential cases. All diagnostics will be documented in validation report with remedial actions taken.'"
   - **Benefit:** Ensures robust inference for Schema × Time interaction test. Demonstrates awareness of small-N assumptions sensitivity. Addresses Category 5 MODERATE concern (Omission Error #3). Aligns with Accessible LME models (PMC, 2022) best practices.

**3. Specify Random Effects Selection Strategy**
   - **Location:** 1_concept.md - Analysis Approach section, Step 5 (Fit LMM)
   - **Current:** "Fit LMM with Congruence × Time interaction, random slopes by UID"
   - **Suggested:** "Fit LMM with Schema × Time interaction. Random effects selection: Start with random intercepts + random slopes for Time (continuous) by UID. Do NOT include random slopes for Schema (categorical factor) to avoid overparameterization with N=100. Test random slope for Time via likelihood ratio test: Model 1 (random intercept + random slope for Time) vs Model 2 (random intercept only). Retain random slope only if LRT p < 0.05 AND model converges without warnings (no singular fit). If convergence fails, use random intercepts only model and acknowledge that individual heterogeneity in Time slopes not modeled. This parsimonious approach follows Bates et al. (2014) recommendation, critical with N=100."
   - **Benefit:** Provides clear selection strategy for random effects structure. Reduces convergence risk by avoiding overparameterized maximal model. Demonstrates understanding of maximal vs parsimonious debate in LMM literature. Addresses Category 5 MODERATE concern (Known Pitfall #1).

**4. Acknowledge Bayesian IRT as Alternative**
   - **Location:** 1_concept.md - Analysis Approach section, Step 1 (IRT Pass 1) OR new subsection "Alternative Approaches Considered"
   - **Current:** Uses variational inference with p1_med prior but doesn't justify frequentist framework
   - **Suggested:** "IRT framework justification: We use variational inference (IWAVE algorithm) with informative priors (p1_med) rather than fully Bayesian MCMC estimation for computational efficiency and alignment with prior REMEMVR analyses. While Bayesian IRT could provide more stable estimates with N=100 via full posterior distributions, variational inference with strong priors offers similar regularization (shrinkage toward prior means) with faster computation. If convergence issues arise, Bayesian MCMC is fallback option. Limitation: Bayesian IRT would provide better uncertainty quantification for multidimensional model with marginal sample size, recommended for future replication studies."
   - **Benefit:** Demonstrates awareness of Bayesian alternatives. Justifies frequentist choice while acknowledging trade-offs. Preempts reviewer question: "Why not use Bayesian IRT when N=100 is small for 3-factor GRM?" Addresses Category 5 MODERATE concern (Alternative Approach #1).

**5. Add Response Category Diagnostics for Ordinal Data**
   - **Location:** 1_concept.md - Section 7: Analysis Approach, add to IRT Assumption Validation subsection
   - **Current:** No mention of checking response category endorsement frequencies or threshold ordering
   - **Suggested:** "Response Category Diagnostics: (1) Check endorsement frequencies for all 5 Likert levels (0, 0.25, 0.5, 0.75, 1.0) per item. Flag items with categories endorsed <10 times. (2) After GRM Pass 1, inspect estimated threshold parameters (b1, b2, b3, b4) per item. Verify ordering: b1 < b2 < b3 < b4. If thresholds disordered for >20% of items, indicates response category collapse. (3) Remedial action: Collapse adjacent categories with low separation (e.g., combine 'Guess' + 'Not Sure' if b1 ≈ b2), reducing to 4-category model. Re-calibrate GRM with collapsed categories. Report category collapsing decision with justification."
   - **Benefit:** Ensures ordinal GRM assumptions met (ordered thresholds, sufficient category endorsements). Prevents nonsensical parameter estimates from category collapse. Addresses Category 5 MODERATE concern (Known Pitfall #2). Demonstrates understanding of ordinal IRT requirements.

---

### Validation Metadata

- **Agent Version:** rq_stats v5.0
- **Rubric Version:** 10-point system (v4.2)
- **Validation Date:** 2025-12-06 18:15
- **Tools Inventory Source:** docs/v4/tools_catalog.md
- **Total Tools Validated:** 6 analysis tools + 1 manual comparison
- **Tool Reuse Rate:** 100% (6/6 analysis tools available)
- **Validation Duration:** ~28 minutes
- **Context Dump:** "9.1/10 CONDITIONAL. Category 1: 2.8/3 (GRM + LMM appropriate, sample size marginal for 3-factor GRM). Category 2: 2.0/2 (100% tool reuse). Category 3: 1.8/2 (parameters specified, IRT prior/random structure justification gaps). Category 4: 1.7/2 (convergence criteria stated, assumption tests missing). Category 5: 0.8/1 (8 concerns generated, 1 CRITICAL + 6 MODERATE, good literature grounding). Address CRITICAL multiple testing strategy + MODERATE sample size justification for APPROVAL."

---
