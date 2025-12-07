# Archive Index

**Last Updated:** 2025-12-07 23:10 (context-manager curation)

**Purpose:** Index of archived context topics (timestamped memory banks)

---

## Available Topics

### automation_foundations
**Description:** Pre-migration automation work completed before Memory System Overhaul. Includes tool suite (49/49 tests passing), 50 RQ specifications, Data-Prep Agent v3.0, Analysis-Executor Agent v2.0, agent testing learnings, automation architecture v2, item name preservation fix, and automation phase info.

### codebase_audit
**Description:** Comprehensive codebase audit completed 2025-11-08 revealing 19 organizational issues (13 codebase + 6 meta-issues). Documents root cause analysis showing context management protocol non-compliance led to organizational drift. Audit led directly to Memory System Overhaul implementation.

### decisions_automation
**Description:** Key automation architecture decisions D037-D047 (2025-11-07 to 2025-11-08). Includes agent-based architecture, 2-pass IRT methodology, automation-robust tool design, strict tool-only rules, embedded critical knowledge principle. Note: Refactor decisions D001-D027 predate this system.

### memory_research
**Description:** Memory management system research and analysis (2025-11-08). Validates 7 proposed solutions against Anthropic best practices. Key findings: Skills System exists (75% token savings), MCP Memory Keeper production-ready, /clear every 20 iterations, /cycle command not viable. Informed Tier 1-3 implementation strategy.

### primer_snapshots
**Description:** Snapshots of primer.md at key milestones. Includes pre-Memory System Overhaul snapshot (2025-11-08 21:00) showing project state with 162k/200k tokens, all automation foundations complete, codebase audit complete, ready for Tier 1 implementation.

### refactor_phase
**Description:** Refactor phase completion snapshot (Phases 0-6, January 2025). Documents transition from monolithic scripts to modular tool suite. Created tools/ package, config/ directory, results structure, Poetry setup, context management system.

### memory_system_overhaul_implementation
**Description:** Detailed execution history for Phases 1-9 of Memory System Overhaul (backup, structure creation, docs index, context consolidation, agent prompts, slash commands, agent testing, slash command testing, CLAUDE.md restructuring). Complete step-by-step implementation details with timestamps.

### memory_system_overhaul_decisions
**Description:** Key architectural and workflow decisions made during Memory System Overhaul. Includes Decision D048 (Proactive Context-Finding Workflow) and Decision D049 (CLAUDE.md is Trait Memory Only). Documents rationale, impact, and implementation details.

### data_prep_phase
**Description:** Data-Prep Agent development and testing (Phase 3-4 of refactor, 2025-11-05 to 2025-11-08). Includes implementation plan, extract_vr_items_wide() function creation, critical validation failure discovery (v2.0 bug), and v3.0 fix. Documents how agent extracted wrong data (73% empty columns) due to missing tag system knowledge, and complete fix embedding tag reference in agent prompt.

### rq_specification_phase
**Description:** RQ-Specification Phase (Phase 7 of refactor, 2025-11-06 to 2025-11-07). Complete 7-step plan for specifying all 50 RQs across chapters 5, 6, 7. Three-agent validation system (RQ-Spec, Scholar, Statistics Expert) with flat file-based architecture. Ultra-conservative context management strategy (7 /clear operations). RQ builder methodology achieving 9.37/10 average quality. Includes phase7_plan, context strategy, clear checklist, step3 plan, agent improvements (MCPs + thesis context), and complete methodology reference.

### agent_standard_procedure_v3
**Description:** Complete overhaul of RQ standard procedure from v2.0 to v3.0 (2025-11-12 16:00). Ultrathink analysis identified 15 critical vagueness issues resolved with stateful agent design, universal templates (not IRT/LMM-locked), hybrid safety gates (Steps 5 & 7), Markdown reports (not JSON), and comprehensive template system (9 templates). Established zero-tolerance for vagueness principle. Key decisions: D056 (keep config.yaml), D057 (stateful rq-spec via context dumps), D058 (universal templates).

### agent_safety_critical_fixes
**Description:** Critical safety fixes preventing catastrophic mock data generation (2025-11-12 13:00). RQ 5.5 testing revealed data-prep agent created MOCK theta scores using logit transform when info.md confused data sources. Added 120-line "NEVER GENERATE MOCK DATA" safety section to data-prep agent, 83-line data source separation requirement to rq-specification agent. Established agent scope boundaries: data-prep extracts RAW data only, analysis-executor creates derived data. Decisions: D054 (mock data prohibition), D055 (data source separation).

### rq_automation_testing
**Description:** Data-prep agent testing on RQs 5.1, 5.3, and 5.5 (2025-11-12 sessions 1-2). RQ 5.1 successful with exemplary documentation. RQ 5.3 successful but inconsistent (no companion .md files). RQ 5.5 attempt 1 detected item code bug (agent quit correctly), attempt 2 generated mock data (catastrophic, led to safety fixes). Established companion .md file requirements, core file edit safety rules (Decision D053). Testing validated agent error detection works when specs have detectable errors.

### agent_framework_cleanup
**Description:** Agent directory cleanup and documentation consolidation (2025-11-11 19:15). Moved user documentation from agents/ to docs/ (DATA_PREP_AGENT_GUIDE.md, README.md, tools_inventory.md). Deleted orphaned files (agents/prompts/, agents/schemas/). Established clear separation: .claude/agents/ for agent prompts (Anthropic spec), docs/ for user documentation. Companion .md file requirements established for data consistency across RQs.

### agent_v3_validation
**Description:** Complete validation history of agent v3.0 features from initial prompt audits through bug discovery and resolution to full validation testing. Includes Groups A & B updates (2025-11-12 17:00), rq-specification stateful design completion and file persistence bug discovery (2025-11-13 08:30). Documents Markdown reports, 10-point rubrics, stateful behavior, universal templates, MCP integration, WebSearch integration, companion file requirements, and GitHub Issue #4462 YAML frontmatter fix leading to successful validation.

### rq_specification_v3_workflow
**Description:** RQ Specification Agent v3.0 human-in-the-loop workflow implementation (2025-11-13 15:45-18:00). Designed 4-mode workflow (Circuit Breaker, Planning, Drafting, Finalization) with stateful operation via logs/rq_spec_context.md. Created concept.md and plan.md templates for user review gates. Updated rq_specification.md from 483 to 1533 lines. Established universal templates (not IRT/LMM-locked) and hybrid safety gates at Steps 5 & 7. Ready for testing on RQ 5.1.

### documentation_ground_truth_consolidation
**Description:** Comprehensive documentation audit and consolidation (2025-11-14 morning). Discovered hallucinations in glossary.md (particularly -L- described as "legacy, mostly unused" when actually for static objects). Fixed 6 conflicts between glossary.md and data_structure.md: A10 UID format, -L- domain description, incongruent suffix (IC→IN), test timing, TCR task count, NART abbreviation. Merged glossary.md into data_structure.md using ultrathink (896 lines total, zero information loss). Added Quick Reference Tables section with domain-paradigm mappings and regex wildcards. Updated 26 agent references across 7 files. Deleted glossary.md. Created single authoritative reference verified against user's ground truth (codebase_explanation.md). Decisions: D066 (single source of truth), D067 (authoritative designation).

### decision_d069_dual_scale_trajectory_plots
**Description:** Decision D069: Dual-scale trajectory plotting requirement (2025-11-14 evening). User requested dual-scale plots for interpretability (theta + probability scales). Theta scale (-3 to +3) abstract for non-psychometricians, probability scale more accessible. Added complete decision to project_specific_stats_insights.md (+245 lines): problem statement, IRT transformation formula, implementation steps, validation checklist (7 items), why project-specific. Updated concept.md and docs_index.md. Tested with rq-spec agent invocation 2: agent successfully detected D069, incorporated in 6 sections of plan.md. Applies to all 50 RQs with trajectory plots. Enhances interpretability while preserving statistical rigor.

### decision_d070_tsvr_pipeline
**Description:** Decision D070: IRT→LMM pipeline with TSVR time variable (2025-11-14 evening). Fixed critical documentation gap where agents would use nominal days (0,1,3,6) instead of TSVR (actual hours since encoding) as LMM time variable. Root cause: lmm_methodology.md said "Days 0,1,3,6", irt_methodology.md didn't explain downstream LMM usage. Created complete 5-step IRT→LMM pipeline documentation (+327 lines in project_specific_stats_insights.md): calibration, theta extraction, TSVR merge, reshape, LMM. Fixed 6 documents: project_specific_stats_insights.md, irt_methodology.md (+25 lines), lmm_methodology.md (+57 lines), data_structure.md (+3 lines), docs_index.md (4 entries), concept.md (6 edits). Tested with rq-spec agent invocation 3: agent successfully detected D070 from all updated docs, incorporated in 12 locations. Prevents measurement error that would have affected ~40 RQs. Critical fix for project validity.

### rq_spec_v3_agent_testing
**Description:** RQ-Specification Agent v3.0 Planning Mode testing (2025-11-14 evening). Tested agent three times on RQ 5.1 to validate stateful operation and incremental decision incorporation. Invocation 1 (baseline), Invocation 2 (after D069 added), Invocation 3 (after D070 added). Key findings: (1) Stateful operation verified - agent reads logs/rq_spec_context.md, preserves decisions across invocations, (2) Proactive documentation scanning verified - re-reads project_specific_stats_insights.md on every invocation, (3) Incremental adaptation verified - D068 → D068+D069 → D068+D069+D070, (4) Explicit verification added - agent creates evidence sections. Planning Mode validated for production. Drafting Mode and Finalization Mode NOT YET TESTED pending user approval.

### git_rollback_recovery_attempt
**Description:** Git forward recovery investigation after uncommitted code lost in rollback (2025-11-15). User discovered 6 functions (purify_items, calibrate_grm, post_hoc_contrasts, compute_effect_sizes, plot_trajectory_probability, fit_lmm_with_tsvr) were documented in state.md commit fe3a940 but never committed to git. Attempted recovery via git reflog, confirmed code irretrievably lost. Lesson learned: Critical work should be committed immediately, not just documented in context files. Led to complete re-implementation via TDD from requirements documentation.

### missing_functions_reimplementation_tdd
**Description:** Complete TDD re-implementation of 6 missing functions after git rollback recovery failure (2025-11-15). Re-implemented from requirements documentation: purify_items (D039, 102 lines, 4 GREEN tests), calibrate_grm (26 lines), post_hoc_contrasts (D068, 117 lines), compute_effect_sizes (86 lines), plot_trajectory_probability (D069, 112 lines), fit_lmm_with_tsvr (D070, 149 lines). Total: +592 lines production code, +155 lines test code. All imports verified, production-ready. Demonstrates TDD enables re-implementation from requirements alone with zero information loss.

### decision_d039_d068_d069_d070_implementation
**Description:** Complete implementation of 4 project-wide decisions via tool functions (2025-11-15). D039 (2-pass IRT purification via purify_items), D068 (dual reporting p-values via post_hoc_contrasts), D069 (dual-scale trajectory plots via plot_trajectory_probability), D070 (TSVR as LMM time variable via fit_lmm_with_tsvr). Ensures quality across all 50 RQs, prevents measurement error in ~40 trajectory RQs, enhances scientific rigor and accessibility. All functions production-ready with GREEN tests.

### import_bug_fixes
**Description:** Fixed missing List type hint imports causing NameError in tools/analysis_lmm.py and tools/plotting.py (2025-11-15). Functions used List type hint but missing import from typing module. Added List imports to both files. All 6 re-implemented functions now import cleanly with proper type hints. Minor bug caught during development, no production impact.

### fit_lmm_with_tsvr_tdd_implementation
**Description:** Implementation of fit_lmm_with_tsvr() function following TDD methodology for Decision D070 (2025-11-14 23:40). Complete IRT→LMM pipeline using TSVR (Time Since VR) instead of nominal days as time variable. Prevents systematic measurement error in ~40 trajectory RQs.

### analysis_script_bug_fixes
**Description:** Fixed multiple script issues during RQ 5.1 analysis execution (2025-11-14 23:40). Column naming mismatches, regex pattern errors, UTF-8 encoding issues. All bugs fixed, script running successfully.

### irt_pass1_execution_results
**Description:** Successful execution of IRT Pass 1 calibration for RQ 5.1 (2025-11-14 23:40). 60-minute runtime, generated pass1_theta.csv and pass1_item_params.csv outputs. Baseline performance established.

### analysis_script_resume_creation
**Description:** Created resume script to skip completed Pass 1 IRT calibration (2025-11-14 23:40). Loads Pass 1 outputs from CSV, saves ~60 minutes per test run. Ready for Steps 2-9 execution.

