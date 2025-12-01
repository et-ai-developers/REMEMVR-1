# RQ 5.4.7: Schema-Based Clustering

**Chapter:** 5
**Type:** Congruence
**Subtype:** Schema-Based Clustering
**Full ID:** 5.4.7

---

## Research Question

**Primary Question:**
Can participants be grouped into latent classes based on congruence-specific forgetting trajectories (intercepts and slopes for Common, Congruent, and Incongruent items)?

**Scope:**
This RQ examines individual differences in schema congruence effects by clustering N=100 participants based on 6 clustering variables: intercept and slope for each of the three congruence levels (Common, Congruent, Incongruent). Random effects are extracted from RQ 5.4.6 variance decomposition analysis. Cluster number (K) determined empirically via BIC model selection testing K=1 to K=6 profiles.

**Theoretical Framing:**
Exploratory analysis to identify latent subgroups with distinct schema-congruence memory profiles. May reveal individuals who show schema-selective impairment (e.g., poor memory specifically for schema-violating incongruent items but preserved memory for schema-consistent congruent items), or individuals who show uniform memory performance across all congruence levels. Clustering approach complements population-level analyses by identifying heterogeneous response patterns masked by group averages.

---

## Theoretical Background

**Relevant Theories:**
- **Schema Theory:** Individuals vary in their ability to utilize schema-based encoding and retrieval support. Some individuals may show strong schema effects (large differences between congruent and incongruent items), while others may show weak schema effects (similar performance across all congruence levels). These individual differences may reflect differences in schema knowledge, strategic encoding, or reliance on schema-based vs item-specific processing.
- **Individual Differences in Episodic Memory:** Forgetting trajectories show stable trait-like individual differences (established in RQ 5.1.4 and RQ 5.4.6). Clustering based on congruence-specific trajectories extends this by examining whether individual differences are uniform across congruence levels or whether some individuals show congruence-selective patterns.

**Key Citations:**
To be added by rq_scholar

**Theoretical Predictions:**
Exploratory analysis with no directional predictions. Possible outcomes include:
1. **Uniform Profiles:** Clusters differentiated by overall memory ability (high/average/low) but similar congruence effects within each cluster
2. **Schema-Selective Profiles:** Clusters showing differential congruence effects (e.g., Cluster A has strong congruence benefit, Cluster B has weak congruence benefit)
3. **Item-Type Specific Profiles:** Clusters with selective impairment for specific congruence categories (e.g., poor memory only for incongruent items, preserved memory for common and congruent items)

**Literature Gaps:**
To be identified by rq_scholar

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis. Expected 2-4 latent profiles based on 6 clustering variables (Common_Intercept, Common_Slope, Congruent_Intercept, Congruent_Slope, Incongruent_Intercept, Incongruent_Slope). Number of profiles determined empirically by BIC model selection.

**Secondary Hypotheses:**
Profiles may show schema-selective patterns such as:
- Poor memory for schema-violating items only (low Incongruent intercept, steep Incongruent slope, but preserved Common and Congruent performance)
- Strong schema benefit (large differences between Congruent and Incongruent intercepts/slopes)
- Weak schema benefit (similar intercepts/slopes across all three congruence levels)

**Theoretical Rationale:**
Individual differences in schema utilization suggest that not all participants benefit equally from schema congruence. Some individuals may show strong schema effects (large congruence benefit), while others show weak schema effects (minimal congruence differences). Clustering reveals these heterogeneous patterns, which may be obscured in population-level analyses that assume homogeneous congruence effects.

**Expected Effect Pattern:**
- Optimal K determined by BIC minimum (lowest BIC value among K=1 to K=6)
- Cluster sizes balanced (no cluster < 10% of sample to ensure interpretability)
- Cluster centers show interpretable patterns (e.g., differentiation on intercepts vs slopes, or differentiation on specific congruence levels)
- Within-cluster variance lower than between-cluster variance (clustering solution captures meaningful individual differences)

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity/naming items included in congruence analysis (inherited from RQ 5.4.1)

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags included in congruence analysis (inherited from RQ 5.4.1)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order/sequence items included in congruence analysis (inherited from RQ 5.4.1)

