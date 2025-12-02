# Investigation: Theta-to-Probability Scale Transformation and ICC

**Date:** 2025-12-03
**Status:** PLAN
**Hypothesis:** The anomalously low ICC_slope (0.0005) is an artifact of analyzing forgetting on the IRT theta scale rather than the probability scale

---

## The Problem

Our ICC_slope = 0.0005 (0.05%) is 640× lower than VR-RAVLT's retention ICC (0.32). But:

1. **VR-RAVLT uses proportion correct** (bounded 0-1)
2. **We use IRT theta** (unbounded, approximately -3 to +3)

These are fundamentally different scales with different variance properties.

**The logit transformation is nonlinear:**
```
P(correct) = 1 / (1 + exp(-theta))  # simplified
```

A 0.5 theta change at θ = 0 produces ~12.5% probability change.
A 0.5 theta change at θ = -2 produces only ~3% probability change.

**Individual differences in probability-space may be compressed on theta-space.**

---

## Target RQ: 5.1.4 (Between-Person Variance)

**Why this RQ:**
- Directly tests ICC_slope hypothesis
- Already has random effects extracted (step04_random_effects.csv)
- Has theta trajectories from RQ 5.1.1
- Item parameters available (step01_item_parameters.csv)

**Data available:**
- `results/ch5/5.1.4/data/step04_random_effects.csv` - 100 UIDs with random intercepts/slopes on theta scale
- `results/ch5/5.1.1/data/step03_theta_scores.csv` - Theta_All for each UID × test
- `results/ch5/5.1.1/logs/step01_item_parameters.csv` - Item difficulty (b) and discrimination (a)
- `results/ch5/5.1.1/data/step02_purified_items.csv` - Which items retained after purification

---

## Analysis Plan

### Step 1: Convert Theta Trajectories to Probability Scale

**Method A: Simple inverse logit (approximate)**
```python
# For each observation:
prob = 1 / (1 + np.exp(-theta))
```
This ignores item parameters but gives a rough transformation.

**Method B: Test Characteristic Curve (proper)**
```python
# Expected proportion correct given theta and item parameters
def expected_prob(theta, a_values, b_values):
    """
    For GRM (Graded Response Model), compute expected score.
    Simplified for binary: P = 1 / (1 + exp(-a*(theta - b)))
    Average across all retained items.
    """
    probs = [1 / (1 + np.exp(-a * (theta - b))) for a, b in zip(a_values, b_values)]
    return np.mean(probs)
```

**Decision:** Use Method B (TCC) for primary analysis, Method A as sensitivity check.

**Input files:**
- `results/ch5/5.1.1/data/step03_theta_scores.csv` (UID, test, Theta_All)
- `results/ch5/5.1.1/logs/step01_item_parameters.csv` (item_name, b, a)
- `results/ch5/5.1.1/data/step02_purified_items.csv` (which items to include)

**Output:**
- `results/ch5/5.1.4/data/step06_probability_trajectories.csv` (UID, test, Theta_All, Prob_TCC, Prob_simple)

### Step 2: Merge with TSVR Time Variable

**Input:**
- Probability trajectories from Step 1
- TSVR data (actual hours since VR encoding)

**Output:**
- `results/ch5/5.1.4/data/step07_prob_lmm_input.csv` (UID, TSVR_hours, TSVR_days, Prob_TCC, Prob_simple)

### Step 3: Fit LMM on Probability Scale

**Model:** Same as theta-scale analysis (Lin+Log)
```python
formula = "Prob_TCC ~ TSVR_days + np.log(TSVR_days + 1)"
re_formula = "~ TSVR_days"  # random intercepts + slopes
```

