# V4.X BUILD HISTORY - COMPLETED PHASES

**Last Updated:** 2025-11-19
**Purpose:** Historical record of v4.X agent building phases (Phases 0-16)
**Status:** All 13 atomic agents built successfully
**Next:** Begin agent testing (Phases 17-29)

---

## Summary

Successfully completed foundation and agent building phases for v4.X architecture:

- **Phase 0:** Names.md design (completed 2025-11-15)
- **Phase 1:** Foundation infrastructure (5 tasks)
- **Phase 2:** Template creation (11 templates, 9,551 lines, completed 2025-11-16)
- **Phase 3:** Thesis files migration (3 files, 50 RQs)
- **Phases 4-16:** All 13 atomic agents built using rigorous 11-step process

**Total Implementation Time:** 5 days (2025-11-15 to 2025-11-19)
**Total Lines of Agent Code:** ~13,000 lines
**Agent Building Process:** 11-step validation with ultrathink analysis

---

## Phase 0: Names.md Design

**Status:** COMPLETE
**Completed:** 2025-11-16
**Tasks:** 2/2

### F0a: Design names.md header content
- Designed header structure for TDD approach
- Empty file with initialization strategy
- Completed: 2025-11-16

### F0b: Design naming convention format
- Established pattern format for item codes
- Regex-compatible naming structure
- Completed: 2025-11-16

---

## Phase 1: Foundation & Infrastructure

**Status:** COMPLETE
**Completed:** 2025-11-16
**Tasks:** 5/5

Built core v4.X infrastructure with agent best practices and workflow documentation.

### F1: Create docs/v4/ folder structure
- Created templates/, thesis/ subdirectories
- Established v4.X documentation hierarchy
- Completed: 2025-11-16

### F2: Build agent_best_practices.md
- 5 circuit breaker types (EXPECTATIONS, STEP, TOOL, CLARITY, SCOPE)
- Platform-specific rules (Windows compatibility, UTF-8 encoding)
- Git safety protocol
- Core file editing prohibition
- Completed: 2025-11-16

### F3: Build names.md (empty, TDD)
- Empty file for TDD initialization
- To be populated during testing when rq_planner needs patterns
- Completed: 2025-11-16

### F4: Build automation.md
- 17-step workflow documentation
- Phase 1 (Manual) and Phase 2 (Automated) specifications
- Agent invocation sequences
- Completed: 2025-11-16

### F5: Build orchestrator.md
- Main claude role as master orchestrator
- Agent coordination guidelines
- Error recovery workflow
- Completed: 2025-11-16

---

## Phase 2: Templates

**Status:** COMPLETE
**Completed:** 2025-11-17
**Tasks:** 11/11
**Total Lines:** 9,862

Created all template specifications for v4.X workflow documents.

### T1: build_folder.md template (305 lines)
- Folder structure specification
- 6 subdirectories: docs/, data/, code/, logs/, plots/, results/
- Completed: 2025-11-16

### T2: build_status.md template (423 lines)
- status.yaml structure with 10 agent sections
- Context dump mechanism (max 5 lines per agent)
- Pseudo-statefulness design
- Completed: 2025-11-16

### T3: concept.md template (687 lines)
- 7-section structure for RQ description
- Preserves thesis detail (comprehensive ground truth)
- Scholar/Stats feedback append sections
- Completed: 2025-11-16

### T4: plan.md template (1,289 lines)
- Step-by-step analysis plan
- Per-step validation requirements
- Data extraction specifications with tag patterns
- Expected outputs and substance criteria
- Completed: 2025-11-16

### T5: tools.md template (712 lines)
- Tool catalog approach (document each tool once)
- Analysis + validation tool pairing
- Full type hints in signatures
- Input/output specifications
- Completed: 2025-11-16

### T6: analysis.md template (1,156 lines)
- Self-contained recipe for g_code
- Complete function signatures with parameters
- Explicit validation inputs (no inference)
- Completed: 2025-11-16

### T7: scholar_report.md template (v4.1, 891 lines)
- 10-point rubric scoring
- Devil's advocate analysis (4 subsections)
- Two-pass WebSearch validation
- Category 5 meta-scoring (0.9-1.0 = 5+ concerns)
- Completed: 2025-11-16

