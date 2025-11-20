# tools.md Template Specification

**Version:** 4.0
**Last Updated:** 2025-11-16
**Purpose:** Specification for 3_tools.yaml format (analysis + validation tool pairs created by rq_tools agent)
**Audience:** rq_tools agent when creating 3_tools.yaml for RQ workflow
**Status:** Current (v4.X architecture)

---

## Overview

### What is 3_tools.yaml?

The 3_tools.yaml file specifies **analysis tool + validation tool pairs** for each step in an RQ's analysis workflow. It is created by the **rq_tools agent** (Step 11 in workflow) and consumed by the **rq_analysis agent** (Step 12) to generate step-by-step analysis + validation call specifications in 4_analysis.yaml.

**Key Characteristics:**
- **Tool Pairs Structure:** Each entry contains BOTH analysis tool AND validation tool (architectural requirement)
- **Full Type Signatures:** Functions specified with complete type hints (prevents v3.0 API mismatches)
- **Sequential Dependency:** Validation tool inputs = analysis tool outputs (validation reads what analysis wrote)
- **YAML Format:** Structured specification for programmatic reading
- **Tool Inventory Integration:** rq_tools reads tool_inventory.md for available validation tools

### Workflow Context

```
Step 9 (Workflow): rq_planner creates 2_plan.md (states "validation MUST be used")
                   ↓
Step 11 (Workflow): rq_tools reads 2_plan.md → creates 3_tools.yaml (THIS FILE)
                   ↓
                   rq_tools specifies analysis tool + validation tool PER STEP
                   ↓
Step 12 (Workflow): rq_analysis reads 3_tools.yaml → creates 4_analysis.yaml
                   ↓
                   rq_analysis embeds validation call AFTER analysis call per step
                   ↓
Step 14 (Workflow): g_code reads 4_analysis.yaml → generates stepN_name.py
                   ↓
                   g_code includes validation function call in generated script
                   ↓
Step 14 (Workflow): bash runs stepN_name.py → analysis executes → validation executes
                   ↓
                   If validation fails → error raised → g_debug invoked
```

**Critical Role:** This file is the **bridge between planning and execution**. It translates the plan's "validation MUST be used" requirement into **concrete tool specifications** that g_code can generate code from.

---

## CRITICAL: Validation Architecture Foundation

### Why Tool Catalog (Option A Architecture)?

**v3.0 Problem:**
- Analysis tools specified in config.yaml
- Validation tools (if any) implied or manual
- No architectural enforcement of validation per step
- Errors cascaded undetected (bad theta → bad LMM → bad plots → bad results)

**v4.X Solution (Tool Catalog):**
- Tool catalog lists each unique tool ONCE (deduplication)
- Each analysis tool includes `validation_tool:` reference (enforces 1:1 relationship)
- rq_analysis transforms catalog + 2_plan.md → creates 4_analysis.yaml with step-by-step instructions
- g_code reads 4_analysis.yaml (phenomenally easy to follow, zero ambiguity)
- bash execution runs validation immediately after analysis (errors caught at source)

**Architectural Flow:**

```
3_tools.yaml (THIS FILE - Tool Catalog):
  analysis_tools:
    calibrate_grm:
      module: "tools.analysis_irt"
      function: "calibrate_grm"
      signature: "calibrate_grm(...)"
      validation_tool: "validate_irt_calibration"  # ← Enforces pairing
  validation_tools:
    validate_irt_calibration:
      module: "tools.validation"
      function: "validate_irt_calibration"
      criteria: [...]
           ↓
rq_analysis reads catalog + 2_plan.md → writes 4_analysis.yaml:
  analysis_steps:
    step01_calibrate_irt_pass1:
      analysis_tool: "calibrate_grm"  # ← Reference to catalog
      validation_tool: "validate_irt_calibration"  # ← Lookup from analysis_tool
      input_files: [...]  # ← From 2_plan.md + 3_tools.yaml
      output_files: [...]
      parameters: {...}
           ↓
g_code reads 4_analysis.yaml → generates step01_calibrate_irt_pass1.py:
  # Analysis
  params, theta = tools.analysis_irt.calibrate_grm(data, dimensions, n_cats=2)
  # Validation (MANDATORY - from 4_analysis.yaml)
  result = tools.validation.validate_irt_calibration(params, theta)
  if not result['valid']:
      raise ValueError(result['message'])
```

**Result:** Validation is **architecturally enforced** via catalog references. Tools deduplicated. 4_analysis.yaml is phenomenally easy for g_code to read (zero bugs, zero ambiguity).

---

## YAML Structure Specification

### Top-Level Structure

