# RQ 6.2.4: Calibration by Accuracy Level

**Chapter:** 6
**Type:** Calibration
**Subtype:** By Accuracy Level
**Full ID:** 6.2.4

---

## Research Question

**Primary Question:**
Are high vs low performers equally well-calibrated?

**Scope:**
This RQ examines the relationship between baseline memory performance and calibration quality. Sample: N=100 participants. Metrics: calibration (difference between confidence and accuracy), gamma (discrimination/resolution), and baseline accuracy levels. Participants grouped into accuracy tertiles (Low/Med/High baseline performers) to test if calibration quality differs by performance level.

**Theoretical Framing:**
Metacognitive accuracy (calibration) may be linked to memory ability. High performers may have better metacognitive monitoring (more accurate confidence judgments), while low performers may exhibit overconfidence patterns (Dunning-Kruger effect). This RQ tests whether metacognitive skill correlates with memory skill or operates independently.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory**: Proposes that individuals track their own memory performance through monitoring processes. High-quality monitoring leads to accurate confidence judgments (good calibration), while poor monitoring leads to miscalibration.
- **Dunning-Kruger Effect**: Low-skill individuals may lack the metacognitive ability to accurately assess their performance, leading to overconfidence. High-skill individuals may be more accurate in self-assessment.
- **Cue-Utilization Framework**: Calibration depends on the quality of cues used for metacognitive judgments. High performers may use more diagnostic cues, leading to better calibration.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Two competing predictions:
1. **Metacognitive Skill Hypothesis**: High baseline performers show better calibration (smaller |calibration| scores, higher gamma values) because metacognitive monitoring ability correlates with memory ability.
2. **Dunning-Kruger Hypothesis**: Low baseline performers show overconfidence (positive calibration: confidence exceeds accuracy) due to poor metacognitive insight, while high performers are more accurately calibrated.

**Literature Gaps:**
Few studies examine calibration across different baseline performance levels in episodic memory paradigms using continuous measures of both accuracy (IRT theta) and confidence (ordinal confidence ratings). Most calibration research uses dichotomous correct/incorrect coding, which may obscure individual differences.

---

## Hypothesis

**Primary Hypothesis:**
High baseline performers will be BETTER calibrated than low performers, showing smaller absolute calibration errors (|calibration|) and higher discrimination (gamma). This reflects a positive correlation between memory skill and metacognitive skill.

**Secondary Hypotheses:**
1. Low performers will exhibit overconfidence (Dunning-Kruger pattern): positive calibration scores (confidence exceeds accuracy).
2. High performers may show slight underconfidence or accurate calibration (calibration near zero).
3. Baseline accuracy will correlate negatively with |calibration| (higher accuracy -> better calibration).
4. Baseline accuracy will correlate positively with gamma (higher accuracy -> better discrimination).

**Theoretical Rationale:**
If metacognitive monitoring and memory encoding share common cognitive resources or processes (e.g., attention, executive function), individuals with strong memory performance should also demonstrate accurate metacognitive judgments. The Dunning-Kruger effect suggests that low performers lack the metacognitive insight to recognize their poor performance, leading to inflated confidence. High performers possess both strong memory traces and accurate self-assessment capabilities.

**Expected Effect Pattern:**
- **Tertile Comparison**: Significant effect of baseline accuracy tertile on calibration metrics (F-test or Kruskal-Wallis, p < 0.05).
- **Dunning-Kruger Test**: Low tertile shows positive mean calibration (overconfidence), significantly different from zero (t-test, p < 0.05).
- **Correlation**: Negative correlation between baseline accuracy and |calibration| (r < -0.30, p < 0.05). Positive correlation between baseline accuracy and gamma (r > 0.30, p < 0.05).

---

## Memory Domains

**Domains Examined:**

This RQ uses omnibus "All" factor theta scores (aggregated across What/Where/When domains) from prior RQs:
- Baseline accuracy theta from Ch5 5.1.1 (omnibus accuracy across all domains)
- Confidence theta from RQ 6.1.1 (omnibus confidence across all domains)
- Calibration from RQ 6.2.1 (confidence - accuracy difference)
- Gamma (resolution) from RQ 6.2.3 (item-level discrimination)

**Domain Aggregation Rationale:**
This RQ examines overall metacognitive-memory relationships using omnibus scores. Domain-specific calibration patterns are addressed in separate RQs (6.3.2 for What/Where/When domains, 6.4.2 for paradigms, 6.5.2 for schema congruence).

---

## Analysis Approach

**Analysis Type:**
Correlation and group comparison (tertile analysis) examining relationships between baseline performance and calibration quality.

**High-Level Workflow:**

