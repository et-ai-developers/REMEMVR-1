# Agent Standard Procedure v3.0 Development

**Topic:** agent_standard_procedure_v3
**Description:** Complete overhaul of RQ standard procedure from v2.0 to v3.0, including ultrathink analysis identifying 15 critical vagueness issues, stateful agent design, universal templates, hybrid safety gates, and comprehensive template system creation.

---

## Session (2025-11-12 16:00) - RQ Standard Procedure v3.0 Complete Overhaul

**Archived from:** state.md
**Original Date:** 2025-11-12 16:00
**Reason:** Completed work, standards documented in docs/, templates created, incorporated into agent prompts in subsequent sessions

### Context

User requested standard procedure for building RQs with emphasis on eliminating ALL vagueness and standardization for 50-RQ automation. Previous v2.0 lacked stateful agent design, used JSON reports, and had numerous ambiguities that would cause compounding errors.

### Ultrathink Analysis Performed

Comprehensive deep analysis of rq_standard_procedure.md v2.0 identified **15 critical issues** requiring fundamental decisions:

1. **Report Format:** JSON vs Markdown - DECISION: Markdown (human-readable, thesis-appropriate, version control friendly)
2. **Safety Audit Automation (Step 5):** Script vs manual vs hybrid - DECISION: Hybrid (I inspect automatically, user approves)
3. **Output Verification Automation (Step 7):** Script vs manual vs hybrid - DECISION: Hybrid (I perform forensic inspection, user confirms)
4. **Analysis Instructions Source:** config.yaml vs info.md vs both - DECISION: Keep config.yaml (machine-readable parameters + tool_functions mapping eliminates ambiguity)
5. **info.md Template Definition:** NEEDED - Created comprehensive 10-section universal template
6. **config.yaml Schema Definition:** NEEDED - Created with tool_functions mapping for analysis-executor
7. **RQ-Spec Context Dump Format:** NEEDED - Created structured format (not raw reasoning dump)
8. **Agent Report Templates:** NEEDED - Created 5 templates (scholar, statistics, data_prep, analysis_executor, results_inspector)
9. **Validation Rubrics:** Embedded in report templates with 10-point scoring systems
10. **Stateful RQ-Spec Agent Design:** USER'S BRILLIANT IDEA - Agent maintains context across invocations via logs/rq_spec_context.md
11. **Iteration Limits:** No hard limit, agent runs as many times as master invokes it
12. **Conflicting Validation Feedback:** User reviews and decides which argument wins
13. **Migration Strategy:** RQ-spec agent handles migration (TDD feature for future changes)
14. **Tool Requirements Discovery:** config.yaml explicitly lists required tools in tool_functions section
15. **Data Dimensions Specification:** info.md Section 4 (Input Data) explicitly states expected dimensions

### Key User Clarifications

- **Markdown over JSON:** All reports now .md format (human-readable, thesis examiners can read directly)
- **Hybrid Safety Gates:** Automated checks + user approval at critical risk points (Steps 5, 7)
- **Keep config.yaml:** Separate machine-readable parameters from human narrative in info.md, prevents conflicts
- **info.md Structure (10 sections):**
  1. Status (phase tracking table)
  2. Research Question (verbatim)
  3. Hypotheses (with scholar agent references)
  4. Input Data (EXECUTABLE specs for data-prep - exact tags, dimensions, filters)
  5. Method (tool-by-tool procedure for analysis-executor)
  6. Validation (procedures + results - both sections)
  7. Plots (specifications for future plotting agent)
  8. Statistical Audit #2 (placeholder for post-analysis)
  9. Results (added by results-inspector)
  10. Theoretical Implications (added by scholar after verified results)
- **Context Dump Format:** Structured sections (Draft Phase, Finalization Phase, Iteration N) with decisions, rationale, open questions
- **Universal Templates:** NOT locked to IRT/LMM - adapt based on analysis type (CTT, correlation, ANOVA, regression, descriptive)

### Files Created (9 files in docs/templates/)

**1. info_template.md (~3k tokens)**
- 10-section universal template with HTML comment noting IRT/LMM are examples
- Section 4 (Input Data) has EXECUTABLE specifications format
- Section 5 (Method) has step-by-step tool procedures
- Section 6 (Validation) has both procedures and results sections
- Status section at top for phase tracking

**2. config_schema.yaml (~2.5k tokens)**
- Universal template with metadata, analysis parameters, tool_functions mapping
- **CRITICAL tool_functions section:** Explicit step-by-step pipeline eliminating ambiguity:
  ```yaml
  tool_functions:
    step_1_[name]:
      function: "tools.module.function"
      input_file: "data/input.csv"
      output_files: ["data/output1.csv", "data/output2.csv"]
      config_section: "section_name"
  ```
