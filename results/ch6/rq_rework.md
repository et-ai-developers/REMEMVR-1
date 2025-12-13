# Chapter 6 Statistical Validity Rework Plan

**Created:** 2025-12-13
**Last Updated:** 2025-12-13 21:30
**Purpose:** Comprehensive validity improvements for thesis-quality episodic memory/metacognition findings
**Scope:** 31 RQs across Chapter 6, cross-chapter dependencies with Ch5

---

## HOW TO USE THIS DOCUMENT

**THIS DOCUMENT IS FOR CLAUDE'S USE** - It is the authoritative source for all Ch6 validity rework tasks. Keeping it updated is MANDATORY.

### At Session Start
1. Run `/refresh` to load state.md
2. Read this file (`results/ch6/rq_rework.md`) - MANDATORY before any work
3. Check "CURRENT STATUS DASHBOARD" for what's done/pending
4. Use TodoWrite to create task list from next pending tier
5. Work through tasks in priority order

### During Task Execution
1. **IMMEDIATELY notify user** if ANY of the following occur:
   - A task cannot be completed as specified (blocked, missing data, etc.)
   - Results differ substantially from expectations (e.g., ICC changes by >20%)
   - A finding becomes non-robust or changes direction
   - Additional issues discovered that aren't in this document
   - A compromise or methodological decision is needed
   - Uncertainty about interpretation or next steps
2. **DO NOT make judgment calls silently** - User must approve any deviations
3. **Document discoveries in APPENDIX E** (Issues Log) as they arise
4. Update task status checkboxes IN REAL-TIME (not at end of session)

### At Session End
1. Update ALL checkboxes in relevant sections
2. Add completion notes with dates to APPENDIX C (Session Log)
3. Add any new issues to APPENDIX E (Issues Log)
4. Verify CURRENT STATUS DASHBOARD reflects true state
5. Run `/save` to preserve progress

### CRITICAL: Document Maintenance Rules
1. **This document MUST stay current** - It is the single source of truth
2. **Never leave stale information** - Update status immediately when things change
3. **Add new tasks here** if discovered during work (in appropriate tier)
4. **Cross-reference state.md** - Both should be consistent
5. **If document becomes outdated, STOP and fix it first**

### User Notification Protocol
**ALWAYS ASK USER via AskUserQuestion tool when:**
- [ ] A statistical finding changes substantially (effect size, direction, significance)
- [ ] A task reveals a previously unknown methodological issue
- [ ] Multiple valid approaches exist and a choice must be made
- [ ] A compromise between rigor and feasibility is needed
- [ ] Something doesn't match what's documented here
- [ ] Interpretation of results is ambiguous
- [ ] Any decision could affect thesis conclusions

**Format for notifications:**
```
🔔 REWORK ISSUE: [Brief description]

Task: T1.X - [Task name]
Issue: [What happened]
Options:
  A) [Option 1]
  B) [Option 2]
Impact: [How this affects findings]

Awaiting your decision before proceeding.
```

**Key Principle:** Each task is self-contained with inputs, outputs, and success criteria. No guessing required. When in doubt, ASK.

---

## CURRENT STATUS DASHBOARD

**Last Reviewed:** 2025-12-13 21:30

### Completed Work (Model Averaging Phase)
- [x] Model averaging: 5/5 ROOT RQs complete (6.1.1, 6.3.1, 6.4.1, 6.5.1, 6.8.1)
- [x] Ch5 5.1.1 MA residuals created (51 models, Eff_N=40.09)
- [x] RQ 6.7.3 fixed to use MA residuals (NULL robust: r=-0.05)
- [x] `tools/model_averaging.py` enhanced (779 lines)
- [x] `docs/lmm_methodology.md` created
- [x] All ROOT RQ summary.md files updated with MA sections

### Pending Work (Validity Enhancement Phase)
- [ ] **TIER 1 - CRITICAL** (2 days) - Protects major findings
- [ ] **TIER 2 - HIGH** (3-4 days) - Strengthens defensibility
- [ ] **TIER 3 - MODERATE** (1-2 weeks) - Publication quality
- [ ] **TIER 4 - LOW** (optional) - Theoretical completeness

