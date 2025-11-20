# inspect_criteria.md - Validation Checklist Template (v4.X)

**Version:** 1.0.0
**Last Updated:** 2025-11-16
**Purpose:** Validation checklist specification for rq_inspect agent
**Audience:** rq_inspect agent when validating analysis step outputs
**Template Type:** Comprehensive (detailed guidance + TDD placeholders)

---

## PURPOSE

This template provides the **validation checklist framework** for the rq_inspect agent (v4.X Layer 5 validation). The rq_inspect agent uses this template to verify that each analysis step:

1. **Received correct inputs** (files exist, formats valid)
2. **Produced expected outputs** (files created, formats correct)
3. **Matches format expectations** (column names, data types)
4. **Meets plan.md criteria** (step-specific validation requirements)

**v4.X Philosophy:** Per-step validation (fail-fast) vs v3.0 end-of-pipeline validation.

**TDD Approach:** This template starts with **generic checklist structure** and **placeholder sections for step-type-specific examples**. During RQ 5.1 execution, validation checks will be discovered empirically and added to this template, following the same TDD philosophy as names.md.

---

## TDD APPROACH (Test-Driven Development)

### Initial State (v1.0.0)

This template provides:
- ✅ **4 required sections** (input/output/format/cross-reference per spec 4.3.3)
- ✅ **Generic checklist structure** (how to validate)
- ✅ **Markdown checkbox format** (v3 proven pattern)
- ⏳ **Step-type examples** (EMPTY - to be populated during RQ 5.1 TDD)

**4-Layer Validation Mapping (per solution.md section 4.3.3):**
- **Layer 1 (Existence):** Sections 1-2 (Input/Output Verification - files exist)
- **Layer 2 (Structure):** Section 3 (Format Verification - columns/dtypes/rows correct)
- **Layer 3 (Substance):** Section 4 (Cross-Reference - values reasonable per plan.md)
- **Layer 4 (Execution Log):** Section 4 (Cross-Reference - logs show convergence, no errors)

This template organizes by verification type (4 sections) but ensures all 4 layers checked per solution.md specification.

### Expected RQ 5.1 Failures

**During RQ 5.1 execution, rq_inspect will need step-specific validation checks that don't exist yet:**

1. **IRT calibration validation** (theta_scores.csv, item_parameters.csv format checks)
2. **Item purification validation** (purified_items.csv, retention rate checks per D039)
3. **LMM fitting validation** (model convergence, TSVR usage per D070)
4. **Plotting validation** (PNG files, dimensions/DPI per D069)

**When rq_inspect encounters a new step type:**
1. Agent uses **generic checklist structure** (Sections 1-4)
2. Agent extracts **step-specific criteria from 2_plan.md**
3. Agent performs validation
4. **Master and user** add discovered validation checks to this template
5. **Retry succeeds** with populated checklist

### Convention: Never Modify Existing Checks

**CRITICAL RULE:** Once a validation check is added to this template, **NEVER modify or delete it**. Changing existing checks can break validation for past RQs. **Only append new checks** with documentation of which RQ introduced them.

---

## HOW TO USE THIS TEMPLATE (for rq_inspect agent)

### Agent Workflow Integration

**rq_inspect agent performs these steps:**

```
Step 1: Read: docs/v4/agent_best_practices.md
Step 2: Read: results/chX/rqY/status.yaml
Step 3: Check: Prior analysis steps success, current step pending
Step 4: Read: docs/v4/templates/inspect_criteria.md (THIS FILE)
Step 5: Read: results/chX/rqY/docs/2_plan.md
Step 6: Read/Bash: Specified step output files (use pandas for CSV)
Step 7: Ultrathink: Verify inputs correct, outputs match plan.md expectations (else FAIL)
Step 8: Edit: status.yaml (update analysis step success + context_dump)
Step 9: Report: Success message
```

### Using the 4 Required Sections

**Section 1: Input Verification Checks**
- Verify step received correct input files
- Check input file formats and required columns
- Use checklist items from this template + 2_plan.md input specs

**Section 2: Output Verification Checks**
- Verify step created expected output files
- Check output file formats and required columns
- Use checklist items from this template + 2_plan.md output specs

