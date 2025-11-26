# RQ 5.14: Latent Forgetting Profiles (K-means Clustering)

**Chapter:** 5
**RQ Number:** 14
**Full ID:** 5.14

---

## Research Question

**Primary Question:**
Can participants be grouped into latent classes based on their forgetting trajectories (intercepts and slopes)?

**Scope:**
This RQ uses K-means clustering to identify distinct forgetting profiles in the N=100 participant sample. Clustering is performed on random intercepts and random slopes extracted from RQ 5.13's mixed-effects model (Total domain analysis). Optimal number of clusters (K) is determined using BIC model selection, testing K=1 to K=6.

**Theoretical Framing:**
Individual differences in episodic memory may reflect categorical subgroups (e.g., "resilient" vs "vulnerable" memory) rather than continuous variation. Identifying latent forgetting profiles informs theoretical models of memory consolidation and could guide targeted interventions for memory-impaired populations.

---

## Theoretical Background

**Relevant Theories:**
- **Individual Differences Framework:** Memory ability and forgetting rates vary systematically across individuals. This variation may reflect discrete latent classes (categorical) or continuous dimensions (dimensional).
- **Dual-Process Theory:** High-performing participants may rely more on recollection (slower forgetting), while low-performing participants may rely on familiarity (faster forgetting).
- **Consolidation Theory:** Subgroups may differ in consolidation efficiency, producing different baseline abilities and forgetting rates.

**Key Citations:**
- Baddeley (2000): Working memory individual differences predict long-term episodic memory performance
- Eysenck (1979): Individual differences in memory reflect cognitive efficiency and strategy use
- Craik & Lockhart (1972): Depth of encoding predicts retention; individual differences in encoding depth may produce distinct profiles

**Theoretical Predictions:**
Clustering may reveal 2-3 profiles: (1) High baseline with slow forgetting (resilient memory), (2) Average baseline with average forgetting (typical memory), (3) Low baseline with fast forgetting (vulnerable memory). Alternative hypothesis: Continuous variation (K=1, no distinct profiles).

**Literature Gaps:**
Most episodic memory studies treat individual differences as continuous random variation. Few studies test for discrete latent classes in longitudinal forgetting trajectories using data-driven clustering. This RQ addresses whether forgetting profiles are categorical or continuous.

---

## Hypothesis

**Primary Hypothesis:**
Exploratory. We may identify 2-3 forgetting profiles based on intercept-slope joint distribution. Number of profiles determined by BIC model selection (balances fit vs complexity).

**Secondary Hypotheses:**
1. If profiles exist, they will show distinct intercept-slope combinations (e.g., high baseline paired with slow forgetting)
2. Cluster sizes will be reasonably balanced (no cluster <10% of sample)
3. BIC will identify optimal K between 2-4 (consistent with small-to-moderate number of profiles)

**Theoretical Rationale:**
Individual differences in episodic memory may reflect qualitatively different memory systems or strategies, producing discrete latent classes. High performers may use deeper encoding or more effective consolidation, yielding both higher baseline ability and slower forgetting. Low performers may show the opposite pattern. Continuous variation (K=1) would suggest dimensional rather than categorical differences.

**Expected Effect Pattern:**
K-means clustering will identify K=2 or K=3 as optimal (BIC minimum). Cluster centers will show distinct intercept-slope combinations. Visualization will show clear separation in 2D scatter plot (intercepts vs slopes) with minimal overlap between clusters.

---

## Memory Domains

**Domains Examined:**

- [x] **Total Domain** (All What/Where/When combined)
  - Tag Codes: `-N-`, `-L-/-U-/-D-`, `-O-` (all combined)
  - Description: Clustering performed on Total domain random effects from RQ 5.13 (single-factor model combining all episodic memory components)

- [ ] **What** (Object Identity)
  - Not used for clustering (uses Total domain only)

- [ ] **Where** (Spatial Location)
  - Not used for clustering (uses Total domain only)

- [ ] **When** (Temporal Order)
  - Not used for clustering (uses Total domain only)

**Inclusion Rationale:**
This RQ uses Total domain (all What/Where/When combined) because it represents overall episodic memory ability. Clustering on domain-specific random effects would require multivariate clustering (beyond scope). Total domain provides interpretable forgetting profiles (high/average/low performers) without domain decomposition.

**Exclusion Rationale:**
Domain-specific random effects (What/Where/When separately) are not used. RQ 5.13 analyzed domains separately but also fit a Total model. This RQ clusters on Total domain only for simplicity and interpretability.

