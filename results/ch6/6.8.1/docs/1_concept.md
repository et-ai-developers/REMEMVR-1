# RQ 6.8.1: Source-Destination Confidence Trajectories

**Chapter:** 6
**Type:** Source-Dest Confidence
**Subtype:** Trajectories
**Full ID:** 6.8.1

---

## Research Question

**Primary Question:**
Do source (-U-) and destination (-D-) locations show different confidence decline patterns over the 6-day retention interval?

**Scope:**
This RQ examines confidence decline trajectories for pick-up (source, -U-) versus put-down (destination, -D-) locations using IRT-derived ability estimates from TC_* confidence items. Analysis includes N=100 participants × 4 test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6) × 2 location types = 800 observations. Time variable uses TSVR (actual hours since encoding), not nominal days.

**Theoretical Framing:**
This RQ tests whether the source-destination dissociation found for accuracy in Ch5 5.5.1 replicates in metacognitive judgments. If destination confidence declines faster than source confidence (paralleling accuracy), this validates that the dissociation reflects fundamental memory processing differences rather than measurement artifacts. Alternatively, if confidence shows no dissociation despite accuracy differences, this suggests metacognitive monitoring cannot distinguish between source and destination memory strength.

---

## Theoretical Background

**Relevant Theories:**
- **Source Monitoring Framework** (Johnson et al., 1993): Distinguishes between memory for event content versus contextual details. Source memory (where object was first encountered) may be encoded more robustly than destination memory (where object was later placed) due to attentional differences during initial encoding versus automatic actions.
- **Encoding Specificity**: Pick-up locations coincide with initial object identification (deeper encoding), while put-down locations occur during task execution (potentially shallower encoding or divided attention).

**Key Citations:**
To be added by rq_scholar

**Theoretical Predictions:**
Destination confidence should decline faster than source confidence, replicating the Ch5 5.5.1 accuracy pattern. If confidence tracks underlying memory strength, LocationType × Time interaction should be significant.

**Literature Gaps:**
To be identified by rq_scholar

---

## Hypothesis

**Primary Hypothesis:**
Destination confidence will show faster decline than source confidence (significant LocationType × Time interaction), replicating Ch5 5.5.1 accuracy findings. This validates that the source-destination dissociation reflects fundamental memory processing differences visible in both accuracy and metacognition.

**Secondary Hypotheses:**
None specified - straightforward replication hypothesis.

**Theoretical Rationale:**
Ch5 5.5.1 found destination accuracy declined faster than source accuracy. If this reflects true differences in memory trace strength (not just measurement noise), confidence judgments should also detect these differences. Metacognitive monitoring should be sensitive to relative memory strength differences between source and destination.

**Expected Effect Pattern:**
Significant LocationType × Time interaction (p < 0.05 with dual p-values per Decision D068). Destination slope steeper (more negative) than source slope. Effect size comparable to Ch5 5.5.1 accuracy finding.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Not examined in this RQ (focus is on Where subdimensions)

- [x] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy - excluded)
  - [x] `-U-` tags (pick-up location, source)
  - [x] `-D-` tags (put-down location, destination)
  - Disambiguation: This RQ specifically examines the source-destination dissociation using only -U- (pick-up/source) and -D- (put-down/destination) tags. Legacy -L- tags excluded.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Not examined in this RQ

**Inclusion Rationale:**
Focus on spatial memory subdimensions (-U- vs -D-) to replicate Ch5 5.5.1 source-destination dissociation in confidence domain. Pick-up locations (source) represent initial encoding context; put-down locations (destination) represent goal-directed action context.

**Exclusion Rationale:**
What and When domains excluded - this RQ specifically targets spatial memory subdivisions to test whether source-destination differences extend from accuracy to metacognitive confidence.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) using GRM for 5-category ordinal confidence data + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 0:** Extract VR data from dfData.csv, filter TC_* confidence items to only -U- (source) and -D- (destination) tags
**Step 1:** IRT Pass 1 calibration with 2-factor GRM (Source/Destination factors) using p1_med prior on 5-category ordinal data (TC_ items: 0, 0.25, 0.5, 0.75, 1.0)
**Step 2:** Item purification (Decision D039): exclude items with |b| > 3.0 OR a < 0.4
**Step 3:** IRT Pass 2 re-calibration on purified items
**Step 4:** Merge theta_confidence scores with TSVR time mapping, create time transformations
**Step 5:** Fit LMM with LocationType × Time interaction and random slopes by UID
**Step 6:** Extract LocationType × Time interaction term, compute contrasts (Source vs Destination slopes)
**Step 7:** Compare results to Ch5 5.5.1 accuracy findings to test replication

**Expected Outputs:**
- data/step00_irt_input.csv (IRT input data)
- data/step00_tsvr_mapping.csv (time mapping)
- data/step02_purified_items.csv (purified item set)
- data/step03_theta_confidence_location.csv (800 rows: 100 participants × 4 tests × 2 locations)
- results/step05_lmm_summary.txt (LMM model summary)
- results/step06_location_contrasts.csv (Source vs Destination slope comparison)
- results/step07_ch5_comparison.csv (comparison to Ch5 5.5.1 accuracy pattern)

**Success Criteria:**
- IRT convergence: theta in [-4,4], SE in [0.1,1.5]
- GRM calibration for 5-category ordinal data (NOT 2PL which is for binary data)
- Item purification: 30-70% retention rate
- LMM converges with 800 observations
- LocationType × Time interaction tested with dual p-values (Decision D068)
- Ch5 5.5.1 comparison documented (does confidence dissociation replicate accuracy dissociation?)

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- Confidence items: TC_* (5-category ordinal: 0, 0.25, 0.5, 0.75, 1.0)
- Spatial subdimensions: -U- (source/pick-up) and -D- (destination/put-down)
- Excludes: -L- tags (legacy general location), -N- (What), -O- (When)

**Extraction Method:**
Step 0 extracts from dfData.csv using tag pattern matching for TC_*-U-* and TC_*-D-* items, creates:
- data/step00_irt_input.csv (wide format with 5-category ordinal responses, NOT binary)
- data/step00_tsvr_mapping.csv (time mapping with UID, TEST, TSVR_hours)
- data/step00_q_matrix.csv (2-factor structure: Source and Destination)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)

**Items:**
- [x] TC_* confidence items only (5-category Likert: 0, 0.25, 0.5, 0.75, 1.0)
- [x] -U- tags (source/pick-up locations)
- [x] -D- tags (destination/put-down locations)
- [ ] -L- tags - EXCLUDED (legacy general location)
- [ ] TQ_* accuracy items - EXCLUDED (this RQ examines confidence only)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)

---