**Quick Reference - What's At Risk:**
| Finding | Risk Level | Mitigation Task |
|---------|------------|-----------------|
| 824× ICC ratio (6.1.4) | HIGH | T1.1 - Validate with MA random effects |
| Metacognitive sensitivity (6.7.2) | HIGH | T1.2 - Bootstrap robustness (p=0.034 marginal) |
| Paradigm calibration (6.4.2) | MODERATE | T1.3 - Lord's paradox sensitivity |
| Domain dissociation (6.3.4) | LOW | T2.5 - Convergence sensitivity |

---

## TIER 1: CRITICAL (Must Complete Before Defense)

**Estimated Time:** 2 days
**Priority:** These protect thesis-critical findings from methodological challenges

### T1.1 - Validate 824× ICC with Model-Averaged Random Effects

**Status:** [ ] NOT STARTED
**RQ:** 6.1.4
**Time:** 30 minutes
**Why Critical:** The 824× ICC ratio is a **thesis centerpiece** finding. Currently computed from single "best" model (Recip_sq, 21.7% weight), ignoring 78% of model evidence.

**Inputs:**
- `results/ch6/6.1.1/data/step05b_model_averaged_random_effects.csv` (already exists)
- Contains: UID, ma_intercept, ma_slope, ma_intercept_var, ma_slope_var

**Task:**
1. Read MA random effects from 6.1.1
2. Compute ICC_slope_MA = var(ma_slope) / [var(ma_slope) + residual_var]
3. Compare to original ICC_slope = 0.41
4. Recompute the ratio: ICC_confidence_slope / ICC_accuracy_slope

**Expected Output:**
- `results/ch6/6.1.4/data/step06b_icc_ma_validation.csv`
- Updated comparison in `results/ch6/6.1.4/results/summary.md`

**Success Criteria:**
- [ ] MA ICC_slope computed
- [ ] Ratio remains >500× (finding robust) OR change documented
- [ ] summary.md updated with MA validation section

**Code Template:**
```python
# results/ch6/6.1.4/code/step06b_icc_ma_validation.py
import pandas as pd
import numpy as np

# Load MA random effects
ma_re = pd.read_csv('results/ch6/6.1.1/data/step05b_model_averaged_random_effects.csv')

# Compute MA ICC for slopes
var_slope_ma = ma_re['ma_slope'].var()
# Need residual variance from original LMM or estimate from data
# ICC_slope_MA = var_slope_ma / (var_slope_ma + var_residual)

# Compare to original ICC_slope = 0.41
# Original ratio = 824×
# MA ratio = ICC_slope_MA / ICC_accuracy_slope (from Ch5)
```

---

### T1.2 - Bootstrap Robustness for Partial Correlation (6.7.2)

**Status:** [ ] NOT STARTED
**RQ:** 6.7.2
**Time:** 1 day
**Why Critical:** p=0.034 is marginal. Finding shows metacognitive sensitivity (confidence variability predicts forgetting beyond ability). Needs validation.

**Current Finding:**
- Partial r = 0.21 (SD_confidence → forgetting | accuracy controlled)
- p = 0.034 (two-tailed)
- Effect interpretation: Confidence variability has unique variance for predicting forgetting

**Inputs:**
- `results/ch6/6.7.2/data/step03_person_summary.csv`
- Variables: UID, SD_confidence, SD_accuracy, forgetting_slope

**Tasks:**
1. Bootstrap 95% CI (10,000 resamples) for partial r
2. Leave-one-out cross-validation (100 iterations)
3. Outlier sensitivity (remove extreme SD values, re-test)
4. Permutation test (1,000 permutations) for non-parametric p-value

**Expected Outputs:**
- `results/ch6/6.7.2/data/step04b_bootstrap_results.csv`
- `results/ch6/6.7.2/data/step04b_loo_results.csv`
- `results/ch6/6.7.2/results/robustness_analysis.md`

**Success Criteria:**
- [ ] Bootstrap 95% CI excludes 0 → finding robust
- [ ] LOO r values all positive (same direction)
- [ ] Permutation p < 0.05 → parametric p confirmed
- [ ] summary.md updated with robustness section

