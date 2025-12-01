# Chapter 5 Validation Results: rq_scholar + rq_stats

**Generated:** 2025-12-01 ~17:00
**Purpose:** Guide for fixing 1_concept.md issues across 16 TODO RQs

---

## Summary Table

| RQ | Type | rq_scholar | rq_stats | Overall Status |
|----|------|------------|----------|----------------|
| 5.2.6 | Domains | 9.3 ✅ APPROVED | 8.95 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.2.7 | Domains | 9.2 ✅ APPROVED | 8.7 ❌ REJECTED | ✅ **FIXED** (2025-12-01) |
| 5.2.8 | Domains | 9.2 ✅ APPROVED | 8.8 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.3.3 | Paradigms | 9.3 ✅ APPROVED | 8.5 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.3.4 | Paradigms | 9.3 ✅ APPROVED | 9.15 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.3.5 | Paradigms | 8.9 ⚠️ CONDITIONAL | 9.5 ✅ APPROVED | ✅ **FIXED** (2025-12-01) |
| 5.3.6 | Paradigms | 9.4 ✅ APPROVED | 9.15 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.3.7 | Paradigms | 9.1 ⚠️ CONDITIONAL | 9.1 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.3.8 | Paradigms | 9.3 ✅ APPROVED | 8.5 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.3.9 | Paradigms | 9.3 ✅ APPROVED | 9.8 ✅ APPROVED | ✅ READY |
| 5.4.3 | Congruence | 9.3 ✅ APPROVED | 9.1 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.4.4 | Congruence | 9.3 ✅ APPROVED | 8.9 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.4.5 | Congruence | 9.35 ✅ APPROVED | 9.1 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.4.6 | Congruence | 9.1 ⚠️ CONDITIONAL | 9.1 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.4.7 | Congruence | 9.4 ✅ APPROVED | 9.0 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |
| 5.4.8 | Congruence | 9.3 ✅ APPROVED | 8.7 ⚠️ CONDITIONAL | ✅ **FIXED** (2025-12-01) |

**Totals:**
- rq_scholar: 13 APPROVED, 3 CONDITIONAL, 0 REJECTED
- rq_stats: 2 APPROVED, 13 CONDITIONAL, 1 REJECTED
- **ALL 16 TODO RQs NOW FIXED AND READY FOR rq_planner (2025-12-01)**

---

## Common Issues Across RQs

### 1. LMM Convergence Strategy (Affects: 5.2.6, 5.3.3, 5.3.4, 5.3.6, 5.3.7, 5.4.3, 5.4.6)

**Problem:** Random slopes with N=100 frequently fail to converge. No fallback specified.

**Fix Template (add to Section 6 or 7):**
```
### Convergence Contingency Plan

If the full model (random slopes) fails to converge:
1. Try alternative optimizers (bobyqa, nlminb)
2. Use likelihood ratio test (LRT) to compare random slopes vs intercept-only
3. If LRT p < 0.05, retain slopes with simplified correlation structure
4. If LRT p ≥ 0.05, use random intercepts-only model
5. Document which structure achieved in results

Reference: Bates et al. (2015) parsimonious mixed models guidelines.
```

### 2. LMM Assumption Validation (Affects: 5.2.6, 5.3.3, 5.3.4, 5.4.3, 5.4.6, 5.4.8)

**Problem:** No specification of residual diagnostics, normality checks, homoscedasticity tests.

**Fix Template (add as Section 7 or subsection):**
```
### Validation Procedures

**LMM Assumption Checks:**
1. **Residual Normality:** Q-Q plot + Shapiro-Wilk test (accept if p > 0.01)
2. **Homoscedasticity:** Residuals vs fitted plot; Levene's test by group
3. **Random Effects Normality:** Q-Q plot of random effect estimates
4. **Independence:** ACF plot of residuals (no significant autocorrelation)
5. **Linearity:** Residuals vs each predictor (no systematic patterns)
6. **Outliers:** Cook's distance < 4/N threshold

**Remedial Actions:**
- If normality violated: Report robust standard errors or transform DV
- If heteroscedasticity: Use weighted LMM or variance function
- If outliers detected: Sensitivity analysis with/without outliers
```

