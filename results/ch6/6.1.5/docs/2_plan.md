# Analysis Plan: RQ 6.1.5 - Trajectory Clustering

**Research Question:** 6.1.5
**Created:** 2025-12-06
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

This RQ performs K-means clustering on random effects (intercept + slope) extracted from RQ 6.1.4's best-fitting LMM to identify confidence phenotypes. The analysis tests whether participants cluster into distinct confidence decline trajectories (e.g., Resilient vs Vulnerable), and whether these phenotypes align with Ch5 5.1.5 accuracy phenotypes (testing memory-metacognition integration vs dissociation hypothesis).

**Pipeline:** Clustering + Cross-Tabulation (K-means on 2 features from RQ 6.1.4, chi-square test with Ch5 5.1.5)

**Steps:** 8 total analysis steps

**Estimated Runtime:** Medium (clustering steps ~5-10 minutes each, cross-tabulation <1 minute)

**Key Decisions Applied:**
- None (clustering analysis does not use IRT/LMM/trajectory-specific decisions)
- Uses standardization best practices (z-score normalization for equalized feature weighting)
- Applies multiple validation metrics (silhouette, Davies-Bouldin, Jaccard stability)

---

## Analysis Plan

This RQ requires 8 steps:

### Step 1: Load Random Effects from RQ 6.1.4

**Dependencies:** RQ 6.1.4 Step 4 must be complete (random effects extracted)
**Complexity:** Low (data loading only)

**Input:**