**Section 3: Format Verification Checks**
- Verify column names match expectations (exact spelling, case-sensitive)
- Verify data types correct (pandas dtypes)
- Use checklist items from this template + 2_plan.md format specs

**Section 4: Cross-Reference with plan.md Expectations**
- Extract step-specific validation criteria from 2_plan.md
- Verify all criteria met (parameter ranges, special requirements)
- Use checklist items from this template + plan.md validation section

### Error Reporting: Pass/Fail

**Simple binary outcome:**

- **PASS:** All required checks passed → Edit status.yaml (analysis step = success)
- **FAIL:** Any required check failed → Circuit breaker QUIT with error report

**On FAIL, report:**
```markdown
VALIDATION FAILED: stepN for chX/rqY

Failed Checks:
- [ ] Check description (EXPECTED: X, FOUND: Y)
- [ ] Check description (EXPECTED: X, FOUND: Y)

Action Required: Fix errors and re-run stepN
```

---

## SECTION 1: INPUT VERIFICATION CHECKS

### What to Verify

Input verification ensures the analysis step **received the correct input files** before execution. Inputs typically come from:
- **Prior analysis steps** (e.g., step02 uses step01 outputs)
- **Data prep** (e.g., step01 uses irt_input.csv from data-prep agent)
- **Static files** (e.g., master.xlsx, config files)

### How to Verify

**File Existence:**
```bash
# Check file exists
test -f results/chX/rqY/data/input_file.csv && echo "EXISTS" || echo "MISSING"
```

**File Format (CSV):**
```python
# Use pandas to verify CSV format
import pandas as pd
df = pd.read_csv("results/chX/rqY/data/input_file.csv")
print(df.columns.tolist())  # Check column names
print(df.shape)  # Check dimensions (rows, columns)
```

**Required Columns:**
```python
# Verify required columns present
required_cols = ["UID", "test", "composite_ID", "response"]
missing_cols = [col for col in required_cols if col not in df.columns]
if missing_cols:
    print(f"MISSING COLUMNS: {missing_cols}")
else:
    print("ALL REQUIRED COLUMNS PRESENT")
```

### Generic Checklist Structure

**For each input file specified in 2_plan.md:**

```markdown
#### Input File: {filename}

- [ ] File exists at expected path (results/chX/rqY/data/{filename})
- [ ] File is valid CSV format (pandas can read without errors)
- [ ] Required columns present: {list from plan.md}
- [ ] Column data types correct: {types from plan.md}
- [ ] No empty/null values in required columns (unless allowed per plan.md)
- [ ] Row count matches expectations: {expected range from plan.md}
```

### Step-Type-Specific Examples

**STATUS:** TDD - To be populated during RQ 5.1 execution

#### Example: IRT Calibration (step01_calibrate_irt)

**TDD PLACEHOLDER:** This section will be populated when RQ 5.1 reaches step01. Expected validation checks:
- Input file: irt_input.csv
- Required columns: UID, test, composite_ID, response (and dimension columns)
- Data types: response = int64 (0 or 1, dichotomous scoring per D041)
- Row count: N participants × M items × 4 tests (expected: ~40,800 for RQ 5.1)

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first IRT calibration validation

---

#### Example: Item Purification (step02_purify_items)

**TDD PLACEHOLDER:** This section will be populated when RQ 5.1 reaches step02. Expected validation checks:
- Input file: pass1_item_params.csv (from step01)
- Required columns: item, Difficulty, Discrimination (and possibly dimension columns for multivariate IRT)
- Data types: Difficulty/Discrimination = float64
- Row count: Number of items calibrated in Pass 1

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first purification validation

---

#### Example: LMM Fitting (stepN_fit_lmm)

**TDD PLACEHOLDER:** This section will be populated when RQ 5.1 reaches LMM step. Expected validation checks:
- Input file: theta_scores.csv (IRT theta estimates from prior step)
- Required columns: composite_ID, theta
- Merge requirement: TSVR (Time Since VR) per Decision D070
- Data format: Wide or long format (depends on plan.md specification)

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first LMM fitting validation

---

#### Example: Plotting (stepN_plot_results)

