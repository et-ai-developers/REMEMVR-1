# Results Inspection Report

**RQ:** X.Y - [RQ Title]
**Inspection Date:** YYYY-MM-DD HH:MM
**Agent:** results_inspector v1.0
**Report Version:** 1.0

---

## Executive Summary

**Status:** ✅ APPROVED / ⚠️ CONDITIONAL / ❌ REJECTED

**Statistical Correctness:** ✅ VERIFIED / ⚠️ CONCERNS / ❌ ERRORS

**Completeness:** [X]/[X] required outputs present

**Interpretation Quality:** ✅ SOUND / ⚠️ NEEDS REVISION / ❌ INCORRECT

**Recommendation:** PUBLISH / REVISE / RE-ANALYZE

---

## Inspection Scope

**Files Inspected:**
- ✅ data/item_parameters.csv + .md
- ✅ data/theta_scores.csv + .md
- ✅ data/lmm_coefficients.csv + .md
- ✅ data/lmm_random_effects.csv + .md
- ✅ plots/irt_icc_by_domain.png
- ✅ plots/lmm_trajectories_by_domain.png
- ✅ logs/analysis_executor_report.md
- ✅ info.md (Section 5: Validation results)

**Documents Reviewed:**
- ✅ info.md (all sections)
- ✅ config.yaml
- ✅ validation/scholar_report.md
- ✅ validation/statistics_report.md

---

## Statistical Correctness Validation

### IRT Results Validation

**Item Parameters:**
- **Total Items:** [N] ([N] flagged in Pass 1, [N] retained in Pass 2)
- **Discrimination (a) Range:** [min-max] (expected: 0.4-3.0)
- **Difficulty (b) Range:** [min-max] (expected: -3.0 to 3.0)

**Quality Checks:**

| **Check** | **Expected** | **Actual** | **Status** |
|-----------|------------|-----------|-----------|
| All a ≥ 0.4 | 100% | [X]% | ✅ PASS / ❌ FAIL |
| All |b| ≤ 3.0 | 100% | [X]% | ✅ PASS / ❌ FAIL |
| Flagging Rate | 5-15% | [X]% | ✅ PASS / ⚠️ OUTSIDE RANGE |
| Convergence | Yes | [Yes/No] | ✅ PASS / ❌ FAIL |

**Issues:** [None / List any parameter anomalies]

---

**Theta Scores:**
- **Total Observations:** [N] (expected: 400 participants × 4 tests = 1600? Or 100×4=400?)
- **Dimensions:** 3 (Person, Place, Object)
- **Value Range:** [min-max]

**Quality Checks:**

| **Check** | **Expected** | **Actual** | **Status** |
|-----------|------------|-----------|-----------|
| No Missing Values | 0 | [N] | ✅ PASS / ❌ FAIL |
| Theta Range | -4 to +4 typical | [min-max] | ✅ REASONABLE / ⚠️ EXTREME |
| Means Near 0 | ~0 (standardized) | [means] | ✅ PASS / ⚠️ WARNING |

**Issues:** [None / List any theta score anomalies]

---

### LMM Results Validation

**Fixed Effects:**

| **Effect** | **Coefficient** | **p-value** | **95% CI** | **Validation** |
|-----------|----------------|------------|-----------|---------------|
| Intercept | [X] | [X] | [[L], [U]] | ✅ Reasonable baseline |
| Domain_Place | [X] | [X] | [[L], [U]] | ✅ CI excludes 0 / ⚠️ CI includes 0 |
| Domain_Object | [X] | [X] | [[L], [U]] | ✅ CI excludes 0 / ⚠️ CI includes 0 |
| Day | [X] | [X] | [[L], [U]] | ✅ Negative (forgetting) / ⚠️ Unexpected sign |
| Domain_Place × Day | [X] | [X] | [[L], [U]] | ✅ Significant / ⚠️ Non-significant |
| Domain_Object × Day | [X] | [X] | [[L], [U]] | ✅ Significant / ⚠️ Non-significant |

**Quality Checks:**

| **Check** | **Expected** | **Actual** | **Status** |
|-----------|------------|-----------|-----------|
| Day Effect Negative | Yes (forgetting) | [positive/negative] | ✅ PASS / ❌ FAIL |
| Interaction Direction | As hypothesized | [matches/contradicts] | ✅ PASS / ⚠️ UNEXPECTED |
| SE Reasonable | <|β| | All [yes/no] | ✅ PASS / ❌ FAIL |
| p-values Valid | 0 ≤ p ≤ 1 | All [yes/no] | ✅ PASS / ❌ FAIL |

