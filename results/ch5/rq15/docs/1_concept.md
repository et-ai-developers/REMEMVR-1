# RQ 5.15: Item Difficulty × Time Interaction

**Chapter:** 5
**RQ Number:** 15
**Full ID:** 5.15

---

## Research Question

**Primary Question:**
Do easier items (lower difficulty) show faster forgetting than harder items, consistent with initial strength predicting decay rate?

**Scope:**
This RQ examines the cross-level interaction between item-level difficulty (from IRT calibration) and person-level forgetting trajectories (time). Analysis uses item-level responses across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6) with TSVR (actual hours since encoding) as time variable. Focuses on all VR items across What/Where/When domains to test whether item difficulty moderates forgetting rate.

**Theoretical Framing:**
Jost's law of forgetting predicts that weaker memories (easier items = lower encoding strength) decay faster than stronger memories. This RQ tests whether item difficulty (proxy for initial strength) predicts decay rate, which has implications for understanding whether forgetting trajectories reflect encoding strength or retrieval dynamics.

---

## Theoretical Background

**Relevant Theories:**
- **Jost's Law of Forgetting** (Jost, 1897): If two memories have equal current strength but different ages, the older memory will decay more slowly. Extended interpretation: Weaker initial encoding → faster decay.
- **Strength Theory** (Underwood, 1964): Item difficulty reflects encoding strength. Easier items = lower encoding strength → faster forgetting.
- **Ceiling Effects Hypothesis**: Easier items may show slower apparent forgetting due to ceiling effects (high performance at T1 leaves less room to decline).

**Key Citations:**
- Jost (1897): Original statement of forgetting law linking initial strength to decay rate
- Underwood (1964): Strength theory of forgetting with item difficulty as proxy for encoding strength
- Wixted & Ebbesen (1991): Reinterpretation of Jost's law using IRT framework

**Theoretical Predictions:**
Three competing predictions exist:
1. **Positive interaction** (easier items forget faster): Strength theory predicts lower initial strength → faster decay
2. **Negative interaction** (easier items forget slower): Ceiling effects dominate, high T1 performance constrains apparent decline
3. **No interaction** (difficulty affects intercept only): Item difficulty affects baseline performance but not forgetting rate

**Literature Gaps:**
Most forgetting research examines aggregate trajectories without testing whether item-level properties (difficulty) moderate decay. Few studies use IRT-derived difficulty estimates to test cross-level interactions in longitudinal episodic memory data. This RQ fills the gap by testing item difficulty as predictor of forgetting rate.

---

## Hypothesis

**Primary Hypothesis:**
Exploratory. No directional prediction given competing theoretical accounts.

**Secondary Hypotheses:**
1. If positive interaction (Time × Difficulty > 0): Easier items (lower difficulty) forget slower, consistent with ceiling effects
2. If negative interaction (Time × Difficulty < 0): Easier items forget faster, consistent with strength theory
3. If no interaction (Time × Difficulty = ns): Item difficulty affects intercept only, not forgetting rate

**Theoretical Rationale:**
Competing theories make opposite predictions. Strength theory predicts easier items (weaker encoding) forget faster (negative interaction). Ceiling effects predict easier items forget slower (positive interaction). No interaction would suggest item difficulty and forgetting rate are orthogonal (difficulty affects baseline, not decay).

**Expected Effect Pattern:**
Cross-level interaction in LMM analysis: Time × Difficulty_c (centered item difficulty). If significant (p < 0.0033 after Bonferroni correction), interaction coefficient sign determines which theoretical account is supported. Non-significant interaction supports orthogonality (difficulty affects intercept only).

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
  - Disambiguation: **ALL Where tags included** for complete spatial coverage

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ examines item difficulty × time interaction across ALL domains. Including all three WWW domains maximizes item diversity (difficulty range) and generalizability of findings. Item difficulty is derived from IRT calibration that includes all domains, so excluding domains would create mismatch between difficulty estimates and response data.

**Exclusion Rationale:**
None - all WWW domains included to match IRT calibration used for difficulty estimates (from RQ 5.1 outputs).

---

## Analysis Approach

**Analysis Type:**
Cross-Classified Linear Mixed Model (LMM) with crossed random effects (UID × Item)

**High-Level Workflow:**

**Step 0:** Get Data - Use item parameters from results/ch5/rq1/ (IRT difficulty estimates), raw response data from data/cache/dfData.csv, TSVR mapping from results/ch5/rq1/data/step00_tsvr_mapping.csv

