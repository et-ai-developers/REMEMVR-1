# RQ 5.9: Does age affect baseline memory ability or forgetting rate?

**Chapter:** 5
**RQ Number:** 9
**Full ID:** 5.9

---

## Research Question

**Primary Question:**
Do older adults show lower baseline episodic memory (intercept) and/or faster forgetting (steeper slope) compared to younger adults?

**Scope:**
This RQ examines age as a continuous predictor of both baseline episodic memory ability (Day 0 intercept) and forgetting rate (slope across 6-day retention interval). Analysis uses IRT-derived theta scores from all memory domains combined (What/Where/When) as the dependent variable. Age effects are tested on both linear and logarithmic time components. Time variable uses TSVR (actual hours since encoding, not nominal days). Sample includes all 100 participants across 4 test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6).

**Theoretical Framing:**
Hippocampal aging literature suggests older adults exhibit dual deficits: lower baseline episodic memory and faster forgetting rates. This RQ tests whether age predicts forgetting trajectory parameters, informing theoretical models of age-related memory decline beyond simple cross-sectional differences.

---

## Theoretical Background

**Relevant Theories:**
- **Hippocampal Aging Hypothesis** (Raz et al., 2005): Hippocampal volume declines with age (~1% per year after age 60), particularly in CA1 and subiculum regions critical for episodic memory encoding and retrieval.
- **Dual Deficit Hypothesis** (Nyberg et al., 2012): Age affects both encoding efficiency (lower baseline ability) and consolidation/retrieval processes (faster forgetting), not just one or the other.
- **Consolidation Theory Applied to Aging** (Dudai, 2004): Age-related hippocampal dysfunction impairs both initial encoding and time-dependent consolidation, predicting steeper forgetting curves in older adults.

**Key Citations:**
- Raz et al. (2005): Meta-analysis showing hippocampal volume declines accelerate after age 60
- Nyberg et al. (2012): Longitudinal study demonstrating age predicts both baseline memory and forgetting rate
- Dudai (2004): Consolidation framework predicting age effects on time-dependent memory processes

**Theoretical Predictions:**
Hippocampal aging hypothesis predicts older adults will show:
1. **Lower intercept** (baseline memory at Day 0) due to encoding deficits
2. **Steeper slope** (faster forgetting) due to consolidation/retrieval deficits
3. **Logarithmic interaction** (age effects stronger early in retention interval, when consolidation most active)

**Literature Gaps:**
Most aging studies use cross-sectional designs with single time points. Few studies test age effects on forgetting trajectories across multiple retention intervals (0-6 days) using IRT-calibrated ability estimates. This RQ fills the gap by testing dual deficit hypothesis with longitudinal forgetting data.

---

## Hypothesis

**Primary Hypothesis:**
Age will negatively predict both intercept (baseline memory at Day 0) and slope (forgetting rate across 6 days), consistent with hippocampal aging effects.

**Secondary Hypotheses:**
1. Age effect on intercept will be significant (well-established in literature)
2. Age × log(Time+1) interaction will be significant (consolidation-related forgetting)
3. Age × linear Time interaction may be weaker (less theoretical support for constant-rate age effects)

**Theoretical Rationale:**
Hippocampal aging hypothesis (Raz et al., 2005) predicts dual deficits: encoding (lower baseline) and consolidation (faster forgetting). Older adults show reduced hippocampal volume and function, impairing both initial memory formation and time-dependent consolidation processes. Logarithmic forgetting form (established in RQ 5.7) aligns with consolidation theory, where early retention interval (0-24h) is most vulnerable to age-related deficits.

**Expected Effect Pattern:**
- **Main effect of Age_c on Intercept:** β < 0, p < 0.0033 (older adults lower baseline)
- **Age_c × log(Time+1) interaction:** β < 0, p < 0.0033 (older adults faster logarithmic decline)
- **Age_c × Time interaction:** β < 0, but may not reach significance after Bonferroni correction (α = 0.0033)
- **Effect size:** Cohen's d ~ 0.2-0.5 (small-medium) for age effects on Day 6 theta

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object identity / naming

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: **ALL Where tags included** (inherited from RQ 5.7 "All" analysis)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ uses "All" factor analysis from RQ 5.7, which combines What/Where/When domains into a single composite episodic memory score. Rationale: Age effects on episodic memory are theoretically broad (affecting all domain types), not domain-specific. Using combined score increases statistical power for detecting age effects and tests overall episodic memory decline, consistent with hippocampal aging hypothesis.

