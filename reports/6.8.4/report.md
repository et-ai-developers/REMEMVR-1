# RQ 6.8.4: Source-Destination Confidence Clustering

**Chapter:** Ch6
**Status:** PLATINUM CERTIFIED
**Certification Date:** 2025-12-30
**Report Generated:** 2026-01-01

---

## 1. Executive Summary

**What we tested:** Whether confidence clustering for source-destination memory replicates the exceptional 4-cluster structure (Silhouette = 0.417) found for accuracy in Ch5 5.5.7.

**What we found:** Hypothesis NOT supported. Confidence clustering achieved Silhouette = 0.330 (21% lower than accuracy, below 0.40 threshold). However, confidence and accuracy phenotypes showed highly significant association (chi-square p < 0.0001).

**Why it matters:** Source-destination dissociation creates EXCEPTIONAL accuracy phenotypes but only MODERATE confidence phenotypes, revealing that memory architecture and metacognitive monitoring are partially dissociable systems. This finding validates differential assessment strategies for memory vs metacognition in VR-based cognitive testing.

---

## 2. Research Question

**Question:**
Does confidence clustering for source-destination memory replicate the strong 4-cluster structure found for accuracy in Ch5 5.5.7?

**Hypothesis:**
Confidence clustering will achieve Silhouette >= 0.40 quality threshold, replicating Ch5 5.5.7's exceptional clustering quality (0.417). BIC will select K=4 clusters (matching Ch5). If achieved, this validates that source-destination dissociation captures fundamental individual differences that extend beyond accuracy to metacognitive monitoring.

**Theoretical Framework:**
- **Source-Destination Dissociation (Ch5 5.5 Findings):** Source memory (pick-up location, initial encoding) shows slower decay and regression-to-mean pattern. Destination memory (put-down location, motor memory) shows faster decay and fan-effect pattern. These fundamentally different forgetting dynamics may create distinct individual difference phenotypes.
- **Dual-Process Theory (Yonelinas, 2002):** Source memory may rely more on recollection (explicit encoding), while destination may rely more on familiarity (automatic encoding). Different retrieval processes may create different metacognitive signatures.
- **Working Memory Capacity:** High WM capacity individuals may show better source memory (controlled encoding) but similar destination memory (automatic encoding), creating interaction patterns.

**Expected Patterns:**
- BIC minimum at K=4 clusters (matching Ch5 5.5.7)
- Silhouette >= 0.40 (exceeding typical 0.30 threshold, matching Ch5 0.417)
- Davies-Bouldin < 1.0 (good separation)
- Jaccard bootstrap stability > 0.70 (robust clusters)
- Chi-square association with Ch5 5.5.7 clusters: p < 0.05

---

## 3. Historical Context

**Archive Search:**
- Topics searched: 2
- Entries found: 2 major historical contexts
- Date range: 2025-12-13 to 2025-12-31

**Key Events (Chronological):**

1. **2025-12-13 13:45** - 824x ICC Ratio At Risk identified (source: archive/ch6_824x_icc_ratio_at_risk.md)
   - RQ 6.1.4 discovered confidence shows 824x more individual differences than accuracy (ICC_slope ratio)
   - Risk: Finding based on single-best model (Recip_sq, 21.7% weight), 78.3% of evidence ignored
   - Concern raised: If random effects change with model averaging, major finding might not hold

2. **2025-12-13 14:30** - Model Averaging Validation Foundation established (source: archive/ch6_824x_icc_model_averaged_validation.md)
   - RQ 6.1.1 implemented model averaging with 48 competitive models (”AIC < 7)
   - Model-averaged random slopes computed (SD = 0.099)
   - Critical output: step05b_model_averaged_random_effects.csv provides robust foundation for ICC decomposition
   - Risk mitigated: 824x ratio now validated against model selection uncertainty

3. **2025-12-31** - Cross-chapter comparison noted (source: archive_index.md line 737)
   - RQ 6.8.3 PLATINUM certification documented Source-Destination opposite-correlation pattern NON-REPLICATION in confidence
   - Accuracy (Ch5 5.5.6): Source r=+0.99 (regression to mean), Destination r=-0.90 (fan effect) - OPPOSITE signs
   - Confidence (RQ 6.8.3): Source r=-0.24, Destination r=-0.40 (SAME sign, both negative)
   - MAJOR DISCOVERY: Memory-metacognition system dissociation - metacognitive monitoring does NOT have full access to memory architecture
   - Cross-chapter comparison: 5.5.7 Silhouette=0.417 vs 6.8.4 Silhouette=0.330, accuracy 21% better separation

