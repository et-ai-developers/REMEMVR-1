# Results Summary: RQ 5.4.7 - Schema-Based Clustering

**Research Question:** Can participants be grouped into latent classes based on congruence-specific forgetting trajectories (intercepts and slopes for Common, Congruent, and Incongruent items)?

**Analysis Completed:** 2025-12-03

**Analyst:** rq_results agent (v4.0) with master claude orchestration

---

## 1. Statistical Findings

### Sample Characteristics

- Total N: 100 participants (from RQ 5.4.6 random effects)
- Clustering variables: 6 features (intercept and slope for Common, Congruent, Incongruent)
- Missing data: None (all participants had complete random effects from RQ 5.4.6)
- Data source: DERIVED from RQ 5.4.6 congruence-specific LMM random effects

### Cluster Model Selection (BIC)

**K-means tested for K=1 to K=6:**

| K | Inertia | BIC |
|---|---------|-----|
| 1 | 600.00 | 183.78 |
| 2 | 264.14 | 106.34 |
| 3 | 189.34 | 77.65 |
| 4 | 161.00 | 66.04 |
| 5 | 137.02 | 54.52 |
| 6 | 118.65 | **44.73** |

**Optimal K:** K=6 (BIC minimum = 44.73)

**BOUNDARY WARNING:** Optimal K at upper boundary (K=6) suggests model may benefit from testing K=7+ in sensitivity analysis. BIC monotonically decreasing indicates additional clusters might improve fit, but stopped at K=6 per plan specification.

### Final Clustering Solution (K=6)

**Cluster Sizes:**
- Cluster 0 (High): N=22 (22%)
- Cluster 1 (Low): N=17 (17%)
- Cluster 2 (Low): N=15 (15%)
- Cluster 3 (Medium): N=22 (22%)
- Cluster 4 (High): N=18 (18%)
- Cluster 5 (High): N=6 (6%)

**Note:** Cluster 5 below 10% guideline (N=6, 6% of sample), but within technical minimum for clustering. Small cluster size may limit interpretability.

### Cluster Quality Metrics

| Metric | Value | Threshold | Pass |
|--------|-------|-----------|------|
| Silhouette Score | 0.254 | >= 0.40 | **FAIL** |
| Davies-Bouldin Index | 1.088 | < 1.50 | PASS |
| Bootstrap Jaccard (mean) | 0.592 | > 0.75 | **FAIL** |
| Bootstrap Jaccard (median) | 0.586 | > 0.75 | **FAIL** |
| Bootstrap Jaccard (min) | 0.306 | > 0.75 | **FAIL** |

**CLUSTERING QUALITY:** WEAK

- **Silhouette = 0.254:** Below 0.40 threshold indicates weak cluster cohesion. Per template guidance: < 0.25 = no structure, 0.25-0.50 = weak structure. Result at boundary suggests minimal but detectable clustering structure.
- **Davies-Bouldin = 1.088:** PASSES < 1.50 threshold, indicates acceptable cluster separation despite weak cohesion.
- **Jaccard = 0.592:** Bootstrap stability FAILS > 0.75 threshold. Clusters are unstable across resampling (59% consistency). Suggests clustering solution may not replicate well in new samples.

### Cluster Profiles (Original Scale)

**Pattern:** All clusters differentiated primarily by INTERCEPTS (baseline memory ability), NOT slopes (forgetting rates).

**Inspection of random effects reveals:**
- Common_Slope range: [-0.00054 to 0.00041] (essentially zero)
- Congruent_Slope range: [-0.00040 to 0.00039] (essentially zero)
- Incongruent_Slope range: [-0.00034 to 0.00083] (essentially zero)

**Implication:** Consistent with RQ 5.4.6 finding of ICC_slope = 0.000 (zero between-participant variance in slopes). Clustering is ENTIRELY driven by baseline memory differences, NOT schema-specific trajectory patterns.

