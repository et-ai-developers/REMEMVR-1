# REMEMVR STATISTICAL ANALYSIS BIBLE

**Version:** 2.0 DEFINITIVE
**Date:** 2025-11-01
**Status:** 🔒 LOCKED - Implementation Ready
**Purpose:** Complete, unambiguous specification for Chapters 5, 6, and 7

**CRITICAL:** This document has ZERO ambiguity. Every RQ has complete executable specifications.

---

## DOCUMENT CONVENTIONS

### ✅ **Completeness Standard**

Every Research Question (RQ) contains ALL 8 elements:

1. **Research Question** - Clear, answerable question
2. **Hypothesis** - Directional or exploratory prediction with theoretical grounding
3. **Data Required** - Exact files, variables, preprocessing steps
4. **Analysis Recipe** - Numbered steps with complete executable code
5. **Statistical Justification** - Why this method? Theoretical/methodological rationale
6. **Expected Output** - Exact tables, plots, statements with column specifications
7. **Success Criteria** - How to verify analysis completed correctly (diagnostics)
8. **Reviewer Rebuttals** - Anticipated objections with preemptive responses

### 📊 **Statistical Approach**

- **Philosophy:** Exploratory (not preregistered), framework-agnostic, data-driven
- **Sample:** N=100 participants, all included unless explicitly stated
- **Software:** Python 3.10+ (deepirtools, statsmodels, scipy, numpy, pandas)
- **Reproducibility:** Fixed seed (42), version-controlled code, saved models

---

## PART 0: GLOBAL SPECIFICATIONS

All analyses share these foundational specifications. Read this section FIRST.

---

### 0.1 IRT PIPELINE SPECIFICATION (TQ_ and TC_)

**CRITICAL:** Both TQ_ (accuracy) and TC_ (confidence) undergo IDENTICAL IRT processing.

#### 0.1.1 Input Data

**TQ_ (Accuracy):**
- Format: Long-form CSV (rows = Composite_ID × Item)
- Scoring: Dichotomous (0 or 1, NO partial credit)
- Source: `results/{set}/TQ_corr_noroom_2cats_data.csv`

**TC_ (Confidence):**
- Format: Long-form CSV (rows = Composite_ID × Item)
- Scoring: 5-category (0.0, 0.25, 0.5, 0.75, 1.0 rescaled from 1-5 Likert)
- Source: `results/{set}/TC_corr_noroom_5cats_data.csv`

#### 0.1.2 Q-Matrix (Factor Structure)

**Confirmatory Factor Analysis:** Items load on predefined factors based on analysis set.

**Example (All by Domain):**
```python
# Q-matrix specification
q_matrix = {
    'What': [item for item in items if '-N-' in item],  # Object identity
    'Where': [item for item in items if ('-U-' in item or '-D-' in item)],  # Spatial
    'When': [item for item in items if '-O-' in item]  # Temporal
}

# Factor correlation structure
correlated = True  # Primary analysis (oblique rotation)
# correlated = False  # Sensitivity analysis (orthogonal rotation)
```

**Critical:** TC_ uses IDENTICAL Q-matrix structure as corresponding TQ_ analysis.

#### 0.1.2.1 Correlated vs Uncorrelated Factors: Theoretical Justification

**PRIMARY MODEL:** Correlated factors (`correlated=True`)

**Rationale:**
1. **Theoretical:** What/Where/When memory dimensions are expected to share variance
   - Remembering object identity (What) facilitates spatial recall (Where) via semantic cues
   - Example: Remembering "toothbrush" (What) helps recall bathroom sink location (Where)
   - Temporal order (When) correlates with encoding strength → affects both What and Where

2. **Empirical:** Cognitive neuroscience evidence shows overlapping neural substrates
   - Hippocampal CA1/CA3 support both spatial and object-context binding
   - Entorhinal cortex integrates spatial (MEC) and object (LEC) information
   - Pattern completion processes retrieve associated features jointly

3. **Psychometric:** Orthogonal factors assume zero correlation → unrealistic for episodic memory
   - Strong episodic memory ability likely manifests across domains
   - General memory factor (g_memory) may underlie all three dimensions

