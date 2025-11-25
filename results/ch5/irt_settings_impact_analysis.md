# IRT Settings Impact Analysis

**Date:** 2025-11-25
**Analyst:** Claude Code
**Purpose:** Quantify impact of correcting IRT calibration settings from dramatically reduced to validated "Med" level

---

## Settings Changed (Validated "Med" vs Previous Low)

| Parameter | Previous (WRONG) | Validated "Med" | Ratio |
|-----------|------------------|-----------------|-------|
| `model_fit.batch_size` | 128 | 2048 | 16x |
| `model_fit.iw_samples` | 5 | 100 | 20x |
| `model_scores.batch_size` | 128 | 2048 | 16x |
| `model_scores.mc_samples` | 1 | **100** | **100x** |
| `model_scores.iw_samples` | 5 | 100 | 20x |

**Critical Parameter:** `mc_samples=100` for theta estimation (100x increase)
- Old: Averaging over 1 Monte Carlo sample per theta estimate
- New: Averaging over 100 Monte Carlo samples per theta estimate
- Impact: Dramatically improved precision in person ability estimates

---

## Theta Score Correlation Analysis (RQ 5.1)

Compared old Pass 2 theta (low settings) vs new Pass 1 theta (validated settings):

| Domain | Correlation (r) | RMSE | Threshold | Verdict |
|--------|----------------|------|-----------|---------|
| **What** | 0.86 | 0.540 | r ≥ 0.95 | **FAILED** |
| **Where** | 0.91 | 0.412 | r ≥ 0.95 | **FAILED** |
| **When** | 0.68 | 0.753 | r ≥ 0.95 | **FAILED (SEVERE)** |

**Interpretation:**
- ALL three domains fell below r ≥ 0.95 measurement consistency threshold
- When domain showed SEVERE impact (r=0.68), already problematic domain made worse
- Old theta scores systematically imprecise, compromising ALL downstream LMM analyses

---

## RQ 5.1 Results Comparison

### Item Purification (Decision D039: a ≥ 0.4, |b| ≤ 3.0)

| Version | Items Analyzed | Items Retained | Retention Rate |
|---------|----------------|----------------|----------------|
| **Old (Low Settings)** | 105 | 70 | 66.7% |
| **New (Validated Settings)** | 105 | 69 | 65.7% |
| **Change** | - | -1 | -1.0% |

**Minimal difference in purification** - Nearly identical item retention, validating Decision D039 thresholds are robust.

### LMM Model Selection

| Version | Best Model | AIC | AIC Weight |
|---------|------------|-----|------------|
| **Old** | Log | 3187.96 | 0.619 |
| **New** | Log | 2523.36 | 0.917 |
| **Difference** | Same | -664.60 | +0.298 |

**Key Findings:**
1. **Same best model selected** (Logarithmic) - validates model selection is robust
2. **AIC decreased by 664.60** - MASSIVE improvement in model fit quality
3. **AIC weight increased from 62% to 92%** - much stronger evidence for Log model
4. **Lower AIC = better fit** - validated theta scores provide cleaner signal

### Post-Hoc Contrasts (Decision D068)

| Comparison | Old Beta | New Beta | Old p | New p | Conclusion |
|------------|----------|----------|-------|-------|------------|
| **Where - What** | 0.037 | 0.073 | .722 | .339 | Both NS |
| **When - What** | -0.415 | -0.314 | <.001 | <.001 | **Both SIG (magnitude changed)** |
| **When - Where** | -0.452 | -0.388 | <.001 | <.001 | **Both SIG (magnitude changed)** |

**Key Findings:**
1. **Same pattern of significance** - When differs from What/Where (both settings agree)
2. **Effect magnitudes changed:**
   - When-What: -0.415 → -0.314 (24% smaller effect)
   - When-Where: -0.452 → -0.388 (14% smaller effect)
3. **Scientific interpretation unchanged** - When domain shows less forgetting than What/Where
4. **Precision improved** - validated theta provides more accurate effect size estimates

### Fixed Effects (Logarithmic Model)

