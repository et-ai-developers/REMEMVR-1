# analysis.md Template Specification

**Version:** 4.0
**Last Updated:** 2025-11-16
**Purpose:** Specification for 4_analysis.yaml format (analysis + validation calls per step created by rq_analysis agent)
**Audience:** rq_analysis agent when creating 4_analysis.yaml for RQ workflow
**Status:** Current (v4.X architecture)

---

## Overview

### What is 4_analysis.yaml?

The 4_analysis.yaml file specifies **executable analysis + validation call pairs** for each step in an RQ's analysis workflow. It is created by the **rq_analysis agent** (Step 12 in workflow) and consumed by the **g_code agent** (Step 14) to generate Python scripts with embedded validation.

**Key Characteristics:**
- **Nested Step Structure:** Each step contains analysis_call + validation_call + log_file
- **Full Function Signatures:** Complete signatures with type hints (enables g_code pre-generation validation)
- **Sequential Execution:** Validation call AFTER analysis call per step (errors caught immediately)
- **YAML Format:** Structured specification for g_code code generation
- **Atomic Scripts:** Each step generates stepNN_name.py file (vs v3.0 monolithic script)

### Workflow Context

```
Step 11 (Workflow): rq_tools creates 3_tools.yaml (analysis + validation tool pairs)
                    ↓
Step 12 (Workflow): rq_analysis reads 3_tools.yaml → creates 4_analysis.yaml (THIS FILE)
                    ↓
                    rq_analysis combines tool pairs into executable specifications
                    ↓
Step 14 (Workflow): g_code reads 4_analysis.yaml → validates signatures (4-layer validation)
                    ↓
                    g_code generates stepNN_name.py with analysis + validation calls
                    ↓
Step 14 (Workflow): master runs bash stepNN_name.py → analysis executes → validation executes
                    ↓
                    If validation fails → error raised → g_debug invoked → fix → re-run
```

**Critical Role:** This file is the **blueprint for code generation**. g_code treats 4_analysis.yaml as authoritative source for function signatures, input/output files, parameters, and validation criteria.

---

## CRITICAL: Validation Call Requirement

### Mandatory Validation Per Step

**SPECIFICATION REQUIREMENT (Section 4.2.4, Line 1068):**

> "Each step MUST end with validation tool call"

This is **not optional**. This is the **architectural foundation** preventing cascading failures.

### Why Validation AFTER Analysis (Sequential, Not Parallel)

**Execution Order:**
```python
# CORRECT (v4.X):
# Step 1: Analysis
params, theta = tools.analysis_irt.calibrate_grm(data, groups, config)

# Step 2: Validation (uses analysis outputs)
result = tools.validation.validate_irt_parameters(params, (0.1, 5.0), (-4, 4))
if not result['valid']:
    raise ValueError(result['message'])  # Halt execution immediately

# INCORRECT (validation before analysis):
# result = tools.validation.validate_irt_parameters(???)  # What to validate? Analysis hasn't run yet!
```

**Why Sequential:**
- Validation uses analysis outputs as inputs (sequential dependency)
- Errors caught immediately after analysis (not 5 steps later)
- Script halts on validation failure (prevents cascade)

### Enforcement Mechanism

**rq_analysis agent:**
- Reads 2_plan.md validation requirement ("validation MUST be used")
- Reads 3_tools.yaml tool pairs
- Writes 4_analysis.yaml with validation_call AFTER analysis_call per step
- Circuit breaker: VALIDATION_MISSING if validation_call absent from any step

**g_code agent:**
- Reads 4_analysis.yaml
- Generates stepNN_name.py with validation function call after analysis
- Embeds error handling: `if not result['valid']: raise ValueError(result['message'])`

**Result:** Validation architecturally enforced, errors halted at source, no cascading failures.

---

## g_code 4-Layer Pre-Generation Validation Protocol

### Why Signatures Critical for v4.X

