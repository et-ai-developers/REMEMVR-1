# RQ 5.13: Between-Person Variance in Forgetting Rates

**Chapter:** 5
**RQ Number:** 13
**Full ID:** 5.13

---

## Research Question

**Primary Question:**
What proportion of variance in forgetting rate (slopes) is between-person (stable individual differences) vs within-person (measurement error)?

**Scope:**
This RQ examines the variance decomposition of forgetting trajectories from RQ 5.7's best-fitting mixed model. It quantifies how much variation in forgetting rates reflects stable individual differences (between-person variance) versus measurement noise or within-person fluctuation. Analysis uses random slopes from LMM with all VR items (single-factor "All" analysis) across four test sessions (T1, T2, T3, T4).

**Theoretical Framing:**
Understanding whether forgetting rate is a trait-like individual difference has theoretical implications for episodic memory research. High between-person variance (ICC > 0.40) suggests forgetting rate is a stable cognitive characteristic, justifying person-centered analyses (e.g., identifying fast vs slow forgetters in RQ 5.14). Low variance suggests forgetting is primarily driven by situational factors or measurement error.

---

## Theoretical Background

**Relevant Theories:**
- **Individual Differences in Memory:** Cognitive psychology literature suggests substantial individual differences exist in baseline memory ability (e.g., working memory capacity), but forgetting rate variability is less studied
- **Trait vs State Forgetting:** Debate over whether forgetting rate is a stable trait (like IQ) or state-dependent (context-driven). ICC quantifies this distinction
- **Random Effects Models:** Mixed-effects models partition variance into between-person (random effects) and within-person (residual) components, enabling ICC computation

**Key Citations:**
- ICC methodology for random slopes in longitudinal designs (Raudenbush & Bryk, 2002)
- Individual differences in episodic memory trajectories (Nyberg et al., 2012)
- Stability of memory decline rates across aging studies (Hedden & Gabrieli, 2004)

**Theoretical Predictions:**
If forgetting rate is trait-like, ICC for slopes should exceed 0.40 (substantial between-person variance). If forgetting is primarily noise-driven, ICC should be low (<0.20). Moderate ICC (0.20-0.40) suggests mixed trait/state influences.

**Literature Gaps:**
Most episodic memory studies report group-level forgetting curves but do not decompose variance to quantify individual difference stability. This RQ fills that gap by computing ICC for forgetting rate slopes using rigorous LMM methodology.

---

## Hypothesis

**Primary Hypothesis:**
Substantial between-person variance exists in forgetting rate (ICC for slopes > 0.40), indicating forgetting rate is a stable, trait-like individual difference rather than random noise.

**Secondary Hypotheses:**
1. Baseline ability (intercepts) will show higher ICC than forgetting rate (slopes), as baseline memory is more stable than trajectory
2. Negative intercept-slope correlation: individuals with higher baseline ability will show slower forgetting (maintain advantage over time)

**Theoretical Rationale:**
Cognitive abilities generally show moderate-to-high stability (ICC > 0.40) across repeated measurements. If forgetting rate reflects a stable cognitive process (e.g., consolidation efficiency, retrieval strength decline), between-person variance should be substantial. The intercept-slope correlation tests whether high performers maintain their advantage (negative r) or regress to the mean (positive r).

**Expected Effect Pattern:**
- ICC (intercepts) H 0.60-0.70 (high stability in baseline)
- ICC (slopes) H 0.40-0.50 (moderate-to-high stability in forgetting rate)
- Intercept-slope correlation: r H -0.20 to -0.40 (negative, modest strength)
- Random slopes approximately normally distributed (justifies parametric LMM assumptions)

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
  - Disambiguation: **ALL Where tags included** (comprehensive spatial coverage)

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ uses the "All" (single-factor) analysis from RQ 5.7, which aggregates all three WWW domains into a single latent construct. The focus is on overall forgetting rate variance, not domain-specific differences. All domains contribute to the composite ability estimate used for variance decomposition.

**Exclusion Rationale:**
None - all WWW domains included as part of the omnibus "All" factor from RQ 5.7.

