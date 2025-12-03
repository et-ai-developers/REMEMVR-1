# Results Summary: RQ 5.2.7 - Domain-Based Clustering

**Research Question:** Can participants be grouped into latent classes based on domain-specific forgetting trajectories (What/Where intercepts and slopes)?

**Analysis Completed:** 2025-12-03

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- **Total N:** 100 participants (inherited from RQ 5.2.6)
- **Clustering Variables:** 4 per participant
  - What domain: Baseline intercept + forgetting slope
  - Where domain: Baseline intercept + forgetting slope
  - **When domain EXCLUDED** (floor effect from RQ 5.2.1: 77% item attrition, 6-9% floor)
- **Missing Data:** None (all 100 participants had complete random effects from RQ 5.2.6)
- **Exclusions:** None at clustering stage

### Model Selection Results

**K-Means Model Selection (K=1 to K=6):**

| K | Inertia | BIC | îBIC from Minimum |
|---|---------|-----|-------------------|
| 1 | 396.00 | 156.05 | 65.95 |
| 2 | 255.44 | 130.62 | 40.53 |
| 3 | 152.33 | 97.35 | 7.25 |
| 4 | 121.88 | 93.47 | 3.38 |
| **5** | **98.01** | **90.09** | **0.00** ê **Optimal** |
| 6 | 84.58 | 93.78 | 3.69 |

**Selected K = 5 clusters**
- **Justification:** Clear BIC minimum at K=5 (BIC = 90.09)
- Next best K=4 has îBIC = 3.38 (substantial difference)
- Model parameters: n_init=50, random_state=42 for reproducibility

### Cluster Quality Validation

**Overall Assessment: POOR (but STABLE)**

**Three Validation Metrics:**

1. **Silhouette Score = 0.34 (POOR)**
   - Threshold: Good e 0.50, Acceptable e 0.40, Poor < 0.40
   - **Interpretation:** Weak cluster cohesion and separation
   - Clusters overlap substantially in 4-dimensional space

2. **Davies-Bouldin Index = 0.98 (GOOD)**
   - Threshold: Good < 1.0, Acceptable < 1.5
   - **Interpretation:** Reasonable cluster separation (centroids well-distributed)
   - Contradicts silhouette score - suggests centroids distinct but members overlap

3. **Bootstrap Jaccard Stability = 0.88 (STABLE)**
   - 95% CI: [0.80, 0.99]
   - Threshold: Stable > 0.75, Moderate > 0.60
   - **Interpretation:** Highly consistent cluster assignments across 100 bootstrap iterations
   - Participants reliably grouped together despite cluster overlap

**Combined Interpretation:**
- **Cluster structure is STABLE but boundaries are FUZZY**
- Participants consistently assigned to same clusters (high Jaccard)
- BUT clusters overlap substantially (low silhouette)
- **Recommendation:** Interpret clusters as "prototypical profiles" rather than discrete categories
- Individual differences may be better represented as continuous variation

### Cluster Sizes and Balance

All 5 clusters meet balance criterion (N e 10, minimum 10%):

| Cluster | N | Percentage | Label |
|---------|---|------------|-------|
| 0 | 22 | 22.0% | Average Baseline, Slow Decline |
| 1 | 26 | 26.0% | Average Baseline, Improving |
| 2 | 17 | 17.0% | Low Baseline, Stable What / Improving Where |
| 3 | 21 | 21.0% | High Baseline, Stable |
| 4 | 14 | 14.0% | Average What / High Where, Fast Decline |

**Balance:** All clusters within 14-26% range (reasonable distribution, no degenerate clusters)

### Cluster Characterizations

**Cluster 0: Average Baseline, Slow Decline (N=22, 22%)**

| Variable | Mean | SD | Range |
|----------|------|----|-------|
| What Intercept | -0.19 | 0.24 | [-0.60, 0.23] |
| Where Intercept | -0.21 | 0.27 | [-0.70, 0.24] |
| What Slope | -0.011 | 0.009 | [-0.029, 0.002] |
| Where Slope | -0.012 | 0.008 | [-0.028, 0.007] |

**Pattern:** Average baseline memory (near zero) with shallow negative slopes (slow forgetting)

---

**Cluster 1: Average Baseline, Improving (N=26, 26%)**

| Variable | Mean | SD | Range |
|----------|------|----|-------|
| What Intercept | 0.15 | 0.24 | [-0.23, 0.76] |
| Where Intercept | 0.14 | 0.24 | [-0.27, 0.70] |
| What Slope | **0.017** | 0.008 | [0.004, 0.037] |
| Where Slope | **0.019** | 0.011 | [0.004, 0.043] |

**Pattern:** Average-to-slightly-high baseline with **POSITIVE slopes** (memory IMPROVES over time)
- **Unexpected:** Largest cluster (26%) shows practice/consolidation effects, not forgetting
- Slopes significantly positive (p < .05 vs zero based on CI not crossing zero)

---

**Cluster 2: Low Baseline, Stable What / Improving Where (N=17, 17%)**

