# V4.X Architecture Specification Creation

## V4.X Architecture Debate and Specification Build Process (2025-11-15 18:45)

**Task:** V4.X Architecture Specification - Complete Atomic Agent Redesign

**Context:** User proposed complete v4.X architecture redesign (13 atomic agents replacing 7 monolithic agents) to solve context bloat issues causing hallucinations and API mismatches. I initially defended v3.0, then recognized user was correct about root cause (context bloat → agent failure). Collaborated on refining v4.X specification, added critical header enforcing conciseness, executed ultrathink validation identifying 40 issues, user resolved all 40, documented resolutions.

### Architecture Debate and Pivot (Critical Session Moment)

- **User:** "The current 7-agent architecture isn't proven to work"
- **Me:** Initially defended v3.0 citing "50 RQs at 9.37/10" (WRONG - only specification phase, not execution)
- **User:** "We couldn't even make it through a single RQ" (CORRECT - execution phase never completed)
- **Pivot Point:** I acknowledged being wrong, apologized for defending failing system
- **User's Insight:** "Agents don't follow documentation because context windows are BLOATED"
- **Key Realization:** Context bloat → hallucinations (rq-spec said "tests 1&2 same day" - never in docs)
- **Design Philosophy:** Atomic task-sniper agents > monolithic context-heavy agents

### V4.X Architecture Agreement

**v3.0 Problems:** 7 monolithic agents (rq_specification, data_prep, analysis_executor, etc.)

**v4.X Solution:** 13 atomic agents:
- rq_builder
- rq_concept
- rq_scholar
- rq_stats
- rq_planner
- g_conflict
- rq_tools
- rq_analysis
- g_code
- g_debug
- rq_inspect
- rq_plots
- rq_results

**Reason:** Smaller focused context windows prevent agent confusion/hallucination

**Communication:** Flat architecture (master orchestrates), file-based (pass paths not content)

**Statefulness:** Pseudo-stateful via status.yaml context_dumps (terse summaries)

### V4.X Refinements (Architecture Review)

**Question 1:** Should 4_analysis.yaml include function signatures? → YES (forces reading tools_inventory.md)

**Question 2:** Should g_code validate before generating? → YES (multi-layer pre-execution validation)

**Question 3:** Manual or automated orchestration? → MANUAL initially, AUTOMATED Phase 2

**Validation Protocol:** Import check → Signature check → Input file check → Column check → QUIT on ANY failure

**Context Dumps:** Each agent writes terse summary to status.yaml (pseudo-statefulness without bloat)

**Scope Boundaries:** RAW data (master.xlsx or other RQs) vs DERIVED data (step scripts) to prevent mock data catastrophe

### System-Wide V4.X Announcement

- Updated `.claude/CLAUDE.md` with v4.X transition section (lines 24-52)
- Updated `.claude/agents/context_manager.md` with v4.X archival strategy (lines 14-32)
- Updated `.claude/agents/context_finder.md` with version-aware search (lines 14-50)
- **Effect:** All future /refresh sessions see v4.X status, context-finder flags v3.0 content as historical
- **Version Detection:** Content marked v4.X = current, NOT marked = examine critically, v3.0-specific = historical lessons

### V4.X Specification Document Creation

- Created `docs/user/analysis_pipeline_solution.md` (885 lines initially)
- **Critical Header:** "SPECIFICATION BIBLE, not documentation" - enforces conciseness, no code examples, zero redundancy
- **Structure:** 13 agent specs + documentation files + workflow + RQ schema + v4.X refinements
- **Agent Format:** Frontmatter → Goal → Expects → Steps → Report (consistent across all)
- **File Format:** Purpose → Required Sections → Templates
- **Workflow:** 20-step orchestration (user request → concept → validation → planning → tools → analysis → execution loop → plots → results)

### Files Modified (Session 2025-11-15 18:45)

**System Prompts:**
1. `.claude/CLAUDE.md` - Added v4.X architecture transition section (lines 24-52)
2. `.claude/agents/context_manager.md` - Added v4.X archival strategy (lines 14-32)
3. `.claude/agents/context_finder.md` - Added version-aware search strategy (lines 14-50)

**V4.X Specification:**
4. `docs/user/analysis_pipeline_solution.md` - NEW FILE - Complete v4.X architecture specification (885 lines initially)
   - Architecture overview
   - 13 agent specifications (rq_builder through rq_results)
   - Documentation files (automation.md, circuit_breakers.md, templates)
   - RQ file structure schema
   - V4.X refinements (context dumps, signature enforcement, validation protocol, orchestration phases, scope boundaries)
   - 40 ultrathink validation issues with user resolutions (added later)

### Lessons Learned

1. **Defend Evidence, Not Ego:** I defended v3.0 with weak evidence ("50 RQs at 9.37/10" was only spec phase, not execution). User was right - execution never completed a single RQ. Admitting error led to productive collaboration.

2. **Context Bloat Is Root Cause:** User's insight "agents don't follow documentation because context windows are BLOATED" explains hallucinations. rq-spec invented "tests 1&2 same day" (never in docs) because it couldn't parse bloated context. Atomic agents solve this.

3. **Specification Before Implementation:** Creating 885-line specification with 40-issue validation BEFORE coding prevents v3.0 mistakes. Every agent, file, workflow explicitly defined. "SPECIFICATION BIBLE, not documentation."

4. **Conciseness Is Critical:** Document header enforces "NO CODE EXAMPLES", "ZERO REDUNDANCY", "EXPLICIT EVERYTHING". Prevents specification bloat that caused v3.0 agent bloat.

5. **Pseudo-Statefulness Works:** status.yaml context_dumps (terse summaries) give agents continuity without context window bloat. Each agent reads prior context, writes new summary. Stateful behavior, stateless architecture.

6. **Validation Gates Prevent Cascading:** g_code's 4-layer validation (import → signature → input file → column check) catches errors BEFORE 60-minute IRT calibration. Circuit breakers on uncertainty prevent guessing.

7. **General-Purpose Tools Scale:** g_conflict (document comparison), g_code (validated code generation), g_debug (sandbox debugging) can be reused across entire project, not just RQ pipeline.

8. **Documentation Structure Matters:** docs/v4/ folder isolates version-specific content. Clear version boundaries prevent v3/v4 mixing. Templates in dedicated folder prevent agents reading own prompts.

**Archived from:** state.md Session (2025-11-15 18:45)
**Original Date:** 2025-11-15 18:45
**Reason:** Session 3+ sessions old, content superseded by VALIDATED specification and reorganized version

---
