# RQ 6.1.5: Trajectory Clustering

**Chapter:** 6
**Type:** Confidence
**Subtype:** Trajectory Clustering
**Full ID:** 6.1.5

---

## Research Question

**Primary Question:**
Do participants cluster into confidence phenotypes, and do they match accuracy phenotypes?

**Scope:**
This RQ examines individual differences in confidence decline trajectories using random effects (intercept and slope) extracted from the best-fitting LMM in RQ 6.1.4. Sample: N=100 participants, with 2 clustering features (random intercept and random slope) derived from 400 observations (100 participants × 4 tests). K-means clustering will identify 2-6 candidate cluster solutions, with optimal K selected via BIC.

**Theoretical Framing:**
Building on Ch5 5.1.5 (accuracy phenotypes: Resilient vs Vulnerable), this RQ tests whether confidence decline shows similar individual difference structure. If confidence and accuracy phenotypes align, it suggests an integrated memory-metacognition system. If they diverge, it suggests dissociable systems (e.g., good memory with poor metacognition, or vice versa). Critically, 5-level ordinal confidence data may reveal stronger clustering structure than dichotomous accuracy data.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory:** Individuals differ in metacognitive skill, which may manifest as stable individual differences (trait-like) in confidence trajectories. If confidence phenotypes exist, metacognitive monitoring is a stable trait.
- **Memory-Metacognition Integration:** If confidence and accuracy phenotypes match, suggests memory and metacognition are tightly coupled. If divergent, suggests dissociable systems (dual-process framework).
- **Measurement Sensitivity:** 5-level ordinal data provides approximately 2.3× more information per response than dichotomous data. If RQ 6.1.4 reveals detectable slope variance (ICC_slope > 0.10), clustering quality may exceed Ch5 accuracy clustering.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Expected 2-3 confidence profiles paralleling Ch5 5.1.5 Resilient vs Vulnerable phenotypes. If confidence and accuracy phenotypes match (high concordance in cross-tabulation), suggests integrated system. If divergent (low concordance), suggests dissociable memory-metacognition systems.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
K-means clustering will identify 2-3 distinct confidence phenotypes, paralleling Ch5 5.1.5 accuracy clusters (Resilient vs Vulnerable). Clustering quality (silhouette score) expected > 0.40 threshold, potentially exceeding Ch5 accuracy clustering due to richer 5-level ordinal data providing more variance to cluster.

**Secondary Hypotheses:**
1. **Integration Hypothesis:** If confidence and accuracy phenotypes match (chi-square test of association significant, p < 0.05), suggests integrated memory-metacognition system where good/poor memory corresponds to accurate/poor metacognitive monitoring.
2. **Dissociation Hypothesis:** If confidence and accuracy phenotypes diverge (non-significant association), suggests dissociable systems with potential patterns like: good memory + poor metacognition (underconfident), or poor memory + high confidence (overconfident/Dunning-Kruger).

**Theoretical Rationale:**
Individual differences in forgetting trajectories (if they exist) should manifest in both accuracy and confidence if metacognitive monitoring tracks memory state. Ch5 5.1.5 found modest clustering (silhouette likely < 0.40 due to dichotomous data limitations). If RQ 6.1.4 reveals higher ICC_slope for confidence vs accuracy, clustering structure should be stronger. Silhouette > 0.40 is threshold for acceptable cluster quality.

**Expected Effect Pattern:**
- BIC identifies optimal K (likely 2-3 clusters matching Ch5)
- Silhouette > 0.40 (acceptable quality, may exceed Ch5 due to 5-level data)
- Cluster sizes >= 10% (no trivial clusters)
- Chi-square test of association between confidence and accuracy cluster labels (test integration vs dissociation)
- If integrated: Concordance high (e.g., Resilient accuracy -> Resilient confidence)
- If dissociated: Off-diagonal cross-tabulation patterns (e.g., Resilient accuracy + Vulnerable confidence)

---

## Memory Domains

**Domains Examined:**

- [x] **All Domains Combined** (Omnibus)
  - Description: Single omnibus "All" factor aggregating all interactive paradigm items
  - Analysis inherits from RQ 6.1.1 -> RQ 6.1.4 pipeline
  - No domain-specific clustering (that would be RQ 6.3.4 ICC by Domain)

**Inclusion Rationale:**
This RQ clusters based on general confidence trajectory phenotypes, not domain-specific patterns. Uses omnibus "All" factor confidence estimates from RQ 6.1.1, following Ch5 5.1.5 structure (General type clustering on omnibus factor). Domain-specific clustering would require separate analysis with domain-stratified random effects.

