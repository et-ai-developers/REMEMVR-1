# LMM Methodology Reference

**Purpose:** Technical explanation of Linear Mixed Models implementation in REMEMVR.

**Audience:** Analysis-executor agent, results-inspector agent, statistics-expert agent.

**Last Updated:** 2025-01-04

---

## OVERVIEW

REMEMVR uses **Linear Mixed-Effects Models (LMMs)** to model longitudinal forgetting trajectories.

**Why LMM over Repeated-Measures ANOVA?**
- LMM handles unbalanced data (missing timepoints)
- LMM models continuous time (not just categorical)
- LMM allows participant-specific trajectories (random slopes)
- LMM provides better estimates for non-linear change

**Implementation:** Python `statsmodels.MixedLM`

---

## REMEMVR-SPECIFIC: IRT→LMM DATA FLOW

**CRITICAL:** REMEMVR LMM inputs come from IRT theta scores with composite_ID stacking.

### Upstream: IRT Phase
- 100 participants × 4 tests = 400 "pseudo-participants" (composite_ID stacking)
- Each composite_ID gets theta scores: A010_T1, A010_T2, A010_T3, A010_T4
- IRT treats each composite_ID as independent for calibration

### Data Reshaping for LMM
**Step 1:** Parse composite_ID
- A010_T1 → UID=A010, Test=T1

**Step 2:** Merge with TSVR (actual delay period)
- Extract from master.xlsx: `{UID}-RVR-{Test}-STA-X-TSVR`
- Merge on [UID, Test]
- Convert to days: TSVR_days = TSVR_hours / 24

**Step 3:** Reshape to long format
- Melt theta domains (What/Where/When) into single column
- Create Domain factor variable

### LMM Input Structure
```python
# Final LMM dataset: 400 composite_IDs × 3 domains = 1200 rows
lmm_input = pd.DataFrame({
    'composite_ID': ['A010_T1', 'A010_T1', 'A010_T1', ...],  # One per domain
    'UID': ['A010', 'A010', 'A010', ...],                     # Parsed from composite_ID
    'Test': ['T1', 'T1', 'T1', ...],                          # Parsed from composite_ID
    'TSVR_days': [0.02, 0.02, 0.02, ...],                     # Actual delay (hours/24)
    'Domain': ['What', 'Where', 'When', ...],                 # Melted from Theta_What/Where/When
    'Theta': [0.45, 0.30, 0.20, ...]                          # Outcome variable
})
```

**Grouping Variable:** `UID` (100 participants, not 400 composite_IDs)
- Random effects cluster by participant, not by composite_ID
- Each participant contributes 4 tests × 3 domains = 12 observations to LMM

**See Decision D070 in project_specific_stats_insights.md for complete pipeline.**

---

## MODEL SPECIFICATION

### General Form:

Y_ij = β₀ + β₁×Time_ij + ... + u₀j + u₁j×Time_ij + ε_ij

Where:
- Y_ij = Outcome (theta score) for participant j at timepoint i
- β₀, β₁, ... = Fixed effects (population-average parameters)
- u₀j = Random intercept for participant j
- u₁j = Random slope for participant j
- ε_ij = Residual error

---

## FIXED EFFECTS

### Time Coding:

**CRITICAL:** In REMEMVR, use **TSVR (Time Since VR)** - the ACTUAL hours/days since encoding, NOT nominal test days.

**TSVR_days:** TSVR_hours / 24 (actual delay period from VR encoding to test completion)

**Why TSVR, not nominal days (0, 1, 3, 6)?**
- Participants completed tests within windows (e.g., "Day 1" = 20-32 hours), not exact times
- T1/T2/T3/T4 are TEST LABELS, not time measurements
- Using nominal days introduces measurement error (ignores participant-level variance in test timing)
- TSVR provides precise delay period for each composite_ID (A010_T1 = 0.5 hours, A010_T2 = 27.2 hours, etc.)

