# CRITICAL AUDIT: analyses.md

**Purpose:** Identify ALL ambiguities, errors, and gaps before thesis implementation
**Date:** 2025-11-01
**Auditor:** Claude (Sonnet 4.5)
**Status:** COMPREHENSIVE LINE-BY-LINE REVIEW

---

## SEVERITY LEVELS

🔴 **CRITICAL** - Will cause analysis failure or wrong results
🟡 **HIGH** - Major ambiguity that could lead to confusion
🟢 **MEDIUM** - Minor clarification needed
⚪ **LOW** - Stylistic or documentation improvement

---

## SCHEMA REQUIREMENTS (User-Specified)

Every RQ MUST have:
1. ✅ **Research Question** - Clear, answerable question
2. ✅ **Hypothesis** - Directional or exploratory prediction
3. ✅ **Data Required** - Exact datasets, variables, file paths
4. ✅ **Analysis Recipe** - Step-by-step procedure (numbered, code included)
5. ✅ **Statistical Justification** - Why this method? Preemptive rebuttals
6. ✅ **Expected Output** - Exact tables, plots, statements with validation criteria
7. ✅ **Success Criteria** - How to know if done correctly (NEW - missing throughout)
8. ✅ **Reviewer Rebuttals** - Anticipated objections + responses (missing for most)

---

## GLOBAL ISSUES (Affect Multiple RQs)

### 🔴 CRITICAL-G1: Missing Success Criteria Throughout

**Problem:** NO RQs specify validation checks
**Impact:** Can't verify analyses were done correctly
**Fix Required:** Add to EVERY RQ:

```markdown
**Success Criteria:**
- [ ] Model converged (check .summary() for convergence warnings)
- [ ] Residuals approximately normal (Q-Q plot R² > 0.95)
- [ ] No extreme outliers (Cook's D < 1.0 for all observations)
- [ ] VIF < 5 for all predictors (if regression)
- [ ] Random effects variance > 0 (not boundary values)
- [ ] Coefficients in plausible range (document expected ranges)
- [ ] AIC comparison: Chosen model has lowest AIC
- [ ] Results replicate when re-run (reproducibility check)
```

---

### 🔴 CRITICAL-G2: IRT Analysis Set Specification Ambiguous

**Problem:** Many RQs say "All by Domain" but don't specify:
- Correlated (primary) or Uncorrelated (sensitivity)?
- Which iteration: p1_med or p2_high?
- Which file exactly?

**Example (RQ5.1 line 92):**
```markdown
- Analysis Set: **All by Domain** (3 factors: What, Where, When)
```

**Should be:**
```markdown
- Analysis Set: **All by Domain** (Correlated, p1_med)
  - File: `results/All by Domain/TQ_corr_noroom_2cats_p1_med_data_ability.csv`
  - Factors: What, Where, When (3 correlated factors)
  - Items retained after purification: Check `*_data_difficulty.csv` (only items with 0.5 ≤ discrim ≤ 4.0)
```

**Affected RQs:** 5.1, 5.2, 5.9, 5.10, 5.11, 5.12, 6.1, 6.2, 7.1, 7.2

---

### 🔴 CRITICAL-G3: TC_ IRT Processing Details Missing

**Problem:** Decision made to run TC_ through IRT (lines 653-773) but ZERO RQs specify:
- Same Q-matrix as TQ_?
- Same discrimination thresholds (0.5-4.0)?
- Same iterative purification?
- What if different items removed for TC_ vs TQ_?
- How to handle mismatched item sets?

**Fix Required:** Add section BEFORE Chapter 6:

```markdown
### TC_ IRT Pipeline Specification

**Critical Decision:** TC_ undergoes IDENTICAL IRT processing as TQ_

**Step-by-Step:**

1. **Input Data**
   - TC_ items (5-category Likert: 0.0, 0.25, 0.5, 0.75, 1.0 rescaled)
   - Same participants, same time points as TQ_

2. **Q-Matrix**
   - IDENTICAL factor structure as corresponding TQ_ analysis
   - Example: If TQ_All_by_Domain has What/Where/When, TC_All_by_Domain has What/Where/When

3. **Iterative Purification**
   - Apply SAME thresholds: 0.5 ≤ discrimination ≤ 4.0
   - Items may differ between TQ_ and TC_ (expected)
   - **CRITICAL:** For calibration analyses (RQ6.1-6.3), only use items retained in BOTH TQ_ and TC_ models

4. **Probability Transformation**
   - Extract theta_confidence per factor
   - Compute average item discrimination and difficulty PER FACTOR (from retained items)
   - Transform: P(high_conf) = 1 / (1 + exp(-(a_avg * (theta - b_avg))))
   - a_avg = mean discrimination for factor
   - b_avg = mean difficulty for factor

5. **Files Generated**
   - `results/{set}/TC_corr_noroom_5cats_p1_med_data_ability.csv` (theta scores)
   - `results/{set}/TC_corr_noroom_5cats_p1_med_data_difficulty.csv` (item parameters)
   - `results/{set}/TC_corr_noroom_5cats_p1_med_data.csv` (long-format input data)
```