### T8: stats_report.md template (v4.1, 944 lines)
- 10-point rubric with methodological rigor
- Devil's advocate analysis (parallel to scholar)
- Statistical appropriateness validation
- Literature citation requirements
- Completed: 2025-11-16

### T9: inspect_criteria.md template (987 lines)
- Four-layer validation (existence, structure, substance, logs)
- Plan.md cross-reference requirements
- Log file validation patterns
- Completed: 2025-11-16

### T10: plots.md template (1,059 lines)
- Option B architecture (visualization-only)
- Plot source CSV specifications
- Decision D069 dual-scale trajectory requirements
- Completed: 2025-11-17

### T11: results.md template (1,409 lines)
- 5-section publication-ready summary
- Multimodal plot inspection guidance
- 6-source synthesis approach
- Anomaly flagging framework
- Completed: 2025-11-17

---

## Phase 3: Thesis Files Migration

**Status:** COMPLETE
**Completed:** 2025-11-17
**Tasks:** 3/3
**Total RQs:** 50

Migrated thesis analysis files to v4.X location using git mv (preserves history).

### H1: ANALYSES_CH5.md
- 15 RQs (Trajectory of Forgetting)
- 79K file size
- Moved to: docs/v4/thesis/
- Completed: 2025-11-17

### H2: ANALYSES_CH6.md
- 15 RQs (Metacognition)
- 106K file size
- Moved to: docs/v4/thesis/
- Completed: 2025-11-17

### H3: ANALYSES_CH7.md
- 20 RQs (Individual Differences)
- 163K file size
- Moved to: docs/v4/thesis/
- Completed: 2025-11-17

---

## Phase 4: rq_builder Agent

**Status:** COMPLETE
**Agent:** A01 - rq_builder
**Completed:** 2025-11-18
**Specification:** Section 2.1.1
**Lines:** 543 lines

Creates RQ folder structure and initial status.yaml.

### Key Features
- Hybrid approach: Bash mkdir + Write .gitkeep
- QUIT behavior on non-empty folder (safety)
- 7 steps with circuit breakers
- Creates 6 subdirectories + status.yaml
- Initializes all 10 agent sections as pending

### User Decisions
- Hybrid Bash/Write approach approved
- QUIT on non-empty prevents accidents
- No force overwrite option

