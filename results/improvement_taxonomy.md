# RQ Improvement Taxonomy - Path to PLATINUM Status

**Purpose:** Comprehensive checklist of potential improvements for Ch5/Ch6 RQs
**Goal:** Zero flaws, maximum defensibility, robust findings

---

## 1. GLMM VALIDATION

**Purpose:** Verify IRT→LMM findings with single-stage GLMM on item-level data

### 1.1 Intercept Effects (HIGH PRIORITY)
- [ ] Test group baseline differences (Age, Domain, Paradigm, Schema)
- [ ] Compare IRT→LMM vs GLMM p-values for intercepts
- [ ] Report if marginal/null findings become significant
- [ ] Power advantage: 28,800 observations vs 400-1,200

### 1.2 Slope/Interaction Effects (LOW PRIORITY)
- [ ] Verify trajectory findings agree (they always do per glmm.md)
- [ ] Only run if intercept validation reveals issues

### 1.3 Binary Outcomes (CRITICAL)
- [ ] Use binomial GLMM with logit link (NOT LMM on binary)
- [ ] Check overdispersion
- [ ] Report odds ratios with 95% CIs

**When to Apply:**
- RQs with group comparisons (Age, Domain, Paradigm, Schema)
- RQs with NULL intercept findings (verify robust vs underpowered)
- RQs with marginal p-values (p=0.04-0.13 range)

---

## 2. STATISTICAL ROBUSTNESS

### 2.1 Bootstrap Confidence Intervals
- [ ] Non-parametric bootstrap (1000-5000 iterations)
- [ ] Report bootstrapped CIs alongside parametric CIs
- [ ] Check if findings robust to outliers
- [ ] Flag if bootstrap CIs wider (outlier-sensitive)