**SENSITIVITY ANALYSIS:** Uncorrelated factors (`correlated=False`)
- Run as secondary analysis reported in supplementary materials
- If conclusions DIFFER between correlated/uncorrelated, report both and discuss implications
- Orthogonal rotation provides cleaner interpretation of domain-specific effects (no shared variance)

**DECISION RULE:**
- Present correlated factors in main text (more realistic model)
- If uncorrelated model yields substantially different conclusions, note in discussion
- Report both factor correlation matrix and factor loadings for transparency

#### 0.1.3 IRT Model: Graded Response Model (GRM)

**Software:** deepirtools IWAVE (importance-weighted amortized variational inference)

**Hyperparameters:**
```python
# Primary analysis (p1_med)
batch_size = 2048
iw_samples = 100  # Importance-weighted samples for ELBO
mc_samples_fit = 1  # Monte Carlo samples during fitting
mc_samples_score = 100  # Monte Carlo samples during scoring
max_epochs = 500
learning_rate = 0.001
```

**Model Fitting:**
```python
from deepirtools import IWAVE

model = IWAVE(
    data=response_matrix,  # (n_respondents × n_items)
    q_matrix=q_matrix,
    model_type='grm',  # Graded Response Model
    correlated_factors=True,  # Or False for sensitivity
    device='cuda:0'  # GPU acceleration
)

model.fit(
    batch_size=batch_size,
    iw_samples=iw_samples,
    mc_samples=mc_samples_fit,
    max_epochs=max_epochs,
    learning_rate=learning_rate
)

# Extract theta scores (latent ability estimates)
thetas = model.score(
    response_matrix,
    mc_samples=mc_samples_score
)  # Returns: (n_respondents × n_factors)

# Extract item parameters
item_params = model.item_parameters()
# Columns: item_name, Difficulty, Discrim_{factor1}, Discrim_{factor2}, ..., Overall_Discrimination
```

#### 0.1.4 Iterative Item Purification

**Purpose:** Remove poorly discriminating items, refit until stable.

**Discrimination Thresholds:** 0.5 ≤ discrimination ≤ 4.0 (Embretson & Reise, 2000)

**Procedure:**
```python
iteration = 1
max_iterations = 10
converged = False

while not converged and iteration <= max_iterations:

    # Step 1: Fit IRT model
    model.fit(...)

    # Step 2: Extract item parameters
    df_params = model.item_parameters()

    # Step 3: Identify poorly discriminating items
    # Item removed if discrimination < 0.5 OR > 4.0 on ANY loaded factor
    poor_items = []
    for factor in factors:
        discrim_col = f'Discrim_{factor}'
        poor = df_params[
            (df_params[discrim_col] < 0.5) | (df_params[discrim_col] > 4.0)
        ]['item_name'].tolist()
        poor_items.extend(poor)

    poor_items = list(set(poor_items))  # Remove duplicates

    # Step 4: Check convergence
    if len(poor_items) == 0:
        converged = True
        print(f"Converged at iteration {iteration}")
    else:
        print(f"Iteration {iteration}: Removing {len(poor_items)} items")
        # Remove poor items from response_matrix
        response_matrix = response_matrix.drop(columns=poor_items)
        iteration += 1

# Save final parameters
df_params.to_csv(f'results/{set}/TQ_corr_noroom_2cats_p1_med_data_difficulty.csv', index=False)
```

#### 0.1.5 Output Files

After IRT pipeline completes, the following files are generated:

1. **Theta scores (ability estimates):**
   - File: `results/{set}/TQ_corr_noroom_2cats_p1_med_data_ability.csv`
   - Columns: `UID, Test, Days, Theta_{factor1}, Theta_{factor2}, ...`
   - Rows: 400 (100 UIDs × 4 Tests)

2. **Item parameters:**
   - File: `results/{set}/TQ_corr_noroom_2cats_p1_med_data_difficulty.csv`
   - Columns: `item_name, Difficulty, Discrim_{factor1}, ..., Overall_Discrimination`
   - Rows: Number of retained items (varies by analysis)

3. **Input data (for reference):**
   - File: `results/{set}/TQ_corr_noroom_2cats_p1_med_data.csv`
   - Long-format response data used as IRT input

