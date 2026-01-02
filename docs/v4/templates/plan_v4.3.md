# plan.md Template Specification

**Version:** 4.3
**Last Updated:** 2026-01-02
**Purpose:** Specification for 2_plan.md format (analysis plan created by rq_planner agent)
**Audience:** rq_planner agent when creating 2_plan.md for RQ workflow
**Status:** Current (v4.X architecture with Ch7 enhancements)

---

## CRITICAL - ASCII-Only Format

**Per universal.md Section 2.1:** ALL content in 2_plan.md must use ASCII-only characters for WSL2/Windows compatibility.

**Mathematical Notation - Use ASCII equivalents ONLY:**
- Multiplication: Use `x` not `×` (example: "100 x 4 tests")
- Set membership: Use `in` not `∈` (example: "theta in [-3, 3]")
- Comparisons: Use `>=` not `≥`, `<=` not `≤`
- Arrows: Use `->` not `→`
- Ranges: Write as words (example: "theta range: [-3, 3]" or "theta: -3 to 3")

**Why:** Unicode symbols (×, ∈, ≥, →) cause encoding issues in WSL2, displaying as � or backspace characters. ASCII ensures universal compatibility.

---

## NEW IN v4.3: Statistical Implementation Requirements

### Cross-Validation Specifications

When implementing k-fold cross-validation, ALWAYS specify:
- **Number of folds:** Default 5-fold unless sample size requires adjustment
- **Random seed:** ALWAYS set seed=42 for reproducibility
- **Stratification:** For regression, use quantile-based stratification if outcome is skewed
- **Resampling strategy:** Use KFold from sklearn with shuffle=True
- **Generalization gap threshold:** train-test R² difference should be < 0.10

**Example:**
```markdown
**Processing:**
- Implement 5-fold cross-validation using sklearn.model_selection.KFold
- Random seed: 42 for reproducibility
- Shuffle: True (randomize before splitting)
- For each fold: fit model on training set, evaluate on test set
- Compute mean and std of R² across folds
- Flag if train-test gap > 0.10 (overfitting detected)
```

### Bootstrap Specifications

When implementing bootstrap procedures, ALWAYS specify:
- **Number of iterations:** Default 1000 unless computationally prohibitive
- **Random seed:** ALWAYS set seed=42 for reproducibility
- **Resampling unit:** Participant-level for hierarchical data, observation-level for independent data
- **Replacement:** With replacement (standard bootstrap)
- **CI method:** Percentile method (2.5th and 97.5th percentiles for 95% CI)

**Example:**
```markdown
**Processing:**
- Implement participant-level block bootstrap (preserves within-participant correlation)
- Iterations: 1000
- Random seed: 42 for reproducibility
- For each iteration:
  - Resample participants WITH replacement
  - Keep all observations for selected participants
  - Fit both models, compute R² difference
- CI computation: percentile method (2.5th, 97.5th percentiles)
```

### Power Analysis Specifications

When implementing power analysis, ALWAYS specify:
- **Type:** Post-hoc (for completed analyses) or a priori (for planning)
- **Effect size metric:** Cohen's f² for regression, Cohen's d for t-tests
- **Alpha level:** Chapter-specific (e.g., 0.05/28 = 0.00179 for Ch7)
- **Power target:** 0.80 (standard)
- **Software:** statsmodels.stats.power or G*Power calculations

**Example:**
```markdown
**Processing:**
- Post-hoc power analysis for hierarchical regression
- Given: N=100, 12 predictors, alpha=0.00179
- Calculate: minimum detectable f² at 80% power
- Use: statsmodels.stats.power.FTestAnovaPower()
- Report: actual power for observed effect sizes
- If power < 0.80: acknowledge limitation in interpretation
```

### Multiple Comparison Corrections

When implementing Bonferroni or other corrections, ALWAYS specify:
- **Family definition:** Within-RQ, within-theme, or chapter-level
- **Number of tests:** Explicit count with justification
- **Correction method:** Bonferroni (conservative) or FDR (less conservative)
- **Dual reporting:** ALWAYS report both uncorrected AND corrected p-values (Decision D068)