**Issues:** [None / List any coefficient anomalies]

---

**Random Effects:**
- **Intercept SD:** [X] (variability in baseline ability)
- **Slope SD:** [X] (variability in forgetting rate)
- **Correlation:** [X] (intercept-slope relationship)

**Quality Checks:**

| **Check** | **Reasonable Range** | **Actual** | **Status** |
|-----------|---------------------|-----------|-----------|
| Intercept SD | >0, <2 typical | [X] | ✅ REASONABLE / ⚠️ EXTREME |
| Slope SD | >0, <1 typical | [X] | ✅ REASONABLE / ⚠️ EXTREME |
| Correlation | -1 to +1 | [X] | ✅ VALID / ❌ INVALID |

**Issues:** [None / List any random effects anomalies]

---

**Effect Sizes:**
- **Domain×Day Interaction:** Cohen's f² = [X], 95% CI [[L], [U]]
- **Interpretation:** [small (<0.15) / medium (0.15-0.35) / large (>0.35)]

**Quality Checks:**

| **Check** | **Expected** | **Actual** | **Status** |
|-----------|------------|-----------|-----------|
| f² ≥ 0 | Yes | [yes/no] | ✅ PASS / ❌ FAIL |
| CI Validity | Lower < Upper | [yes/no] | ✅ PASS / ❌ FAIL |
| Magnitude Reasonable | <1.0 typical | [X] | ✅ REASONABLE / ⚠️ EXTREME |

**Issues:** [None / List any effect size anomalies]

---

### Validation Results Review

**IRT Assumptions (from info.md Section 5):**

| **Assumption** | **Test** | **Result** | **Validation** |
|---------------|---------|-----------|---------------|
| Local Independence | Q3 < 0.2 | Max Q3 = [X] | ✅ MET / ❌ VIOLATED |
| Unidimensionality | Ratio > 3.0 | Ratio = [X] | ✅ MET / ❌ VIOLATED |
| Model Fit (RMSEA) | <0.08 | RMSEA = [X] | ✅ MET / ❌ VIOLATED |
| Model Fit (CFI) | >0.90 | CFI = [X] | ✅ MET / ❌ VIOLATED |
| Item Fit | S-X² p>0.01 | [N]/[N] pass | ✅ MET / ⚠️ SOME FAIL |

**LMM Assumptions (from info.md Section 5):**

| **Assumption** | **Test** | **Result** | **Validation** |
|---------------|---------|-----------|---------------|
| Residual Normality | Shapiro-Wilk p>0.05 | p = [X] | ✅ MET / ❌ VIOLATED |
| Homoscedasticity | Levene's p>0.05 | p = [X] | ✅ MET / ❌ VIOLATED |
| Independence | DW 1.5-2.5 | DW = [X] | ✅ MET / ❌ VIOLATED |

**Assumption Violations:** [None / List and assess severity]

---

## Completeness Check

### Required Outputs

**Data Files:**
- ✅ item_parameters.csv + .md
- ✅ theta_scores.csv + .md
- ✅ lmm_input.csv + .md
- ✅ lmm_coefficients.csv + .md
- ✅ lmm_random_effects.csv + .md

**Plot Files:**
- ✅ irt_icc_by_domain.png + _data.csv
- ✅ lmm_trajectories_by_domain.png + _data.csv
- ✅ lmm_random_effects.png + _data.csv

**Documentation Files:**
- ✅ logs/data_prep_report.md
- ✅ logs/analysis_executor_report.md
- ✅ code/data_prep_script.py
- ✅ code/analysis_script.py

**Completeness Score:** [X]/[X] (100% / [X]%)

**Missing Files:** [None / List]

---

## Interpretation Quality Assessment

### Answer to Research Question (info.md Section 8)

**Current Answer:** [Quote from info.md]

**Statistical Support:**
- **Main Finding:** Domain×Day interaction: β = [X], p = [X], f² = [X]
- **Direction:** [Matches hypothesis / Contradicts hypothesis / Mixed]
- **Strength:** [Significant/Non-significant], [Small/Medium/Large effect]

**Quality Evaluation:**

| **Criterion** | **Assessment** | **Status** |
|--------------|---------------|-----------|
| Answer Addresses RQ | Directly / Partially / No | ✅ / ⚠️ / ❌ |
| Cites Correct Statistics | All relevant / Some / None | ✅ / ⚠️ / ❌ |
| Interprets Direction Correctly | Yes / No | ✅ / ❌ |
| Interprets Magnitude Correctly | Yes / No | ✅ / ❌ |
| Acknowledges Limitations | Yes / No | ✅ / ⚠️ |