**File:** results/ch6/6.1.4/data/step04_random_effects.csv
**Source:** RQ 6.1.4 (ICC decomposition, random effects extraction)
**Format:** CSV with columns:
  - `UID` (string, participant identifier, format: P### with leading zeros)
  - `intercept` (float, random intercept for baseline confidence at Day 0)
  - `slope` (float, random slope for rate of confidence decline over time)
**Expected Rows:** 100 (one row per participant)
**Expected Columns:** 3 (UID, intercept, slope)

**Processing:**

1. Read CSV from dependency path
2. Validate required columns present (UID, intercept, slope)
3. Validate 100 participants (no missing data)
4. Check for NaN values (must be zero - LMM estimates for all participants)

**Output:**

**File:** data/step01_random_effects_loaded.csv
**Format:** CSV, identical to input (pass-through for validation)
**Columns:** UID, intercept, slope
**Expected Rows:** 100

**Validation Requirement:**

Validation tools MUST be used after data loading tool execution. Specific validation tools will be determined by rq_tools based on data format requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step01_random_effects_loaded.csv exists
- Expected rows: 100 (all participants)
- Expected columns: 3 (UID, intercept, slope)
- Data types: UID (string), intercept (float), slope (float)

*Value Ranges:*
- intercept: scientifically reasonable range (typical LMM random effects: -2 to +2 SD units)
- slope: scientifically reasonable range (typical temporal effects: -0.5 to +0.5 SD units per unit time)
- No extreme outliers (>4 SD from mean suggests estimation error)

*Data Quality:*
- No NaN values tolerated (LMM estimates for all 100 participants required)
- Expected N: Exactly 100 rows
- No duplicate UIDs
- UID format matches P### pattern

*Log Validation:*
- Required pattern: "Loaded 100 random effects from RQ 6.1.4"
- Required pattern: "Validation PASS: All 100 participants present"
- Forbidden patterns: "ERROR", "NaN detected", "Missing participants"

**Expected Behavior on Validation Failure:**
- If file missing: QUIT with "DEPENDENCY ERROR: RQ 6.1.4 must complete Step 4 first"
- If N != 100: Raise error with "Expected 100 participants, found {N}"
- If NaN detected: Raise error with "NaN values in random effects (participant UIDs: {list})"
- Log failure to logs/step01_load_random_effects.log
- g_debug invoked to diagnose root cause

---

### Step 2: Standardize Features to Z-Scores

**Dependencies:** Step 1 (requires loaded random effects)
**Complexity:** Low (simple transformation)

**Input:**

**File:** data/step01_random_effects_loaded.csv
**Source:** Step 1 output
**Columns:** UID, intercept, slope

**Processing:**

1. Compute z-scores for intercept: (intercept - mean) / SD
2. Compute z-scores for slope: (slope - mean) / SD
3. Create new columns: intercept_z, slope_z
4. Retain original intercept, slope columns for interpretability
5. Rationale: Standardization equalizes weighting of intercept and slope dimensions in K-means distance metric (prevents larger-scale feature dominating clustering)

**Output:**

**File:** data/step02_standardized_features.csv
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `intercept` (float, original random intercept)
  - `slope` (float, original random slope)
  - `intercept_z` (float, z-score standardized intercept)
  - `slope_z` (float, z-score standardized slope)
**Expected Rows:** 100
**Expected Columns:** 5

**Validation Requirement:**

Validation tools MUST be used after standardization tool execution. Specific validation tools will be determined by rq_tools based on standardization validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step02_standardized_features.csv exists
- Expected rows: 100
- Expected columns: 5 (UID, intercept, slope, intercept_z, slope_z)
- Data types: UID (string), all others (float)

*Value Ranges:*
- intercept_z: approximately -3 to +3 (z-score range, >3 = extreme outlier)
- slope_z: approximately -3 to +3 (z-score range)
- Original intercept and slope preserved (unchanged from Step 1)

*Data Quality:*
- No NaN values in z-score columns
- intercept_z mean approximately 0 (tolerance: |mean| < 0.01)
- intercept_z SD approximately 1 (tolerance: 0.95 < SD < 1.05)
- slope_z mean approximately 0 (tolerance: |mean| < 0.01)
- slope_z SD approximately 1 (tolerance: 0.95 < SD < 1.05)
- All 100 participants present

*Log Validation:*
- Required pattern: "Standardization complete: intercept_z (mean={X}, SD={Y}), slope_z (mean={X}, SD={Y})"
- Required pattern: "VALIDATION PASS: Z-score statistics within tolerance"
- Forbidden patterns: "ERROR", "NaN in z-scores", "Standardization failed"
- Acceptable warnings: "Outliers detected (N={X} participants >3 SD)" (outliers acceptable, not errors)

**Expected Behavior on Validation Failure:**
- If z-score mean/SD outside tolerance: Raise error with "Standardization validation failed: {details}"
- If NaN in z-scores: Raise error with "NaN values after standardization (check input for constant variance)"
- Log failure to logs/step02_standardize_features.log
- g_debug invoked

---

### Step 3: K-Means Clustering for K=1-6 with BIC Selection

**Dependencies:** Step 2 (requires standardized features)
**Complexity:** Medium (iterative clustering, ~5-10 minutes)

**Input:**

**File:** data/step02_standardized_features.csv
**Source:** Step 2 output
**Columns:** UID, intercept, slope, intercept_z, slope_z

**Processing:**

1. Extract clustering features: intercept_z, slope_z (2D feature space)
2. For K in range(1, 7):
   - Fit K-means model with K clusters (seed=42 for reproducibility)
   - Compute sum of squared errors (SSE)
   - Compute BIC: N * log(SSE/N) + K * log(N)
   - Record K, SSE, BIC
3. Select optimal K: argmin(BIC) across K=1-6
4. Flag optimal K in results table

**Output:**

**File 1:** data/step03_cluster_selection.csv
**Format:** CSV with columns:
  - `K` (int, number of clusters, range: 1-6)
  - `SSE` (float, sum of squared errors within clusters)
  - `BIC` (float, Bayesian Information Criterion)
  - `optimal` (bool, True for K with minimum BIC)
**Expected Rows:** 6 (one row per K candidate)
**Expected Columns:** 4

**File 2:** data/step03_bic_plot_data.csv
**Format:** CSV for BIC elbow plot (plots/ folder receives PNG from rq_plots later)
**Columns:** K, BIC
**Expected Rows:** 6

**Validation Requirement:**

Validation tools MUST be used after K-means selection tool execution. Specific validation tools will be determined by rq_tools based on clustering validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step03_cluster_selection.csv exists
- Expected rows: 6 (K=1 to K=6)
- Expected columns: 4 (K, SSE, BIC, optimal)
- Data types: K (int), SSE (float), BIC (float), optimal (bool)

*Value Ranges:*
- K in [1, 6] (all K values represented)
- SSE > 0 (strictly positive, decreases monotonically as K increases)
- BIC: scientifically reasonable (typically negative for standardized data)
- Exactly one K flagged as optimal (optimal column sums to 1)

*Data Quality:*
- No NaN values in any column
- SSE decreases monotonically: SSE(K=1) > SSE(K=2) > ... > SSE(K=6)
- BIC has clear minimum (not flat across all K - would indicate poor clustering structure)
- Optimal K in [2, 6] range (K=1 is trivial, should not be optimal)

*Log Validation:*
- Required pattern: "K-means clustering complete for K=1-6"
- Required pattern: "Optimal K selected: K={X} (BIC={Y})"
- Required pattern: "VALIDATION PASS: BIC minimum identified"
- Forbidden patterns: "ERROR", "Clustering failed", "No BIC minimum"
- Acceptable warnings: "BIC curve relatively flat (weak clustering structure)" (indicates result quality, not error)

**Expected Behavior on Validation Failure:**
- If BIC minimum is K=1: WARN user "No clustering structure detected (K=1 optimal)"
- If SSE not monotonic: Raise error "K-means SSE must decrease with K (numerical instability detected)"
- If multiple K flagged optimal: Raise error "Exactly one K must be optimal (BIC computation error)"
- Log failure to logs/step03_cluster_selection.log
- g_debug invoked

---

### Step 4: Fit Final K-Means Model with Optimal K

**Dependencies:** Step 3 (requires optimal K selection)
**Complexity:** Low (single K-means fit)

**Input:**

**File 1:** data/step02_standardized_features.csv
**Source:** Step 2 output (features for clustering)
**Columns:** UID, intercept, slope, intercept_z, slope_z

**File 2:** data/step03_cluster_selection.csv
**Source:** Step 3 output (optimal K identified)
**Columns:** K, SSE, BIC, optimal

**Processing:**

1. Read optimal K from step03_cluster_selection.csv (row where optimal=True)
2. Fit K-means model on (intercept_z, slope_z) with K=optimal_K, seed=42
3. Extract cluster assignments (0 to K-1) for each participant
4. Assign cluster labels to UID

**Output:**

**File:** data/step04_cluster_assignments.csv
**Format:** CSV with columns:
  - `UID` (string, participant identifier)
  - `cluster_label` (int, cluster assignment, range: 0 to K-1)
  - `intercept_z` (float, z-score features used for clustering)
  - `slope_z` (float, z-score features used for clustering)
**Expected Rows:** 100
**Expected Columns:** 4

**Validation Requirement:**

Validation tools MUST be used after final K-means fitting tool execution. Specific validation tools will be determined by rq_tools based on cluster assignment validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step04_cluster_assignments.csv exists
- Expected rows: 100 (all participants assigned)
- Expected columns: 4 (UID, cluster_label, intercept_z, slope_z)
- Data types: UID (string), cluster_label (int), intercept_z (float), slope_z (float)

*Value Ranges:*
- cluster_label in [0, K-1] where K = optimal K from Step 3
- All cluster IDs present (0, 1, ..., K-1 all represented)
- intercept_z and slope_z match Step 2 output (unchanged)

*Data Quality:*
- No NaN values in cluster_label
- All 100 participants assigned to exactly one cluster
- No duplicate UIDs
- Minimum cluster size >= 10% of N (no trivial clusters with <10 participants)

*Log Validation:*
- Required pattern: "Final K-means fit complete with K={optimal_K}"
- Required pattern: "Cluster sizes: {cluster 0: N0, cluster 1: N1, ...}"
- Required pattern: "VALIDATION PASS: All clusters >= 10% threshold"
- Forbidden patterns: "ERROR", "Empty cluster", "Unassigned participants"
- Acceptable warnings: "Cluster imbalance detected (largest/smallest ratio > 3:1)" (imbalance acceptable, not error)

**Expected Behavior on Validation Failure:**
- If cluster size < 10 participants: WARN user "Trivial cluster detected (cluster {X}: N={Y})"
- If empty cluster: Raise error "K-means produced empty cluster (K={K}, empty cluster ID={X})"
- If unassigned participants: Raise error "Not all participants assigned (missing UIDs: {list})"
- Log failure to logs/step04_fit_final_kmeans.log
- g_debug invoked

---

### Step 5: Validate Cluster Quality (Silhouette, Davies-Bouldin, Jaccard)

**Dependencies:** Step 4 (requires final cluster assignments)
**Complexity:** Medium (bootstrap stability testing ~5 minutes)

**Input:**

**File:** data/step04_cluster_assignments.csv
**Source:** Step 4 output
**Columns:** UID, cluster_label, intercept_z, slope_z

**Processing:**

1. Compute silhouette score (average across all participants, range: -1 to +1, >0.40 = acceptable quality)
2. Compute Davies-Bouldin index (lower is better, <1.0 = good separation)
3. Compute Jaccard bootstrap stability:
   - Bootstrap 1000 samples with replacement
   - Refit K-means on each bootstrap sample
   - Compute Jaccard coefficient (proportion of participant pairs with same cluster co-membership)
   - Report mean Jaccard, 95% CI, threshold check (>0.75 = stable)
4. Save all three metrics to results file

**Output:**

**File:** data/step05_validation_metrics.csv
**Format:** CSV with columns:
  - `metric` (string, metric name: "silhouette", "davies_bouldin", "jaccard_mean", "jaccard_ci_lower", "jaccard_ci_upper")
  - `value` (float, metric value)
  - `threshold` (float, acceptable threshold for this metric)
  - `pass` (bool, True if value meets threshold)
**Expected Rows:** 5 (one row per metric)
**Expected Columns:** 4

**Validation Requirement:**

Validation tools MUST be used after cluster quality validation tool execution. Specific validation tools will be determined by rq_tools based on clustering validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step05_validation_metrics.csv exists
- Expected rows: 5 (silhouette, Davies-Bouldin, Jaccard mean/CI_lower/CI_upper)
- Expected columns: 4 (metric, value, threshold, pass)
- Data types: metric (string), value (float), threshold (float), pass (bool)

*Value Ranges:*
- silhouette in [-1, 1] (typical range: 0.20-0.60 for real data)
- davies_bouldin > 0 (lower is better, typically 0.5-2.0)
- jaccard_mean in [0, 1] (bootstrap stability, typically 0.60-0.90)
- jaccard_ci_lower in [0, 1], jaccard_ci_upper in [0, 1]
- CI ordering: jaccard_ci_lower < jaccard_mean < jaccard_ci_upper

*Data Quality:*
- No NaN values in value column
- All 5 metrics present (silhouette, Davies-Bouldin, Jaccard metrics)
- pass column consistent with threshold logic (value vs threshold comparison)
- Bootstrap CI width reasonable (<0.20 suggests stable estimates)

*Log Validation:*
- Required pattern: "Silhouette score: {X} (threshold: 0.40, pass: {T/F})"
- Required pattern: "Davies-Bouldin index: {X} (threshold: 1.0, pass: {T/F})"
- Required pattern: "Jaccard stability: {X} (95% CI: [{L}, {U}], threshold: 0.75, pass: {T/F})"
- Required pattern: "VALIDATION PASS: Cluster quality metrics computed"
- Forbidden patterns: "ERROR", "Bootstrap failed", "NaN in metrics"
- Acceptable warnings: "Silhouette < 0.40 (weak clustering structure)" or "Jaccard < 0.75 (unstable clusters)" (indicates result quality, not error)

**Expected Behavior on Validation Failure:**
- If silhouette < 0.40: WARN user "Weak clustering structure (silhouette={X})"
- If Jaccard < 0.75: WARN user "Unstable clusters (Jaccard={X}, bootstrap instability)"
- If Davies-Bouldin > 2.0: WARN user "Poor cluster separation (Davies-Bouldin={X})"
- Log warnings to logs/step05_validate_cluster_quality.log
- Warnings do NOT trigger g_debug (acceptable result quality, not errors)

---

### Step 6: Characterize Clusters (Mean Intercept and Slope per Cluster)

**Dependencies:** Step 4 (requires cluster assignments)
**Complexity:** Low (descriptive statistics)

**Input:**

**File:** data/step04_cluster_assignments.csv
**Source:** Step 4 output
**Columns:** UID, cluster_label, intercept_z, slope_z

**Processing:**

1. Merge with data/step01_random_effects_loaded.csv to get original intercept, slope (not z-scores)
2. Group by cluster_label
3. Compute mean intercept, mean slope, SD intercept, SD slope, N per cluster
4. Interpret phenotypes based on intercept/slope combinations:
   - High intercept + shallow slope = Resilient (high baseline, slow decline)
   - Low intercept + steep slope = Vulnerable (low baseline, fast decline)
   - Other patterns = Mixed phenotypes
5. Document interpretations in text report

**Output:**

**File 1:** data/step06_cluster_characterization.csv
**Format:** CSV with columns:
  - `cluster_label` (int, cluster ID: 0 to K-1)
  - `N` (int, number of participants in cluster)
  - `mean_intercept` (float, mean random intercept in original scale)
  - `sd_intercept` (float, SD of random intercept)
  - `mean_slope` (float, mean random slope in original scale)
  - `sd_slope` (float, SD of random slope)
  - `phenotype` (string, interpreted phenotype: "Resilient", "Vulnerable", "Mixed", etc.)
**Expected Rows:** K (optimal number of clusters from Step 3)
**Expected Columns:** 7

**File 2:** data/step06_phenotype_descriptions.txt
**Format:** Text report with cluster interpretations
**Content:** One paragraph per cluster describing intercept/slope pattern and phenotype label

**Validation Requirement:**

Validation tools MUST be used after cluster characterization tool execution. Specific validation tools will be determined by rq_tools based on summary statistics validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step06_cluster_characterization.csv exists
- Expected rows: K (optimal number of clusters)
- Expected columns: 7 (cluster_label, N, mean_intercept, sd_intercept, mean_slope, sd_slope, phenotype)
- Data types: cluster_label (int), N (int), means (float), SDs (float), phenotype (string)
- data/step06_phenotype_descriptions.txt exists

*Value Ranges:*
- N sums to 100 (all participants accounted for)
- mean_intercept: scientifically reasonable (typical LMM random effects range)
- mean_slope: scientifically reasonable (negative for decline, magnitude <1.0 typical)
- sd_intercept >= 0, sd_slope >= 0 (SD cannot be negative)
- All cluster_labels in [0, K-1] represented

*Data Quality:*
- No NaN values in numeric columns
- N >= 10 for all clusters (consistent with Step 4 validation)
- SD values reasonable (not 0 unless cluster N=1, which violates N >= 10 rule)
- phenotype labels assigned for all clusters (no empty strings)

*Log Validation:*
- Required pattern: "Cluster characterization complete: K={X} clusters"
- Required pattern: "Cluster {X}: N={Y}, mean_intercept={Z}, mean_slope={W}, phenotype={P}"
- Required pattern: "VALIDATION PASS: All clusters characterized"
- Forbidden patterns: "ERROR", "NaN in cluster statistics", "Missing phenotype label"

**Expected Behavior on Validation Failure:**
- If N sum != 100: Raise error "Cluster N mismatch (total={X}, expected=100)"
- If phenotype label missing: Raise error "Phenotype interpretation required for all clusters"
- Log failure to logs/step06_characterize_clusters.log
- g_debug invoked

---

### Step 7: Cross-Tabulate with Ch5 5.1.5 Accuracy Clusters

**Dependencies:** Step 4 (confidence clusters) + Ch5 5.1.5 Step 4 (accuracy clusters)
**Complexity:** Low (simple cross-tabulation)

**Input:**

**File 1:** data/step04_cluster_assignments.csv
**Source:** This RQ Step 4 (confidence cluster labels)
**Columns:** UID, cluster_label (confidence), intercept_z, slope_z

**File 2:** results/ch5/5.1.5/data/step04_cluster_assignments.csv
**Source:** Ch5 5.1.5 Step 4 (accuracy cluster labels from accuracy phenotype clustering)
**Columns:** UID, cluster_label (accuracy)

**Processing:**

1. Read confidence cluster labels (this RQ)
2. Read accuracy cluster labels (Ch5 5.1.5)
3. Merge on UID (inner join, expect 100 matches)
4. Rename columns to avoid collision: cluster_label_confidence, cluster_label_accuracy
5. Create K_confidence x K_accuracy contingency table (cross-tabulation)
6. Compute row percentages (what % of each confidence cluster maps to each accuracy cluster)
7. Compute column percentages (what % of each accuracy cluster maps to each confidence cluster)

**Output:**

**File 1:** data/step07_crosstab_confidence_accuracy.csv
**Format:** CSV contingency table (K_confidence rows x K_accuracy columns)
**Rows:** Confidence cluster labels (0 to K_confidence-1)
**Columns:** Accuracy cluster labels (0 to K_accuracy-1)
**Values:** Count of participants in each confidence x accuracy combination

**File 2:** data/step07_crosstab_row_percentages.csv
**Format:** CSV with row percentages (each row sums to 100%)
**Interpretation:** For each confidence phenotype, what % fall into each accuracy phenotype

**File 3:** data/step07_crosstab_column_percentages.csv
**Format:** CSV with column percentages (each column sums to 100%)
**Interpretation:** For each accuracy phenotype, what % fall into each confidence phenotype

**Validation Requirement:**

Validation tools MUST be used after cross-tabulation tool execution. Specific validation tools will be determined by rq_tools based on crosstab validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step07_crosstab_confidence_accuracy.csv exists
- data/step07_crosstab_row_percentages.csv exists
- data/step07_crosstab_column_percentages.csv exists
- All three files have dimensions: K_confidence rows x K_accuracy columns

*Value Ranges:*
- Count table: all values >= 0 (non-negative counts)
- Count table: sum of all cells = 100 (all participants accounted for)
- Row percentages: each row sums to 100% (tolerance: 99.9-100.1 due to rounding)
- Column percentages: each column sums to 100% (tolerance: 99.9-100.1)

*Data Quality:*
- No NaN values in count table
- All 100 participants matched between RQ 6.1.5 and Ch5 5.1.5 (no missing UIDs)
- Crosstab dimensions match optimal K from each RQ (K_confidence from Step 3, K_accuracy from Ch5 5.1.5)

*Log Validation:*
- Required pattern: "Cross-tabulation complete: {K_confidence} confidence clusters x {K_accuracy} accuracy clusters"
- Required pattern: "All 100 participants matched between RQ 6.1.5 and Ch5 5.1.5"
- Required pattern: "VALIDATION PASS: Crosstab sums to 100 participants"
- Forbidden patterns: "ERROR", "UID mismatch", "Missing participants in merge"

**Expected Behavior on Validation Failure:**
- If merge produces <100 rows: QUIT with "DEPENDENCY ERROR: Ch5 5.1.5 must complete Step 4 first (only {N} UIDs matched)"
- If crosstab sum != 100: Raise error "Crosstab count mismatch (total={X}, expected=100)"
- If row/column percentages don't sum to 100%: Raise error "Percentage computation error (row {X} sums to {Y}%)"
- Log failure to logs/step07_crosstab_clusters.log
- g_debug invoked

---

### Step 8: Chi-Square Test of Association (Integration vs Dissociation Hypothesis)

**Dependencies:** Step 7 (requires crosstab)
**Complexity:** Low (single hypothesis test)

**Input:**

**File:** data/step07_crosstab_confidence_accuracy.csv
**Source:** Step 7 output (K_confidence x K_accuracy contingency table)

**Processing:**

1. Perform chi-square test of independence on contingency table
2. Compute chi-square statistic, degrees of freedom, p-value
3. Compute effect size (Cramer's V for nominal association)
4. Interpret result:
   - p < 0.05: INTEGRATED (confidence and accuracy phenotypes associated - metacognition tracks memory state)
   - p >= 0.05: DISSOCIATED (confidence and accuracy phenotypes independent - dissociable systems)
5. Document interpretation in text report

**Output:**

**File 1:** data/step08_chi_square_test.csv
**Format:** CSV with columns:
  - `statistic` (string, test statistic name: "chi_square", "df", "p_value", "cramers_v")
  - `value` (float, statistic value)
  - `interpretation` (string, "integrated" or "dissociated")
**Expected Rows:** 4 (one row per statistic)
**Expected Columns:** 3

**File 2:** data/step08_association_interpretation.txt
**Format:** Text report with hypothesis test interpretation
**Content:** Paragraph describing integration vs dissociation finding with statistical details

**Validation Requirement:**

Validation tools MUST be used after chi-square test tool execution. Specific validation tools will be determined by rq_tools based on hypothesis test validation requirements.

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- data/step08_chi_square_test.csv exists
- Expected rows: 4 (chi_square, df, p_value, cramers_v)
- Expected columns: 3 (statistic, value, interpretation)
- Data types: statistic (string), value (float), interpretation (string)
- data/step08_association_interpretation.txt exists

*Value Ranges:*
- chi_square >= 0 (test statistic non-negative)
- df > 0 (degrees of freedom: (K_confidence-1) x (K_accuracy-1))
- p_value in [0, 1] (probability value)
- cramers_v in [0, 1] (effect size bounded)

*Data Quality:*
- No NaN values in value column
- All 4 statistics present (chi_square, df, p_value, cramers_v)
- interpretation column values in {"integrated", "dissociated"} (no other values)
- interpretation consistent with p-value (p < 0.05 -> "integrated", p >= 0.05 -> "dissociated")

*Log Validation:*
- Required pattern: "Chi-square test complete: chi2={X}, df={Y}, p={Z}"
- Required pattern: "Effect size (Cramer's V): {V}"
- Required pattern: "Interpretation: {integrated/dissociated} (p {< / >=} 0.05)"
- Required pattern: "VALIDATION PASS: Association test complete"
- Forbidden patterns: "ERROR", "NaN in test statistics", "Invalid p-value"

**Expected Behavior on Validation Failure:**
- If p_value outside [0, 1]: Raise error "Invalid p-value (p={X}, must be in [0, 1])"
- If cramers_v outside [0, 1]: Raise error "Invalid Cramer's V (V={X}, must be in [0, 1])"
- If interpretation missing or invalid: Raise error "Interpretation must be 'integrated' or 'dissociated'"
- Log failure to logs/step08_chi_square_test.log
- g_debug invoked

---

## Expected Data Formats

### Step-to-Step Transformations

**Step 1 -> Step 2:** Pass-through validation (random effects loaded, no transformation)

**Step 2 -> Step 3:** Standardization adds z-score columns (intercept_z, slope_z) for equalized feature weighting in K-means distance metric

**Step 3 -> Step 4:** BIC selection identifies optimal K, final K-means fit assigns cluster labels

**Step 4 -> Step 5:** Cluster assignments validated via silhouette, Davies-Bouldin, Jaccard bootstrap stability

**Step 4 -> Step 6:** Cluster assignments merged with original random effects for phenotype interpretation (mean intercept/slope per cluster)

**Step 4 + Ch5 5.1.5 -> Step 7:** Cross-tabulation merges confidence clusters (this RQ) with accuracy clusters (Ch5 5.1.5) on UID

**Step 7 -> Step 8:** Contingency table tested for association via chi-square (integration vs dissociation hypothesis)

### Column Naming Conventions

**From names.md:**
- `UID` - Participant unique identifier (format: P### with leading zeros)
- `intercept` - Random intercept (original scale, not z-score)
- `slope` - Random slope (original scale, not z-score)
- `intercept_z` - Z-score standardized intercept
- `slope_z` - Z-score standardized slope
- `cluster_label` - Cluster assignment (0 to K-1)

**New conventions introduced (to be added to names.md):**
- `cluster_label_confidence` - Confidence cluster assignment (this RQ 6.1.5)
- `cluster_label_accuracy` - Accuracy cluster assignment (Ch5 5.1.5)
- `phenotype` - Interpreted cluster phenotype (e.g., "Resilient", "Vulnerable")

### Data Type Constraints

**UID:** string, format P### (e.g., P001, P042, P100)
**intercept, slope:** float, unrestricted range (LMM random effects)
**intercept_z, slope_z:** float, approximately -3 to +3 (z-scores)
**cluster_label:** int, 0 to K-1 (consecutive cluster IDs)
**K, N, df:** int, positive integers
**BIC, SSE, silhouette, davies_bouldin, jaccard, chi_square, p_value, cramers_v:** float

---

## Cross-RQ Dependencies

**This RQ requires outputs from:**

1. **RQ 6.1.4 (ICC Decomposition)** - Provides random effects for confidence clustering
   - File: results/ch6/6.1.4/data/step04_random_effects.csv
   - Used in: Step 1 (load random effects: intercept, slope)
   - Rationale: RQ 6.1.4 extracts random effects from best-fitting LMM (RQ 6.1.1). These random effects represent participant-level confidence trajectory phenotypes (baseline and decline rate).

2. **Ch5 5.1.5 (Accuracy Clustering)** - Provides accuracy cluster labels for cross-tabulation
   - File: results/ch5/5.1.5/data/step04_cluster_assignments.csv
   - Used in: Step 7 (cross-tabulate confidence clusters with accuracy clusters)
   - Rationale: Ch5 5.1.5 identifies accuracy phenotypes (Resilient vs Vulnerable memory trajectories). This RQ tests whether confidence phenotypes align with accuracy phenotypes (integration hypothesis) or diverge (dissociation hypothesis).

**Execution Order Constraint:**
1. RQ 6.1.4 must complete Step 4 (random effects extraction)
2. Ch5 5.1.5 must complete Step 4 (accuracy cluster assignments)
3. This RQ executes after both dependencies complete

**Data Source Boundaries:**
- **DERIVED data:** Both random effects (RQ 6.1.4) and accuracy clusters (Ch5 5.1.5) are analysis outputs, not raw master.xlsx data
- **Scope:** This RQ performs clustering on confidence trajectories (random effects), NOT re-estimating LMMs or re-calibrating IRT models

**Validation:**
- Step 1: Check results/ch6/6.1.4/data/step04_random_effects.csv exists (circuit breaker: DEPENDENCY ERROR if absent)
- Step 7: Check results/ch5/5.1.5/data/step04_cluster_assignments.csv exists (circuit breaker: DEPENDENCY ERROR if absent)
- If either file missing -> QUIT with error -> user must execute dependency RQs first

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

**Step 1: Load Random Effects**
- Validation: File exists, 100 rows, 3 columns (UID, intercept, slope), no NaN values, UID format P###

**Step 2: Standardize Features**
- Validation: Z-score mean approximately 0, SD approximately 1 (tolerance: |mean| < 0.01, 0.95 < SD < 1.05)

**Step 3: K-Means Clustering (K=1-6)**
- Validation: SSE decreases monotonically, BIC minimum identified (not K=1), optimal K in [2, 6]

**Step 4: Final K-Means Fit**
- Validation: All cluster IDs 0 to K-1 present, all 100 participants assigned, minimum cluster size >= 10

**Step 5: Cluster Quality Validation**
- Validation: Silhouette in [-1, 1], Davies-Bouldin > 0, Jaccard in [0, 1], CI ordering correct

**Step 6: Cluster Characterization**
- Validation: N sums to 100, SD >= 0, phenotype labels assigned for all clusters

**Step 7: Cross-Tabulation**
- Validation: Crosstab sum = 100, row percentages sum to 100%, column percentages sum to 100%

**Step 8: Chi-Square Test**
- Validation: p_value in [0, 1], cramers_v in [0, 1], interpretation in {"integrated", "dissociated"}

---

## Summary

**Total Steps:** 8 (all clustering and cross-tabulation)

**Estimated Runtime:** Medium (~15-20 minutes total: Steps 1-2 <1 min each, Step 3 ~5-10 min, Steps 4-8 <5 min total)

**Cross-RQ Dependencies:** 2 dependencies (RQ 6.1.4 random effects, Ch5 5.1.5 accuracy clusters)

**Primary Outputs:**
- Cluster assignments (data/step04_cluster_assignments.csv)
- Validation metrics (data/step05_validation_metrics.csv)
- Cluster characterization (data/step06_cluster_characterization.csv)
- Crosstab with accuracy clusters (data/step07_crosstab_confidence_accuracy.csv)
- Chi-square test (data/step08_chi_square_test.csv)
- Interpretation text reports (data/step06_phenotype_descriptions.txt, data/step08_association_interpretation.txt)

**Validation Coverage:** 100% (all 8 steps have validation requirements with 4-layer substance criteria)

**Key Research Questions Addressed:**
1. Do participants cluster into distinct confidence phenotypes? (Steps 1-5)
2. What are the confidence phenotype characteristics? (Step 6)
3. Do confidence and accuracy phenotypes align (integration) or diverge (dissociation)? (Steps 7-8)

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. Workflow continues to Step 11: rq_tools reads this plan -> creates 3_tools.yaml
3. Workflow continues to Step 12: rq_analysis reads this plan + 3_tools.yaml -> creates 4_analysis.yaml
4. Workflow continues to Step 14: g_code reads 4_analysis.yaml -> generates stepNN_name.py scripts

---

**Version History:**
- v1.0 (2025-12-06): Initial plan created by rq_planner agent for RQ 6.1.5
