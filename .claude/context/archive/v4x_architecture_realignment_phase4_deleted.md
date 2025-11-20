# V4.X Architecture Realignment - Phase 4 Deleted

**Topic:** v4x_architecture_realignment_phase4_deleted
**Purpose:** Archive detailed execution steps for Sessions 01:30, 02:45, 12:00, and 17:00 during v4.X architecture realignment
**Scope:** Phase 2 Templates T9-T11 completion, Phase 3 Thesis Files migration, Phase 4 V1 audit, and critical architecture realignment

---

## Session 01:30 - Phase 2 Templates T9-T10 Complete (2025-11-17 01:30)

**Archived from:** state.md Session (2025-11-17 01:30)
**Original Date:** 2025-11-17 01:30
**Reason:** Session 3+ ago, archive detailed execution steps (keep milestones in state.md)

### Task Context

Built final 2 output/validation templates totaling 2,046 lines. T9 (inspect_criteria.md) provides Layer 5 validation checklist for rq_inspect agent (per-step output validation). T10 (plots.md) catalogs 6 plotting functions from tools/plotting.py with MANDATORY Decision D069 dual-scale trajectory requirements.

### T9: inspect_criteria.md (987 lines)

**10-Step Process Execution:**
1. **Context-finder (spec 4.3.3, rq_inspect workflow, v3 results_inspector lessons)** - Found 7 key sources
2. **Ultrathink** - Identified design tensions
3. **AskUserQuestion** - 4 design questions:
   - Scope: Comprehensive (like T7-T8) vs minimal
   - Format: Markdown checkboxes vs JSON schema vs plain text
   - Examples: TDD placeholders vs complete examples
   - Error reporting: Simple pass/fail vs detailed diagnostics
4. **Verify** - No spec conflicts
5. **Create** - 987-line template

**User Design Choices:**
- Comprehensive scope (like T7-T8)
- Markdown checkbox format (v3 proven pattern)
- TDD step-type examples (populate during RQ 5.1)
- Simple pass/fail error reporting

**Template Structure:**
- 4 required sections: Input Verification, Output Verification, Format Verification, Cross-Reference with plan.md
- TDD placeholders: IRT calibration, item purification, LMM fitting, plotting (empty, populate during RQ 5.1)
- v4.X per-step validation (fail-fast) vs v3.0 end-of-pipeline validation (too late)
- Layer 5 of multi-layer validation defense
- Checklist structure from v3 rq_file_structure_ground_truth.md
- Integration with rq_inspect workflow: reads status.yaml, validates outputs, updates context_dump

### T10: plots.md (1,059 lines)

**10-Step Process Execution:**
1. **Context-finder (spec 4.4.1, tools/plotting.py, D069, v3 lessons)** - Found 12 organized sources
2. **Ultrathink** - Identified design tensions
3. **AskUserQuestion** - 3 design questions:
   - Documentation depth: Full signatures vs summary + key parameters vs minimal
   - D069 prominence: Dedicated major section vs integrated throughout
   - TDD naming: Generic only vs propose conventions
4. **Verify** - No spec conflicts
5. **Create** - 1,059-line template

**User Design Choices:**
- Summary + key parameters (hybrid, agent reads source code anyway)
- D069 dedicated major section (MANDATORY, prominent)
- Generic TDD naming only (pure emergent from RQ 5.1)

**Template Structure:**
- **Section 1:** 6 plotting functions documented
  - setup_plot_style
  - plot_trajectory
  - plot_trajectory_probability
  - plot_diagnostics
  - plot_histogram_by_group
  - theta_to_probability
  - save_plot_with_data
- **Section 2:** Decision D069 DEDICATED (MANDATORY dual-scale trajectory plots)
  - 7-item validation checklist
  - IRT transformation formula P=1/(1+exp(-(a*(θ-b))))
  - Rejection criteria if probability plot missing
- **Section 3:** Output formats (PNG 300 DPI, dimensions, REMEMVR color scheme)
- **Section 4:** File naming (generic TDD only, consult names.md, propose during RQ 5.1)