**Step 0:** Load calibration scores from RQ 6.2.1, gamma scores from RQ 6.2.3, baseline accuracy (Ch5 5.1.1 Day 0 theta), baseline confidence (RQ 6.1.1 Day 0 theta). Merge into single dataset with N=100 participants.

**Step 1:** Create accuracy tertiles by splitting participants into three equal groups based on baseline accuracy (Day 0 theta from Ch5 5.1.1): Low, Medium, High performers (approximately 33 participants per tertile).

**Step 2:** Compute mean absolute calibration (|calibration|) and mean gamma by tertile. Compare tertiles using ANOVA or Kruskal-Wallis test to assess whether calibration quality differs by baseline performance level.

**Step 3:** Test tertile effects on calibration metrics: calibration metrics ~ Baseline_tertile. Report F-statistics and p-values for each metric.

**Step 4:** Test Dunning-Kruger pattern: For low performers tertile, test if mean calibration > 0 (overconfidence) using one-sample t-test against zero. For high performers tertile, test if calibration is near zero or negative (accurate/underconfident).

**Step 5:** Compute correlations: (1) baseline accuracy vs absolute calibration, (2) baseline accuracy vs gamma. Test if baseline performance predicts calibration quality continuously (not just tertile differences).

**Expected Outputs:**
- data/step01_merged_metrics.csv (100 rows): UID, baseline_accuracy, baseline_confidence, mean_calibration, mean_gamma
- data/step02_accuracy_tertiles.csv (100 rows): UID, baseline_accuracy, tertile_label (Low/Med/High)
- results/step03_tertile_comparison.csv: Mean calibration and gamma by tertile, ANOVA/Kruskal-Wallis results
- results/step04_dunning_kruger_test.csv: One-sample t-tests for each tertile (test against zero calibration)
- results/step05_correlation.csv: Pearson/Spearman correlations with p-values and confidence intervals
- plots/step06_calibration_by_accuracy.csv: Plot data showing calibration metrics vs baseline accuracy (scatterplot + tertile boxplots)

**Success Criteria:**
- Tertiles created with approximately equal N (30-35 participants per group).
- Calibration metrics (|calibration|, gamma) computed for all 100 participants.
- Tertile comparison completed (ANOVA or non-parametric equivalent).
- Dunning-Kruger hypothesis tested for low performers tertile (one-sample t-test).
- Correlations computed with significance tests and effect sizes reported.
- Results interpretable: Can answer whether high performers are better calibrated and whether Dunning-Kruger pattern exists.

---

## Data Source

**Data Type:**
DERIVED (from multiple prior RQs across Ch5 and Ch6)

### DERIVED Data Source:

**Source RQs:**
1. **RQ 6.2.1** (Calibration Over Time): calibration scores (confidence - accuracy difference)
2. **RQ 6.2.3** (Resolution Over Time): gamma scores (item-level discrimination)
3. **RQ 6.1.1** (Confidence Model Selection): theta_confidence Day 0 (baseline confidence)
4. **Ch5 5.1.1** (Accuracy Functional Form): theta_accuracy Day 0 (baseline accuracy)

**File Paths:**
- results/ch6/6.2.1/data/step02_calibration_scores.csv (400 observations) - filter to Day 0 or compute mean across timepoints
- results/ch6/6.2.3/data/step01_gamma_scores.csv (400 observations) - filter to Day 0 or compute mean
- results/ch6/6.1.1/data/step03_theta_confidence.csv (400 observations) - filter to TEST = T1 (Day 0)
- results/ch5/5.1.1/data/step03_theta_scores.csv (400 observations) - filter to TEST = T1 (Day 0)

**Dependencies:**
This RQ requires successful completion of:
- RQ 6.2.1 (calibration scores available)
- RQ 6.2.3 (gamma scores available)
- RQ 6.1.1 (confidence theta scores available)
- Ch5 5.1.1 (accuracy theta scores available)

All source RQs must have completed their analysis workflows before this RQ can execute.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from source RQs)
- Baseline metrics computed from Day 0 (T1) only
- Tertile grouping creates approximately 33-34 participants per tertile

**Items:**
- N/A (analysis uses participant-level theta scores, not item-level data)

**Tests:**
- [x] Day 0 (T1) baseline only for primary analysis
- Alternative: Mean calibration and gamma across all 4 timepoints (optional sensitivity analysis)

**Metrics:**
- Calibration: theta_confidence - theta_accuracy (both z-standardized)
- Gamma: Goodman-Kruskal gamma (item-level confidence-accuracy discrimination)
- Baseline accuracy: theta_accuracy at Day 0 from Ch5 5.1.1
- Baseline confidence: theta_confidence at Day 0 from RQ 6.1.1

---
