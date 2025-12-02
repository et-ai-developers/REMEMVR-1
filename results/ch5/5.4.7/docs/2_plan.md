# Analysis Plan: RQ 5.4.7 - Schema-Based Clustering

**Research Question:** 5.4.7
**Created:** 2025-12-02
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ performs exploratory K-means clustering to identify latent subgroups with distinct schema-congruence memory profiles. The analysis uses 6 clustering variables (intercept and slope for Common, Congruent, and Incongruent items) extracted as random effects from RQ 5.4.6 variance decomposition. Cluster number (K) is determined empirically via BIC model selection testing K=1 to K=6 profiles.

**Pipeline:** Clustering (K-means with BIC selection)
**Steps:** 7 total analysis steps
**Estimated Runtime:** Low to Medium (clustering is computationally efficient, ~5-15 minutes total)

**Key Decisions Applied:**
- Clustering-Specific Validation: Silhouette >= 0.40, Davies-Bouldin < 1.5, Jaccard > 0.75 for bootstrap stability
- Cluster Size Constraint: Each cluster must contain >= 10% of sample (N >= 10)
- Sphericity Check: Visual validation via scatter plot matrix

**Dependencies:**
- RQ 5.4.6 must complete (provides random effects for clustering)

---

## Analysis Plan

### Step 0: Extract and Reshape Random Effects from RQ 5.4.6

**Purpose:** Load random effects from RQ 5.4.6 and reshape from long format (300 rows: 100 UID x 3 congruence levels) to wide format (100 rows x 6 features) for clustering.

**Dependencies:** None (first step, but requires RQ 5.4.6 completion)

**Complexity:** Low (data extraction and reshaping, <1 minute)

**Input:**

**File:** results/ch5/5.4.6/data/step04_random_effects.csv
**Source:** RQ 5.4.6 variance decomposition (Step 4 output)
**Format:** CSV, long format
**Columns:**
  - `UID` (string, participant identifier, e.g., "P001")
  - `congruence` (string, values: "Common", "Congruent", "Incongruent")
  - `Total_Intercept` (float, participant-specific intercept for congruence level)
  - `Total_Slope` (float, participant-specific slope for congruence level)
**Expected Rows:** 300 (100 participants x 3 congruence levels)
**Expected Data:** Each participant has 3 rows (one per congruence level) with intercept and slope

**Processing:**

**Reshape Logic:**
1. Read long-format random effects (300 rows)
2. Pivot to wide format:
   - Rows: UID (100 participants)
   - Columns: Common_Intercept, Common_Slope, Congruent_Intercept, Congruent_Slope, Incongruent_Intercept, Incongruent_Slope
3. Verify no missing values (all participants must have complete data for all 6 features)
4. Verify exactly 100 participants present

**Output:**

**File:** data/step00_random_effects_from_rq546.csv
**Format:** CSV, wide format (one row per participant)
**Columns:**
  - `UID` (string, participant identifier)
  - `Common_Intercept` (float, intercept for Common items)
  - `Common_Slope` (float, slope for Common items)
  - `Congruent_Intercept` (float, intercept for Congruent items)
  - `Congruent_Slope` (float, slope for Congruent items)
  - `Incongruent_Intercept` (float, intercept for Incongruent items)
  - `Incongruent_Slope` (float, slope for Incongruent items)
**Expected Rows:** 100 (one per participant)
**Expected Columns:** 7 (UID + 6 clustering features)

**Validation Requirement:**

Validation tools MUST be used after data extraction and reshaping. Specific validation tools will be determined by rq_tools based on data format requirements (likely validate_dataframe_structure, validate_missing_data).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_random_effects_from_rq546.csv exists (exact path)
- Expected rows: 100 (one per participant)
- Expected columns: 7 (UID + 6 features)
- Data types: UID (object/string), all features (float64)

*Value Ranges:*
- Intercepts typically in [-2, 2] range (theta scale, scientifically reasonable for IRT ability)
- Slopes typically in [-1, 1] range (change per unit time, scientifically reasonable for forgetting rates)
- Note: These are random effects (deviations from population mean), so values can be positive or negative

*Data Quality:*
- No NaN values allowed (all 100 participants must have complete data for all 6 features)
- No duplicate UIDs (each participant appears exactly once)
- All 100 participants from RQ 5.4.6 must be present (no data loss during reshape)

*Log Validation:*
- Required pattern: "Reshaped from 300 rows (long) to 100 rows (wide)"
- Required pattern: "All 100 participants present, no missing values"
- Forbidden patterns: "ERROR", "Missing data detected", "Duplicate UIDs found"
- Acceptable warnings: None expected for data reshaping

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 87")
- Log failure to logs/step00_extract_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose (common causes: RQ 5.4.6 incomplete, file path incorrect, data corruption)

---

### Step 1: Standardize Clustering Features to Z-Scores

**Purpose:** Standardize all 6 clustering features to mean=0, SD=1 (z-scores) to ensure equal weighting in K-means algorithm. Prevents features with larger scales (e.g., intercepts) from dominating clustering solution.

**Dependencies:** Step 0 (requires reshaped random effects)