```yaml
# 3_tools.yaml - Tool Catalog (Analysis + Validation Tools)
# Created by: rq_tools agent (Step 11)
# Consumed by: rq_analysis agent (Step 12)
# Architecture: Tool Catalog (Option A) - Each tool listed once, deduplication

analysis_tools:
  calibrate_grm:
    [analysis tool specification - see below]
  purify_items:
    [analysis tool specification]
  fit_lmm_with_tsvr:
    [analysis tool specification]
  [... all unique analysis tools used across all steps]

validation_tools:
  validate_irt_calibration:
    [validation tool specification - see below]
  validate_purification:
    [validation tool specification]
  validate_lmm_fit:
    [validation tool specification]
  [... all unique validation tools used across all steps]

summary:
  analysis_tools_count: 12
  validation_tools_count: 12
  total_unique_tools: 24
  mandatory_decisions_embedded: [D039, D068, D069, D070]
```

**Key Principles:**
- **analysis_tools:** Top-level YAML key (dictionary of analysis tool specifications)
- **validation_tools:** Top-level YAML key (dictionary of validation tool specifications)
- **Tool names as keys:** Each tool listed ONCE (deduplication across steps)
- **validation_tool reference:** Each analysis tool includes `validation_tool: "tool_name"` field linking to validation tool
- **summary:** Optional metadata section with counts and decision tracking
- **Order:** Alphabetical or appearance order (rq_analysis maps tools to steps via 2_plan.md)

---

### Analysis Tool Specification

**Required Fields:**

```yaml
calibrate_grm:  # Tool name (key in analysis_tools dictionary)
  module: "tools.analysis_irt"  # Python module path
  function: "calibrate_grm"      # Function name
  signature: "calibrate_grm(df: pd.DataFrame, dimensions: List[str], n_cats: int = 2, device: str = 'cpu', max_iter: int = 200) -> Tuple[pd.DataFrame, pd.DataFrame]"
  validation_tool: "validate_irt_calibration"  # Reference to validation_tools key

  input_files:
    - path: "data/irt_input.csv"
      required_columns: ["UID", "test", "item_name", "score"]
      expected_rows: "~400 (100 participants × 4 tests)"
      data_types:
        UID: "string (format: DDD-SSS-TTT)"
        test: "int (values: 0, 1, 3, 6)"
        item_name: "string (format: RVR-{domain}-{variant}-{subtype})"
        score: "int (values: 0 or 1, NaN if missing)"

  output_files:
    - path: "data/pass1_item_params.csv"
      columns: ["item_name", "discrimination", "difficulty_1", "difficulty_2", "dimension"]
      description: "IRT item parameters from Pass 1 calibration"
    - path: "data/pass1_theta.csv"
      columns: ["UID", "test", "Theta_What", "Theta_Where", "Theta_When", "SE_What", "SE_Where", "SE_When"]
      description: "Participant ability estimates from Pass 1 calibration"

  parameters:
    model_type: "GRM"                    # Graded Response Model
    correlated_factors: true             # Allow factor correlations
    dimensions:                          # Dimension definitions
      - name: "What"
        items: ["RVR-OBJ-*", "RVR-ACT-*"]
      - name: "Where"
        items: ["RVR-LOC-*", "RVR-SPA-*"]
      - name: "When"
        items: ["RVR-TEM-*"]
    convergence_threshold: 0.001
    max_iterations: 1000

  description: "Calibrate multidimensional GRM on all items (Pass 1 of 2-pass purification per Decision D039)"

  source_reference: "tool_inventory.md section 'IRT Analysis Tools'"
```

**Field Descriptions:**

**module (required):**
- Python module path where function lives
- Format: `tools.{submodule}` (e.g., `tools.analysis_irt`, `tools.analysis_lmm`, `tools.plotting`)
- Must match import statement in generated code

**function (required):**
- Function name exactly as defined in module
- Case-sensitive (Python naming conventions)
- rq_tools reads tool_inventory.md to get exact name

**signature (required):**
- **CRITICAL:** Full function signature with type hints
- Format: `function_name(param1: Type1, param2: Type2, ...) -> ReturnType`
- Type hints prevent v3.0 API mismatches (agent cannot guess parameter types)
- Must match tool_inventory.md signature exactly

**input_files (required):**
- List of input files this analysis tool reads
- Each entry contains:
  - `path`: Relative to RQ root (results/chX/rqY/)
  - `required_columns`: Column names expected (for CSV/tabular data)
  - `expected_rows`: Approximate row count (helps validation detect errors)
  - `data_types`: Type + format per column (validation uses this)

**output_files (required):**
- List of output files this analysis tool creates
- Each entry contains:
  - `path`: Relative to RQ root
  - `columns`: Column names produced (for CSV/tabular data)
  - `description`: Human-readable explanation (for rq_results agent)
- **CRITICAL:** These outputs become validation tool inputs (sequential dependency)

**parameters (required):**
- Tool-specific configuration values
- Can be flat (key: value) or nested (key: {subkeys})
- rq_tools infers from 2_plan.md + project_specific_stats_insights.md mandatory requirements
- If parameter not inferrable → circuit breaker: PARAMETER_UNKNOWN

**description (required):**
- Human-readable explanation of what this tool does in this step
- 1-2 sentences maximum
- Used by rq_results agent when summarizing workflow

**source_reference (optional but recommended):**
- Cross-reference to tool_inventory.md section documenting this tool
- Format: "tool_inventory.md section '{Section Name}'"
- Helps future debugging if API changes

