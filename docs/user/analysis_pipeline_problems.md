# Analysis Pipeline Problems - Comprehensive List

**Last Updated:** 2025-11-15 (Post-RQ 5.1 execution)
**Status:** Problems identified, solutions deferred

---

## Problem 1 - Naming Conventions
**Description:** Significant mismatch exists between column/variable names employed by analysis-executor and actual tools suite.
**Cause:** Analysis-executor guesses parameter names from config.yaml instead of reading tools_inventory.md function signatures.
**Effect:** Generated scripts crash with KeyError on missing columns (composite_ID, test vs Test, tsvr vs TSVR_hours, Theta vs Theta_What/Where/When).

## Problem 2 - Unicode Characters
**Description:** Analysis-executor adds Unicode symbols (✓⚠❌✅📊) in programmatic .md file creation and print statements.
**Cause:** Agent generates code without considering Windows cp1252 encoding restrictions.
**Effect:** Scripts crash with UnicodeEncodeError, requiring manual find-replace of all Unicode symbols with ASCII equivalents.

## Problem 3 - Single Script
**Description:** Analysis-executor writes monolithic script to run entire analysis from start to finish.
**Cause:** Agent generates one large analysis_script.py containing all 9 steps sequentially.
**Effect:** Any bug requires restarting entire analysis from Step 1, wasting hours on re-running completed steps (60+ minutes for IRT Pass 1 alone).

## Problem 4 - Verbose Documentation
**Description:** Process generates very large markdown files containing lots of information not needed by various agents.
**Cause:** Agent embeds full methodology explanations, validation checklists, and historical context in every .md file.
**Effect:** Token waste when agents load these files, reduced context space for actual work.

## Problem 5 - Agent Workload
**Description:** Analysis-executor and rq-spec agents required to complete HUGE tasks in single invocation.
**Cause:** Workflow assigns entire RQ specification (8 steps) or entire analysis execution (9 steps) to one agent call.
**Effect:** Quality degradation in generated content, higher probability of errors, agent exhaustion/truncation.

## Problem 6 - API Documentation Ignorance
**Description:** Analysis-executor does not read tools_inventory.md before generating function calls.
**Cause:** Agent prioritizes config.yaml structure over actual tool function signatures documented in tools_inventory.md.
**Effect:** 6 distinct API mismatches discovered (purify_items, fit_lmm_with_tsvr, post_hoc_contrasts, compute_effect_sizes, variable naming, encoding).

## Problem 7 - Config Assumption
**Description:** Agent assumes config.yaml structure without validating against actual schema.
**Cause:** Agent generates code based on mental model of config rather than reading actual config structure.
**Effect:** KeyError crashes when script expects 'dimension_patterns' but config has 'item_mapping' with nested tag_pattern/tag_patterns structure.

## Problem 8 - Case Sensitivity
**Description:** Inconsistent capitalization between data files and function expectations (test vs Test).
**Cause:** No standardization enforced across data-prep outputs and analysis tool inputs.
**Effect:** Column name mismatches causing KeyError crashes requiring manual column renaming in functions.

## Problem 9 - Data Format Mismatch
**Description:** Tools expect specific data formats (long vs wide, univariate vs multivariate) without auto-detection.
**Cause:** IRT calibration outputs multivariate format (['Difficulty', 'Discrim_*']) but purify_items expected univariate format (['factor', 'a', 'b']).
**Effect:** Format incompatibility crashes requiring function rewrites to handle both formats with auto-detection logic.

## Problem 10 - Missing Column Creation
**Description:** Scripts use columns without creating them first (composite_ID from UID + Test).
**Cause:** Agent assumes composite_ID exists in data when it only exists conceptually (must be constructed).
**Effect:** Merge operations fail with 100% missing data warnings, requiring explicit composite_ID = UID + '_' + Test construction.

## Problem 11 - Wide vs Long Format
**Description:** fit_lmm_with_tsvr expects long format theta_scores but receives wide format from IRT Pass 2.
**Cause:** No data reshaping step between IRT output (wide: Theta_What/Where/When) and LMM input (long: Domain, Theta).
**Effect:** Catastrophic merge failure with 100% missing TSVR data and KeyError on 'Theta' column.

## Problem 12 - Cascading Errors
**Description:** Single root error (API mismatch) cascades into 5+ downstream errors discovered sequentially.
**Cause:** No validation layer between script generation and execution, errors only discovered at runtime.
**Effect:** Iterative debugging cycle requiring 6+ script versions (v1→v2→v3→v4) to fix all cascading issues.

