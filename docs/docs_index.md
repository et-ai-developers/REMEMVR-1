# Documentation Index

**Last Updated:** 2025-12-08 (Kitchen sink model selection tool added to tools_catalog and tools_inventory)

---

## Templates

### templates/concept_template.md
**Purpose:** Template for users to create concept.md (RQ description in their own words before agent starts)
**Audience:** Users creating new RQs, main claude when assisting with RQ setup
**Status:** Current (v3.0 workflow)
**Key Topics:** RQ intent, memory domains, analysis approach, hypothesis, special considerations, user questions

### templates/plan_template.md
**Purpose:** Template for rq-specification agent Planning Mode output (agent's interpretation + questions for user)
**Audience:** rq-specification agent (Planning mode), users reviewing agent's plan
**Status:** Current (v3.0 workflow)
**Key Topics:** Agent's understanding, domain tag mapping, tool requirements, CRITICAL/CLARIFICATION/OPTIONAL questions, user answer section

### templates/mode1_planning_new.md
**Purpose:** MODE 1 (Planning) workflow documentation for rq-specification agent v3.0
**Audience:** Agent developers, main claude when debugging agent behavior
**Status:** Current (embedded in .claude/agents/rq_specification.md)
**Key Topics:** Read concept.md, generate questions, create plan.md, circuit breaker checks

### templates/mode2_drafting_new.md
**Purpose:** MODE 2 (Drafting) workflow documentation for rq-specification agent v3.0
**Audience:** Agent developers, main claude when debugging agent behavior
**Status:** Current (embedded in .claude/agents/rq_specification.md)
**Key Topics:** Read plan.md answers, generate info.md + config.yaml, create directories

---

## Core Documentation

### project_specific_stats_insights.md
**Purpose:** REMEMVR-specific statistical requirements discovered through analysis execution (MANDATORY: 2-pass IRT purification, dual reporting of corrected/uncorrected results, dual-scale trajectory plots, IRT→LMM pipeline with TSVR)
**Audience:** rq-specification agent, statistics-expert agent (MUST read before creating/validating any RQ)
**Status:** Current
**Key Topics:** 2-pass IRT methodology (Decision D039), item purification thresholds (|b|>3.0, a<0.4), temporal items difficulty, expected retention rates (40-50%), dual reporting approach (Decision D068: report both uncorrected and Bonferroni-corrected p-values), dual-scale trajectory plots (Decision D069: theta + probability scales for interpretability), IRT→LMM pipeline with TSVR (Decision D070: use actual hours since encoding, NOT nominal days 0,1,3,6), exploratory thesis philosophy, implementation requirements

### data_structure.md
**Purpose:** Detailed master.xlsx tag system, UID format, critical tag formatting rules
**Audience:** Data-prep agent, main claude when working with data extraction
**Status:** Current
**Key Topics:** Tag schema (DEM, COG, RVR), exact tag formatting with dashes, data extraction workflow using data.py directly

### irt_methodology.md
**Purpose:** IRT deep dive, model specifications, parameter interpretation, downstream usage for LMM
**Audience:** Analysis-executor agent, main claude when building IRT tools, statistics-expert agent
**Status:** Current
**Key Topics:** Graded Response Model (GRM), multidimensional IRT, deepirtools IWAVE implementation, theta estimation, composite_ID stacking, downstream usage in LMM pipeline (theta scores + TSVR)

### lmm_methodology.md
**Purpose:** LMM deep dive, formula syntax, random effects structure, IRT→LMM data flow
**Audience:** Analysis-executor agent, main claude when building LMM tools, statistics-expert agent
**Status:** Current
**Key Topics:** Linear Mixed Models, longitudinal trajectories, statsmodels.MixedLM, fixed and random effects, REMEMVR-specific IRT→LMM data flow (composite_ID parsing, TSVR merge, theta as outcome), time variable requirements (TSVR, NOT nominal days)

### cognitive_tests.md
**Purpose:** RAVLT, BVMT, NART, RPM scoring procedures with exact tag names
**Audience:** Data-prep agent when extracting cognitive test scores
**Status:** Current
**Key Topics:** Cognitive battery administration, scoring procedures, derived scores, exact tag names in master.xlsx

### README.md
**Purpose:** Overview of documentation system and loading guidelines
**Audience:** All agents and main claude
**Status:** Current
**Key Topics:** When to load each doc, on-demand loading strategy, doc usage guidelines

---

## Reference Documentation

### data_structure.md
**Purpose:** AUTHORITATIVE SINGLE REFERENCE for master.xlsx structure, tag system, UID format, domain codes, and data extraction API
**Audience:** All agents working with REMEMVR data (especially data-prep, rq-specification)
**Status:** Current (merged from glossary.md 2025-11-14, added Decision D070 cross-reference 2025-11-14)
**Key Topics:** Master.xlsx format, UID system, tag schema, quick reference tables (domains, paradigms, item codes), demographic data, cognitive tests, REMEMVR test sections, regex wildcards, data extraction examples, TSVR (Time Since VR) for IRT→LMM pipeline (Decision D070)

### design_decisions.md
**Purpose:** Documents key design decisions and their rationales (composite_ID stacking, dichotomous scoring, agent architecture)
**Audience:** Main claude when questioning why specific design choices were made
**Status:** Current
**Key Topics:** Why composite_ID stacking, why dichotomous scoring, why agent-based architecture

### thesis_chapters.md
**Purpose:** Overview of thesis chapters 5, 6, 7 with RQ counts and focus areas
**Audience:** Main claude when working on specific RQs or planning chapter-level work
**Status:** Current
**Key Topics:** Chapter 5 (Trajectory of Forgetting, 15 RQs), Chapter 6 (Metacognition, 15 RQs), Chapter 7 (Individual Differences, 20 RQs)

---

## Workflow Documentation

### refactor_overview.md
**Purpose:** Explains refactor rationale, principles, and high-level workflow (old vs new pipeline)
**Audience:** Main claude when understanding refactor context or planning refactor tasks
**Status:** Current
**Key Topics:** Old monolithic pipeline, new agent-based pipeline, refactor principles, user approval gates

### rq_workflow.md
**Purpose:** Documents flat agent architecture and 6-step RQ specification workflow
**Audience:** Main claude when creating/executing RQs, understanding agent communication
**Status:** Superseded by rq_standard_procedure.md (lacks safety gates)
**Key Topics:** Flat architecture (no nesting), file-based communication, RQ-Spec → Scholar → Statistics validation flow

### rq_standard_procedure.md
**Purpose:** Complete 8-step procedure for building RQs with safety gates, verification checkpoints, and user approval requirements (v2.0)
**Audience:** Main claude when executing ANY RQ, ALL agents must follow this procedure
**Status:** Current (Production-Ready)
**Key Topics:** 8-step workflow, safety audit (Step 5), output verification (Step 7), contamination detection, hybrid approval gates, quality metrics

### results_schema.md
**Purpose:** Standardized RQ folder structure and info.md template
**Audience:** Results-inspector agent, main claude when creating RQ outputs
**Status:** Superseded by rq_file_structure_ground_truth.md (outdated, inconsistent with reality)
**Key Topics:** RQ folder structure (data/, code/, plots/, logs/, validation/), info.md template with 11 sections

### rq_file_structure_ground_truth.md
**Purpose:** ABSOLUTE GROUND TRUTH for RQ file/folder structure - mandatory for all agents, defines naming conventions, location rules, phase-by-phase evolution
**Audience:** ALL agents (rq-spec scans structure on every invocation), main claude when validating RQs
**Status:** AUTHORITATIVE (v2.0 - all agents must follow exactly)
**Key Topics:** Stateful rq-spec agent with context dumps, companion .md requirements, strict naming conventions, file location rules, validation checklists, migration instructions

---

## Agent Documentation

### agents_overview.md
**Purpose:** Complete overview of the 7 RQ pipeline agents and supporting agents (context-manager, context-finder)
**Audience:** Main claude when working with agents, users learning agent architecture
**Status:** Current
**Key Topics:** Agent types, communication protocol, 6-step pipeline, invocation methods, JSON report format

### data_prep_agent_guide.md
**Purpose:** Complete usage guide for Data-Prep agent (v3.0 with critical bug fix)
**Audience:** Main claude when invoking data-prep agent, troubleshooting extraction issues
**Status:** Current (v3.0 production-ready)
**Key Topics:** When to use agent, input specifications, workflow examples, troubleshooting, validation rules

### tools_inventory.md
**Purpose:** Comprehensive reference of all statistical analysis tools (IRT, LMM, plotting, validation, config)
**Audience:** Statistics-expert agent, analysis-executor agent, main claude when building analysis scripts
**Status:** Current (49/49 tests passing)
**Key Topics:** Complete API reference for tools.analysis_irt, tools.analysis_lmm, tools.plotting, tools.validation, tools.config modules

---

## Legacy Documentation

### variables_system.md
**Purpose:** LEGACY documentation on old variables.xlsx system
**Audience:** Historical reference only
**Status:** Deprecated (DO NOT USE)
**Key Topics:** OLD method of defining all variables in variables.xlsx, why it was abandoned, migration to NEW direct data.py approach

---

## User Documentation

### user/codebase_explanation.md
**Purpose:** User-generated explanation of codebase structure and data format
**Audience:** Main claude for understanding user's mental model
**Status:** Current (user-maintained)
**Key Topics:** Master.xlsx structure from user perspective, tag system explanation, participant UID format

### user/analysis_pipeline_solution.md
**Purpose:** V4.X ARCHITECTURE SPECIFICATION - Complete atomic agent redesign ground truth (13 agents replacing 7 monolithic agents)
**Audience:** ALL v4.X agents (MUST read before any v4.X implementation), main claude when building v4.X system
**Status:** VALIDATED (2025-11-15, ultrathink validation with 40 issues resolved)
**Key Topics:** 13 atomic agent specifications (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, g_conflict, rq_tools, rq_analysis, g_code, g_debug, rq_inspect, rq_plots, rq_results), docs/v4/ file structure, best_practices/ (universal.md, workflow.md, code.md - circuit breakers + platform rules split by agent type), status.yaml pseudo-statefulness, context_dump mechanism, workflow orchestration (manual Phase 1, automated Phase 2), g_code validation protocol, error recovery workflow, scope boundaries (RAW vs DERIVED data), cross-RQ dependencies, legacy v3 archival (_legacy/v3/agents/), transition rationale (context bloat → hallucinations)

---

## V4.X Documentation

### v4/best_practices/universal.md
**Purpose:** Universal error handling and platform rules for ALL 13 v4.X agents (circuit breakers, platform compatibility, reporting, task-sniper philosophy)
**Audience:** ALL 13 agents (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, g_conflict, rq_tools, rq_analysis, g_code, g_debug, rq_inspect, rq_plots, rq_results)
**Status:** Current (2025-11-21, split from agent_best_practices.md)
**Key Topics:** 5 circuit breaker types (EXPECTATIONS/STEP/TOOL/CLARITY/SCOPE), ASCII-only output, UTF-8 file encoding, Bash commands, Windows environment, report format (success/error), task-sniper philosophy, stateless architecture, fail-fast validation, git workflow exclusion

### v4/best_practices/workflow.md
**Purpose:** Workflow-specific best practices for RQ-specific agents using status.yaml (pseudo-statefulness, context dumps, file paths, validation gates)
**Audience:** 10/13 workflow agents (rq_builder, rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, rq_inspect, rq_plots, rq_results) - NOT for g_conflict, g_code, g_debug
**Status:** Current (2025-11-21, split from agent_best_practices.md)
**Key Topics:** YAML parsing (general LLM reasoning, no parser needed), pseudo-statefulness (reading prior context_dumps), context dump format (max 5 lines, terse summaries), file path conventions (relative to results/chX/rqY/), validation gates (status check, file check, information check)

### v4/best_practices/code.md
**Purpose:** Code-specific best practices for agents generating/validating/debugging Python code (Poetry environment, data source boundaries, MCP tool usage)
**Audience:** 5/13 code-aware agents (rq_planner, rq_tools, rq_analysis, g_code, g_debug) - NOT for rq_builder, rq_concept, rq_scholar, rq_stats, g_conflict, rq_inspect, rq_plots, rq_results
**Status:** Current (2025-11-21, split from agent_best_practices.md)
**Key Topics:** Poetry-only execution (never pip install), dependency management (poetry add/show), RAW data boundaries (master.xlsx or other RQ outputs), DERIVED data (analysis pipeline outputs), NEVER generate mock data (CLARITY ERROR if source unclear), MCP tools (resolve-library-id, get-library-docs)

### v4/chronology.md
**Purpose:** Complete chronological audit trail of ALL documents read by ALL 13 v4.X agents in execution order - maps agent workflows against solution.md specification
**Audience:** Quality control (audit documents for bloat/hallucinations/contradictions), debugging (trace what agents should read), development (update when modifying agent workflows)
**Status:** Current (2025-11-21)
**Key Topics:** Execution order for 13 agents, document read/write/update annotations, Phase 1 manual setup (10 agents), Phase 2 automated execution loop (g_code + rq_inspect + g_debug), Phase 3 results (rq_plots + rq_results), validation gates (g_conflict at steps 10 & 13, 4-layer validations), context window budgets per agent (<5k tokens), document reuse patterns, TDD approach for names.md, multimodal inspection for plots, quality control audit checklist

### v4/templates/scholar_report.md
**Purpose:** Template specification for rq_scholar agent scholarly validation feedback (10-point rubric with devil's advocate analysis)
**Audience:** rq_scholar agent when creating standalone 1_scholar.md validation report
**Status:** Current (2025-11-21, updated for standalone file approach)
**Key Topics:** 10-point rubric system (5 categories), decision thresholds (≥9.25 APPROVED, ≥9.0 CONDITIONAL, <9.0 REJECTED), two-pass WebSearch strategy (validation + challenge), devil's advocate criticisms (4 subsections: commission errors, omission errors, alternative frameworks, methodological confounds), literature citation table, actionable recommendations, thesis/methods.md integration

### v4/templates/stats_report.md
**Purpose:** Template specification for rq_stats agent statistical validation feedback (10-point rubric with devil's advocate analysis)
**Audience:** rq_stats agent when creating standalone 1_stats.md validation report
**Status:** Current (2025-11-21, updated for standalone file approach)
**Key Topics:** 10-point rubric system (5 categories: statistical appropriateness, tool availability, parameter specification, validation procedures, devil's advocate analysis), decision thresholds (≥9.25 APPROVED, ≥9.0 CONDITIONAL, <9.0 REJECTED), two-pass WebSearch strategy (validation + challenge), devil's advocate criticisms (4 subsections: commission errors, omission errors, alternative approaches, known pitfalls), tool availability validation tables, IRT/LMM assumption checklists, thesis/methods.md integration

### v4/tool_audit.md
**Purpose:** Comprehensive statistical tools and functions inventory across REMEMVR codebase (legacy .archive/v1 + current tools/)
**Audience:** ALL v4.X agents (rq_planner, rq_tools, rq_analysis, g_code, g_debug), main claude when referencing tool capabilities
**Status:** Current (2025-11-22, comprehensive audit)
**Key Topics:** 70+ statistical functions (36 legacy + 34 current), IRT calibration (7 functions), LMM analysis (10 functions), plotting (6 functions), validation (11 functions NEW), Decision implementations (D039 purify_items, D068 post_hoc_contrasts, D069 plot_trajectory_probability, D070 fit_lmm_with_tsvr), function signatures, usage patterns, comparative analysis (v1 vs current), RQ workflow mapping, tool-by-use-case reference, quick reference appendix, migration status, known gaps, 100% coverage for core RQ workflow

### v4/tools_naming.md
**Purpose:** Formulaic naming patterns for tools and functions (8 core patterns: CONVERT, LOAD, RESOLVE, SET, COMPUTE, FIT, PREPARE, COMPARE)
**Audience:** Main claude when adding new functions, ALL agents when referencing tools, developers
**Status:** Current (2025-11-22, v2.0 - 33 functions renamed)
**Key Topics:** 8 formulaic patterns (convert_X_to_Y, load_X_from_Y, resolve_X_from_Y, set_X_Y, compute_X_Y, fit_X_Y, prepare_X_from_Y, compare_X_by_Y), source/target/method explicitness, self-documenting function names, pattern distribution (LOAD=8, EXTRACT=4, FIT=3, COMPUTE=2), quick reference guide, agent communication patterns (rq_planner uses pipelines, rq_analysis uses atomics)

### v4/tools_catalog.md
**Purpose:** Lightweight tool discovery catalog for rq_planner (TIER 1: "What exists?") - 96% lighter than tools_inventory.md
**Audience:** rq_planner agent (planning phase), main claude browsing available tools
**Status:** Current (2025-12-08, added kitchen sink model selection tool)
**Key Topics:** 52 functions across 6 modules (analysis_irt, analysis_lmm, model_selection, plotting, validation, config), one-line descriptions (name + purpose + basic I/O), organized by workflow (IRT calibration, LMM trajectory, model selection, plotting, validation), Decision cross-reference (D039/D068/D069/D070), stdlib exemption list (pandas/numpy/pathlib), missing tools (CTT), ~300 lines total

### v4/tools_inventory.md
**Purpose:** Authoritative API reference for VALIDATED analysis tools (TIER 2: "How do I use it?") - Complete specifications with inputs/outputs/examples
**Audience:** rq_tools, rq_analysis, g_code agents (implementation phase), main claude for precise API details
**Status:** Current (2025-12-08, added kitchen sink model selection tool)
**Key Topics:** 52 validated functions with complete specs (Status, Description, Inputs, Outputs, Model Suite [for model_selection], Interactions, Validation, Use Cases, Examples, Important Notes, References), module organization (tools.analysis_irt, tools.analysis_lmm, tools.model_selection, tools.plotting, tools.validation), Decision implementations (D039/D068/D069/D070), YELLOW/GREEN status only (RED/ORANGE excluded), self-contained API reference for agents

---

**Notes:**
- Main claude MUST update this file when creating/modifying docs
- context-finder searches this index + docs/ directory
- NOT managed by context-manager (docs/ is separate from context system)
- Load documentation on-demand only, do NOT keep in permanent context
