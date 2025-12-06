# RQ 6.6.3: High-Confidence Errors - Domain Specificity

**Chapter:** 6
**Type:** HCE
**Subtype:** Domain Specificity
**Full ID:** 6.6.3

---

## Research Question

**Primary Question:**
Are high-confidence errors domain-specific, showing different rates for What versus Where versus When memory domains?

**Scope:**
This RQ examines high-confidence errors (HCE: Confidence >= 0.75 AND Accuracy = 0) at the item level across three episodic memory domains (What/Where/When) over four test sessions (T1, T2, T3, T4; Days 0, 1, 3, 6). Sample: ~27,200 item-responses (approximately 68 items × 100 participants × 4 tests). Analysis tests Domain × Time interaction effects on HCE rate using item-level confidence (TC_*) and accuracy (TQ_*) data.

**Theoretical Framing:**
High-confidence errors represent the most problematic metacognitive failure - being confidently wrong. Domain-specific differences in HCE rates could reveal differential metacognitive access to What (object identity), Where (spatial location), and When (temporal order) memory systems. The When domain, which showed floor effects in Ch5 accuracy analyses, may produce the highest HCE rates due to low accuracy combined with guessing that feels confident.

---

## Theoretical Background

**Relevant Theories:**

- **Dual-Process Theory (Yonelinas, 2002):** What memory can rely on familiarity (fast, automatic, high confidence), while Where and When require recollection (slow, effortful, more uncertain). Familiarity-based responses may generate more high-confidence errors when familiarity misleads.

- **Source Monitoring Framework (Johnson et al., 1993):** Different memory domains require different source monitoring processes. Spatial (Where) and temporal (When) memory require more complex source attribution than object identity (What), potentially leading to different metacognitive error patterns.

- **Consolidation Theory (Dudai, 2004):** Hippocampal-dependent domains (Where, When) may show different metacognitive signatures than perirhinal-dependent domains (What), with spatial/temporal memory being more vulnerable to high-confidence errors during consolidation.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**

The When domain is predicted to show the MOST high-confidence errors due to floor effects in accuracy (from Ch5) combined with guessing responses that may feel confident despite low accuracy. What and Where domains may differ if object memory versus spatial memory have different metacognitive access - What domain may show lower HCE rates if familiarity-based recognition provides more reliable confidence calibration, while Where domain may show intermediate HCE rates requiring spatial recollection with associated uncertainty.

