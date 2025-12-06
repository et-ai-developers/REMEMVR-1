# RQ 6.8.2: Source-Destination Calibration

**Chapter:** 6
**Type:** Source-Dest Confidence
**Subtype:** Calibration
**Full ID:** 6.8.2

---

## Research Question

**Primary Question:**
Are people better calibrated for source (pick-up location) or destination (put-down location) memory?

**Scope:**
This RQ examines metacognitive calibration differences between source and destination spatial memories across a 6-day retention interval. Analysis uses IRT-derived ability estimates for both accuracy (from Ch5 5.5.1) and confidence (from Ch6 6.8.1) across four test sessions (T1, T2, T3, T4). N=100 participants x 4 tests x 2 location types = 800 observations.

**Theoretical Framing:**
Source-destination dissociation in episodic memory (Ch5 5.5.1 found different forgetting patterns) may extend to metacognitive monitoring. If calibration differs by location type, this suggests metacognitive access is not uniform across spatial memory components but reflects the underlying memory processing differences.

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Component Spatial Memory Theory**: Source (pick-up) locations involve initial object-location binding during encoding, while destination (put-down) locations are encoded during automatic placement actions. These distinct encoding contexts may produce different metacognitive signatures.
- **Metacognitive Monitoring Theory**: Calibration quality depends on cue validity - if source and destination memories have different retrieval cue characteristics, confidence judgments may differ in accuracy.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
Source memory may show better calibration due to stronger encoding context (initial object identification occurs at pick-up location). Destination memory may show overconfidence - put-down actions are automatic and feel familiar, but Ch5 5.5.1 showed destination memory decays faster than source memory. If confidence doesn't adjust proportionally to the faster destination decay, overconfidence emerges.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
Source locations will show BETTER calibration (smaller |calibration| error, calibration closer to 0) than destination locations. Destination locations may show OVERCONFIDENCE (calibration > 0, confidence exceeds accuracy) because put-down actions feel familiar (high confidence) but decay faster (lower accuracy per Ch5 5.5.1).

**Secondary Hypotheses:**
LocationType x Time interaction may emerge: if destination accuracy declines faster than destination confidence adjusts, overconfidence should increase over time specifically for destination locations.

**Theoretical Rationale:**
Source memory involves deliberate encoding during object identification (stronger metacognitive signal). Destination memory involves automatic placement actions (weaker metacognitive signal, reliance on familiarity which is less diagnostic). Based on Ch5 5.5.1 finding that destination decays faster, if confidence doesn't track this differential decay, destination will show worse calibration.

**Expected Effect Pattern:**
Significant LocationType main effect on calibration (p < 0.05 with dual p-values per Decision D068). Expected pattern: Source calibration H 0 (well-calibrated), Destination calibration > 0 (overconfident). Possible LocationType x Time interaction if overconfidence worsens differentially.

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Not examined in this RQ (focus is spatial location only)

- [x] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy - NOT used)
  - [x] `-U-` tags (pick-up location / SOURCE)
  - [x] `-D-` tags (put-down location / DESTINATION)
  - Disambiguation: This RQ examines ONLY source (-U-) vs destination (-D-) spatial memories. Legacy -L- tags excluded. Source = pick-up location where object was initially found. Destination = put-down location where participant placed object.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Not examined in this RQ

**Inclusion Rationale:**
Focus on source vs destination dissociation discovered in Ch5 5.5.1 (different forgetting patterns). Testing whether metacognitive calibration also dissociates by location type. Only -U- and -D- tags used to ensure clean source-destination comparison.

**Exclusion Rationale:**
Legacy -L- tags excluded (ambiguous about source vs destination). What and When domains excluded (orthogonal to spatial location type question).

---

## Analysis Approach

**Analysis Type:**
Linear Mixed Models (LMM) for calibration trajectories with LocationType (Source vs Destination) as within-subjects factor

**High-Level Workflow:**

**Step 0:** Merge accuracy and confidence by location type
- Load accuracy theta from Ch5 5.5.1: results/ch5/5.5.1/data/step03_theta_accuracy_location.csv (800 rows)
- Load confidence theta from RQ 6.8.1: results/ch6/6.8.1/data/step03_theta_confidence_location.csv (800 rows)
- Merge by UID x TEST x LocationType (Source/Destination)
- Verify 800 observations after merge

