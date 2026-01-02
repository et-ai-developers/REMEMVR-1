# RQ 7.1.4: Unique REMEMVR variance unexplained by all predictors?

**Chapter:** 7
**Type:** Predictive Validity (Core)
**Subtype:** Incremental Validity Analysis
**Full ID:** 7.1.4

---

## Research Question

**Primary Question:**
What proportion of REMEMVR variance remains unexplained after accounting for ALL available predictors (cognitive tests, demographics, self-report)?

**Scope:**
100 participants with complete cognitive test data, episodic memory theta scores from Ch5 5.1.1, and demographics/self-report from master.xlsx

**Theoretical Framing:**
Tests whether REMEMVR captures unique variance beyond traditional neuropsychological batteries, supporting its clinical utility and ecological validity

---

## Theoretical Background

**Relevant Theories:**
Incremental validity framework (Hunsley & Meyer, 2003) for establishing test utility beyond existing measures. Ecological validity gap theory (Chaytor & Schmitter-Edgecombe, 2003) predicts naturalistic memory tasks capture variance missed by laboratory assessments.

**Key Citations:**
Hunsley & Meyer (2003) - Incremental validity framework
Chaytor & Schmitter-Edgecombe (2003) - Ecological validity gap

**Theoretical Predictions:**
Traditional tests should predict substantial REMEMVR variance (convergent validity) but miss naturalistic encoding, multi-day consolidation, and confidence monitoring processes unique to real-world memory

**Literature Gaps:**
Limited evidence on how much variance remains unexplained when comprehensive neuropsychological batteries are used to predict VR-based episodic memory performance

---

## Hypothesis

**Primary Hypothesis:**
Substantial residual variance (>50%) should remain unexplained after accounting for all predictors, supporting REMEMVR's incremental validity over traditional tests

**Secondary Hypotheses:**
1. Cognitive tests (Block 2) will show largest incremental R² (~0.28, medium-large effect)
2. Demographics and self-report measures will add minimal incremental variance (<0.10)
3. When domain will show highest residual variance (temporal memory most naturalistic)

**Theoretical Rationale:**
The "ecological validity gap" represents genuine signal REMEMVR was designed to capture - naturalistic memory processes not assessed by traditional laboratory paradigms

**Expected Effect Pattern:**
Total R² < 0.55, with true residual (after removing measurement error) > 40%, demonstrating substantial unique REMEMVR variance supporting incremental validity

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in overall theta_all scores from Ch5 5.1.1, also examined separately

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in overall theta_all scores from Ch5 5.1.1, also examined separately

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in overall theta_all scores from Ch5 5.1.1, also examined separately

**Inclusion Rationale:**
Primary analysis uses omnibus theta_all scores from Ch5 5.1.1 aggregating across all episodic memory domains. Secondary analyses examine domain-specific residuals to test prediction that When domain shows highest unexplained variance.

**Exclusion Rationale:**
No domains excluded - comprehensive analysis of all episodic memory components

---

## Analysis Approach

**Analysis Type:**
Hierarchical Multiple Regression with incremental validity testing

**High-Level Workflow:**

**Step 1:** Extract theta_all scores from Ch5 5.1.1 and cognitive test scores from master.xlsx
**Step 2:** Build hierarchical regression models with three blocks:
  - Model 1: Demographics (Age, Sex, Education)
  - Model 2: + Cognitive Tests (RAVLT_T, BVMT_T, NART_T, RPM_T)
  - Model 3: + Self-Report (DASS_Dep, DASS_Anx, DASS_Str, VR_Exp, Sleep)
**Step 3:** Compute incremental R² and Cohen's f² for each block
**Step 4:** Quantify unexplained variance separating measurement error from true residual
**Step 5:** Repeat analysis for domain-specific theta scores (What, Where, When)

**Expected Outputs:**
- data/step01_cognitive_tests.csv (extracted test scores from master.xlsx)
- data/step02_theta_scores.csv (theta_all and domain-specific from Ch5)
- data/step03_merged_dataset.csv (complete analysis dataset)
- data/step04_hierarchical_models.csv (R², Delta_R², f² for each model)
- data/step05_variance_decomposition.csv (explained vs unexplained components)
- data/step06_domain_residuals.csv (domain-specific unexplained variance)
- results/incremental_validity_summary.md (interpretation for thesis)
- plots/variance_decomposition.png (visualization of explained/unexplained)

**Success Criteria:**
- Block 2 (cognitive tests) shows significant increment (p < 0.00179, Bonferroni-corrected)
- Total R² < 0.55 (at least 45% unexplained variance)
- True residual (after removing measurement error) > 40%
- When domain shows highest residual variance among domains

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 5.1.1 (General episodic memory theta scores across all domains/paradigms)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (omnibus theta_all per participant)
- results/ch5/5.2.*/data/step03_theta_scores.csv (domain-specific theta scores)
- data/cache/master.xlsx (cognitive test scores and demographics)

**Dependencies:**
Ch5 5.1.1 must complete successfully before this RQ can run. Domain-specific analyses require Ch5 5.2.x completion.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants with complete cognitive test data
- Listwise deletion for any missing predictors

**Variables:**
**Block 1 - Demographics:**
- Age: {UID}-DEM-X-Age
- Sex: {UID}-DEM-X-Sex 
- Education: {UID}-DEM-X-Education

**Block 2 - Cognitive Tests:**
- RAVLT_Total: sum({UID}-COG-X-RAV-T1Sc through T5Sc)
- BVMT_Total: sum({UID}-COG-X-BVM-T1Sc through T3Sc)
- NART: {UID}-COG-X-NAR-Scor
- RPM: {UID}-COG-X-RPM-Scor

**Block 3 - Self-Report:**
- DASS_Depression: {UID}-DEM-X-DASS_Dep
- DASS_Anxiety: {UID}-DEM-X-DASS_Anx
- DASS_Stress: {UID}-DEM-X-DASS_Str
- VR_Experience: {UID}-DEM-X-VR_Exp
- Typical_Sleep: {UID}-DEM-X-SLEEP

**Tests:**
- All REMEMVR tests included in omnibus theta_all calculation
- Domain-specific analyses use What/Where/When theta scores separately

---