- Analysis-executor reads this to know exactly which tool to call, inputs to use, outputs to create
- Includes sections for IRT, LMM, CTT, data prep, plotting (adapt based on RQ needs)
- Top comment emphasizes universality: "Delete irrelevant sections"

**3. rq_spec_context_template.md (~2k tokens)**
- Structured format for stateful rq-spec agent context dumps
- Draft Phase section: Decisions Made, Rationale, Open Questions, Files Created
- Finalization Phase section: Prior Context Recap, Validation Feedback Review, Changes Implemented, Quality Check
- Iteration 3+ section: Reason for re-invocation, changes made
- Agent reads this on every invocation to maintain continuity

**4. scholar_report_template.md (~2k tokens)**
- Markdown report format (not JSON)
- 10-point rubric: Theoretical Grounding (3), Literature (2), Interpretation (2), Implications (2), Rebuttals (1)
- Detailed feedback sections for each rubric item
- Literature search results with citations to add
- Decision: APPROVED (≥9.25) / CONDITIONAL (9.0-9.24) / REJECTED (<9.0)
- Required changes vs suggested improvements

**5. statistics_report_template.md (~2k tokens)**
- Markdown report format
- 10-point rubric: Statistical Appropriateness (3), Tool Availability (2), Parameters (2), Validation (2), Complexity (1)
- Tool inventory cross-reference with availability checklist
- Parameter appropriateness assessment
- Missing tools section (if any)
- Updates docs/tools_inventory.md with RQ-tool mapping

**6. data_prep_report_template.md (~3k tokens)**
- Markdown report format
- Execution steps: Load → Extract → Filter → Validate → Save
- **CRITICAL Safety Verification section:** "Did agent generate mock data?" (MUST be NO)
- Data summary with descriptive statistics
- Prohibited files check (no theta_scores.csv, no mock files)
- Next steps for analysis-executor

**7. analysis_executor_report_template.md (~3k tokens)**
- Markdown report format
- Step-by-step execution log (IRT calibration, reshaping, LMM, validation, plots)
- Tool usage summary (functions called, versions, duration)
- **No improvisation check:** All tools from tools/ package (no custom functions)
- Convergence status, quality checks
- Validation results (assumptions tested, violations found)

**8. results_inspector_report_template.md (~3k tokens)**
- Markdown report format
- Statistical correctness validation (IRT + LMM parameter ranges, p-values, effect sizes)
- Completeness check (all required outputs present?)
- Interpretation quality assessment
- Scholarly summary with publication readiness evaluation
- Decision: APPROVED / CONDITIONAL / REJECTED

**9. agent_reports/ directory created** with all report templates

### Documents Updated

**1. rq_standard_procedure.md → v3.0 (complete rewrite, ~15k tokens)**

Key improvements:
- **Stateful rq-spec agent design** with context dumps (maintains continuity across invocations)
- **All JSON → Markdown** for reports (scholar_report.md, statistics_report.md, data_prep_report.md, analysis_executor_report.md, results_inspector_report.md, status.md)
- **Hybrid safety audits** at Steps 5 and 7 (automated checks + user approval)
- **Universal templates** (not locked to IRT/LMM - explicitly noted in Prerequisites and Step 1)
- **11 steps total** (8 current + 3 future): Specification → Scholar → Statistics → Finalization → Safety Audit → Data Prep → Output Verification → Analysis → Results Validation → Theoretical Implications → Final Statistical Audit

**Step 1 (Specification Draft):** Agent behavior detailed - scans folder structure, determines phase from file existence, maintains context via logs/rq_spec_context.md

**Step 4 (Finalization):** Agent reads prior context + validation reports, checks for conflicts (if conflicting feedback → user resolves), incorporates changes, documents all changes in logs/rq_specification_report.md

**Step 5 (Safety Audit - NEW):** Master performs 5 automated checks on info.md Section 4:
1. Data Prep Section Structure (separates raw from derived data?)
2. Primary Source Declaration (master.xlsx vs IRT output?)
3. Variables Required List (all extractable from master.xlsx?)
4. Expected Dimensions Specified (explicit dimensions for validation?)
5. Analysis Pipeline Clear (Step 1 data-prep → Step 2 IRT sequence?)
- Generates audit report with PROCEED/BLOCK recommendation
- User MUST approve before data-prep runs

**Step 7 (Output Verification - NEW):** Master performs 5 forensic checks after data-prep:
1. Files Created Match Report (no unexpected CSVs?)
2. Companion .md Files Exist (every CSV documented?)
3. No Mock Data Keywords (searches .md for "mock", "placeholder", "temporary", "fake", "simulated", "proxy")
4. Data Provenance Clear (extraction from master.xlsx documented?)
5. File Sizes Reasonable (match info.md expected dimensions?)
- Generates verification report with CLEAN/CONTAMINATED status
- User MUST confirm before analysis-executor runs

