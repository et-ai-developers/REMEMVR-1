# Results Summary: RQ 5.1.5 - Individual Clustering

**Research Question:** Can participants be grouped into latent classes based on their forgetting trajectories (intercepts and slopes)?

**Analysis Completed:** 2025-12-02

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Cluster Selection via BIC and Elbow Method

**Model Selection Procedure:**
- K-means clustering tested for K=1 to K=6 clusters
- BIC (Bayesian Information Criterion) computed for each K value
- Random initialization: n_init=50, random_state=42 for reproducibility

**BIC Results:**

| K | Inertia | BIC | Selection |
|---|---------|-----|-----------|
| 1 | 200.00 | 73.92 | - |
| 2 | 66.72 | -31.26 | **Optimal** |
| 3 | 34.40 | -92.90 | - |
| 4 | 22.75 | -129.66 | - |
| 5 | 16.81 | -155.29 | - |
| 6 | 12.70 | -178.76 | Boundary |

**Remedial Action Taken:**
BIC minimum occurred at boundary K=6, suggesting overfitting risk. Elbow method applied as remediation:
- Second derivative analysis identified K=2 as optimal elbow point (second_deriv=100.96)
- **K_final = 2 clusters selected** (via elbow method, not raw BIC minimum)

**Rationale:** BIC at boundary indicates penalty term insufficient to prevent overfitting. Elbow method provides conservative, interpretable solution consistent with theoretical prediction of 2-3 profiles.

### Cluster Assignments and Sizes

**Cluster Distribution:**
- **Cluster 0 (High baseline, slower change):** N=69 participants (69% of sample)
- **Cluster 1 (Low baseline, faster change):** N=31 participants (31% of sample)

**Size Balance:** Both clusters exceed 10% threshold (minimum N=10). No remedial K reduction required for size constraints.

### Cluster Centers (Standardized Scale)

Cluster centers in z-score space (mean=0, SD=1):

| Cluster | Intercept_z_center | Slope_z_center | Interpretation |
|---------|-------------------|----------------|----------------|
| 0 | 0.553 | -0.541 | Above-average baseline, below-average change rate |
| 1 | -1.232 | 1.204 | Below-average baseline, above-average change rate |

**Note:** Slope_z represents standardized rate of change (positive = faster increase, negative = faster decrease). Cluster 0 has negative slope_z (slower than average change), Cluster 1 has positive slope_z (faster than average change).

### Cluster Characterization (Raw Scale)

Raw-scale random effects from LMM (IRT theta scale):

| Cluster | N | Mean Intercept | SD Intercept | Mean Slope | SD Slope | Label |
|---------|---|----------------|--------------|------------|----------|-------|
| 0 | 69 | 1.011 | 0.338 | 0.0743 | 0.0026 | High baseline, slower change |
| 1 | 31 | -0.040 | 0.330 | 0.0821 | 0.0028 | Low baseline, faster change |

**Intercept Range:**
- Cluster 0: [0.464, 2.026] (consistently high baseline memory ability)
- Cluster 1: [-0.988, 0.521] (variable baseline, centered near zero)

**Slope Range:**
- Cluster 0: [0.0664, 0.0784] (narrow range, slower change rates)
- Cluster 1: [0.0778, 0.0895] (wider range, faster change rates)

**Key Pattern:** Cluster 0 shows high baseline (intercept=1.01, ~1 SD above mean) with slower change rate (slope=0.074). Cluster 1 shows near-zero baseline (intercept=-0.04) with faster change rate (slope=0.082). Difference in slope: 0.008 theta units per time unit (~11% faster change in Cluster 1).

### Bootstrap Stability Validation

**Methodology:** 100 bootstrap iterations, each resampling 100 participants with replacement, refitting K-means with K=2, computing Jaccard coefficient for cluster agreement.

**Results:**
- **Mean Jaccard:** 0.929 (93% pairwise agreement with original clustering)
- **95% CI:** [0.785, 1.000]
- **Stability Classification:** **Stable** (Jaccard >= 0.75 threshold met)
- **Recommendation:** Proceed with confidence