### 2.2 Outlier Sensitivity
- [ ] Identify outliers (>3 SD from mean, Cook's D > 4/n)
- [ ] Re-run analysis excluding outliers
- [ ] Report if conclusions change
- [ ] Document outlier characteristics (who, why)

### 2.3 GEE for Clustered Binary Data
- [ ] Use GEE with exchangeable correlation (NOT LMM)
- [ ] Report within-person correlation
- [ ] Compare LMM vs GEE p-values (e.g., RQ 6.5.3: p=0.043→0.056)

### 2.4 Multiple Comparison Corrections
- [ ] Verify Bonferroni correction applied correctly
- [ ] Consider less conservative: Holm, FDR, Tukey HSD
- [ ] Report BOTH uncorrected and corrected p-values (Decision D068)

**When to Apply:**
- RQs with marginal findings (p=0.03-0.07 range)
- RQs with binary outcomes
- RQs with many pairwise comparisons

---

## 3. POWER & EFFECT SIZES

### 3.1 Power Analysis for NULL Findings
- [ ] Compute post-hoc power for observed effect size
- [ ] Report power to detect small (d=0.20), medium (d=0.50), large (d=0.80)
- [ ] Estimate N required for 0.80 power
- [ ] Flag if underpowered (power < 0.60 for small effects)

### 3.2 Equivalence Testing (TOST)
- [ ] For NULL findings: test if effect significantly smaller than meaningful threshold
- [ ] Set equivalence bound (e.g., Cohen's d < 0.20 or f² < 0.02)
- [ ] Report equivalence p-value (establishes "true null" vs "underpowered")

### 3.3 Effect Size Reporting
- [ ] Cohen's d for mean differences
- [ ] Cohen's f² for variance explained
- [ ] Partial η² for LMM fixed effects
- [ ] Report 95% CIs for all effect sizes
- [ ] Interpret: negligible (<0.10), small (0.20), medium (0.50), large (0.80)

### 3.4 Confidence Intervals
- [ ] Report CIs for ALL estimates (not just p-values)
- [ ] Visualize CIs in plots (error bars, shaded regions)
- [ ] Flag if CIs very wide (high uncertainty)

**When to Apply:**
- ALL RQs with NULL findings (power analysis mandatory)
- RQs claiming "no effect" (equivalence testing establishes true null)
- RQs with significant findings (effect sizes for practical importance)

---

## 4. MODEL SELECTION & SPECIFICATION

### 4.1 Model Averaging
- [ ] Fit multiple candidate models (linear, log, power law, quadratic, etc.)
- [ ] Compute Akaike weights
- [ ] Model-average predictions if top model < 90% weight
- [ ] Report effective N models (uncertainty quantification)

### 4.2 Extended Model Comparisons
- [ ] Test 17+ models including power law variants (α=0.3, 0.5, 0.7)
- [ ] Fractional exponents (sqrt, cube root)
- [ ] Reciprocal, exponential proxies
- [ ] Log-log transformations

### 4.3 Alternative Time Transformations
- [ ] Linear time (Days)
- [ ] Log time (log(Days + 1))
- [ ] Square root time (sqrt(Days))
- [ ] Power law time ((Days + 1)^α)
- [ ] Compare AIC/BIC across transformations

### 4.4 Random Effects Structure
- [ ] Test intercepts-only vs random slopes
- [ ] Test correlated vs uncorrelated random effects
- [ ] AIC/BIC model selection
- [ ] Report variance components with CIs
- [ ] Flag boundary warnings (variance near zero)

### 4.5 Non-Linear Effects
- [ ] Test quadratic time terms (Time²)
- [ ] Test cubic terms if theory supports
- [ ] Test piecewise models (consolidation windows)
- [ ] Compare linear vs non-linear AIC

**When to Apply:**
- RQs with trajectory modeling (forgetting curves)
- RQs with model uncertainty (top model < 90% weight)
- RQs with boundary warnings in LMM
- RQs testing consolidation hypotheses

---

## 5. ASSUMPTION VALIDATION

### 5.1 LMM Diagnostics
- [ ] Residual normality (Q-Q plots, Shapiro-Wilk)
- [ ] Homoscedasticity (residuals vs fitted)
- [ ] Independence (no autocorrelation in residuals)
- [ ] Leverage/influence (Cook's D, DFBETAS)
- [ ] Multicollinearity (VIF < 5)

### 5.2 Heteroscedasticity Checks
- [ ] Breusch-Pagan test
- [ ] If detected: Use robust SEs or weighted LMM
- [ ] Document if N > 100 (robust to moderate heteroscedasticity)

### 5.3 IRT Assumptions
- [ ] Item fit (infit/outfit MNSQ 0.7-1.3)
- [ ] Local independence (Q3 statistic < 0.20)
- [ ] Unidimensionality (first eigenvalue ratio > 3:1)
- [ ] Monotonicity (ICC curves don't cross)

### 5.4 Missing Data Diagnostics
- [ ] Missingness pattern (MCAR, MAR, MNAR)
- [ ] Little's MCAR test
- [ ] Compare completers vs non-completers
- [ ] Sensitivity analysis: worst-case imputation

**When to Apply:**
- ALL RQs (basic diagnostics mandatory)
- RQs with convergence warnings
- RQs with high missing data (>5%)
- IRT-based RQs (item fit checks)

---

## 6. SENSITIVITY ANALYSES

### 6.1 Lord's Paradox Mitigation (Calibration RQs)
- [ ] ANCOVA approach: `Confidence ~ Group + Accuracy`
- [ ] Within-group standardization
- [ ] Compare to primary analysis (do conclusions change?)

### 6.2 Difference Score Reliability (Calibration RQs)
- [ ] Compute r(Accuracy, Confidence)
- [ ] Apply formula: r_diff = (r_xx + r_yy - 2*r_xy) / (2 - 2*r_xy)
- [ ] Report if r_diff < 0.70 (low reliability)
- [ ] Consider latent variable models if unreliable

### 6.3 Alternative Breakpoints (Piecewise Models)
- [ ] Test multiple breakpoints (24h, 36h, 48h, 72h)
- [ ] Data-driven breakpoint selection (change-point detection)
- [ ] Compare AIC across breakpoints
- [ ] Report if findings robust to breakpoint choice

### 6.4 Pre-IRT vs Post-IRT Calibration
- [ ] Compute metrics on raw scores (before IRT)
- [ ] Compare to IRT theta-based metrics
- [ ] Test if IRT scaling attenuates effects

### 6.5 Paradigm Order Effects
- [ ] Check if paradigm order randomized
- [ ] If fixed order: add Order as covariate
- [ ] Test Order × Paradigm interaction

**When to Apply:**
- Calibration RQs (6.1-6.8 series)
- Piecewise models (consolidation RQs)
- RQs with fixed testing order
- RQs with weak effects (check if IRT removes signal)

---

## 7. DOCUMENTATION & PRESENTATION

### 7.1 Dual P-Value Reporting (Decision D068)
- [ ] Report uncorrected AND Bonferroni-corrected p-values
- [ ] Annotate plots with both p-values
- [ ] Transparency about multiple comparisons

### 7.2 Dual-Scale Reporting (Decision D069)
- [ ] Theta scale (standardized, comparable)
- [ ] Probability scale (interpretable, practical)
- [ ] Both scales in plots (2×2 grid or dual y-axes)

### 7.3 Plot Regeneration
- [ ] Verify plots match current analysis
- [ ] Check for stale plots (outdated data)
- [ ] Update annotations (p-values, effect sizes)
- [ ] High-resolution export (300+ DPI for publication)

### 7.4 Results Summary Completeness
- [ ] Statistical findings table
- [ ] Plot descriptions
- [ ] Theoretical interpretation
- [ ] Limitations section
- [ ] Next steps recommendations

### 7.5 Cross-References
- [ ] Link to plan.md expected outputs
- [ ] Link to concept.md hypotheses
- [ ] Link to upstream/downstream RQs
- [ ] Document dependencies

**When to Apply:**
- ALL RQs (documentation standards)
- RQs with multiple comparisons (dual p-values)
- RQs with theta-based outcomes (dual scales)
- RQs with updated analyses (regenerate plots)

---

## 8. DATA QUALITY

### 8.1 IRT Purification Verification
- [ ] Report % items excluded
- [ ] Check if exclusion balanced across groups
- [ ] Document purification criteria
- [ ] Sensitivity: re-run without purification

### 8.2 Response Pattern Analysis
- [ ] Extreme response style (ERS) detection (% 1s and 5s)
- [ ] Restricted range (SD < 0.8)
- [ ] Ceiling/floor effects (>20% at min/max)
- [ ] Acquiescence bias (mean rating vs midpoint)

### 8.3 Confidence Rating Patterns (Section 1.4 Requirement)
- [ ] % participants using full scale (1-5)
- [ ] % extremes only (1s and 5s)
- [ ] SD of ratings per participant
- [ ] Flag restricted range (limits calibration)

### 8.4 Item Parameter Checks
- [ ] Discrimination (a) range: expect 0.5-2.5
- [ ] Difficulty (b) range: expect -3 to +3
- [ ] Flag misfitting items (infit/outfit > 1.3)
- [ ] Check domain balance (equal items per domain)

**When to Apply:**
- IRT-based RQs (purification checks)
- Confidence RQs (response patterns)
- RQs with low reliability (item parameter issues?)
- RQs with floor/ceiling effects

---

## 9. THEORETICAL GROUNDING

### 9.1 Literature Alignment
- [ ] Cite relevant meta-analyses
- [ ] Compare effect sizes to published literature
- [ ] Explain unexpected findings (vs theory)
- [ ] Acknowledge paradigm-specific constraints

### 9.2 Mechanistic Interpretation
- [ ] Explain WHY effect occurred (or didn't)
- [ ] Connect to cognitive theory (dual-process, encoding-retrieval, etc.)
- [ ] Propose testable mechanisms
- [ ] Alternative explanations considered

### 9.3 Boundary Conditions
- [ ] Specify population limits (age, education, clinical status)
- [ ] Specify context limits (VR vs real-world, desktop vs HMD)
- [ ] Specify task limits (recognition vs recall, intentional vs incidental)

### 9.4 Practical Implications
- [ ] Clinical relevance (assessment applications)
- [ ] Effect size interpretation (meaningful vs trivial)
- [ ] Intervention targets (if applicable)

**When to Apply:**
- ALL RQs (theory section mandatory)
- RQs with unexpected findings (theory reconciliation)
- RQs with null findings (explain why no effect)
- Applied RQs (clinical implications)

---

## 10. CRITICAL ISSUES (BLOCKERS TO PLATINUM)

### 10.1 Convergence Failures
- [ ] LMM/GLMM convergence warnings
- [ ] Boundary warnings (variance = 0)
- [ ] Singular fit warnings
- [ ] **Action:** Simplify random effects, use priors (Bayesian), check data quality

### 10.2 Missing Required Analyses
- [ ] Power analysis for NULL findings (MANDATORY)
- [ ] Difference score reliability for calibration RQs (MANDATORY)
- [ ] Confidence response patterns (Section 1.4, MANDATORY)
- [ ] **Action:** Complete missing analyses before PLATINUM status

### 10.3 Lord's Paradox Violations
- [ ] Calibration RQs comparing groups with different baselines
- [ ] Difference scores confounded with baseline
- [ ] **Action:** Run ANCOVA, within-group standardization

### 10.4 Stale/Mismatched Outputs
- [ ] Plots don't match current analysis
- [ ] Results summary references old model
- [ ] Dependencies on updated upstream RQs
- [ ] **Action:** Regenerate all outputs, verify consistency

### 10.5 Unresolved Anomalies
- [ ] Unexpected patterns flagged but not investigated
- [ ] Post-hoc explanations not tested
- [ ] Contradictory findings across related RQs
- [ ] **Action:** Follow-up analyses, sensitivity checks, cross-RQ validation

---

## PLATINUM STATUS CRITERIA

An RQ achieves PLATINUM status when:

✅ **Statistical Rigor:**
- [ ] All assumptions validated (Section 5)
- [ ] Robustness checks passed (Section 2)
- [ ] Effect sizes reported with CIs (Section 3)
- [ ] NULL findings have power analysis + TOST (Section 3)

✅ **Methodological Soundness:**
- [ ] Appropriate model selected (Section 4)
- [ ] Sensitivity analyses completed (Section 6)
- [ ] No Lord's paradox violations (Section 6.1)
- [ ] Difference scores reliable if used (Section 6.2)

✅ **Documentation Excellence:**
- [ ] Dual p-values reported (Section 7.1)
- [ ] Dual scales for theta outcomes (Section 7.2)
- [ ] Plots current and annotated (Section 7.3)
- [ ] Complete results summary (Section 7.4)

✅ **Data Quality:**
- [ ] IRT purification justified (Section 8.1)
- [ ] Response patterns documented (Section 8.2-8.3)
- [ ] No extreme responding issues (Section 8.2)

✅ **Theoretical Coherence:**
- [ ] Findings grounded in literature (Section 9.1)
- [ ] Mechanistic interpretation (Section 9.2)
- [ ] Boundary conditions specified (Section 9.3)

✅ **Zero Critical Issues:**
- [ ] No convergence failures (Section 10.1)
- [ ] No missing mandatory analyses (Section 10.2)
- [ ] No unresolved anomalies (Section 10.5)

---

## USAGE INSTRUCTIONS

**For each RQ:**
1. Review all 10 sections of this taxonomy
2. Check applicable items for that RQ
3. Prioritize by section numbers (1-3 = HIGH, 4-6 = MEDIUM, 7-9 = LOW, 10 = BLOCKER)
4. Create step-by-step action plan
5. Execute improvements
6. Verify PLATINUM criteria met
7. Document in finalization roadmap

**Prioritization Heuristic:**
- **BLOCKERS FIRST** (Section 10) - Can't achieve PLATINUM without resolving these
- **GLMM if applicable** (Section 1) - Quick wins, high impact for null/marginal findings
- **Power/Effect Sizes** (Section 3) - Mandatory for null findings
- **Robustness** (Section 2) - For marginal findings (p < 0.10)
- **Model Selection** (Section 4) - For trajectory RQs, model uncertainty
- **Documentation** (Section 7) - Final polish before PLATINUM

---

**End of Taxonomy**
