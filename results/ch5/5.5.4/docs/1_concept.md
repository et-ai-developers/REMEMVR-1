# RQ 5.5.4: IRT-CTT Convergence for Source-Destination Memory

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** IRT-CTT Convergence
**Full ID:** 5.5.4

---

## Research Question

**Primary Question:**
Do IRT theta scores and CTT sum scores show high convergence for source (pick-up location: -U-) and destination (put-down location: -D-) memory, validating RQ 5.5.1 findings are not measurement artifacts?

**Scope:**
This RQ examines measurement convergence between IRT theta scores and CTT mean scores for source and destination spatial memory. Sample: N=100 participants × 4 test sessions × 2 location types = 800 observations. CTT scores computed on IRT-purified item sets (from RQ 5.5.1). Convergence assessed via: (1) Pearson correlations per location type (threshold r > 0.70), (2) parallel LMM fixed effects agreement (Cohen's kappa > 0.60), (3) overall classification agreement (> 80%).

**Theoretical Framing:**
This RQ extends the IRT-CTT convergence validation trilogy from Chapter 5 (RQs 5.2.4 for Domains, 5.3.5 for Paradigms, 5.4.4 for Congruence) to the novel source-destination spatial memory factor. High convergence demonstrates that the source-destination memory dissociation found in RQ 5.5.1 is robust to measurement approach (IRT vs CTT), validating findings are not IRT-specific artifacts. This is critical for establishing generalizability and replicability of the source-destination phenomenon.

---

## Theoretical Background

**Relevant Theories:**

- **Measurement Invariance Theory:** Robust psychological findings should replicate across different measurement approaches (Borsboom, 2006). IRT and CTT represent fundamentally different psychometric frameworks - IRT models item-level response patterns, CTT aggregates raw scores. High convergence demonstrates the underlying latent construct (source/destination memory) is measurement-method-independent.

- **Source-Destination Memory Dissociation (from RQ 5.5.1):** Source memory (pick-up locations) shows higher accuracy than destination memory (put-down locations), attributed to (1) proactive interference theory - source encoded first, (2) schema support - source locations more semantically appropriate, (3) "lost keys" phenomenon, (4) goal discounting after task completion, (5) elaborated encoding during pick-up vs motor execution during put-down.

**Key Citations:**
To be added by rq_scholar

**Theoretical Predictions:**

Based on the IRT-CTT convergence trilogy (RQs 5.2.4, 5.3.5, 5.4.4), which established measurement robustness across domains, paradigms, and congruence factors in Chapter 5, the same pattern should extend to source-destination memory:

1. Strong correlations (r > 0.70) between IRT theta and CTT mean scores for both location types, demonstrating linear association
2. Substantial fixed effects agreement (Cohen's kappa > 0.60) when fitting parallel LMMs to IRT vs CTT scores, demonstrating structural equivalence
3. High overall classification agreement (> 80%) across measurement approaches

If convergence is strong, the source-destination dissociation (RQ 5.5.1 findings) is validated as measurement-independent.

**Literature Gaps:**

The IRT-CTT convergence literature focuses on educational testing and personality assessment. Application to episodic memory measurement, particularly spatial source-destination memory in immersive VR contexts, is novel. To be expanded by rq_scholar.

---

## Hypothesis

**Primary Hypothesis:**
IRT theta scores and CTT mean scores will converge strongly (r > 0.70 for both source and destination location types), validating RQ 5.5.1 findings are robust to measurement approach and not IRT-specific artifacts.

**Secondary Hypotheses:**

1. Cohen's kappa for LMM fixed effects agreement will exceed 0.60 threshold, indicating substantial structural agreement between IRT-based and CTT-based trajectory models
2. Overall classification agreement across measurement approaches will exceed 80%
3. Convergence strength may be similar for source and destination location types (both r > 0.70), indicating measurement robustness holds for both memory types

**Theoretical Rationale:**

The IRT-CTT convergence trilogy (RQs 5.2.4 for Domains, 5.3.5 for Paradigms, 5.4.4 for Congruence) established a consistent pattern: despite fundamental differences in psychometric frameworks (IRT models item-level parameters and latent traits, CTT aggregates raw scores), both approaches yield highly convergent ability estimates when measuring episodic memory constructs. This suggests the underlying latent constructs are robust and measurement-method-independent.

Source-destination memory should follow the same pattern because: (1) both location types use the same IRT calibration framework (2-factor GRM from RQ 5.5.1), (2) both use purified items passing identical quality criteria (|b| ≤ 3.0, a ≥ 0.4 per Decision D039), (3) both measure spatial episodic memory with binary response format (correct/incorrect location recall).

**Expected Effect Pattern:**

1. **Correlations:** r > 0.70 for both source and destination (strong to very strong association per Cohen, 1988)
2. **Cohen's kappa:** κ > 0.60 (substantial agreement per Landis & Koch, 1977)
3. **Overall agreement:** > 80% classification agreement across IRT and CTT approaches
4. Convergence demonstrated via Bonferroni-corrected significance tests (3 comparisons: source, destination, overall; family-wise alpha = 0.05) per Decision D068
5. Dual p-values reported per Decision D068 (both uncorrected p_raw and Bonferroni-corrected p_bonferroni)

**Acknowledgment - Restriction of Range:**
Item purification restricts variance in both IRT and CTT scores by removing items with extreme difficulty or low discrimination. This restriction of range may attenuate observed correlations between IRT theta and CTT mean scores. Sensitivity analysis will compare correlations using full vs purified item sets to quantify this effect.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - **EXCLUDED** from this RQ

- [x] **Where** (Spatial Location)
  - [x] **-U- tags** (pick-up / source location)
  - [x] **-D- tags** (put-down / destination location)
  - [ ] `-L-` tags (legacy static location) - **EXCLUDED**
  - **Disambiguation:** This RQ uses the source-destination spatial memory framework, distinguishing between pick-up locations (-U-) encoded during object acquisition versus put-down locations (-D-) encoded during object placement. This is a novel factor structure for Chapter 5, introduced in Type 5.5 RQs.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - **EXCLUDED** from this RQ

**Inclusion Rationale:**

Source-destination spatial memory is the focus of this RQ. Only Where domain items with -U- (source) and -D- (destination) tags are included. This follows the factor structure established in RQ 5.5.1, which demonstrated a source-destination memory dissociation (source > destination accuracy) attributed to encoding depth, schema support, and goal discounting mechanisms.

**Exclusion Rationale:**

- **What domain (-N-):** Object identity is orthogonal to spatial location type. What memory measures "which object" while source-destination measures "where was it."
- **When domain (-O-):** Temporal order memory is separate from spatial location memory.
- **Static location (-L-):** Legacy tags from earlier design, not distinguished by source vs destination, thus excluded from source-destination analyses.
- **Non-interactive paradigms (RFR, TCR):** Room-level recall tasks don't involve pick-up/put-down actions, so source-destination distinction doesn't apply.

---

## Analysis Approach

**Analysis Type:**
IRT-CTT Convergence Validation. Uses IRT theta scores (from RQ 5.5.1) and CTT mean scores (computed in this RQ) to assess measurement method robustness. Employs correlation analysis with significance testing, parallel LMM fitting with fixed effects comparison, and assumption validation.

**High-Level Workflow:**

**Step 0:** Load IRT theta scores, TSVR time mapping, and purified items list from RQ 5.5.1 dependency (results/ch5/5.5.1/). Filter raw response data (data/cache/dfData.csv) to purified -U- and -D- items only (items that passed IRT quality criteria in RQ 5.5.1).

**Step 1:** Compute CTT mean scores per participant × test × location type. For each observation (UID, test, location type), calculate mean of binary responses (0/1) across purified items. Output: 800 rows (100 participants × 4 tests × 2 location types), CTT scores in [0,1] range.

**Step 2:** Pearson correlations between IRT theta and CTT mean scores, stratified by location type (source, destination). Test significance with Bonferroni correction (3 comparisons: source, destination, overall; family-wise alpha = 0.05) per Decision D068. Test convergence criteria: r > 0.70 (strong), r > 0.90 (exceptional). Report dual p-values per Decision D068 (both uncorrected p_raw and Bonferroni-corrected p_bonferroni).

**Step 3:** Fit parallel LMMs using identical model formula for IRT theta and CTT mean scores. Model formula: score ~ LocationType × log_TSVR + (log_TSVR | UID), REML=False. If either model fails convergence, simplify both identically (remove random slopes, use random intercepts only). Extract fixed effects for both models.

**Step 4:** Validate LMM assumptions for both IRT-based and CTT-based models using comprehensive validation procedure:
- **(1) Linearity:** Residuals vs fitted plot, expect random scatter around y=0
- **(2) Homoscedasticity:** Scale-location plot, Breusch-Pagan test (p > 0.05)
- **(3) Normality of residuals:** Q-Q plot, Shapiro-Wilk test (p > 0.05 or visual assessment for n>50)
- **(4) Normality of random effects:** Q-Q plot for BLUPs, Shapiro-Wilk test
- **(5) Independence:** Residuals vs observation order plot, Durbin-Watson test (1.5-2.5 acceptable)
- **(6) No multicollinearity:** VIF < 10 for all predictors
- **(7) Influential observations:** Cook's distance < 1.0

**Remedial Action for Bounded CTT Data:**
CTT mean scores are bounded [0,1], which may violate normality and homoscedasticity assumptions. If assumption violations are detected:
- **Primary remedy:** Report violations and interpret LMM results with caution
- **Secondary remedy:** Fit GLMM with logit link (binomial family) as sensitivity analysis
- **Tertiary remedy:** Apply arcsine square root transformation to CTT scores

Document all violations and remedial actions taken. Output: assumption validation comparison table with pass/fail status per criterion.

**Step 5:** Compare fixed effects between IRT-based and CTT-based LMMs. Compute Cohen's kappa for agreement on coefficient signs and significance (threshold κ > 0.60 for substantial agreement per Landis & Koch, 1977). Compute overall classification agreement (percentage of coefficients with matching direction and significance). Report dual p-values per Decision D068.

**Step 6:** Compare model fit via AIC and BIC. Compute ΔAIC and ΔBIC between IRT-based and CTT-based models. Per Burnham & Anderson (2002): ΔAIC < 2 indicates equivalent fit, 2-10 indicates some support for better model, >10 indicates strong support.

**Step 7:** Prepare scatterplot data: IRT theta vs CTT mean score for all 800 observations, colored by location type (source, destination). Include regression lines per location type.

**Step 8:** Prepare trajectory comparison data: Aggregate mean IRT theta and mean CTT score per location type × test session (8 rows total: 2 location types × 4 tests). Include 95% confidence intervals. This visualizes whether IRT and CTT yield parallel forgetting trajectories.

**Expected Outputs:**

- data/step00_irt_theta_from_rq551.csv (800 rows: IRT theta scores from RQ 5.5.1)
- data/step00_purified_items_from_rq551.csv (list of items retained after IRT purification)
- data/step01_ctt_scores.csv (800 rows: UID, test, location_type, ctt_mean_score)
- results/step02_correlations.csv (3 rows: Source, Destination, Overall; columns: r, p_raw, p_bonferroni, r_threshold_70, r_threshold_90)
- results/step03_irt_lmm_summary.txt (LMM summary for IRT theta)
- results/step03_ctt_lmm_summary.txt (LMM summary for CTT mean scores)
- results/step04_assumptions_comparison.csv (assumption validation results for both models)
- results/step05_coefficient_comparison.csv (12 columns: term, irt_coef, irt_se, irt_p, ctt_coef, ctt_se, ctt_p, sign_match, sig_match, dual_p_raw, dual_p_bonferroni)
- results/step05_agreement_metrics.csv (Cohen's kappa, overall agreement percentage)
- results/step06_model_fit_comparison.csv (AIC, BIC, ΔAIC, ΔBIC for IRT vs CTT models)
- plots/step07_scatterplot_data.csv (800 rows: UID, test, location_type, irt_theta, ctt_score)
- plots/step08_trajectory_data.csv (16 rows: 2 location types × 4 tests × 2 methods [IRT, CTT]; columns: location_type, test, method, mean_score, ci_lower, ci_upper)

**Success Criteria:**

- **Dependency validation:** RQ 5.5.1 complete, outputs exist and loadable
- **Correlations:** All three correlations (source, destination, overall) r > 0.70; Holm-Bonferroni correction applied correctly
- **Cohen's kappa:** κ > 0.60 for fixed effects agreement (substantial agreement)
- **Overall agreement:** ≥ 80% of fixed effects show matching direction and significance
- **Model convergence:** Both IRT-based and CTT-based LMMs converge with identical model structure (if simplification needed, applied to both)
- **Dual p-values:** All statistical tests report both uncorrected (p_raw) and Bonferroni-corrected (p_bonferroni) p-values per Decision D068
- **Output completeness:** All expected files created with correct row/column counts
- **Data integrity:** CTT scores in [0,1], no missing values, scatterplot data includes all 800 observations, trajectory data includes all 16 rows (2 locations × 4 tests × 2 methods)

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.5.1 IRT outputs and raw data filtered to purified items)

### DERIVED Data Source:

**Source RQ:**
RQ 5.5.1 (Source-Destination Trajectories - ROOT RQ for Type 5.5)

**File Paths:**

From RQ 5.5.1:
- results/ch5/5.5.1/data/step03_theta_scores.csv (IRT theta scores, 400 rows: 100 participants × 4 tests, columns: UID, test, theta_source, se_source, theta_destination, se_destination)
- results/ch5/5.5.1/data/step02_purified_items.csv (list of items retained after IRT purification with Decision D039 criteria: |b| ≤ 3.0, a ≥ 0.4)
- results/ch5/5.5.1/data/step00_tsvr_mapping.csv (time-since-VR hours, 400 rows: UID, test, TSVR_hours)

From raw data:
- data/cache/dfData.csv (master VR dataset, binary responses to all items, used to compute CTT scores on purified item sets)

**Dependencies:**

RQ 5.5.1 must complete through Step 3 (IRT Pass 2 re-calibration on purified items, theta score extraction) before this RQ can run. Specifically:
1. IRT 2-factor calibration complete (source/destination factors)
2. Item purification complete (Decision D039 applied)
3. Theta scores extracted for all 100 participants × 4 tests × 2 location types

This RQ does NOT require RQ 5.5.1 Steps 4-7 (LMM trajectory modeling), only the IRT calibration outputs (Steps 0-3).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.5.1)
- [ ] No exclusions

**Items:**
- [x] Purified item subset from RQ 5.5.1 (items passing |b| ≤ 3.0 AND a ≥ 0.4 criteria)
- [x] Source location items (-U- tags, pick-up locations)
- [x] Destination location items (-D- tags, put-down locations)
- [ ] Full item set - **EXCLUDED** (CTT computed on purified items only, matching IRT calibration item set)
- [ ] Static location items (-L-) - **EXCLUDED**
- Expected: 20-30 items retained per location type after purification (total ~50-60 items from original ~72 -U-/-D- items)

**Tests:**
- [x] All 4 test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- [ ] No exclusions

**Paradigms:**
- [x] Interactive paradigms only (IFR, ICR, IRE - inherited from RQ 5.5.1)
- [ ] Room-level recall (RFR, TCR) - **EXCLUDED**

**Rationale:**
This RQ validates that RQ 5.5.1 findings (source-destination memory dissociation) replicate when using CTT mean scores instead of IRT theta scores. CTT must be computed on the SAME item set as IRT (purified items) for fair comparison. Using full item set for CTT would introduce measurement artifacts (non-psychometric items that failed IRT quality checks).

---