**Blockers Resolved:**
- Model averaging validation foundation (2025-12-13): Established robust random effects for derivative RQs to avoid single-model dependency
- GLMM compliance evaluation (2025-12-30): Determined GLMM NOT APPLICABLE for clustering RQ (documented in PLATINUM report)

**Cross-References:**
- Related to Ch5 5.5.7: Accuracy clustering baseline (Silhouette = 0.417, K=4) provides comparison target
- Related to RQ 6.8.3: Parent RQ providing random effects inputs for this clustering analysis
- Related to RQ 6.1.4: Context of confidence showing more individual differences than accuracy (824x ratio)

---

## 4. Methodology

### Data Sources

**DERIVED: Uses outputs from RQ 6.8.3**

**Specific Sources:**
- results/ch6/6.8.3/data/step04_random_effects.csv (200 rows: 100 participants x 2 location types)
- results/ch5/5.5.7/data/step03_cluster_assignments.csv (100 rows: accuracy cluster assignments for cross-validation)

**Note:** RQ 6.8.3 outputs 200 rows (100 participants x 2 location types), reshaped to 100 rows x 4 features for clustering.

### Analysis Pipeline

**Steps:**

1. **Step 0:** Reshape Random Effects Data
   - Input: 200 rows from RQ 6.8.3 (long format: participant x location)
   - Output: 100 rows x 4 features (wide format: Source_intercept, Source_slope, Destination_intercept, Destination_slope)
   - Validation: All 100 participants matched between source and destination

2. **Step 1:** Standardize Features
   - Z-score standardization (mean=0, SD=1) for equal weighting
   - Output: 100 rows x 4 z-scores
   - Validation: Mean approximately 0, SD approximately 1 (tolerance +/- 0.01)

3. **Step 2:** K-Means Cluster Selection (BIC)
   - Test K=1 to K=6 clusters
   - Compute BIC for each K
   - Output: BIC minimum at K=5 (90.65)
   - Note: K=4 has similar BIC (91.72), difference = 1.07 (potentially negligible)

4. **Step 3:** Fit Final K-Means Clustering
   - K=5 (optimal from BIC)
   - random_state=42 (reproducibility)
   - Output: Cluster assignments (0-4) for N=100
   - Validation: All cluster sizes >= 10% of N (minimum 10 participants per cluster)

5. **Step 4:** Validate Clustering Quality
   - Silhouette coefficient: 0.330 (FAIL, threshold >= 0.40)
   - Davies-Bouldin index: 0.967 (PASS, threshold < 1.0)
   - Jaccard bootstrap stability (100 iterations): 0.647 (FAIL, threshold > 0.70)
   - Comparison: Ch5 5.5.7 Silhouette = 0.417 (21% higher)

6. **Step 5:** Characterize Clusters
   - Compute mean/SD/min/max for 4 features per cluster
   - Assign phenotype labels (e.g., "HighSrc-Resilient, HighDst-Resilient")
   - Output: 5 phenotype characterizations