---

### Validation Tool Specification

**Required Fields:**

```yaml
validation:
  module: "tools.validation"           # Python module path
  function: "validate_irt_parameters"  # Function name
  signature: "validate_irt_parameters(params_df: pd.DataFrame, disc_range: Tuple[float, float], diff_range: Tuple[float, float]) -> Dict[str, Any]"

  input_files:  # USES ANALYSIS TOOL OUTPUTS
    - path: "data/pass1_item_params.csv"  # From analysis.output_files[0].path
      required_columns: ["item_name", "discrimination", "difficulty_1", "difficulty_2"]
      source: "analysis tool output (step01_calibrate_grm)"

  parameters:
    disc_range: [0.1, 5.0]    # Discrimination (a) valid range
    diff_range: [-4.0, 4.0]   # Difficulty (b) valid range

  criteria:
    - "All discrimination (a) values in range [0.1, 5.0]"
    - "All difficulty (b) values in range [-4.0, 4.0]"
    - "No NaN values in item parameters (indicates estimation failure)"
    - "All items from input present in output (no dropped items)"

  expected_output:
    format: "Dict[str, Any]"
    fields:
      valid: "bool (True if all criteria passed, False otherwise)"
      message: "str (human-readable explanation)"
      flagged_items: "List[str] (item names violating criteria, empty if valid=True)"

  behavior_on_failure:
    action: "raise ValueError"
    log_to: "logs/step01_calibrate.log"
    invoke: "g_debug (master invokes after error)"

  description: "Validate IRT item parameters are in acceptable ranges, no estimation failures"

  source_reference: "tool_inventory.md section 'IRT Validation Tools'"
```

**Field Descriptions:**

**module (required):**
- Typically `tools.validation` (all validation functions centralized)
- Can be different if validation is domain-specific (e.g., `tools.analysis_irt.validate_convergence`)

**function (required):**
- Validation function name from tool_inventory.md
- **Pairing Approach (Dual Strategy):**
  1. **Explicit:** tool_inventory.md documents "Recommended Validation" per analysis function
  2. **Inference:** rq_tools infers from analysis type (IRT → validate_irt_*, LMM → validate_lmm_*, plotting → validate_file_exists)
  3. **Fallback:** If neither works → circuit breaker: VALIDATION_TOOL_UNKNOWN

**signature (required):**
- **CRITICAL:** Full signature with type hints (like analysis tool)
- Prevents API mismatches in validation calls
- Must match tool_inventory.md exactly

**input_files (required):**
- **SEQUENTIAL DEPENDENCY:** Validation inputs = analysis outputs
- Each entry contains:
  - `path`: Must match an `analysis.output_files[*].path` entry
  - `required_columns`: Subset of analysis output columns needed for validation
  - `source`: Human-readable attribution (e.g., "analysis tool output (step01_calibrate_grm)")
- rq_analysis uses this to verify analysis → validation data flow

**parameters (required):**
- Validation-specific configuration (e.g., thresholds, ranges, alpha levels)
- rq_tools infers from project_specific_stats_insights.md (e.g., Decision D039 thresholds)
- Can reference analysis parameters (e.g., if analysis uses alpha=0.05, validation uses same)

**criteria (required):**
- List of validation checks this tool performs
- Human-readable statements (for rq_results agent when documenting validation)
- Each criterion maps to a check in validation function code
- If criterion fails → `valid: False` in output

**expected_output (required):**
- **Standard Format:** ALL validation tools return `Dict[str, Any]` with `valid` and `message` fields
- Additional fields vary by function (e.g., `flagged_items`, `failed_checks`, `warnings`)
- rq_analysis embeds check: `if not result['valid']: raise ValueError(result['message'])`

**behavior_on_failure (required):**
- **action:** What code does if `valid: False` (typically "raise ValueError" or "raise ValidationError")
- **log_to:** Which log file error written to (format: logs/stepNN_name.log)
- **invoke:** What happens next (typically "g_debug (master invokes after error)")
- g_code uses this to generate error handling code

**description (required):**
- Human-readable explanation (1-2 sentences)
- Used by rq_results when summarizing validation coverage

**source_reference (optional but recommended):**
- Cross-reference to tool_inventory.md validation section

---

## Complete Tool Pair Example

### Example: IRT Pass 1 Calibration with Validation (Tool Catalog Structure)