**Literature Gaps:**
[To be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
When domain will show MOST high-confidence errors due to floor effects (low accuracy) combined with guessing (which may feel confident). Specifically: HCE_rate_When > HCE_rate_Where > HCE_rate_What.

**Secondary Hypotheses:**
What and Where domains may differ if object vs spatial memory have different metacognitive access. What domain may show lowest HCE rates if familiarity-based object recognition provides more reliable confidence calibration. Where domain may show intermediate HCE rates due to spatial recollection demands.

**Theoretical Rationale:**
Based on dual-process theory, What memory can rely on familiarity which, while potentially misleading, provides consistent confidence signals. Where and When memory require recollection, which is more vulnerable to source monitoring errors. The When domain specifically showed floor effects in Ch5 accuracy analyses, suggesting fundamental encoding/retrieval difficulties. When combined with metacognitive processes that may not fully adjust confidence for this difficulty, the result is high-confidence errors. Source monitoring framework suggests that temporal attribution is particularly challenging, leading to confident but incorrect temporal judgments.

**Expected Effect Pattern:**
Significant Domain × Time interaction (p < 0.05 Bonferroni corrected for multiple comparisons). When domain expected to show HCE rates > 15% (combining floor accuracy with maintained confidence). What domain expected to show HCE rates < 10% (better calibrated). Where domain intermediate (~12%). Time effect may show increasing HCE rates across all domains as memories degrade but confidence fails to fully adjust.

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: Object naming and identity recognition from interactive paradigms

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where tags included (-L-, -U-, -D-) to maximize statistical power for domain comparison. Separate -U-/-D- analysis is focus of RQ 6.8.X series.

- [x] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: Temporal order and sequence memory

**Inclusion Rationale:**
All three WWW episodic memory domains included to test domain-specific metacognitive failure patterns. Complete domain coverage allows testing whether HCE rates differ systematically across fundamental components of episodic memory (object identity, spatial context, temporal context). When domain critical despite Ch5 floor effects - if low accuracy combines with maintained confidence, produces highest HCE rates demonstrating metacognitive failure.

**Exclusion Rationale:**
None - complete WWW domain coverage required for domain comparison hypothesis.

---

## Analysis Approach

**Analysis Type:**
Item-level descriptive analysis + Linear Mixed Models (LMM) for Domain × Time interaction effects on HCE rates

**High-Level Workflow:**

**Step 0:** Extract item-level data from dfData.csv, filtering to both TQ_* (accuracy, dichotomous 0/1) and TC_* (confidence, 5-level ordinal: 0, 0.25, 0.5, 0.75, 1.0) items. Tag items by domain: What (*-N-*), Where (*-L-*/*-U-*/*-D-*), When (*-O-*). Sample: ~27,200 item-responses (68 items × 100 participants × 4 tests).

**Step 1:** Compute high-confidence error flags per item-response: HCE = 1 if (TQ_accuracy = 0 AND TC_confidence >= 0.75), else HCE = 0. Creates binary HCE flag for each of ~27,200 item-responses.

**Step 2:** Compute HCE rates aggregated by domain × timepoint: For each combination of domain (What/Where/When) and test session (T1/T2/T3/T4), compute HCE_rate = mean(HCE) across all item-responses in that cell. Produces 12 rows (3 domains × 4 tests) summarizing mean HCE rates.

**Step 3:** Fit Linear Mixed Model testing Domain × Time interaction: HCE_rate ~ Domain × Time + (Time | UID). Model tests whether HCE rate trajectories differ across domains. Random slopes by participant (UID) account for individual differences in HCE trajectory. REML=True for variance component estimation.

**Step 4:** Test Domain main effect and Domain × Time interaction using Bonferroni-corrected alpha = 0.025 (two tests). Extract fixed effect estimates, standard errors, t-statistics, and dual p-values (parametric + bootstrap per Decision D068). Report whether domain differences in HCE rates are statistically significant.

**Step 5:** Rank domains by mean HCE rate: Compute overall mean HCE rate per domain (averaged across all timepoints) and rank from highest to lowest. Compare to hypothesis prediction (When > Where > What). Report whether observed ranking matches theoretical prediction.

**Step 6:** Create plot data for visualization: Export domain × time HCE rates for plotting. Include observed mean HCE rates per domain per timepoint, plus LMM model predictions with confidence intervals. Data structured for downstream plotting by rq_plots agent.

**Expected Outputs:**
- data/step00_item_level.csv (~27,200 rows: item-level TQ_ accuracy + TC_ confidence with domain tags)
- data/step01_hce_by_domain.csv (~27,200 rows: item-level with HCE flag added)
- results/step02_hce_rates_summary.csv (12 rows: 3 domains × 4 tests with mean HCE rates)
- results/step03_domain_hce_lmm.txt (LMM summary output with fixed effects, random effects, fit statistics)
- results/step04_domain_effects.csv (Domain main effect and Domain × Time interaction statistics with dual p-values)
- results/step05_domain_ranking.csv (3 rows: domains ranked by mean HCE rate)
- plots/step06_hce_by_domain.csv (plot data: observed + predicted HCE rates by domain × time)

**Success Criteria:**
- Item-level extraction successful: ~27,200 item-responses with complete TQ_/TC_ data
- HCE flag computation correct: HCE = 1 only when accuracy = 0 AND confidence >= 0.75
- Domain × timepoint aggregation correct: 12 summary rows (3 domains × 4 tests)
- LMM convergence: Model converges with no singularity warnings
- Domain effects tested: Both Domain main effect and Domain × Time interaction tested with Bonferroni-corrected alpha = 0.025
- Dual p-values present per Decision D068
- Domain ranking complete: Observed ranking compared to hypothesis prediction (When > Where > What)
- Plot data complete: All 12 domain × time cells have observed and predicted HCE rates

---

## Data Source

**Data Type:**
DERIVED (from item-level accuracy and confidence data in dfData.csv)

### DERIVED Data Source:

**Source File:**
data/cache/dfData.csv (master dataset)

**Variables Required:**
- **UID:** Participant ID (N=100)
- **TEST:** Test session (T1, T2, T3, T4)
- **TQ_* items:** Accuracy (dichotomous 0/1) for all VR memory items
- **TC_* items:** Confidence (5-level ordinal: 0, 0.25, 0.5, 0.75, 1.0) for all VR memory items
- **Tag structure:** Item tags containing domain codes (-N-, -L-/-U-/-D-, -O-)

**Tag Patterns:**
- **What domain:** Items with `-N-` tag (object naming/identity)
- **Where domain:** Items with `-L-` (legacy location), `-U-` (pick-up location), or `-D-` (put-down location) tags
- **When domain:** Items with `-O-` tag (temporal order)

**Extraction Method:**
Step 0 extracts from dfData.csv using tag pattern matching:
1. Filter to interactive paradigm items (IFR/ICR/IRE, excluding RFR/TCR/RRE)
2. Extract both TQ_* (accuracy) and TC_* (confidence) columns for same items
3. Tag each item by domain based on tag patterns
4. Reshape to long format: one row per item-response (~27,200 rows)
5. Creates data/step00_item_level.csv with columns: UID, TEST, item_id, domain, TQ_accuracy, TC_confidence

**Dependencies:**
None - this is root-level extraction from dfData.csv. However, conceptually builds on:
- RQ 6.1.1 (establishes confidence measurement with 5-level GRM IRT)
- RQ 6.3.1 (establishes domain-level confidence trajectories)
- RQ 6.6.1 (establishes HCE definition and temporal trajectory)

Item-level analysis required here (not theta scores) because HCE is defined at individual item-response level, not participant-level aggregates.

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- Sample: N=100 with complete data across all 4 test sessions

**Items:**
- [x] All VR interactive paradigm items with matching TQ_/TC_ pairs
- [x] Items must have domain tags (-N-, -L-/-U-/-D-, -O-) for classification
- [ ] Exclude: Room Free Recall (RFR) and other non-interactive items (no confidence ratings)
- [ ] Exclude: Items missing either TQ_ or TC_ data

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Complete test coverage required to examine HCE trajectory over retention interval

**Note on When domain:**
When domain included despite Ch5 floor effects. If purification in RQ 6.3.1 resulted in <10 items, may affect statistical power but is theoretically critical for testing hypothesis that floor effects + guessing = high HCE rates.

---
