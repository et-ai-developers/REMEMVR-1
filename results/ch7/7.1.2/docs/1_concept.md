# RQ 7.1.2: Intercept vs Slope Prediction

**Chapter:** 7
**Type:** Predictive Validity
**Subtype:** Intercept vs Slope Prediction
**Full ID:** 7.1.2

---

## Research Question

**Primary Question:**
Do cognitive tests predict baseline ability (Day 0 intercept) more than forgetting rate (slope), consistent with tests measuring encoding but not consolidation?

**Scope:**
This RQ examines differential prediction of LMM random effects (intercept and slope) using cognitive tests (RAVLT, BVMT, RPM). Intercept represents Day 0 baseline ability, slope represents forgetting rate across 6-day retention interval. Analysis uses per-participant random effects from Ch5 LMM models. N=100 participants.

**Theoretical Framing:**
Tests whether traditional neuropsychological tests capture encoding processes (measured immediately) versus consolidation processes (measured over days). Critical for understanding what cognitive tests actually measure in relation to real-world memory function.

---

## Theoretical Background

**Relevant Theories:**
- **Two-process theory** (Craik & Rose, 2012): Distinguishes encoding from consolidation processes in episodic memory
- **Consolidation Theory**: Multi-day memory retention involves different neural mechanisms than immediate encoding/retrieval
- **Transfer-appropriate processing**: Performance depends on match between encoding and retrieval processes

**Key Citations:**
Craik & Rose, 2012 (two-process theory of encoding vs consolidation)

**Theoretical Predictions:**
Two-process theory predicts cognitive tests should strongly predict encoding ability (intercept) but weakly predict consolidation efficiency (slope). Traditional tests measure immediate memory over 20-30 minutes, not multi-day retention processes.

**Literature Gaps:**
Limited research examining whether standard neuropsychological tests predict real-world forgetting patterns versus laboratory encoding performance.

---

## Hypothesis

**Primary Hypothesis:**
Cognitive tests predict intercept strongly (R² > 0.30) but slope weakly (R² < 0.10). Tests measure encoding/retrieval capacity over minutes, not multi-day consolidation processes.

**Secondary Hypotheses:**
- R²_intercept significantly > R²_slope (bootstrap CI excludes 0)
- No individual cognitive test significantly predicts slope after Bonferroni correction
- RAVLT and BVMT should show similar pattern (both immediate memory tests)

**Theoretical Rationale:**
Traditional neuropsychological tests assess immediate encoding and retrieval over 20-30 minute sessions. Multi-day forgetting involves consolidation processes (synaptic strengthening, replay, integration) that differ mechanistically from immediate memory performance.

**Expected Effect Pattern:**
Large effect for intercept prediction (R² = 0.30-0.40), minimal effect for slope prediction (R² < 0.10). Bootstrap confidence interval for difference should exclude zero, indicating significantly stronger intercept prediction.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Uses overall episodic memory from Ch5 (all domains combined)

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: Uses overall episodic memory from Ch5 (all domains combined)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Uses overall episodic memory from Ch5 (all domains combined)

**Inclusion Rationale:**
RQ uses overall episodic memory theta scores from Ch5 5.1.1 which combines all domains (What, Where, When) into single omnibus factor. This provides sufficient power for intercept/slope analysis and matches cognitive test generality.

**Exclusion Rationale:**
No domain-specific exclusions. This RQ focuses on overall episodic memory rather than domain-specific patterns.

---

## Analysis Approach

**Analysis Type:**
Linear regression predicting LMM random effects (intercepts and slopes) using cognitive test T-scores

**High-Level Workflow:**

**Step 1:** Extract random effects from Ch5 LMM with bias acknowledgment
- PRIMARY APPROACH: Simultaneous modeling to avoid two-stage bias:
  Model: `Theta ~ log_Days + (1 + log_Days | UID) + RAVLT*log_Days + BVMT*log_Days + RPM*log_Days`
  This tests differential prediction directly without BLUP extraction bias
- SECONDARY APPROACH (for comparison): Extract BLUPs from Ch5 5.1.1
  WARNING: BLUPs exhibit shrinkage bias - extreme values pulled toward population mean
  This differential shrinkage affects subsequent regression validity (Verbeke & Molenberghs, 2000)
- Document shrinkage magnitude: Compare BLUP variance to empirical variance

**Step 2:** Extract and standardize cognitive tests
- Load RAVLT, BVMT, RPM scores from master.xlsx
- Convert to T-scores (M=50, SD=10)
- Exclude NART due to language validity concerns

**Step 3:** Predict intercepts (if using two-stage approach)
- Model: `Intercept ~ RAVLT_T + BVMT_T + RPM_T`
- Check linearity: Partial regression plots for each predictor
- If non-linear patterns: Consider polynomial terms or transformations
- Report R², individual beta coefficients, p-values
- Apply Bonferroni correction: alpha = 0.05/6 = 0.0083 (3 predictors × 2 models)
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Include bootstrap 95% CIs for all coefficients (1000 replications)