**Data Source:**
- Extract from master.xlsx: `{UID}-RVR-{Test}-STA-X-TSVR`
- Merge with theta scores after parsing composite_ID
- Convert to days: TSVR_days = TSVR_hours / 24

**See Decision D070 in project_specific_stats_insights.md for complete IRT→LMM pipeline.**

**Advantages of TSVR:**
- Accurate delay period (reduces measurement error)
- Interpretable units (change per day)
- Continuous variable (allows flexible time modeling)

**Disadvantages:**
- Requires data extraction step (merge TSVR with theta scores)

### Time Transformations:

#### Days²: Quadratic time
**Use:** Models accelerating or decelerating change
**Formula:** `Days + I(Days**2)`

#### log(Days+1): Logarithmic time
**Use:** Models rapid initial change, then plateau (classic forgetting curve)
**Formula:** `np.log(Days+1)`

**Why +1?** log(0) undefined, so log(0+1) = 0 at baseline.

#### Combined: Linear + Log
**Use:** Flexible model capturing both linear and logarithmic trends
**Formula:** `Days + np.log(Days+1)`

**Default in REMEMVR:** Lin+Log model.

### Categorical Predictors:

**Factor (Domain/Paradigm/Congruence):**
- Coded as categorical with reference group
- Syntax: `C(Factor, Treatment("Reference"))`

**Example:**
```python
formula = "Theta ~ (Days + np.log(Days+1)) * C(Domain, Treatment('What'))"
```

**Interpretation:**
- Main effect of Domain: Difference at baseline
- Interaction Domain×Days: Difference in forgetting rate

---

## RANDOM EFFECTS

### Random Intercepts:
**Model:** `~ 1`

**Interpretation:** Each participant has their own baseline ability (shift up/down).

**When to use:** Always include (accounts for between-person variability).

### Random Slopes:
**Model:** `~ Days` or `~ Days + np.log(Days+1)`

**Interpretation:** Each participant has their own forgetting rate.

**When to use:**
- When forgetting rates vary substantially across people
- Test via likelihood ratio test (LRT)

**Trade-off:** More parameters to estimate → need sufficient data.

---

## MODEL COMPARISON

### Candidate Models (for RQ 5.7):

1. **Linear:** `Theta ~ Days`
2. **Quadratic:** `Theta ~ Days + I(Days**2)`
3. **Logarithmic:** `Theta ~ np.log(Days+1)`
4. **Lin+Log:** `Theta ~ Days + np.log(Days+1)` ← Default
5. **Quad+Log:** `Theta ~ Days + I(Days**2) + np.log(Days+1)`

### Selection Criteria:

#### AIC (Akaike Information Criterion):
**Formula:** AIC = -2×log-likelihood + 2×k

Where k = number of parameters.

**Lower AIC = better model**

**Use:** Balances fit vs complexity.

#### ΔAIC:
**Definition:** Difference from best model (AIC - AIC_min)

**Interpretation:**
- ΔAIC < 2: Substantial support
- ΔAIC 4-7: Considerably less support
- ΔAIC > 10: Essentially no support

#### Akaike Weights:
**Formula:** w_i = exp(-ΔAIC_i / 2) / Σ exp(-ΔAIC_j / 2)

**Interpretation:** Probability that model i is the best model in the set.

**Use:** Model averaging, evidence for best model.

### Likelihood Ratio Test (LRT):

**Use:** Compare nested models.

**Formula:** χ² = -2×(log-likelihood_restricted - log-likelihood_full)
- df = difference in number of parameters
- p-value from chi-square distribution

**Example:** Test if random slopes improve fit over intercepts-only.

**IMPORTANT:** Only valid for nested models fit with REML=False (maximum likelihood).

---

## STATSMODELS SYNTAX

### Basic LMM:
```python
import statsmodels.formula.api as smf

model = smf.mixedlm(
    formula="Theta ~ Days",
    data=df,
    groups=df["UID"],
    re_formula="~ Days"
)

result = model.fit(reml=False)
print(result.summary())
```

