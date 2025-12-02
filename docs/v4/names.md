# V4.X Naming Convention Registry

**Last Updated:** 2025-11-20
**Purpose:** Live registry of naming conventions for v4.X RQ analysis pipeline
**Status:** POPULATED (33 conventions from RQ 5.1 - 8 step_names, 14 file_names, 11 variable_names)
**Version:** 4.0

---

## PURPOSE

This file serves as the **naming convention registry** for the v4.X atomic agent architecture. It provides standardized naming patterns for:

- **Analysis steps** - Consistent step naming across all 50 RQs
- **File names** - Data files, scripts, outputs, logs
- **Variable names** - DataFrame columns, intermediate variables
- **Plot names** - Visualization output files

**Why this exists:** Ensures consistency across all RQs, prevents naming conflicts, enables agents (rq_planner, rq_tools, rq_analysis) to generate standardized code/documentation.

---

## TDD APPROACH

**This file starts EMPTY** per Test-Driven Development philosophy.

**Expected Behavior:**
1. **RQ 5.1 (first RQ) WILL FAIL** when rq_tools (step 9) attempts to look up naming conventions
2. Failure is INTENTIONAL - conventions should emerge from actual needs, not speculation
3. Master and user will MANUALLY add required naming conventions during RQ 5.1 execution
4. Subsequent RQs (5.2, 5.3, ..., 7.20) will reference this registry for existing conventions OR add new ones with user approval

**Philosophy:** Build conventions bottom-up from real requirements, not top-down from assumptions.

---

## USAGE INSTRUCTIONS

**When building a new RQ:**

1. **CHECK REGISTRY FIRST** - Search existing conventions below for matching patterns
2. **REUSE when possible** - If convention exists, use it exactly as specified (promotes consistency)
3. **ADD when needed** - If no matching convention exists, propose new convention following format below
4. **DOCUMENT RQ introduced** - Always record which RQ first required the convention (enables traceability)
5. **GET USER APPROVAL** - New conventions require master + user agreement before adding to registry

**What agents do:**
- `rq_planner` reads this file to suggest step names, file names, variable names in 2_plan.md
- `rq_tools` reads this file to validate naming patterns specified in 3_tools.yaml
- `rq_analysis` reads this file to enforce naming consistency in 4_analysis.yaml

---

## CONVENTION RULES

**NEVER modify existing conventions** - Changing a convention breaks compatibility with all past RQs that use it

**ONLY append new conventions** - Add new entries to appropriate category section below

**Preserve format exactly** - Follow YAML structure specified below for all new entries

**Rationale:** Naming consistency across 50 RQs is CRITICAL for:
- Code reusability (functions expect specific column names)
- Documentation clarity (step names referenced across multiple files)
- Debugging efficiency (standardized file names enable quick location)
- Scientific reproducibility (exact variable names in published results)

---

## CONVENTIONS

**Format:** YAML structure organized by category

**Categories:**
- `step_names` - Analysis step naming patterns
- `file_names` - Data file, script file, output file naming patterns
- `variable_names` - DataFrame column, variable naming patterns
- `plot_names` - Plot file naming patterns

**Entry Fields:**
- `name` - Identifier for the convention type
- `pattern` - Format template with placeholders (e.g., `stepNN_<verb>_<noun>`)
- `example` - Concrete instance demonstrating pattern
- `introduced` - Which RQ first required this convention (e.g., `RQ 5.1`)
- `notes` - Optional clarifications or usage context

**Example Entry Structure:**
```yaml
step_names:
  - name: calibration
    pattern: stepNN_<verb>_<noun>
    example: step01_calibrate_irt
    introduced: RQ 5.1
    notes: "IRT model calibration using GRM"
```

**IMPORTANT: Step Numbers Are RQ-Specific (Not Global)**

Step numbers (step00, step01, step02, etc.) indicate **file generation order within a single RQ**, NOT a global analysis sequence across all RQs.

- ✅ **RQ 5.1** might have: step01 = IRT calibration, step02 = purification
- ✅ **RQ 6.3** might have: step01 = cognitive test extraction, step02 = correlation matrix
- ✅ **RQ 7.8** might have: step00 = demographics, step01 = t-test (no IRT at all)

**The conventions below are EXAMPLES from RQ 5.1**, not requirements for all RQs. Different RQs will have different analysis pipelines and can reuse step numbers for completely different tasks.

**What IS consistent:** The pattern format (stepNN_verb_noun), NOT the task assigned to each step number.

---

### Step Names

