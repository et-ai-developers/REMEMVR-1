# GRM Probability Transformation Bug Fix - CRITICAL CORRECTION

## Session (2025-12-11 23:15) - GRM Probability Bug Fix

**Archived from:** state.md
**Original Date:** 2025-12-11 23:15
**Reason:** Session now 3+ sessions old, archiving per standard curation policy

---

**Task:** GRM Probability Transformation Bug Fix - CRITICAL CORRECTION to Ch6 Trajectory Plots

**Context:** User identified that RQ 6.4.1 probability plot looked wrong (values hugging floor at 2-20%). Investigation revealed systematic bug in all Ch6 GRM confidence RQs using `b=0.0` for theta-to-probability transformation.

**Major Accomplishment: FIXED GRM Probability Transformation in 4 RQs**

### 1. Bug Diagnosis

**Problem Identified:**
- RQ 6.4.1 probability plot showed values in 2-20% range (hugging the floor)
- Y-axis 0-1 made trajectories appear compressed at bottom
- User correctly identified this as incorrect

**Root Cause Analysis:**
- Ch6 uses GRM (Graded Response Model) for 5-level ordinal confidence (not 2PL binary)
- GRM theta is systematically negative (mean ≈ -0.78) because participants use middle/lower confidence categories
- Ch5 2PL accuracy theta naturally centers at 0 (mean theta ≈ 0.006)
- Step 07 scripts used `b = 0.0` (assumed centered scale) for 2PL probability transformation
- With negative theta and b=0: `P = 1/(1+exp(-a*θ))` → very low probabilities

**Comparison:**
| Chapter | Model | Mean Theta | Theta Crosses Zero | b=0 Valid? |
|---------|-------|------------|-------------------|------------|
| Ch5 | 2PL (binary accuracy) | +0.006 | Yes | ✅ YES |
| Ch6 | GRM (ordinal confidence) | -0.78 | No (all negative) | ❌ NO |

### 2. Statistical Solution: EAP Normalization

**Fix Applied:**
- Changed `b = 0.0` to `b = sample_mean_theta` (EAP normalization)
- Standard statistical practice when theta distributions differ from assumed N(0,1)
- Produces interpretable probabilities representing "probability relative to average participant"

**Code Change (in all 4 step07 files):**
```python
# BEFORE (wrong):
b = 0.0  # Centered scale (theta mean = 0)

# AFTER (correct):
sample_mean_theta = theta_data['theta'].mean()
b = sample_mean_theta  # EAP normalization
```

### 3. Files Modified and Results

**4 RQ step07 scripts fixed:**
1. `results/ch6/6.3.1/code/step07_prepare_trajectory_plot_data.py`
2. `results/ch6/6.4.1/code/step07_prepare_trajectory_plot_data.py`
3. `results/ch6/6.5.1/code/step07_prepare_trajectory_plot_data.py`
4. `results/ch6/6.8.1/code/step07_prepare_trajectory_plot_data.py`

**Before vs After Probability Ranges:**

| RQ | Before (b=0) | After (b=mean_theta) | Improvement |
|----|--------------|----------------------|-------------|
| 6.3.1 | 2-20% | 25-79% | ✅ Sensible |
| 6.4.1 | 2-20% | 25-75% | ✅ Sensible |
| 6.5.1 | 2-20% | 24-77% | ✅ Sensible |
| 6.8.1 | 2-20% | 29-75% | ✅ Sensible |

**All 4 plots regenerated with corrected probability scales.**

### 4. Documentation Update

**Lesson added to `results/ch6/execute.md` (Section: "GRM Probability Transformation Lessons"):**
- Bug description: `b=0.0` used for GRM data
- Symptom: Probabilities hugging floor (2-20%)
- Root cause: GRM theta systematically negative (mean ≈ -0.78)
- Fix: Use `b = sample_mean_theta` (EAP normalization)
- Files fixed: All 4 step07 scripts listed
- Statistical justification: EAP normalization standard practice
- Future prevention: ALWAYS use sample mean theta for GRM confidence probability centering

### 5. Connection to Prior Knowledge

**context_finder Search Results:**
- Found CRITICAL prior bug fix (2025-12-05): Multi-dimensional IRT probability conversion
- RQ 5.5.1 had similar issue: Using b=0 masked 30-45 percentage point effect
- Decision D069: Dual-scale plots required (theta + probability)
- GRM-2PL mismatch already noted in RQ 6.3.1 validation.md

**Pattern Recognition:**
- This is the SECOND instance of b=0 causing problems
- Ch5 5.5.1: Factor-specific b needed for multi-dimensional IRT
- Ch6: Sample mean theta needed for GRM ordinal data
- **GENERAL RULE:** Never assume b=0 without checking theta distribution

### 6. Session Metrics

**Session Duration:** ~30 minutes
**Tokens Used:** ~15k
**Files Modified:** 5 (4 step07 scripts + execute.md)
**Plots Regenerated:** 8 (4 RQs × 2 plots each)
**Bug Severity:** HIGH (visual misrepresentation of results)

### 7. Active Topics

- grm_probability_transformation_bug_fix_critical (Session 2025-12-11 23:15: b_equals_zero_wrong_for_grm, sample_mean_theta_eap_normalization, 4_rqs_fixed_6.3.1_6.4.1_6.5.1_6.8.1, probability_range_corrected_2_20_to_25_80)

- ch6_probability_plots_floor_effect_resolved (Session 2025-12-11 23:15: grm_theta_systematically_negative_mean_neg_0.78, ch5_2pl_theta_centers_zero, b_equals_mean_theta_standard_practice)

- lesson_never_assume_b_zero (Session 2025-12-11 23:15: second_instance_after_5.5.1, general_rule_check_theta_distribution_first, factor_specific_or_sample_mean_required)

**Relevant Archived Topics:**
- multidimensional_irt_probability_conversion_bug_fix (prior factor-specific b fix)
- ch6_validation_workflow_complete_four_root_rqs_thesis_ready (original execution)
- rq_plots_agent_v4.0.1_update (agent guidance updated for multi-dim IRT)

**End of Session (2025-12-11 23:15)**

**Status:** ✅ **GRM PROBABILITY BUG FIXED - 4 RQs Corrected - Plots Regenerated**

Critical bug in Ch6 probability plots identified and fixed. GRM ordinal confidence theta is systematically negative (mean ≈ -0.78), causing b=0 transformation to produce misleadingly low probabilities (2-20%). Solution: Use b=sample_mean_theta (EAP normalization) for interpretable probabilities (25-80%). All 4 affected RQs (6.3.1, 6.4.1, 6.5.1, 6.8.1) corrected, plots regenerated, lesson documented in execute.md.

**Next Actions:** Execute remaining ROOT RQs (6.6.1 HCE, 6.7.2 Variability)

---
