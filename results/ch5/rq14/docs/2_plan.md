# Analysis Plan for RQ 5.14: Latent Forgetting Profiles (K-means Clustering)

**Created by:** rq_planner agent
**Date:** 2025-11-27
**Status:** Ready for rq_tools (Step 11 workflow)

---

## Overview

This RQ uses K-means clustering to identify latent forgetting profiles in the N=100 participant sample. Clustering is performed on random intercepts (baseline ability) and random slopes (forgetting rate) extracted from RQ 5.13's Total domain mixed-effects model. The analysis is exploratory, testing whether participants fall into discrete latent classes (e.g., "resilient" vs "vulnerable" memory) or exhibit continuous variation.

**Analysis Pipeline:** K-means clustering with BIC model selection (K=1 to K=6)

**Total Steps:** 7 steps (Step 0: load data + Steps 1-6: standardize, optimize K, fit model, validate stability, characterize clusters, visualize)

**Estimated Runtime:** Medium (10-20 minutes total - bootstrap stability is most time-intensive)

**Key Methods Applied:**
- Standardization (z-scores) to ensure equal contribution of intercepts/slopes to distance metric
- BIC model selection for optimal cluster count, constrained by silhouette score >=0.5
- Gap statistic to test K>1 vs K=1 (discrete profiles vs continuous variation)
- Bootstrap stability validation (100 iterations, Jaccard similarity coefficient)
- Minimum cluster size constraint (>=10% of sample, n>=10 participants)

**Cross-RQ Dependencies:**
- RQ 5.13 MUST complete successfully (provides random_effects_total.csv)
- RQ 5.7 optional (if trajectory plotting needed, requires theta_scores.csv + tsvr_mapping.csv)

---

## Analysis Plan

### Step 0: Load Random Effects from RQ 5.13

**Purpose:** Load participant-level random intercepts and slopes from RQ 5.13's Total domain mixed-effects model

**Dependencies:** None (first step, but requires RQ 5.13 completion)

**Complexity:** Low (data loading only, <1 minute)

**Input:**

**File:** `results/ch5/rq13/data/random_effects_total.csv` (from RQ 5.13)
**Format:** CSV, one row per participant (UID)
**Required Columns:**
- `UID` (string, participant identifier, format: P### with leading zeros)
- `Total_Intercept` (float, baseline ability at TSVR=0 hours, estimated from LMM)
- `Total_Slope` (float, forgetting rate, change in ability per unit time, estimated from LMM)

**Expected Rows:** 100 participants (full sample from RQ 5.13)
**Expected Values:**
- Total_Intercept: Continuous, typically in range [-1.0, 1.0] (standardized in LMM)
- Total_Slope: Continuous, typically in range [-0.05, 0.05] (small values, gradual forgetting)
- No missing values (all participants in RQ 5.13 have random effects estimated)

**Processing:**

1. Check RQ 5.13 status: Read `results/ch5/rq13/status.yaml`, verify `rq_results.status == "success"`
2. If RQ 5.13 incomplete: QUIT with EXPECTATIONS ERROR ("RQ 5.13 must complete before RQ 5.14 (dependency)")
3. Load `results/ch5/rq13/data/random_effects_total.csv` using pandas
4. Validate required columns present: UID, Total_Intercept, Total_Slope
5. Validate no missing values (all 100 participants must have non-NaN random effects)
6. Compute descriptive statistics: mean, SD, min, max, median for Total_Intercept and Total_Slope
7. Save descriptive statistics to `logs/step00_random_effects_descriptives.txt`
8. Save loaded data to `data/step00_random_effects.csv` (copy for lineage tracking)

**Output:**

**File 1:** `data/step00_random_effects.csv`
**Format:** CSV, identical to input file (copy from RQ 5.13 for lineage)
**Columns:** UID, Total_Intercept, Total_Slope
**Expected Rows:** 100
**Purpose:** Establish data lineage (RQ 5.13 -> RQ 5.14)

**File 2:** `logs/step00_random_effects_descriptives.txt`
**Format:** Plain text report
**Content:** Descriptive statistics table (mean, SD, min, max, median) for Total_Intercept and Total_Slope
**Purpose:** Document raw clustering variable distributions before standardization

**Validation Requirement:**
Validation tools MUST be used after data loading execution. Specific validation tools determined by rq_tools based on data loading requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- `data/step00_random_effects.csv` exists
- Expected rows: Exactly 100 (one per participant)
- Expected columns: 3 (UID, Total_Intercept, Total_Slope)
- Data types: UID (object/string), Total_Intercept (float64), Total_Slope (float64)

*Value Ranges:*
- Total_Intercept in [-2.0, 2.0] (scientifically reasonable range for standardized LMM random effects)
- Total_Slope in [-0.2, 0.2] (small values expected, large |slope| > 0.2 indicates extreme forgetting/improvement)
- No infinite values (finite floats only)

*Data Quality:*
- No NaN values tolerated (all participants must have random effects)
- All 100 participants present (no data loss from RQ 5.13)
- No duplicate UIDs (each participant appears once)
- Distribution check: Both variables approximately normal (central limit theorem for random effects)

*Log Validation:*
- Required pattern: "Loaded 100 participants from RQ 5.13"
- Required pattern: "All required columns present: UID, Total_Intercept, Total_Slope"
- Required pattern: "No missing values detected"
- Forbidden patterns: "ERROR", "RQ 5.13 incomplete", "Missing column", "NaN detected"
- Acceptable warnings: None expected for data loading

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 100 rows, found 87 - data loss from RQ 5.13")
- Log failure to `logs/step00_load_random_effects.log`
- Quit script immediately (do NOT proceed to Step 1)
- g_debug invoked to diagnose root cause (check RQ 5.13 outputs)

---

### Step 1: Standardize Clustering Variables

**Purpose:** Standardize Total_Intercept and Total_Slope to z-scores (mean=0, SD=1) to ensure both dimensions contribute equally to K-means Euclidean distance metric

**Dependencies:** Step 0 (requires loaded random effects)

**Complexity:** Low (simple z-score transformation, <1 minute)

**Input:**

**File:** `data/step00_random_effects.csv` (from Step 0)
**Format:** CSV, one row per participant
**Columns:** UID, Total_Intercept, Total_Slope
**Expected Rows:** 100

**Processing:**

1. Load `data/step00_random_effects.csv`
2. Compute mean and SD for Total_Intercept and Total_Slope (grand mean/SD across all participants)
3. Standardize Total_Intercept: `Total_Intercept_z = (Total_Intercept - mean_Intercept) / SD_Intercept`
4. Standardize Total_Slope: `Total_Slope_z = (Total_Slope - mean_Slope) / SD_Slope`
5. Validate standardization: Check that mean(Total_Intercept_z) approximately 0 and SD(Total_Intercept_z) approximately 1 (allow tolerance +-0.01 for rounding)
6. Validate standardization: Check that mean(Total_Slope_z) approximately 0 and SD(Total_Slope_z) approximately 1
7. Save standardization parameters (mean_Intercept, SD_Intercept, mean_Slope, SD_Slope) to `logs/step01_standardization_params.txt` for later unstandardization
8. Create new DataFrame with UID, Total_Intercept_z, Total_Slope_z
9. Save to `data/step01_clustering_input.csv`

**Output:**

**File 1:** `data/step01_clustering_input.csv`
**Format:** CSV, one row per participant
**Columns:**
- `UID` (string, participant identifier)
- `Total_Intercept_z` (float, standardized baseline ability, mean=0, SD=1)
- `Total_Slope_z` (float, standardized forgetting rate, mean=0, SD=1)
**Expected Rows:** 100
**Purpose:** Standardized clustering variables for K-means input (ensures equal contribution to distance)

**File 2:** `logs/step01_standardization_params.txt`
**Format:** Plain text report
**Content:** Standardization parameters (mean_Intercept, SD_Intercept, mean_Slope, SD_Slope) for unstandardization in Step 5
**Purpose:** Enable conversion of cluster centers back to original scale for interpretability

**Validation Requirement:**
Validation tools MUST be used after standardization execution. Specific validation tools determined by rq_tools (likely `validate_standardization` from tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- `data/step01_clustering_input.csv` exists
- Expected rows: Exactly 100
- Expected columns: 3 (UID, Total_Intercept_z, Total_Slope_z)
- Data types: UID (object), Total_Intercept_z (float64), Total_Slope_z (float64)

*Value Ranges:*
- Total_Intercept_z in [-4.0, 4.0] (z-scores beyond +-4 extremely rare, likely error)
- Total_Slope_z in [-4.0, 4.0] (same reasoning)
- No infinite values

*Data Quality:*
- No NaN values tolerated
- All 100 participants present
- Standardization validation: mean(Total_Intercept_z) in [-0.01, 0.01] (approximately 0)
- Standardization validation: SD(Total_Intercept_z) in [0.99, 1.01] (approximately 1)
- Standardization validation: mean(Total_Slope_z) in [-0.01, 0.01]
- Standardization validation: SD(Total_Slope_z) in [0.99, 1.01]

*Log Validation:*
- Required pattern: "Standardization complete: mean approximately 0, SD approximately 1"
- Required pattern: "VALIDATION - PASS: Standardization criteria met"
- Forbidden patterns: "ERROR", "Standardization failed", "SD near zero" (SD=0 causes division by zero)
- Acceptable warnings: None expected for standardization

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Standardization failed: mean(Total_Intercept_z) = 0.5, expected 0")
- Log failure to `logs/step01_standardize_variables.log`
- Quit script immediately
- g_debug invoked (likely cause: SD near zero indicates no variation in variable)

---

### Step 2: Determine Optimal Number of Clusters

**Purpose:** Test K=1 to K=6 clusters using K-means, compute BIC + silhouette + gap statistic for each K, select optimal K using BIC minimum constrained by silhouette >=0.5, validate minimum cluster size >=10% of sample

**Dependencies:** Step 1 (requires standardized clustering variables)

**Complexity:** High (bootstrap-intensive, gap statistic computationally expensive, 5-10 minutes)

**Input:**

**File:** `data/step01_clustering_input.csv` (from Step 1)
**Format:** CSV, one row per participant
**Columns:** UID, Total_Intercept_z, Total_Slope_z
**Expected Rows:** 100

**Processing:**

**For K=1 to K=6:**

1. Fit K-means model with K clusters (random_state=42, n_init=50 for stability)
2. Extract cluster assignments (labels)
3. Compute inertia (within-cluster sum of squares, RSS)
4. Compute BIC: `BIC = n*log(RSS/n) + k*log(n)` where n=100, k=K
5. Compute average silhouette score across all participants (measures cluster cohesion + separation)
6. Compute gap statistic: Compare observed inertia to null distribution (uniform random data, 50 bootstrap iterations)
7. Store K, inertia, BIC, silhouette, gap statistic in results table

**Selection Criterion:**

8. Identify K with minimum BIC across K=1 to K=6
9. Check constraint: If silhouette(K_min_BIC) >= 0.5, select K_optimal = K_min_BIC
10. If silhouette(K_min_BIC) < 0.5: Select next-lowest BIC with silhouette >= 0.5
11. If NO K has silhouette >= 0.5: Report warning, select K_min_BIC anyway (document poor cluster quality)
12. Gap statistic validation: If gap statistic selects K=1 (no clustering structure), OVERRIDE BIC and report K_optimal=1 (continuous variation, no latent profiles)
13. Minimum cluster size constraint: Fit K-means with K_optimal, check all clusters have >=10% of sample (n>=10)
14. If any cluster <10 participants: Reduce K_optimal by 1, refit, recheck cluster sizes
15. Repeat until all clusters >=10 participants
16. Report final K_optimal with justification (BIC value, silhouette score, gap statistic result, cluster sizes)

**Output:**

**File 1:** `results/step02_model_selection.csv`
**Format:** CSV, one row per K tested (K=1 to K=6)
**Columns:**
- `K` (int, number of clusters)
- `inertia` (float, within-cluster sum of squares)
- `BIC` (float, Bayesian Information Criterion)
- `silhouette` (float, average silhouette score, range [-1, 1])
- `gap_statistic` (float, gap statistic value)
- `gap_SE` (float, standard error of gap statistic)
**Expected Rows:** 6 (one per K)
**Purpose:** Model comparison table for optimal K selection

**File 2:** `results/step02_optimal_K.txt`
**Format:** Plain text report
**Content:**
- Optimal K selected (integer)
- BIC value for optimal K
- Silhouette score for optimal K (with interpretation: >0.7 strong, >0.5 reasonable, >0.25 weak)
- Gap statistic result (K=1 vs K>1 conclusion)
- Cluster sizes for optimal K (n per cluster, percentage of sample)
- Justification for selection (why this K chosen over alternatives)
**Purpose:** Document model selection decision for transparency

**File 3:** `plots/step02_elbow_plot.png`
**Format:** PNG image (800 x 600 @ 300 DPI)
**Content:** Elbow plot showing inertia vs K (visual aid for optimal K identification)
**Purpose:** Diagnostic visualization

**File 4:** `plots/step02_bic_plot.png`
**Format:** PNG image (800 x 600 @ 300 DPI)
**Content:** BIC vs K plot (lower BIC = better fit, minimum indicates optimal K)
**Purpose:** Model selection visualization

**File 5:** `plots/step02_silhouette_plot.png`
**Format:** PNG image (800 x 600 @ 300 DPI)
**Content:** Silhouette score vs K plot (horizontal line at 0.5 threshold for reasonable quality)
**Purpose:** Cluster quality visualization

**Validation Requirement:**
Validation tools MUST be used after model selection execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- `results/step02_model_selection.csv` exists
- Expected rows: Exactly 6 (K=1 to K=6)
- Expected columns: 6 (K, inertia, BIC, silhouette, gap_statistic, gap_SE)
- Data types: K (int64), others (float64)

*Value Ranges:*
- K in [1, 6] (only tested range)
- inertia > 0 (always positive, sum of squared distances)
- BIC values reasonable (typically positive for K-means, decreases then increases with K)
- silhouette in [-1, 1] (by definition)
- gap_statistic > 0 (compares observed vs null, typically positive)
- gap_SE > 0 (standard error always positive)

*Data Quality:*
- No NaN values tolerated (all metrics must be computed for all K)
- All 6 rows present (K=1 to K=6 tested)
- Monotonicity check: inertia decreases as K increases (always true for K-means)
- BIC check: BIC has minimum somewhere in [1, 6] (not monotonic, U-shaped expected)
- Optimal K reported in `step02_optimal_K.txt` is integer in [1, 6]
- Cluster sizes sum to 100 (all participants assigned)
- All clusters >=10 participants (10% minimum enforced)

*Log Validation:*
- Required pattern: "Tested K=1 to K=6, computed BIC + silhouette + gap statistic for each"
- Required pattern: "Optimal K selected: {K_optimal} (BIC={BIC_value}, silhouette={silhouette_value})"
- Required pattern: "All clusters meet minimum size constraint (>=10 participants)"
- Forbidden patterns: "ERROR", "BIC computation failed", "Cluster with <10 participants" (after constraint applied)
- Acceptable warnings: "K={K} has silhouette <0.5 (poor cluster quality)" if some K have low silhouette

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Optimal K has cluster with n=7 participants, violates minimum size constraint")
- Log failure to `logs/step02_determine_optimal_K.log`
- Quit script immediately
- g_debug invoked (likely cause: sample size too small for requested K, or poor clustering structure)

---

### Step 3: Fit Final K-means Model

**Purpose:** Fit K-means with optimal K from Step 2, extract cluster assignments for each participant, compute cluster centers (unstandardize to original scale for interpretation)

**Dependencies:** Step 2 (requires optimal K determination)

**Complexity:** Low (single K-means fit, <1 minute)

**Input:**

**File 1:** `data/step01_clustering_input.csv` (from Step 1)
**Format:** CSV with UID, Total_Intercept_z, Total_Slope_z
**Expected Rows:** 100

**File 2:** `results/step02_optimal_K.txt` (from Step 2)
**Format:** Plain text, contains optimal K value
**Content:** Optimal K (integer, e.g., K=3)

**File 3:** `logs/step01_standardization_params.txt` (from Step 1)
**Format:** Plain text with mean/SD for unstandardization
**Content:** mean_Intercept, SD_Intercept, mean_Slope, SD_Slope

**Processing:**

1. Load `data/step01_clustering_input.csv`
2. Read optimal K from `results/step02_optimal_K.txt`
3. Fit K-means model with K=optimal_K, random_state=42, n_init=50
4. Extract cluster assignments (labels) for each participant
5. Extract cluster centers (K rows x 2 columns: Total_Intercept_z, Total_Slope_z)
6. Load standardization parameters from `logs/step01_standardization_params.txt`
7. Unstandardize cluster centers: `Total_Intercept = Total_Intercept_z * SD_Intercept + mean_Intercept`
8. Unstandardize cluster centers: `Total_Slope = Total_Slope_z * SD_Slope + mean_Slope`
9. Create cluster assignments DataFrame: UID, cluster_id (0 to K-1)
10. Create cluster centers DataFrame: cluster_id, Total_Intercept (original scale), Total_Slope (original scale), Total_Intercept_z, Total_Slope_z
11. Save cluster assignments to `data/step03_cluster_assignments.csv`
12. Save cluster centers to `results/step03_cluster_centers.csv`

**Output:**

**File 1:** `data/step03_cluster_assignments.csv`
**Format:** CSV, one row per participant
**Columns:**
- `UID` (string, participant identifier)
- `cluster_id` (int, cluster assignment 0 to K-1)
**Expected Rows:** 100
**Purpose:** Participant-level cluster membership (used for downstream analyses, trajectory plotting by cluster)

**File 2:** `results/step03_cluster_centers.csv`
**Format:** CSV, one row per cluster
**Columns:**
- `cluster_id` (int, cluster identifier 0 to K-1)
- `Total_Intercept` (float, cluster center baseline ability in original scale)
- `Total_Slope` (float, cluster center forgetting rate in original scale)
- `Total_Intercept_z` (float, cluster center in standardized scale)
- `Total_Slope_z` (float, cluster center in standardized scale)
**Expected Rows:** K (optimal K from Step 2, likely 2-4)
**Purpose:** Cluster center coordinates for interpretation and plotting

**Validation Requirement:**
Validation tools MUST be used after K-means fitting execution. Specific validation tools determined by rq_tools (likely `validate_cluster_assignment` from tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- `data/step03_cluster_assignments.csv` exists
- Expected rows: Exactly 100 (one per participant)
- Expected columns: 2 (UID, cluster_id)
- Data types: UID (object), cluster_id (int64)
- `results/step03_cluster_centers.csv` exists
- Expected rows: K (optimal K from Step 2, likely 2-4)
- Expected columns: 5 (cluster_id, Total_Intercept, Total_Slope, Total_Intercept_z, Total_Slope_z)
- Data types: cluster_id (int64), others (float64)

*Value Ranges:*
- cluster_id in [0, K-1] (consecutive integers, no gaps)
- Total_Intercept in [-2.0, 2.0] (scientifically reasonable for LMM random effects)
- Total_Slope in [-0.2, 0.2] (small values expected)
- Total_Intercept_z in [-4.0, 4.0] (z-scores)
- Total_Slope_z in [-4.0, 4.0] (z-scores)

*Data Quality:*
- No NaN values tolerated
- All 100 participants present in cluster_assignments.csv
- All K clusters present in cluster_centers.csv (0 to K-1, no missing clusters)
- Cluster sizes >=10 participants per cluster (inherited constraint from Step 2)
- Unstandardization check: Applying reverse z-score formula should recover original scale (verify on sample row)

*Log Validation:*
- Required pattern: "K-means fitted with K={optimal_K}"
- Required pattern: "Cluster assignments created for 100 participants"
- Required pattern: "Cluster centers unstandardized to original scale"
- Forbidden patterns: "ERROR", "Missing cluster", "Empty cluster" (all clusters must have members)
- Acceptable warnings: None expected for K-means fitting

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 2 missing from cluster_centers.csv")
- Log failure to `logs/step03_fit_kmeans.log`
- Quit script immediately
- g_debug invoked

---

### Step 4: Bootstrap Cluster Stability Validation

**Purpose:** Assess cluster stability via bootstrap resampling (100 iterations), compute Jaccard similarity between original and bootstrap cluster assignments, validate mean Jaccard >=0.75 for stable clusters

**Dependencies:** Step 3 (requires cluster assignments from final model)

**Complexity:** High (100 bootstrap iterations with K-means fitting, 5-10 minutes)

**Input:**

**File 1:** `data/step01_clustering_input.csv` (from Step 1)
**Format:** CSV with UID, Total_Intercept_z, Total_Slope_z
**Expected Rows:** 100

**File 2:** `data/step03_cluster_assignments.csv` (from Step 3)
**Format:** CSV with UID, cluster_id (original cluster assignments)
**Expected Rows:** 100

**File 3:** `results/step02_optimal_K.txt` (from Step 2)
**Content:** Optimal K value

**Processing:**

1. Load `data/step01_clustering_input.csv` (standardized variables for clustering)
2. Load `data/step03_cluster_assignments.csv` (original cluster assignments)
3. Read optimal K from `results/step02_optimal_K.txt`
4. Initialize empty list for Jaccard similarities (100 iterations)

**For iteration i=1 to 100:**

5. Bootstrap sample: Randomly resample 100 participants WITH REPLACEMENT from clustering_input
6. Fit K-means on bootstrap sample with K=optimal_K, random_state=i, n_init=50
7. Extract bootstrap cluster assignments
8. Match original and bootstrap assignments: For participants appearing in bootstrap sample, compare cluster labels
9. Compute Jaccard similarity: `J = |A intersect B| / |A union B|` where A=original pairs in same cluster, B=bootstrap pairs in same cluster
10. Store Jaccard similarity for iteration i

**After 100 iterations:**

11. Compute mean Jaccard similarity across 100 iterations
12. Compute 95% confidence interval for Jaccard (percentile method: 2.5th and 97.5th percentiles)
13. Assign stability rating:
    - mean_Jaccard >= 0.85: "Highly Stable"
    - mean_Jaccard >= 0.75: "Stable"
    - mean_Jaccard >= 0.6: "Questionable"
    - mean_Jaccard < 0.6: "Unstable"
14. If mean_Jaccard < 0.75: Report warning that clusters may be sample-specific artifacts (consider reducing K or accepting continuous variation)
15. Save all 100 Jaccard values to `logs/step04_bootstrap_jaccard_values.csv` (for histogram/distribution inspection)
16. Save summary to `results/step04_bootstrap_stability.txt` (mean, 95% CI, stability rating, recommendation)

**Output:**

**File 1:** `results/step04_bootstrap_stability.txt`
**Format:** Plain text report
**Content:**
- Mean Jaccard similarity (float, 0 to 1)
- 95% CI for Jaccard (lower, upper bounds)
- Stability rating (Highly Stable / Stable / Questionable / Unstable)
- Recommendation: Proceed with optimal K or reduce K if unstable
**Purpose:** Document cluster stability for interpretation confidence

**File 2:** `logs/step04_bootstrap_jaccard_values.csv`
**Format:** CSV, one row per bootstrap iteration
**Columns:**
- `iteration` (int, 1 to 100)
- `jaccard` (float, Jaccard similarity for that iteration)
**Expected Rows:** 100
**Purpose:** Raw bootstrap values for distribution inspection (optional histogram plotting)

**Validation Requirement:**
Validation tools MUST be used after bootstrap validation execution. Specific validation tools determined by rq_tools (likely `validate_bootstrap_stability` from tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- `results/step04_bootstrap_stability.txt` exists
- Contains mean Jaccard (float in [0, 1])
- Contains 95% CI bounds (both in [0, 1])
- Contains stability rating (one of 4 categories)
- `logs/step04_bootstrap_jaccard_values.csv` exists
- Expected rows: Exactly 100 (one per bootstrap iteration)
- Expected columns: 2 (iteration, jaccard)
- Data types: iteration (int64), jaccard (float64)

*Value Ranges:*
- Mean Jaccard in [0, 1] (by definition of Jaccard similarity)
- All 100 Jaccard values in [0, 1]
- 95% CI lower bound < mean < 95% CI upper bound (CI contains mean)
- 95% CI width reasonable (<0.3, tight CI indicates consistent stability)

*Data Quality:*
- No NaN values in Jaccard values (all iterations must produce valid Jaccard)
- All 100 iterations present
- Mean Jaccard matches manual computation from 100 values (verify: sum/100)
- Stability rating matches mean Jaccard threshold (e.g., if mean=0.82, rating MUST be "Stable")

*Log Validation:*
- Required pattern: "Bootstrap validation complete: 100 iterations"
- Required pattern: "Mean Jaccard similarity: {mean_jaccard:.3f}"
- Required pattern: "Stability rating: {rating}" (one of 4 categories)
- Forbidden patterns: "ERROR", "Bootstrap iteration failed", "Jaccard >1.0" (impossible value)
- Acceptable warnings: "Mean Jaccard <0.75 (questionable stability, consider reducing K)" if stability low

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Bootstrap iteration 47 produced NaN Jaccard similarity")
- Log failure to `logs/step04_bootstrap_stability.log`
- Quit script immediately
- g_debug invoked (likely cause: bootstrap sample too small, K-means convergence failure in bootstrap)

---

### Step 5: Characterize Clusters

**Purpose:** Compute summary statistics (mean, SD, min, max) for Total_Intercept and Total_Slope per cluster, assign interpretive labels based on intercept (High/Average/Low baseline) and slope (Slow/Fast forgetting)

**Dependencies:** Step 3 (requires cluster assignments), Step 0 (requires original-scale random effects)

**Complexity:** Low (descriptive statistics only, <1 minute)

**Input:**

**File 1:** `data/step03_cluster_assignments.csv` (from Step 3)
**Format:** CSV with UID, cluster_id
**Expected Rows:** 100

**File 2:** `data/step00_random_effects.csv` (from Step 0)
**Format:** CSV with UID, Total_Intercept, Total_Slope (original scale)
**Expected Rows:** 100

**Processing:**

1. Load `data/step03_cluster_assignments.csv`
2. Load `data/step00_random_effects.csv`
3. Merge on UID: Combine cluster_id with Total_Intercept, Total_Slope
4. Group by cluster_id
5. For each cluster, compute summary statistics:
   - N (cluster size, number of participants)
   - Percentage of sample (N/100 * 100)
   - Mean Total_Intercept
   - SD Total_Intercept
   - Min Total_Intercept
   - Max Total_Intercept
   - Mean Total_Slope
   - SD Total_Slope
   - Min Total_Slope
   - Max Total_Slope
6. Assign interpretive labels:
   - Intercept label: Compare mean Total_Intercept to grand mean (from Step 0 descriptives)
     - If mean >0.25 SD above grand mean: "High Baseline"
     - If mean within +-0.25 SD of grand mean: "Average Baseline"
     - If mean <-0.25 SD below grand mean: "Low Baseline"
   - Slope label: Compare mean Total_Slope to zero (negative slope = forgetting, positive = improvement over time, zero = stable)
     - If mean Total_Slope < -0.01: "Fast Forgetting"
     - If mean Total_Slope > 0.01: "Slow Forgetting / Improvement"
     - If mean Total_Slope in [-0.01, 0.01]: "Stable Memory"
   - Combined label: "{Intercept label}, {Slope label}" (e.g., "High Baseline, Slow Forgetting")
7. Create cluster summary table with columns: cluster_id, N, percentage, mean_Intercept, SD_Intercept, min_Intercept, max_Intercept, mean_Slope, SD_Slope, min_Slope, max_Slope, label
8. Save to `results/step05_cluster_summary.csv`

**Output:**

**File:** `results/step05_cluster_summary.csv`
**Format:** CSV, one row per cluster
**Columns:**
- `cluster_id` (int, 0 to K-1)
- `N` (int, cluster size)
- `percentage` (float, percentage of sample in cluster)
- `mean_Intercept` (float, mean baseline ability for cluster)
- `SD_Intercept` (float, standard deviation of baseline ability)
- `min_Intercept` (float, minimum baseline ability in cluster)
- `max_Intercept` (float, maximum baseline ability in cluster)
- `mean_Slope` (float, mean forgetting rate for cluster)
- `SD_Slope` (float, standard deviation of forgetting rate)
- `min_Slope` (float, minimum forgetting rate in cluster)
- `max_Slope` (float, maximum forgetting rate in cluster)
- `label` (string, interpretive label combining intercept and slope characteristics)
**Expected Rows:** K (optimal K from Step 2)
**Purpose:** Interpretable cluster characterization for discussion/results sections

**Validation Requirement:**
Validation tools MUST be used after cluster characterization execution. Specific validation tools determined by rq_tools (likely `validate_cluster_summary_stats` from tools_catalog.md).

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- `results/step05_cluster_summary.csv` exists
- Expected rows: K (optimal K from Step 2, likely 2-4)
- Expected columns: 12 (cluster_id, N, percentage, mean/SD/min/max for Intercept and Slope, label)
- Data types: cluster_id (int64), N (int64), percentage (float64), others (float64), label (object/string)

*Value Ranges:*
- cluster_id in [0, K-1]
- N >= 10 (minimum cluster size constraint from Step 2)
- percentage in [10.0, 100.0] (10% minimum per cluster)
- mean_Intercept in [-2.0, 2.0]
- SD_Intercept >= 0 (standard deviation always non-negative)
- min_Intercept <= mean_Intercept <= max_Intercept (logical ordering)
- mean_Slope in [-0.2, 0.2]
- SD_Slope >= 0
- min_Slope <= mean_Slope <= max_Slope

*Data Quality:*
- No NaN values tolerated
- All K clusters present (0 to K-1)
- Sum of N across clusters = 100 (all participants assigned)
- Sum of percentage across clusters approximately 100.0 (allow +-0.1 for rounding)
- All labels non-empty strings (interpretive label assigned to each cluster)

*Log Validation:*
- Required pattern: "Cluster characterization complete: {K} clusters summarized"
- Required pattern: "All clusters have interpretive labels assigned"
- Forbidden patterns: "ERROR", "Missing cluster", "Empty label"
- Acceptable warnings: None expected for cluster characterization

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 1 has min_Intercept > mean_Intercept, logical error")
- Log failure to `logs/step05_characterize_clusters.log`
- Quit script immediately
- g_debug invoked

---

### Step 6: Visualize Clusters

**Purpose:** Generate 2D scatter plot (x-axis = Total_Intercept, y-axis = Total_Slope) with points colored by cluster membership, overlay cluster centers, include reference lines at x=0 and y=0, validate spherical assumption (clusters roughly circular)

**Dependencies:** Step 3 (requires cluster assignments and centers), Step 0 (requires original-scale random effects)

**Complexity:** Low (single plot generation, <1 minute)

**Input:**

**File 1:** `data/step03_cluster_assignments.csv` (from Step 3)
**Format:** CSV with UID, cluster_id
**Expected Rows:** 100

**File 2:** `data/step00_random_effects.csv` (from Step 0)
**Format:** CSV with UID, Total_Intercept, Total_Slope (original scale)
**Expected Rows:** 100

**File 3:** `results/step03_cluster_centers.csv` (from Step 3)
**Format:** CSV with cluster_id, Total_Intercept, Total_Slope (original scale)
**Expected Rows:** K

**File 4:** `results/step05_cluster_summary.csv` (from Step 5)
**Format:** CSV with cluster_id, label (interpretive labels for legend)
**Expected Rows:** K

**Processing:**

1. Load `data/step03_cluster_assignments.csv`
2. Load `data/step00_random_effects.csv`
3. Merge on UID: Combine cluster_id with Total_Intercept, Total_Slope
4. Load `results/step03_cluster_centers.csv`
5. Load `results/step05_cluster_summary.csv` (for labels)
6. Create scatter plot:
   - x-axis: Total_Intercept (original scale)
   - y-axis: Total_Slope (original scale)
   - Color points by cluster_id (use distinct colors for each cluster)
   - Marker size: medium (visible but not overlapping)
   - Marker transparency: 0.6 (see overlapping points)
7. Overlay cluster centers:
   - Plot cluster centers as large markers (e.g., stars or X)
   - Use black color with thick outline for visibility
   - Add text labels next to centers showing cluster_id and interpretive label
8. Add reference lines:
   - Vertical line at x=0 (grand mean baseline ability if data centered)
   - Horizontal line at y=0 (no forgetting/improvement)
   - Use dashed gray lines, low zorder (behind data points)
9. Format plot:
   - Title: "Latent Forgetting Profiles (K={K} clusters)"
   - x-axis label: "Total Intercept (Baseline Ability)"
   - y-axis label: "Total Slope (Forgetting Rate)"
   - Legend: Show cluster labels from step05_cluster_summary.csv
   - Grid: Light gray, behind data
   - Size: 800 x 600 pixels @ 300 DPI
10. Save plot to `plots/step06_cluster_scatter.png`
11. **Spherical assumption validation:** Visual inspection of cluster shapes
    - If clusters roughly circular (isotropic variance): K-means assumption satisfied
    - If clusters elongated or irregular: Consider Gaussian Mixture Models (GMM) for elliptical clusters
    - Document observation in `logs/step06_spherical_assumption_check.txt` (manual inspection notes)

**Output:**

**File 1:** `plots/step06_cluster_scatter.png`
**Format:** PNG image (800 x 600 @ 300 DPI)
**Content:** 2D scatter plot of participants in intercept-slope space, colored by cluster membership, with cluster centers overlaid
**Purpose:** Primary visualization for results section, validates K-means assumptions

**File 2:** `logs/step06_spherical_assumption_check.txt`
**Format:** Plain text report
**Content:** Manual notes on cluster shape inspection (circular vs elongated), recommendation to use K-means as-is or consider GMM
**Purpose:** Document K-means assumption validation (spherical clusters)

**Validation Requirement:**
Validation tools MUST be used after plotting execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- `plots/step06_cluster_scatter.png` exists
- File size > 10 KB (non-empty PNG with data)
- Image dimensions: 800 x 600 pixels (verify via PIL or similar)
- `logs/step06_spherical_assumption_check.txt` exists (manual inspection notes)

*Value Ranges:*
- N/A for plot (visual output)

*Data Quality:*
- Plot contains exactly 100 data points (one per participant)
- K cluster centers plotted (one per cluster)
- Legend present with K entries (cluster labels)
- Reference lines at x=0 and y=0 visible
- Title, axis labels present

*Log Validation:*
- Required pattern: "Cluster scatter plot created: 100 participants, {K} clusters"
- Required pattern: "Cluster centers overlaid on plot"
- Forbidden patterns: "ERROR", "Empty plot", "Missing cluster in plot"
- Acceptable warnings: "Cluster {cluster_id} shows elongated shape, consider GMM for elliptical modeling" if assumption violated

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Plot file created but empty (size <10 KB)")
- Log failure to `logs/step06_visualize_clusters.log`
- Quit script immediately
- g_debug invoked

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Copy random effects from RQ 5.13 (UID, Total_Intercept, Total_Slope) unchanged for lineage tracking

**Step 1 -> Step 2:** Standardize Total_Intercept and Total_Slope to z-scores (mean=0, SD=1), create new columns Total_Intercept_z, Total_Slope_z

**Step 2 -> Step 3:** Select optimal K from model selection results, use as input to final K-means fit

**Step 3 -> Step 4:** Use standardized variables + cluster assignments for bootstrap resampling, compute Jaccard similarity

**Step 3 -> Step 5:** Merge cluster assignments with original-scale random effects, compute per-cluster summary statistics

**Step 5 -> Step 6:** Use cluster assignments + original-scale random effects + cluster centers for scatter plot visualization

### Column Naming Conventions

**From RQ 5.13 (inherited):**
- `UID`: Participant unique identifier (format: P### with leading zeros, e.g., P001, P002, ..., P100)
- `Total_Intercept`: Random intercept from Total domain LMM (baseline ability at TSVR=0)
- `Total_Slope`: Random slope from Total domain LMM (forgetting rate per unit time)

**New for RQ 5.14:**
- `Total_Intercept_z`: Standardized baseline ability (mean=0, SD=1)
- `Total_Slope_z`: Standardized forgetting rate (mean=0, SD=1)
- `cluster_id`: Cluster assignment (integer 0 to K-1)
- `inertia`: Within-cluster sum of squares (K-means objective function)
- `BIC`: Bayesian Information Criterion (model selection criterion)
- `silhouette`: Average silhouette score (cluster quality metric, range [-1, 1])
- `gap_statistic`: Gap statistic value (compares observed clustering to null)
- `gap_SE`: Standard error of gap statistic
- `jaccard`: Jaccard similarity coefficient (bootstrap stability metric, range [0, 1])
- `label`: Interpretive cluster label (string, e.g., "High Baseline, Slow Forgetting")

### Data Type Constraints

**Participant identifiers:**
- UID: object/string (non-numeric, format P###)
- cluster_id: int64 (consecutive integers 0 to K-1)

**Continuous variables:**
- Total_Intercept, Total_Slope: float64 (random effects from LMM)
- Total_Intercept_z, Total_Slope_z: float64 (standardized z-scores)
- inertia, BIC, silhouette, gap_statistic, gap_SE, jaccard: float64 (model selection/validation metrics)

**Categorical variables:**
- label: object/string (interpretive cluster labels)

**Counts:**
- N: int64 (cluster size)
- K: int64 (number of clusters)
- iteration: int64 (bootstrap iteration number)

### Null Handling

**NO missing values tolerated** in any analysis step. All 100 participants have random effects from RQ 5.13 (no exclusions), so all variables should be non-null throughout pipeline.

If NaN detected at any step: FAIL immediately with VALIDATION ERROR (indicates upstream data loss or computation failure).

---

## Cross-RQ Dependencies

### Dependency Type: DERIVED Data from Other RQs

**This RQ requires outputs from:**

**RQ 5.13** (Longitudinal Trajectories - Total Domain)
- **File:** `results/ch5/rq13/data/random_effects_total.csv`
- **Used in:** Step 0 (load random effects for clustering)
- **Rationale:** RQ 5.13 fits mixed-effects model to Total domain (What/Where/When combined), extracts participant-level random intercepts (baseline ability) and random slopes (forgetting rate). This RQ clusters participants based on these two dimensions to identify latent forgetting profiles.

**RQ 5.7** (Trajectory of Forgetting - Optional)
- **File 1:** `results/ch5/rq7/data/theta_scores.csv`
- **File 2:** `results/ch5/rq7/data/step00_tsvr_mapping.csv`
- **Used in:** Optional post-clustering trajectory plotting (visualize theta trajectories by cluster)
- **Rationale:** If user wants to visualize how clusters differ in raw theta trajectories over time, can merge cluster_assignments with RQ 5.7 theta scores + TSVR mapping. NOT required for clustering itself.

**Execution Order Constraint:**
1. **RQ 5.7 must complete first** (provides TSVR mapping, used by RQ 5.13 for LMM fitting)
2. **RQ 5.13 must complete second** (provides random_effects_total.csv)
3. **This RQ executes third** (uses RQ 5.13 random effects as clustering input)

**Data Source Boundaries (Per Specification 5.1.6):**
- **RAW data:** None (this RQ does not use master.xlsx directly)
- **DERIVED data:** Random effects from RQ 5.13 (Total_Intercept, Total_Slope per participant)
- **Scope:** This RQ performs K-means clustering on DERIVED random effects, does NOT refit LMM or recalibrate IRT

**Validation:**
- Step 0: Check `results/ch5/rq13/status.yaml`, verify `rq_results.status == "success"` (circuit breaker: EXPECTATIONS ERROR if RQ 5.13 incomplete)
- Step 0: Check `results/ch5/rq13/data/random_effects_total.csv` exists (circuit breaker: EXPECTATIONS ERROR if file missing)
- If RQ 5.13 incomplete: QUIT with error "RQ 5.13 must complete before RQ 5.14 (dependency)", user must execute RQ 5.13 first

---

## Validation Requirements

### CRITICAL MANDATE

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

---

### Validation Requirements By Step

#### Step 0: Load Random Effects from RQ 5.13

**Analysis Tool:** (determined by rq_tools - likely pandas.read_csv wrapper with RQ dependency check)
**Validation Tool:** (determined by rq_tools - likely `validate_dataframe_structure` + `validate_numeric_range`)

**What Validation Checks:**
- RQ 5.13 status.yaml shows rq_results: success (dependency met)
- File `results/ch5/rq13/data/random_effects_total.csv` exists
- Expected columns present: UID, Total_Intercept, Total_Slope
- Expected rows: 100 (full sample)
- No NaN values (all participants have random effects)
- Value ranges scientifically reasonable: Total_Intercept in [-2, 2], Total_Slope in [-0.2, 0.2]

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "RQ 5.13 incomplete: rq_results status = pending")
- Log failure to `logs/step00_load_random_effects.log`
- Quit script immediately (do NOT proceed to Step 1)
- g_debug NOT invoked (user must complete RQ 5.13 first)

---

#### Step 1: Standardize Clustering Variables

**Analysis Tool:** (determined by rq_tools - likely custom z-score transformation function)
**Validation Tool:** (determined by rq_tools - likely `validate_standardization` from tools_catalog.md)

**What Validation Checks:**
- Output file `data/step01_clustering_input.csv` exists
- Expected columns: UID, Total_Intercept_z, Total_Slope_z
- Expected rows: 100
- No NaN values
- Standardization criteria met: mean(Total_Intercept_z) approximately 0 (tolerance +-0.01)
- Standardization criteria met: SD(Total_Intercept_z) approximately 1 (tolerance 0.99-1.01)
- Same for Total_Slope_z

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Standardization failed: SD(Total_Intercept_z) = 0.5, expected 1.0")
- Log failure to `logs/step01_standardize_variables.log`
- Quit script immediately
- g_debug invoked to diagnose (likely cause: SD near zero indicates no variation)

---

#### Step 2: Determine Optimal Number of Clusters

**Analysis Tool:** (determined by rq_tools - likely custom K-means + BIC + silhouette + gap statistic function)
**Validation Tool:** (determined by rq_tools - likely custom validator checking BIC/silhouette/gap results)

**What Validation Checks:**
- Output file `results/step02_model_selection.csv` exists with 6 rows (K=1 to K=6)
- Required columns: K, inertia, BIC, silhouette, gap_statistic, gap_SE
- No NaN values
- Inertia decreases monotonically with K (always true for K-means)
- Silhouette values in [-1, 1]
- Optimal K reported in `results/step02_optimal_K.txt` is integer in [1, 6]
- All clusters in optimal K meet minimum size constraint (>=10 participants)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Optimal K=4 has cluster with n=7 participants, violates minimum size")
- Log failure to `logs/step02_determine_optimal_K.log`
- Quit script immediately
- g_debug invoked (likely cause: sample too small for requested K, reduce K)

---

#### Step 3: Fit Final K-means Model

**Analysis Tool:** (determined by rq_tools - likely sklearn.cluster.KMeans wrapper)
**Validation Tool:** (determined by rq_tools - likely `validate_cluster_assignment` from tools_catalog.md)

**What Validation Checks:**
- Output files exist: `data/step03_cluster_assignments.csv`, `results/step03_cluster_centers.csv`
- Cluster assignments: 100 rows (one per participant), cluster_id in [0, K-1], consecutive integers
- Cluster centers: K rows (one per cluster), unstandardized values reasonable
- All K clusters present in both files (no missing clusters)
- Cluster sizes >=10 participants each (inherited from Step 2)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 2 missing from cluster_centers.csv")
- Log failure to `logs/step03_fit_kmeans.log`
- Quit script immediately
- g_debug invoked

---

#### Step 4: Bootstrap Cluster Stability Validation

**Analysis Tool:** (determined by rq_tools - likely custom bootstrap + Jaccard function)
**Validation Tool:** (determined by rq_tools - likely `validate_bootstrap_stability` from tools_catalog.md)

**What Validation Checks:**
- Output file `logs/step04_bootstrap_jaccard_values.csv` has 100 rows (one per iteration)
- All Jaccard values in [0, 1] (by definition)
- No NaN values
- Mean Jaccard reported in `results/step04_bootstrap_stability.txt`
- 95% CI contains mean Jaccard
- Stability rating matches mean Jaccard threshold

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Bootstrap iteration 47 produced NaN Jaccard")
- Log failure to `logs/step04_bootstrap_stability.log`
- Quit script immediately
- g_debug invoked (likely cause: bootstrap K-means convergence failure)

---

#### Step 5: Characterize Clusters

**Analysis Tool:** (determined by rq_tools - likely pandas groupby aggregation)
**Validation Tool:** (determined by rq_tools - likely `validate_cluster_summary_stats` from tools_catalog.md)

**What Validation Checks:**
- Output file `results/step05_cluster_summary.csv` has K rows (one per cluster)
- Required columns present (cluster_id, N, percentage, mean/SD/min/max for Intercept/Slope, label)
- Logical ordering: min <= mean <= max for each variable
- SD >= 0 (always true)
- Sum of N across clusters = 100
- Sum of percentage across clusters approximately 100.0
- All labels non-empty strings

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 1 has min_Intercept > mean_Intercept")
- Log failure to `logs/step05_characterize_clusters.log`
- Quit script immediately
- g_debug invoked

---

#### Step 6: Visualize Clusters

**Analysis Tool:** (determined by rq_tools - likely matplotlib/seaborn scatter plot wrapper)
**Validation Tool:** (determined by rq_tools - likely file existence + size check)

**What Validation Checks:**
- Output file `plots/step06_cluster_scatter.png` exists
- File size > 10 KB (non-empty plot)
- Image dimensions 800 x 600 pixels (verify via PIL)
- Log file `logs/step06_spherical_assumption_check.txt` exists (manual inspection notes)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Plot file created but empty (size <10 KB)")
- Log failure to `logs/step06_visualize_clusters.log`
- Quit script immediately
- g_debug invoked

---

## Summary

**Total Steps:** 7 (Step 0 + Steps 1-6)

**Estimated Runtime:** Medium (15-20 minutes total)
- Step 0: <1 minute (data loading)
- Step 1: <1 minute (standardization)
- Step 2: 5-10 minutes (K-means + BIC + silhouette + gap statistic for K=1-6)
- Step 3: <1 minute (final K-means fit)
- Step 4: 5-10 minutes (100 bootstrap iterations)
- Step 5: <1 minute (summary statistics)
- Step 6: <1 minute (scatter plot)

**Cross-RQ Dependencies:** RQ 5.13 (MUST complete first)

**Primary Outputs:**
- Cluster assignments per participant (`data/step03_cluster_assignments.csv`)
- Cluster centers in original scale (`results/step03_cluster_centers.csv`)
- Model selection table (`results/step02_model_selection.csv`)
- Bootstrap stability report (`results/step04_bootstrap_stability.txt`)
- Cluster characterization table (`results/step05_cluster_summary.csv`)
- Cluster scatter plot (`plots/step06_cluster_scatter.png`)

**Validation Coverage:** 100% (all 7 steps have validation requirements)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 10 user gate per workflow)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-11-27): Initial plan created by rq_planner agent for RQ 5.14 (K-means clustering on random effects from RQ 5.13)
