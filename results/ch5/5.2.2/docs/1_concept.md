# RQ 5.2.2: Differential Consolidation Across Memory Domains

**Chapter:** 5
**RQ Number:** 2.2
**Full ID:** 5.2.2

---

## Research Question

**Primary Question:**
Do memory domains (What/Where) show different rates of forgetting during the early consolidation window (Day 0->1) versus later decay (Day 1->6)?

**Scope:**
This RQ examines whether sleep-dependent consolidation (first ~24 hours post-encoding, including one night's sleep) differentially benefits memory domains. Uses piecewise time structure with two segments:
- Early segment: Days 0-1 (consolidation window)
- Late segment: Days 1-6 (decay-dominated phase)

The analysis tests for differential forgetting slopes across segments and domains using a 3-way interaction model.

**Note on When Domain Exclusion:**
When domain excluded due to floor effects discovered in RQ 5.2.1 (6-9% probability, 77% item exclusion). Analysis focuses on What vs Where comparison only.

**Theoretical Framing:**
Sleep consolidation theory predicts that hippocampal-dependent memories receive greater benefit from sleep-dependent replay and consolidation processes. Since spatial memory (Where) is more hippocampus-dependent than object identity (What), we expect spatial memory to show less decline during the early consolidation window.

---

## Theoretical Background

**Relevant Theories:**
- **Sleep-Dependent Consolidation:** Sleep, particularly slow-wave sleep, facilitates memory consolidation through hippocampal-cortical dialogue. The first night post-encoding is critical for initial consolidation (Rasch & Born, 2013).
- **Hippocampal Replay:** During sleep, hippocampal place cells replay recent experiences, strengthening spatial and contextual memories preferentially (Wilson & McNaughton, 1994).
- **Systems Consolidation:** Hippocampal-dependent memories gradually become independent of the hippocampus over time, but the first 24 hours are critical for initial stabilization.

**Key Citations:**
- Rasch & Born (2013): Sleep consolidation preferentially benefits hippocampal-dependent memories
- Hippocampal replay theories: Where memory is more hippocampus-dependent than What memory

**Theoretical Predictions:**
Spatial memory (Where) should show the smallest decline during the Early segment (Day 0-1) due to preferential consolidation benefit. Object identity (What) may show less consolidation benefit as it relies more on perirhinal/familiarity processes.

**Literature Gaps:**
Most consolidation studies examine single memory domains or use recognition paradigms. This RQ tests whether consolidation benefits differ across WWW episodic memory components in an ecologically valid VR paradigm with longitudinal follow-up.

---

## Hypothesis

**Primary Hypothesis:**
Sleep-dependent consolidation (Day 0->1, including one night's sleep) may benefit spatial memory (Where) more than semantic (What), based on hippocampal replay theories.

**Secondary Hypotheses:**
1. Early segment slopes (Day 0-1) will be steeper than late segment slopes (Day 1-6), consistent with two-phase forgetting
2. The 3-way interaction (Days_within x Segment x Domain) will be significant, indicating domain-specific consolidation effects

**Theoretical Rationale:**
Hippocampal replay during sleep preferentially strengthens spatial and contextual memories. Where memory relies heavily on hippocampal binding of spatial information, while What memory can rely more on perirhinal cortex and familiarity processes. Therefore, Where should benefit most from the consolidation window.

**Expected Effect Pattern:**
Significant 3-way interaction: Days_within:Segment[T.Late]:Domain[T.Where]. Where should show less decline in Early segment compared to What (consolidation benefit). The slope difference (Early vs Late) should be larger for Where than for What.

**Note:** Original hypothesis included When domain. With When excluded due to floor effects, analysis focuses on What vs Where comparison only.

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
  - Disambiguation: **ALL Where tags included** (inherited from RQ5.1 theta scores)

- [ ] **When** (Temporal Order) - **EXCLUDED**
  - Tag Code: `-O-`
  - Description: Temporal order / sequence

**Inclusion Rationale:**
This RQ tests domain-specific consolidation effects comparing What and Where domains. Analysis uses theta scores from RQ5.1, which already aggregates domain-specific ability estimates.

**Exclusion Rationale:**
**When domain EXCLUDED due to floor effect discovered in RQ 5.2.1:**
- Performance at 6-9% probability throughout study (near 0% floor)
- 20/26 When items (77%) excluded for low discrimination (a < 0.4)
- Only 6 items retained, limiting reliability
- Cannot meaningfully interpret When domain forgetting trajectory
- Per RQ 5.2.1 recommendation: "Exclude When domain from subsequent RQs until resolved"

---

## Analysis Approach

**Analysis Type:**
LMM (Linear Mixed Models) with piecewise time structure

**High-Level Workflow:**

**Step 1:** Data Preparation
- Use theta scores from RQ5.1 Analysis (results/ch5/5.1.1/...)
- Reshape to long format (Domain as factor variable)
- Create piecewise time structure:
  - Early segment: Days 0-1 (consolidation window, includes one night's sleep)
  - Late segment: Days 1-6 (decay-dominated phase)
  - CRITICAL: Assign Day 1 to Early only (no overlap)
- Create "Days_within" variable (centered at 0 for each segment start)
- Verify no overlap in segment assignments

**Step 2:** Piecewise LMM with 3-Way Interaction
- Formula: Theta ~ Days_within x Segment x Domain
- Treatment coding: What as reference domain, Early as reference segment
- Random effects: Intercepts and slopes by UID
- Fit with REML=False
- Save model pickle

**Step 3:** Extract Key Effects
- Main effect: Days_within:Segment[T.Late] (slope difference between segments)
- 3-way interaction: Days_within:Segment[T.Late]:Domain[T.Where/When]
  - Tests whether consolidation benefit differs by domain

**Step 4:** Compute Slopes by Segment and Domain
- Extract early segment slopes (What/Where/When)
- Extract late segment slopes (What/Where/When)
- Create summary table with slopes, SEs, and 95% CIs

**Step 5:** Planned Contrasts
- Test hypothesis: Where shows less decline in Early segment (consolidation benefit)
- Bonferroni correction: alpha = 0.05/6 = 0.0083 for 6 planned comparisons
- Report results both with and without Bonferroni correction
- Report domain-specific consolidation effects

**Step 6:** Visualization
- Generate piecewise trajectory plot showing slope change at ~24 hours
- Separate lines for What/Where/When
- Highlight Early vs Late segments

**Data Preprocessing (Per Solution Section 1.4):**
- N/A - Uses DERIVED data (theta scores from RQ5.1 already preprocessed)

**Special Methods:**
- **Piecewise LMM:** Allows different slopes for consolidation (Day 0-1) vs decay (Day 1-6) phases
- **Day 1 Assignment to Early Only:** Theoretically motivated - consolidation completes by ~24h post-encoding
- **3-Way Interaction:** Tests if consolidation benefit differs by domain (key hypothesis)
- **Random Slopes within UID:** Accounts for individual differences in consolidation efficiency
- **TSVR Time Variable:** Use actual hours since encoding from TSVR data, not nominal days

---

## Data Source

**Data Type:**
DERIVED (from RQ5.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.1 (Domain-Specific Forgetting Trajectories)

**File Paths:**
- `results/ch5/5.1.1/data/...` (theta scores from IRT calibration)
- Exact file paths determined by RQ5.1 output structure

**Dependencies:**
RQ 5.1 must complete successfully before this RQ can run. Specifically requires:
- IRT calibration and purification (2-pass)
- Theta score extraction per participant x test x domain

**Usage:**
This RQ uses domain-specific theta scores from RQ5.1 as the outcome variable for piecewise trajectory modeling with segment-based analysis.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All participants from RQ5.1 (inherited inclusion criteria)

**Items:**
- N/A (theta scores already aggregated per domain from RQ5.1)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Note: T1 and T2 form Early segment (Days 0-1); T3 and T4 form Late segment (Days 1-6)
- Time variable uses TSVR (actual hours since encoding)

---