**Complexity:** Low (standardization computation, <1 minute)

**Input:**

**File:** data/step00_random_effects_from_rq546.csv
**Source:** Generated by Step 0 (reshaped random effects)
**Format:** CSV, wide format
**Columns:** UID + 6 clustering features (Common_Intercept, Common_Slope, Congruent_Intercept, Congruent_Slope, Incongruent_Intercept, Incongruent_Slope)
**Expected Rows:** 100

**Processing:**

**Standardization Method:**
1. Compute grand mean and SD for each of 6 features across all 100 participants
2. Transform each feature: z = (x - mean) / SD
3. Verify standardization successful: mean ~ 0, SD ~ 1 for all features (tolerance: mean in [-0.1, 0.1], SD in [0.9, 1.1])
4. Preserve UID column (not standardized)

**Output:**

**File:** data/step01_standardized_features.csv
**Format:** CSV, wide format
**Columns:**
  - `UID` (string, participant identifier, unchanged)
  - `Common_Intercept_z` (float, z-scored Common intercept)
  - `Common_Slope_z` (float, z-scored Common slope)
  - `Congruent_Intercept_z` (float, z-scored Congruent intercept)
  - `Congruent_Slope_z` (float, z-scored Congruent slope)
  - `Incongruent_Intercept_z` (float, z-scored Incongruent intercept)
  - `Incongruent_Slope_z` (float, z-scored Incongruent slope)
**Expected Rows:** 100
**Expected Columns:** 7 (UID + 6 z-scored features)

**Validation Requirement:**

Validation tools MUST be used after standardization. Specific validation tools will be determined by rq_tools (likely validate_standardization with tolerance checks).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_standardized_features.csv exists (exact path)
- Expected rows: 100 (unchanged from input)
- Expected columns: 7 (UID + 6 z-scored features)
- Data types: UID (object/string), all z-scored features (float64)

*Value Ranges:*
- Z-scores typically in [-3, 3] range (values > 3 are outliers but not errors)
- Mean ~ 0 for each feature (tolerance: mean in [-0.1, 0.1])
- SD ~ 1 for each feature (tolerance: SD in [0.9, 1.1])

*Data Quality:*
- No NaN values allowed (standardization should not introduce missing data)
- All 100 participants present (no data loss during standardization)
- No duplicate UIDs

*Log Validation:*
- Required pattern: "Standardization complete: 6 features transformed to z-scores"
- Required pattern: "VALIDATION - PASS: mean ~ 0, SD ~ 1 for all features"
- Forbidden patterns: "ERROR", "NaN values detected", "Standardization failed"
- Acceptable warnings: "Feature X has 2 outliers (z > 3)" (outliers are acceptable, just flagged)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Feature Common_Intercept_z has mean=0.5, expected ~ 0")
- Log failure to logs/step01_standardize_features.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose (common causes: constant feature, numerical precision issues)

---

### Step 2: Cluster Model Selection (K=1 to K=6 via BIC)

**Purpose:** Test K-means clustering solutions for K=1 to K=6, compute BIC for each, and select optimal K as BIC minimum. This step determines the number of latent profiles empirically.

**Dependencies:** Step 1 (requires standardized features)

**Complexity:** Medium (6 K-means fits, ~5 minutes total)

**Input:**

**File:** data/step01_standardized_features.csv
**Source:** Generated by Step 1 (z-scored features)
**Format:** CSV, wide format
**Columns:** UID + 6 z-scored features
**Expected Rows:** 100

**Processing:**

**K-means Model Selection:**
1. For each K in {1, 2, 3, 4, 5, 6}:
   a. Fit K-means with random_state=42, n_init=50 (for stability across 50 random initializations)
   b. Extract inertia (within-cluster sum of squares)
   c. Compute BIC = N * log(inertia / N) + K * log(N), where N=100 participants
2. Select optimal K as argmin(BIC) across K=1-6
3. Verify optimal K is not at boundary (K=1 or K=6 suggests model misspecification)
4. Log BIC values for all K to enable inspection

**Output:**

**File 1:** data/step02_cluster_selection.csv
**Format:** CSV, one row per K value tested
**Columns:**
  - `K` (int, number of clusters tested, values: 1-6)
  - `inertia` (float, within-cluster sum of squares)
  - `BIC` (float, Bayesian Information Criterion)
**Expected Rows:** 6 (one per K value)

**File 2:** data/step02_optimal_k.txt
**Format:** Plain text, single integer value
**Content:** Optimal K (e.g., "3")
**Purpose:** Pass optimal K to Step 3 for final clustering

**Validation Requirement:**

Validation tools MUST be used after cluster selection. Specific validation tools will be determined by rq_tools (likely custom BIC validation checking monotonicity and boundary conditions).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cluster_selection.csv exists (6 rows x 3 columns: K, inertia, BIC)
- data/step02_optimal_k.txt exists (single integer value)
- Data types: K (int), inertia (float), BIC (float)

*Value Ranges:*
- K in {1, 2, 3, 4, 5, 6} (exact values tested)
- Inertia monotonically decreasing with K (larger K always reduces within-cluster variance)
- BIC has minimum within K=1-6 range (not at boundary K=1 or K=6)
- Optimal K in {2, 3, 4, 5} (boundary values suggest misspecification)

