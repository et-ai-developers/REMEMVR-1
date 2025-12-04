# Analysis Plan: RQ 5.5.7 - Source-Destination Clustering

**Research Question:** 5.5.7
**Created:** 2025-12-04
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ examines whether participants can be grouped into latent classes based on source (pick-up location -U-) and destination (put-down location -D-) memory patterns using K-means clustering on 4 features: Source_intercept, Source_slope, Destination_intercept, Destination_slope. The features are extracted from RQ 5.5.6 variance decomposition random effects.

**Pipeline:** K-means clustering with BIC model selection and triple validation (Silhouette, Davies-Bouldin, Jaccard bootstrap)

**Steps:** 7 total analysis steps (Step 0: Load data + Steps 1-6: Standardization, Model Selection, Validation, Cluster Assignment, Characterization, Visualization)

**Estimated Runtime:** Low (all clustering steps <5 minutes, no iterative model fitting)

**Key Decisions Applied:**
- No IRT/LMM decisions (clustering-only RQ)
- Follows universal Chapter 5 clustering pattern (weak quality, stable groupings expected per RQ 5.1.5, 5.2.7, 5.3.8, 5.4.7)

**Theoretical Context:**
This is the final RQ in the systematic clustering series across Chapter 5. Prior RQs established the pattern: memory ability is continuous (weak clustering quality: Silhouette < 0.40), but K-means can partition participants into stable, interpretable groupings (Jaccard > 0.60). This RQ tests whether the pattern replicates for source-destination memory, and whether source-destination dissociation (per RQ 5.5.1) creates location-specific profiles.

---

## Analysis Plan

This RQ requires 7 steps:

### Step 0: Load Random Effects from RQ 5.5.6

**Dependencies:** None (first step, but requires RQ 5.5.6 completion)

**Complexity:** Low (data loading and reshaping only)

**Purpose:** Load random effects from RQ 5.5.6 and reshape from 200 rows (100 UID x 2 location types) to 100 rows x 4 features (Source_intercept, Source_slope, Destination_intercept, Destination_slope).

**Input:**

**File:** results/ch5/5.5.6/data/step04_random_effects.csv
**Source:** RQ 5.5.6 variance decomposition (location-stratified LMMs)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, e.g., P001)
  - `location_type` (string, values: {Source, Destination})
  - `Total_Intercept` (float, random intercept per participant per location type)
  - `Total_Slope` (float, random slope per participant per location type)
**Expected Rows:** 200 (100 UID x 2 location types)
**Expected Values:**
  - Total_Intercept: theta scale (typically [-2, 2])
  - Total_Slope: theta/day scale (typically [-0.5, 0.5], likely near 0 per ICC_slope pattern)

**Dependency Check:**
- Verify results/ch5/5.5.6/status.yaml shows rq_results: success
- If RQ 5.5.6 incomplete, QUIT with EXPECTATIONS ERROR

**Processing:**

1. Load results/ch5/5.5.6/data/step04_random_effects.csv
2. Validate structure: 200 rows, 4 columns (UID, location_type, Total_Intercept, Total_Slope)
3. Reshape wide: Pivot on location_type to create 4 feature columns
   - Source_intercept (from location_type=Source, Total_Intercept)
   - Source_slope (from location_type=Source, Total_Slope)
   - Destination_intercept (from location_type=Destination, Total_Intercept)
   - Destination_slope (from location_type=Destination, Total_Slope)
4. Validate reshaping: 100 rows (one per UID), 5 columns (UID + 4 features)
5. Check for missing values (no NaN tolerated)

**Output:**

**File:** data/step00_random_effects_from_rq556.csv
**Format:** CSV, wide format (one row per participant)
**Columns:**
  - `UID` (string, participant identifier, e.g., P001)
  - `Source_intercept` (float, baseline source memory at Day 0)
  - `Source_slope` (float, source memory forgetting rate)
  - `Destination_intercept` (float, baseline destination memory at Day 0)
  - `Destination_slope` (float, destination memory forgetting rate)
**Expected Rows:** 100 (one per participant)
**Expected Columns:** 5 (UID + 4 features)

**Validation Requirement:**
Validation tools MUST be used after data loading and reshaping. Specific validation tools will be determined by rq_tools based on data format requirements (CSV structure validation, missing data checks, reshape correctness).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_random_effects_from_rq556.csv exists (exact path)
- Expected rows: 100 (one per participant)
- Expected columns: 5 (UID, Source_intercept, Source_slope, Destination_intercept, Destination_slope)
- Data types: UID (object/string), all features (float64)

*Value Ranges:*
- Source_intercept in [-3, 3] (theta scale, typical range [-2, 2])
- Source_slope in [-1, 1] (theta/day scale, likely near 0)
- Destination_intercept in [-3, 3] (theta scale, typical range [-2, 2])
- Destination_slope in [-1, 1] (theta/day scale, likely near 0)

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 100 rows (no missing participants)
- No duplicate UIDs (unique participants)
- All UIDs match RQ 5.5.6 participant set

