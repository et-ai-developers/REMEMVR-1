# RQ 5.5.2: Source-Destination Consolidation (Two-Phase)

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** Consolidation (Two-Phase)
**Full ID:** 5.5.2

---

## Research Question

**Primary Question:**
Do source (-U-) and destination (-D-) memories show different consolidation patterns across the Early (Day 0→1) and Late (Day 1→6) retention periods?

**Scope:**
This RQ examines consolidation patterns for pick-up locations (-U- tags, source memory) versus put-down locations (-D- tags, destination memory) across two retention windows: Early phase (tests T1→T2, 0-48 hours) and Late phase (tests T2→T3→T4, 48-144 hours). Sample: N=100 participants, 800 observations (400 per location type across 4 test sessions). Time measured using TSVR_hours (actual hours since encoding). Piecewise analysis with 48-hour breakpoint to test differential consolidation.

**Theoretical Framing:**
Tests whether weaker initial encoding (destination < source, per RQ 5.5.1) leads to differential consolidation trajectories. If destination encoding is weaker, destination memory may show steeper Early-phase forgetting due to sleep-dependent consolidation preferentially benefiting strongly encoded traces. Both location types expected to show consolidation benefit (Early slope > Late slope), but magnitude may differ. This RQ extends two-phase forgetting framework to the source-destination distinction, linking encoding strength to consolidation dynamics.

---

## Theoretical Background

**Relevant Theories:**
- **Two-phase consolidation theory** (Hardt et al., 2013; Wixted, 2004): Episodic forgetting exhibits rapid initial decay followed by slower stabilization. Consolidation window (first 24-48 hours) is critical for memory stabilization.
- **Sleep-dependent consolidation** (Diekelmann & Born, 2010): Sleep preferentially benefits strongly encoded memories. Weakly encoded traces may show less consolidation benefit or greater early vulnerability.
- **Synaptic homeostasis hypothesis** (Tononi & Cirelli, 2014): Sleep downscales weak synaptic traces while preserving strong ones. Predicts weak memories (destination) show greater early forgetting during consolidation window.
- **Encoding strength hypothesis** (from RQ 5.5.1): Source memory (-U-) benefits from richer encoding (object identification + location + schema support + retrieval practice), while destination memory (-D-) has minimal encoding depth (motor execution only). This differential strength should manifest in consolidation trajectories.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
If destination encoding is weaker than source (per RQ 5.5.1 findings), destination memory will show steeper Early-phase forgetting but similar Late-phase stabilization. Strongly encoded source memories benefit more from sleep-dependent consolidation. Both location types should show consolidation benefit (Early slope > Late slope), consistent with two-phase forgetting pattern. The LocationType × Phase interaction tests whether encoding strength modulates consolidation dynamics.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
If destination encoding is weaker than source (per RQ 5.5.1), destination memory will show STEEPER Early-phase forgetting (Day 0→1, 0-48h) but SIMILAR Late-phase stabilization (Day 1→6, 48-144h) compared to source memory. This predicts a significant LocationType × Phase interaction with destination showing relatively steeper Early slope.

**Secondary Hypotheses:**
1. Both location types will show consolidation benefit: Early-phase forgetting (Day 0→1) will be significantly steeper than Late-phase decay (Day 1→6) for both source and destination memory.
2. The magnitude of consolidation benefit may differ between location types, reflecting differential encoding strength effects on consolidation.

**Theoretical Rationale:**
Sleep-dependent consolidation (Diekelmann & Born, 2010) preferentially benefits strongly encoded memories. Source memory has richer encoding (object identification, schema support, retrieval practice per RQ 5.5.1 theory), while destination memory has minimal encoding depth (motor execution only). Synaptic homeostasis (Tononi & Cirelli, 2014) predicts weak traces are preferentially downscaled during sleep. Therefore, destination memory (weaker encoding) should show steeper Early-phase forgetting when consolidation mechanisms are active. Both types should stabilize by Late phase (consolidation complete), showing similar slow decay rates.