---

### 🟡 HIGH-G4: Probability Transformation Formula Incomplete

**Problem (lines 810, 250 reference):**
```python
df_conf['P_high_conf'] = 1 / (1 + np.exp(-(discrim * (df_conf['Theta'] - difficulty))))
```

**Missing:**
- What is `discrim`? Overall or factor-specific?
- What is `difficulty`? Item-specific or average?
- How computed exactly?

**From analysis.py line 232-237:**
```python
avg_discrimination = acceptable_items['Overall_Discrimination'].mean()
avg_difficulty = acceptable_items['Difficulty'].mean()
```

**Correct specification:**
```python
# Step 1: Load item parameters
df_params = pd.read_csv(f'results/{set}/TQ_corr_noroom_2cats_p1_med_data_difficulty.csv')

# Step 2: Filter retained items (post-purification)
retained_items = df_params[
    (df_params[f'Discrim_{factor}'] >= 0.5) &
    (df_params[f'Discrim_{factor}'] <= 4.0)
]

# Step 3: Compute average parameters PER FACTOR
avg_discrim = retained_items['Overall_Discrimination'].mean()  # Or use factor-specific?
avg_difficulty = retained_items['Difficulty'].mean()

# Step 4: Transform theta to probability
df['P_correct'] = 1 / (1 + np.exp(-(avg_discrim * (df['Theta'] - avg_difficulty))))
```

**CLARIFICATION NEEDED:** Use `Overall_Discrimination` or `Discrim_{factor}`?
**Recommendation:** Use factor-specific discrimination, document clearly.

---

### 🔴 CRITICAL-G5: Utility Inversion Unresolved

**Problem (lines 1009-1027, RQ6.5):**
```markdown
# Line 1009
df['Utility'] = (df['Theta'] - df['TC_mean']) * -1

# Line 1022: "**CLARIFY THIS**" ← RED FLAG!!!

# Line 1025 suggests alternative:
df['Utility_abs'] = np.abs(df['Theta'] - df['TC_mean'])
```

**This MUST be resolved definitively:**

**Option A: Signed Utility (Current in analysis.py line 299)**
```python
Utility = (P_correct - P_high_conf) * -1
# Positive = Better calibration (overconfident or underconfident reversed)
# Zero = Perfect calibration
# Negative = Worse calibration
```
**Problem:** Sign inversion is confusing. What does "positive" mean?

**Option B: Absolute Utility**
```python
Utility_abs = np.abs(P_correct - P_high_conf)
# Lower = Better calibration
# Zero = Perfect calibration
# Symmetrically treats over- and under-confidence
```
**Advantage:** Unambiguous interpretation.

**Option C: Calibration Error (Standard nomenclature)**
```python
Calibration = P_correct - P_high_conf
# Positive = Underconfident (accuracy > confidence)
# Negative = Overconfident (confidence > accuracy)
# Zero = Perfect

# THEN analyze absolute value for "calibration error magnitude"
Calibration_error = np.abs(Calibration)
```

**RECOMMENDATION:** Use Option C (matches RQ6.2 already uses this!)
- Call it "Calibration" not "Utility"
- Analyze BOTH signed (for direction) and absolute (for magnitude)
- Remove all "×-1" inversions
- Update RQ6.5, 6.6, 6.12-6.15

---

### 🟡 HIGH-G6: Bonferroni Application Inconsistent

**Current State:**
- Ch5: α = 0.05/15 = 0.0033 (stated line 49)
- Ch6: α = 0.05/15 = 0.0033 (stated line 50)
- Ch7: α = 0.05/20 = 0.0025 (stated line 51)

**But:**
- Some RQs apply additional Bonferroni for post-hocs (e.g., RQ5.1 line 123: α=0.05/3 for pairwise tests)
- Others don't mention correction at all

**Clarification Needed:**
1. **Family-wise correction:** Applied once per chapter to ALL RQs
2. **Post-hoc corrections:** Applied WITHIN each RQ for multiple comparisons

**Example (RQ5.1):**
- Main LMM test (Domain × Days interaction): Use α = 0.0033 (chapter-level Bonferroni)
- Post-hoc pairwise contrasts (3 comparisons): Use α = 0.0033/3 = 0.0011 (nested Bonferroni)

**Fix:** Make this explicit in EVERY RQ that does post-hocs.

---

### 🟡 HIGH-G7: CTT Convergence Checks Incomplete

**Problem:** Only RQ6.1 and 6.2 specify CTT validation.
**Missing in:** RQ6.3-6.15

**Required Addition to EVERY Chapter 6 RQ:**
```markdown
**CTT Convergence Check:**
```python
# Compute CTT equivalent
df_ctt = df_raw.groupby(['UID', 'Test', 'Days', 'Domain']).agg({
    'TQ': 'mean',  # Accuracy
    'TC_rescaled': 'mean'  # Confidence (rescaled 0-1)
}).reset_index()

