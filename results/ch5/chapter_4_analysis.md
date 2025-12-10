# Chapter 4: Statistical Analysis

## 4.1 Overview of Analytic Strategy

[TBD: 200-300 words explaining multi-stage analysis pipeline, why IRT+LMM, dealing with repeated measures]

---

## 4.2 Item Response Theory (IRT) Calibration

### 4.2.1 Graded Response Model (GRM)

The Graded Response Model (Samejima, 1969) was used to estimate latent memory ability (θ) from polytomous confidence-rated item responses. The GRM is a unidimensional IRT model suitable for ordinal response categories (e.g., 1-5 star confidence ratings).

**Model Specification:**

For participant *j* on item *i* with response category *k*:

```
P(X_ij ≥ k | θ_j, a_i, b_ik) = 1 / (1 + exp(-a_i(θ_j - b_ik)))
```

Where:
- θ_j = Latent memory ability for participant *j* (continuous scale)
- a_i = Discrimination parameter for item *i* (slope of item response function)
- b_ik = Threshold parameter for item *i* at category boundary *k* (difficulty)
- Response categories: 1-5 (1 = Guess/No Memory, 5 = Absolutely Certain)

**Estimation Method:**

- Algorithm: Marginal maximum likelihood estimation (MMLE)
- Priors: None (frequentist estimation)
- Standard errors: Computed from observed information matrix
- Software: [TBD: Extract from logs - likely mirt package or PyIRT]

**Convergence Criteria:**

- Log-likelihood change: < 0.001 between iterations
- Maximum iterations: 500 (default)
- Convergence status: Flagged in output if not achieved

**Output:**

- Theta estimates (θ̂): One per participant per test session
- Standard errors (SE_θ): Measurement uncertainty for each estimate
- Item parameters: Discrimination (a) and difficulty thresholds (b) for each item
- Model fit statistics: Log-likelihood, AIC, BIC

### 4.2.2 Item Purification Protocol (Decision D039)

To ensure robust IRT calibration, poor-quality items were systematically excluded using empirical quality thresholds before final theta estimation. This two-pass calibration approach prevents measurement distortion from items with low discrimination or extreme difficulty.

**Rationale:**

Low-quality items (e.g., items with weak discrimination or extreme difficulty) contribute noise rather than reliable measurement. Including such items can:
- Inflate measurement error (larger SE_θ)
- Distort ability estimates (bias in θ̂)
- Reduce statistical power in downstream analyses

**Quality Criteria:**

Items were retained only if they met BOTH conditions:

1. **Discrimination:** a ≥ 0.4 (minimum slope threshold)
2. **Difficulty:** |b| ≤ 3.0 (difficulty within ±3 SD of mean ability)

**Two-Pass Calibration Protocol:**

**Pass 1: Exploratory Calibration (All Items)**
- Calibrate GRM using all available items
- Extract item parameters (a, b) for each item
- Flag items violating quality criteria

**Pass 2: Confirmatory Calibration (Purified Items Only)**
- Exclude flagged items
- Re-calibrate GRM using purified item set
- Generate final theta estimates for analysis
- Verify all retained items still meet criteria

**Typical Outcomes:**

- Retention rate: 40-70% of original items (varies by domain/task)
- Excluded items: Predominantly temporal order items (inherently difficult, low discrimination)
- Impact on theta range: Minimal distortion (±0.1-0.2 SD typical shift)

**Decision Justification (D039):**

This protocol balances two competing goals:
1. **Maximizing information:** More items = lower SE_θ
2. **Maximizing quality:** Fewer, better items = unbiased θ̂

The a ≥ 0.4 threshold is standard in applied IRT (Reise & Waller, 2009). The |b| ≤ 3.0 threshold prevents floor/ceiling effects where few participants can answer correctly.

### 4.2.3 Dimensionality Considerations

[TBD: Omnibus vs domain-specific factors, justification for different RQ approaches]

---

## 4.3 Linear Mixed Models (LMM)