**Code Template:**
```python
# results/ch6/6.7.2/code/step04b_robustness_analysis.py
import numpy as np
import pandas as pd
from scipy import stats

def bootstrap_partial_r(data, n_bootstrap=10000):
    """Bootstrap CI for partial correlation."""
    partial_rs = []
    for _ in range(n_bootstrap):
        sample = data.sample(frac=1.0, replace=True)
        # Compute partial r for this sample
        # ...
        partial_rs.append(r)
    return np.percentile(partial_rs, [2.5, 97.5])

def leave_one_out(data):
    """LOO cross-validation for stability."""
    loo_rs = []
    for i in range(len(data)):
        subset = data.drop(data.index[i])
        # Compute partial r without participant i
        # ...
        loo_rs.append(r)
    return loo_rs
```

---

### T1.3 - Lord's Paradox Sensitivity Check (6.4.2)

**Status:** [ ] NOT STARTED
**RQ:** 6.4.2
**Time:** 2-3 hours
**Why Critical:** Paradigm calibration differences may be regression artifact if paradigms differ in baseline accuracy.

**Current Finding:**
- IFR: calibration ≈ 0 (well-calibrated)
- ICR: calibration = +0.09 (slight overconfidence)
- IRE: calibration = +0.11 (slight overconfidence)
- Interpretation: Free Recall best calibrated

**Problem:**
- Calibration = z(confidence) - z(accuracy)
- If accuracy differs by paradigm (it does: IRE > IFR > ICR), z-standardization may create spurious differences
- Lord's paradox: Group differences in change scores can be artifacts of baseline differences

**Inputs:**
- `results/ch6/6.4.2/data/step03_calibration_data.csv`
- Variables: UID, paradigm, confidence_theta, accuracy_theta, calibration

**Tasks:**
1. ANCOVA: calibration ~ paradigm + baseline_accuracy (partial out accuracy)
2. Within-paradigm z-standardization (z-score confidence/accuracy separately per paradigm)
3. Compare calibration differences: Original vs ANCOVA vs Within-paradigm

**Expected Outputs:**
- `results/ch6/6.4.2/data/step04b_lords_paradox_check.csv`
- `results/ch6/6.4.2/results/sensitivity_analysis.md`

**Success Criteria:**
- [ ] ANCOVA paradigm effect p-value computed
- [ ] Within-paradigm calibration differences computed
- [ ] If all 3 approaches agree → finding robust
- [ ] If approaches disagree → document limitation

**Code Template:**
```python
# results/ch6/6.4.2/code/step04b_lords_paradox_sensitivity.py
import statsmodels.formula.api as smf

# Method 1: ANCOVA (partial out accuracy)
model = smf.ols('calibration ~ C(paradigm) + accuracy_theta', data=df).fit()
print(model.summary())

# Method 2: Within-paradigm standardization
for paradigm in ['IFR', 'ICR', 'IRE']:
    mask = df['paradigm'] == paradigm
    df.loc[mask, 'z_conf_within'] = stats.zscore(df.loc[mask, 'confidence_theta'])
    df.loc[mask, 'z_acc_within'] = stats.zscore(df.loc[mask, 'accuracy_theta'])
df['calibration_within'] = df['z_conf_within'] - df['z_acc_within']

# Compare
print("Original calibration by paradigm:", df.groupby('paradigm')['calibration'].mean())
print("Within-paradigm calibration:", df.groupby('paradigm')['calibration_within'].mean())
```

---

### T1.4 - Difference Score Reliability Check (6.4.2)

**Status:** [ ] NOT STARTED
**RQ:** 6.4.2
**Time:** 1-2 hours
**Why Critical:** If difference score reliability < 0.70, effect sizes (d=0.09-0.11) may be measurement noise.

**Background:**
- Calibration = z(confidence) - z(accuracy) (difference score)
- Reliability formula: r_diff = (r_xx + r_yy - 2*r_xy) / (2 - 2*r_xy)
- Where: r_xx = reliability of confidence, r_yy = reliability of accuracy, r_xy = their correlation

**Inputs:**
- IRT test information from Ch5 5.3.1 (accuracy) and Ch6 6.4.1 (confidence)
- Person-level theta estimates