*Log Validation:*
- Required pattern: "Loaded 200 rows from RQ 5.5.6"
- Required pattern: "Reshaped to 100 rows x 4 features"
- Required pattern: "No missing values detected"
- Forbidden patterns: "ERROR", "NaN values detected", "Reshaping failed"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 97")
- Log failure to logs/step00_load_random_effects.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause

---

### Step 1: Standardize Features to Z-Scores

**Dependencies:** Step 0 (requires random effects loaded)

**Complexity:** Low (standardization computation only)

**Purpose:** Standardize all 4 features to z-scores (mean=0, SD=1) to equalize scale across intercepts and slopes. This is critical because intercepts (theta scale H [-2, 2]) and slopes (theta/day scale H [-0.5, 0.5]) are on different scales. Without standardization, clustering would be dominated by intercepts.

**Input:**

**File:** data/step00_random_effects_from_rq556.csv (from Step 0)
**Format:** CSV with 100 rows x 5 columns (UID + 4 features)
**Required Columns:**
  - `UID` (string)
  - `Source_intercept` (float)
  - `Source_slope` (float)
  - `Destination_intercept` (float)
  - `Destination_slope` (float)

**Processing:**

1. Load data/step00_random_effects_from_rq556.csv
2. For each of the 4 features:
   - Compute mean (mu) and standard deviation (sigma)
   - Transform: z = (x - mu) / sigma
   - Verify: mean(z) H 0, SD(z) H 1 (within sampling tolerance)
3. Retain UID column unchanged
4. Save standardized features

**Output:**

**File:** data/step01_standardized_features.csv
**Format:** CSV with 100 rows x 5 columns (UID + 4 z-scored features)
**Columns:**
  - `UID` (string, unchanged from input)
  - `Source_intercept` (float, z-scored: mean H 0, SD H 1)
  - `Source_slope` (float, z-scored: mean H 0, SD H 1)
  - `Destination_intercept` (float, z-scored: mean H 0, SD H 1)
  - `Destination_slope` (float, z-scored: mean H 0, SD H 1)
**Expected Rows:** 100
**Expected Columns:** 5

**Validation Requirement:**
Validation tools MUST be used after standardization. Specific validation tools will be determined by rq_tools based on standardization requirements (z-score verification: mean H 0, SD H 1).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_standardized_features.csv exists (exact path)
- Expected rows: 100
- Expected columns: 5 (UID + 4 features)
- Data types: UID (object/string), all features (float64)

*Value Ranges:*
- All z-scored features: typical range [-3, 3] (extreme outliers possible but rare)
- Mean per feature: [-0.1, 0.1] (sampling tolerance around 0)
- SD per feature: [0.9, 1.1] (sampling tolerance around 1)

*Data Quality:*
- No NaN values tolerated
- Expected N: Exactly 100 rows (no data loss during standardization)
- No duplicate UIDs
- All UIDs match Step 0 input

*Log Validation:*
- Required pattern: "Standardized 4 features to z-scores"
- Required pattern: "Mean check: all features in [-0.1, 0.1]" (or similar mean verification)
- Required pattern: "SD check: all features in [0.9, 1.1]" (or similar SD verification)
- Forbidden patterns: "ERROR", "NaN after standardization", "Division by zero"
- Acceptable warnings: None expected for standardization

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Feature Source_intercept has mean=0.5, expected H 0")
- Log failure to logs/step01_standardize_features.log
- Quit script immediately (do NOT proceed to Step 2)
- g_debug invoked to diagnose root cause

---

### Step 2: K-Means Model Selection (K=1 to K=6)

**Dependencies:** Step 1 (requires standardized features)

**Complexity:** Low (K-means fitting is fast, 6 models tested)

**Purpose:** Test K=1 to K=6 using K-means clustering, compute inertia and BIC for each K, select optimal K as BIC minimum (or K-1 if BIC minimum at boundary K=6).

**Input:**

**File:** data/step01_standardized_features.csv (from Step 1)
**Format:** CSV with 100 rows x 5 columns (UID + 4 z-scored features)
**Required Columns:**
  - `UID` (string)
  - `Source_intercept` (float, z-scored)
  - `Source_slope` (float, z-scored)
  - `Destination_intercept` (float, z-scored)
  - `Destination_slope` (float, z-scored)

**Processing:**

1. Load data/step01_standardized_features.csv
2. Extract feature matrix X (100 rows x 4 columns, exclude UID)
3. For K in {1, 2, 3, 4, 5, 6}:
   - Fit K-means: sklearn.cluster.KMeans(n_clusters=K, random_state=42, n_init=50)
   - Extract inertia (within-cluster sum of squares)
   - Compute BIC: BIC = inertia + K * log(N) * D
     - N = 100 (sample size)
     - D = 4 (number of features)
   - Store K, inertia, BIC
4. Select optimal K:
   - If BIC minimum at K < 6: optimal_K = argmin(BIC)
   - If BIC minimum at K = 6: optimal_K = 5 (avoid boundary, test K=7,8 in remedial analysis if needed)
