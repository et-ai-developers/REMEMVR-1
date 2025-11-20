# 10-Step Process with V3 Leverage

**Topic:** Expanded task execution process from 7 steps to 10 steps with explicit v3 architecture leverage
**Status:** In use - Active process for all v4.X implementation tasks

---

## 10-Step Process Design: V3 Leverage (2025-11-16 03:30)

**Archived from:** state.md Session (2025-11-16 03:30)
**Original Date:** 2025-11-16 03:30
**Reason:** Process documented and in active use, archived for reference

**Context:** During third validation pass, user requested enhancement to task execution process to explicitly leverage existing v3 architecture rather than rebuilding from scratch.

### User Requirement

**Quote:** "Add three steps between 1&2 where context-finder searches for how this was done in v3, reads those files, then ultrathink about execution"

**Rationale:** "Don't rebuild from scratch what already exists in working form" - Explicitly leverage v3 validation tools, templates, patterns

### Original 7-Step Process

1. context-finder: Search analysis_pipeline_solution.md for task info
2. AskUserQuestion: Iterate until clarified
3. context-finder: Verify no conflicts with spec
4. perform: Execute task
5. verify: Confirm correct
6. update_toc: Mark spec TOC
7. update_todo: Mark complete

### Enhanced 10-Step Process

1. context-finder: Search analysis_pipeline_solution.md for task info
2. **context-finder: Search archives/ + docs/ for v3 how-was-this-done** (NEW)
3. **context-finder: Read v3 files for implementation details** (NEW)
4. **ultrathink: Best approach based on steps 1-3? What to clarify?** (NEW)
5. AskUserQuestion: Iterate until clarified
6. context-finder: Verify no conflicts with spec
7. perform: Execute task
8. verify: Confirm correct
9. update_toc: Mark spec TOC
10. update_todo: Mark complete

### Philosophy

**Core Principle:** "Don't rebuild from scratch what already exists in working form"

**Benefits:**
- Leverages existing v3 validation tools (IRT, LMM, CTT, plotting validation)
- Preserves v3 learnings and patterns that worked
- Massive efficiency gain (migrate vs build)
- Ensures continuity of working solutions

**Application:**
- Explicitly search for v3 implementations before building
- Read v3 code to understand patterns
- Ultrathink about best approach given v3 context
- Migrate/adapt what works, enhance what needs improvement, build only gaps

### Impact on Phase 4: Validation Tools

**Before (7-step):** Build validation tools from scratch
**After (10-step):** Migrate validation tools from v3

**Reframed Tasks:**
- V1: Audit v3 validation (what exists, what's missing, what works, what needs enhancement)
- V2a-V2d: Migrate IRT/LMM/CTT/plotting validation by category (not build from zero)
- V3: Update tool_inventory.md with migrated tools
- V4: Test all validation (100% coverage required)

### Usage in Practice

**Session 12:15 Example (F0a-F0b-F3):**
- Step 2: Searched archives/docs for v3 naming conventions
- Step 3: Read v3 rq_file_structure_ground_truth.md and config/models.yaml
- Step 4: Analyzed findings, prepared questions based on spec + v3 context
- Result: F0a-F0b design decisions informed by v3 patterns, F3 created with better understanding

### Documentation

**Location:** docs/v4/todo.yaml lines 10-21 (header)
**Status:** Active process for all remaining tasks (T1-T11, V1-V4, A01-A13, etc.)

---