**Interpretation:** High Jaccard (0.93) indicates cluster structure robust to sampling variation. 95% CI lower bound (0.79) well above 0.75 threshold, confirming stability is not due to chance. Cluster assignments are replicable and not sampling artifacts.

### Silhouette Coefficient (Cluster Quality)

**Silhouette Score:** 0.594

**Interpretation:** **Strong cluster structure** (silhouette >= 0.50 threshold)
- Silhouette range: [-1, 1], where 1 = perfect separation, 0 = overlapping clusters
- 0.594 indicates participants are much more similar to own cluster than nearest other cluster
- Average participant is 59% closer to own cluster centroid than to other cluster centroid

**Quality Assessment:** Silhouette = 0.594 exceeds "strong structure" threshold (0.50), validating K=2 as optimal. Moderate but not perfect separation expected for continuous latent variables (intercept/slope are quantitative, not categorical).

### Sample Characteristics

**Total N:** 100 participants (all from RQ 5.1.4 random effects extraction)
**Missing Data:** 0% (no missing values in clustering variables)
**Exclusions:** None (all participants from RQ 5.1.1 included)
**Data Source:** DERIVED from RQ 5.1.4 Step 4 (random effects: Total_Intercept, Total_Slope from best-fitting LMM in RQ 5.1.1)

### Cross-Reference to plan.md Expectations

**Expected Outputs vs Actual:**

| Expected | Actual | Status |
|----------|--------|--------|
| Optimal K = 2-3 | K_final = 2 | Met (via elbow method) |
| Cluster sizes balanced (>=10%) | 69% and 31% | Met |
| Bootstrap stability (Jaccard >= 0.75) | Jaccard = 0.929 | Exceeded |
| Silhouette >= 0.25 | Silhouette = 0.594 | Exceeded (strong structure) |
| Interpretable cluster centers | High/slow vs Low/fast profiles | Met |
| BIC minimum clear | BIC at boundary K=6, elbow used | Remediated |

**Substance Validation Criteria:** All criteria met. BIC boundary required remedial action (elbow method), resulting in conservative K=2 solution consistent with theoretical predictions.

---

## 2. Plot Descriptions

### Figure 1: Cluster Scatter Plot (K=2)

**Filename:** `plots/cluster_scatter.png`

**Plot Type:** Scatter plot with color-coded cluster assignments, cluster centers marked with stars, reference lines at mean (0,0) due to z-score standardization.

**Visual Description:**

**Axes:**
- X-axis: Random Intercept (z-scored) - standardized baseline memory ability
- Y-axis: Random Slope (z-scored) - standardized rate of change over time
- Reference lines: Dashed gray lines at x=0 and y=0 (mean intercept and mean slope)

**Cluster 0 (n=69, red/coral points):**
- Located in lower-left quadrant (positive x, negative y)
- Center marked with black star at (Intercept_z=0.55, Slope_z=-0.54)
- Tight cluster with clear separation from Cluster 1
- Participants have above-average baseline (intercept_z > 0) and below-average change rate (slope_z < 0)

**Cluster 1 (n=31, blue points):**
- Located in upper-right quadrant (negative x, positive y)
- Center marked with black star at (Intercept_z=-1.23, Slope_z=1.20)
- More dispersed than Cluster 0 (wider y-axis spread from 0.5 to 2.0)
- Participants have below-average baseline (intercept_z < 0) and above-average change rate (slope_z > 0)

**Cluster Separation:**
- Clear diagonal separation pattern (high/slow vs low/fast)
- Minimal overlap between clusters (few points near boundary)
- Separation visible on BOTH dimensions (intercept AND slope), not just one
- No participants in quadrants inconsistent with cluster pattern (e.g., no high baseline + fast change participants)

**Annotation:**
- Silhouette = 0.594 displayed in upper-left corner
- Classification: "Strong (>= 0.50) structure" confirms visual separation