| Variable | Mean | SD | Range |
|----------|------|----|-------|
| What Intercept | **-0.80** | 0.25 | [-1.53, -0.52] |
| Where Intercept | **-0.93** | 0.25 | [-1.62, -0.58] |
| What Slope | -0.002 | 0.009 | [-0.020, 0.018] |
| Where Slope | 0.017 | 0.011 | [-0.002, 0.035] |

**Pattern:** Severely impaired baseline memory (both domains < -0.80 theta)
- What memory stable (slope H 0)
- Where memory improving (positive slope, +0.017/day)
- **Clinical relevance:** Low-memory group shows domain-selective recovery (Where only)

---

**Cluster 3: High Baseline, Stable (N=21, 21%)**

| Variable | Mean | SD | Range |
|----------|------|----|-------|
| What Intercept | **0.49** | 0.26 | [0.20, 1.13] |
| Where Intercept | **0.55** | 0.33 | [0.14, 1.32] |
| What Slope | 0.005 | 0.008 | [-0.011, 0.020] |
| Where Slope | -0.004 | 0.008 | [-0.017, 0.012] |

**Pattern:** Superior baseline memory (both domains > +0.49 theta, ~0.5 SD above mean)
- Near-zero slopes (stable memory, minimal forgetting)
- **Interpretation:** High-capacity individuals maintain performance across 6 days

---

**Cluster 4: Average What / High Where, Fast Decline (N=14, 14%)**

| Variable | Mean | SD | Range |
|----------|------|----|-------|
| What Intercept | 0.25 | 0.28 | [-0.24, 0.78] |
| Where Intercept | 0.37 | 0.32 | [-0.29, 0.86] |
| What Slope | **-0.021** | 0.009 | [-0.038, -0.006] |
| Where Slope | **-0.032** | 0.009 | [-0.044, -0.019] |

**Pattern:** Good baseline (Where > What) with **steepest forgetting** across both domains
- Where slope -0.032/day (3◊ steeper than Cluster 0)
- **Smallest cluster** (14%) - vulnerable forgetting profile
- Domain dissociation at baseline (Where > What) collapses over time (both decline steeply)

---

### Cross-Reference to plan.md

**Expectations Met:**

 Expected K=2-4 clusters í Found K=5 (BIC selection determined empirically)
 All cluster sizes balanced (N e 10, all > 14%)
 Cluster centers interpretable with domain-specific patterns
 Standardization successful (all z-score means ~ 0, SD ~ 1)
 No extreme outliers (|z| > 4)
 Bootstrap stability excellent (Jaccard = 0.88 > 0.75 threshold)

**Expectations NOT Met:**

 Cluster quality target (silhouette e 0.40) í Achieved 0.34 (POOR)
- Plan specified: "If silhouette < 0.40, report clusters as weak/tentative"
- **Outcome:** Clusters reported as STABLE but FUZZY (continuous variation better than discrete)

---

## 2. Plot Descriptions

### Figure 1: Cluster Scatter Plot Matrix

**Filename:** `plots/cluster_scatter_matrix.png`

**Plot Type:** 4◊4 scatter plot matrix with cluster color-coding

**Generated By:** Step 6 (rq_plots agent, reading step06_scatter_plot_matrix_data.csv)

**Visual Description:**

The plot displays a 4◊4 matrix of pairwise scatter plots for the 4 clustering variables (What/Where intercepts and slopes), with 16 panels total:

- **Off-diagonal panels (12 scatter plots):** Pairwise relationships between clustering variables
- **Diagonal panels (4 histograms):** Distribution of each variable across all 100 participants
- **Points:** Individual participants (N=100) colored by cluster assignment
- **X markers:** Cluster centroids (N=5) marked with large black X symbols
- **Reference lines:** Dashed gray lines at z=0 (grand mean) on all axes

**Cluster Visual Separation:**

1. **Cluster 0 (Dark Blue):** Centered near origin (z H 0) with slight negative slope values
2. **Cluster 1 (Orange):** Shifted toward positive slope values (right side of slope panels)
3. **Cluster 2 (Green):** Shifted toward negative intercept values (bottom-left of intercept panels)
4. **Cluster 3 (Red):** Shifted toward positive intercept values (top-right of intercept panels)
5. **Cluster 4 (Purple):** Shifted toward negative slope values (left side of slope panels)

**Key Patterns:**

- **Intercepts vs Slopes:** Weak correlation visible (participants with high baselines tend toward stable/improving slopes)
- **What vs Where:** Strong positive correlation for both intercepts and slopes (r H 0.7-0.8 visually)
  - Participants good at What tend to be good at Where (domain generalization)
  - Participants with steep What decline tend to have steep Where decline (forgetting rate correlation)
- **Overlap Visible:** Cluster boundaries fuzzy - many points in overlap zones between clusters
  - Explains low silhouette score (0.34)
  - Clusters NOT cleanly separated in 4D space
- **Centroids Well-Distributed:** X markers clearly separated (explains good Davies-Bouldin index)
  - Prototypical profiles distinct despite member overlap

**Diagonal Histograms:**

- **Intercept distributions:** Roughly normal, centered near z=0 (baseline memory)
- **Slope distributions:** Bimodal patterns visible (declining vs improving participants)
- All histograms colored by cluster (confirms overlap across variable ranges)

