# RQ 5.3.6: Purified CTT Effects (Paradigms)

**Chapter:** 5
**Type:** Paradigms
**Subtype:** Purified CTT Effects
**Full ID:** 5.3.6

---

## Research Question

**Primary Question:**
If we compute CTT (Classical Test Theory) scores using only IRT-retained items (post-purification), do conclusions differ from full-item CTT for paradigm-specific forgetting trajectories (Free Recall, Cued Recall, Recognition)?

**Scope:**
This RQ compares two CTT scoring approaches across N=100 participants x 4 test sessions = 400 observations. Compares Full CTT (all items pre-purification) vs Purified CTT (only items retained after IRT purification per Decision D039: a >= 0.4, |b| <= 3.0). Examines paradigm-specific scores (IFR/ICR/IRE) across 6-day retention interval (T1, T2, T3, T4; nominal Days 0, 1, 3, 6).

**Theoretical Framing:**
This RQ tests measurement robustness by comparing two scoring approaches. Item purification removes psychometrically problematic items (low discrimination, extreme difficulty), potentially reducing measurement noise. If purified CTT shows higher correlation with IRT theta and better LMM fit (lower AIC), this validates the purification process and demonstrates improved measurement precision supports the same theoretical conclusions about paradigm-specific forgetting.

---

## Theoretical Background