*Data Quality:*
- All 6 rows present (one per K value)
- No NaN values in inertia or BIC
- Optimal K is integer in valid range

*Log Validation:*
- Required pattern: "Tested K=1 to K=6, BIC minimum at K={optimal_k}"
- Required pattern: "Optimal K not at boundary (K != 1 and K != 6)"
- Forbidden patterns: "ERROR", "BIC computation failed", "Optimal K=1" (suggests no clustering structure), "Optimal K=6" (suggests model underspecified)
- Acceptable warnings: None expected for BIC model selection

**Expected Behavior on Validation Failure:**
- If optimal K at boundary (K=1 or K=6): Log warning, proceed with caution (results may indicate poor cluster structure)
- If BIC computation fails: Raise error, log to logs/step02_cluster_selection.log, quit, invoke g_debug
- If inertia not monotonically decreasing: Raise error (algorithm failure), quit, invoke g_debug

---

### Step 3: Fit Final K-means Model with Optimal K

**Purpose:** Fit K-means using optimal K from Step 2, extract cluster assignments for all 100 participants, and extract cluster centers in z-score space.

**Dependencies:** Step 2 (requires optimal K), Step 1 (requires standardized features)

**Complexity:** Low (single K-means fit, <1 minute)

**Input:**

**File 1:** data/step01_standardized_features.csv
**Source:** Generated by Step 1 (z-scored features for clustering)
**Format:** CSV, 100 rows x 7 columns (UID + 6 features)

**File 2:** data/step02_optimal_k.txt
**Source:** Generated by Step 2 (optimal K value)
**Format:** Plain text, single integer

**Processing:**

**Final K-means Fit:**
1. Read optimal K from step02_optimal_k.txt
2. Fit K-means on 6 z-scored features with:
   - n_clusters = optimal_k
   - random_state = 42 (reproducibility)
   - n_init = 50 (stability across random initializations)
3. Extract cluster assignments (100 participant labels, 0 to K-1)
4. Extract cluster centers (K x 6 matrix in z-score space)
5. Verify cluster size constraint: Each cluster >= 10% of sample (N >= 10 participants)

**Output:**

**File 1:** data/step03_cluster_assignments.csv
**Format:** CSV, one row per participant
**Columns:**
  - `UID` (string, participant identifier)
  - `cluster` (int, cluster assignment 0 to K-1)
**Expected Rows:** 100
**Expected Columns:** 2

**File 2:** data/step03_cluster_centers.csv
**Format:** CSV, one row per cluster
**Columns:**
  - `cluster` (int, cluster ID 0 to K-1)
  - `Common_Intercept_z` (float, cluster center for Common intercept in z-score space)
  - `Common_Slope_z` (float, cluster center for Common slope in z-score space)
  - `Congruent_Intercept_z` (float, cluster center for Congruent intercept in z-score space)
  - `Congruent_Slope_z` (float, cluster center for Congruent slope in z-score space)
  - `Incongruent_Intercept_z` (float, cluster center for Incongruent intercept in z-score space)
  - `Incongruent_Slope_z` (float, cluster center for Incongruent slope in z-score space)
**Expected Rows:** K (optimal cluster number from Step 2)
**Expected Columns:** 7 (cluster + 6 features)

**Validation Requirement:**

Validation tools MUST be used after K-means fitting. Specific validation tools will be determined by rq_tools (likely validate_cluster_assignment checking consecutive cluster IDs and minimum cluster size).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_cluster_assignments.csv exists (100 rows x 2 columns)
- data/step03_cluster_centers.csv exists (K rows x 7 columns)
- Data types: UID (object/string), cluster (int), all centers (float64)

*Value Ranges:*
- Cluster assignments in {0, 1, ..., K-1} (consecutive integers starting from 0)
- Cluster centers in z-score space typically in [-2, 2] range (centers can be outside participant range)
- Each cluster must have >= 10 participants (10% of sample constraint)

*Data Quality:*
- All 100 participants assigned to exactly one cluster
- No missing cluster IDs (0 to K-1 all represented)
- Cluster sizes balanced (no singleton clusters driven by outliers)
- No NaN values in cluster centers

*Log Validation:*
- Required pattern: "K-means fitted with K={optimal_k} clusters"
- Required pattern: "Cluster sizes: Cluster 0: N1, Cluster 1: N2, ... (all >= 10)"
- Required pattern: "VALIDATION - PASS: All clusters meet 10% size constraint"
- Forbidden patterns: "ERROR", "Cluster size < 10", "Missing cluster ID"
- Acceptable warnings: "Cluster size imbalance detected (range: 10-40)" (imbalance is acceptable if all >= 10)

**Expected Behavior on Validation Failure:**
- If cluster size < 10: Raise error, log to logs/step03_fit_final_kmeans.log, quit, invoke g_debug
- If missing cluster IDs: Raise error (algorithm failure), quit, invoke g_debug
- If NaN in cluster centers: Raise error (numerical issue), quit, invoke g_debug

---

### Step 4: Validate Clustering Quality Metrics