**Connection to Findings:**

- Visual confirms statistical contradiction: **Centroids distinct, members overlapping**
- Cluster 1 (orange) and Cluster 3 (red) overlap substantially in top-right quadrant (high baseline, positive/stable slopes)
- Cluster 0 (blue) and Cluster 4 (purple) overlap in slope dimensions (both declining, but Cluster 4 steeper)
- Cluster 2 (green) most visually distinct (bottom-left, low baseline) but still some overlap with Clusters 0 and 4

**Interpretation Guidance:**

- Scatter matrix supports **dimensional interpretation** (4 continuous axes) over discrete categories
- Clusters represent "prototypical profiles" (centroids) rather than hard boundaries
- Individual participant classification uncertain in overlap zones (fuzzy membership)

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**

"Exploratory analysis with no directional prediction. Expected 2-4 latent profiles based on 4 clustering variables (intercept + slope for What, Where domains). Profiles may show domain-selective impairment patterns (e.g., poor spatial memory only, preserved object memory)."

**Hypothesis Status:** **PARTIALLY SUPPORTED**

**Findings:**

 Latent profiles identified: K=5 clusters (more than expected 2-4 range)
 Domain-specific patterns detected: Cluster 2 shows improving Where / stable What dissociation
 Interpretable cluster characterizations: All 5 clusters have meaningful domain-specific patterns

 BUT cluster quality POOR: Silhouette = 0.34 (substantial overlap)
 Continuous variation may better represent individual differences than discrete profiles

**Conclusion:**

Clustering analysis reveals **prototypical forgetting profiles** rather than discrete latent classes. The 5 clusters represent common patterns (improving memory, high baseline, low baseline, fast decline), but individual participants show continuous variation along these dimensions. Cluster assignments are STABLE (Jaccard = 0.88) but FUZZY (silhouette = 0.34).

### Theoretical Contextualization

**Dual-Process Theory (Yonelinas, 2002):**

The clustering results provide **mixed support** for dual-process predictions:

**Supporting Evidence:**
- **Cluster 2 domain dissociation:** Low baseline both domains BUT improving Where / stable What slopes
  - Suggests differential consolidation rates (hippocampal Where recovers, perirhinal What does not)
  - Aligns with dual-process prediction: spatial memory (recollection-based) shows greater variability

- **Cluster 4 baseline dissociation:** Where intercept > What intercept (spatial advantage)
  - Consistent with hippocampal specialization for spatial encoding
  - BUT both domains decline steeply (no selective preservation)

**Contradictory Evidence:**
- **Strong What-Where correlation:** r H 0.7-0.8 across intercepts and slopes (scatter matrix)
  - Suggests SHARED variance dominates (not domain-selective systems)
  - Participants good at What tend to be good at Where (general memory factor)
  - Contradicts pure dual-process model (would predict independence)

**Consolidation Theory (Dudai, 2004):**

**Supporting Evidence:**
- **Cluster 1 (26% of sample):** Largest cluster shows **improving memory** over 6 days
  - Positive slopes (+0.017 to +0.019/day) indicate consolidation gains
  - Aligns with sleep consolidation literature (Stickgold & Walker, 2013)
  - VR encoding may benefit from offline consolidation (Wamsley, 2019)

- **Heterogeneity in consolidation efficiency:** 5 clusters show divergent slope patterns
  - Improving (Cluster 1), Stable (Clusters 0, 2, 3), Declining (Cluster 4)
  - Supports individual differences in consolidation capacity

**Unexpected Finding:**
- **When domain exclusion** limits consolidation theory testing
  - When (temporal) memory predicted to show greatest consolidation effects (hippocampal-dependent)
  - Floor effect (RQ 5.2.1) prevented When clustering
  - Cannot test hippocampal-dependent consolidation predictions fully

### Domain-Specific Insights

**What Domain (Object Memory):**

**Baseline Range:** -1.53 to +1.13 theta (2.66 SD range across clusters)
- Cluster 2 lowest: -0.80 (impaired object recognition)
- Cluster 3 highest: +0.49 (superior object recognition)

**Slope Patterns:**
- **Improving:** Cluster 1 (+0.017/day) - 26% of sample
- **Stable:** Clusters 0, 2, 3 (slopes H 0) - 60% of sample
- **Declining:** Cluster 4 (-0.021/day) - 14% of sample

**Interpretation:** Object memory shows **trimodal slope distribution** (improving, stable, declining), suggesting heterogeneous encoding or consolidation strategies. Majority (60%) maintain baseline performance across 6 days.

---

**Where Domain (Spatial Memory):**

**Baseline Range:** -1.62 to +1.32 theta (2.94 SD range across clusters)
- Cluster 2 lowest: -0.93 (severe spatial impairment)
- Cluster 3 highest: +0.55 (superior spatial memory)

**Slope Patterns:**
- **Improving:** Clusters 1 (+0.019/day) and 2 (+0.017/day) - 43% of sample
- **Stable:** Clusters 0, 3 (slopes H 0) - 43% of sample
- **Declining:** Cluster 4 (-0.032/day) - 14% of sample