**Step 1:** Load and Merge Data - Load item parameters (difficulty estimates from IRT), load response data in long format (UID × Test × TSVR × Item), merge item difficulty into response-level data, merge TSVR data on UID-Test, verify data structure (number of observations, unique UIDs, unique items)

**Step 2:** Center Predictors - Grand-mean center Difficulty for interpretability (Difficulty_c = Difficulty - mean), create time variables (Days and log(Days+1)), centered Difficulty allows intercept to represent average item at average difficulty

**Step 3:** Fit Cross-Classified LMM - Formula: Response ~ Time × Difficulty_c + (Time | UID) + (1 | Item), random effects crossed (UID for person-specific intercepts/slopes, Item for item-specific intercepts), software: pymer4 (Python wrapper for R's lme4, statsmodels doesn't support crossed random effects), alternative if pymer4 unavailable: Treat Item as fixed effect (less ideal, loses generalizability)

**Step 4:** Extract and Interpret Cross-Level Interaction - Extract Time × Difficulty_c interaction term, test significance using Bonferroni-corrected α = 0.0033, interpretation: Positive β = easier items forget slower (ceiling effect), Negative β = easier items forget faster (weak encoding), Non-significant = difficulty affects intercept only

**Step 5:** Visualize Interaction - Generate predicted trajectories for easy items (-1 SD difficulty) vs hard items (+1 SD difficulty), plot Days (0, 1, 3, 6) on x-axis with predicted response probability on y-axis, include both trajectories on same plot, if interaction significant: trajectories diverge, if non-significant: parallel lines

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores:** Response data is dichotomized (0/1) from original TQ_* values (1 = 1, <1 = 0)
- **IRT Difficulty Estimates:** Use difficulty parameters from RQ 5.1 purified IRT calibration (Step 3 output: step03_difficulty.csv)
- **TSVR Time Variable:** Use actual hours since encoding (not nominal days)
- **Grand-Mean Centering:** Difficulty_c = Difficulty - mean(Difficulty) for interpretability

**Special Methods:**
- **Cross-Classified Random Effects:** pymer4 required (statsmodels doesn't support crossed UID × Item random effects)
- **Cross-Level Interaction:** Item-level predictor (difficulty) moderating person-level trajectory (time)
- **Bonferroni Correction:** α = 0.05/15 = 0.0033 (15 RQs in Chapter 5)
- **Centered Predictors:** Grand-mean centering Difficulty allows intercept to represent average item at average difficulty (improves interpretability)
- **Fallback Method:** If pymer4 unavailable, treat Item as fixed effect (loses generalizability but allows convergence)

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.1 outputs) + RAW (from master.xlsx)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1 (Domain-Specific Forgetting Trajectories)

**File Paths:**
- `results/ch5/rq1/data/step03_difficulty.csv` (IRT item difficulty estimates from purified calibration)
- `results/ch5/rq1/data/step00_tsvr_mapping.csv` (TSVR time variable mapping)

**Dependencies:**
RQ 5.1 must complete Steps 1-3 (IRT calibration, purification, theta extraction) before this RQ can access difficulty parameters. Specifically requires step03_difficulty.csv (purified item difficulty estimates).

**Usage:**
This RQ uses item difficulty estimates as predictor (moderator) of forgetting trajectories. Difficulty is merged into item-level response data to test cross-level interaction (Time × Difficulty_c).

### RAW Data Source:

**Tag Patterns:**
- Domain tags: `-N-` (What), `-L-/-U-/-D-` (Where), `-O-` (When)
- Paradigm codes: IFR, ICR, IRE (interactive paradigms only, excludes RFR per RQ 5.1)
- Complete patterns:
  - What: `RVR-X-N-{IFR|ICR|IRE}-`
  - Where: `RVR-X-{L|U|D}-{IFR|ICR|IRE}-`
  - When: `RVR-X-O-{IFR|ICR|IRE}-`

**Extraction Method:**
Load raw response data from data/cache/dfData.csv (created by RQ 5.1 Step 1), extract TQ_* columns matching tag patterns above, convert to long format (UID × Test × Item × Response), merge with TSVR and item difficulty.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.1)

**Items:**
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (different response format, excluded from RQ 5.1 IRT calibration)
- [x] All items from RQ 5.1 purified set (items with |difficulty| ≤ 3.0 and discrimination ≥ 0.4)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Note: Time variable uses TSVR (actual hours since encoding), not nominal days

---
