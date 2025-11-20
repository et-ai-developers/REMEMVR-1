# Refactor Overview

**Last Updated:** 2025-01-11
**Purpose:** Explains the rationale for the refactor, core principles, and high-level workflow
**Audience:** Main claude when understanding refactor context
**Status:** Current

---

## REFACTOR GOALS

### Current State (OLD PIPELINE):
- Monolithic scripts (irt.py, analysis.py) running bulk analyses
- Results scattered across folders with inconsistent naming
- Hard to verify correctness of individual research questions
- Difficult to reproduce specific analyses

### Target State (NEW AGENT-BASED PIPELINE):
- Modular analysis tools (CLI-accessible functions)
- Agent-driven sequential execution with validation at each step
- Structured results schema per research question
- Full audit trail (terminal logs, validation reports, draft write-ups)

### Refactor Principles:
1. **User must understand everything** - No black-box analysis
2. **One RQ at a time** - Sequential, not bulk
3. **Validation at every step** - Inspector agent checks outputs before proceeding
4. **Full transparency** - All decisions logged and explainable
5. **Manual approval gates** - Critical decisions (methodology, interpretation) require user input

---

## REFACTOR WORKFLOW (HIGH-LEVEL)

### Phase 1: Tool Suite Development
1. Audit existing functions in irt.py, analysis.py, tools.py
2. Extract reusable functions into modular tools (data_prep.py, lmm_tools.py, etc.)
3. Create CLI wrappers for each tool
4. Write unit tests for critical functions
5. Document each tool's inputs/outputs/purpose

### Phase 2: Agent System Setup
1. Define agent prompts and contexts
2. Create report schemas (JSON format)
3. Test single-RQ workflow manually
4. Implement error handling and rollback procedures

### Phase 3: RQ Execution
1. Start with simple RQs (e.g., 5.1: domain forgetting trajectories)
2. Run data-prep → analysis-executor → results-inspector pipeline
3. User reviews results before proceeding to next RQ
4. Iterate and refine tools/agents based on learnings

### Phase 4: Integration (FUTURE)
1. Thesis-manager agent generates suggested edits
2. Plot-maker agent standardizes visualizations
3. Cross-RQ synthesis and chapter-level summaries

---

## IMPORTANT: USER APPROVAL GATES

**Master agent MUST ask user before:**
1. Running any statistical analysis for the first time on an RQ
2. Choosing between competing methodologies (e.g., which model formula to use)
3. Interpreting ambiguous results
4. Modifying core analysis tools
5. Proceeding after an agent reports an error

**Principle:** This is the user's PhD thesis. They must understand and approve every decision.