**Step 1:** Compute calibration per location type
- Z-standardize both theta_accuracy and theta_confidence (separately for each location type to preserve within-location calibration signal)
- Compute calibration = theta_confidence - theta_accuracy
- Calibration > 0 indicates overconfidence (confidence exceeds accuracy)
- Calibration < 0 indicates underconfidence (accuracy exceeds confidence)
- Calibration H 0 indicates good calibration

**Step 2:** Fit LMM: Calibration ~ LocationType x Time + (Time | UID)
- LocationType = Source (-U-) vs Destination (-D-) [within-subjects factor]
- Time = TSVR (hours since encoding) or Days (TSVR/24)
- Random effects: Random intercepts and random slopes for Time by participant UID
- Estimation: REML=True for final model (unbiased variance estimates)

**Step 3:** Test location effects on calibration
- LocationType main effect: Does source vs destination differ in overall calibration?
- LocationType x Time interaction: Does calibration diverge over time?
- Report dual p-values (standard + Bonferroni/Kenward-Roger per Decision D068)
- Extract effect sizes (Cohen's d for LocationType effect)

**Step 4:** Plot calibration by location
- Prepare plot data: mean calibration by LocationType x Time
- Include error bars (95% CI)
- Horizontal line at Calibration = 0 (perfect calibration reference)
- Color-code: Source vs Destination trajectories

**Expected Outputs:**
- data/step01_calibration_by_location.csv (800 rows: UID, TEST, LocationType, theta_accuracy, theta_confidence, calibration)
- results/step02_lmm_summary.txt (model summary with coefficients, p-values)
- results/step03_location_effects.csv (LocationType main effect and interaction with dual p-values)
- plots/step04_calibration_by_location.csv (plot source data: LocationType x Time means + CI)

**Success Criteria:**
- Merge successful: 800 observations (100 UID x 4 tests x 2 location types)
- Calibration computed per person-location-timepoint (no missing values)
- LMM converges successfully (no singularity warnings)
- LocationType effects tested with dual p-values (Decision D068)
- Plot data includes 8 rows (2 LocationTypes x 4 tests) with means and CI

---

## Data Source

**Data Type:**
DERIVED (from Ch5 5.5.1 accuracy outputs and Ch6 6.8.1 confidence outputs)

### DERIVED Data Source:

**Source RQs:**
1. Ch5 RQ 5.5.1 (Source-Destination Accuracy Trajectories)
2. Ch6 RQ 6.8.1 (Source-Destination Confidence Trajectories)

**File Paths:**
- results/ch5/5.5.1/data/step03_theta_accuracy_location.csv (800 rows: UID, TEST, LocationType, theta_accuracy)
- results/ch6/6.8.1/data/step03_theta_confidence_location.csv (800 rows: UID, TEST, LocationType, theta_confidence)

**Dependencies:**
- RQ 5.5.1 must complete Steps 1-3 (IRT calibration for accuracy with Source/Destination factors)
- RQ 6.8.1 must complete Steps 1-3 (IRT calibration for confidence with Source/Destination factors)
- Both RQs must use identical LocationType coding: Source = -U- tags, Destination = -D- tags

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.5.1 and 6.8.1 - no additional exclusions)

**Items:**
- [x] Source location items (-U- tags): pick-up locations
- [x] Destination location items (-D- tags): put-down locations
- [ ] Legacy location items (-L- tags): EXCLUDED (ambiguous, not source-destination specific)
- Item purification performed independently by RQ 5.5.1 and 6.8.1 (may result in different item sets for accuracy vs confidence - this is expected and acceptable)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4 = Days 0, 1, 3, 6)

**Critical Merge Note:**
Merge by UID x TEST x LocationType. If item sets differ between accuracy and confidence due to independent purification, theta scores are still comparable (IRT ability estimates are item-invariant within each factor). Expected N=800 after merge (100 participants x 4 tests x 2 location types).

---
