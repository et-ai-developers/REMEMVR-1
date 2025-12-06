# RQ 6.7.2: Confidence Variability Predicts Memory Variability

**Chapter:** 6
**Type:** Predictive
**Subtype:** Confidence Variability
**Full ID:** 6.7.2

---

## Research Question

**Primary Question:**
Do people with variable confidence show variable memory? Is within-person confidence variability correlated with within-person accuracy variability?

**Scope:**
This RQ examines the relationship between metacognitive variability (SD of confidence across items) and memory variability (SD of accuracy across items). Analysis conducted at the person-by-timepoint level: N=100 participants x 4 test sessions = 400 observations. Item-level confidence (TC_*) and accuracy (TQ_*) are aggregated to compute within-person standard deviations at each timepoint.

**Theoretical Framing:**
If metacognitive monitoring reflects encoding quality, individuals with noisy encoding (high variability in item-level accuracy) should also show noisy confidence judgments (high variability in item-level confidence). This would suggest confidence tracking is sensitive to trial-by-trial encoding fluctuations. Conversely, if confidence variability does NOT correlate with accuracy variability, it suggests metacognitive judgments operate independently of encoding quality (fixed confidence bias regardless of actual performance).

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory**: Confidence judgments are proposed to reflect internal monitoring of memory trace strength. If monitoring is accurate, confidence variability should mirror accuracy variability at the individual level.
- **Signal Detection Theory**: Memory retrieval operates with both signal (true memory) and noise (encoding/retrieval variability). High-noise individuals should show both high accuracy variability and high confidence variability if confidence tracking is sensitive to signal-to-noise ratio.
- **Encoding Variability Hypothesis**: Within-person variability in encoding success creates item-to-item differences in memory strength. If confidence is based on memory strength, encoding variability should manifest in both accuracy and confidence variability.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If confidence tracking is sensitive to encoding quality, positive correlation expected: individuals with high SD_confidence also show high SD_accuracy. If confidence operates independently (fixed bias), no correlation expected (r H 0).

**Literature Gaps:**
Prior metacognition research focuses on mean calibration (average confidence vs average accuracy) but rarely examines within-person variability as a marker of metacognitive sensitivity to trial-by-trial fluctuations.

---

## Hypothesis

**Primary Hypothesis:**
High within-person confidence variability (SD of confidence across items at a given timepoint) will predict high within-person accuracy variability (SD of accuracy across items). Expected positive correlation: r > 0.30 indicates meaningful association.

**Secondary Hypotheses:**
- Correlation strength may INCREASE over time (Day 0 to Day 6) if metacognitive tracking becomes noisier as memories degrade.
- Alternatively, correlation may be STABLE across time if the variability relationship is a stable individual-difference trait.

**Theoretical Rationale:**
Metacognitive noise (variability in confidence judgments) should reflect encoding noise (variability in memory traces). If an individual has inconsistent encoding success across items (some well-encoded, some poorly-encoded), confidence should track this variability, creating correlated SD_confidence and SD_accuracy. This would support the view that confidence monitoring is sensitive to item-level memory strength rather than operating as a fixed bias.

**Expected Effect Pattern:**
Positive correlation (r > 0.30) between SD_confidence and SD_accuracy. Pearson correlation tested with dual p-values (parametric and permutation-based, per Decision D068). Effect size interpretation: r > 0.50 = strong association, r = 0.30-0.50 = moderate, r < 0.30 = weak.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Not separated by domain in this RQ

- [ ] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [ ] `-U-` tags (pick-up location)
  - [ ] `-D-` tags (put-down location)
  - Not separated by domain in this RQ

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Not separated by domain in this RQ

**Inclusion Rationale:**
This RQ uses omnibus "All" items (aggregated across all domains) to compute within-person variability. Domain separation not required because the analysis focuses on individual-difference patterns in variability, not domain-specific effects.

**Exclusion Rationale:**
No domain-specific exclusions. All VR interactive paradigm items (IFR, ICR, IRE) included in variability computation, consistent with Chapter 6 General analyses (RQ 6.1.X series).

---

## Analysis Approach

**Analysis Type:**
Correlation analysis (Pearson r with dual p-values per Decision D068) examining the relationship between within-person confidence variability and within-person accuracy variability.

**High-Level Workflow:**

**Step 0:** Compute within-person SD of confidence per participant per timepoint
- Extract item-level TC_* confidence ratings (5-level Likert: 0, 0.25, 0.5, 0.75, 1.0)
- Compute SD(confidence) for each participant at each test session (T1, T2, T3, T4)
- Output: data/step01_sd_confidence.csv (400 rows: N=100 x 4 tests)

**Step 1:** Compute within-person SD of accuracy per participant per timepoint
- Extract item-level TQ_* accuracy responses (binary: 0 = incorrect, 1 = correct)
- Compute SD(accuracy) for each participant at each test session
- Output: data/step02_sd_accuracy.csv (400 rows)

**Step 2:** Correlate SD_confidence vs SD_accuracy using multilevel approach to handle non-independence
- Merge SD_confidence and SD_accuracy by UID x test
- **CRITICAL:** 400 observations from 100 participants are NOT independent (4 repeated measures per person)