### Files Created
- `.claude/agents/rq_builder.md` (543 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (TOC: 2.1.1 ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 4 COMPLETE, A01 completed 2025-11-18)

---

## Phase 5: rq_concept Agent

**Status:** COMPLETE
**Agent:** A02 - rq_concept
**Completed:** 2025-11-18
**Specification:** Section 2.1.2
**Lines:** 625 lines

Extracts RQ concept from thesis, creates comprehensive 1_concept.md.

### Key Features
- TOC line number extraction for efficiency
- Preserves thesis detail (not over-distilled)
- Maps to 7-section concept.md template
- Omits Reviewer Rebuttals (validation agents generate concerns)
- 11 steps with context_dump integration

### Critical Insight
- concept.md is ground truth document (comprehensive, not summary)
- Downstream agents need full detail for accurate work
- User APPROVES after generation (not user writes)

### Files Created
- `.claude/agents/rq_concept.md` (625 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (TOC: 2.1.2 ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 5 COMPLETE, A02 completed 2025-11-18)

---

## Phase 6: rq_scholar Agent

**Status:** COMPLETE
**Agent:** A03 - rq_scholar
**Completed:** 2025-11-18
**Specification:** Section 2.2.1
**Lines:** 778 lines

Validates 1_concept.md scholarly accuracy via WebSearch with devil's advocate analysis.

### Key Features
- Two-pass WebSearch (validation 3-5 + challenge 3-5 = 6-10 queries)
- Devil's advocate analysis (4 subsections: commission errors, omission errors, alternatives, confounds)
- 10-point rubric with Category 5 meta-scoring (0.9-1.0 = 5+ concerns)
- Edit tool appends feedback to 1_concept.md (doesn't overwrite)
- Status.yaml context_dump integration

### Template Enhancement
- Enhanced scholar_report.md v4.0 → v4.1 (+devil's advocate section)

### Files Created
- `.claude/agents/rq_scholar.md` (778 lines)

### Files Modified
- `docs/v4/templates/scholar_report.md` (v4.1)
- `docs/user/analysis_pipeline_solution.md` (TOC: 2.2.1 ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 6 COMPLETE, A03 completed 2025-11-18)

---

## Phase 7: rq_stats Agent

**Status:** COMPLETE
**Agent:** A04 - rq_stats
**Completed:** 2025-11-18
**Specification:** Section 2.2.2
**Lines:** 692 lines

Validates 1_concept.md statistical methods appropriateness with parallel devil's advocate architecture.

### Key Features
- Identical architecture to rq_scholar (consistency)
- Two-pass WebSearch (6-10 total queries for methodology validation)
- Devil's advocate analysis (4 subsections: Commission, Omission, Alternatives, Pitfalls)
- All criticisms MUST cite methodological literature
- 10-point rubric with Category 5 devil's advocate meta-scoring

### Template Enhancement
- Enhanced stats_report.md v4.0 → v4.1 (+253 lines with devil's advocate)

### Files Created
- `.claude/agents/rq_stats.md` (692 lines)

### Files Modified
- `docs/v4/templates/stats_report.md` (v4.1)
- `docs/user/analysis_pipeline_solution.md` (TOC: 2.2.2 ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 7 COMPLETE, A04 completed 2025-11-18)

---

## Phase 8: g_conflict Agent

**Status:** COMPLETE
**Agent:** A05 - g_conflict
**Completed:** 2025-11-18
**Specification:** Section 2.6.1
**Lines:** 269 lines

General-purpose document conflict detection (within/between documents).

### Key Features
- Stateless general-purpose design (NO status.yaml)
- 4 steps: Circuit Breaker, Read all, Ultrathink conflicts, Report
- Detects ALL conflict types (generic, structured, semantic)
- Reports grouped by topic, ranked CRITICAL/MODERATE/MINOR
- Line number references for all conflicts

### Design Philosophy
- Hard-coded circuit breakers (doesn't read agent_best_practices.md)
- Read-only (no modifications)
- Works on any documents (not RQ-specific)

### Files Created
- `.claude/agents/g_conflict.md` (269 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (Section 2.6.1 updated, TOC ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 8 COMPLETE, A05 completed 2025-11-18)

---

## Phase 9: rq_planner Agent

**Status:** COMPLETE
**Agent:** A06 - rq_planner
**Completed:** 2025-11-18
**Specification:** Section 2.3.1
**Lines:** 1,165 lines

Creates 2_plan.md with step-by-step analysis plan and validation requirements.

### Key Features
- 13 steps with 5 circuit breakers
- Reads 7 required files (best_practices, status, template, concept, data_structure, tool_inventory, names)
- High-detail data extraction (exact tag patterns with wildcards)
- Per-step validation requirements (MANDATORY)
- names.md FAIL-on-missing safety
- Complexity estimates (Low/Medium/High)
- Decision integration (D039/D068/D069/D070 auto-applied)
- Cross-RQ dependency checks

### Status.yaml Integration
- 3-piece context_dump (# steps, tool requirements, expected outputs)
- Creates analysis_steps section (all pending initially)

### Files Created
- `.claude/agents/rq_planner.md` (1,165 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (TOC: 2.3.1 ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 9 COMPLETE, A06 completed 2025-11-18)

---

## Phase 10: rq_tools Agent

**Status:** COMPLETE
**Agent:** A07 - rq_tools
**Completed:** 2025-11-18
**Specification:** Section 2.3.2
**Lines:** 746 lines

Creates 3_tools.yaml with analysis + validation tool pairs, FAILS if tools missing.

### Key Features
- Tool catalog approach (document each tool ONCE)
- Full type hints in signatures (enables g_code validation)
- Validation tools nested under analysis tools
- Steps 9-10: CHECK tool_inventory.md and names.md, FAIL with list if missing
- Never improvises (TDD detection point)
- Separation of concerns (HOW to use vs WHEN to use)

### Critical Role
- WHERE tool migration is DETECTED
- Agent FAILs cleanly → User migrates with TDD → Update docs → Re-run → PASS

### Files Created
- `.claude/agents/rq_tools.md` (746 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (TOC: 2.3.2 ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 10 COMPLETE, A07 completed 2025-11-18)

---

## Phase 11: rq_analysis Agent

**Status:** COMPLETE
**Agent:** A08 - rq_analysis
**Completed:** 2025-11-18
**Specification:** Section 2.3.3
**Lines:** 1,185 lines

Creates 4_analysis.yaml with complete self-contained recipe for g_code.

### Key Features
- 12 steps (merged step 3 into 2, added QA step 8)
- CRITICAL: g_code reads ONLY 4_analysis.yaml (not 3_tools.yaml)
- 4_analysis.yaml must be COMPLETE (merges plan + tools, omits NOTHING)
- Full function signatures with type hints for analysis AND validation
- Explicit validation inputs (no inference)
- Names.md FAIL-on-missing enforcement
- Creates analysis_steps section in status.yaml (all pending)

### Context Dump Format
- '[N] steps specified with validation ([analysis_type])'
- Terse summary (max 5 lines)

### Files Created
- `.claude/agents/rq_analysis.md` (1,185 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (TOC: 2.3.3 ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 11 COMPLETE, A08 completed 2025-11-18)

---

## Phase 12: g_code Agent

**Status:** COMPLETE
**Agent:** A09 - g_code
**Completed:** 2025-11-18 (enhanced 2025-11-19)
**Specification:** Sections 2.4.1, 6.1
**Lines:** 1,150 lines

Generates Python code with 4-layer pre-generation validation preventing v3.0 API mismatches.

### Key Features
- 8 steps with 4-layer validation protocol (Step 4a-4d)
  - 4a: Import check (importlib + hasattr)
  - 4b: Signature check (inspect.signature vs tools/ source)
  - 4c: Input file check (os.path.exists)
  - 4d: Column check (pd.read_csv exact match)
- QUIT on ANY validation failure
- UTF-8 encoding + ASCII output (Windows cp1252 compatibility)
- Comprehensive error formats with actionable recommendations
- General-purpose design (no status.yaml)

### V3.0 Lessons Applied
- 6 API mismatches prevented by signature validation
- Trust but verify approach (validates 4_analysis.yaml against tools/ source)
- Conservative column matching
- Never generates without validation

### Files Created
- `.claude/agents/g_code.md` (1,150 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (TOC: 2.4.1 ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 12 COMPLETE, A09 completed 2025-11-18)

---

## Phase 13: g_debug Agent

**Status:** COMPLETE
**Agent:** A10 - g_debug
**Completed:** 2025-11-19
**Specification:** Section 2.6.2
**Lines:** 585 lines

Debugs code with git safety, reports solution (master applies fix).

### Key Features
- 12 steps with triple-checked git safety protocol
  - Commit → Push to remote → Verify → Debug → Rollback
- 6-type error classification (syntax, data, instructions, logic, import, column)
- Circuit breakers (same error 3× → QUIT, same error type 5× → QUIT, 10 iteration max)
- In-place debugging (not sandbox, avoids path/import issues)
- Rollback verification (git status + commit hash check)
- Enhanced report format (7 sections with root cause + targeted improvements)
- Leverages g_code inline reasoning (header comments)
- Core file safety preserved from v3.0

### Critical Philosophy
- Reports solution, doesn't fix original (enables learning, prevents black-box changes)
- User understands and applies fix (PhD thesis standard)

### Files Created
- `.claude/agents/g_debug.md` (585 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (Sections 2.6.2 and 3.4 updated, TOC ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 13 COMPLETE, A10 completed 2025-11-19)

---

## Phase 14: rq_inspect Agent

**Status:** COMPLETE
**Agent:** A11 - rq_inspect
**Completed:** 2025-11-19
**Specification:** Section 2.4.2
**Lines:** 1,150+ lines

Validates analysis step outputs against plan.md expectations.

### Key Features
- 9 steps with four-layer validation
  - Layer 1: Existence (files exist per plan.md)
  - Layer 2: Structure (columns, dimensions match specifications)
  - Layer 3: Substance (criteria from plan.md met)
  - Layer 4: Logs (ERROR/CONVERGENCE patterns, validation results)
- Log file reading (Step 6 enhancement)
- Status.yaml analysis_steps integration (sequential safety, pending→success)
- inspect_criteria.md template usage
- Core file safety preserved from v3.0

### Status.yaml Updates
- Checks analysis_steps section (step01...stepN-1 = success, stepN = pending)
- Updates current step pending→success with context_dump (max 5 lines)

### Files Created
- `.claude/agents/rq_inspect.md` (1,150+ lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (Section 2.4.2 steps 6-7 updated, TOC ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 14 COMPLETE, A11 completed 2025-11-19)

---

## Phase 15: rq_plots Agent

**Status:** COMPLETE
**Agent:** A12 - rq_plots
**Completed:** 2025-11-19
**Specification:** Section 2.5.1
**Lines:** 1,050+ lines

Generates plots.py calling ONLY existing functions from tools/plotting.py (Option B Architecture).

### Key Features
- 13 steps with 6 circuit breakers
- Option B: Visualization-only (plot source CSVs from g_code)
- Reads tools/plotting.py SOURCE CODE (step 5)
- Checks source CSVs exist (step 7, FAIL if missing)
- Checks functions exist (step 9, FAIL with list if missing)
- NEVER creates new plot functions (triggers TDD migration like rq_tools)
- UTF-8 + absolute paths + NO data aggregation
- Decision D069 support (dual-scale trajectories)

### Critical Role
- WHERE plotting function migration is DETECTED (parallel to rq_tools for analysis)
- Agent FAILs → User adds to tools/plotting.py with TDD → Re-run → PASS

### Files Created
- `.claude/agents/rq_plots.md` (1,050+ lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (Sections 2.3.1, 2.3.3, 2.5.1 updated for Option B, TOC ✨ IMPLEMENTED)
- `docs/v4/templates/plots.md` (Section 3.5 two-phase approach)
- `docs/v4/todo.yaml` (Phase 15 COMPLETE, A12 completed 2025-11-19)

---

## Phase 16: rq_results Agent

**Status:** COMPLETE
**Agent:** A13 - rq_results (FINAL AGENT)
**Completed:** 2025-11-19
**Specification:** Section 2.5.2
**Lines:** 811 lines

Validates scientific plausibility and creates publication-ready summary.md.

### Key Features
- 10 steps with scientific plausibility validation
- 6 check categories (value ranges, effect directions, sample characteristics, model diagnostics, visual inspection, plan expectations)
- Anomaly flagging (extensible 5+ types: implausible values, wrong direction, impossible statistics, contradictions, unexpected nulls)
- Multimodal PNG inspection (existence check FIRST, visual coherence with statistics)
- 6-source synthesis (context_dumps highest priority, data selective, plots multimodal, logs, concept, plan)
- 5-section summary.md (Statistical Findings, Plot Descriptions, Interpretation with Unexpected Patterns, Limitations with Plausibility Concerns, Next Steps)
- Healthy skepticism tone (automated pipeline acknowledgment)
- WebSearch for cognitive neuroscience norms when uncertain

### Primary Mission
- Scientific sanity checker FIRST (does this make any sense?)
- Then summary generation
- First transition from technical automation to cognitive neuroscience context

### Files Created
- `.claude/agents/rq_results.md` (811 lines)

### Files Modified
- `docs/user/analysis_pipeline_solution.md` (Section 2.5.2 complete rewrite, line 1808 quick ref, TOC ✨ IMPLEMENTED)
- `docs/v4/todo.yaml` (Phase 16 COMPLETE, A13 completed 2025-11-19)

---

## Implementation Statistics

**Total Phases Completed:** 17 (Phases 0-16)
**Total Tasks Completed:** 35
**Overall Progress:** 58% of 31-phase roadmap

### Agent Building
- **Total Agents Built:** 13/13 (100%)
- **Total Agent Code:** ~13,000 lines
- **Average Agent Size:** ~770 lines
- **Largest Agent:** rq_planner (1,165 lines)
- **Smallest Agent:** g_conflict (269 lines)

### Templates
- **Total Templates:** 11
- **Total Template Lines:** 9,862
- **Enhanced to v4.1:** 2 (scholar_report, stats_report)

### Documentation
- **Foundation Files:** 5 (best_practices, names, automation, orchestrator, folder structure)
- **Thesis Files:** 3 (CH5, CH6, CH7 with 50 RQs total)
- **Specification Updates:** 13 TOC entries marked ✨ IMPLEMENTED

### Process Adherence
- **11-step process:** Applied to all 13 agent builds
- **Context-finder invocations:** ~40 (averaging 3 per agent)
- **Ultrathink analyses:** 13 (one per agent)
- **User clarifications:** ~25 via AskUserQuestion
- **Specification conflicts resolved:** ~50 across all phases

---

## Key Design Decisions Applied

### Architecture
- **Atomic task-sniper agents** (vs v3.0 monolithic)
- **Pseudo-statefulness** via status.yaml context_dumps
- **Emergent TDD** (tools migrate AS NEEDED during testing)
- **Separation of concerns** (validation vs plausibility, HOW vs WHEN)

### Safety
- **names.md FAIL-on-missing** (prevents hallucinated patterns)
- **Core file editing prohibition** (preserved from v3.0)
- **Git safety protocol** (g_debug triple-check)
- **4-layer validation** (g_code prevents API mismatches)

### Quality
- **Devil's advocate analysis** (rq_scholar, rq_stats)
- **Template-guided generation** (all agents use templates)
- **Context dump mechanism** (max 5 lines, terse summaries)
- **Circuit breakers** (5 types, proactive failure prevention)

### Project-Specific
- **Decision D039:** 2-pass IRT purification (auto-applied by rq_planner)
- **Decision D068:** Dual reporting p-values (uncorrected + Bonferroni)
- **Decision D069:** Dual-scale trajectories (theta + probability)
- **Decision D070:** TSVR time variable (actual hours, not nominal days)

---

## Lessons Learned

### What Worked Well
1. **11-step process with Step 2 explanation** - User confirmation prevented misunderstandings
2. **Ultrathink analysis** - Identified design questions before building
3. **V3 leverage** - Preserved strengths (core safety, devil's advocate, scholarly rigor)
4. **User-driven specifications** - Enhanced spec sections based on user corrections
5. **g_conflict validation** - Caught specification conflicts during agent building

### Challenges Overcome
1. **Context bloat prevention** - Designed atomic agents with lean context windows
2. **Template scope** - Universal templates (not IRT/LMM-locked) with adaptable examples
3. **TDD philosophy** - Resisted upfront tool migration, embraced emergent approach
4. **Orchestration clarity** - Documented master claude role explicitly
5. **Option B architecture** - Separated data aggregation (g_code) from visualization (rq_plots)

### Improvements Made
1. **Enhanced 2 templates to v4.1** (scholar, stats with devil's advocate)
2. **Four-layer validation** (g_code, rq_inspect with log reading)
3. **Multimodal inspection** (rq_results with PNG existence check)
4. **Scientific plausibility** (rq_results primary mission clarified)
5. **In-place debugging** (g_debug with git safety, not sandbox)

---

## Next Steps

**Immediate:** Begin Phase 17 (Test rq_builder agent)

**Testing Sequence:**
1. Phases 17-22: Test setup/validation/planning agents
2. Phase 23: Test rq_tools (FIRST TOOLS DETECTION - critical TDD migration)
3. Phases 24-27: Test execution agents (g_code, g_debug, rq_inspect)
4. Phase 28: Test rq_plots (PLOTTING FUNCTION DETECTION - critical TDD migration)
5. Phase 29: Test rq_results
6. Phase 30: Integration test RQ 5.1 end-to-end
7. Phases 31-32: Legacy archival and finalization

**Expected Timeline:** 7-10 days for all testing phases

**Critical Success Factors:**
- TDD migration when agents FAIL (not upfront guessing)
- Document all tool additions in tool_inventory.md
- Validate each agent individually before integration
- Preserve git rollback points at each phase

---

**End of Build History**