**rq_plots Workflow Integration:**
- Step 5 reads tools/plotting.py SOURCE CODE (learns complete signatures)
- Step 8 validates all required functions exist (FAIL if missing, no hallucination)
- v4.X philosophy: ONLY call existing functions, consistency across 50 RQs, fail-fast validation

**D069 Prominence:**
- Dedicated 200+ line section ensures dual-scale trajectory compliance
- Theta + probability scales BOTH required
- Applies to ~40 RQs

**Reproducibility:**
- PNG + CSV pairs via save_plot_with_data() for all plots

### Context-Finder Performance

**T9 findings:** 7 key sources
- Spec 4.3.3
- rq_inspect agent 2.4.2
- v3 results_inspector
- v3 file structure validation checklists
- Multi-layer validation architecture

**T10 findings:** 12 organized findings
- Spec 4.4.1
- rq_plots agent 2.5.1
- tools/plotting.py 6 functions
- D069 complete specification
- D070 time variable
- names.md TDD status
- Output formats
- v3 lessons learned

**Total:** 19 sources analyzed, ~15k tokens consumed

### Design Patterns Established

1. **Comprehensive scope:** All templates 700-1100 lines (detailed guidance + examples + integration notes)
2. **Production-proven elements:** v3 rubrics preserved (T7-T8), v3 checkbox patterns reused (T9), v3 lessons learned applied (T10)
3. **TDD compatibility:** Empty placeholders where conventions/examples emerge from RQ 5.1
4. **User-driven design:** AskUserQuestion for all ambiguous decisions (3-4 questions per template)
5. **Multi-layer integration:** Each template explains role in broader v4.X architecture

### Files Modified

1. `docs/v4/templates/inspect_criteria.md` - NEW (987 lines)
2. `docs/v4/templates/plots.md` - NEW (1,059 lines)
3. `docs/user/analysis_pipeline_solution.md` - TOC updated (Section 4.3 COMPLETE, 4.4.1 IMPLEMENTED)
4. `docs/v4/todo.yaml` - T9 & T10 marked completed

### Lessons Learned

1. **Hybrid documentation depth works:** Summary + key parameters prevents duplication while providing essential guidance
2. **D069 needs prominence:** Dedicated major section with validation checklist ensures MANDATORY requirement impossible to miss
3. **TDD placeholders effective:** Empty examples with clear instructions for RQ 5.1 population maintains TDD philosophy
4. **Context-finder scales well:** 19 sources across 2 templates enables comprehensive evidence-based design
5. **10-step process consistency:** Following same procedure builds muscle memory, ensures thoroughness

### Progress Metrics

**Phase 2 Templates: 91% Complete (10/11 done)**

Total template lines: 8,130 lines across 10 files
- T1: build_folder.md (349 lines)
- T2: build_status.md (542 lines)
- T3: concept.md (767 lines)
- T4: plan.md (870 lines)
- T5: tools.md (1,022 lines)
- T6: analysis.md (892 lines)
- T7: scholar_report.md (745 lines)
- T8: stats_report.md (910 lines)
- T9: inspect_criteria.md (987 lines)
- T10: plots.md (1,059 lines)

**Remaining:** T11 results.md

**Section 4.3 Validation Templates:** COMPLETE (all 3 done)
**Section 4.4 Output Templates:** 50% (1/2 done)

### Token Budget

- Session start after /clear + /refresh: ~10k
- Session end: ~119k (60%)
- Growth: ~109k
- Status: Approaching /save threshold (recommend at 140k)

---

## Session 02:45 - Phases 2 & 3 COMPLETE (T11 + H1-H3) (2025-11-17 02:45)

**Archived from:** state.md Session (2025-11-17 02:45)
**Original Date:** 2025-11-17 02:45
**Reason:** Session 3+ ago, archive detailed execution steps (keep milestones in state.md)

### Task Context