```yaml
step_names:
  - name: data_extraction
    pattern: step00[a-z]?_extract_<source>_data
    example: step00_extract_vr_data, step00a_extract_tsvr_data
    introduced: RQ 5.1
    notes: "Extract data from master.xlsx using domain-specific tag patterns. Use lowercase letter suffix (step00a_, step00b_) for multiple extractions at same step level."

  - name: irt_calibration_pass1
    pattern: step01_irt_calibration_pass1
    example: step01_irt_calibration_pass1
    introduced: RQ 5.1
    notes: "IRT calibration on all items (Decision D039 - 2-pass purification, first pass)"

  - name: item_purification
    pattern: step02_purify_items
    example: step02_purify_items
    introduced: RQ 5.1
    notes: "Filter items by thresholds |b|≤3.0, a≥0.4 per Decision D039"

  - name: irt_calibration_pass2
    pattern: step03_irt_calibration_pass2
    example: step03_irt_calibration_pass2
    introduced: RQ 5.1
    notes: "IRT calibration on purified items (Decision D039 - final pass)"

  - name: tsvr_merge
    pattern: step04_merge_theta_tsvr
    example: step04_merge_theta_tsvr
    introduced: RQ 5.1
    notes: "Merge theta scores with TSVR time variable per Decision D070 (actual hours, not nominal days)"

  - name: lmm_fitting
    pattern: step05_fit_lmm
    example: step05_fit_lmm
    introduced: RQ 5.1
    notes: "Fit Linear Mixed Model (trajectories, cross-sectional, or other designs). Specify model type in plan."

  - name: post_hoc_contrasts
    pattern: step06_compute_post_hoc_contrasts
    example: step06_compute_post_hoc_contrasts
    introduced: RQ 5.1
    notes: "Post-hoc group comparisons with dual p-value reporting per Decision D068"

  - name: plot_data_preparation
    pattern: step07_prepare_<plottype>_plot_data
    example: step07_prepare_trajectory_plot_data
    introduced: RQ 5.1
    notes: "Create plot source CSVs (Option B architecture). Use step07a_, step07b_ for multiple plots. Decision D069 requires dual-scale for trajectories."
```

---

### File Names

```yaml
file_names:
  # =============================================================================
  # FOLDER STRUCTURE (v4.1 - Aligned 2025-12-02)
  # =============================================================================
  # /code   = ALL .py code files for running analysis
  # /data   = ALL inputs AND outputs from analysis steps (intermediate + final)
  # /docs   = ALL planning documentation (1_concept.md, 2_plan.md, 3_tools.yaml, 4_analysis.yaml, validation reports)
  # /logs   = ONLY .log files (execution logs from each step - stdout/stderr capture)
  # /plots  = EMPTY until rq_plots generates PNG/PDF visualizations
  # /results = EMPTY until rq_results generates summary.md
  # =============================================================================

  # Data files - ALL analysis inputs and outputs go here
  - name: irt_input
    pattern: data/step00_irt_input.csv
    example: data/step00_irt_input.csv
    introduced: RQ 5.1
    notes: "Wide-format IRT input from extraction (composite_ID x item columns). Step 00 prefix for clear ordering."

  - name: pass1_item_params
    pattern: data/step01_pass1_item_params.csv
    example: data/step01_pass1_item_params.csv
    introduced: RQ 5.1
    notes: "Pass 1 IRT item parameters (before purification). Used to identify items for exclusion. Step 01 prefix."

  - name: pass1_theta
    pattern: data/step01_pass1_theta.csv
    example: data/step01_pass1_theta.csv
    introduced: RQ 5.1
    notes: "Pass 1 theta estimates (diagnostic, used for purification decisions). Step 01 prefix."

  - name: purified_items
    pattern: data/step02_purified_items.csv
    example: data/step02_purified_items.csv
    introduced: RQ 5.1
    notes: "List of items retained after purification (Decision D039 thresholds applied). Step 02 prefix."

  - name: purification_report
    pattern: data/step02_purification_report.txt
    example: data/step02_purification_report.txt
    introduced: RQ 5.1
    notes: "Text report listing excluded items with reasons (low discrimination or extreme difficulty). Step 02 prefix."

  - name: item_parameters
    pattern: data/step03_item_parameters.csv
    example: data/step03_item_parameters.csv
    introduced: RQ 5.1
    notes: "Final IRT item parameters from Pass 2 calibration. Columns: item_name, dimension, a, b. Step 03 prefix."

  - name: theta_scores
    pattern: data/step03_theta_scores.csv
    example: data/step03_theta_scores.csv
    introduced: RQ 5.1
    notes: "Final IRT ability estimates from Pass 2. Columns: composite_ID, theta per dimension, SE per dimension. Step 03 prefix."

  - name: lmm_input
    pattern: data/step04_lmm_input.csv
    example: data/step04_lmm_input.csv
    introduced: RQ 5.1
    notes: "Long-format LMM input (one row per observation). Includes theta + TSVR per Decision D070. Step 04 prefix."

  - name: lmm_model_summary
    pattern: data/step05_lmm_model_summary.txt
    example: data/step05_lmm_model_summary.txt
    introduced: RQ 5.1
    notes: "LMM fitted model summary (fixed effects, random effects, fit indices). Step 05 prefix."

  - name: post_hoc_contrasts
    pattern: data/step06_post_hoc_contrasts.csv
    example: data/step06_post_hoc_contrasts.csv
    introduced: RQ 5.1
    notes: "Post-hoc pairwise comparisons with BOTH uncorrected and Bonferroni p-values (Decision D068). Step 06 prefix."

  - name: effect_sizes
    pattern: data/step06_effect_sizes.csv
    example: data/step06_effect_sizes.csv
    introduced: RQ 5.1
    notes: "Effect size estimates (Cohen's d, partial eta-squared) for contrasts. Step 06 prefix (same step as contrasts)."

  - name: trajectory_theta_data
    pattern: data/step07_trajectory_theta_data.csv
    example: data/step07_trajectory_theta_data.csv
    introduced: RQ 5.1
    notes: "Plot source CSV for theta-scale trajectory (Decision D069 dual-scale requirement). Step 07 prefix. rq_plots reads from data/, writes PNG to plots/."

  - name: trajectory_probability_data
    pattern: data/step07_trajectory_probability_data.csv
    example: data/step07_trajectory_probability_data.csv
    introduced: RQ 5.1
    notes: "Plot source CSV for probability-scale trajectory (Decision D069 dual-scale requirement). Step 07 prefix. rq_plots reads from data/, writes PNG to plots/."

  # Log files - ONLY execution logs (.log files capturing stdout/stderr)
  - name: step_execution_log
    pattern: logs/stepNN_<step_name>.log
    example: logs/step01_irt_calibration_pass1.log
    introduced: RQ 5.1
    notes: "Execution log capturing stdout/stderr from running stepNN_<name>.py. One .log per .py script."
```

