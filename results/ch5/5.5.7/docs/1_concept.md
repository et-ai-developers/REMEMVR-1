# RQ 5.5.7: Source-Destination Clustering

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** Clustering
**Full ID:** 5.5.7

---

## Research Question

**Primary Question:**
Can participants be grouped into latent classes based on source (pick-up location: -U-) and destination (put-down location: -D-) memory patterns (intercepts and slopes)?

**Scope:**
This RQ examines individual differences in source and destination memory using K-means clustering on 4 features (Source_intercept, Source_slope, Destination_intercept, Destination_slope) extracted from RQ 5.5.6 variance decomposition. Sample: N=100 participants, tests K=1 to K=6 clusters with BIC model selection.

**Theoretical Framing:**
Exploratory analysis to determine if participants cluster into interpretable profiles based on source-destination memory patterns. This is part of a systematic clustering series across Chapter 5 (RQ 5.1.5, 5.2.7, 5.3.8, 5.4.7) examining whether memory ability clusters or exists on a continuum.

---

## Theoretical Background

**Relevant Theories:**

- **Continuous vs Categorical Individual Differences:** Memory ability may exist on a continuum (dimensional model) rather than discrete classes (categorical model). Clustering analyses can test this hypothesis.

- **Source-Destination Dissociation:** If source and destination memory rely on dissociable mechanisms (per RQ 5.5.1), participants may show differential performance patterns (e.g., "good source, poor destination" profile).

- **Intercept-Driven Clustering:** Given the universal Chapter 5 pattern that ICC_slope ≈ 0 (RQ 5.5.6), clustering will be driven primarily by intercepts (baseline memory ability) rather than slopes (forgetting rates).

**Key Citations:**

- **Parsons, S., Kruijt, A. W., & Fox, E. (2019).** Psychological science needs a standard practice of reporting the reliability of cognitive-behavioral measurements. Advances in Methods and Practices in Psychological Science, 2(4), 378-395. [Slope reliability in cognitive tasks; relevant for ICC_slope near-zero interpretation]
- **Hennig, C. (2007).** Cluster-wise assessment of cluster stability. Computational Statistics & Data Analysis, 52(1), 258-271. [Jaccard bootstrap stability methodology; B=100 iterations standard]
- **Van Mechelen, I., & De Boeck, P. (2004).** Person-situation interactions: Modelling and analysis. Current Directions in Psychological Science, 13(1), 29-33. [Continuous vs categorical individual differences; mixture model alternatives]

[Additional citations to be added by rq_scholar]

**Theoretical Predictions:**

Based on the consistent pattern across Chapter 5 clustering RQs (5.1.5, 5.2.7, 5.3.8, 5.4.7):
- Memory ability is continuous, not categorical (clustering quality will be weak)
- Clusters will show moderate stability (useful for descriptive purposes)
- Clustering driven by intercepts only (slopes near zero)
- If source-destination dissociation exists, clusters may show location-type-specific patterns

**Literature Gaps:**

The source-destination clustering RQ is the final installment in the systematic clustering series across Chapter 5. Previous RQs (General, Domains, Paradigms, Congruence) established weak clustering quality but stable groupings. This RQ tests whether the pattern replicates for source-destination memory, and whether source-destination dissociation creates location-specific profiles.

---

## Hypothesis

**Primary Hypothesis:**

Clustering will show weak quality (Silhouette score < 0.40) but stable groupings (Jaccard bootstrap stability > 0.60), consistent with the universal Chapter 5 pattern (RQ 5.1.5, 5.2.7, 5.3.8, 5.4.7).

**Secondary Hypotheses:**

1. Clustering will be driven by intercepts only (slopes ≈ 0 per RQ 5.5.6)
2. If source-destination shows a true dissociation (per RQ 5.5.1), clusters may differentiate by location-type-specific intercepts (e.g., "good source, poor destination" profile vs "poor source, good destination" profile)
3. Davies-Bouldin index < 1.50 (moderate cluster separation)

**Theoretical Rationale:**

Memory ability is continuous, not categorical (dimensional model). The weak clustering quality reflects the absence of natural clusters in memory ability. However, K-means can still partition participants into stable, interpretable groupings useful for descriptive purposes. The hypothesis of weak-but-stable clustering is grounded in:

