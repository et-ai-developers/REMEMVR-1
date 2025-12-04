# RQ 5.5.1: Source-Destination Spatial Memory Trajectories

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** Trajectories (ROOT)
**Full ID:** 5.5.1

---

## Research Question

**Primary Question:**
Do pick-up locations (source: -U-) and put-down locations (destination: -D-) show different forgetting trajectories in VR episodic spatial memory?

**Scope:**
This RQ examines forgetting trajectories for two types of spatial location memory in VR: source memory (pick-up locations tagged -U-) and destination memory (put-down locations tagged -D-). Sample: N=100 participants × 4 test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6) × 2 location types = 800 observations (400 per location type). Time variable uses TSVR_hours (actual hours since encoding). Items: 18 -U- items, 18 -D- items. Only interactive paradigms included (IFR, ICR, IRE); RFR, TCR, and static -L- location items excluded.

**Theoretical Framing:**
This RQ addresses a fundamental dissociation in episodic spatial memory: whether the location where an object was first encountered (source) differs in forgetting trajectory from the location where it was placed (destination). This distinction has theoretical implications for encoding depth, schema support, and goal-related memory processes. The RQ is a ROOT analysis, extracting directly from raw data (dfData.csv) to establish foundational source-destination trajectories.

---

## Theoretical Background

**Relevant Theories:**

1. **Proactive Interference Theory** (Underwood, 1957): Source locations are encoded first during VR exploration and receive retrieval practice advantage during subsequent actions. This temporal priority predicts better source memory retention.

2. **Schema Support / Levels of Processing** (Bartlett, 1932; Craik & Lockhart, 1972): Source locations have stronger schema support because objects are typically found in semantically appropriate locations (e.g., keys on table, book on shelf). Destination locations may violate schemas (e.g., keys placed in drawer). Deeper, schema-consistent encoding predicts slower forgetting for source memory.

3. **"Lost Keys" Phenomenon** (Real-world Evidence): Everyday memory failures predominantly involve forgetting where objects were placed (destination), not where they were originally found (source). This anecdotal evidence suggests destination memory is inherently more difficult or vulnerable to forgetting.

4. **Goal Discounting / Zeigarnik Effect** (Zeigarnik, 1927; Förster et al., 2005): Information relevant to ongoing goals receives processing advantage. Once a goal is completed (object placed at destination), goal-related information may be released or downgraded in priority. This predicts weaker encoding and faster forgetting for destination memory.

5. **Attention Allocation During Encoding**: Pick-up actions require dual attention to both object identity (What) and location (Where), resulting in elaborated, multimodal encoding. Put-down actions may be more automatic motor executions with less attentional focus on location encoding. This predicts stronger, more durable source memory traces.

**Key Citations:**
To be added by rq_scholar

**Theoretical Predictions:**
These converging theoretical perspectives predict: (1) Source memory accuracy will be higher than destination memory across all timepoints (main effect of LocationType with -U- > -D-); (2) Destination memory may show steeper forgetting trajectory (LocationType × Time interaction, with -D- exhibiting faster decay).

**Literature Gaps:**
This RQ addresses whether the source-destination dissociation, which has been observed in laboratory studies, replicates in ecologically valid VR episodic memory with naturalistic retention intervals (6-day span with sleep consolidation). The interactive VR paradigm allows for controlled manipulation of source vs destination encoding while maintaining high ecological validity.

---

## Hypothesis

**Primary Hypothesis:**
Source memory (-U-) will show HIGHER accuracy than destination memory (-D-) across all timepoints. This will manifest as a significant main effect of LocationType (source > destination) in the best-fitting linear mixed model (LMM).

**Secondary Hypotheses:**
1. A LocationType × Time interaction may emerge, with destination memory showing steeper forgetting than source memory across the 6-day retention interval.
2. The source-destination difference will be present at encoding (Day 0) and maintained across all test sessions (Days 1, 3, 6).

**Theoretical Rationale:**
Five converging theoretical mechanisms support this prediction: (1) Proactive interference theory: source encoded first with retrieval practice advantage; (2) Schema support: source locations have stronger semantic coherence; (3) Real-world "lost keys" phenomenon: destination memory failures are more common; (4) Goal discounting: destination information released after goal completion; (5) Attention allocation: pick-up requires elaborated dual encoding (object + location), while put-down may be automatic motor execution with minimal location encoding.