**TDD PLACEHOLDER:** This section will be populated when RQ 5.1 reaches plotting step. Expected validation checks:
- Input files: Statistical results (coefficients, p-values, effect sizes)
- Required columns: Depends on plot type (trajectory plots need theta/TSVR, effect size plots need estimates/CI)
- Special requirements: Dual-scale trajectory plots per Decision D069 (theta + probability scales)

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first plotting validation

---

## SECTION 2: OUTPUT VERIFICATION CHECKS

### What to Verify

Output verification ensures the analysis step **created the expected output files** as specified in 2_plan.md. Outputs become inputs for subsequent steps, so correctness is critical for preventing cascading failures.

### How to Verify

**File Creation:**
```bash
# Check output file created
test -f results/chX/rqY/data/output_file.csv && echo "CREATED" || echo "MISSING"
```

**File Not Empty:**
```bash
# Check file has content (not 0 bytes)
[ -s results/chX/rqY/data/output_file.csv ] && echo "HAS CONTENT" || echo "EMPTY FILE"
```

**Output Format (CSV):**
```python
# Verify CSV format
import pandas as pd
df = pd.read_csv("results/chX/rqY/data/output_file.csv")
print(f"Output shape: {df.shape}")  # Verify rows and columns created
print(f"Output columns: {df.columns.tolist()}")
```

**Output Completeness:**
```python
# Check for unexpected missing values
null_counts = df.isnull().sum()
if null_counts.any():
    print(f"NULL VALUES DETECTED:\n{null_counts[null_counts > 0]}")
else:
    print("NO NULL VALUES (complete output)")
```

### Generic Checklist Structure

**For each output file specified in 2_plan.md:**

```markdown
#### Output File: {filename}

- [ ] File created at expected path (results/chX/rqY/data/{filename})
- [ ] File is not empty (> 0 bytes)
- [ ] File is valid CSV format (pandas can read without errors)
- [ ] Expected columns present: {list from plan.md}
- [ ] Column data types correct: {types from plan.md}
- [ ] No unexpected null values (check against plan.md expectations)
- [ ] Row count matches expectations: {expected range from plan.md}
- [ ] Output contains actual data (not placeholder/mock values)
```

### Step-Type-Specific Examples

**STATUS:** TDD - To be populated during RQ 5.1 execution

#### Example: IRT Calibration Output (step01_calibrate_irt)

**TDD PLACEHOLDER:** Expected validation checks:
- Output files: theta_scores.csv, item_parameters.csv
- theta_scores.csv columns: composite_ID, theta (and possibly SE_theta)
- item_parameters.csv columns: item, Difficulty, Discrimination (and dimension info for multivariate)
- Row counts: theta_scores = N composite_IDs, item_parameters = M items
- No mock data check: Verify theta values are not generated via logit transform (per safety fix from archive)

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first IRT calibration validation

---

#### Example: Item Purification Output (step02_purify_items)

**TDD PLACEHOLDER:** Expected validation checks:
- Output file: purified_items.csv
- Required columns: item, Difficulty, Discrimination, retained (boolean)
- Retention rate: 40-50% expected per D039 thresholds (|b| ≤ 3.0, a ≥ 0.4)
- Purified item count: Should match number of TRUE values in retained column

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first purification validation

---

#### Example: LMM Fitting Output (stepN_fit_lmm)

**TDD PLACEHOLDER:** Expected validation checks:
- Output files: lmm_summary.csv, lmm_coefficients.csv
- Model convergence: Check convergence status in summary
- TSVR usage: Verify time variable is TSVR (not nominal days) per D070
- Coefficient extraction: Fixed and random effects present

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first LMM fitting validation

---

#### Example: Plotting Output (stepN_plot_results)

**TDD PLACEHOLDER:** Expected validation checks:
- Output files: PNG files in results/chX/rqY/plots/
- File existence: All expected plots created
- File format: Valid PNG images
- Dimensions/DPI: Per D069 specifications for dual-scale trajectory plots
- Dual-scale requirement: Trajectory plots have both theta and probability axes

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first plotting validation

---

## SECTION 3: FORMAT VERIFICATION CHECKS