**Cluster Characterization (Intercepts Only):**
- **High clusters (C0, C4, C5):** Above-average baseline memory across all congruence levels
- **Medium cluster (C3):** Near-zero baseline memory (population average)
- **Low clusters (C1, C2):** Below-average baseline memory across all congruence levels

**No schema-selective patterns observed:** Clusters do NOT show differential congruence effects (e.g., no cluster with high Common but low Incongruent). All clusters show similar congruence ordering (Common ~ Congruent > Incongruent), just shifted up/down by overall ability.

### Cross-Reference to plan.md

**Outputs match expectations:** All 10 data files generated, 7 logs present, 3 plots created.

**Substance criteria:**
- Row counts: 100 participants (PASS)
- Column counts: 7-10 columns per file (PASS)
- Value ranges: Intercepts in [-0.56, 0.62] (PASS, scientifically reasonable theta scale)
- Cluster size constraint: 5/6 clusters >= 10%, 1 cluster = 6% (MARGINAL PASS)

**Expectation violations:**
- Optimal K at boundary (plan expected K in {2,3,4,5}, found K=6 at upper bound)
- Quality metrics FAIL (plan expected silhouette >= 0.40, Jaccard > 0.75)
- Zero slope variance (plan anticipated slope-based clustering, but slopes ~ 0)

---

## 2. Plot Descriptions

### Figure 1: BIC Model Selection Elbow Plot

**Filename:** plots/bic_elbow.png

**Plot Type:** Line plot with optimal K marker

**Visual Description:**

The BIC elbow plot shows monotonic decrease from K=1 (BIC=183.78) to K=6 (BIC=44.73). No clear "elbow" point where BIC flattens, indicating continuous improvement with increasing K. Optimal K=6 marked with red circle at right boundary.

**Key Pattern:**
- Steep decline K=1 to K=3 (BIC drops ~106 points)
- Gradual decline K=3 to K=6 (BIC drops ~33 points)
- No plateau observed, suggesting K=7+ might improve fit further

**Connection to Findings:**
Boundary selection (K=6) confirms BIC table finding. Visual lack of elbow supports BOUNDARY WARNING in Section 1 - model selection stopped at arbitrary upper bound, not at clear optimum. This is a methodological concern flagged for investigation.

---

### Figure 2: Cluster Profiles by Schema Congruence

**Filename:** plots/cluster_profiles.png

**Plot Type:** Grouped bar chart (baseline memory intercepts only)

**Visual Description:**

Bar chart shows cluster center intercepts for Common, Congruent, and Incongruent items (original theta scale). Six clusters color-coded: C0/C4/C5 (High, blue/purple/brown), C3 (Medium, red), C1/C2 (Low, orange/green).

**Subtitle note:** "(Baseline Memory Performance)" with clarification "Slopes H 0" - indicates plot shows intercepts only because slopes have zero variance.

**Key Patterns:**
1. **Vertical stratification:** Clusters differ in overall height (baseline ability), not congruence-specific patterns
2. **Similar congruence ordering:** All clusters show Common ~ Congruent (near-identical), both higher than Incongruent
3. **High clusters (C0/C4/C5):** Intercepts +0.18 to +0.62 (above average)
4. **Medium cluster (C3):** Intercepts near 0 (population average)
5. **Low clusters (C1/C2):** Intercepts -0.22 to -0.54 (below average)
6. **No schema-selective patterns:** No cluster shows high Common but low Incongruent, or vice versa

**Missing Slope Information:**
Plot subtitle explicitly notes "Slopes H 0" - slope bars not shown because all slope random effects are effectively zero (consistent with RQ 5.4.6 ICC_slope = 0.000). Clustering based on 6 features (3 intercepts + 3 near-zero slopes) reduces to 3-feature clustering (intercepts only).

