# Ch7 RQ_CONCEPT GUIDELINES

**Purpose:** Ch7-specific instructions for rq_concept agent
**Created:** 2026-01-02
**CRITICAL:** Read this BEFORE creating any Ch7 1_concept.md file

---

## Ch7 UNIQUE CHARACTERISTICS

### 1. Data Sources
Ch7 RQs are almost ALL **DERIVED** from Ch5/Ch6 outputs:
- Theta scores from Ch5 RQs (5.1.1, 5.2.x, 5.3.x, etc.)
- Confidence/calibration from Ch6 RQs (6.1.x, 6.2.x, 6.6.x)
- Cognitive tests from master.xlsx (NOT dfData.csv)

### 2. Primary Analysis Type
Most Ch7 RQs use **Multiple Regression** or **Hierarchical Regression**:
- DVs: REMEMVR theta scores (from Ch5/Ch6)
- IVs: Cognitive tests (RAVLT, BVMT, NART, RPM)
- Covariates: Age, Education, DASS, Sleep

### 3. Cross-Sectional Design
Ch7 is CROSS-SECTIONAL prediction:
- Cognitive tests (baseline) → REMEMVR performance
- NOT longitudinal (no time × predictor interactions)
- Some RQs examine slope prediction (individual differences in forgetting)
- Requires cross-validation for predictive models

---

## CRITICAL RULES FOR 1_CONCEPT.MD

### File Organization (MANDATORY)
```
✓ data/step##_*.csv         # ALL CSV outputs go here
✓ results/*.md or *.txt      # Summary documents ONLY
✓ plots/*.png                # Visualizations
✗ results/step##_*.csv       # WRONG - CSVs never in results/
```

### Character Encoding
- Use "R²" or "R-squared" (NOT "R�" which is corrupted)
- Use UTF-8 encoding consistently

### Placeholder Text
- DO NOT write "[To be added by rq_scholar]" 
- DO NOT write "[To be identified by rq_scholar]"
- Leave sections blank if content unknown

### Domain Specifications
For Ch7 omnibus analyses (e.g., 7.1.1):
```markdown
- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall theta_all scores

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall theta_all scores

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall theta_all scores

**Inclusion Rationale:**
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains
```

### Data Source Section
For Ch7 DERIVED data (most RQs):
```markdown
## Data Source

**Data Type:**
DERIVED (from Ch5 X.Y.Z outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 X.Y.Z (specify which RQ provides theta scores)

**File Paths:**
- results/ch5/X.Y.Z/data/step03_theta_scores.csv
- data/cache/master.xlsx (cognitive test scores)

**Dependencies:**
Ch5 X.Y.Z must complete before this RQ can run
```

---

## CH7-SPECIFIC TAG PATTERNS

From specs.md Methodological Framework (lines 86-194):

### Cognitive Tests (master.xlsx)
```
RAVLT: {UID}-COG-X-RAV-T1Sc through T5Sc, DRSc, FRSc
BVMT: {UID}-COG-X-BVM-TotR, {UID}-COG-X-BVM-TDSc
NART: {UID}-COG-X-NAR-Scor
RPM: {UID}-COG-X-RPM-Scor
```

### Demographics (master.xlsx)
```
Age: {UID}-DEM-X-Age
Sex: {UID}-DEM-X-Sex
Education: {UID}-DEM-X-Education
VR_Experience: {UID}-DEM-X-VR_Exp
Sleep: {UID}-DEM-X-SLEEP
```

### DASS-21 (master.xlsx)
```
Depression: {UID}-DEM-X-DASS_Dep
Anxiety: {UID}-DEM-X-DASS_Anx
Stress: {UID}-DEM-X-DASS_Str
```

---

## MULTIPLE COMPARISONS & P-VALUE REPORTING (Decision D068)

### MANDATORY: Dual P-Value Reporting
ALL Ch7 RQs must report BOTH:
1. **Uncorrected p-values** - Raw statistical significance
2. **Corrected p-values** - After multiple comparison adjustment

### Correction Methods (in order of preference):
1. **Bonferroni** - Conservative, use when few comparisons (k < 10)
   - Ch7 family-wise: α = 0.05/28 = 0.00179
   - Per-predictor (4 tests): α = 0.00179/4 = 0.000448
2. **FDR (False Discovery Rate)** - Less conservative, use for many comparisons
3. **Holm-Bonferroni** - Sequential, slightly less conservative than Bonferroni

### Example for Analysis Approach:
```markdown
**Step 3:** Test individual predictors
- Extract standardized beta coefficients with 95% CIs
- Compute semi-partial correlations (sr²) for unique variance
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni (α = 0.00179/4 = 0.000448)
- Secondary: FDR correction for comparison
```

---

## EFFECT SIZE & POWER REPORTING

### MANDATORY Effect Sizes for Ch7:
1. **R² and Adjusted R²** - Overall model fit
2. **Cohen's f²** - Effect size for regression: f² = R²/(1-R²)
3. **Standardized betas (β)** - With 95% confidence intervals
4. **Semi-partial correlations (sr²)** - Unique variance explained
5. **Cohen's d** - For pairwise comparisons

### Power Analysis Requirements:
```markdown
**Step 6:** Power Analysis
- Post-hoc power for observed effect sizes
- Sensitivity analysis: smallest detectable effect at 80% power
- Sample size adequacy for number of predictors (N/k ratio)
```

---

## EXPECTED OUTPUT FORMAT