### What to Verify

Format verification ensures **column names and data types match expectations**. This prevents downstream errors caused by:
- Column name typos (case-sensitive, spelling errors)
- Wrong data types (string vs int, object vs float)
- Unexpected column additions/deletions

### How to Verify

**Column Names (Exact Match):**
```python
# Verify exact column names (case-sensitive)
expected_cols = ["UID", "test", "composite_ID", "response"]
actual_cols = df.columns.tolist()

if actual_cols != expected_cols:
    print(f"COLUMN MISMATCH:")
    print(f"  Expected: {expected_cols}")
    print(f"  Actual:   {actual_cols}")
else:
    print("COLUMN NAMES MATCH")
```

**Data Types:**
```python
# Verify column data types
expected_dtypes = {
    "UID": "object",
    "test": "int64",
    "composite_ID": "object",
    "response": "int64"
}

actual_dtypes = df.dtypes.to_dict()
mismatches = {col: (expected_dtypes[col], str(actual_dtypes[col]))
              for col in expected_cols
              if str(actual_dtypes[col]) != expected_dtypes[col]}

if mismatches:
    print(f"DATA TYPE MISMATCHES: {mismatches}")
else:
    print("DATA TYPES MATCH")
```

**Value Ranges (if specified in plan.md):**
```python
# Check value ranges for numeric columns
if "response" in df.columns:
    unique_values = df["response"].unique()
    if set(unique_values) != {0, 1}:
        print(f"INVALID RESPONSE VALUES: {unique_values} (expected: [0, 1])")
    else:
        print("RESPONSE VALUES VALID (dichotomous)")
```

### Generic Checklist Structure

**For each file (input or output):**

```markdown
#### Format Verification: {filename}

- [ ] Column names match expectations (exact, case-sensitive): {list from plan.md}
- [ ] No extra columns present (unless allowed per plan.md)
- [ ] No missing columns
- [ ] Column data types correct: {types from plan.md}
- [ ] Value ranges valid (if specified): {ranges from plan.md}
- [ ] No data type coercion errors (e.g., numeric stored as string)
```

### Step-Type-Specific Examples

**STATUS:** TDD - To be populated during RQ 5.1 execution

#### Example: IRT Input Format (irt_input.csv)

**TDD PLACEHOLDER:** Expected format checks:
- Columns: UID, test, composite_ID, response, [dimension columns]
- UID format: A10XXXXX (alphanumeric, 8 chars per data_structure.md)
- test: int64 (0, 1, 3, 6 for REMEMVR paradigm per data_structure.md)
- composite_ID: object (UID_test_item format, e.g., A10ABC01_0_RVR-S-01)
- response: int64 (0 or 1, dichotomous scoring per D041)
- Dimension columns: int64 (0 or 1 for multidimensional IRT)

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first IRT input validation

---

#### Example: Theta Scores Format (theta_scores.csv)

**TDD PLACEHOLDER:** Expected format checks:
- Columns: composite_ID, theta (and possibly SE_theta, EAP, MAP depending on IRT method)
- composite_ID: object (same format as IRT input)
- theta: float64 (typically range -4 to +4 for standardized IRT)
- No duplicate composite_IDs (each should be unique)

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first theta extraction validation

---

#### Example: Item Parameters Format (item_parameters.csv)

**TDD PLACEHOLDER:** Expected format checks:
- Columns: item, Difficulty, Discrimination (and dimension info for multivariate)
- item: object (item code, e.g., RVR-S-01)
- Difficulty: float64 (b parameter, typically -3 to +3)
- Discrimination: float64 (a parameter, typically 0 to 4)
- For multivariate IRT: additional columns per dimension

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first IRT calibration validation

---

## SECTION 4: CROSS-REFERENCE WITH PLAN.MD EXPECTATIONS

### What to Verify

This section ensures the analysis step **meets step-specific validation criteria** defined in 2_plan.md. While Sections 1-3 verify generic file/format correctness, Section 4 verifies **analysis-specific requirements**.

### How to Extract Criteria from plan.md

**rq_inspect agent workflow:**

