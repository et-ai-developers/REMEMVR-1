# RQ 6.8.4: Source-Destination Confidence Clustering

**Chapter:** 6
**Type:** Source-Dest Confidence
**Subtype:** Clustering
**Full ID:** 6.8.4

---

## Research Question

**Primary Question:**
Does confidence clustering for source-destination memory replicate the strong 4-cluster structure found for accuracy in Ch5 5.5.7?

**Scope:**
This RQ examines individual differences in confidence trajectories for source (-U- pick-up location) and destination (-D- put-down location) memory. Using random effects (intercepts and slopes) from RQ 6.8.3, K-means clustering identifies participant phenotypes based on 4 features: source intercept, source slope, destination intercept, destination slope. N=100 participants × 4 clustering features. Critical comparison to Ch5 5.5.7, which was the ONLY accuracy clustering RQ to achieve Silhouette >= 0.40 quality threshold (0.417 for 4 clusters).

**Theoretical Framing:**
Ch5 5.5.7 demonstrated exceptional clustering quality for source-destination accuracy trajectories, suggesting source-destination dissociation captures fundamental individual differences in spatial memory processing. If confidence clustering also achieves good quality (Silhouette >= 0.40), this validates that source-destination is genuinely special for individual differences in both memory AND metacognition. If confidence clustering is poor (Silhouette < 0.40 like other Ch5 clustering RQs), source-destination may be special only for accuracy, not confidence.

---

## Theoretical Background

**Relevant Theories:**
- **Source-Destination Dissociation (Ch5 5.5 Findings):** Source (pick-up location, where initial object encoding occurs) shows slower decay and regression-to-mean pattern. Destination (put-down location, automatic motor memory) shows faster decay and fan-effect pattern. These fundamentally different forgetting dynamics may create distinct individual difference phenotypes.

- **Dual-Process Theory (Yonelinas, 2002):** Source memory may rely more on recollection (explicit encoding of pick-up context), while destination may rely more on familiarity (automatic motor memory of put-down action). Different retrieval processes may create different metacognitive signatures.