**Connection to Findings:**
Visually confirms statistical finding that clustering reflects BASELINE MEMORY DIFFERENCES, not schema-specific trajectory heterogeneity. The hoped-for schema-selective profiles (Hypothesis: "poor memory for incongruent only" or "strong schema benefit") are NOT observed. Clusters simply represent high/medium/low overall memory ability.

---

### Figure 3: Cluster Scatter Matrix (6-Dimensional)

**Filename:** plots/cluster_scatter_matrix.png

**Plot Type:** 3x3 scatter matrix (intercepts only, slopes excluded due to zero variance)

**Subtitle:** "(Baseline Intercepts Only - Slopes H 0)"

**Visual Description:**

Matrix shows all pairwise scatter plots for Common, Congruent, and Incongruent intercepts (z-scored). Points colored by cluster membership (6 colors), cluster centroids marked with crosshatch pattern. Diagonal shows frequency histograms by cluster.

**Axes:** All axes labeled with "(z)" indicating standardized scale (mean=0, SD=1).

**Key Patterns:**
1. **High overlap:** Clusters overlap substantially in most panels - NOT cleanly separated spheres
2. **Diagonal histograms:** Multimodal distributions visible (peaks for high/medium/low clusters)
3. **Centroid positions:** Centroids (crosshatch markers) separated along main diagonal (overall ability dimension)
4. **Weak separation:** No single panel shows clear cluster separation - points intermingle across all pairwise combinations
5. **Sphericity assumption:** Clusters appear approximately spherical (no severe elongation), validating K-means assumption

**Specific Panel Observations:**
- **Common vs Congruent:** Strong positive correlation (points align along diagonal), clusters differentiated vertically (ability level)
- **Common vs Incongruent:** Moderate positive correlation, slightly more scatter than Common-Congruent
- **Congruent vs Incongruent:** Similar to Common-Incongruent, moderate correlation

**Connection to Findings:**
Visual overlap confirms WEAK CLUSTERING QUALITY (silhouette=0.254, Jaccard=0.592). Clusters are not distinct groups but rather gradations along a single "overall memory ability" continuum. Lack of clear separation explains bootstrap instability (clusters shift membership across resampling iterations). This visualization makes the NULL-ish finding tangible: schema-based individual differences do NOT form discrete profiles.

---

## 3. Interpretation

### Hypothesis Testing

**Original Hypothesis (from 1_concept.md):**

Exploratory analysis expected 2-4 latent profiles with possible schema-selective patterns such as:
- Poor memory for schema-violating items only (low Incongruent, preserved Common/Congruent)
- Strong vs weak schema benefit (large vs small congruence differences)
- Uniform high/medium/low profiles differentiated by overall ability

**Hypothesis Status:** **PARTIALLY SUPPORTED (Uniform Profiles Only)**

The K-means analysis identified 6 clusters (more than expected 2-4), but these clusters reflect:
- **Uniform profiles ONLY:** Differentiated by overall memory ability (high/medium/low), NOT schema-selective patterns
- **No schema-selective patterns:** Expected patterns (poor Incongruent only, strong schema benefit clusters) NOT observed
- **Intercept-driven clustering:** All differentiation based on baseline memory, zero slope heterogeneity

**Critical finding:** The absence of schema-selective profiles is itself a meaningful result. It suggests schema congruence effects are HOMOGENEOUS across individuals (everyone shows similar Common > Congruent > Incongruent ordering), rather than heterogeneous (some individuals sensitive to schema, others not).

### Theoretical Contextualization

**Schema Theory Interpretation:**

The clustering results have important implications for schema theory in episodic memory:

1. **Universal schema effects:** The lack of schema-selective clusters suggests schema congruence influences memory UNIFORMLY across individuals. This contradicts predictions from schema theory that individuals vary in their ability to utilize schema-based encoding support. Instead, findings suggest schema effects are a fundamental property of episodic memory architecture, not a strategic skill varying across individuals.

