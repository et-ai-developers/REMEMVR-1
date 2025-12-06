# Analysis Plan: RQ 6.8.4 - Source-Destination Confidence Clustering

**Research Question:** 6.8.4
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ performs K-means clustering on source-destination confidence random effects to test whether the exceptional clustering quality found for accuracy in Ch5 5.5.7 (Silhouette = 0.417) replicates for confidence data. The analysis uses 4 random effect features per participant (source intercept, source slope, destination intercept, destination slope) extracted from RQ 6.8.3's location-stratified LMMs.

**Pipeline:** Unsupervised machine learning (K-means clustering)
**Steps:** 8 analysis steps
**Estimated Runtime:** Low (~5-10 minutes total - mostly data manipulation and clustering algorithms)

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting for chi-square association test with Ch5 5.5.7 (uncorrected + Bonferroni)

**Critical Comparison:** This RQ directly tests whether source-destination dissociation extends from accuracy (Ch5 5.5.7, Silhouette = 0.417) to confidence (this RQ). If confidence clustering achieves Silhouette >= 0.40, source-destination is genuinely special for individual differences in both memory and metacognition.

---

## Analysis Plan

### Step 0: Reshape Random Effects Data

**Dependencies:** None (first step, loads from RQ 6.8.3)
**Complexity:** Low (data reshaping only)

**Input:**