5. Document selection rationale (BIC values, elbow plot if helpful)

**Output:**

**File 1:** data/step02_cluster_selection.csv
**Format:** CSV with 6 rows (one per K tested)
**Columns:**
  - `K` (int, values: {1, 2, 3, 4, 5, 6})
  - `inertia` (float, within-cluster sum of squares)
  - `BIC` (float, Bayesian Information Criterion)
**Expected Rows:** 6

**File 2:** data/step02_optimal_k.txt
**Format:** Plain text file
**Content:**
  - Optimal K value (integer)
  - Justification (e.g., "K=3 selected as BIC minimum (BIC=1234.56)")
  - BIC values for all K (for transparency)

**Validation Requirement:**
Validation tools MUST be used after K-means model selection. Specific validation tools will be determined by rq_tools based on clustering model selection requirements (BIC computation correctness, optimal K selection logic).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_cluster_selection.csv exists (exact path)
- Expected rows: 6 (K=1 to K=6)
- Expected columns: 3 (K, inertia, BIC)
- Data types: K (int64), inertia (float64), BIC (float64)
- data/step02_optimal_k.txt exists (exact path)

*Value Ranges:*
- K in {1, 2, 3, 4, 5, 6} (consecutive integers)
- inertia: decreasing with K (monotonic decrease expected)
- BIC: positive values, minimum at optimal K

*Data Quality:*
- No NaN values in cluster_selection.csv
- inertia decreases monotonically (each K has lower inertia than K-1)
- BIC has clear minimum (not all values equal)
- optimal_k.txt contains valid K in {1, 2, 3, 4, 5, 6}

