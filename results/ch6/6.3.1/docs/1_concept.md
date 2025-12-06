# RQ 6.3.1: Domain Confidence Trajectories

**Chapter:** 6
**Type:** Domain Confidence
**Subtype:** Trajectories
**Full ID:** 6.3.1

---

## Research Question

**Primary Question:**
Do What/Where/When episodic memory domains show different confidence decline patterns across a 6-day retention interval?

**Scope:**
This RQ examines confidence trajectories for three WWW episodic memory domains using IRT-derived ability estimates from 5-level Likert confidence ratings (TC_* items: 0, 0.25, 0.5, 0.75, 1.0). Data includes N=100 participants × 4 test sessions (T1, T2, T3, T4; nominal Days 0, 1, 3, 6) × 3 domains (What, Where, When) = 1200 observations. Time variable uses TSVR (actual hours since encoding). Graded Response Model (GRM) for ordinal data with 3-factor structure (What/Where/When).

**Theoretical Framing:**
Tests whether metacognitive monitoring (confidence) shows the same domain-invariant pattern found for accuracy in Ch5 5.2.1. If confidence parallels accuracy, domain × time interaction should be NULL (unitized VR encoding eliminates domain separation). Possible exception: When domain may show overconfidence if floor effects in accuracy (Ch5) persist but confidence doesn't adjust.

---

## Theoretical Background

**Relevant Theories:**
- **Dual-Process Theory** (Yonelinas, 2002): Memory retrieval relies on familiarity (fast, automatic) and recollection (slow, effortful). What domain can rely on familiarity, while Where/When require recollection. If confidence tracks retrieval process, domains may show different confidence trajectories even if accuracy trajectories are similar.
- **Consolidation Theory** (Dudai, 2004): Hippocampal-dependent memories (Where, When) consolidate more slowly and show greater vulnerability during consolidation compared to perirhinal-dependent memories (What). If confidence reflects consolidation quality, Where/When may show faster confidence decline.
- **Unitized Encoding in VR** (Ch5 finding): Immersive VR encoding creates unitized WWW memory representations, eliminating traditional domain separations. If true, confidence should also be domain-invariant.

**Key Citations:**
[To be added by rq_scholar]

**Theoretical Predictions:**
NULL expected based on Ch5 5.2.1 findings: Domain differences were NULL for accuracy (unitized encoding eliminates separation). If confidence parallels accuracy, domain × time interaction should be NULL. However, When domain showed floor effects in Ch5 accuracyif confidence doesn't adjust to this poor performance, overconfidence may emerge (low accuracy but maintained confidence).

**Literature Gaps:**
- Whether metacognitive monitoring (confidence) shows same domain-invariant pattern as objective memory performance
- Whether VR unitized encoding affects confidence judgments similarly to accuracy
- Whether When domain floor effects produce dissociation between confidence and accuracy

[Additional gaps to be identified by rq_scholar]

---

## Hypothesis

**Primary Hypothesis:**
NULL hypothesis: Domain × Time interaction will be non-significant (p > 0.05), replicating Ch5 5.2.1 accuracy findings. Confidence decline rate will not differ across What/Where/When domains.

**Secondary Hypotheses:**
1. When domain may show highest baseline confidence despite lowest accuracy (overconfidence pattern)
2. If When domain has <10 items after purification (due to Ch5 floor effects), exclude from analysis and document

**Theoretical Rationale:**
Ch5 5.2.1 found unitized VR encoding eliminates traditional WWW domain separations in accuracy trajectories. If metacognitive monitoring (confidence) reflects the same underlying memory representations, confidence should show identical domain-invariant pattern. Exception: When domain floor effects in Ch5 may indicate fundamental encoding failureif confidence doesn't track this poor performance, dissociation emerges.

**Expected Effect Pattern:**
- Domain × Time interaction: p > 0.05 (NULL)
- Main effect of Time: p < 0.05 (all domains decline)
- Main effect of Domain: possible at baseline (What/Where > When) but not interaction with Time
- Post-hoc contrasts: What vs Where (NULL), When vs others (possible baseline difference only)
- When domain status: if <10 items remain after purification, document and exclude

---

## Memory Domains

**Domains Examined:**

- [x] **What** (Object Identity)
  - Tag Code: `*-N-*` (name/object identity in TC_* confidence items)
  - Description: Confidence ratings for object identity retrieval (What object was in this location?)

- [x] **Where** (Spatial Location)
  - [x] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location)
  - [x] `-D-` tags (put-down location)
  - Disambiguation: All Where subtags included (`*-L-*`, `*-U-*`, `*-D-*`) for comprehensive spatial confidence assessment

- [x] **When** (Temporal Order)
  - Tag Code: `*-O-*` (order/temporal sequence in TC_* confidence items)
  - Description: Confidence ratings for temporal order retrieval (When did this event occur relative to others?)

**Inclusion Rationale:**
All three WWW domains included to parallel Ch5 5.2.1 accuracy analysis. Comprehensive domain assessment tests whether metacognitive monitoring (confidence) shows same unitized pattern as objective performance. Where subtags (-L-, -U-, -D-) combined for maximum power and consistency with Ch5 approach.

**Exclusion Rationale:**
When domain may be excluded AFTER item purification if <10 items remain (Ch5 showed When floor effects). Decision criterion: post-purification item count. If excluded, analysis proceeds with What/Where only and documents reason.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for confidence ability estimation using Graded Response Model (GRM) for 5-category ordinal data + LMM (Linear Mixed Models) for domain × time trajectory modeling