# Re-run same LMM with CTT scores
# Compare:
# - β coefficients (should be similar direction)
# - p-values (should agree on significance)
# - Correlation: corr(IRT_estimates, CTT_estimates) > 0.90

# Report: "IRT and CTT approaches converged (r=0.XX), confirming robustness."
```
```

---

### 🟢 MEDIUM-G8: "Same as RQ X.Y" References Problematic

**Examples:**
- RQ5.4 line 219: "Use LMM from RQ5.3"
- RQ5.8 line 358: "Use Model Comparison from RQ5.7"

**Problem:** Forces reader to flip back, risking confusion.

**Fix:** Repeat the formula/procedure or provide explicit cross-reference:
```markdown
**Analysis Recipe:**
1. **Use LMM from RQ5.3 (repeated for clarity):**
   - Formula: `Theta ~ Days * C(Paradigm, Treatment('Free')) + (Days | UID)`
   - (See RQ5.3 for full specification)
```

---

### 🟢 MEDIUM-G9: Missing Decimal Place Specifications

**Problem:** No guidance on reporting precision.

**Fix:** Add to global section:
```markdown
### Reporting Precision

- **P-values:** 3 decimal places (e.g., p=0.001), report p<0.001 if smaller
- **Coefficients (β):** 3 decimal places (e.g., β=0.123)
- **Effect sizes (d, f²):** 2 decimal places (e.g., d=0.45)
- **Correlations (r):** 2 decimal places (e.g., r=0.87)
- **R²:** 3 decimal places (e.g., R²=0.456)
- **AIC:** 1 decimal place (e.g., AIC=1234.5)
```

---

## CHAPTER-SPECIFIC ISSUES

### CHAPTER 5: Forgetting Trajectories

#### 🟡 RQ5.1 (Lines 87-141)

**Missing:**
- Success criteria (model convergence, residuals)
- Which model to select if multiple have similar AIC (e.g., ΔAIC < 2)?
- Reviewer rebuttal for Treatment coding choice

**Add:**
```markdown
**Model Selection Rule:**
- If ΔAIC < 2: Models are equivalent, select simpler model (fewest parameters)
- If ΔAIC > 10: Strong evidence for better model
- Report Akaike weights for all models

**Reviewer Rebuttal:**
**Q:** "Why Treatment coding for Domain?"
**A:** "Treatment coding with What as reference provides interpretable intercept (What baseline) and contrasts (Where vs What, When vs What). Dummy coding would give same model fit but less intuitive coefficients. We also report helmert contrasts in supplementary materials for completeness."
```

---

#### 🟡 RQ5.2 (Lines 144-183)

**Ambiguity:**
- Line 157: "Days_within_segment" creation unclear

**Clarify:**
```python
# More explicit code
df_long['Segment'] = np.where(df_long['Days'] <= 1, 'Early', 'Late')

# Early segment: Days 0, 1 → Days_within = 0, 1
# Late segment: Days 1, 3, 6 → Days_within = 0, 2, 5
df_long['Days_within_segment'] = df_long.groupby(['UID', 'Segment'])['Days'].transform(
    lambda x: x - x.min()
)

# Verify:
# Day 0 → Early, Days_within=0
# Day 1 → Early, Days_within=1 (AND Late, Days_within=0 if overlap)
# WAIT - this creates overlap at Day 1!

# CORRECTED (no overlap):
df_long['Segment'] = pd.cut(df_long['Days'], bins=[0, 1, 6], labels=['Early', 'Late'], include_lowest=True)
```

**CRITICAL:** Day 1 is in BOTH segments currently. Fix this!

---

#### 🔴 RQ5.7 (Lines 295-346) - MAJOR ISSUE

**Problem:** Akaike weights formula (line 325) is correct but validation missing.

**Missing:**
- What if all models have similar weights (e.g., all 0.15-0.25)? → Model uncertainty high, report all
- How to interpret Akaike weights in results?

**Add:**
```markdown
**Interpretation of Akaike Weights:**
- Weight > 0.90: Very strong evidence for this model
- Weight 0.60-0.90: Strong evidence
- Weight 0.30-0.60: Moderate evidence (consider reporting top 2 models)
- All weights < 0.30: High model uncertainty (report model-averaged predictions)

**If model uncertainty high:**
```python
# Compute model-averaged predictions
predictions = sum([weight_i * pred_i for i, (weight_i, pred_i) in enumerate(zip(weights, predictions))])
```
```

---

#### 🟡 RQ5.9 (Lines 382-420)

**Missing specification:**
- Mean-centering: Use grand mean or age=45?

**Clarify:**
```python
# Explicit centering
grand_mean_age = df_long['Age'].mean()  # E.g., 45.3
df_long['Age_c'] = df_long['Age'] - grand_mean_age

# Document in text:
"Age was grand-mean centered (M=45.3, SD=14.2), so intercept represents memory ability for an average-aged participant."
```