2. **Individual differences in LEVEL, not PATTERN:** Participants differ in overall memory ability (high/medium/low clusters), but show similar RELATIVE congruence effects. A high-ability individual remembers more items overall, but shows the same Congruent > Incongruent advantage as a low-ability individual. This dissociates memory capacity from schema sensitivity.

3. **Consistency with RQ 5.4.6 findings:** The zero slope variance (ICC_slope = 0.000 from RQ 5.4.6) pre-determined this outcome. If all participants have identical forgetting rates (slopes ~ 0), clustering based on slopes CANNOT reveal trajectory heterogeneity. The weak clustering quality reflects this fundamental limitation: we asked "do forgetting trajectories differ?" when trajectories don't exist (no decline over time).

**Literature Connections (from rq_scholar validation):**

The rq_scholar context_dump notes "Schema theory + methodology sound" but does not provide specific citations for schema-based individual differences. The NULL finding (no schema-selective clusters) may reflect:
- **Measurement limitation:** 4 test sessions (Day 0,1,3,6) insufficient to capture individual trajectory differences
- **VR paradigm specificity:** Schema effects in immersive VR may be so strong that individual differences are compressed (ceiling effects for all participants)
- **True population homogeneity:** Schema congruence may genuinely affect everyone similarly

### Unexpected Patterns

**1. K=6 at Boundary (Expected K=2-4):**

BIC selected K=6, the maximum tested. Visual inspection of BIC elbow plot shows no plateau - BIC continues declining through K=6. This suggests:
- **Insufficient K range:** Testing K=7, K=8, K=9 might reveal true optimum
- **Overfitting risk:** K=6 may partition noise rather than meaningful structure (supported by weak quality metrics)
- **Recommendation:** Sensitivity analysis testing K=7-10 needed to confirm K=6 is true optimum or artifact of search range

**2. Weak Clustering Quality (Multiple Metrics Fail):**

Silhouette=0.254 and Jaccard=0.592 both fail thresholds. This dual failure indicates:
- **Poor cohesion:** Points within clusters are not tightly grouped (silhouette)
- **Instability:** Cluster assignments shift across bootstrap resampling (Jaccard)
- **Interpretation:** Clusters are TENTATIVE patterns, not robust profiles

Per concept.md guidance: "If cluster quality fails, interpret as continuously distributed individual differences rather than discrete clusters." This is the appropriate interpretation here.

**3. Zero Slope Variance (Slopes H 0):**

All slope random effects are near-zero (range: -0.00054 to +0.00083). This was anticipated from RQ 5.4.6 (ICC_slope=0.000), but has profound implications:
- **6 features reduce to 3:** Clustering specified 6 features (3 intercepts + 3 slopes), but slopes contribute no information
- **Trajectory clustering impossible:** Cannot cluster by "forgetting trajectory" when no participant shows forgetting (slopes = 0)
- **Theoretical puzzle:** Why is there zero between-participant variance in forgetting rates? Suggests forgetting rate is a FIXED parameter, not an individual difference trait

This finding deserves follow-up investigation (see Section 5).

**4. Cluster 5 Small Size (N=6, 6%):**

One cluster falls below 10% guideline. This may represent:
- **Outlier cluster:** 6 participants with extreme baseline memory (very high intercepts)
- **Overfitting artifact:** K=6 solution creates small cluster to fit noise
- **Validation concern:** Bootstrap instability may be driven by small cluster instability

### Broader Implications

**REMEMVR Validation:**

Findings have mixed implications for REMEMVR as an assessment tool:

- **Positive:** Individual differences in BASELINE memory ability are detectable (high/medium/low clusters). REMEMVR can stratify participants by overall performance.
- **Negative:** No individual differences in FORGETTING RATES (slopes = 0). REMEMVR does NOT detect trajectory heterogeneity over 6-day retention interval.
- **Schema congruence:** Congruence effects are homogeneous (no schema-selective profiles). This limits clinical utility if goal was to identify individuals with schema-specific impairments.

