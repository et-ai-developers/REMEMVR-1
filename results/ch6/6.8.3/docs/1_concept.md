# RQ 6.8.3: Source-Destination Confidence ICC - Opposite Correlation Pattern

**Chapter:** 6
**Type:** Source-Dest Confidence
**Subtype:** ICC
**Full ID:** 6.8.3

---

## Research Question

**Primary Question:**
Does confidence ICC reveal the same opposite-correlation pattern as accuracy? Specifically, do source (-U-) and destination (-D-) locations show opposite intercept-slope correlations in confidence trajectories, replicating the Ch5 5.5.6 accuracy findings?

**Scope:**
This RQ examines intraclass correlation coefficients (ICC) for confidence trajectories across source (pick-up location, -U-) and destination (put-down location, -D-) memory. Sample: N=100 participants x 4 test sessions x 2 location types = 800 observations. Time variable uses TSVR (actual hours since encoding). Focus on intercept-slope correlation patterns per location type.

**Theoretical Framing:**
CRITICAL REPLICATION TEST: Ch5 5.5.6 discovered fundamentally opposite forgetting dynamics - Source memory showed r=+0.99 intercept-slope correlation (regression to mean pattern: high baseline -> slower decay), while Destination memory showed r=-0.90 correlation (fan effect pattern: high baseline -> faster decay). If this opposite pattern replicates in confidence data, it validates that source and destination memory operate under different forgetting mechanisms at both the memory and metacognitive levels. If confidence shows same pattern, suggests integrated memory-metacognition system. If different pattern, suggests dissociable systems.

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory** (Yonelinas, 2002): Source memory (pick-up location) may rely on recollection (effortful retrieval with access to encoding context), while destination memory (put-down location) may rely more on familiarity (automatic processing during action execution).
- **Encoding Depth** (Craik & Lockhart, 1972): Source locations receive deeper encoding (object identification occurs at pick-up), while destination locations receive shallower encoding (automatic action endpoint). Depth may affect both memory and metacognitive monitoring.
- **Regression to Mean vs Fan Effect**: Two opposite statistical patterns - regression to mean predicts convergence (high baseline -> slower decay), fan effect predicts divergence (high baseline -> faster decay due to interference or fragility of strong initial encoding).

**Key Citations:**
To be added by rq_scholar

**Theoretical Predictions:**
If source-destination dissociation reflects fundamental memory architecture differences, the opposite intercept-slope correlation pattern should replicate in confidence. Source confidence: high baseline confidence should predict slower confidence decay (r > 0, regression to mean). Destination confidence: high baseline confidence should predict faster confidence decay (r < 0, fan effect). Replication would be strongest evidence yet that source and destination memory operate under different forgetting dynamics.

**Literature Gaps:**
No prior studies have examined whether opposite forgetting dynamics replicate across memory accuracy and metacognitive confidence. This RQ tests whether the Ch5 5.5.6 discovery generalizes beyond accuracy to the metacognitive level.

---

## Hypothesis

**Primary Hypothesis:**
Source confidence will show POSITIVE intercept-slope correlation (r > +0.50, replicating Ch5 5.5.6 r=+0.99 pattern: high baseline confidence -> slower confidence decay). Destination confidence will show NEGATIVE intercept-slope correlation (r < -0.50, replicating Ch5 5.5.6 r=-0.90 pattern: high baseline confidence -> faster confidence decay).

**Secondary Hypotheses:**
If confidence correlations are weaker than accuracy correlations (e.g., Source r_confidence=+0.60 vs r_accuracy=+0.99), suggests metacognitive monitoring has less access to the underlying forgetting dynamics than direct memory performance. If confidence correlations are similar strength, suggests tight coupling between memory and metacognition.

**Theoretical Rationale:**
The opposite pattern in Ch5 5.5.6 was the most striking individual difference finding in the entire thesis - two memory systems with fundamentally opposite forgetting dynamics within the same task. If this replicates in confidence, it validates that: (1) source and destination are genuinely different memory systems, not just different difficulty levels, (2) metacognitive monitoring has access to these system-level differences, (3) confidence is not just rescaled accuracy but reflects underlying memory architecture.

**Expected Effect Pattern:**
Source: intercept-slope correlation r > +0.50 (ideally approaching +0.99 if perfect replication)
Destination: intercept-slope correlation r < -0.50 (ideally approaching -0.90 if perfect replication)
Critical test: correlations should have OPPOSITE signs
Comparison to Ch5 5.5.6 should document: correlation magnitudes, confidence intervals, direction consistency

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Not examined in this RQ (focus on spatial memory only)

