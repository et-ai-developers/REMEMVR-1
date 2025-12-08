# RQ 5.3.1 - Extended Model Selection & Averaging Complete

**Date:** 2025-12-08
**Task:** Kitchen sink + model averaging propagation from 5.2.1
**Status:** ✅ COMPLETE

---

## Executive Summary

### Model Selection Results

**Original (Basic 5):**
- Winner: Log model
- Weight: 99.98%
- Interpretation: Overwhelming confidence (likely overconfident)

**Extended (Kitchen Sink 66):**
- Winner: **PowerLaw_01** (α=0.1)
- AIC: 2375.72
- Weight: **6.7%** (EXTREME uncertainty)
- Log models: Ranks #2-4 (ΔAIC=0.07, essentially tied)
- Competitive models (ΔAIC < 2): **14 models**

### Key Finding: Model Uncertainty

**Original vs Extended:**
- Log dominance: 99.98% → 6.46% (demoted but still competitive)
- Evidence shift: **Log overconfidence factor = 15.5×**
- Power-law α=0.1 edges out Log by ΔAIC=0.07 (negligible)

**Interpretation:**
- Basic 5 comparison **severely underestimated** model uncertainty
- Extended testing reveals **NO clear winner** (14 competitive models)
- Log, PowerLaw α=0.1-0.2, SquareRoot all nearly equivalent
- Paradigm × Time interaction adds complexity (not simple trajectory)

---

## Model Averaging Solution

### Why Averaging Was Mandatory

**Single-model risk:**
- Best weight = 6.7% < 30% threshold → **EXTREME uncertainty**
- Cannot defend single model with 93.3% probability it's wrong
- Ph.D. thesis requirement: Scientifically defensible foundation

**Burnham & Anderson (2002) criterion:**
- Weight < 30% → Model averaging MANDATORY
- Accounts for functional form uncertainty
- Provides robust predictions across competing models

### Averaging Results

**Models Used:** 14 (ΔAIC < 2)
**Cumulative Weight:** 57.9% (renormalized to 100%)
**Effective N Models:** 12.90 (Shannon diversity - high diversity)

**Model Composition:**
- Logarithmic family: 9 models (Log, Log2, Log10, combos)
- Power-law family: 3 models (α=0.1, 0.2, Log-hybrid)
- Root family: 2 models (SquareRoot, CubeRoot+Log)

**Effective Functional Form:**
- Weighted mean α = 0.140 (shallow power-law decline)
- Dominated by Log/PowerLaw hybrid (nearly identical trajectories)
- Paradigm × Time interaction preserved across all models

**Uncertainty Quantification:**
- Prediction SE: 0.003-0.047 (between-model variance)
- All paradigms show same range (symmetric interaction)

---

## Comparison to Other ROOT RQs

| RQ | Basic Winner | Extended Winner | Best Weight | Action Taken |
|----|-------------|-----------------|-------------|--------------|
| **5.1.1** | Log (48%) | PowerLaw α=0.5 (5.6%) | 5.6% | ✅ Averaged 16 models |
| **5.2.1** | Log (92%) | Recip+Log (8.9%) | 8.9% | ✅ Averaged 10 models |
| **5.3.1** | Log (99.98%) | **PowerLaw α=0.1 (6.7%)** | 6.7% | ✅ Averaged 14 models |
| **5.4.1** | Log (99.98%) | Recip+Log (74%) | 74% | ❌ Single model OK |

### Pattern Across Ch5 ROOT RQs

**Log model performance:**
- Basic 5: Unanimous winner (4/4 tested)
- Extended 66: Challenged in 3/4 cases
- Only 5.2.1 maintains Log lead (but weak 8.9% weight)

**Model uncertainty:**
- Simple trajectories (5.1.1): Moderate (5.6% weight)
- Interactions (5.2.1, 5.3.1): Extreme (<10% weight)
- Complex interactions (5.4.1): Moderate (74% weight, Recip+Log)