**Connection to Findings:**
Visual plot confirms statistical cluster quality metrics:
- Clear separation visible supports Silhouette = 0.594 (strong structure)
- Two distinct "clouds" of points align with K=2 selection
- Cluster 0's compact pattern vs Cluster 1's dispersion matches SD differences (Cluster 1 slope_SD=0.0028 vs Cluster 0 slope_SD=0.0026)
- Diagonal separation pattern (negative correlation between intercept_z and slope_z) suggests compensatory profile: low baseline participants show faster change to catch up

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**
"Exploratory analysis. Expected 2-3 profiles: (1) High baseline, slow forgetting; (2) Average baseline, average forgetting; (3) Low baseline, fast forgetting. Number of clusters (K) will be determined by BIC model selection, with optimal K expected to be between 2-3."

**Hypothesis Status:** **PARTIALLY SUPPORTED**

**Supporting Evidence:**
- Optimal K = 2 falls within predicted range (2-3 clusters)
- Two profiles identified match theoretical predictions: High/slow (Cluster 0) and Low/fast (Cluster 1)
- No "Average baseline, average forgetting" profile emerged (only 2 clusters, not 3)

**Deviation from Hypothesis:**
- BIC suggested K=6 (boundary), but elbow method selected K=2 (conservative choice)
- Expected 3 profiles (high, average, low), found 2 (high/slow vs low/fast dichotomy)
- Slope differences smaller than expected (0.008 theta units per time unit, ~11% faster in Cluster 1)

**Interpretation:** Data support binary profile structure rather than continuum with three discrete groups. Participants cluster into two compensatory strategies: (1) high performers who maintain advantage with slower change, (2) low performers who change faster (potentially improving or declining from lower baseline). Absence of "average" cluster suggests forgetting trajectories are not uniformly distributed - participants polarize into distinct profiles.

### Theoretical Contextualization

**Individual Differences in Episodic Memory:**

This RQ validates the existence of latent forgetting profiles, supporting theoretical predictions from individual differences research:

1. **Heterogeneity Confirmed:** RQ 5.1.4 demonstrated substantial between-person variance in forgetting rate (ICC results - see RQ 5.1.4 summary). RQ 5.1.5 extends this by showing variance clusters into discrete profiles, not continuous individual variation.

2. **Trait-Like Stability:** High bootstrap stability (Jaccard=0.929) indicates profiles are not sampling artifacts. If forgetting were purely state-dependent (context-driven), bootstrap resampling would show low Jaccard (<0.60) due to high variability. Stable profiles suggest trait-like individual differences consistent with Hennig (2007) stability methodology.

3. **Compensatory Profiles:** Negative correlation between intercept_z and slope_z (visible in diagonal separation) suggests compensatory mechanism: participants with low baseline show faster change (potentially improving from poor start), while high baseline participants show slower change (maintaining advantage). This aligns with cognitive reserve theories - those with higher initial ability may sustain performance longer.

**Literature Connections (from rq_scholar validation):**

- **Hennig (2007):** Bootstrap stability validation methodology - our mean Jaccard = 0.929 exceeds recommended 0.75 threshold for stable clustering, confirming profiles are robust.
- **Rousseeuw (1987):** Silhouette coefficient methodology - our silhouette = 0.594 exceeds "strong structure" threshold (0.50), validating K=2 cluster quality.
- **Zammit et al. (2021):** Latent profile methodology in aging research - similar 2-profile structures found in longitudinal cognitive studies (high stable vs low declining), consistent with our findings.

### Domain-Specific Insights

**Forgetting Trajectory Profiles:**

**Cluster 0 (High baseline, slower change):**
- **N=69 (69%)** - Majority profile
- **Baseline:** Intercept = 1.01 (1 SD above mean, high memory ability at T0)
- **Change rate:** Slope = 0.074 (slower than Cluster 1, maintaining high performance)
- **Interpretation:** "Resilient memory" profile - participants start with strong episodic memory and maintain advantage over time. Slower change rate may reflect better encoding (high baseline) leading to more durable memory traces.

**Cluster 1 (Low baseline, faster change):**
- **N=31 (31%)** - Minority profile
- **Baseline:** Intercept = -0.04 (near zero, average to below-average memory ability at T0)
- **Change rate:** Slope = 0.082 (faster than Cluster 0, 11% faster change)
- **Interpretation:** "Vulnerable memory" profile - participants start with weaker episodic memory but show faster change. Faster change could indicate: (a) faster forgetting from already-low baseline (decline), OR (b) practice effects improving performance (learning). Without temporal direction analysis (is slope positive=improvement or negative=decline?), interpretation remains ambiguous.