**Same files generated for TC_ with `TC_corr_noroom_5cats_p1_med_*` naming.**

---

### 0.2 PROBABILITY TRANSFORMATION SPECIFICATION

**Purpose:** Convert unbounded theta scores to interpretable 0-1 probabilities.

#### 0.2.1 Rationale

- **Theta scores:** Unbounded (-∞ to +∞), latent trait estimates
- **Probabilities:** Bounded (0 to 1), interpretable as response likelihoods
- **Calibration analysis:** Requires comparable scales for P(correct) vs P(high confidence)

#### 0.2.2 Formula

**Logistic (inverse logit) transformation:**

```
P(response | θ) = 1 / (1 + exp(-(a * (θ - b))))
```

Where:
- **θ** = Theta score for a given factor (e.g., Theta_What)
- **a** = Average discrimination parameter for that factor
- **b** = Average difficulty parameter for that factor

#### 0.2.3 Implementation (Factor-Specific Discrimination)

**CRITICAL DECISION:** Use **factor-specific discrimination**, not Overall_Discrimination.

**Theoretical Justification:**
- Factor-specific discrimination reflects how well items differentiate ability *on that specific dimension*
- Overall_Discrimination averages across potentially orthogonal factors → dilutes signal
- Since we transform domain-specific thetas, we must use domain-specific discrimination

**Code:**
```python
def transform_theta_to_probability(df_theta, df_params, factor):
    """
    Transform theta scores to probabilities using factor-specific parameters.

    Args:
        df_theta: DataFrame with columns [UID, Test, Days, Theta_{factor}]
        df_params: Item parameters from IRT (difficulty.csv)
        factor: str, factor name (e.g., 'What', 'Where', 'When')

    Returns:
        df_theta with added column P_{factor}
    """

    # Step 1: Filter retained items for this factor
    # (Items with discrimination in acceptable range)
    discrim_col = f'Discrim_{factor}'
    retained_items = df_params[
        (df_params[discrim_col] >= 0.5) &
        (df_params[discrim_col] <= 4.0)
    ].copy()

    # Step 2: Compute average parameters for this factor
    avg_discrim = retained_items[discrim_col].mean()
    avg_difficulty = retained_items['Difficulty'].mean()

    print(f"{factor}: avg_discrim={avg_discrim:.3f}, avg_difficulty={avg_difficulty:.3f}")

    # Step 3: Transform theta to probability
    theta_col = f'Theta_{factor}'
    prob_col = f'P_{factor}'

    df_theta[prob_col] = 1 / (
        1 + np.exp(-(avg_discrim * (df_theta[theta_col] - avg_difficulty)))
    )

    return df_theta

# Example usage
df_ability = pd.read_csv('results/All by Domain/TQ_corr_noroom_2cats_p1_med_data_ability.csv')
df_difficulty = pd.read_csv('results/All by Domain/TQ_corr_noroom_2cats_p1_med_data_difficulty.csv')

for factor in ['What', 'Where', 'When']:
    df_ability = transform_theta_to_probability(df_ability, df_difficulty, factor)

# Result: df_ability now has P_What, P_Where, P_When columns (0-1 scale)
```

**For TQ_:** Interpret as **P(correct response)**
**For TC_:** Interpret as **P(high confidence rating)**

---

### 0.3 CALIBRATION NOMENCLATURE (Not "Utility")

**RESOLVED:** All "Utility" references removed. Use **Calibration** nomenclature.

#### 0.3.1 Primary Metric: Calibration (Direction)

```python
Calibration = P_correct - P_high_conf
```

**Interpretation:**
- **Calibration > 0:** Underconfident (accuracy exceeds confidence)
- **Calibration < 0:** Overconfident (confidence exceeds accuracy)
- **Calibration = 0:** Perfect calibration

**Visualization:** Horizontal line at y=0 represents perfect calibration. Positive values above, negative below.

#### 0.3.2 Secondary Metric: Calibration Error (Magnitude)

```python
Calibration_error = abs(Calibration)
```

**Interpretation:**
- **Lower = Better** (closer to zero = better calibrated)
- Treats over- and under-confidence symmetrically
- Range: 0 (perfect) to 1 (maximally miscalibrated)

#### 0.3.3 Usage in Analyses

