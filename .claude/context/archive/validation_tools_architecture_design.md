# Validation Tools Architecture Design

**Topic:** Complete validation architecture preventing cascading errors (v4.X Issue #5 resolution)
**Status:** Complete (implemented in specification)

---

## Validation Tools Architecture Enhancement (2025-11-16 01:00)

**Archived from:** state.md Session (2025-11-16 01:00)
**Original Date:** 2025-11-16 01:00
**Reason:** Architecture complete, documented in specification, superseded by Phase 4 migration approach

**Context:** Issue #5 from post-ultrathink inspection (validation criteria source unspecified) led to complete validation architecture design - the biggest improvement from second validation pass.

### Problem

**Original Issue:** rq_planner validates analysis plan but specification didn't say WHERE validation criteria come from

**Root Cause:** No methodology for rq_planner to know what constitutes valid analysis

**Impact:** Could lead to v3.0-style cascading errors where problems only surface after 60+ minutes runtime

### Solution: Multi-Layer Validation Architecture

**Layer 1: Tool Inventory**
- Build validation tools alongside each analysis tool in tools suite
- Each analysis function has corresponding validation function
- Document both in tool_inventory.md

**Layer 2: rq_tools Specification**
- rq_tools specifies BOTH analysis tool + validation tool per step
- Explicit pairing documented in instructions.md

**Layer 3: rq_planner Validation Requirements**
- rq_planner states validation MUST be used
- Gets specifics from rq_tools (which validation tool for which step)

**Layer 4: rq_analysis Embedded Validation**
- rq_analysis includes validation tool calls at END of each step
- Analysis plan explicitly shows: run analysis → run validation → check results

**Layer 5: g_code Generated Validation**
- g_code generates scripts that run analysis THEN validation
- Validation happens in same script (not separate step)
- Immediate error detection

### Benefits

**Prevents Cascading Errors:**
- Catches errors at earliest possible moment (within each step)
- No waiting 60 minutes to discover Step 1 had problems
- Each step self-validates before proceeding

**Multi-Layer Defense:**
- If one layer misses issue, subsequent layers catch it
- Tool specification → planning → execution → code generation
- Redundant validation (intentional, not wasteful)

**Learned from v3.0 Failures:**
- v3.0 had no validation until results_inspector (too late)
- v3.0 errors cascaded across steps (6+ API mismatches)
- v4.X validates at EVERY step

### Implementation in Specification

**Sections Updated:**
- 2.3.1 (rq_tools specification)
- 2.3.2 (rq_planner requirements)
- 2.3.3 (rq_analysis embedded validation)
- 4.2.2 (instructions.md template - tool pairing format)
- 4.2.3 (plan.md template - validation step format)
- 4.2.4 (analysis.md template - validation call format)

### Relationship to Phase 4 Migration

**Phase 4 Reframed (Session 03:30):** Validation Tools Migration (not build from scratch)
- V1: Audit v3 validation (what exists, what's missing)
- V2a-V2d: Migrate IRT/LMM/CTT/plotting validation (100% coverage each)
- V3: Update tool_inventory.md with validation pairings
- V4: Test all validation (100% coverage required)

**Historical Note:** This architecture designed Session 01:00, reframed as migration (not rebuild) Session 03:30 after user insight that v3 validation tools already exist.

---