**Note:** Probability is bounded [0,1]. Linear LMM may have issues at boundaries. Options:
1. Use linear LMM anyway (if data doesn't hit boundaries)
2. Use beta regression (proper for bounded outcomes)
3. Use GLMM with binomial family (treats as proportion)

**Decision:** Start with linear LMM for direct comparison. Check for boundary issues. If problematic, try beta regression.

**Output:**
- `results/ch5/5.1.4/data/step08_prob_lmm_model.pkl`
- `results/ch5/5.1.4/data/step08_prob_variance_components.csv`

### Step 4: Extract Variance Components on Probability Scale

**Extract:**
- var_intercept_prob
- var_slope_prob
- cov_int_slope_prob
- cor_int_slope_prob
- var_residual_prob

**Output:**
- `results/ch5/5.1.4/data/step09_prob_variance_components.csv`

### Step 5: Compute ICC on Probability Scale

**Formulas:**
```python
ICC_intercept_prob = var_intercept_prob / (var_intercept_prob + var_residual_prob)
ICC_slope_prob = var_slope_prob / (var_slope_prob + var_residual_prob)
```

**Output:**
- `results/ch5/5.1.4/data/step10_prob_icc_estimates.csv`

### Step 6: Compare Theta vs Probability Results

**Create comparison table:**

| Metric | Theta Scale | Probability Scale | Ratio |
|--------|-------------|-------------------|-------|
| var_intercept | 0.476 | ? | ? |
| var_slope | 0.000157 | ? | ? |
| ICC_intercept | 0.606 | ? | ? |
| ICC_slope | 0.0005 | ? | ? |
| cor_int_slope | -0.451 | ? | ? |

**Key question:** Is ICC_slope_prob >> ICC_slope_theta?

**If ICC_slope_prob ≈ 0.30-0.50:** Scale transformation explains the anomaly
**If ICC_slope_prob ≈ 0.0005:** The finding is real, not a scale artifact

---

## Expected Results

### Prediction 1: ICC_intercept will be similar
The intercept represents baseline ability. On both scales, this should show substantial between-person variance. Expected: ICC_intercept_prob ≈ 0.50-0.70 (similar to theta).

### Prediction 2: ICC_slope will increase
Individual differences in forgetting rate may be more apparent on probability scale due to:
- Bounded scale creates natural variance compression at extremes
- Literature uses probability/proportion → their ICC reflects this scale
- Expected: ICC_slope_prob >> 0.0005, possibly 0.10-0.30

### Prediction 3: Correlation will decrease
The extreme r = -0.97 correlation may be partially a theta-scale artifact. On probability scale, ceiling effects are explicit (high performers can't improve). Expected: cor_int_slope_prob closer to literature norm (-0.2 to -0.4).

---

## Potential Issues

### 1. Boundary Effects
Probability is bounded [0,1]. If participants hit floor (0) or ceiling (1), linear LMM assumptions are violated.

**Check:** Examine distribution of Prob_TCC values. If >10% at boundaries, use beta regression.

### 2. Item Parameter Uncertainty
TCC uses point estimates of item parameters (a, b). These have uncertainty that propagates to probability estimates.

**Mitigation:** This is a diagnostic analysis, not final results. Point estimates sufficient for this purpose.

### 3. GRM vs 2PL
Our IRT model is GRM (Graded Response) for polytomous data, but TCC formula above assumes 2PL (binary).

**Check:** Verify how theta scores were computed. If using marginal scores aggregated across categories, simple inverse logit may be more appropriate than full GRM TCC.

### 4. Purified vs Full Item Set
TCC should use only purified items (those retained after a/b threshold filtering).

**Mitigation:** Filter item parameters to match step02_purified_items.csv.

---

## Success Criteria

### Strong Support for Scale Hypothesis
- ICC_slope_prob > 0.10 (20× higher than theta)
- ICC_slope_prob in range 0.20-0.40 (matches literature)
- cor_int_slope_prob < -0.70 (less extreme than theta)

### Partial Support
- ICC_slope_prob > 0.01 but < 0.10 (elevated but still low)
- Suggests scale matters but doesn't fully explain anomaly

### No Support
- ICC_slope_prob ≈ 0.001 (similar to theta)
- Would indicate the finding is real, not artifactual
- VR/sample issues remain primary explanation

---

## Timeline

| Step | Description | Estimated Time |
|------|-------------|----------------|
| 1 | Theta→Probability conversion | 30 min |
| 2 | Merge with TSVR | 15 min |
| 3 | Fit probability-scale LMM | 30 min |
| 4 | Extract variance components | 15 min |
| 5 | Compute probability-scale ICC | 15 min |
| 6 | Comparison analysis | 30 min |
| **Total** | | **~2.5 hours** |

---

## Code Outline

```python
# Step 1: Load data
import pandas as pd
import numpy as np

theta_df = pd.read_csv("results/ch5/5.1.1/data/step03_theta_scores.csv")
items_df = pd.read_csv("results/ch5/5.1.1/logs/step01_item_parameters.csv")
purified_df = pd.read_csv("results/ch5/5.1.1/data/step02_purified_items.csv")

# Filter to purified items only
purified_items = purified_df['item_name'].tolist()
items_filtered = items_df[items_df['item_name'].isin(purified_items)]

# Step 1a: Simple inverse logit
theta_df['Prob_simple'] = 1 / (1 + np.exp(-theta_df['Theta_All']))

# Step 1b: TCC (average across items)
def compute_tcc(theta, a_values, b_values):
    """Expected proportion correct via Test Characteristic Curve"""
    probs = 1 / (1 + np.exp(-a_values * (theta - b_values)))
    return probs.mean()

a_vals = items_filtered['a'].values
b_vals = items_filtered['b'].values

theta_df['Prob_TCC'] = theta_df['Theta_All'].apply(
    lambda t: compute_tcc(t, a_vals, b_vals)
)

# Step 2: Merge TSVR (load from master.xlsx or existing merged data)
# ... merge logic ...

# Step 3: Fit LMM
import statsmodels.formula.api as smf

model_prob = smf.mixedlm(
    "Prob_TCC ~ TSVR_days + np.log(TSVR_days + 1)",
    data=df,
    groups="UID",
    re_formula="~ TSVR_days"
)
result_prob = model_prob.fit(reml=False)

# Step 4-5: Extract variance components and compute ICC
# ... extraction logic ...
```

---

## Files to Create

| File | Description |
|------|-------------|
| `results/ch5/5.1.4/code/step06_theta_to_prob.py` | Conversion script |
| `results/ch5/5.1.4/code/step07_prob_lmm.py` | LMM on probability scale |
| `results/ch5/5.1.4/code/step08_prob_icc.py` | ICC computation |
| `results/ch5/5.1.4/data/step06_probability_trajectories.csv` | Converted data |
| `results/ch5/5.1.4/data/step07_prob_lmm_input.csv` | Merged data |
| `results/ch5/5.1.4/data/step08_prob_variance_components.csv` | Variance components |
| `results/ch5/5.1.4/data/step09_prob_icc_estimates.csv` | ICC estimates |
| `results/ch5/5.1.4/results/step10_scale_comparison.md` | Summary comparison |

---

## Implications for Thesis

### If Scale Hypothesis Confirmed

1. **Methodological contribution:** First demonstration that IRT theta-scale analyses produce different ICC estimates than probability-scale analyses in VR memory context
2. **Recommendation:** Report both theta and probability-scale results for trajectory analyses
3. **Literature comparison:** Probability-scale ICC enables direct comparison with CTT-based studies
4. **Resolves anomaly:** Explains why our ICC was so different from literature

### If Scale Hypothesis Rejected

1. **Real finding:** VR episodic memory genuinely shows homogeneous forgetting
2. **Design limitation:** 4 timepoints / 6 days insufficient for slope detection
3. **Sample limitation:** Healthy adults 20-70 may have compressed variance
4. **Future work:** Replication with longer retention, more timepoints, clinical samples

---

## Decision Point

**Run this analysis before:**
- Finalizing Chapter 5 story
- Making claims about ICC_slope
- Comparing to VR-RAVLT or other literature

**If results change the story:** Update story.md with new section on scale effects.