**Issues:** [None / List interpretation errors or omissions]

**Recommended Revisions:**
1. [Specific revision if needed]
2. [Specific revision if needed]

---

### Theoretical Implications (info.md Section 9)

[Will be filled by scholar agent - placeholder check]

**Status:** ⏳ PENDING (scholar agent not yet invoked) / ✅ COMPLETE

**If Complete:**
- **Alignment with Results:** [Implications match findings / Overstated / Understated]
- **Literature Integration:** [Well-integrated / Needs expansion / Disconnected]

---

## Scholarly Summary

### Key Findings

**Research Question:** [Restate RQ]

**Main Result:** [1-sentence finding]

**Supporting Evidence:**
1. **IRT Analysis:** [Key IRT finding - e.g., "27 items showed acceptable psychometric properties after 2-pass purification"]
2. **LMM Analysis:** [Key LMM finding - e.g., "Significant Domain×Day interaction (f²=0.18, medium effect) indicates domain-specific forgetting trajectories"]
3. **Pattern:** [Describe the pattern - e.g., "Person items showed slower forgetting (slope=-0.05/day) than Place items (slope=-0.12/day)"]

**Hypothesis Confirmation:** ✅ SUPPORTED / ⚠️ PARTIALLY SUPPORTED / ❌ NOT SUPPORTED

---

### Result Interpretation

**What This Means:**
[2-3 paragraph scholarly interpretation]

**Example:**
The significant Domain×Day interaction provides evidence for domain-specific consolidation processes in episodic memory. Person-related memories exhibited slower forgetting rates compared to place- and object-related memories, consistent with the self-reference effect (Symons & Johnson, 1997) and schema congruence theory. This pattern suggests that person-related information benefits from richer semantic networks and stronger consolidation, leading to more durable episodic traces over the 7-day retention interval. The medium effect size (f²=0.18) indicates this is a robust and practically significant phenomenon that should be considered in episodic memory assessment tools like REMEMVR.

---

### Limitations

**Acknowledged in info.md:**
- [List limitations already acknowledged]

**Additional Limitations Identified:**
- [Any limitations missed in original specification]

**Severity Assessment:**
- [High / Medium / Low - whether limitations undermine conclusions]

---

### Publication Readiness

**Strengths:**
- [What's publication-quality]

**Weaknesses:**
- [What needs improvement before publication]

**Recommendation:**
- ✅ READY FOR THESIS CHAPTER (meets PhD standards)
- ⚠️ MINOR REVISIONS NEEDED (small fixes to interpretation or documentation)
- ❌ MAJOR REVISIONS NEEDED (re-analysis or significant interpretation changes)

---

## Recommendations

### Required Changes (Must Address Before Approval)

[If status = APPROVED, write "None - all results validated"]

1. **[Issue 1]**
   - **Location:** [Which file/section]
   - **Problem:** [What's wrong]
   - **Fix:** [Specific action needed]
   - **Rationale:** [Why this is critical]

---

### Suggested Improvements (Optional)

1. **[Suggestion 1]**
   - **Location:** [Which file/section]
   - **Current:** [What it says/shows]
   - **Suggested:** [What it should say/show]
   - **Benefit:** [Why this would improve quality]

---

### Next Steps

**If APPROVED:**
1. ✅ Results validated and ready for thesis
2. Invoke scholar agent to complete Section 9 (Theoretical Implications)
3. Invoke statistics-expert agent for second audit (Section 7)
4. Update status.md to "results_inspection: complete"

**If CONDITIONAL:**
1. Address required changes in info.md
2. No re-analysis needed (statistical results are correct)
3. Re-invoke results-inspector after revisions

**If REJECTED:**
1. Address critical issues (may require re-analysis)
2. Fix analysis-executor errors or re-run with different parameters
3. Re-invoke results-inspector after fixes

---

## Decision

**Final Status:** ✅ APPROVED / ⚠️ CONDITIONAL / ❌ REJECTED

**Reasoning:**
[Paragraph explaining decision]

**Confidence Level:** High / Medium / Low
[Based on statistical quality, completeness, interpretation soundness]

---

## Inspection Metadata

**Agent Version:** results_inspector v1.0
**Inspection Duration:** [X minutes]
**Files Inspected:** [N]
**Statistical Tests Validated:** [N]
**Plots Reviewed:** [N]
**Documentation Pages Reviewed:** [N]

---

**End of Results Inspection Report**