### onedrive_version_history_recovery
**Description:** Emergency recovery of v3.0 rq_specification agent using OneDrive version history (2025-11-15 01:40). CRITICAL SUCCESS - Recovered 1571-line agent after git reset HEAD~1 disaster. OneDrive auto-versioning saved 2+ days of work. Cloud storage is reliable last-resort backup.

### git_rollback_disaster_recovery
**Description:** Complete disaster recovery process after git reset HEAD~1 deleted uncommitted work (2025-11-15 01:40). Full recovery via OneDrive + git history. Prevention measures implemented (git add -A in /save, enhanced analysis-executor). Lessons learned documented.

### analysis_script_api_mismatch_fixes
**Description:** Fixed 6 API mismatches in analysis_script.py after background process errors (2025-11-15 01:40). Agent guessed parameters from config.yaml instead of tools_inventory.md. Corrected purify_items, fit_lmm_with_tsvr, post_hoc_contrasts, compute_effect_sizes calls plus variable names and UTF-8 encoding.

### analysis_executor_code_generation_rules
**Description:** Enhanced analysis_executor agent with 3 critical code generation rules (2025-11-15 01:40). Rule 1: UTF-8 encoding mandatory. Rule 2: Study tools_inventory.md before generating calls. Rule 3: Python unbuffered output for monitoring. Prevents future API mismatches. Committed ce7e1f2.

### save_command_enhancement_git_add_all
**Description:** Updated /save command to commit ALL modified files with git add -A (2025-11-15 01:40). Previously only committed .claude/context/, leaving agents/tools/tests vulnerable. Both "before" and "after" commits now save everything. Prevents lost work disasters. Committed 570fbbf.

### resume_script_creation
**Description:** Created analysis_script_resume_from_step2.py with all API fixes applied (2025-11-15 01:40). 1021-line script loads Pass 1 from CSV, runs Steps 2-9 with correct function signatures. Saves 60 minutes. Ready for overnight test.