**High-Level Workflow:**

**Step 0:** Extract TC_* confidence items from dfData.csv, filter by domain tags (What: *-N-*, Where: *-L-*/*-U-*/*-D-*, When: *-O-*). Create 3-factor Q-matrix (What/Where/When).

**Step 1:** IRT Pass 1 calibration with 3-factor GRM (Graded Response Model for 5-category ordinal: 0, 0.25, 0.5, 0.75, 1.0), p1_med prior. GRM required (NOT 2PL) because TC_* items are ordinal, not dichotomous.

**Step 2:** Item purification (Decision D039): exclude items with |b| > 3.0 OR a < 0.4. Check When domain item countif <10 items remain, exclude entire When domain and document.

**Step 3:** IRT Pass 2 re-calibration on purified items with updated Q-matrix. Extract theta_confidence scores per domain (1200 observations: 100 participants × 4 tests × 3 domains).

**Step 4:** Merge theta_confidence_domain with TSVR time data. Create time transformations per Ch5 best model (likely log-transformed based on 6.1.1 functional form results).

**Step 5:** Fit LMM with Domain × Time interaction: theta ~ Domain × Time + (Time | UID), REML=False for model comparison. Test Domain × Time interaction (primary hypothesis).

**Step 6:** Post-hoc contrasts if Domain × Time significant: What vs Where, When vs others (What+Where). Bonferroni correction for multiple comparisons.

**Step 7:** Compare to Ch5 5.2.1 accuracy domain analysis. Document convergence/divergence between confidence and accuracy domain patterns.

**Step 8:** Document When domain status: item count after purification, inclusion/exclusion decision, rationale.

**Expected Outputs:**
- data/step00_irt_input.csv (TC_* items by domain, wide format)
- data/step00_tsvr_mapping.csv (time mapping for 1200 observations)
- data/step00_q_matrix.csv (3-factor: What/Where/When)
- data/step02_purified_items.csv (item retention rates per domain)
- data/step03_theta_confidence_domain.csv (1200 rows: UID × test × domain × theta)
- data/step04_lmm_input.csv (1200 rows with time transformations)
- results/step05_lmm_summary.txt (Domain × Time interaction test)
- results/step06_domain_contrasts.csv (post-hoc comparisons if needed)
- results/step07_ch5_comparison.csv (confidence vs accuracy domain patterns)
- results/step08_when_domain_status.txt (item count, inclusion decision)

**Success Criteria:**
- IRT convergence: theta in [-4,4], SE in [0.1,1.5]
- GRM calibration successful for 5-category ordinal data (NOT 2PL)
- Purification: item retention documented per domain
- When domain: if <10 items post-purification, excluded and documented
- 1200 observations total (or 800 if When excluded: 100 × 4 × 2 domains)
- LMM convergence: Domain × Time interaction tested with dual p-values (Decision D068)
- Ch5 5.2.1 comparison documented (convergence/divergence)
- Post-hoc contrasts Bonferroni-corrected if interaction significant

---

## Data Source

**Data Type:**
RAW (extracts directly from dfData.csv)

### RAW Data Extraction:

**Source File:**
data/cache/dfData.csv

**Tag Patterns:**
- **What domain:** TC_* items containing `*-N-*` tag (object identity confidence)
- **Where domain:** TC_* items containing `*-L-*`, `*-U-*`, or `*-D-*` tags (spatial location confidence)
- **When domain:** TC_* items containing `*-O-*` tag (temporal order confidence)
- **Item type:** TC_* only (5-category ordinal confidence ratings: 0, 0.25, 0.5, 0.75, 1.0)
- **Paradigm codes:** Interactive paradigms only (IFR, ICR, IRE)
- **Exclude:** TQ_* accuracy items, RFR/TCR/RRE non-interactive paradigms

**Extraction Method:**
Step 0 extracts from dfData.csv, filtering to TC_* confidence items and creating:
- data/step00_irt_input.csv (wide format: UID × Item, 5-category ordinal responses)
- data/step00_tsvr_mapping.csv (UID × test × TSVR_hours time mapping)
- data/step00_q_matrix.csv (3-factor structure: What=1/Where=2/When=3)

Domain assignment based on tag parsing:
- What: if tag contains '-N-'
- Where: if tag contains '-L-' OR '-U-' OR '-D-'
- When: if tag contains '-O-'

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (no exclusions)
- N=100 across all analyses

**Items:**
- [x] TC_* confidence items only (5-category Likert: 0, 0.25, 0.5, 0.75, 1.0)
- [x] Interactive paradigms only (IFR, ICR, IRE)
- [ ] TQ_* accuracy items - EXCLUDED (Chapter 5 data, not confidence)
- [ ] RFR/TCR/RRE paradigms - EXCLUDED (non-interactive)
- Domain-specific inclusion:
  - What (*-N-*): all items passing purification
  - Where (*-L-*/*-U-*/*-D-*): all subtags combined, all items passing purification
  - When (*-O-*): conditionalif e10 items after purification, include; if <10, exclude entire domain

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- TSVR (actual hours since encoding) used for time variable, not nominal days

**Critical Notes:**
1. GRM (Graded Response Model) REQUIRED for 5-category ordinal dataNOT 2PL which assumes dichotomous responses
2. When domain conditional inclusion based on post-purification item count (e10 threshold)
3. 1200 total observations if all domains included (100 × 4 × 3), or 800 if When excluded (100 × 4 × 2)
4. Direct comparison to Ch5 5.2.1 accuracy domain analysis to test confidence-accuracy convergence

---