**Exclusion Rationale:**
None - all WWW domains included via "All" composite factor from RQ 5.7.

---

## Analysis Approach

**Analysis Type:**
LMM (Linear Mixed Model) with Age × Time interaction, testing age as continuous predictor of baseline memory and forgetting rate

**High-Level Workflow:**

**Step 0:** Get Data - Use theta scores from RQ 5.7 "All" analysis (results/ch5/rq7/), load Age from data/cache/dfData.csv, merge TSVR mapping

**Step 1:** Data Preparation - Merge Age with theta scores on UID, grand-mean center Age (Age_c = Age - mean(Age)), verify no missing Age values, create time transformations (TSVR, log(TSVR+1))

**Step 2:** Fit LMM with Age × Time Interaction - Formula: Theta ~ (Time + log(Time+1)) × Age_c + (Time | UID), using Lin+Log functional form (best model from RQ 5.7), random intercepts and slopes by UID, fit with REML=False, save model pickle

**Step 3:** Extract and Test Age Effects - Main effect: Age_c on intercept (baseline memory at Day 0), interactions: Age_c × Time and Age_c × log(Time+1) (forgetting rate), apply Bonferroni correction (α = 0.0033), interpret direction (negative β = older adults worse/faster forgetting)

**Step 4:** Effect Size Computation - Standardized effect: How much does 1 SD increase in Age change Day 6 theta? Compute age-related decline from Day 0 to Day 6, report in theta units and as proportion of Day 0 ability

**Step 5:** Visualization - Create Age tertiles (Young/Middle/Older) for plotting, generate trajectory plot with 3 lines (one per tertile), include observed means with 95% CIs, overlay model predictions for each age group

**Data Preprocessing (Per Solution Section 1.4):**
- **IRT theta scores:** Inherited from RQ 5.7 (already calibrated using GRM with dichotomized accuracy and raw confidence ratings)
- **Age variable:** Use raw age in years, grand-mean centered (Age_c = Age - mean(Age)) to make intercept interpretable as average-aged adult
- **Time variable:** Use TSVR (Time Since VR, actual hours), transformed as linear (TSVR) and logarithmic (log(TSVR+1))
- **No dichotomization or Likert correction needed** (theta scores already processed in RQ 5.7)

**Special Methods:**
- **Grand-mean centering Age:** Makes intercept represent memory for average-aged adult (interpretable), reduces multicollinearity with interaction terms
- **Age × Time interaction:** Tests key hypothesis (forgetting rate varies with age)
- **Continuous Age predictor:** More powerful than age-group comparisons, avoids arbitrary cut-points (per dual deficit hypothesis)
- **Lin+Log functional form:** Inherits best-fitting model from RQ 5.7 (log component aligns with consolidation theory)
- **Bonferroni correction:** α = 0.0033 for multiple comparisons (3 age effects tested: intercept, linear slope, log slope)
- **Age tertile visualization:** Discretizes continuous age for interpretable plotting while preserving continuous analysis

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.7 theta scores + Age from dfData.csv)

### DERIVED Data Source:

**Source RQ:**
RQ 5.7 (Which functional form best describes forgetting trajectories?)

**File Paths:**
- `results/ch5/rq7/data/step03_theta_all.csv` (IRT theta scores for "All" factor analysis)
  - Columns: composite_ID (UID-Test), theta
- `results/ch5/rq7/data/step00_tsvr_mapping.csv` (TSVR time mapping)
  - Columns: UID, TEST, TSVR (hours since encoding)
- `data/cache/dfData.csv` (Age variable)
  - Columns: UID, age (years)

**Dependencies:**
RQ 5.7 must complete Steps 0-3 (data preparation, IRT calibration, theta extraction for "All" analysis) before this RQ can run.

**Usage:**
This RQ uses theta scores from RQ 5.7 "All" composite factor as the dependent variable. Age is merged from dfData.csv as a between-subjects predictor. TSVR provides the time variable for trajectory modeling.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.7)
- [x] Verify no missing Age values (exclusion criterion: any participant without Age in dfData.csv)

**Items:**
- N/A (theta scores already aggregated per participant × test via RQ 5.7 "All" factor)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; inherited from RQ 5.7)
- Note: Time variable uses TSVR (actual hours since encoding), not nominal days

---