**Tasks:**
1. Extract marginal reliability from IRT models (test information at mean theta)
2. Compute r(theta_accuracy, theta_confidence) across participants
3. Apply difference score reliability formula
4. Interpret: r_diff < 0.70 = unreliable difference scores

**Expected Outputs:**
- `results/ch6/6.4.2/data/step04c_reliability_check.csv`
- Report: r_xx, r_yy, r_xy, r_diff

**Success Criteria:**
- [ ] r_diff computed
- [ ] If r_diff ≥ 0.70 → effect sizes interpretable
- [ ] If r_diff < 0.70 → document limitation, effects may be noise
- [ ] summary.md updated with reliability section

---

## TIER 2: HIGH PRIORITY (Strengthen Major Findings)

**Estimated Time:** 3-4 days
**Priority:** Defense preparation - reviewers will ask these questions

### T2.1 - LMM Residual Diagnostics (Multiple RQs)

**Status:** [ ] NOT STARTED
**RQs:** 6.2.1, 6.3.2, 6.4.2, 6.6.3, 6.8.2
**Time:** 2-3 hours (automated script)
**Why Important:** Assumption violations can invalidate p-values. Reviewers WILL ask.

**Tasks per RQ:**
1. Extract residuals from fitted LMM
2. Generate QQ plot (normality check)
3. Generate residuals vs fitted plot (homoscedasticity)
4. Run Shapiro-Wilk test on residuals
5. Compute Cook's D for influential observations