Completed final Phase 2 template (T11 results.md, 1,408 lines) bringing Phase 2 to 100% (all 11 templates, 9,551 lines total). Immediately transitioned to Phase 3 and moved all 3 thesis analysis files (ANALYSES_CH5/6/7.md, 50 RQs total) to docs/v4/thesis/ directory. Two full phases completed in single session.

### T11: results.md (1,408 lines) - Phase 2 Final Template

**10-Step Process Execution:**
1. **Context-finder (spec, v3, verification)** - Used 3 times, returned comprehensive findings
2. **Ultrathink** - Design tensions identified
3. **AskUserQuestion** - 4 design questions resolved all ambiguities upfront
4. **Verify** - No spec conflicts
5. **Create** - 1,408-line comprehensive template

**User Design Choices (4 Questions Answered):**
- Section-level examples ideal for TDD (provides structural guidance, maintains emergent design)
- Workflow integration sections essential (6 input sources + synthesis strategy explicit)
- D069 prominence critical (dedicated subsection in results.md after plots.md coverage)
- Template consistency matters (matches T7-T10 pattern)

**Template Features:**
- Comprehensive scope (1,408 lines, largest template)
- Error handling guidance
- Section-level examples (NOT complete document)
- Integration notes (6 input sources documented)
- D069 dual-scale interpretation (200+ lines dedicated)
- Workflow synthesis strategy explicit

**Why Largest Template:**
- Results synthesis is most complex task
- Must integrate 6 different input sources
- D069 interpretation requires detailed guidance
- Error handling scenarios numerous

### Phase 3: Thesis Files Migration (H1-H3)

**Files Moved:**
1. **H1:** ANALYSES_CH5.md → docs/v4/thesis/ANALYSES_CH5.md
   - 15 RQs
   - 79K size
   - Git history preserved via `git mv`

2. **H2:** ANALYSES_CH6.md → docs/v4/thesis/ANALYSES_CH6.md
   - 15 RQs
   - 106K size
   - Git history preserved via `git mv`

3. **H3:** ANALYSES_CH7.md → docs/v4/thesis/ANALYSES_CH7.md
   - 20 RQs
   - 163K size
   - Git history preserved via `git mv`

**Total:** 50 RQs across 3 chapters (348K total)

**Integration with v4.X:**
- Location: docs/v4/thesis/ (accessible to rq_concept agent per spec 2.1.2 step 5)
- Purpose: rq_concept agent reads thesis files to generate concept.md
- Git history: Preserved for future investigation of RQ specification changes

### Files Modified

**Created:**
1. `docs/v4/templates/results.md` - NEW (1,408 lines, Phase 2 final template)

**Moved:**
2. `docs/v4/thesis/ANALYSES_CH5.md` (was in docs/)
3. `docs/v4/thesis/ANALYSES_CH6.md` (was in docs/)
4. `docs/v4/thesis/ANALYSES_CH7.md` (was in docs/)

**Updated:**
5. `docs/user/analysis_pipeline_solution.md` - TOC updated (Section 4.4 COMPLETE, Section 4.5 COMPLETE)
6. `docs/v4/todo.yaml` - T11 & H1-H3 marked completed
7. `.claude/context/current/state.md` - Session summary

### Progress Metrics

**Overall Implementation: 21/50 tasks complete (42%)**

**Phase Status:**
- Phase 0: Names.md Design - COMPLETE (F0a-F0b, 2 tasks)
- Phase 1: Foundation - COMPLETE (F1-F5, 5 tasks)
- Phase 2: Templates - COMPLETE (T1-T11, 11 tasks, 9,551 lines)
- Phase 3: Thesis Files - COMPLETE (H1-H3, 3 tasks, 50 RQs)
- Phase 4: Validation Tools Migration - PENDING (V1-V4, 4 tasks)

**Template Statistics (Phase 2 Final):**
- Total templates: 11 files
- Total lines: 9,551 lines
- Average size: 868 lines per template
- Size range: 349 lines (T1) to 1,408 lines (T11)