### 4.3.1 Model Specification

Linear Mixed Models (LMMs) were used to model trajectories of memory ability (θ) across repeated measurements while accounting for within-subject correlation. LMMs partition variance into fixed effects (population-level patterns) and random effects (individual differences).

**General Form:**

```
y_ij = β₀ + β₁X_ij + ... + β_pX_ij + u_j + ε_ij
```

Where:
- y_ij = Outcome (theta) for participant *j* at observation *i*
- β₀, β₁, ..., β_p = Fixed effects (population parameters)
- X_ij = Predictor variables (time, age, domain, etc.)
- u_j ~ N(0, σ²_u) = Random intercept for participant *j*
- ε_ij ~ N(0, σ²_ε) = Residual error

**Fixed Effects:**

Fixed effects varied by research question but typically included:
- Time-based predictors: Days, log(Days+1), TSVR_hours, power-law transformations
- Demographic predictors: Age, age², gender
- Task factors: Domain (What/Where/When), congruence, schema
- Cognitive predictors: RAVLT, BVMT, NART, Raven's

**Random Effects:**

**Random Intercepts by Participant (UID):**

All models included random intercepts to account for between-subject variability in baseline memory ability. This structure recognizes that participants differ in average theta but assumes parallel trajectories (equal forgetting rates).

```
θ_ij = (β₀ + u_j) + β₁×Time_ij + ε_ij
```

**Random Slopes (When Tested):**

Some RQs tested random slopes for time effects, allowing forgetting rates to vary across participants:

```
θ_ij = (β₀ + u_0j) + (β₁ + u_1j)×Time_ij + ε_ij
```

Where:
- u_0j ~ N(0, σ²_intercept) = Random intercept variance
- u_1j ~ N(0, σ²_slope) = Random slope variance
- Cov(u_0j, u_1j) = ρ × σ_intercept × σ_slope

Random slope models were fit when theoretically justified and convergent. Models with singular covariance matrices or boundary solutions were reported but interpreted cautiously.

**Piecewise LMM Specification:**

Some RQs tested hypotheses involving discrete phase transitions (e.g., pre-consolidation vs post-consolidation). Piecewise LMMs allow different slopes in different time segments while accounting for repeated measures:

```
θ_ij = β₀ + β₁×Time_within_ij + β₂×Segment_ij + β₃×(Time_within × Segment)_ij + u_j + ε_ij
```

Where:
- Time_within = Time variable recentered within each segment (0 = segment start)
- Segment = Categorical indicator (Early vs Late, or Practice vs Forgetting)
- Time_within × Segment = Interaction term (tests whether slopes differ across segments)
- Inflection point: Theoretically motivated (e.g., 48 hours for consolidation, 24 hours for practice effects)

**Interpretation:**
- β₁ = Slope in reference segment (e.g., Early phase)
- β₁ + β₃ = Slope in comparison segment (e.g., Late phase)
- β₃ = Difference in slopes (test via p-value on interaction term)
- Slope ratio: (β₁ + β₃) / β₁ quantifies proportional change in rate

**Model Comparison:**
- Continuous models (e.g., quadratic, logarithmic): Smooth trajectory, no discrete phases
- Piecewise models: Allow abrupt slope changes at theoretically motivated inflection points
- AIC decision: ΔAIC < -2 favors piecewise; ΔAIC > +2 favors continuous; |ΔAIC| < 2 equivalent

**Estimation Method:**

- **Parameter Estimation:** REML = True (restricted maximum likelihood)
  - Preferred for unbiased variance component estimates
  - Used for final model parameters reported in results

- **Model Comparison:** REML = False (maximum likelihood)
  - Required for valid AIC comparison (see §4.3.2)
  - All candidate models refit with ML before AIC computation

**Software Implementation:**

- Software: [TBD: Extract from logs - likely statsmodels.MixedLM or lme4]
- Optimizer: [TBD: Default optimizer for respective package]
- Convergence tolerance: [TBD: Extract from logs]