- **Working Memory Capacity:** High WM capacity individuals may show better source memory (controlled encoding) but similar destination memory (automatic encoding), creating interaction patterns.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If confidence clustering achieves Silhouette >= 0.40 (matching or exceeding Ch5 5.5.7's 0.417), source-destination dissociation reflects fundamental individual differences in both memory and metacognition. If confidence clustering is poor, source-destination dissociation may be specific to accuracy (memory strength) but not metacognitive monitoring.

**Literature Gaps:**
Ch5 5.5.7 was the only clustering RQ with good quality, but that was for accuracy data. Unknown whether source-destination dissociation extends to confidence (metacognitive monitoring) or is specific to memory traces. This RQ directly tests generalization across data types (5-level ordinal confidence vs binary accuracy).

---

## Hypothesis

**Primary Hypothesis:**
Confidence clustering for source-destination memory will achieve Silhouette >= 0.40 quality threshold, replicating Ch5 5.5.7's exceptional clustering quality. BIC will select K=4 clusters (matching Ch5). If achieved, this validates that source-destination dissociation captures fundamental individual differences that extend beyond accuracy to metacognitive monitoring.

**Secondary Hypotheses:**
(1) Cluster assignments will show significant association with Ch5 5.5.7 accuracy cluster assignments (chi-square p < 0.05), indicating confidence and accuracy phenotypes align for source-destination memory.

(2) If clustering quality is poor (Silhouette < 0.40), source-destination dissociation may be specific to memory strength (accuracy) and not extend to metacognitive confidence. This would suggest different underlying mechanisms for accuracy vs confidence trajectories.

**Theoretical Rationale:**
Ch5 5.5.7 found opposite intercept-slope correlations (Source r=+0.99 regression to mean, Destination r=-0.90 fan effect), creating rich multivariate structure ideal for clustering. RQ 6.8.3 tests whether these opposite patterns replicate in confidence. If they do, same multivariate structure should produce good clustering. Additionally, 5-level ordinal confidence data provides 2.3× more information per response than binary accuracy, which may enhance clustering quality.

**Expected Effect Pattern:**
- BIC minimum at K=4 clusters (matching Ch5 5.5.7)
- Silhouette >= 0.40 (exceeding typical 0.30 threshold, matching Ch5 0.417)
- Davies-Bouldin < 1.0 (good separation)
- Jaccard bootstrap stability > 0.70 (robust clusters)
- Chi-square association with Ch5 5.5.7 clusters: p < 0.05
- Cluster size distribution similar to Ch5 (all clusters >= 10% of N=100)

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT examined in this RQ

- [x] **Where** (Spatial Location)
  - [x] `-U-` tags (pick-up location / source)
  - [x] `-D-` tags (put-down location / destination)
  - [ ] `-L-` tags (general location, legacy - NOT examined)
  - Disambiguation: This RQ focuses EXCLUSIVELY on source-destination dissociation. Source (-U-) = where participant picked up object (initial encoding context). Destination (-D-) = where participant put down object (motor memory endpoint). Legacy -L- tags excluded.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT examined in this RQ

**Inclusion Rationale:**
Source-destination dissociation is the focus of Type 6.8 RQs. This RQ extends Ch5 5.5 findings to confidence data. Only -U- and -D- tags are examined because these capture the theoretically-motivated distinction between encoding context (source) and motor endpoint (destination). General -L- tags are ambiguous and excluded.

**Exclusion Rationale:**
What (-N-) and When (-O-) domains are excluded because this RQ focuses on spatial memory dissociation within the Where domain. Type 6.3 RQs examine confidence across all three WWW domains. This RQ is specific to source-destination within Where domain only.

---

## Analysis Approach

**Analysis Type:**
K-means clustering on random effects from Linear Mixed Models (LMMs). Unsupervised machine learning for participant phenotype identification.

**High-Level Workflow:**

**Step 0:** Load random effects from RQ 6.8.3 (source and destination intercepts and slopes for N=100 participants, total 4 features per participant = 200 rows from 6.8.3, but restructured to 100 rows × 4 columns for clustering).

**Step 1:** Standardize all 4 features to z-scores (mean=0, SD=1) to ensure equal weighting in clustering algorithm. Features: Source_intercept, Source_slope, Destination_intercept, Destination_slope.

**Step 2:** K-means cluster selection using BIC (Bayesian Information Criterion) for K=1 to K=6 clusters. Identify optimal K via BIC minimum. Expect K=4 based on Ch5 5.5.7 findings.

**Step 3:** Fit final K-means clustering with optimal K using random seed=42 for reproducibility.

**Step 4:** Validate clustering quality using three metrics: (1) Silhouette coefficient (threshold >= 0.40 for good quality), (2) Davies-Bouldin index (< 1.0 for good separation), (3) Jaccard bootstrap stability (> 0.70 for robust clusters, 100 bootstrap iterations).

**Step 5:** Characterize clusters: Compute mean feature values per cluster, identify phenotypes (e.g., "High Source Resilient", "Fast Destination Decliners", etc.). Compare to Ch5 5.5.7 cluster characterizations.

**Step 6:** Cross-tabulate confidence cluster assignments (this RQ) with Ch5 5.5.7 accuracy cluster assignments. Compute chi-square test of association to determine if confidence and accuracy phenotypes align.

**Step 7:** Compare clustering quality metrics to Ch5 5.5.7 (Silhouette=0.417, K=4) and other Ch5 clustering RQs (5.1.5, 5.2.7, 5.3.8, 5.4.5, all Silhouette < 0.40). Determine if source-destination is genuinely special across data types.

**Step 8:** Generate scatter plots of cluster assignments in 2D principal component space and 4D feature space visualizations.

**Expected Outputs:**
- data/step01_standardized_features.csv (100 rows × 4 columns: standardized source/destination intercepts and slopes)
- results/step02_cluster_selection.csv (K=1-6 rows with BIC values, optimal K identified)
- data/step04_cluster_assignments.csv (100 rows: UID + cluster label)
- results/step05_validation.csv (clustering quality metrics: Silhouette, Davies-Bouldin, Jaccard)
- results/step06_ch5_comparison.csv (comparison to Ch5 5.5.7 quality metrics and other Ch5 clustering RQs)
- results/step07_crosstab.csv (cross-tabulation of confidence vs accuracy cluster assignments + chi-square test)
- plots/step08_cluster_scatter.png (visualization of clusters in PC space)

**Success Criteria:**
- Standardization correct: all features mean=0, SD=1 (+/- 0.01)
- BIC values finite for all K=1-6
- Optimal K identified (expect K=4 based on Ch5 5.5.7)
- All cluster sizes >= 10% of N=100 (no tiny clusters)
- Silhouette computed (compare to 0.40 threshold and Ch5 5.5.7's 0.417)
- Davies-Bouldin and Jaccard computed
- Cross-tabulation with Ch5 5.5.7 complete (100 participants matched)
- Chi-square test executed with p-value reported
- Comparison table includes all Ch5 clustering RQs (5.1.5, 5.2.7, 5.3.8, 5.4.5, 5.5.7) for context

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.8.3 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 6.8.3 (Source-Destination Confidence ICC)

**File Paths:**
- results/ch6/6.8.3/data/step04_random_effects.csv (200 rows: 100 participants × 2 location types, with random intercepts and slopes per participant-location combination)

**Note on Data Structure:**
RQ 6.8.3 outputs 200 rows (100 participants × 2 location types), with each participant having separate random effects for source and destination. For clustering, this must be reshaped to 100 rows × 4 columns: Source_intercept, Source_slope, Destination_intercept, Destination_slope. Step 0 handles this reshaping.

**Additional Dependencies:**
- Ch5 5.5.7 cluster assignments for cross-tabulation (results/ch5/5.5.7/data/step04_cluster_assignments.csv)

**Dependencies:**
RQ 6.8.3 must complete Step 4 (random effects extraction) before this RQ can run. Specifically, 6.8.3 must fit location-stratified LMMs with random intercepts and slopes, and extract variance components and random effects per participant per location type.

Ch5 5.5.7 must be complete for cross-tabulation comparison.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 6.8.3 (inherited inclusion criteria)
- No exclusions

**Items:**
- N/A (clustering uses participant-level random effects, not item-level data)

**Tests:**
- N/A (random effects aggregate across all 4 tests, capturing overall trajectory patterns)

---