**Example:**
```markdown
**Processing:**
- Family: Within-RQ comparisons (3 predictors x 2 models = 6 tests)
- Bonferroni correction: alpha = 0.05/6 = 0.0083 per test
- Also compute FDR-adjusted p-values using Benjamini-Hochberg
- Report BOTH uncorrected AND corrected p-values (Decision D068)
- Format: p_uncorrected = 0.023, p_bonferroni = 0.138, p_fdr = 0.069
```

### Remedial Actions for Assumption Violations

When checking statistical assumptions, ALWAYS specify remedial actions:

**Normality Violations:**
- Minor: Report with acknowledgment, use robust standard errors
- Moderate: Apply transformation (log, sqrt) or use bootstrap CIs
- Severe: Use non-parametric alternatives

**Heteroscedasticity:**
- Use HC3 heteroscedasticity-consistent standard errors
- Report both regular and robust SEs

**Multicollinearity:**
- VIF 5-10: Acknowledge, proceed with caution
- VIF > 10: Drop collinear predictors or use ridge regression

**Outliers:**
- Cook's D > 4/n: Report results with and without outliers
- Document number and nature of outliers

**Example:**
```markdown
**Processing:**
- Check assumptions: normality (Shapiro-Wilk), homoscedasticity (Breusch-Pagan), VIF
- Remedial actions if violated:
  - Normality p < 0.05: Use bootstrap CIs (1000 iterations)
  - Heteroscedasticity p < 0.05: Report HC3 robust SEs
  - VIF > 5: Document multicollinearity, consider ridge if VIF > 10
  - Outliers (Cook's D > 0.04): Report with/without outliers
```

### Cross-RQ File Path Verification

