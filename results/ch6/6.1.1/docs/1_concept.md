# RQ 6.1.1: Functional Form Comparison for Confidence Decline

**Chapter:** 6
**Type:** Confidence
**Subtype:** Model Selection
**Full ID:** 6.1.1

---

## Research Question

**Primary Question:**
Which functional form best describes confidence decline over a 6-day retention interval in VR episodic memory?

**Scope:**
This RQ examines confidence trajectory patterns using IRT-derived ability estimates from 5-level Likert confidence ratings (TC_* items: 0, 0.25, 0.5, 0.75, 1.0) across four test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6). Time variable uses TSVR (actual hours since encoding), with transformations: Days = TSVR_hours/24, Days_squared, log_Days_plus1. Compares 5 candidate models (Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic). N=100 participants × 4 tests = 400 observations.

**Theoretical Framing:**
Exploratory analysis paralleling Ch5 5.1.1 (accuracy functional form) to determine optimal functional form for confidence trajectory modeling. Best model selected via AIC and Akaike weights. This is foundation for all confidence trajectory analyses in Chapter 6.

---

## Theoretical Background

**Relevant Theories:**
- **Metacognitive Monitoring Theory**: Confidence judgments reflect metacognitive assessment of memory strength. If confidence tracks memory decay, both should show similar functional forms (e.g., logarithmic decline).
- **Dual-Process Theory**: If confidence relies on familiarity (fast-decaying) while accuracy reflects recollection (slower consolidation), functional forms may differ between confidence and accuracy.
- **Sleep-Dependent Consolidation**: Consolidation processes affecting memory traces should similarly affect metacognitive monitoring if monitoring is veridical.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If confidence monitoring tracks accuracy decline, logarithmic model should best fit confidence trajectories (paralleling Ch5 accuracy findings). Rapid early decline (Day 0->1, sleep-dependent consolidation window) followed by asymptotic leveling. If confidence and accuracy show divergent functional forms, suggests dissociable memory vs metacognition systems.

**Literature Gaps:**
Few studies examine confidence trajectory functional forms in ecologically valid VR episodic memory with multi-session longitudinal design. This RQ addresses whether metacognitive monitoring mirrors memory decay patterns.

---

## Hypothesis

**Primary Hypothesis:**
Exploratory analysis comparing 5 candidate models (Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic). Expected: Logarithmic model best (paralleling Ch5 accuracy findings). Akaike weight > 0.30 for best model.

**Secondary Hypotheses:**
None - exploratory functional form determination.

**Theoretical Rationale:**
If confidence tracks accuracy (veridical metacognitive monitoring), both should show rapid early decline followed by asymptotic leveling, characteristic of logarithmic functions. This pattern reflects sleep-dependent consolidation (Day 0->1 rapid decay) and subsequent stabilization. Non-linear forms (logarithmic) typically fit forgetting data better than linear forms based on empirical forgetting curves.

**Expected Effect Pattern:**
Best model identified by lowest AIC. Akaike weights sum to 1.0 +/- 0.01. Best model weight > 0.30 indicates clear winner. Comparison to Ch5 5.1.1 accuracy model selection will test if confidence and accuracy share functional form.

---

## Memory Domains

**Domains Examined:**

- [x] **Omnibus "All" Factor**
  - Description: Single aggregate factor combining all TC_* confidence items across What/Where/When domains
  - Tag Code: All VR confidence items (TC_*)
  - Rationale: Parallels Ch5 5.1.1 General analysis (omnibus factor)

- [ ] **What** (Object Identity)
  - Analyzed separately in RQ 6.3.1 (Domain Confidence)

- [ ] **Where** (Spatial Location)
  - Analyzed separately in RQ 6.3.1 (Domain Confidence)

- [ ] **When** (Temporal Order)
  - Analyzed separately in RQ 6.3.1 (Domain Confidence)

**Inclusion Rationale:**
This RQ parallels Ch5 5.1.1 General analysis using omnibus "All" factor to determine overall confidence trajectory functional form. Domain-specific analyses deferred to RQ 6.3.1 Domains type.