### 4.3.2 Model Comparison Procedures

When multiple candidate models are theoretically plausible, information-theoretic model selection via Akaike Information Criterion (AIC) provides a principled framework for comparing non-nested models. This approach balances model fit against model complexity.

**Akaike Information Criterion (AIC):**

```
AIC = -2 × log(L) + 2k
```

Where:
- log(L) = Log-likelihood of the fitted model
- k = Number of estimated parameters (including variance components)

Lower AIC indicates better balance between fit and parsimony. Models must be fit with REML=False (maximum likelihood) for valid AIC comparison.

**Delta AIC (ΔAIC):**

For model comparison, compute ΔAIC relative to the best model:

```
ΔAIC_i = AIC_i - AIC_best
```

**Interpretation (Burnham & Anderson, 2002):**
- ΔAIC < 2: Competitive models (substantial empirical support)
- ΔAIC 2-10: Weak support (considerably less plausible)
- ΔAIC > 10: Essentially no support (implausible given data)

**Akaike Weights:**

Akaike weights quantify relative probability each model is the best in the candidate set:

```
w_i = exp(-ΔAIC_i / 2) / Σ_j exp(-ΔAIC_j / 2)
```

**Interpretation:**
- w_i = 0.90: 90% probability this model is best (strong single-model support)
- w_i = 0.30: 30% probability (high uncertainty, multiple competitive models)
- Evidence ratio: w_i / w_j quantifies relative support (e.g., 4:1 means 4× more likely)

**Model Averaging:**

When model selection uncertainty is high (best model weight < 0.30 or multiple models with ΔAIC < 2), model averaging provides robust predictions by weighting predictions across competitive models:

**Trigger:** Best model weight < 0.30 threshold

**Procedure:**
1. Identify competitive models: All models with ΔAIC < 2
2. Renormalize Akaike weights to sum = 1.0 (conditional weights)
3. Compute weighted-average predictions: ŷ = Σ w_i ŷ_i
4. Compute between-model variance: Var(ŷ) = Σ w_i [(ŷ_i - ŷ)² + Var(ŷ_i)]

**Advantages:**
- Accounts for model uncertainty (no false precision from single-model selection)
- Provides uncertainty estimates (prediction SE includes between-model variance)
- Robust to model misspecification (averaging reduces impact of single poor model)

**Reporting Standards:**

For all model comparisons, report:
- AIC table: Model name, AIC, ΔAIC, Akaike weight
- Best model: Specification, parameters, fit statistics
- Competitive models: Any with ΔAIC < 2 noted
- Model averaging: If triggered, report number of models averaged, cumulative weight, prediction SE range

### 4.3.3 Assumption Checking

Linear mixed models assume specific distributional properties of residuals and random effects. Violations can inflate Type I error rates or bias parameter estimates. Systematic assumption checks were performed for all LMM analyses.

**Residual Normality:**
- Method: Shapiro-Wilk test, Q-Q plots
- Threshold: p > 0.05 (fail to reject normality)
- Impact if violated: Inflated Type I error for fixed effects tests, biased standard errors
- Robustness: LMMs reasonably robust to mild normality violations with N ≥ 100

**Homoscedasticity (Constant Variance):**
- Method: Breusch-Pagan test, residual vs fitted plots
- Threshold: p > 0.05 (fail to reject homoscedasticity)
- Impact if violated: Biased standard errors, inflated Type I error
- Mitigation: Heteroscedasticity-consistent standard errors if severe

**Independence (Temporal Autocorrelation):**
- Method: Autocorrelation function (ACF) plots, Durbin-Watson test
- Threshold: |ACF| < 0.1 at Lag 1
- Impact if violated: Underestimated standard errors (inflated Type I error)
- Mitigation: AR(1) correlation structure (when theoretically justified and convergent)

