# RQ 7.5.3: Memory Strategies Predicting Performance

**Chapter:** 7
**Type:** Lifestyle and Individual Differences
**Subtype:** Memory Strategies
**Full ID:** 7.5.3

---

## Research Question

**Primary Question:**
Do self-reported memory strategies (rehearsal, visualization, mnemonics) predict REMEMVR performance?

**Scope:**
This RQ examines the relationship between self-reported memory strategy usage and overall REMEMVR accuracy. Data includes rehearsal frequency and mnemonic usage variables extracted from STR questionnaire tags in master.xlsx. Analysis uses mean theta_all scores as the outcome measure across all 100 participants. Strategy variables require text coding from questionnaire responses.

**Theoretical Framing:**
Individual differences in memory strategy use may account for performance variation in episodic memory tasks, even in incidental encoding paradigms where strategies are not explicitly prompted.

---

## Theoretical Background

**Relevant Theories:**
- **Memory Strategy Theory**: Effective memory strategies (elaboration, organization, rehearsal) improve encoding and retrieval across episodic memory tasks
- **Individual Differences Framework**: People vary in spontaneous strategy use, with strategic individuals showing better memory performance
- **Incidental Encoding Effects**: Even when encoding is incidental (as in VR tasks), individuals may spontaneously apply memory strategies

**Key Citations:**


**Theoretical Predictions:**
Active memory strategy use (rehearsal, mnemonics) should predict better episodic memory performance through enhanced encoding and retrieval processes.

**Literature Gaps:**
Limited research on memory strategy effects in immersive VR episodic memory paradigms with incidental encoding.

---

## Hypothesis

**Primary Hypothesis:**
Active strategy use may improve performance, but effect may be small given incidental encoding paradigm.

**Secondary Hypotheses:**
Rehearsal frequency will show positive correlation with theta scores (r ~ 0.18). Mnemonic users will show marginally higher performance than non-users.

**Theoretical Rationale:**
Memory strategies enhance encoding even in incidental learning contexts, but effects are attenuated when strategies are not explicitly instructed or prompted.

**Expected Effect Pattern:**
Small positive correlations between strategy use and performance: Rehearsal frequency r ~ 0.18, p = 0.07; Mnemonic use t ~ 1.45, p = 0.15. Effects marginal but positive.

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
Uses omnibus theta_all scores that aggregate across all episodic memory domains to examine overall strategy effects on episodic memory performance.

**Exclusion Rationale:**
None - comprehensive omnibus measure captures general memory strategy effects.

---

## Analysis Approach

**Power Analysis:**
- Sample size: N=100 with k predictors
- Post-hoc power for medium effects (f²=0.15): Approximately 80%
- Minimum detectable effect: f²=0.10 with current sample
- Limitation acknowledged: Underpowered for small effects (f²<0.10)


**Analysis Type:**
Correlational analysis and independent samples t-test with multiple regression control variables

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load theta scores from Ch5 5.1.1 outputs (theta_all per participant)
- Extract STR questionnaire data from master.xlsx
- Code strategy variables from text responses

**Step 2:** Code strategy variables
- Rehearsal frequency: Extract from `{UID}-RVR-T{N}-STR-X-TNK1-` tags (quantitative)
- Mnemonic use: Extract from `{UID}-RVR-T{N}-STR-X-MNE1-` tags (requires text coding)
- Compute mean rehearsal frequency across tests
- Create binary mnemonic use variable (yes/no)

**Step 3:** Descriptive statistics
- Check strategy variable distributions
- Identify extreme values and missing data
- Report strategy use prevalence

**Step 4:** Primary correlational analyses
- Correlation between rehearsal frequency and theta_all
- Independent samples t-test: mnemonic users vs non-users
- Report effect sizes with confidence intervals

**Step 5:** Control variable analysis
- Add age and cognitive ability controls
- Test whether strategy effects remain significant
- Hierarchical regression: demographics  strategies

**Step 6:** Model diagnostics and sensitivity
- Check assumptions (normality, homoscedasticity)
- Examine outliers and influential points
- Report BOTH uncorrected AND corrected p-values (Decision D068)

**Step 7:** Effect sizes and interpretation
- Compute Cohen's d for group differences
- Report R² and confidence intervals
- bootstrap (1000 replications, seed=42) CIs for non-normal distributions

**Expected Outputs:**
- data/step01_theta_scores.csv (participant theta_all scores)
- data/step02_strategy_variables.csv (coded strategy measures)  
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_correlation_results.csv (r values, CIs, dual p-values)
- data/step05_group_comparison.csv (t-test results with effect sizes)
- data/step06_regression_control.csv (controlled analysis results)
- data/step07_sensitivity_analysis.csv (outlier and bootstrap (1000 replications, seed=42) results)
- results/strategy_summary.md (text summary for thesis)
- plots/strategy_performance_scatter.png (correlational plots)
- plots/strategy_group_comparison.png (boxplot comparison)

**

**Cross-Validation:**
- Implement 5-fold CV (seed=42) for generalization assessment
- Report mean CV-R² and SD across folds
- CV-R² to full-sample R² gap should be <0.10
- If gap >0.10: Consider regularization


**Success Criteria:**
- [ ] Successfully extract strategy variables from STR questionnaire
- [ ] Report correlations with performance (uncorrected and corrected p-values)
- [ ] Acknowledge text coding limitations and reliability
- [ ] Control for age and cognitive ability covariates
- [ ] Effect sizes with 95% confidence intervals
- [ ] Check assumptions and report diagnostic statistics
- [ ] bootstrap (1000 replications, seed=42) CIs for robust inference

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx strategy questionnaires)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (omnibus theta_all scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv
- data/cache/master.xlsx (STR questionnaire tags)

**Dependencies:**
Ch5 5.1.1 must complete before this RQ can run

### Strategy Variable Extraction:

**STR Questionnaire Tags:**
- Rehearsal frequency: `{UID}-RVR-T{N}-STR-X-TNK1-` (quantitative ratings)
- Mnemonic strategies: `{UID}-RVR-T{N}-STR-X-MNE1-` (text responses requiring coding)

**Coding Requirements:**
- Rehearsal: Extract numeric ratings per test, compute mean across T1-T4
- Mnemonics: Binary coding of text responses (any strategy use vs none)
- Text coding reliability check on subset of responses

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (complete STR data expected)
- [ ] Exclude: Participants with missing strategy questionnaire data

**Items:**
- N/A (uses aggregated theta_all scores)

**Tests:**
- [x] All 4 tests (strategy reports averaged across tests)

---