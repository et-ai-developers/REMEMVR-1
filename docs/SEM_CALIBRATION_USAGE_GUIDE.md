# SEM Calibration Usage Guide

**Version:** 1.0.0
**Created:** 2025-12-28
**Purpose:** Guide for applying SEM calibration to REMEMVR thesis RQs

---

## Quick Start

### Basic Usage

```python
from tools.sem_calibration import quick_sem_calibration

# Run complete SEM analysis with defaults
sem = quick_sem_calibration(
    theta_accuracy_file='results/ch5/5.X.1/data/step03_theta_scores.csv',
    theta_confidence_file='results/ch6/6.X.1/data/step03_theta_scores.csv',
    output_dir='results/ch6/6.X.2/data/sem/'
)

# Latent calibration scores now available
latent_calib = sem.get_latent_calibration('difference')
```

### Advanced Usage

```python
from tools.sem_calibration import SEMCalibration

# Initialize with explicit measurement error
sem = SEMCalibration(
    theta_accuracy='path/to/accuracy.csv',
    theta_confidence='path/to/confidence.csv',
    measurement_error_acc='path/to/se_accuracy.csv',  # IRT standard errors
    measurement_error_conf='path/to/se_confidence.csv',
    id_vars=['UID', 'test', 'domain']  # For domain-stratified analyses
)

# Fit both models
fit_stats_diff = sem.fit_latent_difference()
fit_stats_resid = sem.fit_residualized()

# Compare approaches
comparison = sem.compare_approaches()
print(comparison)

# Get latent scores
latent_diff = sem.get_latent_calibration('difference')
latent_resid = sem.get_latent_calibration('residualized')

# Check validation stats
print(sem.validation_stats)

# Save all results
sem.save_results('output/directory/', prefix='rq_6.2.2')
```

---

## For Each RQ: Step-by-Step Workflow

### Step 1: Identify Data Sources

**Check RQ concept document (docs/1_concept.md):**
- Which RQ provides `theta_accuracy`? (usually Ch5 X.X.1)
- Which RQ provides `theta_confidence`? (usually Ch6 X.X.1)
- What are the ID variables? (`['UID', 'test']` or `['UID', 'test', 'domain']` etc.)

**Example for RQ 6.2.2:**
```yaml
Accuracy source: results/ch5/5.1.1/data/step03_theta_scores.csv
Confidence source: results/ch6/6.1.1/data/step05b_model_averaged_theta.csv
ID variables: ['UID', 'test']
```

### Step 2: Check for Measurement Error Files

**Look for IRT standard error files:**
```python
# Option 1: Test information (preferred)
# Usually: data/irt_test_information.csv or similar

# Option 2: Standard errors per observation
# Usually: data/theta_scores.csv with 'se' column

# Option 3: Use reliability estimate
# From validation.md or IRT model summary
# Typical IRT reliability: 0.75-0.90
```

**If not available:**
```python
# Use conservative reliability estimate
reliability_acc = 0.75  # Conservative for IRT
reliability_conf = 0.75
```

### Step 3: Run SEM Analysis

**Template script for each RQ:**
```python
#!/usr/bin/env python3
"""
SEM Calibration for RQ X.X.X

Upgrades from naive difference scores to latent variable approach.
"""

from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from tools.sem_calibration import SEMCalibration

# Paths
RQ_DIR = Path(__file__).parent.parent
ACC_FILE = Path('results/ch5/X.X.1/data/step03_theta_scores.csv')
CONF_FILE = Path('results/ch6/X.X.1/data/step03_theta_scores.csv')
OUTPUT_DIR = RQ_DIR / 'data' / 'sem'

# Initialize SEM
sem = SEMCalibration(
    theta_accuracy=ACC_FILE,
    theta_confidence=CONF_FILE,
    reliability_acc=0.75,  # Adjust based on IRT validation
    reliability_conf=0.75,
    id_vars=['UID', 'test']  # Adjust for domain/paradigm RQs
)

# Fit models
print("Fitting latent difference model...")
fit_diff = sem.fit_latent_difference()

print("Fitting residualized model...")
fit_resid = sem.fit_residualized()

# Compare
print("\nComparing approaches:")
print(sem.compare_approaches())

# Save results
print(f"\nSaving to {OUTPUT_DIR}...")
sem.save_results(OUTPUT_DIR, prefix='sem_calibration')

print("\n✓ SEM calibration complete")
```

### Step 4: Update Analysis to Use SEM Scores

**Replace old calibration computation:**