When referencing outputs from other RQs, ALWAYS:
- Verify actual file names (don't assume)
- Include fallback paths if naming conventions vary
- Document expected format even if file name uncertain

**Example:**
```markdown
**Input:**
- Primary path: results/ch5/5.1.1/data/step05_lmm_model_summary.txt
- Alternative: results/ch5/5.1.1/data/lmm_fitted_model.rds
- Fallback: results/ch5/5.1.1/data/*lmm*.{txt,rds,csv}
- Expected content: Fitted LMM object with random effects
- If none exist: QUIT with "Ch5 5.1.1 LMM output not found"
```

---

## Overview

### What is 2_plan.md?

The 2_plan.md file is the **master analysis plan** for an RQ. It is created by the **rq_planner agent** and consumed by downstream agents (rq_tools, rq_analysis, g_code, rq_inspect) to understand the step-by-step analysis workflow.

**Key Characteristics:**
- **Agent-to-agent specification** (not user-facing)
- **Numbered step structure** (step 0, step 1, ... step N)
- **Input/output contracts** per step (file paths, formats, columns)
- **Validation requirements** embedded (MANDATORY per step with 4-layer criteria)
- **Statistical implementation details** (NEW in v4.3 - seeds, iterations, remedial actions)
- **Dependencies documented** (cross-RQ data requirements if applicable)
- **Tool-agnostic language** (rq_tools determines exact tools, planner specifies what needs to happen)

### Workflow Context

```
Step 9 (Workflow): rq_planner creates 2_plan.md
                   ↓
Step 11 (Workflow): rq_tools reads 2_plan.md  ->  creates 3_tools.yaml
                   ↓
Step 12 (Workflow): rq_analysis reads 2_plan.md + 3_tools.yaml  ->  creates 4_analysis.yaml
                   ↓
Step 14 (Workflow): g_code reads 4_analysis.yaml (derived from plan)  ->  generates code
                   ↓
Step 14 (Workflow): rq_inspect reads 2_plan.md  ->  validates outputs match expectations
```

**Critical Role:** The plan is the **contract** between planning agents and execution agents. If plan is vague, downstream agents will fail or guess incorrectly.

---

## CRITICAL: Validation Requirements

### Global Validation Mandate

**EVERY analysis step in 2_plan.md MUST include validation requirements with 4-layer substance criteria.**

This is not optional. This is not "nice to have." This is the **foundation of v4.X architecture** preventing cascading failures that plagued v3.0.

### 4-Layer Substance Validation Structure (MANDATORY)

Each step MUST include ALL FOUR layers with these exact headers:

1. **Output Files:** Exact paths, row counts, column counts, data types
2. **Value Ranges:** Scientific bounds (theta in [-3, 3], p in [0, 1])
3. **Data Quality:** Missing data tolerance, expected N, distribution checks
4. **Log Validation:** Required patterns, forbidden patterns, acceptable warnings

### Mandatory Text (From Specification)

The plan MUST state for each step:

> **"Validation tools MUST be used after analysis tool execution"**

### How rq_planner States This

**In each step's specification:**

```
### Step N: [Step Name]

**Purpose:** [What this step accomplishes]

**Input:**
- [Input files/data with exact paths or patterns]

**Processing:**
- [What analysis happens with implementation details]
- [Statistical specifications: seeds, iterations, corrections]
- [Remedial actions for assumption violations]

**Output:**
- [Output files/data with exact paths]

**Validation Requirement:**
Validation tools MUST be used after analysis tool execution. Specific validation
tools will be determined by rq_tools based on analysis type. 

**Substance Validation Criteria (for rq_inspect post-execution validation):**

*Output Files:*
- [Exact file paths, expected row counts, expected column counts, data types]

*Value Ranges:*
- [Expected value ranges with scientific justification]

*Data Quality:*
- [Missing data tolerance, expected N, duplicate checks, distribution checks]

*Log Validation:*
- Required patterns: [specific success messages]
- Forbidden patterns: ["ERROR", "FAIL", specific failure messages]
- Acceptable warnings: [known non-critical warnings]

**Expected Behavior on Validation Failure:**
[What should happen if validation fails - e.g., quit with error, log warning, etc.]
```

---

## Required Sections

The 2_plan.md file MUST contain the following sections:

### 1. Step-by-Step Analysis Plan (Numbered Steps)

**Purpose:** Define the complete analysis workflow from data extraction to final outputs.

**Step Numbering Convention:**
- **Step 0:** ALWAYS use for dependency validation or prerequisite checks
- **Step 1+:** Main analysis steps
- **Documentation format:** "Step 0", "Step 1", "Step 2" (human-readable)
- **File naming format:** "step00", "step01", "step02" (zero-padded for sorting)

**Example Structure:**

```markdown
## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
**Dependencies:** None (prerequisite validation step)
**Complexity:** Low (<5 minutes)

**Purpose:** Verify required Ch5 outputs exist before proceeding

**Input:**
- results/ch5/5.1.1/status.yaml (verify rq_results: success)
- results/ch5/5.1.1/data/*lmm*.{txt,rds,csv} (find LMM output)

**Processing:**
- Check Ch5 5.1.1 completed successfully
- Locate LMM model file (try multiple patterns)
- Verify file contains random effects
- Log validation results

**Output:**
- data/step00_dependency_validation.txt

**Validation Requirement:**
Validation tools MUST be used after dependency check execution.

**Substance Validation Criteria:**
[4-layer validation structure as shown above]

### Step 1: Extract and Prepare Data
[Continue with main analysis steps...]
```

---

### 2. Input Specifications Per Step

Must include:
- **Exact file paths** or **search patterns** for cross-RQ dependencies
- **Fallback options** if primary path not found
- **Format verification** (CSV columns, data types)
- **Missing data handling** strategy

---

### 3. Output Specifications Per Step

**CRITICAL - Folder Destinations:**
- **ALL analysis outputs** (CSV, TXT, etc.) go to `data/` folder
- **Execution logs** (.log files only) go to `logs/` folder
- **Plot source CSVs** go to `data/` (not plots/) with prefix `step##_*_plot_data.csv`
- `plots/` stays EMPTY until rq_plots runs (generates PNG/PDF there)
- `results/` stays EMPTY until rq_results runs (generates summary.md there)

---

### 4. Expected Data Formats Per Step

Document:
- **Data transformations** with explicit steps
- **Statistical implementation details** (NEW in v4.3)
- **Random seeds** for reproducibility
- **Iteration counts** for bootstrap/resampling
- **Remedial action triggers** and responses

---

### 5. Dependencies on Other RQs (If Applicable)

**Must include:**
- **Primary and fallback file paths**
- **File discovery patterns** if exact name unknown
- **Format expectations** regardless of file name
- **Circuit breakers** if dependencies missing

---

### 6. Validation Requirements Per Step (MANDATORY)

**Structure for EVERY step:**
1. Validation requirement statement
2. 4-layer substance criteria (with exact headers)
3. Expected behavior on failure

---

## Statistical Specifications Checklist

When creating a plan, ensure ALL statistical procedures specify:

☐ **Cross-validation:** folds, seed, stratification, shuffle, gap threshold
☐ **Bootstrap:** iterations, seed, resampling unit, replacement, CI method
☐ **Power analysis:** type, effect size metric, alpha, power target, software
☐ **Multiple comparisons:** family definition, test count, method, dual reporting
☐ **Assumption checks:** tests to run, thresholds, remedial actions
☐ **Random seeds:** seed=42 for ALL randomized procedures
☐ **File paths:** primary, alternative, fallback patterns for dependencies

---

## Template Structure Summary

A well-formed 2_plan.md contains:

```markdown
# Analysis Plan: RQ X.Y.Z - [Title]

**Research Question:** X.Y.Z
**Created:** YYYY-MM-DD
**Status:** Planning complete, ready for tool specification (rq_tools)

---

## Overview

[Brief description of analysis approach, pipeline type, key methodological notes]

**Pipeline:** [e.g., Multiple Linear Regression, LMM, IRT calibration]
**Steps:** N total analysis steps (Step 0: validation + Steps 1-N: analysis)
**Estimated Runtime:** [Total estimated time]

**Key Decisions Applied:**
- Decision D068: Dual p-value reporting (uncorrected + corrected)
- [Other relevant decisions]

---

## Analysis Plan

### Step 0: Validate Cross-RQ Dependencies
[ALWAYS include Step 0 for dependency/prerequisite validation]

### Step 1: [First Main Analysis Step]
[Continue with numbered steps...]

---

## Expected Outputs

### Data Files (ALL analysis inputs and outputs)
[List all CSV, TXT files in data/ folder]

### Logs (ONLY execution logs)
[List all .log files in logs/ folder]

### Plots (EMPTY until rq_plots runs)
[Note which plot source CSVs created in data/]

### Results (EMPTY until rq_results runs)
[Note that summary.md created by rq_results]

---

## Expected Data Formats

### Step-to-Step Transformations
[Document how data flows between steps]

### Column Naming Conventions
[Document standardized column names]

### Data Type Constraints
[Document nullable vs non-nullable, ranges]

---

## Cross-RQ Dependencies

[Document any dependencies on other RQ outputs]

---

## Validation Requirements

**CRITICAL MANDATE:**
Every analysis step in this plan MUST use validation tools after analysis tool execution.

### Validation Requirements By Step

#### Step 0: Validate Dependencies
[Full 4-layer validation structure]

#### Step 1: [Analysis Step]
[Full 4-layer validation structure]

[Continue for ALL steps]

---

## Summary

**Total Steps:** N
**Estimated Runtime:** [Time]
**Cross-RQ Dependencies:** [List or "None"]
**Primary Outputs:** [Key deliverables]
**Validation Coverage:** 100% (all N steps have 4-layer validation requirements)

**Key Hypothesis:** [Main hypothesis being tested]

**Critical Methodological Notes:**
[Important statistical considerations, limitations acknowledged]

---

**Next Steps (Workflow):**
1. User reviews and approves this plan
2. rq_tools reads this plan -> creates 3_tools.yaml
3. rq_analysis reads plan + tools -> creates 4_analysis.yaml
4. g_code reads analysis -> generates executable code

---

**Version History:**
- v1.0 (YYYY-MM-DD): Initial plan created by rq_planner agent
```

---

## Version History

- **v4.3** (2026-01-02): Enhanced statistical specifications
  - Added detailed requirements for CV, bootstrap, power, corrections
  - Mandated random seeds for reproducibility
  - Required remedial actions for assumption violations
  - Improved cross-RQ dependency handling with fallback paths
  - Emphasized 4-layer validation structure with exact headers
  
- **v4.2** (2025-12-02): Previous version
  - Comprehensive structure (500-700 lines)
  - Generic examples (no v3.0-specific content)
  - Extensive validation documentation

---

**End of Template Specification**