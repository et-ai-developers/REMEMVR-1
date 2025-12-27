# Chapter 5 & 6 Finalization Roadmap - Path to PLATINUM Status

**Document Purpose:** Comprehensive improvement plan for all Ch5/Ch6 RQs
**Goal:** Zero flaws, maximum defensibility, thesis-ready
**Date Created:** 2025-12-27
**Based On:** improvement_taxonomy.md + context-finder analysis of 10 priority RQs + glmm_candidates.md

---

## EXECUTIVE SUMMARY

### Current Landscape

**Total RQs:** 66 (35 Ch5 + 31 Ch6)
**Analyzed in Detail:** 10 high-impact RQs
**GLMM Validated:** 4 RQs (5.1.3, 5.4.1, 6.1.1, 6.1.3)
**Critical Discoveries:** 2 major findings changed with GLMM validation

### 🚨 CRITICAL DISCOVERIES

**1. Schema "Quadruple NULL" is FALSE (RQ 5.4.1)**
- **Original claim:** Schema has NO effect on accuracy (IRT→LMM p=.548)
- **GLMM finding:** Congruent items have HIGHER baseline accuracy (p=.011)
- **Impact:** "Quadruple null" → "Triple null + baseline effect"
- **Action required:** BLOCKER - Must integrate before defense

**2. Age Effects on Baseline SIGNIFICANT (RQs 5.1.3, 6.1.3)**
- **Original claim:** Age has NO effect on baseline memory (p=.061 marginal)
- **GLMM finding:** Age DOES affect baseline accuracy (p=.014) and confidence (p=.041)
- **Preserved finding:** Age × Time slopes remain NULL (age-invariant forgetting)
- **Reinterpretation:** Age affects ENCODING (baseline) NOT FORGETTING (trajectory)

### Estimated Total Work

**BLOCKERS (Must Fix):** 25-35 hours
**HIGH PRIORITY (Recommended):** 40-60 hours
**MEDIUM PRIORITY (Polish):** 60-80 hours
**TOTAL TO PLATINUM:** 125-175 hours (15-22 working days)

### Phased Approach

**PHASE 1 (Week 1):** BLOCKERS - 5 critical RQs (25-35 hours)
**PHASE 2 (Week 2):** HIGH PRIORITY - 15 key RQs (40-60 hours)
**PHASE 3 (Week 3):** MEDIUM PRIORITY - Remaining 46 RQs (60-80 hours)

---

## TIER 1: BLOCKER RQs (CRITICAL - Must Complete Before Defense)

### 5.4.1 - Schema Congruence Effect on Accuracy ⚠️ CRITICAL

**Status:** GLMM validation CHANGES finding (NULL → SIGNIFICANT)

**Critical Issue:**
- GLMM shows congruent intercept p=.011 (SIGNIFICANT) vs IRT→LMM p=.548 (NULL)
- "Schema quadruple null" narrative OBSOLETE
- Summary documents NOT updated with GLMM finding
- Archive entry `ch6_schema_quadruple_null_pattern.md` contains FALSE information

**Required Actions (TIER 1 - URGENT):**

1. **Integrate GLMM into summary.md** (1-2 hours)
   - Add GLMM validation subsection to Section 1 (Statistical Findings)
   - Update interpretation: Schema affects BASELINE not TRAJECTORY
   - Revise "Hypothesis NOT SUPPORTED" to "PARTIALLY SUPPORTED (baseline only)"
   - Cross-reference glmm.md for methodology

2. **Update archive entry** (30 min)
   - Create `ch6_schema_triple_null_baseline_effect.md`
   - Document NULL → SIGNIFICANT change
   - Flag old "quadruple null" entry as superseded

3. **Search thesis for "quadruple null" references** (2-3 hours)
   - Update all chapters mentioning schema quadruple null
   - Revise to "triple null + baseline effect"
   - Update theoretical interpretation sections

4. **Regenerate plots with GLMM annotations** (1 hour)
   - Add note: "GLMM validation shows baseline difference (p=.011)"
   - Update plot legends to distinguish IRT→LMM vs GLMM

**Timeline:** 5-6.5 hours
**Priority:** 🔴 BLOCKER
**Dependencies:** Must complete before RQ 6.5.1, 6.5.2, 6.5.3 (schema series)

---

### 5.1.3 - Age Effects on Accuracy Trajectory ⚠️ NARRATIVE IMPACT

**Status:** GLMM validation STRENGTHENS finding (marginal → significant)