**Step 4:** Predict slopes (if using two-stage approach)
- Model: `Slope ~ RAVLT_T + BVMT_T + RPM_T`
- Check linearity assumptions as in Step 3
- Report R², individual beta coefficients, p-values
- Apply same Bonferroni correction (alpha = 0.0083)
- CRITICAL LIMITATION: BLUP shrinkage creates non-uniform bias
  - Extreme slopes shrunk more than moderate slopes
  - This differential shrinkage can artificially reduce/inflate R²
  - Report bias-corrected standard errors if available

**Step 5:** Compare R² values with multiple approaches
- PRIMARY: From simultaneous model, compare main effects (intercept prediction) vs interaction effects (slope prediction)
- SECONDARY: For two-stage approach if used:
  - Participant-level block bootstrap (1000 replications, seed=42)
  - Preserves within-participant correlation structure
  - Bootstrap 95% CI for R²_intercept - R²_slope difference
  - Fisher's Z-test only if normality verified (Q-Q plots, Shapiro-Wilk)
  - If normality violated: Use bootstrap percentile method exclusively
- Hypothesis test: R²_intercept > R²_slope

**Step 6:** Model diagnostics and remedial actions
- Check residual normality (Q-Q plots, Shapiro-Wilk p > 0.05)
  - If violated: Use robust standard errors (HC3) or bootstrap inference
- Check homoscedasticity (Breusch-Pagan test, p > 0.05)
  - If violated: White's heteroscedasticity-consistent standard errors
- Check multicollinearity (VIF < 5, noting context-dependent thresholds)
  - If VIF > 5: Report predictor correlations, consider ridge regression
- Check outliers (Cook's D < 4/n, leverage values)
  - If influential points: Report results with and without outliers

**CRITICAL LIMITATIONS TO REPORT:**
1. Two-stage bias: BLUP extraction introduces non-uniform shrinkage (Hanusz & Tarasińska, 2015)
2. Type I error inflation: Two-stage analysis inflates false positive rates (Clark, 2019)
3. Solution: Report BOTH simultaneous model (primary) AND two-stage (sensitivity) results
4. Interpretation caveat: Two-stage R² may be biased; simultaneous model provides unbiased estimates

**CRITICAL for Ch7 and multiple comparisons:**
- Report BOTH uncorrected AND Bonferroni-corrected p-values (Decision D068)
- Include effect sizes with 95% CIs (R², beta coefficients)
- Bootstrap confidence intervals for R² difference
- Include power analysis if null findings

**Expected Outputs:**
- data/step01_random_effects.csv (extracted intercepts and slopes)
- data/step02_cognitive_tests.csv (T-scored predictors)
- data/step03_intercept_predictions.csv (intercept model results)
- data/step04_slope_predictions.csv (slope model results)
- data/step05_r_squared_comparison.csv (bootstrap results)
- results/intercept_vs_slope_summary.md (interpretation for thesis)
- plots/intercept_slope_prediction.png (visualization)

**Success Criteria:**
- R²_intercept > 0.25
- R²_slope < 0.15
- R²_intercept significantly > R²_slope (bootstrap CI excludes 0)
- No individual predictor significantly predicts slope after correction
- Model diagnostics pass (VIF < 5, residuals normal)

---

## Data Source

**Data Type:**
DERIVED (from Ch5 LMM results and master.xlsx cognitive tests)

### DERIVED Data Source:

**Source RQ:**
Ch5 5.1.1 (Functional Form Comparison - provides LMM with random intercepts/slopes)

**File Paths:**
- results/ch5/5.1.1/data/step06_best_model.pkl (saved LMM model with random effects)
- results/ch5/5.1.1/data/step04_lmm_input.csv (400 observations with UID and time)
- master.xlsx (cognitive test scores via tag patterns)

**Dependencies:**
Ch5 5.1.1 must complete through Step 6 (LMM fitting with random intercepts/slopes) before this RQ can extract random effects. Cognitive tests are independent data from master.xlsx.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from Ch5 5.1.1 (inherited inclusion criteria)
- [ ] Exclude: None (uses same sample as Ch5)

**Items:**
- [x] Uses theta scores (already aggregated from IRT calibration)
- Description: Overall episodic memory theta from omnibus factor

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - used to derive intercepts/slopes
- Description: LMM random effects capture per-participant baseline and trajectory

**Cognitive Tests:**
- [x] RAVLT Total (sum of T1-T5)
- [x] BVMT Total Recognition
- [x] RPM (Raven's Progressive Matrices)
- [ ] NART - EXCLUDED (language validity concerns in diverse sample)
