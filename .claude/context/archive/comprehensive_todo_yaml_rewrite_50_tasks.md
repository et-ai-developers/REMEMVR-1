# Comprehensive Todo.yaml Rewrite 50 Tasks

**Topic:** Complete todo.yaml rewrite establishing 50-task implementation roadmap across 14 phases with 10-step process
**Status:** Complete - Roadmap established and in use

---

## Todo.yaml Complete Rewrite: 50 Tasks, 14 Phases (2025-11-16 03:30)

**Archived from:** state.md Session (2025-11-16 03:30)
**Original Date:** 2025-11-16 03:30
**Reason:** Roadmap established, now following tasks sequentially

**Context:** During third validation pass, discovered task count error and multiple enhancement opportunities. User approved complete rewrite expanding from 48 tasks (claimed 52) to actual 50 tasks with Phase 0 addition.

### Rewrite Scope

**Before:** 634 lines, 48 tasks (claimed 52), 13 phases, 7-step process
**After:** 716 lines, 50 tasks, 14 phases, 10-step process

### Major Changes

**1. Process Enhancement:**
- Added 10-step process with v3 leverage (steps 2-3-4 NEW)
- Documented process in header (lines 10-21)

**2. Phase 0 Addition (Issue #12):**
- User: "Add steps to yaml where we come up with the best system for this file"
- Created F0a-F0b: names.md header design
- Lines 32-63 in todo.yaml

**3. Phase 4 Reframing (Issue #14):**
- User: "Lots of v3 tools exist, this should be about MIGRATING not building from scratch"
- Renamed: "Validation Tools Build" → "Validation Tools Migration"
- V1: Audit v3 validation (what exists, what's missing)
- V2a-V2d: Migrate by category (IRT, LMM, CTT, plotting)
- V3: Update tool_inventory.md
- V4: Test all validation
- Lines 259-333

**4. V2 Granularization (Issue #15):**
- Split monolithic V2 into category-specific tasks
- V2a: IRT validation migration
- V2b: LMM validation migration
- V2c: CTT validation migration
- V2d: Plotting validation migration
- Each with 100% coverage requirement

**5. Coverage Requirement Strengthening (Issue #22):**
- User: "100% coverage. Nothing short of perfect is acceptable"
- Changed: ≥80% → EXACTLY 100%
- Lines 288-289, 332-333

**6. Verification Enhancements:**
- Template tasks (lines 138-222): Comprehensive spec-matching checklists
- Agent tasks (lines 352-548): Step sequence verification
- Validation tasks (lines 275-333): 100% coverage checks

**7. Token Estimates Removed (Issue #9):**
- User: "These are meaningless. Remove them"
- Removed all token estimates
- Lines 697-698: Note explaining removal

### 14 Phases Structure

**Phase 0:** Foundation Design (F0a-F0b) - names.md header system
**Phase 1:** Foundation Build (F1-F5) - Folders, agent_best_practices, names, automation, orchestrator
**Phase 2:** Templates (T1-T11) - All 11 template specifications
**Phase 3:** Thesis Files (H1-H3) - Move ANALYSES_CHX.md
**Phase 4:** Validation Tools Migration (V1-V4) - Audit, migrate, document, test
**Phase 5-10:** Agents (A01-A13) - All 13 agents in workflow order
**Phase 11:** Legacy (L1-L2) - Archive v3 agents
**Phase 12:** Testing (TEST1-TEST6) - RQ 5.1 in 4 sub-phases
**Phase 13:** Finalization (FIN1-FIN4) - docs_index, README, completion

### Key Design Decisions

**Dependencies:**
- Validation Tools (Phase 4) BEFORE Planning Agents (Phase 5-7)
  - Reason: rq_tools reads tool_inventory.md for validation tools
- Templates (Phase 2) BEFORE Agents (Phase 5-10)
  - Reason: Agents read templates for format requirements
- General-Purpose Agents (A10-A12) BEFORE they're used
  - Reason: g_conflict used at workflow steps 10 & 13

**TDD Throughout:**
- names.md starts empty (RQ 5.1 expected to fail, add names manually)
- Validation tools test-first (write failing tests, make pass)
- All expected to have initial failures

**V3 Leverage:**
- Steps 2-3 NEW: Search v3, read v3 files
- Migration not rebuild philosophy
- Lines 27-29, 261-262, 711

### Critical Tasks Highlighted

**Foundation:**
- F2: agent_best_practices.md (ALL agents read this first)
- F4: automation.md (17-step master orchestration)

**Validation:**
- V1-V4: Complete validation migration (prevents cascading errors)

**Agents:**
- A07: rq_analysis (embeds validation calls)
- A10: g_code (generates scripts with validation)

**Testing:**
- TEST3: Execution loop (most critical validation)

### Current Progress

**Completed (as of Session 12:15):**
- Phase 0: F0a-F0b ✅ (design decisions documented)
- Phase 1: F1-F3 ✅ (folders, agent_best_practices, names)
- Phase 1: F4-F5 pending (automation, orchestrator)

**Next:**
- F4: automation.md (17-step workflow)
- F5: orchestrator.md
- Phase 2: T1-T11 (templates)

### Files Modified

**Created:** docs/v4/todo.yaml (716 lines, 50 tasks, 14 phases)

**Documentation:** Complete implementation roadmap across multiple /save-/clear-/refresh cycles

---
