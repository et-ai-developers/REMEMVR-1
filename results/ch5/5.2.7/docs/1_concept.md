# RQ 5.2.7: Domain-Based Clustering

**Chapter:** 5
**Type:** Domains
**Subtype:** Domain-Based Clustering
**Full ID:** 5.2.7

---

## Research Question

**Primary Question:**
Can participants be grouped into latent classes based on domain-specific forgetting trajectories (What/Where/When intercepts and slopes)?

**Scope:**
This RQ examines individual differences in forgetting patterns across three episodic memory domains (What, Where, When). Uses 6 clustering variables per participant: intercept and slope for each domain. Sample: N=100 participants. Clustering explores 2-6 potential latent classes using K-means algorithm with BIC model selection.

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
Profiles may emerge reflecting: (1) global high/average/low memory across all domains, (2) domain-selective impairment (poor spatial only, poor temporal only), (3) dissociations between What versus Where/When reflecting dual-process system differences. Number of profiles (2-4) determined empirically via BIC model selection.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis with no directional prediction. Expected 2-4 latent profiles based on 6 clustering variables (intercept + slope for What, Where, When domains). Profiles may show domain-selective impairment patterns (e.g., poor spatial memory only, preserved object memory).

**Secondary Hypotheses:**
None - exploratory clustering analysis.

**Theoretical Rationale:**
Individual differences in episodic memory may reflect differential reliance on or integrity of domain-specific neural systems (hippocampus for Where/When, perirhinal cortex for What). Clustering analysis can identify whether participants show global versus domain-selective forgetting patterns, informing theories of episodic memory architecture and individual differences.

**Expected Effect Pattern:**
Optimal cluster number (K) determined by BIC minimum across K=1 to K=6 models. All cluster sizes should be balanced (no cluster < 10% of sample). Cluster centers should show interpretable patterns in 6-dimensional space (intercept and slope for each domain). Cluster characterization should reveal meaningful domain-specific patterns.

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

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence memory
  - Clustering Variables: Total_Intercept_When, Total_Slope_When

**Inclusion Rationale:**
All three episodic memory domains (What, Where, When) are included to capture domain-specific individual differences in baseline memory (intercepts) and forgetting rates (slopes). The 6 clustering variables (2 per domain) provide a comprehensive profile of each participant's domain-specific forgetting trajectories.

**Exclusion Rationale:**
None - all three domains required for domain-based clustering.

---

## Analysis Approach

**Analysis Type:**
K-means clustering on domain-specific random effects (intercepts and slopes)

**High-Level Workflow:**

**Step 1:** Load random effects from RQ 5.2.6 (6 variables per UID: Total_Intercept_What/Where/When, Total_Slope_What/Where/When)

**Step 2:** Standardize all 6 variables to z-scores (mean=0, SD=1) to ensure equal weighting across domains and parameters

**Step 3:** Test K=1 to K=6 models using K-means clustering; compute inertia and BIC for each K; select optimal K as BIC minimum

**Step 4:** Fit final K-means model with optimal K (random_state=42, n_init=50 for stability); extract cluster assignments and cluster centers

**Step 5:** Characterize clusters by domain-specific patterns: compute mean intercept/slope per cluster for each domain; assign interpretive labels based on patterns (e.g., "High What, Low Where/When")

**Step 6:** Create scatter plot matrix colored by cluster membership with cluster centers marked and reference lines

**Expected Outputs:**
- data/step00_random_effects_from_rq526.csv (100 rows, 6 clustering variables)
- data/step01_standardized_features.csv (100 rows x 6 z-scored variables)
- results/step02_cluster_selection.csv (6 rows: K=1-6 with inertia and BIC)
- results/step03_optimal_k.txt (selected K value)
- data/step04_cluster_assignments.csv (100 rows: UID, cluster)
- results/step04_cluster_centers.csv (K rows x 6 variables)
- results/step05_cluster_characterization.txt (interpretive cluster descriptions)
- plots/step06_cluster_scatter_matrix.png (scatter plot matrix)

**Success Criteria:**
- Random effects loaded successfully (100 participants x 6 variables)
- Standardization correct (mean ~ 0, SD ~ 1 for all 6 variables)
- BIC minimum clearly identified across K=1-6 range
- All cluster sizes balanced (no cluster < 10% of sample)
- Cluster centers interpretable with domain-specific patterns
- Scatter plot shows clear separation between clusters
- Results replicate with random_state=42

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.2.6 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.2.6 (Domain-Specific Variance Decomposition)

**File Paths:**
- results/ch5/5.2.6/data/step04_random_effects.csv (300 rows: 100 UID x 3 domains, contains Total_Intercept and Total_Slope per domain)

**Dependencies:**
RQ 5.2.6 must complete Step 4 (extract individual random effects per domain) before this RQ can run. RQ 5.2.6 fits domain-stratified LMMs with random slopes, extracting intercept and slope estimates for each participant in each domain.

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
- [x] Total_Intercept_When (baseline When memory at Day 0)
- [x] Total_Slope_When (When forgetting rate)

---