### 3. Practice Effects Acknowledgment (Affects: 5.2.6, 5.3.3, 5.3.5, 5.3.7, 5.4.6)

**Problem:** 4-session repeated testing creates practice effect confounds not discussed.

**Fix Template (add to Theoretical Background or Limitations):**
```
### Practice Effects Consideration

The 4-session design (Days 0, 1, 3, 6) creates potential practice effects:
- Literature documents 13.3% improvement in episodic memory with repeated testing
- IRT theta scoring partially mitigates item-level practice effects
- Test Session will be included as a fixed effect covariate in LMM analyses
- Session × [main predictor] interaction will be examined to detect differential practice

Reference: BMC Neuroscience practice effects longitudinal study.
```

### 4. Binary Response → GLMM (Affects: 5.2.8, 5.4.8)

**Problem:** Using LMM for binary (0/1) response data violates normality assumptions.

**Fix Template:**
```
### Statistical Model Specification

**Primary Analysis:** Generalized Linear Mixed Model (GLMM) with binomial family and logit link.

Formula: `Response ~ Time * Predictor + (Time | UID) + (1 | Item)`
Family: binomial (link = "logit")

**Justification:** Item-level responses are binary (correct/incorrect), requiring GLMM rather than linear LMM. Coefficients represent log-odds; will report odds ratios for interpretation.

**Implementation:** pymer4 Lmer() with family='binomial' parameter.
```

### 5. K-means vs LCA Justification (Affects: 5.2.7, 5.3.8, 5.4.7)

**Problem:** K-means chosen without justifying against Latent Class/Profile Analysis.

**Fix Template:**
```
### Clustering Method Selection

**Method:** K-means clustering with BIC-based model selection (K=2-6)

**Justification for K-means over Latent Profile Analysis (LPA):**
1. Exploratory nature of analysis (discovering patterns, not testing model fit)
2. Interpretability of cluster centroids for clinical translation
3. Computational efficiency for sensitivity analyses
4. N=100 at lower bound for stable LPA estimation

**Robustness Checks:**
- Silhouette score (target ≥ 0.40) for cluster cohesion
- Davies-Bouldin index (target < 1.5) for cluster separation
- Bootstrap stability (100 iterations, Jaccard > 0.75)

**Sensitivity:** If K-means shows poor cluster metrics, Gaussian Mixture Models will be tested as alternative.
```

### 6. Cluster Validation Metrics (Affects: 5.2.7, 5.3.8, 5.4.7)

**Problem:** BIC alone insufficient for cluster validation. Need silhouette/stability metrics.

**Fix Template (add to Analysis Approach):**
```
### Cluster Validation

**Model Selection:** BIC across K=2-6 (select minimum)

**Quality Metrics:**
- Silhouette Score: Target ≥ 0.40 (acceptable cluster cohesion)
- Davies-Bouldin Index: Target < 1.5 (acceptable cluster separation)

**Stability Assessment:**
- Bootstrap resampling: 100 iterations, 80% subsampling
- Jaccard Index threshold: > 0.75 for stable clusters
- If stability < 0.75: Report as "tentative clustering" and interpret cautiously

**Cluster Size Constraint:** Each cluster must contain ≥ 10% of sample (N ≥ 10)
```

---

## RQ-Specific Required Changes

### 5.2.6 (Variance Decomposition - Domains) ✅ FIXED

**rq_scholar (9.3 APPROVED):** No changes required. Suggested: Add practice effects mitigation paragraph.

**rq_stats (8.95 CONDITIONAL):** 3 required changes:
1. Add formal "Section 7: Validation Procedures" with assumption checks
2. Specify convergence remedial action protocol
3. Justify or update ICC threshold (0.40 vs 0.50 standard)

**Files to edit:** `results/ch5/5.2.6/docs/1_concept.md`