- **RQ6.1-6.3:** Analyze Calibration (direction)
- **RQ6.5-6.6:** Analyze Calibration_error (magnitude)
- **RQ6.12-6.15:** Analyze both direction and magnitude

**No ×-1 inversions.** All signs interpretable as specified above.

---

### 0.4 LINEAR MIXED-EFFECTS MODEL (LMM) SPECIFICATION

#### 0.4.1 Model Structure

**Software:** statsmodels.regression.mixed_linear_model.MixedLM

**General Form:**
```python
import statsmodels.formula.api as smf

model = smf.mixedlm(
    formula="Outcome ~ Time + (Time | UID)",
    data=df,
    groups=df["UID"],
    re_formula="~Time"  # Random intercepts + random slopes
)

fit = model.fit(method=['lbfgs'], reml=False)
```

**Components:**
- **Fixed effects:** Population-level average trajectory
- **Random intercepts:** Individual differences in baseline (Day 0 ability)
- **Random slopes:** Individual differences in forgetting rate
- **REML=False:** Maximum likelihood estimation (allows AIC comparison across models)

#### 0.4.2 Time Variable Transformations

**Available transformations:**
```python
# Linear time
df['Time'] = df['Days']  # 0, 1, 3, 6

# Quadratic time
df['Time_sq'] = df['Days'] ** 2  # 0, 1, 9, 36

# Logarithmic time
df['Time_log'] = np.log(df['Days'] + 1)  # 0, 0.69, 1.39, 1.95

# Piecewise (for consolidation analyses)
df['Segment'] = pd.cut(df['Days'], bins=[0, 1, 6], labels=['Early', 'Late'], include_lowest=True)
df['Days_within_segment'] = df.groupby(['UID', 'Segment'])['Days'].transform(lambda x: x - x.min())
```

#### 0.4.3 Candidate Models for Trajectory Fitting

For each RQ, fit 5 models and select best via AIC:

1. **Linear:** `Outcome ~ Days + (Days | UID)`
2. **Quadratic:** `Outcome ~ Days + Days_sq + (Days | UID)`
3. **Logarithmic:** `Outcome ~ log(Days+1) + (Days | UID)`
4. **Lin+Log:** `Outcome ~ Days + log(Days+1) + (Days | UID)` ← Often best
5. **Quad+Log:** `Outcome ~ Days + Days_sq + log(Days+1) + (Days | UID)`

**Selection Rule:**
- If ΔAIC < 2: Models equivalent → Choose simpler (fewest parameters)
- If ΔAIC > 10: Strong evidence for better model
- Report Akaike weights for transparency

#### 0.4.4 Random Effects Specification

**Random intercepts + slopes (default):**
```python
re_formula="~Days"  # Allows individual variation in both baseline and rate
```

**Random intercepts only (if slopes fail to converge):**
```python
re_formula="~1"  # Only individual baselines vary
```

**IMPORTANT:** If random slopes variance = 0 (boundary issue), refit with intercepts only.

---

### 0.5 MULTIPLE COMPARISONS CORRECTION

#### 0.5.1 Chapter-Level Bonferroni

**Applied to primary hypothesis tests:**

| Chapter | # RQs | α per RQ | Calculation |
|---------|-------|----------|-------------|
| **Chapter 5** | 15 | 0.0033 | 0.05 / 15 |
| **Chapter 6** | 15 | 0.0033 | 0.05 / 15 |
| **Chapter 7** | 20 | 0.0025 | 0.05 / 20 |

**Usage:** Apply corrected α to main LMM interaction term (e.g., Domain × Days).

#### 0.5.2 Nested Bonferroni for Post-Hocs

**WITHIN each RQ**, additional correction for pairwise contrasts:

**Example (RQ5.1 - 3 domain comparisons):**
- Chapter-level α = 0.0033
- Post-hoc comparisons: What vs Where, What vs When, Where vs When (k=3)
- Post-hoc α = 0.0033 / 3 = 0.0011

**Formula:** α_posthoc = α_chapter / k_comparisons

#### 0.5.3 Reporting