**PRIMARY ANALYSIS: Person-level aggregation (N=100)**
- Compute person-level means: avg_SD_confidence and avg_SD_accuracy (averaging across 4 timepoints per person)
- Compute Pearson correlation on person-level means (N=100 independent observations)
- This is the PRIMARY analysis due to interpretive clarity and statistical validity
- Rationale: Avoids complex multilevel modeling, provides straightforward person-level association

**SUPPLEMENTARY ANALYSIS: Multilevel model (N=400 observations)**
- SD_accuracy ~ SD_confidence + (1 | UID) to account for within-person clustering
- Extract fixed effect slope; standardize to obtain standardized β (analogous to r)
- Compare multilevel result to person-level aggregation as robustness check
- If results diverge substantially (r_person vs β_multilevel differ by >0.15), report both and discuss

**Dual p-values:**
- For person-level: Parametric Pearson test + bootstrap 95% CI (10000 resamples)
- For multilevel: Wald p-value + parametric bootstrap p-value
- Output: results/step03_correlation.csv

**Step 3:** Test if variability predicts variability
- Test null hypothesis: r = 0 (no relationship between confidence and accuracy variability)
- Interpret effect size: r > 0.50 strong, 0.30-0.50 moderate, < 0.30 weak
- Document direction: positive (variability correlated), negative (inverse), or null (no association)
- Output: plots/step04_variability_correlation.csv (plot data with regression line)

**Expected Outputs:**
- data/step01_sd_confidence.csv (400 rows: UID, test, SD_confidence)
- data/step02_sd_accuracy.csv (400 rows: UID, test, SD_accuracy)
- results/step03_correlation.csv (r, p_parametric, p_permutation, CI_95)
- plots/step04_variability_correlation.csv (400 rows for scatterplot with regression line)

**Success Criteria:**
- SD computed for all 400 person-timepoint observations
- No missing values (all participants have sufficient items to compute SD)
- **Non-independence addressed:** Person-level aggregation (N=100) as primary, multilevel (N=400) as supplementary
- Correlation/association tested with dual p-values (parametric + bootstrap)
- Direction of effect documented (positive/negative/null)
- Effect size interpretation provided (strong/moderate/weak based on r thresholds)
- **Analysis choice documented:** Primary = person-level aggregation (interpretive clarity), Supplementary = multilevel (preserves information)
- **SD binary constraint sensitivity analysis completed** (see below)

**SD of Binary Data Constraint - Sensitivity Analysis (REQUIRED)**

**Issue:** SD of binary accuracy (0/1) is mathematically constrained by mean proportion: SD = sqrt[p*(1-p)]. This creates a potential artifact where participants with intermediate accuracy (~50%) automatically have higher SD than those at extremes (~0% or ~100%). The observed correlation between SD_confidence and SD_accuracy might partially reflect this mathematical constraint rather than true metacognitive sensitivity.

**Required Sensitivity Analysis:**
1. Compute mean_accuracy per person-timepoint alongside SD_accuracy
2. Compute partial correlation: r(SD_confidence, SD_accuracy | mean_accuracy) controlling for mean accuracy
3. Report BOTH unadjusted correlation AND partial correlation
4. **Interpretation guide:**
   - If unadjusted r significant but partial r is NOT significant: Mathematical constraint dominates; cannot conclude metacognitive sensitivity
   - If BOTH unadjusted r AND partial r are significant: Variability relationship robust to mean accuracy confound; genuine metacognitive signal
   - If neither significant: No evidence for variability relationship regardless of constraint

**Output:** results/step03b_partial_correlation.csv (r_partial, p_partial, comparison to unadjusted)

---

## Data Source

**Data Type:**
DERIVED (from item-level raw data extracted separately for confidence and accuracy)

### DERIVED Data Source:

**Source Data:**
Item-level data from data/cache/dfData.csv:
- TC_* tags (confidence ratings, 5-level Likert scale)
- TQ_* tags (accuracy responses, binary 0/1)

**Extraction Method:**
No Step 0 extraction from dfData.csv within this RQ workflow. Instead, analysis scripts will:
1. Load item-level TC_* confidence data (from dfData.csv or intermediate RQ outputs if available)
2. Load item-level TQ_* accuracy data (from dfData.csv or intermediate RQ outputs if available)
3. Aggregate to compute within-person SD per timepoint

Note: Unlike other RQs, this analysis does NOT require IRT-derived theta scores. Raw item-level responses are used directly because variability computation requires item-level dispersion, not aggregate ability estimates.

**File Paths:**
- data/cache/dfData.csv (master dataset)
- Alternatively, if item-level data already extracted in prior RQs:
  - Item-level confidence may be available from RQ 6.6.1 or similar
  - Item-level accuracy may be available from Chapter 5 analyses

**Dependencies:**
None - this RQ can run independently as long as dfData.csv is accessible. No dependency on other RQ outputs (unlike most Chapter 6 RQs which derive from 6.1.1 or Chapter 5).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] All VR interactive paradigm items (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (not part of interactive WWW paradigm)
- [ ] Test-Cued Recall (TCR) - EXCLUDED
- [ ] Test-Recognition (RRE) - EXCLUDED

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 corresponding to nominal Days 0, 1, 3, 6)
- Note: Actual retention intervals use TSVR (hours since encoding), but variability analysis aggregates within each test session regardless of exact timing

**Item-Level Requirements:**
- Minimum items per participant per test: Recommend >= 10 items to compute stable SD estimates
- If participant has < 10 items at a given test, exclude that observation (flag as missing rather than compute unreliable SD)

---