---

## Analysis Approach

**Analysis Type:**
Variance Decomposition of LMM Random Effects (from RQ 5.7 best-fitting model)

**High-Level Workflow:**

**Step 0:** Get Data
- Load best-fitting LMM model object from RQ 5.7 (`results/ch5/rq7/`)
- Load theta scores from RQ 5.7 (`step04_theta_scores_allitems.csv`)
- Load TSVR mapping from RQ 5.7 (`step00_tsvr_mapping.csv`)

**Step 1:** Extract Variance Components
- Extract random effects covariance matrix from saved LMM
- Compute variance components: var_intercept, var_slope, cov_int_slope
- Extract residual variance (within-person error)

**Step 2:** Compute Intraclass Correlation Coefficients (ICC)
- ICC for intercepts: var_intercept / (var_intercept + var_residual)
- ICC for slopes (Method 1): var_slope / (var_slope + var_residual) [simple ratio]
- ICC for slopes (Method 2): Conditional ICC at Day 6 [accounts for intercept-slope covariance]
- Interpret magnitude: ICC > 0.40 = substantial, 0.20-0.40 = moderate, <0.20 = low

**Step 3:** Extract Individual Random Effects
- Extract person-specific random intercepts and slopes
- Compute total intercept and slope per person (fixed + random effects)
- Generate descriptive statistics for random slopes distribution (mean, SD, min, max, quartiles)
- Save random effects CSV for use in RQ 5.14 (clustering analysis)

**Step 4:** Test Intercept-Slope Correlation
- Compute Pearson correlation between baseline ability (intercept) and forgetting rate (slope)
- Test significance using t-test
- Apply Bonferroni correction (± = 0.0033)
- Interpret direction: negative = high performers maintain advantage

**Step 5:** Visualize Random Slopes Distribution
- Generate histogram showing distribution of individual forgetting rates
- Create Q-Q plot to assess normality assumption for random effects
- Include population mean reference line on histogram

**Data Preprocessing (Per Solution Section 1.4):**
- **Data Source:** DERIVED from RQ 5.7 (no raw data preprocessing needed)
- **Model Object:** Load saved LMM object directly (Python pickle or statsmodels result object)
- **No dichotomization or IRT needed:** This RQ uses pre-computed theta scores and fitted LMM

**Special Methods:**
- **ICC Methods:** Two ICC computations for slopes (simple ratio vs conditional at Day 6) to account for intercept-slope covariance
- **Bonferroni Correction:** ± = 0.0033 for intercept-slope correlation test (conservative threshold)
- **Normality Check:** Q-Q plot validates LMM assumption that random effects are normally distributed
- **Dependency:** Requires RQ 5.7 to complete Steps 0-5 (IRT calibration, purification, theta extraction, TSVR merge, LMM trajectory modeling with random slopes)

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.7 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.7 (Which functional form best describes forgetting trajectories?)

**File Paths:**
- `results/ch5/rq7/data/step05_lmm_all_bestmodel.pkl` (saved LMM model object with random slopes)
- `results/ch5/rq7/data/step04_theta_scores_allitems.csv` (IRT ability estimates, columns: UID, TEST, theta)
- `results/ch5/rq7/data/step00_tsvr_mapping.csv` (TSVR time variable, columns: UID, TEST, TSVR)

**Dependencies:**
RQ 5.7 must complete all 5 steps (IRT calibration on "All" items, purification, theta extraction, TSVR merge, LMM trajectory modeling with random slopes) before this RQ can run. Specifically, RQ 5.7 must save the best-fitting LMM model object with random slopes enabled.

**Usage:**
This RQ extracts variance components and random effects from RQ 5.7's saved LMM to quantify between-person vs within-person variance in forgetting trajectories.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ 5.7 (inherited inclusion criteria - all 100 participants unless excluded in RQ 5.7)

**Items:**
- [x] "All" factor items from RQ 5.7 (purified item set after 2-pass IRT, includes What/Where/When combined into single latent construct)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) - inherited from RQ 5.7

---