**Problem (v3.0):**
- analysis_executor guessed function signatures from config.yaml
- 6 API mismatches in RQ 5.1 testing (purify_items, fit_lmm_with_tsvr, post_hoc_contrasts parameters)
- Each error discovered at runtime (60+ minutes per IRT calibration wasted)
- Cascading failures (1 API error → 5+ downstream failures)

**Solution (v4.X):**
- 4_analysis.yaml MUST include full signatures with type hints
- g_code validates signatures PRE-generation using Python inspect.signature()
- Errors caught BEFORE code generation (saves runtime)
- No cascading failures (invalid code never generated)

### 4-Layer Validation Protocol

**Detailed Protocol:** See docs/user/analysis_pipeline_solution.md section 6.1

**Summary (4 Layers):**
1. **Import Check:** Tool module/function exists (importlib + hasattr)
2. **Signature Check:** Matches 4_analysis.yaml specification (inspect.signature)
3. **Input File Check:** Expected files exist if step >1 (os.path.exists)
4. **Column Check:** CSV columns match expectations if tabular (pandas)

**Quit-on-Failure:** ANY layer fails → Circuit breaker → g_code QUITS without generating code

**Benefits:**
- Catches errors pre-execution (saves 60+ minutes per IRT calibration)
- Prevents invalid code generation (no syntax errors in stepNN_name.py)
- Prevents cascading failures (bad inputs detected before analysis runs)
- Enables debugging BEFORE expensive computations

### How 4_analysis.yaml Enables Validation

**Example: IRT Calibration**

```yaml
steps:
  - name: "step01_calibrate_irt_pass1"
    analysis_call:
      module: "tools.analysis_irt"
      function: "calibrate_grm"
      signature: "calibrate_grm(data: pd.DataFrame, groups: Dict[str, List[str]], config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]"
      # g_code uses this signature for:
      # - Step 4a: import tools.analysis_irt, hasattr(calibrate_grm)
      # - Step 4b: inspect.signature(calibrate_grm) == signature above
      # - Step 4c: os.path.exists(input_files paths)
      # - Step 4d: pd.read_csv checks required_columns
```

**If signature missing or incomplete:**
- g_code cannot validate (no baseline for comparison)
- Must guess signature from context (v3.0 failure mode)
- API mismatches inevitable (parameter order, types, defaults)

**Result:** Signatures are MANDATORY, not optional.

---

## YAML Structure Specification

### Top-Level Structure

```yaml
# 4_analysis.yaml - Analysis + Validation Calls Per Step
# Created by: rq_analysis agent (Step 12)
# Consumed by: g_code agent (Step 14), rq_inspect agent (Step 14 loop)

steps:
  - name: "step01_extract_irt_data"
    step_number: "01"
    analysis_call:
      [analysis call specification - see below]
    validation_call:
      [validation call specification - see below]
    log_file: "logs/step01_extract_irt_data.log"

  - name: "step02_calibrate_irt_pass1"
    step_number: "02"
    analysis_call:
      [analysis call specification]
    validation_call:
      [validation call specification]
    log_file: "logs/step02_calibrate_irt_pass1.log"

  [... continue for all N steps from 2_plan.md]
```

**Key Principles:**
- **steps:** Top-level YAML key (list of dictionaries)
- **name:** Step identifier (from names.md, format: stepNN_verb_noun)
- **step_number:** Zero-padded integer (01, 02, ..., 99)
- **analysis_call:** Nested dictionary with analysis function specification
- **validation_call:** Nested dictionary with validation function specification (MANDATORY)
- **log_file:** Relative path (format: logs/stepNN_name.log)
- **Order:** Sequential (step01, step02, ..., stepN matching 2_plan.md)

---

### Analysis Call Specification

**Required Fields:**