**Purpose:** Compute and validate cluster quality metrics (silhouette score, Davies-Bouldin index) and stability metrics (bootstrap Jaccard coefficient) to assess clustering solution quality.

**Dependencies:** Step 3 (requires cluster assignments and centers), Step 1 (requires standardized features)

**Complexity:** Medium (bootstrap resampling with 100 iterations, ~5 minutes)

**Input:**

**File 1:** data/step01_standardized_features.csv
**Source:** Generated by Step 1 (z-scored features)
**Format:** CSV, 100 rows x 7 columns

**File 2:** data/step03_cluster_assignments.csv
**Source:** Generated by Step 3 (cluster labels)
**Format:** CSV, 100 rows x 2 columns

**Processing:**

**Cluster Quality Metrics:**
1. **Silhouette Score:** Compute mean silhouette coefficient across all participants
   - Range: -1 to +1 (higher = better cluster cohesion and separation)
   - Target: >= 0.40 (acceptable cluster structure per concept.md)
2. **Davies-Bouldin Index:** Compute DB index (ratio of within-cluster to between-cluster distances)
   - Range: 0 to infinity (lower = better cluster separation)
   - Target: < 1.5 (acceptable cluster separation per concept.md)
3. **Bootstrap Stability:** Resample 80% of participants, refit K-means, compute Jaccard similarity with original clustering
   - Repeat 100 iterations
   - Report mean Jaccard coefficient and 95% CI
   - Target: Jaccard > 0.75 (stable clustering per concept.md)

**Output:**

**File:** data/step04_cluster_quality_metrics.csv
**Format:** CSV, one row per metric
**Columns:**
  - `metric` (string, metric name: "silhouette", "davies_bouldin", "jaccard_mean", "jaccard_95ci_lower", "jaccard_95ci_upper")
  - `value` (float, metric value)
  - `threshold` (float, target threshold for quality)
  - `pass` (bool, True if metric meets threshold, False otherwise)
**Expected Rows:** 5 (one per metric)

**Validation Requirement:**

Validation tools MUST be used after quality metric computation. Specific validation tools will be determined by rq_tools (likely validate_bootstrap_stability for Jaccard validation, custom validators for silhouette/DB thresholds).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_cluster_quality_metrics.csv exists (5 rows x 4 columns)
- Data types: metric (object/string), value (float), threshold (float), pass (bool)

*Value Ranges:*
- Silhouette in [-1, 1], target >= 0.40
- Davies-Bouldin >= 0, target < 1.5
- Jaccard mean in [0, 1], target > 0.75
- Jaccard 95% CI bounds in [0, 1], CI_lower < CI_upper

*Data Quality:*
- All 5 metrics present (no missing rows)
- No NaN values in metric values
- Pass/fail flags accurate (value compared to threshold correctly)

*Log Validation:*
- Required pattern: "Silhouette score: {value:.2f} (threshold >= 0.40)"
- Required pattern: "Davies-Bouldin index: {value:.2f} (threshold < 1.5)"
- Required pattern: "Bootstrap stability (Jaccard): {mean:.2f} [95% CI: {lower:.2f}, {upper:.2f}] (threshold > 0.75)"
- Required pattern: "VALIDATION - PASS: All metrics meet quality thresholds" (if all pass=True)
- Acceptable warnings: "Silhouette below threshold (weak cluster structure)" (if silhouette < 0.40, log warning but proceed)
- Forbidden patterns: "ERROR", "Bootstrap resampling failed", "NaN metric values"

**Expected Behavior on Validation Failure:**
- If silhouette < 0.40: Log warning to logs/step04_validate_clustering.log, set pass=False, proceed with caution (report tentative clusters in results)
- If Davies-Bouldin >= 1.5: Log warning, set pass=False, proceed with caution
- If Jaccard < 0.75: Log warning, set pass=False, proceed with caution (unstable clustering)
- If bootstrap resampling fails: Raise error, quit, invoke g_debug
- Note: Quality metric failures are WARNINGS, not errors (clustering proceeds, but results interpreted as tentative)

---

### Step 5: Characterize Clusters by Congruence-Specific Patterns

**Purpose:** Transform cluster centers from z-score space back to original scale, compute cluster-specific summary statistics, and assign interpretive labels based on congruence-specific patterns.

**Dependencies:** Step 3 (requires cluster centers), Step 0 (requires original scale means/SDs for back-transformation)

**Complexity:** Low (statistical summarization, <1 minute)

**Input:**

**File 1:** data/step03_cluster_centers.csv
**Source:** Generated by Step 3 (cluster centers in z-score space)
**Format:** CSV, K rows x 7 columns

**File 2:** data/step00_random_effects_from_rq546.csv
**Source:** Generated by Step 0 (original scale for back-transformation)
**Format:** CSV, 100 rows x 7 columns

**File 3:** data/step03_cluster_assignments.csv
**Source:** Generated by Step 3 (to compute cluster-specific statistics)
**Format:** CSV, 100 rows x 2 columns

**Processing:**

**Cluster Characterization:**
1. **Back-transformation:** For each cluster center feature, transform z-score to original scale:
   - original_value = z * SD + mean (using Step 0 grand means and SDs)
