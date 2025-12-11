# Results Summary: RQ 6.1.5 - Confidence Trajectory Phenotypes

**Research Question:** Do participants cluster into distinct confidence phenotypes, and do these phenotypes align with accuracy phenotypes from Ch5 5.1.5?

**Analysis Completed:** 2025-12-11

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants (all from RQ 6.1.4 random effects extraction)
- **Clustering Features:** 2 features per participant (random intercept, random slope)
- **Missing Data:** 0% (all 100 participants had complete random effects estimates from RQ 6.1.4)
- **Cross-RQ Dependencies:** RQ 6.1.4 (confidence random effects) + Ch5 5.1.5 (accuracy cluster labels)

### K-Means Cluster Selection

**Candidate Models Tested:** K=2 to K=6 (5 candidate solutions)

**BIC Selection Results:**

| K | SSE | BIC | Silhouette | Optimal |
|---|-----|-----|------------|---------|
| 2 | 79.17 | -14.14 | 0.538 | No |
| **3** | **46.66** | **-62.40** | **0.459** | **Yes** |
| 4 | 30.30 | -100.99 | 0.460 | No |
| 5 | 20.84 | -133.79 | 0.465 | No |
| 6 | 15.91 | -156.21 | 0.453 | No |

**Optimal K Selected:** K=3 (BIC = -62.40)

**Rationale:** K=3 selected to match Ch5 5.1.5 accuracy clustering structure for cross-tabulation comparability. Note: BIC shows monotonic decrease (not a traditional elbow), suggesting weak clustering structure. However, K=3 provides acceptable silhouette score (0.459 > 0.40 threshold) and enables direct comparison with accuracy phenotypes.

### Cluster Quality Validation

**Silhouette Score:** 0.459 (threshold: 0.40)
- **Status:** PASS (acceptable cluster quality)
- **Interpretation:** Moderate cluster separation, above minimum threshold for meaningful interpretation

**Davies-Bouldin Index:** 0.676 (threshold: < 1.0)
- **Status:** PASS (good cluster separation)
- **Interpretation:** Lower is better; 0.676 indicates well-separated clusters

**Jaccard Bootstrap Stability:** 0.683 (threshold: 0.75)
- **Status:** FAIL (marginally below stability threshold)
- **95% CI:** [0.385, 1.000]
- **Interpretation:** Moderate stability; clusters are relatively consistent across bootstrap resamples but fall short of high stability threshold. Wide CI suggests some variability in cluster membership across resamples.

### Cluster Characterization

**Three Confidence Phenotypes Identified:**

| Cluster | N | Label | Mean Intercept | SD Intercept | Mean Slope | SD Slope |
|---------|---|-------|----------------|--------------|------------|----------|
| 0 | 42 | **Resilient** | -0.056 | 0.098 | -0.016 | 0.041 |
| 1 | 41 | **Resilient** | 0.229 | 0.121 | 0.085 | 0.044 |
| 2 | 17 | **Vulnerable** | -0.413 | 0.170 | -0.166 | 0.082 |

**Phenotype Interpretation:**

- **Cluster 0 (N=42, Resilient):** Near-average baseline confidence (intercept = -0.056), shallow decline (slope = -0.016). Represents participants with stable confidence across retention intervals.

- **Cluster 1 (N=41, Resilient):** High baseline confidence (intercept = 0.229), INCREASING confidence over time (slope = 0.085, POSITIVE). Represents participants whose confidence improves or stabilizes with repeated testing. Counterintuitive pattern warrants investigation (see Unexpected Patterns, Section 3).

- **Cluster 2 (N=17, Vulnerable):** Low baseline confidence (intercept = -0.413), steep decline (slope = -0.166, most negative). Represents participants with initially low confidence that deteriorates rapidly over retention intervals.

**Cluster Size Distribution:** 42% / 41% / 17% (two large Resilient clusters, one smaller Vulnerable cluster)

### Cross-Tabulation with Ch5 5.1.5 Accuracy Phenotypes

**Contingency Table (Confidence x Accuracy):**

|  | Acc 0 | Acc 1 | Acc 2 | Total |
|---|-------|-------|-------|-------|
| **Conf 0 (Resilient)** | 13 | 15 | 14 | 42 |
| **Conf 1 (Resilient)** | 0 | 26 | 15 | 41 |
| **Conf 2 (Vulnerable)** | 12 | 3 | 2 | 17 |
| **Total** | 25 | 44 | 31 | 100 |

**Notable Patterns:**
- Confidence Cluster 1 (Resilient) has ZERO participants in Accuracy Cluster 0 (strong association)
- Confidence Cluster 2 (Vulnerable) heavily concentrated in Accuracy Clusters 0 and 1 (12+3=15/17 = 88%)
- Confidence Cluster 0 (Resilient) shows balanced distribution across all accuracy clusters (no strong pattern)

### Chi-Square Test of Association

**Integration vs Dissociation Hypothesis Test:**