**Random Effects Normality:**
- Method: Q-Q plots of Best Linear Unbiased Predictors (BLUPs)
- Threshold: Qualitative assessment (points follow diagonal)
- Impact if violated: Biased variance component estimates, invalid random effect predictions
- Robustness: Generally robust with moderate sample sizes (N ≥ 50)

**Outlier Detection:**
- Method: Studentized residuals
- Threshold: <5% observations with |residual| > 3.0
- Action: Report outliers, refit models with/without outliers to assess influence
- Exclusion: Only if outliers represent data entry errors (not valid extreme observations)

**Convergence Diagnostics:**
- Singular covariance matrices: Random effect variance = 0 (overfitted)
- Boundary solutions: Variance estimates hit constraint (e.g., correlation = ±1.0)
- Gradient warnings: Optimizer failed to converge (parameter estimates unreliable)
- Action: Simplify random structure, increase iterations, try alternative optimizers

**Reporting Standards:**

When assumptions violated but effects highly significant (e.g., p < 0.001), conclusions typically robust despite violations. Report violations transparently but note when effect magnitudes far exceed threshold (e.g., 10× smaller p-value than critical α).

---

## 4.4 Effect Size Reporting

### 4.4.1 Standardized Effect Sizes

[TBD: Cohen's d, f², partial η² - will be populated as effect sizes are reported]

### 4.4.2 LMM-Specific Effect Sizes

**Intraclass Correlation Coefficient (ICC):**

ICC quantifies the proportion of total variance attributable to between-group (or between-person) differences:

```
ICC = σ²_between / (σ²_between + σ²_within)
```

**Interpretation:**
- ICC < 0.20: Low clustering (minimal stable individual differences)
- ICC 0.20-0.40: Moderate clustering (meaningful trait-like stability)
- ICC > 0.40: Substantial clustering (strong trait-like stability)

**Applications:**
- ICC_intercept: Proportion of baseline ability variance that is between-person
- ICC_slope: Proportion of forgetting rate variance that is between-person
- ICC_conditional(t): Time-varying ICC accounting for intercept-slope covariance

**Marginal R² and Conditional R²:**

[TBD: Will be populated when these metrics are reported]

---

## 4.5 Multiple Comparisons Corrections

### 4.5.1 Bonferroni Correction (Decision D068)

When conducting multiple hypothesis tests within a single analysis or research question, the probability of at least one false positive (family-wise error rate) increases. Bonferroni correction controls this inflation by adjusting the significance threshold.

**When Applied:**

Bonferroni correction was applied when:
1. Multiple pairwise comparisons within a single RQ (e.g., comparing 3+ groups)
2. Testing multiple interaction terms in exploratory analyses
3. Hierarchical model comparisons with multiple candidate predictors

**Correction Formula:**

```
α_adjusted = α_family / k
```

Where:
- α_family = Family-wise Type I error rate (typically 0.05)
- k = Number of planned comparisons
- α_adjusted = Threshold for individual test significance

**Example:** For k = 15 comparisons with α_family = 0.05:
```
α_adjusted = 0.05 / 15 = 0.00333
```

Effects significant at p < 0.00333 are considered significant after Bonferroni correction.

**Dual Reporting (Decision D068):**

To maintain transparency and allow readers to assess effect robustness:
1. **Report both uncorrected and Bonferroni-corrected p-values**
2. State correction factor explicitly (e.g., "Bonferroni α = 0.003, correcting for 15 tests")
3. Interpret effects in context of both thresholds:
   - p < α_adjusted: Survives correction (robust to multiple testing)
   - α_adjusted < p < 0.05: Marginal (significant without correction, fails with correction)
   - p > 0.05: Not significant by either standard

**Rationale:**

Bonferroni is conservative (increases Type II error) but ensures strong control of family-wise error rate. Dual reporting balances:
- **Type I error control:** Protect against false positives from multiple testing
- **Transparency:** Readers can assess evidence strength across correction thresholds
- **Context sensitivity:** Different fields have different tolerance for Type I vs Type II error trade-offs

**Limitations:**

- Assumes tests are independent (conservative if tests correlated)
- Can be overly conservative with large k (consider False Discovery Rate for exploratory analyses)
- Only controls family-wise error within defined "family" (does not correct across separate RQs)

### 4.5.2 False Discovery Rate (FDR)

[TBD: Benjamini-Hochberg procedure for exploratory analyses]

---

## 4.6 Cluster Analysis for Individual Differences

Some RQs used cluster analysis to identify latent subgroups of participants with distinct trajectory profiles. K-means clustering partitioned participants based on model-derived random effects (intercepts and slopes).

**K-means Clustering:**

K-means partitions N observations into K clusters by minimizing within-cluster variance:

```
argmin Σ_k Σ_{i∈C_k} ||x_i - μ_k||²
```

Where:
- x_i = Feature vector for participant i (e.g., random intercept, random slope)
- μ_k = Centroid of cluster k (multivariate mean)
- C_k = Set of participants assigned to cluster k

**Optimal K Selection:**

**Method 1: Bayesian Information Criterion (BIC)**
```
BIC = -2×log(L) + k×log(N)
```
- Lower BIC indicates better model (penalizes complexity)
- Minimum BIC identifies optimal K
- **Limitation:** May select boundary K if tested range insufficient

**Method 2: Elbow Method (Remediation)**
- Plot inertia (within-cluster sum of squares) vs K
- Compute second derivative of BIC curve
- Largest absolute second derivative = strongest "elbow"
- Used when BIC minimum at boundary (overfitting indicator)

**Cluster Quality Metrics:**

**Silhouette Coefficient:**
```
s_i = (b_i - a_i) / max(a_i, b_i)
```
Where:
- a_i = Mean distance from participant i to other members of own cluster
- b_i = Mean distance from participant i to members of nearest other cluster
- Range: [-1, 1], where 1 = perfect separation, 0 = overlapping

**Interpretation:**
- s > 0.50: Strong cluster structure
- s = 0.25-0.50: Reasonable/weak structure
- s < 0.25: Artificial/poor structure

**Bootstrap Stability:**
- Resample N participants with replacement (B=100 iterations typical)
- Refit K-means with same K
- Compute Jaccard coefficient (pairwise cluster agreement)

```
Jaccard = |A ∩ B| / |A ∪ B|
```

**Interpretation:**
- Jaccard ≥ 0.75: Stable clustering
- Jaccard = 0.60-0.74: Questionable stability
- Jaccard < 0.60: Unstable (consider reducing K)

**Preprocessing:**

- **Standardization:** Z-score all clustering variables (mean=0, SD=1) to ensure equal weighting
- **Random effects extraction:** Use model-averaged random effects when functional form uncertain
- **Sample size:** Minimum 10% per cluster (N≥10) to avoid singleton/tiny clusters

**Reporting Standards:**

For all cluster analyses, report:
- K selection process (BIC, elbow method)
- Cluster sizes (N, percentage)
- Cluster centers (both standardized and raw scales)
- Silhouette coefficient (overall and per-cluster if available)
- Bootstrap Jaccard coefficient with 95% CI
- Interpretation of cluster profiles (theoretical meaning)

**When Clustering is Unstable:**

Low Jaccard (<0.60) indicates cluster structure sensitive to sampling variation. This may reflect:
1. **Model averaging artifact:** Incorporating model uncertainty increases variance (FEATURE, not bug)
2. **Weak separation:** Clusters not robustly distinct (consider reducing K)
3. **Overfitting:** Too many clusters for sample size (use elbow method, not BIC minimum at boundary)

Unstable clustering is not necessarily fatal—report findings transparently and interpret profiles cautiously as "provisional latent patterns" rather than "robust subgroups."

---

## 4.7 Missing Data Handling

[TBD: Will document REMEMVR's 0% missing data post-calibration]

---

## 4.8 Software and Reproducibility

[TBD: Software versions to be extracted from RQ logs]

---

**END CHAPTER 4 (Analysis Methods)**