2. **Cluster-specific statistics:** For each cluster, compute:
   - N participants in cluster
   - Mean, SD, min, max for each of 6 features (on original scale)
3. **Interpretive labeling:** Assign descriptive labels based on patterns:
   - Example: "High Common, Low Incongruent" (if cluster has high Common intercept/slope, low Incongruent intercept/slope)
   - Example: "Uniform High" (if cluster has high intercepts/slopes across all congruence levels)
   - Example: "Schema-Selective Impairment" (if cluster has selective deficit for Incongruent items only)
4. **Key differentiating features:** Identify which features (intercepts vs slopes, specific congruence levels) most differentiate clusters

**Output:**

**File 1:** data/step05_cluster_centers_original_scale.csv
**Format:** CSV, one row per cluster
**Columns:**
  - `cluster` (int, cluster ID 0 to K-1)
  - `Common_Intercept` (float, cluster center for Common intercept, original scale)
  - `Common_Slope` (float, cluster center for Common slope, original scale)
  - `Congruent_Intercept` (float, cluster center for Congruent intercept, original scale)
  - `Congruent_Slope` (float, cluster center for Congruent slope, original scale)
  - `Incongruent_Intercept` (float, cluster center for Incongruent intercept, original scale)
  - `Incongruent_Slope` (float, cluster center for Incongruent slope, original scale)
  - `N` (int, number of participants in cluster)
  - `label` (string, interpretive label for cluster)
**Expected Rows:** K

**File 2:** data/step05_cluster_summary_stats.csv
**Format:** CSV, one row per cluster x feature combination
**Columns:**
  - `cluster` (int, cluster ID)
  - `feature` (string, feature name: "Common_Intercept", "Common_Slope", etc.)
  - `mean` (float, mean value for feature within cluster)
  - `SD` (float, standard deviation within cluster)
  - `min` (float, minimum value within cluster)
  - `max` (float, maximum value within cluster)
**Expected Rows:** K x 6 (each cluster has 6 features)

**Validation Requirement:**

Validation tools MUST be used after cluster characterization. Specific validation tools will be determined by rq_tools (likely validate_cluster_summary_stats checking min <= mean <= max, SD >= 0, N > 0).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cluster_centers_original_scale.csv exists (K rows x 9 columns)
- data/step05_cluster_summary_stats.csv exists (K x 6 rows)
- Data types: cluster (int), features (float), N (int), label (object/string)

*Value Ranges:*
- Original scale centers typically in [-2, 2] for intercepts, [-1, 1] for slopes (theta scale)
- Summary stats: min <= mean <= max, SD >= 0, N >= 10 (per cluster size constraint)

*Data Quality:*
- All K clusters characterized (no missing clusters)
- All 6 features per cluster (no missing features)
- No NaN values in centers or summary stats
- Labels are non-empty strings (interpretive labels assigned)

*Log Validation:*
- Required pattern: "Back-transformed K={K} cluster centers to original scale"
- Required pattern: "Assigned interpretive labels: Cluster 0 = '{label0}', Cluster 1 = '{label1}', ..."
- Required pattern: "VALIDATION - PASS: All clusters characterized"
- Forbidden patterns: "ERROR", "NaN values in cluster centers", "Empty cluster label"
- Acceptable warnings: "Cluster overlap detected (centers within 0.5 SD)" (acceptable if BIC still selected K)

**Expected Behavior on Validation Failure:**
- If min > mean or mean > max: Raise error (statistical inconsistency), quit, invoke g_debug
- If SD < 0: Raise error (computation error), quit, invoke g_debug
- If N < 10: Raise error (violates cluster size constraint from Step 3), quit, invoke g_debug
- If empty label: Log warning, assign default label "Cluster {id}", proceed

---

### Step 6: Prepare Scatter Plot Matrix Data for Visualization

**Purpose:** Create plot source CSV for scatter plot matrix visualization showing 6-dimensional clustering solution. This data will be used by rq_plots to generate the final visualization.

**Dependencies:** Step 1 (requires standardized features for plotting), Step 3 (requires cluster assignments for coloring), Step 5 (requires cluster labels for legend)

**Complexity:** Low (data aggregation, <1 minute)

**Plot Description:** Scatter plot matrix with 6x6 panels showing all pairwise combinations of clustering features (Common_Intercept, Common_Slope, Congruent_Intercept, Congruent_Slope, Incongruent_Intercept, Incongruent_Slope). Points colored by cluster membership, cluster centers overlaid as reference markers. Marginal density plots on diagonal to show cluster separation.

**Required Data Sources:**
- data/step01_standardized_features.csv (6 z-scored features for scatter plots)
- data/step03_cluster_assignments.csv (cluster membership for coloring)
- data/step03_cluster_centers.csv (cluster centers for overlay markers)
- data/step05_cluster_centers_original_scale.csv (cluster labels for legend)

**Input:**

**File 1:** data/step01_standardized_features.csv
**Source:** Generated by Step 1
**Format:** CSV, 100 rows x 7 columns (UID + 6 z-scored features)

