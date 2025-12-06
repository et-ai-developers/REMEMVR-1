# RQ 6.7.1: Initial Confidence Predicting Forgetting Rates

**Chapter:** 6
**Type:** Predictive
**Subtype:** Day 0 Confidence
**Full ID:** 6.7.1

---

## Research Question

**Primary Question:**
Does high initial confidence at Day 0 predict slower forgetting trajectories across a 6-day retention interval?

**Scope:**
This RQ examines the relationship between initial metacognitive confidence (theta_confidence at T1/Day 0) and subsequent forgetting rates (random slopes from accuracy trajectories). Sample: N=100 participants with both Day 0 confidence estimates and individual forgetting slopes.

**Theoretical Framing:**
If metacognitive judgments at encoding reflect encoding quality, then items encoded with high confidence should show slower decay. Alternatively, if confidence judgments are imperfect or dissociated from encoding strength, initial confidence may not predict forgetting trajectories. This RQ tests whether Day 0 metacognitive state has predictive validity for subsequent memory dynamics.

---

## Theoretical Background

**Relevant Theories:**
- **Encoding Strength Theory**: Well-encoded items should generate both high confidence judgments and durable memory traces, creating positive correlation between Day 0 confidence and slower forgetting.
- **Metacognitive Monitoring Models**: If confidence judgments accurately reflect memory strength, high confidence should predict better retention. If metacognitive access is imperfect, confidence may dissociate from objective memory quality.
- **Levels of Processing**: Items encoded with elaborative processing should generate high confidence (due to fluent retrieval at encoding) and slower forgetting (due to rich trace formation).

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
High Day 0 confidence predicting slower forgetting would support the view that metacognitive judgments at encoding tap into encoding quality. Null result would suggest confidence is dissociated from factors controlling consolidation, possibly reflecting only retrieval fluency at T1 rather than trace durability.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
High Day 0 confidence may predict slower forgetting slope (well-encoded items have both high confidence and slower decay). Positive correlation expected between Day0_confidence and forgetting_slope (more positive/less negative slopes for high confidence individuals).

**Secondary Hypotheses:**
Alternatively, confidence may NOT predict forgetting if metacognitive judgments are imperfect and only reflect momentary retrieval fluency at T1 rather than encoding quality or consolidation trajectory.

**Theoretical Rationale:**
If confidence at encoding reflects genuine encoding strength (not just retrieval fluency), then high initial confidence should correlate with durable traces that resist decay. This assumes metacognitive monitoring has access to encoding quality information, not just retrieval ease.

**Expected Effect Pattern:**
Positive correlation between Day0_confidence and forgetting_slope. Tertile analysis (High/Med/Low initial confidence groups) should show high confidence group with slower (less negative) forgetting slopes. Direction of effect will clarify whether confidence has predictive validity for consolidation.

---

## Memory Domains

**Domains Examined:**

- [x] **Omnibus "All" Factor**
  - Description: Single aggregate confidence score combining all VR items
  - Parallels Ch5 5.1.X General analyses

**Inclusion Rationale:**
Uses omnibus confidence factor from RQ 6.1.1 to match the omnibus accuracy factor from Ch5 5.1.4. General forgetting slopes (not domain-specific) to test broad relationship between initial metacognitive state and memory dynamics.

**Exclusion Rationale:**
Domain-specific analyses not needed for this predictive RQ. Focus is on overall confidence-forgetting relationship, not domain differences.

---

## Analysis Approach

**Analysis Type:**
Correlation and regression analysis testing predictive relationship between Day 0 confidence and individual forgetting slopes

**High-Level Workflow:**

**Step 0:** Load Day 0 confidence from RQ 6.1.1 (theta_confidence at T1)
**Step 1:** Load forgetting slopes from Ch5 5.1.4 (random slopes from accuracy LMM)
**Step 2:** Compute correlation: Day0_confidence vs slope with dual p-values (Decision D068)
**Step 3:** Test if high confidence predicts slower forgetting (directional hypothesis)
**Step 4:** Tertile analysis - create High/Med/Low confidence tertiles, compare mean forgetting slopes across groups
**Step 5:** Prepare plot data showing relationship between initial confidence and forgetting trajectories

**Expected Outputs:**
- data/step01_predictive_data.csv (100 rows: UID, Day0_confidence, forgetting_slope)
- results/step02_correlation.csv (correlation coefficient, dual p-values)
- results/step03_tertile_slopes.csv (3 rows: tertile means for confidence and slopes)
- plots/step04_confidence_predicts_forgetting.csv (plot data showing relationship)

**Success Criteria:**
- Day 0 confidence extracted successfully from RQ 6.1.1 (100 values)
- Forgetting slopes extracted successfully from Ch5 5.1.4 (100 values)
- Correlation computed with dual p-values (Wald and LRT per Decision D068)
- Tertile analysis complete with valid group sizes (each tertile >= 30 participants)
- Direction of effect documented (positive/negative/null)
- Plot data complete with no missing values

---

## Data Source

**Data Type:**
DERIVED (from RQ 6.1.1 and Ch5 5.1.4 outputs)

### DERIVED Data Source:

**Source RQs:**
- **RQ 6.1.1** (Confidence Functional Form): Provides Day 0 confidence estimates
- **Ch5 5.1.4** (Accuracy ICC Decomposition): Provides individual forgetting slopes

**File Paths:**
- results/ch6/6.1.1/data/step03_theta_confidence.csv (confidence theta scores, filter to T1/Day 0)
- results/ch5/5.1.4/data/step04_random_effects.csv (individual random slopes for accuracy forgetting)

**Dependencies:**
- RQ 6.1.1 must complete Step 3 (IRT calibration for confidence)
- Ch5 RQ 5.1.4 must complete Step 4 (random effects extraction from accuracy LMM)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from both source RQs)
- No exclusions - all participants with both Day 0 confidence and forgetting slope estimates

**Items:**
- N/A (theta scores and slopes already aggregated to person-level)

**Tests:**
- Day 0 confidence: T1 only (baseline measurement)
- Forgetting slopes: Derived from all 4 tests (T1-T4) in Ch5 5.1.4

---