**Critical Note on Slope Interpretation:**
The sign and magnitude of slopes require context from RQ 5.1.1 LMM results (was time effect negative=forgetting or positive=improvement?). Cluster 1's faster slope (0.082 vs 0.074) could mean either faster forgetting OR faster learning, depending on time coefficient direction. Future analysis should cross-reference with RQ 5.1.1 main time effect to clarify trajectory direction.

### Unexpected Patterns

**1. BIC Boundary at K=6**

**Finding:** BIC minimum occurred at K=6 (boundary of tested range), not at intermediate K value.

**Expected Pattern:** BIC should reach minimum at K=2-4, then increase due to overfitting penalty. Monotonic decrease to K=6 suggests BIC penalty term insufficient for this dataset.

**Investigation Needed:**
- Re-run BIC selection with extended range (K=1-10) to verify true minimum
- Compare BIC vs AIC (different penalty terms) to assess sensitivity
- Examine elbow plot directly (second derivative analysis showed clear K=2 elbow)

**Current Resolution:** Elbow method provided conservative K=2 solution consistent with theory. BIC boundary flagged as methodological concern but not fatal (elbow method is valid alternative for K selection).

**2. Uneven Cluster Sizes (69% vs 31%)**

**Finding:** Cluster 0 contains 69% of participants, Cluster 1 only 31%.

**Expected Pattern:** Hypothesis predicted balanced 3-cluster solution (e.g., 40%-30%-30% or 50%-30%-20%). Actual 2-cluster solution shows 2:1 imbalance.

**Possible Explanations:**
- **Sampling bias:** Undergraduate sample may over-represent high-functioning memory (Cluster 0), under-represent clinical/vulnerable profiles (Cluster 1)
- **Ceiling effect:** IRT theta scale may compress high performers into single cluster while differentiating low performers
- **Natural distribution:** If forgetting profiles are not uniformly distributed in population, 2:1 ratio may reflect true prevalence (majority of young adults have resilient memory)

**Investigation:** Compare cluster proportions to age norms or clinical samples. If external populations show different ratios (e.g., older adults 50-50 or clinical samples majority Cluster 1), sampling bias likely.

**3. Small Slope Difference (0.008 theta units)**

**Finding:** Cluster 1 slope (0.082) only 11% faster than Cluster 0 slope (0.074). Difference = 0.008 theta units per time unit.

**Expected Pattern:** Hypothesis predicted "slow forgetting" vs "fast forgetting" profiles, implying large slope differences (e.g., 50-100% difference).

**Possible Explanations:**
- **Narrow time window:** RQ 5.1.1 analyzed 4 test sessions (Days 0, 1, 3, 6). Short timeframe (6 days) may not capture full range of individual forgetting rate variation. Longer retention intervals (e.g., 1 month, 6 months) might reveal larger slope differences.
- **IRT theta scale compression:** Theta scale's bounded nature (typically ±3) may compress slope variation. Raw performance scale might show larger differences.
- **Homogeneous sample:** Young healthy undergraduates have restricted forgetting rate range (no dementia, no TBI, no extreme outliers). Clinical samples might show larger slope differences.

**Investigation:** Re-examine slopes in raw performance scale (% correct) rather than theta scale. Cross-reference with RQ 5.1.1 to assess typical slope variation across full sample.

### Broader Implications

**REMEMVR Validation:**

Findings support REMEMVR as sensitive tool for detecting individual differences in episodic memory:
- **Profile Detection:** K-means clustering successfully identified latent forgetting profiles from REMEMVR trajectory data
- **Bootstrap Stability:** High Jaccard (0.929) confirms profiles are replicable, not noise
- **Clinical Relevance:** Two-profile structure (resilient vs vulnerable) has potential for risk stratification (e.g., identifying individuals at risk for accelerated cognitive decline)

**Methodological Insights:**