**Template:**
> "We applied Bonferroni correction for family-wise error rate control (Chapter 5: α=0.0033 for 15 tests). Post-hoc pairwise contrasts used nested Bonferroni correction (α=0.0011 for 3 comparisons)."

---

### 0.6 EFFECT SIZE REPORTING

**MANDATORY:** Report effect sizes alongside all p-values.

#### 0.6.1 LMM Effect Sizes

**Cohen's f² for fixed effects:**
```python
# f² = R²_full - R²_reduced / (1 - R²_full)
# Compare model with vs without term of interest

# Thresholds: small=0.02, medium=0.15, large=0.35
```

**Conditional R² (variance explained by fixed + random effects):**
```python
from statsmodels.regression.mixed_linear_model import MixedLM

# R² conditional: Proportion of total variance explained
# Computed via likelihood ratio approach or manual calculation
```

#### 0.6.2 Group Comparison Effect Sizes

**Cohen's d for mean differences:**
```python
from scipy import stats

# Cohen's d = (M1 - M2) / pooled_SD
d = (group1.mean() - group2.mean()) / np.sqrt(
    ((len(group1)-1)*group1.std()**2 + (len(group2)-1)*group2.std()**2) /
    (len(group1) + len(group2) - 2)
)

# Thresholds: small=0.2, medium=0.5, large=0.8
```

#### 0.6.3 Correlation Effect Sizes

**Pearson r:**
- small = 0.10
- medium = 0.30
- large = 0.50

**Report with 95% CI:**
```python
from scipy.stats import pearsonr

r, p = pearsonr(x, y)

# Fisher's z transformation for CI
z = np.arctanh(r)
se = 1 / np.sqrt(len(x) - 3)
ci_z = [z - 1.96*se, z + 1.96*se]
ci_r = np.tanh(ci_z)

print(f"r = {r:.2f}, 95% CI [{ci_r[0]:.2f}, {ci_r[1]:.2f}], p = {p:.3f}")
```

---

### 0.7 ASSUMPTION CHECKING (All LMMs)

**Run for EVERY LMM analysis. Document in "Success Criteria" section.**

#### 0.7.1 Model Convergence

```python
# Check convergence flag
assert fit.converged == True, "Model did not converge!"

# Inspect summary for warnings
print(fit.summary())
```

**If fails:** Try different optimizer, check for singularity (variance=0), remove random slopes.

#### 0.7.2 Residual Normality

```python
import scipy.stats as stats
import matplotlib.pyplot as plt

residuals = fit.resid

# Q-Q plot (visual inspection primary)
stats.probplot(residuals, dist="norm", plot=plt)
plt.title(f"{analysis_name}: Q-Q Plot")
plt.savefig(f'diagnostics/{analysis_name}_qq.png', dpi=300)
plt.close()

# Shapiro-Wilk test (supplementary)
stat, p = stats.shapiro(residuals)
print(f"Shapiro-Wilk: W={stat:.3f}, p={p:.3f}")

# NOTE: LMM robust to mild violations if Q-Q approximately linear
```

**Criterion:** Visual linearity in Q-Q plot more important than Shapiro p-value (large n inflates Type I error).

#### 0.7.3 Homoscedasticity

```python
fitted = fit.fittedvalues

plt.scatter(fitted, residuals, alpha=0.5)
plt.axhline(0, color='red', linestyle='--')
plt.xlabel("Fitted Values")
plt.ylabel("Residuals")
plt.title(f"{analysis_name}: Residuals vs Fitted")
plt.savefig(f'diagnostics/{analysis_name}_resid_fitted.png', dpi=300)
plt.close()

# Look for: No funnel pattern, variance constant across fitted values
```

**If violated:** Consider robust SEs or log-transformation of outcome.

#### 0.7.4 Random Effects Normality

```python
re_df = pd.DataFrame(fit.random_effects).T

# Random intercepts
plt.hist(re_df.iloc[:, 0], bins=20, edgecolor='black')
plt.title(f"{analysis_name}: Random Intercepts Distribution")
plt.savefig(f'diagnostics/{analysis_name}_re_intercepts.png', dpi=300)
plt.close()

# Random slopes (if included)
if re_df.shape[1] > 1:
    plt.hist(re_df.iloc[:, 1], bins=20, edgecolor='black')
    plt.title(f"{analysis_name}: Random Slopes Distribution")
    plt.savefig(f'diagnostics/{analysis_name}_re_slopes.png', dpi=300)
    plt.close()
```

