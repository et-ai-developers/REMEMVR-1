# Chapter 7: Individual Differences in Episodic Memory
# Complete RQ Specifications

**Author:** Claude Code Assistant
**Date:** 2026-01-02
**Status:** SPECIFICATION COMPLETE - Ready for rq_concept execution
**Version:** 2.0 (Refined based on Ch5/Ch6 findings)

---

## PURPOSE

This document contains complete specifications for all Ch7 RQs. Each specification provides sufficient detail for rq_concept to generate concept.md files.

**Central Thesis Question:** If REMEMVR (ecological VR memory) and traditional tests (RAVLT, BVMT) measure the same construct, they should correlate highly. If they don't, what explains the gap?

**Three Key Claims:**
1. **Convergent Validity:** Traditional tests DO predict REMEMVR (moderate r~0.5)
2. **Divergent Validity:** Traditional tests leave >50% unexplained
3. **Clinical Utility:** REMEMVR findings inform reinterpretation of traditional tests

---

## TABLE OF CONTENTS

**INSTRUCTIONS FOR rq_concept:** Use this TOC to navigate directly to the RQ you need. Each RQ specification contains: Research Question, Hypothesis, Theoretical Framework, Data Required, Analysis Specification, Expected Output, and Success Criteria.

### Quick Reference: RQ → Line Number

| RQ | Title | Line | Priority |
|----|-------|------|----------|
| **METHODOLOGICAL FRAMEWORK** | Data sources, tags, extraction protocol | 86 | - |
| **THEME 1** | Predictive Validity (Core) | 195 | TIER 1 |
| 7.1.1 | Do cognitive tests predict overall REMEMVR ability? | 197 | TIER 1 |
| 7.1.2 | Do tests predict intercept vs slope? | 261 | TIER 1 |
| 7.1.3 | Which test predicts which domain? | 315 | TIER 1 |
| 7.1.4 | Unique REMEMVR variance unexplained? | 376 | TIER 1 |
| **THEME 2** | Age × VR Scaffolding | 443 | TIER 1 |
| 7.2.1 | Does age predict REMEMVR after controlling for tests? | 445 | TIER 1 |
| 7.2.2 | Do cognitive tests attenuate age effects? | 506 | TIER 1 |
| 7.2.3 | Is there Age × Cognitive Test interaction? | 553 | TIER 1 |
| 7.2.4 | VR Scaffolding Validation (NEW) | 604 | TIER 1 |
| **THEME 3** | Metacognition Predictors | 661 | TIER 2 |
| 7.3.1 | Do cognitive tests predict confidence trajectories? (NEW) | 663 | TIER 2 |
| 7.3.2 | Do cognitive tests predict calibration quality? (NEW) | 709 | TIER 2 |
| 7.3.3 | Do cognitive tests predict HCE rate? (NEW) | 754 | TIER 2 |
| 7.3.4 | Does DASS predict metacognition more than memory? (NEW) | 800 | TIER 2 |
| 7.3.5 | Does confidence-accuracy gap predict cognitive reserve? (NEW) | 846 | TIER 2 |
| **THEME 4** | Process-Specific Prediction | 895 | TIER 3 |
| 7.4.1 | Does RAVLT Free Recall predict REMEMVR Free Recall > Recognition? | 897 | TIER 3 |
| 7.4.2 | Does BVMT predict Where more than What? | 942 | TIER 3 |
| 7.4.3 | Does RPM predict complex integration? | 980 | TIER 3 |
| **THEME 5** | Self-Report & Contextual | 1024 | TIER 4 |
| 7.5.1 | Do sleep, education, VR experience predict REMEMVR? | 1026 | TIER 4 |
| 7.5.2 | Does DASS predict memory performance? | 1074 | TIER 4 |
| 7.5.3 | Do memory strategies correlate with performance? | 1119 | TIER 4 |
| 7.5.4 | Per-Test Sleep predicting same-test performance (NEW) | 1160 | TIER 4 |
| **THEME 6** | Individual Differences in Forgetting | 1211 | TIER 3 |
| 7.6.1 | Do cognitive tests predict individual differences in slope? | 1213 | TIER 3 |
| 7.6.2 | Does RAVLT Delayed predict REMEMVR slope? (NEW) | 1257 | TIER 3 |
| 7.6.3 | ICC slope replication across domains (NEW) | 1299 | TIER 3 |
| 7.6.4 | Purification & Slope predictors (NEW) | 1344 | TIER 3 |
| **THEME 7** | Clinical Utility & Alternative Interpretation | 1387 | TIER 1 |
| 7.7.1 | Reverse Inference - Can REMEMVR predict RAVLT? | 1389 | TIER 1 |
| 7.7.2 | Discrepancy Analysis - Who diverges? (NEW) | 1435 | TIER 1 |
| 7.7.3 | Alternative RAVLT Scoring (NEW) | 1484 | TIER 1 |
| 7.7.4 | Clinical Profiles - False Negatives (NEW) | 1534 | TIER 1 |
| **THEME 8** | Latent Profiles & Models | 1582 | TIER 4 |
| 7.8.1 | Distinct REMEMVR memory profiles? | 1584 | TIER 4 |
| 7.8.2 | Cognitive test profiles predict REMEMVR profiles? | 1639 | TIER 4 |
| 7.8.3 | Parsimonious predictive model with cross-validation | 1686 | TIER 4 |
| 7.8.4 | Multivariate vs univariate prediction | 1733 | TIER 4 |
| **SUMMARY** | Total RQs, Priority Tiers, Data Sources | 1775 | - |

### Priority Tier Summary

| Tier | Themes | RQs | Description |
|------|--------|-----|-------------|
| **TIER 1** | 1, 2, 7 | 12 | Core thesis: Predictive validity + Age + Clinical utility |
| **TIER 2** | 3 | 5 | Metacognition: Connects to Ch6 |
| **TIER 3** | 4, 6 | 7 | Process-specific + Slope predictors: Connects to Ch5 |
| **TIER 4** | 5, 8 | 8 | Self-report + Profiles: Nice-to-have |

---

## FILE ORGANIZATION CONVENTIONS

### Standard RQ Folder Structure

All Ch7 RQs follow the standard folder organization:

```
results/ch7/{RQ_ID}/
├── code/          # Python analysis scripts (step##_description.py)
├── data/          # ALL CSV outputs from analysis (step##_description.csv)
├── docs/          # Documentation (1_concept.md, 2_plan.md)
├── logs/          # Execution logs
├── plots/         # Visualizations (PNG/PDF files)
├── results/       # Summary documents ONLY (.md, .txt files)
└── status.yaml    # Execution status tracker
```