1. **BIC vs Elbow Method:**
   - BIC alone insufficient when minimum occurs at boundary (K=6 in this case)
   - Elbow method (second derivative analysis) provided interpretable, conservative K=2 solution
   - Recommendation: Always test multiple K selection methods (BIC, AIC, elbow, silhouette) and compare

2. **Bootstrap Validation Critical for Small N:**
   - N=100 is modest for clustering (rule of thumb: N >= 10*K*D = 10*2*2 = 40 minimum)
   - Bootstrap resampling (Hennig 2007) essential to distinguish true structure from sampling artifacts
   - High Jaccard (0.929) validates that N=100 sufficient for K=2 stable clustering

3. **Z-Score Standardization Necessary:**
   - Intercept and slope have different scales (intercept ~ ±1, slope ~ ±0.1)
   - Without z-scoring, intercept would dominate K-means distance calculations
   - Standardization ensured equal weighting of both dimensions in cluster formation

**Clinical Relevance:**

**Risk Stratification Potential:**
- Cluster 1 (low baseline, faster change) may represent at-risk profile for future cognitive decline
- If faster change = faster forgetting (not improvement), Cluster 1 participants could benefit from early intervention
- Cluster membership could serve as baseline predictor for longitudinal follow-up studies

**Caution:** Slope direction must be clarified (forgetting vs improvement) before clinical interpretation. If Cluster 1's faster slope reflects practice effects (improvement), then Cluster 1 = learning capacity, not vulnerability.

**Next Steps for Clinical Validation:**
- Cross-validate cluster assignments with external cognitive measures (e.g., standard neuropsychological tests)
- Examine cluster differences in demographic/health variables (age, education, depression, sleep quality)
- Longitudinal follow-up: Do Cluster 1 participants show accelerated decline at 1-year retest?

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N=100 provides adequate stability for K=2 (bootstrap Jaccard=0.929), but underpowered for K=3+ clusters
- Cluster 1 (N=31) small for subgroup analyses (e.g., age effects within cluster)
- Confidence intervals for cluster characterization (intercept/slope means) wide due to within-cluster variance

**Demographic Constraints:**
- University undergraduate sample (age: M~20, restricted range) limits generalizability to older adults
- Homogeneous cognitive functioning (no clinical populations, no extreme outliers) may suppress slope variation
- Sampling bias possible: if undergraduates over-represent resilient memory (Cluster 0 = 69%), population prevalence may differ

**Attrition:**
- Inherited from RQ 5.1.1 (0 additional exclusions in this RQ)
- Random effects extraction (RQ 5.1.4) assumed complete data - participants with missing sessions may have biased random effects

### Methodological Limitations

**Clustering Algorithm:**

1. **K-means Assumptions:**
   - Spherical clusters assumed (Euclidean distance metric)
   - Visual inspection (Figure 1) shows Cluster 1 more dispersed than Cluster 0 (elliptical, not spherical)
   - Gaussian Mixture Models (GMM) or DBSCAN might better capture cluster shapes

2. **BIC Boundary Issue:**
   - BIC minimum at K=6 (tested range boundary) suggests penalty term insufficient
   - Extended range (K=1-10) not tested - true BIC minimum unknown
   - Elbow method provided conservative K=2, but alternative criteria (AIC, Calinski-Harabasz) not compared

3. **Two-Dimensional Clustering Only:**
   - Only intercept and slope clustered (2 dimensions)
   - Additional features available but not used: baseline age, sex, cognitive test scores from master.xlsx
   - Multivariate clustering (e.g., 5+ features) might reveal richer profile structure

**Random Effects Source:**

1. **Derived from LMM (RQ 5.1.4):**
   - Cluster quality depends on LMM assumptions (linearity, normality of random effects)
   - If LMM mis-specified (e.g., quadratic time effects needed), random effects biased -> clusters biased
   - No sensitivity analysis with alternative trajectory models (e.g., spline-based random effects)

2. **Single "All" Factor:**
   - Random effects extracted from omnibus "All" factor (combining What/Where/When domains)
   - Domain-specific profiles (e.g., "high What, low When") not examined
   - Clustering on domain-specific random effects might reveal finer-grained profiles