**File 2:** data/step03_cluster_assignments.csv
**Source:** Generated by Step 3
**Format:** CSV, 100 rows x 2 columns (UID + cluster)

**File 3:** data/step03_cluster_centers.csv
**Source:** Generated by Step 3
**Format:** CSV, K rows x 7 columns (cluster + 6 z-scored centers)

**File 4:** data/step05_cluster_centers_original_scale.csv
**Source:** Generated by Step 5
**Format:** CSV, K rows x 9 columns (cluster + 6 original scale centers + N + label)

**Processing:**

**Aggregation Logic:**
1. Merge standardized features with cluster assignments on UID (adds cluster column to participant data)
2. Add cluster labels from step05 cluster characterization (for legend)
3. Include cluster centers for overlay markers
4. Select required columns for plotting:
   - Participant data: UID, cluster, cluster_label, 6 z-scored features
   - Cluster centers: cluster, cluster_label, 6 z-scored centers
5. Save to plot source CSV

**Output (Plot Source CSV):** data/step06_scatter_matrix_plot_data.csv

**Required Columns:**
- `UID` (string, participant identifier, for participant data rows)
- `cluster` (int, cluster assignment 0 to K-1)
- `cluster_label` (string, interpretive cluster label from Step 5)
- `Common_Intercept_z` (float, z-scored Common intercept)
- `Common_Slope_z` (float, z-scored Common slope)
- `Congruent_Intercept_z` (float, z-scored Congruent intercept)
- `Congruent_Slope_z` (float, z-scored Congruent slope)
- `Incongruent_Intercept_z` (float, z-scored Incongruent intercept)
- `Incongruent_Slope_z` (float, z-scored Incongruent slope)
- `data_type` (string, "participant" or "center", distinguishes participant data rows from cluster center rows)

**Expected Rows:** 100 + K (100 participant rows + K cluster center rows)

**Plotting Function (General):** Scatter plot matrix (rq_plots maps to appropriate seaborn pairplot or custom scatter matrix function)

**Validation Requirement:**

Validation tools MUST be used after plot data preparation. Specific validation tools will be determined by rq_tools (likely validate_plot_data_completeness checking all clusters represented, no NaN in critical columns).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_scatter_matrix_plot_data.csv exists (exact path)
- Expected rows: 100 + K (participants + cluster centers)
- Expected columns: 10 (UID, cluster, cluster_label, 6 z-scored features, data_type)
- Data types: UID (object/string), cluster (int), cluster_label (object/string), features (float64), data_type (object/string)

*Value Ranges:*
- Z-scored features in [-3, 3] range (outliers acceptable)
- Cluster in {0, 1, ..., K-1}
- Data_type in {"participant", "center"}

*Data Quality:*
- No NaN values in cluster, cluster_label, or z-scored features (UID can be NaN for cluster center rows)
- All K clusters represented (both in participant data and cluster center rows)
- Exactly 100 participant rows + K center rows
- No duplicate UIDs in participant rows

*Log Validation:*
- Required pattern: "Plot data prepared: 100 participant rows + {K} cluster center rows"
- Required pattern: "All {K} clusters represented in plot data"
- Required pattern: "VALIDATION - PASS: Plot data complete and ready for visualization"
- Forbidden patterns: "ERROR", "Missing cluster in plot data", "NaN values detected"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 103 rows (100+3), found 100")
- Log failure to logs/step06_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- g_debug invoked to diagnose root cause

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)
- data/step00_random_effects_from_rq546.csv (from Step 0: extracted and reshaped random effects, 100 rows x 7 columns)
- data/step01_standardized_features.csv (from Step 1: z-scored features, 100 rows x 7 columns)
- data/step02_cluster_selection.csv (from Step 2: BIC model selection, 6 rows x 3 columns)
- data/step02_optimal_k.txt (from Step 2: optimal K value, single integer)
- data/step03_cluster_assignments.csv (from Step 3: cluster membership, 100 rows x 2 columns)
- data/step03_cluster_centers.csv (from Step 3: cluster centers in z-score space, K rows x 7 columns)
- data/step04_cluster_quality_metrics.csv (from Step 4: silhouette, DB, Jaccard metrics, 5 rows x 4 columns)
- data/step05_cluster_centers_original_scale.csv (from Step 5: cluster centers back-transformed, K rows x 9 columns)
- data/step05_cluster_summary_stats.csv (from Step 5: cluster-specific statistics, K x 6 rows)
- data/step06_scatter_matrix_plot_data.csv (from Step 6: plot source CSV, 100 + K rows x 10 columns)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)
- logs/step00_extract_data.log
- logs/step01_standardize_features.log
- logs/step02_cluster_selection.log
- logs/step03_fit_final_kmeans.log
- logs/step04_validate_clustering.log
- logs/step05_characterize_clusters.log
- logs/step06_prepare_plot_data.log

### Plots (EMPTY until rq_plots runs)
- plots/scatter_matrix_clusters.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)
- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step 0 Output: Reshaped Random Effects

**Transformation:** Long (300 rows: 100 UID x 3 congruence levels) -> Wide (100 rows: 1 per UID)