1. **Read 2_plan.md** from results/chX/rqY/docs/
2. **Locate step section** (e.g., "Step 1: IRT Calibration - Pass 1")
3. **Extract validation requirements** from step's validation subsection
4. **Compare actual outputs** against plan.md expectations

**Example plan.md structure:**

```markdown
### Step 1: IRT Calibration - Pass 1

**Input Files:**
- irt_input.csv (from data-prep)

**Output Files:**
- theta_scores.csv
- item_parameters.csv

**Validation Requirements:**
- Model convergence: IWAVE calibration should converge (check logs)
- Theta range: -4 to +4 (standardized IRT scale)
- Item parameters: a ≥ 0, |b| ≤ 5 (reasonable ranges before purification)
- No missing estimates: All composite_IDs have theta scores
```

### How to Verify Plan.md Criteria

**Step 1: Extract Validation Requirements**
```markdown
From plan.md "Validation Requirements" section:
- Model convergence check
- Theta range check
- Item parameter range check
- Completeness check
```

**Step 2: Verify Each Requirement**
```python
# Example: Verify theta range
theta_min = df["theta"].min()
theta_max = df["theta"].max()
if theta_min < -4 or theta_max > 4:
    print(f"THETA OUT OF RANGE: [{theta_min}, {theta_max}] (expected: [-4, +4])")
else:
    print("THETA RANGE VALID")
```

**Step 3: Report Results**
- PASS: All plan.md criteria met
- FAIL: Any criterion not met (report which ones)

### Generic Checklist Structure

**For each step validation (from plan.md):**

```markdown
#### Cross-Reference: {stepN_name}

**From plan.md Validation Requirements:**

- [ ] Criterion 1 from plan.md: {description}
- [ ] Criterion 2 from plan.md: {description}
- [ ] Criterion 3 from plan.md: {description}
- [ ] Special requirements met: {any RQ-specific needs from plan.md}
- [ ] Project-specific decisions satisfied: {D039, D068, D069, D070 if applicable}
```

### Step-Type-Specific Examples

**STATUS:** TDD - To be populated during RQ 5.1 execution

#### Example: IRT Calibration Validation (step01)

**TDD PLACEHOLDER:** Expected plan.md criteria:
- Model convergence: Check logs/step01_calibrate_irt.log for convergence status
- Theta estimates: All composite_IDs have theta scores (no missing)
- Item parameters: Reasonable ranges (a ≥ 0, finite b values)
- Runtime: Calibration completed within expected time (not timeout)
- Decision D039 awareness: Pass 1 calibrates all items (purification happens in Pass 2)

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first IRT calibration validation

---

#### Example: Item Purification Validation (step02)

**TDD PLACEHOLDER:** Expected plan.md criteria:
- Purification thresholds applied: |b| ≤ 3.0, a ≥ 0.4 per Decision D039
- Retention rate: 40-50% expected (temporal items have extreme difficulty)
- Purified item count: Documented in plan.md as expected N items
- Decision D039 compliance: 2-pass IRT methodology confirmed

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first purification validation

---

#### Example: LMM Fitting Validation (stepN)

**TDD PLACEHOLDER:** Expected plan.md criteria:
- Model convergence: LMM fit converged successfully
- TSVR usage: Time variable is TSVR (actual hours) not nominal days per Decision D070
- Fixed effects: Expected predictors included
- Random effects: Subject-level random intercepts (at minimum)
- Coefficient extraction: All specified effects present in output

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first LMM fitting validation

---

#### Example: Plotting Validation (stepN)

**TDD PLACEHOLDER:** Expected plan.md criteria:
- All required plots generated: List from plan.md present in plots/
- Plot format: PNG with specified dimensions/DPI
- Dual-scale requirement: Trajectory plots have both theta and probability axes per Decision D069
- Consistent theme: All plots use tools/plots.py functions (consistent styling across RQs)

**Introduced:** RQ 5.1 (expected)
**Notes:** To be added after first plotting validation

---

## ERROR REPORTING (Pass/Fail Instructions)

### Pass Outcome

**When all checks pass:**

```markdown
VALIDATION PASSED: stepN for chX/rqY

All checks passed:
- ✓ Input files verified
- ✓ Output files created
- ✓ Formats match expectations
- ✓ Plan.md criteria satisfied

Action: rq_inspect updates status.yaml (analysis stepN = success)
```