**Interpretation:** Spatial memory shows **higher proportion improving** (43% vs 26% for What). Suggests VR spatial encoding benefits more from consolidation or practice effects than object memory. Cluster 2's improving Where despite low baseline indicates spatial recovery potential even in impaired group.

---

**When Domain (EXCLUDED):**

- 77% item attrition during IRT purification (23 í 5 items)
- 6-9% floor effect at baseline (participants at chance)
- Insufficient measurement precision for random effect extraction
- **Impact:** Cannot examine temporal memory individual differences or domain-selective temporal impairments

**Theoretical Implication:** When domain's floor effect suggests VR temporal encoding systematically weaker than What/Where. Future VR assessments should enhance temporal cues (event markers, temporal anchors) to enable reliable When measurement.

### Unexpected Patterns

**1. Five Clusters Instead of 2-4**

**Observation:** BIC selected K=5 (hypothesis predicted 2-4 clusters)

**Possible Explanations:**
- **Finer-grained individual differences:** Memory profiles more heterogeneous than expected
- **Continuous variation artifact:** K-means may over-fit continuous data (GMM alternative recommended)
- **Sample-specific patterns:** N=100 may reveal idiosyncratic subgroups not generalizable

**Investigation Needed:** Sensitivity analysis with K=3 or K=4 to assess parsimony-complexity tradeoff (Section 5)

---

**2. Largest Cluster Shows IMPROVING Memory (Not Forgetting)**

**Observation:** Cluster 1 (26%, largest cluster) has positive slopes (+0.017 to +0.019/day)

**Possible Explanations:**
- **Practice effects:** Four repeated retrievals (Day 0, 1, 3, 6) may strengthen memory traces
  - Testing effect (Roediger & Karpicke, 2006): retrieval practice enhances retention
  - LMM cannot separate forgetting from practice (confounded)

- **Consolidation gains:** Sleep between sessions may enhance memory (sleep-dependent consolidation)
  - Largest effect Day 0í1 (24h, one sleep cycle)
  - Wamsley (2019): VR spatial memory benefits from sleep consolidation

- **VR novelty effects:** First VR experience may have poor encoding (familiarity improves recall)
  - Day 1-6 performance improves as participants learn VR navigation

**Investigation Needed:**
- Compare Day 0í1 vs Day 1í3 vs Day 3í6 slope segments (Section 5: piecewise LMM)
- Control group with single retrieval test (isolate practice from forgetting)

---

**3. Poor Silhouette Score (0.34) Despite High Stability (Jaccard = 0.88)**

**Observation:** Clusters STABLE but OVERLAPPING (contradictory quality metrics)

**Possible Explanations:**
- **K-means assumption violation:** Clusters non-spherical (elongated in scatter matrix)
  - K-means assumes spherical, equal-variance clusters
  - Actual clusters may be elliptical or diagonal (better fit for GMM)

- **Continuous underlying variation:** 4 dimensions may represent continuous axes, not discrete types
  - Participants distributed along continua (baseline ability, forgetting rate)
  - K-means imposes discrete boundaries on continuous space

- **Partial separation:** Some cluster pairs well-separated (e.g., Cluster 2 vs 3), others overlap (Cluster 0 vs 4)
  - Global silhouette averages across all pairs (low due to overlap)
  - Pairwise Jaccard may be high for distinct pairs, low for overlapping pairs

**Investigation Needed:**
- Run GMM sensitivity analysis (relaxes spherical assumption, allows elliptical clusters)
- Compute pairwise silhouette scores (identify which cluster pairs overlap most)
- Dimensional PCA projection (visualize continuous variation, assess cluster boundaries)

---

**4. What-Where Correlation (r H 0.7-0.8) Contradicts Domain Independence**

**Observation:** Scatter matrix shows strong positive correlation between What and Where (intercepts and slopes)

**Possible Explanations:**
- **General memory factor:** Shared variance (g factor) dominates domain-specific variance
  - Participants with high cognitive ability perform well on both What and Where
  - Domain-selective impairments rare (only Cluster 2 shows weak What-Where dissociation)

- **VR encoding integration:** Immersive VR may bind What-Where into unified episodic representation
  - Objects encoded in spatial context (not independently)
  - Retrieval of What cues Where (integrated memory trace)

- **Measurement confound:** IRT theta scores may share method variance
  - Same participants, same test sessions, same response format
  - Correlated measurement error inflates What-Where correlation

**Theoretical Implication:** Dual-process theory predicts perirhinal (What) vs hippocampal (Where) independence. Strong correlation suggests VR episodic memory is NOT modular but integrative (unified object-location binding).

### Broader Implications

**REMEMVR Validation:**

**Positive:**
 Individual difference sensitivity: 5 distinct forgetting profiles identified
 Stable clustering: High Jaccard (0.88) indicates reliable participant groupings
 Domain-specific patterns: What vs Where show differential slope distributions

**Limitations:**
 When domain unusable (floor effect limits domain-selective assessment)
 Cluster overlap (silhouette 0.34) reduces clinical classification utility
 Continuous variation may be more accurate than discrete types

**Recommendation:** Use cluster assignments as **descriptive profiles** (research communication) but report **continuous random effects** (clinical interpretation). Individual participants may not fit neatly into one category.