**File 1:** results/ch6/6.8.3/data/step04_random_effects.csv
**Source:** RQ 6.8.3 Step 4 (location-stratified LMM random effects)
**Format:** CSV with 200 rows (100 participants x 2 location types)
**Columns:**
  - `UID` (string, participant identifier, format: P###)
  - `location_type` (string, values: {source, destination})
  - `intercept` (float, random intercept for participant-location combination)
  - `slope` (float, random slope for participant-location combination)
**Expected Rows:** 200 (100 participants x 2 locations)

**Processing:**

Reshape from long format (200 rows, 2 location types per participant) to wide format (100 rows, 4 features per participant):

1. Filter location_type = "source" -> extract intercept and slope
2. Filter location_type = "destination" -> extract intercept and slope
3. Merge on UID to create 4-column feature matrix per participant
4. Rename columns to: Source_intercept, Source_slope, Destination_intercept, Destination_slope

**Output:**

**File 1:** data/step00_clustering_input.csv
**Format:** CSV, wide format (one row per participant)
**Columns:**
  - `UID` (string, participant identifier)
  - `Source_intercept` (float, source random intercept)
  - `Source_slope` (float, source random slope)
  - `Destination_intercept` (float, destination random intercept)
  - `Destination_slope` (float, destination random slope)
**Expected Rows:** 100 (one per participant)
**Expected Columns:** 5 (UID + 4 features)

**Validation Requirement:**

Validation tools MUST be used after data reshaping execution. Specific validation tools will be determined by rq_tools based on data transformation validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_clustering_input.csv: 100 rows x 5 columns (UID: object, 4 features: float64)

*Value Ranges:*
- All feature values finite (no NaN, no inf)
- Intercepts unrestricted range (confidence scale can be negative or positive)
- Slopes unrestricted range (can be positive, negative, or near-zero)

*Data Quality:*
- All 100 participants present (no data loss from RQ 6.8.3)
- No NaN values (all random effects estimated for all participants)
- No duplicate UIDs

*Log Validation:*
- Required pattern: "Reshaped 200 rows -> 100 rows (2 locations -> 4 features per participant)"
- Required pattern: "All 100 participants matched between source and destination"
- Forbidden patterns: "ERROR", "Missing location_type", "Unmatched UID"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 100 rows, found 87")
- Log failure to logs/step00_reshape_random_effects.log
- Quit immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose data loss

---

### Step 1: Standardize Features

**Dependencies:** Step 0 (requires clustering input)
**Complexity:** Low (standardization only)

**Input:**

**File:** data/step00_clustering_input.csv
**Format:** 100 rows x 5 columns (UID + 4 features)
**Required Columns:** Source_intercept, Source_slope, Destination_intercept, Destination_slope

**Processing:**

Z-score standardization for all 4 features to ensure equal weighting in K-means:
1. Compute mean and SD for each feature across N=100 participants
2. Transform: z = (x - mean) / SD
3. Verify: mean approximately 0, SD approximately 1 for each standardized feature
4. Retain UID column (not standardized)

**Output:**

**File:** data/step01_standardized_features.csv
**Format:** CSV, 100 rows x 5 columns
**Columns:**
  - `UID` (string, unchanged)
  - `Source_intercept_z` (float, z-score)
  - `Source_slope_z` (float, z-score)
  - `Destination_intercept_z` (float, z-score)
  - `Destination_slope_z` (float, z-score)
**Expected Rows:** 100

**Validation Requirement:**

Validation tools MUST be used after standardization execution. Specific validation tools will be determined by rq_tools based on standardization validation requirements (likely validate_standardization from tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_standardized_features.csv: 100 rows x 5 columns (UID: object, 4 z-scores: float64)

*Value Ranges:*
- All z-scores finite (no NaN, no inf)
- Mean of each z-score column in [-0.01, 0.01] (approximately 0)
- SD of each z-score column in [0.99, 1.01] (approximately 1)

*Data Quality:*
- All 100 participants present
- No NaN values
- No duplicate UIDs

*Log Validation:*
- Required pattern: "Standardized 4 features: mean approximately 0, SD approximately 1"
- Required pattern: "VALIDATION - PASS: standardization"
- Forbidden patterns: "ERROR", "NaN in standardized features", "VALIDATION - FAIL"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Feature Source_intercept_z has mean = 0.52, expected approximately 0")
- Log failure to logs/step01_standardize_features.log
- Quit immediately
- g_debug invoked

---

### Step 2: K-Means Cluster Selection (BIC)

**Dependencies:** Step 1 (requires standardized features)
**Complexity:** Low (clustering algorithm, fast for N=100)

**Input:**

**File:** data/step01_standardized_features.csv
**Format:** 100 rows x 5 columns (UID + 4 z-scores)
**Features Used:** 4 z-score columns (exclude UID column from clustering)

**Processing:**

K-means cluster selection using BIC for K=1 to K=6:
1. For each K in {1, 2, 3, 4, 5, 6}:
   - Fit K-means with random_state=42 (reproducibility)
   - Compute inertia (within-cluster sum of squares)
   - Compute BIC = N * log(inertia/N) + K * log(N) * 4 (where 4 = number of features)
2. Identify optimal K via BIC minimum
3. Expect K=4 based on Ch5 5.5.7 findings

**Output:**

**File:** data/step02_cluster_selection.csv
**Format:** CSV, 6 rows (one per K value)
**Columns:**
  - `K` (int, values: {1, 2, 3, 4, 5, 6})
  - `inertia` (float, within-cluster SS)
  - `BIC` (float, Bayesian Information Criterion)
  - `optimal` (bool, True for K with minimum BIC)
**Expected Rows:** 6

**Validation Requirement:**

Validation tools MUST be used after cluster selection execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cluster_selection.csv: 6 rows x 4 columns (K: int, inertia: float64, BIC: float64, optimal: bool)

*Value Ranges:*
- K in {1, 2, 3, 4, 5, 6} (all values represented)
- Inertia > 0, finite
- BIC finite
- Exactly one row with optimal = True

*Data Quality:*
- All 6 K values present (no missing)
- No NaN in inertia or BIC columns
- Inertia decreases monotonically as K increases (more clusters -> lower within-cluster variance)

*Log Validation:*
- Required pattern: "BIC minimum at K = [number]"
- Required pattern: "Optimal K selected: [number]"
- Forbidden patterns: "ERROR", "BIC contains NaN", "No optimal K found"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step02_cluster_selection.log
- Quit immediately
- g_debug invoked

---

### Step 3: Fit Final K-Means Clustering

**Dependencies:** Step 2 (requires optimal K)
**Complexity:** Low (single K-means fit)

**Input:**

**File 1:** data/step01_standardized_features.csv (100 rows x 5 columns)
**File 2:** data/step02_cluster_selection.csv (optimal K value identified)

**Processing:**

1. Read optimal K from step02_cluster_selection.csv (expect K=4)
2. Fit final K-means with:
   - n_clusters = optimal K
   - random_state = 42 (reproducibility)
   - Features: 4 z-score columns
3. Extract cluster assignments (labels) for each participant

**Output:**

**File:** data/step03_cluster_assignments.csv
**Format:** CSV, 100 rows
**Columns:**
  - `UID` (string, participant identifier)
  - `cluster` (int, cluster assignment 0 to K-1)
**Expected Rows:** 100

**Validation Requirement:**

Validation tools MUST be used after K-means fitting execution. Specific validation tools will be determined by rq_tools (likely validate_cluster_assignment from tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_cluster_assignments.csv: 100 rows x 2 columns (UID: object, cluster: int)

*Value Ranges:*
- Cluster labels in {0, 1, ..., K-1} (consecutive integers)
- All cluster IDs represented (no empty clusters)

*Data Quality:*
- All 100 participants present
- No NaN in cluster column
- No duplicate UIDs
- All cluster sizes >= 10% of N (minimum 10 participants per cluster, no tiny clusters)

*Log Validation:*
- Required pattern: "Fitted K-means with K = [number] clusters"
- Required pattern: "Cluster sizes: [list of sizes]"
- Required pattern: "All clusters >= 10% of N"
- Forbidden patterns: "ERROR", "Empty cluster detected", "Cluster size < 10"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 3 has only 4 participants, minimum 10 required")
- Log failure to logs/step03_fit_final_kmeans.log
- Quit immediately
- g_debug invoked

---

### Step 4: Validate Clustering Quality

**Dependencies:** Step 3 (requires cluster assignments)
**Complexity:** Low (quality metric computation)

**Input:**

**File 1:** data/step01_standardized_features.csv (100 rows, 4 z-score features)
**File 2:** data/step03_cluster_assignments.csv (100 rows, cluster labels)

**Processing:**

Compute three clustering quality metrics:

1. **Silhouette Coefficient:**
   - Measures cluster cohesion vs separation
   - Range: [-1, 1], higher is better
   - Threshold: >= 0.40 for good quality (Ch5 5.5.7 = 0.417)

2. **Davies-Bouldin Index:**
   - Measures cluster similarity (lower is better)
   - Range: [0, inf), values < 1.0 indicate good separation

3. **Jaccard Bootstrap Stability:**
   - Measures cluster stability across 100 bootstrap samples
   - Range: [0, 1], higher is better
   - Threshold: > 0.70 for robust clusters

**Output:**

**File:** data/step04_validation.csv
**Format:** CSV, 3 rows (one per metric)
**Columns:**
  - `metric` (string, values: {Silhouette, Davies_Bouldin, Jaccard})
  - `value` (float, metric value)
  - `threshold` (float, quality threshold)
  - `pass` (bool, value meets threshold)
**Expected Rows:** 3

**Validation Requirement:**

Validation tools MUST be used after quality metric computation. Specific validation tools will be determined by rq_tools (likely validate_bootstrap_stability from tools_catalog.md for Jaccard metric).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_validation.csv: 3 rows x 4 columns (metric: object, value: float64, threshold: float64, pass: bool)

*Value Ranges:*
- Silhouette in [-1, 1]
- Davies_Bouldin >= 0
- Jaccard in [0, 1]

*Data Quality:*
- All 3 metrics present
- No NaN values
- All values finite

*Log Validation:*
- Required pattern: "Silhouette coefficient: [value] (threshold >= 0.40)"
- Required pattern: "Davies-Bouldin index: [value] (threshold < 1.0)"
- Required pattern: "Jaccard stability: [value] (threshold > 0.70)"
- Forbidden patterns: "ERROR", "NaN metric", "Bootstrap failed"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step04_validate_clustering_quality.log
- Quit immediately
- g_debug invoked

---

### Step 5: Characterize Clusters

**Dependencies:** Step 3 (requires cluster assignments)
**Complexity:** Low (descriptive statistics)

**Input:**

**File 1:** data/step00_clustering_input.csv (100 rows, 4 raw features - unstandardized for interpretability)
**File 2:** data/step03_cluster_assignments.csv (100 rows, cluster labels)

**Processing:**

For each cluster (0 to K-1):
1. Compute mean, SD, min, max for each of 4 features
2. Compute N (cluster size)
3. Identify cluster phenotype based on mean feature values:
   - High/Low source intercept (starting confidence for source memory)
   - Positive/Negative source slope (improvement vs decline)
   - High/Low destination intercept (starting confidence for destination memory)
   - Positive/Negative destination slope (improvement vs decline)

**Output:**

**File:** data/step05_cluster_characterization.csv
**Format:** CSV, K rows (one per cluster)
**Columns:**
  - `cluster` (int, 0 to K-1)
  - `N` (int, cluster size)
  - For each feature: `{feature}_mean`, `{feature}_SD`, `{feature}_min`, `{feature}_max`
  - `phenotype` (string, interpretive label)
**Expected Rows:** K (expect 4 based on Ch5 5.5.7)

**Validation Requirement:**

Validation tools MUST be used after cluster characterization. Specific validation tools will be determined by rq_tools (likely validate_cluster_summary_stats from tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cluster_characterization.csv: K rows x ~18 columns (cluster: int, N: int, 4 features x 4 stats each + phenotype: object)

*Value Ranges:*
- N > 0 for all clusters
- min <= mean <= max for all features
- SD >= 0 for all features

*Data Quality:*
- All K clusters represented
- No NaN in summary statistics
- Phenotype labels assigned (not empty strings)

*Log Validation:*
- Required pattern: "Characterized [K] clusters"
- Required pattern: "Cluster sizes range: [min] to [max]"
- Forbidden patterns: "ERROR", "NaN in summary stats", "Empty phenotype"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step05_characterize_clusters.log
- Quit immediately
- g_debug invoked

---

### Step 6: Cross-Tabulate with Ch5 5.5.7 Accuracy Clusters

**Dependencies:** Step 3 (requires confidence cluster assignments)
**Complexity:** Low (cross-tabulation and chi-square test)

**Input:**

**File 1:** data/step03_cluster_assignments.csv (100 rows, confidence cluster labels from this RQ)
**File 2:** results/ch5/5.5.7/data/step03_cluster_assignments.csv (100 rows, accuracy cluster labels from Ch5 5.5.7)

**Processing:**

1. Merge confidence and accuracy cluster assignments on UID
2. Create cross-tabulation (contingency table):
   - Rows: Confidence clusters (this RQ)
   - Columns: Accuracy clusters (Ch5 5.5.7)
   - Cells: Count of participants in each combination
3. Compute chi-square test of association:
   - Null hypothesis: Cluster assignments independent
   - Alternative: Association between confidence and accuracy phenotypes
   - Report BOTH uncorrected p-value AND Bonferroni-corrected p-value (Decision D068)

**Output:**

**File 1:** data/step06_crosstab.csv
**Format:** CSV, contingency table (K_confidence rows x K_accuracy columns + margins)

**File 2:** data/step06_chi_square.csv
**Format:** CSV, 1 row with test results
**Columns:**
  - `chi_square` (float, test statistic)
  - `df` (int, degrees of freedom)
  - `p_uncorrected` (float, uncorrected p-value)
  - `p_bonferroni` (float, Bonferroni-corrected p-value)
  - `significant_uncorrected` (bool, p < 0.05)
  - `significant_bonferroni` (bool, p_bonferroni < 0.05)
**Expected Rows:** 1

**Validation Requirement:**

Validation tools MUST be used after chi-square test execution. Specific validation tools will be determined by rq_tools (likely validate_hypothesis_test_dual_pvalues from tools_catalog.md for Decision D068 compliance).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_crosstab.csv: K_confidence rows x K_accuracy columns (expect 4x4 based on Ch5 5.5.7)
- data/step06_chi_square.csv: 1 row x 6 columns

*Value Ranges:*
- chi_square >= 0
- df > 0
- p_uncorrected in [0, 1]
- p_bonferroni in [0, 1]

*Data Quality:*
- All 100 participants matched between confidence and accuracy files
- Crosstab row sums = K_confidence cluster sizes
- Crosstab column sums = K_accuracy cluster sizes
- Both p-values present (Decision D068 requirement)

*Log Validation:*
- Required pattern: "Chi-square test: X2 = [value], df = [value], p = [value]"
- Required pattern: "VALIDATION - PASS: dual p-values (uncorrected + bonferroni)"
- Forbidden patterns: "ERROR", "Missing p-value", "VALIDATION - FAIL"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step06_crosstab_ch5.log
- Quit immediately
- g_debug invoked

---

### Step 7: Compare Quality Metrics to Ch5 RQs

**Dependencies:** Step 4 (requires clustering quality metrics)
**Complexity:** Low (comparison table creation)

**Input:**

**File 1:** data/step04_validation.csv (this RQ's quality metrics)

**File 2:** Ch5 clustering RQ quality metrics (read from prior RQs):
- results/ch5/5.1.5/data/step04_validation.csv (General clustering)
- results/ch5/5.2.7/data/step04_validation.csv (Domains clustering)
- results/ch5/5.3.8/data/step04_validation.csv (Paradigms clustering)
- results/ch5/5.4.5/data/step04_validation.csv (Congruence clustering)
- results/ch5/5.5.7/data/step04_validation.csv (Source-Dest ACCURACY clustering)

**Processing:**

1. Read Silhouette, Davies-Bouldin, Jaccard, and optimal K from all 6 RQs (5 Ch5 + this RQ)
2. Create comparison table with columns:
   - RQ_ID (e.g., "5.1.5", "5.2.7", ..., "6.8.4")
   - RQ_description (e.g., "General Accuracy", "Source-Dest Accuracy", "Source-Dest Confidence")
   - Data_type (Accuracy vs Confidence)
   - K (optimal number of clusters)
   - Silhouette (quality metric)
   - Davies_Bouldin (separation metric)
   - Jaccard (stability metric)
3. Sort by Silhouette descending to identify best clustering quality

**Output:**

**File:** data/step07_ch5_comparison.csv
**Format:** CSV, 6 rows (5 Ch5 RQs + this RQ)
**Columns:**
  - `RQ_ID` (string)
  - `RQ_description` (string)
  - `Data_type` (string, values: {Accuracy, Confidence})
  - `K` (int, optimal clusters)
  - `Silhouette` (float)
  - `Davies_Bouldin` (float)
  - `Jaccard` (float)
**Expected Rows:** 6

**Validation Requirement:**

Validation tools MUST be used after comparison table creation.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_ch5_comparison.csv: 6 rows x 7 columns

*Value Ranges:*
- K in {2, 3, 4, 5, 6} (typical range)
- Silhouette in [-1, 1]
- Davies_Bouldin >= 0
- Jaccard in [0, 1]

*Data Quality:*
- All 6 RQs represented
- No NaN in metrics columns
- Ch5 5.5.7 row present (critical comparison)
- This RQ (6.8.4) row present

*Log Validation:*
- Required pattern: "Compared 6 clustering RQs (5 Ch5 + this RQ)"
- Required pattern: "Ch5 5.5.7 Silhouette: [value]"
- Required pattern: "RQ 6.8.4 Silhouette: [value]"
- Forbidden patterns: "ERROR", "Missing RQ", "Failed to read Ch5 data"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step07_compare_ch5.log
- Quit immediately
- g_debug invoked

---

### Step 8: Prepare Cluster Visualization Data

**Dependencies:** Step 3 (requires cluster assignments)
**Complexity:** Low (PCA projection for visualization)

**Input:**

**File 1:** data/step01_standardized_features.csv (100 rows, 4 z-scores)
**File 2:** data/step03_cluster_assignments.csv (100 rows, cluster labels)

**Processing:**

1. Apply PCA (Principal Component Analysis) to 4 standardized features
2. Project to 2D (PC1 and PC2) for scatter plot visualization
3. Merge with cluster assignments
4. Save as plot source CSV for rq_plots to generate PNG later

**Output:**

**File:** data/step08_cluster_scatter_data.csv
**Format:** CSV, 100 rows
**Columns:**
  - `UID` (string)
  - `PC1` (float, first principal component)
  - `PC2` (float, second principal component)
  - `cluster` (int, cluster assignment)
**Expected Rows:** 100

**Validation Requirement:**

Validation tools MUST be used after PCA projection execution.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_cluster_scatter_data.csv: 100 rows x 4 columns (UID: object, PC1: float64, PC2: float64, cluster: int)

*Value Ranges:*
- PC1 and PC2 finite (no NaN, no inf)
- Cluster labels in {0, 1, ..., K-1}

*Data Quality:*
- All 100 participants present
- No NaN values
- No duplicate UIDs

*Log Validation:*
- Required pattern: "PCA projection complete: 4D -> 2D"
- Required pattern: "PC1 explains [X]% variance, PC2 explains [Y]% variance"
- Forbidden patterns: "ERROR", "PCA failed", "NaN in PCA projection"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log failure to logs/step08_prepare_cluster_scatter_data.log
- Quit immediately
- g_debug invoked

**Plot Specifications for rq_plots:**

**Plot Description:** Scatter plot of cluster assignments in 2D principal component space with color-coded clusters

**Source CSV Path:** data/step08_cluster_scatter_data.csv

**Required Columns:** PC1, PC2, cluster

**Plotting Function (General):** Scatter plot with cluster color coding

**Note:** rq_plots will read this CSV and generate PNG visualization to plots/ folder. No data aggregation in rq_plots (visualization only per Option B architecture).

---

## Expected Data Formats

### Step 0: Reshaping Transformation (Long -> Wide)

**Input Format (from RQ 6.8.3):**
- File: results/ch6/6.8.3/data/step04_random_effects.csv
- Format: Long (200 rows: 100 participants x 2 location types)
- Columns: `UID`, `location_type`, `intercept`, `slope`

**Transformation Logic:**
1. Pivot on location_type to create separate columns for source and destination
2. Each participant gets 4 columns: Source_intercept, Source_slope, Destination_intercept, Destination_slope

**Output Format:**
- File: data/step00_clustering_input.csv
- Format: Wide (100 rows: one per participant)
- Columns: `UID`, `Source_intercept`, `Source_slope`, `Destination_intercept`, `Destination_slope`

### Column Naming Conventions

Per names.md (v4.X registry):
- **UID:** Participant identifier (format: P### with leading zeros)
- **Feature names:** {Location}_{parameter} format (e.g., Source_intercept, Destination_slope)
- **Standardized features:** Append `_z` suffix (e.g., Source_intercept_z)
- **Cluster assignments:** `cluster` column (int, 0 to K-1)

### Data Type Constraints

**Non-nullable columns:**
- All feature columns (Source_intercept, Source_slope, Destination_intercept, Destination_slope)
- UID column
- Cluster column

**Nullable columns:**
- None (all columns must have valid values)

**Valid Ranges:**
- Random effects: Unrestricted range (can be positive, negative, or zero)
- Z-scores: Mean approximately 0, SD approximately 1
- Cluster labels: {0, 1, ..., K-1} consecutive integers
- Quality metrics: Silhouette in [-1, 1], Davies-Bouldin >= 0, Jaccard in [0, 1]

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

**RQ 6.8.3** (Source-Destination Confidence ICC - location-stratified LMM random effects)
  - File: results/ch6/6.8.3/data/step04_random_effects.csv
  - Used in: Step 0 (reshape to create 4-feature clustering input)
  - Rationale: RQ 6.8.3 fits location-stratified LMMs and extracts random intercepts/slopes per participant per location. This RQ clusters participants based on those 4 random effects (source intercept, source slope, destination intercept, destination slope).

**Ch5 5.5.7** (Source-Dest Accuracy Clustering - for cross-tabulation comparison)
  - File: results/ch5/5.5.7/data/step03_cluster_assignments.csv
  - Used in: Step 6 (cross-tabulate confidence vs accuracy cluster assignments)
  - Rationale: This RQ tests whether exceptional clustering quality found for accuracy (Ch5 5.5.7, Silhouette = 0.417) replicates for confidence. Cross-tabulation determines if confidence and accuracy phenotypes align.

**Ch5 Clustering RQs** (5.1.5, 5.2.7, 5.3.8, 5.4.5 - for quality metric comparison)
  - Files: results/ch5/{5.1.5, 5.2.7, 5.3.8, 5.4.5}/data/step04_validation.csv
  - Used in: Step 7 (compare clustering quality across all Ch5 clustering RQs)
  - Rationale: Provides context for whether source-destination dissociation is genuinely special. Ch5 5.5.7 was the ONLY RQ with Silhouette >= 0.40. Step 7 tests if confidence clustering also achieves this threshold.

**Execution Order Constraint:**
1. RQ 6.8.3 must complete Step 4 first (provides random effects)
2. Ch5 5.5.7 must be complete (provides accuracy cluster assignments)
3. Ch5 clustering RQs (5.1.5, 5.2.7, 5.3.8, 5.4.5) must be complete (provides quality metrics)
4. This RQ executes after all dependencies complete

**Data Source Boundaries:**
- **DERIVED data:** All inputs are from other RQ outputs (no master.xlsx extraction)
- **Scope:** This RQ does NOT re-fit LMMs (uses RQ 6.8.3 random effects as fixed)

**Validation:**
- Step 0: Check results/ch6/6.8.3/data/step04_random_effects.csv exists (circuit breaker: FILE_MISSING if absent)
- Step 6: Check results/ch5/5.5.7/data/step03_cluster_assignments.csv exists
- Step 7: Check results/ch5/{5.1.5, 5.2.7, 5.3.8, 5.4.5}/data/step04_validation.csv exist
- If any file missing -> quit with error -> user must execute dependency RQs first

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

#### Step 0: Reshape Random Effects Data

**Analysis Tool:** (determined by rq_tools - likely pandas pivot/merge operations)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step00_clustering_input.csv)
- Expected row count (100 participants, no data loss from RQ 6.8.3)
- Expected column count (5 columns: UID + 4 features)
- No NaN values (all random effects estimated)
- All UIDs matched between source and destination location types

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step00_reshape_random_effects.log
- Quit immediately
- g_debug invoked

---

#### Step 1: Standardize Features

**Analysis Tool:** (determined by rq_tools - likely tools.validation.validate_standardization or sklearn.preprocessing.StandardScaler)
**Validation Tool:** (determined by rq_tools - likely validate_standardization from tools_catalog.md)

**What Validation Checks:**
- Mean of each z-score column approximately 0 (tolerance +/- 0.01)
- SD of each z-score column approximately 1 (tolerance +/- 0.01)
- No NaN values
- All 100 participants present

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step01_standardize_features.log
- Quit immediately
- g_debug invoked

---

#### Step 2: K-Means Cluster Selection (BIC)

**Analysis Tool:** (determined by rq_tools - likely sklearn.cluster.KMeans with custom BIC computation)
**Validation Tool:** (determined by rq_tools - likely validate_numeric_range)

**What Validation Checks:**
- All K values {1, 2, 3, 4, 5, 6} present
- BIC finite for all K (no NaN, no inf)
- Inertia decreases monotonically as K increases
- Exactly one optimal K identified

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step02_cluster_selection.log
- Quit immediately
- g_debug invoked

---

#### Step 3: Fit Final K-Means Clustering

**Analysis Tool:** (determined by rq_tools - likely sklearn.cluster.KMeans)
**Validation Tool:** (determined by rq_tools - likely validate_cluster_assignment from tools_catalog.md)

**What Validation Checks:**
- Cluster labels consecutive {0, 1, ..., K-1}
- All K clusters represented (no empty clusters)
- All cluster sizes >= 10% of N=100 (minimum 10 participants per cluster)
- No NaN in cluster column

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step03_fit_final_kmeans.log
- Quit immediately
- g_debug invoked

---

#### Step 4: Validate Clustering Quality

**Analysis Tool:** (determined by rq_tools - likely sklearn.metrics.silhouette_score, davies_bouldin_score, custom Jaccard bootstrap)
**Validation Tool:** (determined by rq_tools - likely validate_bootstrap_stability from tools_catalog.md)

**What Validation Checks:**
- Silhouette in [-1, 1]
- Davies_Bouldin >= 0
- Jaccard in [0, 1]
- Bootstrap completed successfully (100 iterations)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step04_validate_clustering_quality.log
- Quit immediately
- g_debug invoked

---

#### Step 5: Characterize Clusters

**Analysis Tool:** (determined by rq_tools - likely pandas.groupby with descriptive statistics)
**Validation Tool:** (determined by rq_tools - likely validate_cluster_summary_stats from tools_catalog.md)

**What Validation Checks:**
- min <= mean <= max for all features
- SD >= 0 for all features
- N > 0 for all clusters
- Phenotype labels assigned (not empty)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step05_characterize_clusters.log
- Quit immediately
- g_debug invoked

---

#### Step 6: Cross-Tabulate with Ch5 5.5.7

**Analysis Tool:** (determined by rq_tools - likely pandas.crosstab + scipy.stats.chi2_contingency)
**Validation Tool:** (determined by rq_tools - likely validate_hypothesis_test_dual_pvalues from tools_catalog.md for Decision D068)

**What Validation Checks:**
- All 100 participants matched between confidence and accuracy files
- Crosstab row/column sums match cluster sizes
- Both p-values present (uncorrected + Bonferroni per Decision D068)
- Chi-square statistic >= 0

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step06_crosstab_ch5.log
- Quit immediately
- g_debug invoked

---

#### Step 7: Compare Quality Metrics to Ch5 RQs

**Analysis Tool:** (determined by rq_tools - likely pandas.concat to merge quality metrics)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure)

**What Validation Checks:**
- All 6 RQs represented (5 Ch5 + this RQ)
- No NaN in metrics columns
- Ch5 5.5.7 row present (critical comparison)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step07_compare_ch5.log
- Quit immediately
- g_debug invoked

---

#### Step 8: Prepare Cluster Visualization Data

**Analysis Tool:** (determined by rq_tools - likely sklearn.decomposition.PCA)
**Validation Tool:** (determined by rq_tools - likely validate_dataframe_structure)

**What Validation Checks:**
- PCA projection successful (no NaN in PC1, PC2)
- All 100 participants present
- Cluster labels valid

**Expected Behavior on Validation Failure:**
- Raise error with specific failure
- Log to logs/step08_prepare_cluster_scatter_data.log
- Quit immediately
- g_debug invoked

---

## Summary

**Total Steps:** 8 (Step 0 - Step 7 analysis + Step 8 plot data preparation)
**Estimated Runtime:** Low (~5-10 minutes total - clustering algorithms fast for N=100)
**Cross-RQ Dependencies:** RQ 6.8.3 (random effects), Ch5 5.5.7 (accuracy clusters), Ch5 clustering RQs (quality metrics)
**Primary Outputs:**
  - data/step03_cluster_assignments.csv (confidence cluster phenotypes for N=100)
  - data/step04_validation.csv (Silhouette, Davies-Bouldin, Jaccard quality metrics)
  - data/step06_chi_square.csv (association test with Ch5 5.5.7 accuracy clusters)
  - data/step07_ch5_comparison.csv (quality comparison across 6 clustering RQs)
  - data/step08_cluster_scatter_data.csv (plot source CSV for PCA visualization)
**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent
