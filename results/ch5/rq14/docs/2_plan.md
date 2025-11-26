# Analysis Plan: RQ 5.14 - Latent Forgetting Profiles (K-means Clustering)

**Research Question:** 5.14
**Created:** 2025-11-26
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ uses K-means clustering to identify latent forgetting profiles based on participants' random intercepts and random slopes from RQ 5.13's mixed-effects model (Total domain). The analysis tests whether forgetting trajectories reflect discrete subgroups (e.g., "resilient" vs "vulnerable" memory) or continuous variation.

**Pipeline:** Clustering (K-means) with multi-metric model selection (BIC, silhouette, gap statistic) and bootstrap stability validation

**Steps:** 6 analysis steps (Step 0: Get Data + Steps 1-5: clustering workflow + plot data preparation)

**Estimated Runtime:** Medium (20-40 minutes total - Step 3 model selection most time-intensive)

**Key Methodological Features:**
- 4-part validation strategy: BIC model selection constrained by silhouette >=0.5, gap statistic for K=1 vs K>1, bootstrap stability (Jaccard >=0.75), minimum cluster size (>=10% sample)
- Standardization (z-scores) ensures equal weighting of intercepts and slopes in distance metric
- Spherical assumption validation via scatter plot (post-hoc check for K-means appropriateness)
- Remedial plan documented: if spherical assumption violated, rerun using GMM (Gaussian Mixture Models)

**Novel Analysis:**
This is the FIRST clustering RQ in the thesis (0% method reuse per rq_stats validation). All subsequent clustering RQs (if any) should reference this RQ's methodology.

---

## Analysis Plan

### Step 0: Get Data

**Purpose:** Load random effects from RQ 5.13 (clustering variables), theta scores from RQ 5.7 (for trajectory plotting), and TSVR mapping from RQ 5.7 (for timepoint labels)

**Dependencies:** None (first step, but requires RQ 5.13 and RQ 5.7 completion)

**Complexity:** Low (<5 minutes - file loading and basic merges)

**Input:**

**File 1:** results/ch5/rq13/data/random_effects_total.csv (assumed path from RQ 5.13)
**Source:** RQ 5.13 output (Total domain mixed-effects model)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, format: A###)
  - `Total_Intercept` (float, baseline ability at TSVR=0)
  - `Total_Slope` (float, forgetting rate, change in ability per unit time)
**Expected Rows:** 100 (one per participant)
**Expected Values:**
  - Total_Intercept: typically -1.0 to +1.0 range (centered around 0 if model included fixed intercept)
  - Total_Slope: typically -0.2 to +0.2 range (negative = forgetting, positive = improvement)

**File 2:** results/ch5/rq7/data/step03_theta_scores.csv (theta scores for trajectory plotting, optional)
**Source:** RQ 5.7 output (IRT theta estimates)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test)
  - `theta_common` (float, IRT ability estimate for common items dimension)
  - `se_common` (float, standard error)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Note:** Used for trajectory plotting by cluster (optional visualization)

**File 3:** results/ch5/rq7/data/step00_tsvr_mapping.csv (TSVR time variable)
**Source:** RQ 5.7 output (extracted from master.xlsx)
**Format:** CSV with columns:
  - `composite_ID` (string, format: UID_test)
  - `TSVR_hours` (float, time since VR session in hours)
  - `test` (string, test session identifier: T1, T2, T3, T4)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Note:** Used to convert composite_ID to timepoint for trajectory plotting

**Processing:**

1. **Load random effects from RQ 5.13:**
   - Read results/ch5/rq13/data/random_effects_total.csv
   - Verify all 100 participants present (no missing data)
   - Verify columns: UID, Total_Intercept, Total_Slope

2. **Load theta scores from RQ 5.7 (optional for plotting):**
   - Read results/ch5/rq7/data/step03_theta_scores.csv
   - Parse composite_ID to extract UID and test number
   - Merge with TSVR mapping on composite_ID

3. **Basic descriptive statistics:**
   - Compute mean, SD, min, max for Total_Intercept and Total_Slope
   - Report to console (sanity check for reasonable values)

**Output:**

**File 1:** data/step00_random_effects.csv
**Format:** CSV with columns:
  - `UID` (string)
  - `Total_Intercept` (float)
  - `Total_Slope` (float)
**Expected Rows:** 100 (one per participant)
**Note:** Copy of RQ 5.13 random effects for local analysis (prevents cross-RQ path dependencies in downstream steps)

**File 2:** data/step00_theta_tsvr.csv (optional, for plotting)
**Format:** CSV with columns:
  - `composite_ID` (string)
  - `UID` (string)
  - `test` (string)
  - `TSVR_hours` (float)
  - `theta_common` (float)
  - `se_common` (float)
**Expected Rows:** ~400 (100 participants x 4 tests)
**Note:** Merged theta + TSVR for trajectory plotting by cluster

**Validation Requirement:**

Validation tools MUST be used after data loading execution. Specific validation tools will be determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step00_random_effects.csv: 100 rows x 3 columns (UID: object, Total_Intercept: float64, Total_Slope: float64)
- data/step00_theta_tsvr.csv: 380-400 rows x 6 columns (composite_ID, UID, test, TSVR_hours, theta_common, se_common - all expected types)

*Value Ranges:*
- Total_Intercept in [-3, 3] (typical LMM random effect range)
- Total_Slope in [-1, 1] (forgetting rate per unit time - extreme values beyond +-1 unlikely)
- theta_common in [-3, 3] (standard IRT ability range)
- TSVR_hours in [0, 300] (0 = encoding, 300 = ~12.5 days maximum observed delay)

*Data Quality:*
- No NaN values in Total_Intercept or Total_Slope (all 100 participants must have random effects)
- Exactly 100 unique UIDs (full sample)
- No duplicate UIDs in step00_random_effects.csv
- theta_tsvr file: 380-400 rows acceptable (some participants may have missing tests)

*Log Validation:*
- Required pattern: "Loaded 100 random effects from RQ 5.13"
- Required pattern: "Descriptive statistics: Total_Intercept mean=X.XX, SD=X.XX"
- Forbidden patterns: "ERROR", "Missing random effects for UID", "NaN detected"
- Acceptable warnings: "Theta data missing for some composite_IDs" (if RQ 5.7 had exclusions)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 participants, found 87")
- Log failure to logs/step00_get_data.log
- Quit script immediately (do NOT proceed to Step 1)
- Check RQ 5.13 completion status (random effects file may be missing or incomplete)

---

### Step 1: Standardize Clustering Variables

**Purpose:** Standardize intercepts and slopes to z-scores (mean=0, SD=1) to ensure equal contribution to Euclidean distance metric used by K-means

**Dependencies:** Step 0 (requires random effects loaded)

**Complexity:** Low (<1 minute - simple transformation)

**Input:**

**File:** data/step00_random_effects.csv
**Format:** CSV with columns: UID, Total_Intercept, Total_Slope
**Expected Rows:** 100

**Processing:**

1. **Compute z-scores:**
   - For Total_Intercept: z_intercept = (Total_Intercept - mean_intercept) / sd_intercept
   - For Total_Slope: z_slope = (Total_Slope - mean_slope) / sd_slope

2. **Rationale:** K-means uses Euclidean distance, which is scale-sensitive. Without standardization, variables with larger variances dominate distance calculations. Intercepts (range ~0.5) and slopes (range ~0.1) have different scales - standardization ensures both contribute equally.

3. **Store standardization parameters:**
   - Save mean_intercept, sd_intercept, mean_slope, sd_slope for unstandardizing cluster centers later
   - Log to console for reproducibility

**Output:**

**File 1:** data/step01_clustering_input.csv
**Format:** CSV with columns:
  - `UID` (string)
  - `z_intercept` (float, standardized intercept)
  - `z_slope` (float, standardized slope)
**Expected Rows:** 100

**File 2:** data/step01_standardization_params.csv
**Format:** CSV with standardization parameters:
  - `variable` (string: "intercept" or "slope")
  - `mean` (float)
  - `sd` (float)
**Expected Rows:** 2 (one for intercept, one for slope)
**Note:** Used in Step 4 to unstandardize cluster centers for interpretation

**Validation Requirement:**

Validation tools MUST be used after standardization execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_clustering_input.csv: 100 rows x 3 columns (UID: object, z_intercept: float64, z_slope: float64)
- data/step01_standardization_params.csv: 2 rows x 3 columns (variable: object, mean: float64, sd: float64)

*Value Ranges:*
- z_intercept: typically in [-3, 3] (>99% of normal distribution)
- z_slope: typically in [-3, 3] (extreme z-scores beyond +-3 indicate outliers)
- mean_intercept: unrestricted (depends on RQ 5.13 model specification)
- sd_intercept: >0 (must be positive, typically 0.1-1.0 range)
- mean_slope: unrestricted (typically negative for forgetting)
- sd_slope: >0 (must be positive, typically 0.01-0.1 range)

*Data Quality:*
- No NaN values in z_intercept or z_slope
- z_intercept and z_slope should have mean ~0.0 (within rounding error: +-0.01)
- z_intercept and z_slope should have SD ~1.0 (within rounding error: 0.99-1.01)
- Exactly 100 rows in clustering_input.csv
- Exactly 2 rows in standardization_params.csv

*Log Validation:*
- Required pattern: "Standardization complete: z_intercept mean=0.00, SD=1.00"
- Required pattern: "Standardization complete: z_slope mean=0.00, SD=1.00"
- Required pattern: "Saved standardization parameters for unstandardization"
- Forbidden patterns: "ERROR", "Division by zero" (would indicate zero variance - impossible for random effects)

**Expected Behavior on Validation Failure:**
- Raise error with specific message (e.g., "z_intercept SD = 0.85, expected ~1.0")
- Log failure to logs/step01_standardize.log
- Quit immediately (standardization must be correct for K-means to work properly)

---

### Step 2: Determine Optimal Number of Clusters

**Purpose:** Test K=1 to K=6 clusters, compute BIC, silhouette score, and gap statistic for each K, select optimal K using BIC minimum constrained by silhouette >=0.5 and validated by gap statistic

**Dependencies:** Step 1 (requires standardized clustering variables)

**Complexity:** High (15-25 minutes - fits 6 models with bootstrap for gap statistic)

**Input:**

**File:** data/step01_clustering_input.csv
**Format:** CSV with columns: UID, z_intercept, z_slope
**Expected Rows:** 100

**Processing:**

1. **For each K in {1, 2, 3, 4, 5, 6}:**
   - Fit K-means with K clusters (random_state=42, n_init=50)
   - Compute inertia (within-cluster sum of squares)
   - Compute BIC = n * log(inertia / n) + K * log(n) where n=100
   - Compute average silhouette score (sklearn.metrics.silhouette_score)
   - Note: K=1 has undefined silhouette (set to NaN or 0.0 for table reporting)

2. **Gap statistic (validates K=1 vs K>1):**
   - For each K in {1, 2, 3, 4, 5, 6}:
     - Generate 100 bootstrap samples from uniform distribution matching observed data range
     - Fit K-means to each bootstrap sample, compute mean log(inertia)
     - Gap(K) = mean_bootstrap_log_inertia - observed_log_inertia
     - Compute SE of gap statistic across 100 bootstraps
   - Decision rule: Choose smallest K such that Gap(K) >= Gap(K+1) - SE(K+1)
   - If gap statistic selects K=1: conclude no distinct latent profiles (continuous variation only)

3. **Selection criterion:**
   - Primary: Choose K with minimum BIC
   - Constraint: Selected K must have silhouette >=0.5 (reasonable cluster quality threshold)
   - If BIC minimum has silhouette <0.5: choose next-lowest BIC with silhouette >=0.5
   - Constraint: All clusters must contain >=10% of sample (n>=10 participants)
   - If selected K produces any cluster <10%: reduce K by 1 and recheck
   - Validation: If gap statistic selected K=1, report "No latent profiles detected" and terminate analysis
   - Validation: If gap statistic selected K>1, proceed with BIC-selected K (constrained by silhouette and cluster size)

4. **Generate diagnostic plots:**
   - Plot 1: Elbow plot (inertia vs K)
   - Plot 2: BIC plot (BIC vs K, mark optimal K with vertical line)
   - Plot 3: Silhouette plot (silhouette score vs K, horizontal line at 0.5 threshold)
   - Plot 4: Gap statistic plot (Gap(K) vs K with error bars = +-SE, mark selected K)

**Output:**

**File 1:** results/step02_model_selection.csv
**Format:** CSV with columns:
  - `K` (int, number of clusters: 1, 2, 3, 4, 5, 6)
  - `inertia` (float, within-cluster sum of squares)
  - `BIC` (float, Bayesian Information Criterion)
  - `silhouette` (float, average silhouette score, NaN for K=1)
  - `gap` (float, gap statistic)
  - `gap_se` (float, standard error of gap statistic)
**Expected Rows:** 6 (one per K value tested)

**File 2:** results/step02_optimal_k.txt
**Format:** Plain text summary
**Content:**
  - Optimal K selected (e.g., "Optimal K = 3")
  - BIC value for optimal K
  - Silhouette score for optimal K
  - Gap statistic result (K=1 vs K>1 decision)
  - Constraint checks passed (silhouette >=0.5, cluster sizes >=10%)

**File 3:** plots/step02_elbow_plot.png
**Format:** PNG (800 x 600 @ 300 DPI)
**Content:** Inertia vs K with elbow point marked

**File 4:** plots/step02_bic_plot.png
**Format:** PNG (800 x 600 @ 300 DPI)
**Content:** BIC vs K with optimal K marked (vertical line)

**File 5:** plots/step02_silhouette_plot.png
**Format:** PNG (800 x 600 @ 300 DPI)
**Content:** Silhouette score vs K with 0.5 threshold (horizontal dashed line)

**File 6:** plots/step02_gap_plot.png
**Format:** PNG (800 x 600 @ 300 DPI)
**Content:** Gap statistic vs K with error bars (+-SE) and selected K marked

**Validation Requirement:**

Validation tools MUST be used after model selection execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step02_model_selection.csv: 6 rows x 6 columns (K: int64, inertia: float64, BIC: float64, silhouette: float64, gap: float64, gap_se: float64)
- results/step02_optimal_k.txt: text file containing optimal K decision
- plots/step02_elbow_plot.png: PNG file exists
- plots/step02_bic_plot.png: PNG file exists
- plots/step02_silhouette_plot.png: PNG file exists
- plots/step02_gap_plot.png: PNG file exists

*Value Ranges:*
- K in {1, 2, 3, 4, 5, 6} (exactly these 6 values)
- inertia: decreasing as K increases (monotonic decrease expected)
- BIC: must have minimum at some K in {1, 2, 3, 4, 5, 6}
- silhouette: in [0, 1] for K>=2, NaN or 0.0 for K=1
- gap: positive values expected (observed clustering better than random)
- gap_se: positive values (standard errors must be >0)
- Optimal K in {1, 2, 3, 4, 5, 6} (within tested range)

*Data Quality:*
- All 6 K values present in model_selection.csv
- No NaN values in inertia, BIC, gap, gap_se columns
- silhouette NaN only for K=1 row
- BIC minimum should be at K>=2 (K=1 typically has poor BIC unless no structure)
- Inertia decreases monotonically (if not, indicates numerical instability)
- optimal_k.txt contains exactly one integer K value

*Log Validation:*
- Required pattern: "Testing K=1 through K=6"
- Required pattern: "BIC minimum at K=X"
- Required pattern: "Gap statistic selected K=X"
- Required pattern: "Silhouette constraint: K=X has silhouette=X.XX (>=0.5: pass/fail)"
- Required pattern: "Cluster size constraint: all clusters >=10% sample (pass/fail)"
- Forbidden patterns: "ERROR", "Convergence failed for K=X", "Negative silhouette" (if K>=2)

**Expected Behavior on Validation Failure:**
- Raise error with specific message (e.g., "BIC minimum K=4 has silhouette=0.42 <0.5, next K=3 also fails")
- Log failure to logs/step02_model_selection.log
- If NO K satisfies constraints: report "No valid clustering solution found" and QUIT
- If gap statistic selects K=1: report "No latent profiles detected, continuous variation only" and TERMINATE analysis (this is a valid scientific outcome, not an error)

**Scientific Outcome Note:**
If gap statistic selects K=1, this is a scientifically valid result meaning "no discrete latent forgetting profiles detected, individual differences are continuous rather than categorical." This should be reported in results, not treated as analysis failure.

---

### Step 3: Fit Final K-means Model

**Purpose:** Fit K-means with optimal K selected in Step 2, extract cluster assignments and cluster centers

**Dependencies:** Step 2 (requires optimal K determination)

**Complexity:** Low (1-2 minutes - single model fit)

**Input:**

**File 1:** data/step01_clustering_input.csv
**Format:** CSV with columns: UID, z_intercept, z_slope
**Expected Rows:** 100

**File 2:** results/step02_optimal_k.txt
**Format:** Plain text containing optimal K (e.g., "Optimal K = 3")
**Note:** Parse this file to extract K value for model fitting

**Processing:**

1. **Parse optimal K:**
   - Read results/step02_optimal_k.txt
   - Extract integer K value (e.g., K=3)

2. **Fit K-means model:**
   - sklearn.cluster.KMeans(n_clusters=K, random_state=42, n_init=50)
   - random_state=42: reproducibility
   - n_init=50: run K-means 50 times with different initializations, select best solution (prevents local minima)
   - Fit to z_intercept and z_slope columns

3. **Extract cluster assignments:**
   - model.labels_ gives cluster assignment (0, 1, ..., K-1) for each participant
   - Add cluster column to UID

4. **Extract cluster centers:**
   - model.cluster_centers_ gives (z_intercept, z_slope) for each cluster center
   - Store in standardized scale for now (will unstandardize in Step 4)

5. **Compute cluster sizes:**
   - Count participants per cluster
   - Report to console (e.g., "Cluster 0: 35 participants, Cluster 1: 42, Cluster 2: 23")

**Output:**

**File 1:** data/step03_cluster_assignments.csv
**Format:** CSV with columns:
  - `UID` (string)
  - `cluster` (int, range 0 to K-1)
**Expected Rows:** 100
**Note:** Each participant assigned to exactly one cluster

**File 2:** data/step03_cluster_centers_standardized.csv
**Format:** CSV with columns:
  - `cluster` (int, range 0 to K-1)
  - `z_intercept` (float, cluster center on standardized intercept)
  - `z_slope` (float, cluster center on standardized slope)
**Expected Rows:** K (one row per cluster)

**File 3:** results/step03_cluster_sizes.csv
**Format:** CSV with columns:
  - `cluster` (int)
  - `n` (int, number of participants)
  - `proportion` (float, n / 100)
**Expected Rows:** K

**Validation Requirement:**

Validation tools MUST be used after K-means fitting execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_cluster_assignments.csv: 100 rows x 2 columns (UID: object, cluster: int64)
- data/step03_cluster_centers_standardized.csv: K rows x 3 columns (cluster: int64, z_intercept: float64, z_slope: float64)
- results/step03_cluster_sizes.csv: K rows x 3 columns (cluster: int64, n: int64, proportion: float64)

*Value Ranges:*
- cluster in {0, 1, ..., K-1} (all cluster IDs present)
- z_intercept (centers): typically in [-2, 2] (cluster centers near population mean)
- z_slope (centers): typically in [-2, 2]
- n: sum across all clusters = 100 (all participants assigned)
- proportion: in [0, 1], sum across all clusters = 1.0 (within rounding: 0.99-1.01)
- Each cluster must have n >= 10 (10% minimum constraint from Step 2)

*Data Quality:*
- All 100 participants present in cluster_assignments.csv
- No NaN values in cluster column
- No duplicate UIDs
- Cluster IDs are consecutive integers starting from 0
- cluster_sizes.csv sums to exactly 100 participants
- proportions sum to 1.0 (within rounding error)

*Log Validation:*
- Required pattern: "Fitted K-means with K=X clusters"
- Required pattern: "Cluster sizes: Cluster 0: N participants, Cluster 1: M participants, ..."
- Required pattern: "All clusters meet >=10% threshold (pass)"
- Forbidden patterns: "ERROR", "Empty cluster detected", "Cluster size <10 participants"

**Expected Behavior on Validation Failure:**
- Raise error with specific message (e.g., "Cluster 2 has only 7 participants, below 10% threshold")
- Log failure to logs/step03_fit_kmeans.log
- If cluster too small detected: reduce K by 1 and refit (remedial action)
- If K=2 produces cluster <10: report "No valid clustering solution, K=1 only" and terminate

---

### Step 4: Bootstrap Cluster Stability Validation

**Purpose:** Assess cluster stability via bootstrap resampling (Jaccard similarity between original and bootstrap cluster assignments), acceptance criterion: mean Jaccard >=0.75

**Dependencies:** Step 3 (requires original cluster assignments)

**Complexity:** High (10-20 minutes - 100 bootstrap iterations of K-means fitting)

**Input:**

**File 1:** data/step01_clustering_input.csv
**Format:** CSV with columns: UID, z_intercept, z_slope
**Expected Rows:** 100

**File 2:** data/step03_cluster_assignments.csv
**Format:** CSV with columns: UID, cluster
**Expected Rows:** 100
**Note:** Original cluster assignments to compare against bootstrap assignments

**File 3:** results/step02_optimal_k.txt
**Format:** Plain text containing optimal K
**Note:** Use same K for all bootstrap iterations

**Processing:**

1. **Bootstrap resampling (100 iterations):**
   - For each iteration i in {1, 2, ..., 100}:
     - Resample 100 participants WITH replacement from clustering_input.csv
     - Some participants sampled multiple times, others not sampled
     - Fit K-means with optimal K (random_state=42+i for different initialization per bootstrap)
     - Extract bootstrap cluster assignments
     - For participants in BOTH original and bootstrap samples:
       - Compute Jaccard similarity = (agreements) / (agreements + disagreements)
       - Jaccard measures cluster assignment consistency
     - Store Jaccard_i for iteration i

2. **Aggregate stability metrics:**
   - Compute mean Jaccard across 100 iterations
   - Compute 95% CI for mean Jaccard (percentile method: 2.5th and 97.5th percentiles)
   - Assign stability rating:
     - mean Jaccard >=0.85: "Highly Stable"
     - mean Jaccard >=0.75: "Stable"
     - mean Jaccard >=0.6: "Questionable"
     - mean Jaccard <0.6: "Unstable"

3. **Acceptance criterion (per Liu 2022 guidelines):**
   - If mean Jaccard >=0.75: Accept clustering solution as stable
   - If mean Jaccard <0.75: Reduce K by 1 and retest stability
   - Iterate until mean Jaccard >=0.75 or K=1

4. **Report stability results:**
   - Mean Jaccard with 95% CI
   - Stability rating
   - Bootstrap distribution histogram (Jaccard values across 100 iterations)

**Output:**

**File 1:** results/step04_bootstrap_stability.csv
**Format:** CSV with columns:
  - `iteration` (int, 1 to 100)
  - `jaccard` (float, Jaccard similarity for that bootstrap sample)
**Expected Rows:** 100

**File 2:** results/step04_stability_summary.txt
**Format:** Plain text summary
**Content:**
  - Mean Jaccard with 95% CI
  - Stability rating (Highly Stable / Stable / Questionable / Unstable)
  - Acceptance decision (Accept K=X / Reduce to K=X-1)

**File 3:** plots/step04_bootstrap_histogram.png
**Format:** PNG (800 x 600 @ 300 DPI)
**Content:** Histogram of Jaccard values across 100 bootstrap iterations, vertical line at mean, shaded region for 95% CI

**Validation Requirement:**

Validation tools MUST be used after bootstrap stability execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- results/step04_bootstrap_stability.csv: 100 rows x 2 columns (iteration: int64, jaccard: float64)
- results/step04_stability_summary.txt: text file containing stability metrics
- plots/step04_bootstrap_histogram.png: PNG file exists

*Value Ranges:*
- iteration in {1, 2, ..., 100} (exactly 100 bootstrap samples)
- jaccard in [0, 1] (Jaccard similarity bounded)
- mean_jaccard in [0, 1]
- 95% CI bounds in [0, 1]
- Expected mean_jaccard >=0.75 (acceptance threshold per concept.md)

*Data Quality:*
- All 100 iterations present in bootstrap_stability.csv
- No NaN values in jaccard column
- mean_jaccard reported in summary.txt
- 95% CI reported in summary.txt
- Stability rating assigned (one of four categories)

*Log Validation:*
- Required pattern: "Bootstrap stability: 100 iterations complete"
- Required pattern: "Mean Jaccard = X.XX (95% CI: [X.XX, X.XX])"
- Required pattern: "Stability rating: [Highly Stable / Stable / Questionable / Unstable]"
- Required pattern: "Acceptance decision: [Accept K=X / Reduce to K=X-1]"
- Forbidden patterns: "ERROR", "Bootstrap failed for iteration X", "Jaccard = NaN"

**Expected Behavior on Validation Failure:**
- Raise error with specific message (e.g., "Mean Jaccard = 0.62 <0.75, unstable clustering")
- Log failure to logs/step04_bootstrap_stability.log
- If mean Jaccard <0.75: reduce K by 1, refit K-means (Step 3), retest stability (Step 4)
- If K=2 fails stability: report "No stable clustering solution, K=1 only" and terminate

**Remedial Action:**
If clustering solution fails stability check (mean Jaccard <0.75), the analysis should reduce K by 1 and repeat Steps 3-4 until stability criterion met or K=1 reached. This is scientifically valid remedial action (not error).

---

### Step 5: Characterize and Interpret Clusters

**Purpose:** Unstandardize cluster centers to original scale, compute summary statistics per cluster, assign interpretive labels based on intercept (baseline) and slope (forgetting rate)

**Dependencies:** Steps 1, 3, 4 (requires standardization parameters, cluster assignments, and stability validation passed)

**Complexity:** Low (1-2 minutes - descriptive statistics)

**Input:**

**File 1:** data/step00_random_effects.csv
**Format:** CSV with columns: UID, Total_Intercept, Total_Slope (original scale)
**Expected Rows:** 100

**File 2:** data/step03_cluster_assignments.csv
**Format:** CSV with columns: UID, cluster
**Expected Rows:** 100

**File 3:** data/step03_cluster_centers_standardized.csv
**Format:** CSV with columns: cluster, z_intercept, z_slope
**Expected Rows:** K

**File 4:** data/step01_standardization_params.csv
**Format:** CSV with columns: variable, mean, sd
**Expected Rows:** 2

**Processing:**

1. **Unstandardize cluster centers:**
   - For each cluster center (z_intercept, z_slope):
     - intercept_original = z_intercept * sd_intercept + mean_intercept
     - slope_original = z_slope * sd_slope + mean_slope
   - Store unstandardized centers for interpretation

2. **Merge cluster assignments with original random effects:**
   - Merge step00_random_effects.csv with step03_cluster_assignments.csv on UID
   - Result: UID, Total_Intercept, Total_Slope, cluster

3. **Compute summary statistics per cluster:**
   - Group by cluster
   - For Total_Intercept: mean, SD, min, max
   - For Total_Slope: mean, SD, min, max
   - Report cluster sizes (from Step 3)

4. **Assign interpretive labels:**
   - Based on cluster center positions:
     - Intercept: High (>0.5), Average (-0.5 to 0.5), Low (<-0.5)
     - Slope: Slow forgetting (>-0.05), Average (-0.15 to -0.05), Fast forgetting (<-0.15)
   - Example labels:
     - Cluster 0: "High Baseline, Slow Forgetting" (resilient memory)
     - Cluster 1: "Average Baseline, Average Forgetting" (typical memory)
     - Cluster 2: "Low Baseline, Fast Forgetting" (vulnerable memory)
   - Note: Exact thresholds should be data-driven based on observed distribution

**Output:**

**File 1:** data/step05_cluster_centers_original.csv
**Format:** CSV with columns:
  - `cluster` (int)
  - `intercept` (float, original scale)
  - `slope` (float, original scale)
**Expected Rows:** K

**File 2:** results/step05_cluster_summary.csv
**Format:** CSV with columns:
  - `cluster` (int)
  - `n` (int, cluster size)
  - `intercept_mean` (float)
  - `intercept_sd` (float)
  - `intercept_min` (float)
  - `intercept_max` (float)
  - `slope_mean` (float)
  - `slope_sd` (float)
  - `slope_min` (float)
  - `slope_max` (float)
  - `label` (string, interpretive label)
**Expected Rows:** K

**File 3:** results/step05_cluster_labels.txt
**Format:** Plain text summary
**Content:**
  - Cluster 0: [Label] (n=X, intercept=Y.YY, slope=Z.ZZ)
  - Cluster 1: [Label] (n=X, intercept=Y.YY, slope=Z.ZZ)
  - [... for all K clusters]

**Validation Requirement:**

Validation tools MUST be used after cluster characterization execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_cluster_centers_original.csv: K rows x 3 columns (cluster: int64, intercept: float64, slope: float64)
- results/step05_cluster_summary.csv: K rows x 11 columns (cluster, n, intercept stats, slope stats, label)
- results/step05_cluster_labels.txt: text file with K cluster labels

*Value Ranges:*
- intercept (centers): typically in [-1, 1] (original LMM random effect scale)
- slope (centers): typically in [-0.3, 0.1] (forgetting rate, usually negative)
- intercept_mean, slope_mean: similar ranges as centers
- intercept_sd, slope_sd: >0 (positive variance within clusters)
- n: sum across clusters = 100

*Data Quality:*
- All K clusters present in output files
- No NaN values in intercept, slope columns
- Cluster labels assigned (one per cluster)
- Summary statistics (mean, SD, min, max) mathematically consistent (min <= mean <= max, SD >= 0)

*Log Validation:*
- Required pattern: "Unstandardized cluster centers to original scale"
- Required pattern: "Cluster 0: [Label] (n=X, intercept=Y.YY, slope=Z.ZZ)"
- Required pattern: "All K clusters characterized"
- Forbidden patterns: "ERROR", "NaN in cluster center", "Negative SD detected"

**Expected Behavior on Validation Failure:**
- Raise error with specific message (e.g., "Cluster 1 SD = -0.05, impossible negative variance")
- Log failure to logs/step05_characterize_clusters.log
- Check unstandardization logic (mean/SD parameters may be incorrect)

---

### Step 6: Prepare Cluster Scatter Plot Data

**Purpose:** Create plot source CSV for 2D scatter plot (intercepts vs slopes, colored by cluster membership) with cluster centers overlaid - Option B architecture

**Dependencies:** Steps 3, 5 (requires cluster assignments and original-scale cluster centers)

**Complexity:** Low (1-2 minutes - data aggregation for plotting)

**Plot Description:** Scatter plot showing participants in 2D space (x-axis = Total_Intercept, y-axis = Total_Slope), points colored by cluster membership, large markers at cluster centers, reference lines at x=0 and y=0 for interpretation

**Required Data Sources:**
- data/step00_random_effects.csv (columns: UID, Total_Intercept, Total_Slope)
- data/step03_cluster_assignments.csv (columns: UID, cluster)
- data/step05_cluster_centers_original.csv (columns: cluster, intercept, slope)

**Output (Plot Source CSV):** plots/step06_cluster_scatter_data.csv

**Required Columns:**
- `Total_Intercept` (float): x-axis position (original scale, not standardized)
- `Total_Slope` (float): y-axis position (original scale)
- `cluster` (int): cluster membership for color coding (0, 1, ..., K-1)
- `is_center` (bool): True for cluster centers, False for individual participants
- `label` (string): interpretive label for cluster centers (empty for participants)

**Expected Rows:** 100 + K (100 participants + K cluster centers)

**Aggregation Logic:**
1. Merge step00_random_effects.csv with step03_cluster_assignments.csv on UID
2. Add column is_center = False for all participants
3. Append K cluster center rows from step05_cluster_centers_original.csv
4. For cluster centers: set is_center = True, copy interpretive label from step05_cluster_summary.csv
5. Select and rename columns to match required schema
6. Save to plots/step06_cluster_scatter_data.csv

**Validation Requirement:**

Validation tools MUST be used after plot data preparation execution. Specific validation tools determined by rq_tools.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- plots/step06_cluster_scatter_data.csv exists (exact path)
- Expected rows: 100 + K (e.g., 103 if K=3)
- Expected columns: 5 (Total_Intercept, Total_Slope, cluster, is_center, label)
- Data types: float (Total_Intercept, Total_Slope), int (cluster), bool (is_center), object (label)

*Value Ranges:*
- Total_Intercept in [-3, 3] (typical LMM random effect range)
- Total_Slope in [-1, 1] (forgetting rate range)
- cluster in {0, 1, ..., K-1} (all cluster IDs present)
- is_center: False for 100 rows (participants), True for K rows (centers)

*Data Quality:*
- No NaN values in Total_Intercept, Total_Slope, cluster columns
- Exactly 100 + K rows (no missing participants or centers)
- K rows with is_center = True (one per cluster)
- 100 rows with is_center = False (one per participant)
- label column non-empty for is_center = True rows
- label column empty for is_center = False rows

*Log Validation:*
- Required pattern: "Plot data preparation complete: {100+K} rows created"
- Required pattern: "All K clusters represented in scatter data"
- Forbidden patterns: "ERROR", "NaN values detected", "Missing cluster center"

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 103 rows, found 100 - missing cluster centers")
- Log failure to logs/step06_prepare_plot_data.log
- Quit script immediately (do NOT proceed to rq_plots)
- Check step05 outputs (cluster centers may be missing)

**Plotting Function (rq_plots will call):** Scatter plot with cluster membership coloring
- rq_plots agent maps this description to specific tools/plots.py function (likely new function to be created)
- Plot reads plots/step06_cluster_scatter_data.csv (created by this step)
- No data aggregation in rq_plots (visualization only per Option B)
- Plot specifications:
  - x-axis: Total_Intercept (label: "Random Intercept (Baseline Ability)")
  - y-axis: Total_Slope (label: "Random Slope (Forgetting Rate)")
  - Color by cluster (use categorical color palette, K distinct colors)
  - Marker size: small for participants (is_center=False), large for centers (is_center=True)
  - Marker shape: circles for participants, stars for centers
  - Reference lines: vertical at x=0, horizontal at y=0 (dashed gray lines)
  - Legend: cluster labels (from label column for centers)
  - Title: "Latent Forgetting Profiles (K={K} Clusters)"

**Spherical Assumption Validation (Manual):**
After plotting, visually inspect cluster shapes. If clusters appear roughly spherical (circular, isotropic variance), K-means assumption satisfied. If clusters appear elongated or irregular, document in results that spherical assumption may be violated and consider remedial analysis using GMM (Gaussian Mixture Models) for elliptical cluster modeling.

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 0 -> Step 1:** Random effects (original scale) to standardized z-scores
- Input: Total_Intercept, Total_Slope (original scale, different variances)
- Output: z_intercept, z_slope (standardized scale, mean=0, SD=1)
- Rationale: Equal weighting in Euclidean distance metric

**Step 1 -> Step 3:** Standardized features to cluster assignments
- Input: z_intercept, z_slope (continuous variables)
- Output: cluster (categorical variable, 0 to K-1)
- Rationale: K-means partitions continuous space into discrete clusters

**Step 3 -> Step 5:** Standardized cluster centers to original scale
- Input: z_intercept, z_slope (cluster centers, standardized)
- Output: intercept, slope (cluster centers, original scale)
- Rationale: Interpretation requires original scale (meaningful units)

**Step 5 -> Step 6:** Merge participants + cluster centers for plotting
- Input: Participants (UID, Total_Intercept, Total_Slope, cluster), Centers (cluster, intercept, slope, label)
- Output: Combined data (Total_Intercept, Total_Slope, cluster, is_center, label)
- Rationale: Single data source for scatter plot simplifies rq_plots logic

### Column Naming Conventions

Per names.md (existing conventions):
- `UID`: participant identifier (no underscore)
- `composite_ID`: UID_test format (for theta scores if used)
- `TSVR_hours`: time variable (uppercase acronym + unit)

New conventions for clustering (to be added to names.md after RQ 5.14):
- `z_intercept`: standardized intercept (z-score)
- `z_slope`: standardized slope (z-score)
- `Total_Intercept`: random intercept from LMM (original scale)
- `Total_Slope`: random slope from LMM (original scale)
- `cluster`: cluster assignment (integer 0 to K-1)
- `is_center`: Boolean flag for cluster centers vs participants

### Data Type Constraints

**Clustering variables:**
- z_intercept, z_slope: float64, no NaN (all participants must have values)
- Total_Intercept, Total_Slope: float64, no NaN

**Cluster assignments:**
- cluster: int64, values in {0, 1, ..., K-1}, no NaN

**Standardization parameters:**
- mean, sd: float64, sd must be >0 (division by zero check)

**Bootstrap stability:**
- jaccard: float64, range [0, 1], no NaN

---

## Cross-RQ Dependencies

### Dependency Type 2: DERIVED Data from Other RQs (Dependencies Exist)

**This RQ requires outputs from:**

- **RQ 5.13** (Mixed-Effects Model - Total Domain)
  - File: results/ch5/rq13/data/random_effects_total.csv
  - Used in: Step 0 (primary clustering input)
  - Rationale: RQ 5.13 estimates random intercepts and slopes for each participant. This RQ clusters participants based on those random effects to identify latent forgetting profiles.

- **RQ 5.7** (IRT Calibration - Common Items) [OPTIONAL for trajectory plotting]
  - File: results/ch5/rq7/data/step03_theta_scores.csv
  - File: results/ch5/rq7/data/step00_tsvr_mapping.csv
  - Used in: Step 0 (optional - for trajectory plotting by cluster)
  - Rationale: Theta scores enable visualization of forgetting trajectories by cluster membership.

**Execution Order Constraint:**
1. RQ 5.13 must complete first (provides random_effects_total.csv)
2. RQ 5.7 must complete if trajectory plotting desired (provides theta scores + TSVR)
3. This RQ executes after dependencies complete

**Data Source Boundaries:**
- **RAW data:** None (this RQ uses only DERIVED data from other RQs)
- **DERIVED data:** Random effects from RQ 5.13 (primary), theta scores from RQ 5.7 (optional)
- **Scope:** This RQ performs clustering analysis only (no IRT, no LMM fitting - uses outputs from those RQs)

**Validation:**
- Step 0: Check results/ch5/rq13/data/random_effects_total.csv exists (circuit breaker: EXPECTATIONS ERROR if absent)
- Step 0: Check that random_effects_total.csv contains all 100 participants (circuit breaker: STEP ERROR if <100)
- If random effects file missing -> quit with error -> user must execute RQ 5.13 first

---

## Validation Requirements

**CRITICAL MANDATE:**

Every analysis step in this plan MUST use validation tools after analysis tool execution.

This is not optional. This is the core architectural principle preventing cascading failures observed in v3.0 (where analysis errors propagated undetected through 5+ downstream steps before discovery).

**Exact Specification Requirement:**

> "Validation tools MUST be used after analysis tool execution"

**Implementation:**
- rq_tools (Step 11 workflow) will read tools_catalog.md validation tools section
- rq_tools will specify BOTH analysis tool + validation tool per step in 3_tools.yaml
- rq_analysis (Step 12 workflow) will embed validation tool call AFTER analysis tool call in 4_analysis.yaml
- g_code (Step 14 workflow) will generate stepNN_*.py scripts with validation function calls
- bash execution (Step 14 workflow) will run analysis -> validation -> error on validation failure

**Downstream Agent Requirements:**
- **rq_tools:** MUST specify validation tool for EVERY analysis step (no exceptions)
- **rq_analysis:** MUST embed validation tool call for EVERY analysis step (no exceptions)
- **g_code:** MUST generate code with validation function calls (no exceptions)
- **rq_inspect:** MUST verify validation ran successfully (checks logs/stepNN_*.log for validation output)

### Validation Requirements By Step

#### Step 0: Get Data

**Analysis Tool:** (determined by rq_tools - likely pandas read_csv + merge operations)
**Validation Tool:** (determined by rq_tools - likely custom data format validation)

**What Validation Checks:**
- Output files exist (step00_random_effects.csv, step00_theta_tsvr.csv)
- Expected column counts (3 for random effects, 6 for theta_tsvr)
- Expected row counts (100 for random effects, 380-400 for theta_tsvr)
- No unexpected NaN patterns (0% NaN in Total_Intercept, Total_Slope)
- UID format correct (A### pattern)
- Value ranges reasonable (intercepts ~-1 to +1, slopes ~-0.3 to +0.1)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure message (e.g., "Expected 100 participants, found 87 in random_effects_total.csv")
- Log failure to logs/step00_get_data.log
- Quit script immediately (do NOT proceed to Step 1)
- Check RQ 5.13 completion status (dependency may be incomplete)

---

#### Step 1: Standardize Clustering Variables

**Analysis Tool:** (determined by rq_tools - likely custom standardization function or sklearn.preprocessing.StandardScaler)
**Validation Tool:** (determined by rq_tools - likely custom validation checking mean=0, SD=1)

**What Validation Checks:**
- Output file exists (step01_clustering_input.csv)
- Standardization successful (z_intercept mean ~0.0, SD ~1.0)
- Standardization successful (z_slope mean ~0.0, SD ~1.0)
- No NaN values introduced during standardization
- Standardization parameters saved (step01_standardization_params.csv exists)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "z_intercept SD = 0.85, expected ~1.0")
- Log failure to logs/step01_standardize.log
- Quit script immediately
- Check standardization logic (division by zero, incorrect SD calculation)

---

#### Step 2: Determine Optimal Number of Clusters

**Analysis Tool:** (determined by rq_tools - likely sklearn.cluster.KMeans + custom BIC/silhouette/gap functions)
**Validation Tool:** (determined by rq_tools - likely custom validation for model selection outputs)

**What Validation Checks:**
- Output file exists (step02_model_selection.csv)
- All K in {1, 2, 3, 4, 5, 6} present
- BIC has minimum at some K
- Silhouette scores in [0, 1] for K>=2
- Gap statistic positive values
- Optimal K selected and documented (step02_optimal_k.txt)
- Constraint checks passed (silhouette >=0.5 for selected K, cluster sizes >=10%)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "No K satisfies silhouette >=0.5 constraint")
- Log failure to logs/step02_model_selection.log
- If no valid K: report "No stable clustering solution found" and QUIT
- If gap statistic selects K=1: report "Continuous variation only, no latent profiles" and TERMINATE (valid scientific outcome)

---

#### Step 3: Fit Final K-means Model

**Analysis Tool:** (determined by rq_tools - likely sklearn.cluster.KMeans)
**Validation Tool:** (determined by rq_tools - likely custom cluster assignment validation)

**What Validation Checks:**
- Output files exist (step03_cluster_assignments.csv, step03_cluster_centers_standardized.csv, step03_cluster_sizes.csv)
- All 100 participants assigned to clusters
- Cluster IDs consecutive integers (0 to K-1)
- Cluster sizes sum to 100
- Cluster sizes all >=10 (10% minimum)
- Cluster centers within reasonable z-score range (typically -2 to +2)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 2 has only 7 participants, below 10% threshold")
- Log failure to logs/step03_fit_kmeans.log
- If cluster size too small: reduce K by 1 and refit (remedial action)

---

#### Step 4: Bootstrap Cluster Stability Validation

**Analysis Tool:** (determined by rq_tools - likely custom bootstrap function with KMeans + Jaccard computation)
**Validation Tool:** (determined by rq_tools - likely custom stability metric validation)

**What Validation Checks:**
- Output file exists (step04_bootstrap_stability.csv)
- 100 bootstrap iterations completed
- Jaccard values in [0, 1]
- Mean Jaccard computed
- 95% CI computed
- Stability rating assigned
- Acceptance criterion checked (mean Jaccard >=0.75)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Mean Jaccard = 0.62 <0.75, unstable clustering")
- Log failure to logs/step04_bootstrap_stability.log
- If unstable: reduce K by 1, refit K-means (Step 3), retest stability (remedial action)

---

#### Step 5: Characterize and Interpret Clusters

**Analysis Tool:** (determined by rq_tools - likely pandas groupby + custom unstandardization)
**Validation Tool:** (determined by rq_tools - likely custom cluster summary validation)

**What Validation Checks:**
- Output files exist (step05_cluster_centers_original.csv, step05_cluster_summary.csv, step05_cluster_labels.txt)
- All K clusters characterized
- Summary statistics mathematically consistent (min <= mean <= max, SD >= 0)
- No NaN values in cluster centers
- Interpretive labels assigned (one per cluster)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Cluster 1 SD = -0.05, impossible negative variance")
- Log failure to logs/step05_characterize_clusters.log
- Check unstandardization logic

---

#### Step 6: Prepare Cluster Scatter Plot Data

**Analysis Tool:** (determined by rq_tools - likely pandas merge + concatenate)
**Validation Tool:** (determined by rq_tools - likely custom plot data validation)

**What Validation Checks:**
- Output file exists (plots/step06_cluster_scatter_data.csv)
- Expected row count (100 + K)
- Required columns present (Total_Intercept, Total_Slope, cluster, is_center, label)
- No NaN values in critical columns
- K cluster centers present (is_center = True)
- 100 participants present (is_center = False)

**Expected Behavior on Validation Failure:**
- Raise error with specific failure (e.g., "Expected 103 rows, found 100 - missing cluster centers")
- Log failure to logs/step06_prepare_plot_data.log
- Quit immediately (do NOT proceed to rq_plots)

---

## Summary

**Total Steps:** 6 (Step 0: Get Data + Steps 1-5 analysis + Step 6 plot data prep)

**Estimated Runtime:** 35-50 minutes
- Step 0: <5 min (data loading)
- Step 1: <1 min (standardization)
- Step 2: 15-25 min (model selection with gap statistic bootstrap)
- Step 3: 1-2 min (final K-means fit)
- Step 4: 10-20 min (100 bootstrap iterations)
- Step 5: 1-2 min (cluster characterization)
- Step 6: 1-2 min (plot data preparation)

**Cross-RQ Dependencies:** RQ 5.13 (random effects - REQUIRED), RQ 5.7 (theta scores + TSVR - OPTIONAL for plotting)

**Primary Outputs:**
- Cluster assignments: data/step03_cluster_assignments.csv (100 participants x cluster ID)
- Cluster centers: data/step05_cluster_centers_original.csv (K cluster centers x intercept/slope)
- Cluster summary: results/step05_cluster_summary.csv (K clusters x summary statistics + interpretive labels)
- Model selection metrics: results/step02_model_selection.csv (6 K values x BIC/silhouette/gap statistics)
- Bootstrap stability: results/step04_bootstrap_stability.csv (100 bootstrap iterations x Jaccard similarity)
- Scatter plot data: plots/step06_cluster_scatter_data.csv (100+K rows for visualization)

**Validation Coverage:** 100% (all 6 steps have validation requirements stated)

**Methodological Innovation:**
First clustering analysis in thesis with gold-standard 4-part validation:
1. BIC model selection (parsimony)
2. Silhouette constraint (cluster quality >=0.5)
3. Gap statistic (K=1 vs K>1 validation)
4. Bootstrap stability (Jaccard >=0.75)

**Scientific Outcomes:**
- If gap statistic selects K=1: "No latent forgetting profiles detected, continuous variation only" (valid result)
- If K>=2 with stable clusters: "K distinct latent forgetting profiles identified" (categorical individual differences)
- Spherical assumption validated post-hoc via scatter plot visual inspection

---

**Next Steps (Workflow):**
1. User reviews and approves this plan (Step 7 user gate)
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_*.py scripts

---

**Version History:**
- v1.0 (2025-11-26): Initial plan created by rq_planner agent for RQ 5.14 (first clustering RQ in thesis)
