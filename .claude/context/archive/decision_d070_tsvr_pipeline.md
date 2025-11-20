# Decision D070: IRT→LMM Pipeline with TSVR - Historical Archive

**Topic:** Critical documentation gap fix - Use TSVR (actual hours since encoding), not nominal days (0,1,3,6) as LMM time variable
**Time Period:** 2025-11-14 evening
**Status:** Complete (validated with rq-spec agent testing)

---

## Decision D070: IRT→LMM Pipeline with TSVR (2025-11-14 Evening)

**User Request:** "I see the plan.md says use days 0, 1, 3, 6 for time, not use the TSVR data for the actual number of hours since encoding. When doing an IRT, we have 100 participants that completed 4 tests, but we run the IRT pretending we have 400 people doing 1 test, then run those abilities against time in the LMM using the {UID}-RVR-T1-STA-X-TSVR data."

**Critical Issue Identified:**
- rq-specification agent generated plan.md with "Days 0, 1, 3, 6" as time variable
- **WRONG:** Should use TSVR (Time Since VR) = actual hours since encoding
- T1/T2/T3/T4 are TEST LABELS, not time measurements
- Participants completed tests within windows (e.g., T2 at 20-32 hours, not exactly 24)

**Archived from:** state.md
**Original Date:** 2025-11-14 evening
**Reason:** Critical documentation gap fixed, decision documented, tested with rq-spec agent

---

### Root Cause Analysis

**Documents Causing the Mistake:**

1. **lmm_methodology.md (Line 44) - PRIMARY CULPRIT**
   - Said: "Days: Raw days since VR encoding (0, 1, 3, 6)"
   - WRONG - Should specify TSVR, not nominal days

2. **irt_methodology.md (Lines 123-142) - INCOMPLETE**
   - Explained composite_ID stacking (100 participants × 4 tests = 400 "people")
   - BUT didn't explain what happens AFTER IRT
   - MISSING: How theta scores connect to LMM with TSVR

3. **concept.md (Lines 27, 139) - PROPAGATED ERROR**
   - Followed wrong guidance from lmm_methodology.md
   - Said "Days since VR encoding (0, 1, 3, 6)"

**Document with CORRECT Info (But Buried):**
- **data_structure.md (Lines 80, 112, 212, 892) - CORRECT BUT ISOLATED**
  - Line 80: "Use **TSVR** for ACTUAL delay period"
  - Line 112: "Use `{UID}-RVR-T{N}-STA-X-TSVR` for hours since VR"
  - Problem: Info isolated in tag reference section, not connected to IRT→LMM pipeline

---

### Decision D070: Use TSVR (Hours Since Encoding), Not Nominal Days

**Problem:**
- Nominal days (0, 1, 3, 6) are INSTRUCTED test schedules, not actual delays
- Participants completed tests within windows (scheduling conflicts, late submissions)
- Using nominal days introduces measurement error

**Solution:**
- Use TSVR (Time Since VR) tags for ACTUAL delay period
- Extract from master.xlsx: `{UID}-RVR-{Test}-STA-X-TSVR`
- Merge with theta scores after parsing composite_ID
- Convert to days: TSVR_days = TSVR_hours / 24

**Complete IRT→LMM Pipeline (5 steps):**
1. **IRT Calibration:** 100 participants × 4 tests = 400 composite_IDs (A010_T1, A010_T2, A010_T3, A010_T4)
2. **Extract Theta Scores:** One theta per composite_ID per domain
3. **Extract TSVR Data:** Load from master.xlsx tags `{UID}-RVR-{Test}-STA-X-TSVR`
4. **Create LMM Input:** Parse composite_ID → merge with TSVR on [UID, Test] → reshape to long format
5. **Fit LMM:** Use TSVR_days as time variable (NOT nominal days 0, 1, 3, 6)

**Why TSVR is Mandatory:**
- T1 (nominal "Day 0"): TSVR range 0.3 to 2.5 hours (variance exists)
- T2 (nominal "Day 1"): TSVR range 20 to 32 hours (target 24 hours)
- T3 (nominal "Day 3"): TSVR range 68 to 80 hours (target 72 hours)
- T4 (nominal "Day 6"): TSVR range 140 to 156 hours (target 144 hours)
- Using nominal days = measurement error in time variable → biased slope estimates, reduced power

---

### Documentation Added/Fixed

**File 1: project_specific_stats_insights.md (+327 lines)**
- Complete Decision D070 section (lines 656-979)
- Problem statement (nominal days incorrect)
- Solution (TSVR extraction and merge)
- Complete IRT→LMM pipeline (5 steps with Python code examples)
- Why TSVR not nominal days (statistical validity, example variance)
- Implementation requirements for info.md and config.yaml (3 subsections)
- Validation checklist (8 items)
- Why project-specific (scheduling variance, composite_ID stacking, master.xlsx design)
- Common misunderstandings (4 FAQs)
- Updated Updates Log (line 1006)