*Log Validation:*
- Required pattern: "Tested K=1 to K=6"
- Required pattern: "BIC minimum at K={optimal_K}"
- Required pattern: "Selected optimal K={optimal_K}"
- Forbidden patterns: "ERROR", "All BIC values equal", "No clear minimum"
- Acceptable warnings: "BIC minimum at boundary (K=6), consider testing K=7,8" (if applicable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Inertia not monotonically decreasing")
- Log failure to logs/step02_cluster_selection.log
- Quit script immediately (do NOT proceed to Step 3)
- g_debug invoked to diagnose root cause

---

### Step 3: Validate Clustering Quality

**Dependencies:** Step 2 (requires optimal K selected)

**Complexity:** Medium (bootstrap stability requires B=100 iterations)

**Purpose:** Validate clustering quality using 3 metrics: Silhouette score (threshold >=0.40 for acceptable quality), Davies-Bouldin index (threshold <1.50 for acceptable separation), and Jaccard bootstrap stability (threshold >=0.75 for acceptable stability, B=100 iterations per Hennig, 2007).

**Input:**

**File 1:** data/step01_standardized_features.csv (from Step 1)
**Format:** CSV with 100 rows x 5 columns (UID + 4 z-scored features)

**File 2:** data/step02_optimal_k.txt (from Step 2)
**Format:** Plain text with optimal K value

**Processing:**

1. Load optimal K from data/step02_optimal_k.txt
2. Load standardized features from data/step01_standardized_features.csv
3. Fit K-means with optimal K (random_state=42, n_init=50)
4. Extract cluster labels (100 assignments)
5. Compute Silhouette score:
   - sklearn.metrics.silhouette_score(X, labels)
   - Interpretation: >=0.40 acceptable, <0.40 weak (no natural clusters)
6. Compute Davies-Bouldin index:
   - sklearn.metrics.davies_bouldin_score(X, labels)
   - Interpretation: <1.50 acceptable, >=1.50 poor separation
7. Compute Jaccard bootstrap stability:
   - For b in 1 to B=100:
     - Resample 100 participants with replacement
     - Fit K-means on bootstrap sample
     - Compute Jaccard similarity between original and bootstrap cluster assignments
   - Report: mean Jaccard, 95% CI
   - Interpretation: >=0.75 acceptable stability, <0.75 unstable
8. Assess overall quality:
   - PASS: Silhouette >= 0.40 OR Jaccard >= 0.75 (at least one criterion met)
   - FAIL: Silhouette < 0.40 AND Jaccard < 0.75 (both criteria fail)
   - If FAIL: Document as meaningful null finding (memory ability is continuous, not categorical)

**Output:**

**File:** data/step03_cluster_validation.csv
**Format:** CSV with 3 rows (one per metric)
**Columns:**
  - `metric` (string, values: {Silhouette, Davies-Bouldin, Jaccard})
  - `value` (float, metric value)
  - `threshold` (float, acceptance threshold: 0.40, 1.50, 0.75)
  - `status` (string, values: {PASS, FAIL})
**Expected Rows:** 3

**Validation Requirement:**
Validation tools MUST be used after clustering quality validation. Specific validation tools will be determined by rq_tools based on validation metric computation requirements (Silhouette range [0,1], Davies-Bouldin >=0, Jaccard in [0,1]).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_cluster_validation.csv exists (exact path)
- Expected rows: 3 (one per metric)
- Expected columns: 4 (metric, value, threshold, status)
- Data types: metric (object/string), value (float64), threshold (float64), status (object/string)

*Value Ranges:*
- Silhouette in [0, 1] (typical range for K>1: [0.1, 0.6] in memory data)
- Davies-Bouldin >= 0 (typical range: [0.8, 2.0])
- Jaccard in [0, 1] (typical range: [0.4, 0.9])

*Data Quality:*
- No NaN values
- All 3 metrics present
- status in {PASS, FAIL} (exact string match)
- threshold values match documentation (0.40, 1.50, 0.75)

*Log Validation:*
- Required pattern: "Silhouette score: {value:.3f} (threshold: 0.40)"
- Required pattern: "Davies-Bouldin index: {value:.3f} (threshold: 1.50)"
- Required pattern: "Jaccard stability: {value:.3f} (threshold: 0.75)"
- Required pattern: "Overall quality: {PASS/FAIL}"
- Forbidden patterns: "ERROR", "Bootstrap failed", "Invalid metric value"
- Acceptable warnings: "Both criteria failed (Silhouette<0.40 AND Jaccard<0.75), clustering quality weak" (if applicable)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Silhouette score NaN, computation failed")
- Log failure to logs/step03_validate_quality.log
- Quit script immediately (do NOT proceed to Step 4)
- g_debug invoked to diagnose root cause

---

### Step 4: Fit Final K-Means with Optimal K

**Dependencies:** Steps 2, 3 (requires optimal K selected and validated)

**Complexity:** Low (single K-means fit)

**Purpose:** Fit final K-means with optimal K (random_state=42, n_init=50), extract cluster assignments (100 UIDs with cluster labels), and cluster centers (K centers x 4 features).

**Input:**

**File 1:** data/step01_standardized_features.csv (from Step 1)
**Format:** CSV with 100 rows x 5 columns (UID + 4 z-scored features)

**File 2:** data/step02_optimal_k.txt (from Step 2)
**Format:** Plain text with optimal K value

**Processing:**

1. Load optimal K from data/step02_optimal_k.txt
2. Load standardized features from data/step01_standardized_features.csv
3. Extract feature matrix X (100 rows x 4 columns, exclude UID)
4. Fit K-means: sklearn.cluster.KMeans(n_clusters=K, random_state=42, n_init=50)
5. Extract cluster assignments (labels_)
6. Extract cluster centers (cluster_centers_: K x 4 array)
7. Validate cluster sizes: no cluster < 10% of sample (minimum 10 participants per cluster)
8. Save assignments (UID + cluster label)
9. Save centers (cluster ID + 4 feature means)

**Output:**

**File 1:** data/step04_cluster_assignments.csv
**Format:** CSV with 100 rows (one per participant)
**Columns:**
  - `UID` (string, participant identifier)
  - `cluster` (int, cluster assignment, values: 0 to K-1)
**Expected Rows:** 100

**File 2:** data/step04_cluster_centers.csv
**Format:** CSV with K rows (one per cluster)
**Columns:**
  - `cluster` (int, cluster ID, values: 0 to K-1)
  - `Source_intercept` (float, cluster center for Source_intercept z-score)
  - `Source_slope` (float, cluster center for Source_slope z-score)
  - `Destination_intercept` (float, cluster center for Destination_intercept z-score)
  - `Destination_slope` (float, cluster center for Destination_slope z-score)
**Expected Rows:** K (number of clusters)

**Validation Requirement:**
Validation tools MUST be used after final K-means fitting. Specific validation tools will be determined by rq_tools based on clustering requirements (cluster assignments consecutive 0...K-1, cluster sizes >= 10, cluster centers within reasonable z-score range).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_cluster_assignments.csv exists (exact path)
- Expected rows: 100 (one per participant)
- Expected columns: 2 (UID, cluster)
- Data types: UID (object/string), cluster (int64)
- data/step04_cluster_centers.csv exists (exact path)
- Expected rows: K (from step02_optimal_k.txt)
- Expected columns: 5 (cluster, 4 features)
- Data types: cluster (int64), all features (float64)

*Value Ranges:*
- cluster in {0, 1, ..., K-1} (consecutive integers starting at 0)
- cluster centers: typical range [-2, 2] in z-score space (extreme outliers possible)

*Data Quality:*
- No NaN values in either file
- All 100 participants assigned to exactly one cluster
- No duplicate UIDs in cluster_assignments.csv
- Cluster IDs in cluster_centers.csv match {0, 1, ..., K-1} (no gaps)
- Minimum cluster size >= 10 participants (no cluster < 10% of sample)

*Log Validation:*
- Required pattern: "Fitted K-means with K={optimal_K}"
- Required pattern: "Cluster sizes: {counts per cluster}"
- Required pattern: "All clusters >= 10 participants: {True/False}"
- Forbidden patterns: "ERROR", "Empty cluster", "Cluster size < 10"
- Acceptable warnings: None expected for final K-means

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 2 has only 5 participants, minimum 10 required")
- Log failure to logs/step04_fit_final_kmeans.log
- Quit script immediately (do NOT proceed to Step 5)
- g_debug invoked to diagnose root cause

---

### Step 5: Characterize Clusters

**Dependencies:** Step 4 (requires cluster assignments and centers)

**Complexity:** Low (descriptive statistics computation only)

**Purpose:** Characterize clusters by computing mean intercept/slope per location type (Source, Destination) per cluster, assign interpretive labels (e.g., "High Source, Low Destination", "Balanced High Performers"), and create human-readable cluster descriptions.

**Input:**

**File 1:** data/step00_random_effects_from_rq556.csv (from Step 0)
**Format:** CSV with 100 rows x 5 columns (UID + 4 features in original scale, not z-scored)

**File 2:** data/step04_cluster_assignments.csv (from Step 4)
**Format:** CSV with 100 rows (UID, cluster)

**File 3:** data/step04_cluster_centers.csv (from Step 4)
**Format:** CSV with K rows (cluster, 4 z-scored feature centers)

**Processing:**

1. Load original-scale features from data/step00_random_effects_from_rq556.csv
2. Load cluster assignments from data/step04_cluster_assignments.csv
3. Merge on UID
4. For each cluster (0 to K-1):
   - Compute mean and SD for each of 4 features (original scale, not z-scores)
   - Compute sample size (N participants in cluster)
   - Assign interpretive label based on feature patterns:
     - Example: High Source_intercept + Low Destination_intercept -> "High Source, Low Destination"
     - Example: High both -> "Balanced High Performers"
     - Example: Low both -> "Balanced Low Performers"
     - Example: High Destination_intercept + Low Source_intercept -> "High Destination, Low Source"
5. Create summary table with cluster descriptions
6. Write human-readable characterization text (for rq_results later)

**Output:**

**File 1:** data/step05_cluster_characterization.csv
**Format:** CSV with K rows (one per cluster)
**Columns:**
  - `cluster` (int, cluster ID, values: 0 to K-1)
  - `N` (int, number of participants in cluster)
  - `Source_intercept_mean` (float, mean in original theta scale)
  - `Source_intercept_sd` (float, SD in original theta scale)
  - `Source_slope_mean` (float, mean in original theta/day scale)
  - `Source_slope_sd` (float, SD in original theta/day scale)
  - `Destination_intercept_mean` (float, mean in original theta scale)
  - `Destination_intercept_sd` (float, SD in original theta/day scale)
  - `Destination_slope_mean` (float, mean in original theta/day scale)
  - `Destination_slope_sd` (float, SD in original theta/day scale)
  - `label` (string, interpretive cluster label)
**Expected Rows:** K

**File 2:** data/step05_cluster_descriptions.txt
**Format:** Plain text file with human-readable cluster characterizations
**Content:**
  - One paragraph per cluster
  - Include: cluster ID, N participants, mean intercepts/slopes, interpretive label
  - Example: "Cluster 0 (N=35, 'Balanced High Performers'): High baseline memory for both source (mean theta=0.8) and destination (mean theta=0.7), with minimal forgetting (slopes near 0)."

**Validation Requirement:**
Validation tools MUST be used after cluster characterization. Specific validation tools will be determined by rq_tools based on characterization requirements (summary statistics correctness: min <= mean <= max, SD >= 0, N > 0).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cluster_characterization.csv exists (exact path)
- Expected rows: K (from step02_optimal_k.txt)
- Expected columns: 11 (cluster, N, 4 features x 2 stats, label)
- Data types: cluster (int64), N (int64), all means/SDs (float64), label (object/string)
- data/step05_cluster_descriptions.txt exists (exact path)

*Value Ranges:*
- N: sum(N across clusters) = 100
- All means: scientifically reasonable (intercepts in [-2, 2], slopes in [-0.5, 0.5])
- All SDs >= 0 (non-negative)

*Data Quality:*
- No NaN values in characterization.csv
- All clusters present (cluster IDs = {0, 1, ..., K-1})
- N >= 10 for all clusters (minimum cluster size enforced in Step 4)
- label column non-empty (all clusters have interpretive labels)

*Log Validation:*
- Required pattern: "Characterized {K} clusters"
- Required pattern: "Cluster sizes: {N per cluster}"
- Required pattern: "All clusters labeled"
- Forbidden patterns: "ERROR", "Empty cluster", "Missing label"
- Acceptable warnings: None expected for characterization

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 1 has SD=-0.5, must be non-negative")
- Log failure to logs/step05_characterize_clusters.log
- Quit script immediately (do NOT proceed to Step 6)
- g_debug invoked to diagnose root cause

---

### Step 6: Create Scatter Plot Matrix

**Dependencies:** Steps 1, 4 (requires standardized features and cluster assignments)

**Complexity:** Low (plotting only)

**Purpose:** Create 4x4 scatter plot matrix showing pairwise relationships among the 4 features (Source_intercept, Source_slope, Destination_intercept, Destination_slope), colored by cluster membership, with cluster centers overlaid and reference lines at z=0.

**Input:**

**File 1:** data/step01_standardized_features.csv (from Step 1)
**Format:** CSV with 100 rows x 5 columns (UID + 4 z-scored features)

**File 2:** data/step04_cluster_assignments.csv (from Step 4)
**Format:** CSV with 100 rows (UID, cluster)

**File 3:** data/step04_cluster_centers.csv (from Step 4)
**Format:** CSV with K rows (cluster, 4 z-scored feature centers)

**Processing:**

1. Load standardized features from data/step01_standardized_features.csv
2. Load cluster assignments from data/step04_cluster_assignments.csv
3. Merge on UID
4. Load cluster centers from data/step04_cluster_centers.csv
5. Create 4x4 scatter plot matrix:
   - x-axis: one of 4 features
   - y-axis: one of 4 features
   - Color: cluster membership (K colors)
   - Diagonal: Histograms (distribution per feature, colored by cluster)
   - Off-diagonal: Scatter plots with cluster centers overlaid as large markers
   - Reference lines: Horizontal and vertical at z=0 (dashed gray)
6. Apply consistent plot styling from config
7. Save plot as PNG

**Output:**

**File:** plots/step06_cluster_scatter_matrix_data.csv
**Format:** CSV with plot source data
**Columns:**
  - `UID` (string)
  - `Source_intercept` (float, z-scored)
  - `Source_slope` (float, z-scored)
  - `Destination_intercept` (float, z-scored)
  - `Destination_slope` (float, z-scored)
  - `cluster` (int)
**Expected Rows:** 100
**Note:** PNG output created later by rq_plots (plots/step06_cluster_scatter_matrix.png)

**Validation Requirement:**
Validation tools MUST be used after plot data preparation. Specific validation tools will be determined by rq_tools based on plot data format requirements (CSV structure validation, all clusters present, feature ranges reasonable).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step06_cluster_scatter_matrix_data.csv exists (exact path)
- Expected rows: 100 (one per participant)
- Expected columns: 6 (UID, 4 features, cluster)
- Data types: UID (object/string), all features (float64), cluster (int64)

*Value Ranges:*
- All features: z-score scale (typical range [-3, 3])
- cluster in {0, 1, ..., K-1}

*Data Quality:*
- No NaN values tolerated (all cells must have valid values)
- Expected N: Exactly 100 rows
- All clusters represented (K unique cluster values)
- No duplicate UIDs

*Log Validation:*
- Required pattern: "Plot data prepared: 100 participants, {K} clusters"
- Required pattern: "All clusters represented in plot data"
- Forbidden patterns: "ERROR", "Missing cluster", "NaN in features"
- Acceptable warnings: None expected for plot data preparation

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 2 missing from plot data")
- Log failure to logs/step06_prepare_scatter_matrix_data.log
- Quit script immediately
- g_debug invoked to diagnose root cause

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs - intermediate and final)

