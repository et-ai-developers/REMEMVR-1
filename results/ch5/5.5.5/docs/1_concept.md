# RQ 5.5.5: Purified CTT Effects for Source-Destination Memory

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** Purified CTT Effects
**Full ID:** 5.5.5

---

## Research Question

**Primary Question:**
Does IRT-based item purification improve CTT-IRT correlation for source (-U-) and destination (-D-) scores, and does the purification-trajectory paradox replicate?

**Scope:**
This RQ examines the measurement convergence between IRT and CTT approaches for source (pick-up location, -U- tags) and destination (put-down location, -D- tags) memory. Sample: N=100 participants × 4 tests = 400 observations per location type (800 total observations). Full CTT uses all ~36 items (18 per location type), while Purified CTT uses only IRT-retained items (~25-32 items after purification). Compares correlation with IRT theta and LMM model fit (AIC) between Full and Purified CTT versions.

**Theoretical Framing:**
This RQ tests the purification-trajectory paradox: whether IRT-based item purification (removing items with extreme difficulty |b| > 3.0 or low discrimination a < 0.4) improves measurement quality for both correlation and trajectory modeling. The paradox—discovered in RQ 5.2.5 (Domains), replicated in 5.3.6 (Paradigms) and 5.4.5 (Congruence)—suggests that removed items contribute noise to correlations but provide variance useful for trajectory estimation. This RQ provides the 4th independent test, extending the paradox to source-destination memory.

---

## Theoretical Background

**Relevant Theories:**

- **Classical Test Theory (CTT):** Sum scores assume equal item weighting and parallel measurement error. Purification removes psychometrically weak items to reduce error variance and improve measurement precision (Lord & Novick, 1968).

- **Item Response Theory (IRT):** Ability estimates (theta) are sample-independent and account for item difficulty and discrimination. Item purification via IRT parameters improves scale psychometric properties by removing items that don't fit the measurement model (Embretson & Reise, 2000).

- **Measurement Convergence:** High correlation between IRT and CTT (r > 0.70) indicates robustness to measurement approach. Purification should increase convergence by removing noise sources (Reise & Waller, 2009).

- **Purification-Trajectory Paradox:** Empirical pattern discovered in Chapter 5 where IRT-purified CTT shows: (1) HIGHER correlation with IRT theta (improved measurement precision), BUT (2) WORSE LMM trajectory fit (higher AIC). Mechanism: Removed items contribute measurement noise (reducing correlation) but capture individual differences in trajectories (useful variance for LMM). This creates a psychometric tension between cross-sectional reliability and longitudinal validity.

**Key Citations:**

- **Lord, F. M., & Novick, M. R. (1968).** Statistical theories of mental test scores. Addison-Wesley. [CTT foundations]
- **Embretson, S. E., & Reise, S. P. (2000).** Item response theory for psychologists. Lawrence Erlbaum. [IRT foundations]
- **Burnham, K. P., & Anderson, D. R. (2002).** Model selection and multimodel inference: A practical information-theoretic approach. Springer. [AIC guidelines: ΔAIC >2 substantial, >10 decisive]
- **Gorter, R., Fox, J.P., & Twisk, J.W.R. (2015).** Why item response theory should be used for longitudinal questionnaire data analysis in medical research. BMC Medical Research Methodology, 15, 55. [Longitudinal IRT: sum-scores overestimate within-person variance]
- **Perlman, G., & Simms, L.J. (2022).** Establishing thresholds for meaningful within-individual change using longitudinal item response theory. Assessment, 29(6), 1241-1254. [LIRT for trajectory modeling]
- **Salthouse, T.A., et al. (2022).** Parameterizing practice in a longitudinal measurement burst design to dissociate retest effects from developmental change. Psychology and Aging, 37(4), 453-464. [Practice effects confound in repeated testing]
- **Cogn-IQ (2024).** Ceiling and floor effects in psychometric testing. https://www.cogn-iq.org/learn/theory/ceiling-floor-effects/ [CTT bounded scale limitations]

**Theoretical Predictions:**

Based on the established pattern from RQs 5.2.5, 5.3.6, and 5.4.5:

1. **Correlation Improvement:** Purified CTT will show HIGHER correlation with IRT theta than Full CTT for both source and destination memory. Expected effect size: Δr ≈ +0.02 to +0.10 (Steiger's z-test p < 0.05).

2. **Model Fit Degradation:** Despite higher correlation, Purified CTT will show WORSE LMM trajectory fit compared to Full CTT (higher AIC). Expected effect: ΔAIC > +2 (substantial evidence per Burnham & Anderson, 2002).

3. **Location-Type Consistency:** The paradox should replicate for both source (-U-) and destination (-D-) memory, indicating a measurement principle rather than content-specific artifact.

**Literature Gaps:**

The purification-trajectory paradox is an empirical discovery from this project. If RQ 5.5.5 confirms the paradox for source-destination memory, it would represent the 4th independent replication across distinct episodic memory constructs (Domains, Paradigms, Congruence, Source-Destination). This pattern challenges conventional psychometric assumptions that item purification universally improves measurement quality.

---

## Hypothesis

**Primary Hypothesis:**

The purification-trajectory paradox will replicate for source-destination memory:

1. **Correlation Component:** Purified CTT shows HIGHER correlation with IRT theta than Full CTT (Steiger's z-test p < 0.05, Bonferroni-corrected for 2 location types). Expected: Full CTT r ≈ 0.75, Purified CTT r ≈ 0.80, Δr ≈ +0.05.

2. **Model Fit Component:** Purified CTT shows WORSE LMM trajectory fit than Full CTT (higher AIC). Expected: ΔAIC > +2 for both source and destination models, indicating substantial evidence favoring Full CTT for trajectory modeling.

**Secondary Hypotheses:**

1. **Reliability Improvement:** Cronbach's alpha will increase after purification for both location types, indicating improved internal consistency. Expected: Full CTT α ≈ 0.75-0.85, Purified CTT α ≈ 0.80-0.90.

2. **Location-Type Consistency:** The paradox magnitude will be similar for source and destination memory, indicating a general measurement principle rather than location-specific artifact.

**Theoretical Rationale:**

The paradox arises from a psychometric tension:

- **Cross-Sectional Perspective:** IRT purification removes items that don't fit the unidimensional measurement model (high/low difficulty, low discrimination). These items add noise to correlations, reducing measurement precision at single timepoints.

- **Longitudinal Perspective:** Removed items may capture individual differences in change patterns (e.g., certain items show differential forgetting rates). Discarding these items reduces the variance available for modeling trajectories, degrading LMM fit despite improved correlation.

This creates a methodological dilemma: optimizing measurement for reliability (purification) conflicts with optimizing for trajectory validity (retaining variance). If the paradox replicates, it suggests item purification decisions should depend on research goals (cross-sectional vs longitudinal).

**Expected Effect Pattern:**

| Measurement | Correlation with IRT | LMM AIC | Interpretation |
|-------------|---------------------|---------|----------------|
| Full CTT | r ≈ 0.75 | Lower (better fit) | Noisy measurement, rich trajectories |
| Purified CTT | r ≈ 0.80 | Higher (worse fit) | Precise measurement, impoverished trajectories |

Success criteria:
- Steiger's z-test: Δr significant at Bonferroni alpha = 0.025 (2 comparisons)
- ΔAIC > +2 favoring Full CTT (Burnham & Anderson threshold)
- Pattern consistent across both source and destination memory

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT examined in this RQ

- [x] **Where** (Spatial Location)
  - [x] `-U-` tags (pick-up location / source memory, 18 items)
  - [x] `-D-` tags (put-down location / destination memory, 18 items)
  - [ ] `-L-` tags (static location, legacy) - EXCLUDED
  - Disambiguation: This RQ specifically examines the source (-U-) vs destination (-D-) distinction within spatial memory. Static locations (-L-) are excluded to isolate the pick-up/put-down contrast.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT examined in this RQ

**Inclusion Rationale:**

This RQ focuses exclusively on spatial memory subdivided by action phase:
- **Source memory (-U-):** Pick-up locations encoded during object acquisition. Theoretically predicted to show higher accuracy due to retrieval practice advantage, schema support, and elaborated encoding (object identification + location binding).
- **Destination memory (-D-):** Put-down locations encoded during object placement. Theoretically predicted to show lower accuracy due to proactive interference, goal discounting, and motor-only encoding.

The source-destination factor extends the What/Where/When domain analysis (Type 5.2) by probing within-domain heterogeneity in spatial memory.

**Exclusion Rationale:**

- **Object identity (What, -N-):** Not relevant for testing purification effects on spatial memory.
- **Temporal order (When, -O-):** Not relevant for testing purification effects on spatial memory.
- **Static locations (Where, -L-):** Excluded because they don't have the source-destination temporal structure. Legacy tags from early design iterations.
- **Room Free Recall (RFR), Task Cued Recall (TCR):** Excluded to maintain consistency with RQ 5.5.1 root analysis. Only interactive paradigms (IFR, ICR, IRE) are included.

---

## Analysis Approach

**Analysis Type:**

CTT (Classical Test Theory) sum score computation + Psychometric Comparison:
1. **Correlation Analysis:** Pearson r between CTT and IRT theta, comparing Full vs Purified CTT using Steiger's z-test for dependent correlations
2. **Reliability Assessment:** Cronbach's alpha with bootstrap confidence intervals before/after purification
3. **Trajectory Modeling:** Parallel LMM fitting on z-standardized measurements, comparing AIC per Burnham & Anderson (2002) guidelines

**High-Level Workflow:**

**Step 0:** Load RQ 5.5.1 outputs (theta scores, purified item list, TSVR mapping) and validate dependency completion

**Step 1:** Map retained vs removed items per location type (-U- vs -D-) from IRT purification. Expected: ~36 total items (18 per location), ~25-32 retained after purification.

**Step 2:** Compute Full CTT sum scores per UID × test × location type using all -U-/-D- items from raw data (data/cache/dfData.csv). Dichotomization: TQ < 1 → 0, TQ ≥ 1 → 1. CTT score = mean of binary responses per location type.

**Step 3:** Compute Purified CTT sum scores using only IRT-retained items per location type.

**Step 4:** Reliability assessment: Compute Cronbach's alpha with 10,000 bootstrap resamples for 95% CI. Calculate for 4 conditions: Source_Full, Source_Purified, Destination_Full, Destination_Purified. Test alpha improvement after purification.

**Step 5:** Correlation analysis: Compute Pearson r between Full CTT and IRT theta, Purified CTT and IRT theta, separately for Source and Destination. Test Δr using Steiger's z-test for dependent correlations (Steiger, 1980). Apply Bonferroni correction: alpha = 0.05/2 = 0.025 for 2 location types. Report dual p-values per Decision D068 (p_uncorrected and p_bonferroni).

**Step 6:** Z-standardize all measurements (IRT theta, Full CTT, Purified CTT) within location type to enable AIC comparison across different scales.

**Methodological Justification for Z-Standardization AIC Comparison:**
Z-standardization (centering to mean=0, scaling to SD=1) is a monotonic transformation that preserves rank-order relationships between observations. AIC comparison across z-standardized variables is valid for comparing relative model fit within the same dataset because:
1. **Likelihood preservation:** Monotonic transformations preserve maximum likelihood ordering (Pawitan, 2001)
2. **Rank-order preservation:** AIC rankings are preserved because log-likelihood differences remain constant under linear transformations
3. **Scale equalization:** Z-standardization ensures model coefficients and residuals are on comparable scales, preventing scale-driven AIC differences

Alternative approaches (raw AIC without transformation) would conflate scale differences with model fit differences. The z-standardization approach isolates trajectory structure from measurement scale.

**Step 7:** Fit parallel LMMs on z-standardized scores with identical formula structure: score ~ Time + (Time | UID), REML=False. Fit 6 models total: IRT_Source, IRT_Destination, CTT_Full_Source, CTT_Full_Destination, CTT_Purified_Source, CTT_Purified_Destination. Compare AIC per location type: Full vs Purified. ΔAIC > 2 = substantial evidence favoring lower-AIC model (Burnham & Anderson, 2002). ΔAIC > 10 = decisive evidence.

**Step 7.5:** Validate LMM assumptions for all 6 fitted models using comprehensive validation procedure:
- **(1) Linearity:** Residuals vs fitted plot, expect random scatter around y=0
- **(2) Homoscedasticity:** Scale-location plot, Breusch-Pagan test (p > 0.05)
- **(3) Normality of residuals:** Q-Q plot, Shapiro-Wilk test (p > 0.05 or visual assessment for n>50)
- **(4) Normality of random effects:** Q-Q plot for BLUPs, Shapiro-Wilk test
- **(5) Independence:** Residuals vs observation order plot, Durbin-Watson test (1.5-2.5 acceptable)
- **(6) No multicollinearity:** VIF < 10 for all predictors (N/A for single predictor models)
- **(7) Influential observations:** Cook's distance < 1.0

Document violations for each model. If CTT models show assumption violations (expected due to bounded [0,1] range), note as limitation but proceed with comparison (consistent with prior Chapter 5 RQs). Output: assumption_validation.csv with pass/fail per criterion per model.

**CTT Bounded Scale Limitations:**
Unlike IRT theta (unbounded continuous scale), CTT sum scores are bounded [0,1], creating potential ceiling/floor effects that violate LMM normality assumptions. If destination memory shows low accuracy (predicted based on goal discounting and proactive interference), floor effects may restrict variance and create left-skewed distributions. Step 7.5 LMM assumption validation will assess normality, homoscedasticity, and influential observations. If CTT models show assumption violations, this represents an inherent limitation of bounded scales for trajectory modeling (Cogn-IQ, 2024), and AIC comparisons should be interpreted cautiously. The z-standardization (Step 6) partially mitigates scale differences by equalizing variance, but does not resolve distributional shape issues. This bounded-scale limitation applies to both Full and Purified CTT, suggesting that relative AIC differences (Purified vs Full) remain interpretable even if absolute AIC values are elevated due to scale constraints.

**Practice Effects Consideration:**
The 4-test repeated measures design (Days 0, 1, 3, 6) may introduce practice effects where task familiarity improves performance independent of VR room-specific memory. However, several design features mitigate this confound:
1. **Different rooms per test:** Each test assesses a different room (Latin square counterbalancing), preventing item-specific practice effects
2. **IRT theta scoring:** Separates item difficulty from person ability, accounting for systematic differences in item response patterns
3. **Tutorial session:** Day 0 provides initial familiarization with VR mechanics and test format, reducing learning curve effects in subsequent tests
4. **LMM Time predictor:** Captures linear practice effects if present, allowing model to distinguish practice from forgetting

Nevertheless, practice effects remain a potential confound that cannot be fully eliminated in repeated-measures longitudinal designs (Salthouse et al., 2022). If practice effects elevate later-session performance, this would attenuate observed forgetting slopes for both Full and Purified CTT equally, preserving relative AIC comparisons.

**Step 8:** Prepare plot data:
- Correlation comparison: 4 rows (Source_Full, Source_Purified, Destination_Full, Destination_Purified) with r, 95% CI, Steiger's z, p-values
- AIC comparison: 4 rows (IRT, Full CTT, Purified CTT × 2 location types) with AIC, ΔAIC, evidence strength interpretation

**Expected Outputs:**

- data/step01_item_mapping.csv (~36 rows: item, location_type, retained)
- data/step02_ctt_full_scores.csv (800 rows: UID, test, location_type, ctt_full_score)
- data/step03_ctt_purified_scores.csv (800 rows: UID, test, location_type, ctt_purified_score)
- data/step04_reliability_assessment.csv (4 rows: location_type, version, alpha, CI_lower, CI_upper)
- data/step05_correlation_analysis.csv (2 rows: location_type, r_full, r_purified, delta_r, steiger_z, p_uncorrected, p_bonferroni)
- data/step06_standardized_scores.csv (800 rows: UID, test, location_type, irt_z, ctt_full_z, ctt_purified_z)
- data/step07_lmm_model_comparison.csv (2 rows: location_type, aic_irt, aic_ctt_full, aic_ctt_purified, delta_aic_full_purified)
- data/step07.5_assumption_validation.csv (42 rows: 6 models × 7 assumption tests, with pass/fail status)
- plots/step08_correlation_comparison_data.csv (4 rows for plotting: location_type, version, r, CI_lower, CI_upper)
- plots/step08_aic_comparison_data.csv (4 rows for plotting: location_type, model, aic, delta_aic_interpretation)

**Success Criteria:**

1. **Dependency Validation:** RQ 5.5.1 status = success in status.yaml, all required input files exist
2. **Item Mapping:** 30-36 total items identified, 20-30 retained per location type (purification rate 55-85%)
3. **CTT Score Range:** All CTT scores in [0,1], no NaN values, 800 observations total
4. **Reliability:** All Cronbach's alpha in [0.60, 0.95] (acceptable to excellent), bootstrap CIs non-overlapping with 0
5. **Correlation Analysis:** All correlations r > 0.50 (moderate), dual p-values present per Decision D068 (p_uncorrected and p_bonferroni)
6. **Standardization:** Z-scores have mean ≈ 0 (±0.05), SD ≈ 1 (±0.05) within location type
7. **LMM Convergence:** All 6 LMMs (IRT + Full + Purified × 2 locations) converge successfully
8. **LMM Assumptions:** Step 7.5 assumption validation completed for all 6 models, violations documented
9. **Plot Data Structure:** Correlation plot data has 4 rows with CI_upper > CI_lower; AIC plot data has 4 rows with interpretable ΔAIC values

**Paradox Confirmation Criteria:**

If paradox replicates (expected outcome):
- Steiger's z-test: Purified CTT r > Full CTT r at Bonferroni alpha = 0.025 for at least 1 location type
- AIC comparison: Purified CTT AIC > Full CTT AIC + 2 for both location types (substantial evidence favoring Full CTT for trajectories)

If paradox FAILS to replicate (unexpected outcome):
- Report null correlation difference OR Purified CTT shows equal/better AIC
- Interpret implications: May indicate source-destination memory has different psychometric properties compared to Domains/Paradigms/Congruence

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.5.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.5.1 (Source-Destination Trajectories, ROOT)

**File Paths:**
- results/ch5/5.5.1/data/step02_purified_items.csv (retained items after IRT purification with item names, location type, IRT parameters)
- results/ch5/5.5.1/data/step03_theta_scores.csv (IRT ability estimates: 400 rows with UID, test, theta_source, se_source, theta_destination, se_destination)
- results/ch5/5.5.1/data/step00_tsvr_mapping.csv (time mapping: UID, test, TSVR_hours)
- data/cache/dfData.csv (raw binary response data for computing CTT sum scores on full item set)

**Dependencies:**

RQ 5.5.1 must complete successfully before RQ 5.5.5 can run:
- Step 0: Data extraction (IFR/ICR/IRE paradigms, -U-/-D- items only)
- Step 1: IRT Pass 1 calibration (2-factor GRM: source/destination)
- Step 2: Item purification (Decision D039: exclude |b| > 3.0 OR a < 0.4)
- Step 3: IRT Pass 2 re-calibration on purified items (final theta scores)

Circuit breaker: If RQ 5.5.1 status ≠ success in results/ch5/5.5.1/status.yaml, QUIT with EXPECTATIONS ERROR.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.5.1)
- No exclusions

**Items:**
- [x] Source memory items (-U- tags, pick-up locations): 18 items
- [x] Destination memory items (-D- tags, put-down locations): 18 items
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [ ] Static location items (-L-) - EXCLUDED (not part of source-destination factor)
- [ ] Room Free Recall (RFR) - EXCLUDED (room-level memory, not item-level)
- [ ] Task Cued Recall (TCR) - EXCLUDED (room-level memory, not item-level)

**Full CTT Computation:**
Uses all 36 items (18 -U- + 18 -D-) per location type from raw data.

**Purified CTT Computation:**
Uses only IRT-retained items per location type from step02_purified_items.csv. Expected retention: 25-32 items total (12-16 per location type), representing 69-89% retention rate based on typical IRT purification outcomes in Chapter 5.

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 at nominal Days 0, 1, 3, 6)
- [x] Time variable: TSVR_hours (actual hours since encoding, more precise than nominal days)

**Note on Data Dependency:**

This RQ requires both IRT outputs (theta, purified items) from RQ 5.5.1 AND raw binary responses from dfData.csv. The raw data is necessary to compute Full CTT scores on the complete item set before purification. Purified CTT scores use only the subset of items retained by IRT purification.

---