---

## Analysis Approach

**Analysis Type:**
K-means clustering (unsupervised machine learning) for latent profile identification + BIC model selection

**High-Level Workflow:**

**Step 0:** Get Data - Load random effects from RQ 5.13 (Total_Intercept, Total_Slope per participant), theta scores from RQ 5.7 for trajectory plotting, TSVR mapping from RQ 5.7

**Step 1:** Load Random Effects from RQ 5.13 - Extract Total_Intercept and Total_Slope for each UID, compute descriptive statistics (mean, SD, range) for clustering variables

**Step 2:** Standardize Clustering Variables - Standardize intercepts and slopes to z-scores (mean=0, SD=1) to ensure both dimensions contribute equally to distance metric (different scales otherwise: intercepts ~0.5 range, slopes ~0.1 range)

**Step 3:** Determine Optimal Number of Clusters - Test K=1 to K=6 clusters using K-means, compute inertia (within-cluster sum of squares) and BIC for each K, generate elbow plot (inertia vs K) and BIC plot, select optimal K as BIC minimum (balances fit vs complexity)

**Step 4:** Fit Final K-means Model - Fit K-means with optimal K (random_state=42, n_init=50 for stability), extract cluster assignments for each participant, compute cluster centers (unstandardize to original scale for interpretation), report cluster sizes

**Step 5:** Characterize Clusters - Compute summary statistics (mean, SD, min, max) for intercepts and slopes per cluster, assign interpretive labels based on intercept (High/Average/Low baseline) and slope (Fast/Slow forgetting), example labels: "High Baseline, Slow Forgetting" vs "Low Baseline, Fast Forgetting"

**Step 6:** Visualize Clusters - Generate scatter plot (x-axis = Total_Intercept, y-axis = Total_Slope), color points by cluster membership, overlay cluster centers (large markers), include reference lines at x=0 and y=0, save cluster assignments for potential downstream analyses

**Data Preprocessing:**
- **Random Effects:** Use Total_Intercept and Total_Slope from RQ 5.13 (extracted from statsmodels MixedLM output)
- **Standardization:** Z-score transformation ensures intercepts and slopes contribute equally to Euclidean distance (K-means uses distance metric sensitive to scale)
- **No Missing Data:** All 100 participants have random effects (RQ 5.13 used all participants with ≥3 test sessions)

**Special Methods:**
- **BIC Model Selection:** BIC = n*log(RSS/n) + k*log(n), where RSS = inertia (within-cluster sum of squares), k = number of clusters, n = sample size. BIC penalizes complexity more heavily than AIC, preventing overfitting (important for small sample clustering).
- **K-means Initialization:** random_state=42 ensures replicability, n_init=50 runs K-means 50 times with different random initializations and selects best solution (prevents local minima).
- **Unstandardization:** Cluster centers reported in original scale (not z-scores) for interpretability.

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.13 and RQ 5.7 outputs)

### DERIVED Data Source:

**Source RQs:**
- **RQ 5.13:** Random effects (Total_Intercept, Total_Slope per participant) from `results/ch5/rq13/` (primary clustering input)
- **RQ 5.7:** Theta scores for trajectory plotting, TSVR mapping from `results/ch5/rq7/data/step00_tsvr_mapping.csv`

**File Paths:**
- `results/ch5/rq13/data/random_effects_total.csv` (assumed filename from RQ 5.13, columns: UID, Total_Intercept, Total_Slope)
- `results/ch5/rq7/data/theta_scores.csv` (for trajectory plotting, optional for visualization)
- `results/ch5/rq7/data/step00_tsvr_mapping.csv` (UID-Test-TSVR mapping)

**Dependencies:**
- RQ 5.13 must complete successfully (random effects extraction from mixed-effects model)
- RQ 5.7 must complete Step 0 (TSVR mapping) and theta extraction (if trajectory plotting needed)

**Usage:**
This RQ uses random intercepts and slopes from RQ 5.13's Total domain model as clustering variables. K-means identifies latent profiles based on joint distribution of baseline ability (intercept) and forgetting rate (slope).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.13 (inherited inclusion criteria: ≥3 test sessions, valid random effects)
- Expected N=100 (full sample, minimal exclusions)

**Items:**
- N/A (clustering uses participant-level random effects, not item-level data)

**Tests:**
- N/A (random effects already aggregate across all 4 tests)

**Clustering Variables:**
- [x] Total_Intercept (baseline ability at TSVR=0)
- [x] Total_Slope (forgetting rate, change in ability per unit time)

---