**Critical Issue:**
- Age intercept: IRT→LMM p=.061 (marginal) → GLMM p=.014 (SIGNIFICANT)
- Age × Time slope: NULL robust (p=.46 GLMM, p=.83 IRT→LMM)
- Current summaries claim "age has NO effect on baseline" (FALSE per GLMM)
- Thesis narrative needs revision: "age-invariant" → "age affects baseline, not forgetting"

**Required Actions (TIER 1):**

1. **Update summary.md with GLMM findings** (2 hours)
   - Add GLMM validation table to Section 1
   - Change interpretation from "NOT SUPPORTED" to "SUPPORTED (baseline only)"
   - Revise theoretical sections (age affects encoding, not consolidation)

2. **Update summary_extended.md** (30 min)
   - Add GLMM comparison row
   - Note: Single-model p=.061 vs GLMM item-level p=.014

3. **Revise validation.md thesis alignment** (1 hour)
   - Remove "null findings align with thesis narrative"
   - Add "age affects encoding (baseline p=.014) not forgetting (slope p=.46)"
   - Reframe: encoding-specific deficit hypothesis

4. **Regenerate plot with GLMM p-value** (30 min)
   - Change "Age baseline: p=0.061 (marginal)" to "p=.014 (GLMM, sig)"

**Timeline:** 4 hours
**Priority:** 🔴 BLOCKER
**Dependencies:** Must complete before 6.1.3 (parallel finding for confidence)

---

### 6.4.2 - Paradigm Calibration ⚠️ LORD'S PARADOX

**Status:** BLOCKERS documented but NOT resolved

**Critical Issue:**
- Difference score reliability NOT computed (MANDATORY per taxonomy 6.2)
- Lord's Paradox mitigation planned but NOT executed
- Confidence response patterns NOT documented (Section 1.4 requirement)
- Paradox: LRT significant (p=.040) but NO pairwise contrast significant

**Required Actions (TIER 1):**

1. **Difference score reliability** (30-45 min) - **MANDATORY**
   - Compute r(theta_accuracy, theta_confidence)
   - Apply formula: r_diff = (r_xx + r_yy - 2*r_xy) / (2 - 2*r_xy)
   - Report r_diff by paradigm
   - If r_diff < 0.70 → STOP, implement latent variable approach

2. **Lord's Paradox ANCOVA** (20-25 min)
   - Fit: `Confidence ~ Paradigm + Accuracy + Paradigm×Accuracy`
   - Test if paradigm effect survives controlling for baseline
   - Compare to primary analysis (difference score)

3. **Confidence response patterns** (15-20 min)
   - % participants using full scale (1-5)
   - % extremes only (1s and 5s)
   - SD of ratings per participant
   - Flag restricted range

4. **GLMM paradigm baselines** (10 min) - **HIGH PRIORITY**
   - Resolve LRT vs pairwise paradox
   - Test which specific pairs drive omnibus effect

**Timeline:** 1.5-2 hours
**Priority:** 🔴 BLOCKER
**Dependencies:** Feeds into 6.3.2 (same calibration methodology)

---

### 6.3.2 - Domain Calibration (Crossover Interaction) ⚠️ DIFFERENCE SCORE

**Status:** Difference score reliability MISSING

**Critical Issue:**
- Calibration = confidence - accuracy (difference score)
- Reliability NOT computed (MANDATORY per taxonomy 6.2)
- Time-specific contrasts NOT run (AT T1, AT T4)
- When domain's extreme calibration (mean |cal|=1.024) may be artifact

**Required Actions (TIER 1):**

1. **Difference score reliability** (30-45 min) - **BLOCKER**
   - Same formula as 6.4.2
   - Critical: Check When domain separately (floor effects may reduce reliability)

2. **Time-specific contrasts** (15-20 min) - **BLOCKER**
   - Re-run contrasts at T1 (When overconfident, What/Where underconfident)
   - Re-run contrasts at T4 (When underconfident, What/Where overconfident)
   - Expected: Significant at BOTH timepoints (confirms crossover)

3. **GLMM T1 baseline validation** (10-15 min)
   - Test if T1 domain differences significant with item-level power
   - Expected: When vs What/Where significant at encoding

**Timeline:** 1-1.5 hours
**Priority:** 🔴 BLOCKER
**Dependencies:** Uses same data as 6.4.2

---

### 5.2.2 - Domain Consolidation (When Excluded) ⚠️ STALE DATA

**Status:** Data files STALE (3 domains), plots CURRENT (2 domains)