**Input Format (from RQ 5.4.6):**
- Columns: UID, congruence, Total_Intercept, Total_Slope
- Example rows:
  - P001, Common, 0.25, -0.12
  - P001, Congruent, 0.30, -0.10
  - P001, Incongruent, 0.15, -0.18

**Output Format:**
- Columns: UID, Common_Intercept, Common_Slope, Congruent_Intercept, Congruent_Slope, Incongruent_Intercept, Incongruent_Slope
- Example row:
  - P001, 0.25, -0.12, 0.30, -0.10, 0.15, -0.18

**Pivot Logic:**
- Key: UID (participant identifier)
- Columns: congruence level (Common, Congruent, Incongruent) x metric (Intercept, Slope)
- Values: Total_Intercept and Total_Slope from RQ 5.4.6

### Step 1 Output: Standardized Features

**Transformation:** Original scale -> Z-scores

**Standardization Formula:** z = (x - mean) / SD

**Input Format:**
- Columns: UID, Common_Intercept, Common_Slope, Congruent_Intercept, Congruent_Slope, Incongruent_Intercept, Incongruent_Slope
- Values: Original scale (theta units for intercepts, theta/hour for slopes)

**Output Format:**
- Columns: UID, Common_Intercept_z, Common_Slope_z, Congruent_Intercept_z, Congruent_Slope_z, Incongruent_Intercept_z, Incongruent_Slope_z
- Values: Z-scores (mean=0, SD=1)

**Verification:** Compute mean and SD for each z-scored feature, confirm mean in [-0.1, 0.1] and SD in [0.9, 1.1]

### Step 6 Output: Plot Source Data

**Merge Logic:**
- Merge standardized features (Step 1) with cluster assignments (Step 3) on UID
- Add cluster labels from cluster characterization (Step 5)
- Append cluster center rows (marked with data_type="center", UID=NA)

**Output Format:**
- Participant rows: UID, cluster, cluster_label, 6 z-scored features, data_type="participant"
- Cluster center rows: NA, cluster, cluster_label, 6 z-scored centers, data_type="center"

**Purpose:** Single CSV containing all data needed for scatter plot matrix (participant points colored by cluster, cluster centers as overlay markers, cluster labels for legend)

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQ (Dependency Exists)

**This RQ requires outputs from:**
- **RQ 5.4.6** (Schema-Specific Variance Decomposition)
  - File: results/ch5/5.4.6/data/step04_random_effects.csv
  - Used in: Step 0 (extract and reshape random effects for clustering)
  - Rationale: RQ 5.4.6 decomposes congruence-specific forgetting trajectories into individual participant random effects (intercepts and slopes per congruence level). This RQ clusters participants based on those random effects to identify latent subgroups with distinct schema-congruence memory profiles.

**Execution Order Constraint:**
1. RQ 5.4.6 must complete Step 4 first (provides random effects)
2. This RQ executes after RQ 5.4.6 completion (uses random effects as clustering features)

**Data Source Boundaries:**
- **RAW data:** None (this RQ does not extract from master.xlsx directly)
- **DERIVED data:** Random effects from RQ 5.4.6 (100 participants x 3 congruence levels x 2 metrics = 6 clustering features per participant)
- **Scope:** This RQ performs clustering on random effects (does NOT re-run LMM or IRT analyses)

**Validation:**
- Step 0: Check results/ch5/5.4.6/data/step04_random_effects.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Verify file contains 300 rows (100 UID x 3 congruence levels) with columns UID, congruence, Total_Intercept, Total_Slope
- If file missing or incomplete -> quit with error -> user must execute RQ 5.4.6 first

**Reference:** Specification section 5.1.6 (Data Source Boundaries)

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tool_inventory.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Extract and Reshape Random Effects

**Analysis Tool:** (determined by rq_tools - likely pandas pivot or custom reshape function)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure + validate_missing_data)

**What Validation Checks:**
- Output file exists (data/step00_random_effects_from_rq546.csv)
- Expected column count (7: UID + 6 features)
- Expected row count (100 participants)
- No NaN values (complete data for all participants and features)
- No duplicate UIDs (each participant appears exactly once)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 87")
- Log failure to logs/step00_extract_data.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Standardize Features

**Analysis Tool:** (determined by rq_tools - likely custom standardization function or sklearn StandardScaler)
**Validation Tool:** (determined by rq_tools - likely validate_standardization)

**What Validation Checks:**
- Output file exists (data/step01_standardized_features.csv)
- Expected row count (100, unchanged from input)
- Mean ~ 0 for all features (tolerance: [-0.1, 0.1])
- SD ~ 1 for all features (tolerance: [0.9, 1.1])
- No NaN values introduced during standardization

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Feature Common_Intercept_z has mean=0.5, expected ~ 0")
- Log failure to logs/step01_standardize_features.log
- Quit script immediately
- g_debug invoked to diagnose (common causes: constant feature, numerical precision issues)

---

#### Step 2: Cluster Model Selection

**Analysis Tool:** (determined by rq_tools - likely sklearn KMeans + custom BIC computation)
**Validation Tool:** (determined by rq_tools - likely custom BIC validation checking monotonicity and boundary conditions)