**Thesis Files Statistics (Phase 3 Final):**
- Total files: 3 chapters
- Total RQs: 50 (CH5=15, CH6=15, CH7=20)
- Total size: 348K
- Location: docs/v4/thesis/

**Specification Sections Complete:**
- Section 4.1 Setup Templates: COMPLETE
- Section 4.2 RQ Documentation Templates: COMPLETE
- Section 4.3 Validation Templates: COMPLETE
- Section 4.4 Output Templates: COMPLETE (T11 completed this section)
- Section 4.5 Support Documentation: COMPLETE (H1-H3 completed this section)

**All Section 4 (Documentation Templates) Now 100% Complete**

### Token Budget

- Session start: ~47k
- After T11 context-finder: ~69k
- After T11 creation: ~85k
- After H1-H3 migration: ~96k
- After docs updates: ~103k
- Session end: ~108k (54%)
- Growth: ~61k
- Free space: 92k (46%)
- Status: Good for /save, healthy buffer

### Lessons Learned

1. **Parallel phase completion possible:** T11 + H1-H3 in single session demonstrates efficiency
2. **Git mv preserves history:** File relocations maintain git history for future investigation
3. **Comprehensive templates pay off:** 1,408-line template prevents agent mistakes during RQ execution
4. **Section-level examples ideal for TDD:** Structural guidance without complete document
5. **Workflow integration sections essential:** Explicit 6 input sources + synthesis strategy reduces guesswork
6. **D069 prominence critical:** Dedicated subsection in results.md ensures compliance for ~40 trajectory RQs
7. **Phase boundaries flexible:** H1-H3 straightforward after T11 complexity, parallel execution natural
8. **10-step process scales:** Context-finder used 3 times, comprehensive findings enabled informed decisions
9. **User-driven design prevents rework:** 4 AskUserQuestion queries resolved ambiguities upfront
10. **Template consistency matters:** T11 matches T7-T10 pattern, predictable structure for agents

---

## Session 12:00 - Phase 4 V1 Audit Complete (2025-11-17 12:00)

**Archived from:** state.md Session (2025-11-17 12:00)
**Original Date:** 2025-11-17 12:00
**Reason:** Detailed execution steps archived (keep high-level milestone in state.md)

### Task Context

After completing Phases 0-3 (21/50 tasks, 42%), began Phase 4 Validation Tools Migration. V1 task required comprehensive audit of existing v3 validation capabilities to design v4.X migration strategy. Following mandatory 10-step process with proactive context-finding workflow.

### Context-Finding (Steps 1-3)

**Invoked context-finder agent:**
- Searched for v4.X validation requirements
- Searched for v3 validation implementations
- Found 8 comprehensive findings across 7 files

**Key Findings:**
- Spec sections 4.2.3, 4.2.4, 4.3.3, 5.1, 6.1
- Archives
- tool_inventory.md
- 5-layer validation architecture:
  - Layer 1: tool inventory
  - Layer 2: rq_tools
  - Layer 3: rq_planner
  - Layer 4: rq_analysis
  - Layer 5: g_code

**v3 Validation Tools:**
- 14 functions in tools/validation.py (650 lines)
- Categories:
  - Data Lineage Tracking (4 functions)
  - IRT Validation (3 functions)
  - LMM Validation (2 functions)
  - General Validation (3 functions)
  - Validation Reporting (2 functions)
- All 49/49 tests passing in tests/test_validation.py (362 lines)

**Gaps Identified:**
- No CTT validation
- No plotting-specific validation
- No standardized interface

**Files Read:**
- tools/validation.py (650 lines)
- tests/test_validation.py (362 lines)

### User Design Decisions (Step 5)

**4 Questions Asked via AskUserQuestion:**

1. **Interface standardization:**
   - Choice: Hybrid approach
   - Keep existing v3 fields (valid, converged, exists)
   - Add standardized `validation_passed` field for v4.X

