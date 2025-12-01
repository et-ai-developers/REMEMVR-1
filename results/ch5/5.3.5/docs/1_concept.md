# RQ 5.3.5: IRT-CTT Convergence for Paradigm-Specific Forgetting

**Chapter:** 5
**Type:** Paradigms
**Subtype:** IRT-CTT Convergence
**Full ID:** 5.3.5

---

## Research Question

**Primary Question:**
Do IRT theta scores and CTT mean scores yield the same conclusions about paradigm-specific forgetting trajectories for Free Recall, Cued Recall, and Recognition paradigms?

**Scope:**
This RQ examines measurement convergence across three retrieval paradigms using IRT-derived ability estimates (theta) and Classical Test Theory mean scores computed from the same item set. Sample: N=100 participants x 4 test sessions (T1, T2, T3, T4; Days 0, 1, 3, 6) x 3 paradigms (Free Recall, Cued Recall, Recognition) = 1200 observations. Analyses compare IRT vs CTT at three levels: (1) score-level correlations per paradigm, (2) parallel LMM trajectory models, and (3) fixed effect agreement metrics.

**Theoretical Framing:**
This RQ addresses methodological robustness of paradigm-specific forgetting findings (RQ 5.3.1). Convergent evidence across measurement approaches (IRT vs CTT) strengthens confidence that paradigm differences reflect genuine psychological constructs rather than measurement artifacts. Discrepancies would indicate sensitivity to scaling assumptions and require cautious interpretation.

---

## Theoretical Background

**Relevant Theories:**
- **Measurement Theory:** IRT assumes non-linear item response functions and provides interval-level ability estimates, while CTT assumes parallel tests and provides ordinal proportion-correct scores. Convergence across methods demonstrates robustness to scaling assumptions.
- **Classical Test Theory (CTT):** Observed score = true score + error. Simple proportion-correct scoring, assumes equal item weights and linear scoring.
- **Item Response Theory (IRT):** Models probability of correct response as function of latent ability (theta) and item parameters. Provides interval-level measurement and accounts for item difficulty/discrimination.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Strong convergence expected for robust psychological phenomena. IRT theta and CTT mean scores should correlate highly (r > 0.70) and yield equivalent conclusions about paradigm-specific forgetting trajectories. Divergence would indicate measurement-dependent effects requiring further investigation.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
IRT theta scores and CTT mean scores will converge, demonstrating robustness of paradigm-specific forgetting findings (RQ 5.3.1) to measurement approach. Expected convergence criteria: (1) Pearson correlations r > 0.70 per paradigm (strong), with exceptional convergence r > 0.90; (2) Cohen's kappa > 0.60 for fixed effect agreement (substantial agreement); (3) Agreement on statistical significance >= 80% of fixed effects.

**Secondary Hypotheses:**
None - convergence analysis is the sole focus.

**Theoretical Rationale:**
Paradigm differences in forgetting (Free > Cued > Recognition; RQ 5.3.1) should be robust to measurement approach if they reflect genuine retrieval processes rather than scaling artifacts. Strong IRT-CTT convergence indicates paradigm effects are not dependent on IRT's non-linear transformations or item weighting. Weak convergence would suggest paradigm findings require cautious interpretation.

**Expected Effect Pattern:**
- Score-level: Pearson r > 0.70 per paradigm (Free Recall, Cued Recall, Recognition), p < 0.05 after Holm-Bonferroni correction
- Model-level: Parallel LMMs (identical formula) converge for both IRT and CTT measurements
- Coefficient-level: Cohen's kappa > 0.60 for fixed effect significance agreement, agreement percentage >= 80%
- Model fit: AIC/BIC comparison shows similar relative fit across IRT vs CTT (ΔAIC < 2 indicates equivalent fit)

---

## Memory Domains

**Domains Examined:**

**Paradigm-Based Grouping (Not Domain-Based):**

This RQ uses paradigm-based factors (Free Recall, Cued Recall, Recognition), not traditional WWW domains (What/Where/When). However, paradigm items implicitly assess all three domains:

- [x] **Free Recall (IFR)** - Item Free Recall paradigm
  - Tag Pattern: `IFR-*` items
  - Retrieval: Self-initiated, no cues
  - All WWW domains assessed within IFR items

- [x] **Cued Recall (ICR)** - Item Cued Recall paradigm
  - Tag Pattern: `ICR-*` items
  - Retrieval: Category cue provided
  - All WWW domains assessed within ICR items

- [x] **Recognition (IRE)** - Item Recognition paradigm
  - Tag Pattern: `IRE-*` items
  - Retrieval: Target presented with foils
  - All WWW domains assessed within IRE items

**Inclusion Rationale:**
IRT theta scores derived from RQ 5.3.1 three-factor model (Free/Cued/Recognition factors). CTT mean scores computed on same purified item set (post-IRT purification from RQ 5.3.1) to ensure fair comparison. Interactive paradigms only (IFR/ICR/IRE); passive paradigms excluded (RFR, TCR, RRE).