**Critical Issue:**
- Steps 02-04 data files show 3 domains (What/Where/When) from Nov 30
- Plots correctly show 2 domains (When excluded) from Dec 9
- Summary incorrectly claims plots are stale (they're not)
- Power analysis MISSING for NULL finding (MANDATORY per taxonomy 10.2)

**Required Actions (TIER 1):**

1. **Re-run steps 02-04** (1-2 hours)
   - Regenerate data files to match current 2-domain analysis
   - Verify outputs consistent with plots

2. **Fix summary.md documentation error** (15 min)
   - Remove false "plots are stale" warning
   - Confirm plots are current (Dec 9, 2 domains)

3. **Compute power analysis** (2 hours) - **MANDATORY**
   - Post-hoc power for observed d=0.03
   - Sample size for 0.80 power
   - Distinguish "underpowered" vs "true null"

**Timeline:** 4-5 hours
**Priority:** 🔴 BLOCKER
**Dependencies:** None

---

**TIER 1 SUMMARY:**

| RQ | Issue | Time | Priority | Status |
|----|-------|------|----------|--------|
| 5.4.1 | Schema GLMM integration | 5-6.5h | 🔴 CRITICAL | NOT DONE |
| 5.1.3 | Age GLMM integration | 4h | 🔴 CRITICAL | NOT DONE |
| 6.4.2 | Difference score reliability | 1.5-2h | 🔴 BLOCKER | NOT DONE |
| 6.3.2 | Difference score reliability | 1-1.5h | 🔴 BLOCKER | NOT DONE |
| 5.2.2 | Stale data + power analysis | 4-5h | 🔴 BLOCKER | NOT DONE |

**TOTAL TIER 1:** 16-20 hours

---

## TIER 2: HIGH PRIORITY RQs (Recommended Before Defense)

### 6.1.3 - Age Effects on Confidence Trajectory

**Status:** GLMM done, power analysis MISSING

**GLMM Validation:** ✅ COMPLETE
- Age intercept: IRT→LMM p=.125 → GLMM p=.041 (marginal)
- Age × Time: NULL robust (p=.323 → p=.27-.30)

**Required Actions (TIER 2):**

1. **Power analysis for Age × Time NULL** (1-2 hours) - **MANDATORY**
   - Post-hoc power for observed effect
   - Validates "age-invariant forgetting" claim

2. **TOST equivalence testing** (30 min)
   - Establish "true null" vs underpowered
   - Set equivalence bound (d < 0.20)

3. **GLMM narrative integration** (30 min)
   - Update summary.md with GLMM finding (marginal intercept p=.041)
   - Cross-reference to 5.1.3 (parallel finding for accuracy)

4. **LMM diagnostics** (20 min)
   - ACF check (per 5.1.3 precedent)
   - Residual plots

5. **Confidence response patterns** (1-2 hours) - **Section 1.4 requirement**
   - Document in summary limitations

**Timeline:** 3-4 hours
**Priority:** 🟡 HIGH
**Dependencies:** Parallels 5.1.3

---

### 6.1.1 - Confidence Trajectory (Overall Forgetting)

**Status:** Model averaging DONE, response patterns MISSING

**GLMM Validation:** ✅ Time effect validated (agrees with IRT→LMM)

**Strengths:**
- 65-model kitchen sink comparison DONE
- Model averaging DONE (48 competitive models, effective_n=31.1)
- Extended suite exceeds CLAUDE.md requirements

**Required Actions (TIER 2):**

1. **Response pattern analysis** (1 hour) - **MANDATORY**
   - % full-range vs extreme-only users
   - Addresses 100% threshold violations

2. **Alternative IRT models** (2-3 hours) - **CRITICAL**
   - Threshold violations in 100% items = GRM invalid
   - Test Nominal Response Model, Partial Credit Model
   - May affect downstream RQs 6.1.2-6.1.5

3. **LMM diagnostics for Recip_sq model** (30 min)
   - Q-Q plot, residuals vs fitted, Cook's D

4. **Verify plots use model-averaged predictions** (30 min)
   - Check if plots show MA predictions or single model
   - Regenerate if needed with uncertainty shading

5. **Outlier sensitivity** (30 min)
   - Extreme heterogeneity (-3 to +2 theta range) flagged
   - Test if findings robust to outliers

**Timeline:** 5-6 hours
**Priority:** 🟡 HIGH
**Dependencies:** Affects 6.1.2, 6.1.3, 6.1.4, 6.1.5 (all use theta from 6.1.1)

---

### 6.5.3 - Schema Effect on High-Confidence Errors

**Status:** GEE DONE, power analysis needed

**GEE Analysis:** ✅ COMPLETE
- LPM p=.043 (significant) → GEE p=.056 (NULL)
- Effect disappeared with proper clustering

**Critical Comparison:**
- RQ 5.4.1: Schema affects accuracy BASELINE (GLMM p=.011, significant)
- RQ 6.5.3: Schema does NOT affect HCE (GEE p=.056, marginal null)
- **Apparent contradiction needs reconciliation**

**Required Actions (TIER 2):**

1. **Power analysis for marginal null** (2-3 hours)
   - p=.056 very close to threshold
   - OR=1.46 suggests non-trivial effect
   - Determine underpowered vs true null

2. **Cross-check with 5.4.1 GLMM** (1 day)
   - Resolve: Accuracy sig, HCE null
   - Test if accuracy baseline predicts HCE patterns
   - Explore accuracy × confidence interaction

3. **Bootstrap CI for OR=1.46** (3-4 hours)
   - Validate parametric uncertainty estimates
   - Low base rate (5% HCE) may violate asymptotics

**Timeline:** 1.5 days (12 hours)
**Priority:** 🟡 HIGH
**Dependencies:** Requires 5.4.1 GLMM integration first

---

### 5.5.2 - Source-Destination Consolidation

**Status:** ROOT verification DONE, power analysis MISSING

**ROOT Verification:** ✅ COMPLETE (GLMM-equivalent)
- 13-model averaging confirms NULL interaction (p=1.000)
- Both Log-only and MA yield NULL

**Required Actions (TIER 2):**

1. **Power analysis for NULL interaction** (1-2 hours) - **MANDATORY**
   - Post-hoc power for f²=0.0005
   - Power for meaningful threshold (f²=0.02)

2. **TOST equivalence testing** (1-2 hours)
   - Establish "true null" vs underpowered
   - Recommended in summary Section 5.1

3. **Alternative breakpoint sensitivity** (2-3 hours)
   - Test 24h, 36h, 72h breakpoints
   - 48h never empirically validated

4. **LMM diagnostics** (1 hour)
   - Standard checks missing from documentation

**Timeline:** 5-8 hours
**Priority:** 🟡 HIGH
**Dependencies:** None

---

### 5.1.1 - Trajectory Model Selection (Overall Accuracy)

**Status:** Model averaging DONE, minor documentation gaps

**Strengths:**
- 66-model extended comparison ✅ DONE
- Model averaging ✅ DONE (16 competitive models)
- Power-law paradigm shift documented
- Plots current with MA predictions

**Required Actions (TIER 2):**

1. **Verify residual diagnostics exist** (10 min)
   - Check if step05d generated plots
   - Generate if missing

2. **Add formal Cohen's d with CIs** (30 min)
   - Currently descriptive only ("1.18 SD decline")
   - Need bootstrap 95% CI

3. **Optional: Test random slopes model** (30 min)
   - Compare intercepts-only vs intercepts+slopes
   - Current implementation defensible

**Timeline:** 40-90 minutes
**Priority:** 🟢 MEDIUM (minor polish)
**Dependencies:** None

---

**TIER 2 SUMMARY:**

| RQ | Issue | Time | Priority | Key Tasks |
|----|-------|------|----------|-----------|
| 6.1.3 | Power analysis, response patterns | 3-4h | 🟡 HIGH | Power + TOST + diagnostics |
| 6.1.1 | Response patterns, alt IRT | 5-6h | 🟡 HIGH | Alt IRT models critical |
| 6.5.3 | Power analysis, 5.4.1 cross-check | 12h | 🟡 HIGH | Resolve contradiction |
| 5.5.2 | Power analysis, TOST | 5-8h | 🟡 HIGH | Breakpoint sensitivity |
| 5.1.1 | Documentation polish | 1-1.5h | 🟢 MEDIUM | Minor enhancements |

**TOTAL TIER 2:** 26.5-34 hours

---

## TIER 3: MEDIUM PRIORITY RQs (Polish to PLATINUM)

### Template for Remaining 56 RQs

Based on improvement_taxonomy.md, each remaining RQ should undergo:

**Standard Checklist (applies to ALL):**

1. **GLMM Validation** (if applicable)
   - Intercept effects: Test group baseline differences
   - Binary outcomes: Use binomial GLMM with logit link
   - Skip if: Slope/interaction only (GLMM always agrees per glmm.md)

2. **Power Analysis** (MANDATORY for NULL findings)
   - Post-hoc power for observed effect
   - Power for meaningful threshold
   - Estimate N for 0.80 power

3. **Equivalence Testing (TOST)** (for NULL claims)
   - Set equivalence bound (d < 0.20 or f² < 0.02)
   - Establish "true null" vs "underpowered"

4. **LMM Diagnostics**
   - Q-Q plots, residuals vs fitted
   - Homoscedasticity (Breusch-Pagan)
   - Leverage/influence (Cook's D)

5. **Documentation**
   - Dual p-values (uncorrected + Bonferroni)
   - Dual scales (theta + probability for IRT RQs)
   - Plots current and annotated
   - Complete results summary

**Time per RQ:** 2-4 hours average

---

### Ch5 Remaining RQs (30 RQs)

**Trajectory/Model Selection RQs (5.1.x, 5.2.1):**
- Check if extended model suite (17+ models) tested
- If only 5 basic models → Run power law variants
- Model averaging if top model < 90% weight

**Age Effects RQs (5.2.3, 5.3.4, 5.4.3, 5.5.3):**
- GLMM validation recommended (per glmm_candidates.md MEDIUM priority)
- Test if age affects baselines for Domain/Paradigm/Schema/Source-Dest
- Power analysis for NULL age × time interactions

**Domain/Paradigm/Schema Series:**
- Cross-validate findings (e.g., 5.3.x domains, 5.4.x schema, etc.)
- Ensure consistent interpretation across related RQs

**Estimated Time:** 60-120 hours (30 RQs × 2-4 hours)

---

### Ch6 Remaining RQs (26 RQs)

**Calibration RQs (6.2.x-6.5.x series):**
- Difference score reliability (MANDATORY per taxonomy 6.2)
- Lord's Paradox mitigation (ANCOVA sensitivity)
- Confidence response patterns (Section 1.4 requirement)

**Age Effects RQs (6.2.5, 6.3.3, 6.4.3):**
- GLMM validation recommended
- Power analysis for NULL age × time interactions

**Schema Completion (6.5.1, 6.5.2):**
- GLMM validation (per glmm_candidates.md MEDIUM priority)
- Cross-check with 5.4.1 finding (baseline significant)
- Complete "triple null + baseline" validation

**Estimated Time:** 52-104 hours (26 RQs × 2-4 hours)

---

**TIER 3 SUMMARY:**

| Chapter | RQs | Est. Time | Key Focus |
|---------|-----|-----------|-----------|
| Ch5 | 30 | 60-120h | Age GLMM, power analysis, model completeness |
| Ch6 | 26 | 52-104h | Calibration reliability, response patterns, schema completion |

**TOTAL TIER 3:** 112-224 hours

---

## GLMM VALIDATION PRIORITY MATRIX

From glmm_candidates.md + context-finder findings:

### Already Validated ✅

| RQ | Effect | IRT→LMM | GLMM | Status |
|----|--------|---------|------|--------|
| 5.1.3 | Age intercept | p=.061 | **p=.014** | ✅ DONE |
| 5.1.3 | Age × Time | p=.83 | p=.46 | ✅ DONE |
| 5.4.1 | Schema intercept | p=.548 | **p=.011** | ✅ DONE |
| 5.4.1 | Schema × Time | NULL | NULL | ✅ DONE |
| 6.1.1 | Time effect | Sig | Sig | ✅ DONE |
| 6.1.3 | Age intercept | p=.125 | p=.041 | ✅ DONE |
| 6.1.3 | Age × Time | p=.32 | p=.27-.30 | ✅ DONE |

### HIGH Priority (Run Next)

| RQ | Hypothesis | Expected Finding | Time | Impact |
|----|-----------|------------------|------|--------|
| 6.3.2 | Domain T1 baselines | When vs What/Where sig | 10 min | HIGH |
| 6.4.2 | Paradigm baselines | Resolve LRT paradox | 10 min | HIGH |
| 6.5.1 | Schema → Confidence | Likely NULL | 10 min | MEDIUM |
| 6.5.2 | Schema → Calibration | Likely NULL | 10 min | MEDIUM |

### MEDIUM Priority (Validate if Time)

| RQ | Hypothesis | Expected Finding | Time | Impact |
|----|-----------|------------------|------|--------|
| 5.2.3 | Age × Domain | Likely NULL | 10 min | MEDIUM |
| 5.3.4 | Age × Paradigm | Likely NULL | 10 min | MEDIUM |
| 5.4.3 | Age × Schema | Likely NULL | 10 min | LOW |
| 5.5.3 | Age × Source-Dest | Likely NULL | 10 min | LOW |

**TOTAL GLMM TIME:** ~80 minutes (8 RQs × 10 min)

---

## IMPLEMENTATION TIMELINE

### Week 1: BLOCKERS (Days 1-5)

**Day 1-2: Schema Integration (8-10 hours)**
- RQ 5.4.1: GLMM integration (5-6.5h)
- Search thesis for "quadruple null" (2-3h)
- Update archive entries (30 min)

**Day 3: Age Effects Integration (4 hours)**
- RQ 5.1.3: GLMM integration (4h)

**Day 4: Calibration Reliability (3-3.5 hours)**
- RQ 6.4.2: Difference score + Lord's Paradox (1.5-2h)
- RQ 6.3.2: Difference score + time contrasts (1-1.5h)

**Day 5: Domain Consolidation (4-5 hours)**
- RQ 5.2.2: Re-run steps + power analysis (4-5h)

**WEEK 1 TOTAL:** 19-22 hours

---

### Week 2: HIGH PRIORITY (Days 6-10)

**Day 6: Confidence Validation (5-6 hours)**
- RQ 6.1.1: Response patterns + alt IRT (5-6h)

**Day 7-8: Age Effects Confidence + HCE (15-16 hours)**
- RQ 6.1.3: Power analysis + diagnostics (3-4h)
- RQ 6.5.3: Power analysis + 5.4.1 cross-check (12h)

**Day 9: Source-Dest Consolidation (5-8 hours)**
- RQ 5.5.2: Power + TOST + breakpoints (5-8h)

**Day 10: Documentation Polish (1-1.5 hours)**
- RQ 5.1.1: Minor enhancements (1-1.5h)

**WEEK 2 TOTAL:** 26.5-34 hours

---

### Week 3-4: MEDIUM PRIORITY (Days 11-22)

**Systematic Processing:**
- Process 5-6 RQs per day
- 2-4 hours per RQ
- Focus: Power analysis, GLMM where applicable, diagnostics

**Priority Order:**
1. **Days 11-12:** Age effects GLMM (5.2.3, 5.3.4, 6.2.5, 6.3.3, 6.4.3) - 5 RQs
2. **Days 13-14:** Schema completion GLMM (6.5.1, 6.5.2) + related - 6 RQs
3. **Days 15-16:** Calibration RQs (6.2.x series) - 6 RQs
4. **Days 17-18:** Domain RQs (5.2.x, 5.3.x, 6.3.x) - 8 RQs
5. **Days 19-20:** Paradigm RQs (5.3.x, 6.4.x) - 7 RQs
6. **Days 21-22:** Source-Dest + cleanup (5.5.x series, misc) - 8 RQs

**WEEK 3-4 TOTAL:** 80-120 hours (40 RQs × 2-3 hours avg)

---

## CRITICAL DEPENDENCIES

### Must Complete First (Upstream)

1. **5.4.1 GLMM Integration** → Affects:
   - 6.5.1 (schema → confidence)
   - 6.5.2 (schema → calibration)
   - 6.5.3 (schema → HCE)
   - All thesis "schema null" narrative

2. **5.1.3 GLMM Integration** → Affects:
   - 6.1.3 (parallel finding for confidence)
   - All "age-invariant" narrative

3. **6.1.1 Alternative IRT Models** → Affects:
   - 6.1.2 (uses theta from 6.1.1)
   - 6.1.3 (uses theta from 6.1.1)
   - 6.1.4 (ICC analysis, uses random effects from 6.1.1)
   - 6.1.5 (uses theta from 6.1.1)

4. **6.4.2 Difference Score Reliability** → Informs:
   - 6.3.2 (same calibration methodology)
   - All calibration RQs (6.2.x-6.5.x)

### Parallel Tracks (Can Run Simultaneously)

- **Ch5 Age Effects** (5.2.3, 5.3.4, 5.4.3, 5.5.3) - Independent
- **Ch6 Age Effects** (6.2.5, 6.3.3, 6.4.3) - Independent
- **Domain Series** (5.2.x, 5.3.x, 6.3.x) - Independent
- **Paradigm Series** (separate from domains)

---

## TOOLS & TEMPLATES

### GLMM Validation Script

**Location:** `results/glmm.md` contains validated approach for 4 RQs

**Template:**
```python
# Single-stage GLMM on item-level data
import statsmodels.formula.api as smf

# Load item-level data (NOT theta aggregated)
item_data = pd.read_csv('master.xlsx_item_level_responses.csv')

# For binary outcomes (accuracy)
model = smf.mixedlm(
    "Correct ~ Group * Time + (1 + Time | UID) + (1 | Item)",
    data=item_data,
    groups=item_data['UID'],
    family=sm.families.Binomial()
)

# For continuous outcomes (confidence)
# Use standard LMM on item-level responses
```

**Runtime:** ~10 minutes per RQ with 28,800 observations

---

### Power Analysis Script

**Template:**
```python
from statsmodels.stats.power import FTestAnovaPower

# Post-hoc power for observed effect
effect_size = observed_f_squared
alpha = 0.05
k_groups = 3  # Number of groups
n_total = 100  # Total sample size

power_analysis = FTestAnovaPower()
power = power_analysis.solve_power(
    effect_size=effect_size,
    nobs=n_total,
    alpha=alpha,
    k_groups=k_groups
)

# N required for 0.80 power
n_required = power_analysis.solve_power(
    effect_size=effect_size,
    power=0.80,
    alpha=alpha,
    k_groups=k_groups
)
```

**Runtime:** ~5 minutes per RQ

---

### TOST Equivalence Testing

**Template:**
```python
from scipy import stats

# Two One-Sided Tests
equivalence_bound = 0.20  # Cohen's d
observed_effect = 0.03

# Test 1: Effect > -equivalence_bound
t1 = (observed_effect - (-equivalence_bound)) / SE
p1 = stats.t.cdf(t1, df)

# Test 2: Effect < equivalence_bound
t2 = (equivalence_bound - observed_effect) / SE
p2 = stats.t.cdf(t2, df)

# Equivalence if both p < 0.05
tost_p = max(p1, p2)
```

**Runtime:** ~5 minutes per RQ

---

## QUALITY GATES

### BLOCKER Gate (Week 1)

**Criteria to pass Week 1:**
- ✅ 5.4.1 GLMM integrated, thesis updated
- ✅ 5.1.3 GLMM integrated, narrative revised
- ✅ 6.4.2 difference score reliability computed
- ✅ 6.3.2 difference score reliability computed
- ✅ 5.2.2 data files current, power analysis done

**If ANY blocker incomplete:** STOP, resolve before Week 2

---

### HIGH PRIORITY Gate (Week 2)

**Criteria to pass Week 2:**
- ✅ 6.1.1 threshold violations resolved (alt IRT models)
- ✅ 6.1.3 power analysis complete
- ✅ 6.5.3 5.4.1 cross-check resolved
- ✅ 5.5.2 TOST complete
- ✅ All TIER 1 + TIER 2 RQs thesis-ready

**If ANY high-priority incomplete:** Extend Week 2 by 1-2 days

---

### PLATINUM Certification (Week 4)

**Per RQ Checklist:**
- ✅ Statistical rigor (assumptions validated, robustness checks, effect sizes, power if NULL)
- ✅ Methodological soundness (appropriate model, sensitivity, no paradoxes)
- ✅ Documentation excellence (dual p-values, dual scales, plots current)
- ✅ Data quality (IRT justified, response patterns if applicable)
- ✅ Theoretical coherence (literature grounded, mechanisms, boundaries)
- ✅ Zero critical issues (no convergence failures, no missing mandatory analyses)

**Sign-off:** User approves each RQ's PLATINUM status before moving to next

---

## RISK MITIGATION

### Risk 1: Alternative IRT Models Change Downstream RQs

**Scenario:** RQ 6.1.1 alternative IRT produces different theta estimates

**Impact:** RQs 6.1.2-6.1.5 need refitting (estimated 2-4 hours each)

**Mitigation:**
- Run 6.1.1 alt IRT EARLY (Week 2 Day 6)
- If theta changes significantly (>0.2 SD): Refit 6.1.2-6.1.5 before Week 3
- Budget extra 8-16 hours contingency

---

### Risk 2: Difference Score Reliability < 0.70

**Scenario:** Calibration RQs have unreliable difference scores

**Impact:** Must switch to latent variable models (structural equation modeling)

**Mitigation:**
- Compute reliability EARLY (Week 1 Day 4)
- If r_diff < 0.70: Implement SEM approach (adds 4-6 hours per calibration RQ)
- Budget extra 40-60 hours for all calibration RQs if needed

---

### Risk 3: GLMM Reveals More Significant Effects

**Scenario:** Additional RQs show NULL → SIGNIFICANT changes

**Impact:** Major thesis narrative revisions

**Mitigation:**
- Run all HIGH/MEDIUM GLMM validations in Week 2
- Identify narrative impacts early
- Allocate extra 10-15 hours for cross-thesis updates if needed

---

## THESIS INTEGRATION CHECKLIST

After completing all RQs, update thesis chapters:

### Introduction
- ✅ Update research questions reflecting GLMM findings
- ✅ Revise hypotheses (schema, age effects)

### Methods
- ✅ Add GLMM validation methodology section
- ✅ Document difference score reliability approach
- ✅ Update power analysis procedures

### Results - Chapter 5
- ✅ Update all "age-invariant" claims to "age-invariant forgetting, not baseline"
- ✅ Update schema "quadruple null" to "triple null + baseline effect"
- ✅ Cross-reference GLMM validations

### Results - Chapter 6
- ✅ Update calibration methodology (reliability checks)
- ✅ Update schema findings (convergence with Ch5)
- ✅ Cross-reference GLMM validations

### Discussion
- ✅ Revise theoretical interpretation (encoding vs forgetting dissociation)
- ✅ Update schema theory implications (affects encoding, not metacognition)
- ✅ Strengthen VR scaffolding hypothesis (encoding support, not consolidation)

### Limitations
- ✅ Add GLMM vs IRT→LMM differences
- ✅ Note difference score reliability constraints
- ✅ Document threshold violations (if 6.1.1 alt IRT not fully resolved)

---

## SUMMARY METRICS

### Total Work Estimate

| Phase | RQs | Hours | Days | Status |
|-------|-----|-------|------|--------|
| **TIER 1 (BLOCKERS)** | 5 | 16-20 | 2-3 | 🔴 CRITICAL |
| **TIER 2 (HIGH)** | 5 | 26-34 | 3-4 | 🟡 RECOMMENDED |
| **TIER 3 (MEDIUM)** | 56 | 112-224 | 14-28 | 🟢 POLISH |
| **TOTAL** | 66 | 154-278 | 19-35 | |

### Conservative Estimate (Assume Upper Bound)

**Total Hours:** 278 hours
**Working Days (8h/day):** 35 days
**Calendar Time (5-day weeks):** 7 weeks

### Aggressive Estimate (Assume Lower Bound + Parallelization)

**Total Hours:** 154 hours
**Working Days (10h/day intense sprint):** 15 days
**Calendar Time:** 3 weeks

---

## RECOMMENDED APPROACH

### Option A: DEFENSE-READY (3 Weeks)

**Focus:** TIER 1 + TIER 2 only (10 RQs)

**Timeline:**
- Week 1: TIER 1 blockers (5 RQs, 16-20h)
- Week 2: TIER 2 high-priority (5 RQs, 26-34h)
- Week 3: Thesis integration + review (10-15h)

**Total:** 52-69 hours (6.5-8.5 days)
**Result:** Defense-ready, core findings robust, acceptable for thesis pass

---

### Option B: PUBLICATION-READY (6-8 Weeks)

**Focus:** TIER 1 + TIER 2 + TIER 3 (all 66 RQs)

**Timeline:**
- Week 1: TIER 1 blockers
- Week 2: TIER 2 high-priority
- Weeks 3-6: TIER 3 systematic processing (10 RQs/week)
- Weeks 7-8: Thesis integration, cross-validation, final review

**Total:** 154-278 hours (19-35 days)
**Result:** PLATINUM status all RQs, publication-ready, reviewer-proof

---

### Option C: HYBRID (4-5 Weeks)

**Focus:** TIER 1 + TIER 2 + selective TIER 3 (30 highest-impact RQs)

**Timeline:**
- Week 1: TIER 1 blockers (5 RQs)
- Week 2: TIER 2 high-priority (5 RQs)
- Weeks 3-4: TIER 3 selective (20 RQs with NULL findings, age effects, schema series)
- Week 5: Thesis integration + review

**Total:** 80-120 hours (10-15 days)
**Result:** Defense-ready + strong publication foundation for key findings

---

## FINAL RECOMMENDATIONS

**For PhD Defense (Minimal Viable):**
→ **Option A: DEFENSE-READY (3 weeks, 52-69 hours)**

**For First Journal Submission:**
→ **Option C: HYBRID (4-5 weeks, 80-120 hours)**

**For Comprehensive Publication Suite:**
→ **Option B: PUBLICATION-READY (6-8 weeks, 154-278 hours)**

---

**Next Steps:**

1. User reviews this roadmap
2. User selects Option A, B, or C
3. Begin with TIER 1 Day 1: RQ 5.4.1 GLMM integration (5-6.5 hours)
4. Progress through systematic checklist
5. Quality gate after each phase
6. Final PLATINUM certification

---

**Document Prepared By:** Claude Code
**Date:** 2025-12-27
**Version:** 1.0 - Comprehensive Finalization Roadmap
**Based On:**
- improvement_taxonomy.md (10-section framework)
- Context-finder analysis of 10 priority RQs
- glmm_candidates.md (GLMM validation strategy)
- 66 total Ch5/Ch6 RQs

**Status:** READY FOR USER REVIEW AND SELECTION