2. **Error reporting:**
   - Choice: BREAKING CHANGE
   - Raise `ValidationError(message, details=dict)` on failure
   - No more returning dict (prevents silent fails)
   - Provides detailed error logs

3. **CTT validation:**
   - Choice: DEFERRED
   - Build only if RQ 5.1 testing reveals need
   - TDD approach (no CTT tools in v3)

4. **Plotting validation:**
   - Choice: Build 4 categories
   - Lineage/file checks (existing sufficient)
   - D069 dual-scale validation (~40 trajectory RQs)
   - DPI/dimensions validation (300 DPI compliance)
   - Plot content validation (axes/labels)

### V1 Audit Document (Step 7: Perform)

**File Created:** docs/v4/validation_audit.md
- 766 lines
- 19,700 words
- 9 comprehensive sections

**Section Breakdown:**

**1. Existing v3 Validation Tools** (14 functions inventoried)
- 1.1 Data Lineage Tracking (4 functions) - Prevents Pass 1/Pass 2 mixups
- 1.2 IRT Validation (3 functions) - Convergence, parameters per D039, missing data
- 1.3 LMM Validation (2 functions) - Convergence, residuals normality
- 1.4 General Validation (3 functions) - Columns, file existence, numeric ranges
- 1.5 Validation Reporting (2 functions) - Multi-check aggregation, JSON persistence

**2. Gaps Identified**
- 2.1 CTT Validation - DEFERRED (no CTT in v3)
- 2.2 Plotting Validation - BUILD NEW (4 functions)
- 2.3 Interface Standardization - ENHANCE EXISTING (add validation_passed)
- 2.4 Error Reporting - BREAKING CHANGE (ValidationError exception)

**3. Migration Plan**
- V2a: Migrate 3 IRT validation functions (30-60 min, TDD)
- V2b: Migrate 2 LMM validation functions (20-40 min, TDD)
- V2c: CTT deferred (0 min unless RQ 5.1 requires)
- V2d: Build 4 new plotting functions + enhance 9 general (2-3 hours, Pillow dependency)
- Total estimate: 5-7 hours

**4. Validation Tool Interface Design**
- Function signature pattern
- Return dict structure
- Field mapping rules (valid→validation_passed, etc.)
- Error reporting pattern (ValidationError class example)
- Integration with v4.X 5-layer architecture

**5. Dependencies**
- Existing: pandas, numpy, scipy.stats, pathlib, json, typing (satisfied)
- New: Pillow (PIL) for PNG metadata (HIGH priority for V2d)
- Deferred: pytesseract for OCR (LOW priority)