**Exclusion Rationale:**
- **Room Free Recall (RFR):** Not part of RQ 5.3.1 paradigm analysis
- **Target Cued Recall (TCR):** Not part of RQ 5.3.1 paradigm analysis
- **Room Recognition (RRE):** Not part of RQ 5.3.1 paradigm analysis

---

## Analysis Approach

**Analysis Type:**
Methodological convergence analysis: Pearson correlations, parallel Linear Mixed Models (LMMs), coefficient agreement metrics (Cohen's kappa), model comparison (AIC/BIC)

**High-Level Workflow:**

**Step 0:** Load IRT theta scores, TSVR mapping, and purified items from RQ 5.3.1. Verify dependency: RQ 5.3.1 must have completed IRT calibration (Steps 1-3) and produced theta scores for Free Recall, Cued Recall, and Recognition paradigms.

**Step 1:** Compute CTT mean scores per UID x test x paradigm using purified item set (post-IRT purification from RQ 5.3.1). Filter raw data from dfData.csv to retained items only. Calculate proportion correct per participant-test-paradigm combination (1200 scores: 100 participants x 4 tests x 3 paradigms).

**Step 2:** Compute Pearson correlations between IRT theta and CTT mean scores separately for each paradigm (Free Recall, Cued Recall, Recognition) plus overall correlation. Test correlation strength against thresholds (r > 0.70 strong, r > 0.90 exceptional). Apply Holm-Bonferroni correction for 4 correlations (3 paradigms + overall). Report dual p-values per Decision D068 (p_uncorrected and p_bonferroni).

**Step 3:** Fit parallel LMMs using identical model formula for IRT theta vs CTT mean scores. Model formula determined by best-fitting model from RQ 5.3.1 (likely includes Paradigm x Time interactions with random slopes). If either model fails to converge, simplify both models equally (remove random slopes, then random effects) to maintain structural equivalence. Report convergence status and any simplifications applied.

**Step 4:** Validate LMM assumptions for both IRT and CTT models: (1) linearity, (2) normality of residuals, (3) homoscedasticity, (4) independence of residuals, (5) normality of random effects, (6) absence of influential outliers. Document assumption violations and compare violation patterns across IRT vs CTT.

**Step 5:** Compare fixed effects between IRT and CTT models. Extract all fixed effect coefficients with standard errors, z-values, and p-values. Classify each effect as significant (p < 0.05) or non-significant. Compute Cohen's kappa for agreement on significance classifications (threshold: kappa > 0.60 indicates substantial agreement). Compute percentage agreement. Report dual p-values per Decision D068.

**Step 6:** Compare model fit between IRT and CTT using AIC and BIC. Compute ΔAIC and ΔBIC (IRT - CTT). Interpret per Burnham & Anderson: |Δ| < 2 = equivalent fit, 2-10 = moderate evidence, > 10 = strong evidence for better model. Expected: equivalent fit (both capture same underlying trajectories).

**Step 7:** Prepare scatterplot data for visual inspection of IRT-CTT convergence. Create dataset with 1200 rows (100 participants x 4 tests x 3 paradigms) containing: UID, test, paradigm, IRT_theta, CTT_mean, fitted values from both models. For plotting: scatterplot IRT vs CTT colored by paradigm, with y=x reference line and paradigm-specific regression lines.

**Step 8:** Prepare trajectory comparison data showing observed means and model predictions from both IRT and CTT models. Create aggregated dataset with paradigm x test means (12 rows: 3 paradigms x 4 tests) containing: observed IRT means, observed CTT means, IRT model predictions, CTT model predictions, confidence intervals. For plotting: two-panel figure (IRT trajectories vs CTT trajectories) showing convergence of forgetting patterns.

**Expected Outputs:**
- results/step02_correlations.csv (4 rows: 3 paradigms + overall, columns: paradigm, n, r, p_uncorrected, p_bonferroni, threshold_0.70, threshold_0.90)
- results/step03_irt_lmm_summary.txt (IRT model summary with convergence status)
- results/step03_ctt_lmm_summary.txt (CTT model summary with convergence status)
- results/step04_assumptions_comparison.csv (assumption violations for IRT vs CTT models)
- results/step05_coefficient_comparison.csv (12 columns: effect_name, IRT_coef, IRT_se, IRT_z, IRT_p, IRT_sig, CTT_coef, CTT_se, CTT_z, CTT_p, CTT_sig, agreement)
- results/step05_agreement_metrics.csv (Cohen's kappa, percentage agreement, interpretation)
- results/step06_model_fit_comparison.csv (AIC, BIC, ΔAIC, ΔBIC, interpretation)
- plots/step07_scatterplot_data.csv (1200 rows: UID, test, paradigm, IRT_theta, CTT_mean, IRT_fitted, CTT_fitted)
- plots/step08_trajectory_data.csv (24 rows: 3 paradigms x 4 tests x 2 measurement types, columns: paradigm, test, measurement_type, observed_mean, model_prediction, CI_lower, CI_upper)

**Success Criteria:**
- All Pearson correlations r > 0.70 (strong convergence threshold met)
- Cohen's kappa > 0.60 (substantial agreement on fixed effect significance)
- Agreement on statistical significance >= 80% of fixed effects
- Both IRT and CTT models converge with identical structure (or both simplified equally)
- Dual p-values present per Decision D068 (p_uncorrected and p_bonferroni reported)
- No NaN values in correlation or coefficient comparison tables
- Plot data files exist with correct row counts (1200 for scatterplot, 24 for trajectories)

---

## Practice Effects Consideration

### Repeated Testing Design

The 4-session design (Days 0, 1, 3, 6) creates potential practice effects that affect both IRT and CTT scores:
- Literature documents 13.3% improvement in episodic memory with repeated testing (Goldberg et al., BMC Neuroscience)
- Practice effects may differentially affect IRT vs CTT if item-level learning occurs

### Differential Item Functioning (DIF) by Test Session

**Consideration:** Items may function differently across test sessions if practice effects create item-specific learning. This could manifest as DIF by session.

**Mitigation:**
- IRT calibration in RQ 5.3.1 uses all sessions pooled, assuming measurement invariance across time
- If DIF suspected, future analyses could test measurement invariance via multi-group IRT
- For this convergence RQ, the key question is whether IRT and CTT yield the same conclusions regardless of any shared practice effects bias

### Interpretation Guidance

If IRT-CTT convergence is high (r > 0.70, kappa > 0.60), this indicates:
- Both measurement approaches capture the same underlying construct
- Conclusions about paradigm-specific forgetting are robust to scaling method
- Any practice effects affect both IRT and CTT similarly

If convergence is low for specific paradigms, this would suggest:
- Paradigm-specific measurement artifacts requiring further investigation
- Potential DIF by test session within that paradigm
- Cautious interpretation of paradigm findings pending measurement validation

### Correlation Threshold Justification

The r > 0.70 threshold for "strong" convergence is based on:
- Cohen's (1988) guidelines for correlation magnitude interpretation
- Convergent validity standards in psychometrics (Campbell & Fiske, 1959)
- Fornell & Larcker (1981) AVE criterion suggesting r > 0.70 for discriminant validity
- Prior IRT-CTT convergence literature showing r = 0.85-0.95 for well-constructed scales

The exceptional threshold (r > 0.90) indicates near-identical rank ordering of participants.

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.3.1 outputs and raw data)

### DERIVED Data Source:

**Source RQ:**
RQ 5.3.1 (Paradigm-Specific Trajectories)

**File Paths:**
- results/ch5/5.3.1/data/step03_theta_scores.csv (IRT theta scores after Pass 2 calibration, 400 rows with 3 paradigm columns: theta_IFR, theta_ICR, theta_IRE)
- results/ch5/5.3.1/data/step00_tsvr_mapping.csv (time mapping: UID, TEST, TSVR_hours, Days)
- results/ch5/5.3.1/data/step02_purified_items.csv (retained items post-purification, ~40-80 items)
- data/cache/dfData.csv (raw binary responses for CTT computation)

**Dependencies:**
RQ 5.3.1 must complete Steps 0-3 before this RQ can run:
- Step 0: Data extraction with paradigm Q-matrix (IFR/ICR/IRE factors)
- Step 1: IRT Pass 1 calibration (3-factor GRM model)
- Step 2: Item purification per Decision D039 (|b| <= 3.0, a >= 0.4)
- Step 3: IRT Pass 2 re-calibration on purified items (final theta scores)

**CTT Data Requirements:**
In addition to RQ 5.3.1 outputs, this RQ extracts raw response data from dfData.csv filtered to purified items. CTT mean scores computed as proportion correct using only items retained after IRT purification (fair comparison: same item set for both IRT and CTT).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 5.3.1 (inherited inclusion criteria, no additional exclusions)

**Items:**
- [x] Purified items only (post-IRT purification from RQ 5.3.1)
- [x] Interactive paradigms: IFR (Item Free Recall), ICR (Item Cued Recall), IRE (Item Recognition)
- [ ] Passive paradigms EXCLUDED: RFR (Room Free Recall), TCR (Target Cued Recall), RRE (Room Recognition)
- Expected: ~40-80 items retained (varies by purification outcome), minimum 10 items per paradigm required

**Tests:**
- [x] All 4 test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Time variable: TSVR_hours (actual hours since encoding, accounts for circadian and individual timing differences)

**Notes:**
- IRT theta scores from RQ 5.3.1 are on logit scale (typically range -3 to +3)
- CTT mean scores are proportion correct (range 0 to 1)
- Both measurements derived from identical item set (purified items)
- Paradigm structure: 3 separate scores per participant-test combination (Free, Cued, Recognition)
- Total observations: 1200 (100 participants x 4 tests x 3 paradigms)

---
