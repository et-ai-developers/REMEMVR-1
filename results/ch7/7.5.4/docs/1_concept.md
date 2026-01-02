# RQ 7.5.4: Per-Test Sleep Effects on Same-Test Performance

**Chapter:** 7
**Type:** Self-Report & Contextual
**Subtype:** Within-Person Sleep Variation Analysis
**Full ID:** 7.5.4

---

## Research Question

**Primary Question:**
Does sleep quality BEFORE each test predict THAT test's performance, demonstrating within-person state-dependent sleep effects?

**Scope:**
This RQ examines within-person sleep variability across the four REMEMVR test sessions. Uses 400 observations (100 participants × 4 tests) where each participant provides sleep data before each test (T1, T2, T3, T4). Tests state-dependent effects of sleep hours and sleep quality on same-test episodic memory performance.

**Theoretical Framing:**
Novel longitudinal approach to sleep-memory relationships by decomposing within-person (state) vs between-person (trait) sleep effects. Most research examines between-person correlations; this design allows causal inference about acute sleep impacts on memory retrieval.

---

## Theoretical Background

**Relevant Theories:**
- **Sleep-Memory Consolidation Theory**: Sleep deprivation impairs memory retrieval acutely through disrupted hippocampal function and attention networks
- **State-Dependent Performance Theory**: Acute physiological states (sleep quality, alertness) affect cognitive performance beyond stable trait differences

**Key Citations:**

**Theoretical Predictions:**
Sleep-memory theories predict that poor sleep before a specific test should impair that test's performance through reduced attention, working memory capacity, and hippocampal function. Within-person analysis isolates acute sleep effects from individual differences in chronic sleep patterns.

**Literature Gaps:**
Most sleep-memory research uses between-person designs (comparing good vs poor sleepers). Per-test sleep data allows within-person analysis to test state-dependent effects while controlling for trait sleep quality.

---

## Hypothesis

**Primary Hypothesis:**
Poor sleep before a specific test will impair that test's performance (within-person effect), independent of individual differences in overall sleep quality.

**Secondary Hypotheses:**
Within-person sleep effects will be stronger than between-person sleep differences, demonstrating state-dependent rather than trait-dependent sleep-memory relationships.

**Theoretical Rationale:**
Sleep deprivation acutely impairs hippocampal function and attention networks required for episodic memory retrieval. Per-test design allows isolation of acute sleep effects from confounding individual differences.

**Expected Effect Pattern:**
Significant positive within-person effects of sleep hours and sleep quality on theta scores. Effect sizes expected: beta = 0.05-0.10 for hours, beta = 0.08-0.15 for quality, with p-values < 0.05 after correction.

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
Uses omnibus theta_all scores from Ch5 that aggregate across all episodic memory domains. Sleep effects expected to impact all domains through general attention and hippocampal mechanisms rather than domain-specific processes.

**Exclusion Rationale:**
Domain-specific analysis not appropriate for sleep research question. Sleep deprivation affects general cognitive resources rather than specific episodic memory domains.

---

## Analysis Approach

**Analysis Type:**
Multilevel modeling (mixed effects regression) with within-person sleep predictors and cross-validation

**High-Level Workflow:**

**Step 1:** Extract and prepare per-test sleep data
- Load sleep hours and quality data from master.xlsx (SLP tags)
- Extract per-test sleep: `{UID}-RVR-T{N}-SLP-X-HOUR-` and `{UID}-RVR-T{N}-SLP-X-QUAL-`
- Merge with per-test theta scores from Ch5
- Create 400-row dataset (100 UIDs × 4 tests)

**Step 2:** Descriptive analysis and data quality
- Check within-person sleep variability (SD within each UID)
- Examine missing data patterns and outliers
- Compute person-mean sleep variables for decomposition

**Step 3:** Fit multilevel models
- Model 1: `Theta ~ Hours_Slept + Sleep_Quality + (1|UID)` (within-person only)
- Model 2: Add person-mean sleep variables for between-person effects
- Use REML estimation for variance component accuracy

**Step 4:** Model diagnostics and assumptions
- Check residual normality (Q-Q plot, Shapiro-Wilk test)
- Test homoscedasticity (residual vs fitted plot)
- Examine influential observations (Cook's D)
- Check multicollinearity between sleep variables (VIF)

**Step 5:** Effect decomposition and interpretation
- Decompose within-person vs between-person sleep variance
- Compute standardized effect sizes for sleep predictors
- Test significance with BOTH uncorrected AND corrected p-values (Decision D068)

**Step 6:** Cross-validation and robustness
- 5-fold cross-validation to test model generalizability
- Sensitivity analysis: exclude potential outliers
- Bootstrap confidence intervals for effect sizes

**Step 7:** Power analysis and clinical significance
- Post-hoc power for observed within-person effects
- Interpret effect sizes in context of sleep intervention potential
- Compare effect sizes to between-person sleep correlations

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Include model diagnostics step (VIF, residuals, homoscedasticity)
- Include cross-validation for predictive models
- Include power analysis for null findings
- Include effect sizes with 95% CIs (R², f², sr², ²)

**Expected Outputs:**
- data/step01_per_test_sleep.csv (extracted sleep data per test)
- data/step02_theta_sleep_merged.csv (400 rows: UID × Test × Sleep × Theta)
- data/step03_descriptive_stats.csv (within-person sleep variability)
- data/step04_multilevel_model_results.csv (fixed effects, random effects)
- data/step05_effect_decomposition.csv (within vs between person effects)
- data/step06_model_diagnostics.csv (residuals, VIF, Cook's D)
- data/step07_cross_validation.csv (CV performance metrics)
- data/step08_bootstrap_CIs.csv (bootstrapped confidence intervals)
- results/sleep_effects_summary.md (text summary for thesis)
- plots/within_person_sleep_effects.png (visualization)
- plots/model_diagnostics.png (residual plots)

**Success Criteria:**
- Successfully extract per-test sleep data with <10% missing
- Multilevel model converges with reasonable random effects
- Significant within-person sleep effect (p < 0.05 uncorrected, assess after Bonferroni)
- Effect size beta > 0.03 (small but meaningful for intervention)
- Model diagnostics pass (residual normality, homoscedasticity, VIF < 5)
- Cross-validation R² within 10% of training model
- Within-person effects stronger than between-person effects

---

## Data Source

**Data Type:**
DERIVED (from Ch5 outputs + master.xlsx sleep data)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (Overall theta scores per test)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (theta per UID per test)
- data/cache/master.xlsx (per-test sleep data)

**Dependencies:**
Ch5 5.1.1 must complete Step 3 (theta score generation) before this RQ can run

### Sleep Data Extraction:

**Source File:**
data/cache/master.xlsx

**Tag Patterns:**
- Sleep Hours: `{UID}-RVR-T{N}-SLP-X-HOUR-` (per test N=1,2,3,4)
- Sleep Quality: `{UID}-RVR-T{N}-SLP-X-QUAL-` (per test N=1,2,3,4)

**Extraction Method:**
Step 1 extracts sleep data from master.xlsx and creates per-test sleep variables, then merges with theta scores by UID and Test to create 400-row longitudinal dataset

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- Sleep data completeness checked - participants with <3 tests excluded from within-person analysis

**Items:**
- N/A (theta scores already aggregated across all items)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - REQUIRED for within-person analysis
- Minimum 3 tests with complete sleep data required per participant

**Sleep Variables:**
- [x] Sleep Hours: Continuous variable (hours of sleep before each test)
- [x] Sleep Quality: Likert scale (subjective sleep quality before each test)
- Exclude sleep data >3 SD from person mean (likely data entry errors)

---