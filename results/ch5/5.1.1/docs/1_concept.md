# RQ 5.7: Functional Form of Forgetting Trajectories

**Chapter:** 5
**RQ Number:** 7
**Full ID:** 5.7

---

## Research Question

**Primary Question:**
Which functional form best describes episodic forgetting trajectories across a 6-day retention interval?

**Scope:**
This RQ compares 5 candidate mathematical models (linear, quadratic, logarithmic, linear+logarithmic, quadratic+logarithmic) using IRT-derived ability estimates aggregated across all VR items (all domains and paradigms combined into single omnibus factor). Analysis covers 100 participants × 4 test sessions = 400 observations. Time variable uses TSVR (actual hours since encoding, labeled "Days" for interpretability). Model selection via AIC.

**Theoretical Framing:**
Competing memory theories predict different forgetting trajectories. Classical Ebbinghaus curve predicts logarithmic decay, power-law theory (Wixted & Ebbesen, 1991) predicts log-log decline, two-phase consolidation theory (Hardt et al., 2013) predicts quadratic (rapid then slow). Linear decline represents simple trace decay. This exploratory analysis tests which mathematical approximation best fits observed data, informing theoretical understanding of forgetting dynamics.

---

## Theoretical Background

**Relevant Theories:**
- **Ebbinghaus Forgetting Curve (1885):** Logarithmic forgetting (log(time+1)) where memory declines rapidly at first then levels off asymptotically
- **Power Law of Forgetting (Wixted & Ebbesen, 1991):** Power-law decay (y ~ t^-α, equivalent to log-log transformation) suggesting scale-invariant forgetting
- **Two-Phase Consolidation Theory (Hardt et al., 2013):** Rapid initial decay (first 24h) followed by gradual asymptotic decline, mathematically approximated by quadratic function
- **Trace Decay Theory:** Simple linear decline over time (baseline null hypothesis)

**Key Citations:**
- Ebbinghaus (1885): Original forgetting curve - logarithmic decline
- Wixted & Ebbesen (1991): Power-law forgetting as fundamental mathematical form
- Hardt et al. (2013): Two-phase memory consolidation (rapid then slow)
- Burnham & Anderson (2004): AIC model selection framework for comparing non-nested models

**Theoretical Predictions:**
- **Logarithmic model:** Predicts steeper decline early (0-24h) then asymptotic plateau
- **Power-law model:** Predicts log-log linearity (not directly tested here, log model is approximation)
- **Quadratic model:** Predicts curved trajectory with inflection point around consolidation window
- **Combined models (Lin+Log, Quad+Log):** Allow flexible approximation of complex forgetting dynamics

**Literature Gaps:**
Most forgetting studies test single functional form (usually logarithmic). Few studies systematically compare multiple candidate forms using model selection framework (AIC). Fewer still use IRT-derived ability estimates (avoiding CTT ceiling/floor artifacts). This RQ fills gap by testing 5 plausible forms and quantifying relative evidence via Akaike weights.

---

## Hypothesis

**Primary Hypothesis:**
Exploratory - no directional prediction. Competing theories support different functional forms. We compare 5 candidate models and select via AIC, quantifying relative evidence with Akaike weights.

**Secondary Hypotheses:**
1. Linear model likely to have worst fit (too simple to capture forgetting dynamics)
2. Combined models (Lin+Log, Quad+Log) may outperform single-term models (greater flexibility)
3. Best model should have Akaike weight > 0.30 (if <0.30, high uncertainty documented and top 2-3 models reported)

**Theoretical Rationale:**
This is exploratory analysis, not hypothesis-driven. Goal is to identify best approximating model for forgetting trajectories, not to confirm/reject specific theory. Different theories predict different forms, and we don't impose functional form a priori. Data selects best approximation. AIC framework (Burnham & Anderson, 2004) appropriate for exploratory model comparison where no single "true" model exists.

**Expected Effect Pattern:**
- Best model: Lin+Log or Quad+Log (combined models balance flexibility vs overfitting)
- ΔAIC between best and second-best > 2 (clear preference threshold per Burnham & Anderson)
- Akaike weight interpretation:
  - >0.90: Very strong evidence for best model
  - 0.60-0.90: Strong evidence
  - 0.30-0.60: Moderate evidence (consider model averaging)
  - <0.30: High uncertainty (report top 2-3 models)

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
  - Disambiguation: **ALL Where tags included** in omnibus factor

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ aggregates ALL VR items (What/Where/When, all paradigms) into single omnibus factor. Purpose is to identify overall functional form of forgetting, not domain-specific differences. Single-factor IRT calibration yields one theta estimate per participant×test. Domain-specific functional forms examined in separate RQs.

**Exclusion Rationale:**
None - all WWW domains and all paradigms included for comprehensive omnibus forgetting trajectory.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for functional form comparison

