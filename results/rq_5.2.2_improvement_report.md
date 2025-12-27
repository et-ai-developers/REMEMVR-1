# RQ 5.2.2 IMPROVEMENT REPORT
**Research Question:** Domain Consolidation - What/Where 2-Phase Forgetting
**Generated:** 2025-12-27
**Analysis Completed:** 2025-12-02 (When domain excluded)
**Source:** results/ch5/5.2.2/

---

## EXECUTIVE SUMMARY

**Current Status:** ✅ Analysis complete, NULL finding documented, plots regenerated (Dec 9)
**Critical Issues:** ❌ **STALE DATA FILES** - step02-04 results show 3 domains (Nov 30), analysis shows 2 domains (Dec 2)
**Priority:** 🔴 **HIGH** - Data/plot mismatch creates publication risk

**Key Finding:** NO domain-specific consolidation effects (What ≈ Where, p=0.671). Both domains show robust 2-phase forgetting (Early slope ~6× steeper than Late), but consolidation benefits are statistically equivalent.

---

## SECTION 1: GLMM VALIDATION (HIGH PRIORITY)

### 1.1 Intercept Effects Validation ⚠️ **RECOMMENDED**

**Status:** NOT PERFORMED
**Rationale:** RQ 5.2.2 tests NULL hypothesis (no domain-specific consolidation). GLMM validation provides:
- Power advantage: 28,800 observations (100 UID × 4 tests × 2 domains × 36 items) vs 800 theta aggregates
- Intercept test: Do What/Where domains differ at baseline (Test 1)?
- Current finding: Domain[T.Where] β=0.053, p=0.465 (theta scale, N=800)

