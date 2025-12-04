# Plots Style - 5.2.1 Publication Format

**Topic:** Trajectory plot formatting standard - individual scatter + CI bands + continuous TSVR
**Created:** 2025-12-05 (context-manager)
**Status:** Active

---

## Plot Style Fix - Match 5.2.1 Format with Individual Scatter (2025-12-05 09:30)

**Task:** Complete RQ 5.5.1 Production Execution + IRT Settings Fix + Plots Fix

**Context:** Fixed RQ 5.5.1 trajectory plots to match publication-quality 5.2.1 format. Original rq_plots agent used binned summary data (4 timepoints) instead of individual scatter points from 800 observations.

**Archived from:** state.md Session (2025-12-05 09:30)
**Original Date:** 2025-12-05 09:30
**Reason:** Session current (N), but plot formatting is orthogonal completed work

---

### Problem

**Original rq_plots output:** Used binned summary data from step07_summary_by_timebin.csv (4 rows = Day 0, 1, 3, 6)

**Issue:** Lost granularity, doesn't show individual variability, violates 5.2.1 publication standard

### Fix Applied - Complete Rewrite to 5.2.1 Style

**File:** `results/ch5/5.5.1/plots/plots.py` (complete rewrite)

**New Format (Publication Standard):**

1. **Faded scatter points** (alpha=0.15) from 800 individual observations
   - Source: `step07_individual_trajectories.csv` (800 rows: 400 composite_IDs × 2 LocationTypes)
   - Shows full data distribution, not just binned means
   - Faded to avoid overplotting, emphasize fitted curves

2. **Dashed fitted curves** from LMM predictions
   - Source: `step07_predicted_trajectories.csv` (200 rows: 100 timepoints × 2 LocationTypes)
   - Logarithmic model predictions from Step 5
   - Continuous trajectories (not 4 discrete points)

3. **95% CI bands** from fixed effects covariance matrix
   - Computed from LMM coefficients + covariance matrix
   - Shows uncertainty in population-level trajectories
   - Shaded region around fitted curves

4. **Continuous TSVR x-axis** (actual hours, not binned)
   - Range: [0, 360] hours (0 to 15 days)
   - Captures long retention intervals (some participants >7 days)
   - Not limited to nominal test days (0, 1, 3, 6)

### Code Example

```python
import pandas as pd
import matplotlib.pyplot as plt

# Load individual observations (800 rows)
df_individual = pd.read_csv('data/step07_individual_trajectories.csv')

# Load fitted predictions (200 rows)
df_predicted = pd.read_csv('data/step07_predicted_trajectories.csv')

# Plot individual scatter (faded)
for location in ['source', 'destination']:
    data = df_individual[df_individual['LocationType'] == location]
    plt.scatter(data['TSVR_hours'], data['theta'],
                alpha=0.15, s=20, label=f'{location} (observed)')

# Plot fitted curves (dashed) + CI bands
for location in ['source', 'destination']:
    pred = df_predicted[df_predicted['LocationType'] == location]
    plt.plot(pred['TSVR_hours'], pred['theta_pred'],
             linestyle='--', linewidth=2, label=f'{location} (fitted)')
    plt.fill_between(pred['TSVR_hours'],
                      pred['ci_lower'], pred['ci_upper'],
                      alpha=0.2)

plt.xlabel('Time Since VR (hours)')
plt.ylabel('Theta (IRT ability)')
plt.legend()
plt.savefig('plots/trajectory_theta.png', dpi=300)
```

### Dual-Scale Plots (Decision D069)

**Theta scale plot:** `trajectory_theta.png`
- Y-axis: [-0.8, 0.6] (IRT theta units)
- For psychometricians and statistical analysis

**Probability scale plot:** `trajectory_probability.png`
- Y-axis: [30%, 65%] (probability of correct response)
- For general audience and interpretability
- Transformation via logistic function with mean discrimination a=0.992

**Investigation: Why do they look identical?**
- Mean discrimination a=0.992 ≈ 1.0 (close to linear)
- Theta range: [-0.68, 0.49] (narrow, ~1.2 SDs)
- Probability range: [33.7%, 61.8%] (28 percentage points)
- **Logistic is nearly linear in this range** (correct behavior, not a bug)

### Files Created

**Plots:**
- `results/ch5/5.5.1/plots/trajectory_theta.png` (300 DPI)
- `results/ch5/5.5.1/plots/trajectory_probability.png` (300 DPI)

**Code:**
- `results/ch5/5.5.1/plots/plots.py` (complete rewrite, 200 lines)

### Validation

- ✅ rq_inspect: Step 7 file naming adapted (individual_trajectories.csv exists)
- ✅ rq_plots: 2 plots generated successfully
- ✅ Visual inspection: Matches 5.2.1 publication format exactly

### Standard Established

**All future trajectory plots must use:**
1. Individual scatter points (alpha=0.15) from step07_individual_trajectories.csv
2. Fitted curves (dashed) from step07_predicted_trajectories.csv
3. 95% CI bands from LMM covariance matrix
4. Continuous TSVR x-axis (not binned)
5. Dual-scale output (theta + probability) per D069
6. 300 DPI resolution for publication

**Template:** `results/ch5/5.5.1/plots/plots.py` serves as reference implementation

---