**Expected Effect Pattern:**
- **Main Effect:** LocationType main effect with source > destination, p < 0.025 (Bonferroni-corrected alpha for 2 primary tests: main effect and interaction).
- **Interaction Effect:** LocationType × Time interaction may be significant, with effect sizes at Days 0, 1, 3, 6 showing progressive divergence (destination forgetting faster than source).
- **Model Selection:** Best-fitting LMM (among 5 candidate time transformations: Linear, Quadratic, Logarithmic, Linear+Logarithmic, Quadratic+Logarithmic) will be selected via AIC. Akaike weights will sum to 1.0 +/- 0.01, with best model weight > 0.30 indicating clear winner.
- **Post-Hoc Contrasts:** Dual p-values (uncorrected and Bonferroni-corrected per Decision D068) will be reported for transparency.
- **Effect Size:** Cohen's d or f^2 will quantify the magnitude of source-destination difference at each timepoint.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT examined in this RQ (focused on spatial location only)

- [x] **Where** (Spatial Location)
  - [x] `-U-` tags (pick-up location / source memory)
  - [x] `-D-` tags (put-down location / destination memory)
  - [ ] `-L-` tags (static location, legacy) - EXCLUDED
  - Disambiguation: This RQ specifically examines the source-destination dissociation within spatial memory. -U- tags represent the location where an object was first encountered (pick-up, source). -D- tags represent the location where the participant placed the object (put-down, destination). Static -L- location items are excluded to isolate the source-destination manipulation.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT examined in this RQ (focused on spatial location only)

**Inclusion Rationale:**
This RQ targets a specific within-domain dissociation in spatial memory. Only -U- (source) and -D- (destination) items are included to directly compare forgetting trajectories for these two types of location memory. The theoretical question is whether the temporal and functional distinction between source and destination during encoding produces differential forgetting patterns.

**Exclusion Rationale:**
- **-L- tags excluded:** Static location items (legacy tagging system) do not have a source-destination manipulation and would confound the analysis.
- **-N- (What) excluded:** Object identity is orthogonal to this spatial location question.
- **-O- (When) excluded:** Temporal order is orthogonal to this spatial location question.
- **RFR, TCR excluded:** Room Free Recall and Template Cued Recall paradigms do not involve interactive pick-up/put-down actions and thus lack the source-destination structure.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 0:** Data Extraction from Raw Source
- Extract VR episodic memory data from data/cache/dfData.csv
- Filter to interactive paradigms only (IFR, ICR, IRE)
- Filter to source (-U-) and destination (-D-) location items only
- Dichotomize responses: TQ < 1 -> 0 (incorrect), TQ >= 1 -> 1 (correct)
- Create Q-matrix with 2 factors: source (all *-U-* items), destination (all *-D-* items)
- Expected: 18 items per factor (36 total), N=100 participants, 4 tests = 14,400 item-level responses
- Outputs: data/step00_irt_input.csv (wide format binary responses), data/step00_q_matrix.csv (2-factor structure), data/step00_tsvr_mapping.csv (time mapping with TSVR_hours)

**Step 1:** IRT Pass 1 - Initial Calibration
- Calibrate 2-dimensional Graded Response Model (GRM) with correlated factors (source, destination)
- Prior: p1_med (median difficulty prior per project standards)
- Estimation method: Maximum Likelihood
- Extract item parameters (discrimination a, difficulty b) and ability estimates (theta_source, theta_destination)
- Convergence validation: theta in [-4, 4], SE in [0.1, 1.5]

**Step 2:** Item Purification (Decision D039)
- Apply purification criteria: exclude items with |b| > 3.0 OR a < 0.4
- Extreme difficulty items (|b| > 3.0) provide little information at typical ability levels
- Low discrimination items (a < 0.4) fail to differentiate between ability levels
- Requirement: Retain >= 10 items per location type to maintain reliable measurement
- Expected: 25-32 items retained (70-90% retention)
- Output: data/step02_purified_items.csv (list of retained items with parameters)