- data/step00_random_effects_from_rq556.csv (from Step 0: load and reshape RQ 5.5.6 random effects)
- data/step01_standardized_features.csv (from Step 1: z-score standardization)
- data/step02_cluster_selection.csv (from Step 2: BIC model selection results)
- data/step02_optimal_k.txt (from Step 2: selected K value with justification)
- data/step03_cluster_validation.csv (from Step 3: Silhouette, Davies-Bouldin, Jaccard metrics)
- data/step04_cluster_assignments.csv (from Step 4: final cluster labels per participant)
- data/step04_cluster_centers.csv (from Step 4: K cluster centers x 4 features)
- data/step05_cluster_characterization.csv (from Step 5: cluster means/SDs with labels)
- data/step05_cluster_descriptions.txt (from Step 5: human-readable cluster characterizations)
- plots/step06_cluster_scatter_matrix_data.csv (from Step 6: plot source CSV)

### Logs (ONLY execution logs - .log files capturing stdout/stderr)

- logs/step00_load_random_effects.log
- logs/step01_standardize_features.log
- logs/step02_cluster_selection.log
- logs/step03_validate_quality.log
- logs/step04_fit_final_kmeans.log
- logs/step05_characterize_clusters.log
- logs/step06_prepare_scatter_matrix_data.log