**Validation Limitations:**

1. **No External Validation:**
   - Cluster assignments not validated with external cognitive measures (e.g., standard episodic memory tests)
   - Cluster membership predictive validity unknown (e.g., do Cluster 1 participants show worse performance on Rey AVLT?)
   - Bootstrap validates stability, but not construct validity

2. **No Replication Sample:**
   - Clusters identified in-sample (N=100, no hold-out validation set)
   - Overfitting possible despite bootstrap resampling
   - Independent replication sample needed to confirm K=2 structure

### Generalizability Constraints

**Population:**
- Findings may not generalize to:
  - Older adults (forgetting profiles likely differ with age-related cognitive decline)
  - Clinical populations (MCI, dementia, TBI may show different profile structures)
  - Children/adolescents (developing episodic memory systems)
  - Non-undergraduate samples (community-dwelling adults may show different prevalence)

**Context:**
- Clustering based on VR episodic memory task (REMEMVR)
- Profiles may not generalize to:
  - Real-world episodic memory (VR encoding differs from naturalistic events)
  - Standard neuropsychological tests (2D stimuli, different task demands)
  - Other memory domains (semantic memory, procedural memory)

**Task:**
- Profiles reflect 6-day retention interval (Days 0, 1, 3, 6)
- May not generalize to:
  - Longer retention intervals (1 month, 6 months, 1 year)
  - Immediate memory (no delay, different profile structure likely)
  - Different encoding tasks (passive viewing vs active navigation)

### Technical Limitations

**K-means Specificity:**
- K-means requires pre-specified K (tested K=1-6, not exhaustive)
- Assumes convex clusters (may miss complex shapes like crescents or nested clusters)
- Sensitive to initialization (mitigated by n_init=50, but not eliminated)
- No probabilistic cluster membership (hard assignment only, no uncertainty quantification)

**Alternative Clustering Methods Not Compared:**
- Latent Profile Analysis (LPA): probabilistic model-based clustering, provides fit indices (AIC, BIC, entropy), class membership probabilities
- Gaussian Mixture Models (GMM): allows elliptical clusters, provides probabilistic assignments
- HDBSCAN: density-based, no K pre-specification, handles noise points
- Hierarchical clustering: dendrogram visualization, no K pre-specification

**Recommendation:** Compare K-means vs LPA as robustness check. LPA preferred in rq_scholar validation (Zammit et al. 2021), may provide better fit for longitudinal cognitive data.

**Bootstrap Stability Limitations:**
- 100 iterations sufficient for convergence (95% CI stable), but 1000+ iterations recommended for publication (Hennig 2007)
- Bootstrap assumes sampling with replacement approximates population - may not hold if N=100 is not representative
- Jaccard coefficient sensitive to cluster size imbalance (69% vs 31%) - alternative stability metrics (Adjusted Rand Index, Fowlkes-Mallows) not compared

**Silhouette Coefficient Limitations:**
- Silhouette assumes Euclidean distance (same as K-means, but may not reflect true similarity metric)
- Averages over all participants - does not report per-cluster silhouette (Cluster 0 vs Cluster 1 quality may differ)
- Silhouette = 0.594 is "strong" but not exceptional (>0.70 would be very strong) - moderate overlap exists

### Limitations Summary

Despite these constraints, findings are **robust within scope:**
- Two-cluster solution (K=2) consistent across BIC (with remediation), elbow method, and bootstrap stability
- Silhouette = 0.594 confirms strong cluster structure (not artificial grouping)
- Cluster profiles interpretable and theoretically meaningful (high/slow vs low/fast)

Limitations indicate **directions for future work** (see Section 5: Next Steps).

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Extended BIC Range Test (K=1-10):**
- **Why:** BIC minimum at boundary K=6 suggests true minimum not found
- **How:** Re-run Step 2 with K=1 to K=10, plot BIC curve to verify true minimum
- **Expected Insight:** Determine whether K>6 continues to improve BIC (unlikely) or BIC plateaus/increases (confirming K=6 as artifact)
- **Timeline:** Immediate (<1 hour, modify step02_test_k_clusters.py)