1. **Consistent Chapter 5 Pattern:** RQ 5.1.5 (General), 5.2.7 (Domains), 5.3.8 (Paradigms), and 5.4.7 (Congruence) all showed Silhouette < 0.40 but Jaccard > 0.60
2. **Slope Near Zero:** RQ 5.5.6 established ICC_slope ≈ 0 for both source and destination (design limitation: 4 timepoints insufficient for reliable slope estimation)
3. **Source-Destination Dissociation Hypothesis:** If source and destination memory rely on dissociable mechanisms (stronger source memory per RQ 5.5.1, differential consolidation per RQ 5.5.2), participants may show location-specific profiles not seen in prior clustering RQs

**Expected Effect Pattern:**

- Optimal K determined by BIC minimum (expected K=2-4 based on prior clustering RQs)
- Silhouette score: 0.20-0.39 (weak quality, no natural clusters)
- Davies-Bouldin index: 1.00-1.49 (moderate separation)
- Jaccard bootstrap stability: 0.60-0.80 (stable cluster assignments)
- Cluster sizes balanced (no cluster < 10% of sample)
- Cluster characterization interpretable (location-type-specific patterns if dissociation exists)

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT examined in this RQ

- [x] **Where** (Spatial Location)
  - [x] `-U-` tags (pick-up location / source memory)
  - [x] `-D-` tags (put-down location / destination memory)
  - [ ] `-L-` tags (static location, legacy - EXCLUDED)
  - Disambiguation: This RQ examines clustering on source (-U-) vs destination (-D-) random effects from RQ 5.5.6

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT examined in this RQ

**Inclusion Rationale:**

This RQ focuses on source-destination memory patterns (pick-up vs put-down locations in VR episodic memory). Random effects (intercept + slope per location type) are derived from RQ 5.5.6 variance decomposition, which stratified participants by source (-U-) and destination (-D-) memory performance. The 4 clustering features are:
1. Source_intercept (baseline source memory at Day 0)
2. Source_slope (source memory forgetting rate)
3. Destination_intercept (baseline destination memory at Day 0)
4. Destination_slope (destination memory forgetting rate)

**Exclusion Rationale:**

- `-L-` static location tags: Excluded throughout Type 5.5 (Source-Destination) RQs. Root RQ 5.5.1 filtered to -U-/-D- only.
- What (-N-) and When (-O-) domains: Not relevant to source-destination clustering analysis.

---

## Analysis Approach

**Analysis Type:**

K-means clustering on 4-dimensional feature space (source/destination intercepts and slopes), with BIC model selection, clustering quality validation (Silhouette, Davies-Bouldin), and bootstrap stability assessment (Jaccard index).

**High-Level Workflow:**

**Step 0:** Load random effects from RQ 5.5.6 (200 rows: 100 UID × 2 location types -> 100 rows × 4 features)

**Step 1:** Standardize features to z-scores (mean=0, SD=1) to equalize scale across intercepts and slopes

**Step 2:** Test K=1 to K=6 using K-means clustering (random_state=42, n_init=50); compute inertia and BIC for model selection; select optimal K as BIC minimum (or K-1 if BIC minimum at boundary)

**Step 3:** Validate clustering quality using 3 metrics:
- Silhouette score (threshold ≥0.40 for acceptable quality)
- Davies-Bouldin index (threshold <1.50 for acceptable separation)
- Jaccard bootstrap stability (threshold ≥0.75 for acceptable stability, computed with B=100 bootstrap iterations per Hennig, 2007)

**Bootstrap Parameters:**
- B = 100 bootstrap resamples (with replacement, N=100 per resample)
- For each bootstrap sample, fit K-means with same K and compute cluster assignments
- Jaccard similarity = |A ∩ B| / |A ∪ B| between original and bootstrap cluster assignments
- Report mean Jaccard across B=100 iterations with 95% CI