**Exclusion Rationale:**
- Domain-specific clustering (What/Where/When) is out of scope for Type 6.1 (Confidence General)
- Paradigm-specific clustering (IFR/ICR/IRE) is out of scope
- Congruence-specific clustering is out of scope

---

## Analysis Approach

**Analysis Type:**
K-means clustering on random effects (intercept + slope) extracted from RQ 6.1.4

**High-Level Workflow:**

**Step 1:** Load random effects from RQ 6.1.4 (data/step04_random_effects.csv, 100 rows × 2 features: intercept, slope)

**Step 2:** Standardize features to z-scores (mean=0, SD=1) to equalize weighting of intercept and slope dimensions

**Step 3:** K-means clustering for K=1-6 candidate solutions, compute BIC for each K to select optimal cluster count

**Step 4:** Fit final K-means model with optimal K (seed=42 for reproducibility)

**Step 5:** Validate cluster quality using multiple metrics:
- Silhouette score (target > 0.40 threshold)
- Davies-Bouldin index (lower is better)
- Jaccard bootstrap stability (test cluster robustness)

**Step 6:** Characterize clusters: compute mean intercept and slope per cluster, interpret phenotypes (e.g., Resilient = high intercept + shallow slope, Vulnerable = low intercept + steep slope)

**Step 7:** Cross-tabulate confidence clusters (this RQ) with Ch5 5.1.5 accuracy clusters to test integration vs dissociation hypothesis

**Step 8:** Chi-square test of association between confidence and accuracy cluster labels (test if phenotypes match or diverge)

**Expected Outputs:**
- data/step01_standardized_features.csv (100 rows: UID, intercept_z, slope_z)
- results/step02_cluster_selection.csv (6 rows: K, BIC, optimal_flag)
- data/step04_cluster_assignments.csv (100 rows: UID, cluster_label)
- results/step05_validation.csv (silhouette, Davies-Bouldin, Jaccard metrics)
- results/step06_characterization.txt (cluster means, phenotype descriptions)
- results/step07_ch5_crosstab.csv (K_confidence × K_accuracy cross-tabulation)
- results/step07_chi_square.csv (association test: chi-square statistic, p-value, effect size)
- plots/step08_cluster_scatter.png (2D plot: intercept × slope with cluster colors)

**Success Criteria:**
- BIC minimum clearly identified (not flat across K range)
- All cluster sizes >= 10% (no trivial clusters)
- Silhouette score computed (compare to 0.40 threshold and Ch5 5.1.5 value)
- Cross-tabulation with Ch5 5.1.5 cluster labels complete
- Chi-square test of association computed with p-value and effect size
- Interpretation documented: integrated (match) vs dissociated (divergent) phenotypes

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.1.4 random effects + Ch5 5.1.5 cluster labels)

### DERIVED Data Source:

**Source RQs:**
1. **RQ 6.1.4 (ICC Decomposition):** Provides random effects for confidence clustering
2. **Ch5 5.1.5 (Accuracy Clustering):** Provides accuracy cluster labels for cross-tabulation

**File Paths:**
- **Primary Input:** results/ch6/6.1.4/data/step04_random_effects.csv (100 rows: UID, intercept, slope)
  - Note: RQ 6.1.4 specification explicitly states "REQUIRED for 6.1.5"
- **Comparison Input:** results/ch5/5.1.5/data/step04_cluster_assignments.csv (100 rows: UID, accuracy_cluster_label)

**Dependencies:**
1. **RQ 6.1.4 must complete Step 4** (random effects extraction from best LMM in RQ 6.1.1)
2. **Ch5 5.1.5 must complete Step 4** (cluster assignments for accuracy phenotypes)

**Critical Note:**
RQ 6.1.4 specification states: "data/step04_random_effects.csv (100 rows, REQUIRED for 6.1.5)" - this is explicit dependency documentation. If RQ 6.1.4 has not extracted random effects, this RQ cannot proceed.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 6.1.4)
- [ ] No exclusions

**Items:**
- N/A (clustering operates on aggregated theta scores, not item-level data)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - inherited from RQ 6.1.4
- Random effects summarize across all timepoints

**Clustering Features:**
- [x] Random intercept (baseline confidence at Day 0)
- [x] Random slope (rate of confidence decline over time)
- [ ] Exclude higher-order terms (quadratic, etc.) - only intercept + slope for parsimony

---