**What Validation Checks:**
- Output file exists (data/step02_cluster_selection.csv with 6 rows)
- Inertia monotonically decreasing with K (larger K reduces within-cluster variance)
- BIC has minimum within K=1-6 range (not at boundary K=1 or K=6)
- Optimal K in {2, 3, 4, 5} (boundary values suggest misspecification)
- No NaN values in inertia or BIC

**Expected Behavior on Validation Failure:**
- If optimal K at boundary (K=1 or K=6): Log warning, proceed with caution (results may indicate poor cluster structure)
- If BIC computation fails: Raise error, quit, invoke g_debug
- If inertia not monotonic: Raise error (algorithm failure), quit, invoke g_debug

---

#### Step 3: Fit Final K-means

**Analysis Tool:** (determined by rq_tools - likely sklearn KMeans)
**Validation Tool:** (determined by rq_tools - likely validate_cluster_assignment)

**What Validation Checks:**
- Output files exist (cluster_assignments.csv, cluster_centers.csv)
- Cluster assignments in {0, 1, ..., K-1} (consecutive integers)
- Each cluster has >= 10 participants (10% size constraint)
- No missing cluster IDs (0 to K-1 all represented)
- No NaN values in cluster centers

**Expected Behavior on Validation Failure:**
- If cluster size < 10: Raise error, quit, invoke g_debug
- If missing cluster IDs: Raise error (algorithm failure), quit, invoke g_debug
- If NaN in centers: Raise error (numerical issue), quit, invoke g_debug

---

#### Step 4: Validate Clustering Quality

**Analysis Tool:** (determined by rq_tools - likely sklearn metrics + custom bootstrap function)
**Validation Tool:** (determined by rq_tools - likely validate_bootstrap_stability + custom threshold checkers)

**What Validation Checks:**
- Silhouette score >= 0.40 (acceptable cluster cohesion)
- Davies-Bouldin index < 1.5 (acceptable cluster separation)
- Bootstrap Jaccard coefficient > 0.75 (stable clustering)
- No NaN values in metric computations

**Expected Behavior on Validation Failure:**
- If silhouette < 0.40: Log warning, proceed with caution (report tentative clusters)
- If DB >= 1.5: Log warning, proceed with caution
- If Jaccard < 0.75: Log warning, proceed with caution (unstable clustering)
- If bootstrap fails: Raise error, quit, invoke g_debug
- Note: Quality metric failures are WARNINGS, not errors (clustering proceeds, but results interpreted as tentative)

---

#### Step 5: Characterize Clusters

**Analysis Tool:** (determined by rq_tools - likely custom back-transformation + summary statistics function)
**Validation Tool:** (determined by rq_tools - likely validate_cluster_summary_stats)

**What Validation Checks:**
- Output files exist (cluster_centers_original_scale.csv, cluster_summary_stats.csv)
- Summary stats consistent: min <= mean <= max, SD >= 0
- Cluster sizes N >= 10 (consistent with Step 3)
- All K clusters characterized (no missing clusters)
- No NaN values in centers or summary stats

**Expected Behavior on Validation Failure:**
- If min > mean or mean > max: Raise error (statistical inconsistency), quit, invoke g_debug
- If SD < 0: Raise error (computation error), quit, invoke g_debug
- If N < 10: Raise error (violates cluster size constraint), quit, invoke g_debug

---

#### Step 6: Prepare Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas merge + custom aggregation function)
**Validation Tool:** (determined by rq_tools - likely validate_plot_data_completeness)

**What Validation Checks:**
- Output file exists (step06_scatter_matrix_plot_data.csv)
- Expected row count (100 + K: participants + cluster centers)
- All K clusters represented (both in participant data and center rows)
- No NaN values in cluster, cluster_label, or z-scored features
- No duplicate UIDs in participant rows

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 103 rows, found 100")
- Log failure to logs/step06_prepare_plot_data.log
- Quit script immediately
- g_debug invoked to diagnose

---

## Summary

**Total Steps:** 7 (Step 0 through Step 6)
**Estimated Runtime:** Low to Medium (~10-20 minutes total: Step 0-1-3-5-6 low, Step 2 medium, Step 4 medium due to bootstrap)
**Cross-RQ Dependencies:** RQ 5.4.6 (provides random effects for clustering)
**Primary Outputs:**
  - Cluster assignments (100 participants assigned to K clusters)
  - Cluster centers (K cluster profiles in original scale with interpretive labels)
  - Quality metrics (silhouette, Davies-Bouldin, Jaccard stability)
  - Plot source CSV (scatter plot matrix data ready for rq_plots)
**Validation Coverage:** 100% (all 7 steps have validation requirements)

**Key Decisions:**
- K-means selected over LPA (exploratory nature, interpretability, computational efficiency, sample size considerations)
- BIC model selection (K=1-6 range, empirical determination of cluster number)
- Quality thresholds: Silhouette >= 0.40, Davies-Bouldin < 1.5, Jaccard > 0.75
- Cluster size constraint: Each cluster >= 10% of sample (N >= 10)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-02): Initial plan created by rq_planner agent for RQ 5.4.7 (Schema-Based Clustering)
