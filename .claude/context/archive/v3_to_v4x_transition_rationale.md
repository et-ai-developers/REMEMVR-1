# V3.0 to V4.X Transition Rationale

## Why We're Building V4.X Architecture (2025-11-15 18:45)

**Context:** After v3.0 agent architecture failed to complete a single RQ execution, user proposed complete v4.X redesign. This archive documents the reasoning and evidence for the transition.

### V3.0 Architecture (What We Had)

**7 Monolithic Agents:**
1. rq_specification
2. data_prep
3. analysis_executor
4. results_inspector
5. scholar
6. statistics_expert
7. debug

**Characteristics:**
- Large context windows (full documentation + tools + examples)
- Attempted to handle multiple tasks per agent
- Success in specification phase (50 RQs at 9.37/10 average)
- Complete failure in execution phase (couldn't finish single RQ)

### Root Cause: Context Bloat

**User's Critical Insight:**
"Agents don't follow documentation because context windows are BLOATED"

**Evidence:**
- rq-spec agent hallucinated "tests 1&2 same day" (never in documentation)
- Agent couldn't parse bloated context to find actual requirements
- Invention of details instead of following specification
- API mismatches despite comprehensive tools_inventory.md

**Mechanism:**
Context bloat → Agent confusion → Hallucinations → Failures

### V4.X Architecture (What We're Building)

**13 Atomic Agents:**

**Setup Agents:**
1. rq_builder - Initialize folder structure
2. rq_concept - Create research concept document

**Validation Agents:**
3. rq_scholar - Literature validation
4. rq_stats - Statistical methodology validation

**Planning Agents:**
5. rq_planner - Create analysis plan
6. g_conflict - Document comparison (general-purpose)

**Execution Agents:**
7. rq_tools - Specify required tools
8. rq_analysis - Create analysis specification
9. g_code - Generate validated code (general-purpose)
10. g_debug - Sandbox debugging (general-purpose)

**Results Agents:**
11. rq_inspect - Validate analysis outputs
12. rq_plots - Create visualization plan
13. rq_results - Write results document

**Characteristics:**
- Atomic task-sniper philosophy
- Lean, focused context windows
- Single responsibility per agent
- Pseudo-stateful via status.yaml context_dumps
- Multi-layer validation gates

### Design Philosophy Shift

**V3.0:** "Give agents comprehensive context so they can handle anything"
- Result: Agents overwhelmed, hallucinate, fail

**V4.X:** "Give agents minimum context for single atomic task"
- Expected: Agents focused, follow spec, succeed

### Key Innovations in V4.X

1. **Atomic Agents:**
   - Each agent does ONE thing
   - Can't get confused by unrelated information
   - Easier to debug (smaller surface area)

2. **Pseudo-Statefulness:**
   - status.yaml context_dumps (terse summaries)
   - Agents get continuity without context bloat
   - Read prior context, write new summary

3. **Validation Gates:**
   - g_code: 4-layer validation before execution
   - Import → Signature → Input file → Column check
   - QUIT on ANY failure (no guessing)

4. **General-Purpose Tools:**
   - g_conflict (document comparison)
   - g_code (validated code generation)
   - g_debug (sandbox debugging)
   - Reusable across entire project

5. **File-Based Communication:**
   - Pass paths, not content
   - Prevents context bloat from data transfer
   - Flat architecture (master orchestrates)

### Evidence Supporting V4.X

**V3.0 Failures:**
- Unicode errors (platform assumptions)
- API mismatches (context too large to parse)
- Mock data generation (scope confusion)
- Cascading errors (6+ sequential failures from single root)
- Hallucinations (invented "tests 1&2 same day")

**V4.X Solutions:**
- agent_best_practices.md (platform rules, encoding)
- g_code validation gates (API verification before execution)
- Clear scope boundaries (RAW vs DERIVED data)
- Atomic steps (failures isolated, don't cascade)
- Lean context (agents can actually read documentation)

### Migration Strategy

**Phase 1: Foundation**
- Create docs/v4/ folder structure
- Build agent_best_practices.md
- Build names.md (TDD approach, starts empty)
- Build automation.md
- Build orchestrator.md

**Phase 2: Templates**
- Build 11 template specification files
- Move thesis files to docs/v4/thesis/

**Phase 3: Validation Tools**
- Design validation architecture
- Build validation tools (paired with analysis tools)
- Document in tool_inventory.md
- Test validation tools

**Phase 4-10: Agents**
- Build all 13 agents in workflow order
- Test each agent individually
- Integration testing on RQ 5.1

**Phase 11: Legacy**
- Archive v3 agents to _legacy/v3/agents/
- Preserve v3 lessons learned

**Phase 12: Testing**
- Manual Phase 1 orchestration on RQ 5.1
- 4 sub-phases (concept through results)
- Expected failures (TDD approach)
- Iterate on agents based on testing

**Phase 13: Finalization**
- Documentation updates
- README updates
- Mark v4.X complete

### Why This Will Work

1. **Root Cause Addressed:**
   - Context bloat eliminated via atomic agents
   - No more hallucinations from information overload

2. **Validation-First:**
   - Multi-layer checks prevent execution errors
   - Circuit breakers prevent guessing
   - Fail-fast philosophy

3. **TDD Throughout:**
   - names.md starts empty (will fail, we add names)
   - Validation tools test-first
   - RQ 5.1 expected to fail initially
   - Conventions emerge from actual needs

4. **Lessons Incorporated:**
   - Platform compatibility (agent_best_practices.md)
   - API verification (g_code validation)
   - Data source boundaries (RAW vs DERIVED)
   - Error isolation (atomic steps)

5. **Specification Quality:**
   - 1,700 lines fully specified
   - 40 ultrathink issues resolved
   - 10 post-validation issues resolved
   - VALIDATED status (ready to implement)

### Historical Lessons Preserved

**V3.0 Problems Documented:**
- 24 problems across 5 categories
- 5 meta-patterns identified
- Complete reference in docs/user/analysis_pipeline_problems.md

**V3.0 Context Archived:**
- agent_standard_procedure_v3
- agent_safety_critical_fixes
- rq_automation_testing
- analysis_pipeline_problems_comprehensive_list
- And 30+ more topics in archive_index.md

**Why Archive V3.0:**
- Historical record (what we tried)
- Why it failed (context bloat)
- What we learned (lessons inform v4.X)
- Not deleted (lessons still valuable)

### Commitment to V4.X

This is NOT incremental improvement. This is architectural redesign based on evidence:
- V3.0 execution phase: 0 RQs completed
- Root cause identified: Context bloat
- Solution designed: Atomic agents
- Specification validated: 1,700 lines, 50 issues resolved
- Implementation planned: 52 tasks, 13 phases

**Archived from:** state.md Session (2025-11-15 18:45)
**Original Date:** 2025-11-15 18:45
**Reason:** Transition rationale preserved in specification Section 7.4 and throughout documentation

---