### Plots (EMPTY until rq_plots runs)

- plots/step06_cluster_scatter_matrix.png (created by rq_plots, NOT analysis steps)

### Results (EMPTY until rq_results runs)

- results/summary.md (created by rq_results, NOT analysis steps)

---

## Expected Data Formats

### Step 0 Output: Random Effects (Original Scale)

**File:** data/step00_random_effects_from_rq556.csv

**Format:** Wide format, one row per participant

**Columns:**
- `UID` (string, format: P### with leading zeros)
- `Source_intercept` (float, theta scale, baseline source memory at Day 0)
- `Source_slope` (float, theta/day scale, source memory forgetting rate)
- `Destination_intercept` (float, theta scale, baseline destination memory at Day 0)
- `Destination_slope` (float, theta/day scale, destination memory forgetting rate)

**Expected Dimensions:** 100 rows x 5 columns

**Transformation:** Reshapes RQ 5.5.6 long format (200 rows: 100 UID x 2 location types) to wide format (100 rows: 1 per UID with 4 features)

---

### Step 1 Output: Standardized Features (Z-Scores)

**File:** data/step01_standardized_features.csv

**Format:** Wide format, one row per participant

**Columns:**
- `UID` (string, unchanged from Step 0)
- `Source_intercept` (float, z-scored: mean H 0, SD H 1)
- `Source_slope` (float, z-scored: mean H 0, SD H 1)
- `Destination_intercept` (float, z-scored: mean H 0, SD H 1)
- `Destination_slope` (float, z-scored: mean H 0, SD H 1)

**Expected Dimensions:** 100 rows x 5 columns

**Transformation:** z = (x - mean(x)) / SD(x) applied independently to each feature

---

### Step 4 Output: Cluster Assignments

**File:** data/step04_cluster_assignments.csv

**Format:** Wide format, one row per participant

**Columns:**
- `UID` (string, participant identifier)
- `cluster` (int, values: 0 to K-1, cluster assignment)

**Expected Dimensions:** 100 rows x 2 columns

**Key:** UID is unique (one cluster per participant)

---

### Step 4 Output: Cluster Centers

**File:** data/step04_cluster_centers.csv

**Format:** Wide format, one row per cluster

**Columns:**
- `cluster` (int, values: 0 to K-1, cluster ID)
- `Source_intercept` (float, cluster centroid for Source_intercept in z-score space)
- `Source_slope` (float, cluster centroid for Source_slope in z-score space)
- `Destination_intercept` (float, cluster centroid for Destination_intercept in z-score space)
- `Destination_slope` (float, cluster centroid for Destination_slope in z-score space)

**Expected Dimensions:** K rows x 5 columns

**Key:** cluster is unique (one row per cluster)

---

### Step 6 Output: Plot Source Data

**File:** plots/step06_cluster_scatter_matrix_data.csv

**Format:** Wide format, one row per participant

**Columns:**
- `UID` (string)
- `Source_intercept` (float, z-scored)
- `Source_slope` (float, z-scored)
- `Destination_intercept` (float, z-scored)
- `Destination_slope` (float, z-scored)
- `cluster` (int, cluster assignment)

**Expected Dimensions:** 100 rows x 6 columns

**Usage:** rq_plots reads this CSV to generate 4x4 scatter plot matrix PNG

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 5.5.6** (Source-Destination Variance Decomposition)
  - File: results/ch5/5.5.6/data/step04_random_effects.csv
  - Used in: Step 0 (load random effects for clustering features)
  - Rationale: RQ 5.5.6 extracts participant-level random intercepts and slopes from location-stratified LMMs. This RQ clusters participants based on those random effects to identify latent classes.

**Execution Order Constraint:**
1. RQ 5.5.6 must complete Steps 1-4 (location-stratified LMMs, variance component extraction, ICC computation, random effects extraction)
2. This RQ executes after RQ 5.5.6 (uses random_effects.csv output)

**Data Source Boundaries:**
- **RAW data:** None (no direct extraction from master.xlsx)
- **DERIVED data:** Random effects from RQ 5.5.6 (results/ch5/5.5.6/data/step04_random_effects.csv)
- **Scope:** This RQ performs clustering ONLY (no IRT, no LMM, no re-estimation of random effects)

**Validation:**
- Step 0: Check results/ch5/5.5.6/status.yaml shows rq_results: success (circuit breaker: EXPECTATIONS ERROR if RQ 5.5.6 incomplete)
- Step 0: Check results/ch5/5.5.6/data/step04_random_effects.csv exists (circuit breaker: EXPECTATIONS ERROR if file missing)
- If RQ 5.5.6 incomplete or file missing -> quit with error -> user must execute RQ 5.5.6 first

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
- g_code (Step 14 workflow) will generate stepNN_name.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_name.log for validation output)