**rq_inspect agent actions:**
1. Edit status.yaml: analysis_steps → stepN → status: success
2. Edit status.yaml: context_dump with validation summary
3. Report success to master

### Fail Outcome

**When any check fails:**

```markdown
VALIDATION FAILED: stepN for chX/rqY

Failed checks:
- [ ] Input file missing: {filename} (EXPECTED: path/to/file, FOUND: not exists)
- [ ] Output column mismatch: {filename} (EXPECTED: [col1, col2], FOUND: [col1, col3])
- [ ] Format violation: {filename} column {colname} (EXPECTED: int64, FOUND: object)
- [ ] Plan.md criterion not met: {description} (EXPECTED: X, FOUND: Y)

Action Required:
1. Review failed checks above
2. Debug using g_debug agent (master invokes)
3. Fix errors (code/data/config)
4. Re-run stepN
5. Re-run rq_inspect validation
```

**rq_inspect agent actions:**
1. Circuit breaker: QUIT with VALIDATION_FAILED error
2. Report failure details to master (which checks failed, expected vs found)
3. DO NOT update status.yaml (leave analysis stepN = pending)
4. Master invokes g_debug agent to identify root cause

### Severity: All Checks Required

**v4.X Philosophy:** Simple pass/fail (no severity levels)

- All checks in Sections 1-4 are **REQUIRED**
- Any failure = FAIL (no warnings or optional checks)
- Fail-fast: Catch errors immediately, don't proceed

**Rationale:** Prevents cascading failures (v3.0 lesson learned)

---

## INTEGRATION WITH RQ_INSPECT WORKFLOW

### Agent Invocation Context

**Master invokes rq_inspect after:**
- Analysis step executed (e.g., bash poetry run python code/step01_calibrate_irt.py)
- Validation tool ran (embedded in analysis step per 4_analysis.yaml)
- Log file created (logs/stepN_name.log)

**rq_inspect validates:**
- Analysis step outputs (not validation tool outputs - those are self-validating)
- Step completed successfully
- Outputs ready for next step

### Status.yaml Integration

**rq_inspect reads status.yaml:**

```yaml
analysis_steps:
  step01_calibrate_irt:
    status: success
  step02_purify_items:
    status: pending  # ← rq_inspect validates this step
```

**After validation PASS, rq_inspect updates:**

```yaml
analysis_steps:
  step01_calibrate_irt:
    status: success
  step02_purify_items:
    status: success  # ← Updated by rq_inspect
```

**After validation FAIL, rq_inspect leaves unchanged:**

```yaml
analysis_steps:
  step02_purify_items:
    status: pending  # ← Still pending, requires re-run
```

### Context Dump Format

**rq_inspect writes to status.yaml context_dump:**

```markdown
**rq_inspect:**
- Validated: step02_purify_items
- Inputs verified: pass1_item_params.csv (102 items)
- Outputs verified: purified_items.csv (43 items retained, 42.2%)
- Format checks: All columns present, data types correct
- Plan.md criteria: Purification thresholds met (|b| ≤ 3.0, a ≥ 0.4)
- Result: PASS
```

**Concise summary for other agents to understand what was validated**

---

## TDD APPROACH: Adding Examples During RQ 5.1

### When to Add Examples

**After each new step type validation in RQ 5.1:**

1. **rq_inspect completes validation** (uses generic checklist + plan.md criteria)
2. **Master reviews what checks were performed**
3. **Master and user add checks to this template** under appropriate step-type example section
4. **Document which RQ introduced the example** (RQ 5.1, RQ 5.2, etc.)
5. **Future RQs use populated examples** as starting point

### How to Add Examples

**Template for new step-type example:**

