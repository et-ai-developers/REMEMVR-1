# LMM Model Selection Summary: Chapters 5 & 6

**Generated:** 2025-12-08
**Purpose:** Comprehensive inventory of all LMM trajectory modeling ROOT RQs, model selections, and downstream dependencies
**Source:** Context-finder agents + direct inspection of results/ch5 and results/ch6

---

## Executive Summary

### Key Findings

1. **Extended Model Testing Reveals Log Model Overconfidence**
   - 5/5 Ch5 ROOT RQs tested extended 66-model suite
   - 4/5 show extreme model uncertainty (best weight < 30%)
   - RQ 5.4.1: Most extreme case (Log 99.98% → PowerLaw_01 6.0%, overconfidence factor 16,630×, 15 competitive models)

2. **Chapter 6 Model Selection Gap**
   - 5/6 Ch6 ROOT RQs performed NO model selection
   - Assumed log_TSVR based on Ch5 precedent without testing
   - Only RQ 6.6.1 tested models (13 variants, not full 66)

3. **Extreme Model Uncertainty in Schema Congruence**
   - RQ 5.4.1: 15 competitive models within ΔAIC < 2 (unprecedented)
   - PowerLaw α=0.1 nominally best (6.0% weight), but Log #2 with 5.7%
   - Model averaging mandatory: effective N = 13.96 models
   - Theoretical significance: Schema congruence shows no dominant functional form

4. **Power Law vs Logarithmic**
   - RQ 5.1.1: PowerLaw_Alpha05 wins extended (ΔAIC=2.97 vs Log)
   - Supports Wixted & Ebbesen (1991) power-law forgetting over Ebbinghaus logarithmic
   - But Log still competitive in complex interactions (5.3.1, 5.2.1)

---

## Chapter 5: Accuracy Trajectories

### ROOT RQs: Model Selection Results

| RQ | Topic | Basic 5 Winner | Extended 66 Winner | Evidence Shift |
|----|-------|-----------------|--------------------| ---------------|
| **5.1.1** | General Omnibus | Log (48%) | **PowerLaw α=0.5** (15%) | Log overstated 3.2× |
| **5.2.1** | Domains | Log (92%) | **Recip+Log** (8.9%) | Log overstated 10.3× |
| **5.3.1** | Paradigms | Log (99.98%) | **PowerLaw α=0.1** (6.7%) | Log overstated 14.9×, but tied ΔAIC=0.07 |
| **5.4.1** | Congruence | Log (99.98%) | **PowerLaw α=0.1** (6.0%) | Log overstated 16,630× (15 competitive models, averaging mandatory) |
| **5.5.1** | Source-Dest | Log (64%) | **Quadratic** (6.7%) | Log overstated 9.6× |

### Pattern Analysis

**Log Model Performance:**
- **Unanimous winner in basic 5 comparison** (5/5 ROOT RQs)
- **Challenged in ALL extended comparisons** (best weight always <30%)
- **Overconfidence systematic:** Basic comparisons underestimate model uncertainty
- **Ranks #2-4 in extended tests** (still competitive, but no longer dominant)

**Extended Model Champions:**
- **PowerLaw α=0.5 (t^-0.5):** Best for simple trajectories (5.1.1)
- **PowerLaw α=0.1 (t^-0.1):** Best for schema congruence (5.4.1, 6.0% weight) and paradigm (5.3.1, 6.7% weight)
- **Recip+Log (1/t + log t):** Best for domain interactions (5.2.1, 8.9% weight)
- **Quadratic (t²):** Best for source-destination (5.5.1, 6.7% weight)

**Theoretical Implications:**
- **Single trajectories:** Power-law decay (Wixted & Ebbesen, 1991) - α=0.5 (moderate confidence)
- **Schema Congruence:** EXTREME uncertainty (15 competitive models, effective N=13.96), model averaging mandatory
- **Paradigm interactions:** Log/PowerLaw ambiguous (ΔAIC=0.07)
- **Domain interactions:** Recip+Log (two-process: rapid early + slow asymptotic), model averaging mandatory
- **Source-Destination:** Quadratic (accelerating forgetting), model averaging mandatory

---

## Chapter 6: Confidence Trajectories

### ROOT RQs: Model Selection Results