```yaml
analysis_call:
  module: "tools.analysis_irt"  # Python module path
  function: "calibrate_grm"      # Function name
  signature: "calibrate_grm(data: pd.DataFrame, groups: Dict[str, List[str]], config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]"

  input_files:
    - path: "data/irt_input_wide.csv"
      required_columns: ["composite_ID", "RVR-OBJ-F-MC", "RVR-OBJ-N-MC"]
      variable_name: "irt_data"  # Variable name in generated code

  output_files:
    - path: "data/pass1_item_params.csv"
      variable_name: "item_params"
      description: "IRT item parameters from Pass 1 calibration"
    - path: "data/pass1_theta.csv"
      variable_name: "theta_scores"
      description: "Participant ability estimates from Pass 1"

  parameters:
    groups:
      What: ["RVR-OBJ-*", "RVR-ACT-*"]
      Where: ["RVR-LOC-*", "RVR-SPA-*"]
      When: ["RVR-TEM-*"]
    config:
      model_type: "GRM"
      correlated_factors: true
      convergence_threshold: 0.001

  returns:
    type: "Tuple[pd.DataFrame, pd.DataFrame]"
    unpacking: "item_params, theta_scores"  # How to unpack tuple in generated code

  description: "Calibrate multidimensional GRM on all 102 items (Pass 1 of 2-pass purification)"
```

**Field Descriptions:**

**module (required):**
- Python module path where function exists
- Format: `tools.{submodule}` (e.g., `tools.analysis_irt`, `tools.analysis_lmm`)
- g_code uses for import: `from {module} import {function}`

**function (required):**
- Function name exactly as defined in module
- g_code validates: `hasattr({module}, {function})`

**signature (required):**
- **CRITICAL:** Full function signature with type hints
- Format: `function_name(param1: Type1, param2: Type2) -> ReturnType`
- g_code validates: `inspect.signature(function) matches signature string`
- Must match tool_inventory.md signature exactly

**input_files (required):**
- List of input files analysis function reads
- Each entry:
  - `path`: Relative to RQ root (results/chX/rqY/)
  - `required_columns`: Column names expected (for g_code Step 4d validation)
  - `variable_name`: Variable name in generated code (e.g., `irt_data = pd.read_csv(...)`)

**output_files (required):**
- List of output files analysis function creates
- Each entry:
  - `path`: Relative to RQ root
  - `variable_name`: Variable name holding output in generated code
  - `description`: Human-readable (for logging)

**parameters (required):**
- Function parameters as YAML structure
- Nested dictionaries preserved (e.g., groups: {What: [...], Where: [...]})
- g_code converts to Python literals when generating code

**returns (required):**
- `type`: Return type from signature (for documentation)
- `unpacking`: How to unpack return value (e.g., `item_params, theta_scores = calibrate_grm(...)`)
- If single return: `variable_name: "result"` (no unpacking)

**description (optional but recommended):**
- Human-readable explanation
- g_code includes as comment in generated code

---

### Validation Call Specification

**Required Fields:**

```yaml
validation_call:
  module: "tools.validation"           # Python module path
  function: "validate_irt_parameters"  # Function name
  signature: "validate_irt_parameters(params_df: pd.DataFrame, disc_range: Tuple[float, float], diff_range: Tuple[float, float]) -> Dict[str, Any]"

  input_files:  # USES ANALYSIS CALL OUTPUTS
    - path: "data/pass1_item_params.csv"  # From analysis_call.output_files[0].path
      variable_name: "item_params"         # From analysis_call.output_files[0].variable_name
      source: "analysis call output (calibrate_grm return value)"

  parameters:
    params_df: "item_params"  # Variable name from analysis_call
    disc_range: [0.1, 5.0]
    diff_range: [-4.0, 4.0]

  returns:
    type: "Dict[str, Any]"
    variable_name: "validation_result"

  criteria:
    - "All discrimination (a) values in range [0.1, 5.0]"
    - "All difficulty (b) values in range [-4.0, 4.0]"
    - "No NaN values in item parameters"

  on_failure:
    action: "raise ValueError(validation_result['message'])"
    log_to: "logs/step01_calibrate_irt_pass1.log"

  description: "Validate IRT parameters in acceptable ranges"
```