**6. Testing Strategy**
- 100% coverage requirement (EXACTLY 100%, not ≥80% per Issue #22)
- Test organization: Enhance existing test_validation.py
- TDD workflow per function (RED → GREEN → REFACTOR with code examples)

**7. Timeline Estimate** (5-7 hours total)

**8. Success Criteria** (all tasks with verification checkpoints)

**9. Next Steps** (V1→V2a/V2b/V2d→V3→V4)

**Appendices:**
- Appendix A: Complete v3 function signatures
- Appendix B: Proposed v4.X signatures

### Verification (Step 8)

**All V1 Criteria Met:**
- ✅ Existing validation tools inventoried (14 functions)
- ✅ Gaps identified (CTT deferred, plotting 4 new, interface hybrid, error exception)
- ✅ Migration plan documented (V2a-V2d, 5-7 hour estimate)
- ✅ Validation tool interface design (signatures, return dict, error reporting, 5-layer integration)

**Document Comprehensive:** 9 sections covering all migration aspects

**User Decisions Documented:** 4 questions, 4 answers, design implications

### Documentation Updates (Steps 9-10)

**Files Modified:**
1. `docs/v4/validation_audit.md` - NEW (766 lines, audit document)
2. `docs/v4/todo.yaml` - V1 marked completed with:
   - completed_date: 2025-11-17
   - verified field (comprehensive summary)
   - design_decisions section (4 key decisions)
   - user_answers section (4 questions)
3. `.claude/context/current/state.md` - Session summary

**TodoWrite Updated:** V1 marked completed ✅

**Note:** No analysis_pipeline_solution.md TOC update needed (V1 is implementation audit, not spec section)

### Lessons Learned

1. **10-step process effectiveness:** Mandatory context-finder prevented guessing, enabled evidence-based decisions
2. **Context-finder value:** Single invocation returned 8 findings across 7 files (~15 seconds vs hours of reading)
3. **Proactive user questions:** Ultrathink identified tensions, user answered upfront, prevented rework
4. **User choice: Exception pattern:** Superior to v3 silent-fail, prevents cascading errors, enforces fail-fast
5. **User choice: Hybrid interface:** Backward compatibility + standardized checking in v4.X
6. **User choice: CTT deferral:** TDD approach prevents premature optimization
7. **User choice: Plotting validation depth:** 4-category graduated approach (start D069, add content if needed)
8. **Documentation thoroughness:** 19.7k words prevents future questions
9. **Appendices utility:** Complete signature references for V2a-V2d implementation
10. **Dependency planning:** Pillow requirement identified early, prevents mid-implementation blockers

### Progress Metrics

**Phase 4 Validation Tools Migration: 14% Complete (1/7 tasks)**
- ✅ V1: Audit - COMPLETE
- ⏳ V2a: IRT migration - PENDING (30-60 min)
- ⏳ V2b: LMM migration - PENDING (20-40 min)
- ⏳ V2c: CTT migration - DEFERRED (0 min unless needed)
- ⏳ V2d: Plotting migration - PENDING (2-3 hours)
- ⏳ V3: Update tool_inventory.md - PENDING (30-45 min)
- ⏳ V4: Test all validation - PENDING (15-30 min)

**Overall V4.X Implementation: 22/50 tasks complete (44%)**

**V1 Audit Statistics:**
- Document: 766 lines, 19,700 words
- v3 functions inventoried: 14
- New functions to build: 4 (plotting validation)
- User decisions: 4
- Migration tasks: 4 (V2a, V2b, V2c deferred, V2d)
- Estimated Phase 4 effort: 5-7 hours
- Test coverage: 100% (EXACTLY, not ≥80%)

### Token Budget

- Session start: ~47k
- After context-finder: ~69k
- After tools/validation.py read: ~75k
- After tests/test_validation.py read: ~79k
- After AskUserQuestion: ~81k
- After validation_audit.md: ~90k
- After todo.yaml: ~96k
- After TodoWrite: ~97k
- Session end: ~114k (57%)
- Growth: ~67k
- Free space: 86k (43%)
- Status: Healthy, can continue V2a or /save

---

## Session 17:00 - CRITICAL Architecture Realignment (2025-11-17 17:00)

**Archived from:** state.md Session (2025-11-17 17:00)
**Original Date:** 2025-11-17 17:00
**Reason:** Detailed execution steps archived (keep critical corrections in state.md)

### Critical Issue Identified

**Problem:** User noticed I was conflating v3.0 and v4.X architectures

**Root Cause:** Step 1 of 10-step process said "search analysis_pipeline_solution.md for all info" but didn't explicitly say "ONLY solution.md"

**Result:** Context-finder was reading docs OUTSIDE solution.md, I was mixing v3 context with v4.X design

**User Action:** Requested re-read of solution.md to realign understanding

### Re-Read Solution.md - Critical Corrections

**5 Fundamental Misunderstandings Corrected:**

1. **I am master orchestrator** (Section 1.2 line 164)
   - NOT rq_builder
   - I orchestrate ALL agents

2. **rq_concept GENERATES concept.md** (Section 2.1.2)
   - Extracts from thesis
   - User approves AFTER generation
   - NOT user writes manually like v3

3. **rq_tools DETECTS missing tools** (Section 2.3.2 lines 478-479)
   - Steps 8-9 check tool_inventory.md
   - FAIL with missing list if not found
   - Triggers TDD migration

4. **Tools/validation emerge during testing**
   - NOT upfront migration
   - TDD approach when agents FAIL
   - Phases 23 & 28 are critical detection points

5. **13 agents = 13 testing phases**
   - Section 2 has 13 separate agent specs
   - Each needs rigorous individual testing

### User Questions (4 Questions via AskUserQuestion)

**Question 1: Agent building phases**
- Keep grouped (current 6 phases)?
- Split individual (13 phases)?
- **Answer:** Split individual (13 phases)

**Question 2: Phase 4 status**
- Keep?
- Delete?
- Repurpose?
- **Answer:** Delete entirely, renumber everything

**Question 3: Testing detail**
- Explicit tool migration sub-steps?
- General guidance?
- **Answer:** Yes - explicit sub-steps (4a-4d)

**Question 4: Explain agent step placement**
- Before v3 search?
- After AskUserQuestion?
- **Answer:** Between Step 1 (solution.md ONLY) and Step 2 (v3 materials)

### Complete todo.yaml Restructure

**Changes Made:**
- **Phase 4 DELETED:** V1 audit kept as reference, V2-V4 deferred to testing
- **Phases 0-3:** Foundation COMPLETE (21 tasks, 42%) - No changes
- **Phases 4-16:** Agent Building (13 agents, one phase per agent)
- **Phases 17-29:** Agent Testing (13 agents, one phase per agent, dependency order)
- **Phase 30:** Integration Testing (RQ 5.1 end-to-end)
- **Phases 31-32:** Legacy Archival + Finalization
- **Total: 32 phases, ~60 tasks**

**Agent Building Phases (4-16):**
1. Phase 4: Build rq_builder
2. Phase 5: Build rq_concept
3. Phase 6: Build rq_scholar
4. Phase 7: Build rq_stats
5. Phase 8: Build g_conflict
6. Phase 9: Build rq_planner
7. Phase 10: Build rq_tools
8. Phase 11: Build rq_analysis
9. Phase 12: Build g_code
10. Phase 13: Build g_debug
11. Phase 14: Build rq_inspect
12. Phase 15: Build rq_plots
13. Phase 16: Build rq_results

**Agent Testing Phases (17-29):**
1. Phase 17: Test rq_builder
2. Phase 18: Test rq_concept (depends on rq_builder)
3. Phase 19: Test rq_scholar
4. Phase 20: Test rq_stats
5. Phase 21: Test g_conflict
6. Phase 22: Test rq_planner
7. **Phase 23: Test rq_tools** ← FIRST TOOLS DETECTION/MIGRATION
8. Phase 24: Test rq_analysis
9. Phase 25: Test g_code
10. Phase 26: Test g_debug
11. Phase 27: Test rq_inspect
12. **Phase 28: Test rq_plots** ← PLOTTING FUNCTION DETECTION/MIGRATION
13. Phase 29: Test rq_results

### 11-Step Process for Agent Building (Updated from 10-step)

**Step 1:** context-finder: Search **ONLY docs/user/analysis_pipeline_solution.md** (NOT archives, NOT other docs) ← **CRITICAL FIX**

**Step 2:** **EXPLAIN AGENT** in plain language, WAIT for user confirmation ← **NEW STEP**

**Step 3:** context-finder: Search archives/ and docs/ for v3.0 equivalent

**Step 4:** context-finder: Read relevant v3 files

**Step 5:** ultrathink: Best approach? What needs clarification?

**Step 6:** AskUserQuestion: Iterate until clarified

**Step 7:** context-finder: Verify no conflicts with solution.md

**Step 8:** perform: Build agent prompt in .claude/agents/

**Step 9:** verify: Confirm agent matches spec (steps, frontmatter, report format)

**Step 10:** update_toc: Mark relevant heading in solution.md with ✨ IMPLEMENTED

**Step 11:** update_todo: Mark task complete in todo.yaml

### 6-Step Testing Process with Explicit Tool Migration

**Each testing phase follows:**

**Step 1:** Verify required files exist

**Step 2:** Verify prompt matches spec

**Step 3:** Predict agent behavior (including EXPECTED FAILURES)

**Step 4:** Execute agent with tool migration sub-steps:
- **4a:** Detect missing tools (agent FAILS with "Missing: [list]")
- **4b:** Migrate missing analysis tools (check v3, migrate with TDD, verify GREEN)
- **4c:** Migrate missing validation tools (check validation_audit.md, migrate with TDD, verify GREEN)
- **4d:** Update tool_inventory.md (document newly migrated tools)
- **4e:** Re-run agent (should now PASS)

**Step 5:** Inspect outputs

**Step 6:** Verify against spec

### Files Modified

**Updated:**
1. `docs/v4/todo.yaml` - COMPLETE RESTRUCTURE (805 lines)
   - Deleted Phase 4 (validation upfront migration)
   - Split agent building into 13 individual phases (4-16)
   - Split testing into 13 individual phases (17-29)
   - Added explicit tool migration sub-steps (4a-4e) in testing phases 23 & 28
   - Updated to 32 phases total, ~60 tasks
   - V1 validation audit marked as reference (not deleted, purpose documented)

### Lessons Learned - CRITICAL

1. **Step 1 must be EXPLICIT:** "Search ONLY solution.md" prevents v3 contamination - generic "search for all info" leads to mixed context

2. **User explanation checkpoint critical:** Step 2 (explain agent, wait for confirmation) catches misunderstandings BEFORE building wrong thing

3. **v3/v4 conflation danger real:** Without explicit boundaries, easy to mix v3.0 specs with v4.X design

4. **Tool migration is emergent TDD:** NOT upfront phase - agents FAIL, detect missing, we migrate AS NEEDED with tests

5. **Phase 23 (test rq_tools) is THE critical test:** Agent detects "Missing: calibrate_grm, fit_lmm_with_tsvr, validate_irt_convergence", triggers first TDD migration cycle

6. **Phase 28 (test rq_plots) is second critical test:** Agent detects "Missing plot functions: [list]", triggers plotting function TDD migration

7. **13 individual agent testing phases mandatory:** RIGOROUS testing per agent (task-snipers need marksmanship testing) - v3 failed because agents weren't following instructions

8. **Ongoing tool/validation migration:** Across 50 RQs constantly add new functions - TDD approach scales, upfront build wasteful

9. **Solution.md is ONLY ground truth:** If not in solution.md, it's not v4.X architecture - archives/docs/v3 are reference ONLY

10. **I am master orchestrator:** Fundamentally changes my role - I invoke all agents sequentially per automation.md 17-step workflow, I handle errors, I coordinate

### Progress Metrics

**V4.X Implementation: 21/~60 tasks complete (~35%)**

**Phase Status (NEW STRUCTURE):**
- Phases 0-3: Foundation - COMPLETE (21 tasks, 42% of old roadmap)
- Phases 4-16: Agent Building - PENDING (13 agents, one per phase, 11-step process)
- Phases 17-29: Agent Testing - PENDING (13 agents, one per phase, 6-step verification with tool migration)
- Phase 30: Integration - PENDING (RQ 5.1 end-to-end)
- Phases 31-32: Finalization - PENDING

**Critical Correction:**
- OLD: 14 phases, 50 tasks, Phase 4 = validation migration upfront
- NEW: 32 phases, ~60 tasks, Phase 4 deleted, tools/validation migrate AS NEEDED during testing

### Token Budget

- Session start: ~7k
- After context-finder: ~55k
- After test results read: ~56k
- After 4 burning questions: ~58k
- After re-reading solution.md (1,831 lines): ~90k
- After re-reading todo.yaml (778 lines): ~120k
- After complete restructure (805 lines new): ~140k
- After TodoWrite: ~140k
- Session end: ~164k (82%)
- Growth: ~157k
- Free space: 36k (18%)
- Status: CRITICAL - Need /save immediately

---

**End of Archive**