```yaml
# 3_tools.yaml - Analysis Tools Section
analysis_tools:
  calibrate_grm:
    module: "tools.analysis_irt"
    function: "calibrate_grm"
    signature: "calibrate_grm(df: pd.DataFrame, dimensions: List[str], n_cats: int = 2, device: str = 'cpu', max_iter: int = 200) -> Tuple[pd.DataFrame, pd.DataFrame]"
    validation_tool: "validate_irt_calibration"  # ← Links to validation_tools section

    input_files:
      - path: "data/irt_input_wide.csv"
        required_columns: ["composite_ID", "RVR-OBJ-F-MC", "RVR-OBJ-N-MC", "..."]
        expected_rows: "~400"
        data_types:
          composite_ID: "string (format: {UID}_{test})"
          item_columns: "int (values: 0, 1, NaN)"

    output_files:
      - path: "data/pass1_item_params.csv"
        columns: ["item_name", "discrimination", "difficulty_1", "difficulty_2", "dimension"]
        description: "IRT item parameters (GRM) from Pass 1 calibration"
      - path: "data/pass1_theta.csv"
        columns: ["composite_ID", "Theta_What", "Theta_Where", "Theta_When", "SE_What", "SE_Where", "SE_When"]
        description: "Participant ability estimates (theta) from Pass 1 calibration"

    parameters:
      df: "pd.DataFrame"
      dimensions: "List[str]"
      n_cats: "int (default: 2 for dichotomous)"
      device: "str (default: 'cpu')"
      max_iter: "int (default: 200)"

    description: "Calibrate multidimensional GRM on all 102 items (Pass 1 of 2-pass purification per Decision D039)"
    source_reference: "tool_inventory.md section 'IRT Analysis Tools' - calibrate_grm"

# 3_tools.yaml - Validation Tools Section
validation_tools:
  validate_irt_calibration:
      module: "tools.validation"
      function: "validate_irt_parameters"
      signature: "validate_irt_parameters(params_df: pd.DataFrame, disc_range: Tuple[float, float], diff_range: Tuple[float, float]) -> Dict[str, Any]"

      input_files:
        - path: "data/pass1_item_params.csv"
          required_columns: ["item_name", "discrimination", "difficulty_1", "difficulty_2"]
          source: "analysis tool output (step01_calibrate_grm)"

      parameters:
        disc_range: [0.1, 5.0]
        diff_range: [-4.0, 4.0]

      criteria:
        - "All discrimination (a) values in range [0.1, 5.0]"
        - "All difficulty (b) values in range [-4.0, 4.0]"
        - "No NaN values in parameters (estimation failure)"
        - "All 102 items present in output"

      expected_output:
        format: "Dict[str, Any]"
        fields:
          valid: "bool"
          message: "str"
          flagged_items: "List[str]"

      behavior_on_failure:
        action: "raise ValueError"
        log_to: "logs/step01_calibrate_pass1.log"
        invoke: "g_debug (master invokes)"

      description: "Validate IRT parameters in acceptable ranges, no estimation failures, all items present"
      source_reference: "tool_inventory.md section 'IRT Validation Tools' - validate_irt_parameters"
```

---

### Example: Item Purification with Validation

```yaml
  - name: "step02_purify_items"

    analysis:
      module: "tools.analysis_irt"
      function: "purify_items"
      signature: "purify_items(params_df: pd.DataFrame, max_difficulty: float, min_discrimination: float) -> pd.DataFrame"

      input_files:
        - path: "data/pass1_item_params.csv"
          required_columns: ["item_name", "discrimination", "difficulty_1", "difficulty_2"]
          source: "output from step01_calibrate_irt_pass1"

      output_files:
        - path: "data/retained_items.csv"
          columns: ["item_name", "discrimination", "difficulty_1", "difficulty_2", "dimension", "retention_reason"]
          description: "Items retained after 2-pass purification (Decision D039 thresholds)"

      parameters:
        max_difficulty: 3.0   # Per Decision D039: |b| > 3.0 excluded
        min_discrimination: 0.4  # Per Decision D039: a < 0.4 excluded

      description: "Filter items meeting quality thresholds (2-pass IRT purification per Decision D039)"
      source_reference: "tool_inventory.md section 'IRT Analysis Tools' - purify_items"

    validation:
      module: "tools.validation"
      function: "validate_numeric_range"
      signature: "validate_numeric_range(df: pd.DataFrame, column: str, min_val: float, max_val: float, allow_none: bool = False) -> Dict[str, Any]"

      input_files:
        - path: "data/retained_items.csv"
          required_columns: ["item_name", "discrimination", "difficulty_1"]
          source: "analysis tool output (step02_purify_items)"

      parameters:
        checks:
          - column: "discrimination"
            min_val: 0.4
            max_val: 5.0
            allow_none: false
          - column: "difficulty_1"
            min_val: -3.0
            max_val: 3.0
            allow_none: false

      criteria:
        - "All retained items have discrimination ≥ 0.4 (per Decision D039)"
        - "All retained items have |difficulty| ≤ 3.0 (per Decision D039)"
        - "No NaN values in retained_items.csv"

      expected_output:
        format: "Dict[str, Any]"
        fields:
          valid: "bool"
          message: "str"
          failed_rows: "List[int]"

      behavior_on_failure:
        action: "raise ValueError"
        log_to: "logs/step02_purify_items.log"
        invoke: "g_debug (master invokes)"

      description: "Validate all retained items meet Decision D039 thresholds (no edge cases slipped through)"
      source_reference: "tool_inventory.md section 'Data Validation Tools' - validate_numeric_range"
```

---

### Example: LMM Fitting with Validation

