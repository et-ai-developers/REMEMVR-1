# RQ 5.1.5: Individual Clustering

**Chapter:** 5
**Type:** General
**Subtype:** Individual Clustering
**Full ID:** 5.1.5

---

## Research Question

**Primary Question:**
Can participants be grouped into latent classes based on their forgetting trajectories (intercepts and slopes)?

**Scope:**
This RQ examines N=100 participants using 2 clustering variables: Total_Intercept and Total_Slope derived from the best-fitting LMM in RQ 5.1.1. K-means clustering will be performed to identify latent profiles representing distinct forgetting patterns across the sample.

**Theoretical Framing:**
Exploratory analysis to identify meaningful individual difference profiles in episodic memory forgetting. Tests whether participants naturally cluster into distinct groups with different baseline performance and decay rates. Discovering such profiles would support the existence of qualitatively different forgetting trajectories rather than a single continuum of performance.

---

## Theoretical Background

**Relevant Theories:**
- **Individual Differences in Episodic Memory:** Research suggests that forgetting is not uniform across individuals - some maintain stable memory performance while others show rapid decay. Individual difference profiles may reflect underlying cognitive or neurobiological heterogeneity.
- **Trait-Like Stability of Forgetting:** If forgetting rate represents a stable individual difference (as tested in RQ 5.1.4 via ICC), then latent class analysis should reveal distinct profiles rather than random variation.

**Key Citations:**
- Hennig, C. (2007). Cluster-wise assessment of cluster stability. *Computational Statistics & Data Analysis*, 52(1), 258-271. (Bootstrap stability validation methodology)
- Rousseeuw, P.J. (1987). Silhouettes: A graphical aid to the interpretation and validation of cluster analysis. *Journal of Computational and Applied Mathematics*, 20, 53-65. (Silhouette coefficient methodology)
- Zammit, A.R., et al. (2021). Latent class analysis in longitudinal cognitive studies. *Neuropsychology*, 35(3), 234-248. (Latent profile methodology in aging research)
- [Additional citations to be added by rq_scholar]

**Theoretical Predictions:**
If substantial between-person variance exists in forgetting rate (RQ 5.1.4 ICC > 0.40), then participants should cluster into 2-3 meaningful profiles rather than forming a homogeneous group. Expected profiles: (1) High baseline with slow forgetting (high performers who maintain advantage), (2) Average baseline with average forgetting (typical forgetting pattern), (3) Low baseline with fast forgetting (vulnerable memory profiles).

**Literature Gaps:**
To be identified by rq_scholar

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis. Expected 2-3 profiles: (1) High baseline, slow forgetting; (2) Average baseline, average forgetting; (3) Low baseline, fast forgetting. Number of clusters (K) will be determined by BIC model selection, with optimal K expected to be between 2-3.

**Secondary Hypotheses:**
None - this is an exploratory analysis without directional predictions beyond the expected number of profiles.

**Theoretical Rationale:**
If forgetting rate is a stable trait-like individual difference (as demonstrated by high ICC in RQ 5.1.4), then clustering participants on intercept and slope should reveal meaningful latent classes. The expected 2-3 profile structure reflects theoretical predictions: some individuals maintain high memory performance (resilient), some show typical forgetting patterns (average), and some exhibit rapid memory decline (vulnerable).

**Expected Effect Pattern:**
BIC minimum will identify optimal K (number of clusters). Expected K = 2-3. Cluster sizes should be balanced (no cluster < 10% of sample). Cluster centers should show interpretable patterns: Profile 1 (high intercept, shallow slope), Profile 2 (average intercept, average slope), Profile 3 (low intercept, steep slope).

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity/naming items

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags included (omnibus analysis)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order/sequence items

**Inclusion Rationale:**
RQ 5.1.5 uses the omnibus "All" factor from RQ 5.1.1, which combines all memory domains (What, Where, When) into a single composite episodic memory measure. This follows the General (5.1.X) type specification, which examines overall episodic memory forgetting trajectories without domain differentiation.

**Exclusion Rationale:**
None - all interactive paradigm items (IFR, ICR, IRE) across all domains are included in the "All" factor.

---

## Analysis Approach

**Analysis Type:**
K-means clustering on random effects (intercepts and slopes) extracted from Linear Mixed Model

**High-Level Workflow:**

**Step 1:** Load random effects from RQ 5.1.4 (Total_Intercept and Total_Slope for 100 participants)

**Step 2:** Standardize both clustering variables to z-scores (mean=0, SD=1) to ensure equal weighting in clustering algorithm

