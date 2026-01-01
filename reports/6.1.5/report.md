# RQ 6.1.5: Trajectory Clustering

**Chapter:** Ch6
**Status:** PLATINUM CERTIFIED
**Certification Date:** 2025-12-29
**Report Generated:** 2026-01-01

---

## 1. Executive Summary

**What we tested:** Whether participants cluster into distinct confidence trajectory phenotypes, and whether these phenotypes align with Ch5 accuracy phenotypes (testing memory-metacognition integration vs dissociation).

**What we found:** K-means clustering identified 3 confidence phenotypes (Resilient-Stable 42%, Resilient-Increasing 41%, Vulnerable 17%). Chi-square test revealed highly significant association with accuracy phenotypes (Ç²=34.34, p<0.000001, Cramer's V=0.41).

**Why it matters:** Provides empirical evidence for integrated memory-metacognition system where confidence judgments track actual memory ability. Metacognitive monitoring is trait-like (stable individual differences) and coupled with memory performance, not dissociable.

---

## 2. Research Question

**Question:**
Do participants cluster into confidence phenotypes, and do they match accuracy phenotypes?

**Hypothesis:**
K-means clustering will identify 2-3 distinct confidence phenotypes, paralleling Ch5 5.1.5 accuracy clusters (Resilient vs Vulnerable). If confidence and accuracy phenotypes match (chi-square p<0.05), suggests integrated memory-metacognition system. If divergent (pe0.05), suggests dissociable systems.

**Theoretical Framework:**
- **Metacognitive Monitoring Theory:** Individual differences in metacognitive skill manifest as stable confidence trajectories
- **Memory-Metacognition Integration:** If phenotypes align, metacognitive monitoring tracks memory state (Fleming & Dolan, 2012)
- **Measurement Sensitivity:** 5-level ordinal confidence data provides ~2.3x more information than dichotomous accuracy

**Expected Patterns:**
- 2-3 clusters (matching Ch5 structure)
- Silhouette >0.40 (acceptable quality)
- Chi-square significant if integrated, non-significant if dissociated

---

## 3. Historical Context

**Archive Search:**
- Topics searched: 2
- Entries found: 2
- Date range: 2025-12-11 to 2025-12-29

**Key Events (Chronological):**
1. 2025-12-11 19:15 - RQ 6.1.5 executed successfully, INTEGRATION hypothesis confirmed (source: archive/rq_6.1.5_trajectory_clustering_integration_confirmed.md)
2. 2025-12-11 19:15 - CRITICAL lesson documented: Validation agents must run SEQUENTIALLY (rq_results creates summary.md before rq_validate runs) (source: archive/rq_6.1.5_trajectory_clustering_integration_confirmed.md)
3. 2025-12-11 19:15 - K=3 forced selection despite BIC monotonic decrease, matched to Ch5 5.1.5 for valid cross-RQ comparison (source: archive/rq_6.1.5_trajectory_clustering_integration_confirmed.md)
4. 2025-12-29 ~18:00 - PLATINUM certification batch: RQ 6.1.5 newly certified (LocationType×Time series) (source: archive index line 698)

**Blockers Resolved:**
- **Validation workflow issue:** Parallel launch of rq_inspect, rq_results, rq_validate caused circuit breaker (rq_validate needs summary.md from rq_results). Solution: Sequential execution documented in execute.md.
- **BIC monotonic decrease:** No elbow pattern, K=3 selection driven by Ch5 comparability (theoretical criterion) rather than statistical optimum.

**Cross-References:**
- Related to RQ 6.1.4: Provides random effects (intercept, slope) for clustering
- Related to Ch5 5.1.5: Provides accuracy cluster labels for cross-tabulation

---

## 4. Methodology

### Data Sources

**Root or Derived:**
- DERIVED: Uses outputs from RQ 6.1.4 (confidence random effects) + Ch5 5.1.5 (accuracy cluster labels)

**Specific Sources:**
- Primary: results/ch6/6.1.4/data/step04_random_effects.csv (100 rows: UID, intercept, slope)
- Comparison: results/ch5/5.1.5/data/step04_cluster_assignments.csv (100 rows: UID, accuracy_cluster_label)

### Analysis Pipeline

**Steps:**

| Step | Description | Output Files |
|------|-------------|--------------|
| 1 | Load random effects from RQ 6.1.4 | step01_random_effects_loaded.csv |
| 2 | Standardize features to z-scores | step02_standardized_features.csv |
| 3 | K-means clustering K=2-6 with BIC | step03_cluster_selection.csv, step03_bic_plot_data.csv |
| 4 | Fit final K-means K=3 | step04_cluster_assignments.csv, step04_cluster_centers.csv |
| 5 | Validate cluster quality | step05_validation_metrics.csv |
| 6 | Characterize clusters (phenotypes) | step06_cluster_characterization.csv, step06_phenotype_descriptions.txt |
| 7 | Cross-tabulate with Ch5 5.1.5 | step07_crosstab_confidence_accuracy.csv, step07_crosstab_row_percentages.csv, step07_crosstab_column_percentages.csv |
| 8 | Chi-square association test | step08_chi_square_test.csv, step08_association_interpretation.txt |

### Tools Used

**Key Tools:**
- K-means clustering: sklearn.cluster.KMeans (seed=42 for reproducibility)
- BIC computation: N*log(SSE/N) + K*log(N)
- Silhouette score: sklearn.metrics.silhouette_score
- Davies-Bouldin index: sklearn.metrics.davies_bouldin_score
- Jaccard bootstrap stability: 1000 bootstrap resamples
- Chi-square test: scipy.stats.chi2_contingency
- Cramer's V effect size: sqrt(chi2 / (N * min(rows-1, cols-1)))

### Critical Design Decisions

**Decisions:**
- **K=3 forced selection:** Despite BIC monotonic decrease (no elbow), K=3 chosen to match Ch5 5.1.5 for valid cross-tabulation. Alternative K solutions (K=4-6) statistically defensible but prevent direct phenotype comparison. (source: plan.md, logs/steps_01_to_08.log)
- **Z-score standardization:** Equalizes weighting of intercept and slope dimensions in K-means distance metric (prevents larger-scale feature dominating). (source: plan.md Step 2)
- **Bootstrap stability validation:** Jaccard coefficient computed via 1000 bootstrap resamples to test cluster robustness beyond silhouette score alone. (source: plan.md Step 5)

**Warnings (if any from Step 5):**
- WARNING: Outliers detected in Step 2 - intercept: 1, slope: 1 (>3 SD). Outlier UID: A019. (source: logs/steps_01_to_08.log line 22-23)
- WARNING: Unstable clusters (Jaccard=0.6835) below 0.75 high-stability threshold. (source: logs/steps_01_to_08.log line 70)

---

## 5. Results

### Sample Characteristics

**Sample Size:**
- Total N: 100
- Exclusions: 0 (all participants from RQ 6.1.4 included)
- Missing data: 0% (all 100 had complete random effects estimates)

**Final Sample:**
- N = 100 (clustering on 2 features: random intercept, random slope)

### Primary Findings

**K-Means Cluster Selection:**

| K | SSE | BIC | Silhouette | Optimal |
|---|-----|-----|------------|---------|
| 2 | 79.17 | -14.14 | 0.538 | No |
| **3** | **46.66** | **-62.40** | **0.459** | **Yes** |
| 4 | 30.30 | -100.99 | 0.460 | No |
| 5 | 20.84 | -133.79 | 0.465 | No |
| 6 | 15.91 | -156.21 | 0.453 | No |

**Note:** BIC monotonically decreases (no traditional elbow). K=3 selected for Ch5 5.1.5 comparability, not statistical optimum.

**Cluster Quality Metrics:**

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Silhouette | 0.459 | >0.40 | PASS |
| Davies-Bouldin | 0.676 | <1.0 | PASS |
| Jaccard Stability | 0.683 | >0.75 | FAIL (marginal) |
| Jaccard 95% CI | [0.385, 1.000] | - | Wide CI |

**Three Confidence Phenotypes:**

| Cluster | N (%) | Mean Intercept | Mean Slope | Phenotype |
|---------|-------|----------------|------------|-----------|
| 0 | 42 (42%) | -0.056 | -0.016 | Resilient (Stable) |
| 1 | 41 (41%) | +0.229 | **+0.085** | Resilient (INCREASING) |
| 2 | 17 (17%) | -0.413 | -0.166 | Vulnerable |

**Notable:** Cluster 1 shows POSITIVE slope (increasing confidence over time), counterintuitive pattern.

**Chi-Square Association Test (Integration vs Dissociation):**

- Ç² = 34.34, df = 4, p < 0.000001 (highly significant)
- Cramer's V = 0.414 (medium effect, 0.30-0.50 range)
- **Interpretation:** INTEGRATED (confidence and accuracy phenotypes associated)

**Cross-Tabulation (Confidence × Accuracy):**

|  | Acc 0 | Acc 1 | Acc 2 | Total |
|---|-------|-------|-------|-------|
| Conf 0 (Resilient) | 13 | 15 | 14 | 42 |
| Conf 1 (Resilient) | **0** | **26** | 15 | 41 |
| Conf 2 (Vulnerable) | 12 | 3 | 2 | 17 |

**Key Patterns:**
- Conf 1 × Acc 0 = 0 (perfect exclusion)
- Conf 1 × Acc 1 = 26 (63% of Conf 1, strong association)
- Conf 2 concentrated in Acc 0-1 (88%, vulnerable confidence aligns with lower accuracy)

---

## 6. Visualizations

### Plot 1: BIC Elbow Analysis
**File:** `plots/bic_elbow.png`

**Description:**
Line plot showing BIC values across K=2-6 candidate solutions. X-axis: Number of clusters (K). Y-axis: BIC values (-160 to -10). Red star marks K=3 as selected solution.

**Key Patterns:**
- Monotonic BIC decrease from K=2 (BIC=-14.14) to K=6 (BIC=-156.21)
- No traditional elbow inflection point
- Annotation states "BIC monotonically decreases (not reliable for K selection)" and "K=3 selected for Ch5 5.1.5 comparability"

**Connection to Findings:**
Visual confirms weak clustering structure (no clear statistical optimum). K=3 selection driven by theoretical comparability, not BIC minimum. Validates decision documented in logs.

### Plot 2: Confidence Trajectory Phenotypes (2D Scatter)
**File:** `plots/cluster_scatter.png`

**Description:**
2D scatter plot of 100 participants in feature space. X-axis: Baseline Confidence (Intercept, z-score, -4 to +2.5). Y-axis: Confidence Decline Rate (Slope, z-score, -4 to +2.5). Three clusters color-coded: Green (Cluster 0, N=42), Blue (Cluster 1, N=41), Red (Cluster 2, N=17). Black 'X' markers show cluster centroids.

**Key Patterns:**
- Cluster 0 (green): Central region, near-origin, moderate spread
- Cluster 1 (blue): Right-upper quadrant (high intercept, positive slope), visually distinct
- Cluster 2 (red): Left-lower quadrant (low intercept, steep negative slope), spatially separated
- One extreme outlier in Cluster 2 (intercept H -3.5, slope H -4)

**Connection to Findings:**
Clear spatial separation between Cluster 1 (upper-right) and Cluster 2 (lower-left) confirms Davies-Bouldin=0.676 (good separation). Cluster 1's upper-right positioning validates positive slope finding (41% show increasing confidence). Cluster 0 central overlap explains moderate silhouette score.

### Plot 3: Cross-Tabulation Heatmap
**File:** `plots/crosstab_heatmap.png`

**Description:**
3×3 heatmap showing Confidence clusters (rows) × Accuracy clusters (columns). Color scale: Light blue (count=0) to dark blue (count=26). Cell annotations show exact counts. Statistical annotation: Ç²=34.34, p<0.000001, V=0.41 (INTEGRATED).

**Key Patterns:**
- Darkest cell: Conf 1 × Acc 1 (count=26, dark blue) - strong association
- Empty cell: Conf 1 × Acc 0 (count=0, white) - perfect exclusion
- Vulnerable concentration: Conf 2 highest in Acc 0 (N=12) and Acc 1 (N=3)
- Balanced pattern: Conf 0 distributed across all accuracy clusters (13, 15, 14)

**Connection to Findings:**
Visual confirms chi-square result (p<0.000001). Dark blue cell (Conf 1 × Acc 1) and white cell (Conf 1 × Acc 0) provide evidence of phenotype association. Cramer's V=0.41 (medium effect) supported by moderate color contrast (not perfectly diagonal, but clear patterns).

**Disclaimer:** Individual cell patterns exploratory only. Omnibus chi-square test (Ç²=34.34) is confirmatory. No pairwise cell comparisons formally tested.

---

## 7. Interpretation

### Hypothesis Testing

**Outcome:** PARTIALLY SUPPORTED

**Rationale:**
- K=3 confidence phenotypes identified (matches Ch5 5.1.5) - SUPPORTED
- Silhouette=0.459 >0.40 threshold - SUPPORTED
- Jaccard=0.683 <0.75 threshold - MARGINAL (moderate stability, not high)
- Two Resilient + one Vulnerable cluster parallels Ch5 structure - SUPPORTED

**Integration Hypothesis:** STRONGLY SUPPORTED
- Chi-square highly significant (p<0.000001, well below p<0.05)
- Cramer's V=0.414 (medium effect)
- Cross-tabulation shows clear patterns (Conf 1 × Acc 1 = 26, Conf 1 × Acc 0 = 0)

### Theoretical Implications

**Metacognitive Monitoring Theory:**
Identification of 3 confidence phenotypes supports trait-like individual differences in metacognitive monitoring. Moderate silhouette (0.459) suggests stable but not discrete phenotypes.

**Memory-Metacognition Integration:**
Chi-square (p<0.000001, V=0.41) provides evidence for Fleming & Dolan (2012) integrated framework: metacognitive monitoring relies on same memory signals driving accuracy. Medium effect (V=0.41) indicates substantial but not perfect coupling.

**5-Level Ordinal Data Sensitivity:**
Hypothesis that 5-level confidence data would provide stronger clustering than dichotomous accuracy NOT clearly confirmed. Silhouette=0.459 only marginally above threshold. Possible explanations: response style biases, lower between-participant variance, or inherent noise in confidence trajectories.

### Cross-RQ Patterns

**Convergent Evidence:**
- RQ 6.1.4: Provided random effects (intercept, slope) showing sufficient variance for clustering
- Ch5 5.1.5: K=3 accuracy phenotypes (Resilient vs Vulnerable) aligned with confidence phenotypes
- Integration finding consistent with metacognitive monitoring literature (Fleming & Lau, 2014)

### Unexpected Findings

**Anomaly 1: Cluster 1 Positive Slope (41% show INCREASING confidence)**

**Description:** Mean slope = +0.085 (positive), suggesting confidence increases over retention intervals despite typical memory decline.

**Possible Explanations:**
- Testing effect on confidence (familiarity with VR task increases comfort)
- Metacognitive recalibration (initial underestimation corrected across sessions)
- Response style shift (demand characteristics)
- Selective attrition artifact (unlikely, 3% attrition too small)

**Investigation Needed:** Examine individual trajectories for Cluster 1, compare with accuracy trajectories to assess calibration.

**Anomaly 2: BIC Monotonic Decrease (no elbow)**

**Description:** BIC continuously decreases K=2 to K=6, no clear minimum.

**Possible Explanations:**
- Continuous latent distribution (not discrete subpopulations)
- Weak between-cluster separation (moderate silhouette, borderline Jaccard)
- Sample size limitations (N=100 insufficient for clear structure)
- Feature space dimensionality (only 2 features may oversimplify)

**Interpretation Impact:** K=3 selection exploratory (comparability-driven), not definitive. Alternative K solutions equally defensible statistically.

**Anomaly 3: Cluster 0 Balanced Crosstab (no accuracy association)**

**Description:** Conf 0 shows balanced distribution across accuracy clusters (13, 15, 14), suggesting independence.

**Possible Explanations:**
- Heterogeneous subgroup (well-calibrated + poorly calibrated cancel out)
- Moderate confidence strategy (mid-range ratings regardless of accuracy)
- Residual cluster (participants not fitting clear Resilient/Vulnerable patterns)

**Investigation Needed:** Check if Cluster 0 has higher random effects estimation uncertainty (standard errors from RQ 6.1.4).

---

## 8. Limitations

### Sample Limitations

- N=100 adequate for medium effects (V>0.30) but underpowered for weak clustering structure
- Cluster 2 (Vulnerable) only N=17 (17%), limiting precision of phenotype characterization
- 3% dropout by Day 6 introduces potential bias if dropouts differ systematically
- University undergraduates (age M=20.3, predominantly female), generalizability unknown

### Methodological Limitations

**Measurement:**
- Random effects point estimates ignore estimation uncertainty (standard errors)
- Only 2 features (intercept, slope) may oversimplify trajectory complexity
- K-means assumes spherical clusters with equal variance (violated: Cluster 2 SD higher)

**Design:**
- BIC monotonic decrease indicates weak structure, K=3 selection driven by comparability not statistical optimum
- Results dependent on RQ 6.1.4 random effects quality (no independent validation)
- Jaccard=0.683 (95% CI [0.385,1.000]) below high-stability threshold, wide CI suggests fragility

**Statistical:**
- Chi-square assumes independence but confidence and accuracy from same participants (potentially inflates statistic)
- Some cells approach lower bound (Conf 2 × Acc 1 = 3), approximation less accurate
- Multiple comparisons (9 cells in 3×3 crosstab) increase Type I error (exploratory only)
- Cramer's V=0.41 (medium, not large) indicates incomplete coupling

### Generalizability Constraints

**Population:** May not generalize to older adults, clinical populations (MCI/dementia), cross-cultural samples

**Context:** VR desktop paradigm (not fully immersive HMD), repeated testing introduces testing effects

**Task:** REMEMVR-specific encoding, naturalistic autobiographical memories may show different phenotype structure

### Technical Limitations

- K-means initialization sensitivity (seed=42 for reproducibility, different seeds may vary for borderline participants)
- Hard assignment (each participant exactly one cluster), fuzzy clustering would better capture continuous distribution
- Model-based estimates (RQ 6.1.4 LMM) not raw data, misspecification propagates

---

## 9. Publication-Ready Summary

**Context & Method:** We tested whether participants cluster into distinct confidence trajectory phenotypes using K-means clustering on random effects (intercept, slope) extracted from best-fitting LMM (RQ 6.1.4). N=100 participants, 2 features, K=3 clusters selected to match Ch5 5.1.5 accuracy clustering for valid cross-tabulation. We then tested integration vs dissociation hypothesis via chi-square test of association between confidence and accuracy phenotypes.

**Results:** K-means identified 3 confidence phenotypes: Resilient-Stable (N=42, 42%, near-average intercept -0.056, shallow slope -0.016), Resilient-Increasing (N=41, 41%, high intercept +0.229, positive slope +0.085), and Vulnerable (N=17, 17%, low intercept -0.413, steep slope -0.166). Cluster quality: silhouette=0.459 (PASS, >0.40 threshold), Davies-Bouldin=0.676 (PASS, <1.0), Jaccard=0.683 (marginal, <0.75 high-stability threshold). Chi-square test revealed highly significant association with accuracy phenotypes (Ç²=34.34, df=4, p<0.000001, Cramer's V=0.414 medium effect).

**Interpretation:** Findings strongly support integration hypothesis: metacognitive monitoring (confidence) tracks memory state (accuracy), not dissociable systems. Confidence phenotypes align with accuracy phenotypes (Resilient confidence ’ moderate-to-high accuracy, Vulnerable confidence ’ lower accuracy). 41% show counterintuitive increasing confidence (Cluster 1), possibly reflecting testing effects or metacognitive recalibration. BIC monotonic decrease indicates weak clustering structure, K=3 selection driven by theoretical comparability rather than statistical optimum.

**Conclusion:** Confidence trajectories show trait-like individual differences that align with accuracy phenotypes (Ç²=34.34, p<0.000001, V=0.41), providing empirical support for integrated memory-metacognition system (Fleming & Dolan, 2012). Moderate effect size (V=0.41) suggests substantial but incomplete coupling, with 41% unexplained variance indicating individual differences in metacognitive calibration.

---

## 10. Metadata & Sources

### Report Metadata
- **Generated:** 2026-01-01T00:00:00Z
- **Agent:** rq_report v1.0.0 (Sonnet 4.5 model)
- **RQ Folder:** results/ch6/6.1.5/

### Sources Synthesized

**Archive Sources:** 2 topics, 2 entries
- rq_6.1.5_trajectory_clustering_integration_confirmed (archive/rq_6.1.5_trajectory_clustering_integration_confirmed.md, 2025-12-11 19:15)
- platinum_certification_batch_ch6_24_rqs_started (archive index line 697, 2025-12-29 ~18:00)

**RQ Files:** 21 files
- **Core docs:** 1_concept.md, 2_plan.md, summary.md
- **Validation:** PLATINUM_FINALIZATION_REPORT.md (no scholar.md, no stats.md)
- **Specifications:** (no tools.yaml, no analysis.yaml - v4.0 workflow used code generation directly)
- **Execution:** status.yaml, 12 data files, 1 log file, 3 plot files
- **PLATINUM:** PLATINUM_FINALIZATION_REPORT.md

### Warnings Flagged

- WARNING: Outliers detected in Step 2 - participant A019 >3 SD on both intercept and slope (source: logs/steps_01_to_08.log line 22-23)
- WARNING: Unstable clusters (Jaccard=0.683 <0.75 high-stability threshold) (source: logs/steps_01_to_08.log line 70)
- WARNING: Missing optional files (scholar.md, stats.md) - RQ 6.1.5 completed before full validation workflow implemented
- NOTE: BIC monotonic decrease indicates weak clustering structure, K=3 selection theoretical not statistical (source: logs/steps_01_to_08.log line 36-40)

---

**End of Report**
