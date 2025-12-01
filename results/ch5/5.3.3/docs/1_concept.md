# RQ 5.3.3: Paradigm Consolidation Window

**Chapter:** 5
**Type:** Paradigms
**Subtype:** Paradigm Consolidation Window
**Full ID:** 5.3.3

---

## Research Question

**Primary Question:**
Do retrieval paradigms (Free Recall, Cued Recall, Recognition) show different consolidation benefits during the early consolidation window (Day 0->1) versus later decay period (Day 1->6)?

**Scope:**
This RQ examines forgetting trajectories across three retrieval paradigms (IFR = Item Free Recall, ICR = Item Cued Recall, IRE = Item Recognition) during two temporal segments: Early consolidation window (tests 0-1, approximately 0-24 hours) and Late decay period (tests 3-6, approximately 24-168 hours). Sample: N=100 participants x 4 test sessions = 400 observations, reshaped to 1200 rows (100 participants x 4 tests x 3 paradigms). Time variable uses Days_within (recentered within each segment).

**Theoretical Framing:**
Sleep-dependent consolidation occurs primarily during the initial 24-hour window post-encoding. Different retrieval paradigms may benefit differentially from consolidation processes. Free Recall, requiring self-initiated retrieval and deeper encoding, may show greatest early consolidation benefit. This RQ tests whether paradigm-specific forgetting rates differ between early consolidation and later decay phases.

---

## Theoretical Background

**Relevant Theories:**
- **Sleep-Dependent Consolidation Theory**: Memory consolidation is enhanced during sleep, with most benefit occurring in the first 24 hours post-encoding. Sleep-dependent consolidation may differentially affect memories encoded at different levels of processing.
- **Levels of Processing Framework** (Craik & Lockhart, 1972): Free Recall requires deeper encoding (semantic, elaborative) compared to Cued Recall (associative) and Recognition (familiarity-based). Deeper encoding may lead to greater consolidation benefit.
- **Transfer-Appropriate Processing**: Retrieval paradigms differ in processing demands. Free Recall requires self-initiated retrieval, Cued Recall provides retrieval support, Recognition relies on familiarity. These processing differences may interact with consolidation mechanisms.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Sleep-dependent consolidation may differentially benefit paradigms based on encoding depth. Free Recall (deepest encoding) may show greatest consolidation benefit during Day 0->1, manifesting as slower forgetting during Early segment compared to Late segment. Cued Recall and Recognition (shallower encoding) may show less consolidation benefit, with similar forgetting rates across segments.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Sleep-dependent consolidation (Day 0->1) may differentially benefit paradigms. Free Recall may show greatest early consolidation effect due to deeper encoding requirements.

**Secondary Hypotheses:**
- Early segment forgetting rates will differ across paradigms (3-way interaction: Days_within x Segment x paradigm)
- Consolidation benefit (difference between Early and Late segment forgetting rates) will be greatest for Free Recall, intermediate for Cued Recall, and smallest for Recognition
- All pairwise comparisons of consolidation benefit across paradigms will show significant differences

**Theoretical Rationale:**
Free Recall requires self-initiated retrieval and deeper semantic encoding, processes known to benefit from sleep-dependent consolidation. Cued Recall provides retrieval support, reducing encoding depth requirements. Recognition relies primarily on familiarity, requiring minimal encoding depth. Based on levels of processing theory, deeper encoding (Free Recall) should show greatest consolidation benefit during the early post-encoding window when sleep-dependent consolidation is most active.

**Expected Effect Pattern:**
- Piecewise LMM with 3-way interaction (Days_within x Segment x paradigm) will show significant interaction terms
- 6 segment-paradigm slopes will show clear pattern: Free Recall Early < Free Recall Late (consolidation benefit), with smaller differences for Cued Recall and Recognition
- Consolidation benefit index (Late slope - Early slope) will be positive and largest for Free Recall
- 6 planned contrasts tested at Bonferroni alpha = 0.0083 to control family-wise error rate
- Dual p-values reported per Decision D068 (both uncorrected and Bonferroni-corrected)

---

## Memory Domains

**Domains Examined:**

This RQ analyzes retrieval paradigms rather than memory domains (What/Where/When). Data source is RQ 5.3.1, which already filtered items to three retrieval paradigms:

- [x] **Free Recall (IFR)**
  - Tag Code: `IFR` (Item Free Recall)
  - Description: Self-initiated retrieval without cues

- [x] **Cued Recall (ICR)**
  - Tag Code: `ICR` (Item Cued Recall)
  - Description: Cued retrieval with location prompts

- [x] **Recognition (IRE)**
  - Tag Code: `IRE` (Item Recognition)
  - Description: Familiarity-based recognition

**Inclusion Rationale:**
These three paradigms represent a retrieval support gradient from most demanding (Free Recall, no cues) to least demanding (Recognition, familiarity-based). All three are interactive VR paradigms where participants actively explored the environment. This allows testing whether retrieval paradigm interacts with consolidation window.

**Exclusion Rationale:**
Room-level paradigms (RFR = Room Free Recall, TCR = Table Cued Recall, RRE = Room Recognition) are excluded because they differ qualitatively in scope (room-level vs item-level memory) and do not fit the retrieval support gradient framework being tested.

---

## Analysis Approach

**Analysis Type:**
Piecewise Linear Mixed Model (LMM) with 3-way interaction (Days_within x Segment x paradigm)

**High-Level Workflow:**

**Step 0:** Load theta scores from RQ 5.3.1 (results/ch5/5.3.1/data/step04_lmm_input.csv), verify data structure and dependencies

**Step 1:** Create temporal segments and prepare piecewise data structure:
- Define Segment variable: Early (tests 0-1, approximately 0-24 hours) vs Late (tests 3-6, approximately 24-168 hours)
- Compute Days_within: time recentered within each segment to start at 0
- Merge with TSVR mapping to get actual hours since encoding
- Reshape data if needed to long format (1200 rows: 100 participants x 4 tests x 3 paradigms)

**Step 2:** Fit piecewise LMM:
- Formula: `theta ~ Days_within x Segment x paradigm + (1 + Days_within | UID)`
- Random effects: random intercepts and random slopes for Days_within by participant (UID)
- Fixed effects: main effects of Days_within, Segment, paradigm, all 2-way interactions, and 3-way interaction
- Estimation: REML=False for model comparison compatibility

**Step 3:** Extract 6 segment-paradigm slopes via linear combinations:
- Early Free Recall slope
- Early Cued Recall slope
- Early Recognition slope
- Late Free Recall slope
- Late Cued Recall slope
- Late Recognition slope
- Each slope with SE, z-statistic, CI, and interpretation