**High-Level Workflow:**

**Step 0:** Get IRT input data from RQ 5.1 (results/ch5/rq1/data/step00_irt_input.csv)

**Step 1:** IRT Pass 1 - Calibrate single omnibus factor "All" (all items), p1_med prior, 2-category GRM, extract Pass 1 theta scores and item parameters

**Step 2:** Item Purification - Apply Decision D039 thresholds (exclude items with |b| > 3.0 OR a < 0.4), create purified item list

**Step 3:** IRT Pass 2 - Re-calibrate with purified items only, extract final theta scores (Theta_All)

**Step 4:** Data preparation - Rename Theta_All to Theta, merge with TSVR data, create time transformations (Days, Days², log(Days+1)), validate completeness (400 observations = 100 UIDs × 4 tests)

**Step 5:** Fit 5 candidate LMMs with different functional forms:
  - Linear: Theta ~ Time
  - Quadratic: Theta ~ Time + Time²
  - Logarithmic: Theta ~ log(Time+1)
  - Lin+Log: Theta ~ Time + log(Time+1)
  - Quad+Log: Theta ~ Time + Time² + log(Time+1)
  - All models: Random intercepts and random slopes by UID
  - Fit with REML=False for valid AIC comparison

**Step 6:** Model selection via AIC - Compute AIC, BIC, log-likelihood for all 5 models, calculate Akaike weights (relative evidence, sum to 1.0), select best model via lowest AIC, save comparison table (CSV) and best model pickle

**Step 7:** Prepare plot data - Create dual-scale (theta + probability) plot data with observed means and predicted trajectories for best model

**Validation Steps:**
- After Step 1: validate_irt_convergence, validate_irt_parameters
- After Step 2: validate_purification_quality (retention rate, parameter distributions)
- After Step 3: validate_irt_convergence, validate_irt_parameters (Pass 2)
- After Step 5: validate_lmm_convergence (all 5 models)
- After Step 6: validate_akaike_weights (sum=1.0, best model weight)

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores (-ANS tags):** Dichotomize before IRT: 1 = 1, all <1 = 0 (no partial credit)
- **Confidence Ratings:** Use raw 1-5 Likert scale (no bias correction, preserves interpretability)
- **IRT Model:** GRM (Graded Response Model - handles both dichotomous and polytomous items)
- **Likert Response Bias:** Document response style patterns (% using full range vs extremes), do NOT correct

**Special Methods:**
- **2-Pass IRT Purification (Decision D039):** Mandatory for ALL 50 RQs. Pass 1: calibrate all items. Pass 2: re-calibrate with purified items (|b| ≤ 3.0 AND a ≥ 0.4). Rationale: Extreme item parameters introduce systematic bias that distorts ability scores regardless of dimensionality. Evidence: 46% residual variance reduction in validated IRT settings. Applies to unidimensional RQ 5.7 despite being single-factor model (purification improves measurement quality, not just cross-dimensional contamination control).
- **Single Omnibus Factor:** RQ 5.7 uses "All" factor (aggregates all items) unlike domain-specific RQs (What/Where/When factors)
- **p1_med Prior:** Uses medium-precision prior for theta estimation (Decision D068, precision=1.0)
- **REML=False:** Required for valid AIC comparison across models (REML likelihoods not comparable)
- **Akaike Weights:** Quantify relative evidence for each model; interpret as "probability" model is best in candidate set
- **GRM Model Clarification:** GRM (Graded Response Model) handles BOTH dichotomous (2 categories: 0, 1) and polytomous (5 categories: 1-5) items. For dichotomized accuracy, GRM reduces to 2PL dichotomous IRT mathematically. No conflict with thesis "dichotomous IRT" terminology - same model.

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1 (Domain-Specific Forgetting Trajectories)

**File Paths:**
- `results/ch5/rq1/data/step00_irt_input.csv` (IRT input data - will be processed with "All" factor instead of What/Where/When factors)

**Dependencies:**
RQ 5.1 must complete Step 0 (data preparation) before this RQ can run. RQ 5.7 uses same raw input data but processes with different IRT configuration (single omnibus factor instead of 3 domain-specific factors).

**Usage:**
This RQ reuses IRT input data from RQ 5.1 but calibrates with "All" analysis set (single factor aggregating all items) instead of domain-specific factors. Different IRT configuration yields different theta estimates optimized for omnibus forgetting trajectory.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (same as RQ 5.1)
- Note: Inherited from RQ 5.1 data preparation

**Items:**
- [x] All VR items (What/Where/When combined)
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (inherited from RQ 5.1)
- Note: Aggregated into single omnibus factor "All" instead of separate What/Where/When factors

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Note: Time variable uses TSVR (actual hours since encoding, labeled "Days" for interpretability)

---