---

#### 🟡 RQ5.11 (Lines 455-495)

**Line 479: "Which has better model fit (AIC)?"**

**Problem:** IRT theta vs CTT mean are on different scales → AIC not directly comparable!

**Fix:**
```markdown
3. **Compare Conclusions**
   - Do both detect same Domain × Time interaction? (direction and significance)
   - Are slope estimates similar in magnitude and direction? (compare standardized coefficients)
   - ~~Which has better model fit (AIC)?~~ **[REMOVED - not comparable]**
   - Instead: Compare R² (proportion variance explained)
```

---

#### 🔴 RQ5.12 (Lines 498-538)

**Line 517: `retained_items = df_difficulty[df_difficulty['discrimination'].between(0.5, 4.0)]`**

**Problem:** Column name ambiguous. Is it:
- `Overall_Discrimination`?
- `Discrim_What`, `Discrim_Where`, etc.?

**Fix:**
```python
# EXPLICIT column names
retained_items = df_difficulty[
    ((df_difficulty['Discrim_What'] >= 0.5) & (df_difficulty['Discrim_What'] <= 4.0)) |
    ((df_difficulty['Discrim_Where'] >= 0.5) & (df_difficulty['Discrim_Where'] <= 4.0)) |
    ((df_difficulty['Discrim_When'] >= 0.5) & (df_difficulty['Discrim_When'] <= 4.0))
]['item_name'].tolist()

# NOTE: Items retained if they discriminate well on ANY loaded factor
```

---

#### 🟡 RQ5.13 (Lines 541-571)

**Line 554: ICC calculation formula incorrect**

**Current:**
```python
var_between_slopes = model.cov_re.iloc[1,1]
var_within = model.scale
ICC_slopes = var_between_slopes / (var_between_slopes + var_within)
```

**Problem:** This is ICC for random slopes, but denominator includes residual variance, which inflates denominator.

**Corrected ICC for slopes:**
```python
# Extract variance components
var_intercept = model.cov_re.iloc[0,0]  # Random intercept variance
var_slope = model.cov_re.iloc[1,1]  # Random slope variance
cov_int_slope = model.cov_re.iloc[0,1]  # Covariance
residual_var = model.scale  # Residual (within-person) variance

# ICC for intercepts
ICC_intercept = var_intercept / (var_intercept + residual_var)

# ICC for slopes (proportion of slope variance that's between-person)
# NOTE: No standard formula; some use:
ICC_slope = var_slope / (var_slope + residual_var)

# Interpret: "X% of variance in forgetting rate is between-person"
```

**VERIFY THIS FORMULA** - may need consultation with statistician.

---

#### 🟡 RQ5.15 (Lines 617-648)

**Line 632: Cross-level interaction formula**

**Missing:**
- How to center Item_difficulty? (grand-mean? within-person?)
- Degrees of freedom for (1 | Item) random effect?

**Clarify:**
```python
# Grand-mean center difficulty
df['Item_difficulty_c'] = df['Item_difficulty'] - df['Item_difficulty'].mean()

# Model
import statsmodels.formula.api as smf
model = smf.mixedlm(
    "Theta ~ Days * Item_difficulty_c",
    data=df,
    groups=df["UID"],
    re_formula="~Days",  # Random slopes for UID
    # ADD second random effect for items - NOT SUPPORTED IN statsmodels!
).fit()
```

**CRITICAL:** `statsmodels.MixedLM` does NOT support crossed random effects (UID × Item).
**Alternative:** Use `pymer4` (lme4 wrapper) or `R` via rpy2.

**Code (using pymer4):**
```python
from pymer4.models import Lmer

model = Lmer("Theta ~ Days * Item_difficulty_c + (Days | UID) + (1 | Item)", data=df)
model.fit()
```

**MUST ADD:** Dependency on pymer4 OR note that this analysis requires R.

---

### CHAPTER 6: Metacognition

#### 🔴 RQ6.1 (Lines 791-853) - CRITICAL

**Line 810: Probability transformation**

**PROBLEM:** Doesn't specify how to get `discrim` and `difficulty` for EACH factor.

**Required specification:**
```python
# Load TC_ item parameters
df_params_tc = pd.read_csv(f'results/All by Domain/TC_corr_noroom_5cats_p1_med_data_difficulty.csv')

# For EACH factor, compute average parameters
for factor in ['What', 'Where', 'When']:
    # Filter items that load on this factor AND were retained
    factor_items = df_params_tc[
        (df_params_tc[f'Loads_on_{factor}'] == 1) &  # Assumes Q-matrix column exists
        (df_params_tc[f'Discrim_{factor}'] >= 0.5) &
        (df_params_tc[f'Discrim_{factor}'] <= 4.0)
    ]

    # Compute averages
    avg_discrim = factor_items['Overall_Discrimination'].mean()  # OR use Discrim_{factor}?
    avg_difficulty = factor_items['Difficulty'].mean()

    # Transform thetas to probabilities
    df_conf.loc[df_conf['Factor'] == factor, 'P_high_conf'] = 1 / (
        1 + np.exp(-(avg_discrim * (df_conf.loc[df_conf['Factor'] == factor, 'Theta'] - avg_difficulty)))
    )
```

