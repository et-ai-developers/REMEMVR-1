# RQ 5.3.8: Paradigm-Based Clustering

**Chapter:** 5
**Type:** Paradigms
**Subtype:** Paradigm-Based Clustering
**Full ID:** 5.3.8

---

## Research Question

**Primary Question:**
Can participants be grouped into latent classes based on paradigm-specific forgetting trajectories (intercepts and slopes for Free Recall, Cued Recall, and Recognition)?

**Scope:**
This RQ examines individual differences in forgetting across three retrieval paradigms using random effects from RQ 5.3.7. Sample: N=100 participants. Clustering variables: 6 features (intercept + slope for each of Free Recall, Cued Recall, Recognition). K-means clustering with K=1 to K=6 tested. BIC used for model selection to identify optimal number of latent classes.

**Theoretical Framing:**
Exploratory analysis to identify latent profiles of participants based on paradigm-specific forgetting patterns. Profiles may reveal paradigm-selective impairment (e.g., poor Free Recall but intact Recognition) or generalized memory profiles. Complements variance decomposition (RQ 5.3.7) by identifying discrete participant clusters rather than continuous variance.

---

## Theoretical Background

**Relevant Theories:**
- **Individual Differences Framework:** Forgetting rates show stable between-person variance (ICC > 0.40 expected from RQ 5.3.7), suggesting trait-like individual differences. Clustering may identify discrete memory phenotypes.
- **Retrieval Support Gradient:** Free Recall (self-initiated retrieval) is most demanding, followed by Cued Recall, with Recognition (familiarity-based) being least demanding. Participants may differ in their reliance on retrieval support.
- **Dual-Process Theory (Yonelinas, 2002):** Recognition can rely on familiarity (fast, automatic), while Free Recall requires recollection (slow, effortful). Clustering may identify participants who differ in balance of familiarity vs recollection processes.

**Key Citations:**
[To be added by rq_scholar - literature on individual differences in episodic memory, memory profiles, clustering methodologies]

**Theoretical Predictions:**
Exploratory analysis with no directional prediction. Expected 2-4 latent profiles based on paradigm-specific intercepts and slopes. Possible profiles:
1. High performers across all paradigms (generalized advantage)
2. Low performers across all paradigms (generalized impairment)
3. Paradigm-selective profiles (e.g., poor Free Recall but intact Recognition, suggesting recollection deficit with preserved familiarity)

**Literature Gaps:**
[To be identified by rq_scholar - prior work on clustering episodic memory trajectories by paradigm, individual differences in retrieval support utilization]

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis. Expected 2-4 latent profiles based on 6 clustering variables (intercept + slope for Free Recall, Cued Recall, Recognition). Number of profiles determined by BIC model selection. No directional prediction regarding profile characteristics.

**Secondary Hypotheses:**
Profiles may show paradigm-selective patterns:
- Profile A: Poor Free Recall only (recollection-specific deficit)
- Profile B: Poor Recognition only (familiarity-specific deficit)
- Profile C: Generalized high performance (intact episodic memory)
- Profile D: Generalized low performance (global episodic impairment)

**Theoretical Rationale:**
If forgetting rates show substantial between-person variance within each paradigm (RQ 5.3.7 ICC > 0.40), but variance patterns differ across paradigms, clustering may identify discrete participant groups. Paradigm-selective profiles would support dual-process theory (dissociable familiarity vs recollection systems). Generalized profiles would suggest common episodic memory factor across paradigms.

**Expected Effect Pattern:**
BIC minimum identifies optimal K (expected K=2-4). Cluster sizes balanced (no cluster < 10% of sample). Cluster centers interpretable based on paradigm-specific intercepts and slopes. Scatter plot matrix shows clear separation between clusters on paradigm dimensions.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT directly examined in clustering (aggregated into paradigm theta scores)

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Disambiguation: NOT directly examined in clustering (aggregated into paradigm theta scores)

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT directly examined in clustering (aggregated into paradigm theta scores)

**Paradigms Examined:**

- [x] **Free Recall (IFR)** - Self-initiated retrieval
- [x] **Cued Recall (ICR)** - Cue-supported retrieval
- [x] **Recognition (IRE)** - Familiarity-based retrieval

**Inclusion Rationale:**
Clustering focuses on paradigm-specific random effects (intercepts and slopes) from RQ 5.3.7, which already aggregated What/Where/When domains into paradigm-level theta scores. The 6 clustering variables are paradigm-specific, not domain-specific.