**Interpretation:**
- Interaction terms increase model uncertainty
- Log vs PowerLaw distinction blurs with multiple factors
- Domain/Paradigm effects don't strongly favor one functional form
- Two-process models (Recip+Log) emerge for schema effects (5.4.1)

---

## Theoretical Implications for RQ 5.3.1

### Paradigm × Time Functional Form

**Effective α = 0.140 (shallow power-law):**
- Slower decay than general forgetting (5.1.1: α=0.410)
- Paradigm-specific trajectories but similar decline rates
- IFR/ICR/IRE differences in intercept, not slope shape

**Log models remain competitive:**
- ΔAIC=0.07 (essentially tied with PowerLaw α=0.1)
- Ebbinghaus curve still plausible for paradigm forgetting
- Power-law vs log debate unresolved at this level

**Paradigm interaction:**
- All 14 competitive models preserve paradigm × time structure
- Model averaging captures shared trajectory shape across paradigms
- Differences in magnitude (θ intercepts), not functional form

### Comparison to RQ 5.1.1 (General Forgetting)

| Aspect | RQ 5.1.1 (No Interaction) | RQ 5.3.1 (Paradigm × Time) |
|--------|---------------------------|----------------------------|
| **Best model** | PowerLaw α=0.5 | PowerLaw α=0.1 (tied with Log) |
| **Best weight** | 5.6% | 6.7% |
| **Competitive models** | 16 | 14 |
| **Effective α** | 0.410 (moderate) | 0.140 (shallow) |
| **Interpretation** | Strong power-law evidence | Log/PowerLaw ambiguous |

**Why shallower α in 5.3.1?**
- Paradigm interaction adds complexity
- Averaging over 3 paradigms may flatten trajectory
- IRT scoring may compress paradigm differences
- Recognition ceiling effect (high initial θ)

---

## Impact on Downstream RQs

### Type 5.3.X Derivatives

**RQs affected:** 5.3.2-5.3.9 (8 derivative RQs)

**Current status:**
- All used basic 5-model Log winner (99.98% weight)
- Assumed log_TSVR as time transformation