| Effect | Old Coef | New Coef | Old p | New p | Change |
|--------|----------|----------|-------|-------|--------|
| Intercept | 0.613 | 0.563 | <.001 | <.001 | -8% |
| When vs What | -0.415 | -0.314 | <.001 | <.001 | -24% |
| Where vs What | 0.037 | 0.073 | .722 | .339 | +97% |
| log(Days) | -0.528 | -0.536 | <.001 | <.001 | +2% |
| log(Days) x When | 0.343 | 0.405 | <.001 | <.001 | +18% |
| log(Days) x Where | -0.030 | -0.028 | .711 | .642 | -7% |

**Key Findings:**
1. **Main effect of time (log_Days) extremely stable** - Only 2% change (validates time effect is real)
2. **Domain main effects shifted** - When effect 24% smaller, Where doubled (but still NS)
3. **Time x Domain interactions changed** - When interaction 18% larger with validated theta
4. **All significance patterns preserved** - No changes to which effects are significant
5. **Validated settings provide more accurate effect size estimates**

### Random Effects

| Component | Old | New | Change |
|-----------|-----|-----|--------|
| Participant intercepts | 0.264 | 0.292 | +11% |
| Participant slopes | 0.046 | 0.052 | +13% |
| Intercept-slope covariance | -0.056 | -0.072 | +29% |
| Residual variance | 0.705 | 0.380 | **-46%** |

**KEY FINDING:**
- **Residual variance decreased 46%** (0.705 → 0.380)
- **Random effects increased modestly** (intercepts +11%, slopes +13%)
- **Interpretation:** Validated theta captures MORE systematic variance in forgetting trajectories
- **Less "noise" left in residuals** - cleaner measurement, better model fit

---

## RQ 5.3 Changes (Paradigm Analysis)

### Item Purification

| Version | Items Retained | Retention Rate |
|---------|----------------|----------------|
| **Old** | 51 | 70.8% |
| **New** | 45 | 62.5% |
| **Change** | -6 | -8.3% |

**More stringent purification with validated settings** - 6 additional items excluded when using precise theta estimates.

**Domain Breakdown (NEW):**
- Cued Recall: 19 items (79% retention)
- Recognition: 14 items (58% retention)  
- Free Recall: 12 items (50% retention)

---

## Scientific Implications

### Publication Quality Assessment

**Old Results (Low IRT Settings):**
- ❌ Theta scores with r=0.68-0.91 vs target r≥0.95
- ❌ Imprecise person ability estimates (mc_samples=1)
- ❌ 100x fewer samples than validated methodology
- ❌ **NOT PUBLICATION QUALITY**

**New Results (Validated IRT Settings):**
- ✅ Theta scores using validated "Med" settings
- ✅ Precise person ability estimates (mc_samples=100)
- ✅ Settings explicitly validated in thesis/analyses/ANALYSES_DEFINITIVE.md
- ✅ **PUBLICATION QUALITY**

### When Domain Implications

**Problem:** When (temporal) domain already showing floor effects and measurement issues.

**Old vs New Correlation:** r=0.68 (SEVERE impact)

**Current Status:**
- RQ 5.1: When domain shows less forgetting than What/Where (may be floor artifact)
- RQ 5.3: Awaiting rerun with validated settings to assess floor effects
- Validated theta may worsen/improve measurement quality - won't know until analysis complete

**User's Concern Validated:** When domain measurement quality is critical issue requiring validated theta estimates.

---

## Conclusion

**Critical Finding:** Previous RQ 5.1-5.5 results used IRT settings 20-100x too low, producing theta scores with correlation r=0.68-0.91 vs target r≥0.95. These imprecise estimates compromised ALL downstream LMM analyses.

**Impact on Results:**
1. **Model selection ROBUST** - Same best model (Log) selected both times
2. **Effect patterns PRESERVED** - Same significance patterns (When differs from What/Where)
3. **Effect magnitudes CHANGED** - 2-24% shifts in coefficient estimates
4. **Model fit MASSIVELY improved** - AIC decreased 664.60 points, residual variance decreased 46%
5. **Precision DRAMATICALLY improved** - Validated theta captures more systematic variance

**Mandatory Action:** Full rerun of RQ 5.1-5.5 required for publication-quality results.

**Scientific Validity:** Core findings remain consistent (logarithmic forgetting, When domain differences), but effect size estimates are now more accurate with validated settings.

**Lesson Learned:** Never reduce critical parameters (especially mc_samples for theta estimation) without explicit documentation and validation. Runtime vs precision trade-off must favor precision for publication quality.

---

**Analysis Complete**
