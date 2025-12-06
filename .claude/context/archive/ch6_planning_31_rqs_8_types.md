# Chapter 6 Planning: 31 RQs across 8 Types

**Topic:** ch6_planning_31_rqs_8_types
**Created:** 2025-12-07 (context-manager archival)
**Last Updated:** 2025-12-07

---

## Chapter 6 Planning and Infrastructure Setup (2025-12-06 16:30)

**Task:** Chapter 6 Planning and Infrastructure Setup

**Context:** Chapter 5 effectively complete. User requested Chapter 6 planning based on Ch5 results, creation of story.md elevator pitches, and rq_info.tsv for all Ch6 RQs.

**Archived from:** state.md Session (2025-12-06 16:30)
**Original Date:** 2025-12-06 16:30
**Reason:** Ch6 planning complete, infrastructure built, execution phase underway

---

### Major Accomplishments

#### 1. Updated Ch5 story.md with Complete Elevator Pitches

Added comprehensive RQ elevator pitch section (lines 29-119) covering all 36/38 completed RQs:
- **Type 5.1:** 5 RQs (5.1.1-5.1.5) - General forgetting trajectories
- **Type 5.2:** 7 RQs (5.2.1-5.2.7) - Domain-specific forgetting
- **Type 5.3:** 9 RQs (5.3.1-5.3.9) - Paradigm-specific forgetting
- **Type 5.4:** 7 RQs (5.4.1-5.4.7) - Schema congruence effects
- **Type 5.5:** 7 RQs (5.5.1-5.5.7) - Source-destination memory

**Elevator pitch format:** 1-2 sentences covering WHAT was tested + KEY finding + CONTEXT/implication

#### 2. Created Chapter 6 Analysis Plan (results/ch6/plan.md)

Comprehensive planning document including:
- **Design Rationale:** How Ch5 findings inform Ch6 structure
- **Why Confidence Data is Special:** 5-level Likert provides 2.3× more information per response
- **8 Types with 31 RQs:**

| Type | Focus | RQs | Key Question |
|------|-------|-----|--------------|
| 6.1 | General Confidence | 5 | Does confidence decline like accuracy? |
| 6.2 | Calibration | 5 | Does confidence track accuracy over time? |
| 6.3 | Domain Confidence | 4 | What/Where/When confidence patterns? |
| 6.4 | Paradigm Confidence | 4 | Free/Cued/Recognition confidence? |
| 6.5 | Schema Confidence | 3 | Does schema affect false certainty? |
| 6.6 | High-Confidence Errors | 3 | When are people certain but wrong? |
| 6.7 | Predictive Validity | 3 | Can confidence predict forgetting? |
| 6.8 | Source-Destination | 4 | Does the strong factor replicate? |

**4 Critical Hypotheses:**
1. **H1:** ICC_slope > 0.10 for confidence (proves dichotomous data limited Ch5)
2. **H2:** All Ch5 nulls replicate (convergent validity)
3. **H3:** Calibration reveals new information (over/underconfidence)
4. **H4:** Source-destination replicates (opposite correlations r=+0.99 vs r=-0.90)

#### 3. Created Chapter 6 rq_info.tsv (results/ch6/rq_info.tsv)

Complete TSV specification for all 31 RQs with 11 columns:
- Number, Type, Subtype, Old, Audited, Title, Hypothesis, Data_Required, Analysis_Specification, Expected_Output, Success_Criteria

**Key features of specifications:**
- **Every RQ references corresponding Ch5 RQ** for comparison
- **5-category GRM specified** for all IRT analyses (NOT 2PL)
- **CRITICAL hypotheses highlighted** (6.1.4 ICC test, 6.8.3 opposite correlations)
- **DERIVED dependencies explicit** with exact file paths
- **Calibration metrics defined:** Calibration = theta_conf - theta_acc, Resolution = gamma, HCE = P(Acc=0 | Conf≥0.75)

#### 4. Removed Redundant RQs from Original Plan

**Removed (already proven in Ch5):**
- IRT-CTT convergence RQs (proven 4× in Ch5)
- Purification paradox RQs (documented, apply as method)
- Consolidation window RQs (subsumed into 6.1.2)
- Redundant validation RQs

**Added (unique to confidence):**
- Type 6.2: Calibration dynamics
- Type 6.6: High-confidence errors
- Type 6.7: Predictive validity

#### 5. Created Chapter 6 Folder Structure

Created `results/ch6/` with:
- `plan.md` (comprehensive planning document)
- `rq_info.tsv` (31 RQ specifications)

### Files Created/Modified

**New Files:**
- `results/ch6/plan.md` (~400 lines, comprehensive)
- `results/ch6/rq_info.tsv` (31 RQs × 11 columns)

**Modified Files:**
- `results/ch5/story.md` (added elevator pitches section, updated status)

### Session Metrics

**Chapter 6 Planning:**
- 31 RQs specified (vs 15 in original plan)
- 8 Types hierarchically organized
- All RQs reference Ch5 comparisons

**Tokens:**
- Session start: ~5k (after /refresh)
- Session end: ~75k (at /save)

**Status:** ✅ **Chapter 6 Planning Complete**

Chapter 6 plan created with 31 RQs across 8 hierarchical types. Complete rq_info.tsv ready for rq_builder/rq_concept agents. All specifications reference Ch5 comparisons. 4 critical hypotheses defined (ICC_slope detection, null replication, calibration dynamics, source-dest replication). Ch5 story.md updated with 36 RQ elevator pitches.

**Next Step at Time of Archiving:** Build Ch6 folder structure with rq_builder, then execute Type 6.1 RQs starting with 6.1.1 (ROOT).

---