```yaml
  - name: "step05_fit_lmm_trajectory"

    analysis:
      module: "tools.analysis_lmm"
      function: "fit_lmm_with_tsvr"
      signature: "fit_lmm_with_tsvr(data: pd.DataFrame, formula: str, re_formula: str, groups: str) -> Tuple[Any, pd.DataFrame]"

      input_files:
        - path: "data/theta_long_with_tsvr.csv"
          required_columns: ["UID", "test", "theta", "TSVR_hours", "group"]
          expected_rows: "~400"
          data_types:
            UID: "string"
            test: "int (0, 1, 3, 6)"
            theta: "float"
            TSVR_hours: "float (0 to 168 hours = 1 week)"
            group: "string (e.g., 'high_performers', 'low_performers')"

      output_files:
        - path: "results/lmm_summary.txt"
          description: "LMM fixed effects, random effects, fit statistics"
        - path: "data/lmm_coefficients.csv"
          columns: ["term", "estimate", "std_error", "z_value", "p_value"]
          description: "Fixed effect coefficients from LMM"

      parameters:
        formula: "theta ~ TSVR_hours * group"  # Fixed effects (TSVR not nominal days per D070)
        re_formula: "~TSVR_hours"              # Random effects (random slope per participant)
        groups: "UID"                          # Grouping variable (participant)
        method: "REML"                         # Estimation method

      description: "Fit LMM with TSVR (actual hours) as time variable per Decision D070, group × time interaction"
      source_reference: "tool_inventory.md section 'LMM Analysis Tools' - fit_lmm_with_tsvr"

    validation:
      module: "tools.validation"
      function: "validate_lmm_convergence"
      signature: "validate_lmm_convergence(lmm_result: Any, min_observations: int = 100) -> Dict[str, Any]"

      input_files:
        - path: "results/lmm_summary.txt"
          source: "analysis tool output (step05_fit_lmm_trajectory)"

      parameters:
        min_observations: 100
        check_singularity: true

      criteria:
        - "Model converged (no convergence warnings)"
        - "No singular fit (random effects variance > 0)"
        - "Minimum 100 observations used"
        - "All fixed effects have finite estimates (no NaN/Inf)"

      expected_output:
        format: "Dict[str, Any]"
        fields:
          valid: "bool"
          message: "str"
          convergence_status: "str"
          warnings: "List[str]"

      behavior_on_failure:
        action: "raise ValueError"
        log_to: "logs/step05_fit_lmm_trajectory.log"
        invoke: "g_debug (master invokes)"

      description: "Validate LMM converged successfully, no singular fit, all estimates finite"
      source_reference: "tool_inventory.md section 'LMM Validation Tools' - validate_lmm_convergence"
```

---

### Example: Plotting with Validation

```yaml
  - name: "step08_plot_trajectory_dual_scale"

    analysis:
      module: "tools.plotting"
      function: "plot_trajectory_probability"
      signature: "plot_trajectory_probability(theta_df: pd.DataFrame, time_col: str, theta_col: str, group_col: str, output_prefix: str) -> List[str]"

      input_files:
        - path: "data/theta_long_with_tsvr.csv"
          required_columns: ["TSVR_hours", "theta", "group"]
          source: "output from step04_merge_theta_tsvr"

      output_files:
        - path: "plots/trajectory_theta_scale.png"
          format: "PNG (800×600 @ 300 DPI)"
          description: "Trajectory plot with theta scale (-3 to +3)"
        - path: "plots/trajectory_probability_scale.png"
          format: "PNG (800×600 @ 300 DPI)"
          description: "Trajectory plot with probability scale (0 to 1) via IRT transformation (Decision D069)"

      parameters:
        time_col: "TSVR_hours"
        theta_col: "theta"
        group_col: "group"
        output_prefix: "plots/trajectory"
        scales: ["theta", "probability"]  # Dual-scale per Decision D069
        x_label: "Time Since VR (hours)"
        y_labels: ["Theta (ability)", "Probability of Success"]
        theme: "publication"

      description: "Generate dual-scale trajectory plots (theta + probability) per Decision D069 for interpretability"
      source_reference: "tool_inventory.md section 'Plotting Tools' - plot_trajectory_probability"

    validation:
      module: "tools.validation"
      function: "validate_file_exists"
      signature: "validate_file_exists(file_path: str, min_size_bytes: int = 1000) -> Dict[str, Any]"

      input_files: []  # Validation checks file existence, not content

      parameters:
        files_to_check:
          - path: "plots/trajectory_theta_scale.png"
            min_size_bytes: 10000  # PNG should be >10KB
          - path: "plots/trajectory_probability_scale.png"
            min_size_bytes: 10000

      criteria:
        - "Both plot files exist (theta scale + probability scale)"
        - "Each file >10KB (not empty/corrupted)"
        - "PNG format (readable by image libraries)"

      expected_output:
        format: "Dict[str, Any]"
        fields:
          valid: "bool"
          message: "str"
          missing_files: "List[str]"

      behavior_on_failure:
        action: "raise FileNotFoundError"
        log_to: "logs/step08_plot_trajectory.log"
        invoke: "g_debug (master invokes)"

      description: "Validate both plot files created successfully, not empty, readable format"
      source_reference: "tool_inventory.md section 'File Validation Tools' - validate_file_exists"
```