### Validation Requirements By Step

#### Step 0: Load Random Effects from RQ 5.5.6

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + pivot)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_dataframe_structure)

**What Validation Checks:**
- Output file exists (data/step00_random_effects_from_rq556.csv)
- Expected row count (100 participants)
- Expected column count (5: UID + 4 features)
- No NaN values (all cells populated)
- UID uniqueness (no duplicate participants)
- Value ranges scientifically reasonable (intercepts in [-3, 3], slopes in [-1, 1])

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 rows, found 97")
- Log failure to logs/step00_load_random_effects.log
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked by master to diagnose root cause

---

#### Step 1: Standardize Features to Z-Scores

**Analysis Tool:** (determined by rq_tools - likely sklearn.preprocessing.StandardScaler or manual z-score)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_standardization)

**What Validation Checks:**
- Output file exists (data/step01_standardized_features.csv)
- Z-score correctness: mean(z) H 0, SD(z) H 1 per feature (within tolerance)
- No NaN values introduced during standardization
- Row count preserved (100 participants)
- UID column unchanged

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Source_intercept has mean=0.5, expected H 0")
- Log failure to logs/step01_standardize_features.log
- Quit script immediately
- g_debug invoked

---

#### Step 2: K-Means Model Selection

**Analysis Tool:** (determined by rq_tools - likely sklearn.cluster.KMeans + BIC computation)
**Validation Tool:** (determined by rq_tools - likely custom BIC validation)

