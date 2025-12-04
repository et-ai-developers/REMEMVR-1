# RQ 5.5.3: Age Effects on Source-Destination Memory

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** Age Effects
**Full ID:** 5.5.3

---

## Research Question

**Primary Question:**
Does age moderate the source (-U-) vs destination (-D-) memory difference, or the forgetting rate for either location type?

**Scope:**
This RQ examines whether age effects influence the source-destination memory dissociation identified in RQ 5.5.1. Analysis uses IRT-derived theta scores from RQ 5.5.1 (800 observations: N=100 participants × 4 tests × 2 location types). Age variable ranges 20-70 years, grand-mean centered. Time variable uses TSVR_hours (actual hours since encoding) and log-transformed TSVR.

**Theoretical Framing:**
This RQ tests whether the universal null pattern for age effects observed across Chapter 5 (RQs 5.1.3, 5.2.3, 5.3.4, 5.4.3) extends to the source-destination dissociation. The null hypothesis is theoretically motivated: ecological VR encoding creates rich, multimodal traces that may buffer against age-related hippocampal decline, resulting in age-invariant forgetting patterns.

---

## Theoretical Background

**Relevant Theories:**

- **VR Ecological Encoding Theory** (Plancher et al., 2018): Immersive VR encoding creates rich, multimodal memory traces (visual, spatial, motor, semantic) that buffer against age-related decline. Unlike lab-based verbal learning tasks (where older adults show deficits), ecological VR tasks may engage compensatory mechanisms and preserved spatial navigation abilities, leading to age-invariant forgetting.

- **Hippocampal Aging Theory** (Traditional View): Age-related hippocampal volume loss and reduced neurogenesis predict steeper forgetting, especially for spatiotemporal binding (e.g., Where/When domains). However, Chapter 5 findings consistently reject this prediction in VR contexts, suggesting ecological encoding compensates.

- **Source Memory Theory** (Johnson et al., 1993): Source memory (where information was encountered) typically shows age-related decline. However, if VR encoding creates integrated object-location traces (consistent with RQ 5.5.1 findings), age effects may not emerge for either pick-up (-U-) or put-down (-D-) locations.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Age will NOT moderate the source-destination dissociation (3-way Age × LocationType × Time interaction p > 0.05). This null prediction is based on the consistent pattern across Chapter 5: age effects fail to emerge for omnibus memory (5.1.3), domain-specific trajectories (5.2.3), paradigm-specific trajectories (5.3.4), and schema-specific trajectories (5.4.3). The VR ecological encoding hypothesis suggests age-invariant forgetting should replicate for source-destination memory.

**Literature Gaps:**
Prior source-destination studies used lab-based tasks. No published work examines age effects on source vs destination memory in immersive VR with longitudinal forgetting trajectories. If age effects remain null, this strengthens the claim that VR ecological encoding creates age-resistant memory traces.

---

## Hypothesis

**Primary Hypothesis:**
Age will NOT significantly moderate the source-destination difference or forgetting rates. Specifically, the 3-way Age × LocationType × Time interaction will be non-significant (p > 0.05), consistent with the universal null pattern for age effects across Chapter 5 RQs (5.1.3, 5.2.3, 5.3.4, 5.4.3).

**Secondary Hypotheses:**
None - this is a focused test of age invariance.

**Theoretical Rationale:**
The null hypothesis is theoretically motivated by the VR ecological encoding framework (Plancher et al., 2018). Immersive VR encoding creates rich, multimodal traces that engage multiple memory systems (hippocampus for spatial binding, perirhinal cortex for object familiarity, motor cortex for action execution). This distributed encoding may buffer against age-related hippocampal decline, leading to preserved forgetting trajectories across the adult lifespan (20-70 years). The consistent null pattern across 4 prior Chapter 5 RQs (5.1.3, 5.2.3, 5.3.4, 5.4.3) provides strong empirical support for age invariance in this VR paradigm.

**Expected Effect Pattern:**
- 3-way Age × LocationType × Time interaction: p > 0.05 (non-significant)
- No significant age effects on intercepts or slopes for either location type
- Location-specific age effects (if tested via Tukey HSD) will not differ between Source and Destination
- Bonferroni-corrected alpha = 0.025 for interaction terms

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT included in this RQ (focuses on Where spatial locations only)