---

## How rq_tools Creates 3_tools.yaml

### Agent Workflow (Step 11)

The rq_tools agent follows this process:

1. **Read** this template (docs/v4/templates/tools.md)
2. **Read** 2_plan.md (analysis plan with step-by-step workflow)
3. **Read** status.yaml (rq_planner context_dump with step count)
4. **Read** tool_inventory.md (ALL available analysis + validation tools with signatures)
5. **Read** project_specific_stats_insights.md (mandatory requirements: D039, D068, D069, D070)
6. **Read** names.md (check if naming conventions exist for step names)
7. **Read** agent_best_practices.md (circuit breaker rules, YAML parsing rules)
8. **Ultrathink** tool selection per step:
   - What analysis tool matches step description? (from tool_inventory.md)
   - What validation tool corresponds? (explicit pairing in tool_inventory.md OR infer from analysis type)
   - What parameters? (from 2_plan.md + project_specific_stats_insights.md)
   - What input/output files? (from 2_plan.md)
   - Are type signatures complete? (CRITICAL - copy from tool_inventory.md exactly)
9. **Verify** no conflicts:
   - All analysis tools exist in tool_inventory.md
   - All validation tools exist in tool_inventory.md
   - Type signatures match tool_inventory.md exactly
   - Input/output file paths consistent with 2_plan.md
10. **Write** 3_tools.yaml following this template structure
11. **Update** status.yaml (rq_tools: success, context_dump)
12. **Report** to master: "Successfully created 3_tools.yaml for chX/rqY with N tool pairs"

### Tool Pairing Strategy (Dual Approach)

**Approach 1: Explicit Pairing (Preferred)**

tool_inventory.md documents "Recommended Validation" per analysis function:

```markdown
### calibrate_grm

**Module:** tools.analysis_irt
**Signature:** calibrate_grm(data: pd.DataFrame, groups: Dict[str, List[str]], config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]
**Recommended Validation:** validate_irt_parameters (checks parameter ranges, no NaN)
```

rq_tools reads this → pairs `calibrate_grm` with `validate_irt_parameters` automatically.

**Approach 2: Inference from Context (Fallback)**

If tool_inventory.md lacks explicit pairing, rq_tools infers:

- Analysis module `tools.analysis_irt` → Validation module `tools.validation` with `validate_irt_*` functions
- Analysis module `tools.analysis_lmm` → Validation module `tools.validation` with `validate_lmm_*` functions
- Analysis module `tools.plotting` → Validation module `tools.validation` with `validate_file_exists`

**Circuit Breaker:**

If NEITHER approach succeeds:
- Quit with error: VALIDATION_TOOL_UNKNOWN
- Report to master: "Cannot determine validation tool for {analysis_function}. Update tool_inventory.md with 'Recommended Validation' field."
- Master must update tool_inventory.md or create validation tool
- Retry rq_tools after fix

---

## What rq_tools Does NOT Do

- **Does NOT create new tools:** Only specifies existing tools from tool_inventory.md
- **Does NOT execute tools:** That's bash execution in Step 14
- **Does NOT write code:** That's g_code job in Step 14
- **Does NOT validate analysis outputs:** That's validation tools job during execution

rq_tools creates the **specification** (what tools to use), downstream agents execute it.

---

## Differences from v3.0 config.yaml

### v3.0 Approach (For Historical Context Only - DO NOT REPLICATE)

**v3.0 config.yaml:**

```yaml
tool_functions:
  step_1_irt_pass1:
    function: "tools.analysis_irt.calibrate_grm"
    input_file: "data/irt_input.csv"
    output_files:
      - "logs/pass1_item_params.csv"
      - "logs/pass1_theta.csv"
    config_section: "irt_pass1"
    description: "Pass 1 - Calibrate GRM"
```

**v3.0 Problems:**
- ❌ No validation tools specified
- ❌ No type signatures (caused API mismatches)
- ❌ Singular input_file (not list, inflexible)
- ❌ Config section reference (circular dependency: config.yaml references config.yaml)
- ❌ No validation criteria
- ❌ No error handling specifications

**v3.0 Results:**
- Analysis tools ran without validation
- Errors propagated undetected (cascading failures)
- g_code guessed function signatures from context → API mismatches
- 6 cascading API errors in RQ 5.1 testing (Unicode arrow, composite_ID, test vs Test, tsvr formats, wide vs long)

### v4.X Approach (Current Architecture)

**v4.X 3_tools.yaml:**

```yaml
tool_pairs:
  - name: "step01_calibrate_irt_pass1"
    analysis:
      module: "tools.analysis_irt"
      function: "calibrate_grm"
      signature: "calibrate_grm(data: pd.DataFrame, groups: Dict[str, List[str]], config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]"
      input_files: [...]
      output_files: [...]
      parameters: {...}
    validation:
      module: "tools.validation"
      function: "validate_irt_parameters"
      signature: "validate_irt_parameters(params_df: pd.DataFrame, disc_range: Tuple[float, float], diff_range: Tuple[float, float]) -> Dict[str, Any]"
      input_files: [...]  # Uses analysis outputs
      parameters: {...}
      criteria: [...]
```