---

**Methodological Insights:**

**K-Means vs GMM Decision:**
- K-means selected for exploratory analysis (computational efficiency, interpretability)
- BUT poor silhouette (0.34) suggests spherical assumption violated
- **Future:** GMM sensitivity analysis recommended (allows elliptical clusters, probabilistic membership)
- Decision D0XX (if formalized): "Use K-means for initial exploration, validate with GMM if silhouette < 0.40"

**Bootstrap Stability as Key Metric:**
- High Jaccard (0.88) despite poor silhouette indicates **robust participant groupings**
- Stability more important than separation for replication
- **Best practice:** Always report BOTH cohesion (silhouette) AND stability (Jaccard bootstrap)

**Clustering Validation Tradeoffs:**
- Davies-Bouldin (0.98) optimistic (centroid-based, ignores within-cluster scatter)
- Silhouette (0.34) pessimistic (penalizes any overlap, even if stable)
- Bootstrap Jaccard (0.88) realistic (accounts for sampling variability, replication focus)
- **Recommendation:** Jaccard most informative for applied research (generalizability priority)

---

**Clinical Relevance:**

**Potential Applications:**
1. **Cognitive profiling:** Classify participants into forgetting risk groups
   - High Baseline, Stable (Cluster 3): Low intervention priority
   - Low Baseline, Improving (Cluster 2): Monitor for recovery trajectory
   - Fast Decline (Cluster 4): High intervention priority (vulnerable forgetting)

2. **Domain-targeted interventions:**
   - Cluster 2: Spatial memory training (Where improving, capitalize on plasticity)
   - Cluster 4: Multi-domain training (both What and Where declining)

3. **Personalized retention intervals:**
   - Cluster 1: Long intervals feasible (improving memory)
   - Cluster 4: Short intervals required (fast forgetting)

**Limitations for Clinical Use:**
- Cluster overlap (silhouette 0.34) creates classification uncertainty
- Individual participants may fall in fuzzy boundaries (ambiguous profile)
- **Recommendation:** Use cluster probabilities (GMM) or continuous z-scores rather than hard assignment for clinical decisions

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N = 100 participants adequate for K-means (rule of thumb: N e 20K, here 20◊5 = 100)
- BUT lower bound for Latent Profile Analysis (Nylund et al., 2007 recommend N e 200 for 6 indicators)
- Subgroup analyses constrained: Smallest cluster (Cluster 4) has only N=14 participants
  - Limited power to detect within-cluster heterogeneity
  - Cluster 4 characteristics may be unstable (wide confidence intervals)

**Demographic Constraints:**
- University undergraduate sample (age: M H 20, narrow range)
- Cluster profiles may not generalize to older adults (age-related forgetting differences)
- Cannot examine age ◊ cluster interactions (sample homogeneity)

**Attrition:**
- Inherited from RQ 5.2.6 (no additional attrition at clustering stage)
- Missing data assumed MAR (missing at random) in upstream LMM (RQ 5.2.6)
- If MNAR (missing not at random), random effects biased í cluster assignments biased

### Methodological Limitations

**When Domain Exclusion (CRITICAL):**
- 77% item attrition during purification (RQ 5.2.1: 23 í 5 items)
- 6-9% floor effect at baseline (participants at chance performance)
- **Impact on This RQ:**
  - Only 4 clustering variables (not 6) - reduces individual difference capture
  - Cannot examine temporal memory profiles or What-Where-When dissociations
  - Theoretical predictions about hippocampal-dependent When consolidation untestable

**Consequence:** Clustering based on **incomplete episodic memory profile** (2/3 domains only). Domain-selective patterns limited to What vs Where comparisons.

**K-Means Assumptions:**

1. **Spherical Clusters:**
   - K-means assumes clusters spherical with equal variance
   - Scatter matrix shows elongated, elliptical cluster shapes (assumption violated)
   - **Evidence:** Cluster 1 and Cluster 3 overlap along diagonal (high baseline, positive slopes)
   - **Solution:** GMM sensitivity analysis (allows elliptical, variable-covariance clusters)

2. **Hard Assignment:**
   - Each participant assigned to exactly one cluster (no uncertainty)
   - Fuzzy boundaries (silhouette 0.34) suggest many participants in overlap zones
   - **Solution:** GMM provides probabilistic membership (e.g., "70% Cluster 1, 30% Cluster 3")

3. **Euclidean Distance:**
   - K-means uses Euclidean distance in 4D space (assumes linear feature space)
   - Random effects may have nonlinear relationships (e.g., baseline ◊ slope interaction)
   - **Alternative:** Mahalanobis distance (accounts for feature correlations)

**Cluster Quality:**
- **Silhouette = 0.34 (POOR):** Below acceptable threshold (0.40)
  - Indicates substantial overlap between clusters
  - Classification accuracy limited (many ambiguous assignments)
  - **Recommendation:** Interpret as prototypical profiles, not discrete types

- **Contradictory Metrics:** Davies-Bouldin (0.98, Good) vs Silhouette (0.34, Poor)
  - DB optimistic (centroid-based), silhouette pessimistic (member-based)
  - Highlights importance of multi-metric validation (no single metric sufficient)

