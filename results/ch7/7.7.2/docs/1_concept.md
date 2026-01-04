# RQ 7.7.2: Discrepancy Analysis - Who diverges?

**Chapter:** 7
**Type:** Clinical Utility
**Subtype:** Discrepancy Analysis
**Full ID:** 7.7.2

---

## Research Question

**Primary Question:**
Who shows RAVLT-REMEMVR divergence (high on one, low on other)? What characterizes these individuals?

**Scope:**
This RQ examines discrepancy patterns between traditional neuropsychological assessment (RAVLT) and ecological memory assessment (REMEMVR) across 100 participants. Creates discrepancy scores (REMEMVR_z - RAVLT_z) to identify divergent cases and characterizes them demographically. Focus on clinical interpretation when traditional tests and ecological tests disagree.

**Theoretical Framing:**
Clinical utility analysis examining when traditional tests and ecological tests provide discordant information. Understanding who diverges helps interpretation - e.g., older adults with high REMEMVR but low RAVLT may benefit from VR scaffolding, while younger adults with high RAVLT but low REMEMVR may struggle with ecological memory demands.

---

## Theoretical Background

**Relevant Theories:**
- **Ecological Validity Theory:** Traditional neuropsychological tests may not capture real-world memory function, particularly in older adults who can compensate using environmental cues
- **VR Scaffolding Theory:** Virtual reality provides contextual and spatial cues that may benefit older adults more than younger adults, leading to age-specific divergence patterns
- **Clinical Interpretation Framework:** When two memory measures disagree, demographic and cognitive characteristics can guide interpretation of which is more representative of functional capacity

**Key Citations:**

**Theoretical Predictions:**
Divergent individuals should differ systematically on demographic variables. VR-favored cases (better REMEMVR than RAVLT) predicted to be older adults who benefit from environmental scaffolding. RAVLT-favored cases may be younger adults with strong verbal memory but difficulty with spatial-contextual integration.

**Literature Gaps:**
Limited research on systematic discrepancies between traditional and ecological memory assessments, and demographic predictors of such discrepancies.

---

## Hypothesis

**Primary Hypothesis:**
VR-favored individuals (REMEMVR > RAVLT) will be significantly older than RAVLT-favored individuals (RAVLT > REMEMVR), reflecting age-related benefits from environmental scaffolding in VR assessment.

**Secondary Hypotheses:**
- VR experience may predict VR-favored discrepancy pattern
- Education level may predict RAVLT-favored pattern (verbal advantage)
- Discrepancy groups will differ on other cognitive test performance

**Theoretical Rationale:**
Older adults may show intact ecological memory despite poor performance on decontextualized traditional tests. VR provides environmental context and spatial cues that older adults can leverage effectively. Younger adults may excel on verbal list learning but struggle with complex spatial-temporal integration required in VR.