**BEFORE (naive difference):**
```python
# OLD - unreliable
calibration = theta_confidence - theta_accuracy
```

**AFTER (SEM latent scores):**
```python
# NEW - accounts for measurement error
import pandas as pd

# Load SEM results
sem_data = pd.read_csv('data/sem/sem_calibration_scores.csv')

# Merge with analysis data
lmm_data = pd.merge(
    lmm_data,
    sem_data[['UID', 'test', 'latent_calibration']],
    on=['UID', 'test']
)

# Use latent calibration in models
# calibration = lmm_data['latent_calibration']
```

**Update LMM formula:**
```python
# Before
# model = 'naive_calibration ~ Time + (Time | UID)'

# After
model = 'latent_calibration ~ Time + (Time | UID)'
```

### Step 5: Compare Results (Before vs After)

**Create comparison table:**
```python
import pandas as pd

# Re-run analysis with SEM scores
# ... (fit new LMM)

# Compare
comparison = pd.DataFrame({
    'Approach': ['Naive Difference', 'SEM Latent'],
    'Beta': [beta_naive, beta_sem],
    'SE': [se_naive, se_sem],
    'p_value': [p_naive, p_sem],
    'Conclusion': [conclusion_naive, conclusion_sem]
})

comparison.to_csv('results/sem_comparison.csv', index=False)
```

### Step 6: Update Documentation

**Update results/summary.md:**
```markdown
## Methodology Upgrade (2025-12-28)

**Previous approach:** Simple difference scores (calibration = confidence - accuracy)

**Issue:** Difference score reliability r_diff = X.XX (below 0.70 threshold)
- Caused by: High correlation (r=X.XX) + moderate reliability → reliability collapse
- Formula: r_diff = (r_xx + r_yy - 2*r_xy) / (2 - 2*r_xy)

**New approach:** Structural Equation Modeling (SEM) with latent variables
- Models measurement error in both accuracy and confidence
- Latent calibration = error-free difference
- Model fit: CFI=X.XX, RMSEA=X.XX, SRMR=X.XX

**Impact on findings:**
- Beta (naive): X.XX (SE=X.XX, p=X.XX)
- Beta (SEM): X.XX (SE=X.XX, p=X.XX)
- Conclusion: [Same/Changed/Strengthened]
```

**Update results/validation.md:**
```markdown
### Layer X: SEM Calibration Validation (2025-12-28)

**Method:** Latent difference score SEM

**Model Specification:**
```
eta_acc =~ 1*theta_accuracy
eta_conf =~ 1*theta_confidence
theta_accuracy ~~ sigma2_acc*theta_accuracy
theta_confidence ~~ sigma2_conf*theta_confidence
eta_calibration := eta_conf - eta_acc
```

**Model Fit:**
- CFI = X.XX (criterion: ≥0.95) → [PASS/FAIL]
- RMSEA = X.XX (criterion: <0.06) → [PASS/FAIL]
- SRMR = X.XX (criterion: <0.08) → [PASS/FAIL]

**Validation Stats:**
- Naive r_diff: X.XX (before SEM)
- Latent calibration reliability: X.XX (estimated)
- Convergence: [YES/NO]

**Comparison:**
- Correlation (naive vs latent): r=X.XX
- Mean difference: X.XX
- Conclusion changed: [YES/NO]
```

---

## Troubleshooting

### Issue 1: SEM Fails to Converge

**Symptoms:**
```
semopy.exceptions.NotConvergedError: Model did not converge
```

**Solution:**
```python
# Toolkit automatically falls back to factor score regression
# Check log for:
#   "Using fallback: Factor score regression method"

# This uses empirical Bayes shrinkage:
#   eta = grand_mean + reliability * (theta - grand_mean)

# Should still produce valid results, just without full SEM fit indices
```

### Issue 2: Perfect/Near-Perfect Correlation

**Symptoms:**
```
r_xy = 0.99, difference score reliability undefined
```

**Solution:**
```python
# Use residualized approach instead
sem.fit_residualized()
residual_calib = sem.get_latent_calibration('residualized')

# This avoids the difference score entirely
# Calibration = residual from: confidence ~ accuracy
```

### Issue 3: Measurement Error Not Available

**Symptoms:**
```
No IRT test information files found
```

**Solution:**
```python
# Use reliability estimates from validation reports
# Check results/validation.md for IRT reliability

sem = SEMCalibration(
    theta_accuracy='...',
    theta_confidence='...',
    reliability_acc=0.80,  # From IRT validation
    reliability_conf=0.75,
    # measurement_error files not needed when reliability provided
)
```