**v4.X Improvements:**
- ✅ Validation tools mandatory per tool pair
- ✅ Type signatures prevent API guessing
- ✅ Input/output files as lists (flexible)
- ✅ No circular dependencies (parameters inline, not config section references)
- ✅ Validation criteria documented
- ✅ Error handling specified (behavior_on_failure)

**v4.X Architecture Benefits:**
- Validation catches errors at source (not 5 steps later)
- Type hints eliminate API mismatches (g_code copies signatures exactly)
- Tool pairs enforce 1:1 analysis→validation relationship
- Explicit criteria enable debugging (know what validation checks)

---

## Integration with Validation Architecture

### Phase 4 Validation Migration Context

**Background:** todo.yaml Phase 4 (V1-V4) migrates v3 validation tools to v4.X architecture.

**Dependency:**
- **V3 task:** Update tool_inventory.md with validation tools section
- **Completion:** Before rq_tools can run (rq_tools reads tool_inventory.md for validation signatures)

**What rq_tools Needs from Phase 4:**

1. **tool_inventory.md Validation Section:**
   - All validation functions listed with full signatures
   - "Recommended Validation" field per analysis function (explicit pairing)
   - Input/output formats documented
   - Validation criteria explained

2. **Validation Tool Requirements:**
   - Standard return format: `Dict[str, Any]` with `valid` and `message` fields
   - Type hints complete (no `Any` for critical parameters)
   - All validation functions tested (100% coverage per Phase 4 V4 task)

**Example tool_inventory.md Entry:**

```markdown
### calibrate_grm

**Module:** tools.analysis_irt
**Function:** calibrate_grm
**Signature:** calibrate_grm(data: pd.DataFrame, groups: Dict[str, List[str]], config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]
**Recommended Validation:** validate_irt_parameters
**Purpose:** Calibrate multidimensional GRM
**Returns:** (item_params_df, theta_df)
```

```markdown
### validate_irt_parameters

**Module:** tools.validation
**Function:** validate_irt_parameters
**Signature:** validate_irt_parameters(params_df: pd.DataFrame, disc_range: Tuple[float, float], diff_range: Tuple[float, float]) -> Dict[str, Any]
**Purpose:** Validate IRT parameters in acceptable ranges
**Criteria:**
- Discrimination (a) in disc_range
- Difficulty (b) in diff_range
- No NaN values
**Returns:** {valid: bool, message: str, flagged_items: List[str]}
```

rq_tools reads both entries → creates tool pair automatically.

---

## Circuit Breaker Triggers

The rq_tools agent MUST quit immediately (no guessing) on these errors:

### CB1: TOOL_NOT_FOUND

**Trigger:** 2_plan.md describes analysis step, but no matching tool in tool_inventory.md

**Example:**
- Plan says: "Step 3: Perform factor analysis on theta scores"
- tool_inventory.md has no `perform_factor_analysis` function
- Circuit breaker triggers

**Error Message:**
```
CIRCUIT BREAKER: TOOL_NOT_FOUND

Step: step03_factor_analysis
Required: Factor analysis tool
Available: [list of tool_inventory.md analysis tools]

The plan requires a tool that does not exist. Either:
1. Add the tool to tools/ (following TDD: write test first)
2. Revise 2_plan.md to use existing tools
3. Consult with user on alternative approach

Quitting now. Master must resolve before rq_tools can proceed.
```

**Resolution:** Master adds tool OR revises plan OR consults user

---

### CB2: VALIDATION_TOOL_UNKNOWN

**Trigger:** Cannot determine which validation tool corresponds to analysis tool

**Example:**
- Analysis tool: `calibrate_grm`
- tool_inventory.md has NO "Recommended Validation" field for `calibrate_grm`
- Inference fails (no `validate_irt_*` functions in tools.validation)
- Circuit breaker triggers

**Error Message:**
```
CIRCUIT BREAKER: VALIDATION_TOOL_UNKNOWN

Analysis Tool: calibrate_grm (module: tools.analysis_irt)
Required: Validation tool for IRT calibration
Available Validation Tools: [list from tool_inventory.md]

Cannot determine which validation tool to pair with this analysis tool. Either:
1. Add "Recommended Validation: {function_name}" to tool_inventory.md for calibrate_grm
2. Create validation tool (e.g., validate_irt_calibration) in tools.validation
3. Update agent inference rules if validation tool exists but naming doesn't match pattern

Quitting now. Master must update tool_inventory.md before rq_tools can proceed.
```

**Resolution:** Master updates tool_inventory.md with explicit pairing

---

### CB3: SIGNATURE_INCOMPLETE

**Trigger:** tool_inventory.md function signature lacks type hints

**Example:**
- Function: `calibrate_grm(data, groups, config)` (no type hints)
- Specification requires: `calibrate_grm(data: pd.DataFrame, groups: Dict[str, List[str]], config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]`
- Circuit breaker triggers