---

### Variable Names

```yaml
variable_names:
  # Core identifier columns
  - name: composite_id
    pattern: composite_ID
    example: composite_ID
    introduced: RQ 5.1
    notes: "Primary key combining UID and test (format: UID_test). Used throughout IRT and LMM pipelines."

  - name: participant_uid
    pattern: UID
    example: UID
    introduced: RQ 5.1
    notes: "Participant unique identifier (format: P### with leading zeros)"

  - name: test_session
    pattern: test
    example: test
    introduced: RQ 5.1
    notes: "Test session identifier (T1, T2, T3, T4 for Days 0, 1, 3, 6)"

  # Time variable (Decision D070)
  - name: tsvr_time
    pattern: TSVR_hours
    example: TSVR_hours
    introduced: RQ 5.1
    notes: "Time Since VR in hours (actual elapsed time, NOT nominal days 0/1/3/6). Decision D070 requirement for LMM."

  # IRT outputs
  - name: theta_score
    pattern: theta_<dimension>
    example: theta_common
    introduced: RQ 5.1
    notes: "IRT latent ability estimate for given dimension. Multiple theta columns for multidimensional IRT."

  - name: theta_se
    pattern: se_<dimension>
    example: se_common
    introduced: RQ 5.1
    notes: "Standard error of theta estimate for given dimension"

  - name: item_discrimination
    pattern: a
    example: a
    introduced: RQ 5.1
    notes: "IRT item discrimination parameter (slope). Must be > 0."

  - name: item_difficulty
    pattern: b
    example: b
    introduced: RQ 5.1
    notes: "IRT item difficulty parameter (location). Unrestricted range (temporal items can have |b| > 3.0)."

  # LMM/plotting columns
  - name: domain_factor
    pattern: domain
    example: domain
    introduced: RQ 5.1
    notes: "Memory domain factor (What, Where, When) for grouping/plotting"

  - name: confidence_interval_lower
    pattern: CI_lower
    example: CI_lower
    introduced: RQ 5.1
    notes: "Lower bound of 95% confidence interval for plots"

  - name: confidence_interval_upper
    pattern: CI_upper
    example: CI_upper
    introduced: RQ 5.1
    notes: "Upper bound of 95% confidence interval for plots"
```

---

### Plot Names

```yaml
plot_names:
  # EMPTY - Awaiting RQ 5.1 population
  # Format: List of plot file naming conventions
  # Add entries here as conventions are discovered during RQ execution
```

---

## MAINTENANCE NOTES

**History:**
- 2025-11-16: File created (F3) - Empty TDD initialization
- 2025-11-16: Design decisions F0a-F0b approved (header structure + YAML format)
- 2025-11-20: RQ 5.1 naming conventions added (8 step_names, 14 file_names, 11 variable_names) during Phase 21 testing
- 2025-12-02: v4.1 folder structure alignment - ALL outputs to data/, logs/ for .log only, plots/ empty until rq_plots, results/ empty until rq_results

**Future Additions:**
- All conventions added during RQ 5.1-7.20 execution will be documented above with timestamps
- Each addition should update this maintenance section noting: date, RQ, convention added

---

**End of Naming Registry**