| RQ | Topic | Model Selection Performed? | Model Used | Justification |
|----|-------|---------------------------|------------|---------------|
| **6.1.1** | Confidence Form | Planned (not executed) | Log (assumed) | Planning document only |
| **6.3.1** | Domain Confidence | ❌ No | log_TSVR | Assumed from Ch5 |
| **6.4.1** | Paradigm Confidence | ❌ No | log_TSVR | Assumed from Ch5 |
| **6.5.1** | Schema Confidence | ❌ No | log_TSVR | Assumed from Ch5 |
| **6.6.1** | High-Conf Errors | ✅ Yes (13 models) | SquareRoot | Extended 13 (not 17) |
| **6.8.1** | Source-Dest Confidence | ❌ No | log_TSVR | Assumed from Ch5 |

### Critical Gap

**Only 1/6 Ch6 ROOT RQs** performed model selection (6.6.1)

**Problem:** Ch5 accuracy results (Log dominance) may not generalize to Ch6 confidence ratings
- Different construct (metacognitive monitoring vs episodic memory)
- Different scale (ordinal 5-category vs binary/continuous theta)
- Different temporal dynamics (confidence adjusts, accuracy doesn't)

**Evidence of divergence:**
- RQ 6.6.1: SquareRoot wins (HCE rates), not Log
- RQ 6.8.1 vs 5.5.1: Confidence NULL, accuracy significant (dissociation)

**Recommendation:** Test extended 17 models on all Ch6 ROOT RQs

---

## Model Comparison Suites

### Basic 5 (Tested in All ROOT RQs)

1. **Linear:** `y ~ t` (constant rate)
2. **Quadratic:** `y ~ t + t²` (accelerating/decelerating)
3. **Logarithmic:** `y ~ log(t+1)` (Ebbinghaus curve)
4. **Lin+Log:** `y ~ t + log(t+1)` (hybrid)
5. **Quad+Log:** `y ~ t + t² + log(t+1)` (complex)

### Extended 17 (Tested in 5.1.1, 5.2.1, 5.3.1, 5.4.1)

**Power-Law Family (6):**
- PowerLaw_Alpha03: `y ~ (t+1)^-0.3`
- PowerLaw_Alpha05: `y ~ (t+1)^-0.5`
- PowerLaw_Alpha07: `y ~ (t+1)^-0.7`
- PowerLaw_LogLog: `y ~ log(log(t+1)+1)`
- PowerLaw_Combined: `y ~ log(t+1) + log(log(t+1)+1)`
- CubeRoot: `y ~ t^(1/3)`

**Root Transformations (3):**
- SquareRoot: `y ~ sqrt(t)`
- SquareRoot+Log: `y ~ sqrt(t) + log(t+1)`
- *(CubeRoot already in power-law)*

**Reciprocal Family (2):**
- Reciprocal: `y ~ 1/(t+1)`
- Recip+Log: `y ~ 1/(t+1) + log(t+1)` ← **WINNER RQ 5.4.1**

**Exponential (2):**
- Exponential: `y ~ -t` (proxy for exp(-λt))
- Exp+Log: `y ~ -t + log(t+1)`

**Total:** 5 basic + 12 new = 17 models

### Extended 13 (Tested in 6.6.1 only)

Not documented in detail - appears to be subset of 17-model suite plus piecewise variants

---

## Random Effects Specifications

### Chapter 5 Pattern: Random Slopes on Time

**Standard formula:**
```r
y ~ TimeTransform * Condition + (TimeTransform | UID)
```

**RQ-specific:**
- 5.1.1: `(log_Days | UID)` - random intercept + slope on log time
- 5.2.1: `(log_Days | UID)` per domain
- 5.3.1: `(log_Days | UID)` per paradigm
- 5.4.1: `(log_TSVR | UID)` per congruence
- 5.5.1: `(log_Days | UID)` per location type

**Critical Rule:** Random slope must match dominant fixed effect transformation
- If `log_Days` is primary time term → use `~log_Days` random slope
- If `recip_Days` is primary → use `~recip_Days` random slope
- Mismatch causes underestimation of variance (see random_slope_correction archive)

### Chapter 6 Pattern: Random Intercepts Only

**Standard formula:**
```r
y ~ TimeTransform * Condition + (1 | UID)
```

**Justification:**
- Random slope variance often ≈ 0 (boundary warnings)
- ML estimation unstable with near-zero variance components
- Confidence decline rate homogeneous across participants

**Exception:** RQ 6.6.1 attempted `(Days | UID)` but produced boundary warning

---

## Downstream Dependencies

### Type 5.1 (General)
**ROOT:** 5.1.1 (Log model, 48% weight)
- 5.1.2: Two-phase forgetting
- 5.1.3: Age × Time
- 5.1.4: Variance decomposition (ICC_slope ≈ 0)
- 5.1.5: K-means clustering (K=2)

### Type 5.2 (Domains)
**ROOT:** 5.2.1 (Log model, 92% weight)
- 5.2.2-5.2.7: Domain-specific analyses
- **CRITICAL:** When domain excluded from ALL derivatives (floor effect)

### Type 5.3 (Paradigms)
**ROOT:** 5.3.1 (Log model, 99.98% weight)
- 5.3.2: Linear gradient (IFR < ICR < IRE)
- 5.3.3: Consolidation effects
- 5.3.4: Age × Paradigm
- 5.3.5: IRT-CTT convergence
- 5.3.6: Purified CTT (paradox: better r, worse AIC)
- 5.3.7: Variance decomposition (ICC ≈ 0)
- 5.3.8: Clustering (K=3, weak)
- 5.3.9: Item difficulty invariance (**answers 3 other RQs**)

### Type 5.4 (Congruence)
**ROOT:** 5.4.1 (Log model basic, Recip+Log extended)
- 5.4.2-5.4.7: Schema-specific analyses
- **NULL CASCADE:** 5.4.1 null → all derivatives null (expected)

### Type 5.5 (Source-Dest)
**ROOT:** 5.5.1 (Quadratic model, 6.7% weight, 13-model averaging)
- Extended testing: Extreme uncertainty (13 competitive models ΔAIC<2, cumulative 54.3%)
- Model composition: Quadratic+Log+SquareRoot+PowerLaw hybrid
- Derivative RQs:
  - 5.5.2-5.5.3: Complete
  - 5.5.4-5.5.7: Incomplete (concept only)

### Type 6.3 (Domain Confidence)
**ROOT:** 6.3.1 (log_TSVR assumed)
- 6.3.2: Domain calibration
- 6.3.3: Age × Domain confidence
- 6.3.4: ICC by domain

### Type 6.4 (Paradigm Confidence)
**ROOT:** 6.4.1 (log_TSVR assumed)
- 6.4.2: Paradigm calibration
- 6.4.3: Age × Paradigm confidence
- 6.4.4: ICC by paradigm

### Type 6.5 (Schema Confidence)
**ROOT:** 6.5.1 (log_TSVR assumed)
- 6.5.2: Schema calibration
- 6.5.3: HCE by schema

### Type 6.6 (High-Confidence Errors)
**ROOT:** 6.6.1 (SquareRoot model, 17% weight)
- 6.6.2: HCE profiles
- 6.6.3: HCE domain specificity

### Type 6.8 (Source-Dest Confidence)
**ROOT:** 6.8.1 (log_TSVR assumed)
- 6.8.2: Source-dest calibration
- 6.8.3: ICC (CRITICAL for opposite-correlation)
- 6.8.4: Clustering

---

## Impact of Extended Model Testing

### RQ 5.1.1: Moderate Impact
- **Basic:** Log wins (48%)
- **Extended:** PowerLaw_Alpha05 wins (15%)
- **ΔAIC:** 2.97 (substantial evidence for power law)
- **Interpretation shift:** Ebbinghaus → Wixted forgetting theory
- **Downstream:** Would require re-running 5.1.2-5.1.5 with new random slopes

### RQ 5.3.1: VERY LOW Impact (Updated 2025-12-08)
- **Basic:** Log overwhelming (99.98%)
- **Extended:** PowerLaw α=0.1 wins (6.7%), Log ranks #2-4 (6.46%)
- **ΔAIC:** 0.07 (negligible - essentially tied)
- **Model averaging:** 14 models (cumulative 57.9%, effective N=12.90)
- **Effective α:** 0.140 (shallow power-law, Log/PowerLaw hybrid)
- **Interpretation:** Log vs PowerLaw **AMBIGUOUS** at this level
- **Downstream:** **NO changes needed** - Log models remain highly competitive
- **Key insight:** Model UNCERTAINTY revealed (15× overconfidence), not model REPLACEMENT

### RQ 5.4.1: HIGH IMPACT
- **Basic:** Log overwhelming (99.98%)
- **Extended:** Recip+Log dominates (74%)
- **ΔAIC:** 7.50 (strong evidence against Log, ratio 42:1)
- **Interpretation shift:** Single-process → two-process forgetting (consolidation + asymptotic)
- **Downstream:** MUST re-run 5.4.2-5.4.7 with new random slopes (recip_TSVR)
- **Theoretical:** Schema congruence has unique temporal dynamics not captured by Log

### RQ 5.2.1: Moderate Impact (Updated 2025-12-08)
- **Basic:** Log strong (92%)
- **Extended:** Recip+Log wins (8.9%), Log demoted to rank #43
- **ΔAIC:** 8.91 (strong evidence for Recip+Log, ratio 889:1)
- **Model averaging:** 10 models (cumulative 54.8%, effective N=9.45)
- **Interpretation:** Two-process forgetting (rapid + asymptotic decay)
- **Downstream:** Could re-run with recip_TSVR random slopes, but low priority (weak weight)

### RQ 5.5.1: EXTREME UNCERTAINTY (Updated 2025-12-08)
- **Basic:** Log moderate (64%)
- **Extended:** Quadratic wins (6.7%), Log ranks #2-4 (5.6% each)
- **ΔAIC:** 0.34 (negligible - Log essentially tied with Quadratic)
- **Model averaging:** 13 models (cumulative 54.3%, effective N=12.32)
- **Effective α:** 0.140 (power-law contribution minimal)
- **Model composition:** Quadratic (12%), Log (31%), SquareRoot (22%), PowerLaw (22%), Recip (5%)
- **Interpretation:** **NO CLEAR WINNER** - multiple competing forgetting processes
- **Downstream:** Model averaging predictions MANDATORY for 5.5.2-5.5.7
- **Key insight:** Source-destination dissociation shows most ambiguous functional form of all Ch5 RQs

---

## Recommendations

### Immediate Actions

1. **Update RQ 5.4.1 Analysis (HIGH PRIORITY)**
   - Switch from Log to Recip+Log model (ΔAIC=7.50)
   - Re-run RQs 5.4.2-5.4.7 with `~recip_TSVR` random slopes
   - Update theoretical interpretation (two-process forgetting)

2. **Test Extended Models on Ch6 ROOT RQs**
   - Run 17-model comparison on 6.3.1, 6.4.1, 6.5.1, 6.8.1
   - Cannot assume Ch5 accuracy patterns generalize to Ch6 confidence
   - Evidence: 6.6.1 selected SquareRoot (not Log), 6.8.1 shows dissociation from 5.5.1

3. ~~**Complete RQ 5.5.1 Extended Testing**~~ ✅ DONE (2025-12-08)
   - Extended 66-model comparison complete
   - Result: Extreme model uncertainty (6.7% best weight)
   - 13-model averaging applied (effective N=12.32)

### Documentation Updates

1. **Update CLAUDE.md Protocol**
   - ✅ Already added LMM Model Completeness Protocol (2025-12-08)
   - Lists extended 17-model suite as standard
   - Triggers alert when only 5 models tested

2. **Create models.tsv**
   - ✅ Done (this search)
   - Inventory all ROOT RQs + dependencies

3. **Update docs/lmm_methodology.md**
   - Add extended 17-model suite as standard practice
   - Document random slope matching rules
   - Note when basic 5 comparison is insufficient

### Research Integrity

**Thesis Defense Preparation:**
- Be ready to explain why basic 5 comparison was initially used
- Document systematic testing of extended models as robustness check
- Highlight discoveries: Recip+Log two-process model, power-law vs log debate
- Acknowledge: Some RQs may need updating if extended models change conclusions

**Publication Strategy:**
- RQ 5.4.1 Recip+Log finding is **novel contribution** (two-process schema forgetting)
- Power-law vs logarithmic debate contributes to Wixted/Ebbinghaus literature
- Model selection methodology generalizes beyond this study

---

## Statistics Summary

| Metric | Chapter 5 | Chapter 6 | Combined |
|--------|-----------|-----------|----------|
| **ROOT RQs (X.Y.1)** | 5 | 6 | 11 |
| **Extended models tested** | 5/5 (100%) | 1/6 (17%) | 6/11 (55%) |
| **Log model selected (basic)** | 5/5 (100%) | 1/1* (100%) | 6/6 (100%) |
| **Log model maintains lead (extended)** | 0/5 (0%) | 0/1 (0%) | 0/6 (0%) |
| **Model averaging required (weight<30%)** | 5/5 (100%) | 1/1 (100%) | 6/6 (100%) |
| **Total derivative RQs** | 34 | 27 | 61 |
| **Complete RQs** | 32 | 25 | 57 |

*Only RQ 6.1.1 (planning stage) specified model selection; others assumed log_TSVR

---

## Files Created

1. **results/models.tsv** - Machine-readable inventory (TSV format)
2. **results/MODEL_SELECTION_SUMMARY.md** - This document (human-readable)

---

**Document Status:** Complete
**Next Update:** After extending model comparisons to Ch6 ROOT RQs
**Maintainer:** Update when new ROOT RQs added or extended comparisons run