**Step 8 (Analysis Execution):** Analysis-executor reads config.yaml tool_functions section for explicit step-by-step pipeline, eliminating all ambiguity about which tool to call

**File Format Standards section:** Explains why Markdown (human-readable, thesis-appropriate, version control friendly) NOT JSON (machine-readable but human-hostile, inappropriate for PhD thesis artifacts)

**Version history:** v1.0 (led to RQ 5.5 mock data catastrophe) → v2.0 (added safety gates but lacked stateful agent) → v3.0 (stateful agent, Markdown, hybrid audits, universal templates, all ultrathink clarifications)

**2. rq_file_structure_ground_truth.md (JSON → Markdown conversion)**

- All references to .json files changed to .md (scholar_report.md, statistics_report.md, etc.)
- status.json → status.md (Markdown table format)
- Remaining .json references are only in "FORBIDDEN" sections (explaining what NOT to use)
- File location rules updated to reflect Markdown format
- Companion .md requirements emphasized (every CSV must have companion .md)

**3. Templates updated with universality notes:**

- info_template.md: Added HTML comment at top: "IMPORTANT: UNIVERSAL TEMPLATE. This template shows IRT + LMM pipeline as an EXAMPLE only. Adapt sections based on your RQ's analysis type..."
- config_schema.yaml: Added comments section: "IMPORTANT: UNIVERSAL TEMPLATE. This template shows IRT + LMM pipeline as an EXAMPLE. NOT ALL RQs use IRT or LMM - adapt sections based on analysis_types. Other analysis types: CTT, correlation, ANOVA, regression, descriptive..."

**4. docs_index.md updated:**

- Last Updated: 2025-11-12 (Post-Ultrathink Updates)
- rq_workflow.md marked as "Superseded by rq_standard_procedure.md (lacks safety gates)"
- Added rq_standard_procedure.md entry: "Complete 8-step procedure with safety gates, verification checkpoints, user approval requirements (v3.0)"
- Added rq_file_structure_ground_truth.md entry: "ABSOLUTE GROUND TRUTH for RQ file/folder structure - mandatory for all agents (v2.0 - all agents must follow exactly)"
- results_schema.md marked as "Superseded by rq_file_structure_ground_truth.md (outdated, inconsistent with reality)"

### Decisions Made

**Decision D056** (2025-11-12 16:00): Keep config.yaml Separate from info.md
- **Context:** Ultrathink analysis questioned whether config.yaml is redundant with info.md
- **Decision:** KEEP config.yaml as separate file from info.md
- **Rationale:**
  - **Separation of concerns:** info.md = human narrative (WHY), config.yaml = machine parameters (WHAT)
  - **Parsing efficiency:** Analysis-executor loads YAML directly (1 line: `config = yaml.safe_load()`) vs parsing markdown
  - **Parameter extraction:** YAML guarantees exact values, markdown requires regex that could fail
  - **Conflict prevention:** config.yaml is THE authoritative parameter source, info.md explains reasoning
  - **Tool Function Mapping:** config.yaml has explicit step-by-step pipeline that eliminates ALL ambiguity for analysis-executor
- **Impact:**
  - Analysis-executor reads config.yaml directly for parameters
  - info.md references config.yaml ("see config.yaml for IRT parameters") instead of duplicating
  - tool_functions section in config.yaml tells analysis-executor exactly: which function, which inputs, which outputs, which config section
  - Example:
    ```yaml
    tool_functions:
      step_1_irt_calibration:
        function: "tools.analysis_irt.calibrate_grm"
        input_file: "data/irt_input.csv"
        output_files: ["data/item_parameters.csv", "data/theta_scores.csv"]
        config_section: "irt"
    ```
- **Alternative Considered:** Merge all into info.md - REJECTED because requires markdown parsing for parameter extraction, risk of info.md growing to 8k+ tokens, harder to validate parameters programmatically

**Decision D057** (2025-11-12 16:00): Stateful RQ-Spec Agent via Context Dumps
- **Context:** USER'S BRILLIANT IDEA - Original v2.0 assumed stateless agent with 2 distinct phases (draft, finalization), but no memory between invocations
- **Decision:** RQ-spec agent maintains continuity via logs/rq_spec_context.md file that persists across invocations
- **Rationale:**
  - **Stateless problem:** Finalization phase agent has no memory of draft phase decisions, could make inconsistent changes
  - **Stateful solution:** Agent reads its own prior reasoning from logs/rq_spec_context.md on every invocation
  - **Self-diagnostic:** Agent scans folder structure to determine phase (no validation reports = draft, both reports exist = finalization)
  - **Unlimited iterations:** Can run >2 times if needed (not hard limited to draft + finalization)