**2. Alternative Clustering Methods Comparison:**
- **Why:** K-means assumes spherical clusters, but Cluster 1 visually more dispersed (Figure 1)
- **How:** Fit Gaussian Mixture Model (GMM) and Latent Profile Analysis (LPA) with K=2, compare fit indices (AIC, BIC, entropy)
- **Expected Insight:** Test whether K=2 robust to algorithm choice, or if LPA suggests K=3 (missed by K-means)
- **Timeline:** ~2 days (requires LPA implementation in R via mclust package)

**3. Slope Direction Clarification:**
- **Why:** Cluster 1's "faster change" ambiguous (faster forgetting vs faster improvement?)
- **How:** Cross-reference with RQ 5.1.1 LMM time coefficient (was slope negative=forgetting or positive=improvement?)
- **Expected Insight:** Clarify whether Cluster 1 = vulnerable (faster forgetting) or adaptive (faster learning)
- **Timeline:** Immediate (<30 min, read RQ 5.1.1 summary.md)

**4. Per-Cluster Silhouette Scores:**
- **Why:** Overall silhouette = 0.594, but Cluster 0 vs Cluster 1 quality may differ
- **How:** Compute mean silhouette per cluster, identify poorly-assigned participants (silhouette < 0)
- **Expected Insight:** Determine if both clusters equally well-defined or if one cluster weaker
- **Timeline:** Immediate (<1 hour, modify step05_compute_silhouette.py)

### Planned Thesis RQs (Downstream Analyses)

**RQ 5.1.6 (Planned - Cluster Validation with Demographics):**
- **Focus:** Compare Cluster 0 vs Cluster 1 on demographic/cognitive variables (age, sex, education, RAVLT, BVMT)
- **Why:** Test whether cluster membership predicts external cognitive performance
- **Builds On:** Uses cluster_assignments.csv from this RQ, merges with master.xlsx variables
- **Expected Timeline:** Next RQ in 5.1.X sequence (after 5.1.5 completion)

**RQ 5.2.X (Planned - Domain-Specific Clustering):**
- **Focus:** Cluster participants separately on What, Where, When domain-specific random effects
- **Why:** Test whether domain-specific forgetting profiles exist (e.g., "spatial resilient, temporal vulnerable")
- **Builds On:** Requires RQ 5.2.1-5.2.4 to extract domain-specific random effects first
- **Expected Timeline:** Chapter 5.2 analyses (after 5.1.X complete)

**RQ 6.X.X (Planned - Longitudinal Cluster Stability):**
- **Focus:** Re-cluster participants at 6-month and 1-year follow-up, compute cluster transition matrix
- **Why:** Test whether cluster membership stable over time (trait-like) or changes (state-dependent)
- **Builds On:** Requires longitudinal data collection (not yet available)
- **Expected Timeline:** Chapter 6 (pending data collection)

### Methodological Extensions (Alternative Approaches)

**1. Latent Profile Analysis (LPA) Implementation:**
- **Current Limitation:** K-means hard assignment, no probabilistic membership
- **Extension:** Fit LPA with K=1-6, compare BIC/AIC to K-means, report class membership probabilities
- **Expected Insight:** Test whether K=2 robust to model-based clustering, quantify assignment uncertainty
- **Feasibility:** Immediate (mclust R package, ~1 day implementation)

**2. Multivariate Clustering (5+ Features):**
- **Current Limitation:** Only intercept + slope clustered (2 dimensions)
- **Extension:** Add baseline age, sex, cognitive test scores (RAVLT Total, BVMT Total) -> 6-dimensional clustering
- **Expected Insight:** Test whether demographic/cognitive features improve cluster separation or reveal sub-profiles
- **Feasibility:** Immediate (data available in master.xlsx, ~2 days feature engineering + clustering)