**Relevant Theories:**
- **Classical Test Theory (CTT):** Observed score = true score + error. Total score (mean of dichotomous items) is unbiased estimator of latent ability. Assumes equal item discrimination and parallel test forms.
- **Item Response Theory (IRT):** Models item-level response probabilities using item parameters (discrimination a, difficulty b). Graded Response Model (GRM) used for polytomous responses. Item purification removes items violating IRT assumptions.
- **Measurement Invariance:** Multiple measurement approaches (IRT theta vs CTT mean) should yield convergent conclusions if measuring the same latent construct. Discrepancies may indicate method-specific artifacts.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Item purification (Decision D039) removes items with poor psychometric properties (a < 0.4 indicating low discrimination, |b| > 3.0 indicating extreme difficulty). These problematic items contribute measurement error. Purified CTT should:
1. Show higher correlation with IRT theta compared to full CTT (convergent validity)
2. Show better internal consistency (higher Cronbach's alpha)
3. Yield better LMM model fit (lower AIC) due to reduced measurement noise
4. Replicate paradigm-specific forgetting conclusions from IRT-based analyses

**Literature Gaps:**
Most episodic memory research uses either CTT or IRT exclusively. Few studies compare whether item purification (standard in IRT workflows) improves CTT scoring. This RQ provides empirical evidence for whether purification benefits translate to CTT measurement precision.

---

## Hypothesis

**Primary Hypothesis:**
Purified CTT will show higher correlation with IRT theta compared to Full CTT for paradigm-specific scores, demonstrating item purification removes measurement noise. Expected: delta_r (Purified - Full correlation) ~ +0.02 to +0.05 for each paradigm (Free Recall, Cued Recall, Recognition).

**Secondary Hypotheses:**
1. Purified CTT will show higher internal consistency (Cronbach's alpha) compared to Full CTT
2. Purified CTT-based LMMs will show better model fit (lower AIC) compared to Full CTT-based LMMs
3. Both Full CTT and Purified CTT will replicate the paradigm-specific forgetting pattern (Free Recall > Cued Recall > Recognition forgetting rates)

**Theoretical Rationale:**
Item purification removes items with low discrimination (a < 0.4), which contribute noise to total scores. Removing extreme difficulty items (|b| > 3.0) reduces floor/ceiling effects. IRT theta estimates incorporate item-level precision, so purified items should align better with theta. CTT scoring treats all items equally, so removing noisy items should improve CTT precision and convergence with IRT.

**Expected Effect Pattern:**
- Correlations: All paradigms show r > 0.70 for both Full and Purified CTT (strong convergence). Purified CTT shows delta_r ~ +0.02 improvement (significant via Steiger's z-test with Bonferroni correction).
- Reliability: Purified CTT Cronbach's alpha approximately equal to or slightly higher than Full CTT (fewer items but better discrimination).
- Model Fit: Purified CTT LMMs show AIC < Full CTT LMMs by delta_AIC > 2 (meaningful improvement per Burnham & Anderson).
- Fixed Effects: Cohen's kappa > 0.60 for coefficient agreement between Full CTT and Purified CTT models (substantial agreement on paradigm effects).

---

## Memory Domains

**Domains Examined:**

This RQ does NOT examine domain-specific patterns (What/Where/When). Instead, it examines paradigm-specific patterns:

- **Paradigms:**
  - [x] **Item Free Recall (IFR):** Self-initiated retrieval without cues
  - [x] **Item Cued Recall (ICR):** Retrieval with environmental context cues
  - [x] **Item Recognition (IRE):** Familiarity-based discrimination

**Domain Tags:**
- Paradigm codes: IFR, ICR, IRE (interactive paradigms only)
- Excludes: RFR (Room Free Recall), TCR (Time Cued Recall), RRE (Room Recognition)

**Inclusion Rationale:**
All three interactive paradigms included to test whether item purification effects generalize across retrieval support levels. Free Recall (most demanding) may show largest purification benefit. Recognition (familiarity-based) may show smallest benefit if purification primarily affects recollection-based items.

**Exclusion Rationale:**
Room-based paradigms (RFR, TCR, RRE) excluded per RQ 5.3.1 design. This RQ inherits the same paradigm selection to ensure CTT-IRT comparison uses identical item pools.

---

## Analysis Approach

**Analysis Type:**
Classical Test Theory (CTT) scoring comparison with IRT validation. Includes psychometric analysis (Cronbach's alpha, Steiger's z-test for correlation differences), Linear Mixed Models (LMM) for trajectory modeling, and model comparison (AIC).

**High-Level Workflow:**

**Step 0:** Load RQ 5.3.1 outputs (purified items, IRT theta scores, TSVR mapping) and validate dependency completion

**Step 1:** Map retained vs removed items by paradigm
- Create item mapping table showing which items retained after RQ 5.3.1 purification
- Stratify by paradigm (IFR, ICR, IRE)
- Compute purification retention rate per paradigm

**Step 2:** Compute Full CTT scores (all items pre-purification)
- Extract raw response data from data/cache/dfData.csv for all paradigm items
- Compute mean scores per UID x Test x Paradigm using all items
- Output: 400 rows (100 participants x 4 tests) x 3 paradigm score columns

**Step 3:** Compute Purified CTT scores (retained items only)
- Filter raw data to items retained in RQ 5.3.1 purification
- Compute mean scores per UID x Test x Paradigm using purified items only
- Output: 400 rows x 3 paradigm score columns

**Step 4:** Reliability assessment with Cronbach's alpha and bootstrap confidence intervals
- Compute Cronbach's alpha for Full CTT and Purified CTT per paradigm
- Bootstrap 95% CIs (10,000 iterations)
- Compare alpha_purified vs alpha_full per paradigm

**Step 5:** Correlation analysis with Steiger's z-test for dependent correlations
- Correlate Full CTT with IRT theta per paradigm
- Correlate Purified CTT with IRT theta per paradigm
- Steiger's z-test for difference: r_purified - r_full (dependent correlations sharing theta)
- Holm-Bonferroni correction for 3 paradigms
- Report dual p-values per Decision D068 (p_uncorrected, p_bonferroni)
- Test thresholds: r > 0.70 (strong), r > 0.90 (exceptional)

**Step 6:** Z-standardize all measurements (IRT theta, Full CTT, Purified CTT) for LMM comparison
- Grand-mean center and scale to z-scores
- Ensures comparable coefficients across measurement types

**Step 7:** Fit parallel LMMs on z-standardized scores; compare AIC per Burnham & Anderson
- Fit 3 LMMs with identical formula: Score ~ Time + (Time | UID), REML=False
  - Model 1: IRT theta (reference)
  - Model 2: Full CTT
  - Model 3: Purified CTT
- Extract AIC per model
- Compute delta_AIC: AIC_full - AIC_purified (positive = purified better)
- Threshold: delta_AIC > 2 indicates meaningful improvement
- Extract fixed effect coefficients and compare Cohen's kappa

**Step 8:** Prepare correlation comparison and AIC comparison plot data
- Correlation comparison: 6 rows (3 paradigms x 2 CTT types) with r, CI_lower, CI_upper
- AIC comparison: 3 rows (3 paradigms) with AIC_full, AIC_purified, delta_AIC

**Expected Outputs:**
- data/step01_item_mapping.csv (item-level table: item_id, paradigm, retained_flag)
- data/step02_ctt_full_scores.csv (400 rows x 5 cols: UID, test, IFR_full, ICR_full, IRE_full)
- data/step03_ctt_purified_scores.csv (400 rows x 5 cols: UID, test, IFR_purified, ICR_purified, IRE_purified)
- data/step04_reliability_assessment.csv (3 rows: paradigm, alpha_full, alpha_full_CI_lower, alpha_full_CI_upper, alpha_purified, alpha_purified_CI_lower, alpha_purified_CI_upper)
- data/step05_correlation_analysis.csv (3 rows: paradigm, r_full, r_purified, delta_r, steiger_z, p_uncorrected, p_bonferroni)
- data/step07_lmm_model_comparison.csv (3 rows: paradigm, AIC_irt, AIC_full, AIC_purified, delta_AIC_full_purified)
- plots/step08_correlation_comparison_data.csv (6 rows: paradigm, ctt_type, r, CI_lower, CI_upper)
- plots/step08_aic_comparison_data.csv (duplicate of step07 output for plotting)

**Success Criteria:**
- Item mapping correct: All items assigned to paradigm, retained flag = TRUE/FALSE
- CTT scores in [0,1]: All mean scores valid proportions
- Correlations with dual p-values: All correlations present with both p_uncorrected and p_bonferroni (Decision D068)
- All LMMs converge: convergence flag = TRUE for all 3 models per paradigm
- AIC finite and positive: All models produce valid AIC values
- Plot data: Correct row counts (6 for correlations, 3 for AIC), CI_lower < CI_upper

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.3.1 outputs for purified items and IRT theta) + RAW (from dfData.csv for full-item CTT computation)

### DERIVED Data Source:

**Source RQ:**
RQ 5.3.1 (Paradigm-Specific Trajectories)

**File Paths:**
- results/ch5/5.3.1/data/step02_purified_items.csv (items retained after IRT purification)
- results/ch5/5.3.1/data/step03_theta_scores.csv (IRT ability estimates per UID x Test x Paradigm)
- results/ch5/5.3.1/data/step00_tsvr_mapping.csv (time since encoding mapping)
- results/ch5/5.3.1/data/step00_irt_input.csv (dichotomized response data - may be used to identify original item pool)

**Dependencies:**
RQ 5.3.1 must complete Steps 0-3:
- Step 0: Data extraction from dfData.csv (IFR/ICR/IRE paradigm items)
- Step 1: IRT Pass 1 calibration (3-dimensional GRM)
- Step 2: Item purification (Decision D039: a >= 0.4, |b| <= 3.0)
- Step 3: IRT Pass 2 re-calibration on purified items

This RQ requires the purified item list (step02) and final theta scores (step03) before proceeding.

### RAW Data Source (for Full CTT):

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- Paradigm codes: IFR, ICR, IRE (interactive paradigms)
- All items from original item pool (pre-purification)
- TQ_* response columns (dichotomized: TQ < 1 -> 0, >= 1 -> 1 per RQ 5.3.1 Step 0 specification)

**Extraction Method:**
Step 2 extracts from dfData.csv using the FULL item pool (before purification) to compute Full CTT scores. This requires identifying all items used in RQ 5.3.1 Step 0 (not just retained items).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- Inherited from RQ 5.3.1

**Items:**
- **Full CTT (Step 2):** All paradigm items from RQ 5.3.1 Step 0 (pre-purification, approximately 40-80 items total across IFR/ICR/IRE)
- **Purified CTT (Step 3):** Only items retained in RQ 5.3.1 Step 2 purification (expected 40-80 items after Decision D039 purification)
- Subset determined by RQ 5.3.1 purification outcomes
- Excludes: RFR, TCR, RRE paradigms (not in RQ 5.3.1 scope)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Inherited from RQ 5.3.1

---