**Step 4:** Compute 6 planned contrasts with Bonferroni correction:
- Test consolidation benefit within each paradigm (3 contrasts comparing Late vs Early slopes)
- Test paradigm differences in consolidation benefit (3 contrasts comparing consolidation benefit indices across paradigms)
- Bonferroni alpha = 0.0083 (0.05 / 6 comparisons)
- Report dual p-values per Decision D068 (both uncorrected and Bonferroni-corrected p-values)
- Compute effect sizes (Cohen's d or f^2)

**Step 5:** Compute consolidation benefit index per paradigm:
- Consolidation benefit = Late slope - Early slope (positive = consolidation benefit, negative = consolidation detriment)
- Rank paradigms by consolidation benefit magnitude
- Interpret pattern relative to hypothesis

**Step 6:** Prepare piecewise plot data for visualization:
- Theta scale: observed means with 95% CIs per paradigm x segment x timepoint
- Probability scale: convert theta to probability using IRT transformation per Decision D069
- Two separate CSV files for two-panel plots (Early segment vs Late segment)
- Include model predictions alongside observed data

**Expected Outputs:**
- data/step00_piecewise_lmm_input.csv (1200 rows, paradigm factor in long format)
- data/step01_piecewise_lmm_model.pkl (saved fitted LMM model)
- results/step02_segment_paradigm_slopes.csv (6 rows: Early/Late x Free/Cued/Recognition)
- results/step03_planned_contrasts.csv (6 rows: contrasts with dual p-values)
- results/step04_consolidation_benefit.csv (3 rows: Free/Cued/Recognition benefit indices)
- plots/step05_piecewise_theta_data.csv (plot data for theta scale)
- plots/step05_piecewise_probability_data.csv (plot data for probability scale)

**Success Criteria:**
- LMM model converges successfully (convergence flag = True)
- 6 segment-paradigm slopes extracted with valid SE and CI (no NaN values)
- 6 planned contrasts computed with dual p-values (Decision D068 compliant)
- Consolidation benefit indices interpretable (ranked by magnitude)
- Plot data structured correctly with 12 rows per file (2 segments x 3 paradigms x 2 timepoints per segment)
- All output files created with expected structure
- No missing data or computation errors
- All assumption validation checks documented (see Validation Procedures below)

---

## Validation Procedures

### LMM Assumption Checks

1. **Residual Normality:** Q-Q plot + Shapiro-Wilk test (accept if p > 0.01)
2. **Homoscedasticity:** Residuals vs fitted plot; Levene's test by group (segment × paradigm)
3. **Random Effects Normality:** Q-Q plot of random effect estimates (intercepts and slopes)
4. **Independence:** ACF plot of residuals (no significant autocorrelation at lags 1-5)
5. **Linearity:** Residuals vs Days_within predictor (no systematic patterns)
6. **Outliers:** Cook's distance < 4/N threshold; identify and document any influential observations

### Remedial Actions

- If normality violated (Shapiro-Wilk p < 0.01): Report robust standard errors via sandwich estimator
- If heteroscedasticity detected: Use weighted LMM or variance function by segment
- If outliers detected: Conduct sensitivity analysis with/without outliers; report both results
- If autocorrelation present: Consider AR(1) correlation structure for residuals

### Convergence Contingency Plan

If the full model (random slopes for Days_within) fails to converge:
1. Try alternative optimizers (bobyqa, nlminb)
2. Use likelihood ratio test (LRT) to compare random slopes vs intercept-only model
3. If LRT p < 0.05, retain slopes with simplified correlation structure (diagonal covariance)
4. If LRT p ≥ 0.05, use random intercepts-only model
5. Document which random effects structure achieved convergence in results

Reference: Bates et al. (2015) parsimonious mixed models guidelines.

### Practice Effects Consideration

The 4-session design (Days 0, 1, 3, 6) creates potential practice effects:
- Literature documents 13.3% improvement in episodic memory with repeated testing (Goldberg et al., BMC Neuroscience)
- IRT theta scoring partially mitigates item-level practice effects through ability estimation
- The piecewise model structure (Early vs Late segments) implicitly captures practice effects in intercepts
- Segment × paradigm interactions will reveal whether practice effects differ by retrieval type

This design cannot fully disentangle consolidation from practice effects, but the relative comparison across paradigms within each segment provides valid inference about differential consolidation benefits.

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.3.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.3.1 (Paradigm-Specific Trajectories)

**File Paths:**
- results/ch5/5.3.1/data/step04_lmm_input.csv (1200 rows: 100 participants x 4 tests x 3 paradigms, includes theta scores per paradigm)
- results/ch5/5.3.1/data/step00_tsvr_mapping.csv (TSVR hours since encoding, needed for segment assignment)
- results/ch5/5.3.1/data/step03_item_parameters.csv (item parameters from IRT Pass 2, for context if needed)

**Dependencies:**
RQ 5.3.1 must complete Steps 1-4 (IRT calibration with purification, theta score extraction, merging with TSVR, reshaping to long format) before this RQ can run. This RQ uses the paradigm-specific theta scores as input and adds temporal segmentation analysis.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.3.1 (N=100, inherited inclusion criteria)
- No additional exclusions applied

**Items:**
- N/A (theta scores are already aggregated ability estimates per paradigm, not item-level)
- Item-level purification already applied in RQ 5.3.1

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from RQ 5.3.1
- Tests grouped into segments: Early (T1-T2, approximately 0-24 hours) vs Late (T3-T4, approximately 24-168 hours)

**Paradigms:**
- [x] Free Recall (IFR) - Self-initiated retrieval
- [x] Cued Recall (ICR) - Cued retrieval
- [x] Recognition (IRE) - Familiarity-based
- Room-level paradigms (RFR, TCR, RRE) excluded by RQ 5.3.1

**Temporal Segmentation:**
- Early segment: Tests 0-1 (nominally Day 0 and Day 1, approximately 0-24 hours post-encoding)
- Late segment: Tests 3-6 (nominally Day 3 and Day 6, approximately 24-168 hours post-encoding)
- Days_within computed by recentering time within each segment to start at 0

---