**CRITICAL DECISION NEEDED:** Use `Overall_Discrimination` or `Discrim_{factor}`?
**Recommendation:** `Discrim_{factor}` (factor-specific discrimination).

**Also missing:**
- What if a factor has NO retained items after purification? (rare but possible)
- How to handle NA values?

---

#### 🔴 RQ6.3 (Lines 908-948)

**Line 924: Binning confidence**

**Problem:** Bins may have very unequal sample sizes (most ratings clustered at extremes).

**Solution:**
```markdown
2. **Compute Calibration Index**
   ```python
   # OPTION A: Fixed bins (may have unequal n)
   bins = [0, 0.2, 0.4, 0.6, 0.8, 1.0]
   df['Conf_bin'] = pd.cut(df['TC'], bins=bins, labels=['0-20%', '20-40%', '40-60%', '60-80%', '80-100%'])

   # OPTION B: Quantile bins (equal n per bin)
   df['Conf_bin'] = pd.qcut(df['TC'], q=5, labels=['Q1', 'Q2', 'Q3', 'Q4', 'Q5'])

   # Compute mean accuracy per bin
   calib_curve = df.groupby(['Days', 'Conf_bin'])['TQ'].mean().reset_index()
   ```

   **CHOICE:** Use Option B (quantile bins) to ensure sufficient data per bin.
   **REPORT:** "Confidence was binned into quintiles to ensure equal sample sizes per bin."
```

---

#### 🔴 RQ6.5 (Lines 997-1038) - CRITICAL UNRESOLVED ISSUE

**Line 1022: "**CLARIFY THIS**"**

**SEE CRITICAL-G5 ABOVE.** This MUST be resolved before proceeding.

**DECISION REQUIRED FROM USER:**
- Option A: Signed utility (inverted)
- Option B: Absolute utility
- Option C: Calibration + Calibration_error (RECOMMENDED)

---

#### 🟡 RQ6.10 (Lines 1171-1209)

**Line 1194: Logistic regression formula**

**Missing:**
- Random effects for UID? (items nested in people)
- Should use GLMM, not simple logistic regression

**Fix:**
```python
# USE GLMM (items nested in people)
import statsmodels.formula.api as smf

model = smf.mixedlm(
    "TQ_D6 ~ TC_D0",
    data=df_merged,
    groups=df_merged["UID"],
    family=sm.families.Binomial()  # For binary outcome
).fit()

# OR use pymer4 for cleaner syntax:
from pymer4.models import Lmer
model = Lmer("TQ_D6 ~ TC_D0 + (1 | UID)", data=df_merged, family='binomial')
model.fit()
```

---

### CHAPTER 7: Individual Differences

#### 🔴 RQ7.1 (Lines 1433-1498) - CRITICAL FILE PATH ISSUE

**Line 1448:**
```python
model = pickle.load(open('results/All by Domain/TQ_corr_noroom_2cats_p1_med_data_irt_Lin+Log.pkl', 'rb'))
```

**PROBLEMS:**
1. File name format incorrect. Should be:
   - `TQ_corr_noroom_2cats_p1_med_irt_summary.txt` (NOT .pkl!)
   - OR where are the pickled models stored?
2. No specification of which LMM model to load (Lin+Log assumed but not stated)
3. What if "Lin+Log" wasn't the best-fitting model?

**Fix:**
```python
# Step 1: Identify best model from AIC comparison
df_aic = pd.read_csv('results/All by Domain/TQ_corr_noroom_2cats_p1_med_irt_summary.txt', sep='\t')
best_model = df_aic.loc[df_aic['AIC'].idxmin(), 'Model']  # e.g., 'Lin+Log'

# Step 2: Load pickled model (IF IT EXISTS)
model_path = f'results/All by Domain/pkl/TQ_corr_noroom_2cats_p1_med_{best_model}.pkl'
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found: {model_path}")

model = MixedLMResults.load(model_path)

# Step 3: Extract random effects
random_effects = pd.DataFrame(model.random_effects).T
random_effects.columns = ['Intercept', 'Slope']
random_effects.reset_index(inplace=True)
random_effects.rename(columns={'index': 'UID'}, inplace=True)
```

**ALSO CRITICAL:** User needs to SAVE pickled models in irt.py! Currently unclear if this happens.

---

#### 🔴 RQ7.1 (Line 1456) - Data File Missing

**Line 1456:**
```python
df_cog = pd.read_csv('cog/cognitive_scores.csv')  # Hypothetical file
```

**Comment says "Hypothetical file"!**