**Methodological Insights:**

1. **K-means limitations for weak structure:** K-means WILL produce clusters even when true structure is weak or absent. Quality metrics (silhouette, Jaccard) are essential to avoid over-interpreting noise.

2. **BIC boundary selection:** Hitting K=6 boundary highlights need for adaptive search ranges. Future analyses should test K=max+3 (e.g., K=1-9) to ensure optimum is within range.

3. **Zero variance components:** When random effects show zero variance (ICC=0.000), clustering on those features is futile. Should have excluded slopes from clustering features or tested intercept-only clustering explicitly.

4. **Bootstrap stability critical:** Jaccard=0.592 (59% consistency) means 41% of participants shift clusters across resampling. This is unacceptable for clinical/research applications requiring stable classification.

**Clinical Relevance:**

For cognitive assessment applications:
- **Limited utility for trajectory-based classification:** Cannot identify "fast forgetters" vs "slow forgetters" if forgetting rates are uniform (slopes = 0)
- **Baseline classification possible:** High/medium/low clusters based on Day 0 performance may suffice for cross-sectional screening
- **Schema-based diagnosis not supported:** No evidence for schema-selective impairment profiles (e.g., selective deficit for incongruent items)

---

## 4. Limitations

### Sample Limitations

**Sample Size:**
- N=100 provides adequate power for K-means clustering with K=2-4, but marginal for K=6 (16-22 participants per cluster)
- Cluster 5 (N=6) too small for reliable characterization (below 10% guideline)
- Bootstrap instability (Jaccard=0.592) may reflect insufficient N for stable 6-cluster solution

**Demographic Constraints:**
- Inherited from RQ 5.4.6/5.4.1: University undergraduate sample (age M~20, SD~2)
- Limited generalizability to older adults (schema utilization may differ with age)
- Schema knowledge may vary by education/cultural background (not assessed)

**Attrition:**
- Inherited from upstream RQs (RQ 5.4.1 data source)
- Any missing data or dropout already propagated through RQ 5.4.6 random effects
- Cannot assess attrition impact at this clustering stage

### Methodological Limitations

**Clustering Method:**

1. **K-means assumptions:**
   - Assumes spherical clusters (validated by scatter matrix, no severe elongation)
   - Assumes equal cluster variance (violated: Cluster 5 much smaller than others)
   - Sensitive to initialization (mitigated by n_init=50, but bootstrap Jaccard still low)

2. **BIC model selection:**
   - Optimal K at boundary (K=6) suggests inadequate search range
   - BIC penalizes model complexity, but may not capture clustering instability
   - No comparison to alternative selection methods (silhouette-based, gap statistic)

3. **Feature selection:**
   - 6 clustering features specified (3 intercepts + 3 slopes), but slopes contribute zero information
   - Should have tested 3-feature clustering (intercepts only) as primary model
   - Including zero-variance features dilutes clustering signal

**Quality Metrics:**

1. **Silhouette = 0.254 (WEAK):**
   - Below 0.40 threshold indicates poor cluster cohesion
   - Points within clusters are nearly as close to neighboring cluster centroids as their own
   - Suggests continuous distribution, not discrete clusters

2. **Jaccard = 0.592 (UNSTABLE):**
   - Below 0.75 threshold indicates poor bootstrap stability
   - 41% of participants shift clusters across resampling iterations
   - Clustering solution NOT robust to sample perturbations
   - Clinical/research applications requiring stable classification are NOT supported by this clustering

3. **Interpretation:**
   - Per concept.md guidance: "If silhouette < 0.40 and Jaccard < 0.75, interpret clusters as tentative patterns requiring replication"
   - Clusters should be reported as EXPLORATORY ONLY, not definitive profiles

**Data Source Limitations:**