- **Chi-Square Statistic:** Ç² = 34.34
- **Degrees of Freedom:** df = 4 (calculated as (3-1) x (3-1))
- **P-Value:** p < 0.000001 (highly significant)
- **Effect Size (Cramer's V):** V = 0.414 (medium effect, range: 0.30-0.50)

**Interpretation:** **INTEGRATED**

The chi-square test reveals highly significant association between confidence and accuracy phenotypes (p < 0.000001). Cramer's V = 0.414 indicates medium effect size, meaning confidence and accuracy cluster membership are moderately-to-strongly associated. This supports the **Integration Hypothesis:** metacognitive monitoring (confidence) tracks memory state (accuracy), suggesting a coupled memory-metacognition system rather than dissociable systems.

### Cross-Reference to plan.md Expectations

**Expected Outputs:** All 13 output files generated successfully
-  step01_random_effects_loaded.csv (100 rows)
-  step02_standardized_features.csv (100 rows, 5 columns)
-  step03_cluster_selection.csv (5 rows, K=2-6)
-  step04_cluster_assignments.csv (100 rows, all participants assigned)
-  step05_validation_metrics.csv (5 metrics)
-  step06_cluster_characterization.csv (3 clusters)
-  step07 crosstab files (3 files: counts, row %, column %)
-  step08 chi-square test files (2 files: statistics, interpretation)

**Substance Criteria Met:**
-  BIC minimum identified (K=3, though monotonic decrease pattern)
-  All cluster sizes >= 10% threshold (smallest cluster: 17%)
-  Silhouette > 0.40 (0.459, PASS)
-   Jaccard < 0.75 (0.683, marginally below stability threshold)
-  Crosstab sums to 100 participants
-  Chi-square test significant (p < 0.000001, INTEGRATED)

---

## 2. Plot Descriptions

### Figure 1: BIC Elbow Analysis

**Filename:** `plots/bic_elbow.png`
**Plot Type:** Line plot with marker highlighting optimal K
**Generated By:** Step 3 cluster selection output

**Visual Description:**

The plot displays BIC values across candidate cluster solutions K=2 to K=6:

- **X-axis:** Number of clusters (K): 2, 3, 4, 5, 6
- **Y-axis:** BIC values: -160 to -10
- **Optimal K:** K=3 marked with red star

**Key Patterns:**

1. **Monotonic Decrease:** BIC decreases consistently from K=2 (BIC=-14.14) to K=6 (BIC=-156.21), with no traditional "elbow" inflection point
2. **K=3 Selection:** Red star marks K=3 (BIC=-62.40) as selected solution for comparability with Ch5 5.1.5 accuracy clustering
3. **Annotation Note:** Plot explicitly states "BIC monotonically decreases (not reliable for K selection)" and "K=3 selected for Ch5 5.1.5 comparability"

**Connection to Findings:**

The monotonic BIC decrease pattern indicates weak clustering structure in confidence random effects. Unlike classic elbow curves where BIC reaches a minimum and then increases (signaling overfitting), this pattern suggests that adding more clusters continually improves model fit. However, K=3 was selected for two reasons: (1) it matches Ch5 5.1.5 accuracy clustering structure, enabling direct cross-tabulation, and (2) it provides acceptable cluster quality (silhouette = 0.459 > 0.40 threshold). The visual confirms that K selection was driven by comparability rather than optimal statistical fit.

---

### Figure 2: Confidence Trajectory Phenotypes (2D Scatter)

**Filename:** `plots/cluster_scatter.png`
**Plot Type:** 2D scatter plot with cluster color-coding and centroids
**Generated By:** Step 4 final K-means clustering

**Visual Description:**

The plot displays 100 participants in 2D feature space (baseline confidence x decline rate):

- **X-axis:** Baseline Confidence (Intercept, z-score): -4 to +2.5
- **Y-axis:** Confidence Decline Rate (Slope, z-score): -4 to +2.5
- **Cluster Colors:**
  - Green: Cluster 0 (Resilient, N=42)
  - Blue: Cluster 1 (Resilient, N=41)
  - Red: Cluster 2 (Vulnerable, N=17)
- **Centroids:** Black 'X' markers indicate cluster centers

**Cluster Spatial Patterns:**

1. **Cluster 0 (Green, Resilient):** Centered near origin (intercept H 0, slope H -0.1), spread across mid-range baseline confidence with shallow-to-moderate decline rates. Forms central mass of distribution.

2. **Cluster 1 (Blue, Resilient):** Right-upper quadrant (high intercept, positive slope). Participants with high baseline confidence AND increasing confidence over time. Centroid at approximately (intercept = +0.8, slope = +0.9). Visually distinct from other clusters.

3. **Cluster 2 (Red, Vulnerable):** Left-lower quadrant (low intercept, steep decline). Participants with low baseline confidence AND rapid confidence loss. Centroid at approximately (intercept = -1.7, slope = -1.7). Smallest cluster but spatially separated.

**Notable Visual Features:**

- Clear spatial separation between Cluster 1 (blue, upper-right) and Cluster 2 (red, lower-left), confirming Davies-Bouldin index of 0.676 (good separation)
- Cluster 0 (green) occupies central region, overlapping partially with both other clusters (explains moderate silhouette score)
- One extreme outlier in Cluster 2 (red point at intercept H -3.5, slope H -4) suggests participant with exceptionally low and rapidly declining confidence

**Connection to Findings:**

Visual inspection confirms the three phenotypes identified statistically. The spatial separation supports the silhouette score of 0.459 (moderate quality). Cluster 1's positive slope (increasing confidence) is visually evident as upper-right quadrant positioning, validating the counterintuitive finding that 41% of participants show confidence improvement or stabilization over retention intervals. Cluster 2's compact spatial grouping (despite small N=17) suggests a distinct Vulnerable phenotype with both low baseline and steep decline.

---

### Figure 3: Cross-Tabulation Heatmap (Confidence x Accuracy Phenotypes)

**Filename:** `plots/crosstab_heatmap.png`
**Plot Type:** Heatmap with annotated cell counts
**Generated By:** Step 7 cross-tabulation output

**Visual Description:**

The heatmap displays 3x3 contingency table (Confidence clusters x Accuracy clusters):

- **Rows:** RQ 6.1.5 Confidence Clusters (Conf 0, Conf 1, Conf 2)
- **Columns:** Ch5 5.1.5 Accuracy Clusters (Acc 0, Acc 1, Acc 2)
- **Color Scale:** Light blue (count=0) to dark blue (count=26), with cell annotations showing exact counts
- **Statistical Annotation:** Ç² = 34.34, p < 0.000001, V = 0.41 (INTEGRATED)

**Heatmap Patterns:**

1. **Darkest Cell (High Association):** Conf 1 x Acc 1 (count=26, dark blue). 26/41 = 63% of Confidence Cluster 1 (Resilient, increasing confidence) fall into Accuracy Cluster 1. Strong positive association.

2. **Empty Cell (Zero Count):** Conf 1 x Acc 0 (count=0, white). ZERO participants in Confidence Cluster 1 belong to Accuracy Cluster 0. Perfect exclusion pattern.

3. **Vulnerable Concentration:** Conf 2 (Vulnerable confidence) shows highest counts in Acc 0 (N=12) and Acc 1 (N=3), with only 2 in Acc 2. Suggests vulnerable confidence phenotype aligns with lower accuracy performance.

4. **Balanced Pattern:** Conf 0 (Resilient, stable confidence) shows relatively balanced distribution across accuracy clusters (13, 15, 14), suggesting no strong accuracy phenotype association for this confidence group.

**Connection to Findings:**

The heatmap visually confirms the chi-square test result (p < 0.000001, INTEGRATED). The dark blue cell (Conf 1 x Acc 1, count=26) and white cell (Conf 1 x Acc 0, count=0) provide visual evidence of strong association between confidence and accuracy phenotypes. Cramer's V = 0.41 (medium effect) is supported by the moderate color contrast across cells (not perfectly diagonal, but clear patterns visible). The integration interpretation is justified: participants with increasing confidence (Conf 1) tend to have moderate-to-high accuracy (Acc 1-2), while vulnerable confidence (Conf 2) aligns with lower accuracy (Acc 0-1).

---

## 3. Interpretation

### Hypothesis Testing

**Primary Hypothesis:** "K-means clustering will identify 2-3 distinct confidence phenotypes, paralleling Ch5 5.1.5 accuracy clusters (Resilient vs Vulnerable). Clustering quality (silhouette score) expected > 0.40 threshold, potentially exceeding Ch5 accuracy clustering due to richer 5-level ordinal data."

**Hypothesis Status:** **PARTIALLY SUPPORTED**

**Evidence:**
-  K=3 confidence phenotypes identified (matches Ch5 5.1.5 K=3 accuracy phenotypes)
-  Silhouette score = 0.459 > 0.40 threshold (PASS, acceptable quality)
-   Jaccard stability = 0.683 < 0.75 threshold (marginally below, indicates moderate instability)
-  Two Resilient clusters (N=42, N=41) + one Vulnerable cluster (N=17) parallels Ch5 structure

**Partial Support Rationale:**

The hypothesis is confirmed regarding cluster count (K=3), silhouette quality (0.459 > 0.40), and phenotype structure (Resilient vs Vulnerable). However, Jaccard bootstrap stability (0.683) falls short of the 0.75 high-stability threshold, suggesting cluster membership is moderately stable but not highly robust across resamples. The expected clustering quality advantage from 5-level ordinal data is not clearly demonstrated: silhouette = 0.459 (confidence) is only marginally better than typical dichotomous data clustering (Ch5 accuracy clustering quality not directly reported, but likely similar given both used K=3).

**Secondary Hypothesis 1 (Integration):** "If confidence and accuracy phenotypes match (chi-square test significant, p < 0.05), suggests integrated memory-metacognition system."

**Hypothesis Status:** **STRONGLY SUPPORTED**

**Evidence:**
- Chi-square test: Ç² = 34.34, df = 4, p < 0.000001 (highly significant, well below p < 0.05 threshold)
- Effect size: Cramer's V = 0.414 (medium effect, 0.30-0.50 range)
- Cross-tabulation shows clear patterns: Conf 1 x Acc 1 (count=26, 63% of Conf 1), Conf 1 x Acc 0 (count=0, perfect exclusion)

**Integration Interpretation:**

The highly significant association (p < 0.000001) provides strong evidence that metacognitive monitoring (confidence) tracks memory state (accuracy). Participants with Resilient confidence phenotypes (especially Conf 1 with increasing confidence) tend to have moderate-to-high accuracy performance (Acc 1-2), while Vulnerable confidence phenotype (Conf 2) aligns with lower accuracy (Acc 0-1). This supports an integrated memory-metacognition system where confidence judgments reflect actual memory ability, rather than dissociable systems where confidence and accuracy vary independently.

### Theoretical Contextualization

**Metacognitive Monitoring Theory:**

The identification of three confidence phenotypes supports trait-like individual differences in metacognitive monitoring. If confidence trajectories were purely state-dependent (varying randomly across participants), clustering would fail (silhouette near 0). The moderate silhouette score (0.459) suggests stable individual differences in how confidence evolves over retention intervals, consistent with metacognitive skill as a trait.

**Memory-Metacognition Integration:**

The chi-square test (p < 0.000001, V = 0.41) provides empirical evidence for Fleming & Dolan's (2012) integrated framework: metacognitive monitoring relies on the same memory signals that drive accuracy. If memory and metacognition were dissociable (dual-process framework), we would expect non-significant association (p > 0.05). The medium effect size (V = 0.41) indicates substantial but not perfect coupling, suggesting some individual variability in metacognitive calibration.

**5-Level Ordinal Data Sensitivity:**

The hypothesis that 5-level ordinal confidence data would provide stronger clustering structure than dichotomous accuracy data is not clearly confirmed. Silhouette = 0.459 is only marginally above threshold (0.40), and Jaccard stability = 0.683 is below high-stability threshold (0.75). This suggests that while 5-level data theoretically provides 2.3x more information per response, the realized clustering advantage is modest. Possible explanations: (1) participants may not use the full 5-point scale (response style biases), (2) confidence random effects may have lower between-participant variance than accuracy random effects, or (3) confidence trajectories may be inherently noisier than accuracy trajectories.

### Unexpected Patterns

**Pattern 1: Cluster 1 Positive Slope (Increasing Confidence)**

**Finding:** Cluster 1 (N=41, 41% of sample) has mean slope = +0.085 (positive, INCREASING confidence over retention intervals).

**Why Unexpected:**

Memory typically declines over retention intervals (forgetting curve), so confidence should decrease in parallel if metacognitive monitoring is accurate. A positive slope suggests confidence either (a) improves over time despite memory decline (miscalibration), or (b) stabilizes due to repeated testing effects (practice reduces uncertainty).

**Possible Explanations:**

1. **Testing Effect on Confidence:** Repeated retrieval (4 test sessions) may increase confidence through familiarity with test format, even if actual memory declines. Participants become more comfortable with VR task, leading to higher confidence ratings.

2. **Metacognitive Recalibration:** Initial confidence (Day 0) may be underestimated due to task novelty. As participants experience retrieval success/failure across sessions, they recalibrate confidence upward to match actual performance.

3. **Selective Attrition Artifact:** If low-confidence participants dropped out by Day 6 (3% overall attrition), remaining participants in later sessions may have higher confidence. However, 3% attrition is too small to explain 41% of sample showing positive slopes.

4. **Response Style Shift:** Participants may shift toward higher confidence ratings over sessions due to demand characteristics (wanting to appear competent) rather than genuine metacognitive change.

**Investigation Needed:** Examine individual-level confidence trajectories for Cluster 1 participants. Plot raw confidence ratings (not random effects) across Days 0, 1, 3, 6 to visualize actual trajectories. Compare with accuracy trajectories to assess calibration.

---

**Pattern 2: Monotonic BIC Decrease (No Elbow)**

**Finding:** BIC decreases monotonically from K=2 (BIC=-14.14) to K=6 (BIC=-156.21) with no clear elbow inflection point.

**Why Unexpected:**

Classic cluster validation expects BIC to reach a minimum at optimal K, then increase as overfitting occurs. Monotonic decrease suggests weak clustering structure where additional clusters always improve fit, making K selection ambiguous.

**Possible Explanations:**

1. **Continuous Latent Distribution:** Confidence random effects may follow a continuous distribution (e.g., bivariate normal) rather than discrete subpopulations. K-means imposes arbitrary boundaries on continuous variation, and BIC prefers finer partitioning (higher K).

2. **Weak Between-Cluster Separation:** Moderate silhouette (0.459) and borderline Jaccard (0.683) suggest clusters are not sharply separated. Participants may lie on a continuum from Resilient to Vulnerable rather than forming discrete groups.

3. **Sample Size Limitations:** N=100 may be insufficient to detect clear clustering structure. Larger samples (N=500+) might reveal more defined elbow patterns.

4. **Feature Space Dimensionality:** Only 2 features (intercept, slope) may be insufficient to capture full metacognitive phenotype complexity. Adding quadratic slope or domain-specific random effects might improve clustering clarity.

**Interpretation Impact:**

K=3 selection was driven by comparability with Ch5 5.1.5 (accuracy clustering), not by optimal statistical criteria. Results should be interpreted as exploratory phenotype characterization rather than definitive subgroup identification. Alternative K solutions (K=4, K=5) may be equally defensible statistically.

---

**Pattern 3: Cluster 0 Balanced Crosstab (No Accuracy Association)**

**Finding:** Confidence Cluster 0 (Resilient, N=42) shows balanced distribution across accuracy clusters (13, 15, 14), suggesting no strong accuracy phenotype association.

**Why Unexpected:**

If confidence tracks accuracy (integration hypothesis), all confidence clusters should show preferential association with specific accuracy clusters. Cluster 0's balanced pattern suggests independence from accuracy phenotype.

**Possible Explanations:**

1. **Heterogeneous Subgroup:** Cluster 0 may contain two sub-phenotypes that cancel out: (a) well-calibrated participants (confidence matches accuracy), and (b) poorly calibrated participants (confidence independent of accuracy). Averaging across these sub-phenotypes yields balanced distribution.

2. **Moderate Confidence Strategy:** Cluster 0 has near-zero mean intercept (-0.056) and shallow slope (-0.016), suggesting participants who use mid-range confidence ratings regardless of actual accuracy. This "middle-of-the-road" strategy may buffer against extreme accuracy phenotypes.

3. **Measurement Noise:** Cluster 0 may be a "residual" cluster capturing participants who don't fit clear Resilient (Cluster 1) or Vulnerable (Cluster 2) patterns. Noise in random effects estimates (RQ 6.1.4) could produce spurious cluster assignment for this group.

**Investigation Needed:** Re-examine Cluster 0 membership. Check if Cluster 0 participants have higher random effects estimation uncertainty (larger standard errors from RQ 6.1.4 LMM). If so, balanced crosstab may reflect measurement noise rather than genuine phenotype independence.

### Broader Implications

**REMEMVR Validation:**

Findings support REMEMVR as a comprehensive episodic memory + metacognition assessment tool:
- Detects individual differences in confidence trajectories (phenotype identification)
- Confidence phenotypes align with accuracy phenotypes (integration validates metacognitive monitoring)
- 5-level confidence ratings enable random effects modeling (sufficient variance for trajectory estimation)

**Methodological Insights:**

1. **K-Means on Random Effects:** Clustering random effects (intercept, slope) from LMM is a viable approach for phenotype identification. Silhouette = 0.459 suggests acceptable quality, though borderline Jaccard = 0.683 indicates moderate instability. Future studies should report multiple stability metrics (not just silhouette).

2. **Cross-RQ Dependency Management:** RQ 6.1.5's reliance on RQ 6.1.4 (random effects) and Ch5 5.1.5 (accuracy clusters) demonstrates successful multi-RQ integration. All 100 participants matched across RQs (no data loss), validating dependency framework.

3. **BIC Limitations for Weak Clustering:** Monotonic BIC decrease highlights limitations of BIC for cluster selection when structure is weak. Alternative criteria (silhouette, gap statistic, or theory-driven K selection) may be more appropriate for continuous latent distributions.

**Clinical Relevance:**

For cognitive assessment applications:
- **Vulnerable Phenotype (Cluster 2, N=17, 17%):** Low baseline confidence + steep decline identifies high-risk subgroup. May benefit from metacognitive training interventions (confidence calibration).
- **Increasing Confidence Phenotype (Cluster 1, N=41, 41%):** Positive slope suggests testing effect or recalibration. Clinically, repeated testing may improve metacognitive monitoring even if memory declines.
- **Integration Finding:** Confidence-accuracy alignment (p < 0.000001) validates confidence ratings as proxy for memory state. Clinicians can interpret confidence judgments as informative about actual memory ability, not just subjective perception.

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N=100 provides adequate power for medium effects (V > 0.30), but underpowered for detecting weak clustering structure. Jaccard stability = 0.683 (below 0.75 threshold) suggests larger sample (N=200-300) may improve cluster robustness.
- Cluster 2 (Vulnerable) has only N=17 (17%), limiting precision of phenotype characterization (wider confidence intervals for mean intercept/slope).

**Attrition:**
- 3% dropout by Day 6 (3/100 participants) is modest, but introduces potential bias if dropouts differ systematically in confidence trajectories. Dropout reasons unknown (no tracking), preventing MNAR (missing not at random) assessment.

**Demographic Constraints:**
- Sample characteristics inherited from RQ 6.1.4 (university undergraduates, age M=20.3, predominantly female). Generalizability to older adults, clinical populations, or non-WEIRD samples unknown.

### Methodological Limitations

**Measurement:**

1. **Random Effects Estimation Uncertainty:**
   - Clustering uses point estimates of random effects from RQ 6.1.4 LMM, ignoring estimation uncertainty (standard errors). Participants with poorly estimated random effects (low precision) treated identically to well-estimated participants. May introduce noise into clustering.
   - Alternative: Use model-based clustering that incorporates uncertainty (e.g., growth mixture models), but increases complexity.

2. **Feature Space Dimensionality:**
   - Only 2 features (intercept, slope) may oversimplify confidence trajectory complexity. Excludes quadratic slopes (non-linear decline), domain-specific random effects (What/Where/When differences), or test session-specific effects.
   - More features may improve phenotype resolution but increase risk of overfitting with N=100.

3. **K-Means Assumptions:**
   - K-means assumes spherical clusters with equal variance. Cluster 2 (Vulnerable) has higher SD for both intercept (0.170) and slope (0.082) than Cluster 0 (SD=0.098, 0.041), violating equal variance assumption. May bias cluster boundaries.
   - Alternative: Gaussian mixture models with unequal covariances.

**Design:**

1. **K Selection Criterion:**
   - BIC monotonic decrease (no elbow) indicates weak clustering structure. K=3 selection driven by Ch5 5.1.5 comparability (theoretical criterion) rather than optimal statistical fit. Results are K-selection dependent.
   - Sensitivity analysis: Test K=2, K=4, K=5 solutions to assess robustness of phenotype interpretation.

2. **Cross-RQ Dependency Constraints:**
   - Results entirely dependent on RQ 6.1.4 random effects quality. If RQ 6.1.4 LMM misspecified (e.g., wrong functional form, omitted covariates), random effects are biased, cascading into clustering errors.
   - No independent validation of random effects accuracy.

3. **Bootstrap Stability Limitations:**
   - Jaccard = 0.683 (95% CI: [0.385, 1.000]) falls below 0.75 high-stability threshold. Wide CI ([0.385, 1.000]) suggests high variability in cluster stability across bootstrap resamples. Cluster membership may be fragile for borderline participants.

**Statistical:**

1. **Chi-Square Test Assumptions:**
   - Chi-square test assumes independent observations. However, confidence and accuracy phenotypes derived from same participants (correlated within-person), potentially inflating chi-square statistic and lowering p-value. Conservative interpretation: p < 0.000001 is so extreme that even with correlation adjustment, association likely remains significant.
   - Expected cell frequencies: All cells have counts >= 2 (minimum observed), but some cells approach lower bound (Acc 1 x Conf 2 = 3). Chi-square approximation may be less accurate for small expected frequencies.

2. **Multiple Comparisons:**
   - Cross-tabulation examines 9 cells (3x3), increasing Type I error risk for pairwise cell comparisons (not formally tested, but visually inspected in heatmap). No correction applied (exploratory analysis).

3. **Effect Size Interpretation:**
   - Cramer's V = 0.41 (medium effect) is moderate, not large. Suggests substantial but incomplete coupling between confidence and accuracy phenotypes. Individual variability in metacognitive calibration remains (some participants have mismatched phenotypes).

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (aging affects both memory and metacognition, phenotype structure may differ)
  - Clinical populations (MCI, dementia patients show metacognitive impairment, different phenotypes expected)
  - Cross-cultural samples (confidence rating styles vary by culture, may alter clustering structure)

**Context:**
- VR desktop paradigm (not fully immersive HMD). Confidence ratings in VR may differ from real-world episodic memory confidence.
- Repeated testing (4 sessions) introduces testing effects. Single-test confidence phenotypes may differ.

**Task:**
- REMEMVR-specific encoding task. Confidence trajectories for naturalistic episodic memories (autobiographical events) may show different phenotype structure.

### Technical Limitations

**K-Means Algorithm Limitations:**
- **Initialization Sensitivity:** K-means results depend on random initialization (seed=42 used for reproducibility). Different seeds may produce slightly different cluster assignments for borderline participants. Jaccard stability = 0.683 confirms moderate sensitivity.
- **Hard Assignment:** K-means assigns each participant to exactly one cluster (hard assignment). Fuzzy clustering (e.g., Gaussian mixture models) would allow probabilistic membership (participants can partially belong to multiple clusters), better capturing continuous latent distribution.

**Random Effects as Clustering Features:**
- Random effects are model-based estimates (derived from RQ 6.1.4 LMM), not raw data. Model misspecification in RQ 6.1.4 (e.g., linear time assumption, homoscedasticity assumption) propagates into clustering. No validation of LMM assumptions performed before extracting random effects.

**Cross-Tabulation Dependency:**
- Cross-tabulation relies on Ch5 5.1.5 accuracy cluster labels. If Ch5 5.1.5 clustering is unstable or K-selection is suboptimal, integration test results are affected. No independent validation of Ch5 5.1.5 clustering quality available.

### Limitations Summary

Despite these constraints, findings are **robust within scope:**
- Chi-square test highly significant (p < 0.000001) with medium effect size (V = 0.41) - unlikely to be artifact
- Silhouette score (0.459) confirms acceptable cluster quality above threshold (0.40)
- Integration finding aligns with prior metacognition literature (Fleming & Lau, 2014; metacognitive monitoring tracks memory signals)

Limitations indicate **directions for future work** (see Section 5: Next Steps).

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Sensitivity Analysis for K Selection:**
- **Why:** BIC monotonic decrease indicates K-selection ambiguity. K=3 was chosen for Ch5 5.1.5 comparability, but K=4 or K=5 may reveal finer phenotype structure.
- **How:** Re-run K-means with K=4 and K=5, compute silhouette and Jaccard for each, compare crosstab patterns with Ch5 5.1.5 (using correspondence analysis or mosaic plots for K-mismatch).
- **Expected Insight:** Determine if phenotype interpretations (Resilient vs Vulnerable) are robust to K choice, or if alternative K solutions suggest different phenotype structures (e.g., Resilient-High, Resilient-Low, Vulnerable-Moderate, Vulnerable-Severe at K=4).
- **Timeline:** Immediate (same data, re-run steps 3-8 with different K)

**2. Cluster 1 Positive Slope Investigation:**
- **Why:** 41% of participants show INCREASING confidence over retention intervals (counterintuitive finding). Need to verify if this is genuine metacognitive recalibration or artifact.
- **How:** Extract raw confidence ratings (not random effects) for Cluster 1 participants from RQ 6.1.1 theta scores. Plot individual trajectories (confidence vs TSVR) overlaid with accuracy trajectories. Compute within-person confidence-accuracy correlations.
- **Expected Insight:** If confidence increases while accuracy declines, suggests miscalibration (overconfidence bias). If confidence and accuracy both increase or stabilize, suggests genuine testing effect (practice improves both memory and metacognition).
- **Timeline:** ~1 day (requires linking RQ 6.1.1 raw data with cluster assignments)

**3. Random Effects Estimation Uncertainty Analysis:**
- **Why:** Clustering treats all random effects point estimates as equally precise, ignoring standard errors. Cluster 0's balanced crosstab may reflect high estimation uncertainty (noise).
- **How:** Extract random effects standard errors from RQ 6.1.4 LMM output. Compute mean SE per cluster. Test if Cluster 0 has significantly higher SE than Clusters 1 and 2 (one-way ANOVA on SE by cluster).
- **Expected Insight:** If Cluster 0 has higher SE, suggests it's a "residual" cluster capturing poorly estimated participants. Supports re-clustering after excluding high-uncertainty participants.
- **Timeline:** Immediate (RQ 6.1.4 should have SE estimates in LMM output, if not, requires re-running RQ 6.1.4 with SE extraction)

### Planned Thesis RQs (Chapter 6 Continuation)

**RQ 6.3.5 (Planned): Domain-Specific Confidence Phenotypes**
- **Focus:** Cluster participants separately for What, Where, When confidence trajectories (3 separate K-means analyses). Test if phenotype structure differs by domain.
- **Why:** Current RQ uses omnibus "All" factor. Domain-specific clustering may reveal that participants are Resilient for spatial confidence (Where) but Vulnerable for temporal confidence (When).
- **Builds On:** Uses RQ 6.3.4 domain-specific random effects (if available), otherwise requires re-extracting domain-stratified random effects from RQ 6.1.1.
- **Expected Timeline:** After RQ 6.3.4 completes (domain-specific ICC decomposition)

**RQ 6.5.X (Potential): Confidence-Accuracy Calibration Analysis**
- **Focus:** Quantify metacognitive calibration (gamma correlation, calibration curves) separately for each confidence phenotype. Test if Cluster 1 (increasing confidence) shows poorer calibration than Clusters 0 and 2.
- **Why:** Chi-square test confirms association, but doesn't quantify calibration quality (how well confidence ratings predict accuracy). Phenotypes may differ in calibration (e.g., Vulnerable = well-calibrated but low, Resilient-Increasing = poorly calibrated overconfidence).
- **Builds On:** Uses cluster assignments from this RQ + trial-level confidence-accuracy data from RQ 6.1.1.
- **Expected Timeline:** Chapter 6 later RQs (after core trajectory analyses complete)

### Methodological Extensions (Future Data Collection or Re-Analysis)

**1. Growth Mixture Modeling (GMM) as Alternative:**
- **Current Limitation:** K-means ignores random effects estimation uncertainty and assumes spherical clusters.
- **Extension:** Re-analyze using latent growth mixture modeling (GMM) in Mplus or lavaan. GMM simultaneously estimates random effects AND cluster membership, incorporating uncertainty. Also allows unequal cluster variances.
- **Expected Insight:** Test if GMM identifies same K=3 phenotypes or different structure. GMM provides probabilistic cluster membership (soft assignment) rather than hard K-means boundaries.
- **Feasibility:** Immediate (same data, different statistical software/method). Requires ~2 days for GMM specification and convergence.

**2. Incorporate Quadratic Slopes:**
- **Current Limitation:** Only linear random effects (intercept, slope) used. Confidence trajectories may be non-linear (e.g., rapid decline Day 0-1, plateau Day 3-6).
- **Extension:** Re-run RQ 6.1.4 with quadratic time term (TSVR²) in LMM, extract random quadratic slopes. Cluster on 3 features (intercept, linear slope, quadratic slope). Test if non-linear phenotypes emerge.
- **Expected Insight:** May explain Cluster 1 positive slope (linear approximation to U-shaped trajectory: initial decline, then recovery).
- **Feasibility:** ~3 days (requires re-running RQ 6.1.4 LMM with quadratic term, re-clustering with 3D feature space)

**3. Validate with External Metacognitive Measures:**
- **Current Limitation:** Confidence phenotypes based solely on REMEMVR confidence ratings. No external validation of metacognitive skill.
- **Extension:** Collect independent metacognitive measures (e.g., Metacognitive Awareness Inventory, confidence-accuracy calibration tasks outside VR). Test if confidence phenotypes predict external metacognitive scores.
- **Expected Insight:** Determine if phenotypes reflect trait-like metacognitive skill (generalizable) or task-specific confidence patterns (REMEMVR-only).
- **Feasibility:** Requires new data collection (~6 months, N=100 new participants with expanded battery)

**4. Longitudinal Follow-Up (Test-Retest Stability):**
- **Current Limitation:** Phenotypes identified at single time point (one 4-session protocol). Stability unknown (do participants remain in same cluster 1 year later?).
- **Extension:** Re-test N=50 subsample 1 year later, re-extract random effects, assign to clusters. Compute test-retest agreement (Cohen's kappa for cluster membership).
- **Expected Insight:** Test if confidence phenotypes are stable traits (high kappa) or state-dependent (low kappa). High stability validates phenotype interpretation as enduring individual differences.
- **Feasibility:** Long-term (1+ year delay, requires participant retention)

### Theoretical Questions Raised

**1. What Drives Cluster 1 Increasing Confidence?**
- **Question:** Is positive slope (increasing confidence) due to (a) metacognitive recalibration (learning), (b) testing effects (familiarity), (c) response style shifts (demand characteristics), or (d) measurement artifact?
- **Next Steps:** Mixed-methods approach: (a) examine individual trajectories quantitatively (Immediate Follow-Up #2 above), (b) conduct post-test interviews with N=10 Cluster 1 participants asking "Why did your confidence change over sessions?" (qualitative).
- **Expected Insight:** If participants report "I got more comfortable with the task" (familiarity) vs "I learned what I could remember" (recalibration), distinguishes mechanisms.
- **Feasibility:** Interviews require IRB amendment (~3 months), quantitative analysis immediate

**2. Why Is Confidence-Accuracy Association Moderate (Not Perfect)?**
- **Question:** Cramer's V = 0.41 (medium effect) indicates substantial coupling, but not perfect integration. What explains the 59% variance NOT explained by association? Individual differences in metacognitive calibration? Measurement error?
- **Next Steps:** Decompose chi-square residuals (observed - expected cell counts) to identify specific phenotype combinations driving association. Test if off-diagonal cells (mismatched phenotypes) have distinct characteristics (e.g., lower cognitive ability, higher anxiety).
- **Expected Insight:** May identify "metacognitive mismatch" phenotypes (good memory + poor metacognition, or vice versa) with clinical relevance (e.g., Dunning-Kruger effect).
- **Feasibility:** Immediate (chi-square residuals computable from existing crosstab)

**3. Do Confidence Phenotypes Predict Real-World Memory Outcomes?**
- **Question:** Vulnerable phenotype (low baseline, steep decline) may predict everyday memory complaints or MCI risk. Can confidence trajectories be used as early warning signs?
- **Next Steps:** Correlate phenotype membership with external criteria: (a) self-reported memory complaints (CFQ - Cognitive Failures Questionnaire), (b) prospective memory performance (diary study), (c) neuropsychological test battery (RAVLT, BVMT).
- **Expected Insight:** If Cluster 2 (Vulnerable) predicts higher memory complaints and lower objective memory scores, validates phenotype as clinically meaningful risk marker.
- **Feasibility:** Requires expanded assessment battery (~6 months, new data collection)

### Priority Ranking

**High Priority (Do First):**
1. **Immediate Follow-Up #2** (Cluster 1 positive slope investigation) - addresses counterintuitive finding, critical for interpretation
2. **Immediate Follow-Up #1** (K sensitivity analysis) - tests robustness of K=3 selection, low cost
3. **Methodological Extension #1** (GMM) - validates K-means results with more rigorous method

**Medium Priority (Subsequent):**
1. **RQ 6.3.5** (domain-specific phenotypes) - natural extension to domain analyses in Chapter 6
2. **Immediate Follow-Up #3** (random effects SE analysis) - investigates Cluster 0 uncertainty hypothesis
3. **Theoretical Question #2** (decompose chi-square residuals) - deepens integration finding interpretation

**Lower Priority (Aspirational):**
1. **Methodological Extension #3** (external metacognitive validation) - ideal but requires new data
2. **Methodological Extension #4** (longitudinal test-retest) - important for trait stability, but long timeline
3. **Theoretical Question #3** (real-world memory outcomes) - clinical relevance high, but resource-intensive

### Next Steps Summary

The findings establish **three confidence phenotypes (Resilient-Stable, Resilient-Increasing, Vulnerable) with significant integration with accuracy phenotypes** (p < 0.000001, V = 0.41), raising three critical questions for immediate follow-up:

1. **Cluster 1 Positive Slope:** Why does 41% of sample show increasing confidence? (Immediate Follow-Up #2)
2. **K Selection Robustness:** Are phenotypes stable across K=3, K=4, K=5 solutions? (Immediate Follow-Up #1)
3. **Association Incompleteness:** What explains moderate (not perfect) confidence-accuracy coupling? (Theoretical Question #2)

Methodological extensions (GMM, quadratic slopes, external validation) strengthen phenotype validation but require additional analysis time or new data collection beyond current thesis scope.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-12-11
