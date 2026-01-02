# Parallel Ch7 RQ Fixing Strategy

## Quick Wins First (Minor issues, 8.5-8.9)
These might pass with minimal fixes:
- 7.5.1 (8.6): Add cross-validation + power analysis
- 7.3.2 (8.7): Add remedial actions + bootstrap specs
- 7.6.2 (8.8): Add power analysis + linearity tests  
- 7.8.2 (8.8): Minor parameter justification

## Critical Issues (5.8-7.9)
These need substantial work:
- 7.3.5 (5.8): Major issues - missing assumption testing, poor parameters
- 7.5.3 (7.4): Text coding issues, missing parameters
- 7.6.1 (7.4): Major tool gaps, validation issues
- 7.6.3 (7.6): Bootstrap tools missing
- 7.3.1 (7.8): Tool gaps in regression
- 7.8.4 (7.9): Missing critical tools, validation gaps

## Common Fix Template
For each concept.md, add these sections:

### Power Analysis (add to Analysis Approach)
```
**Power Analysis:**
- Sample size: N=100 with k=[number] predictors
- Power for detecting medium effects (f²=0.15): 80% power
- Minimum detectable effect: f²=0.10 with current sample
- Acknowledge limitation for small effects (f²<0.10)
```

### Cross-Validation (add as new step)
```
**Step X: Cross-validation**
- Implement 5-fold CV (seed=42) to assess generalization
- Report mean CV-R² and SD across folds
- Compare to full-sample R² (gap should be <0.10)
- If gap >0.10: Consider regularization or simpler model
```

### Remedial Actions (add to each assumption test)
```
If [assumption] violated:
- Normality: Use robust standard errors (HC3) or bootstrap
- Homoscedasticity: White's heteroscedasticity-consistent SEs
- Linearity: Consider polynomial terms or transformations
- Multicollinearity: Ridge regression or drop predictors
- Outliers: Report with/without influential points
```

### Bootstrap Specifications
```
- Method: Participant-level block bootstrap
- Replications: 1000 (seed=42)
- CI method: Percentile (2.5%, 97.5%)
- Purpose: Robust inference for non-normal distributions
```

## Batch Execution Commands

### Step 1: Delete all failed plans
```bash
rm results/ch7/{7.3.5,7.5.3,7.6.1,7.6.3,7.3.1,7.8.4,7.4.2,7.1.4,7.1.1,7.7.2,7.4.3,7.2.3,7.5.1,7.3.2,7.6.2,7.8.2}/docs/2_plan.md 2>/dev/null
```

### Step 2: Process in parallel batches
- BATCH 1: Fix 7.5.1, 7.3.2, 7.6.2, 7.8.2 (minor issues)
- BATCH 2: Fix 7.3.5, 7.5.3, 7.6.1 (critical issues)
- BATCH 3: Fix remaining moderate issues

### Step 3: Re-validate in parallel
Run rq_stats on all fixed RQs simultaneously

### Step 4: Run planners for passing RQs
Only create plans for RQs with score ≥9.0