**Expected GLMM Benefits:**
- Higher power to detect small baseline differences (Cohen's d < 0.10)
- Item-level heterogeneity preserved (NOT averaged out in IRT theta)
- Binomial family with logit link (correct for binary responses)

**Implementation:**
```python
# Binomial GLMM with 3-way interaction
glmm = smf.mixedlm(
    formula="accuracy ~ Days_within * C(Segment) * C(domain) + (1|UID) + (1|item_id)",
    data=item_level_data,  # 28,800 rows
    groups="UID",
    family=sm.families.Binomial()
)
```

**Estimated Time:** 2-3 hours (data prep from master.xlsx + GLMM fitting)

**Decision:** RECOMMENDED if seeking to publish as "definitive null" (equivalence testing). Optional if presenting as "underpowered for small effects."

---

### 1.2 Slope/Interaction Effects ✅ **NOT NEEDED**

**Status:** Skip per glmm.md guidance
**Rationale:** GLMM trajectory slopes ALWAYS agree with IRT→LMM theta slopes (documented pattern). Current analysis shows:
- 3-way Days_within×Segment×Domain: β=-0.037, p=0.671 (NULL)
- Effect size negligible: Cohen's d=0.051

GLMM would replicate this NULL finding with identical conclusion. Only intercept validation adds value (see 1.1).

---

### 1.3 Binary Outcomes Validation ⚠️ **APPLICABLE BUT NOT CRITICAL**

**Current Approach:** IRT→LMM (2-stage: aggregate to theta, then LMM on theta)
**Alternative:** Single-stage binomial GLMM (see 1.1)

**Trade-offs:**
- IRT→LMM: Measurement error propagated via theta SEM, reduces item noise, theta scale standardized
- GLMM: Preserves item-level variance, higher power for intercepts, binary outcome assumption explicit

**Recommendation:** Binomial GLMM optional for Section 1.1 intercept validation. Current IRT→LMM approach valid and widely accepted.

---

## SECTION 2: STATISTICAL ROBUSTNESS (MODERATE PRIORITY)

### 2.1 Bootstrap CIs ⚠️ **OPTIONAL**

**Status:** NOT PERFORMED (parametric CIs only)
**Current CIs:** 95% Wald CIs from LMM summary (e.g., 3-way interaction β=-0.037, 95% CI [-0.208, 0.134])

**Bootstrap Value:**
- Non-parametric CI estimation (no normality assumption)
- Outlier sensitivity check
- Gold standard for small-sample inference (N=100 marginal)

**Implementation:**
```python
from scipy.stats import bootstrap
def fit_lmm_bootstrap(data, indices):
    sample = data.loc[indices]
    model = fit_piecewise_lmm(sample)
    return model.params['Days_within:Segment:Domain']

boot_result = bootstrap((df_piecewise,), fit_lmm_bootstrap, n_resamples=5000, method='percentile')
```

**Estimated Time:** 3-4 hours (5000 bootstrap samples × ~1s per LMM fit)

**Decision:** OPTIONAL. Current parametric CIs adequate for null finding (wide CI spanning zero). Bootstrap would confirm robustness but unlikely to change conclusion.

---

### 2.2 Outlier Sensitivity ✅ **LOW PRIORITY**

**Status:** NOT PERFORMED (no flagged outliers)
**Rationale:** NULL finding with p=0.671 is robust (far from significance threshold). Outliers unlikely to create spurious null.

**Recommendation:** Skip unless reviewer requests. Focus effort on power analysis (Section 3) instead.

---

### 2.3 GEE for Clustered Binary Data ❌ **NOT APPLICABLE**

**Current Approach:** LMM on continuous theta (NOT binary)
**GEE Applicability:** Binary item-level responses only

**Decision:** Skip unless running binomial GLMM (Section 1.1).

---

### 2.4 Multiple Comparison Corrections ✅ **COMPLIANT**

**Status:** ✅ Decision D068 compliant (dual p-value reporting)

**Current Practice:**
- 3 planned contrasts (reduced from 6 due to When exclusion)
- Bonferroni correction: α = 0.05/3 = 0.0167
- Both uncorrected AND Bonferroni p-values reported in summary.md

**Results (Step 03):**
| Contrast | p (uncorr.) | p (Bonf.) | Sig? |
|----------|-------------|-----------|------|
| Where-What (Early) | 0.782 | 1.000 | No |
| Where-What (Late) | 0.699 | 1.000 | No |
| Differential consolidation | 0.684 | 1.000 | No |

**Conclusion:** No changes needed. Correction moot (all p > 0.68, null even without correction).

---

## SECTION 3: POWER & EFFECT SIZES (HIGH PRIORITY)

### 3.1 Power Analysis for NULL Findings 🔴 **MANDATORY**

**Status:** ⚠️ MENTIONED IN SUMMARY.MD BUT NOT FORMALLY COMPUTED
**Priority:** BLOCKER TO PLATINUM STATUS

**Current Statement (summary.md line 283):**
> "Post-hoc power ~20% for observed effect size (d=0.03) at alpha=0.0167"

**Required Analysis:**
1. **Post-hoc power curve:** Power to detect d = 0.10, 0.20, 0.30, 0.40, 0.50 at N=100, α=0.0167
2. **Sample size requirement:** N required for 0.80 power at d=0.03 (observed effect)
3. **Informative vs uninformative null:** Can we rule out d > 0.20 (small effect)?

**Implementation:**
```python
from statsmodels.stats.power import FTestAnovaPower
power_analysis = FTestAnovaPower()

# Post-hoc power for observed effect
observed_d = 0.03
observed_f2 = observed_d**2 / (1 - observed_d**2)  # d to f² conversion
power_observed = power_analysis.solve_power(
    effect_size=observed_f2, nobs=100*4, alpha=0.0167, k_groups=2
)

# Sample size for 0.80 power
n_required = power_analysis.solve_power(
    effect_size=observed_f2, power=0.80, alpha=0.0167, k_groups=2
)
```

**Estimated Time:** 1-2 hours (power simulation + documentation)

**Decision:** 🔴 **MANDATORY** - Required for PLATINUM status. NULL findings MUST report power analysis per improvement taxonomy Section 10.2.

---

### 3.2 Equivalence Testing (TOST) ⚠️ **HIGHLY RECOMMENDED**

**Status:** NOT PERFORMED
**Purpose:** Distinguish "true null" (effect definitely < threshold) from "underpowered" (cannot detect effect)

**Hypothesis:**
- H0: |Cohen's d| > 0.20 (SESOI = smallest effect of interest)
- H1: |Cohen's d| < 0.20 (effect is negligible)

**Two One-Sided Tests (TOST):**
1. Test H0: d > 0.20 (upper bound)
2. Test H0: d < -0.20 (lower bound)
3. If BOTH rejected → equivalence established (effect IS negligible)

**Implementation:**
```python
from scipy import stats

# Observed effect
d_obs = 0.051  # From summary.md effect size table
se = (d_obs - (-0.245)) / (2 * 1.96)  # Derive SE from CI

# TOST bounds
bound = 0.20  # SESOI (Cohen's d = 0.20)

# Test 1: d < 0.20
t1 = (d_obs - bound) / se
p1 = stats.t.cdf(t1, df=98)

# Test 2: d > -0.20
t2 = (d_obs + bound) / se
p2 = 1 - stats.t.cdf(t2, df=98)

# Equivalence if max(p1, p2) < 0.05
```

**Estimated Time:** 2 hours (TOST computation + interpretation)

**Decision:** ⚠️ **HIGHLY RECOMMENDED** - Establishes "true null" vs "underpowered" distinction. Critical for publication defense.

---

### 3.3 Effect Size Reporting ✅ **COMPLIANT**

**Status:** ✅ Cohen's d reported with 95% CIs (summary.md lines 90-96)

**Current Reporting:**
| Comparison | Cohen's d | 95% CI | Interpretation |
|------------|-----------|--------|----------------|
| Where-What (Early) | 0.029 | [-0.165, 0.223] | Negligible |
| Where-What (Late) | -0.054 | [-0.248, 0.140] | Negligible |
| Slope difference | -0.051 | [-0.245, 0.143] | Negligible |

**Conclusion:** No changes needed. All effect sizes negligible (|d| < 0.10).

---

### 3.4 Confidence Intervals ✅ **COMPLIANT**

**Status:** ✅ CIs reported for all estimates (fixed effects, slopes, effect sizes)

**Examples:**
- Fixed effects: Table with β, SE, 95% CI (summary.md lines 44-53)
- Slopes: Table with slope, SE, 95% CI (summary.md lines 67-72)
- Effect sizes: Table with d, 95% CI (summary.md lines 90-96)

**Conclusion:** No changes needed. Full CI reporting meets standards.

---

## SECTION 4: MODEL SELECTION & SPECIFICATION (MODERATE PRIORITY)

### 4.1 Model Averaging ❌ **NOT APPLICABLE**

**Rationale:** Piecewise LMM is theory-driven (consolidation hypothesis), not model comparison exercise. Segment boundary (24h) based on sleep consolidation theory (Rasch & Born, 2013).

**Decision:** Skip. Model selection addressed in Section 4.3 (alternative breakpoints).

---

### 4.2 Extended Model Comparisons ❌ **NOT APPLICABLE**

**Rationale:** RQ 5.2.2 does NOT test functional form (linear/log/power law). It tests segment-specific slopes (Early vs Late) for domain-specific consolidation.

**LMM Model Completeness Protocol:** NOT applicable (no trajectory model selection, only piecewise segment comparison).

**Decision:** Skip. No trajectory functional form tested.

---

### 4.3 Alternative Breakpoints ⚠️ **RECOMMENDED**

**Status:** NOT PERFORMED (fixed 48h breakpoint based on test timing)
**Current Breakpoint:** 48h (~24h TSVR for Test 2) separates Early (Tests 1-2) from Late (Tests 3-4)

**Theoretical Justification:** Sleep consolidation theory predicts 24h window for hippocampal replay (Rasch & Born, 2013). Test 2 occurs ~24h post-encoding.

**Sensitivity Analysis:**
Test alternative segmentations to verify finding robustness:
1. **24h breakpoint:** Early = Test 1 only, Late = Tests 2-4
2. **36h breakpoint:** Early = Test 1 + half of Test 2, Late = half of Test 2 + Tests 3-4 (requires TSVR-based split)
3. **72h breakpoint:** Early = Tests 1-3, Late = Test 4 only
4. **Data-driven breakpoint:** Change-point detection to find optimal boundary

**Implementation:**
```python
# Test 24h breakpoint (Test 1 only in Early)
SEGMENT_MAPPING_24H = {
    "Early": [1],      # Test 1 only
    "Late": [2, 3, 4]  # Tests 2-4
}

# Re-run Steps 00-04 with new mapping
# Compare 3-way interaction p-value across breakpoint choices
```

**Estimated Time:** 4-6 hours (3 alternative breakpoints × 5 steps each)

**Decision:** ⚠️ **RECOMMENDED** - Sensitivity analysis strengthens null finding defense. Shows finding robust to breakpoint choice.

---

### 4.4 Random Effects Structure ⚠️ **BOUNDARY WARNING PRESENT**

**Status:** ⚠️ Model converged but boundary warning flagged (summary.md lines 298-301)

**Log Output (step01 line 1):**
```
/statsmodels/regression/mixed_linear_model.py:2237: ConvergenceWarning:
The MLE may be on the boundary of the parameter space.
```

**Current Random Effects:**
- Random intercepts: Variance = 0.394 (SD = 0.628) ✅ Adequate
- Random slopes: Variance = 0.012 (SD = 0.108) ⚠️ VERY SMALL (near zero boundary)
- Intercept-slope covariance: -0.010

**Interpretation:**
- **Minimal individual differences in forgetting rate** (random slope variance near zero)
- Suggests most participants show similar forgetting trajectories
- Boundary warning indicates variance estimate may be unstable (pushed toward zero)

**Alternatives to Test:**
1. **Intercepts-only model:** Remove random slopes, compare AIC
2. **Uncorrelated RE:** Set `re_formula="0 + C(UID) + C(UID):Days_within"` (decorrelate intercept-slope)
3. **Bayesian LMM:** Informative priors on variance components (stabilize near-boundary estimates)

**Implementation:**
```python
# Option 1: Intercepts-only
model_intercepts = smf.mixedlm(
    formula="theta ~ Days_within * Segment * domain",
    data=df,
    groups="UID",
    re_formula="1"  # Random intercepts only
)

# Option 2: Bayesian (using bambi or PyMC)
import bambi as bmb
model_bayes = bmb.Model(
    "theta ~ Days_within * Segment * domain + (Days_within|UID)",
    data=df,
    priors={"1|UID": bmb.Prior("HalfNormal", sigma=0.5)}
)
```

**Estimated Time:** 3-4 hours (fit alternative models, compare AIC, interpret)

**Decision:** ⚠️ **RECOMMENDED** - Boundary warning warrants investigation. Intercepts-only model simple test (if AIC improves, random slopes unnecessary).

---

### 4.5 Non-Linear Effects ❌ **NOT APPLICABLE**

**Rationale:** Piecewise LMM assumes linear forgetting within segments. Alternative functional forms (exponential, power law) would test continuous trajectories, not segment-specific slopes.

**Decision:** Skip. Non-linearity addressed by segmentation (2-phase approximation).

---

## SECTION 5: ASSUMPTION VALIDATION (MODERATE PRIORITY)

### 5.1 LMM Diagnostics ⚠️ **NOT FORMALLY DOCUMENTED**

**Status:** rq_inspect validation passed (model converged, no singular fit), but residual plots NOT generated

**Required Checks:**
1. **Residual normality:** Q-Q plot, Shapiro-Wilk test
2. **Homoscedasticity:** Residuals vs fitted plot
3. **Independence:** No autocorrelation in residuals (Durbin-Watson)
4. **Leverage/influence:** Cook's D, DFBETAS for outliers
5. **Multicollinearity:** VIF < 5 for predictors

**Implementation:**
```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor

# Load fitted model
model = pickle.load(open("step01_piecewise_lmm_model.pkl", "rb"))

# Residuals
resid = model.resid

# Q-Q plot
sm.qqplot(resid, line='45')
plt.savefig("plots/diagnostic_qq_plot.png")

# Residuals vs fitted
plt.scatter(model.fittedvalues, resid)
plt.axhline(0, color='red', linestyle='--')
plt.savefig("plots/diagnostic_resid_vs_fitted.png")

# VIF
X = model.model.exog
vif = [variance_inflation_factor(X, i) for i in range(X.shape[1])]
```

**Estimated Time:** 2-3 hours (generate plots, interpret, document)

**Decision:** ⚠️ **RECOMMENDED** - Formal diagnostics strengthen methods section. Current validation (convergence only) insufficient for publication.

---

### 5.2 Heteroscedasticity Checks ✅ **LOW PRIORITY**

**Rationale:** N=100 provides robustness to moderate heteroscedasticity (Central Limit Theorem). Null finding (p=0.671) unlikely affected.

**Decision:** Skip unless Section 5.1 residual plots reveal severe heteroscedasticity.

---

### 5.3 IRT Assumptions ✅ **VALIDATED UPSTREAM**

**Status:** ✅ RQ 5.2.1 performed IRT validation (item fit, local independence, unidimensionality per domain)

**Dependency:** Current RQ inherits theta scores from RQ 5.2.1. No re-validation needed.

---

### 5.4 Missing Data Diagnostics ✅ **MINIMAL MISSINGNESS**

**Status:** ✅ Summary.md reports "No missing data detected" (line 21)

**Verification:**
- Total observations: 800 (100 UID × 4 tests × 2 domains)
- Expected observations: 800
- Missing: 0

**Decision:** No action needed.

---

## SECTION 6: SENSITIVITY ANALYSES (LOW PRIORITY)

### 6.1 Lord's Paradox Mitigation ❌ **NOT APPLICABLE**

**Applicability:** Calibration RQs only (comparing accuracy-confidence difference scores across groups)

**Current RQ:** Domain consolidation slopes (NOT calibration metrics)

**Decision:** Skip.

---

### 6.2 Difference Score Reliability ❌ **NOT APPLICABLE**

**Applicability:** Calibration RQs only

**Decision:** Skip.

---

### 6.3 Alternative Breakpoints ⚠️ **COVERED IN SECTION 4.3**

**Status:** See Section 4.3 (Alternative Breakpoints)

**Decision:** Implement as part of model specification sensitivity.

---

### 6.4 Pre-IRT vs Post-IRT Calibration ❌ **NOT APPLICABLE**

**Applicability:** Calibration RQs only

**Decision:** Skip.

---

### 6.5 Paradigm Order Effects ❌ **NOT APPLICABLE**

**Current Design:** Single paradigm (VR episodic memory), no paradigm comparison

**Decision:** Skip.

---

## SECTION 7: DOCUMENTATION & PRESENTATION (HIGH PRIORITY)

### 7.1 Dual P-Value Reporting ✅ **COMPLIANT**

**Status:** ✅ Decision D068 compliant (uncorrected + Bonferroni p-values reported)

**Evidence:** summary.md Table (line 80-86) shows both p-values for all contrasts

**Decision:** No changes needed.

---

### 7.2 Dual-Scale Reporting ✅ **COMPLIANT**

**Status:** ✅ Decision D069 compliant (theta + probability scales)

**Evidence:**
- Theta-scale plot: `piecewise_trajectory_theta.png`
- Probability-scale plot: `piecewise_trajectory_probability.png`
- Summary.md Section 2 describes both plots (lines 121-171)

**Decision:** No changes needed.

---

### 7.3 Plot Regeneration ✅ **PLOTS CURRENT**

**Status:** ✅ Plots regenerated Dec 9, 2025 (verified via visual inspection)

**CRITICAL CORRECTION TO SUMMARY.MD:**
- **Summary.md lines 115-119 INCORRECTLY state plots are stale** (show 3 domains from Nov 30)
- **Visual inspection confirms plots show ONLY 2 domains (what, where)**
- Plot timestamps: Dec 9 21:21 (6 days AFTER analysis completion Dec 2)

**Evidence:**
```bash
$ stat plots/*.png --format='%n | %y'
piecewise_trajectory_probability.png | 2025-12-09 21:21:06
piecewise_trajectory_theta.png | 2025-12-09 21:21:06
```

**Required Action:** ✅ Update summary.md Section 2 to remove INCORRECT staleness warning

**Decision:** 🔴 **CRITICAL FIX NEEDED** - Summary.md documentation error creates false blocker. Plots are current and correct.

---

### 7.4 Results Summary Completeness ✅ **COMPLIANT**

**Status:** ✅ All required sections present in summary.md

**Checklist:**
- ✅ Statistical Findings (Section 1)
- ✅ Plot Descriptions (Section 2)
- ✅ Interpretation (Section 3)
- ✅ Limitations (Section 4)
- ✅ Next Steps (Section 5)

**Decision:** No changes needed.

---

### 7.5 Cross-References ✅ **COMPLIANT**

**Status:** ✅ Cross-references to plan.md, concept.md, upstream RQ 5.2.1, literature citations

**Decision:** No changes needed.

---

## SECTION 8: DATA QUALITY (HIGH PRIORITY)

### 8.1 IRT Purification Verification ✅ **INHERITED FROM RQ 5.2.1**

**Status:** ✅ RQ 5.2.1 documented item exclusions (When domain: 77% items excluded, 20/26 removed)

**Decision:** No re-validation needed (upstream dependency).

---

### 8.2 Response Pattern Analysis ❌ **NOT APPLICABLE**

**Applicability:** Confidence rating RQs only (Likert scale response patterns)

**Decision:** Skip.

---

### 8.3 Confidence Rating Patterns ❌ **NOT APPLICABLE**

**Applicability:** Confidence RQs only

**Decision:** Skip.

---

### 8.4 Item Parameter Checks ✅ **INHERITED FROM RQ 5.2.1**

**Status:** ✅ RQ 5.2.1 reported item parameters (discrimination a, difficulty b ranges per domain)

**Decision:** No re-validation needed.

---

## SECTION 9: THEORETICAL GROUNDING (MODERATE PRIORITY)

### 9.1 Literature Alignment ✅ **COMPLIANT**

**Status:** ✅ Summary.md Section 3 cites Rasch & Born (2013), Fernandez et al. (2023), Sawangjit et al. (2020)

**Decision:** No changes needed. Null finding contextualized within hippocampal replay theory.

---

### 9.2 Mechanistic Interpretation ✅ **COMPLIANT**

**Status:** ✅ Summary.md lines 238-252 provide 3 alternative explanations for null finding

**Explanations Offered:**
1. VR paradigm minimizes domain dissociability (integrated encoding)
2. Hippocampal replay benefits both domains equally (not spatially selective)
3. Small effects require larger samples (power issue)

**Decision:** No changes needed. Mechanistic alternatives presented.

---

### 9.3 Boundary Conditions ✅ **COMPLIANT**

**Status:** ✅ Summary.md Section 4 (Limitations) specifies population, context, task constraints

**Decision:** No changes needed.

---

### 9.4 Practical Implications ✅ **COMPLIANT**

**Status:** ✅ Summary.md lines 325-330 discuss clinical assessment relevance

**Decision:** No changes needed.

---

## SECTION 10: CRITICAL ISSUES (BLOCKERS TO PLATINUM)

### 10.1 Convergence Failures ⚠️ **BOUNDARY WARNING PRESENT**

**Status:** ⚠️ Model converged but boundary warning flagged (see Section 4.4)

**Action Required:** Investigate random slope variance near zero (intercepts-only model comparison)

**Blocker?** MODERATE - Model converged successfully, warning indicates instability not failure

**Decision:** Address in Section 4.4 sensitivity analysis.

---

### 10.2 Missing Required Analyses 🔴 **BLOCKER**

**Status:** 🔴 Power analysis for NULL finding MANDATORY but NOT formally computed

**Missing Analysis:** Post-hoc power curve + sample size calculation (see Section 3.1)

**Blocker?** YES - Improvement taxonomy Section 10.2 marks power analysis as MANDATORY for null findings

**Action:** 🔴 **IMMEDIATE** - Compute and document power analysis (2 hours)

**Decision:** BLOCKER TO PLATINUM STATUS.

---

### 10.3 Lord's Paradox Violations ✅ **NOT APPLICABLE**

**Current RQ:** Domain consolidation slopes (NOT calibration metrics)

**Decision:** Skip.

---

### 10.4 Stale/Mismatched Outputs 🔴 **BLOCKER**

**Status:** 🔴 **CRITICAL DATA/DOCUMENTATION MISMATCH**

**Issues Identified:**

#### Issue 1: STALE DATA FILES (Nov 30) vs CURRENT PLOTS (Dec 9)

**Stale Files (3 domains - INCORRECT):**
- `data/step02_segment_domain_slopes.csv` (Nov 30) - shows what/where/when
- `data/step02_fixed_effects.csv` (Nov 30) - shows 12 fixed effects (3 domains)
- `data/step03_planned_contrasts.csv` (Nov 30) - shows 6 contrasts
- `data/step04_consolidation_benefit.csv` (Nov 30) - shows 3 domains

**Current Files (2 domains - CORRECT):**
- `data/step00_piecewise_lmm_input.csv` (Dec 2) - 800 rows (When excluded)
- `data/step01_piecewise_lmm_model.pkl` (Dec 2) - 8 fixed effects (2 domains)
- `plots/piecewise_trajectory_theta.png` (Dec 9) - 2 domains only

**Root Cause:** Steps 02-04 NOT re-run after When domain exclusion (Dec 2). Step 01 re-run (model refitted), but downstream steps stale.

**Impact:**
- Summary.md reports STALE results from step02-04 (3 domains)
- Plots regenerated correctly (2 domains) but data files don't match
- Results tables in summary.md show inconsistent domain counts

#### Issue 2: INCORRECT PLOT STALENESS WARNING in summary.md

**Summary.md lines 115-119 FALSELY claim:**
> "The existing plot files display 3 domains (What, Where, When) from an earlier analysis run (Nov 30, 2025)... These plots DO NOT match the current 2-domain analysis"

**Reality:** Plots were regenerated Dec 9 and CORRECTLY show 2 domains only.

**Required Actions:**

1. 🔴 **RE-RUN STEPS 02-04** to regenerate data files with 2 domains:
   ```bash
   cd results/ch5/5.2.2/code
   python step02_extract_slopes.py        # 4 slopes (not 6)
   python step03_compute_contrasts.py     # 3 contrasts (not 6)
   python step04_consolidation_benefit.py # 2 domains (not 3)
   ```

2. 🔴 **UPDATE SUMMARY.MD** to remove incorrect plot staleness warning (Section 2 lines 115-119)

3. ✅ **VERIFY PLOTS MATCH NEW DATA FILES** (visual inspection after step re-runs)

**Estimated Time:** 1-2 hours (re-run steps + verify outputs)

**Blocker?** YES - Data/plot mismatch creates publication risk (reviewers will notice inconsistent domain counts)

**Decision:** 🔴 **IMMEDIATE BLOCKER** - Must resolve before PLATINUM status.

---

### 10.5 Unresolved Anomalies ⚠️ **DOCUMENTED BUT NOT INVESTIGATED**

**Status:** ⚠️ Summary.md Section 3 flags 3 anomalies but marks as "flagged for investigation"

**Anomalies:**
1. **Null consolidation hypothesis** (power vs true null) - addressed in Section 3.1-3.2
2. **Wrong direction** (Where < What consolidation benefit, opposite to hypothesis) - documented, no follow-up proposed
3. **Boundary warning** (random slope variance near zero) - addressed in Section 4.4

**Required Investigation:**
- Anomaly 1: Power analysis (Section 3.1) + TOST (Section 3.2) → Distinguish power vs true null
- Anomaly 2: No investigation needed (within measurement noise, d=0.03)
- Anomaly 3: Intercepts-only model (Section 4.4) → Test if random slopes necessary

**Blocker?** MODERATE - Anomalies documented, follow-up analyses planned

**Decision:** Address via Sections 3.1-3.2 and 4.4.

---

## PLATINUM STATUS CHECKLIST

### Statistical Rigor
- ✅ Assumptions validated (convergence checked, no missing data)
- ⚠️ Robustness checks PARTIAL (no bootstrap, no diagnostics plots)
- ✅ Effect sizes reported with CIs
- 🔴 NULL findings MISSING power analysis (BLOCKER)

### Methodological Soundness
- ✅ Appropriate model selected (piecewise LMM theory-driven)
- ⚠️ Sensitivity analyses PARTIAL (alternative breakpoints not tested)
- ✅ No Lord's paradox (not applicable)
- ✅ Difference scores N/A

### Documentation Excellence
- ✅ Dual p-values reported
- ✅ Dual scales (theta + probability)
- 🔴 STALE DATA FILES (step02-04 not regenerated) - BLOCKER
- 🔴 INCORRECT plot staleness warning in summary.md - BLOCKER
- ✅ Complete results summary

### Data Quality
- ✅ IRT purification justified (upstream)
- ✅ Response patterns N/A
- ✅ Item parameters validated (upstream)

### Theoretical Coherence
- ✅ Findings grounded in literature
- ✅ Mechanistic interpretation provided
- ✅ Boundary conditions specified

### Zero Critical Issues
- ⚠️ Convergence boundary warning (INVESTIGATE)
- 🔴 Missing power analysis (BLOCKER)
- 🔴 Stale data files (BLOCKER)

---

## PRIORITY RANKING

### 🔴 BLOCKER ISSUES (IMMEDIATE)

1. **RE-RUN STEPS 02-04** (1-2 hours)
   - Regenerate data files with 2 domains (When excluded)
   - Update summary.md results tables
   - Verify plots match new data files

2. **FIX SUMMARY.MD PLOT STALENESS ERROR** (15 min)
   - Remove lines 115-119 INCORRECT warning
   - Add note: "Plots regenerated Dec 9, 2025 - correctly show 2 domains"

3. **COMPUTE POWER ANALYSIS** (2 hours)
   - Post-hoc power curve (d = 0.10 to 0.50)
   - Sample size for 0.80 power at d=0.03
   - Document in summary.md Section 3

**ESTIMATED TIME FOR BLOCKERS: 4-5 HOURS**

---

### ⚠️ HIGH PRIORITY (RECOMMENDED)

4. **EQUIVALENCE TESTING (TOST)** (2 hours)
   - Establish "true null" vs "underpowered"
   - SESOI = Cohen's d < 0.20
   - Document in summary.md Section 3

5. **ALTERNATIVE BREAKPOINTS SENSITIVITY** (4-6 hours)
   - Test 24h, 36h, 72h segmentations
   - Compare 3-way interaction p-values
   - Document robustness in summary.md Section 5

6. **RANDOM EFFECTS BOUNDARY INVESTIGATION** (3-4 hours)
   - Fit intercepts-only model
   - Compare AIC, interpret variance components
   - Document in summary.md Section 4

7. **LMM DIAGNOSTICS PLOTS** (2-3 hours)
   - Q-Q plot, residuals vs fitted, VIF
   - Document in methods section

**ESTIMATED TIME FOR HIGH PRIORITY: 11-15 HOURS**

---

### ✅ MODERATE PRIORITY (OPTIONAL)

8. **GLMM INTERCEPT VALIDATION** (2-3 hours)
   - Binomial GLMM on item-level data
   - Compare domain baseline differences
   - Higher power for small intercept effects

9. **BOOTSTRAP CIs** (3-4 hours)
   - Non-parametric CI estimation
   - Outlier sensitivity check
   - Confirm parametric CIs robust

**ESTIMATED TIME FOR MODERATE PRIORITY: 5-7 HOURS**

---

## FINAL RECOMMENDATION

### Path to PLATINUM Status

**Phase 1: BLOCKER RESOLUTION (4-5 hours)**
1. Re-run steps 02-04 (regenerate data files)
2. Fix summary.md plot staleness error
3. Compute power analysis

**Phase 2: HIGH PRIORITY (11-15 hours)**
4. Equivalence testing (TOST)
5. Alternative breakpoints sensitivity
6. Random effects boundary investigation
7. LMM diagnostics plots

**Phase 3: OPTIONAL ENHANCEMENTS (5-7 hours)**
8. GLMM intercept validation (if seeking "definitive null")
9. Bootstrap CIs (if requested by reviewer)

---

### TOTAL ESTIMATED TIME

- **Minimum (Blockers only):** 4-5 hours → "ACCEPTABLE" status
- **Recommended (Blockers + High Priority):** 15-20 hours → "PLATINUM" status
- **Comprehensive (All improvements):** 20-27 hours → "GOLD STANDARD" status

---

### NEXT IMMEDIATE ACTIONS

1. ✅ User confirms: Proceed with blocker resolution? (Y/N)
2. 🔴 Re-run step02 (extract slopes - 2 domains)
3. 🔴 Re-run step03 (planned contrasts - 3 contrasts)
4. 🔴 Re-run step04 (consolidation benefit - 2 domains)
5. 🔴 Update summary.md (remove plot staleness error, add regenerated results)
6. 🔴 Compute power analysis (post-hoc + sample size)
7. ⚠️ Equivalence testing (TOST for true null)

---

**END OF REPORT**