**Exclusion Rationale:**
Room Free Recall (RFR), Room Cued Recall (TCR), and Room Recognition (RRE) excluded (non-interactive paradigms). Domain distinctions (What/Where/When) are not clustering features in this RQ (see RQ 5.2.7 for domain-based clustering).

---

## Analysis Approach

**Analysis Type:**
K-means clustering on paradigm-specific random effects (unsupervised machine learning)

**High-Level Workflow:**

**Step 1:** Load random effects from RQ 5.3.7 (6 variables per participant: Total_Intercept_Free, Total_Slope_Free, Total_Intercept_Cued, Total_Slope_Cued, Total_Intercept_Recognition, Total_Slope_Recognition). Verify N=100 participants, no missing values.

**Step 2:** Standardize all 6 features to z-scores (mean=0, SD=1) to ensure equal weighting in clustering. Verify standardization correct.

**Step 3:** Test K=1 to K=6 using K-means clustering. For each K: compute inertia (within-cluster sum of squares) and BIC (Bayesian Information Criterion). Identify optimal K as BIC minimum.

**Step 4:** Fit final K-means model with optimal K. Use random_state=42 for replicability and n_init=50 for stability. Extract cluster assignments (100 participants) and cluster centers (K rows x 6 features).

**Step 5:** Characterize clusters by computing mean intercept and slope per paradigm for each cluster. Assign interpretive labels based on patterns (e.g., "High Free Recall performers", "Paradigm-selective impairment"). Compare cluster sizes to ensure balance (no cluster < 10%).

**Step 6:** Create scatter plot matrix (6x6 grid showing all pairwise feature combinations) colored by cluster assignment. Mark cluster centers with reference lines. Verify clear separation between clusters.

**Expected Outputs:**
- data/step00_random_effects_from_rq537.csv (100 rows x 7 cols: UID + 6 random effects)
- data/step01_standardized_features.csv (100 rows x 7 cols: UID + 6 z-scores)
- results/step02_cluster_selection.csv (K=1-6: inertia, BIC per K)
- results/step03_optimal_k.txt (selected K value with rationale)
- data/step04_cluster_assignments.csv (100 rows: UID, cluster label)
- results/step04_cluster_centers.csv (K rows x 6 cols: cluster centers)
- results/step05_cluster_characterization.txt (interpretive labels and profile descriptions)
- plots/step06_cluster_scatter_matrix.png (scatter plot matrix)

**Success Criteria:**
- Random effects loaded: 100 participants, 6 features, no NaN
- Standardization correct: mean ~ 0, SD ~ 1 for all 6 features
- BIC minimum identified at K in [2,6]
- Cluster sizes balanced: no cluster < 10% of sample
- Cluster centers interpretable: clear paradigm-specific patterns
- Plot shows clear separation: distinct clusters visible in scatter matrix
- Replicates with random_state=42

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.3.7 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.3.7 (Paradigm-Specific Variance Decomposition)

**File Paths:**
- results/ch5/5.3.7/data/step04_random_effects.csv (300 rows: 100 participants x 3 paradigms, with Total_Intercept and Total_Slope per paradigm)

**Dependencies:**
RQ 5.3.7 must complete Step 4 (extract individual random effects from paradigm-stratified LMMs) before this RQ can run. RQ 5.3.7 fits separate LMMs for Free Recall, Cued Recall, and Recognition, each with random intercepts and slopes by UID. This RQ clusters participants based on those 6 random effects.

**Data Structure:**
RQ 5.3.7 outputs 300 rows (100 participants x 3 paradigms) with columns: UID, paradigm, Total_Intercept, Total_Slope. This RQ reshapes to wide format: 100 rows x 6 features (Total_Intercept_Free, Total_Slope_Free, Total_Intercept_Cued, Total_Slope_Cued, Total_Intercept_Recognition, Total_Slope_Recognition).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.3.7 (inherited inclusion criteria from RQ 5.3.1)
- Expected N=100 (no exclusions unless RQ 5.3.7 excluded participants due to missing data)

**Items:**
- N/A (theta scores already aggregated at paradigm level by RQ 5.3.1 -> RQ 5.3.7)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - inherited from RQ 5.3.1 via RQ 5.3.7
- Random slopes from RQ 5.3.7 capture individual variation across all 4 test sessions

---