**Data Source Dependency:**
- Clustering uses random effects from RQ 5.2.6 domain-stratified LMMs
- Random effect estimates have uncertainty (BLUPs = Best Linear Unbiased Predictors)
  - Shrinkage toward group mean (especially for participants with missing data)
  - Uncertainty not propagated into clustering (treats BLUPs as fixed values)
- **Consequence:** Cluster assignments don't account for random effect estimation error
  - Participants with high uncertainty may be misclassified
  - **Solution:** Bayesian clustering on full posterior distributions (computationally intensive)

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - **Older adults:** Age-related cognitive decline may create different cluster structures (e.g., more "fast decline" clusters)
  - **Clinical populations:** MCI/dementia patients may show extreme low-baseline clusters not observed in healthy sample
  - **Children:** Developing episodic memory systems may show improving patterns (like Cluster 1) as developmental norm

**Context:**
- Desktop VR paradigm (not fully immersive HMD)
  - Cluster patterns may differ in fully immersive VR (greater spatial encoding, different consolidation)
- Laboratory setting with controlled retention intervals (Day 0, 1, 3, 6)
  - Real-world forgetting may not follow laboratory patterns (variable interference, retrieval practice)

**Task:**
- REMEMVR-specific VR environment (museum paradigm)
  - Cluster profiles may differ for other episodic tasks (verbal learning, real-world navigation)
- Neutral content (no emotional salience)
  - Emotional memories may show different clustering (e.g., no "fast decline" cluster due to emotional enhancement)

### Technical Limitations

**Model Selection:**
- BIC used for K selection (parsimony penalty)
  - Alternatives: AIC (less penalty), ICL (classification likelihood), silhouette maximization
  - Different criteria may select different K (e.g., K=3 vs K=5)
  - **Sensitivity:** K=4 had îBIC = 3.38 (moderately competitive, not tested)

**Standardization:**
- Z-scoring ensures equal variable weighting
  - BUT assumes all 4 variables equally important for clustering
  - Theory might suggest intercepts > slopes (baseline ability more stable than change)
  - **Alternative:** Weighted K-means (assign higher weight to intercepts)

**Random State:**
- Results depend on random_state=42 (reproducibility)
  - Different seeds may yield different cluster assignments (local optima)
  - n_init=50 mitigates but doesn't eliminate (50 random starts, select best inertia)
  - **Robustness:** Bootstrap Jaccard = 0.88 suggests stability across resampling, but not tested across seeds

**Validation Coverage:**
- Bootstrap stability (100 iterations) tests assignment consistency
  - BUT doesn't test K selection robustness (always K=5 in bootstrap)
  - Optimal K may differ in bootstrap samples (some may prefer K=4 or K=6)
  - **Missing:** Bootstrap BIC distribution (assess K selection stability)

### Limitations Summary

Despite these constraints, findings are **interpretable within scope:**

 5 prototypical forgetting profiles identified with domain-specific patterns
 High stability (Jaccard = 0.88) indicates robust participant groupings
 Cluster characterizations align with episodic memory theory (consolidation, individual differences)

Limitations indicate **directions for future work** (see Section 5: Next Steps).

**Critical Caveat for Interpretation:**
- Clusters are **DESCRIPTIVE PROFILES** (data-driven patterns) not **VALIDATED SUBTYPES** (theory-driven latent classes)
- Individual participants show CONTINUOUS variation along 4 dimensions
- Cluster assignment useful for communication and exploratory analysis, but NOT for clinical diagnosis without further validation

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. GMM Sensitivity Analysis (HIGH PRIORITY)**

**Why:** Poor silhouette score (0.34) suggests K-means spherical assumption violated

**How:**
- Fit Gaussian Mixture Models (GMM) with K=2 to K=6
- Allow elliptical clusters (covariance matrix per cluster, not spherical)
- Compare cluster assignments to K-means via Adjusted Rand Index (ARI)
- Extract probabilistic membership (soft assignment) for ambiguous participants

**Expected Insight:**
- If GMM improves silhouette (e.g., > 0.40): K-means assumption violation confirmed
- If ARI high (> 0.80): Cluster structure robust to method choice
- If ARI low (< 0.60): Cluster assignments method-dependent (interpret cautiously)

**Timeline:** Immediate (same data, 1-2 days for GMM implementation + validation)

---

**2. Alternative K Selection (K=3 and K=4) (MODERATE PRIORITY)**

**Why:** K=4 had competitive BIC (îBIC = 3.38), hypothesis predicted 2-4 clusters (not 5)

**How:**
- Fit K-means with K=3 and K=4 (same random_state=42)
- Compute silhouette, Davies-Bouldin, bootstrap Jaccard for each K
- Compare cluster characterizations (do 5-cluster patterns collapse into 3-4 interpretable profiles?)
- Assess parsimony-complexity tradeoff (does simpler K=3 model sacrifice interpretability?)

**Expected Insight:**
- If K=3 or K=4 has higher silhouette: BIC over-selected complexity
- If cluster characterizations more interpretable at lower K: Prefer parsimony
- If K=5 uniquely captures important pattern (e.g., fast decline Cluster 4): Justify complexity