**FIXES APPLIED (2025-12-01):**
- ✅ Added "Validation Procedures" section with 6 LMM assumption checks
- ✅ Added "Convergence Contingency Plan" with 5-step fallback strategy
- ✅ Added "Remedial Actions" for assumption violations
- ✅ Added "ICC Threshold Justification" citing Koo & Li (2016) and McGraw & Wong (1996)
- ✅ Added "Practice Effects Consideration" section

---

### 5.2.7 (Domain-Based Clustering) ✅ FIXED

**rq_scholar (9.2 APPROVED):** No changes required.

**rq_stats (8.7 REJECTED):** 5 required changes:
1. **CRITICAL:** Justify K-means choice vs LCA/LPA with explicit rationale
2. Validate spherical cluster assumption (add diagnostic)
3. Specify BIC calculation method
4. Add cluster stability assessment (bootstrap Jaccard)
5. Specify minimum cluster size handling

**Files to edit:** `results/ch5/5.2.7/docs/1_concept.md`

**FIXES APPLIED (2025-12-01):**
- ✅ Added "Clustering Method Selection" section with 5-point K-means vs LPA justification
- ✅ Added "Alternative Method Consideration" (GMM sensitivity analysis if quality fails)
- ✅ Added outlier check to Step 2 (|z| > 3 documentation)
- ✅ Added parsimony rule for BIC selection (ΔBIC < 2)
- ✅ Added "Step 4b: Cluster Validation" with silhouette (≥0.40), Davies-Bouldin (<1.5), bootstrap Jaccard (>0.75)
- ✅ Added visual sphericity check to Step 6
- ✅ Updated Expected Outputs with step04b_cluster_validation.csv
- ✅ Updated Success Criteria with cluster quality thresholds
- ✅ Added "If Cluster Quality Fails" contingency section

---

### 5.2.8 (Domain × Item Difficulty) ✅ FIXED

**rq_scholar (9.2 APPROVED):** No changes required.

**rq_stats (8.8 CONDITIONAL):** 3 required changes:
1. **CRITICAL:** Specify Binomial GLMM with logit link (not linear LMM)
2. Clarify exploratory vs confirmatory design (Bonferroni inconsistency)
3. Pre-specify random effect model selection strategy

**Files to edit:** `results/ch5/5.2.8/docs/1_concept.md`

**FIXES APPLIED (2025-12-01):**
- ✅ Changed Analysis Type from LMM to GLMM with binomial family and logit link
- ✅ Added "Statistical Model Specification" section with GLMM justification
- ✅ Added "Exploratory vs Confirmatory Design" section clarifying design type
- ✅ Fixed multiple testing: omnibus α=0.05, post-hoc α=0.0167 (only if omnibus significant)
- ✅ Added "Step 4b: Random Effects Model Selection" with 5-step convergence fallback
- ✅ Updated Step 5 to report odds ratios with 95% CIs
- ✅ Updated Expected Outputs (glmm_model_summary.txt, odds ratios)
- ✅ Updated Success Criteria with OR interpretation and random effects documentation
- ✅ Added "Validation Procedures" section with GLMM-specific assumption checks (overdispersion, link function)
- ✅ Added "Remedial Actions" for GLMM issues

---

### 5.3.3 (Consolidation Window - Paradigms)

**rq_scholar (9.3 APPROVED):** Suggested: Pre-register practice-effects analysis, clarify consolidation timescales.

**rq_stats (8.5 CONDITIONAL):** 3 required changes:
1. **CRITICAL:** Add comprehensive assumption validation procedures
2. Specify model selection strategy for random effects
3. Justify linear time-behavior assumption within segments

**Files to edit:** `results/ch5/5.3.3/docs/1_concept.md`

---

### 5.3.4 (Age × Paradigm)

**rq_scholar (9.3 APPROVED):** No changes required.

**rq_stats (9.15 CONDITIONAL):** 4 required changes:
1. Specify LMM assumption diagnostic tests
2. Pre-specify model structure selection (LRT comparison)
3. Document log transformation rationale (log(TSVR_hours + 1))
4. Clarify Bonferroni correction family