**Step 3:** IRT Pass 2 - Re-calibration on Purified Items
- Re-calibrate 2-dimensional GRM on purified item set
- Same model specification as Pass 1 (correlated factors, p1_med prior)
- Extract final theta scores (theta_source, theta_destination) for 100 participants × 4 tests = 400 observations
- Output: data/step03_theta_scores.csv (400 rows, columns: UID, test, theta_source, theta_destination, SE_source, SE_destination)

**Step 4:** Data Preparation for LMM
- Merge theta scores with TSVR mapping (time since encoding in hours)
- Reshape from wide format (theta_source, theta_destination) to long format with LocationType factor
- Treatment coding: Source as reference level (Source = 0, Destination = 1)
- Create time transformations: Days = TSVR_hours/24, log_Days_plus1 = log(Days + 1), Days_squared
- Validate: 800 observations (100 participants × 4 tests × 2 location types)
- Output: data/step04_lmm_input.csv (800 rows, columns: UID, test, TSVR_hours, Days, LocationType, theta, SE)

**Step 5:** LMM Model Selection
- Fit 5 candidate LMMs with LocationType × Time interactions, varying time transformation:
  1. Linear: theta ~ Days × LocationType + (Days | UID)
  2. Quadratic: theta ~ (Days + Days_squared) × LocationType + (Days | UID)
  3. Logarithmic: theta ~ log_Days_plus1 × LocationType + (log_Days_plus1 | UID)
  4. Linear + Logarithmic: theta ~ (Days + log_Days_plus1) × LocationType + (Days | UID)
  5. Quadratic + Logarithmic: theta ~ (Days + Days_squared + log_Days_plus1) × LocationType + (Days | UID)
- All models: REML=False (for AIC comparison), random slopes by UID (allows individual variation in forgetting rate)
- Model selection: Compute AIC for all 5 models, identify best (lowest AIC)
- Compute Akaike weights: Evidence ratio for each model relative to best model
- Threshold: Best model weight > 0.30 indicates clear winner (not merely least bad)
- Outputs: results/step05_model_comparison.csv (5 rows: model name, AIC, delta_AIC, weight), data/step05_lmm_fitted_model.pkl (saved best model)

**Step 6:** Post-Hoc Hypothesis Tests
- Extract fixed effects from best model: LocationType main effect, LocationType × Time interaction
- Test LocationType main effect: source vs destination difference averaged across time (Bonferroni alpha = 0.025 for 2 primary tests)
- Test LocationType × Time interaction: Do forgetting rates differ between source and destination?
- Compute effect sizes at Days 0, 1, 3, 6: Cohen's d or marginal means difference with 95% CIs
- Report dual p-values per Decision D068: p_uncorrected AND p_bonferroni for transparency and replicability
- Outputs: results/step06_post_hoc_contrasts.csv (LocationType main effect, interaction, Bonferroni-corrected p-values), results/step06_effect_sizes.csv (effect sizes at each timepoint with CIs)

**Step 7:** Prepare Plot Data (Decision D069)
- Generate trajectory data on two scales: theta scale (ability metric) and probability scale (interpretable as accuracy)
- Theta scale: Marginal means for source and destination at Days 0, 1, 3, 6 with 95% CIs from best LMM
- Probability scale: Convert theta to predicted probability of correct response using IRT transformation (logistic function with average item difficulty)
- Structure: 2 location types × 4 timepoints = 8 rows per scale
- Validation: Probability values must be in [0, 1], no NaN values
- Outputs: plots/step07_trajectory_theta_data.csv (8 rows: LocationType, Days, theta_mean, CI_lower, CI_upper), plots/step07_trajectory_probability_data.csv (8 rows: LocationType, Days, prob_mean, CI_lower, CI_upper)

**Expected Outputs:**
- data/step00_irt_input.csv (wide format binary responses)
- data/step00_q_matrix.csv (2-factor Q-matrix)
- data/step00_tsvr_mapping.csv (time mapping)
- data/step02_purified_items.csv (25-32 retained items with parameters)
- data/step03_theta_scores.csv (400 rows: final theta scores by participant × test)
- data/step04_lmm_input.csv (800 rows: long format for LMM)
- results/step05_model_comparison.csv (5 candidate models with AIC, Akaike weights)
- data/step05_lmm_fitted_model.pkl (saved best-fitting LMM)
- results/step06_post_hoc_contrasts.csv (LocationType main effect and interaction tests)
- results/step06_effect_sizes.csv (effect sizes at Days 0, 1, 3, 6)
- plots/step07_trajectory_theta_data.csv (8 rows: trajectory data on theta scale)
- plots/step07_trajectory_probability_data.csv (8 rows: trajectory data on probability scale)