- [x] **Where** (Spatial Location)
  - [x] `-U-` tags (pick-up location, SOURCE)
  - [x] `-D-` tags (put-down location, DESTINATION)
  - [ ] `-L-` tags (static location, legacy) - EXCLUDED
  - Disambiguation: This RQ examines the source-destination dissociation within the Where domain. Source locations (-U-) are where objects were picked up (first spatial encounter). Destination locations (-D-) are where objects were put down (final spatial location). The -L- static location tags are excluded as they don't fit the source-destination framework.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT included in this RQ

**Inclusion Rationale:**
This RQ focuses exclusively on spatial location memory (-U- and -D- tags) to test whether the source-destination dissociation identified in RQ 5.5.1 is moderated by participant age. Source memory (pick-up locations) is theorized to have encoding advantages (first encounter, elaborated encoding with object identification, schema support). Destination memory (put-down locations) is theorized to be weaker (goal discounting after action completion, less attention during motor execution). The age moderation test asks whether older adults show differential vulnerability for destination memory compared to source memory.

**Exclusion Rationale:**
- What domain (-N-): Not relevant for source-destination spatial analysis
- When domain (-O-): Not relevant for source-destination spatial analysis
- Legacy Where (-L-): Static location tags don't fit source-destination framework
- Room Free Recall (RFR) and Text Cued Recall (TCR): Excluded to maintain interactive paradigm focus (IFR/ICR/IRE only)

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) with 3-way interactions to test age moderation of source-destination forgetting trajectories

**High-Level Workflow:**

**Step 0:** Load IRT theta scores by location type from RQ 5.5.1 (results/ch5/5.5.1/data/step03_theta_scores.csv) and TSVR mapping. Load Age variable from raw data (data/cache/dfData.csv). Verify RQ 5.5.1 dependency is complete.

**Step 1:** Merge theta scores with TSVR and Age. Grand-mean center Age variable (Age_c = Age - mean(Age)), verify Age_c mean ≈ 0. Create log-transformed TSVR predictor (log_TSVR = log(TSVR_hours + 1)).

**Step 2:** Fit LMM with full 3-way interaction: theta ~ (TSVR_hours + log_TSVR) × Age_c × LocationType + (TSVR_hours | UID), REML=False. LocationType is Treatment-coded with Source (-U-) as reference category. Model includes:
- Main effects: TSVR_hours, log_TSVR, Age_c, LocationType
- 2-way interactions: TSVR_hours:Age_c, log_TSVR:Age_c, TSVR_hours:LocationType, log_TSVR:LocationType, Age_c:LocationType
- 3-way interactions: TSVR_hours:Age_c:LocationType, log_TSVR:Age_c:LocationType
Random effects: Random intercept and TSVR_hours slope per participant (UID).

**Step 2.5:** Validate LMM assumptions using comprehensive validation procedure:
- **(1) Linearity:** Residuals vs fitted plot, expect random scatter around y=0
- **(2) Homoscedasticity:** Scale-location plot, Breusch-Pagan test (p > 0.05)
- **(3) Normality of residuals:** Q-Q plot, Shapiro-Wilk test (p > 0.05 or visual assessment for n>50)
- **(4) Normality of random effects:** Q-Q plot for BLUPs, Shapiro-Wilk test
- **(5) Independence:** Residuals vs observation order plot, Durbin-Watson test (1.5-2.5 acceptable)
- **(6) No multicollinearity:** VIF < 10 for all predictors
- **(7) Influential observations:** Cook's distance < 1.0
Document violations and apply remedial actions if needed. Output: assumption_validation.csv with pass/fail per criterion.

**Step 3:** Extract 3-way interaction terms (Age_c × Time × LocationType). Test significance at Bonferroni-corrected alpha = 0.025 (correcting for 2 time predictors). Report dual p-values per Decision D068 (both uncorrected p-value and Bonferroni-corrected p-value).

**Step 3.5:** Type II Error Quantification (Power Analysis for Null Hypothesis Testing)
Since the primary hypothesis is NULL (age does NOT moderate source-destination forgetting), Type II error must be quantified to ensure the null finding is interpretable:
- Use simulation-based power analysis (simr package in R, or custom Python simulation)
- Simulate 1000 datasets under alternative hypothesis: Age×LocationType×Time interaction β = 0.01 (small effect per Cohen, 1988)
- Compute power to detect this effect at α = 0.025 (Bonferroni-corrected)
- Target: Power ≥ 0.80 to conclude the study is adequately powered to detect small effects
- If power < 0.80, report minimum detectable effect size at 80% power
- Output: power_analysis.csv with effect_size, power, n_simulations columns

