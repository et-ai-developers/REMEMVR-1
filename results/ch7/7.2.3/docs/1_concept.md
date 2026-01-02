# RQ 7.2.3: Age x Cognitive Test Interaction

**Chapter:** 7
**Type:** Age x VR Scaffolding
**Subtype:** Attenuation Analysis
**Full ID:** 7.2.3

---

## Research Question

**Primary Question:**
Do cognitive tests predict REMEMVR differently for younger vs older adults? Tests may be better predictors in older adults if they tap compensatory processes.

**Scope:**
This RQ examines Age x Cognitive Test interactions across 100 participants using mean theta_all scores from Ch5 as the dependent variable. Tests individual interactions for RAVLT, BVMT, NART, and RPM cognitive assessments. Uses continuous age variable and standardized cognitive test scores.

**Theoretical Framing:**
Formally tests whether cognitive ability predicts VR memory performance differently across the age spectrum. If cognitive tests show stronger prediction in older adults, this supports compensatory processing models where crystallized abilities become more important with age.

---

## Theoretical Background

**Relevant Theories:**
- **Cognitive Reserve Theory** (Stern, 2002): High-ability older adults compensate for neural decline through alternative processing strategies. Tests may show stronger prediction in older adults who rely more on crystallized abilities.
- **VR Scaffolding Hypothesis**: Environmental support in VR may reduce age-related variance, potentially altering age x ability interactions seen in traditional testing.

**Key Citations:**
Stern, Y. (2002). What is cognitive reserve? Theory and research application of the reserve concept. Journal of the International Neuropsychological Society, 8(3), 448-460.

**Theoretical Predictions:**
Possible Age x Test interaction where tests predict REMEMVR more strongly in older adults. Alternatively, VR scaffolding may eliminate age differences in predictive utility, showing no interaction.

**Literature Gaps:**
Limited research on age x ability interactions in VR environments. Traditional tests show age-related changes in factor structure, but VR's environmental support may alter these patterns.

---

## Hypothesis

**Primary Hypothesis:**
Possible Age x Test interaction where tests predict REMEMVR more strongly in older adults. Alternatively, no interaction (tests predict equally across age range).

**Secondary Hypotheses:**
If interactions emerge, they should be strongest for fluid abilities (RPM) and weakest for crystallized abilities (NART), consistent with age-related cognitive changes.

**Theoretical Rationale:**
Cognitive reserve theory predicts that high-ability older adults rely more heavily on compensatory strategies. If VR memory performance requires such compensation in older adults, cognitive tests should show stronger predictions with age. However, VR scaffolding may reduce this need.

**Expected Effect Pattern:**
Age x Test interaction terms may reach significance. If significant, simple slopes analysis should show stronger test prediction in older participants. Effect sizes likely small to moderate (² = 0.08-0.20 for interaction terms).

---

## Memory Domains

**Domains Examined:**

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
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains. This provides a comprehensive measure of VR memory performance for testing cognitive test interactions.

**Exclusion Rationale:**
No domain-specific exclusions. Analysis focuses on overall VR memory performance rather than domain-specific patterns.

---

## Analysis Approach

**Power Analysis:**
- Sample size: N=100 with k predictors
- Post-hoc power for medium effects (f²=0.15): Approximately 80%
- Minimum detectable effect: f²=0.10 with current sample
- Limitation acknowledged: Underpowered for small effects (f²<0.10)


**Analysis Type:**
Multiple regression with interaction terms and simple slopes analysis

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load mean theta_all scores from Ch5 5.1.1 results
- Extract cognitive tests from master.xlsx (RAVLT, BVMT, NART, RPM)
- Center predictors: Age_c = Age - mean(Age), Test_c = Test - 50
- Check data quality and compute descriptive statistics

**Step 2:** Center predictors and create interactions
- Age_c = Age - mean(Age) for interpretation
- RAVLT_c = RAVLT_T - 50 (already T-scored)
- Create interaction terms: Age_c × RAVLT_c, Age_c × BVMT_c, etc.

**Step 3:** Fit interaction models
- Model: Theta ~ Age_c + Test_c + Age_c:Test_c
- Test interaction term significance with dual p-value reporting
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni (± = 0.00179/4 = 0.000448)

**Step 4:** Simple slopes analysis (if interactions significant)
- Compute test slope at Age = -1SD (younger adults)
- Compute test slope at Age = +1SD (older adults)
- Test significance of simple slopes
- Create interaction plots for visualization

**Step 5:** Effect sizes and model diagnostics
- Standardized betas with 95% confidence intervals
- Cohen's f² for interaction terms
- VIF check for multicollinearity
- Residual diagnostics (normality, homoscedasticity)

**Step 6:** bootstrap (1000 replications, seed=42) confidence intervals
- 1000 bootstrap (1000 replications, seed=42) samples for interaction coefficients
- Robust confidence intervals for effect sizes
- Assess stability of interaction effects

**Step 7:** Cross-validation
- 5-fold cross-validation for model stability
- Compare interaction effect consistency across folds
- Test generalizability of age x test patterns

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Include model diagnostics (VIF, residuals, homoscedasticity)
- Include bootstrap (1000 replications, seed=42) CIs for non-normal interaction distributions
- Include effect sizes with 95% CIs (², f², sr²)

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted and centered test scores)
- data/step02_theta_means.csv (mean theta per participant from Ch5)
- data/step03_analysis_input.csv (merged dataset with interaction terms)
- data/step04_interaction_results.csv (coefficients with dual p-values)
- data/step05_simple_slopes.csv (if interactions significant)
- data/step06_effect_sizes.csv (², f², sr² with 95% CIs)
- data/step07_bootstrap (1000 replications, seed=42)_CIs.csv (robust confidence intervals)
- data/step08_cross_validation.csv (k-fold CV results)
- results/interaction_summary.md (text summary for thesis)
- plots/interaction_plots.png (Age x Test visualizations)
- plots/diagnostic_plots.png (residuals, Q-Q, influence)

**Success Criteria:**
- Age x Test interactions tested for all 4 cognitive tests
- Report which interactions are significant (if any)
- If significant, provide simple slopes interpretation with effect sizes
- VIF < 5 for all predictors (no multicollinearity)
- Residuals normally distributed (Shapiro-Wilk p > 0.05)
- Cross-validation confirms interaction stability
- bootstrap (1000 replications, seed=42) CIs exclude zero for significant interactions

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates)
- data/cache/master.xlsx (cognitive test scores)

**Dependencies:**
Ch5 5.1.1 must complete IRT calibration and theta score generation before this RQ can run.

**Cognitive Test Variables (master.xlsx):**
- RAVLT: Verbal episodic memory (T-scores)
- BVMT: Visuospatial memory (T-scores)  
- NART: Crystallized intelligence (T-scores)
- RPM: Fluid intelligence (T-scores)

**Age Variable:**
- Age: Continuous variable from demographics (master.xlsx)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete cognitive test data
- [ ] Exclude: Participants missing cognitive test scores

**Variables:**
- [x] Mean theta_all scores from Ch5 5.1.1
- [x] All 4 cognitive tests (RAVLT, BVMT, NART, RPM)
- [x] Age as continuous predictor

**Tests:**
- N/A (uses aggregated theta scores, not individual test sessions)

---