**Inclusion Rationale:**
All three WWW domains (What/Where/When) are included via RQ 5.4.1 data source. Congruence manipulation (Common i1/i2, Congruent i3/i4, Incongruent i5/i6) applies across all domains. Clustering is performed on congruence-specific random effects (aggregated across domains), not domain-specific effects.

**Exclusion Rationale:**
None. This RQ does not stratify by domain; it focuses on congruence-level individual differences aggregated across all WWW domains.

---

## Analysis Approach

**Analysis Type:**
K-means clustering with BIC-based model selection

**High-Level Workflow:**

**Step 1:** Load random effects from RQ 5.4.6 variance decomposition
- Input: results/ch5/5.4.6/data/step04_random_effects.csv
- Variables: UID, Total_Intercept_Common, Total_Slope_Common, Total_Intercept_Congruent, Total_Slope_Congruent, Total_Intercept_Incongruent, Total_Slope_Incongruent
- Expected: N=100 participants x 6 clustering variables

**Step 2:** Standardize clustering features to z-scores
- Grand-mean center and scale to SD=1 for each of 6 variables
- Ensures equal weighting of intercept and slope features
- Prevents scale differences from dominating clustering solution
- Verify standardization: mean ~ 0, SD ~ 1 for all 6 features

**Step 3:** Test K=1 to K=6 cluster solutions using K-means
- Fit K-means for each K value (random_state=42, n_init=50 for stability)
- Compute inertia (within-cluster sum of squares)
- Compute BIC for each solution using inertia and sample size
- Select optimal K as BIC minimum

**Step 4:** Fit final K-means with optimal K
- Use K from Step 3 BIC selection
- Extract cluster assignments (100 participants)
- Extract cluster centers (K x 6 matrix in z-score space)
- Verify cluster sizes >= 10% of sample (no tiny clusters)

**Step 5:** Characterize clusters by congruence-specific patterns
- Compute mean intercept and slope per congruence level for each cluster
- Transform cluster centers back to original scale for interpretation
- Assign interpretive labels based on patterns (e.g., "High Common, Low Incongruent", "Uniform High", "Uniform Low")
- Identify key features differentiating clusters (intercepts vs slopes, specific congruence levels)

**Step 6:** Create scatter plot matrix colored by cluster membership
- Visualize 6-dimensional clustering solution via scatter plot matrix
- Color points by cluster assignment
- Overlay cluster centers as reference points
- Include marginal density plots to show cluster separation
- Verify visual separation matches statistical clustering

**Expected Outputs:**
- data/step00_random_effects_from_rq546.csv (100 rows, 7 columns: UID + 6 features)
- data/step01_standardized_features.csv (100 rows, 7 columns: UID + 6 z-scored features)
- results/step02_cluster_selection.csv (6 rows: K=1-6 with inertia and BIC)
- results/step03_optimal_k.txt (single value: optimal K)
- data/step04_cluster_assignments.csv (100 rows: UID, cluster)
- results/step04_cluster_centers.csv (K rows x 6 columns: cluster centers in z-score space)
- results/step05_cluster_characterization.txt (interpretive description of each cluster)
- plots/step06_cluster_scatter_matrix.png (scatter plot matrix visualization)

**Success Criteria:**
- Random effects loaded: 100 participants present, no missing values
- BIC minimum identified: clear BIC minimum within K=1-6 range (not at boundary)
- Cluster sizes balanced: no cluster < 10% of sample
- Cluster centers interpretable: clear differentiation patterns visible
- Congruence-specific interpretations: clusters show meaningful differences in schema-congruence profiles
- Replicability: random_state=42 ensures reproducible cluster assignments
- Cluster validation metrics meet quality thresholds (see below)

---

## Clustering Method Selection

### K-means vs Latent Profile Analysis (LPA) Justification

**Method Selected:** K-means clustering with BIC-based model selection (K=2-6)