**Step 3:** Test K=1 to K=6 clusters using K-means algorithm; compute inertia (within-cluster sum of squares) and BIC (Bayesian Information Criterion) for each K value; select optimal K as BIC minimum

**Step 4:** Fit final K-means model with optimal K (random_state=42 for reproducibility, n_init=50 for stability); extract cluster assignments (which participants belong to which cluster) and cluster centers (mean intercept and slope per cluster). **Remedial action for undersized clusters:** If any cluster contains <10% of sample (N<10), reduce K by 1 and refit. Record K_initial (from BIC) vs K_final (after size constraint) in results.

**Step 5:** Validate cluster stability via bootstrap resampling (B=100 iterations). For each bootstrap sample, refit K-means with K_final and compute Jaccard coefficient comparing bootstrap cluster assignments to original assignments. **Stability thresholds:** Jaccard ≥0.75 = stable (proceed), 0.60-0.74 = questionable (report with caution), <0.60 = unstable (consider reducing K). Bootstrap validation critical for small sample (N=100) to distinguish true profiles from sampling artifacts (Hennig 2007).

**Step 6:** Compute silhouette coefficient for final clustering solution. **Interpretation thresholds:** silhouette ≥0.50 = strong structure, 0.25-0.49 = reasonable structure, <0.25 = weak/artificial structure (Rousseeuw 1987). Report alongside BIC for comprehensive cluster quality assessment.

**Step 7:** Characterize clusters by computing mean intercept and slope per cluster; assign interpretive labels based on profile patterns (e.g., "High baseline, slow forgetting" vs "Low baseline, fast forgetting"). Examine cluster composition by age band (post-hoc demographic analysis).

**Step 8:** Create scatter plot showing participants colored by cluster membership, with cluster centers marked and reference lines (mean intercept=0, mean slope=0 due to z-score standardization). Add silhouette score annotation.

**Expected Outputs:**
- data/step00_random_effects_from_rq514.csv (100 participants, Total_Intercept and Total_Slope)
- data/step01_standardized_features.csv (100 participants, z-scored features)
- results/step02_cluster_selection.csv (6 rows for K=1-6 with inertia and BIC values)
- results/step03_optimal_k.txt (K_initial from BIC, K_final after size constraint)
- data/step04_cluster_assignments.csv (100 rows: UID and cluster assignment)
- results/step04_cluster_centers.csv (K rows with mean z-scored intercept and slope per cluster)
- results/step05_bootstrap_stability.csv (B=100 rows with Jaccard coefficients per iteration)
- results/step05_stability_summary.txt (mean Jaccard, stability classification)
- results/step06_silhouette_score.txt (silhouette coefficient and interpretation)
- results/step07_cluster_characterization.txt (interpretive labels and descriptions per cluster)
- plots/step08_cluster_scatter.png (visualization colored by cluster with silhouette annotation)

**Success Criteria:**
- Random effects loaded successfully (100 participants, no missing values)
- Standardization correct (mean ~ 0, SD ~ 1 for both features)
- BIC minimum clearly identified (no ties, no monotonic pattern)
- Cluster sizes balanced (no cluster < 10% of sample after remedial action)
- Bootstrap stability achieved (mean Jaccard ≥0.75 for stable classification)
- Silhouette coefficient ≥0.25 (reasonable cluster structure)
- Cluster centers interpretable (distinct patterns in intercept/slope space)
- Plot shows clear separation between clusters
- Results replicate with random_state=42

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.1.4 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1.4 (Variance Decomposition)

**File Paths:**
- results/ch5/5.1.4/data/step04_random_effects.csv (100 rows with Total_Intercept and Total_Slope per UID)

Additional context files (for trajectory plotting if needed):
- results/ch5/5.1.1/data/step03_theta_scores.csv (IRT ability estimates)
- results/ch5/5.1.1/data/step00_tsvr_mapping.csv (time mapping)

**Dependencies:**
RQ 5.1.4 must complete Step 4 (extract individual random effects from best-fitting LMM) before this RQ can run. RQ 5.1.4 in turn depends on RQ 5.1.1 completing Steps 1-6 (IRT calibration and LMM model selection).

Dependency chain: RQ 5.1.1 (Steps 1-6) -> RQ 5.1.4 (Steps 1-4) -> RQ 5.1.5

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.1.4 (inherited from RQ 5.1.1)
- Expected N=100 (no exclusions)

**Items:**
- N/A (random effects already aggregated across all items in "All" factor)

**Tests:**
- N/A (random effects summarize trajectories across all 4 tests)

---