**FIX:** Either:
1. Specify exact file structure required:
```markdown
**Cognitive Scores File Format:**

File: `cog/cognitive_scores.csv`

Columns:
- UID (str): Participant ID (e.g., 'A010')
- RAVLT_total (int): Sum of trials 1-5
- RAVLT_delayed (int): Delayed recall score
- BVMT_total (int): Sum of trials 1-3
- BVMT_delayed (int): Delayed recall score
- NART_correct (int): Number correct
- RPM_correct (int): Number correct (out of 12)
- Age (int): Years
- Sex (str): 'M' or 'F'
- Education_years (int): Years of education

**If this file doesn't exist, create it from df_data:**
```python
# Extract cognitive scores from master data
df_cog = df_data.groupby('UID').agg({
    'RAVLT_T1_T5_sum': 'first',  # Assumes constant per person
    'RAVLT_delayed': 'first',
    'BVMT_T1_T3_sum': 'first',
    'BVMT_delayed': 'first',
    'NART_correct': 'first',
    'RPM_correct': 'first',
    'Age': 'first',
    'Sex': 'first',
    'Education_years': 'first'
}).reset_index()

df_cog.to_csv('cog/cognitive_scores.csv', index=False)
```
```

OR:
2. Load directly from df_data

**DECISION NEEDED FROM USER:** Where are cognitive scores stored?

---

#### 🟡 RQ7.9 (Lines 1648-1689)

**Line 1670: Sobel test SE formula**

**CURRENT:**
```python
SE_indirect = sqrt(beta_A² * SE_B² + beta_B² * SE_A²)
```

**CORRECT (add covariance term if paths overlap):**
```python
SE_indirect = sqrt((beta_A ** 2) * (SE_B ** 2) + (beta_B ** 2) * (SE_A ** 2))
# Simplified formula assumes paths independent
```

**This is actually correct** for independent paths, but add note:
```markdown
**Note:** Sobel test assumes paths A and B are estimated independently. For more accurate SEs with small samples (n=100), bootstrap CIs preferred (see step 3).
```

---

## MISSING SECTIONS

### 🟡 MISSING-1: Assumption Diagnostics Procedure