```markdown
#### Example: {Step Type Name} ({stepNN_name})

**Validation Checks:**

**Section 1: Input Verification**
- [ ] Input file: {filename}
- [ ] Required columns: {list}
- [ ] Data types: {types}
- [ ] Row count: {expected range}

**Section 2: Output Verification**
- [ ] Output file: {filename}
- [ ] Expected columns: {list}
- [ ] Data types: {types}
- [ ] Row count: {expected range}
- [ ] No mock data: {specific check}

**Section 3: Format Verification**
- [ ] Column name format: {exact names}
- [ ] Value ranges: {ranges}

**Section 4: Plan.md Criteria**
- [ ] Criterion 1: {description}
- [ ] Criterion 2: {description}
- [ ] Decision compliance: {D0XX if applicable}

**Introduced:** RQ {X.Y}
**Notes:** {Any special considerations discovered during validation}
```

### Never Modify Existing Examples

**CRITICAL:** Once an example is added, **NEVER modify or delete checks**. Changing existing validation can break past RQs that depend on those checks.

**If a check needs updating:**
- Add NEW check with version note (e.g., "Added in RQ 5.3 to handle edge case")
- Keep old check for backwards compatibility
- Document why new check added

---

## CIRCUIT BREAKERS (Error Detection)

### When rq_inspect Should QUIT

**Circuit breaker triggers:**

1. **VALIDATION_FAILED:** Any required check failed (input/output/format/plan.md)
   - Report which checks failed
   - DO NOT update status.yaml
   - Master invokes g_debug