For Ch7 regression analyses:
```markdown
**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted test scores)
- data/step02_theta_means.csv (mean theta per participant)
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_regression_results.csv (coefficients, CIs, dual p-values)
- data/step05_model_diagnostics.csv (VIF, residuals, Cook's D)
- data/step06_effect_sizes.csv (R², f², sr², with 95% CIs)
- data/step07_cross_validation.csv (k-fold CV results)
- data/step08_power_analysis.csv (post-hoc and sensitivity)
- results/regression_summary.md (text summary for thesis)
- plots/diagnostic_plots.png (residuals, Q-Q, homoscedasticity)
- plots/predictor_importance.png (visualization)
```

---

## MODEL DIAGNOSTICS & VALIDATION

### MANDATORY Diagnostic Checks:
```markdown
**Step 5:** Model Diagnostics
- Multicollinearity: VIF < 5 for all predictors
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test, residual vs fitted plot
- Influential points: Cook's D < 4/N threshold
- Outliers: Standardized residuals within ±3
```

### Cross-Validation Requirements:
```markdown
**Step 7:** Cross-Validation
- Method: k-fold CV (k=5 or 10) OR 70/30 train-test split
- Metrics: RMSE, MAE, R² on test set
- Report: Training vs test performance gap
- Check: Overfitting if test R² << training R²
```

---

## SUCCESS CRITERIA TEMPLATE

For Ch7 predictive validity RQs:
```markdown
**Success Criteria:**
- [ ] Model explains significant variance (p < 0.00179)
- [ ] R² between 0.25 and 0.50 (convergent but not redundant)  
- [ ] At least one episodic test significant after Bonferroni
- [ ] Residual > 50% (substantial unique REMEMVR variance)
- [ ] VIF < 5 for all predictors (no multicollinearity)
- [ ] Residuals normally distributed (Shapiro-Wilk p > 0.05)
- [ ] Homoscedasticity confirmed (Breusch-Pagan p > 0.05)
- [ ] No influential outliers (Cook's D < 4/N)
- [ ] Cross-validation R² within 10% of training R²
- [ ] Power > 0.80 for medium effect (f² = 0.15)
```

---

## HIERARCHICAL REGRESSION & MODEL COMPARISONS

### For Testing Incremental Validity:
```markdown
**Step 4:** Hierarchical Regression
- Model 1: Demographics only (Age, Sex, Education)
- Model 2: + Cognitive tests (RAVLT, BVMT, NART, RPM)
- Model 3: + Additional predictors (if applicable)
- Report: ΔR² and significance test for each step
- Test: F-test for R² change between nested models
```

### Sensitivity Analyses:
```markdown
**Step 8:** Sensitivity Analyses
- Exclude potential outliers, rerun analysis
- Try robust regression (Huber, RANSAC) if outliers present
- Bootstrap CIs (1000 iterations) for non-normal distributions
- Alternative corrections: Compare Bonferroni vs FDR results
- Missing data: Compare complete case vs imputation (if applicable)
```

---

## STANDARD CH7 ANALYSIS WORKFLOW TEMPLATE

Use this template for all Ch7 regression analyses:

```markdown
## Analysis Approach

**Analysis Type:**
Multiple regression with hierarchical entry and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load theta scores from Ch5/Ch6 results
- Extract cognitive tests from master.xlsx
- Compute derived scores and standardize to T-scores
- Check data quality and missingness

**Step 2:** Hierarchical regression
- Model 1: Demographics only (Age, Sex, Education)
- Model 2: + Cognitive tests (RAVLT, BVMT, NART, RPM)
- Report ΔR² and F-test for model improvement

**Step 3:** Test individual predictors
- Extract standardized betas with 95% CIs
- Compute semi-partial correlations (sr²)
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary: Bonferroni (α = 0.00179/k)
- Secondary: FDR for comparison

**Step 4:** Effect sizes and importance
- Cohen's f² = R²/(1-R²)
- Dominance analysis or relative weights
- Bootstrap CIs (1000 iterations)

**Step 5:** Model diagnostics
- Multicollinearity: VIF < 5
- Residual normality: Shapiro-Wilk test, Q-Q plot
- Homoscedasticity: Breusch-Pagan test
- Influential points: Cook's D < 4/N

**Step 6:** Cross-validation
- Method: 5-fold CV
- Metrics: Test R², RMSE, MAE
- Check for overfitting

**Step 7:** Power analysis
- Post-hoc power for observed effects
- Sensitivity: smallest detectable effect at 80% power

**Step 8:** Sensitivity analyses
- Exclude outliers, rerun
- Try robust regression if needed
- Compare Bonferroni vs FDR results
```

---

## WORKFLOW INSTRUCTIONS

1. **Read specs.md TOC** (lines 1-80) to find your RQ line number
2. **Read File Organization** (lines 86-119) for folder structure
3. **Read Methodological Framework** (lines 121-194) for data sources
4. **Read your specific RQ** using TOC line number
5. **Use the Standard Ch7 Analysis Workflow Template** as your base
6. **Adapt the template** to your specific RQ requirements
7. **Create 1_concept.md** following ALL rules above
8. **Update status.yaml** with success and context_dump

---

## COMMON ERRORS TO AVOID

1. ❌ Putting CSV files in results/ folder
2. ❌ Using corrupted R� instead of R²
3. ❌ Including placeholder text like "[To be added]"
4. ❌ Only reporting corrected p-values (MUST report both)
5. ❌ Missing effect sizes with confidence intervals
6. ❌ No model diagnostics (residuals, VIF, etc.)
7. ❌ No cross-validation for predictive models
8. ❌ No power analysis for null findings
9. ❌ No hierarchical regression for incremental validity
10. ❌ Missing sensitivity analyses
11. ❌ Not specifying DERIVED data sources correctly
12. ❌ Confusing longitudinal with cross-sectional design

---

**END OF GUIDELINES**