**Expected Effect Pattern:**
Main effect of age predicting discrepancy direction, with VR-favored group being significantly older (F > 4.0, p < 0.05). Effect size expected to be medium (Cohen's d H 0.5-0.8) based on age-related differences in memory strategy use.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Included in omnibus REMEMVR theta scores used for discrepancy analysis

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Description: Included in omnibus REMEMVR theta scores used for discrepancy analysis

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Included in omnibus REMEMVR theta scores used for discrepancy analysis

**Inclusion Rationale:**
Uses omnibus theta_all scores from Ch5 to provide single REMEMVR performance metric comparable to RAVLT Total score. Aggregating across all episodic memory domains provides most valid comparison to omnibus RAVLT measure.

**Exclusion Rationale:**
Domain-specific analyses not appropriate for this RQ - requires single overall performance metric for meaningful discrepancy calculation with RAVLT Total.

---

## Analysis Approach

**Analysis Type:**
Discrepancy analysis with one-way ANOVA and post-hoc comparisons, plus descriptive characterization of divergent groups

**High-Level Workflow:**

**Step 1:** Extract and standardize scores
- Load theta_all scores from Ch5 omnibus analysis
- Extract RAVLT Total scores from dfnonvr.csv
- Standardize both measures to z-scores (M=0, SD=1)

**Step 2:** Compute discrepancy scores
- Calculate REMEMVR_z - RAVLT_z for each participant
- Positive values = better REMEMVR than RAVLT (VR-favored)
- Negative values = better RAVLT than REMEMVR (RAVLT-favored)

**Step 3:** Create discrepancy groups
- VR-favored: Discrepancy > +1 SD (expected n H 16)
- RAVLT-favored: Discrepancy < -1 SD (expected n H 16)
- Concordant: |Discrepancy| d 1 SD (expected n H 68)

**Step 4:** Extract demographic predictors
- Age, Education, VR_Experience from dfnonvr.csv
- Additional cognitive tests for validation

**Step 5:** Compare groups on characteristics
- One-way ANOVA for each predictor across 3 groups
- Post-hoc Tukey HSD for pairwise comparisons
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Primary correction: Bonferroni (± = 0.00179/4 = 0.000448)

**Step 6:** Effect sizes and clinical interpretation
- Cohen's d for pairwise group differences
- Eta-squared for ANOVA effect sizes
- Clinical significance thresholds and interpretation

**Step 7:** Model diagnostics
- Check ANOVA assumptions: normality (Shapiro-Wilk), homogeneity (Levene's test)
- Identify outliers using Cook's D and standardized residuals
- Report sample sizes per group and power analysis
- Power analysis: For one-way ANOVA with 3 groups, n≥16 per group provides 80% power to detect medium effects (f=0.25) at α=0.05. With N=100 and expected group distribution (33/33/34), power exceeds 0.95 for medium effects

**Expected Outputs:**
- data/step01_theta_ravlt_scores.csv (standardized scores)
- data/step02_discrepancy_scores.csv (discrepancy calculations)
- data/step03_group_assignments.csv (VR-favored, RAVLT-favored, Concordant)
- data/step04_demographic_data.csv (age, education, VR experience)
- data/step05_group_comparisons.csv (ANOVA results with dual p-values)
- data/step06_effect_sizes.csv (Cohen's d, eta-squared with 95% CIs)
- data/step07_clinical_profiles.csv (group characterization data)
- results/discrepancy_analysis_summary.md (text summary for thesis)
- plots/discrepancy_distribution.png (histogram of discrepancy scores)
- plots/group_comparisons.png (box plots of demographic variables by group)

**

**Cross-Validation:**
- Implement 5-fold CV (seed=42) for generalization assessment
- Report mean CV-R² and SD across folds
- CV-R² to full-sample R² gap should be <0.10
- If gap >0.10: Consider regularization


**Success Criteria:**
- [ ] Create meaningful discrepancy groups with adequate n per group (n e 10)
- [ ] Identify significant group differences on at least one demographic variable
- [ ] Effect size medium or larger (d e 0.5) for primary age difference
- [ ] Meet ANOVA assumptions or apply appropriate corrections
- [ ] Both uncorrected and corrected p-values reported (Decision D068)
- [ ] Clinical interpretation provides actionable insights for test interpretation
- [ ] Sample size adequate for detecting medium effects (power e 0.80)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 omnibus analysis + master.xlsx cognitive tests)

### DERIVED Data Sources:

**Source RQ:**
Ch5 omnibus analysis (likely 5.1.1 for theta_all scores)

**File Paths:**
- results/ch5/5.1.1/data/step03_theta_scores.csv (theta_all scores per participant)
- data/cache/master.xlsx (RAVLT Total scores and demographics)

**Dependencies:**
Ch5 5.1.1 must complete IRT calibration and theta estimation before this RQ can run

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from Ch5 analysis)
- [ ] Exclude participants with missing RAVLT or theta scores

**Items:**
- N/A (uses aggregated theta scores from Ch5)

**Tests:**
- [x] REMEMVR: Mean theta across all 4 test sessions (T1-T4)
- [x] RAVLT: Total score (T1+T2+T3+T4+T5) from dfnonvr.csv

**Variables Required:**
- REMEMVR: theta_all (omnibus factor from Ch5)
- RAVLT: RAVLT_Total from dfnonvr.csv
- Demographics: Age, Education, VR_Experience
- Validation: NART, BVMT for characterization

---