1. **Zero slope variance (ICC_slope=0.000):**
   - Inherited from RQ 5.4.6 finding: no between-participant variance in forgetting rates
   - Makes trajectory-based clustering impossible (cannot cluster on constant features)
   - This limitation was NOT anticipated in RQ planning (rq_planner specified 6 features including slopes)

2. **Congruence-aggregated random effects:**
   - Random effects aggregate across all items within congruence level (Common/Congruent/Incongruent)
   - Loses item-level heterogeneity (e.g., some Common items easier than others)
   - May mask schema-selective patterns visible at finer grain

### Generalizability Constraints

**Population:**
- Findings specific to young adult sample (age ~20)
- Schema-based clustering may differ in:
  - Older adults (aging affects schema utilization and episodic memory)
  - Clinical populations (MCI, dementia, schizophrenia show schema processing deficits)
  - Children (developing schema knowledge)

**Context:**
- VR desktop paradigm (not fully immersive HMD)
- Schema congruence defined by scene context (kitchen, bedroom, bathroom)
- Results may not generalize to other schema types (social schemas, event schemas)

**Task:**
- 4 test sessions over 6 days (Day 0,1,3,6)
- Longer retention intervals (weeks, months) might reveal slope heterogeneity
- More frequent testing (daily) might capture early trajectory differences

### Technical Limitations

**K-means Specificity:**

1. **Hard clustering:** K-means assigns each participant to ONE cluster (no soft membership probabilities)
   - Alternative: Gaussian Mixture Models (GMM) allow probabilistic cluster membership
   - May better capture continuous distribution of individual differences

2. **Euclidean distance:** K-means uses Euclidean distance in z-score space
   - Assumes all features equally important (mitigated by standardization)
   - Alternative: Mahalanobis distance accounts for feature correlations

3. **No covariate adjustment:** Clustering does not control for age, sex, education, etc.
   - Cluster differences may reflect demographic confounds, not schema-specific patterns
   - Future analyses could use covariate-adjusted random effects

**Boundary Selection (K=6):**

- Stopped at K=6 per plan specification, but BIC suggests K=7+ might improve fit
- Rerunning with K=1-10 range is RECOMMENDED sensitivity analysis
- Current K=6 solution should be considered provisional until boundary concern addressed

**Bootstrap Validation:**

- 100 iterations with 80% subsampling (standard approach)
- Jaccard index aggregates across all clusters (may mask cluster-specific instability)
- Future validation should report per-cluster Jaccard coefficients

---

## 5. Next Steps

### Immediate Follow-Ups (Current Data)

**1. Test K=7-10 to Resolve Boundary Concern (HIGH PRIORITY):**

- **Why:** BIC optimal at K=6 (upper bound tested), no clear elbow observed
- **How:** Rerun Step 2 (cluster selection) testing K=1 to K=10, compare BIC values
- **Expected Insight:** Determine if K=6 is true optimum or artifact of search range
- **Timeline:** Immediate (same data, extend K range by 4 values, ~5 minutes computation)
- **Decision Rule:** If K=7,8,9, or 10 has lower BIC than K=6, adopt new K as optimal. If K=6 remains optimal with K=10 in range, boundary concern resolved.

**2. Intercept-Only Clustering (3 Features) (HIGH PRIORITY):**

- **Why:** Slopes contribute zero information (all ~ 0), diluting clustering signal
- **How:** Rerun clustering using ONLY Common_Intercept, Congruent_Intercept, Incongruent_Intercept (exclude slopes)
- **Expected Insight:** Test if 3-feature clustering improves quality metrics (silhouette, Jaccard)
- **Timeline:** Immediate (data already prepared, modify Step 1 feature selection, ~10 minutes)
- **Hypothesis:** Removing zero-variance features may improve silhouette from 0.254 to 0.30+ (still weak, but less noise)

**3. Gaussian Mixture Model Sensitivity Analysis (MEDIUM PRIORITY):**