**Justification for K-means over Latent Profile Analysis (LPA):**
1. **Exploratory Nature:** This analysis discovers patterns in schema-based individual differences, not testing a priori structural hypotheses. K-means is appropriate for exploratory pattern discovery.
2. **Interpretability:** K-means cluster centroids directly show mean intercepts and slopes per congruence level, facilitating clinical translation and theoretical interpretation.
3. **Computational Efficiency:** K-means supports rapid sensitivity analyses (varying K, subsampling) without computational burden of GMM estimation.
4. **Sample Size:** N=100 is at the lower bound for stable LPA estimation with 6 continuous indicators; K-means is more robust to small samples.
5. **No Mixture Assumptions:** K-means does not assume multivariate normality within clusters, which may be violated with congruence-specific random effects.

**Alternative Method Consideration:**
If K-means shows poor cluster quality metrics (silhouette < 0.40, instability > 0.25), Gaussian Mixture Models (GMM) will be tested as sensitivity analysis to assess whether soft clustering improves fit.

## Cluster Validation Metrics

### Quality Metrics
- **Silhouette Score:** Target ≥ 0.40 (acceptable cluster cohesion)
  - Range: -1 to +1; higher = better defined clusters
  - < 0.25 = no substantial structure; 0.25-0.50 = weak structure; 0.51-0.70 = reasonable structure; > 0.70 = strong structure
- **Davies-Bouldin Index:** Target < 1.5 (acceptable cluster separation)
  - Lower = better; measures ratio of within-cluster to between-cluster distances

### Stability Assessment
- **Bootstrap Resampling:** 100 iterations, 80% subsampling
- **Jaccard Index Threshold:** > 0.75 for stable clusters
- **Cross-Validation:** k-fold (k=5) stability assessment

### Cluster Size Constraint
Each cluster must contain ≥ 10% of sample (N ≥ 10) to ensure interpretability and avoid singleton clusters driven by outliers.

## Sphericity Assumption Check

K-means assumes spherical (isotropic) clusters. To validate:
1. **Visual Check:** Scatter plot matrix colored by cluster should show approximately circular (not elongated) clusters
2. **PCA Variance:** If first PC explains > 70% of variance, data may have dominant axis violating sphericity
3. **Remedial:** If elongated clusters detected, consider GMM with unconstrained covariance as sensitivity analysis

## If Cluster Quality Fails

If cluster validation metrics are poor (silhouette < 0.40, stability < 0.75):
1. Report metrics transparently
2. Interpret clusters as "tentative" patterns requiring replication
3. Consider: (a) Gaussian Mixture Model with flexible covariance, (b) hierarchical clustering for alternative structure, (c) reporting that schema-specific individual differences may not form discrete clusters
4. Theoretical conclusion: Individual differences in congruence-specific forgetting may be continuously distributed rather than clustered into discrete profiles

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.4.6 variance decomposition outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.4.6 (Schema-Specific Variance Decomposition)

**File Paths:**
- results/ch5/5.4.6/data/step04_random_effects.csv (300 rows: 100 UID x 3 congruence levels, with Total_Intercept and Total_Slope per congruence)

**Dependencies:**
RQ 5.4.6 must complete Step 4 (extract individual random effects per congruence level from congruence-stratified LMMs) before this RQ can run. RQ 5.4.6 depends on RQ 5.4.1 (congruence-specific IRT calibration and LMM trajectory fitting).

**Data Structure Expected:**
RQ 5.4.6 outputs random effects in long format (300 rows: 100 participants x 3 congruence levels). This RQ will reshape to wide format for clustering:
- Common_Intercept, Common_Slope (from congruence=Common rows)
- Congruent_Intercept, Congruent_Slope (from congruence=Congruent rows)
- Incongruent_Intercept, Incongruent_Slope (from congruence=Incongruent rows)

Result: 100 rows x 6 clustering variables per participant

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.4.6 (inherited inclusion criteria from RQ 5.4.1)
- Expected: N=100 participants with complete random effects for all 3 congruence levels

**Items:**
- N/A (random effects are participant-level aggregates, not item-level)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from RQ 5.4.1
- Random effects aggregate across all 4 tests via LMM random slopes

**Congruence Levels:**
- [x] Common (schema-neutral, i1/i2 items)
- [x] Congruent (schema-consistent, i3/i4 items)
- [x] Incongruent (schema-violating, i5/i6 items)

---
