# PLATINUM Certification Plan for RQ 6.2.2

**Date:** 2025-12-28
**Current Status:** PASS WITH NOTES (3 moderate issues)
**Target:** PLATINUM STATUS

---

## MANDATORY TASKS (BLOCKERS)

### 1. Difference Score Reliability Computation ⚠️ BLOCKER
**Priority:** 🔴 CRITICAL
**Time:** 30-45 minutes
**Taxonomy Section:** 6.2

**Issue:** Calibration = confidence - theta_accuracy (difference score). Reliability NOT computed.

**Actions:**
1. Compute r(theta_accuracy, theta_confidence) correlation
2. Get reliabilities from IRT models (Ch5 5.1.1 for accuracy, 6.1.1 for confidence)
3. Apply formula: r_diff = (r_xx + r_yy - 2*r_xy) / (2 - 2*r_xy)
4. Document in validation.md
5. If r_diff < 0.70 → **STOP**, need SEM/latent variable approach

**Output:** validation.md section, add to summary.md limitations

---

### 2. Confidence Response Patterns ⚠️ MANDATORY
**Priority:** 🔴 CRITICAL (Section 1.4 requirement)
**Time:** 1-2 hours
**Taxonomy Section:** 8.3

**Issue:** Confidence RQs MUST document response patterns per taxonomy Section 8.3.

**Actions:**
1. % participants using full scale (1-5)
2. % extremes only (1s and 5s)
3. Mean SD of ratings per participant
4. Flag restricted range (SD < 0.8)
5. Document in summary.md limitations

**Data Source:** results/ch6/6.1.1/ (omnibus confidence data)

**Output:** New summary.md section 3.X (Limitations subsection)

---

## HIGH PRIORITY TASKS

### 3. Mixed-Effects Logistic Regression
**Priority:** 🟡 HIGH
**Time:** 30-45 minutes
**Taxonomy Section:** 4.4

**Issue:** Current logistic regression assumes independence but data are clustered (4 obs/participant).

**Actions:**
1. Fit GLMM: `overconfident ~ time + (1|UID)` using statsmodels MixedLM
2. Compare SEs to original model
3. Check if p-value changes (currently p=0.230, unlikely to become significant)
4. Update summary.md with corrected results
5. Keep original as sensitivity check

**Output:** New analysis script, updated summary.md Section 1

---

### 4. Model Fit Diagnostics
**Priority:** 🟡 HIGH
**Time:** 15-20 minutes
**Taxonomy Section:** 5.1

**Issue:** Logistic model fit quality not assessed.

**Actions:**
1. Compute Hosmer-Lemeshow goodness-of-fit test
2. Generate deviance residual plot
3. Check leverage/influence (large Cook's D?)
4. Document in validation.md

**Output:** validation.md update, diagnostic plots

---

## MEDIUM PRIORITY TASKS

### 5. Documentation Clarifications
**Priority:** 🟢 MEDIUM
**Time:** 10-15 minutes

**Actions:**
1. Clarify multiple comparisons: mean calibration is DESCRIPTIVE not second hypothesis test
2. Update summary.md to note explicit status
3. Cross-reference RQ 6.2.1 more clearly

---

## ESTIMATED TIMELINE

| Task | Priority | Time | Cumulative |
|------|----------|------|------------|
| 1. Difference score reliability | 🔴 BLOCKER | 45 min | 45 min |
| 2. Response patterns | 🔴 MANDATORY | 2 hours | 2h 45min |
| 3. Mixed-effects logistic | 🟡 HIGH | 45 min | 3h 30min |
| 4. Model diagnostics | 🟡 HIGH | 20 min | 3h 50min |
| 5. Documentation | 🟢 MEDIUM | 15 min | 4h 5min |

**TOTAL:** 4-5 hours to PLATINUM status

---

## CIRCUIT BREAKERS

### Difference Score Reliability < 0.70
**Trigger:** If r_diff < 0.70
**Action:** STOP analysis, implement SEM approach
**Impact:** Adds 4-6 hours per calibration RQ (affects all 6.2.X-6.5.X series)

### Mixed-Effects Model Non-Convergence
**Trigger:** If GLMM fails to converge
**Action:** Try simplified random effects, alternative optimizer
**Impact:** Document limitation, keep original logistic model

---

## SUCCESS CRITERIA (PLATINUM)

✅ **Statistical Rigor:**
- [x] Assumptions validated (logistic convergence ✓, need diagnostics)
- [ ] Difference score reliability computed
- [x] Effect sizes with CIs ✓
- [x] Power analysis documented ✓

✅ **Methodological Soundness:**
- [ ] Mixed-effects model for clustering
- [x] Appropriate model (logistic for binary trend) ✓
- [ ] Difference score reliable (r_diff ≥ 0.70)
- [x] No Lord's Paradox (no group comparisons) ✓

✅ **Documentation Excellence:**
- [x] Dual metrics (proportion + mean calibration) ✓
- [x] Dual p-values (N/A, only one test) ✓
- [x] Plots current ✓
- [x] Complete summary.md ✓

✅ **Data Quality:**
- [x] IRT purification documented ✓
- [ ] Response patterns documented (MANDATORY)

✅ **Theoretical Coherence:**
- [x] Literature grounded ✓
- [x] Mechanistic explanation ✓
- [x] Boundary conditions ✓

✅ **Zero Critical Issues:**
- [x] No convergence failures ✓
- [ ] No missing mandatory analyses (need #1, #2)
- [x] No unresolved anomalies ✓

---

## NEXT STEPS

1. Compute difference score reliability (BLOCKER)
2. If r_diff ≥ 0.70 → Proceed
3. Document confidence response patterns (MANDATORY)
4. Fit mixed-effects logistic (HIGH priority)
5. Add model diagnostics (HIGH priority)
6. Final documentation polish
7. PLATINUM certification

---

**Prepared by:** rq_platinum agent
**Date:** 2025-12-28