**Required changes:**
- **LOW PRIORITY** - Log model still competitive (rank #2-4)
- Extended testing shows Log ≈ PowerLaw α=0.1 (ΔAIC=0.07)
- Original Log-based analyses likely robust
- Could note "model selection uncertainty" in limitations

**Contrast with RQ 5.4.X:**
- 5.4.1 found Recip+Log (ΔAIC=7.50 vs Log) → HIGH IMPACT
- 5.3.1 found PowerLaw/Log tie (ΔAIC=0.07) → LOW IMPACT
- 5.3.X derivatives probably don't need re-running

---

## Files Created/Modified

### New Analysis Scripts
1. `code/step05_fit_extended_lmm_models.py` - Kitchen sink (66 models)
2. `code/step05c_model_averaging.py` - Multi-model inference

### New Data Files
1. `data/model_comparison.csv` - All 65 models, AIC-ranked
2. `data/step05_best_model_summary.txt` - PowerLaw_01 summary
3. `data/step05c_averaged_predictions.csv` - Averaged trajectories (300 rows)

### New Results Files
1. `results/step05c_averaging_summary.txt` - Model averaging details
2. `EXTENDED_MODEL_COMPLETION_SUMMARY.md` - This document

### Log Files
1. `logs/step05_kitchen_sink.log` - Model fitting log (65 models)
2. `logs/step05c_model_averaging.log` - Averaging execution log

---

## Validation Checklist

- [x] **Continuous time variable?** YES (TSVR_hours, 295 unique values)
- [x] **Kitchen sink run?** YES (66 models defined, 65 converged)
- [x] **Best model weight >30%?** NO (6.7% → model averaging required)
- [x] **Model averaging implemented?** YES (14 models, 57.9% cumulative)
- [x] **Effective N models reported?** YES (12.90, high diversity)
- [x] **Prediction uncertainty quantified?** YES (SE=0.003-0.047)
- [x] **Functional form interpreted?** YES (Log/PowerLaw hybrid, α_eff=0.140)
- [x] **Thesis defense script prepared?** YES (see "Theoretical Implications")

---

## Thesis Defense Talking Points

### Reviewer Question: "Why did you test 66 models?"

**Answer:**
> "Initial 5-model comparison suggested logarithmic forgetting with 99.98% certainty. However, this excluded power-law models (Wixted & Ebbesen, 1991) and other mathematically plausible functional forms. Extended testing revealed EXTREME model uncertainty (best weight = 6.7%), with logarithmic and power-law α=0.1 models essentially tied (ΔAIC=0.07). We implemented multi-model inference (Burnham & Anderson, 2002) to account for this uncertainty, averaging predictions across 14 competitive models. This provides a scientifically defensible foundation robust to functional form assumptions."

### Reviewer Question: "How do you interpret α=0.140?"

**Answer:**
> "The effective α=0.140 represents a shallow power-law decline, slower than the general forgetting curve (5.1.1: α=0.410). This suggests paradigm-specific forgetting may be more gradual, possibly due to: (1) averaging over three distinct paradigm processes, (2) IRT measurement compressing paradigm differences, or (3) recognition ceiling effects. Notably, logarithmic models remain competitive (ΔAIC=0.07), indicating the power-law vs. log debate is unresolved at this interaction level."

### Reviewer Question: "Did this change your conclusions?"

**Answer:**
> "No. The extended analysis confirmed that logarithmic models remain highly competitive (ranks #2-4, within ΔAIC=0.07 of best). Original downstream analyses (RQs 5.3.2-5.3.9) used log_TSVR and are likely robust. The key discovery is model UNCERTAINTY, not model REPLACEMENT. We now quantify this uncertainty via prediction standard errors (SE=0.003-0.047), which was impossible with single-model approaches."

---

## Comparison to Thesis-Mate RQs (5.2.1, 5.4.1)

### RQ 5.2.1 (Domain × Time)
- Extended winner: Recip+Log (8.9% weight)
- Pattern: Two-process forgetting (rapid + asymptotic)
- Impact: MODERATE (Recip+Log replaces Log, but low weight)

### RQ 5.3.1 (Paradigm × Time)
- Extended winner: PowerLaw α=0.1 (6.7% weight)
- Pattern: Log/PowerLaw ambiguous (ΔAIC=0.07)
- Impact: **LOW** (Log still competitive, original analyses robust)

### RQ 5.4.1 (Schema × Time)
- Extended winner: Recip+Log (74% weight)
- Pattern: Two-process forgetting (consolidation + decay)
- Impact: **HIGH** (Log demoted rank #10, ΔAIC=7.50, derivatives need re-run)

**Takeaway:**
- Schema effects (5.4.1) show STRONGEST deviation from Log
- Domain/Paradigm effects (5.2.1, 5.3.1) show weak-moderate deviations
- Model averaging essential for all three (all < 30% weight)
- Only 5.4.1 requires re-running downstream RQs

---

## Next Steps

### Immediate (This Session)
1. ✅ Kitchen sink complete (65/66 models fit)
2. ✅ Model averaging complete (14 models, effective N=12.90)
3. ⏭️ Update MODEL_SELECTION_SUMMARY.md with 5.3.1 findings
4. ⏭️ Update results/models.tsv with 5.3.1 entry

### Optional (Lower Priority)
- Could regenerate plots with model-averaged predictions (low priority, Log still valid)
- Could update summary.md with model uncertainty caveat (low priority)
- Could create side-by-side comparison plot (Log vs Averaged, nearly identical)

### Future (Other ROOT RQs)
- Test extended models on 5.5.1 (Source-Dest trajectories)
- Test extended models on Ch6 ROOT RQs (confidence trajectories)

---

**Document Status:** Complete
**Analysis Status:** RQ 5.3.1 extended model selection DONE
**Thesis Impact:** LOW (Log models remain competitive, original analyses robust)
**Methodological Contribution:** Demonstrates model averaging protocol for complex interactions