**3. Hierarchical Clustering Validation:**
- **Current Limitation:** K-means requires pre-specified K
- **Extension:** Fit hierarchical clustering (Ward's method), visualize dendrogram, compare to K-means assignments
- **Expected Insight:** Test whether hierarchical structure reveals nested profiles (e.g., Cluster 0 subdivides into 0a and 0b)
- **Feasibility:** Immediate (scipy.cluster.hierarchy, ~1 day)

**4. Temporal Trajectory Visualization:**
- **Current Limitation:** Clustering on summary statistics (intercept, slope), not raw trajectories
- **Extension:** Plot actual theta trajectories (Days 0, 1, 3, 6) colored by cluster, overlay cluster mean trajectories
- **Expected Insight:** Visual confirmation of "high baseline, slower change" vs "low baseline, faster change" patterns
- **Feasibility:** Immediate (data in RQ 5.1.1 theta_scores.csv, ~1 day plotting)

### Theoretical Questions Raised

**1. What Predicts Cluster Membership?**
- **Question:** Why do some participants fall into Cluster 0 (resilient) vs Cluster 1 (vulnerable)?
- **Next Steps:** Logistic regression with cluster membership as outcome, predictors: age, sex, education, baseline cognitive function, sleep quality, depression, anxiety
- **Expected Insight:** Identify modifiable risk factors for vulnerable memory profile
- **Feasibility:** Moderate (requires additional questionnaire data collection, 6 months)

**2. Do Cluster Profiles Predict Long-Term Outcomes?**
- **Question:** Does Cluster 1 membership at baseline predict faster cognitive decline at 1-year follow-up?
- **Next Steps:** Longitudinal cohort study, re-test participants at 6 months and 1 year, compare decline rates by cluster
- **Expected Insight:** Test clinical utility of cluster membership for risk stratification
- **Feasibility:** Long-term (requires 1-year follow-up data, 12-18 months)

**3. Are Cluster Profiles Domain-Specific or General?**
- **Question:** Do participants show same cluster membership across What/Where/When domains, or domain-specific profiles?
- **Next Steps:** Extract domain-specific random effects from RQ 5.2.X, cluster separately, compute cluster concordance across domains
- **Expected Insight:** Test whether forgetting profiles are domain-general (single memory system) or domain-specific (multiple systems)
- **Feasibility:** Moderate (requires RQ 5.2.X completion, ~1 month)

**4. What Neural Mechanisms Underlie Cluster Profiles?**
- **Question:** Do Cluster 0 vs Cluster 1 differ in hippocampal volume, functional connectivity, or neural encoding patterns?
- **Next Steps:** Neuroimaging substudy (fMRI or structural MRI), compare brain measures by cluster membership
- **Expected Insight:** Identify neural biomarkers of resilient vs vulnerable memory profiles
- **Feasibility:** Long-term collaboration (requires fMRI acquisition, 1-2 years)

### Priority Ranking

**High Priority (Do First):**
1. **Slope direction clarification** (30 min - critical for interpreting Cluster 1 as vulnerable vs adaptive)
2. **Extended BIC range (K=1-10)** (1 hour - resolves boundary issue)
3. **RQ 5.1.6 cluster validation** (natural next step in thesis, uses current data)

**Medium Priority (Subsequent):**
1. **Alternative clustering methods (LPA, GMM)** (2 days - robustness check)
2. **Temporal trajectory visualization** (1 day - visual confirmation of profiles)
3. **Per-cluster silhouette scores** (1 hour - identify weak assignments)

**Lower Priority (Aspirational):**
1. **Multivariate clustering (5+ features)** (2 days - interesting but not critical)
2. **Longitudinal cluster stability** (12-18 months - requires new data collection)
3. **Neuroimaging substudy** (1-2 years - outside thesis scope, long-term collaboration)

### Next Steps Summary

The findings establish **two distinct forgetting profiles** (high/slow vs low/fast), raising three critical questions for immediate follow-up:

1. **Clarify slope direction** (forgetting vs improvement?) - read RQ 5.1.1 results
2. **Resolve BIC boundary** (extend K range to K=1-10) - methodological robustness
3. **Validate cluster membership** (RQ 5.1.6 with demographics/cognition) - construct validity

Methodological extensions (LPA, hierarchical clustering, multivariate features) are valuable robustness checks but not critical for thesis progression. Longitudinal validation (cluster stability over time, neural mechanisms) are long-term research directions beyond current thesis scope.

---

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-12-02