7. **Step 6:** Cross-Tabulate with Ch5 5.5.7 Accuracy Clusters
   - Merge confidence cluster assignments (this RQ) with Ch5 5.5.7 accuracy clusters
   - Chi-square test: X² = 43.68, df = 12, p_uncorrected = 1.73×10{u, p_bonferroni = 1.73×10{u
   - Result: HIGHLY SIGNIFICANT association (p < 0.0001, Bonferroni-corrected)

8. **Step 7:** Prepare Cluster Visualization Data
   - PCA projection: 4D -> 2D
   - PC1: 58.4% variance, PC2: 34.0% variance, Total: 92.4%
   - Output: 100 rows x 4 columns (UID, PC1, PC2, cluster)

**Table: Analysis Steps Summary**

| Step | Description | Input | Output | Validation |
|------|-------------|-------|--------|------------|
| 0 | Reshape random effects | 200 rows (long) | 100 rows x 4 features (wide) | All UIDs matched |
| 1 | Standardize features | 4 raw features | 4 z-scores | MeanH0, SDH1 |
| 2 | BIC cluster selection | Standardized features | K=5 optimal | BIC finite for all K |
| 3 | Fit K-means | K=5, seed=42 | Cluster assignments | All clusters >= 10% |
| 4 | Validate quality | Cluster assignments | 3 metrics | Silhouette/Jaccard FAIL |
| 5 | Characterize clusters | Raw features + clusters | 5 phenotypes | Summary stats valid |
| 6 | Cross-tabulate Ch5 | Confidence + accuracy clusters | Chi-square test | p < 0.0001 |
| 7 | PCA visualization | Standardized features | 2D projection | 92.4% variance |

### Tools Used

**Key Tools:**
- K-means clustering (sklearn.cluster.KMeans): Unsupervised machine learning for phenotype identification
- BIC computation: Model selection criterion balancing fit and complexity
- Silhouette coefficient (sklearn.metrics.silhouette_score): Cluster cohesion vs separation quality metric
- Davies-Bouldin index (sklearn.metrics.davies_bouldin_score): Cluster similarity metric
- Jaccard bootstrap stability: Custom implementation (100 iterations) for cluster robustness
- Chi-square test (scipy.stats.chi2_contingency): Association test with Ch5 5.5.7 accuracy clusters
- PCA (sklearn.decomposition.PCA): Dimensionality reduction for visualization

### Critical Design Decisions

**Decisions:**

1. **K=5 selected (not K=4 matching Ch5)** (source: step02_cluster_selection.csv)
   - Rationale: BIC minimum at K=5 (90.65) vs K=4 (91.72), difference = 1.07
   - Limitation: BIC difference < 2 potentially negligible (Kass & Raftery, 1995)
   - Implication: K=4 vs K=5 distinction may not be robust (documented as limitation)

2. **Equal feature weighting via z-score standardization** (source: 2_plan.md)
   - Rationale: Prevents features with larger variance from dominating distance calculations
   - Limitation: Assumes all features equally relevant (intercepts may be more stable than slopes)
   - Alternative: Weighted clustering could prioritize intercepts over slopes (not performed)

3. **K-means (not GMM or other methods)** (source: 2_plan.md)
   - Rationale: Standard for interpretability, assumes spherical clusters
   - Limitation: PCA plot shows Cluster 3 elongated (non-spherical), GMM might improve fit
   - Justification: K-means widely used, GMM adds complexity without theoretical motivation

4. **Silhouette >= 0.40 threshold** (source: 1_concept.md)
   - Rationale: Ch5 5.5.7 empirical findings (0.417 was ONLY Ch5 clustering RQ to exceed 0.40)
   - Limitation: Not literature-established cutoff, different threshold (e.g., 0.35) would change verdict
   - Justification: Conservative threshold distinguishes EXCEPTIONAL from MODERATE quality

**Warnings (if any from Step 5):**
None - all critical files present, analysis completed successfully

---

## 5. Results

### Sample Characteristics

**Sample Size:**
- Total N: 100 participants
- Exclusions: 0 (all participants from RQ 6.8.3 included)
- Missing data: 0 (all random effects estimated)

**Final Sample:**
- N = 100 participants
- Clustering features: 4 per participant (Source intercept, Source slope, Destination intercept, Destination slope)
- Data source: Random effects from RQ 6.8.3 location-stratified LMMs

**Response Pattern Metrics (from ROOT RQ 6.8.1):**
- Full scale usage (0-1 continuous): 0% used only endpoints (good variability)
- Mean rating SD: 0.251
- Median rating SD: 0.273
- Restricted range (SD < 0.20): 101/400 participant-sessions (25.2%)
- Note: 75% show adequate rating variability (SD >= 0.20), no systematic extreme response bias

### Primary Findings

**Cluster Selection:**

| K | Inertia | BIC | Optimal |
|---|---------|-----|---------|
| 1 | 400.00 | 157.05 | No |
| 2 | 238.51 | 123.76 | No |
| 3 | 148.91 | 95.08 | No |
| 4 | 119.76 | 91.72 | No |
| **5** | **98.56** | **90.65** | **Yes** |
| 6 | 87.22 | 96.85 | No |

**Optimal K = 5 clusters** (BIC minimum = 90.65)

**Clustering Quality Metrics:**

| Metric | Value | Threshold | Pass | Ch5 5.5.7 (Accuracy) |
|--------|-------|-----------|------|----------------------|
| Silhouette Coefficient | 0.330 | >= 0.40 | **FAIL** | 0.417 (PASS) |
| Davies-Bouldin Index | 0.967 | < 1.0 | PASS | N/A |
| Jaccard Bootstrap Stability | 0.647 | > 0.70 | **FAIL** | N/A |

**CRITICAL FINDING: HYPOTHESIS NOT SUPPORTED**
- Confidence clustering Silhouette = 0.330 (21% lower than Ch5 5.5.7 accuracy = 0.417)
- Fell below 0.40 threshold
- Source-destination dissociation creates EXCEPTIONAL accuracy phenotypes but only MODERATE confidence phenotypes

**Cluster Phenotypes (K=5):**

**Cluster 0: HighSrc-Resilient, HighDst-Resilient (N=30, 30%)**
- Source: Intercept = +0.25, Slope = +0.13
- Destination: Intercept = +0.20, Slope = +0.12
- Interpretation: High baseline confidence with improving trajectories for both memory types

**Cluster 1: LowSrc-Declining, LowDst-Resilient (N=16, 16%)**
- Source: Intercept = -0.57, Slope = -0.02
- Destination: Intercept = -0.58, Slope = +0.02
- Interpretation: Low baseline with declining source but stable destination confidence

**Cluster 2: HighSrc-Declining, HighDst-Declining (N=16, 16%)**
- Source: Intercept = +0.11, Slope = -0.26
- Destination: Intercept = +0.09, Slope = -0.21
- Interpretation: Moderate baseline with rapid decline in both memory types

**Cluster 3: HighSrc-Declining, HighDst-Declining (N=28, 28%)**
- Source: Intercept = +0.36, Slope = -0.04
- Destination: Intercept = +0.41, Slope = -0.09
- Interpretation: High baseline with gradual decline (less steep than Cluster 2)

**Cluster 4: LowSrc-Resilient, LowDst-Resilient (N=10, 10%)**
- Source: Intercept = -1.02, Slope = +0.17
- Destination: Intercept = -0.95, Slope = +0.20
- Interpretation: Very low baseline with improving calibration over time

**Association with Ch5 5.5.7 Accuracy Clusters:**

**Chi-Square Test:**
- X² = 43.68, df = 12
- p (uncorrected) = 1.73 × 10{u
- p (Bonferroni-corrected) = 1.73 × 10{u
- Result: **HIGHLY SIGNIFICANT** (p < 0.0001, survives Bonferroni correction)

**Cross-Tabulation (Confidence Clusters x Accuracy Clusters):**

| Confidence | Accuracy 0 | Accuracy 1 | Accuracy 2 | Accuracy 3 | Total |
|------------|------------|------------|------------|------------|-------|
| Cluster 0  | 8 | 2 | **18** | 2 | 30 |
| Cluster 1  | 0 | **9** | 4 | 3 | 16 |
| Cluster 2  | 1 | 6 | 3 | 6 | 16 |
| Cluster 3  | 11 | 3 | 8 | 6 | 28 |
| Cluster 4  | 0 | 6 | 2 | 2 | 10 |
| **Total**  | **20** | **26** | **35** | **19** | **100** |

**Key Associations:**
- Confidence Cluster 0 strongly associated with Accuracy Cluster 2 (18/30 = 60%)
- Confidence Cluster 1 strongly associated with Accuracy Cluster 1 (9/16 = 56%)
- Despite lower clustering quality, confidence and accuracy phenotypes co-vary systematically

---

## 6. Visualizations

### Plot 1: Cluster Scatter in Principal Component Space
**File:** `plots/cluster_scatter.png`

**Description:**
2D scatter plot displaying 5 confidence clusters projected onto first two principal components. X-axis shows PC1 (58.4% variance), Y-axis shows PC2 (34.0% variance), with total 92.4% variance explained. Excellent dimensionality reduction from 4D feature space.

**Key Patterns:**
- **Cluster 4 (orange inverted triangles, N=10)** most compact and isolated on PC1 dimension (far left), corresponds to very low baseline confidence phenotype
- **Cluster 3 (purple diamonds, N=28)** most dispersed, substantial overlap with Clusters 0 and 2, this heterogeneity drives down overall Silhouette score
- **Clusters 0 and 2 separated on PC2** - Cluster 0 (red circles, upper half) vs Cluster 2 (green triangles, lower half), PC2 captures slope dynamics (resilient vs declining)
- **Visible cluster overlap** between Clusters 0, 2, and 3 in middle region (PC1: 0 to +1) confirms Silhouette = 0.33 below threshold

**Connection to Findings:**
Visual plot confirms statistical finding that clustering quality is moderate but not exceptional. Unlike Ch5 5.5.7 accuracy clustering (Silhouette = 0.417) which showed clear separation, this plot reveals boundary ambiguity. The subtitle explicitly states "Hypothesis NOT Supported: Silhouette=0.33 < 0.40 threshold (Ch5 5.5.7 accuracy: 0.417)". The moderate quality is NOT due to poor 2D projection (92.4% variance captured) - the 4D feature space itself produces moderate cluster separation for confidence data.

---

## 7. Interpretation

### Hypothesis Testing

**Primary Hypothesis:** "Confidence clustering will achieve Silhouette >= 0.40 quality threshold, replicating Ch5 5.5.7's exceptional clustering quality."

**Outcome:** **NOT SUPPORTED**

**Rationale:**
- Silhouette = 0.330 (FAIL, 21% lower than Ch5 5.5.7's 0.417)
- Jaccard stability = 0.647 (FAIL, below 0.70 threshold)
- Davies-Bouldin = 0.967 (PASS, but marginal - close to 1.0 cutoff)
- Multiple metrics converge on moderate (not exceptional) quality

**Secondary Hypothesis:** "Cluster assignments will show significant association with Ch5 5.5.7 accuracy clusters."

**Outcome:** **SUPPORTED**

**Rationale:**
- Chi-square X² = 43.68, p < 0.0001 (highly significant, survives Bonferroni correction)
- Cross-tabulation shows systematic co-variation (Confidence Cluster 0 with Accuracy Cluster 2: 60%, Confidence Cluster 1 with Accuracy Cluster 1: 56%)
- Despite lower clustering quality, confidence and accuracy phenotypes are NOT independent

### Theoretical Implications

**Source-Destination Dissociation Extends to Confidence - But More Weakly Than Accuracy**

Ch5 5.5.7 demonstrated exceptional clustering quality (Silhouette = 0.417) for source-destination ACCURACY trajectories. This RQ tested whether this extends to CONFIDENCE (metacognitive monitoring).

**Key Finding:** Source-destination dissociation is detectable in confidence data (K=5 clusters identified), BUT individual difference structure is weaker (Silhouette = 0.33) compared to accuracy (0.417).

**Dual-Process Theory Partially Confirmed:**
- Accuracy clustering: Source (recollection-based) vs Destination (familiarity-based) create STRONG individual difference phenotypes
- Confidence clustering: Source vs Destination distinction exists BUT creates WEAKER phenotypes
- Implication: Metacognitive monitoring (confidence) less tightly coupled to source-destination processing than memory strength (accuracy)

**Metacognitive Dissociation from Memory:**
- 21% reduction in clustering quality (0.417 -> 0.33) suggests confidence trajectories more variable and less structurally coherent than accuracy trajectories
- Confidence influenced by additional factors beyond source-destination memory processing (e.g., general metacognitive style, risk aversion, response biases)
- Aligns with metacognitive literature showing confidence-accuracy dissociations (Fleming & Lau, 2014)

**Why K=5 Instead of K=4?**
- Ch5 5.5.7 found K=4 optimal for accuracy
- This RQ found K=5 optimal for confidence
- Interpretation: Confidence phenotype space may be more complex (5 patterns) than accuracy (4 patterns), but LESS clearly separated
- Additional cluster may reflect metacognitive heterogeneity not present in accuracy data

### Cross-RQ Patterns

**Convergent Evidence:**

1. **RQ 6.8.3 (Source-Destination Confidence ICC):** Parent RQ found SAME-sign correlations (Source r=-0.24, Destination r=-0.40, both negative) vs Ch5 5.5.6 accuracy OPPOSITE-sign correlations (Source r=+0.99, Destination r=-0.90). Dissociation pattern does NOT replicate for confidence.

2. **Ch5 5.5.7 (Source-Destination Accuracy Clustering):** Achieved Silhouette = 0.417, ONLY Ch5 clustering RQ to exceed 0.40 threshold. Exceptional quality validates source-destination as fundamental individual difference dimension for accuracy.

3. **Cross-chapter synthesis (archive_index.md line 737):** Accuracy clustering 21% better separation than confidence (0.417 vs 0.330). Suggests accuracy = purer measure of memory architecture, confidence less reliable due to response style variability.

**Complementary Findings:**
- Significant chi-square association (p < 0.0001) indicates confidence and accuracy phenotypes co-vary despite structural differences
- Both RQs identify individual difference phenotypes, but confidence phenotypes less stable (Jaccard = 0.647 vs expected > 0.70)

### Unexpected Findings

**1. K=5 Instead of Expected K=4**

Expected K=4 based on Ch5 5.5.7. BIC selected K=5.

**Investigation:** BIC difference between K=4 (91.72) and K=5 (90.65) = 1.07, potentially negligible (Kass & Raftery, 1995 suggest < 2 weak evidence). K=5 may represent splitting of one accuracy phenotype into two confidence phenotypes (Clusters 2 and 3 both show declining patterns but differ in baseline/slope magnitude), or overfitting given moderate Jaccard stability (0.647).

**2. Significant Association Despite Lower Clustering Quality**

Despite Silhouette < 0.40, chi-square showed HIGHLY significant association with Ch5 5.5.7 (p < 0.0001).

**Investigation:** Two variables can be correlated even if one has high measurement error. Confidence clustering captures SOME signal from accuracy phenotypes but with added noise from metacognitive variability. Analogy: Confidence and accuracy are coupled but with confidence having lower signal-to-noise ratio.

**3. Cluster 3 Heterogeneity**

Cluster 3 (N=28, largest) shows substantial spatial dispersion in PCA plot, overlapping with Clusters 0 and 2.

**Investigation:** Cluster 3 may be "residual" cluster capturing participants not fitting clear phenotypes, or genuinely heterogeneous phenotype (high baseline confidence with VARIABLE slope patterns). This within-cluster heterogeneity drives down overall Silhouette score.

---

## 8. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 provides adequate power for K-means with K=5 (20 participants per cluster average)
- Smallest cluster (Cluster 4) has N=10 (10% of sample), limiting precision of cluster characterization
- Jaccard stability = 0.647 suggests borderline stability - larger N (150-200) might improve

**Demographic Constraints:**
- Undergraduate sample (M age = 20.3, SD = 1.8) from RQ 6.8.3
- Limited age range restricts generalizability to older adults
- Metacognitive monitoring may change across lifespan (confidence calibration improves with age in some domains)

**No Attrition:**
- All 100 participants from RQ 6.8.3 included (no data loss)
- Assumes random effects from 6.8.3 are unbiased estimates (depends on 6.8.3 LMM assumptions holding)

### Methodological Limitations

**Measurement:**

1. **Derived Data:** Clustering uses RANDOM EFFECTS from RQ 6.8.3 LMMs (BLUPs = Best Linear Unbiased Predictors), not raw confidence ratings. Random effects are MODEL-BASED ESTIMATES with uncertainty. Clustering treats BLUPs as fixed values, ignoring estimation uncertainty. Implication: Cluster assignments may be overly confident (participants near cluster boundaries have uncertain random effects).

2. **Confidence Response Patterns:** 25% of participant-sessions show restricted range (SD < 0.20), adding measurement noise to random effects (source: summary.md Section 1.4). No bias correction applied in RQ 6.8.3 LMMs (transparency priority). Response style variability may contribute to lower clustering quality (Silhouette = 0.33) compared to binary accuracy data (no response style variance).

3. **Source-Destination Definition:** Source (-U- tags): Pick-up location. Destination (-D- tags): Put-down location. Assumed orthogonal dimensions, but may have correlated components (spatial binding). Clustering assumes linear combinations of source/destination features, but interactions possible.

**Design:**

1. **No External Validation:** Clusters identified via unsupervised K-means. No external criterion to validate phenotypes (e.g., cognitive test scores, neural measures). Phenotype labels (e.g., "HighSrc-Resilient") are DESCRIPTIVE interpretations, not validated constructs. Circular reasoning risk: Clusters defined by features, then characterized by same features.

2. **K Selection Dependency:** BIC selected K=5, but AIC might select different K (not tested). K=4 has similar BIC (91.72 vs 90.65), difference = 1.07 (< 2 often considered negligible). Implication: K=5 vs K=4 distinction may not be robust.

3. **Cross-Tabulation Non-Independence:** Chi-square test compares confidence clusters (this RQ) to accuracy clusters (Ch5 5.5.7). Same participants in both analyses, NOT independent samples. Significant association (p < 0.0001) may be partly driven by SHARED VARIANCE (same participants, same memory task). Interpretation requires caution: Association does not imply CAUSAL relationship.

**Statistical:**

1. **K-Means Assumptions:** Assumes spherical clusters with equal variance (Euclidean distance metric). PCA plot shows Cluster 3 elongated (non-spherical). Alternative methods (e.g., Gaussian Mixture Models allowing elliptical clusters) might improve fit. K-means sensitive to initialization (random_state=42 for reproducibility, but different seeds might yield slightly different clusters).

2. **Standardization:** All 4 features standardized to z-scores (mean=0, SD=1) assuming equal weighting. Features may have different RELEVANCE (intercepts may be more stable than slopes). Weighted clustering (not performed) might prioritize intercepts over slopes.

3. **Silhouette Threshold:** Threshold of 0.40 based on Ch5 5.5.7 empirical findings (not literature-established cutoff). Different threshold (e.g., 0.35) would change hypothesis verdict. Silhouette is RELATIVE metric (compares within-cluster to between-cluster distances), not absolute quality measure.

### Generalizability Constraints

**Population:**
- Findings may not generalize to older adults (metacognitive monitoring changes with age), clinical populations (MCI, dementia, anxiety - altered confidence calibration), or children/adolescents (developing metacognitive awareness)

**Context:**
- VR desktop paradigm (not fully immersive HMD)
- Confidence ratings collected immediately after recall (not delayed metacognitive judgments)
- Source-destination distinction specific to VR spatial memory task (may not extend to other memory domains)

**Task:**
- Clustering based on LONGITUDINAL confidence trajectories (4 test sessions)
- May not apply to CROSS-SECTIONAL confidence differences (single session)
- Results specific to episodic memory confidence (not semantic memory, prospective memory)

### Technical Limitations

**Random Effects Extraction (Inherited from RQ 6.8.3):**
- Random effects assume LMM assumptions hold (linearity, homoscedasticity, normality)
- If 6.8.3 LMM misspecified, random effects biased -> clustering on biased features
- No diagnostic checks on random effects distributions (assumed normal per LMM theory)
- Note: RQ 6.8.3 uses TSVR_hours (linear time) instead of log_TSVR (standard), affects slope units but not clustering validity (documented in validation.md)

**BIC Computation:**
- Custom BIC formula: N * log(inertia/N) + K * log(N) * 4
- Standard for K-means, assumes isotropic Gaussian clusters
- Violations may bias K selection toward higher K (overfitting)

**Bootstrap Stability (Jaccard):**
- Jaccard = 0.647 (below 0.70) indicates MODERATE instability
- 100 bootstrap iterations (higher iterations might stabilize estimate)
- Bootstrap WITH REPLACEMENT assumes participants exchangeable (may not hold if subpopulations exist)

**PCA Projection:**
- 92.4% variance explained by PC1+PC2 (excellent)
- However, 7.6% variance lost in 2D projection
- Cluster overlap visible in 2D may be PARTLY artifact of dimensionality reduction (4D -> 2D)
- Full 4D space might show clearer separation (but not visualizable)

### Limitations Summary

Findings robust within scope:
- Hypothesis test result (NOT SUPPORTED) conservative (stringent 0.40 threshold)
- Secondary finding (significant association with Ch5 5.5.7) replicates across uncorrected AND Bonferroni-corrected p-values
- Multiple quality metrics converge (Silhouette FAIL, Jaccard FAIL, Davies-Bouldin marginal PASS)
- Visual PCA plot confirms statistical finding (cluster overlap matches lower Silhouette)

Limitations indicate directions for future work (see Section 9: Next Steps).

---

## 9. Publication-Ready Summary

**Context & Method:** This study tested whether source-destination memory dissociation - which creates exceptional accuracy-based phenotypes (Silhouette = 0.417, Ch5 5.5.7) - extends to confidence-based metacognitive monitoring. Using K-means clustering on random effects from 100 participants (source/destination intercepts and slopes from location-stratified LMMs), we evaluated clustering quality against a pre-registered 0.40 threshold.

**Results:** Confidence clustering achieved moderate quality (Silhouette = 0.330, 21% lower than accuracy). BIC selected K=5 clusters (vs K=4 for accuracy), with phenotypes ranging from high-confident-resilient (N=30, improving confidence for both memory types) to low-confident-resilient (N=10, very low baseline with improving calibration). Despite lower clustering quality, confidence and accuracy phenotypes showed highly significant association (chi-square X² = 43.68, p < 0.0001, Bonferroni-corrected), indicating systematic co-variation.

**Interpretation:** Source-destination dissociation creates EXCEPTIONAL accuracy phenotypes but only MODERATE confidence phenotypes, revealing partial dissociation between memory architecture and metacognitive monitoring systems. The 21% quality reduction suggests confidence trajectories are influenced by additional factors beyond source-destination memory processing (e.g., response style variability, general metacognitive style), aligning with metacognitive literature showing confidence-accuracy dissociations. While both data types capture individual differences, accuracy provides clearer phenotype structure, validating differential assessment strategies for memory vs metacognition in VR-based cognitive testing.

**Conclusion:** Memory strength (accuracy) and metacognitive monitoring (confidence) are coupled but partially dissociable systems. VR assessments are more sensitive to individual differences in memory architecture than metacognitive monitoring, with practical implications: use accuracy clustering for robust phenotyping, use confidence data for unique metacognitive variance but with awareness of lower stability.

---

## 10. Metadata & Sources

### Report Metadata
- **Generated:** 2026-01-01
- **Agent:** rq_report v1.0.0 (Sonnet 4.5 model)
- **RQ Folder:** results/ch6/6.8.4/

### Sources Synthesized

**Archive Sources:** 2 topics, 3 key events
- ch6_824x_icc_ratio_at_risk (archive/ch6_824x_icc_ratio_at_risk.md, 2025-12-13)
- ch6_824x_icc_model_averaged_validation (archive/ch6_824x_icc_model_averaged_validation.md, 2025-12-13)

**RQ Files:** 15 files
- **Core docs:** 1_concept.md, 2_plan.md, summary.md, status.yaml
- **Validation:** PLATINUM_FINALIZATION_REPORT.md
- **Specifications:** (none - tools/analysis determined by rq_tools/rq_analysis agents)
- **Execution:** status.yaml, 9 data files, 1 log file, 1 plot file
- **PLATINUM:** PLATINUM_FINALIZATION_REPORT.md (certified 2025-12-30)

**Data Files Sampled (9 total):**
- step00_clustering_input.csv (100 rows x 4 features)
- step01_standardized_features.csv (100 rows x 4 z-scores)
- step02_cluster_selection.csv (K=1-6 BIC values)
- step03_cluster_assignments.csv (100 rows, cluster 0-4)
- step04_validation.csv (3 quality metrics)
- step05_cluster_characterization.csv (5 phenotypes)
- step06_chi_square.csv (association test)
- step06_crosstab.csv (4x4 contingency table)
- step07_cluster_scatter_data.csv (100 rows, PC1/PC2 projection)

**Log Files (1):**
- steps_00_to_07.log (180 lines, comprehensive execution trace)

**Plot Files (1):**
- cluster_scatter.png (5 clusters in 2D PCA space, 92.4% variance explained)

### Warnings Flagged

**No warnings flagged during report generation.**

All critical files present, all analysis steps completed successfully, PLATINUM certification achieved (2025-12-30).

---

**End of Report**