- [x] **Where** (Spatial Location)
  - [x] `-U-` tags (pick-up location, SOURCE)
  - [x] `-D-` tags (put-down location, DESTINATION)
  - [ ] `-L-` tags (general location, legacy - not used)
  - Disambiguation: Separate analyses for -U- (source) and -D- (destination). Source = location where object was initially picked up and identified. Destination = location where object was placed/put down during encoding.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Not examined in this RQ (focus on spatial memory only)

**Inclusion Rationale:**
This RQ specifically examines source-destination dissociation in confidence. Only -U- (source) and -D- (destination) location memory items are included. Ch5 5.5.6 discovered the opposite correlation pattern for accuracy; this RQ tests whether confidence replicates the pattern.

**Exclusion Rationale:**
What (-N-) and When (-O-) domains are excluded because this RQ focuses specifically on the source-destination dissociation within spatial memory. Legacy -L- tags are excluded because they don't disambiguate source vs destination.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for confidence ability estimation (using GRM for 5-category ordinal data) + LMM (Linear Mixed Models) with random slopes for ICC decomposition + correlation analysis for intercept-slope patterns

**High-Level Workflow:**

**Step 1:** Fit location-stratified LMMs with random slopes for source (-U-) and destination (-D-) confidence trajectories separately (data from RQ 6.8.1)

**Step 2:** Extract variance components per location type - var_intercept (baseline confidence variability between people), var_slope (forgetting rate variability between people), cov_int_slope (intercept-slope covariance), var_residual (within-person unexplained variance)

**Step 3:** Compute intercept-slope correlations per location type - Source correlation and Destination correlation, with confidence intervals

**Step 4:** CRITICAL COMPARISON: Compare confidence correlations to Ch5 5.5.6 accuracy correlations (Source r=+0.99, Destination r=-0.90). Document: direction consistency (opposite signs), magnitude similarity, confidence interval overlap

**Expected Outputs:**
- data/step02_variance_components.csv (10 rows: 5 variance parameters x 2 location types)
- data/step04_random_effects.csv (200 rows: 100 participants x 2 location types, REQUIRED for RQ 6.8.4 clustering)
- data/step05_intercept_slope_correlations.csv (2 rows: Source and Destination correlations with CIs)
- results/step06_ch5_comparison.csv (CRITICAL: comparison to Ch5 5.5.6 accuracy pattern)

**Success Criteria:**
- Both location-stratified LMMs converge (Source model and Destination model)
- Variance components successfully extracted for both location types
- Intercept-slope correlations computed with confidence intervals
- CRITICAL: Ch5 5.5.6 comparison documented (Source r=+0.99, Destination r=-0.90 accuracy pattern vs confidence pattern)
- Test of opposite signs: Source correlation and Destination correlation should have different signs
- Random effects file has 200 rows (100 participants x 2 location types) for downstream clustering (RQ 6.8.4)

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.8.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 6.8.1 (Source-Destination Confidence Trajectories)

**File Paths:**
- results/ch6/6.8.1/data/step03_theta_confidence_location.csv (800 rows: 100 participants x 4 tests x 2 location types, IRT-derived confidence theta scores)
- Metadata inherited from RQ 6.8.1: TSVR time mapping, location type labels (-U- vs -D-)

**Dependencies:**
RQ 6.8.1 must complete Steps 1-3 (IRT calibration with 2-factor GRM for source and destination confidence, purification, re-calibration) before this RQ can run. Additionally, Ch5 5.5.6 results must be available for comparison (Source r=+0.99, Destination r=-0.90 accuracy intercept-slope correlations).

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants from RQ 6.8.1 (inherited inclusion criteria)
- No exclusions - full sample needed for individual difference analysis

**Items:**
- N/A (theta scores already aggregated across items within each location type)
- Item-level purification completed in RQ 6.8.1 Step 2

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4) inherited from RQ 6.8.1
- Time variable: TSVR (actual hours since encoding, not nominal days)

**Location Types:**
- [x] Source (-U- tags): pick-up locations
- [x] Destination (-D- tags): put-down locations
- [ ] Legacy -L- tags: excluded (no source-destination disambiguation)

**Comparison Data:**
- [x] Ch5 5.5.6 accuracy results: Source r=+0.99 intercept-slope correlation, Destination r=-0.90 intercept-slope correlation
- Comparison required to assess replication of opposite pattern in confidence data

---

**End of 1_concept.md for RQ 6.8.3**