**Step 4:** Compute location-specific age effects at Day 3 (midpoint of retention interval) using Tukey HSD post-hoc contrasts. Compare age slope for Source vs Destination at this representative timepoint. Report dual p-values.

**Step 5:** Create age tertiles (Young/Middle/Older based on 33rd and 67th percentiles). Aggregate observed theta means by age tertile × location type × test for plotting. Compute 95% confidence intervals per group. Result: 24 rows (3 tertiles × 2 locations × 4 tests).

**Expected Outputs:**
- data/step00_theta_from_rq551.csv (theta scores from RQ 5.5.1)
- data/step01_lmm_input.csv (800 rows: 100 UID × 4 tests × 2 locations, 10+ columns including theta, TSVR_hours, log_TSVR, Age_c, LocationType)
- data/step02_lmm_model.pkl (saved LMM model object)
- results/step02_lmm_summary.txt (model summary with convergence status, AIC, fixed effects table)
- data/step02_fixed_effects.csv (fixed effects coefficients, SE, z-values, p-values for all terms)
- data/step02.5_assumption_validation.csv (7 rows: assumption tests with pass/fail status)
- data/step03_interaction_terms.csv (3-way interaction terms with dual p-values)
- data/step03.5_power_analysis.csv (power analysis results: effect_size, power, n_simulations)
- data/step04_age_effects_by_location.csv (location-specific age effects: 2 rows for Source and Destination)
- plots/step05_age_tertile_plot_data.csv (24 rows: 3 tertiles × 2 locations × 4 tests, with theta_mean, SE, CI_lower, CI_upper)

**Success Criteria:**
- RQ 5.5.1 dependency verified (theta file exists and loads successfully)
- Model converged (model.converged = True, no convergence warnings)
- Age_c grand-mean centered correctly (mean(Age_c) ≈ 0, within ±0.01)
- LMM assumptions validated (Step 2.5): ≥5/7 criteria pass, violations documented with remedial actions
- 3-way interaction terms present in fixed effects output (2 terms expected)
- Dual p-values reported per Decision D068 (both p_uncorrected and p_bonferroni columns)
- Power analysis completed (Step 3.5): Power ≥ 0.80 for small effect (β=0.01), OR minimum detectable effect size reported
- Random variances positive (var_intercept > 0, var_slope > 0, var_residual > 0)
- Plot data structure correct: 24 rows, CI_upper > CI_lower for all groups
- 800 observations in merged LMM input (100 participants × 4 tests × 2 locations)

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.5.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.5.1 (Source-Destination Trajectories ROOT)

**File Paths:**
- results/ch5/5.5.1/data/step03_theta_scores.csv (IRT ability estimates by location type: 400 rows with theta_source and theta_destination columns)
- results/ch5/5.5.1/data/step00_tsvr_mapping.csv (TSVR time mapping: 400 rows with UID, TEST, TSVR_hours)
- data/cache/dfData.csv (Age variable: continuous, range 20-70 years)

**Dependencies:**
RQ 5.5.1 must complete Steps 1-3 (IRT calibration Pass 1, item purification, IRT calibration Pass 2) before this RQ can run. Specifically, Step 3 of RQ 5.5.1 produces the theta scores by location type that serve as the dependent variable for this age moderation analysis.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 5.5.1 (inherited inclusion criteria)
- Age range: 20-70 years (continuous predictor)
- No exclusions based on age

**Items:**
- N/A (theta scores already aggregated per location type)
- Item-level responses not used in this RQ

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - inherited from RQ 5.5.1
- Time variable: TSVR_hours (actual hours since encoding, accounts for individual session timing)
- Nominal retention intervals: Day 0 (T1), Day 1 (T2), Day 3 (T3), Day 6 (T4)

**Location Types:**
- [x] Source (-U-) pick-up locations
- [x] Destination (-D-) put-down locations
- [ ] Legacy (-L-) static locations - EXCLUDED

---
