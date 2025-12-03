# RQ 5.2.7: Domain-Based Clustering

**Chapter:** 5
**Type:** Domains
**Subtype:** Domain-Based Clustering
**Full ID:** 5.2.7

---

## ⚠️ WHEN DOMAIN EXCLUSION

**Exclusion Applied:** When domain (-O- tags) excluded from this analysis.

**Rationale:** RQ 5.2.1 discovered severe floor effect in When domain:
- 77% item attrition during IRT purification (23 → 5 items)
- 6-9% floor effect at baseline (participants at chance)
- Insufficient measurement precision for reliable trajectory estimation

**Impact on This RQ:**
- Clustering uses 4 variables (not 6): What intercept/slope, Where intercept/slope
- Source data: RQ 5.2.6 step04_random_effects.csv (200 rows: 100 UID × 2 domains)
- Expected row counts adjusted throughout

---

## Research Question

**Primary Question:**
Can participants be grouped into latent classes based on domain-specific forgetting trajectories (What/Where intercepts and slopes)?

**Scope:**
This RQ examines individual differences in forgetting patterns across two episodic memory domains (What, Where). When domain excluded due to floor effect (see above). Uses 4 clustering variables per participant: intercept and slope for each domain. Sample: N=100 participants. Clustering explores 2-6 potential latent classes using K-means algorithm with BIC model selection.

**Theoretical Framing:**
Exploratory analysis to identify whether participants exhibit domain-selective memory profiles (e.g., impaired spatial memory only, preserved object memory) versus global memory patterns. Addresses individual differences in domain-specific forgetting trajectories, potentially reflecting differential reliance on hippocampal vs perirhinal systems.

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory** (Yonelinas, 2002): Familiarity-based retrieval (What domain, perirhinal cortex) versus recollection-based retrieval (Where/When domains, hippocampal-dependent). Individual differences may show domain-selective impairments reflecting differential system integrity.
- **Consolidation Theory** (Dudai, 2004): Hippocampal-dependent memories (Where, When) consolidate more slowly and show greater individual variability compared to perirhinal-dependent memories (What). Latent classes may reflect differential consolidation efficiency.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Profiles may emerge reflecting: (1) global high/average/low memory across both domains, (2) domain-selective impairment (poor spatial only OR poor object memory only), (3) dissociations between What versus Where reflecting dual-process system differences (perirhinal vs hippocampal). Number of profiles (2-4) determined empirically via BIC model selection.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis with no directional prediction. Expected 2-4 latent profiles based on 4 clustering variables (intercept + slope for What, Where domains). Profiles may show domain-selective impairment patterns (e.g., poor spatial memory only, preserved object memory).

**Secondary Hypotheses:**
None - exploratory clustering analysis.

**Theoretical Rationale:**
Individual differences in episodic memory may reflect differential reliance on or integrity of domain-specific neural systems (hippocampus for Where, perirhinal cortex for What). Clustering analysis can identify whether participants show global versus domain-selective forgetting patterns, informing theories of episodic memory architecture and individual differences.

**Expected Effect Pattern:**
Optimal cluster number (K) determined by BIC minimum across K=1 to K=6 models. All cluster sizes should be balanced (no cluster < 10% of sample). Cluster centers should show interpretable patterns in 4-dimensional space (intercept and slope for each domain). Cluster characterization should reveal meaningful domain-specific patterns.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming memory
  - Clustering Variables: Total_Intercept_What, Total_Slope_What

- [x] **Where** (Spatial Location)
  - Tag Codes: `-L-`, `-U-`, `-D-`
  - Description: Spatial location memory (general, pick-up, put-down)
  - Disambiguation: All Where tags combined into single domain factor
  - Clustering Variables: Total_Intercept_Where, Total_Slope_Where

- [ ] **When** (Temporal Order) - **EXCLUDED**
  - Tag Code: `-O-`
  - Description: Temporal order / sequence memory
  - **EXCLUDED:** Floor effect discovered in RQ 5.2.1 (77% item attrition, 6-9% floor)

**Inclusion Rationale:**
Two episodic memory domains (What, Where) are included to capture domain-specific individual differences in baseline memory (intercepts) and forgetting rates (slopes). The 4 clustering variables (2 per domain) provide a profile of each participant's domain-specific forgetting trajectories.

**Exclusion Rationale:**
When domain excluded due to floor effect (RQ 5.2.1). Insufficient measurement precision prevents reliable random effect extraction.

---

## Analysis Approach

**Analysis Type:**
K-means clustering on domain-specific random effects (intercepts and slopes)

### Clustering Method Selection

**Method:** K-means clustering with BIC-based model selection (K=2-6)

**Justification for K-means over Latent Profile Analysis (LPA):**
1. **Exploratory nature:** This analysis aims to discover patterns in individual differences, not test specific model fit hypotheses. K-means is appropriate for pattern discovery.
2. **Interpretability:** K-means cluster centroids provide direct interpretability for clinical translation - each centroid represents a prototypical memory profile.
3. **Computational efficiency:** K-means enables rapid sensitivity analyses (bootstrap stability, outlier removal) that would be computationally prohibitive with LPA.
4. **Sample size considerations:** N=100 is at the lower bound for stable LPA estimation with 6 continuous indicators (Nylund et al., 2007 recommend N≥200 for LPA). K-means is more robust at smaller sample sizes.
5. **Continuous indicators:** All 6 clustering variables are continuous random effects, appropriate for K-means. LPA would be preferred if variables were categorical or mixed.