**Field Descriptions:**

**module (required):**
- Typically `tools.validation` (all validation functions centralized)
- g_code uses for import: `from {module} import {function}`

**function (required):**
- Validation function name from 3_tools.yaml
- g_code validates: `hasattr({module}, {function})`

**signature (required):**
- **CRITICAL:** Full signature with type hints (like analysis_call)
- g_code validates via `inspect.signature()`

**input_files (required):**
- **SEQUENTIAL DEPENDENCY:** Validation inputs = analysis outputs
- Each entry:
  - `path`: Must match an `analysis_call.output_files[*].path`
  - `variable_name`: Must match an `analysis_call.output_files[*].variable_name`
  - `source`: Human-readable attribution

**parameters (required):**
- Validation function parameters
- Can reference analysis_call output variables (e.g., `params_df: "item_params"`)
- g_code substitutes variable names when generating code

**returns (required):**
- `type`: Always `Dict[str, Any]` (standard validation return format)
- `variable_name`: Variable name holding validation result

**criteria (required):**
- List of checks validation function performs
- Human-readable (for logging, rq_results documentation)
- g_code includes as comments in generated code

**on_failure (required):**
- `action`: Python code to execute if `validation_result['valid'] == False`
- Typically: `raise ValueError(validation_result['message'])`
- `log_to`: Log file path for error message

**description (optional but recommended):**
- Human-readable explanation
- g_code includes as comment

---

## Complete Step Example

### Example: IRT Pass 1 Calibration with Validation

```yaml
steps:
  - name: "step01_calibrate_irt_pass1"
    step_number: "01"

    analysis_call:
      module: "tools.analysis_irt"
      function: "calibrate_grm"
      signature: "calibrate_grm(data: pd.DataFrame, groups: Dict[str, List[str]], config: Dict[str, Any]) -> Tuple[pd.DataFrame, pd.DataFrame]"

      input_files:
        - path: "data/irt_input_wide.csv"
          required_columns: ["composite_ID", "RVR-OBJ-F-MC", "RVR-OBJ-N-MC", "RVR-LOC-F-MC", "RVR-LOC-N-MC", "RVR-TEM-F-MC", "RVR-TEM-N-MC"]
          variable_name: "irt_data"

      output_files:
        - path: "data/pass1_item_params.csv"
          variable_name: "item_params"
          description: "IRT item parameters (discrimination, difficulty) from Pass 1"
        - path: "data/pass1_theta.csv"
          variable_name: "theta_scores"
          description: "Participant ability estimates (theta) from Pass 1"

      parameters:
        data: "irt_data"
        groups:
          What: ["RVR-OBJ-*", "RVR-ACT-*"]
          Where: ["RVR-LOC-*", "RVR-SPA-*"]
          When: ["RVR-TEM-*"]
        config:
          # MANDATORY: Validated "Med" settings from thesis/analyses/ANALYSES_DEFINITIVE.md
          # These settings are required for publication-quality results
          factors: ["What", "Where", "When"]
          correlated_factors: true
          device: "cpu"
          seed: 42
          model_fit:
            batch_size: 2048        # Validated "Med" level - DO NOT reduce
            iw_samples: 100         # Validated "Med" level - DO NOT reduce
            mc_samples: 1           # Per thesis validation
          model_scores:
            scoring_batch_size: 2048  # Validated "Med" level
            mc_samples: 100           # Validated "Med" level - critical for theta accuracy
            iw_samples: 100           # Validated "Med" level

      returns:
        type: "Tuple[pd.DataFrame, pd.DataFrame]"
        unpacking: "item_params, theta_scores"

      description: "Calibrate multidimensional GRM on all 102 items (Pass 1 of 2-pass purification per Decision D039)"

    validation_call:
      module: "tools.validation"
      function: "validate_irt_parameters"
      signature: "validate_irt_parameters(params_df: pd.DataFrame, disc_range: Tuple[float, float], diff_range: Tuple[float, float]) -> Dict[str, Any]"

      input_files:
        - path: "data/pass1_item_params.csv"
          variable_name: "item_params"
          source: "analysis call output (calibrate_grm return value[0])"

      parameters:
        params_df: "item_params"
        disc_range: [0.1, 5.0]
        diff_range: [-4.0, 4.0]

      returns:
        type: "Dict[str, Any]"
        variable_name: "validation_result"

      criteria:
        - "All discrimination (a) in range [0.1, 5.0]"
        - "All difficulty (b) in range [-4.0, 4.0]"
        - "No NaN parameters (estimation failure)"
        - "All 102 items present"

      on_failure:
        action: "raise ValueError(validation_result['message'])"
        log_to: "logs/step01_calibrate_irt_pass1.log"

      description: "Validate IRT parameters in acceptable ranges, no estimation failures"

    log_file: "logs/step01_calibrate_irt_pass1.log"
```

