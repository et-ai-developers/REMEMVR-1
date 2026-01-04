# RQ 7.3.5: Does confidence-accuracy gap predict cognitive reserve?

**Chapter:** 7
**Type:** Metacognition Predictors
**Subtype:** Confidence-accuracy gap and cognitive reserve
**Full ID:** 7.3.5

---

## Research Question

**Primary Question:**
Do individuals with high confidence AND high accuracy (well-calibrated high performers) show signs of cognitive reserve?

**Scope:**
This RQ examines 100 participants across calibration groups (well-calibrated vs overconfident vs underconfident) created from confidence-accuracy residuals. Compares groups on education, RPM scores, and age as indicators of cognitive reserve. Uses theta scores from Ch5 overall episodic memory and confidence ratings from Ch6.

**Theoretical Framing:**
Tests whether metacognitive awareness (knowing what you know) may serve as an indicator of cognitive reserve. Individuals who maintain accurate self-assessment of their abilities may have developed compensatory strategies that protect against cognitive decline.

---

## Theoretical Background

**Relevant Theories:**
- **Cognitive Reserve Theory** (Stern, 2002): Some individuals maintain cognitive function despite aging or pathology through efficient neural networks, cognitive flexibility, and compensatory strategies. Higher education and fluid intelligence are classic reserve indicators.
- **Metacognitive Theory**: Metacognitive monitoring (awareness of one's cognitive processes) requires executive control and may reflect intact frontal-subcortical circuits. Good calibration between confidence and accuracy suggests preserved metacognitive function.
- **Dual-Process Theory**: Metacognitive judgments rely on both Type 1 (automatic, experiential) and Type 2 (controlled, analytical) processes. Well-calibrated individuals may have better integration between these systems.

**Key Citations:**

**Theoretical Predictions:**
Cognitive reserve theory predicts that individuals with higher education and fluid intelligence should show better metacognitive monitoring. Well-calibrated high performers may represent individuals with robust cognitive reserve who maintain both memory performance and accurate self-assessment.

**Literature Gaps:**
Limited research has examined whether metacognitive calibration itself serves as a cognitive reserve indicator, independent of raw performance levels.

---

## Hypothesis

**Primary Hypothesis:**
Well-calibrated individuals (high confidence matched with high accuracy) will show higher education and RPM scores compared to overconfident or underconfident groups, suggesting metacognitive awareness as a cognitive reserve indicator.

**Secondary Hypotheses:**
1. Well-calibrated group will show higher education levels than other groups
2. Well-calibrated group will show higher RPM scores (fluid intelligence) than other groups
3. Age may not differ between groups, suggesting reserve effects beyond normal aging

**Theoretical Rationale:**
Cognitive reserve develops through educational experiences and is reflected in fluid intelligence. Individuals with higher reserve should maintain both memory performance AND accurate self-assessment. Poor calibration (over/underconfidence) may reflect compromised metacognitive monitoring despite preserved raw performance.

**Expected Effect Pattern:**
Significant group differences on education (F > 3.0, p < 0.05) and RPM (F > 4.0, p < 0.01), with well-calibrated group scoring highest. Moderate correlations between calibration quality and reserve indicators (r = 0.25-0.40).

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
Uses omnibus theta_all scores from Ch5 5.1.1 that aggregate across all episodic memory domains to create overall accuracy measure for calibration analysis.

**Exclusion Rationale:**
No domain-specific exclusions. Analysis focuses on overall episodic memory performance rather than domain-specific patterns.

---

## Analysis Approach

**Power Analysis:**
- Sample size: N=100 with k predictors
- Post-hoc power for medium effects (f²=0.15): Approximately 80%
- Minimum detectable effect: f²=0.10 with current sample
- Limitation acknowledged: Underpowered for small effects (f²<0.10)


**Analysis Type:**
ANOVA and correlation analysis with calibration groups and cognitive reserve indicators

**High-Level Workflow:**

**Step 1:** Extract and prepare data
- Load theta_all scores from Ch5 5.1.1 results
- Load confidence_theta scores from Ch6 results
- Extract education, RPM, age from dfnonvr.csv
- Check data quality and compute missingness

**Step 2:** Create calibration groups
- Compute confidence-accuracy correlation residuals
- Define groups: Overconfident (residual > 0.5 SD), Underconfident (residual < -0.5 SD), Well-calibrated (middle)
- Validate group sizes and distributions

**Step 3:** Compare groups on reserve indicators
- One-way ANOVA: Education by calibration group
- One-way ANOVA: RPM by calibration group
- One-way ANOVA: Age by calibration group
- Report effect sizes (eta-squared) with 95% CIs
- Report BOTH uncorrected AND corrected p-values (Decision D068)

**Step 4:** Correlational analysis
- Correlate calibration quality with education
- Correlate calibration quality with RPM
- Correlate calibration quality with age
- Bootstrap CIs (1000 iterations) for correlations

**Step 5:** Effect sizes and interpretation
- Compute Cohen's d for pairwise group comparisons
- Effect size classification (small/medium/large)
- Clinical significance assessment

**Step 6:** Sensitivity analyses
- Exclude potential outliers, rerun analyses
- Try alternative calibration grouping (tertiles vs SD cutoffs)
- Test robustness of findings

**Expected Outputs:**
- data/step01_accuracy_confidence.csv (merged theta and confidence data)
- data/step02_cognitive_reserve.csv (education, RPM, age scores)
- data/step03_analysis_input.csv (final merged dataset)
- data/step04_calibration_groups.csv (group assignments and descriptives)
- data/step05_anova_results.csv (group comparisons with dual p-values)
- data/step06_correlations.csv (calibration-reserve correlations)
- data/step07_effect_sizes.csv (Cohen's d for group differences)
- results/calibration_reserve_summary.md (text summary for thesis)
- plots/calibration_groups.png (group comparison visualization)

**

**Cross-Validation:**
- Implement 5-fold CV (seed=42) for generalization assessment
- Report mean CV-R² and SD across folds
- CV-R² to full-sample R² gap should be <0.10
- If gap >0.10: Consider regularization


**Success Criteria:**
- Create meaningful calibration groups with reasonable n per group (n > 20)
- Test group differences on reserve indicators
- Report if well-calibrated group differs from others on education/RPM
- Effect sizes in small-medium range (d = 0.3-0.8) for meaningful differences
- Bonferroni-corrected significance at ± = 0.00179/3 = 0.0006 level
- Bootstrap CIs for correlations do not include zero for significant effects

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.1.1 outputs + Ch6 confidence outputs + master.xlsx cognitive reserve indicators)

### DERIVED Data Sources:

**Source RQs:**
- Ch5 5.1.1 (General episodic memory theta scores)
- Ch6 confidence analysis results (theta-scaled confidence ratings)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (overall episodic memory theta)
- results/ch6/[confidence_rq]/data/confidence_theta_scores.csv (confidence ratings)
- data/cache/master.xlsx (cognitive test scores and demographics)

**Dependencies:**
- Ch5 5.1.1 must complete IRT calibration and theta estimation
- Ch6 confidence analysis must complete confidence-theta calibration
- master.xlsx cognitive and demographic data must be available

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions planned)
- [x] Require valid theta_all and confidence_theta scores
- [x] Require valid education, RPM, and age data

**Items:**
- N/A (theta scores already aggregated from item responses)

**Tests:**
- [x] Uses aggregated scores across all 4 tests (T1-T4) for overall ability estimation

---