**What Validation Checks:**
- Output files exist (cluster_selection.csv, optimal_k.txt)
- K values consecutive {1, 2, 3, 4, 5, 6}
- Inertia decreases monotonically with K
- BIC values positive, clear minimum exists
- Optimal K in valid range {1, 2, 3, 4, 5, 6}

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Inertia not monotonically decreasing")
- Log failure to logs/step02_cluster_selection.log
- Quit script immediately
- g_debug invoked

---

#### Step 3: Validate Clustering Quality

**Analysis Tool:** (determined by rq_tools - likely sklearn.metrics.silhouette_score, davies_bouldin_score + custom Jaccard bootstrap)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_bootstrap_stability)

**What Validation Checks:**
- Output file exists (cluster_validation.csv)
- All 3 metrics present (Silhouette, Davies-Bouldin, Jaccard)
- Metric values in valid ranges (Silhouette [0,1], DB >=0, Jaccard [0,1])
- Status field correctly assigned (PASS/FAIL based on thresholds)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Silhouette score NaN")
- Log failure to logs/step03_validate_quality.log
- Quit script immediately
- g_debug invoked

---

#### Step 4: Fit Final K-Means

**Analysis Tool:** (determined by rq_tools - likely sklearn.cluster.KMeans)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_cluster_assignment)

**What Validation Checks:**
- Output files exist (cluster_assignments.csv, cluster_centers.csv)
- Cluster IDs consecutive {0, 1, ..., K-1} (no gaps)
- All 100 participants assigned
- No duplicate UIDs
- Minimum cluster size >= 10 participants
- Cluster centers in reasonable z-score range

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 2 has only 5 participants")
- Log failure to logs/step04_fit_final_kmeans.log
- Quit script immediately
- g_debug invoked

---

#### Step 5: Characterize Clusters

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + descriptive stats)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_cluster_summary_stats)

**What Validation Checks:**
- Output files exist (cluster_characterization.csv, cluster_descriptions.txt)
- Summary statistics valid (SD >= 0, N > 0, min <= mean <= max)
- All clusters characterized (K rows in CSV)
- All clusters labeled (label column non-empty)
- N sums to 100 across clusters

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 1 has SD=-0.5")
- Log failure to logs/step05_characterize_clusters.log
- Quit script immediately
- g_debug invoked

---

#### Step 6: Create Scatter Plot Matrix Data

**Analysis Tool:** (determined by rq_tools - likely pandas merge + CSV write)
**Validation Tool:** (determined by rq_tools - likely tools.validation.validate_plot_data_completeness)

**What Validation Checks:**
- Output file exists (plots/step06_cluster_scatter_matrix_data.csv)
- All clusters represented (K unique cluster values)
- Expected row count (100 participants)
- No NaN values in features or cluster column
- Feature values in z-score range (typical [-3, 3])

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 2 missing from plot data")
- Log failure to logs/step06_prepare_scatter_matrix_data.log
- Quit script immediately
- g_debug invoked

---

## Summary

**Total Steps:** 7 (Step 0: Load + Steps 1-6: Standardize, Select, Validate, Fit, Characterize, Visualize)

**Estimated Runtime:** Low (~5-10 minutes total, dominated by bootstrap stability computation in Step 3)

**Cross-RQ Dependencies:** RQ 5.5.6 (requires random effects extraction complete)

**Primary Outputs:**
- Cluster assignments (100 participants -> K clusters)
- Cluster validation metrics (Silhouette, Davies-Bouldin, Jaccard)
- Cluster characterization (mean intercepts/slopes per cluster with interpretive labels)
- Scatter plot matrix (4x4 grid, colored by cluster)

**Validation Coverage:** 100% (all 7 steps have validation requirements)

**Expected Clustering Quality:**
Based on universal Chapter 5 pattern (RQ 5.1.5, 5.2.7, 5.3.8, 5.4.7):
- Weak clustering quality (Silhouette < 0.40) expected
- Stable groupings (Jaccard > 0.60) expected
- Optimal K = 2-4 (based on prior RQs)
- Clusters interpretable despite weak quality (useful for descriptive purposes)

**Theoretical Interpretation:**
- If Silhouette < 0.40 AND Jaccard < 0.75: Document as meaningful null finding (memory ability is continuous, not categorical)
- If source-destination dissociation exists (per RQ 5.5.1), clusters may differentiate by location-type-specific intercepts
- If ICC_slope H 0 from RQ 5.5.6, clustering driven by intercepts only (slopes contribute minimal variance)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-04): Initial plan created by rq_planner agent for RQ 5.5.7