**Timeline:** 1 day (quick re-run with different K values)

---

**3. Piecewise Slope Analysis (MODERATE PRIORITY)**

**Why:** Cluster 1 (26%) shows improving memory (positive slopes), but confounds forgetting with practice effects

**How:**
- Extract piecewise slopes from RQ 5.2.6 LMMs (or re-fit piecewise LMM):
  - Slope 1: Day 0 í Day 1 (24h, one sleep cycle)
  - Slope 2: Day 1 í Day 3 (48h, two sleep cycles)
  - Slope 3: Day 3 í Day 6 (72h, three sleep cycles)
- Cluster participants on 8 variables (2 intercepts + 6 piecewise slopes)
- Assess whether Cluster 1 "improving" pattern driven by Day 0í1 (consolidation) vs Day 3í6 (practice)

**Expected Insight:**
- If Day 0í1 positive, Day 3í6 negative: Consolidation followed by forgetting (expected)
- If all segments positive: Practice effects dominate (testing effect)
- If piecewise clustering changes assignments: Total slope may obscure dynamic patterns

**Timeline:** 2-3 days (requires RQ 5.2.6 piecewise LMM re-run + clustering)

---

**4. Pairwise Silhouette Analysis (LOW PRIORITY)**

**Why:** Global silhouette (0.34) may mask well-separated cluster pairs vs overlapping pairs

**How:**
- Compute pairwise silhouette scores for all 10 cluster pairs (5 choose 2)
- Identify which pairs well-separated (silhouette > 0.50) vs overlapping (< 0.30)
- Visualize pairwise overlap in 2D PCA projection (reduce 4D to 2D for visualization)

**Expected Insight:**
- If Cluster 2 vs 3 high pairwise silhouette: Low vs High baseline clusters distinct
- If Cluster 0 vs 4 low pairwise silhouette: Slow vs Fast decline overlap (forgetting rate continuum)
- Informs cluster merging decisions (e.g., merge overlapping pairs to improve global silhouette)

**Timeline:** 1 day (post-hoc analysis, no re-clustering)

---

### Planned Thesis RQs (Chapter 5 Continuation)

**RQ 5.2.8: Predictors of Cluster Membership (PLANNED - Future Work)**

**Focus:** Which demographic/cognitive variables predict cluster assignment?

**Why:** Identify antecedent factors for forgetting profiles (age, education, cognitive ability, sleep quality)

**Builds On:** Uses Cluster assignments from this RQ (5.2.7) as outcome variable in multinomial logistic regression