## Problem 13 - Git Workflow
**Description:** /save command only committed .claude/context/ files, not .claude/agents/ or tools/.
**Cause:** Original /save implementation used 'git add .claude/context/' instead of 'git add -A'.
**Effect:** Git rollback disasters losing uncommitted agent prompts (v3.0 rq-specification 1571 lines lost, recovered via OneDrive).

## Problem 14 - Incomplete Commits
**Description:** Work documented in state.md but code never committed to git.
**Cause:** Documentation-first workflow where state.md updates happen without corresponding git commits.
**Effect:** False sense of security - work appears saved in context but code is uncommitted and vulnerable to rollbacks.

## Problem 15 - No Testing Before Commit
**Description:** Generated scripts committed/documented without execution testing.
**Cause:** Agent generates code, documents it in state.md, user runs /save, but script never actually run until later.
**Effect:** Bugs discovered hours/days after generation, requiring extensive debugging of already-committed code.

## Problem 16 - Index vs Column
**Description:** Tools store critical data (item_name) in DataFrame index instead of regular columns.
**Cause:** Pandas idiomatic practice using index for row identifiers, but breaks automation workflows.
**Effect:** Data loss when agents save DataFrames with index=False, requiring reset_index() calls for automation robustness.

## Problem 17 - Tool Signature Guessing
**Description:** Agent invents function parameters that don't exist in actual tool signatures.
**Cause:** Agent hallucinates parameters based on task requirements rather than reading actual function definitions.
**Effect:** TypeError crashes on unexpected keyword arguments (num_comparisons, effect_type, save_models that don't exist).

## Problem 18 - Missing Encoding Specification
**Description:** File operations lack encoding='utf-8' parameter, defaulting to Windows cp1252.
**Cause:** Agent generates file read/write code without explicit encoding parameter.
**Effect:** UnicodeDecodeError on config.yaml reads, UnicodeEncodeError on .md writes with special characters.

## Problem 19 - Unbuffered Output Missing
**Description:** Python scripts run without -u flag, buffering output for 60+ minute processes.
**Cause:** Agent generates subprocess commands as 'python script.py' instead of 'python -u script.py'.
**Effect:** No real-time monitoring of long-running processes, appears frozen until completion/crash.

## Problem 20 - No Validation Gates
**Description:** No intermediate validation between script generation and execution.
**Cause:** Workflow jumps directly from agent-generated code to background execution without syntax/import/API checks.
**Effect:** Runtime errors discovered hours into execution, wasting computation time and requiring full restarts.

## Problem 21 - Documentation Bloat
**Description:** Companion .md files contain 50-100 lines of boilerplate methodology text.
**Cause:** Agent generates comprehensive documentation including purposes, structures, statistics, methodologies, next steps.
**Effect:** Thousands of tokens consumed by redundant information when multiple files loaded, reducing working context space.

## Problem 22 - No Error Recovery
**Description:** Scripts have no try/except blocks or checkpointing for graceful degradation.
**Cause:** Agent generates linear execution flow without error handling or state persistence.
**Effect:** Single error aborts entire analysis, no partial results saved, complete restart required.

## Problem 23 - Column Name Hardcoding
**Description:** Functions hardcode expected column names without checking actual DataFrame structure.
**Cause:** Functions written with specific assumptions about input format rather than defensive programming.
**Effect:** Brittle code breaks when data structure varies slightly (test vs Test, tsvr vs TSVR_hours).

## Problem 24 - No Format Auto-Detection
**Description:** Functions cannot automatically detect input data format (univariate vs multivariate, wide vs long).
**Cause:** Tools designed for single format without introspection logic to adapt to variations.
**Effect:** Manual format detection and transformation required, or function rewrites to handle multiple formats.

---

## Meta-Observations

**Pattern 1 - Documentation-Reality Gap:** Agent reads documentation (tools_inventory.md, config schema) inadequately or not at all, generating code based on assumptions.

**Pattern 2 - Cascading Failures:** Single architectural mismatch (e.g., wide vs long format) triggers 5+ downstream errors discovered sequentially through iterative debugging.

**Pattern 3 - Platform Assumptions:** Agent generates code for generic UNIX/UTF-8 environment, breaking on Windows-specific constraints (cp1252 encoding, path separators).

**Pattern 4 - Monolithic Design:** Single-script, single-invocation design prevents resumability, partial execution, incremental testing, and graceful error recovery.

**Pattern 5 - Quality vs Scope Tradeoff:** Larger agent tasks (8-step RQ spec, 9-step analysis execution) correlate with lower quality outputs and higher error rates.

---

**Total Problems Identified:** 24 distinct issues across 5 meta-patterns
**Next Step:** Solution design and prioritization (deferred)