**Criterion:** Approximately normal distribution (some skew acceptable).

#### 0.7.5 Outliers

```python
# Flag extreme residuals (>3 SD)
threshold = 3
outliers = np.abs(residuals) > (threshold * residuals.std())

print(f"Outliers: {outliers.sum()} ({100*outliers.mean():.1f}%)")

if outliers.sum() > 0:
    print("Outlier UIDs:", df[outliers]['UID'].unique())
    # DOCUMENT but do NOT auto-remove
    # Consider sensitivity analysis excluding outliers
```

---

### 0.8 DATA VALIDATION (Run Before Analysis)

```python
def validate_irt_output(df_ability, df_difficulty, expected_factors):
    """
    Validate IRT output files before using in LMM.

    Raises AssertionError if validation fails.
    """

    # Check 1: Required columns
    required_ability = ['UID', 'Test', 'Days'] + [f'Theta_{f}' for f in expected_factors]
    assert all(col in df_ability.columns for col in required_ability), \
        f"Missing columns: {set(required_ability) - set(df_ability.columns)}"

    # Check 2: No missing thetas
    theta_cols = [f'Theta_{f}' for f in expected_factors]
    assert df_ability[theta_cols].notna().all().all(), "Missing theta values!"

    # Check 3: Expected Days values
    expected_days = [0, 1, 3, 6]
    actual_days = sorted(df_ability['Days'].unique())
    assert actual_days == expected_days, f"Unexpected Days: {actual_days}"

    # Check 4: Expected number of rows
    n_uid = df_ability['UID'].nunique()
    n_test = df_ability['Test'].nunique()
    expected_rows = n_uid * n_test
    assert len(df_ability) == expected_rows, \
        f"Expected {expected_rows} rows ({n_uid} UIDs × {n_test} Tests), got {len(df_ability)}"

    # Check 5: Discrimination in range
    for factor in expected_factors:
        discrim_col = f'Discrim_{factor}'
        if discrim_col in df_difficulty.columns:
            assert df_difficulty[discrim_col].between(0.5, 4.0).all(), \
                f"{discrim_col} outside range (0.5-4.0)"

    # Check 6: Difficulty in plausible range
    assert df_difficulty['Difficulty'].between(-5, 5).all(), \
        "Extreme difficulty values detected"

    print("✓ Data validation passed")
    return True
```

---

### 0.9 REPRODUCIBILITY REQUIREMENTS

#### 0.9.1 Random Seeds

**Set at start of EVERY analysis session:**

```python
import numpy as np
import random
import torch

SEED = 42

np.random.seed(SEED)
random.seed(SEED)
torch.manual_seed(SEED)

if torch.cuda.is_available():
    torch.cuda.manual_seed(SEED)
    torch.cuda.manual_seed_all(SEED)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False

# Verify
print(f"Random seed set to: {SEED}")
print(f"NumPy random test: {np.random.rand()}")  # Should be 0.3745401188473625
```

#### 0.9.2 Version Control

**Before each analysis run:**
```bash
# Record git state
git log -1 --oneline > analysis_git_version.txt

# Freeze package versions
pip freeze > requirements_frozen.txt

# Document start time
echo "Analysis started: $(date)" >> analysis_log.txt
```

#### 0.9.3 Model Saving

**All LMMs must be saved for later inspection:**

```python
import os

# Create directory
os.makedirs(f'results/{set_name}/pkl', exist_ok=True)

# Save fitted model
model_path = f'results/{set_name}/pkl/{analysis_name}.pkl'
fit.save(model_path)

print(f"Model saved: {model_path}")
```

**CRITICAL for Chapter 7:** Random effects must be extracted from saved models.

---

### 0.10 REPORTING PRECISION