**Alternative Method Consideration:**
If K-means shows poor cluster quality metrics (silhouette < 0.25 or non-spherical clusters in scatter plots), Gaussian Mixture Models (GMM) will be tested as sensitivity analysis. GMM relaxes the spherical cluster assumption and provides probabilistic cluster membership.

**High-Level Workflow:**

**Step 1:** Load random effects from RQ 5.2.6 (4 variables per UID: Total_Intercept_What/Where, Total_Slope_What/Where)

**Step 2:** Standardize all 4 variables to z-scores (mean=0, SD=1) to ensure equal weighting across domains and parameters. Check for outliers (|z| > 3) and document any extreme values.

**Step 3:** Test K=1 to K=6 models using K-means clustering; compute inertia and BIC for each K; select optimal K as BIC minimum. If multiple K values have similar BIC (ΔBIC < 2), select the more parsimonious (smaller K) model.

**Step 4:** Fit final K-means model with optimal K (random_state=42, n_init=50 for stability); extract cluster assignments and cluster centers

**Step 4b: Cluster Validation**
- Compute silhouette score (target ≥ 0.40 for acceptable cohesion; ≥ 0.50 preferred)
- Compute Davies-Bouldin index (target < 1.5 for acceptable separation)
- Assess cluster stability via bootstrap resampling (100 iterations, 80% subsampling, Jaccard index > 0.75 for stable clusters)
- If stability < 0.75: Report clusters as "tentative" and interpret cautiously

**Step 5:** Characterize clusters by domain-specific patterns: compute mean intercept/slope per cluster for each domain; assign interpretive labels based on patterns (e.g., "High What, Low Where")

**Step 6:** Create scatter plot matrix colored by cluster membership with cluster centers marked and reference lines. Visually inspect for non-spherical cluster shapes that would indicate K-means assumption violation.

**Expected Outputs:**
- data/step00_random_effects_from_rq526.csv (100 rows, 4 clustering variables)
- data/step01_standardized_features.csv (100 rows x 4 z-scored variables)
- results/step02_cluster_selection.csv (6 rows: K=1-6 with inertia and BIC)
- results/step03_optimal_k.txt (selected K value with justification)
- data/step04_cluster_assignments.csv (100 rows: UID, cluster)
- results/step04_cluster_centers.csv (K rows x 4 variables)
- results/step04b_cluster_validation.csv (silhouette score, Davies-Bouldin index, bootstrap Jaccard)
- results/step05_cluster_characterization.txt (interpretive cluster descriptions)
- plots/step06_cluster_scatter_matrix.png (scatter plot matrix)

**Success Criteria:**
- Random effects loaded successfully (100 participants x 4 variables)
- Standardization correct (mean ~ 0, SD ~ 1 for all 4 variables)
- No extreme outliers (|z| > 4) or documented if present
- BIC minimum clearly identified across K=1-6 range (or parsimony rule applied if ΔBIC < 2)
- All cluster sizes balanced (no cluster < 10% of sample, i.e., N < 10)
- **Cluster quality validated:**
  - Silhouette score ≥ 0.40 (acceptable) or ≥ 0.50 (good)
  - Davies-Bouldin index < 1.5
  - Bootstrap Jaccard stability > 0.75
- Cluster centers interpretable with domain-specific patterns
- Scatter plot shows reasonable separation between clusters (visual confirmation of sphericity assumption)
- Results replicate with random_state=42

**If Cluster Quality Fails:**
- If silhouette < 0.25: Report "poor cluster structure" and consider alternative interpretation (continuous individual differences rather than discrete profiles)
- If bootstrap Jaccard < 0.60: Report clusters as "unstable - interpret with caution"
- If scatter plots show elongated/non-spherical clusters: Run GMM sensitivity analysis and compare cluster assignments

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.2.6 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.2.6 (Domain-Specific Variance Decomposition)

**File Paths:**
- results/ch5/5.2.6/data/step04_random_effects.csv (200 rows: 100 UID x 2 domains, contains Total_Intercept and Total_Slope per domain)

**Dependencies:**
RQ 5.2.6 must complete Step 4 (extract individual random effects per domain) before this RQ can run. RQ 5.2.6 fits domain-stratified LMMs with random slopes, extracting intercept and slope estimates for each participant in each domain (What, Where only - When excluded due to floor effect).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 5.2.6 (inherited inclusion criteria)
- No exclusions at clustering stage

**Items:**
- N/A (clustering uses participant-level random effects, not item-level data)

**Tests:**
- N/A (random effects aggregate across all 4 tests)

**Clustering Variables:**
- [x] Total_Intercept_What (baseline What memory at Day 0)
- [x] Total_Slope_What (What forgetting rate)
- [x] Total_Intercept_Where (baseline Where memory at Day 0)
- [x] Total_Slope_Where (Where forgetting rate)
- [ ] ~~Total_Intercept_When~~ (EXCLUDED - floor effect)
- [ ] ~~Total_Slope_When~~ (EXCLUDED - floor effect)

---