- **Why:** K-means assumes hard clustering, but data may reflect continuous distribution
- **How:** Fit GMM with K=2-6, compare BIC to K-means BIC, examine posterior probabilities
- **Expected Insight:** If GMM shows high posterior uncertainty (e.g., 0.4/0.3/0.3 for 3 clusters), confirms continuous distribution interpretation
- **Timeline:** ~1 day (requires implementing GMM code, not in current tool catalog)
- **Alternative:** Report K-means findings as exploratory, acknowledge continuous distribution interpretation in limitations

**4. Per-Cluster Jaccard Coefficients (LOW PRIORITY):**

- **Why:** Aggregate Jaccard=0.592 may mask cluster-specific instability (e.g., Cluster 5 N=6 may drive instability)
- **How:** Modify Step 4 validation to compute Jaccard per cluster, report range and mean
- **Expected Insight:** Identify which specific clusters are unstable vs stable
- **Timeline:** Immediate (modify bootstrap validation code, ~30 minutes)

### Planned Thesis RQs (Chapter 5 Continuation)

**No direct follow-up RQ planned in current thesis structure.**

Schema-based clustering (RQ 5.4.7) is terminal analysis in Congruence series (RQ 5.4.1-5.4.7). However, findings inform interpretation of earlier RQs:

- **RQ 5.4.6 (Variance Decomposition):** Clustering null result confirms ICC_slope=0.000 finding. No need to model individual slope differences if clustering cannot detect them.
- **RQ 5.4.5 (Purified CTT):** High/medium/low clusters may correspond to CTT-defined high/medium/low performers. Cross-referencing cluster membership with RQ 5.4.5 performance tertiles could validate cluster labels.

### Methodological Extensions (Future Data Collection)

**1. Extended Retention Intervals to Detect Slope Heterogeneity:**

- **Current Limitation:** 6-day retention (Day 0,1,3,6) shows zero slope variance
- **Extension:** Add Day 14, Day 28 test sessions (longer retention interval may reveal forgetting rate differences)
- **Expected Insight:** Test if slope heterogeneity emerges at longer delays (>6 days)
- **Feasibility:** Requires new data collection (N=50 subsample, 2 additional test sessions, ~2 months)

**2. More Frequent Testing to Capture Early Trajectory Differences:**

- **Current Limitation:** 4 test sessions may miss rapid early forgetting differences
- **Extension:** Daily testing Days 0-6 (7 test sessions vs 4)
- **Expected Insight:** Test if slope heterogeneity visible in Days 0-3 window (steep initial forgetting)
- **Feasibility:** Requires new participants (N=50, 7 test sessions, ~1 month)

**3. Covariate-Adjusted Clustering:**

- **Current Limitation:** Clustering does not control for age, sex, education, schema knowledge
- **Extension:** Extract covariate-adjusted random effects from RQ 5.4.6 LMMs (include covariates as fixed effects), then cluster adjusted random effects
- **Expected Insight:** Test if cluster differences reflect schema-specific patterns vs demographic confounds
- **Feasibility:** Moderate (requires re-running RQ 5.4.6 LMMs with covariates, then re-running this RQ, ~1 week)

**4. Alternative Schema Manipulations:**

- **Current Limitation:** Congruence defined by scene context (kitchen/bedroom/bathroom objects)
- **Extension:** Test social schemas, event schemas, semantic schemas
- **Expected Insight:** Test if schema-selective clustering emerges with different schema types
- **Feasibility:** Requires new VR task development and data collection (~6 months)

### Theoretical Questions Raised

**1. Why Zero Between-Participant Variance in Forgetting Rates?**

- **Question:** RQ 5.4.6 found ICC_slope=0.000 (zero random slope variance). Why do all participants forget at identical rates?
- **Possible Explanations:**
  - **Measurement:** 4 test sessions insufficient to detect subtle slope differences (need more time points)
  - **VR task:** Schema-congruence manipulation may standardize forgetting (strong schema support prevents individual differences)
  - **Population:** Young adult sample with homogeneous cognitive function (ceiling effects compress forgetting rates)
  - **Theory:** Forgetting rate may be a FIXED biological parameter, not individual difference trait