**Remedial Actions if Quality Metrics Fail:**
If Silhouette < 0.40 AND Jaccard < 0.75 (both fail):
1. **Report as meaningful null finding:** Document that memory ability is continuous, not categorical
2. **Test dimensionality reduction:** Re-run clustering with 2 features only (intercepts) if ICC_slope ≈ 0 from RQ 5.5.6
3. **Test alternative K:** If BIC minimum is at boundary (K=6), test K=7,8 to verify BIC minimum location
4. **Interpret clusters descriptively:** Even weak clusters can be useful for characterizing performance patterns

If Silhouette ≥ 0.40 OR Jaccard ≥ 0.75 (at least one passes):
- Proceed with standard interpretation, noting which criterion passed/failed

**Step 4:** Fit final K-means with optimal K (random_state=42, n_init=50); extract cluster assignments (100 UIDs) and cluster centers (K centers × 4 features)

**Step 5:** Characterize clusters by mean intercept/slope per location type, assign interpretive labels (e.g., "High Source, Low Destination", "Balanced High Performers", etc.)

**Step 6:** Create scatter plot matrix (4×4 grid) colored by cluster membership with cluster centers overlaid and reference lines at z=0

**Expected Outputs:**

- data/step00_random_effects_from_rq556.csv (100 rows × 4 features)
- data/step01_standardized_features.csv (100 rows × 4 features, z-scored)
- results/step02_cluster_selection.csv (K=1-6: inertia, BIC)
- results/step03_optimal_k.txt (selected K value with justification)
- data/step04_cluster_assignments.csv (100 rows: UID, cluster)
- results/step04_cluster_centers.csv (K rows × 4 features)
- results/step05_cluster_validation.csv (3 metrics: Silhouette, Davies-Bouldin, Jaccard)
- results/step05_cluster_characterization.txt (interpretive cluster descriptions)
- plots/step06_cluster_scatter_matrix.png (4×4 scatter plot matrix)

**Success Criteria:**

- **Dependency verification:** RQ 5.5.6 status = success
- **Data loading:** Random effects loaded correctly (100 rows × 4 features), no missing values
- **Standardization:** Z-scores correct (mean ≈ 0, SD ≈ 1 per feature)
- **BIC minimum identified:** Clear optimal K selected (or boundary case documented)
- **Cluster sizes balanced:** No cluster < 10% of sample (minimum 10 participants per cluster)
- **Validation metrics computed:** Silhouette, Davies-Bouldin, Jaccard all present
- **Cluster characterization interpretable:** Clear descriptions per cluster based on location-type-specific patterns
- **Plot quality:** Scatter matrix shows separation (if any), cluster centers marked, reference lines at z=0
- **Replicability:** Results replicate with random_state=42

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.5.6 variance decomposition random effects)

### DERIVED Data Source:

**Source RQ:**
RQ 5.5.6 (Source-Destination Variance Decomposition)

**File Paths:**
- `results/ch5/5.5.6/data/step04_random_effects.csv` (200 rows: 100 UID × 2 location types, with intercept + slope per location)

**Dependencies:**

RQ 5.5.6 must complete Steps 1-4 (location-stratified LMMs, variance component extraction, ICC computation, random effects extraction) before this RQ can run. The random effects file contains:
- 200 rows: 100 participants × 2 location types (Source, Destination)
- Columns: UID, location_type, Total_Intercept, Total_Slope

This RQ reshapes the 200-row format into 100 rows × 4 features:
- Source_intercept (from location_type="Source")
- Source_slope (from location_type="Source")
- Destination_intercept (from location_type="Destination")
- Destination_slope (from location_type="Destination")

**Dependency Chain:**
- RQ 5.5.1 (root: IRT calibration on -U-/-D- items)
- RQ 5.5.6 (variance decomposition: random effects extraction)
- RQ 5.5.7 (this RQ: clustering on random effects)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 5.5.6 (inherited inclusion criteria from RQ 5.5.1)
- No exclusions based on clustering features (all participants clustered)

**Items:**
- N/A (clustering uses random effects, not item-level data)

**Tests:**
- N/A (random effects aggregate across all 4 tests from RQ 5.5.6)

**Clustering Features:**
- [x] All 4 features included: Source_intercept, Source_slope, Destination_intercept, Destination_slope
- Standardized to z-scores (mean=0, SD=1) before clustering

---