**Generated Code (g_code Output):**

```python
#!/usr/bin/env python3
"""
Step 01: Calibrate IRT Pass 1
RQ: chX/rqY
Generated: YYYY-MM-DD
"""

import sys
import pandas as pd
from pathlib import Path
from typing import Dict, List, Tuple, Any

# Setup paths
RQ_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(RQ_DIR.parent.parent))

# Import analysis and validation tools
from tools.analysis_irt import calibrate_grm
from tools.validation import validate_irt_parameters

def main():
    # Load input data
    print("[Step 01] Loading input data: data/irt_input_wide.csv")
    irt_data = pd.read_csv(RQ_DIR / "data/irt_input_wide.csv")

    # Analysis: Calibrate multidimensional GRM
    print("[Step 01] Running analysis: calibrate_grm")
    item_params, theta_scores = calibrate_grm(
        data=irt_data,
        groups={
            "What": ["RVR-OBJ-*", "RVR-ACT-*"],
            "Where": ["RVR-LOC-*", "RVR-SPA-*"],
            "When": ["RVR-TEM-*"]
        },
        config={
            "model_type": "GRM",
            "correlated_factors": True,
            "convergence_threshold": 0.001,
            "max_iterations": 1000
        }
    )

    # Save analysis outputs
    item_params.to_csv(RQ_DIR / "data/pass1_item_params.csv", index=False)
    theta_scores.to_csv(RQ_DIR / "data/pass1_theta.csv", index=False)
    print(f"[Step 01] Analysis complete. Saved {len(item_params)} items, {len(theta_scores)} theta scores")

    # Validation: Validate IRT parameters in acceptable ranges
    print("[Step 01] Running validation: validate_irt_parameters")
    validation_result = validate_irt_parameters(
        params_df=item_params,
        disc_range=(0.1, 5.0),
        diff_range=(-4.0, 4.0)
    )

    # Check validation result
    if not validation_result['valid']:
        print(f"[Step 01] VALIDATION FAILED: {validation_result['message']}")
        raise ValueError(validation_result['message'])

    print(f"[Step 01] Validation passed: {validation_result['message']}")
    print("[Step 01] Complete")

if __name__ == "__main__":
    main()
```

---

### Example: Item Purification with Validation