**Files to edit:** `results/ch5/5.3.4/docs/1_concept.md`

---

### 5.3.5 (IRT-CTT Convergence - Paradigms)

**rq_scholar (8.9 CONDITIONAL):** 3 required changes:
1. **CRITICAL:** Explicitly address practice effects
2. **CRITICAL:** Test for Differential Item Functioning (DIF) by test session
3. Clarify linking method and scale standardization

**rq_stats (9.5 APPROVED):** No changes required. Suggested: Cite Fornell & Larcker for r > 0.70 threshold.

**Files to edit:** `results/ch5/5.3.5/docs/1_concept.md`

---

### 5.3.6 (Purified CTT Effects - Paradigms)

**rq_scholar (9.4 APPROVED):** Suggested: Add practice effects discussion, acknowledge encoding quality alternative.

**rq_stats (9.15 CONDITIONAL):** 3 required changes:
1. **CRITICAL:** LMM random slopes convergence risk - add fallback strategy
2. Steiger's z-test assumptions unverified - add checks
3. Cronbach's alpha confounded by item count - add Spearman-Brown adjustment

**Files to edit:** `results/ch5/5.3.6/docs/1_concept.md`

---

### 5.3.7 (Variance Decomposition - Paradigms)

**rq_scholar (9.1 CONDITIONAL):** 3 required changes:
1. Add 5-6 high-relevance citations (2020-2024)
2. Add practice effects discussion to Section 4
3. Add Limitations section covering ceiling effects and dropout bias

**rq_stats (9.1 CONDITIONAL):** 3 required changes:
1. **CRITICAL:** Add residual diagnostics (normality, homoscedasticity)
2. Specify convergence contingency plan
3. Clarify scale (log vs original) for ICC interpretation

**Files to edit:** `results/ch5/5.3.7/docs/1_concept.md`

---

### 5.3.8 (Paradigm-Based Clustering)

**rq_scholar (9.3 APPROVED):** Suggested: Add ceiling effects check, BIC + silhouette robustness.

**rq_stats (8.5 CONDITIONAL):** 4 required changes:
1. Add secondary cluster validation criteria (silhouette ≥ 0.5, Dunn index)
2. Implement cluster stability assessment (bootstrap Jaccard ≥ 0.80)
3. Address sphericity assumption
4. Justify K-means vs Latent Profile Analysis

**Files to edit:** `results/ch5/5.3.8/docs/1_concept.md`

---

### 5.3.9 (Paradigm × Item Difficulty)

**rq_scholar (9.3 APPROVED):** No changes required.

**rq_stats (9.8 APPROVED):** No changes required. ✅ **READY FOR rq_planner**

**Files to edit:** None required

---

### 5.4.3 (Age × Schema)

**rq_scholar (9.3 APPROVED):** Suggested: Engage with theoretical debate, address practice effects.

**rq_stats (9.1 CONDITIONAL):** 3 required changes:
1. Add remedial procedures for assumption violations
2. Specify random effects model selection strategy
3. Clarify congruence reference category and contrast coding

**Files to edit:** `results/ch5/5.4.3/docs/1_concept.md`

---

### 5.4.4 (IRT-CTT Convergence - Congruence)

**rq_scholar (9.3 APPROVED):** Suggested: Add practice effects acknowledgment, stratify correlations by time point.

**rq_stats (8.9 CONDITIONAL):** 3 required changes:
1. Clarify Cohen's kappa implementation (define categories)
2. Specify sample size per congruence category with confidence intervals
3. Operationalize random structure simplification strategy

**Files to edit:** `results/ch5/5.4.4/docs/1_concept.md`

---

### 5.4.5 (Purified CTT Effects - Congruence)

**rq_scholar (9.35 APPROVED):** Suggested: Add literature citations, acknowledge practice effects.