**Add after line 1945:**
```markdown
### Detailed Assumption Checking Procedure

**For Every LMM:**

1. **Convergence**
   ```python
   print(model.summary())  # Check for convergence warnings
   assert model.converged == True, "Model did not converge!"
   ```

2. **Residual Normality**
   ```python
   import scipy.stats as stats
   import matplotlib.pyplot as plt

   residuals = model.resid
   stats.probplot(residuals, dist="norm", plot=plt)
   plt.title("Q-Q Plot")
   plt.show()

   # Shapiro-Wilk test (if n < 5000)
   stat, p = stats.shapiro(residuals)
   print(f"Shapiro-Wilk: W={stat:.3f}, p={p:.3f}")
   # NOTE: With large n, minor deviations may be significant but unimportant
   # Visual inspection of Q-Q plot more informative
   ```

3. **Homoscedasticity**
   ```python
   fitted = model.fittedvalues
   plt.scatter(fitted, residuals, alpha=0.5)
   plt.axhline(0, color='red', linestyle='--')
   plt.xlabel("Fitted Values")
   plt.ylabel("Residuals")
   plt.title("Residuals vs Fitted")
   plt.show()

   # Look for: No funnel pattern, points evenly scattered around 0
   ```

4. **Random Effects Normality**
   ```python
   re_df = pd.DataFrame(model.random_effects).T

   # Plot random intercepts
   plt.hist(re_df.iloc[:, 0], bins=20, edgecolor='black')
   plt.title("Distribution of Random Intercepts")
   plt.show()

   # Plot random slopes (if included)
   if re_df.shape[1] > 1:
       plt.hist(re_df.iloc[:, 1], bins=20, edgecolor='black')
       plt.title("Distribution of Random Slopes")
       plt.show()
   ```

5. **Outliers**
   ```python
   from statsmodels.stats.outliers_influence import OLSInfluence

   # Cook's distance (requires conversion to OLS for calculation)
   # Alternative: Manual outlier detection
   threshold = 3  # Standard deviations
   outliers = np.abs(residuals) > (threshold * residuals.std())
   print(f"Outliers detected: {outliers.sum()} ({100*outliers.mean():.1f}%)")

   # Flag for investigation (don't auto-remove)
   if outliers.sum() > 0:
       print("Outlier UIDs:", df[outliers]['UID'].unique())
   ```

6. **Multicollinearity (for regression models)**
   ```python
   from statsmodels.stats.outliers_influence import variance_inflation_factor

   # Prepare design matrix
   X = df[['RAVLT', 'BVMT', 'NART', 'RPM']].dropna()

   # Add constant
   X = sm.add_constant(X)

   # Calculate VIF
   vif_data = pd.DataFrame()
   vif_data["Variable"] = X.columns
   vif_data["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

   print(vif_data)
   # VIF > 10: Severe multicollinearity
   # VIF > 5: Moderate multicollinearity (investigate)
   ```

**Decision Rules:**
- Convergence failure → Try different optimizer, check for singularity
- Non-normal residuals but Q-Q R² > 0.95 → Acceptable (LMM robust to mild violations)
- Heteroscedasticity → Consider robust SEs or transformations
- Random effects variance = 0 → Remove that random effect (boundary issue)
- Outliers > 5% → Investigate (document, consider sensitivity analysis without outliers)
- VIF > 10 → Remove collinear predictors
```

---

### 🟡 MISSING-2: Reproducibility Checklist

**Add after line 1974:**
```markdown
### Reproducibility Checklist (Run BEFORE Each Analysis Session)

```python
# Set random seeds
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

# Verify reproducibility
print(f"Random seed set to: {SEED}")
print(f"NumPy random test: {np.random.rand()}")  # Should be 0.3745401188473625
```

**Documentation:**
- [ ] Git commit hash recorded for this analysis
- [ ] Package versions recorded (`pip freeze > requirements_frozen.txt`)
- [ ] Data file checksums verified (MD5)
- [ ] All models saved with timestamp and seed
```

---

### 🟡 MISSING-3: Data Validation Checks

**Add before Chapter 5:**
```markdown
### Data Validation (Run BEFORE Any Analysis)

```python
def validate_irt_data(df_ability, df_difficulty):
    """
    Validate IRT output files before using in LMM.

    Args:
        df_ability: DataFrame from *_data_ability.csv
        df_difficulty: DataFrame from *_data_difficulty.csv

    Raises:
        AssertionError if validation fails
    """

    # Check 1: Required columns exist
    required_ability = ['UID', 'Test', 'Days']  # + Theta_* columns
    required_difficulty = ['item_name', 'Difficulty', 'Overall_Discrimination']

    assert all(col in df_ability.columns for col in required_ability), \
        f"Missing columns in ability file: {set(required_ability) - set(df_ability.columns)}"

    assert all(col in df_difficulty.columns for col in required_difficulty), \
        f"Missing columns in difficulty file: {set(required_difficulty) - set(df_difficulty.columns)}"

    # Check 2: No missing theta values
    theta_cols = [col for col in df_ability.columns if col.startswith('Theta_')]
    assert df_ability[theta_cols].notna().all().all(), \
        "Missing theta values detected!"

    # Check 3: Days match expected values
    expected_days = [0, 1, 3, 6]
    actual_days = sorted(df_ability['Days'].unique())
    assert actual_days == expected_days, \
        f"Unexpected Days values: {actual_days} (expected {expected_days})"

    # Check 4: UIDs consistent across tests
    n_uid = df_ability['UID'].nunique()
    n_test = df_ability['Test'].nunique()
    expected_rows = n_uid * n_test
    actual_rows = len(df_ability)
    assert actual_rows == expected_rows, \
        f"Expected {expected_rows} rows ({n_uid} UIDs × {n_test} Tests), got {actual_rows}"

    # Check 5: Discrimination values in plausible range
    assert df_difficulty['Overall_Discrimination'].between(0.5, 4.0).all(), \
        "Discrimination values outside expected range (0.5-4.0)"

    # Check 6: Difficulty values in plausible range (typically -3 to +3)
    assert df_difficulty['Difficulty'].between(-5, 5).all(), \
        f"Extreme difficulty values detected: {df_difficulty['Difficulty'].describe()}"

    print("✓ Data validation passed")
    return True

# EXAMPLE USAGE:
df_ability = pd.read_csv('results/All by Domain/TQ_corr_noroom_2cats_p1_med_data_ability.csv')
df_difficulty = pd.read_csv('results/All by Domain/TQ_corr_noroom_2cats_p1_med_data_difficulty.csv')

validate_irt_data(df_ability, df_difficulty)
```
```

---

## SUMMARY OF REQUIRED ACTIONS

### CRITICAL (Must fix before ANY analysis)
1. ✅ Resolve utility inversion (CRITICAL-G5)
2. ✅ Specify exact TC_ IRT processing (CRITICAL-G3)
3. ✅ Fix probability transformation formula (HIGH-G4)
4. ✅ Add IRT analysis set specifications to all RQs (CRITICAL-G2)
5. ✅ Add success criteria to ALL RQs (CRITICAL-G1)
6. ✅ Fix RQ5.2 Day 1 overlap issue
7. ✅ Fix RQ5.12 discrimination column name
8. ✅ Fix RQ5.13 ICC formula
9. ✅ Fix RQ5.15 crossed random effects (needs pymer4)
10. ✅ Fix RQ6.1 probability transformation details
11. ✅ Fix RQ6.10 GLMM specification
12. ✅ Fix RQ7.1 file paths and model loading
13. ✅ Specify cognitive scores data source

### HIGH PRIORITY (Fix before starting analysis)
14. Add CTT convergence to all Chapter 6 RQs
15. Clarify Bonferroni application rules
16. Add model selection rules (ΔAIC thresholds)
17. Add decimal place specifications
18. Remove/clarify all "Same as RQ" references
19. Add assumption checking procedures
20. Add data validation functions

### MEDIUM PRIORITY (Improve before thesis writing)
21. Add reviewer rebuttals to all RQs
22. Add reproducibility checklist
23. Expand expected output sections (exact table columns)
24. Add sensitivity analysis notes where relevant

---

## RECOMMENDATION

**DO NOT PROCEED** with analyses until ALL CRITICAL issues resolved.

This document should be reviewed with user, decisions made, then analyses.md rewritten from scratch with zero ambiguity.

---

**END OF AUDIT**


---

## USER DECISIONS (2025-11-01) - ALL CRITICAL ISSUES RESOLVED

### ✅ DECISION 1: Calibration Nomenclature (was CRITICAL-G5)
**USER CHOICE:** Option A - Signed Calibration + Magnitude

**Implementation:**
```python
# Primary metric (direction)
Calibration = P_correct - P_high_conf
# Positive = Underconfident (accuracy > confidence)
# Negative = Overconfident (confidence > accuracy)
# Zero = Perfect calibration

# Secondary metric (magnitude)
Calibration_error = abs(Calibration)
# Lower = Better calibration, regardless of direction
```

**Rationale:** 
- Intuitive: Underconfidence is ABOVE zero (positive), overconfidence BELOW (negative)
- Removes all "×-1" inversions (source of confusion)
- Matches existing nomenclature in RQ6.2
- Allows analysis of BOTH direction and magnitude

**Action Items:**
- Remove all "Utility" references from Chapter 6
- Replace with "Calibration" and "Calibration_error"
- Update RQ6.5, 6.6, 6.12-6.15

---

### ✅ DECISION 2: TC_ IRT Processing (was CRITICAL-G3)
**USER CHOICE:** Identical to TQ_

**Implementation:**
- Same Q-matrix structure
- Same discrimination thresholds (0.5 ≤ discrim ≤ 4.0)
- Same iterative purification process
- Items may differ between TQ_ and TC_ (expected due to different response patterns)
- For calibration analyses: Use intersection of retained items from both models

**Rationale:** Enables direct P(correct) vs P(high_conf) comparison on same scale

---

### ✅ DECISION 3: Probability Transformation Discrimination (was HIGH-G4)
**USER CHOICE:** Factor-specific discrimination

**Implementation:**
```python
# For each factor (What, Where, When), use factor-specific discrimination
avg_discrim_factor = retained_items[f'Discrim_{factor}'].mean()
avg_difficulty = retained_items['Difficulty'].mean()

P_response = 1 / (1 + np.exp(-(avg_discrim_factor * (theta - avg_difficulty))))
```

**Theoretical Justification:** 
Factor-specific discrimination reflects how well items differentiate ability *on that specific dimension*. Using Overall_Discrimination would average across orthogonal factors (What/Where/When), diluting the signal. Since we're transforming domain-specific thetas, we should use domain-specific discrimination.

**Example:** 
- Item "TQ_IFR-N-i1" loads on "What" factor
- Use Discrim_What (e.g., 2.3) not Overall_Discrimination (e.g., average of 2.3, 0.8, 1.1 = 1.4)
- More accurate probability estimate for that factor

---

### ✅ DECISION 4: Data Source for Chapter 7 (was CRITICAL - RQ7.1)
**USER SPECIFICATION:** All data in master.xlsx extracted via variables.xlsx tag system

**Implementation:**
- dfData.csv already contains ALL variables needed (RAVLT, BVMT, NART, RPM, demographics)
- Use existing data pipeline (data/data.py startup())
- Never edit master.xlsx directly

**Action Items:**
- RQ7.1 loads from dfData.csv (already cached)
- No separate cognitive_scores.csv needed
- User will explain tag system after analysis bible complete

---

### ✅ DECISION 5: Model Pickling Strategy (was CRITICAL - RQ7.1)
**USER SPECIFICATION:** Fresh LMMs, no old pickle files

**Implementation:**
- RECOMPUTE=True → All LMMs re-run from scratch
- Save NEW pickles in irt.py for Chapter 7 random effects extraction
- LMM models must be saved as:
  - File: `results/{set}/pkl/{analysis_name}.pkl`
  - Method: `fit.save(model_path)` (statsmodels MixedLMResults.save())

**Code to add to irt.py (after LMM fitting):**
```python
# Save LMM model for later random effects extraction
import os
os.makedirs(f'results/{set_name}/pkl', exist_ok=True)
fit.save(f'results/{set_name}/pkl/{model_name}.pkl')
```

---

## STATUS: READY TO PROCEED

All critical issues resolved. Proceeding with complete rewrite of analyses.md with:
- Zero ambiguity
- Standardized schema (8 elements per RQ)
- Success criteria for every analysis
- Complete theoretical justifications
- Executable code specifications

---