**CRITICAL FILE PLACEMENT RULES:**
- **data/** folder: ALL CSV outputs from analysis steps (step01_*.csv, step02_*.csv, etc.)
- **results/** folder: Summary documents ONLY (markdown, text files) - NO CSV FILES
- **plots/** folder: Visualization files (PNG, PDF)
- **code/** folder: Python scripts for analysis
- **docs/** folder: Agent-created documents (1_concept.md, 2_plan.md, etc.)

**File Naming Conventions:**
- Analysis outputs: `step##_description.csv` (e.g., step01_cognitive_tests.csv)
- Summary documents: descriptive names (e.g., regression_summary.md)
- Plots: descriptive names (e.g., predictor_importance.png)

**Character Encoding:**
- Use "R²" or "R-squared" (NOT corrupted "R�")
- Use standard ASCII or UTF-8 encoding

---

## METHODOLOGICAL FRAMEWORK

### Dependent Variables (REMEMVR Theta Scores)

Ch7 uses IRT theta scores from Ch5/Ch6 as dependent variables:

| Analysis Set | Source | Description |
|--------------|--------|-------------|
| **Theta_All** | Ch5 5.1.1 | General episodic memory (all items, all paradigms) |
| **Theta_What** | Ch5 5.2.x | Object identity domain |
| **Theta_Where** | Ch5 5.2.x | Spatial location domain |
| **Theta_When** | Ch5 5.2.x | Temporal order domain |
| **Theta_FreeRecall** | Ch5 5.3.x | Free recall paradigm |
| **Theta_CuedRecall** | Ch5 5.3.x | Cued recall paradigm |
| **Theta_Recognition** | Ch5 5.3.x | Recognition paradigm |
| **Confidence_Theta** | Ch6 6.1.x | Confidence ratings (IRT-scaled) |
| **Calibration** | Ch6 6.2.x | Resolution/calibration metrics |
| **HCE_Rate** | Ch6 6.6.x | High-confidence error proportion |

### Independent Variables (Cognitive Tests & Demographics)

**Cognitive Tests (from master.xlsx):**

| Variable | Tag Pattern | Range | Computed Scores |
|----------|-------------|-------|-----------------|
| RAVLT_T1-T5 | `{UID}-COG-X-RAV-T1Sc` to `T5Sc` | 0-15 each | RAVLT_Total = sum(T1-T5) |
| RAVLT_DR | `{UID}-COG-X-RAV-DRSc` | 0-15 | RAVLT_Forgetting = T5-DR |
| RAVLT_FR | `{UID}-COG-X-RAV-FRSc` | 0-15 | RAVLT_Learning = T5-T1 |
| BVMT_T1-T3 | `{UID}-COG-X-BVM-T1Sc` to `T3Sc` | 0-12 each | BVMT_Total = sum(T1-T3) |
| BVMT_TD | `{UID}-COG-X-BVM-TDSc` | 0-12 | BVMT_PerR = TD/T3*100 |
| BVMT_TotR | `{UID}-COG-X-BVM-TotR` | 0-36 | Pre-computed |
| NART | `{UID}-COG-X-NAR-Scor` | 0-50 | Raw score (caveat: language) |
| RPM | `{UID}-COG-X-RPM-Scor` | 0-12 | Raw score |

**Demographics (from master.xlsx):**

| Variable | Tag Pattern | Range | Notes |
|----------|-------------|-------|-------|
| Age | `{UID}-DEM-X-Age` | 20-70 | Continuous |
| Sex | `{UID}-DEM-X-Sex` | 0-3 | 0=F, 1=M, 2=Other, 3=Prefer not |
| Education | `{UID}-DEM-X-Education` | 0-9 | Highest level |
| VR_Experience | `{UID}-DEM-X-VR_Exp` | 0-4 | Hours of VR experience |
| Typical_Sleep | `{UID}-DEM-X-SLEEP` | 0-24 | Typical hours/night |

**DASS-21 (from master.xlsx):**

| Variable | Tag Pattern | Range |
|----------|-------------|-------|
| Depression | `{UID}-DEM-X-DASS_Dep` | 0-42 |
| Anxiety | `{UID}-DEM-X-DASS_Anx` | 0-42 |
| Stress | `{UID}-DEM-X-DASS_Str` | 0-42 |

**Per-Test Sleep (from master.xlsx):**

| Variable | Tag Pattern | Range |
|----------|-------------|-------|
| Hours_Slept | `{UID}-RVR-T{N}-SLP-X-HOUR-` | 0-24 |
| Sleep_Quality | `{UID}-RVR-T{N}-SLP-X-QUAL-` | -1 to 1 |
| Tiredness | `{UID}-RVR-T{N}-SLP-X-TIRE-` | -1 to 1 |
| Caffeine | `{UID}-RVR-T{N}-SLP-X-CAF1-` | 0/1 |

### Statistical Standards

- **Chapter-level alpha:** 0.05 / 28 RQs = **0.00179 per RQ**
- **Within-RQ corrections:** Bonferroni for k predictors
- **Effect sizes:** R², beta, Cohen's d, f², ICC
- **Standardization:** All cognitive tests converted to T-scores (M=50, SD=10)
- **Missing data:** Listwise deletion (report n per analysis)
- **Cross-validation:** 5-fold CV for predictive models

### Data Extraction Protocol

**Step 1: Extract Cognitive Test Scores**
```python
# From master.xlsx using data.py patterns
cog_tags = [
    '{UID}-COG-X-RAV-T1Sc', '{UID}-COG-X-RAV-T2Sc', '{UID}-COG-X-RAV-T3Sc',
    '{UID}-COG-X-RAV-T4Sc', '{UID}-COG-X-RAV-T5Sc', '{UID}-COG-X-RAV-DRSc',
    '{UID}-COG-X-RAV-FRSc', '{UID}-COG-X-BVM-TotR', '{UID}-COG-X-BVM-TDSc',
    '{UID}-COG-X-NAR-Scor', '{UID}-COG-X-RPM-Scor'
]
```

**Step 2: Compute Derived Scores**
```python
df['RAVLT_Total'] = df[['RAV_T1Sc', 'RAV_T2Sc', 'RAV_T3Sc', 'RAV_T4Sc', 'RAV_T5Sc']].sum(axis=1)
df['RAVLT_Learning'] = df['RAV_T5Sc'] - df['RAV_T1Sc']
df['RAVLT_Forgetting'] = df['RAV_T5Sc'] - df['RAV_DRSc']
df['BVMT_PerR'] = (df['BVM_TDSc'] / df['BVM_T3Sc']) * 100
```

**Step 3: Standardize to T-Scores**
```python
for col in ['RAVLT_Total', 'BVMT_TotR', 'NAR_Scor', 'RPM_Scor']:
    df[f'{col}_T'] = 50 + 10 * ((df[col] - df[col].mean()) / df[col].std())
```

**Step 4: Merge with Theta Scores**
```python
# Read theta scores from Ch5/Ch6 results
theta_all = pd.read_csv('results/ch5/5.1.1/data/step03_theta_scores.csv')
# Group by UID, compute mean theta across tests
mean_theta = theta_all.groupby('UID')['theta'].mean().reset_index()
# Merge with cognitive/demographic data
analysis_df = mean_theta.merge(cog_dem_df, on='UID')
```

---

## THEME 1: PREDICTIVE VALIDITY (CORE)

### RQ 7.1.1: Do cognitive tests predict overall REMEMVR ability?

**Research Question:** Do established neuropsychological tests (RAVLT, BVMT, NART, RPM) predict overall episodic memory ability as measured by REMEMVR theta scores?

**Hypothesis:** Cognitive tests should predict REMEMVR with moderate effect (R² = 0.30-0.45), demonstrating convergent validity. RAVLT and BVMT (episodic memory tests) should show stronger prediction than NART and RPM (intelligence tests).

**Theoretical Framework:** Predictive validity (Cronbach & Meehl, 1955). If standard tests validly measure episodic memory, they should correlate with ecological episodic performance. However, ecological validity gap (Chaytor & Schmitter-Edgecombe, 2003) predicts imperfect prediction due to contextual differences.

**Data Required:**
- **DV:** Mean Theta_All per UID (average across 4 test sessions)
- **IVs:** RAVLT_Total_T, BVMT_TotR_T, NART_T, RPM_T (all T-scores)
- **Source:** Ch5 5.1.1 theta scores + master.xlsx cognitive tests
- **N:** 100 participants

**Analysis Specification:**

1. **Extract and prepare data**
   - Load theta scores from `results/ch5/5.1.1/data/step03_theta_scores.csv`
   - Compute mean theta per UID
   - Extract cognitive tests from master.xlsx
   - Compute derived scores (RAVLT_Total)
   - Standardize to T-scores
   - Check assumptions: normality, homoscedasticity, VIF < 5

2. **Fit multiple regression**
   - Model: `Theta_Mean ~ RAVLT_T + BVMT_T + NART_T + RPM_T`
   - Report: R², adjusted R², F-statistic, p-value

3. **Test individual predictors**
   - Extract standardized beta for each predictor
   - Compute semi-partial correlations (sr²) for unique variance
   - Bonferroni correction: alpha = 0.00179/4 = 0.000448

4. **Compare predictor importance**
   - Dominance analysis or relative importance weights
   - Hypothesis: RAVLT_beta > RPM_beta (episodic > fluid)

5. **Sensitivity analysis**
   - Repeat excluding NART (language validity concerns)
   - Compare R² with and without NART

**Expected Output:**
```
Model: Theta ~ RAVLT + BVMT + NART + RPM
R² = 0.35, Adjusted R² = 0.32, F(4,95) = 12.8, p < 0.001

Predictor   Beta    SE     t      p         sr²
RAVLT_T     0.32    0.09   3.56   <0.001    0.10
BVMT_T      0.25    0.09   2.78   0.007     0.06
NART_T      0.12    0.10   1.20   0.233     0.01
RPM_T       0.18    0.09   2.00   0.048     0.03

Variance explained by cognitive tests: 35%
Residual (unexplained): 65%
```

**Success Criteria:**
- [ ] Model explains significant variance (p < 0.00179)
- [ ] R² between 0.25 and 0.50 (convergent but not redundant)
- [ ] At least one episodic test (RAVLT or BVMT) significant after Bonferroni
- [ ] Residual > 50% (substantial unique REMEMVR variance)

---

### RQ 7.1.2: Do tests predict intercept (Day 0) vs slope (forgetting)?

**Research Question:** Do cognitive tests predict baseline ability (Day 0 intercept) more than forgetting rate (slope), consistent with tests measuring encoding but not consolidation?

**Hypothesis:** Cognitive tests predict intercept strongly (R² > 0.30) but slope weakly (R² < 0.10). Rationale: Traditional tests measure encoding/retrieval over 20-30 minutes, not multi-day consolidation.

**Theoretical Framework:** Two-process theory (Craik & Rose, 2012) distinguishes encoding from consolidation. Ch5 established power-law forgetting with individual differences in slope (ICC_slope = 21% under model averaging). If tests measure encoding only, they should predict intercept but not slope.

**Data Required:**
- **DVs:** Per-participant intercept and slope from LMM random effects
- **IVs:** RAVLT_T, BVMT_T, RPM_T (excluding NART due to concerns)
- **Source:** Ch5 5.1.1 LMM results + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Extract random effects from LMM**
   - Use model-averaged predictions from Ch5 5.1.1
   - Extract BLUPs: Intercept_i (Day 0 ability), Slope_i (forgetting rate)
   - Or re-fit LMM: `Theta ~ log_Days + (1 + log_Days | UID)`

2. **Predict intercepts**
   - Model: `Intercept ~ RAVLT_T + BVMT_T + RPM_T`
   - Report R², beta coefficients

3. **Predict slopes**
   - Model: `Slope ~ RAVLT_T + BVMT_T + RPM_T`
   - Report R², beta coefficients

4. **Compare R² values**
   - Bootstrap 95% CI for R²_intercept - R²_slope
   - Hypothesis: R²_intercept >> R²_slope

5. **Test differential prediction**
   - Fisher's Z-test for comparing model R²

**Expected Output:**
```
Analysis       R²     RAVLT_beta  BVMT_beta  RPM_beta
Intercept      0.38   0.35***     0.28**     0.15
Slope          0.08   0.12        0.08       0.10

Difference: R²_intercept - R²_slope = 0.30, 95% CI [0.18, 0.42]
Conclusion: Tests predict encoding (intercept), NOT consolidation (slope)
```

**Success Criteria:**
- [ ] R²_intercept > 0.25
- [ ] R²_slope < 0.15
- [ ] R²_intercept significantly > R²_slope (bootstrap CI excludes 0)
- [ ] No individual predictor significantly predicts slope

---

### RQ 7.1.3: Which test predicts which domain?

**Research Question:** Do verbal tests (RAVLT) preferentially predict What memory, visuospatial tests (BVMT) predict Where memory, and neither predicts When memory?

**Hypothesis:** Domain-specific prediction pattern:
- RAVLT → What (object identity verbally encoded)
- BVMT → Where (spatial locations visuospatially encoded)
- Neither → When (temporal order relies on distinct mechanism)
- RPM → All domains equally (fluid intelligence is domain-general)

**Theoretical Framework:** Baddeley's working memory model (1992) posits dissociable verbal and visuospatial subsystems. Temporal order memory may rely on hippocampal sequence encoding (Eichenbaum, 2014) not captured by either test.

**Data Required:**
- **DVs:** Mean Theta_What, Theta_Where, Theta_When per UID
- **IVs:** RAVLT_T, BVMT_T, RPM_T
- **Source:** Ch5 5.2.x domain theta scores + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Extract domain-specific theta scores**
   - Load from Ch5 5.2.1/5.2.2/etc. results
   - Compute mean per UID per domain

2. **Fit domain-specific models**
   - Model_What: `Theta_What ~ RAVLT_T + BVMT_T + RPM_T`
   - Model_Where: `Theta_Where ~ RAVLT_T + BVMT_T + RPM_T`
   - Model_When: `Theta_When ~ RAVLT_T + BVMT_T + RPM_T`

3. **Compare beta coefficients across domains**
   - Extract beta_RAVLT for each domain
   - Steiger's Z-test: Is beta_RAVLT_What > beta_RAVLT_Where?
   - Steiger's Z-test: Is beta_BVMT_Where > beta_BVMT_What?

4. **Compare R² across domains**
   - Bootstrap CIs for each model's R²
   - Hypothesis: R²_When < R²_What ≈ R²_Where

5. **Create beta coefficient matrix**
   - Heatmap visualization: rows=domains, columns=tests

**Expected Output:**
```
Domain   R²     RAVLT_beta  BVMT_beta  RPM_beta
What     0.38   0.35***     0.18       0.20*
Where    0.32   0.15        0.38***    0.22*
When     0.15   0.12        0.10       0.18

Domain-Specificity Tests (Steiger's Z):
RAVLT_What > RAVLT_Where: Z=2.45, p=0.014
BVMT_Where > BVMT_What:   Z=2.78, p=0.005
```

**Success Criteria:**
- [ ] RAVLT_beta_What > RAVLT_beta_Where (p < 0.05)
- [ ] BVMT_beta_Where > BVMT_beta_What (p < 0.05)
- [ ] R²_When < R²_What and R²_When < R²_Where
- [ ] RPM shows similar beta across all domains

---

### RQ 7.1.4: Unique REMEMVR variance unexplained by all predictors?

**Research Question:** What proportion of REMEMVR variance remains unexplained after accounting for ALL available predictors (cognitive tests, demographics, self-report)?

**Hypothesis:** Substantial residual (>50%) should remain unexplained, supporting REMEMVR's incremental validity. This "ecological validity gap" is the signal REMEMVR was designed to capture.

**Theoretical Framework:** Incremental validity (Hunsley & Meyer, 2003). Ecological validity gap (Chaytor & Schmitter-Edgecombe, 2003) predicts traditional tests miss naturalistic encoding, multi-day consolidation, and confidence monitoring.

**Data Required:**
- **DV:** Mean Theta_All per UID
- **IVs (hierarchical entry):**
  - Block 1: Age, Sex, Education
  - Block 2: RAVLT_T, BVMT_T, NART_T, RPM_T
  - Block 3: DASS_Dep, DASS_Anx, DASS_Str, VR_Exp, Sleep
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Build hierarchical regression**
   - Model 1: `Theta ~ Age + Sex + Education`
   - Model 2: `Theta ~ Age + Sex + Education + RAVLT + BVMT + NART + RPM`
   - Model 3: `Theta ~ (all above) + DASS_Dep + DASS_Anx + DASS_Str + VR_Exp + Sleep`

2. **Compute incremental R²**
   - Delta_R²_block2 = R²_model2 - R²_model1
   - Delta_R²_block3 = R²_model3 - R²_model2
   - F-test for each increment

3. **Compute Cohen's f² for each block**
   - f² = Delta_R² / (1 - R²_full)
   - Interpret: 0.02=small, 0.15=medium, 0.35=large

4. **Quantify unexplained variance**
   - Residual = 1 - R²_model3
   - Use IRT theta SEs to separate measurement error from true residual

5. **Domain-specific residuals**
   - Repeat for What, Where, When
   - Hypothesis: When shows highest residual

**Expected Output:**
```
Model   Predictors                        R²     Delta_R²  f²
1       Demographics                      0.12   -         -
2       + Cognitive Tests                 0.40   0.28      0.47 (large)
3       + Self-Report                     0.44   0.04      0.07 (small)

Variance Decomposition:
- Explained by all predictors: 44%
- Measurement error (from theta SEs): 8%
- True residual (unique REMEMVR): 48%

Domain-Specific Residuals:
- What: 52% unexplained
- Where: 58% unexplained
- When: 75% unexplained
```

**Success Criteria:**
- [ ] Block 2 (cognitive tests) significant increment (p < 0.00179)
- [ ] Total R² < 0.55 (at least 45% unexplained)
- [ ] True residual (after removing measurement error) > 40%
- [ ] When domain shows highest residual

---

## THEME 2: AGE x VR SCAFFOLDING

### RQ 7.2.1: Does age predict REMEMVR after controlling for cognitive tests?

**Research Question:** Does age explain variance in REMEMVR performance beyond what cognitive tests predict? If not, VR may compensate for age-related decline.

**Hypothesis:** Age should NOT predict REMEMVR after controlling for cognitive tests, consistent with Ch5's age-invariant VR forgetting finding (Age×Time p=.96).

**Theoretical Framework:** VR scaffolding hypothesis - contextual richness in VR compensates for age-related encoding deficits. If true, age effects should be fully mediated by cognitive ability (which VR bypasses through environmental support).

**Data Required:**
- **DV:** Mean Theta_All per UID
- **IVs:** Age (continuous), RAVLT_T, BVMT_T, RPM_T
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Bivariate correlations**
   - r(Age, Theta) = ? (expect small negative)
   - r(Age, RAVLT) = ? (expect negative, from literature)

2. **Hierarchical regression**
   - Model 1: `Theta ~ Age`
   - Model 2: `Theta ~ Age + RAVLT_T + BVMT_T + RPM_T`
   - Does Age remain significant in Model 2?

3. **Mediation analysis (conceptual)**
   - Path a: Age → Cognitive Tests (expect significant)
   - Path b: Cognitive Tests → REMEMVR (from 7.1.1)
   - Path c': Age → REMEMVR controlling for tests (expect NULL)

4. **Compare standardized betas**
   - beta_Age in Model 1 vs Model 2
   - If beta_Age drops to non-significance, tests mediate age effects

**Expected Output:**
```
Bivariate: r(Age, Theta) = -0.18, p = 0.073

Hierarchical Regression:
Model 1: Theta ~ Age
         Age: beta=-0.18, p=0.073
         R² = 0.032

Model 2: Theta ~ Age + RAVLT + BVMT + RPM
         Age:   beta=-0.05, p=0.612 (attenuated to null)
         RAVLT: beta=0.32, p<0.001
         BVMT:  beta=0.26, p=0.008
         RPM:   beta=0.17, p=0.082
         R² = 0.36

Conclusion: Age effects fully mediated by cognitive ability.
VR scaffolding compensates for age-related decline.
```

**Success Criteria:**
- [ ] Age significant (or trending) in bivariate (r < -0.15)
- [ ] Age NOT significant after controlling for tests (p > 0.05)
- [ ] Beta_Age drops substantially from Model 1 to Model 2

---

### RQ 7.2.2: Do cognitive tests attenuate age effects on REMEMVR?

**Research Question:** What proportion of age-related variance is attenuated when controlling for cognitive tests? Complete attenuation suggests tests capture all age-sensitive processes; partial attenuation suggests REMEMVR captures additional age-sensitive processes.

**Hypothesis:** Complete or near-complete attenuation expected, consistent with VR scaffolding hypothesis from Ch5.

**Theoretical Framework:** If RAVLT/BVMT comprehensively measure episodic memory, they should fully explain age-related REMEMVR variance. If attenuation is partial, REMEMVR captures age-sensitive processes beyond traditional tests.

**Data Required:**
- **DV:** Mean Theta_All per UID
- **IVs:** Age, RAVLT_T, BVMT_T, RPM_T
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Compute attenuation ratio**
   - beta_Age_bivariate (from 7.2.1)
   - beta_Age_controlled (from 7.2.1 Model 2)
   - Attenuation = (beta_bivariate - beta_controlled) / beta_bivariate

2. **Domain-specific attenuation**
   - Repeat for What, Where, When
   - Are some domains more age-sensitive than others after control?

3. **Bootstrap confidence intervals**
   - 95% CI for attenuation ratio
   - If CI includes 1.0, complete attenuation

**Expected Output:**
```
Domain   beta_Age (bivariate)  beta_Age (controlled)  Attenuation%
All      -0.18                 -0.05                  72%
What     -0.20                 -0.04                  80%
Where    -0.15                 -0.06                  60%
When     -0.22                 -0.08                  64%

Mean Attenuation: 69% [95% CI: 52%, 86%]
```

**Success Criteria:**
- [ ] Attenuation > 50% for overall REMEMVR
- [ ] No domain shows significant residual age effect after control
- [ ] Pattern consistent with VR scaffolding hypothesis

---

### RQ 7.2.3: Is there an Age x Cognitive Test interaction?

**Research Question:** Do cognitive tests predict REMEMVR differently for younger vs older adults? Tests may be better predictors in older adults if they tap compensatory processes.

**Hypothesis:** Possible Age × Test interaction where tests predict REMEMVR more strongly in older adults. Alternatively, no interaction (tests predict equally across age range).

**Theoretical Framework:** Cognitive reserve theory (Stern, 2002) suggests high-ability older adults compensate for neural decline. Tests may show stronger prediction in older adults who rely more on crystallized abilities.

**Data Required:**
- **DV:** Mean Theta_All per UID
- **IVs:** Age (continuous), RAVLT_T, Age × RAVLT_T
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Center predictors**
   - Age_c = Age - mean(Age)
   - RAVLT_c = RAVLT_T - 50 (already T-scored)

2. **Fit interaction model**
   - Model: `Theta ~ Age_c + RAVLT_c + Age_c:RAVLT_c`
   - Test interaction term significance

3. **Simple slopes analysis (if interaction significant)**
   - RAVLT slope at Age = -1SD (younger)
   - RAVLT slope at Age = +1SD (older)
   - Plot interaction

4. **Repeat for each cognitive test**
   - Age × BVMT interaction
   - Age × RPM interaction

**Expected Output:**
```
Model: Theta ~ Age + RAVLT + Age:RAVLT
       Age:       beta=-0.06, p=0.52
       RAVLT:     beta=0.33, p<0.001
       Age:RAVLT: beta=0.08, p=0.38 (not significant)

Interpretation: No Age × RAVLT interaction.
Tests predict REMEMVR equally across age range.
```

**Success Criteria:**
- [ ] Age × Test interactions tested for all 4 tests
- [ ] Report which interactions are significant (if any)
- [ ] If significant, provide simple slopes interpretation

---

### RQ 7.2.4: VR Scaffolding Validation (NEW)

**Research Question:** Does REMEMVR show age-invariance while RAVLT shows age decline in the same sample? This formally tests the VR scaffolding hypothesis.

**Hypothesis:**
- RAVLT should show significant age decline (r < -0.30, from literature)
- REMEMVR should show minimal age decline (r ≈ 0, from Ch5 finding)
- The difference validates VR's compensatory effect

**Theoretical Framework:** Traditional tests show robust age decline (r = -0.40 to -0.50 for RAVLT). Ch5 found Age×Time p=.96 for VR forgetting. If the same participants show age decline on RAVLT but not REMEMVR, it's the VR context (not the sample) that differs.

**Data Required:**
- **DVs:** RAVLT_Total, Mean Theta_All (standardized)
- **IV:** Age (continuous)
- **Source:** master.xlsx + Ch5
- **N:** 100 participants

**Analysis Specification:**

1. **Compute bivariate correlations**
   - r(Age, RAVLT_Total)
   - r(Age, REMEMVR_Theta)

2. **Test correlation difference**
   - Steiger's Z-test for comparing dependent correlations
   - H0: r_RAVLT = r_REMEMVR
   - H1: |r_RAVLT| > |r_REMEMVR|

3. **Visualize age effects**
   - Scatter plot: Age vs RAVLT with regression line
   - Scatter plot: Age vs REMEMVR with regression line
   - Side-by-side comparison

4. **Report effect size difference**
   - d = (|r_RAVLT| - |r_REMEMVR|) / pooled SE

**Expected Output:**
```
Correlation with Age:
- RAVLT_Total:  r = -0.38, p < 0.001
- REMEMVR_Theta: r = -0.12, p = 0.24

Steiger's Z-test: Z = 2.89, p = 0.004
RAVLT shows significantly stronger age decline than REMEMVR.

Interpretation: VR scaffolding hypothesis SUPPORTED.
Same participants show age decline on traditional test but not VR test.
```

**Success Criteria:**
- [ ] RAVLT shows significant age decline (p < 0.05)
- [ ] REMEMVR shows non-significant age decline (p > 0.10)
- [ ] Difference is significant (Steiger's Z p < 0.05)
- [ ] Consistent with Ch5 age-invariance finding

---

## THEME 3: METACOGNITION PREDICTORS

### RQ 7.3.1: Do cognitive tests predict confidence trajectories? (NEW)

**Research Question:** Do cognitive tests predict confidence ratings (IRT-scaled) as they predict accuracy? This tests whether metacognition shares predictors with memory.

**Hypothesis:** Cognitive tests may predict confidence weakly or not at all. Ch6 established confidence-accuracy dissociation (824× ICC ratio) - if confidence is partially independent, it may have different predictors.

**Theoretical Framework:** Metacognitive monitoring may rely on executive processes (self-awareness, error detection) rather than memory encoding capacity. Tests designed for memory may not predict metacognition.

**Data Required:**
- **DV:** Mean Confidence_Theta per UID (from Ch6 6.1.x)
- **IVs:** RAVLT_T, BVMT_T, RPM_T
- **Source:** Ch6 confidence theta scores + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Extract confidence theta scores**
   - Load from Ch6 6.1.1 or equivalent
   - Compute mean per UID

2. **Fit prediction model**
   - Model: `Confidence_Theta ~ RAVLT_T + BVMT_T + RPM_T`
   - Compare R² to accuracy prediction (from 7.1.1)

3. **Compare predictors for accuracy vs confidence**
   - Which tests predict accuracy but not confidence?
   - Which predict both?
   - Which predict neither?

**Expected Output:**
```
                      R²      RAVLT_beta  BVMT_beta  RPM_beta
Accuracy (7.1.1)      0.35    0.32***     0.25**     0.18
Confidence (7.3.1)    0.18    0.15        0.12       0.22*

Observation: RPM (fluid intelligence) predicts confidence more than RAVLT/BVMT.
Metacognitive monitoring may rely on executive/reasoning processes.
```

**Success Criteria:**
- [ ] R²_confidence < R²_accuracy (confidence less predicted)
- [ ] Report which tests predict confidence vs accuracy differently
- [ ] Connects to Ch6 confidence-accuracy dissociation

---

### RQ 7.3.2: Do cognitive tests predict calibration quality? (NEW)

**Research Question:** Do cognitive tests predict who is well-calibrated (confidence matches accuracy) vs overconfident (confidence exceeds accuracy)?

**Hypothesis:** RPM may predict calibration (metacognitive monitoring requires reasoning). RAVLT/BVMT may not (memory capacity ≠ metacognitive accuracy).

**Theoretical Framework:** Calibration requires comparing internal confidence signals to actual performance - a metacognitive executive function. This differs from memory encoding capacity.

**Data Required:**
- **DV:** Calibration metric per UID (from Ch6 6.2.x - resolution or Brier decomposition)
- **IVs:** RAVLT_T, BVMT_T, RPM_T
- **Source:** Ch6 calibration results + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Extract calibration metric**
   - Options: Resolution, Calibration slope, Brier reliability
   - Compute per-participant calibration quality

2. **Fit prediction model**
   - Model: `Calibration ~ RAVLT_T + BVMT_T + RPM_T`

3. **Compare to accuracy/confidence prediction**
   - Is calibration predicted by different tests?

**Expected Output:**
```
Model: Calibration ~ RAVLT + BVMT + RPM
R² = 0.12
RAVLT: beta=0.08, p=0.42
BVMT:  beta=0.06, p=0.55
RPM:   beta=0.24, p=0.018

Conclusion: Only RPM predicts calibration quality.
Metacognitive accuracy relies on fluid reasoning, not memory capacity.
```

**Success Criteria:**
- [ ] R² for calibration < R² for accuracy
- [ ] Identify which (if any) test predicts calibration
- [ ] Theoretical interpretation connecting to metacognition literature

---

### RQ 7.3.3: Do cognitive tests predict HCE rate? (NEW)

**Research Question:** Who makes more high-confidence errors (HCE)? Ch6 found 15-20% stable HCE rate - do individual differences have cognitive predictors?

**Hypothesis:** Lower RPM may predict higher HCE rate (monitoring failure from limited executive resources). RAVLT/BVMT may not predict HCE (memory capacity is orthogonal to monitoring failure).

**Theoretical Framework:** HCE represents monitoring failure - confident when wrong. This requires executive control to detect errors. If RPM measures executive capacity, lower RPM should predict more HCEs.

**Data Required:**
- **DV:** HCE_Rate per UID (from Ch6 6.6.x - proportion of errors that are high-confidence)
- **IVs:** RAVLT_T, BVMT_T, RPM_T, Age
- **Source:** Ch6 HCE results + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Extract HCE rates**
   - From Ch6 6.6.1 or equivalent
   - Compute mean HCE rate per UID

2. **Fit prediction model**
   - Model: `HCE_Rate ~ RAVLT_T + BVMT_T + RPM_T + Age`

3. **Test hypothesized predictors**
   - Is RPM negatively associated with HCE_Rate?
   - Does Age predict HCE_Rate?

**Expected Output:**
```
Model: HCE_Rate ~ RAVLT + BVMT + RPM + Age
R² = 0.15
RAVLT: beta=-0.05, p=0.62
BVMT:  beta=-0.08, p=0.44
RPM:   beta=-0.28, p=0.008 (higher RPM = fewer HCEs)
Age:   beta=0.15, p=0.14

Conclusion: Fluid intelligence predicts fewer high-confidence errors.
```

**Success Criteria:**
- [ ] HCE rate has identifiable predictors
- [ ] Report direction of significant effects
- [ ] Connect to Ch6 HCE mechanism interpretation

---

### RQ 7.3.4: Does DASS predict metacognition more than memory? (NEW)

**Research Question:** Does anxiety/depression predict metacognitive accuracy (confidence, calibration) more than memory accuracy?

**Hypothesis:** DASS-Anxiety may impair metacognitive monitoring (worry disrupts self-evaluation) without impairing memory encoding. This would show as DASS predicting confidence/calibration but not accuracy.

**Theoretical Framework:** Anxiety impairs executive functions (worry occupies working memory). Metacognitive monitoring requires executive resources. Memory encoding may be more automatic and less affected by anxiety.

**Data Required:**
- **DVs:** Mean Theta_All, Mean Confidence_Theta, Calibration
- **IVs:** DASS_Dep, DASS_Anx, DASS_Str
- **Source:** Ch5 + Ch6 + master.xlsx
- **N:** ~97 (some DASS missing)

**Analysis Specification:**

1. **Fit models for each DV**
   - Model_Accuracy: `Theta ~ DASS_Dep + DASS_Anx + DASS_Str`
   - Model_Confidence: `Confidence ~ DASS_Dep + DASS_Anx + DASS_Str`
   - Model_Calibration: `Calibration ~ DASS_Dep + DASS_Anx + DASS_Str`

2. **Compare beta coefficients**
   - Does DASS_Anx predict metacognition more than accuracy?

3. **Control for cognitive ability**
   - Add RAVLT, RPM as covariates
   - Do DASS effects remain?

**Expected Output:**
```
               R²      DASS_Dep   DASS_Anx   DASS_Str
Accuracy       0.05    -0.08      -0.12      -0.06
Confidence     0.11    -0.18*     -0.22*     -0.10
Calibration    0.09    -0.10      -0.24*     -0.05

Conclusion: Anxiety specifically impairs metacognitive monitoring.
Memory accuracy relatively preserved.
```

**Success Criteria:**
- [ ] Compare DASS effects on accuracy vs metacognition
- [ ] Report if DASS_Anx shows differential prediction
- [ ] Control for cognitive ability to rule out confound

---

### RQ 7.3.5: Does confidence-accuracy gap predict cognitive reserve? (NEW)

**Research Question:** Do individuals with high confidence AND high accuracy (well-calibrated high performers) show signs of cognitive reserve?

**Hypothesis:** High-performers with good calibration may have higher education, higher RPM, suggesting metacognitive awareness as reserve indicator.

**Theoretical Framework:** Cognitive reserve (Stern, 2002) suggests some individuals maintain function despite aging. Good metacognitive monitoring (knowing what you know) may be a reserve indicator.

**Data Required:**
- **Variables:** Accuracy_Theta, Confidence_Theta, Education, Age, RPM
- **Derived:** Calibration_Group (well-calibrated vs overconfident vs underconfident)
- **Source:** Ch5 + Ch6 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Create calibration groups**
   - Compute confidence-accuracy residual
   - Group: Overconfident (residual > 0.5 SD), Underconfident (< -0.5 SD), Well-calibrated (middle)

2. **Compare groups on predictors**
   - ANOVA: Education by calibration group
   - ANOVA: RPM by calibration group
   - ANOVA: Age by calibration group

3. **Correlate calibration with reserve indicators**
   - r(Calibration_quality, Education)
   - r(Calibration_quality, RPM)

**Expected Output:**
```
Calibration Group   n    Education   RPM      Age
Well-calibrated     35   15.2        7.8      48
Overconfident       40   13.5        6.2      52
Underconfident      25   14.8        7.0      45

F-test Education: F=3.2, p=0.045
F-test RPM: F=4.8, p=0.010

Well-calibrated individuals have higher education and RPM.
```

**Success Criteria:**
- [ ] Create meaningful calibration groups
- [ ] Test group differences on reserve indicators
- [ ] Report if well-calibrated group differs from others

---

## THEME 4: PROCESS-SPECIFIC PREDICTION

### RQ 7.4.1: Does RAVLT Free Recall predict REMEMVR Free Recall > Recognition?

**Research Question:** Does RAVLT (a verbal free recall task) show stronger prediction for REMEMVR Free Recall than Recognition, consistent with process-specific transfer?

**Hypothesis:** r(RAVLT, REMEMVR_FreeRecall) > r(RAVLT, REMEMVR_Recognition). Both RAVLT and Free Recall require generative retrieval (self-initiated search), while Recognition relies on familiarity.

**Theoretical Framework:** Transfer-appropriate processing (Morris et al., 1977). Performance is better when encoding-retrieval processes match. RAVLT and REMEMVR Free Recall engage similar retrieval strategies.

**Data Required:**
- **DVs:** Mean Theta_FreeRecall, Mean Theta_Recognition per UID
- **IV:** RAVLT_Total (not T-scored, use raw)
- **Source:** Ch5 5.3.x paradigm theta scores + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Compute bivariate correlations**
   - r1 = cor(RAVLT, Theta_FreeRecall)
   - r2 = cor(RAVLT, Theta_Recognition)

2. **Test process-specificity**
   - Steiger's Z-test: H1: r1 > r2
   - Alpha = 0.00179 (chapter-level)

3. **Visualize**
   - Scatter plots with regression lines
   - Difference in slopes visually apparent

**Expected Output:**
```
r(RAVLT, FreeRecall)   = 0.45, p < 0.001
r(RAVLT, Recognition)  = 0.28, p = 0.005

Steiger's Z = 2.12, p = 0.034
RAVLT predicts Free Recall significantly more than Recognition.
Process-specific transfer confirmed.
```

**Success Criteria:**
- [ ] Both correlations significant
- [ ] r_FreeRecall > r_Recognition
- [ ] Difference significant (Steiger's Z)

---

### RQ 7.4.2: Does BVMT predict Where more than What?

**Research Question:** Does BVMT (visuospatial memory test) show stronger prediction for Where (spatial location) than What (object identity)?

**Hypothesis:** r(BVMT, Where) > r(BVMT, What). BVMT requires spatial configuration memory, which should transfer to REMEMVR Where domain.

**Theoretical Framework:** Domain-specificity - visuospatial tests predict visuospatial memory. Object identity (What) may rely more on verbal encoding.

**Data Required:**
- **DVs:** Mean Theta_Where, Mean Theta_What per UID
- **IV:** BVMT_TotR
- **Source:** Ch5 5.2.x domain theta scores + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Compute bivariate correlations**
   - r1 = cor(BVMT, Theta_Where)
   - r2 = cor(BVMT, Theta_What)

2. **Test domain-specificity**
   - Steiger's Z-test: H1: r1 > r2

**Expected Output:**
```
r(BVMT, Where) = 0.42, p < 0.001
r(BVMT, What)  = 0.28, p = 0.005

Steiger's Z = 1.76, p = 0.078
Marginal support for domain-specificity.
```

**Success Criteria:**
- [ ] r_Where > r_What in expected direction
- [ ] Report whether difference is significant

---

### RQ 7.4.3: Does RPM predict complex integration?

**Research Question:** Does RPM (fluid intelligence) predict performance on items requiring integration of What+Where+When information?

**Hypothesis:** RPM should predict complex integration items more than simple items. Relational binding across domains requires fluid reasoning.

**Theoretical Framework:** Fluid intelligence supports relational binding and complex integration (Oberauer, 2019). Items requiring What+Where+When may tap RPM more than single-domain items.

**Data Required:**
- **DVs:** Theta for high-integration vs low-integration items (if available)
- **IV:** RPM_Scor
- **Alternative:** Composite theta across all domains vs single-domain theta
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Define integration complexity**
   - Option A: Use Order (-O-) questions as proxy for temporal integration
   - Option B: Compare overall theta (requires all domains) vs single-domain

2. **Compute correlations**
   - r(RPM, Theta_Integration)
   - r(RPM, Theta_SingleDomain)

3. **Test differential prediction**
   - Steiger's Z-test for difference

**Expected Output:**
```
r(RPM, Overall_Theta)     = 0.32, p = 0.001
r(RPM, What_Only_Theta)   = 0.25, p = 0.012

Difference not significant (Z=0.85, p=0.39)
RPM predicts both integration and single-domain similarly.
```

**Success Criteria:**
- [ ] Report RPM correlation with overall performance
- [ ] Compare to domain-specific predictions
- [ ] Interpret in terms of fluid intelligence role

---

## THEME 5: SELF-REPORT & CONTEXTUAL

### RQ 7.5.1: Do sleep, education, VR experience predict REMEMVR?

**Research Question:** Do self-reported factors (typical sleep, education level, VR experience) predict REMEMVR performance?

**Hypothesis:**
- Sleep: May predict consolidation (slope) but not encoding (intercept)
- Education: Should predict performance (cognitive reserve)
- VR_Experience: May reduce novelty effects, improving performance

**Data Required:**
- **DV:** Mean Theta_All per UID
- **IVs:** Typical_Sleep, Education, VR_Exp
- **Covariates:** Age (control for confound)
- **Source:** master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Fit regression model**
   - Model: `Theta ~ Sleep + Education + VR_Exp + Age`

2. **Test each predictor**
   - Report beta, p-value for each

3. **Compare to cognitive test effects (from 7.1.1)**
   - Do self-report factors add beyond cognitive tests?

**Expected Output:**
```
Model: Theta ~ Sleep + Education + VR_Exp + Age
R² = 0.18

Predictor    Beta    p
Sleep        0.12    0.24
Education    0.22    0.032
VR_Exp       0.08    0.42
Age         -0.15    0.14

Only Education significantly predicts performance.
```

**Success Criteria:**
- [ ] Report all predictor effects
- [ ] Identify significant predictors
- [ ] Compare to cognitive test model R²

---

### RQ 7.5.2: Does DASS predict memory performance?

**Research Question:** Do depression, anxiety, or stress (DASS subscales) predict REMEMVR accuracy?

**Hypothesis:** Small negative effects expected. Depression may impair encoding motivation. Anxiety may impair working memory during retrieval.

**Data Required:**
- **DV:** Mean Theta_All per UID
- **IVs:** DASS_Dep, DASS_Anx, DASS_Str
- **Source:** master.xlsx
- **N:** ~97 (some missing)

**Analysis Specification:**

1. **Descriptive statistics for DASS**
   - Mean, SD, range for each subscale
   - Check for floor/ceiling effects

2. **Fit regression model**
   - Model: `Theta ~ DASS_Dep + DASS_Anx + DASS_Str`

3. **Control for age and cognitive ability**
   - Add Age, RAVLT as covariates
   - Do DASS effects remain?

**Expected Output:**
```
DASS Descriptives:
Depression: M=8.2, SD=7.5, Range=0-28
Anxiety:    M=6.5, SD=6.2, Range=0-24
Stress:     M=10.1, SD=7.8, Range=0-30

Model: Theta ~ DASS_Dep + DASS_Anx + DASS_Str
R² = 0.06

No DASS subscale significantly predicts accuracy (all p > 0.10).
```

**Success Criteria:**
- [ ] Report DASS effects on accuracy
- [ ] Compare to metacognition effects (from 7.3.4)
- [ ] Control for cognitive ability

---

### RQ 7.5.3: Do memory strategies correlate with performance?

**Research Question:** Do self-reported memory strategies (rehearsal, visualization, mnemonics) predict REMEMVR performance?

**Hypothesis:** Active strategy use may improve performance, but effect may be small given incidental encoding paradigm.

**Data Required:**
- **DV:** Mean Theta_All per UID
- **IVs:** Strategy variables from STR questionnaire (require coding)
- **Source:** master.xlsx STR tags
- **N:** 100 participants

**Analysis Specification:**

1. **Code strategy variables**
   - Rehearsal frequency: `{UID}-RVR-T{N}-STR-X-TNK1-` (quantitative)
   - Mnemonic use: `{UID}-RVR-T{N}-STR-X-MNE1-` (requires text coding)

2. **Compute strategy index**
   - Mean rehearsal frequency across tests
   - Binary: Any mnemonic use (yes/no)

3. **Correlate with performance**
   - r(Rehearsal, Theta)
   - Compare strategy users vs non-users

**Expected Output:**
```
Rehearsal frequency: r = 0.18, p = 0.07
Mnemonic use (Yes vs No): t = 1.45, p = 0.15

Strategies show marginal positive effects but not significant.
```

**Success Criteria:**
- [ ] Successfully extract strategy variables
- [ ] Report correlations with performance
- [ ] Acknowledge text coding limitations

---

### RQ 7.5.4: Per-Test Sleep Predicting Same-Test Performance (NEW)

**Research Question:** Does sleep quality BEFORE each test predict THAT test's performance? This uses unique per-test sleep data.

**Hypothesis:** Poor sleep before a specific test should impair that test's performance (state-dependent effect), beyond trait-level sleep quality.

**Theoretical Framework:** Sleep deprivation impairs memory retrieval acutely. Per-test sleep data allows within-person state analysis.

**Data Required:**
- **DV:** Theta per test (T1, T2, T3, T4)
- **IVs:** Sleep_Hours, Sleep_Quality per test
- **Structure:** 400 observations (100 UIDs × 4 tests)
- **Source:** master.xlsx SLP tags + Ch5 theta per test

**Analysis Specification:**

1. **Extract per-test sleep data**
   - `{UID}-RVR-T{N}-SLP-X-HOUR-`
   - `{UID}-RVR-T{N}-SLP-X-QUAL-`

2. **Merge with per-test theta**
   - Match by UID and Test number

3. **Fit multilevel model**
   - Model: `Theta ~ Hours_Slept + Sleep_Quality + (1|UID)`
   - Tests within-person effect of sleep

4. **Compare within-person vs between-person effects**
   - Add person-mean sleep as between-person predictor
   - Decompose variance

**Expected Output:**
```
Multilevel Model: Theta ~ Hours + Quality + (1|UID)

Fixed Effects:
Hours_Slept:   beta=0.05, SE=0.02, p=0.015 (within-person)
Sleep_Quality: beta=0.08, SE=0.03, p=0.008 (within-person)

Interpretation: Better sleep before a test improves that test's performance.
This is a state-dependent effect, not just trait sleep quality.
```

**Success Criteria:**
- [ ] Successfully extract and merge per-test sleep
- [ ] Fit multilevel model with random intercepts
- [ ] Report within-person sleep effects
- [ ] Novel contribution using unique longitudinal data

---

## THEME 6: INDIVIDUAL DIFFERENCES IN FORGETTING

### RQ 7.6.1: Do cognitive tests predict individual differences in slope?

**Research Question:** Do cognitive tests predict the rate of forgetting (slope), or only initial encoding (intercept)?

**Hypothesis:** Cognitive tests should NOT predict slope. Ch5 found ICC_slope = 21% under model averaging - there ARE individual differences in slope, but tests may not capture the processes that govern them (consolidation).

**Theoretical Framework:** Slopes reflect consolidation/forgetting processes, which differ from encoding. Traditional tests measure encoding (immediate recall), not consolidation (multi-day retention).

**Data Required:**
- **DV:** Per-participant slope from model-averaged LMM
- **IVs:** RAVLT_T, BVMT_T, RPM_T
- **Source:** Ch5 5.1.4 model-averaged random effects + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Extract model-averaged slopes**
   - From Ch5 5.1.4 or 5.1.1 extended analysis
   - Each participant has estimated slope under model averaging

2. **Fit prediction model**
   - Model: `Slope ~ RAVLT_T + BVMT_T + RPM_T`
   - Compare R² to intercept prediction (from 7.1.2)

3. **Identify any slope predictors**
   - Which (if any) tests predict forgetting rate?

**Expected Output:**
```
Model: Slope ~ RAVLT + BVMT + RPM
R² = 0.06, F(3,96) = 2.0, p = 0.12

No predictor significant (all p > 0.10).
Cognitive tests do NOT predict forgetting rate.
Individual differences in slope exist (ICC=21%) but are not predicted by traditional tests.
```

**Success Criteria:**
- [ ] R²_slope < R²_intercept (from 7.1.2)
- [ ] Report which (if any) tests predict slope
- [ ] Connect to Ch5 ICC_slope finding

---

### RQ 7.6.2: Does RAVLT Delayed predict REMEMVR slope? (NEW)

**Research Question:** Does RAVLT forgetting (T5 - Delayed Recall) predict REMEMVR forgetting rate? This tests whether short-term forgetting predicts long-term forgetting.

**Hypothesis:** Possible weak correlation. RAVLT delay is 20-30 min; REMEMVR is 6 days. If consolidation processes generalize, RAVLT forgetting should predict REMEMVR slope.

**Theoretical Framework:** If forgetting reflects stable individual differences in consolidation efficiency, different time scales should correlate.

**Data Required:**
- **DV:** Per-participant REMEMVR slope
- **IV:** RAVLT_Forgetting = T5Sc - DRSc
- **Source:** Ch5 slopes + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Compute RAVLT forgetting index**
   - RAVLT_Forgetting = RAV_T5Sc - RAV_DRSc

2. **Correlate with REMEMVR slope**
   - r(RAVLT_Forgetting, REMEMVR_Slope)

3. **Control for initial encoding**
   - Partial correlation controlling for RAVLT_T5 and REMEMVR_Intercept

**Expected Output:**
```
r(RAVLT_Forgetting, REMEMVR_Slope) = 0.15, p = 0.14

Partial r (controlling for encoding): r = 0.12, p = 0.24

Weak, non-significant relationship.
Short-term and long-term forgetting may not share mechanisms.
```

**Success Criteria:**
- [ ] Report bivariate and partial correlations
- [ ] Interpret in terms of consolidation mechanisms
- [ ] Compare to encoding-to-encoding correlations (7.1.1)

---

### RQ 7.6.3: ICC slope replication across domains (NEW)

**Research Question:** Does the ICC_slope pattern (21% between-person variance) replicate across What, Where, When domains?

**Hypothesis:** From Ch5 findings:
- What/Where should show ICC_slope ≈ 20%
- When may show lower ICC_slope (measurement issues with 77% item exclusion)

**Data Required:**
- **DVs:** Per-participant slopes for What, Where, When from domain-specific LMMs
- **Source:** Ch5 5.2.x domain analyses
- **N:** 100 participants

**Analysis Specification:**

1. **Extract domain-specific slopes**
   - From Ch5 5.2.1 (What), 5.2.2 (Where), etc.
   - Or re-fit domain-specific LMMs

2. **Compute ICC for each domain's slope variance**
   - ICC_slope_What
   - ICC_slope_Where
   - ICC_slope_When

3. **Compare ICCs**
   - Bootstrap CIs for each ICC
   - Test differences

**Expected Output:**
```
Domain   ICC_slope   95% CI
What     0.19        [0.08, 0.32]
Where    0.22        [0.10, 0.35]
When     0.08        [0.00, 0.20]

When domain shows lowest ICC_slope - consistent with measurement issues.
```

**Success Criteria:**
- [ ] Report domain-specific ICC_slopes
- [ ] Compare to overall ICC_slope (21%)
- [ ] Note When domain limitations

---

### RQ 7.6.4: Purification & Slope Predictors (NEW)

**Research Question:** Do predictors of slope CHANGE after IRT purification? Ch5 found purification-trajectory paradox.

**Hypothesis:** Pre-purification and post-purification slopes may have different predictors, as purification changes what items contribute.

**Theoretical Framework:** The purification paradox (from Ch5) showed improved static fit but worse dynamic fit. Exploring whether predictors change informs this paradox.

**Data Required:**
- **DVs:** Slopes from Pass 1 (pre-purification) and Pass 2 (post-purification) IRT
- **IVs:** RAVLT_T, BVMT_T, RPM_T
- **Source:** Ch5 5.2.5 or equivalent + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Extract pre- and post-purification slopes**
   - From Ch5 IRT pass comparisons

2. **Fit prediction models for each**
   - Model_Pass1: `Slope_Pass1 ~ RAVLT + BVMT + RPM`
   - Model_Pass2: `Slope_Pass2 ~ RAVLT + BVMT + RPM`

3. **Compare coefficients**
   - Do predictors differ between passes?

**Expected Output:**
```
           R²      RAVLT_beta  BVMT_beta  RPM_beta
Pass 1     0.10    0.12        0.18       0.15
Pass 2     0.05    0.06        0.08       0.12

Predictor relationships weaken after purification.
Consistent with purification-trajectory paradox.
```

**Success Criteria:**
- [ ] Compare prediction models across purification passes
- [ ] Connect to Ch5 purification findings
- [ ] Interpret differences theoretically

---

## THEME 7: CLINICAL UTILITY & ALTERNATIVE INTERPRETATION

### RQ 7.7.1: Reverse Inference - Can REMEMVR predict RAVLT?

**Research Question:** Can REMEMVR performance predict standard test performance (RAVLT, BVMT)? If REMEMVR is a "purer" episodic measure, it should predict traditional tests.

**Hypothesis:** Bidirectional prediction - tests predict REMEMVR and REMEMVR predicts tests, but neither completely explains the other.

**Theoretical Framework:** Reverse inference tests whether REMEMVR contains the construct measured by traditional tests. If REMEMVR fully encompasses RAVLT's construct, REMEMVR → RAVLT should be strong.

**Data Required:**
- **DVs:** RAVLT_Total, BVMT_TotR
- **IV:** Mean Theta_All
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Fit reverse regression**
   - Model: `RAVLT_Total ~ REMEMVR_Theta`
   - Report R², beta

2. **Compare to forward regression (from 7.1.1)**
   - Forward R²: Tests → REMEMVR
   - Reverse R²: REMEMVR → Tests

3. **Interpret asymmetry**
   - If forward > reverse: Tests contain unique construct REMEMVR doesn't measure
   - If reverse > forward: REMEMVR is a superset of tests

**Expected Output:**
```
Direction                    R²
Forward (Tests→REMEMVR)      0.35
Reverse (REMEMVR→RAVLT)      0.28
Reverse (REMEMVR→BVMT)       0.22

REMEMVR predicts traditional tests moderately.
Bidirectional relationship confirms shared construct.
```

**Success Criteria:**
- [ ] Report reverse prediction R²
- [ ] Compare to forward prediction
- [ ] Interpret in terms of construct overlap

---

### RQ 7.7.2: Discrepancy Analysis - Who diverges? (NEW)

**Research Question:** Who shows RAVLT-REMEMVR divergence (high on one, low on other)? What characterizes these individuals?

**Hypothesis:** Divergent individuals may differ systematically - e.g., older adults with high REMEMVR but low RAVLT may benefit from VR scaffolding.

**Theoretical Framework:** Clinical utility - when traditional tests and ecological tests disagree, understanding who diverges helps interpretation.

**Data Required:**
- **Variables:** RAVLT_Total_z, REMEMVR_Theta_z (both standardized)
- **Derived:** Discrepancy = REMEMVR_z - RAVLT_z
- **Predictors:** Age, Education, VR_Exp
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Compute discrepancy score**
   - REMEMVR_z - RAVLT_z
   - Positive = better on REMEMVR than RAVLT

2. **Identify divergent cases**
   - Discrepancy > 1 SD: "VR-favored" (n ≈ 16)
   - Discrepancy < -1 SD: "RAVLT-favored" (n ≈ 16)
   - |Discrepancy| < 1 SD: "Concordant" (n ≈ 68)

3. **Compare groups on characteristics**
   - Age: Are VR-favored cases older?
   - Education: Any differences?
   - VR_Experience: Do experienced VR users show VR advantage?

**Expected Output:**
```
Group           n    Age(M)   Education(M)   VR_Exp(M)
VR-favored      18   56.2     13.8           1.8
RAVLT-favored   14   42.5     15.2           1.2
Concordant      68   48.8     14.5           1.5

VR-favored group is significantly OLDER (F=4.2, p=0.018).
VR scaffolding benefits older adults specifically.
```

**Success Criteria:**
- [ ] Create meaningful discrepancy groups
- [ ] Compare groups on predictors
- [ ] Interpret clinical implications

---

### RQ 7.7.3: Alternative RAVLT Scoring (NEW)

**Research Question:** Does RAVLT Learning Slope (T5-T1/T1) predict REMEMVR better than RAVLT Total? Can we suggest better RAVLT interpretation?

**Hypothesis:** Learning slope may better capture encoding efficiency, which should transfer to REMEMVR. Total conflates learning speed with baseline.

**Theoretical Framework:** Clinical utility - if alternative RAVLT scores predict ecological memory better, clinicians should use them.

**Data Required:**
- **DV:** Mean Theta_All
- **IVs:** RAVLT_Total, RAVLT_Learning (T5-T1), RAVLT_LearningSlope ((T5-T1)/T1)
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Compute alternative RAVLT scores**
   - Learning = T5Sc - T1Sc
   - LearningSlope = (T5Sc - T1Sc) / T1Sc (proportional gain)
   - Forgetting = T5Sc - DRSc

2. **Compare predictive validity**
   - Model 1: `Theta ~ RAVLT_Total`
   - Model 2: `Theta ~ RAVLT_Learning`
   - Model 3: `Theta ~ RAVLT_LearningSlope`
   - Model 4: `Theta ~ RAVLT_Total + RAVLT_Learning` (incremental)

3. **Test incremental validity**
   - Does Learning add to Total?
   - Does LearningSlope outperform Total?

**Expected Output:**
```
Scoring Method         R²      Beta
RAVLT_Total            0.22    0.47
RAVLT_Learning         0.18    0.42
RAVLT_LearningSlope    0.15    0.39
RAVLT_Total + Learning 0.26    Total=0.35, Learning=0.22

Learning adds marginal unique variance beyond Total.
Clinical recommendation: Report both Total and Learning.
```

**Success Criteria:**
- [ ] Compare alternative RAVLT scoring methods
- [ ] Report which predicts REMEMVR best
- [ ] Provide clinical interpretation guidance

---

### RQ 7.7.4: Clinical Profiles - False Negatives (NEW)

**Research Question:** Can we identify "false negatives" - individuals with low RAVLT but normal REMEMVR? These may have intact ecological memory despite poor lab performance.

**Hypothesis:** Some low-RAVLT individuals may show normal REMEMVR, suggesting traditional tests underestimate their real-world memory function.

**Theoretical Framework:** Clinical utility - false negatives on traditional tests may receive unnecessary concern. REMEMVR could provide reassurance.

**Data Required:**
- **Variables:** RAVLT_Total_z, REMEMVR_Theta_z
- **Criteria:** Low RAVLT (z < -1), Normal REMEMVR (z > -0.5)
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Identify false negatives**
   - RAVLT_z < -1 AND REMEMVR_z > -0.5
   - Count cases meeting criteria

2. **Characterize false negatives**
   - Age, Education, VR_Experience
   - NART (premorbid IQ) - may suggest language confound

3. **Compare to true positives**
   - True positive: Both low (z < -1)
   - Are false negatives older? Higher education? Non-native English?

**Expected Output:**
```
Classification Matrix:
                    REMEMVR_Normal  REMEMVR_Low
RAVLT_Low (n=16)    6 (false neg)   10 (true pos)
RAVLT_Normal (n=84) 70 (true neg)   14 (false pos)

False Negatives (n=6): M_Age=58, M_Education=14.2
True Positives (n=10): M_Age=52, M_Education=12.8

False negatives may be older adults with intact ecological memory.
```

**Success Criteria:**
- [ ] Identify false negative cases
- [ ] Characterize them demographically
- [ ] Discuss clinical implications

---

## THEME 8: LATENT PROFILES & MODELS

### RQ 7.8.1: Distinct REMEMVR memory profiles?

**Research Question:** Are there distinct latent profiles of REMEMVR performance (e.g., "generalists" vs "specialists" vs "low performers")?

**Hypothesis:** Expect 2-4 profiles:
- Generalists: High on all domains
- What-specialists: High What, lower Where/When
- Low performers: Low across all domains

**Theoretical Framework:** Latent Profile Analysis identifies subgroups with distinct patterns. If memory is unidimensional, one profile should fit. If multidimensional, multiple profiles emerge.

**Data Required:**
- **Variables:** Mean Theta_What, Theta_Where, Theta_When per UID
- **Source:** Ch5 domain theta scores
- **N:** 100 participants

**Analysis Specification:**

1. **Fit LPA with K=1,2,3,4 profiles**
   - Variables: What, Where, When (standardized)
   - Compare fit: BIC, AIC, entropy, LMR-LRT

2. **Select optimal K**
   - Use BIC minimum or LMR-LRT significance

3. **Characterize profiles**
   - Mean What, Where, When for each profile
   - Label profiles meaningfully

4. **Validate profiles**
   - Do profiles differ on age, cognitive tests?

**Expected Output:**
```
LPA Fit Comparison:
K=1: BIC=850
K=2: BIC=825, LMR p=0.02
K=3: BIC=820, LMR p=0.12
K=4: BIC=828, LMR p=0.35

Optimal: K=3 (BIC minimum, K=2 significant improvement)

Profile Characterization:
Profile 1 (n=45): Generalist - high on all domains
Profile 2 (n=35): Average - moderate on all
Profile 3 (n=20): Low performer - low on all
```

**Success Criteria:**
- [ ] Fit LPA with multiple K values
- [ ] Select optimal K using fit indices
- [ ] Characterize and label profiles

---

### RQ 7.8.2: Cognitive test profiles predict REMEMVR profiles?

**Research Question:** Do cognitive test profiles (e.g., verbal-dominant vs spatial-dominant) correspond to REMEMVR profiles?

**Hypothesis:** Verbal-dominant (high RAVLT, low BVMT) may predict What-specialist profile. Spatial-dominant may predict Where-specialist. Generalists high on both.

**Data Required:**
- **REMEMVR profiles:** From 7.8.1
- **Cognitive test profiles:** LPA on RAVLT, BVMT, RPM
- **Source:** 7.8.1 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Fit LPA on cognitive tests**
   - Variables: RAVLT_T, BVMT_T, RPM_T
   - Select optimal K

2. **Cross-tabulate profiles**
   - Cognitive profile × REMEMVR profile
   - Chi-square test of association

3. **Calculate correspondence**
   - Cramér's V for association strength
   - Do test profiles predict memory profiles?

**Expected Output:**
```
Cross-tabulation:
                    REMEMVR_Generalist  REMEMVR_Average  REMEMVR_Low
Cog_HighAll (n=30)  22                  6                2
Cog_Average (n=50)  18                  25               7
Cog_LowAll (n=20)   5                   4                11

Chi-square = 28.5, p < 0.001
Cramér's V = 0.38 (medium-large association)

Cognitive profiles moderately predict REMEMVR profiles.
```

**Success Criteria:**
- [ ] Fit cognitive LPA
- [ ] Cross-tabulate with REMEMVR profiles
- [ ] Report association strength

---

### RQ 7.8.3: Parsimonious predictive model with cross-validation

**Research Question:** What is the most parsimonious model to predict REMEMVR, and how well does it generalize?

**Hypothesis:** Age + RAVLT + BVMT should achieve R² ≈ 0.30-0.35 with minimal overfitting. Adding more predictors may not improve cross-validated R².

**Data Required:**
- **DV:** Mean Theta_All
- **Candidate IVs:** Age, RAVLT, BVMT, NART, RPM, Education, DASS, Sleep
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Fit candidate models**
   - Minimal: Age + RAVLT
   - Core: Age + RAVLT + BVMT
   - Extended: + RPM + Education
   - Full: All predictors

2. **5-fold cross-validation**
   - Compute CV-R² for each model
   - Compare training R² to CV-R² (overfitting gap)

3. **Select parsimonious model**
   - Best CV-R² with fewest predictors
   - Report shrinkage from training to CV

**Expected Output:**
```
Model                  R²_train  R²_CV    Shrinkage
Age + RAVLT            0.28      0.24     0.04
Age + RAVLT + BVMT     0.36      0.31     0.05
+ RPM + Education      0.40      0.33     0.07
Full (11 predictors)   0.45      0.28     0.17

Optimal: Age + RAVLT + BVMT
Best CV-R² with acceptable shrinkage.
```

**Success Criteria:**
- [ ] Compare multiple models with CV
- [ ] Select parsimonious model
- [ ] Report CV-R² for generalization

---

### RQ 7.8.4: Multivariate vs univariate prediction

**Research Question:** Does predicting all three domains jointly (multivariate) outperform separate domain predictions?

**Hypothesis:** Multivariate model should fit better because domains are correlated. Efficiency gain from joint modeling.

**Data Required:**
- **DVs:** Theta_What, Theta_Where, Theta_When
- **IVs:** Age, RAVLT, BVMT, RPM
- **Source:** Ch5 + master.xlsx
- **N:** 100 participants

**Analysis Specification:**

1. **Fit univariate models**
   - Separate: What, Where, When each predicted by all IVs
   - Sum univariate R² values

2. **Fit multivariate model**
   - MANOVA or multivariate regression
   - Joint R² (Pillai's trace or similar)

3. **Compare approaches**
   - AIC comparison
   - Do cross-domain covariances improve prediction?

**Expected Output:**
```
Approach        AIC      Interpretation
Univariate      1250     3 separate models
Multivariate    1235     1 joint model

Multivariate slightly better (ΔAIC=15).
Cross-domain covariances improve efficiency.
```

**Success Criteria:**
- [ ] Fit both approaches
- [ ] Compare fit statistics
- [ ] Interpret in terms of domain structure

---

## SUMMARY

### Total RQs: 28

| Theme | RQs | Description |
|-------|-----|-------------|
| 1. Predictive Validity | 4 | Core convergent/divergent validity |
| 2. Age × VR Scaffolding | 4 | Age effects and mediation |
| 3. Metacognition Predictors | 5 | Confidence, calibration, HCE |
| 4. Process-Specific | 3 | RAVLT-Free Recall, BVMT-Where |
| 5. Self-Report & Contextual | 4 | Sleep, DASS, strategies |
| 6. Individual Differences in Forgetting | 4 | Slope predictors |
| 7. Clinical Utility | 4 | Reverse inference, discrepancy |
| 8. Latent Profiles & Models | 4 | Profiles, cross-validation |

### Priority Tiers

**Tier 1 - Core Thesis (12 RQs, ~12h):**
- 7.1.1-7.1.4 (Predictive Validity)
- 7.2.1-7.2.4 (Age × VR Scaffolding)
- 7.7.1-7.7.4 (Clinical Utility)

**Tier 2 - Metacognition (5 RQs, ~6h):**
- 7.3.1-7.3.5

**Tier 3 - Slopes & Processes (7 RQs, ~8h):**
- 7.4.1-7.4.3
- 7.6.1-7.6.4

**Tier 4 - Profiles & Self-Report (8 RQs, ~8h):**
- 7.5.1-7.5.4
- 7.8.1-7.8.4

### Data Sources Summary

| Data Type | Source | Tags/Files |
|-----------|--------|------------|
| REMEMVR Theta | Ch5 results | step03_theta_scores.csv |
| Domain Theta | Ch5 5.2.x | Theta_What/Where/When |
| Confidence Theta | Ch6 6.1.x | Confidence theta scores |
| HCE Rate | Ch6 6.6.x | HCE proportions |
| Calibration | Ch6 6.2.x | Resolution/Brier |
| LMM Slopes | Ch5 5.1.1-4 | Random effects |
| Cognitive Tests | master.xlsx | COG-X-RAV/BVM/NAR/RPM |
| Demographics | master.xlsx | DEM-X-* tags |
| DASS | master.xlsx | DEM-X-DASS_* |
| Per-Test Sleep | master.xlsx | RVR-T{N}-SLP-X-* |

---

**END OF CH7 SPECIFICATIONS**