```yaml
  - name: "step02_purify_items"
    step_number: "02"

    analysis_call:
      module: "tools.analysis_irt"
      function: "purify_items"
      signature: "purify_items(params_df: pd.DataFrame, max_difficulty: float, min_discrimination: float) -> pd.DataFrame"

      input_files:
        - path: "data/pass1_item_params.csv"
          required_columns: ["item_name", "discrimination", "difficulty_1"]
          variable_name: "pass1_params"

      output_files:
        - path: "data/retained_items.csv"
          variable_name: "retained_items"
          description: "Items retained after 2-pass purification thresholds"

      parameters:
        params_df: "pass1_params"
        max_difficulty: 3.0      # Per Decision D039
        min_discrimination: 0.4  # Per Decision D039

      returns:
        type: "pd.DataFrame"
        variable_name: "retained_items"

      description: "Filter items meeting quality thresholds (2-pass IRT purification per Decision D039)"

    validation_call:
      module: "tools.validation"
      function: "validate_numeric_range"
      signature: "validate_numeric_range(df: pd.DataFrame, column: str, min_val: float, max_val: float) -> Dict[str, Any]"

      input_files:
        - path: "data/retained_items.csv"
          variable_name: "retained_items"
          source: "analysis call output (purify_items return value)"

      parameters:
        df: "retained_items"
        column: "discrimination"
        min_val: 0.4
        max_val: 5.0

      returns:
        type: "Dict[str, Any]"
        variable_name: "validation_result"

      criteria:
        - "All retained items have discrimination ≥ 0.4"
        - "All retained items have |difficulty| ≤ 3.0"

      on_failure:
        action: "raise ValueError(validation_result['message'])"
        log_to: "logs/step02_purify_items.log"

      description: "Validate all retained items meet Decision D039 thresholds"

    log_file: "logs/step02_purify_items.log"
```

---

### Example: LMM Fitting with Validation

```yaml
  - name: "step05_fit_lmm_trajectory"
    step_number: "05"

    analysis_call:
      module: "tools.analysis_lmm"
      function: "fit_lmm_with_tsvr"
      signature: "fit_lmm_with_tsvr(data: pd.DataFrame, formula: str, re_formula: str, groups: str) -> Tuple[Any, pd.DataFrame]"

      input_files:
        - path: "data/theta_long_with_tsvr.csv"
          required_columns: ["UID", "test", "theta", "TSVR_hours", "group"]
          variable_name: "theta_data"

      output_files:
        - path: "results/lmm_summary.txt"
          variable_name: "lmm_model"
          description: "LMM model object (saved via pickle or summary text)"
        - path: "data/lmm_coefficients.csv"
          variable_name: "lmm_coeffs"
          description: "Fixed effect coefficients from LMM"

      parameters:
        data: "theta_data"
        formula: "theta ~ TSVR_hours * group"  # Fixed effects (TSVR per Decision D070)
        re_formula: "~TSVR_hours"              # Random effects
        groups: "UID"

      returns:
        type: "Tuple[Any, pd.DataFrame]"
        unpacking: "lmm_model, lmm_coeffs"

      description: "Fit LMM with TSVR (actual hours) as time variable per Decision D070"

    validation_call:
      module: "tools.validation"
      function: "validate_lmm_convergence"
      signature: "validate_lmm_convergence(lmm_result: Any, min_observations: int) -> Dict[str, Any]"

      input_files:
        - path: "results/lmm_summary.txt"
          variable_name: "lmm_model"
          source: "analysis call output (fit_lmm_with_tsvr return value[0])"

      parameters:
        lmm_result: "lmm_model"
        min_observations: 100

      returns:
        type: "Dict[str, Any]"
        variable_name: "validation_result"

      criteria:
        - "Model converged (no warnings)"
        - "No singular fit (variance > 0)"
        - "Minimum 100 observations"

      on_failure:
        action: "raise ValueError(validation_result['message'])"
        log_to: "logs/step05_fit_lmm_trajectory.log"

      description: "Validate LMM converged successfully, no singular fit"

    log_file: "logs/step05_fit_lmm_trajectory.log"
```

---

### Example: Plotting with Validation