**Exclusion Rationale:**
Room Free Recall (RFR), Test-Cued Recall (TCR), and Room Recognition (RRE) paradigms excluded - focus on interactive VR paradigms only (IFR, ICR, IRE) to match Ch5 General type methodology.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) with Graded Response Model (GRM) for 5-category ordinal confidence data + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 0:** Extract VR data from data/cache/dfData.csv, filter to TC_* confidence items (5-level Likert: 0, 0.25, 0.5, 0.75, 1.0) for omnibus "All" factor. Create IRT input (wide format), TSVR mapping, and Q-matrix (single factor).

**Step 1:** IRT Pass 1 calibration with single omnibus "All" factor on all TC_* items using Graded Response Model (GRM) for 5-category ordinal data, p1_med prior. GRM appropriate for ordered polytomous responses (NOT 2PL which is for dichotomous).

**Step 2:** Item purification (Decision D039): exclude items with |b| > 3.0 (threshold parameter) OR a < 0.4 (discrimination parameter). Target 30-70% item retention.

**Step 3:** IRT Pass 2 re-calibration on purified items using GRM. Extract theta_confidence scores (ability estimates on latent confidence trait).

**Step 4:** Merge theta_confidence with TSVR (time since VR in hours), create time transformations: Days = TSVR/24, Days_squared, log_Days_plus1 = log(Days + 1).

**Step 5:** Fit 5 candidate LMMs with REML=False for model comparison:
- Model 1: Linear (theta ~ Days)
- Model 2: Quadratic (theta ~ Days + Days_squared)
- Model 3: Logarithmic (theta ~ log_Days_plus1)
- Model 4: Linear+Logarithmic (theta ~ Days + log_Days_plus1)
- Model 5: Quadratic+Logarithmic (theta ~ Days + Days_squared + log_Days_plus1)
All models include random intercepts and slopes by participant (UID).

**Step 6:** Model selection via AIC (Akaike Information Criterion). Compute Akaike weights (model probabilities). Identify best model (lowest AIC, highest weight).

**Step 7:** Compare to Ch5 5.1.1 accuracy model selection. Document if confidence and accuracy share same functional form or diverge.

**Expected Outputs:**
- data/step00_irt_input.csv (wide format TC_* confidence responses)
- data/step00_tsvr_mapping.csv (UID × TEST × TSVR hours)
- data/step00_q_matrix.csv (single "All" factor Q-matrix)
- data/step02_purified_items.csv (30-70% items retained after purification)
- data/step03_theta_confidence.csv (400 rows: 100 UID × 4 tests, theta_confidence scores)
- data/step04_lmm_input.csv (400 rows: theta_confidence + TSVR + time transformations)
- results/step05_model_comparison.csv (5 models: AIC, BIC, log-likelihood)
- data/step06_best_model.pkl (saved LMM model object)
- results/step06_aic_comparison.csv (Akaike weights per model)
- results/step07_ch5_comparison.csv (confidence vs accuracy model comparison)

**Success Criteria:**
- IRT convergence: theta_confidence in [-4, 4], standard errors in [0.1, 1.5]
- GRM used for 5-category ordinal data (NOT 2PL for dichotomous)
- Purification: 30-70% item retention
- All 5 LMMs converge successfully
- AIC values finite for all models
- Akaike weights sum to 1.0 +/- 0.01
- Best model Akaike weight > 0.30 (clear winner threshold)
- Comparison to Ch5 5.1.1 documented

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- Confidence items: TC_* (5-level Likert: 0, 0.25, 0.5, 0.75, 1.0)
- Paradigm codes: Interactive paradigms only (IFR, ICR, IRE)
- Excludes: RFR (Room Free Recall), TCR (Test-Cued Recall), RRE (Room Recognition)

**Extraction Method:**
Step 0 extracts from dfData.csv, filtering to TC_* confidence items across all What/Where/When domains and all interactive paradigms. Creates:
- data/step00_irt_input.csv (wide format: UID × items, 5-category ordinal responses)
- data/step00_tsvr_mapping.csv (UID × TEST × TSVR hours since encoding)
- data/step00_q_matrix.csv (single "All" factor: all items load on one dimension)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] All TC_* confidence items (5-level Likert)
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED
- [ ] Test-Cued Recall (TCR) - EXCLUDED
- [ ] Room Recognition (RRE) - EXCLUDED

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)

**Critical Note:**
TC_* items are 5-category ordinal (0, 0.25, 0.5, 0.75, 1.0), NOT dichotomous like TQ_* accuracy items. This requires Graded Response Model (GRM) in IRT, NOT 2PL. GRM is appropriate for ordered polytomous responses.

---