- **Next Steps:** Extend retention interval (Days 14, 28), test in heterogeneous sample (young vs old), compare VR vs 2D paradigm
- **Feasibility:** Long-term research program (~2 years)

**2. Are Schema Effects Universal or Domain-Specific?**

- **Question:** Lack of schema-selective clusters suggests schema congruence affects everyone similarly. But is this true across all schema types, or specific to scene-based schemas?
- **Possible Explanations:**
  - **Universal:** Schema effects are fundamental property of episodic memory (everyone encodes congruent items better)
  - **Domain-specific:** Scene-based schemas (kitchen, bedroom) are so overlearned that individual differences are minimal. Other schemas (social, event) may show heterogeneity.
- **Next Steps:** Test clustering with social schema manipulation (role-congruent vs role-incongruent actions)
- **Feasibility:** Requires new VR task development (~1 year)

**3. Can Clustering Detect Schema-Selective Impairments in Clinical Populations?**

- **Question:** Current sample shows no schema-selective profiles. Would clinical populations (MCI, schizophrenia) show selective deficits for incongruent items?
- **Possible Explanations:**
  - **Healthy ceiling:** Young adults have intact schema processing (no room for selective deficits)
  - **Clinical heterogeneity:** MCI patients may cluster into schema-intact vs schema-impaired profiles
- **Next Steps:** Replicate RQ 5.4.7 clustering in MCI sample (N=50), compare cluster quality metrics to healthy sample
- **Feasibility:** Requires clinical recruitment (~1-2 years)

### Priority Ranking

**High Priority (Do First):**
1. Test K=7-10 to resolve boundary concern (immediate, same data)
2. Intercept-only clustering (3 features) to remove zero-variance noise (immediate, same data)
3. Report findings as WEAK CLUSTERING QUALITY + continuous distribution interpretation (publication strategy)

**Medium Priority (Subsequent):**
1. GMM sensitivity analysis (test soft clustering vs hard K-means)
2. Per-cluster Jaccard coefficients (identify unstable clusters)
3. Covariate-adjusted clustering (control for demographics)

**Lower Priority (Aspirational):**
1. Extended retention intervals (Days 14, 28) to detect slope heterogeneity (requires new data)
2. Alternative schema manipulations (social, event schemas) (requires new VR task)
3. Clinical sample replication (MCI patients) (requires clinical recruitment)

### Next Steps Summary

The weak clustering quality (silhouette=0.254, Jaccard=0.592) and K=6 boundary selection raise two critical questions for immediate follow-up:

1. **Is K=6 optimal, or artifact of search range?** (Test K=7-10, ~5 minutes)
2. **Do zero-variance slopes dilute clustering signal?** (Test 3-feature intercept-only clustering, ~10 minutes)

These sensitivity analyses will determine whether weak clustering reflects:
- **True continuous distribution** (no discrete schema-based profiles exist) ’ Report as meaningful NULL finding
- **Methodological artifact** (wrong K, wrong features) ’ Revise clustering approach

Broader methodological extensions (longer retention, alternative schemas, clinical samples) remain valuable but require substantial new data collection beyond current thesis scope.

**CRITICAL INTERPRETATION:** The absence of schema-selective clusters is ITSELF a meaningful finding. It suggests schema congruence effects are HOMOGENEOUS across individuals (universal property of episodic memory), not HETEROGENEOUS (strategic skill varying by person). This null finding contributes to schema theory by constraining models of individual differences in schema utilization.

---

**End of Summary**

**Summary generated by:** rq_results agent (v4.0)
**Pipeline version:** v4.X (13-agent atomic architecture)
**Date:** 2025-12-03