### resume_script_config_structure_fix
**Description:** Resume script config loading mismatch resolution (2025-11-15 11:30). Fixed KeyError: 'dimension_patterns' by correcting config structure (item_mapping with tag_pattern/tag_patterns). Added missing irt_config building. Demonstrates API Documentation Ignorance pattern (Problem #6).

### resume_script_utf8_encoding_fix
**Description:** Unicode symbol replacement for Windows cp1252 compatibility (2025-11-15 11:30). Fixed UnicodeEncodeError by replacing checkmarks/emojis with ASCII equivalents. Demonstrates Platform Assumptions pattern (Problem #16). Added UTF-8 encoding rule to analysis_executor.

### purify_items_multivariate_implementation
**Description:** Rewrote purify_items() to handle both univariate and multivariate IRT formats (2025-11-15 11:30). Auto-detects format via 'Difficulty' column presence, normalizes multivariate to univariate by extracting primary dimension. All 4 tests GREEN. Production-validated on RQ 5.1 Step 2.

### rq51_step2_item_purification_results
**Description:** Step 2 item purification results for RQ 5.1 (2025-11-15 11:30). 43/102 items retained (42.2%) per Decision D039 thresholds (a ≥ 0.4, |b| ≤ 3.0). Majority excluded for extreme difficulty (temporal items). Purification successful, ready for Pass 2 calibration.

### rq51_step3_irt_pass2_in_progress
**Description:** Step 3 IRT Pass 2 calibration progress snapshot (2025-11-15 11:30). 43 purified items, ~25% complete (Epoch 350), ~30-minute estimated runtime. Background process 54966e running Steps 2-9 automatically. Historical snapshot - may be completed now.

### analysis_pipeline_problems_comprehensive_list
**Description:** Complete 24-problem documentation of automation pipeline failures (2025-11-15 17:00). Organized into 5 categories (API/Contract, Workflow/Process, Code Quality, Documentation/Tooling, Meta-Patterns) with 5 meta-patterns identified. Used context-finder to discover 19 additional problems beyond user's initial 5. Created comprehensive reference document (docs/user/analysis_pipeline_problems.md). v3.0 historical record, v4.X architecture designed to solve these problems.

### resume_script_v5_creation
**Description:** Step 5 resume script creation process (2025-11-15 17:00). Modified Step 2 resume script to skip Steps 1-4, load their outputs (theta_scores.csv, item_parameters.csv, purified_items.csv), resume from Step 5. Created to bypass Unicode arrow error. Executed 4 versions with sequential failures. v3.0 monolithic approach, demonstrates fragility of resume scripts vs v4.X atomic step design.

### cascading_api_errors_6_discovered
**Description:** Sequential discovery of 6 cascading API errors during resume script v5 testing (2025-11-15 17:00). Unicode arrow, missing composite_ID creation, test vs Test mismatch, tsvr composite_ID, tsvr vs TSVR_hours, wide vs long format. Demonstrates Pattern 2 (Cascading Failures) where single root error (API ignorance) triggers 5+ downstream failures. Each error only visible after fixing previous error. v3.0 runtime discovery vs v4.X validation gates.

### fit_lmm_with_tsvr_defensive_programming
**Description:** Defensive programming enhancements to fit_lmm_with_tsvr function (2025-11-15 17:00). Added test/Test auto-detection, conditional composite_ID creation, tsvr/TSVR_hours auto-detection (tools/analysis_lmm.py lines 903-917). Patches symptoms of API ignorance but doesn't solve root cause. v3.0 band-aid approach vs v4.X validation gates that eliminate need for defensive code.

### problem_documentation_schema
**Description:** Description/Cause/Effect schema established for systematic problem documentation (2025-11-15 17:00). Single-sentence format enforces clarity and conciseness. Applied to all 24 problems in comprehensive list. Schema benefits: enforces clarity, enables pattern recognition, facilitates communication, prevents solution bias, reusable methodology. Template archived for future problem documentation tasks.

### v4x_architecture_specification_creation
**Description:** Complete v4.X architecture specification build process (2025-11-15 18:45). Architecture debate and pivot from v3.0 defense to v4.X acceptance, 13 atomic agents replacing 7 monolithic agents, specification document creation (885 lines), system-wide v4.X announcements, design philosophy (atomic task-sniper agents), refinements (validation protocol, context dumps, scope boundaries). Superseded by VALIDATED and reorganized specification versions.

### v4x_ultrathink_validation_40_issues
**Description:** Ultrathink validation of v4.X specification identifying 40 issues with complete user resolutions (2025-11-15 18:45). Critical errors (step numbering, file extensions), circular references (agents reading own prompts), missing specifications (names.md, plan.md, plots.md, etc.), vagueness (master entity, invocation format), rule violations (code examples), conflicts (g_conflict design, context dumps), omissions (legacy archival, platform, git, error recovery). All 40 issues resolved and applied to specification.

### v3_to_v4x_transition_rationale
**Description:** Complete rationale for v3.0 to v4.X architecture transition (2025-11-15 18:45). Root cause analysis (context bloat causes hallucinations), v3.0 failures documented (0 RQs completed in execution phase), v4.X solution designed (13 atomic agents, lean context windows, pseudo-statefulness via status.yaml), migration strategy (13 phases, 52 tasks), evidence supporting transition, historical lessons preserved. Critical decision point explaining why complete architectural redesign necessary.

### v4x_specification_systematic_fixes_40_applied
**Description:** Applied all 40 systematic fixes to v4.X specification document (2025-11-15 19:30). Critical errors, template corrections, missing specifications, vagueness clarifications, rule compliance, conflicts resolved, omissions addressed. Document status changed from Draft to VALIDATED. Superseded by subsequent validation passes (10 more issues Session 01:00, 24 more issues Session 03:30).

### v4x_specification_reorganization_7_chapters
**Description:** Complete v4.X specification document reorganization (2025-11-15 19:30). Created 7-chapter structure with comprehensive TOC, numbered sections, status indicators, Quick Reference section. 1,700 lines organized into: Introduction, Agent Specifications, Workflow & Orchestration, Documentation Templates, Standards & Conventions, Technical Specifications, Quick Reference. Enables easy navigation during implementation.

### docs_index_v4x_entry
**Description:** Added comprehensive v4.X specification entry to docs_index.md (2025-11-15 19:30). Documented audience (ALL v4.X agents, main claude), status (VALIDATED), all 13 agent names, key concepts. Part of standard documentation procedure per CLAUDE.md.

### phase1_foundation_f1_f2_complete
**Description:** Phase 1 Foundation implementation (2025-11-16 01:00). Post-ultrathink inspection found 10 additional issues, user resolved with critical decisions (TDD approach, validation tools architecture), created todo.yaml roadmap (52 tasks, 13 phases), completed F1-F2 (folder structure + agent_best_practices.md). Superseded by F0a-F0b-F3 completion in Session 12:15.

### v4x_third_validation_24_issues_resolved
**Description:** Third comprehensive validation pass after 50 prior issues (2025-11-16 03:30). Ultrathink analysis found 24 issues (9 CRITICAL, 15 POTENTIAL), all resolved with systematic fixes. Created 10-step process with v3 leverage, reframed Phase 4 as migration not rebuild, established 100% coverage requirement. Specification implementation-ready.

### ten_step_process_v3_leverage
**Description:** Enhanced task execution process from 7 to 10 steps with explicit v3 architecture leverage (2025-11-16 03:30). Added context-finder v3 search, v3 file reading, ultrathink analysis. Philosophy: "Don't rebuild from scratch what already exists" - migrate/adapt v3 tools, enhance what needs improvement, build only gaps.

### comprehensive_todo_yaml_rewrite_50_tasks
**Description:** Complete todo.yaml rewrite establishing 50-task roadmap across 14 phases (2025-11-16 03:30). Added Phase 0 (names.md design), reframed Phase 4 (validation migration), granularized V2 into V2a-V2d, strengthened to 100% coverage, enhanced verifications. 10-step process documented, v3 leverage philosophy embedded.

### context_checkpoints_enhancement_working
**Description:** Enhanced 10-step process with context checkpoints between tasks (2025-11-16 12:15). User requested pause points for /context checks and save/clear/refresh decisions. Prevents token overflow, enables proactive token management, demonstrated success at 105k and 114k checkpoints. Active enhancement in use.

### v4x_phase2_templates_t1_t11_complete
**Description:** Complete Phase 2 template creation history (T1-T11, 9,551 lines, comprehensive scope). Documents progression from initial 10-step process establishment through all 11 template creations to 100% Phase 2 completion. Includes Phase 0 & F3 setup, Templates T1-T3 (setup/documentation), T4-T6 (core workflow), T7-T8 (dual validation), T9-T10 (validation checklist + plots), T11 (results summary). Comprehensive design decisions, user questions/answers, context-finder performance, lessons learned, and integration with v4.X architecture. Demonstrates consistent 10-step process application and user-driven design philosophy.

### v4x_phase3_thesis_files_migration
**Description:** Complete Phase 3 thesis files migration (H1-H3, 50 RQs moved to docs/v4/thesis/). Documents git mv operations preserving file history for ANALYSES_CH5.md (15 RQs, 79K), ANALYSES_CH6.md (15 RQs, 106K), and ANALYSES_CH7.md (20 RQs, 163K). Verification of RQ counts, integration with v4.X architecture for rq_concept agent access per spec 2.1.2 step 5. Completed in parallel with T11 demonstrating flexible phase boundaries and efficiency of simplified process for straightforward tasks.

### v4x_architecture_realignment_phase4_deleted
**Description:** Critical architecture realignment Sessions 01:30, 02:45, 12:00, 17:00 (2025-11-17). Phase 2 Templates T9-T10 complete (inspect_criteria 987 lines, plots 1,059 lines with D069 dual-scale requirements), Phase 3 H1-H3 thesis files migration (50 RQs to docs/v4/thesis/), Phase 4 V1 validation audit (766 lines, 14 v3 functions inventoried, migration plan 5-7 hours), and CRITICAL v3/v4 conflation correction. User identified fundamental misunderstandings: I am master orchestrator (not rq_builder), rq_concept GENERATES concept.md (not user writes), rq_tools DETECTS missing and FAILS (triggers TDD migration), tools emerge AS NEEDED during testing (NOT upfront). Complete todo.yaml restructure: Phase 4 DELETED, 32 phases total (4-16 build agents individually, 17-29 test agents individually with explicit tool migration sub-steps 4a-4e at phases 23 & 28), 11-step agent building process (Step 1 ONLY solution.md, Step 2 explain first), 6-step testing process. 10 CRITICAL lessons learned about v3/v4 boundaries, emergent TDD, and solution.md as ONLY ground truth.

### v4x_phase17_22_testing_and_quality_control
**Description:** Complete history of Phases 17-22 quality control infrastructure and testing (2025-11-21 through 2025-11-22). Phase 17: rq_builder (100% PASS, 56% bloat reduction). Phase 18: rq_concept (100% PASS, 29% bloat reduction, Step 8.5 enhancement). Phase 19: rq_scholar (100% PASS, 40% bloat reduction, 9.1/10 CONDITIONAL, standalone 1_scholar.md). Phase 20: rq_stats (100% PASS, 16% bloat reduction, 8.2/10 REJECTED, standalone 1_stats.md, agent more rigorous than predicted). Phase 20.5: 1_concept.md perfection (6 critical fixes from dual-agent validation feedback). Phase 21: rq_planner (100% PASS, 20% bloat reduction, 2_plan.md with 8 steps, validation workflow fix, Unicode encoding issue discovered/fixed). Phase 22: rq_tools (100% PASS, 14% bloat reduction, TDD detection validated, 37% phantom tool elimination, stdlib exemption added). Quality control infrastructure: chronology.md (800 lines), best practices split (universal.md + workflow.md + code.md, 20% context reduction), bloat audit methodology, g_conflict pre-flight checks, 11-step testing protocol. Demonstrates systematic quality control prevents cascading errors.

### phase18_rq_concept_complete_100_pass
**Description:** Phase 18 rq_concept agent testing complete (2025-11-20 22:30). Step 8.5 enhancement added (44 lines "Handling Incomplete Thesis Sections" with atomic agent philosophy - rq_concept reformats, downstream agents enhance). Agent execution EXCEEDED predictions: created comprehensive Theoretical Background (4 subsections, 17 lines) from minimal thesis hypothesis, synthesized from hypothesis + Decisions D039/D068/D069/D070 + Expected Outputs. Prediction accuracy 95%, zero runtime errors, zero spec violations, circuit breaker EXPECTATIONS ERROR validated. Created 1_concept.md (160 lines, 9.6KB) with 7 sections, updated status.yaml. Demonstrated intelligent inference beyond literal instructions (comprehensive not minimal), v4.X atomic agent philosophy working, quality control approach validated.

### v4x_validation_architecture_enhancement
**Description:** V4.X validation architecture redesign (2025-11-21 22:00). Decision D071 (Validation Report Separation): rq_scholar writes standalone 1_scholar.md, rq_stats writes standalone 1_stats.md instead of appending to 1_concept.md (prevents 20k token bloat, keeps concept.md lean ~5-7k for rq_planner). Decision D072 (Experimental Context Integration): both agents read thesis/methods.md Step 6 for study design constraints (N=100, 4 sessions, VR apparatus), grounds devil's advocate in reality not just theory. Decision D073 (Standalone File Approach): Write tool for standalone files vs Edit append (cleaner separation, easier version control). 13 files modified (2 agent prompts, solution.md, 2 templates, chronology.md, docs_index.md), workflow 10→11 steps, net 12-13k token savings in concept.md. Testing ready for Phases 19-20.

### tools_reality_audit_rq51
**Description:** Comprehensive 21-tool audit for RQ 5.1 execution readiness (2025-11-22 02:30). Invoked 3 parallel context-finder agents to audit IRT, LMM, plotting, and validation tools. Found 4 critical bugs: calibrate_irt() calling 4 non-existent functions (would crash immediately), compute_contrasts_pairwise() searching wrong column name (silent failure), prepare_lmm_input_from_theta() violating Decision D070 (using nominal days not TSVR), validate_lmm_residuals() KS test missing standardization. All critical bugs fixed in ~7 minutes. Tools remain ORANGE (flagged for development) until live RQ 5.1 testing validates them. 4-color tracking system (RED→ORANGE→YELLOW→GREEN) established. Created ch5rq1-tools-reality.tsv + summary.md. Demonstrates TDD approach: audit before execution prevents runtime failures.

### v4x_tools_infrastructure
**Description:** Complete tools naming v2.0 + three-tier documentation architecture (2025-11-22 22:00 & 23:45). Tools naming v2.0: Replaced 800-line verb/noun taxonomies with 8 formulaic patterns (CONVERT, LOAD, RESOLVE, SET, COMPUTE, FIT, PREPARE, COMPARE + 3 special cases), 44% reduction (800→445 lines). Systematically renamed 33/51 functions (65%) across all 5 tool modules with complete cross-reference updates (docstrings, examples, internal calls, exports). Created tools_convert.md conversion reference (old→new mappings). Three-tier architecture: tools_catalog.md (300 lines, 2k tokens, lightweight discovery for rq_planner), tools_inventory.md (767 lines, 20k tokens, detailed API specs for rq_tools), tool_audit.md (8,000+ lines, 200k tokens, comprehensive historical reference). QA/QC with g_conflict agent (3 conflicts found/fixed, 100% consistency). Context savings: 18k tokens (90% reduction) for rq_planner. Git commits: e17a63b (naming v2.0), 5715e84 (catalog), 955307d (rq_planner updated), 1ed3715 (QA/QC fixes). Benefits: self-documenting function names, predictable patterns, hierarchical structure (pipelines vs atomics), agent clarity.

### phase19_20_21_testing_quality_control
**Description:** Complete history of Phases 19-21 testing (rq_scholar 9.1/10 CONDITIONAL, rq_stats 8.2/10 REJECTED, 1_concept.md perfection with 6 critical fixes, rq_planner 100% PASS with Unicode encoding fixes). Phase 19: 40% bloat cleanup (419 lines), 6 conflicts resolved, standalone 1_scholar.md (458 lines). Phase 20: 16% bloat cleanup (310 lines), 7 conflicts resolved, standalone 1_stats.md (463 lines), agent exceeded predictions with MORE rigorous validation. Concept perfection session: addressed all validation feedback (recent VR citations, encoding quality alternative, Q3 local independence validation, purification rationale, LMM convergence strategy, comprehensive validation procedures & limitations section), 100% critical issue coverage. Phase 21: 20% bloat cleanup (591 lines), 4 conflicts resolved, validation workflow clarification (status="success" means "report created" not "concept approved"), 2_plan.md created (953 lines, 8 steps), comprehensive Unicode encoding fix (ASCII-only enforcement across all agent prompts and templates). Validation architecture working: standalone reports, experimental context integration, quality control preventing cascading errors.

### v4x_phase23_27_testing_complete
**Description:** Complete history of v4.X pipeline testing Phases 23-27 (2025-11-22 to 2025-11-23). Phase 23 rq_analysis (765-line 4_analysis.yaml), Phase 24 g_code (full 8-step IRT/LMM pipeline execution, compute_contrasts_pairwise fix, folder reorganization, g_code.md enhancements), Phase 26 rq_inspect (70% bloat reduction, 4-layer validation, step07 fixes), Phase 27 rq_plots (74% bloat reduction, 8 conflicts fixed, dual-scale trajectory plots generated). Key technical achievements: treatment coding fix for statsmodels, delta method for non-reference comparisons, test value mapping (1,2,3,4 to 0,1,3,6), folder discipline rules, Option B visualization architecture validated. All 8 pipeline steps executed and validated successfully.

### pipeline_stability
**Description:** v4.X pipeline stability documentation including RQ 5.2 execution (4 bug fixes, agent prompt enhancements), D0XX reference removal (2025-11-23), Phase 28 rq_results testing completion, and trajectory plot enhancement (continuous TSVR + publication style). Documents pipeline reaching stable state: 4 bugs fixed in RQ 5.2, zero bugs in RQ 5.3, 1 bug fix in RQ 5.4. Validates g_code.md REMEMVR Data Conventions and rq_analysis.md folder conventions.

### when_domain_anomalies
**Description:** Documentation of floor effects and item attrition in When (temporal) domain across RQ analyses. Includes RQ 5.1 floor effect (probability 6-9%, 20/26 items excluded), RQ 5.2 consolidation analysis anomalies (When appearing to show least forgetting may be floor artifact), and confirmation that RQ 5.3 paradigm analysis does NOT exhibit these anomalies (domain-specific, not paradigm-specific issue).

### rq53_paradigm_analysis
**Description:** Complete RQ 5.3 (Paradigm Differences: Free/Cued/Recognition) pipeline execution record (2025-11-24). Zero bugs encountered. IRT calibration (43/72 items retained), LMM results (logarithmic best model), post-hoc contrasts showing Recognition > (Cued = Free). Hypothesis PARTIALLY SUPPORTED - retrieval support gradient confirmed at extremes but not middle. Consistent with dual-process theory.

### rq55_schema_congruence_complete
**Description:** Complete RQ 5.5 (Schema Congruence Effects on Forgetting Trajectories) pipeline execution. First v4.X RQ with zero bugs encountered. IRT calibration (51/72 items retained), LMM results (logarithmic best model, AIC=2652.57), post-hoc contrasts ALL non-significant. Hypothesis NOT SUPPORTED - no differential forgetting by schema congruence level (Common/Congruent/Incongruent show parallel trajectories). Demonstrates pipeline stability (5th consecutive RQ).

### validated_irt_settings_complete
**Description:** Complete history of IRT settings correction crisis and resolution. Discovery of systematic error (mc_samples 1 vs 100, 100x difference), impact assessment (theta r=0.68-0.91, below r≥0.95 threshold), full RQ 5.1-5.5 rerun with validated "Med" settings from ANALYSES_DEFINITIVE.md, comprehensive impact analysis showing 46% residual variance reduction and AIC improvement of 665 points. Scientific robustness confirmed - same models selected, same significance patterns, effect magnitudes adjusted 2-24%. Publication quality achieved. Includes user Q&A on item purification necessity and GPU cluster optimization decisions.

### rq57_complete_pipeline
**Description:** RQ 5.7 ALL 11 PHASES COMPLETE - Steps 1-5 executed with 9 bugs fixed, Steps 6-7 skipped due to pickle issues, rq_inspect validated outputs, rq_plots manual plot, rq_results summary.md with 3 anomalies. Best model: Logarithmic AIC=873.7 weight=0.48. Includes RQ 5.1-5.6 summary regeneration, minimal settings testing validation, g_code API ignorance pattern documentation.

### ch5_rq8_15_concept_validation
**Description:** Complete history of RQ 5.8-5.15 concept generation, dual-agent validation (rq_scholar + rq_stats), iterative enhancement cycles, and acceptance of 9.1/10 CONDITIONAL publication-quality standard. Includes RQ 5.7 completion, agent prompt enhancements, first validation cycle (4 APPROVED, 2 CONDITIONAL, 2 REJECTED), final enhancement cycle achieving 6 APPROVED and 2 CONDITIONAL (9.1/10). Documents validation iteration dynamics and transition to pipeline execution phase.

### ch5_rq8_15_pipeline_planning
**Description:** RQ 5.8-5.15 pipeline execution preparation via rq_planner (8/8 successful plans) and TDD tool detection via rq_tools (7/8 failures expected). Includes execution order constraints (4 tiers), cross-RQ dependencies identified, 26 missing tools catalogued across 3 categories (LMM validation, specialized analysis, clustering). Created tools_status.tsv tracking system (21 GREEN production-validated, 25 ORANGE flagged, 28 RED legacy) and tools_todo.yaml development roadmap (25 tools, 3 priority levels, 24-33 hour estimate). Documents TDD detection working as designed and strategic options for tool development vs RQ execution.

### phase1_critical_path_complete
**Description:** Phase 1 Critical Path TDD tool development complete (4/4 HIGH priority tools, 50/50 tests GREEN, 1,590 lines code, 3 hours execution). Tool 1 check_file_exists (10 GREEN, 15min), Tool 2 validate_lmm_assumptions_comprehensive (14 GREEN, 90min, 7 comprehensive diagnostics with plots/CSVs), Tool 3 compute_cronbachs_alpha (13 GREEN, 45min, creates NEW MODULE tools/analysis_ctt.py with bootstrap CIs), Tool 4 compare_correlations_dependent (13 GREEN, 30min, Steiger's z-test). Unblocks 4/8 RQs (5.8, 5.11, 5.12, 5.15 = 50%). Validates TDD methodology benefits and 9-step workflow effectiveness. Documents legacy code integration strategies and module creation principles.

### phase2_tools_5_6_7_complete
**Description:** Phase 2 TDD tool development continuation (Tools 5-7 COMPLETE, velocity acceleration 120min→45min→30min via workflow mastery). Tool 5 select_lmm_random_structure_via_lrt (12/15 GREEN with 3 skipped for statsmodels limitations, REML=False decision approved, v1 pragmatic simplification Uncorrelated=Full documented). Tool 6 prepare_age_effects_plot_data (15/15 GREEN, 45min, pd.qcut tertiles with 95% CIs). Tool 7 compute_icc_from_variance_components (14/14 GREEN, 30min, 3 ICC estimates with interpretation). Total progress 7/25 tools (28%), demonstrates TDD velocity gains and simplified workflow effectiveness.

### phase2_tools_8_through_17_complete
**Description:** TDD tool development continuation - Tools 8-17 COMPLETE (68% total progress). Session 00:15 (Tools 8-12, Phase 2 complete, D068 validator suite COMPLETE 4/4, 57/57 tests GREEN). Session 01:00 (Tools 13-17, 53/53 tests GREEN, batch documentation validated). Velocity mastery sustained at 10 min/tool for LOW complexity validators (9 consecutive tools). 100% test pass rate maintained across all implementations. Documents TDD workflow mastery, batch documentation efficiency, validator design patterns, and perfect velocity prediction accuracy for complexity tiers. Strategic assessment estimates ~10.5 hours and 4 sessions remaining for 18 tools.

### tools_18_25_implementation_complete
**Description:** Phase 3 TDD tool development COMPLETION - Tools 18-25 ALL COMPLETE achieving 100% tools_todo.yaml completion (25/25 tools, 247/250 tests GREEN). Sustained 10 min/tool velocity for all 8 LOW complexity validators (validate_standardization, validate_variance_positivity, validate_icc_bounds, validate_dataframe_structure, validate_plot_data_completeness, validate_cluster_assignment, validate_bootstrap_stability, validate_cluster_summary_stats). Perfect test pass rate 54/54 GREEN in session. 100% implementation milestone reached, documentation pending at session end. Superseded by Session 02:00 documentation completion.

### tool_26_extract_segment_slopes_complete_rq_tools_investigation
**Description:** Tool 26 extract_segment_slopes_from_lmm implementation complete (11/11 tests GREEN, delta method SE propagation for slope ratios). Unblocked RQ 5.8 execution. Investigation revealed rq_tools circuit breaker violation (agents invented ~20 function names instead of failing generically).

### documentation_sync_complete_90_percent_coverage
**Description:** Documentation gap fixes via g_conflict analysis. 22 undocumented functions added to tools_inventory.md, 3 CRITICAL bugs fixed (duplicate function, module mismatches). Documentation coverage improved from 57% → 90%. Root cause: documentation gap, not code gap.

### rq_5_8_through_5_13_conflict_detection_resolution
**Description:** Initial conflict detection pipeline for RQs 5.8-5.13. 5 g_conflict agents identified 50 conflicts total. RQ 5.10 fully fixed (8/8 conflicts resolved). Comprehensive fix documentation created. Remaining 5 RQs had 42 conflicts documented.

### rq_5_8_through_5_13_critical_conflicts_resolved_verification_complete
**Description:** CRITICAL conflict resolution achieving 67% readiness (4/6 RQs). 18 CRITICAL conflicts fixed across 5 RQs (15 files modified). Parallel g_conflict verification identified 4 RQs CLEAN (5.9, 5.10, 5.11, 5.13) with RQ 5.8 and 5.12 needing additional fixes.

### rq_5_8_through_5_13_100_percent_ready_all_conflicts_resolved
**Description:** Final conflict resolution achieving 100% readiness (6/6 RQs) for g_code execution. RQ 5.8 had 7 fixes (4 CRITICAL, 3 HIGH) including early_cutoff_hours default, segment boundary specification, RQ 5.7 convergence validation, exact Bonferroni alpha (0.003333). RQ 5.12 investigation revealed NOT BLOCKED (filenames already correct, 1 typo fixed). All fixes verified via parallel g_conflict agents.

### rq_5_8_g_code_execution_complete_5_of_7_steps_successful
**Description:** First v4.X g_code production execution on RQ 5.8. Parallel code generation (9 agents, 7 steps, ~15 minutes). Sequential debugging (5/7 steps successful, 2 tool bugs). 3 bugs fixed in generated code (file references, API mismatches, DataFrame.data). 2 tool bugs documented (get_influence(), categorical coefficient naming). Core scientific finding obtained: deltaAIC = +5.03 favors continuous model (evidence AGAINST two-phase forgetting). YELLOW status tools revealed bugs on first production use. Superseded by Session 17:00 publication-ready completion.

### rq_5_8_complete_publication_ready_all_bugs_fixed
**Description:** Complete history of RQ 5.8 execution achieving publication-ready quality (Session 2025-11-28 17:00). Fixed 5 bugs total (2 tool bugs: validate_lmm_assumptions_comprehensive get_influence() → studentized residuals, extract_segment_slopes_from_lmm coefficient auto-detection; 3 g_code bugs: unit conversion, convergence fallback, CI calculation). Re-ran full analysis pipeline, achieved 100% validation PASS (rq_inspect 4-layer), generated publication-quality plots (300 DPI), created comprehensive summary with 3 anomalies transparently flagged. Scientific finding: Nuanced two-phase pattern exists but mechanism is gradual (not sharp 48h inflection). Both tools production-validated (YELLOW → GREEN). v4.X workflow completely validated end-to-end. Total efficiency: 45 minutes thesis-quality completion.

### rq_5_9_complete_end_to_end_pipeline_null_results_scientifically_valid
**Description:** Complete history of RQ 5.9 execution with scientifically valid null result (Session 2025-11-28 20:00). Full workflow: parallel g_code (6 agents, 15 minutes, 1,988 lines) → g_conflict pre-execution (5 conflicts, 4 fixed) → sequential debugging (7 bugs, 30 minutes) → rq_inspect (conditional pass, 4 anomalies) → rq_plots (300 DPI) → rq_results (comprehensive summary). First RQ after RQ 5.8 tool fixes, testing production-validated tools. Scientific finding: No significant age effects on forgetting (null result, p > 0.18, contradicts dual deficit hypothesis). Most likely explanation: practice effects from 4 repeated tests. Tool improvements made (case-insensitive age, optional domain_name). Total bugs fixed: 12 (4 pre-execution + 7 execution + 1 plotting). Total efficiency: 54 minutes end-to-end. Demonstrates null results + transparent anomaly documentation = PhD-quality scientific reporting.

### rq_5_10_complete_null_result_new_tool_tdd
**Description:** Complete execution history of RQ 5.10 (Age × Domain × Time Interaction Analysis). Parallel g_code generation (8 agents, 5 successful, 3 circuit breakers), step-by-step debugging (steps 00-02), new tool development via full TDD workflow (extract_marginal_age_slopes_by_domain, 15/15 tests GREEN, 203 lines, delta method SE propagation), remaining steps execution (02b-05), full validation pipeline (rq_inspect, rq_plots, rq_results). Scientific finding: NULL RESULT - Age effects on forgetting do NOT vary by domain (all interactions p > 0.68). Hypothesis NOT SUPPORTED (hippocampal aging theory). Scientifically valid with 3 plausible explanations: VR unified encoding, insufficient power, age range too narrow. Total bugs fixed: 21 (11 in session 20:30, 10 in session 17:30). Production-validated tools accumulated. Demonstrates TDD workflow success with real data.

### rq_5_11_complete_publication_ready_critical_fixes_applied
**Description:** Complete execution history of RQ 5.11 (IRT-CTT Convergent Validity Comparison). Circuit breaker validation (g_conflict + g_code), dichotomization critical fix (1=1, <1=0 for methodological validity), step-by-step execution (steps 00-07, 8 bugs fixed), full validation. Scientific finding: Strong convergent validity (r > 0.90 all domains), perfect significance agreement (kappa=1.0), expected coefficient discrepancies (IRT 8x more sensitive than CTT for log_TSVR). Methodology validated: dichotomization ensures fair comparison, circuit breakers prevent runtime errors, production workflow working. User domain expertise critical for catching conceptual errors.

### rq_5_12_planning_schema_verification_hallucination_corrected
**Description:** RQ 5.12 planning phase (2025-11-30). Initial 4_analysis.yaml verification found 5 CRITICAL schema errors (dimension→factor, theta_common/congruent/incongruent→theta_what/where/when). g_conflict investigation discovered rq_planner hallucinated false schema congruence framework (common/congruent/incongruent) not present in actual RQ 5.1 outputs. User deleted poisoned documents (2_plan, 3_tools, 4_analysis). Regenerated 2_plan.md with explicit verification instructions ("verify actual RQ 5.1 output files"). New plan 100% accurate with correct schema. Prevented catastrophic execution failures (would have failed step00 immediately). Time savings: 45 minutes verification vs 2-3 hours debugging (4-6× ROI). Lesson: LLMs need explicit empirical grounding instructions.

### rq_5_12_workflow_execution_tools_analysis_conflict_fixes
**Description:** RQ 5.12 workflow execution (2025-11-30 12:30). Executed rq_tools (4 analysis + 10 validation tools, zero missing). rq_analysis circuit breaker caught 9 folder convention violations (CSV/TXT files in results/ instead of data/), all fixed in 2_plan.md. g_conflict validation found 12 conflicts (3 CRITICAL, 5 HIGH, 3 MODERATE, 1 LOW) across 347 entities and 628 cross-checks. Fixed 3_tools.yaml file path violations. Investigated fit_lmm_trajectory_tsvr signature mismatch discovering function incompatibility with parallel LMM design. Implemented detailed loop specification in 4_analysis.yaml Step 7 (unmerge TSVR, loop 3 times renaming z_column→'theta', stitch outputs). All planning documents validated and conflict-free. Prevented 10 execution-blocking errors. Total efficiency 95 minutes.

### rq_5_12_complete_execution_steps_0_8_paradox_discovered
**Description:** RQ 5.12 analysis execution complete (2025-11-30 01:00). All 9 steps (0-8) executed with comprehensive statistical validation. Fixed 6 bugs (status schema, column_types tuples, item count, test column, 2x formula variables). Generated 9 Python scripts, 19 data files, 9 logs, 2 plot CSVs. CRITICAL FINDINGS: (1) Hypothesis 1 PARTIALLY SUPPORTED - Purified CTT significantly improves correlation with IRT in What/Where (p<0.001), When shows massive improvement (r: 0.45→0.84) but fails Bonferroni (underpowered, 5 items). (2) Hypothesis 2 REJECTED - SHOCKING REVERSAL: Full CTT BEST model fit (AIC=2954), IRT middle (3007), Purified CTT WORST (3108). PARADOX DISCOVERED: Purified CTT has better convergent validity (higher r) BUT worse predictive validity (worse trajectory fit). When domain 81% attrition (26→5 items), purified set too homogeneous, full set captures more forgetting variance. Item count > item quality for trajectory modeling. Publication-quality with dual p-values (D068), bootstrap CIs. PhD contributions: theoretical paradox, methodological comparison, practical recommendations. Total 98 minutes.

### rq_5_12_validation_complete_publication_ready_3_anomalies
**Description:** RQ 5.12 validation pipeline complete (2025-11-30 13:50). Executed rq_inspect (100% PASS, 4-layer validation, all 18 data + 9 logs validated). rq_plots generated 2 publication-quality plots (300 DPI) using manual script after circuit breaker detected missing functions. rq_results performed 6 scientific plausibility checks and flagged 3 anomalies: (1) CRITICAL - When domain catastrophic item loss (5/26 retained, 19.2%, uninterpretable results, HIGH priority diagnostic), (2) Paradoxical LMM fit (Full CTT best AIC=2954 contradicts theory, domain imbalance artifact hypothesis, MEDIUM priority domain-specific re-analysis), (3) Hypothesis partial support (What/Where significant, When massive effect Δr=+0.388 but p=0.111 Bonferroni failure, MEDIUM priority sensitivity analysis). Generated comprehensive summary.md (~30KB) with transparent anomaly documentation. Total validation 8 minutes. Overall RQ 5.12 timeline 3.3 hours (planning 95min + execution 98min + validation 8min). Publication-ready with complete transparency about measurement limitations.

### rq_5_13_step01_complete_specification_fixed_statsmodels_workaround
**Description:** RQ 5.13 Step01 complete (2025-11-30 13:30). g_conflict found 7 specification conflicts (3 CRITICAL, 3 HIGH, 1 MODERATE), all fixed in 4 documents. Updated to use actual RQ 5.7 output file names (lmm_Log.pkl, step03_theta_scores.csv, step04_lmm_input.csv) not hypothetical names. Generated step01 code via g_code, encountered NEW statsmodels/patsy pickle error (f_locals None during formula re-evaluation, not seen in RQ 5.12 loading same model). Implemented monkey-patch workaround (custom __setstate__ bypasses patsy formula, safe for variance extraction). Successfully loaded RQ 5.7 Logarithmic LMM model (100 participants, 400 observations, converged, random intercepts+slopes). Statistical validity confirmed via validate_model_convergence (PASS). Total session 48 minutes. 11 issues resolved. ROI 8-12× (15 min validation prevented 2-3 hours debugging). SUPERSEDED by full Steps 01-05 RE-RUN with Lin+Log model (Session 2025-11-30 15:10).

### rq_5_13_complete_rerun_linlog_model_validation_pipeline
**Description:** Complete execution history of RQ 5.13 (Between-Person Variance in Forgetting Rates) with model switch from singular Log model to non-singular Lin+Log model (2025-11-30 15:10). Includes root cause investigation of Log model singular covariance matrix (statsmodels warning, slope var = 9.07e-08 despite raw data SD = 0.396), comparison of all 5 RQ 5.7 models (Log/Quadratic singular, Linear/Lin+Log/Quad+Log non-singular), model selection decision (ΔAIC = 0.8, statistically equivalent, Burnham & Anderson threshold), full Steps 01-05 re-execution with Lin+Log model (1,729× increase in slope variance, ICC_slope 0.05% vs 0.00003%, correlation r = -0.973 vs -1.000), and comprehensive validation pipeline (rq_inspect 100% PASS, rq_plots 2 diagnostic plots, rq_results comprehensive summary). Hypothesis REJECTED (ICC_slope = 0.05% << 0.40 threshold). Scientific finding: Forgetting rate is STATE-DEPENDENT (situational) not TRAIT-LIKE (stable), contradicts literature. Three residual anomalies documented (slope variance 3,000× smaller than intercept, r = -0.973 still 2-5× higher than literature norms, random slope SD only 2.1% of population mean). Publication-ready with transparent model selection documentation. Total 55 minutes (investigation 15min, model switch 5min, re-execution 25min, validation 10min). 23 files modified. Documents singular covariance matrix as model failure not biology, ΔAIC < 2 equivalence criterion, model choice impacts on scientific conclusions, and thesis transparency requirements.

### chapter_5_reorganization_hierarchical_numbering_implemented
**Description:** Complete history of Chapter 5 RQ reorganization implementing hierarchical 5.X.X numbering system to address When domain floor effects and create logical categorical structure (2025-11-30 19:20). Comprehensive audit of RQs 5.1-5.13 via 13 parallel context_finder agents identified When domain floor effects (6-9% probability, 77% attrition, cascading effects). Designed 4-type structure: General (5.1.x, 6 RQs), Domains (5.2.x, 8 RQs), Paradigms (5.3.x, 9 RQs), Congruence (5.4.x, 8 RQs) = 31 total RQs. Created rq_refactor.tsv tracking table. Created 31 hierarchical folders, migrated 15 existing RQs (710 files), 16 TODO RQs ready for creation. Updated rq_builder agent and 4 template files (build_folder, concept, plan, plots) with hierarchical path format (chX/Y.Z.W). Organizational benefits: clear conceptual grouping, When handled elegantly (present in General, absent from Domains), consistent analytical treatment, easy cross-type comparisons. Migration preserves rollback safety via git. TODO RQs can reuse 80% of code via factor swaps. Total 135 minutes. v4.X architecture validated by audit (100% validation success, bugs decreasing, null results scientifically valid).

### chapter_5_infrastructure_todo_folders_asbuilt_documentation_conflict_detection
**Description:** Complete history of Chapter 5 infrastructure work including parallel rq_builder execution for 16 TODO RQ folders (Type 1: 2 RQs, Type 2: 3 RQs, Type 3: 7 RQs, Type 4: 6 RQs, all with 6 subfolders + status.yaml initialization, 2 minutes total), as-built documentation generation via 13 parallel context_finder agents FORBIDDEN from reading original plan (extracted from actual RQ folders only, 498 lines, standardized template, source citations, 10 minutes), and comprehensive g_conflict comparison identifying 47 discrepancies between planned (ANALYSES_CH5.md, 1426 lines) vs actual (ANALYSES_CH5_actual.md, 498 lines): 8 CRITICAL, 21 HIGH, 14 MODERATE, 4 LOW severity. Most conflicts are DOCUMENTATION GAPS not analysis errors.

### rq_refactor_tsv_extended_6_columns_comprehensive_specification_database
**Description:** Complete history of extending rq_refactor.tsv from 5 columns to 11 columns by adding Title, Hypothesis, Data_Required, Analysis_Specification, Expected_Output, and Success_Criteria. Includes parallel specification extraction from 13 completed RQs via context_finder agents (exact file names, variable names, thresholds from actual documentation), TODO RQ pattern mapping for 16 RQs based on analogous completed RQs (80% code reuse via factor swaps), and path migration from legacy rqN to hierarchical 5.X.X format. Final: 31 RQs × 11 columns = comprehensive specification database ready for rq_concept agent consumption.

### rq_audit_agent_creation_parallel_audit_13_completed_rqs
**Description:** Complete history of rq_audit agent creation and parallel audit execution (Session 2025-12-01 10:30). Created new rq_audit agent (.claude/agents/rq_audit.md) with 6-layer validation (Path References, Numbering Consistency, Data Sources, Documentation Consistency, Step Completeness, Naming Conventions). Performed manual audit of RQ 5.1.1 identifying 6 issues (2 CRITICAL, 3 HIGH, 1 MODERATE). Root cause: hierarchical numbering refactor (rqN→5.X.X) updated folder names but not code/doc path references. Ran parallel audits on all 13 completed RQs in ~3 minutes. Aggregate results: 85 total issues (25 CRITICAL blocking execution, 27 HIGH, 23 MODERATE, 10 LOW). All fixes are string replacements. Created audit.md reports for each RQ.

### rq_fixer_agent_creation_parallel_fixes_15_rqs_chain_map
**Description:** Complete history of rq_fixer agent creation and parallel execution resolving 85 audit issues across 15 RQs (Session 2025-12-01 11:30). Manual fixes for RQ 5.1.1 (11 files, 2 CRITICAL + 3 HIGH + 1 MODERATE path references and RQ ID consistency). Created rq_fixer agent (.claude/agents/rq_fixer.md) with 8-step workflow, mapping table for 13 RQs (rqN→5.X.X), and Haiku model for speed. Parallel execution on 14 remaining RQs (~76 issues fixed in 5 minutes, all RQs READY). Created comprehensive data dependency chain map (results/ch5/chain.md, 250+ lines) documenting cross-type dependencies: 5.1.1/5.1.6 depend on 5.2.1, 5.3.1/5.4.1 ambiguous. Target architecture: each type (General/Domains/Paradigms/Congruence) independently extracts from dfData.csv. Migration debt fully resolved (85→0 issues).

### cross_type_dependency_resolution_step0_creation_documentation_update
**Description:** Complete resolution of cross-type dependencies via Step 0 creation for root RQs (Session 2025-12-01 14:00). Created new step00_extract_data.py for 5.1.1 (General ROOT, ~300 lines, omnibus "All" factor Q-matrix). Rewrote step00 scripts for 5.3.1 (Paradigms ROOT, ~345 lines, free_recall/cued_recall/recognition factors) and 5.4.1 (Congruence ROOT, ~360 lines, common/congruent/incongruent factors). All 4 root RQs now extract independently from dfData.csv with type-specific Q-matrices. Updated 3 downstream code paths in 5.1.1 to use local outputs. Updated chain.md marking dependencies RESOLVED. Updated 3 concept.md files changing Data Source from DERIVED to RAW. Clean architecture achieved: cross-type dependencies 0, root RQs extracting raw 4/4, each type fully independent.

### agent_framework_v5_update_hierarchical_numbering_rq_concept_mass_execution
**Description:** Complete history of Agent Framework v5.0 update implementing chX/X.Y.Z hierarchical numbering format and rq_refactor.tsv as authoritative specification source. Updated 4 RQ workflow agents (rq_concept major rewrite with TSV column mapping, rq_planner, rq_scholar, rq_stats). Updated templates and workflow documentation. Mass execution via rq_concept on 16 TODO RQs (all SUCCESS). ANALYSES_CH5.md deprecated. 52-minute total session with 113k token consumption. Parallel execution efficiency demonstrated (15 agents in 5 minutes). Session 2025-12-01 16:30.

### validation_mass_execution_32_agents_stats_scholar_guide_3_rq_fixes
**Description:** Mass validation execution (16 TODO RQs × 2 agents = 32 parallel agents with Haiku model), comprehensive stats_scholar.md guide creation with 6 common fix templates and priority order, and 3 RQ fixes (5.2.6, 5.2.7 was REJECTED, 5.2.8) achieving publication-quality validation scores. Documents dual-agent validation results (13 scholar APPROVED, 2 stats APPROVED, 1 fully ready RQ 5.3.9), common methodological issues (LMM convergence, assumption validation, practice effects, GLMM for binary responses, K-means justification, cluster validation), and reusable fix patterns applied.

### fix_13_rqs_revalidate_all_16_approved
**Description:** Complete history of fixing remaining 13 RQs (5.3.3-5.3.8, 5.4.3-5.4.8) using stats_scholar.md templates and re-validating all CONDITIONAL RQs with 14 parallel agents (3 rq_scholar + 11 rq_stats). All 16 TODO RQs achieved APPROVED threshold (≥9.25) with average score improvements of +0.5 to +0.9 points. Documents 6 common fix templates (LMM convergence strategy, assumption validation, practice effects, GLMM for binary responses, K-means justification, cluster validation metrics), comprehensive fixes applied across paradigms and congruence types, final status table, files modified, and publication-quality standard achievement.

### rq_status_creation_root_validation_pipeline_analysis
**Description:** Root RQ pipeline analysis, rq_status.tsv creation, and When domain floor effect documentation (2025-12-02 16:30). Identified 8 unique analysis pipeline types covering 30 of 31 RQs (only 5.3.2 unique to Paradigms). Updated all 4 root RQ step00 scripts to use local step00_input_data.csv for data isolation. Comprehensive validity analysis via context_finder discovered When domain floor effect (6-9% accuracy, 77% item attrition) invalidating 5.2.X downstream analyses unless What/Where only. Created accurate rq_status.tsv tracking file (32 rows, 13 COMPLETE, 16 Partial, 2 NOT STARTED) with critical notes column documenting When exclusion requirements, clustering variable counts, and investigation priorities.

### rq_5.1.5_5.1.6_concept_validation_folder_alignment
**Description:** RQ 5.1.5 and 5.1.6 concept creation, dual-agent validation, critical fixes, and v4.2 folder structure alignment (2025-12-02 17:30). Created RQ 5.1.5 (K-means clustering) with bootstrap stability and silhouette validation (rq_scholar 9.5, rq_stats 9.3 APPROVED). Created RQ 5.1.6 (Item Difficulty) with critical LMM→binomial GLMM fix for binary responses, convergence fallback strategy, and GLMM diagnostics (score improvement +3.1, rq_scholar 9.3, rq_stats 9.4 APPROVED). Updated folder structure documentation (names.md v4.1, plan.md v4.2, rq_planner v5.1.0): all analysis outputs to data/, logs/ for .log files only, plots/results empty until final agents. Files modified: 2 concept files, 2 status files, 3 documentation files. Session efficiency: 53 minutes total.

### rq_5.3.3_complete_execution_piecewise_lmm_consolidation
**Description:** Complete RQ 5.3.3 execution (Piecewise LMM Paradigm Consolidation Window Analysis, 2025-12-02 20:45). 7 steps executed (load theta, assign segments, fit LMM, extract slopes, contrasts, consolidation benefit, plot data). Fixed 3 bugs (validation key mismatch, variance component NaN handling, SE column specification). Created new tool plot_piecewise_trajectory() in tools/plotting.py (lines 844-1005, dual-scale 2×2 layout, D069 compliant). Results: Early steeper forgetting than Late all paradigms, consolidation benefit ranking ICR > IFR > IRE contradicts hypothesis but non-significant (0/6 contrasts p_bonf > 0.16). Validated via rq_inspect (4 layers pass), rq_plots (piecewise_trajectory.png 592KB), rq_results (summary.md 46KB, 1 anomaly flagged). Publication-ready with comprehensive statistical validation. Files: 7 code, 11 data, 7 logs, 1 plot, 1 summary. Session metrics: 110k tokens, 3 bugs fixed.

### rq_mass_parallel_execution_planner_tools_analysis
**Description:** Mass parallel execution of rq_planner, rq_tools, and rq_analysis agents across 18 RQs (Session 2025-12-02 18:30). Agent path format updates to hierarchical chX/X.Y.Z structure (rq_tools v4.3.0, rq_analysis v4.1.0). rq_planner 18/18 SUCCESS (31 RQs now have 2_plan.md), rq_tools 14/18 SUCCESS (4 BLOCKED by missing GLMM/CTT tools), rq_analysis 14/14 SUCCESS (27 RQs now have 4_analysis.yaml). TDD detection workflow validated: 4 RQs blocked (5.1.6, 5.2.8, 5.3.5, 5.4.4), 14 RQs ready for g_code. Parallel execution efficiency: 12 minutes total vs 3+ hours sequential (12× speedup). Updated rq_status.tsv tracking. Files modified: 2 agents, 1 status, 18 plans, 14 tools, 14 analysis recipes.

### rq_5.1.5_complete_execution_kmeans_clustering
**Description:** Complete RQ 5.1.5 K-means clustering execution (Session 2025-12-02 19:30). 8-step analysis pipeline (load random effects, standardize, test K, fit, bootstrap stability, silhouette, characterize, plot data). Fixed 5 bugs (BIC boundary elbow fallback, 3 validation signature mismatches, plots import path). Results: K=2 clusters (69%/31%), Jaccard=0.929 stable, silhouette=0.594 reasonable structure. Two memory profiles identified (Resilient vs Improving). Validated via full pipeline (rq_inspect 4-layer pass, rq_plots cluster_scatter.png 283KB, rq_results summary.md 34KB 0 anomalies). Added scikit-learn to Poetry. First clustering RQ fully executed end-to-end. Publication-ready.

### rq_5.3.4_complete_execution_age_paradigm_interaction
**Description:** Complete RQ 5.3.4 execution (Age × Paradigm × Time 3-way interaction LMM, Session 2025-12-02 21:45). 6 steps executed (load theta, merge TSVR, fit LMM, extract interactions, age effects, plot tertiles). Fixed 6 bugs (dfData dedup, TSVR validation, pickle/patsy CSV workaround, direct computation, spec updates, plots import). NULL FINDING: No significant 3-way interactions (all p > 0.7), age effects uniform across IFR/ICR/IRE paradigms, challenges retrieval support hypothesis in VR. Validated via rq_inspect (4 layers pass), rq_plots (age_paradigm_trajectories.png 408KB), rq_results (summary.md 53KB, 0 anomalies). Publication-ready. Documents statsmodels pickle/patsy limitation and specification drift patterns.

### rq_5.4.3_complete_execution_age_schema_congruence
**Description:** Complete RQ 5.4.3 execution (Age × Schema Congruence × Time 3-way interaction LMM, Session 2025-12-02 22:20). 6 steps executed (load dependencies, prepare LMM input, fit 3-way LMM, extract interactions, age effects + Tukey, plot data by tertiles). Fixed 2 bugs (fixed effects extraction alignment, n_groups attribute). NULL FINDING: No significant 3-way interactions (all p_bonferroni > 0.025), age effects similar across Common/Congruent/Incongruent conditions, challenges schema compensation hypothesis in VR episodic memory. Validated via rq_inspect (4 layers pass, D068/D070 compliance), rq_plots (age_congruence_trajectories.png 724KB, 3-panel), rq_results (summary.md 31KB, 0 anomalies). Publication-ready. Consistent null pattern with RQ 5.3.4.

### rq_5.2.2_partial_execution_when_exclusion_consolidation
**Description:** Complete RQ 5.2.2 execution (Domain-Specific Consolidation Effects with When Domain Exclusion, Sessions 2025-12-02 23:15 and 2025-12-03 00:15). 6 steps executed (prepare piecewise input, fit piecewise LMM, extract slopes, compute contrasts, consolidation benefit, plot data). Fixed 4 bugs in partial session (data source correction, test numbering, When filter, slope reduction). When domain excluded due to floor effect (6-9% probability, 77% item attrition). Statistical results: Strong consolidation effect (~6× slope reduction Early→Late) but NO domain-specific consolidation (What ≈ Where, all contrasts p > 0.68). Hypothesis NOT SUPPORTED. Validated via full pipeline (rq_inspect, rq_plots regenerated for 2 domains, rq_results). Publication-ready with When exclusion documented.

### random_slope_correction_log_tsvr
**Description:** Critical model correction fixing random slope specification across 3 RQs (5.2.4, 5.3.4, 5.4.3) from TSVR_hours to log_TSVR per ROOT RQ model selection. Revealed IRT var=0.021 vs CTT var=0.000 (IRT detects individual differences, CTT cannot). Documents silent model specification errors, methodological lesson that random slopes must align with fixed effects time transformation, and IRT vs CTT dynamic divergence as key thesis finding (Session 2025-12-03 06:00).

### chapter_5_story_narrative_assessment
**Description:** Comprehensive Chapter 5 story draft creation with good/bad/ugly framework, extended literature search of 15+ VR memory studies, critical insight about theta scale artifact hypothesis (no VR study uses IRT theta for trajectories), investigation plan for theta→probability conversion via Test Characteristic Curve, and correction that REMEMVR uses Oculus Pro HMD not desktop VR (Session 2025-12-03 09:15).

### icc_slope_deep_investigation_complete
**Description:** Complete 6-hypothesis investigation explaining ICC_slope = 0.0005 anomaly. Scale transformation gave 3.5× improvement (not primary cause), model specification 22× improvement (partial), shrinkage 93% from sparse design (KEY FINDING), LR test p=0.69 (random slopes not significant), sleep covariates no effect, dichotomous data 81% max reliability. Design limitation confirmed not biological reality. Recommendation: do NOT report ICC_slope, focus on fixed effects and ICC_intercept (Session 2025-12-03 14:30).

### thesis_reframe_laboratory_artifacts_dissolve
**Description:** Major thesis narrative transformation from "failed to find effects" to "laboratory dissociations dissolve in ecological memory encoding." Includes 2024 literature support (Scientific Reports Dec 2024 N=236 confirms null age effects replicate SOTA), binding hypothesis integration (Yonelinas 2019 unitization explains pattern), story.md major rewrite, comprehensive validation framework (execution_plan.md with 6-layer checklist), rq_validate agent creation, and Type 5.5 Source-Destination memory proposal (Session 2025-12-03 18:45).

### rq_validate_agent_mass_testing
**Description:** rq_validate agent testing on 16 completed RQs, discovery of critical random structure mismatch in RQ 5.1.2 (quadratic used (1|UID), piecewise used (Days_within|UID)), fix to matched (1|UID) structure, Test 2 interpretation changed from "continuous favored" to "models equivalent", achievement of 100% validation pass rate (all 16 RQs), and rq_status.tsv validate column addition (Session 2025-12-03 19:30).

### rq_5.2.5_when_exclusion_complete
**Description:** Complete RQ 5.2.5 re-execution after discovering When domain contamination (26 items in step01_item_mapping.csv). When domain excluded per RQ 5.2.1 floor effect discovery (77% item attrition, 6-9% floor). All 9 code steps fixed (step00-step08) to analyze only What/Where domains (79 items). Key findings: purification improves CTT-IRT correlation significantly (What Δr=0.027, Where Δr=0.015, both p<0.001 Bonferroni k=2), IRT theta superior for trajectory modeling (AIC 1655 vs Full CTT 1780 vs Purified CTT 1812), paradox pattern confirmed (purified CTT higher correlation but worse model fit than full CTT due to item homogeneity), reliability maintained (α 0.70-0.83). All 4 validation layers PASS (Session 2025-12-03 20:45).

### ctt_irt_convergence_validated
**Description:** CTT-IRT convergence validation across multiple RQs documenting purification benefit hypothesis using Steiger's z-test for dependent correlations. Primary evidence from RQ 5.2.5 (When excluded): purified CTT shows significantly higher correlation with IRT theta than full CTT (What Δr=0.027 z=10.06, Where Δr=0.015 z=14.22, both p<0.001 Bonferroni k=2). Paradox pattern: purified CTT better convergence but worse trajectory fit (AIC 1812 vs full CTT 1780) due to item homogeneity reducing variance. Cross-references RQ 5.12 paradox discovery, When domain floor effect, Steiger's z-test tool creation. Implications: dual-reporting strategy (full CTT for trajectories, purified CTT for convergence validation) (Session 2025-12-03 20:45).

### rq_5.2.6_complete_domain_variance_decomposition
**Description:** Complete RQ 5.2.6 execution (Domain-Specific Variance Decomposition with When exclusion). 8 analysis steps executed, all validation passed. ICC estimates show substantial between-person variance in forgetting rates (ICC_slope_conditional ~0.52 for both What/Where domains). Where domain shows significant Fan Effect (r=-0.316, p=0.003), What domain does not. Cross-domain correlations extremely high (r=0.96 intercept, r=0.77 slope) suggesting general memory factor. 200 random effects extracted for RQ 5.2.7 clustering. When domain excluded per floor effect (Session 2025-12-03 21:30).

### rq_5.2.7_complete_domain_clustering
**Description:** Complete RQ 5.2.7 execution (Domain-Based K-means Clustering with When exclusion). 7 analysis steps executed, K=5 clusters selected via BIC (BIC=90.09), cluster quality validation (silhouette=0.34 poor but Jaccard=0.88 stable), 5 distinct memory profiles identified (Average-Slow, Average-Improving, Low-Stable, High-Stable, High-Fast decline). Notable finding: 26% of sample shows improving trajectories (practice/consolidation effect). What-Where highly correlated suggesting general memory factor. Full validation pipeline complete (rq_inspect, rq_plots, rq_results, rq_validate all PASS). Session 2025-12-03 22:50.

### tdd_irt_ctt_tools_creation
**Description:** Complete TDD workflow for creating 4 IRT-CTT convergence analysis tools via Red-Green-Refactor methodology. 27 tests written first (Red phase), 4 functions implemented in tools/analysis_ctt.py (compute_ctt_mean_scores_by_factor, compute_pearson_correlations_with_correction, compute_cohens_kappa_agreement, compare_lmm_fit_aic_bic) with 491 lines total (Green phase). All 27/27 tests passing. Tools feature D068 dual p-values (uncorrected + Holm-Bonferroni correction), generic factor support (domain/paradigm/congruence), Landis & Koch kappa interpretation, Burnham & Anderson AIC/BIC thresholds. tools_inventory.md updated with 4 new entries. Successfully unblocked RQ 5.3.5 and 5.4.4 (rq_tools and rq_analysis both succeeded after tool creation). Session 2025-12-03 23:30.

### rq_5.3.5_complete_execution_irt_ctt_convergence
**Description:** Complete execution of RQ 5.3.5 (IRT-CTT Convergence for Paradigms). All 8 analysis steps executed successfully. Key findings: Strong static convergence (r=0.84-0.88 across IFR/ICR/IRE paradigms), substantial dynamic convergence (Cohen's κ=0.667, agreement=83.3%), both LMMs converged with random slopes on log_TSVR. Validates RQ 5.3.1 paradigm findings are robust to measurement approach (not IRT artifacts). Fixed data format mismatch (long to wide pivot). Regenerated 4 plots in 5.2.1 style (continuous TSVR, faded scatter, dashed curves, shaded CIs). Full validation pipeline PASS (rq_inspect, rq_plots, rq_results, rq_validate). 0 anomalies flagged. Session 2025-12-04 00:00.

### rq_5.4.4_complete_execution_irt_ctt_convergence
**Description:** Complete execution of RQ 5.4.4 (IRT-CTT Convergence for Schema Congruence). All 8 analysis steps executed successfully. Key findings: EXCEPTIONAL static convergence (r=0.87-0.91 with incongruent reaching 0.91), substantial dynamic convergence (Cohen's κ=0.667, agreement=83.3%), both LMMs converged with random slopes on log_TSVR. Validates RQ 5.4.1 NULL schema congruence findings are robust to measurement approach (Common/Congruent/Incongruent all similar trajectories is real empirical finding, not measurement artifact). Fixed missing 4_analysis.yaml by adapting from 5.3.5. Full validation pipeline PASS (rq_inspect, rq_plots, rq_results). 1 anomaly flagged (CTT fit dominance). Chapter 5 IRT-CTT convergence trilogy complete (5.2.4 domains, 5.3.5 paradigms, 5.4.4 congruence). Session 2025-12-04 00:30.

### rq_5.4.5_complete_execution_purified_ctt_congruence
**Description:** Complete execution of RQ 5.4.5 (Purified CTT Effects for Schema Congruence). 9 analysis steps executed. Purified CTT shows significantly HIGHER correlation with IRT theta (Δr=+0.096 to +0.108, p<0.001) BUT WORSE LMM model fit (ΔAIC +17 to +35). Purification-trajectory paradox confirmed across all 3 factor structures. Incongruent showed lowest retention (54%) and largest reliability improvement (Δα=+0.063). Full validation pipeline PASS (rq_inspect, rq_plots, rq_results). Session 2025-12-04 01:30.

### rq_5.4.6_5.4.7_complete_variance_clustering_congruence
**Description:** Complete execution of RQ 5.4.6 (Variance Decomposition) and RQ 5.4.7 (Clustering) for Schema Congruence. RQ 5.4.6: ICC_slope=0.000 for all congruence levels (forgetting NOT trait-like), ICC_intercept 0.27-0.37 (Congruent highest). RQ 5.4.7: K=6 clusters, weak quality (silhouette=0.254, Jaccard=0.592), meaningful null finding (no schema-selective memory phenotypes). Congruence section 7/8 complete. Chapter 5 at 81% completion (25/31 RQs). Session 2025-12-04 02:15.

### paradigms_5.3.6_5.3.9_complete_cross_cutting_replication
**Description:** Complete execution of final 4 Paradigms RQs (5.3.6-5.3.9). All cross-cutting findings replicated: (1) Purification-trajectory paradox confirmed 3rd time, (2) ICC_slope≈0 across all paradigms, (3) Weak clustering with no paradigm-selective phenotypes, (4) Item difficulty paradigm-invariant. Paradigms section 100% complete (9/9 RQs). Chapter 5 at 94% completion (29/31 RQs). Only 2 GLMM RQs remaining (5.1.6, 5.2.8). Session 2025-12-04 03:00.

### type_5.5_pipeline_complete
**Description:** Complete history of Type 5.5 Source-Destination RQ creation and documentation. Session 2025-12-04 04:30: 7 RQs created (5.5.1-5.5.7 pickup vs putdown analysis), story.md updated with 10 new findings, GLMM RQs deprioritized (5.1.6/5.2.8/5.4.8), scholar validation mixed results, hypothesis direction debate. Session 2025-12-04 21:00: complete pipeline documentation (rq_planner/rq_tools/rq_analysis executed, agent prompt bug fixes, folder convention violations corrected).

### type_5.5_validation_fixes_complete
**Description:** Complete history of Type 5.5.3-5.5.7 validation fixes achieving APPROVED status. Session 2025-12-04 19:00: Fixed 5 RQ concept documents per validation summary, key improvement 5.5.4 from REJECTED 8.3 to APPROVED 9.3, comprehensive methodological patterns established (LMM 7-criteria validation, power analysis for null hypotheses, bounded CTT remedial hierarchy, bootstrap B=100 standard, practice effects mitigation). All 5 downstream RQs validated via dual-agent (rq_scholar + rq_stats) achieving scores 9.3-9.6.

### irt_mc_samples_pattern_discovery
**Description:** Discovery and documentation of correct IRT mc_samples configuration pattern across ROOT RQs. model_fit uses mc_samples=1 for fast point estimates of item parameters, model_scores uses mc_samples=100 for accurate Monte Carlo integration of theta. RQ 5.5.1 violated pattern (100/100 instead of 1/100) causing 100× slowdown. Pattern now documented and validated across all ROOT RQs (5.1.1, 5.2.1, 5.3.1, 5.4.1, 5.5.1).

### plots_style_5.2.1_format
**Description:** Publication-quality trajectory plot formatting standard established. Individual scatter points (alpha=0.15) from 800 observations, dashed fitted curves from LMM predictions, 95% CI bands from covariance matrix, continuous TSVR x-axis (not binned). Dual-scale output (theta + probability) per Decision D069. Template implementation in results/ch5/5.5.1/plots/plots.py. Supersedes binned summary approach from initial rq_plots agent.

### rq_5.5.1_pipeline_execution_minimum_settings_complete
**Description:** First production execution of Type 5.5 Source-Destination RQ with MINIMUM IRT settings (pipeline validation phase). All 8 analysis steps executed successfully, 6 code fixes applied, statistical results preliminary. MEDIUM settings upgrade in progress with WRONG mc_samples configuration (100/100 instead of 1/100). Superseded by Session 2025-12-05 09:30 production execution with corrected IRT settings.

### rq_5.5.1_complete_production_execution
**Description:** RQ 5.5.1 Source-Destination memory analysis with corrected IRT settings and publication-quality plots. Complete 8-step pipeline re-execution with mc_samples=1/100 pattern, logarithmic model selected (AIC=1747.77), marginally significant interaction (p=0.05 Bonferroni) showing destination forgetting faster than source. Plot style fixed to 5.2.1 format with individual scatter points. Full validation pipeline complete (rq_inspect + rq_plots + rq_results). 1 anomaly flagged. Production-ready.

### rq_5.5.4_complete_irt_ctt_convergence_validation
**Description:** Complete RQ 5.5.4 execution (IRT-CTT Convergence for Source-Destination Memory). All 9 analysis steps successful. Primary hypothesis SUPPORTED: correlations exceed r>0.70 threshold (Source r=0.944 exceptional, Destination r=0.871 strong). Secondary finding: Cohen's kappa=0.000 (significance agreement 50%) indicates inferential divergence despite measurement convergence. Key insight: IRT and CTT measure SAME constructs (high r) but IRT MORE SENSITIVE for detecting location-specific effects (bounded CTT compresses variance). Fourth in IRT-CTT convergence series (5.2.4 domains, 5.3.5 paradigms, 5.4.4 congruence, 5.5.4 source-destination).

### irt_ctt_inferential_divergence_pattern
**Description:** Documentation of measurement convergence vs inferential divergence pattern across IRT-CTT analyses. High correlations (r>0.87) validate same constructs measured, but divergent significance patterns (kappa varies 0.00-0.667) reflect IRT's superior sensitivity. Mechanism: CTT bounded [0,1] scale compresses variance near boundaries, attenuating effect sizes. Pattern varies by factor structure and effect magnitude. Methodological implications: report both static convergence (correlations) and dynamic convergence (kappa), interpret divergence as sensitivity difference not measurement failure. Cross-RQ evidence from 5.3.5, 5.4.4, 5.5.4.

### statsmodels_coefficient_extraction_pattern
**Description:** Documentation of statsmodels LMM coefficient extraction patterns and common errors. Problem: model.params/tvalues/pvalues include random effects, not just fixed effects. Solution: slice to fixed effects only using [:n_fe] where n_fe = len(model.model.exog_names). Alternative: export coefficients to CSV immediately after fitting to avoid pickle loading errors (patsy eval_env failures). Applies to ALL LMM coefficient comparisons (RQ 5.5.2 segment slopes, 5.5.3 interactions, 5.5.4 parallel LMMs). Tool development pattern for compare_lmm_coefficients() and downstream analysis steps.

### rq_5.5.5_complete_purified_ctt_paradox_4th_replication
**Description:** Complete RQ 5.5.5 execution (Purified CTT Effects for Source-Destination Memory) with 4th independent paradox replication. Destination shows full paradox (Δr=+0.072 sig, ΔAIC=+17.92 decisive). Source shows partial paradox (Δr=+0.010 n.s. due to ceiling effect at r=0.93, ΔAIC=+5.26 substantial). All 9 analysis steps plus validation (29/30 checks passed). Establishes purification-trajectory paradox as general measurement principle: IRT purification improves cross-sectional correlation but degrades longitudinal trajectory fit by removing variance useful for individual differences. High retention rate (89%) means removed items contributed unique variance.

### multidimensional_irt_probability_conversion_bug_fix
**Description:** Critical bug discovery and fix for multi-dimensional IRT models requiring factor-specific item difficulties when converting theta to probability scale. 2-dimensional IRT (source vs destination) creates TWO SEPARATE theta scales with different item difficulty distributions (Source b=-0.453 easy, Destination b=+1.371 hard). Using difficulty=0.0 for all factors masks 25-30 percentage point baseline accuracy difference. Factor-specific conversion reveals 30-45 percentage point effect. Bug fix applied to results/ch5/5.5.1/plots/plots.py. Pattern documented from .archive/v1/plots.py lines 543-561 which correctly used factor-specific difficulties.

### rq_plots_agent_v4.0.1_update
**Description:** rq_plots agent enhancement adding critical multi-dimensional IRT probability conversion guidance (v4.0.1). Added "CRITICAL: Multi-Dimensional IRT Probability Conversion" section explaining problem (factor-specific difficulties create different theta scales), wrong approach (difficulty=0.0 for all), correct approach (loop through factors with factor-specific b values), validation check (compare to raw accuracy). Includes code example and RQ 5.5.1 lesson learned. Prevents masking of large baseline effects in multi-factor IRT analyses.

### rq_5.5.2_complete_pipeline_execution_null_finding
**Description:** Complete RQ 5.5.2 Source-Destination Consolidation (Two-Phase) pipeline execution with null hypothesis result. All 8 steps successful (load dependencies, create piecewise variables, reshape, fit LMM, extract slopes, test benefit, test interaction, plot data). Primary finding: 3-way Days_within × Segment × LocationType interaction NOT significant (p=0.61, f²=0.0005 negligible). Source and destination show SIMILAR consolidation patterns (~0.10 benefit Early→Late for both). Null finding supports ecological binding hypothesis (no dissociation). 7 code fixes applied (TSVR range, statsmodels direct use, vcov extraction, pickle workaround, plotting bugs). Full validation PASS. D069 dual-scale plots generated.

### plotting_tool_bug_fixes
**Description:** Collection of bug fixes in tools/plotting.py discovered during RQ execution. Bug 1: pred_sorted UnboundLocalError (variable referenced before assignment in conditional branches). Bug 2: Data_Type value mismatch ('prediction' vs 'predicted'). Bug 3: vcov matrix extraction wrong dimensions (11x11 full matrix vs 8x8 fixed effects only). All discovered during RQ 5.5.2 piecewise trajectory plot generation.

### statsmodels_pickle_workaround_pattern
**Description:** Workaround pattern for statsmodels/patsy pickle loading errors (f_locals eval_env failures). Problem: loading pickled MixedLM models fails with patsy eval error preventing coefficient access. Solution: Export coefficients to CSV immediately after fitting, read from CSV in downstream steps instead of loading pickle. Alternative monkey-patch approach fragile and not recommended. Pattern applies to ALL LMM steps needing loaded models for coefficient extraction (interactions, contrasts, hypothesis tests). Emerged from RQ 5.5.2 Step 6 failure, used extensively in RQ 5.5.4.

### rq_5.5.3_complete_age_effects_null_hypothesis_supported
**Description:** Complete RQ 5.5.3 Age Effects on Source-Destination Memory with null hypothesis supported and 100% statistical power. All 8 steps successful (load, prepare, fit LMM, validate assumptions 6/7, extract interactions, power analysis, contrasts, plot tertiles). Primary finding: 3-way Age × LocationType × Time interaction NOT significant (p=0.16, 0.33 Bonferroni). Age effects identical for Source (-0.005/year) and Destination (-0.005/year), contrast p=0.99, Cohen's d=-0.02. Power=1.00 (100%) ensures null is interpretable. Third replication of universal null age pattern (5.3.4, 5.4.3, 5.5.3). Supports VR ecological encoding creates age-resistant memory traces. Thesis-ready validated.

### power_analysis_simulation_method
**Description:** Parametric bootstrap power analysis approach for LMM 3-way interactions. Method: 100 simulated datasets with true effect β=0.01 (small), fit LMM, extract Bonferroni-corrected p-value, compute power as rejection proportion, binomial exact CI (Clopper-Pearson). RQ 5.5.3 results: Power=1.00 [0.97-1.00], target 0.80 met. Interpretation: null finding completely interpretable (not Type II error). Mandatory for null findings to distinguish "no effect" from "insufficient power". Generalizes to any LMM 3-way interaction.

### age_tertile_plot_methodology
**Description:** Methodology for creating age tertile trajectory plots with factor-specific IRT probability conversion. Uses pd.qcut(Age, q=3) for equal group sizes (33rd/67th percentiles). RQ 5.5.3 cutoffs: Young ≤37y (33p), Middle 37-52y (34p), Older >52y (33p). Plot data: 24 rows (3 tertiles × 2 locations × 4 tests). CRITICAL: Must use location-specific item parameters for probability conversion (Source b=-0.453 easy, Destination b=+1.371 hard). Validation: compare plot probabilities to raw accuracy. Applies to RQ 5.3.4, 5.4.3, 5.5.3 (any Age × Factor × Time plots).

### rq_5.5.6_complete_variance_decomposition_opposite_correlations_discovery
**Description:** Complete RQ 5.5.6 Source-Destination Variance Decomposition execution (Session 2025-12-05 16:30). All 6 analysis steps successful with MAJOR NOVEL FINDING: Source and destination memory show OPPOSITE intercept-slope correlations (Source r=+0.989 regression to mean, Destination r=-0.903 fan effect, both p<10^-37). ICC_intercept: Destination (0.42 Fair) 75% higher than Source (0.24 Poor). ICC_slope near zero both (design limitation confirmed). Cross-location correlations: intercept r=0.66, slope r=-0.44. Extracted 200 random effects (100 UID × 2 locations) for RQ 5.5.7 clustering dependency. rq_validate PASS WITH NOTES (2 moderate: no bootstrap CIs, no residual plots - mitigated by convergence + large N). Type 5.5: 6/7 complete, Chapter 5: 37/38 complete (97%). Theoretical significance: First demonstration source vs destination memory show opposite forgetting dynamics, supports binding hypothesis dissociation, important for thesis narrative on ecological memory patterns.

### rq_5.5.7_complete_clustering_exceptional_silhouette
**Description:** Complete RQ 5.5.7 Source-Destination Clustering execution (Session 2025-12-06 14:30). All 7 analysis steps successful with EXCEPTIONAL FINDING: This is the ONLY Chapter 5 clustering RQ with Silhouette ≥ 0.40 threshold met (actual: 0.417). All three quality metrics PASSED (Silhouette=0.417, Davies-Bouldin=0.785, Jaccard=0.831). K=4 clusters identified via BIC minimum (BIC=164.76). Cluster profiles directly reflect opposite intercept-slope correlations from RQ 5.5.6: Cluster 0 (N=20) Dual High with source declining/destination maintaining, Cluster 1 (N=26) Dual Low reversed pattern. Source-destination memory shows STRONGER clustering structure than all other Ch5 analyses (5.1.5, 5.2.7, 5.3.8, 5.4.7 all had Silhouette < 0.40). rq_validate PASS with 1 moderate issue (borderline Silhouette +0.017 margin, mitigated by other metrics). TYPE 5.5 COMPLETE: 7/7 RQs (100%). CHAPTER 5 EFFECTIVELY COMPLETE: 38/38 RQs minus 2 BLOCKED by GLMM (5.1.6, 5.2.8). Ready for Chapter 6.

### ch6_planning_31_rqs_8_types
**Description:** Complete Chapter 6 planning session (2025-12-06 16:30). Created comprehensive Ch6 analysis plan with 31 RQs across 8 hierarchical types (General Confidence, Calibration, Domain Confidence, Paradigm Confidence, Schema Confidence, High-Confidence Errors, Predictive Validity, Source-Destination). Updated Ch5 story.md with 36 RQ elevator pitches. Created rq_info.tsv specification (11 columns per RQ). 4 critical hypotheses (H1: ICC_slope > 0.10, H2: null replication, H3: calibration dynamics, H4: source-dest opposite correlations). 5-category GRM specified for all IRT analyses. Removed redundant IRT-CTT convergence RQs (proven 4× in Ch5).

### ch6_mass_parallelization_186_agents
**Description:** Complete Chapter 6 mass parallelization infrastructure (2025-12-06 17:45). Created 31 RQ folders with complete structure (code/data/docs/plots/results/logs/, status.yaml). Executed 186 agent invocations (31 RQs × 6 agents). Results: rq_concept 31/31 success, rq_planner 31/31 success, rq_tools 30/31 success (6.2.3 blocked by missing gamma tools), rq_analysis 30/31 success, rq_scholar 30/31 (6.7.1 rejected), rq_stats ~25/31 (3 conditional, 3 rejected). Created rq_status.tsv tracking. 97% success rate (30/31 RQs ready for g_code). Largest parallel agent execution in project.

### ch6_concept_fixes_execution_protocol
**Description:** Fixed 5 CONDITIONAL/REJECTED RQ concepts to gold standard quality (2025-12-06 19:30). RQ 6.4.2 added reliability check and Lord's paradox mitigation. RQ 6.6.3 CRITICAL fix from LMM to GLMM binomial with overdispersion validation. RQ 6.7.1 terminology fix (retrieval confidence) with normality validation. RQ 6.7.2 added aggregation strategy and SD constraint sensitivity. RQ 6.8.1 added enactment effect and VR validity. Created ch6/execute.md execution protocol (~2k tokens) with Ch5 lessons learned (IRT mc_samples, LMM coefficient extraction, CSV not pickle), common mistakes, step execution template, validation workflow.

### rq_6.1.1_complete_execution_logarithmic_best
**Description:** Complete execution history of RQ 6.1.1 (Confidence Trajectory Functional Form), the first production ROOT RQ for Chapter 6. Documents all 8 steps, logarithmic model selection (AIC=338.60, weight=0.64), 72-item GRM with 100% retention, power-law forgetting trajectory, and 3 runtime fixes. Key finding: confidence declines logarithmically (steep initial decline slowing over time), supporting metacognitive monitoring tracks memory decay hypothesis. Files: 8 code scripts, 15 data outputs, 8 logs. Execution time: ~15 min. Session 2025-12-06 22:00.

### ch6_grm_irt_pattern_mc_samples_1_100
**Description:** GRM IRT calibration pattern using mc_samples=1 for fitting (fast convergence) and mc_samples=100 for scoring (accurate theta estimates). Pattern originated in Ch5 RQ 5.5.1, applied successfully to Ch6 RQs. Prevents 7000+ epoch hangs. Fitting phase uses mc_samples=1 for efficient gradient descent optimization (~35k epochs in ~2 min). Scoring phase uses mc_samples=100 for accurate numerical integration of theta. Applied to RQ 6.1.1 and all future Ch6 GRM calibrations. Session 2025-12-06 22:00.

### ch6_lmm_statsmodels_cov_re_fix
**Description:** Fix for statsmodels random effects covariance matrix extraction. In newer statsmodels versions, cov_re is a DataFrame (not ndarray), requiring .values.flatten() for safe extraction. Safe pattern: check hasattr(cov_re, 'values') and use .values.flatten() for DataFrame, .flatten() for ndarray. Affects ICC computation, model diagnostics, variance component reporting, and random effects interpretation. Applied in RQ 6.1.1 step05. Pattern needed for all LMM trajectory models in Ch6. Session 2025-12-06 22:00.

### ch6_dfdata_wide_format_paradigm_parsing
**Description:** dfData.csv column structure for confidence data. Data is in WIDE format with paradigm embedded in column names (TC_{PARADIGM}-{DOMAIN}-{ITEM}), NOT long format with separate Paradigm column. Requires parsing column names to filter paradigms. Example columns: TC_IFR-What-01, TC_ICR-Where-01, TC_IRE-When-01. Column naming is self-documenting (paradigm/domain/item encoded in name). Applies to TC_* (confidence) and AC_* (accuracy) columns. Affects any RQ filtering by paradigm subset (6.1.1, 6.3.1, 6.4.1, etc.). Session 2025-12-06 22:00.

### rq_6.3.1_partial_execution_when_domain_significant
**Description:** RQ 6.3.1 Steps 00-05 execution history (domain-based 3-factor GRM). Extracted 72 TC items across 3 domains (What/Where/When). Fixed 3 critical issues: long format column mapping, return value unpacking, validation column names. All 72 items retained (100%). LMM revealed UNEXPECTED finding: When domain × Time interaction significant (p=0.020), Where domain NULL as expected. Primary hypothesis partially refuted. Added 3 critical fixes to execute.md: IRT background process management (no epoch polling), flush pattern for log functions, MINIMUM settings for validation (mc_samples=1). Session 2025-12-07 11:00. Superseded by complete execution in Session 2025-12-07 13:50.

### rq_6.3.1_complete_execution_when_domain_steeper_decline
**Description:** RQ 6.3.1 COMPLETE execution history - Steps 06-07 (post-hoc contrasts and trajectory plots). When domain shows significantly steeper confidence decline than both What (p=0.019) and Where (p=0.028) domains. NULL hypothesis PARTIALLY REFUTED. Scientific finding: confidence-accuracy dissociation for temporal memory (When domain confidence decays faster than accuracy suggests). Two technical patterns identified: (1) g_code aggregation bug - groups by continuous TSVR_hours instead of discrete test (fix: group by test, compute mean TSVR_hours), (2) tool bypass for LMM post-hoc - compute_contrasts_pairwise has internal bugs (fix: direct statsmodels implementation cleaner). Dual-scale trajectory data generated per Decision D069 (theta-scale and probability-scale with domain-specific discrimination parameters). All 8 steps complete. Session 2025-12-07 13:50.

### ch6_execute_md_updates
**Description:** Runtime fixes and execution protocol updates for Chapter 6. Three critical patterns documented: (1) IRT background process management - don't poll epoch status repeatedly (blows up context), (2) Flush pattern for log functions - f.flush() + print(flush=True) for real-time visibility, (3) MINIMUM settings for code validation - mc_samples=1/iw_samples=1 for first runs (2-7 min validation), then production settings after validation. Two-phase execution strategy prevents wasting time on buggy code with 30-60 min production runs. Session 2025-12-07 11:00.

### ch6_tool_interface_issues
**Description:** Tool interface mismatches discovered during Ch6 execution. fit_lmm_trajectory_tsvr tool has column name expectations that differ from prepared data in Step 04. Solution: bypass tool, use statsmodels directly when data pre-prepared and formula specified. Tool bypass pattern confirmed: tools valuable for multi-step pipelines and standardized outputs, less valuable for single-step operations with pre-prepared data. Bypassing tools is acceptable when cleaner/faster. Priority is scientific correctness, not tool usage. Similar pattern in RQ 6.3.1 Step 06 (compute_contrasts_pairwise had sig_uncorrected bug). Session 2025-12-07 11:00.

### rq_6.4.1_step00_complete_paradigm_extraction
**Description:** RQ 6.4.1 Step 00 data extraction complete - 72 TC items extracted (24 per paradigm: IFR/ICR/IRE), 3-factor Q-matrix created, n_cats=5 detected adaptively, TSVR range 1.0-246.24 hours. Paradigm-based 3-factor GRM testing whether Free Recall, Cued Recall, and Recognition paradigms show different confidence decline patterns. Primary hypothesis NULL (paradigm affects baseline, not slopes). Generated step00_extract_confidence_data.py (435 lines), execution <10 seconds. Session 2025-12-07 19:45.

### rq_6.4.1_step01_five_systematic_bug_fixes
**Description:** RQ 6.4.1 Step 01 IRT calibration Pass 1 with 5 systematic bug fixes applied iteratively. Bugs: (1) missing UID/test columns parsed from composite_ID, (2) wrong return unpacking order corrected, (3) n_cats must be list for configure_irt_model, (4) n_cats must be list for extract_parameters_from_irt, (5) MIRT column format kept as-is (Difficulty/Overall_Discrimination/Discrim_*). All bugs repeatable from RQ 6.3.1 and 6.1.1 (same pattern across all GRM RQs). Root cause: g_code lacks multidimensional IRT training examples. Pattern documented for future RQs. Session 2025-12-07 19:45.

### g_code_multidimensional_irt_bug_pattern
**Description:** Systematic pattern of 5 bugs repeatable across ALL GRM-based RQs (6.1.1 single-factor, 6.3.1 domain 3-factor, 6.4.1 paradigm 3-factor). Root cause: g_code lacks training examples for multidimensional IRT models. Pattern WILL recur in future GRM RQs (6.5.1, 6.6.1, 6.7.2, 6.8.1). Solution: Use code-copying strategy from 6.3.1/6.4.1 (copy working code, replace factor names via find/replace) vs g_code debugging (saves 75-80% time, 45 min vs 4-5 hours). Documents all 5 bugs with fixes and pattern sources. Session 2025-12-07 19:45.

### proactive_context_finding_before_execution
**Description:** Proactive context-finding strategy using context_finder agent BEFORE RQ execution to gather historical patterns, identify bug patterns from past RQs, apply fixes proactively, reduce debugging time by referencing known solutions. RQ 6.4.1 validation: searched archives before coding, found 8 relevant topics (98-70% relevance, all current v4.X), identified bug patterns from RQ 6.1.1 and 6.3.1, applied fixes during debugging iterations, reduced time vs reactive approach. Strategy follows CLAUDE.md Proactive Context-Finding Workflow. Recommended for all future RQs with similar structure or complex statistical workflows. Session 2025-12-07 19:45.
---

## How to Use This Index

**For main claude:**
- Check this file after /refresh to see what archived context is available
- Reference topic names when creating "Active Topics" section in state.md
- Update this file when creating new documentation (NOT for archived context - context-manager handles that)

**For context-finder agent:**
- Read this file first to identify relevant archive topics
- Search .claude/context/archive/*.md based on topic names
- Also search docs/*.md (indexed in docs/docs_index.md)

---

**Notes:**
- This file is maintained by context-manager agent (NOT main claude)
- Topics have NO timestamps or relevance scores in this index
- Timestamps are IN the archive files themselves (each entry timestamped)
- New topics added automatically when context-manager archives content
- Each topic file max 50k tokens (context-manager enforces)