**Expected Effect Pattern:**
- **Main consolidation effect:** Early slope > Late slope for both location types (two-phase pattern replicates)
- **LocationType × Phase interaction:** Destination shows relatively steeper Early slope compared to source (p < 0.025 Bonferroni)
- **Effect size:** Cohen's f^2 for interaction > 0.02 (small effect threshold)
- Expected pattern: Source Early ≈ Destination Early initially, but destination drops more steeply during consolidation window

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - NOT included in this RQ (focuses on spatial memory: Where subdomain)

- [x] **Where** (Spatial Location) - SUBDOMAIN COMPARISON
  - [x] `-U-` tags (pick-up location, SOURCE memory, 18 items)
  - [x] `-D-` tags (put-down location, DESTINATION memory, 18 items)
  - [ ] `-L-` tags (static location, legacy) - EXCLUDED
  - **Disambiguation:** This RQ specifically examines the source vs destination distinction within spatial memory. Source (-U-) represents the location where an object was initially picked up (encoded during object interaction with elaborated processing). Destination (-D-) represents where that object was subsequently placed (encoded during motor execution with minimal elaboration).

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - NOT included in this RQ

**Inclusion Rationale:**
This RQ extends the source-destination framework (RQ 5.5.1) to test consolidation dynamics. Source vs destination represents a theoretically motivated distinction within spatial memory based on encoding depth and processing demands. Pick-up locations benefit from elaborated encoding (object identification + location + schema support), while put-down locations have minimal encoding (motor execution). This asymmetry should manifest in consolidation trajectories if sleep-dependent consolidation preferentially benefits strongly encoded traces.

**Exclusion Rationale:**
- `-L-` static location tags excluded because they don't map to source-destination distinction (legacy items)
- What (-N-) and When (-O-) excluded because this RQ focuses on spatial memory subdomain comparison
- Only interactive paradigms (IFR, ICR, IRE) included, excluding room-level recall (RFR, TCR) per standard Chapter 5 procedure

---

## Analysis Approach

**Analysis Type:**
Piecewise Linear Mixed Model (LMM) with two-phase time structure (Early: 0-48h, Late: 48-144h). Uses IRT-derived theta scores from RQ 5.5.1 as dependent variable.

**High-Level Workflow:**

**Step 0:** Load RQ 5.5.1 theta scores and TSVR mapping; verify dependency completion (RQ 5.5.1 status = success)

**Step 1:** Create piecewise time variables with 48-hour breakpoint: Early_time (within [0,48h]), Late_time (max(0, time-48)). Code Segment factor (Early: tests T1→T2, Late: tests T2→T3→T4). Compute Days_within (recentered time within each segment for interpretable intercepts).

**Step 2:** Reshape data from wide format (1 row per UID × test, 2 theta columns) to long format with LocationType factor (2 rows per UID × test). Validate: 800 observations (100 UID × 4 tests × 2 location types).

**Step 3:** Fit piecewise LMM: theta ~ Days_within × Segment × LocationType + (1 + Days_within | UID), REML=False. Model includes:
- Random intercepts by UID (baseline individual differences)
- Random slopes for Days_within by UID (individual forgetting rate differences)
- Three-way interaction to test hypothesis (LocationType × Phase interaction on slopes)

**Step 4:** Extract 4 segment-location slopes via linear combinations:
- Source_Early: Early-phase forgetting rate for source memory
- Source_Late: Late-phase decay rate for source memory
- Destination_Early: Early-phase forgetting rate for destination memory
- Destination_Late: Late-phase decay rate for destination memory

**Step 5:** Test consolidation benefit per location type: Early slope > Late slope? Compute difference (Early - Late) with 95% CI. If CI excludes 0, consolidation benefit confirmed.

**Step 6:** Test LocationType × Phase interaction (primary hypothesis): Does difference in consolidation benefit (Early - Late slope difference) differ between Source and Destination? Extract interaction term from model, apply Bonferroni alpha = 0.025 (2 main hypothesis tests: consolidation benefit per type). Report dual p-values per Decision D068 (p_uncorrected and p_bonferroni).