### Parameters:

#### formula
R-style formula for fixed effects.

**Examples:**
- `"Theta ~ Days"` = Simple linear
- `"Theta ~ Days + np.log(Days+1)"` = Lin+Log
- `"Theta ~ Days * C(Domain, Treatment('What'))"` = Domain × Time interaction

#### data
Long-format dataframe with:
- Outcome column (Theta)
- Time column (Days)
- Grouping column (UID)
- Factor columns (Domain, etc.)

#### groups
Column defining independent groups (typically UID for participants).

#### re_formula
Random effects formula.

**Examples:**
- `"~ 1"` = Random intercepts only
- `"~ Days"` = Random intercepts + random slopes for Days
- `"~ Days + np.log(Days+1)"` = Random effects for both time terms

#### reml
Boolean, use Restricted Maximum Likelihood (REML)?

**REML=True (default):** Better for small samples, but can't compare models with different fixed effects via AIC.

**REML=False:** Required for AIC-based model comparison.

---

## EXTRACTING RESULTS

### Fixed Effects Table:
```python
result.summary().tables[1]
```

**Columns:**
- Coef: β estimate
- Std.Err: Standard error
- z: z-statistic
- P>|z|: p-value
- [0.025, 0.975]: 95% confidence interval

### Random Effects Variance:
```python
result.cov_re
```

**Interpretation:**
- Variance of random intercepts: σ²_u0
- Variance of random slopes: σ²_u1
- Correlation between intercepts and slopes

### Residual Variance:
```python
result.scale
```

**Interpretation:** σ²_ε (within-person variability)

### ICC (Intraclass Correlation):
**Formula:** ICC = σ²_u0 / (σ²_u0 + σ²_ε)

**Interpretation:** Proportion of variance between-person vs within-person.

**High ICC (>0.5):** Most variability is between people (justify random effects).

### BLUPs (Best Linear Unbiased Predictors):
```python
result.random_effects
```

**Returns:** Dictionary with participant-specific random effects.

**Use:** Extract individual intercepts/slopes for further analysis (e.g., regress on cognitive tests).

### Predicted Values:
```python
result.predict()  # Population-level (fixed effects only)
result.fittedvalues  # Subject-specific (fixed + random effects)
```

---

## ASSUMPTIONS

### 1. Linearity
**Definition:** Relationship between predictors and outcome is linear (on link scale).

**Check:** Residuals vs fitted plot (should be flat, no patterns).

**Solution if violated:** Add polynomial terms or transform outcome.

### 2. Normality of Residuals
**Definition:** ε_ij ~ Normal(0, σ²)

**Check:** Q-Q plot of residuals.

**Solution if violated:** Often robust to moderate violations. Consider transformation.

### 3. Normality of Random Effects
**Definition:** u_j ~ Normal(0, Σ)

**Check:** Q-Q plot of random effects.

**Solution if violated:** May need non-parametric bootstrap for inference.

### 4. Homoscedasticity
**Definition:** Residual variance is constant across fitted values and time.

**Check:** Residuals vs fitted plot (spread should be constant).

**Solution if violated:** Weighted regression or heteroscedastic variance structure.

### 5. Independence
**Definition:** Observations from different participants are independent.

**Check:** No clustering beyond what's modeled.

**In REMEMVR:** Composite_ID stacking violates strict independence (same person across 4 tests). Trade-off accepted for increased sample size.

---

## DIAGNOSTICS

### Residual Plots:

#### Residuals vs Fitted:
**Check:** No systematic patterns (should be cloud around zero).

**Issues:**
- Funnel shape → Heteroscedasticity
- Curved pattern → Non-linearity

#### Q-Q Plot:
**Check:** Points fall on diagonal line.

**Issues:**
- Heavy tails → Non-normality
- S-shape → Skewness

#### Scale-Location Plot:
**Check:** Constant spread across fitted values.

