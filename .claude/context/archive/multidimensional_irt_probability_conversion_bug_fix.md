# Multi-Dimensional IRT Probability Conversion Bug Fix

**Topic:** multidimensional_irt_probability_conversion_bug_fix
**Created:** 2025-12-05 (context-manager archival)
**Description:** Critical bug discovery and fix for multi-dimensional IRT models requiring factor-specific item difficulties when converting theta to probability scale.

---

## Multi-Dimensional IRT Scale Mismatch - Factor-Specific Difficulty Required (2025-12-05 12:30)

**Archived from:** state.md Session (2025-12-05 12:30)
**Original Date:** 2025-12-05 12:30
**Reason:** Completed investigation and bug fix, agent updated

### Root Cause Discovery

The 2-dimensional IRT model (source vs destination) creates TWO SEPARATE THETA SCALES:

| Factor | Items | Mean Difficulty (b) | Theta=0 means |
|--------|-------|---------------------|---------------|
| Source | 17 items | **-0.453** (easy) | ~65% accuracy |
| Destination | 15 items | **+1.371** (hard) | ~25% accuracy |

**The Problem:**
- Theta_source and theta_destination are NOT comparable because they're calibrated to different item difficulties
- Mean thetas are nearly identical (-0.02 vs +0.02) because IRT anchors each dimension to mean=0
- The 1.82 theta unit difficulty difference is absorbed into item parameters, invisible in theta

**Raw Accuracy Verification:**
| Test | Source Accuracy | Dest Accuracy | Difference |
|------|-----------------|---------------|------------|
| Day 0 | 69.4% | 41.4% | **28.0%** |
| Day 1 | 63.4% | 33.5% | **29.9%** |
| Day 3 | 54.7% | 29.6% | **25.1%** |
| Day 6 | 45.7% | 26.4% | **19.3%** |

This is a MASSIVE effect (~25-30 percentage points) that the LMM cannot detect when comparing raw thetas!

### Bug Fix: Factor-Specific Probability Conversion

**The Error (in original plots.py):**
```python
# WRONG: Using difficulty=0.0 for all factors
probability = convert_theta_to_probability(theta, discrimination=mean_a, difficulty=0.0)
```

**The Fix (now applied):**
```python
# CORRECT: Use factor-specific item difficulty
FACTOR_PARAMS = {
    'source': {'discrimination': 1.096, 'difficulty': -0.453},
    'destination': {'discrimination': 0.873, 'difficulty': +1.371}
}

for loc_type in df['LocationType'].unique():
    params = FACTOR_PARAMS[loc_type]
    df.loc[mask, 'probability'] = convert_theta_to_probability(
        df.loc[mask, 'theta'].values,
        discrimination=params['discrimination'],
        difficulty=params['difficulty']  # FACTOR-SPECIFIC!
    )
```

**Result After Fix:**
- Source: 43.8% - 73.4% probability range
- Destination: 16.9% - 29.6% probability range
- **30-45 percentage point difference now visible!**

### v1 Analysis Pattern Discovery

Examined `.archive/v1/plots.py` lines 543-561 which shows the CORRECT pattern:
```python
# v1 code correctly uses factor-specific difficulty
regex = '|'.join(groups[factor])
factor_items = df_items[df_items.index.str.contains(regex)]
avg_difficulty = acceptable_items['Difficulty'].mean()  # FACTOR-SPECIFIC!

def to_prob(theta):
    logit = avg_discrimination * (theta - avg_difficulty)  # Uses factor b!
    return 1 / (1 + np.exp(-logit))
```

This is why user's previous analyses showed significant intercept difference!

### Files Modified

- results/ch5/5.5.1/plots/plots.py (factor-specific probability conversion)

**Key Lesson:** Multi-dimensional IRT models create separate theta scales per factor. Factor-specific item difficulties MUST be used when converting to probability, otherwise baseline accuracy differences are completely masked.

---