**Success Criteria:**
- **IRT Convergence:** All theta estimates in [-4, 4] range, standard errors in [0.1, 1.5] range (indicates reliable estimation)
- **Purification:** >= 10 items retained per location type (minimum 20 total out of 36), expected 25-32 items (70-90% retention)
- **LMM Convergence:** Best model converges successfully, no singularity warnings
- **Observation Count:** Exactly 800 observations in merged LMM input (100 participants × 4 tests × 2 location types)
- **Model Selection:** Akaike weights sum to 1.0 +/- 0.01 (numerical precision check)
- **Model Quality:** Best model weight > 0.30 (clear evidence for selected model)
- **Dual P-Values:** All hypothesis tests report both p_uncorrected and p_bonferroni per Decision D068
- **Plot Data Validation:** 8 rows per plot file (2 location types × 4 timepoints), probability values in [0, 1], no NaN values
- **File Integrity:** All expected output files exist with correct row counts and column structure

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv) - This is a ROOT RQ

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- **Source memory (pick-up location):** Items with `-U-` tag (e.g., TQ_VR_IFR_i2_N_U, TQ_VR_ICR_i4_D_U)
- **Destination memory (put-down location):** Items with `-D-` tag (e.g., TQ_VR_IFR_i1_O_D, TQ_VR_IRE_i6_N_D)
- **Paradigm filtering:** Include only interactive paradigms (IFR = Item Free Recall, ICR = Item Cued Recall, IRE = Item Recognition)
- **Exclusions:**
  - Static location items with `-L-` tag (legacy spatial memory items without source-destination manipulation)
  - Room Free Recall (RFR) and Template Cued Recall (TCR) paradigms (no interactive pick-up/put-down actions)

**Extraction Method:**
Step 0 extracts VR episodic memory item responses from dfData.csv using the following procedure:
1. Filter columns to TQ_VR_* items matching interactive paradigms (IFR, ICR, IRE)
2. Further filter to items with -U- or -D- location tags only
3. Expected: 18 items per tag type (36 total items)
4. Dichotomize responses: TQ < 1 -> 0 (incorrect), TQ >= 1 -> 1 (correct binary response)
5. Create Q-matrix with 2 correlated factors: source (all *-U-* items loading on Factor 1), destination (all *-D-* items loading on Factor 2)
6. Extract TSVR (Time Since Virtual Reality session) variable per participant × test, convert to TSVR_hours (actual hours since encoding)
7. Output files: data/step00_irt_input.csv (wide format binary responses, 100 rows × 36 item columns × 4 tests), data/step00_q_matrix.csv (36 rows × 2 factor columns), data/step00_tsvr_mapping.csv (400 rows: UID, test, TSVR_hours)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- No participant-level exclusions; all participants who completed VR testing are included

**Items:**
- [x] Interactive paradigm items only: IFR (Item Free Recall), ICR (Item Cued Recall), IRE (Item Recognition)
- [x] Source location items: `-U-` tag (pick-up location, 18 items)
- [x] Destination location items: `-D-` tag (put-down location, 18 items)
- [ ] **EXCLUDED:** Static location items with `-L-` tag (do not have source-destination manipulation)
- [ ] **EXCLUDED:** RFR (Room Free Recall) paradigm (no item-level pick-up/put-down actions)
- [ ] **EXCLUDED:** TCR (Template Cued Recall) paradigm (no item-level pick-up/put-down actions)
- **Rationale:** Only items with explicit source-destination structure (-U- vs -D-) from interactive paradigms (IFR/ICR/IRE) are included to isolate the source-destination dissociation

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 corresponding to nominal Days 0, 1, 3, 6)
- Time variable: TSVR_hours (actual hours since VR encoding session, not nominal days)
- No test-level exclusions

---