| Statistic | Decimal Places | Example | Notes |
|-----------|----------------|---------|-------|
| **P-values** | 3 | p=0.001 | If p<0.001, report as "p<0.001" |
| **Coefficients (β)** | 3 | β=0.123 | Include sign |
| **Effect sizes (d, f²)** | 2 | d=0.45 | Always positive |
| **Correlations (r)** | 2 | r=0.87 | Include sign |
| **R²** | 3 | R²=0.456 | Always between 0-1 |
| **AIC** | 1 | AIC=1234.5 | Lower is better |
| **Theta scores** | 2 | θ=1.23 | Can be negative |
| **Probabilities** | 3 | P=0.875 | Always 0-1 |

---

### 0.11 STANDARDIZED RQ SCHEMA

**Every RQ follows this exact template:**

```markdown
### RQX.Y: [Question Title]

**Research Question:** [Precise, answerable question]

**Hypothesis:** [Directional prediction OR "Exploratory" with rationale]

**Data Required:**
- Analysis Set: [Name] (file: results/[exact_path].csv)
- Variables: [List all columns needed]
- Preprocessing: [Any transformations required]

**Analysis Recipe:**

1. **[Step Name]**
   [Description]
   ```python
   [Executable code]
   ```

2. **[Step Name]**
   [Description]
   ```python
   [Executable code]
   ```

[Continue for all steps...]

**Statistical Justification:**
- [Why this method?]
- [Theoretical grounding]
- [Methodological advantages]
- [Citations where relevant]

**Expected Output:**
- [Table/Plot 1]: [Exact columns/elements]
- [Table/Plot 2]: [Exact columns/elements]
- [Statement]: "[Exact wording template]"

**Success Criteria:**
- [ ] Model converged (fit.converged == True)
- [ ] Residuals approximately normal (Q-Q visual check)
- [ ] No extreme outliers (Cook's D < 1.0)
- [ ] [Analysis-specific checks]
- [ ] Results replicate when re-run (same seed)

**Reviewer Rebuttals:**

**Q:** "[Anticipated objection]"
**A:** "[Preemptive response with citation/justification]"

[Additional Q&A as needed]

---
```

**This schema is MANDATORY for all 50 RQs.**

---

### 0.12 DATA PIPELINE: FROM MASTER.XLSX TO ANALYSES

**CRITICAL:** All analyses start from raw data in `master.xlsx`. This section documents the complete pipeline.

#### 0.12.1 Data Source

**File:** `data/master.xlsx`
- Contains all raw experimental data for N=100 participants × 4 tests
- Size: ~3.9 MB
- Never edit this file directly - it is the source of truth

**Variable definitions:** `data/variables.xlsx`
- Maps column names to conceptual variables
- Contains regex patterns for extracting variable subsets (tag system)
- User will explain tag system after analyses are specified

#### 0.12.2 Loading Pipeline

**Primary function:** `data/data.py::startup()`

**Procedure:**
```python
from data import data

# Load all data
dfData = data.startup()

# Returns pandas DataFrame with columns:
# - UID: Participant ID (A001-A100)
# - Test: Test number (1-4)
# - Days: Days since VR encoding (0, 1, 3, 6)
# - Composite_ID: UID_T{test} (e.g., A042_T3)
# - TQ_* columns: Test Question accuracy scores (0 or 1)
# - TC_* columns: Test Confidence ratings (0.0, 0.25, 0.5, 0.75, 1.0)
# - Demographics: Age, Sex, Education, etc.
# - Cognitive tests: RAVLT_*, BVMT_*, NART, RPM
# - Sleep/strategy: Self-report variables
```

**Caching:** Results cached in `data/cache/dfData.csv` for faster subsequent loads

#### 0.12.3 Partial Credit Scoring CLARIFICATION

**CRITICAL DECISION:** NO partial credit used in final analyses.

**What was collected:**
- During scoring (methods.md lines 114-117), partial credit WAS assigned:
  - 0.5 for adjacent spatial responses
  - 0.5 for off-by-1 temporal responses
  - 0.25 for off-by-2 temporal responses

**What is used for IRT:**
- All TQ_ scores recoded to **dichotomous (0 or 1)** before IRT analysis
- Partial scores (0.25, 0.5) → 0 (incorrect)
- Only 1.0 → 1 (correct)

**Rationale:**
1. **Arbitrary thresholds:** "Adjacent" spatial and "off-by-1" temporal are judgment calls
2. **Uneven scoring:** Edge items (position 1, position 6) have fewer adjacent options
3. **IRT requirement:** 2-category GRM requires dichotomous data
4. **Reviewer concerns:** Partial credit invites criticism without adding substantial information