```yaml
  - name: "step08_plot_trajectory_dual_scale"
    step_number: "08"

    analysis_call:
      module: "tools.plotting"
      function: "plot_trajectory_probability"
      signature: "plot_trajectory_probability(theta_df: pd.DataFrame, time_col: str, theta_col: str, group_col: str, output_prefix: str) -> List[str]"

      input_files:
        - path: "data/theta_long_with_tsvr.csv"
          required_columns: ["TSVR_hours", "theta", "group"]
          variable_name: "theta_data"

      output_files:
        - path: "plots/trajectory_theta_scale.png"
          variable_name: "plot_files"  # List element [0]
          description: "Trajectory plot with theta scale"
        - path: "plots/trajectory_probability_scale.png"
          variable_name: "plot_files"  # List element [1]
          description: "Trajectory plot with probability scale (Decision D069)"

      parameters:
        theta_df: "theta_data"
        time_col: "TSVR_hours"
        theta_col: "theta"
        group_col: "group"
        output_prefix: "plots/trajectory"

      returns:
        type: "List[str]"
        variable_name: "plot_files"

      description: "Generate dual-scale trajectory plots per Decision D069"

    validation_call:
      module: "tools.validation"
      function: "validate_file_exists"
      signature: "validate_file_exists(file_path: str, min_size_bytes: int) -> Dict[str, Any]"

      input_files: []  # Validation checks file existence, not data

      parameters:
        file_path: "plots/trajectory_theta_scale.png"
        min_size_bytes: 10000

      returns:
        type: "Dict[str, Any]"
        variable_name: "validation_result"

      criteria:
        - "Both plot files exist"
        - "Each file >10KB (not empty)"

      on_failure:
        action: "raise FileNotFoundError(validation_result['message'])"
        log_to: "logs/step08_plot_trajectory.log"

      description: "Validate plot files created successfully"

    log_file: "logs/step08_plot_trajectory.log"
```

---

## How rq_analysis Creates 4_analysis.yaml

### Agent Workflow (Step 12)

The rq_analysis agent follows this process:

1. **Read** agent_best_practices.md (circuit breaker rules, YAML parsing rules)
2. **Read** status.yaml (rq_planner, rq_tools context_dumps)
3. **Read** this template (docs/v4/templates/analysis.md)
4. **Read** 2_plan.md (step order, validation requirements, expected data formats)
5. **Read** 3_tools.yaml (analysis + validation tool pairs per step)
6. **Read** names.md (step naming conventions)
7. **Ultrathink** step specifications:
   - How many steps? (from 2_plan.md)
   - What tool pairs per step? (from 3_tools.yaml)
   - What input/output files? (from 3_tools.yaml, cross-referenced with 2_plan.md)
   - What parameters? (from 3_tools.yaml)
   - What log file names? (format: logs/stepNN_name.log)
   - Are signatures complete with type hints? (CRITICAL - verify from 3_tools.yaml)
8. **Bash:** Create 4_analysis.yaml
9. **Write:** Fill with analysis + validation calls per step following this template structure
10. **Edit:** status.yaml (add analysis_steps section listing stepNN: pending for all steps)
11. **Edit:** status.yaml (update rq_analysis: success, context_dump)
12. **Report** to master: "Successfully created 4_analysis.yaml for chX/rqY with N steps"

### Critical Verification Checks

**Before writing 4_analysis.yaml, rq_analysis MUST verify:**

1. **Tool Pair Completeness:** Every step in 2_plan.md has corresponding tool pair in 3_tools.yaml
   - If missing → Circuit Breaker: TOOL_PAIR_MISSING → quit, report to master
2. **Signature Completeness:** Every analysis + validation function has full signature with type hints
   - If incomplete → Circuit Breaker: SIGNATURE_INCOMPLETE → quit, report to master
3. **Input/Output Consistency:** Validation inputs match analysis outputs
   - If mismatch → Circuit Breaker: INPUT_OUTPUT_MISMATCH → quit, report to master
4. **Log File Format:** All log files follow `logs/stepNN_name.log` pattern
   - If invalid → Circuit Breaker: LOG_PATH_INVALID → quit, report to master

**Result:** rq_analysis guarantees 4_analysis.yaml is well-formed, g_code can parse without errors.

---

## Integration with status.yaml

### analysis_steps Section

When rq_analysis completes, it updates status.yaml with `analysis_steps` section:

```yaml
# status.yaml excerpt (after rq_analysis completes)

rq_analysis:
  status: success
  context_dump: |
    Created 4_analysis.yaml with 9 steps:
    - step01_calibrate_irt_pass1
    - step02_purify_items
    - step03_calibrate_irt_pass2
    - step04_extract_theta
    - step05_merge_tsvr
    - step06_reshape_long
    - step07_fit_lmm
    - step08_plot_trajectory
    - step09_summarize_results
    All steps have analysis + validation calls.
    All signatures complete with type hints.

analysis_steps:
  step01_calibrate_irt_pass1: pending
  step02_purify_items: pending
  step03_calibrate_irt_pass2: pending
  step04_extract_theta: pending
  step05_merge_tsvr: pending
  step06_reshape_long: pending
  step07_fit_lmm: pending
  step08_plot_trajectory: pending
  step09_summarize_results: pending
```

**Usage:**
- Master tracks progress during Step 14 (CODE EXECUTION LOOP)
- After each stepNN_name.py completes successfully → master updates `stepNN: success`
- rq_inspect reads `analysis_steps` to verify prior steps completed before validating current step
- If stepN fails → remains `pending`, g_debug invoked, fixed script re-run, then updated to `success`

---

## What rq_analysis Does NOT Do

- **Does NOT create tools:** Only specifies existing tools from 3_tools.yaml
- **Does NOT execute analysis:** That's bash execution in Step 14
- **Does NOT generate code:** That's g_code job in Step 14
- **Does NOT validate outputs:** That's validation tools job during execution
- **Does NOT update analysis_steps to success:** That's master's job after successful execution

rq_analysis creates the **specification** (what calls to make), downstream agents execute it.

---

## Validation Checklist (For Template Verification)

When template is complete, verify:

- [ ] File exists at docs/v4/templates/analysis.md
- [ ] Overview section explains 4_analysis.yaml purpose and workflow context
- [ ] CRITICAL section explains validation call requirement (mandatory per step, sequential after analysis)
- [ ] g_code 4-layer validation protocol documented (import/signature/input/column checks)
- [ ] YAML Structure section documents top-level structure (steps list with nested analysis_call/validation_call/log_file)
- [ ] Analysis Call Specification section documents all required fields (module, function, signature, input_files, output_files, parameters, returns, description)
- [ ] Validation Call Specification section documents all required fields (module, function, signature, input_files, parameters, returns, criteria, on_failure, description)
- [ ] Complete Step Examples section provides 4+ examples:
  - [ ] IRT Pass 1 Calibration (analysis + validation)
  - [ ] Item Purification (analysis + validation)
  - [ ] LMM Fitting (analysis + validation)
  - [ ] Plotting (analysis + validation)
- [ ] Generated Code Example shows how g_code converts 4_analysis.yaml to stepNN_name.py
- [ ] rq_analysis workflow documented (12-step agent process)
- [ ] Critical verification checks documented (tool pair completeness, signature completeness, input/output consistency, log file format)
- [ ] Integration with status.yaml documented (analysis_steps section)
- [ ] Template is very comprehensive (800-1000 lines per user requirement)
- [ ] Nested per step YAML structure (per user requirement)
- [ ] g_code 4-layer validation protocol included (per user requirement)
- [ ] No v3.0 comparison (per user requirement - keep v4.X focused)
- [ ] Signatures emphasized throughout (prevents API mismatches)

---

## Version History

- **v4.0** (2025-11-16): Initial template created for v4.X architecture
  - Very comprehensive structure (800-1000 lines per user requirement)
  - Nested YAML structure (steps: [{name, analysis_call, validation_call, log_file}])
  - g_code 4-layer validation protocol documented
  - No v3.0 comparison (v4.X focused per user requirement)
  - Complete examples (IRT, LMM, plotting)
  - Generated code example included
  - status.yaml integration documented
  - Aligned with specification section 4.2.4

---

**End of Template Specification**