**rq_stats (9.1 CONDITIONAL):** 3 required changes:
1. Explicit z-standardization rationale
2. Bivariate normality assumption check (before Steiger's z-test)
3. Missing data handling specification

**Files to edit:** `results/ch5/5.4.5/docs/1_concept.md`

---

### 5.4.6 (Variance Decomposition - Congruence)

**rq_scholar (9.1 CONDITIONAL):** 1 required + 3 suggested:
1. **Required:** Add practice effects discussion
2. Suggested: Add ceiling effect check, VR sickness limitation, mechanism clarity

**rq_stats (9.1 CONDITIONAL):** 2 required changes:
1. **CRITICAL:** Document convergence failure strategy
2. **CRITICAL:** Add homoscedasticity testing procedure

**Files to edit:** `results/ch5/5.4.6/docs/1_concept.md`

---

### 5.4.7 (Schema-Based Clustering)

**rq_scholar (9.4 APPROVED):** Suggested: Add literature citations, acknowledge practice effects.

**rq_stats (9.0 CONDITIONAL):** 4 required changes:
1. Add cluster quality validation thresholds (silhouette ≥ 0.40, Davies-Bouldin < 1.5)
2. Add bootstrap/cross-validation stability assessment
3. Address sphericity assumption
4. Justify K-means vs Latent Profile Analysis

**Files to edit:** `results/ch5/5.4.7/docs/1_concept.md`

---

### 5.4.8 (Congruence × Item Difficulty)

**rq_scholar (9.3 APPROVED):** Suggested: Strengthen Initial Strength section, add practice effects discussion.

**rq_stats (8.7 CONDITIONAL):** 4 required changes:
1. **CRITICAL:** Add comprehensive LMM assumption validation
2. **CRITICAL:** Acknowledge binary response issue & justify LMM or use GLMM
3. **CRITICAL:** Specify power analysis for 3-way interaction
4. Expand convergence contingency plan

**Files to edit:** `results/ch5/5.4.8/docs/1_concept.md`

---

## Fix Priority Order

**Tier 1 - REJECTED (Fix First):**
1. ~~5.2.7 - K-means vs LCA justification (blocking issue)~~ ✅ FIXED

**Tier 2 - Binary Response (Methodological Error):**
2. ~~5.2.8 - Change LMM to GLMM~~ ✅ FIXED
3. 5.4.8 - Change LMM to GLMM or justify

**Tier 3 - Common Fixes (Apply Template):**
4. ~~5.2.6 - Add convergence strategy + assumption validation~~ ✅ FIXED
5. All remaining LMM RQs - Add convergence strategy template (5.3.3, 5.3.4, 5.3.6, 5.3.7, 5.4.3, 5.4.6)
6. All remaining clustering RQs - Add cluster validation metrics template (5.3.8, 5.4.7)

**Tier 4 - Scholar Fixes:**
7. 5.3.5, 5.3.7, 5.4.6 - Add practice effects discussion

**Tier 5 - Already Ready:**
8. 5.3.9 - No fixes needed, proceed to rq_planner
9. **5.2.6, 5.2.7, 5.2.8 - Now ready for rq_planner**

---

## Detailed Validation Reports

Full validation reports with rubric breakdowns, devil's advocate criticisms, and literature citations are available at:

- `results/ch5/5.X.X/docs/1_scholar.md` - Scholarly validation
- `results/ch5/5.X.X/docs/1_stats.md` - Statistical validation

Each report contains:
- 5-category rubric scoring with justifications
- Devil's advocate criticisms (commission errors, omission errors, alternatives, pitfalls)
- WebSearch literature citations
- Required changes with specific locations
- Suggested improvements (optional)

---

## Next Steps

1. **Apply common fix templates** to all affected RQs (convergence, assumptions, practice effects)
2. **Fix REJECTED 5.2.7** with K-means justification
3. **Fix binary response RQs** (5.2.8, 5.4.8) with GLMM specification
4. **Run rq_planner** on 5.3.9 (already ready) while fixing others
5. **Re-validate** fixed RQs if desired (optional - master can verify changes directly)