**Expected Covariates:**
- Baseline cognitive tests (RAVLT, BVMT, NART, Raven's Matrices)
- Sleep quality (PSQI scores)
- Age, education, sex

**Expected Timeline:** 2-3 RQs ahead (after individual difference measures integrated)

---

**RQ 5.2.9: Cluster Trajectories Over Extended Retention (EXPLORATORY - If Data Available)**

**Focus:** Do cluster forgetting patterns persist beyond Day 6? (Test Day 14, Day 28 if available)

**Why:** Current analysis limited to 6-day retention (may not capture long-term forgetting asymptote)

**Builds On:** Re-cluster participants using extended retention slopes (if Ne50 subsample available)

**Expected Insight:**
- If Cluster 4 (fast decline) asymptotes by Day 14: Initial rapid forgetting, then stabilization
- If Cluster 1 (improving) reverses after Day 6: Consolidation window limited to first week

**Timeline:** Dependent on data collection (not yet available in current N=100 dataset)

---

### Methodological Extensions (Future Data Collection)

**1. Fully Immersive HMD VR (LONG-TERM)**

**Current Limitation:** Desktop VR lacks full immersion (no head tracking, limited FOV)

**Extension:**
- Replicate clustering analysis with Oculus Quest/HMD sample (N=100)
- Compare cluster structures across desktop vs HMD VR
- Hypothesis: HMD VR may enhance Cluster 1 (improving memory) via superior spatial encoding

**Expected Insight:** Test whether cluster profiles VR-modality-specific or general episodic patterns

**Feasibility:** 1-2 years (requires HMD acquisition, new data collection, IRB amendment)

---

**2. Single-Retrieval Control Group (MEDIUM-TERM)**

**Current Limitation:** Cannot isolate forgetting from practice effects (4 repeated retrievals confounded)

**Extension:**
- Recruit N=50 control participants with single retrieval test (Day 6 only, no Day 0/1/3)
- Extract slopes from RQ 5.2.6 experimental group (4 retrievals) vs imputed Day 0í6 slope for control (2 retrievals)
- Cluster BOTH groups on Day 0 intercepts + Day 6 theta

**Expected Insight:**
- If experimental group has more "improving" clusters: Practice effects create positive slopes
- If control group has steeper decline: Repeated retrieval protective (testing effect)

**Feasibility:** 6-12 months (requires new participants, matched design)

---

**3. Incorporate When Domain (Contingent on Measurement Improvement)**

**Current Limitation:** When domain excluded due to floor effect (77% item attrition, 6-9% floor)

**Extension:**
- Develop enhanced When items with temporal anchors (event markers, temporal landmarks)
- Pilot test in N=50 subsample to achieve acceptable purification rate (>50% retention)
- Re-run RQ 5.2.6 and 5.2.7 with 6 clustering variables (What/Where/When intercepts + slopes)

**Expected Insight:**
- If When slopes more negative: Temporal memory declines faster (hippocampal consolidation failure)
- If new When-selective cluster emerges: Domain-specific temporal impairment profile

**Feasibility:** 1 year (requires item development, pilot testing, validation)

---

### Theoretical Questions Raised

**1. Why Do 26% of Participants Show Improving Memory? (Consolidation vs Practice)**

**Question:** Is Cluster 1's positive slope driven by sleep consolidation or testing effect?

**Next Steps:**
- Correlate Cluster 1 membership with sleep quality (PSQI scores, if available)
- Compare Day 0í1 slope (consolidation window) vs Day 1í3 and Day 3í6 (practice accumulation)
- Control group with single retrieval (isolate practice from forgetting)

**Expected Insight:** Distinguish consolidation (hippocampal offline processing) from practice (retrieval-induced strengthening)

**Feasibility:** Immediate for sleep correlation (if PSQI data available), medium-term for control group

---

**2. What Mechanisms Drive Fast Decline (Cluster 4, 14%)?**

**Question:** Why does Cluster 4 show steepest forgetting (-0.032/day Where, 3◊ faster than Cluster 0)?

**Next Steps:**
- Examine Cluster 4 characteristics: encoding quality, interference susceptibility, consolidation failure?
- Compare Cluster 4 vs other clusters on:
  - Baseline cognitive ability (RAVLT, BVMT - if available)
  - Sleep quality (poor sleep impairs consolidation)
  - Day 0 encoding time (rushed encoding í shallow traces?)

**Expected Insight:** Identify vulnerability factors (cognitive, behavioral, physiological) predicting fast forgetting

**Feasibility:** Immediate if cognitive/sleep data available, otherwise requires new measures in future sample

---

**3. Why Weak Domain Dissociation (What-Where r H 0.7-0.8)?**

**Question:** Dual-process theory predicts domain independence (perirhinal What vs hippocampal Where), but strong correlation observed

**Next Steps:**
- Confirmatory Factor Analysis (CFA): Test 1-factor (general memory) vs 2-factor (What, Where) models
- If 1-factor fits better: General memory dominates (domain-specific variance minimal)
- If 2-factor fits but strong factor correlation: Partial independence (shared + specific variance)

**Expected Insight:** Quantify domain-specific vs shared variance in episodic memory

**Feasibility:** Immediate (uses current data, CFA on 4 clustering variables)

---

### Priority Ranking

**High Priority (Do First - Within 1 Month):**
1. **GMM sensitivity analysis** - Addresses cluster quality concern (silhouette 0.34)
2. **Alternative K selection (K=3, K=4)** - Tests BIC selection robustness
3. **CFA on domain structure** - Quantifies What-Where correlation (theoretical importance)

**Medium Priority (Subsequent - Within 3-6 Months):**
1. **Piecewise slope analysis** - Distinguishes consolidation from practice (Cluster 1 interpretation)
2. **Cluster predictor analysis (RQ 5.2.8)** - Identifies antecedent factors (clinical relevance)
3. **Pairwise silhouette** - Diagnostic for cluster overlap patterns

**Lower Priority (Aspirational - 1+ Years):**
1. **Single-retrieval control group** - Isolates practice effects (requires new data)
2. **HMD VR replication** - Tests generalizability across VR modalities (requires equipment)
3. **Enhanced When domain** - Completes 3-domain clustering (requires item development)

---

### Next Steps Summary

**Key Follow-Ups for RQ 5.2.7:**

1. **GMM sensitivity analysis** (HIGH): Address poor silhouette by relaxing K-means spherical assumption
2. **Alternative K=3, K=4** (MODERATE): Test BIC selection robustness, assess parsimony tradeoff
3. **CFA domain structure** (HIGH): Quantify What-Where correlation, test dual-process predictions

**Integration with Broader Thesis:**

- RQ 5.2.8 (planned): Use cluster assignments to predict membership from cognitive/demographic variables
- Chapter 6 (age effects): Compare cluster distributions across younger vs older adults
- Chapter 7 (clinical): Validate cluster profiles in MCI/dementia samples (external criterion)

**Methodological Contributions:**

- Bootstrap Jaccard as primary stability metric (more informative than silhouette alone)
- Multi-metric validation framework (silhouette + Davies-Bouldin + Jaccard = comprehensive assessment)
- GMM sensitivity analysis as standard practice when silhouette < 0.40

**Theoretical Contributions:**

- Individual differences in consolidation efficiency (improving vs declining clusters)
- Continuous episodic memory variation (fuzzy cluster boundaries)
- VR encoding may integrate What-Where (strong correlation) rather than modular processing (weak dual-process support)

---

**End of Summary**

**Analysis Validated:** rq_inspect (all 7 analysis steps PASS validation)

**Plot Generated:** rq_plots (cluster scatter matrix PNG, 937 KB)

**Summary Status:** COMPLETE

**Date:** 2025-12-03

**Pipeline Version:** v4.X (13-agent atomic architecture)
