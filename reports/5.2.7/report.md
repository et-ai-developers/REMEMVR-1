# RQ 5.2.7: Domain-Based Clustering

**Chapter:** Ch5
**Status:** Completed (Model-Averaged Rerun)
**Certification Date:** 2025-12-09 (Rerun with model-averaged random effects)
**Report Generated:** 2026-01-01

---

## 1. Executive Summary

**What we tested:** Whether participants can be grouped into latent classes based on domain-specific forgetting trajectories (What/Where intercepts and slopes).

**What we found:** K=4 stable but fuzzy clusters identified using model-averaged random effects (parsimony rule: K=4 and K=5 equivalent BIC, selected K=4). Cluster quality POOR (silhouette=0.352) but STABLE (Jaccard=0.871). Four prototypical profiles: (1) Average/Declining (36%), (2) Average/Improving (28%), (3) Low/Domain-Dissociated (17%), (4) High/Stable (19%). Notable: 47% show improving memory over 6 days.

**Why it matters:** Individual differences in domain-specific forgetting reveal heterogeneous consolidation capacity. Model averaging (PowerLaw dominance vs Log #10) produces more parsimonious clustering (K=4 vs original K=5), with improved interpretability but maintained fuzzy boundaries.

---

## 2. Research Question

**Question:**
Can participants be grouped into latent classes based on domain-specific forgetting trajectories (What/Where intercepts and slopes)?

**Hypothesis:**
Exploratory analysis with no directional prediction. Expected 2-4 latent profiles based on 4 clustering variables (intercept + slope for What, Where domains). Profiles may show domain-selective impairment patterns (e.g., poor spatial memory only, preserved object memory).

**Theoretical Framework:**
- **Dual-Process Theory** (Yonelinas, 2002): Familiarity-based retrieval (What domain, perirhinal cortex) versus recollection-based retrieval (Where domain, hippocampal-dependent)
- **Consolidation Theory** (Dudai, 2004): Individual differences in hippocampal/cortical consolidation efficiency

**Expected Patterns:**
2-4 latent profiles with interpretable domain-specific patterns: global high/low memory, domain-selective impairment, dual-process dissociations.

---

## 3. Historical Context

**Archive Search:**
- Topics searched: 2 relevant
- Entries found: 2 sessions
- Date range: 2025-12-03 to 2025-12-09

**Key Events (Chronological):**

1. **2025-12-03 22:50** - Original K=5 clustering execution (archive/rq_5.2.7_complete_domain_clustering.md)
   - K=5 selected via BIC minimum (BIC=90.09)
   - Silhouette=0.34 (POOR), Jaccard=0.88 (STABLE)
   - When domain excluded due to floor effect (77% item attrition)
   - 5 clusters: Average-Slow (22%), Average-Improving (26%), Low-Stable (17%), High-Stable (21%), High-Fast decline (14%)
   - Input: Log-only random effects from RQ 5.2.6 Step 04

2. **2025-12-09** - Model-averaged rerun (results/summary.md timestamp)
   - K=4 selected via parsimony rule (”BIC < 2 between K=4 and K=5)
   - Silhouette=0.352 (marginal improvement +0.012), Jaccard=0.871 (stable -0.009)
   - Input: RQ 5.2.6 Step 08 model-averaged random effects (17-model Akaike-weighted ensemble)
   - PowerLaw models dominate (top 5 positions, 60% weight), Log ranked #10 (3.4% weight)
   - More parsimonious structure: 4 clusters vs 5

**Blockers Resolved:**
- **rq_stats rejection (2025-12-02):** K-means vs LPA justification required (CRITICAL), cluster validation metrics needed (MODERATE)
  - Resolution: Justification added to concept.md (sample size N=100 at lower bound for LPA, K-means appropriate for exploratory), validation steps 4-6 added with silhouette/Davies-Bouldin/bootstrap Jaccard
- **When domain exclusion:** Floor effect from RQ 5.2.1 (77% item attrition, 6-9% floor) prevents 6-variable clustering
  - Resolution: Documented in concept.md and plan.md, clustering uses 4 variables (What/Where only)

**Cross-References:**
- Related to RQ 5.2.6: Domain-Specific Variance Decomposition (data source dependency)
- Related to RQ 5.1.5: General K-means Clustering (same methodology, K=2 for general factor)

---

## 4. Methodology

### Data Sources

**Root or Derived:**
- DERIVED: Uses outputs from RQ 5.2.6 Step 08 (model-averaged random effects)

**Specific Sources:**
- results/ch5/5.2.6/data/step08_model_averaged_random_effects.csv (200 rows: 100 UID × 2 domains)
- 17-model Akaike-weighted ensemble (PowerLaw_Alpha05 weight=15.2%, Log weight=3.4%)

### Analysis Pipeline

**Steps:**

| Step | Description | Output Files |
|------|-------------|--------------|
| **Step 0** | Load random effects from RQ 5.2.6 | step00_random_effects_from_rq526.csv (100×5) |
| **Step 1** | Standardize features to z-scores | step01_standardized_features.csv (100×5), step01_standardization_summary.txt |
| **Step 2** | K-means model selection (K=1-6, BIC) | step02_cluster_selection.csv (6 rows), step02_optimal_k_selection.txt |
| **Step 3** | Fit final K-means (K=4) | step03_cluster_assignments.csv (100 rows), step03_cluster_centers.csv (4 rows), step03_cluster_sizes.csv |
| **Step 4** | Validate cluster quality | step04_cluster_validation.csv (5 metrics), step04_validation_summary.txt |
| **Step 5** | Characterize clusters | step05_cluster_summary_statistics.csv (16 rows), step05_cluster_characterization.txt |
| **Step 6** | Prepare scatter plot data | step06_scatter_plot_matrix_data.csv (105 rows: 100 participants + 4 centroids) |

### Tools Used

**Key Tools:**
- sklearn.cluster.KMeans: K-means clustering (n_init=50, random_state=42)
- sklearn.metrics.silhouette_score: Cohesion/separation metric
- sklearn.metrics.davies_bouldin_score: Cluster separation index
- Bootstrap Jaccard: 100 iterations, 80% subsample stability analysis

### Critical Design Decisions

**Decisions:**
- **K-means over LPA:** Justified by exploratory nature, interpretability, computational efficiency, sample size (N=100 at lower bound for LPA) (source: concept.md)
- **Parsimony rule applied:** K=4 selected despite ”BIC=0.001 from K=5 (parsimony rule: select smaller K when ”BIC < 2) (source: step02_optimal_k_selection.txt)
- **Model-averaged input:** Uses RQ 5.2.6 Step 08 ensemble random effects (not single-model) to reduce overfitting (source: summary.md)
- **When domain excluded:** Floor effect prevents reliable random effect extraction (source: concept.md, plan.md)

**Warnings:**
- No PLATINUM certification files found (RQ completed before certification workflow implemented)
- Cluster quality POOR (silhouette=0.352 < 0.40 acceptable threshold)
- Interpret clusters as "prototypical profiles" not discrete categories (source: summary.md Section 4)

---

## 5. Results

### Sample Characteristics

**Sample Size:**
- Total N: 100 participants (inherited from RQ 5.2.6)
- Exclusions: None at clustering stage
- Missing data: None (all 100 participants had complete random effects)

**Final Sample:**
- N = 100 (100% retention from RQ 5.2.6)

### Primary Findings

**K-means Model Selection:**

| K | BIC | ”BIC | Status |
|---|-----|------|--------|
| 1 | 156.05 | +64.19 | - |
| 2 | 122.99 | +31.14 | - |
| 3 | 95.15 | +3.29 | - |
| **4** | **91.86** | **0.00** | **Selected (Parsimony)** |
| 5 | 91.86 | 0.00 | Equivalent BIC |
| 6 | 94.14 | +2.29 | - |

**K=4 selected:** Parsimony rule applied (K=4 and K=5 equivalent BIC, selected smaller K)

**Cluster Quality Validation:**

| Metric | Value | Threshold | Status |
|--------|-------|-----------|--------|
| Silhouette Score | 0.352 | e0.40 acceptable | POOR (improved from 0.34) |
| Davies-Bouldin Index | 0.952 | <1.0 good | GOOD |
| Bootstrap Jaccard | 0.871 | >0.75 stable | STABLE |
| Jaccard 95% CI | [0.756, 1.000] | - | Robust |

**Interpretation:** Clusters STABLE but FUZZY (centroids distinct, members overlap substantially)

### Cluster Characterizations

**Cluster 0: Average Baseline, Fast Decline (N=36, 36%)**

| Variable | Mean | SD |
|----------|------|----|
| What Intercept | +0.284 | 0.260 |
| Where Intercept | +0.256 | 0.270 |
| What Slope | **-0.036/day** | 0.023 |
| Where Slope | **-0.028/day** | 0.024 |

- Classic forgetting profile: average baseline, gradual decay
- Largest cluster (36% of sample)

---

**Cluster 1: Average Baseline, Improving (N=28, 28%)**

| Variable | Mean | SD |
|----------|------|----|
| What Intercept | -0.207 | 0.263 |
| Where Intercept | -0.202 | 0.294 |
| What Slope | **+0.037/day** | 0.024 |
| Where Slope | **+0.039/day** | 0.024 |

- Memory IMPROVES across both domains (practice/consolidation effects)
- Positive slopes significantly above zero
- Second largest cluster (28%)

---

**Cluster 2: Low Baseline, Domain-Dissociated Slopes (N=17, 17%)**

| Variable | Mean | SD |
|----------|------|----|
| What Intercept | **-0.815** | 0.258 |
| Where Intercept | **-0.850** | 0.237 |
| What Slope | **+0.011/day** | 0.024 |
| Where Slope | **-0.039/day** | 0.024 |

- Severely impaired baseline (both domains < -0.81 theta)
- Domain dissociation: What stable/improving, Where declining
- Smallest cluster (17%)

---

**Cluster 3: High Baseline, Stable/Improving (N=19, 19%)**

| Variable | Mean | SD |
|----------|------|----|
| What Intercept | **+0.497** | 0.295 |
| Where Intercept | **+0.573** | 0.308 |
| What Slope | **+0.004/day** | 0.024 |
| Where Slope | **+0.030/day** | 0.024 |

- Superior baseline memory (both domains > +0.49 theta)
- Stable/improving trajectories (cognitive reserve profile)

---

### Model Comparison (K=4 vs K=5)

**Original (Log-Only Random Effects):**
- K=5 selected (clear BIC minimum: 90.09)
- Silhouette=0.34, Jaccard=0.88

**Model-Averaged Rerun:**
- K=4 selected (parsimony rule: ”BIC=0.001 between K=4 and K=5)
- Silhouette=0.352 (+0.012), Jaccard=0.871 (-0.009)

**Impact:** Model averaging reduces overfitting ’ more parsimonious structure (K=4 vs K=5)

---

## 6. Visualizations

### Plot 1: Cluster Scatter Plot Matrix
**File:** `plots/cluster_scatter_matrix.png`

**Description:**
4×4 scatter plot matrix showing pairwise relationships among 4 clustering variables (What/Where intercepts and slopes), with 16 panels total. Individual participants (N=100) colored by cluster assignment (4 colors), cluster centroids marked with large black X symbols.

**Key Patterns:**
- **Cluster 0 (Blue, N=36):** Central position with negative slope values (declining memory)
- **Cluster 1 (Orange, N=28):** Shifted toward positive slope values (improving memory)
- **Cluster 2 (Green, N=17):** Bottom-left quadrant (low baseline), most visually distinct
- **Cluster 3 (Red, N=19):** Top-right quadrant (high baseline, stable/improving)
- **Diagonal histograms:** Bimodal slope distributions visible (declining vs improving participants)
- **Overlap:** Fuzzy boundaries between adjacent clusters (explains silhouette=0.352)
- **What-Where correlation:** Strong positive correlation for intercepts (rH0.85) and slopes (rH0.75)

**Connection to Findings:**
Visual confirms statistical pattern: centroids distinct (good Davies-Bouldin=0.952), members overlapping (poor silhouette=0.352). Bimodal slope distribution (declining vs improving) well-captured by K=4 structure.

---

### Plot 2: BIC Elbow Curve
**File:** `plots/bic_elbow.png`

**Description:**
Line plot showing BIC values across K=1 to K=6. Clear minimum at K=5 (BIC=91.86), with K=4 essentially equivalent (”BIC=0.001). Parsimony rule selects K=4.

---

### Plot 3: Cluster Profiles
**File:** `plots/cluster_profiles.png`

**Description:**
Bar plot showing mean intercepts and slopes for each cluster across What/Where domains. Clear visualization of 4 prototypical profiles.

---

## 7. Interpretation

### Hypothesis Testing

**Outcome:** SUPPORTED (with model-averaged input)

**Rationale:**
- Latent profiles identified: K=4 clusters (within expected 2-4 range)
- Domain-specific patterns detected: Cluster 2 shows domain dissociation (improving What, declining Where)
- Interpretable cluster characterizations: All 4 clusters have meaningful domain-specific patterns
- BUT cluster quality POOR: Silhouette=0.352 (substantial overlap, continuous variation likely)

**Conclusion:**
K=4 prototypical forgetting profiles identified via model-averaged random effects. Parsimony rule selected K=4 (not K=5), resulting in more interpretable structure: (1) Average/Declining, (2) Average/Improving, (3) Low/Dissociated, (4) High/Stable. Cluster assignments STABLE (Jaccard=0.871) but FUZZY (silhouette=0.352), suggesting continuous variation along baseline and trajectory dimensions.

### Theoretical Implications

**Dual-Process Theory (Yonelinas, 2002):**
- **Mixed support:** Cluster 2 shows domain dissociation (improving What, declining Where), suggesting differential consolidation rates
- **BUT:** Strong What-Where correlation (rH0.85 intercepts, rH0.75 slopes) suggests shared variance dominates (general memory factor)
- **Interpretation:** VR encoding may integrate What-Where into unified episodic representation, with domain dissociation emerging only in low-baseline subgroup

**Consolidation Theory (Dudai, 2004):**
- **Strong support:** 47% of sample (Clusters 1+3) show improving memory over 6 days (positive slopes)
- **Individual differences:** 4 clusters show divergent slope patterns (declining 36%, improving 47%, mixed 17%)
- **Heterogeneity in consolidation efficiency:** Not uniform forgetting, but individual variation in offline processing

**Model Averaging Impact:**
- Ensemble smoothing reduces single-model noise (Log model #10 may over-estimate decline)
- PowerLaw dominance (top 5 models, 60% weight) produces shallower/positive slopes
- More robust cluster structure (K=4) aligns better with theoretical predictions (2-4 profiles expected)

### Cross-RQ Patterns

**Convergent Evidence:**
- RQ 5.2.6 (Domain-Specific Variance Decomposition): High What-Where correlation confirmed (ICC_slope r=0.77), supports general memory factor interpretation
- RQ 5.1.5 (General Clustering): K=2 for omnibus factor, K=4 for domain-specific suggests domain analysis reveals finer individual differences
- RQ 5.2.1 (When Domain Floor Effect): When exclusion consistent across domain-specific RQs (77% attrition prevents reliable analysis)

### Unexpected Findings

**1. K=4 Selected (Not K=5) via Parsimony Rule**
- Original Log-only analysis: K=5 (clear BIC minimum)
- Model-averaged rerun: K=4 and K=5 equivalent (”BIC=0.001), parsimony rule applied
- **Explanation:** Model averaging smooths random effects ’ reduces small-cluster formation ’ triggers parsimony threshold
- **Investigation suggested:** Compare K=4 vs K=5 cluster assignments (Adjusted Rand Index) to assess whether 5th cluster was noise artifact

**2. Nearly Half of Sample Shows IMPROVING Memory (47% Clusters 1+3)**
- Contradicts forgetting expectation (memory should decline over 6 days)
- **Possible explanations:** Practice effects (testing effect), sleep consolidation, PowerLaw model weighting (shallower decline), VR novelty effects
- **Investigation suggested:** Examine whether Cluster 1 participants had high PowerLaw model weights in RQ 5.2.6

**3. Cluster 2 Domain Dissociation (What Improving, Where Declining) in Low-Baseline Group**
- Domain-selective consolidation pattern: Object memory improves (+0.011/day), spatial memory declines (-0.039/day)
- **Only in low-baseline group** (not high-baseline Cluster 3)
- **Possible explanations:** Differential consolidation (perirhinal vs hippocampal), floor effects, model averaging revealing masked dissociation
- **Theoretical implication:** Plasticity mechanisms may differ across baseline ability levels

---

## 8. Limitations

### Sample Limitations
- N=100 adequate for K-means (rule: N e 20K = 80), BUT lower bound for LPA (Nylund et al. recommend Ne200)
- Smallest cluster (Cluster 2) has only N=17 participants (limited power for within-cluster heterogeneity)
- University undergraduate sample (age MH20, narrow range) ’ may not generalize to older adults or clinical populations
- Missing data assumed MAR (if MNAR, random effects biased ’ cluster assignments biased)

### Methodological Limitations

**When Domain Exclusion (CRITICAL):**
- 77% item attrition during purification (23 ’ 5 items)
- 6-9% floor effect at baseline
- **Impact:** Only 4 clustering variables (not 6), cannot examine What-Where-When dissociations
- **Consequence:** Incomplete episodic memory profile (2/3 domains only)

**Model Averaging as Input:**
- **Strengths:** Reduces single-model overfitting, ensemble weighting captures uncertainty
- **Limitations:** Smoothing bias (may under-estimate extreme slopes), uncertainty not propagated (treats ensemble as fixed values)

**K-Means Assumptions:**
- **Spherical clusters:** Scatter matrix shows elongated/elliptical shapes (assumption violated)
- **Hard assignment:** No uncertainty (fuzzy boundaries suggest many participants in overlap zones)
- **Solution:** GMM sensitivity analysis recommended (allows elliptical clusters, probabilistic membership)

**Cluster Quality:**
- Silhouette=0.352 (POOR, below 0.40 acceptable threshold)
- Contradictory metrics: Davies-Bouldin (0.952, Good) vs Silhouette (0.352, Poor)
- **Recommendation:** Interpret as prototypical profiles, not discrete types

**Data Source Dependency:**
- Clustering uses model-averaged random effects from RQ 5.2.6 Step 08
- Random effect estimates have uncertainty (BLUPs + model weight uncertainty)
- Cluster assignments don't account for estimation error

### Generalizability Constraints

**Population:**
- May not generalize to: older adults (age-related cognitive decline), clinical populations (MCI/dementia), children (developing episodic systems)

**Context:**
- Desktop VR paradigm (not fully immersive HMD) ’ cluster patterns may differ in immersive VR
- Laboratory setting with controlled retention intervals (Day 0, 1, 3, 6) ’ real-world forgetting may differ

**Task:**
- REMEMVR-specific VR environment (museum paradigm) ’ cluster profiles may differ for other episodic tasks
- Neutral content (no emotional salience) ’ emotional memories may show different clustering

---

## 9. Publication-Ready Summary

**Context & Method:** We examined whether N=100 participants could be grouped into latent classes based on domain-specific forgetting trajectories (What/Where intercepts and slopes) using K-means clustering on model-averaged random effects from 17-model Akaike-weighted ensemble. When domain excluded due to floor effect (77% item attrition). K=1-6 models tested via BIC selection.

**Results:** K=4 clusters selected via parsimony rule (K=4 and K=5 equivalent BIC, ”BIC=0.001). Cluster quality POOR (silhouette=0.352) but STABLE (Jaccard=0.871, 95% CI [0.756, 1.000]). Four prototypical profiles: (1) Average/Declining (36%), (2) Average/Improving (28%), (3) Low/Domain-Dissociated (17%), (4) High/Stable (19%). Notable: 47% of sample shows improving memory over 6 days (Clusters 1+3), suggesting heterogeneous consolidation capacity. Cluster 2 shows domain dissociation (What improving +0.011/day, Where declining -0.039/day) in low-baseline subgroup only.

**Interpretation:** Individual differences in domain-specific forgetting reveal 4 stable but fuzzy prototypical profiles. Model averaging (PowerLaw dominance vs Log #10) produces more parsimonious clustering (K=4 vs original K=5) with maintained stability (Jaccard=0.871 vs 0.88). Strong What-Where correlation (rH0.85 intercepts, rH0.75 slopes) suggests general memory factor dominates, with domain dissociation emerging only in low-baseline subgroup. Nearly half show improving memory, supporting individual differences in consolidation efficiency.

**Conclusion:** K=4 prototypical forgetting profiles provide exploratory framework for individual differences in domain-specific episodic memory. Fuzzy boundaries (silhouette=0.352) indicate continuous variation more accurate than discrete types. Recommend interpreting clusters as descriptive profiles (research communication) while reporting continuous random effects (clinical interpretation). Model averaging provides more robust, parsimonious structure resilient to single-model overfitting.

---

## 10. Metadata & Sources

### Report Metadata
- **Generated:** 2026-01-01
- **Agent:** rq_report v1.0.0 (Sonnet 4.5 model)
- **RQ Folder:** results/ch5/5.2.7/

### Sources Synthesized

**Archive Sources:** 2 topics, 2 entries
- rq_5.2.7_complete_domain_clustering.md (archive, 2025-12-03 22:50)
- Archive index entry line 398-399 (complete execution summary)

**RQ Files:** 23 files
- Core docs: concept.md, plan.md, summary.md
- Validation: (none - no PLATINUM certification)
- Specifications: (none - tools specified in 3_tools.yaml embedded in workflow)
- Execution: status.yaml, 13 data files, 7 log files, 3 plot files (cluster_scatter_matrix.png, bic_elbow.png, cluster_profiles.png)
- PLATINUM: (none - RQ completed before certification workflow implemented)

### Warnings Flagged

**Warnings:**
- No PLATINUM certification files found (RQ completed before certification workflow)
- Cluster quality POOR (silhouette=0.352 < 0.40 acceptable threshold) - interpret clusters as prototypical profiles not discrete categories
- When domain excluded (77% item attrition) - incomplete episodic memory profile (2/3 domains)
- Model averaging smoothing bias - may under-estimate extreme slopes (continuous random effects recommended for clinical use)

---

**End of Report**