**Expected Outputs per RQ:**
- `plots/diagnostic_qq.png`
- `plots/diagnostic_residuals_vs_fitted.png`
- `data/step_diagnostics.csv` (residuals, Cook's D)

**Success Criteria:**
- [ ] QQ plots approximately linear (normality OK)
- [ ] Residuals vs fitted shows no funnel pattern (homoscedasticity OK)
- [ ] No Cook's D > 1.0 (no extreme outliers)
- [ ] If violations found → document + note robustness of large N

---

### T2.2 - Post-Hoc Power Analysis for NULL Findings

**Status:** [ ] NOT STARTED
**RQs:** 6.1.3, 6.2.5, 6.3.3, 6.4.3, 6.5.2, 6.5.3, 6.7.3, 6.8.2
**Time:** 1 day
**Why Important:** Distinguishes "no effect" from "underpowered study"

**Tasks per NULL RQ:**
1. Compute minimum detectable effect size (MDES) given N=100, 4 timepoints
2. Report observed power for d=0.30 (medium effect)
3. Report observed power for d=0.20 (small effect)
4. Classify: "Well-powered null" (power >0.80 for d=0.20) vs "Underpowered" (power <0.50)

**Expected Output:**
- `results/ch6/power_analysis_null_findings.csv`
- Columns: RQ, observed_effect, MDES, power_d020, power_d030, classification

**Success Criteria:**
- [ ] Power analysis completed for all NULL RQs
- [ ] Well-powered nulls can claim "evidence of no effect"
- [ ] Underpowered nulls noted as "absence of evidence, not evidence of absence"

---

### T2.3 - Bootstrap CI for Correlation Reversal (6.8.3)

**Status:** [ ] NOT STARTED
**RQ:** 6.8.3
**Time:** 1 hour
**Why Important:** Source r=-0.24 vs Destination r=+0.58 reversal is major theoretical puzzle.

**Current Finding:**
- Source items: r(confidence, accuracy) = -0.24 (NEGATIVE)
- Destination items: r(confidence, accuracy) = +0.58 (POSITIVE)
- Interpretation: Metacognitive calibration REVERSES by item type

**Tasks:**
1. Fisher's z-test for dependent correlations (formally test if r_source ≠ r_dest)
2. Bootstrap 95% CI for difference (r_dest - r_source)
3. Effect size for reversal magnitude

**Expected Outputs:**
- `results/ch6/6.8.3/data/step04b_correlation_comparison.csv`
- Fisher's z, p-value, bootstrap CI for difference

**Success Criteria:**
- [ ] Fisher's z computed
- [ ] Bootstrap CI for difference excludes 0 → reversal is real
- [ ] Effect size for reversal documented
- [ ] summary.md updated

---

### T2.4 - Confidence Response Pattern Analysis (6.1.1, 6.8.1)

**Status:** [ ] NOT STARTED
**RQs:** 6.1.1, 6.8.1 (and potentially others)
**Time:** 2 hours
**Why Important:** Extreme response style (only 1s and 5s) violates GRM assumptions.

**Tasks:**
1. Extract raw confidence ratings (1-5 scale) from source data
2. Compute per-participant metrics:
   - % responses at each level (1, 2, 3, 4, 5)
   - % at endpoints (1 or 5)
   - SD of responses (< 0.8 indicates restricted range)
3. Flag extreme response style: >50% at endpoints
4. Test: Do theta estimates differ for ERS vs non-ERS groups?

**Expected Outputs:**
- `results/ch6/6.1.1/data/step00b_response_patterns.csv`
- `results/ch6/confidence_response_patterns.md` (cross-RQ summary)

**Success Criteria:**
- [ ] Response distribution documented
- [ ] % ERS participants identified
- [ ] If ERS >20%: Document limitation
- [ ] If ERS <10%: Note as validation of measurement quality

---

### T2.5 - LMM Convergence Sensitivity (6.3.4, 6.8.1)

**Status:** [ ] NOT STARTED
**RQs:** 6.3.4, 6.8.1
**Time:** 2-3 hours
**Why Important:** Non-positive definite Hessian warnings suggest parameter estimates at boundary.

**Current Issue:**
- 6.3.4: Boundary warning for What/Where domains
- 6.8.1: Implicit boundary issues in M1

**Tasks:**
1. Refit with compound symmetry (uncorrelated intercept/slope)
2. Refit with diagonal covariance (explicit cov=0)
3. Compare ICC_slope across specifications
4. If consistent (within ±0.05) → original robust
5. If differs >0.10 → document instability

**Expected Outputs:**
- `results/ch6/6.3.4/data/step_convergence_sensitivity.csv`
- Alternative ICC estimates

**Success Criteria:**
- [ ] Alternative covariance structures tested
- [ ] ICC_slope stable across specifications OR instability documented

---

## TIER 3: MODERATE (Publication Quality)

**Estimated Time:** 1-2 weeks
**Priority:** Enhances rigor for journal publication

### T3.1 - IRT Purification Sensitivity (6.1.1, 6.4.1, 6.5.1)

**Status:** [ ] NOT STARTED
**RQs:** 6.1.1, 6.4.1, 6.5.1
**Time:** 6-9 hours total
**Why Important:** 100% item retention is unusual (typical 40-60% exclusion). May indicate lenient thresholds.

**Current State:**
- All ROOT RQs retained 100% of items after IRT purification
- Discrimination range: 1.98-6.14 (all well above a≥0.4 threshold)

**Tasks per RQ:**
1. Refit IRT with stricter thresholds (a ≥ 0.6 instead of a ≥ 0.4, |b| ≤ 2.5)
2. Compare retention rates
3. Compare theta estimates (correlation with original)
4. If r > 0.95 → original robust
5. If r < 0.95 → document sensitivity

**Expected Outputs per RQ:**
- `data/step02b_strict_purification.csv`
- Theta comparison: original vs strict

---

### T3.2 - Equivalence Testing for NULL Findings

**Status:** [ ] NOT STARTED
**RQs:** 6.1.3, 6.2.5, 6.3.3, 6.4.3, 6.5.2, 6.5.3, 6.7.3, 6.8.2, 6.8.3
**Time:** 2-3 days
**Why Important:** TOST proves NULLs are genuine zeros, not just non-significant.

**Method:** Two One-Sided Tests (TOST)
- Define equivalence bound (e.g., d = ±0.20)
- Test H1: effect < -0.20 AND effect > +0.20
- If both rejected → effect is equivalent to zero

**Expected Output:**
- `results/ch6/equivalence_testing_summary.csv`
- Per-RQ: effect, bound, TOST p-values, equivalence conclusion

---

### T3.3 - GLMM Refit for Non-Independence Issues (6.2.2, 6.5.3)

**Status:** [ ] NOT STARTED
**RQs:** 6.2.2, 6.5.3
**Time:** 1 day
**Why Important:** Standard logistic regression ignores 4-obs-per-participant clustering.

**Current Issue:**
- 6.2.2: Logistic regression with 4 observations per participant
- 6.5.3: Linear probability model (LPM) instead of logistic GLMM

**Tasks:**
1. Refit as mixed-effects logistic regression: `y ~ X + (1|UID)`
2. Compare coefficients and p-values
3. If conclusions unchanged → original approach adequate
4. If conclusions change → update with GLMM results

---

### T3.4 - Cross-Validation for Clustering (6.1.5, 6.8.4)

**Status:** [ ] NOT STARTED
**RQs:** 6.1.5, 6.8.4
**Time:** 4-6 hours total
**Why Important:** K-means can overfit; need stability validation.

**Tasks:**
1. Split sample (N=70 train, N=30 test)
2. Fit K-means on training set
3. Assign test set to nearest centroid
4. Compare Silhouette scores (train vs test)
5. Repeat 10× with different splits
6. Report stability: mean ± SD of test Silhouette

---

## TIER 4: LOW PRIORITY (Optional Enhancements)

**Estimated Time:** Variable
**Priority:** Theoretical completeness; do if time permits

### T4.1 - Alternative Time Transformations Sensitivity

**RQs:** Multiple (those using log_TSVR or linear)
**Time:** 3-4 hours
**Task:** Refit key LMMs with sqrt(TSVR), 1/TSVR, quadratic; compare conclusions

---

### T4.2 - Derivative RQs Re-Run with MA Outputs

**RQs:** 16 derivative RQs (all except 6.1.4)
**Time:** 2-4 weeks total
**Task:** Re-execute derivatives using step05b MA outputs instead of single-model outputs
**Note:** Deferred because all show NULL or robust findings; MA outputs available if needed

---

### T4.3 - Ch5 When Domain ICC Comparison (6.3.4)

**RQ:** 6.3.4
**Time:** 1-2 hours
**Task:** Verify When domain ICC available from Ch5 5.2.6; if missing, document why (floor effects)

---

### T4.4 - Missing Documentation Creation

**Tasks:**
- [ ] Create `docs/irt_methodology.md` (GRM specs, purification criteria, MED settings)
- [ ] Create `docs/design_decisions.md` (Ch6-specific methodological choices)
- [ ] Create `docs/ch6_limitations.md` (consolidated MODERATE issues)

---

## APPENDIX A: KNOWN LIMITATIONS TO DOCUMENT IN THESIS

**Include in Discussion chapter:**

1. **Model Averaging Limited to ROOT RQs**
   - Derivative RQs use single-best model from ROOT
   - MA outputs available for sensitivity if needed

2. **GRM-2PL Transformation Mismatch**
   - 2PL transformation invalid for GRM (ignores category structure)
   - Probability scale for visualization only; theta scale valid

3. **Non-Independence in Some Analyses**
   - Standard logistic regression used where GLMM ideal
   - Conservative for non-significant findings

4. **Day 6 Floor Effects**
   - Confidence trajectories approach measurement floor (2-3% probability)
   - Limits interpretability at endpoint

5. **100% Item Retention Pattern**
   - Unusual vs typical IRT purification (40-60% exclusion)
   - Sensitivity analysis recommended

6. **Desktop VR Ecological Limitations**
   - Lacks vestibular/proprioceptive cues (not HMD)
   - Single cultural context; ages 20-70

7. **Transfer/Generalization Unknown**
   - VR findings may not transfer to 2D or real-world memory
   - No comparison to traditional neuropsychological tests

---

## APPENDIX B: COMPLETED MODEL AVERAGING (Reference)

**Infrastructure Created:**
- `tools/model_averaging.py` (779 lines) with:
  - `identify_competitive_models()` - ΔAIC < 7 filter
  - `compute_unconditional_variance()` - Burnham & Anderson (2002) eq 4.9
  - `compute_model_averaged_random_effects()` - For ICC derivatives
  - `run_model_averaging_pipeline()` - Complete workflow

**ROOT RQ Implementation:**

| RQ | Competitive Models | Effective N | Uncertainty | Date |
|----|-------------------|-------------|-------------|------|
| 6.8.1 | 51 (99.6% weight) | 43.4 | EXTREME | 2025-12-13 |
| 6.1.1 | 48 (97.5% weight) | 31.1 | EXTREME | 2025-12-13 |
| 6.3.1 | 4 (92.0% weight) | 2.4 | LOW | 2025-12-13 |
| 6.4.1 | 2 (100% weight) | 2.0 | LOW | 2025-12-13 |
| 6.5.1 | 2 (87.5% weight) | 1.8 | LOW | 2025-12-13 |

**6.7.3 Fix:**
- Ch5 5.1.1 MA residuals created (51 models, Eff_N=40.09)
- 6.7.3 updated: r = -0.05, p = 0.65 (vs original r = 0.02, p = 0.85)
- NULL finding ROBUST across model specifications

**Outputs per ROOT RQ:**
- `step05b_competitive_models.csv`
- `step05b_model_averaged_predictions.csv`
- `step05b_model_averaged_theta.csv`
- `step05b_model_averaged_random_effects.csv`
- `step05b_metadata.csv`

---

## APPENDIX C: SESSION COMPLETION LOG

**Use this section to track progress across sessions:**

### Session 1: [DATE]
- [ ] Completed tasks:
- [ ] Notes:
- [ ] Next session priorities:

### Session 2: [DATE]
- [ ] Completed tasks:
- [ ] Notes:
- [ ] Next session priorities:

### Session 3: [DATE]
- [ ] Completed tasks:
- [ ] Notes:
- [ ] Next session priorities:

---

## APPENDIX D: QUICK REFERENCE - FILE LOCATIONS

**Key Data Files:**
- `results/ch6/6.1.1/data/step05b_model_averaged_random_effects.csv` - MA slopes for T1.1
- `results/ch6/6.7.2/data/step03_person_summary.csv` - Data for T1.2
- `results/ch6/6.4.2/data/step03_calibration_data.csv` - Data for T1.3, T1.4

**Key Code Templates:**
- `results/ch6/6.1.1/code/step05b_model_averaging.py` - MA reference implementation
- `tools/model_averaging.py` - Reusable MA functions

**Key Documentation:**
- `docs/lmm_methodology.md` - MA procedure documentation
- `results/ch6/rq_status.tsv` - RQ tracking spreadsheet

---

## APPENDIX E: ISSUES LOG

**Purpose:** Document any issues, surprises, or decisions that arise during rework execution. User must be notified of all entries here.

### Issue Template
```
### Issue [NUMBER]: [DATE] - [BRIEF TITLE]
**Task:** T#.# - [Task name]
**Discovered:** [What was found]
**Impact:** [How it affects findings/thesis]
**Resolution:** [What was decided / PENDING USER INPUT]
**User Notified:** [YES/NO + date]
```

### Active Issues

_None yet - add issues here as they arise during rework execution_

### Resolved Issues

_None yet - move issues here after resolution_

---

## APPENDIX F: DECISION LOG

**Purpose:** Track all methodological decisions made during rework for thesis documentation.

### Decision Template
```
### D[NUMBER]: [DATE] - [BRIEF TITLE]
**Task:** T#.# - [Task name]
**Question:** [What needed to be decided]
**Options Considered:** [List options]
**Decision:** [What was chosen]
**Rationale:** [Why this choice]
**User Approved:** [YES + date]
```

### Decisions Made

_None yet - add decisions here as they are made_

---

**END OF REWORK PLAN**

**Next Action:** Begin TIER 1 tasks (T1.1 most impactful, 30 minutes)

---

## REVISION HISTORY

| Date | Changes | By |
|------|---------|-----|
| 2025-12-13 11:50 | Initial creation - Model averaging plan | Claude |
| 2025-12-13 14:30 | Added implementation status for 5 ROOT RQs | Claude |
| 2025-12-13 20:50 | Marked all MA tasks complete, added 6.7.3 fix | Claude |
| 2025-12-13 21:30 | **Major restructure:** Added validity enhancement tiers (T1-T4), user notification protocol, appendices E/F, session/issues logs | Claude |