**File 2: irt_methodology.md (+25 lines)**
- Added "Downstream Usage: Theta Scores for LMM Analysis" section (lines 189-212)
- Pipeline flow: IRT → Output → Reshaping → LMM
- Time variable warning: WRONG (nominal days) vs CORRECT (TSVR)
- Why TSVR is mandatory (precise delay for each composite_ID)
- Data source (master.xlsx tags)
- Cross-reference to Decision D070

**File 3: lmm_methodology.md (+57 lines)**
- Fixed "Time Coding" section (lines 42-67) - Replaced "Days 0,1,3,6" with TSVR
- Added "REMEMVR-SPECIFIC: IRT→LMM DATA FLOW" section (lines 25-64)
- Upstream: IRT Phase (composite_ID stacking)
- Data Reshaping for LMM (3 steps: parse, merge, reshape)
- LMM Input Structure (Python DataFrame example with 1200 rows)
- Grouping variable clarification (UID, not composite_ID)
- Cross-reference to Decision D070

**File 4: concept.md (RQ 5.1) (6 edits)**
- Fixed time variable definition (line 27): Added TSVR with data source, rationale, expected range
- Added Step 4: Extract TSVR data (line 58)
- Enhanced Step 5: Data reshaping with TSVR merge (line 59)
- Fixed Step 6: LMM with TSVR_days (lines 60-64)
- Renumbered Steps 7-9 (was 6-8 before TSVR extraction added)
- Fixed Question 4 (line 144): Replaced nominal days with TSVR + Decision D070

**File 5: data_structure.md (+3 lines)**
- Enhanced line 80 TSVR warning with IRT→LMM pipeline cross-reference (line 82)
- Added extraction instructions, conversion formula (TSVR_hours / 24), Decision D070 link

**File 6: docs_index.md (4 entries updated)**
- project_specific_stats_insights.md: Added Decision D070 to Purpose and Key Topics
- irt_methodology.md: Added "downstream usage for LMM" to Purpose and Key Topics
- lmm_methodology.md: Added "IRT→LMM data flow" to Purpose and Key Topics
- data_structure.md: Added Decision D070 cross-reference to Status and Key Topics

**Total Documentation Updated:** 6 files, +412 lines net

---

### Testing Decision D070

**Method:**
- Deleted plan.md again to force agent re-generation
- Invoked rq-specification agent Planning Mode (third invocation)

**Agent Detection:**
- Agent successfully detected Decision D070 from all updated documentation:
  - project_specific_stats_insights.md (lines 656-839)
  - irt_methodology.md (downstream usage section)
  - lmm_methodology.md (IRT→LMM data flow)
  - concept.md (TSVR in Steps 4-5, time variable definition)

**Agent Incorporation in plan.md:**
- Circuit Breaker Check 3D added (D070 compliance verification)
- Analysis Pipeline Step 4 added (Extract TSVR data from master.xlsx)
- Analysis Pipeline Step 5 enhanced (Data reshaping with TSVR merge)
- Analysis Pipeline Step 6 reformulated (All 5 LMM models use TSVR_days)
- Key Variables section updated (Time variable = TSVR_days continuous ~0-6.5 days)
- Decision 9 added to Key Specification Decisions (TSVR Time Variable - Decision D070)
- Tools Required table enhanced (Step 4 TSVR extraction, Step 5 TSVR merge)
- Proposed config.yaml enhanced (tsvr_extraction section + enhanced data_reshaping)
- Proposed info.md structure enhanced (TSVR Data subsection)
- Explicit "Decision D070 Incorporation Evidence" section (11 pieces of evidence)

**Test Result:** PASSED

---

### Impact

**Scope:** ~40 RQs (all IRT→LMM analyses across chapters 5, 6, 7)

**Critical Importance:**
- **Prevents measurement error** that would have affected all LMM results
- Using nominal days would have introduced systematic bias in time variable
- TSVR provides precise delay for each participant × test combination
- Enables accurate slope estimation for memory trajectories

**Implementation Requirements:**
- Mandatory for ALL RQs using IRT→LMM pipeline
- rq-specification agent will read Decision D070 and include TSVR extraction in info.md
- Data-prep agent will extract TSVR data from master.xlsx
- Analysis-executor agent will merge TSVR with theta scores before LMM fitting

**Statistical Validity:**
- Accurate time variable reduces measurement error
- Increases power to detect trajectory effects
- Enables correct interpretation of Time × Domain interactions
- Preserves precision in participant-level random effects

---

### Why This Was Critical

**If this gap had not been fixed:**
- All 40 IRT→LMM analyses would have used nominal days (0, 1, 3, 6)
- Time variable measurement error would have:
  - Attenuated slope estimates (underestimate trajectory effects)
  - Reduced power to detect significant changes over time
  - Biased interaction effects (Time × Domain)
  - Invalidated clinical interpretations of memory trajectories
- Results would have been statistically flawed
- PhD thesis validity compromised

**Now:**
- All agents know to use TSVR (explicit documentation in 6 files)
- Pipeline fully documented (5-step IRT→LMM workflow)
- Validation checklist ensures compliance (8 items)
- Common misunderstandings section prevents future errors

---