**Issues:** Upward/downward trend → Heteroscedasticity

### Influence Diagnostics:

#### Cook's Distance:
**Check:** No observations with excessive influence.

**Threshold:** > 4/n (where n = sample size)

**Action:** Investigate influential cases, consider sensitivity analysis.

#### Leverage:
**Check:** No observations with extreme predictor values.

**Action:** High leverage + high residual = influential.

---

## INTERACTION EFFECTS

### Domain × Time Interaction:

**Formula:** `Theta ~ (Days + np.log(Days+1)) * C(Domain, Treatment("What"))`

**Interpretation:**
- **Main effect of Domain:** Difference at baseline (Day 0)
- **Interaction Domain×Days:** Difference in linear forgetting rate
- **Interaction Domain×log(Days+1):** Difference in logarithmic forgetting rate

**Testing:**
- Wald test on interaction terms
- LRT comparing model with vs without interaction

**Visualization:** Plot predicted trajectories per domain.

### Continuous × Time Interaction:

**Example:** `Theta ~ (Days + np.log(Days+1)) * Age`

**Interpretation:**
- **Age:** Effect at baseline
- **Age×Days:** How forgetting rate changes with age

**Centering:** Mean-center Age to make main effects interpretable.

---

## BEST PRACTICES

### 1. Start Simple:
Fit random-intercepts model first, then add random slopes if LRT significant.

### 2. Use REML=False for Model Comparison:
AIC comparison requires ML estimation.

### 3. Check Convergence:
Ensure model converged (check warnings).

**Action if not converged:**
- Rescale variables
- Simplify random effects structure
- Increase max iterations

### 4. Report Multiple Models:
Don't just report best AIC model. Show comparison table with ΔAIC and weights.

### 5. Validate Assumptions:
Always check diagnostic plots before interpreting results.

---

## COMMON PITFALLS

### 1. Ignoring Random Slopes:
**Issue:** Underestimates variability in forgetting rates.

**Solution:** Test random slopes via LRT.

### 2. Using REML for Model Comparison:
**Issue:** AIC not comparable across models with different fixed effects.

**Solution:** Fit with REML=False for AIC comparison.

### 3. Overfitting:
**Issue:** Too many parameters for sample size.

**Solution:** Simplify random effects or fixed effects if convergence issues.

### 4. Not Centering:
**Issue:** Main effects uninterpretable when interaction present.

**Solution:** Mean-center continuous predictors.

### 5. Forgetting to Check Assumptions:
**Issue:** Invalid inference if assumptions violated.

**Solution:** Always generate diagnostic plots.

---

## OUTPUT FILES (REMEMVR)

### Model Pickle (.pkl):
Saved fitted MixedLM result object.

**Use:** Load for further analysis, prediction, diagnostics.

### Fixed Effects CSV:
Table with:
- Term
- β estimate
- SE
- z-statistic
- p-value
- 95% CI

**Use:** Report in thesis, compare across RQs.

### Summary TXT:
Full model summary including:
- Fixed effects table
- Random effects variances
- Model fit statistics (AIC, BIC, log-likelihood)
- Convergence status

**Use:** Comprehensive model documentation.

### AIC Comparison CSV:
For multiple models:
- Model name
- AIC
- ΔAIC
- Akaike weight
- Convergence status

**Use:** Select best model, report evidence.

---

## REFERENCES

- Fitzmaurice, G. M., Laird, N. M., & Ware, J. H. (2011). *Applied Longitudinal Analysis* (2nd ed.). Wiley.
- Singer, J. D., & Willett, J. B. (2003). *Applied Longitudinal Data Analysis*. Oxford University Press.
- Bates, D., Mächler, M., Bolker, B., & Walker, S. (2015). Fitting linear mixed-effects models using lme4. *Journal of Statistical Software, 67*(1), 1-48.
- statsmodels documentation: https://www.statsmodels.org/stable/mixed_linear.html

---

**End of LMM Methodology Reference**