**Step 7:** Prepare piecewise plot data for visualization:
- Theta scale: Model-predicted trajectories for 4 conditions (2 locations × 2 segments), with 95% CI
- Probability scale: Convert theta predictions to probability using IRT response function (Decision D069)
- Both scales required for interpretation (theta = latent ability, probability = observable performance)

**Expected Outputs:**
- data/step00_theta_from_rq551.csv (loaded from RQ 5.5.1)
- data/step01_piecewise_lmm_input.csv (800 rows: 100 UID × 4 tests × 2 locations)
- data/step02_piecewise_lmm_model.pkl (saved model object)
- results/step02_piecewise_lmm_summary.txt (model convergence, fixed effects, random effects)
- results/step03_segment_location_slopes.csv (4 rows: Source_Early, Source_Late, Destination_Early, Destination_Late)
- results/step04_consolidation_benefit.csv (2 rows: Source, Destination consolidation benefit metrics)
- results/step05_interaction_tests.csv (LocationType × Phase interaction with dual p-values)
- plots/step06_piecewise_theta_data.csv (8 rows: 2 locations × 2 segments × 2 timepoints per segment)
- plots/step06_piecewise_probability_data.csv (8 rows: theta converted to probability scale)

**Success Criteria:**
- RQ 5.5.1 dependency verified: status = success, required files exist
- Model convergence: model.converged = True, no singular fit warnings
- 4 segment-location slopes extracted with valid SE and 95% CI (CI_lower < estimate < CI_upper)
- Consolidation benefit computed for both location types (Early - Late difference with CI)
- LocationType × Phase interaction tested with dual p-values (Decision D068: p_uncorrected and p_bonferroni both reported)
- Plot data: 8 rows per scale (theta and probability), correct segment assignments, probability in [0,1], no NaN values
- Interpretation aligns with hypothesis: If interaction significant (p < 0.025), destination shows steeper Early slope relative to source

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.5.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.5.1 (Source-Destination Trajectories - ROOT)

**File Paths:**
- results/ch5/5.5.1/data/step03_theta_scores.csv (IRT theta scores by location type: 400 rows, columns: UID, test, theta_source, theta_destination, se_source, se_destination)
- results/ch5/5.5.1/data/step00_tsvr_mapping.csv (TSVR time mapping: 400 rows, columns: UID, test, TSVR_hours)

**Dependencies:**
RQ 5.5.1 must complete Steps 0-3 (data extraction, IRT Pass 1, item purification, IRT Pass 2 calibration) before this RQ can run. Specifically:
- Step 0: Extraction of -U- and -D- items from dfData.csv
- Step 1: IRT Pass 1 calibration (2-factor GRM)
- Step 2: Item purification (Decision D039: |b| ≤ 3.0, a ≥ 0.4)
- Step 3: IRT Pass 2 re-calibration on purified items
Dependency validated via circuit breaker: If RQ 5.5.1 status ≠ success OR required files missing, rq_concept FAILS with EXPECTATIONS ERROR.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.5.1, no additional exclusions)
- Sample: 100 UID across all 4 test sessions

**Items:**
- N/A (theta scores already aggregated from purified -U- and -D- items in RQ 5.5.1)
- RQ 5.5.1 purified ~25-32 items per location type (from ~18 items each pre-purification)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from RQ 5.5.1
- Test timing: T1 (Day 0, ~0h), T2 (Day 1, ~24h), T3 (Day 3, ~72h), T4 (Day 6, ~144h)
- TSVR_hours used for precise time measurement (actual hours since encoding, not nominal days)

**Time Segmentation (Unique to this RQ):**
- Early segment: 0-48 hours (tests T1 → T2), consolidation window
- Late segment: 48-144 hours (tests T2 → T3 → T4), post-consolidation decay
- Breakpoint: 48 hours chosen based on consolidation literature (Diekelmann & Born, 2010)

---