- **Implementation:**
  - Agent scans RQ folder on every invocation
  - Checks if logs/rq_spec_context.md exists → reads prior context if yes
  - Checks if validation/scholar_report.md and validation/statistics_report.md exist → determines phase
  - Executes appropriate phase (draft or finalization)
  - Appends current reasoning to logs/rq_spec_context.md
  - Format: Structured sections (not raw reasoning dump) with Decisions Made, Rationale, Open Questions
- **Benefits:**
  - Agent recalls why it made each decision
  - Can iterate indefinitely without losing context
  - Master can read logs/rq_spec_context.md to understand agent's reasoning
  - TDD feature: If we change RQ standard again in future, agent can handle migration

**Decision D058** (2025-11-12 16:00): Universal Templates (Not IRT/LMM-Locked)
- **Context:** Initial templates showed only IRT + LMM pipeline, but not all 50 RQs use these analyses
- **Decision:** Make all templates universal with IRT/LMM as examples, explicit instructions to adapt
- **Rationale:**
  - 50 RQs span different analysis types: IRT, LMM, CTT, correlation, ANOVA, regression, descriptive
  - Locking templates to IRT/LMM would force inappropriate methodology or require multiple template versions
  - Better: Single universal template with clear adaptation guidance
- **Implementation:**
  - info_template.md: HTML comment at top explaining IRT/LMM are examples, lists other analysis types
  - config_schema.yaml: Top comments section explaining universality, instruction to delete irrelevant sections
  - rq_standard_procedure.md: Prerequisites explicitly state "Templates available" and Step 1 notes "universal template, adapted to RQ's analysis type"
  - Section 5 (Method) and Section 6 (Validation) adapt based on analysis type
  - config.yaml analysis_types field: ["irt", "lmm"] or ["ctt"] or ["correlation"] etc.
- **Other Analysis Types Documented:**
  - CTT: Classical Test Theory (reliability, item analysis)
  - Correlation: Pearson/Spearman correlations
  - ANOVA: Between/within-subjects designs
  - Regression: Linear/logistic regression
  - Descriptive: Descriptive statistics only

### Key Principles Established

**1. Zero Tolerance for Vagueness:**
- Every ambiguity identified in ultrathink analysis was resolved with explicit specifications
- Templates provide concrete examples, not abstract descriptions
- config.yaml tool_functions section eliminates "which tool?" ambiguity
- info.md Section 4 provides executable specifications (exact tags, dimensions, filters)

**2. Human-Readable Thesis Artifacts:**
- All reports Markdown (not JSON)
- Thesis examiners can read directly
- Version control friendly (git diffs work)
- Documentation appropriate for PhD thesis

**3. Stateful Agents:**
- RQ-spec agent maintains context via logs/rq_spec_context.md
- Can iterate indefinitely without losing continuity
- Self-diagnostic (scans structure to determine phase)

**4. Hybrid Safety Gates:**
- Automated checks provide consistency
- User approval provides PhD-level oversight
- Master performs forensic inspection + reports findings
- User makes final decisions

**5. Universal Standardization:**
- One template system for all 50 RQs
- Adapt based on analysis type (not multiple template versions)
- Clear guidance on adaptation

### Files Modified This Session

**Created (9 files):**
- docs/templates/info_template.md
- docs/templates/config_schema.yaml
- docs/templates/rq_spec_context_template.md
- docs/templates/agent_reports/scholar_report_template.md
- docs/templates/agent_reports/statistics_report_template.md
- docs/templates/agent_reports/data_prep_report_template.md
- docs/templates/agent_reports/analysis_executor_report_template.md
- docs/templates/agent_reports/results_inspector_report_template.md
- docs/templates/agent_reports/ (directory)

**Updated (3 files):**
- docs/rq_standard_procedure.md (v2.0 → v3.0, complete rewrite, ~15k tokens)
- docs/rq_file_structure_ground_truth.md (JSON → Markdown conversion)
- docs/docs_index.md (updated with new entries, marked superseded docs)

### Token Budget
- Session start: ~90k/200k (45%) after user opened files
- Current: ~116k/200k (58%)
- Plenty of room for agent prompt audits in next session

### Quality Achieved
- All 15 ultrathink vagueness issues resolved
- Comprehensive template system created (9 templates covering all RQ workflow aspects)
- Standard procedure v3.0 is publication-quality documentation
- Zero ambiguity for agent execution
- PhD thesis-appropriate artifacts (Markdown, human-readable)

---