2. **PLAN_MD_MISSING:** Cannot read 2_plan.md (file doesn't exist or corrupted)
   - Report error
   - QUIT (cannot validate without plan.md criteria)

3. **STATUS_YAML_CORRUPTED:** Cannot parse status.yaml (YAML syntax error)
   - Report error
   - QUIT (cannot determine step status or update)

4. **STEP_NOT_FOUND:** Specified step doesn't exist in status.yaml analysis_steps section
   - Report error
   - QUIT (step wasn't added to status.yaml by rq_analysis)

5. **PRIOR_STEP_FAILED:** Prior analysis step status ≠ success (cannot validate current step if previous failed)
   - Report which prior step failed
   - QUIT (fix prior step first)

### Error Message Format

```markdown
CIRCUIT BREAKER TRIGGERED: {ERROR_TYPE}

Context:
- RQ: chX/rqY
- Step: stepN_name
- Trigger: {description of what caused error}

Details:
{Specific error information}

Action Required:
{What master/user should do to fix}
```

---

## INTEGRATION WITH MULTI-LAYER VALIDATION ARCHITECTURE

### v4.X 5-Layer Validation Defense

**rq_inspect is Layer 5 of multi-layer validation:**

**Layer 1: Tool Inventory (tools_inventory.md)**
- Documents both analysis tools AND validation tools
- Provides function signatures with type hints

**Layer 2: rq_tools (3_tools.yaml)**
- Specifies both analysis tool AND validation tool per step
- Paired validation (validation tool validates analysis tool output)

**Layer 3: rq_planner (2_plan.md)**
- States "Validation tools MUST be used after analysis tool execution"
- Specifies validation criteria per step

**Layer 4: rq_analysis (4_analysis.yaml)**
- Embeds validation tool call at END of each analysis step
- Enforces validation signatures (prevents API guessing)

**Layer 5: rq_inspect (this template) ← YOU ARE HERE**
- Validates step outputs match plan.md expectations
- Checks input/output/format/cross-reference
- Final verification before proceeding to next step

### Why Layer 5 Needed (Layers 1-4 not sufficient)

**Layers 1-4 prevent:**
- API mismatches (Layer 1-2: signatures enforced)
- Cascading errors (Layer 2-4: validation embedded in steps)
- Missing validation (Layer 3: validation mandated)

**Layer 5 (rq_inspect) adds:**
- **Human verification checkpoint:** Master sees validation results before proceeding
- **Plan.md cross-reference:** Ensures outputs match original plan (not just tool specs)
- **Step-by-step gates:** Each step must pass before next step runs
- **Context accumulation:** status.yaml context_dump builds understanding across steps

**Redundancy is intentional:** Multiple layers catch errors at different points (defense in depth)

---

## V3.0 VS V4.X DIFFERENCES (Historical Context)

### v3.0 results_inspector Approach

**When:** End-of-pipeline (after all analysis complete)
**Scope:** Validate entire RQ outputs together
**Focus:** Publication readiness (statistical correctness, interpretation quality, scholarly summary)
**Outcome:** APPROVED / CONDITIONAL / REJECTED decision
**Timing:** 60+ minutes after analysis start

**Limitations (why v3.0 failed):**
- Errors discovered too late (after hours of runtime)
- Cascading failures (early errors corrupted later steps)
- No per-step validation (all-or-nothing approach)

### v4.X rq_inspect Approach

**When:** After EACH analysis step (per-step validation)
**Scope:** Validate single step outputs
**Focus:** Technical correctness (files exist, formats valid, plan.md criteria met)
**Outcome:** PASS / FAIL (simple binary)
**Timing:** Immediately after step execution (fail-fast)

**Advantages (why v4.X should succeed):**
- Errors caught immediately (within seconds of occurrence)
- Prevents cascading (bad step outputs caught before next step runs)
- Per-step gates (each step validated independently)
- Rapid iteration (fix → re-run → validate in minutes)

### Migration Notes

**What changed:**
- End-of-pipeline → Per-step validation
- Publication assessment → Technical verification
- Comprehensive report → Simple pass/fail
- Single invocation → Multiple invocations (one per step)

**What stayed the same:**
- Checklist structure (v3 validation checklists proven effective)
- Markdown format (human-readable)
- Input/output/format verification (core validation needs)

**What's new:**
- Plan.md cross-reference (v4.X planning-driven validation)
- TDD approach (populate examples during RQ 5.1)
- Multi-layer integration (Layer 5 of 5-layer defense)
- Status.yaml integration (pseudo-statefulness via context dumps)

---

## IMPLEMENTATION NOTES

### For Master (Main Claude)

**When to invoke rq_inspect:**

```
Step 14 CODE EXECUTION LOOP (automation.md):
  14.1: Master reads 4_analysis.yaml
  14.2: For each analysis step:
    14.3: Master invokes g_code (generates stepN.py with validation embedded)
    14.4: Master runs: bash poetry run python code/stepN.py
    14.5: Master checks: exit code 0 = success, non-zero = error
    14.6: IF error: Master invokes g_debug → fix → re-run → loop to 14.4
    14.7: IF success: Master invokes rq_inspect ← VALIDATION CHECKPOINT
    14.8: IF rq_inspect PASS: Continue to next step (loop to 14.2)
    14.9: IF rq_inspect FAIL: Master invokes g_debug → fix → re-run step → loop to 14.4
```

**rq_inspect is mandatory gate between steps**

### For rq_inspect Agent

**Read these files in order:**
1. agent_best_practices.md (circuit breakers, platform rules)
2. status.yaml (check prior steps success, current step pending)
3. inspect_criteria.md (THIS FILE - checklist framework)
4. 2_plan.md (step-specific validation criteria)
5. Step output files (verify using pandas for CSV)

**Use generic checklist + plan.md criteria + step-type examples (if populated)**

**Report:**
- Success: "Successfully validated stepN outputs for chX/rqY"
- Failure: "VALIDATION FAILED: stepN for chX/rqY" + details

### For Users

**During RQ 5.1 execution:**
- Expect validation failures (TDD - examples not populated yet)
- Review rq_inspect validation results
- Work with master to add discovered checks to this template
- Document which RQ introduced each check
- Never modify existing checks (only append)

**After RQ 5.1:**
- inspect_criteria.md will have populated examples
- Subsequent RQs will use these as starting point
- Continue adding checks as new step types discovered

---

## VERSION HISTORY

### v1.0.0 (2025-11-16)

**Initial template creation**

**Includes:**
- 4 required sections (input/output/format/cross-reference per spec 4.3.3)
- Generic checklist structure (how to validate)
- Markdown checkbox format (v3 proven pattern)
- TDD placeholders for step-type examples (IRT, purification, LMM, plotting)
- Simple pass/fail error reporting
- Integration with rq_inspect workflow
- Multi-layer validation architecture context
- v3.0 vs v4.X comparison

**Status:** TDD - Examples to be populated during RQ 5.1 execution

**Next:** RQ 5.1 will discover validation checks empirically, populate example sections

---

**End of inspect_criteria.md Template**