**Error Message:**
```
CIRCUIT BREAKER: SIGNATURE_INCOMPLETE

Function: calibrate_grm
Current Signature: calibrate_grm(data, groups, config)
Required: Type hints for ALL parameters and return value

Type hints are CRITICAL for v4.X architecture (prevent v3.0 API mismatches). Update tool_inventory.md with complete signature including:
- Parameter types (e.g., data: pd.DataFrame)
- Return type (e.g., -> Tuple[pd.DataFrame, pd.DataFrame])

Quitting now. Master must update tool_inventory.md before rq_tools can proceed.
```

**Resolution:** Master updates tool_inventory.md with type hints

---

### CB4: PARAMETER_UNKNOWN

**Trigger:** Cannot infer required parameter value from 2_plan.md or project_specific_stats_insights.md

**Example:**
- Analysis tool requires `convergence_threshold` parameter
- 2_plan.md does not specify value
- project_specific_stats_insights.md does not specify value
- No default value in tool_inventory.md
- Circuit breaker triggers

**Error Message:**
```
CIRCUIT BREAKER: PARAMETER_UNKNOWN

Function: calibrate_grm
Parameter: convergence_threshold (type: float)
Sources Checked:
- 2_plan.md: Not specified
- project_specific_stats_insights.md: Not specified
- tool_inventory.md: No default documented

Cannot infer parameter value. Either:
1. Add to 2_plan.md (if RQ-specific)
2. Add to project_specific_stats_insights.md (if project-wide requirement)
3. Add default to tool_inventory.md function documentation

Quitting now. Master must provide parameter value before rq_tools can proceed.
```

**Resolution:** Master specifies parameter in appropriate location

---

### CB5: INPUT_OUTPUT_MISMATCH

**Trigger:** Validation tool input files don't match analysis tool output files

**Example:**
- Analysis outputs: `data/pass1_item_params.csv`
- Validation expects: `data/item_parameters.csv` (different filename)
- Circuit breaker triggers

**Error Message:**
```
CIRCUIT BREAKER: INPUT_OUTPUT_MISMATCH

Analysis Tool: calibrate_grm
Analysis Outputs: ["data/pass1_item_params.csv", "data/pass1_theta.csv"]

Validation Tool: validate_irt_parameters
Validation Inputs: ["data/item_parameters.csv"]

Mismatch: Validation input "data/item_parameters.csv" not in analysis outputs.

Validation tools MUST use analysis tool outputs as inputs (sequential dependency). Either:
1. Update validation tool to use correct filename
2. Update analysis tool to produce expected filename
3. Verify 2_plan.md specifies correct filenames

Quitting now. Master must resolve filename mismatch before rq_tools can proceed.
```

**Resolution:** Master fixes filename inconsistency

---

## Validation Checklist (For Template Verification)

When template is complete, verify:

- [ ] File exists at docs/v4/templates/tools.md
- [ ] Overview section explains 3_tools.yaml purpose and workflow context
- [ ] CRITICAL section explains validation architecture (tool pairs, not separate lists)
- [ ] YAML Structure section documents top-level structure (tool_pairs list)
- [ ] Analysis Tool Specification section documents all required fields (module, function, signature, input_files, output_files, parameters, description, source_reference)
- [ ] Validation Tool Specification section documents all required fields (module, function, signature, input_files, parameters, criteria, expected_output, behavior_on_failure, description, source_reference)
- [ ] Complete Tool Pair Examples section provides 4+ examples:
  - [ ] IRT Pass 1 Calibration
  - [ ] Item Purification
  - [ ] LMM Fitting
  - [ ] Plotting
- [ ] rq_tools workflow documented (13-step agent process)
- [ ] Tool Pairing Strategy documented (dual approach: explicit + inference)
- [ ] v3.0 vs v4.X differences explained (config.yaml problems → tool pairs solution)
- [ ] Integration with Phase 4 Validation Migration documented
- [ ] Circuit breaker triggers documented (5 types: TOOL_NOT_FOUND, VALIDATION_TOOL_UNKNOWN, SIGNATURE_INCOMPLETE, PARAMETER_UNKNOWN, INPUT_OUTPUT_MISMATCH)
- [ ] Template is very comprehensive (700-900 lines per user requirement)
- [ ] tool_inventory.md referenced but not duplicated (per user requirement)
- [ ] Type signatures emphasized (prevents v3.0 API mismatches)
- [ ] Sequential dependency explained (validation inputs = analysis outputs)

---

## Version History

- **v4.0** (2025-11-16): Initial template created for v4.X architecture
  - Very comprehensive structure (700-900 lines per user requirement)
  - Nested YAML structure (tool_pairs per step)
  - Dual pairing approach (explicit + inference)
  - tool_inventory.md integration (reference only, no duplication)
  - Complete examples (IRT, LMM, plotting)
  - Circuit breaker documentation (5 triggers)
  - Aligned with specification section 4.2.3

---

**End of Template Specification**