**Implementation:**
```python
# In tools.py or preprocessing step
def recode_to_dichotomous(df, tq_columns):
    """
    Recode all TQ_ columns to strict 0/1 (no partial credit).

    Args:
        df: DataFrame with TQ_ columns
        tq_columns: List of TQ_ column names

    Returns:
        df with TQ_ columns recoded
    """
    for col in tq_columns:
        # Only 1.0 → 1, everything else (0, 0.25, 0.5, 0.75) → 0
        df[col] = (df[col] == 1.0).astype(int)

    return df
```

**CTT Analyses:** Use dichotomous scores (same as IRT) for consistency

#### 0.12.4 Analysis Set Creation

**Function:** `tools.py::select_data()`

**Purpose:** Extract item subsets for specific analysis sets (e.g., "All by Domain")

**Procedure:**
```python
from tools import tools

# Define analysis set
analysis_set = {
    'label': 'All by Domain',
    'groups': {
        'What': r'TQ_.*-N-',  # Regex: All TQ items with -N- (Name/What)
        'Where': r'TQ_.*-[UD]-',  # Regex: All TQ items with -U- or -D- (spatial)
        'When': r'TQ_.*-O-'  # Regex: All TQ items with -O- (Order/When)
    },
    'correlated_factors': True,
    'specify_room': False  # Pool across rooms
}

# Extract relevant columns
df_subset = tools.select_data(dfData, analysis_set)

# Returns long-format DataFrame:
# Composite_ID | Item | Response | Factor | Days
# A001_T1      | TQ_IFR-N-i1 | 1 | What | 0
# A001_T1      | TQ_IFR-N-i2 | 0 | What | 0
# ...

# Save for IRT input
df_subset.to_csv('results/All by Domain/TQ_corr_noroom_2cats_data.csv', index=False)
```

#### 0.12.5 Complete Workflow Summary

**For each analysis set:**

1. **START:** `master.xlsx` (raw data)
   ↓
2. **LOAD:** `data/data.py::startup()` → `dfData.csv` (all variables)
   ↓
3. **RECODE:** Partial credit → Dichotomous (TQ_ columns)
   ↓
4. **SELECT:** `tools.py::select_data()` → Extract analysis-specific items
   ↓
5. **IRT:** `irt.py::DeepIrt()` → Fit GRM, extract thetas + item params
   ↓
6. **TRANSFORM:** Theta → Probability (factor-specific discrimination)
   ↓
7. **LMM:** `statsmodels.MixedLM()` → Model trajectories, test hypotheses
   ↓
8. **OUTPUT:** Tables, plots, model summaries

**Key Files at Each Stage:**
- Stage 1-2: `master.xlsx` → `dfData.csv`
- Stage 3-4: `dfData.csv` → `results/{set}/TQ_*_data.csv`
- Stage 5: `TQ_*_data.csv` → `TQ_*_ability.csv` + `TQ_*_difficulty.csv`
- Stage 6: `TQ_*_ability.csv` → Add `P_{factor}` columns
- Stage 7-8: `TQ_*_ability.csv` → Model summaries + plots

#### 0.12.6 Reproducibility

**CRITICAL:** Every analysis MUST be reproducible from `master.xlsx` alone.

**Requirements:**
1. Fixed random seed (42) for all stochastic processes
2. Version-controlled code (Git)
3. Saved model objects (.pkl files) for LMMs
4. Documented package versions (requirements.txt)
5. No manual data editing between stages

**Verification:**
```python
# At start of any analysis script
import numpy as np
import random
import torch

SEED = 42
np.random.seed(SEED)
random.seed(SEED)
torch.manual_seed(SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed_all(SEED)
```

---

## END OF PART 0: GLOBAL SPECIFICATIONS

**Next:** PART 1 (Chapter 5), PART 2 (Chapter 6), PART 3 (Chapter 7) will follow this foundation.

All RQs build on these specifications. Any deviation is explicitly noted within the RQ.

---

**STATUS:** Part 0 complete. Ready for Chapter-specific RQs.