### Issue 4: Merge Failure

**Symptoms:**
```
ValueError: Merge produced 0 rows
```

**Solution:**
```python
# Check ID variables match between files
# Common issues:
#   - 'TEST' vs 'test'
#   - 'domain' vs 'Domain'
#   - Missing timepoints

# Solution: Specify id_vars explicitly
sem = SEMCalibration(
    ...,
    id_vars=['UID', 'test']  # Adjust to match your data
)

# Or check source files:
import pandas as pd
df_acc = pd.read_csv('accuracy.csv')
df_conf = pd.read_csv('confidence.csv')
print(df_acc.columns)
print(df_conf.columns)
```

### Issue 5: Negative Latent Calibration Reliability

**Symptoms:**
```
Estimated latent calibration reliability: -0.15
```

**This is expected** when naive r_diff < 0. The SEM approach FIXES this by:
1. Properly modeling measurement error
2. Extracting latent scores (error-free)
3. Computing difference at latent level

**Validation:**
- Check that SEM model converged (CFI, RMSEA)
- Compare naive vs SEM results
- SEM should give HIGHER precision (narrower CIs, better power)

---

## Domain/Paradigm-Stratified Analyses

**For RQs with domain or paradigm stratification:**

### Example: RQ 6.3.2 (Domain Calibration)

```python
# Domain-stratified RQs have 3× observations
# UID × test × domain (1200 rows instead of 400)

sem = SEMCalibration(
    theta_accuracy='results/ch5/5.2.1/data/step03_theta_domain.csv',
    theta_confidence='results/ch6/6.3.1/data/step03_theta_domain.csv',
    id_vars=['UID', 'test', 'domain'],  # Add 'domain' to ID vars
    reliability_acc=0.75,
    reliability_conf=0.75
)

# Fit models (same as before)
sem.fit_latent_difference()

# Extract scores (now have domain column)
sem.save_results('data/sem/')

# Load for LMM
sem_data = pd.read_csv('data/sem/sem_calibration_scores.csv')
# Now has: UID, test, domain, latent_calibration

# LMM with domain effects
# Calibration ~ Domain × Time + (Time | UID)
```

---

## Batch Processing

**For processing multiple RQs:**

```python
# tools/batch_sem_calibration.py

from pathlib import Path
from tools.sem_calibration import quick_sem_calibration

# Define RQs to process
rqs = [
    ('6.2.2', 'results/ch5/5.1.1', 'results/ch6/6.1.1'),
    ('6.3.2', 'results/ch5/5.2.1', 'results/ch6/6.3.1'),
    ('6.4.2', 'results/ch5/5.3.1', 'results/ch6/6.4.1'),
    # ... add more
]

for rq_id, acc_path, conf_path in rqs:
    print(f"\nProcessing RQ {rq_id}...")

    try:
        sem = quick_sem_calibration(
            theta_accuracy_file=f'{acc_path}/data/step03_theta_scores.csv',
            theta_confidence_file=f'{conf_path}/data/step03_theta_scores.csv',
            output_dir=f'results/ch6/{rq_id}/data/sem/',
            reliability_acc=0.75,  # Adjust per RQ
            reliability_conf=0.75
        )

        print(f"  ✓ RQ {rq_id} complete")

    except Exception as e:
        print(f"  ✗ RQ {rq_id} failed: {e}")
```

---

## References

**Methodological:**
- McArdle, J.J. (2009). Latent variable modeling of differences and changes with longitudinal data. *Annual Review of Psychology*, 60, 577-605.
- Cole, D.A., & Maxwell, S.E. (2003). Testing mediational models with longitudinal data: Questions and tips in the use of structural equation modeling. *Journal of Abnormal Psychology*, 112(4), 558.

**Difference Score Reliability:**
- Rogosa, D., & Willett, J.B. (1983). Demonstrating the reliability of the difference score in the measurement of change. *Journal of Educational Measurement*, 20(4), 335-343.
- Williams, R.H., & Zimmerman, D.W. (1996). Are simple gain scores obsolete? *Applied Psychological Measurement*, 20(1), 59-69.

**Lord's Paradox:**
- Lord, F.M. (1967). A paradox in the interpretation of group comparisons. *Psychological Bulletin*, 68(5), 304.
- Tennant, P.W., et al. (2023). Use of directed acyclic graphs (DAGs) in applied health research: review and recommendations. *International Journal of Epidemiology*, 52(2), 620-632.

---

**End of Usage Guide**
