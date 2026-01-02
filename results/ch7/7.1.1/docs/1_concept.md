# RQ 7.1.1: Do cognitive tests predict overall REMEMVR ability?

**Chapter:** 7
**Type:** Predictive Validity (Core)
**Subtype:** General episodic memory prediction
**Full ID:** 7.1.1

---

## Research Question

**Primary Question:**
Do established neuropsychological tests (RAVLT, BVMT, NART, RPM) predict overall episodic memory ability as measured by REMEMVR theta scores?

**Scope:**
100 participants, mean theta scores averaged across 4 test sessions, standardized cognitive test scores (T-scores)

**Theoretical Framing:**
This addresses the central thesis question: if REMEMVR (ecological VR memory) and traditional tests measure the same construct, they should correlate moderately. Testing convergent validity while examining ecological validity gap.

---

## Theoretical Background

**Relevant Theories:**
Predictive validity framework (Cronbach & Meehl, 1955) - if standard tests validly measure episodic memory, they should correlate with ecological episodic performance. Ecological validity gap theory (Chaytor & Schmitter-Edgecombe, 2003) predicts imperfect prediction due to contextual differences between laboratory and real-world settings.

**Key Citations:**
Cronbach & Meehl (1955) on construct validity
Chaytor & Schmitter-Edgecombe (2003) on ecological validity gap

**Theoretical Predictions:**
Moderate correlation between traditional tests and REMEMVR (convergent validity), but substantial residual variance due to ecological context differences. RAVLT and BVMT should predict better than NART/RPM since they directly assess episodic memory.

**Literature Gaps:**
Limited research on ecological validity of neuropsychological tests in VR environments, particularly for complex episodic memory scenarios involving multiple domains.

---

## Hypothesis

**Primary Hypothesis:**
Cognitive tests should predict REMEMVR with moderate effect (R² = 0.30-0.45), demonstrating convergent validity while leaving substantial unique variance.

**Secondary Hypotheses:**
RAVLT and BVMT (episodic memory tests) should show stronger prediction than NART and RPM (intelligence tests). Specifically, RAVLT_beta > RPM_beta reflecting episodic memory specificity.

**Theoretical Rationale:**
Traditional neuropsychological tests assess memory under controlled laboratory conditions over 20-30 minutes. REMEMVR assesses memory in rich ecological VR context over multiple days. Convergent validity predicts moderate correlation, but ecological validity gap limits predictive power.

**Expected Effect Pattern:**
R² between 0.25-0.50 (convergent but not redundant)
RAVLT standardized beta > RPM standardized beta (episodic > fluid intelligence)
Bonferroni-corrected alpha = 0.00179/4 = 0.000448 per predictor
Residual variance > 50% indicating substantial unique REMEMVR variance

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall theta_all scores from Ch5 5.1.1

- [x] **Where** (Spatial Location)  
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall theta_all scores from Ch5 5.1.1

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall theta_all scores from Ch5 5.1.1

**Inclusion Rationale:**
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains and paradigms to provide overall episodic memory ability measure.

**Exclusion Rationale:**
None - this is an omnibus analysis including all domains to establish general predictive validity before examining domain-specific predictions in later RQs.

---

## Analysis Approach

**Analysis Type:**
Multiple regression with dominance analysis for predictor importance

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load theta scores from results/ch5/5.1.1/data/step03_theta_scores.csv
- Compute mean theta per UID across 4 test sessions
- Extract cognitive tests from master.xlsx using tag patterns
- Compute derived scores (RAVLT_Total = sum of T1-T5)
- Standardize all cognitive tests to T-scores (M=50, SD=10)
- Check assumptions: normality, homoscedasticity, VIF < 5

**Step 2:** Fit multiple regression
- Model: Theta_Mean ~ RAVLT_T + BVMT_T + NART_T + RPM_T
- Report: R², adjusted R², F-statistic, p-value

**Step 3:** Test individual predictors
- Extract standardized beta for each predictor
- Compute semi-partial correlations (sr�) for unique variance
- Apply Bonferroni correction: alpha = 0.00179/4 = 0.000448

**Step 4:** Compare predictor importance
- Dominance analysis or relative importance weights
- Test hypothesis: RAVLT_beta > RPM_beta (episodic > fluid)

**Step 5:** Sensitivity analysis
- Repeat excluding NART (language validity concerns)
- Compare R² with and without NART

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted test scores from master.xlsx)
- data/step02_theta_means.csv (mean theta per participant)  
- data/step03_analysis_input.csv (merged analysis dataset)
- data/step04_regression_results.csv (coefficients, p-values, effect sizes)
- data/step05_predictor_importance.csv (dominance analysis results)
- results/regression_summary.md (text summary for thesis)
- plots/predictor_importance.png (visualization)

**Success Criteria:**
- [ ] Model explains significant variance (p < 0.00179)
- [ ] R² between 0.25 and 0.50 (convergent but not redundant)  
- [ ] At least one episodic test (RAVLT or BVMT) significant after Bonferroni
- [ ] Residual > 50% (substantial unique REMEMVR variance)
- [ ] VIF < 5 for all predictors (no multicollinearity)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (General episodic memory theta scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (REMEMVR theta scores)
- data/cache/master.xlsx (cognitive test scores and demographics)

**Dependencies:**
Ch5 5.1.1 must complete before this RQ can run

### Cognitive Test Variables (from master.xlsx):

**RAVLT (Rey Auditory Verbal Learning Test):**
- Tag patterns: `{UID}-COG-X-RAV-T1Sc` through `T5Sc`, `DRSc`, `FRSc`
- Computed: RAVLT_Total = sum(T1-T5), RAVLT_Learning = T5-T1, RAVLT_Forgetting = T5-DR

**BVMT (Brief Visuospatial Memory Test):**
- Tag patterns: `{UID}-COG-X-BVM-TotR`, `{UID}-COG-X-BVM-TDSc`
- Computed: BVMT_PerR = (TD/T3)*100

**NART (National Adult Reading Test):**
- Tag pattern: `{UID}-COG-X-NAR-Scor`
- Range: 0-50 (caveat: language validity concerns)

**RPM (Raven's Progressive Matrices):**
- Tag pattern: `{UID}-COG-X-RPM-Scor`
- Range: 0-12

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants
- Missing data handled via listwise deletion (report n per analysis)

**REMEMVR Data:**
- [x] All 4 test sessions (T1, T2, T3, T4)
- [x] All paradigms (IFR, ICR, IRE) from omnibus theta_all
- [x] All domains (What, Where, When) from omnibus theta_all

**Cognitive Tests:**
- [x] All 4 test batteries (RAVLT, BVMT, NART, RPM)
- Sensitivity analysis excludes NART to address language validity concerns

---