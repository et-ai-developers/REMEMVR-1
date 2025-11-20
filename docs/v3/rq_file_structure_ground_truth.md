# RQ File Structure - Absolute Ground Truth

**Version:** 2.0
**Last Updated:** 2025-11-12
**Status:** AUTHORITATIVE (all agents must follow this exactly)
**Supersedes:** results_schema.md (v1.0 - outdated)

---

## Purpose

This document defines the **absolute ground truth** file and folder structure for every RQ in the REMEMVR PhD thesis. This structure is mandatory and unchangeable. All agents must:
1. **Scan** RQ structure on every invocation
2. **Validate** files are in correct locations
3. **Fix** misplaced files automatically
4. **Report** missing required files
5. **Follow** strict naming conventions

---

## Directory Structure Overview

```
results/
├── ch5/                          # Chapter 5: Trajectory of Episodic Forgetting
│   ├── rq1/                      # RQ 5.1
│   ├── rq2/                      # RQ 5.2
│   ├── ...
│   └── rq15/                     # RQ 5.15
├── ch6/                          # Chapter 6: Metacognition in Episodic Memory
│   ├── rq1/                      # RQ 6.1
│   ├── ...
│   └── rq15/                     # RQ 6.15
└── ch7/                          # Chapter 7: Individual Differences
    ├── rq1/                      # RQ 7.1
    ├── ...
    └── rq20/                     # RQ 7.20
```

**Total:** 50 RQs (15 + 15 + 20)

---

## RQ Folder Structure (Mandatory)

Every RQ directory (`results/chX/rqY/`) MUST have this structure:

```
rqY/
├── info.md                       # [REQUIRED] RQ specification (11 sections)
├── config.yaml                   # [REQUIRED] IRT/LMM parameters
├── status.md                   # [REQUIRED] Execution status tracker
├── validation/                   # [REQUIRED] Validation reports
│   ├── scholar_report.md       # [REQUIRED after Step 2]
│   └── statistics_report.md    # [REQUIRED after Step 3]
├── logs/                         # [REQUIRED] Agent execution logs
│   ├── rq_spec_context.md        # [REQUIRED] RQ-spec agent context dump (stateful)
│   ├── rq_specification_report.md  # [REQUIRED after Step 4]
│   ├── data_prep_report.md     # [REQUIRED after Step 6]
│   ├── analysis_executor_report.md # [REQUIRED after Step 8]
│   └── results_inspector_report.md # [REQUIRED after Step 9]
├── data/                         # [REQUIRED] All CSV files + companion .md
│   ├── {filename}.csv            # Data file
│   ├── {filename}.md             # [REQUIRED] Companion documentation
│   └── ...
├── code/                         # [REQUIRED] Agent-generated scripts
│   ├── data_prep_script.py       # [REQUIRED] Created by data-prep agent
│   ├── analysis_script.py        # [REQUIRED] Created by analysis-executor agent
│   └── data_prep_script.log      # [OPTIONAL] Execution logs from scripts
└── plots/                        # [REQUIRED] Visualizations + plot data
    ├── {plotname}.png            # Plot image
    ├── {plotname}_data.csv       # [REQUIRED] Data for plot regeneration
    └── ...
```

---

## Phase-by-Phase Structure Evolution

### After Step 1: Specification (Draft)

**Agent:** rq_specification (draft phase)
**Creates:**
```
rqY/
├── info.md                       # Draft with all 11 sections
├── config.yaml                   # IRT/LMM parameters
├── status.md                   # {"specification": "in_progress", ...}
├── validation/                   # Empty directory
├── logs/
│   └── rq_spec_context.md        # Agent's reasoning + decisions (first dump)
├── data/                         # Empty directory
├── code/                         # Empty directory
└── plots/                        # Empty directory
```

**Required Files:** 3 (info.md, config.yaml, status.md)
**Required Directories:** 5 (validation/, logs/, data/, code/, plots/)
**Agent Context Dump:** `logs/rq_spec_context.md` (captures draft phase reasoning)

---

### After Step 2: Scholar Validation

**Agent:** scholar
**Creates:**
```
rqY/
├── validation/
│   └── scholar_report.md       # NEW: Score (0-10) + feedback
└── status.md                   # Updated: {"validation_scholar": "passed/failed"}
```

**Required Files:** +1 (scholar_report.md)
**No changes to:** info.md, config.yaml, logs/rq_spec_context.md

---

### After Step 3: Statistics Expert Validation

**Agent:** statistics_expert
**Creates:**
```
rqY/
├── validation/
│   └── statistics_report.md    # NEW: Score (0-10) + feedback
└── status.md                   # Updated: {"validation_statistics": "passed/failed"}
```

**Required Files:** +1 (statistics_report.md)
**Side Effect:** Updates `docs/tools_inventory.md` with RQ-tool mapping

---

### After Step 4: Specification (Finalization)

**Agent:** rq_specification (finalization phase)
**Updates:**
```
rqY/
├── info.md                       # Updated: Incorporates scholar/stats feedback
├── logs/
│   ├── rq_spec_context.md        # Updated: Appends finalization reasoning
│   └── rq_specification_report.md  # NEW: Documents changes made
└── status.md                   # Updated: {"specification": "complete"}
```

**Required Files:** +1 (rq_specification_report.md in logs/)
**Agent Context Dump:** `logs/rq_spec_context.md` (appends finalization phase)

**CRITICAL:** Agent reads its own prior context dump + scholar/stats reports before making changes

---

### After Step 5: Safety Audit

**Phase:** Master validates info.md (automatic)
**No Files Created:** This is validation only
**Master generates:** Audit report (ephemeral, not saved) with PROCEED/BLOCK recommendation
**User approves:** Proceed to data-prep or fix info.md

---

### After Step 6: Data Preparation

**Agent:** data_prep
**Creates:**
```
rqY/
├── data/
│   ├── irt_input.csv             # RAW VR items from master.xlsx
│   ├── irt_input.md              # [REQUIRED] Companion documentation
│   ├── lmm_input.csv             # RAW data for LMM (if applicable)
│   ├── lmm_input.md              # [REQUIRED] Companion documentation
│   └── ...
├── code/
│   ├── data_prep_script.py       # Extraction script
│   └── data_prep_script.log      # Execution log (if script saves it)
├── logs/
│   └── data_prep_report.md     # Agent execution report
└── status.md                   # Updated: {"data_prep": "success/failure"}
```

**Naming Convention:**
- Input CSVs: `{analysis_type}_input.csv` (e.g., irt_input.csv, lmm_input.csv, ctt_input.csv)
- Companion docs: `{filename}.md` (e.g., irt_input.md)
- Script: ALWAYS `data_prep_script.py` (no variation)

**FORBIDDEN FILES:**
- ❌ `theta_scores.csv` (derived data - analysis-executor creates this)
- ❌ `item_parameters.csv` (derived data)
- ❌ Any file with "mock", "placeholder", "temporary" in name
- ❌ Any CSV without companion .md file

**Required Files:** Minimum 3 (1 CSV + 1 .md + data_prep_report.md)

---

### After Step 7: Output Verification

**Phase:** Master inspects data-prep outputs (forensic)
**No Files Created:** This is validation only
**Master generates:** Verification report (ephemeral) with CLEAN/CONTAMINATED status
**User confirms:** Proceed to analysis or delete contaminated files

---

### After Step 8: Analysis Execution

**Agent:** analysis_executor
**Creates:**
```
rqY/
├── data/
│   ├── theta_scores.csv          # IRT ability estimates
│   ├── theta_scores.md           # [REQUIRED] Companion documentation
│   ├── item_parameters.csv       # IRT item parameters
│   ├── item_parameters.md        # [REQUIRED] Companion documentation
│   ├── lmm_results.csv           # LMM coefficients
│   ├── lmm_results.md            # [REQUIRED] Companion documentation
│   └── ...
├── code/
│   └── analysis_script.py        # Analysis execution script
├── plots/
│   ├── irt_icc_plot.png          # Item Characteristic Curves
│   ├── irt_icc_plot_data.csv     # Data for plot regeneration
│   ├── lmm_trajectory_plot.png   # Forgetting trajectories
│   ├── lmm_trajectory_plot_data.csv
│   └── ...
├── logs/
│   └── analysis_executor_report.md  # Agent execution report
└── status.md                   # Updated: {"analysis_executor": "success/failure"}
```

**Naming Convention:**
- Output CSVs: `{analysis_type}_{output_type}.csv` (e.g., irt_theta_scores.csv, lmm_coefficients.csv)
- Companion docs: `{filename}.md`
- Script: ALWAYS `analysis_script.py` (no variation)
- Plots: `{analysis_type}_{plot_type}.png` (e.g., irt_icc_plot.png, lmm_trajectory_plot.png)
- Plot data: `{plotname}_data.csv` (exact plot name + _data suffix)

**Required Files:** Varies by RQ (minimum 3 CSVs + 3 .md + script + report + 2 plots)

---

### After Step 9: Results Validation (Future)

**Agent:** results_inspector
**Creates:**
```
rqY/
├── info.md                       # Updated: Adds interpretation section
├── logs/
│   └── results_inspector_report.md  # Validation results
└── status.md                   # Updated: {"results_inspection": "complete"}
```

**Status:** Stub only (not yet implemented)

---

## Mandatory Naming Conventions

### File Names (Strict Rules)

| **File Type** | **Naming Pattern** | **Example** | **Agent** |
|--------------|-------------------|-------------|-----------|
| RQ Specification | `info.md` | `info.md` | rq_specification |
| Configuration | `config.yaml` | `config.yaml` | rq_specification |
| Status Tracker | `status.md` | `status.md` | All agents update |
| Scholar Report | `scholar_report.md` | `scholar_report.md` | scholar |
| Statistics Report | `statistics_report.md` | `statistics_report.md` | statistics_expert |
| RQ-Spec Context | `rq_spec_context.md` | `rq_spec_context.md` | rq_specification |
| RQ-Spec Report | `rq_specification_report.md` | `rq_specification_report.md` | rq_specification |
| Data-Prep Report | `data_prep_report.md` | `data_prep_report.md` | data_prep |
| Executor Report | `analysis_executor_report.md` | `analysis_executor_report.md` | analysis_executor |
| Inspector Report | `results_inspector_report.md` | `results_inspector_report.md` | results_inspector |
| Data-Prep Script | `data_prep_script.py` | `data_prep_script.py` | data_prep |
| Analysis Script | `analysis_script.py` | `analysis_script.py` | analysis_executor |
| Input CSV | `{type}_input.csv` | `irt_input.csv` | data_prep |
| Output CSV | `{type}_{output}.csv` | `theta_scores.csv` | analysis_executor |
| Companion Doc | `{filename}.md` | `irt_input.md` | data_prep / analysis_executor |
| Plot Image | `{type}_{plot}.png` | `irt_icc_plot.png` | analysis_executor |
| Plot Data | `{plotname}_data.csv` | `irt_icc_plot_data.csv` | analysis_executor |

### Directory Names (Strict Rules)

| **Directory** | **Purpose** | **Created By** |
|--------------|------------|---------------|
| `validation/` | Scholar + statistics reports | rq_specification (Step 1 creates empty) |
| `logs/` | Agent execution reports + context dumps | rq_specification (Step 1 creates empty) |
| `data/` | All CSV files + companion .md | rq_specification (Step 1 creates empty) |
| `code/` | Agent-generated scripts | rq_specification (Step 1 creates empty) |
| `plots/` | Visualizations + plot data | rq_specification (Step 1 creates empty) |

**FORBIDDEN:**
- ❌ No subdirectories inside `data/`, `code/`, or `plots/` (flat structure only)
- ❌ No custom directory names (e.g., `diagnostics/`, `checks/`, `outputs/`)
- ❌ No files at RQ root except: info.md, config.yaml, status.md

---

## File Location Rules (Strict Enforcement)

### Root Level (`rqY/`)
**ALLOWED:**
- ✅ info.md
- ✅ config.yaml
- ✅ status.md

**FORBIDDEN:**
- ❌ Any .json files except status.md
- ❌ Any .md files except info.md
- ❌ Any .py files
- ❌ Any .csv files
- ❌ Any .png files

### logs/ Directory
**ALLOWED:**
- ✅ rq_spec_context.md (RQ-spec agent context dump)
- ✅ rq_specification_report.md
- ✅ data_prep_report.md
- ✅ analysis_executor_report.md
- ✅ results_inspector_report.md

**FORBIDDEN:**
- ❌ Any files with "agent_" prefix (old naming convention)
- ❌ Any extraction plans or temporary files
- ❌ Any .csv or .png files

### validation/ Directory
**ALLOWED:**
- ✅ scholar_report.md
- ✅ statistics_report.md

**FORBIDDEN:**
- ❌ Any files with "statistics_expert_report.json" (use statistics_report.md)
- ❌ Any input files like scholar_input.json (agents receive paths, not files)
- ❌ Any subdirectories

### data/ Directory
**ALLOWED:**
- ✅ Any .csv file created by data-prep or analysis-executor agents
- ✅ Corresponding .md companion file for EVERY .csv

**FORBIDDEN:**
- ❌ Any .csv without companion .md file
- ❌ Any .json files (use logs/ directory)
- ❌ Any summary files not in .md or .csv format

### code/ Directory
**ALLOWED:**
- ✅ data_prep_script.py
- ✅ analysis_script.py
- ✅ .log files from script execution (optional)

**FORBIDDEN:**
- ❌ Custom script names (prepare_irt_input.py, prepare_data.py, etc. - RENAME to data_prep_script.py)
- ❌ Any test scripts or debugging scripts
- ❌ Any .json or .csv files

### plots/ Directory
**ALLOWED:**
- ✅ Any .png file created by analysis-executor
- ✅ Corresponding _data.csv file for EVERY .png

**FORBIDDEN:**
- ❌ Any .png without corresponding _data.csv
- ❌ Any subdirectories (e.g., plot_data/)
- ❌ Any .json or .md files

---

## status.md Schema

**Required Format:**
```json
{
  "rq_id": "5.1",
  "rq_title": "Domain-specific forgetting trajectories",
  "last_updated": "2025-11-12 14:30:00",
  "specification": "complete" | "in_progress" | "not_started",
  "validation_scholar": "passed" | "failed" | "not_started",
  "validation_statistics": "passed" | "failed" | "not_started",
  "safety_audit": "proceed" | "block" | "not_started",
  "data_prep": "success" | "failure" | "not_started",
  "output_verification": "clean" | "contaminated" | "not_started",
  "analysis_executor": "success" | "failure" | "not_started",
  "results_inspection": "complete" | "not_started",
  "quality_scores": {
    "scholar": 9.5,
    "statistics": 9.3
  },
  "notes": "Any issues or decisions made during RQ building"
}
```

**Update Rules:**
- Every agent MUST update status.md after execution
- Use ISO 8601 format for timestamps
- Include quality_scores after Step 4
- Add notes for any failures or issues

---

## Companion .md File Requirements

Every CSV file in `data/` MUST have a companion .md file documenting:

**Required Sections:**
1. **Data Structure** - Column names, types, dimensions
2. **Methodology** - How data was created (extraction tags, tool functions, parameters)
3. **Quality Summary** - Missing values, outliers, validation checks
4. **Next Steps** - What analysis-executor should do with this file (if input CSV)
5. **Critical Insights** - Any important patterns or issues
6. **Example Code** - How to load and use this CSV

**Naming:** `{csv_filename}.md` (e.g., irt_input.csv → irt_input.md)

**FORBIDDEN Keywords:**
- ❌ "mock"
- ❌ "placeholder"
- ❌ "temporary"
- ❌ "fake"
- ❌ "to be replaced"
- ❌ "simulated"
- ❌ "proxy"

If any of these keywords appear, file is CONTAMINATED and must be deleted.

---

## Agent Responsibilities for File Structure

### rq_specification Agent
**On Every Invocation:**
1. Scan RQ directory structure
2. Check if `logs/rq_spec_context.md` exists:
   - YES → Read prior context + determine phase from folder structure
   - NO → This is draft phase, create all directories
3. Check if `validation/scholar_report.md` and `validation/statistics_report.md` exist:
   - BOTH EXIST → This is finalization phase, read reports + incorporate feedback
   - NEITHER EXIST → This is draft phase, create specification
4. Update `logs/rq_spec_context.md` with current reasoning
5. Validate all files in correct locations, fix if misplaced
6. Update `status.md`

**Files Created/Updated:**
- Draft phase: info.md, config.yaml, status.md, logs/rq_spec_context.md, all 5 directories
- Finalization phase: info.md (updated), logs/rq_spec_context.md (appended), logs/rq_specification_report.md

### scholar Agent
**On Every Invocation:**
1. Read info.md from RQ directory
2. Validate theoretical grounding
3. Write `validation/scholar_report.md`
4. Update `status.md`

**Files Created:** validation/scholar_report.md

### statistics_expert Agent
**On Every Invocation:**
1. Read info.md and config.yaml from RQ directory
2. Validate methodology
3. Write `validation/statistics_report.md`
4. Update `status.md`
5. Update `docs/tools_inventory.md` with RQ-tool mapping

**Files Created:** validation/statistics_report.md

### data_prep Agent
**On Every Invocation:**
1. Read info.md and config.yaml
2. Extract data from master.xlsx
3. Save CSV(s) in `data/` with companion .md files
4. Save script in `code/data_prep_script.py`
5. Write `logs/data_prep_report.md`
6. Update `status.md`
7. **NEVER create derived data** (theta_scores, item_parameters, etc.)

**Files Created:** data/*.csv, data/*.md, code/data_prep_script.py, logs/data_prep_report.md

### analysis_executor Agent
**On Every Invocation:**
1. Read info.md, config.yaml, and input CSVs from data/
2. Run IRT/LMM/CTT analysis using tools/ package ONLY
3. Save output CSV(s) in `data/` with companion .md files
4. Save plots in `plots/` with _data.csv files
5. Save script in `code/analysis_script.py`
6. Write `logs/analysis_executor_report.md`
7. Update `status.md`

**Files Created:** data/*.csv, data/*.md, plots/*.png, plots/*_data.csv, code/analysis_script.py, logs/analysis_executor_report.md

### results_inspector Agent (Future)
**On Every Invocation:**
1. Read all data/, plots/, logs/ files
2. Validate statistical correctness
3. Update info.md with interpretation
4. Write `logs/results_inspector_report.md`
5. Update `status.md`

**Files Created:** logs/results_inspector_report.md, info.md (updated)

---

## Structure Validation Checklist

Use this checklist to validate any RQ structure:

### Phase 1: Specification Complete
- [ ] info.md exists at root with all 11 sections
- [ ] config.yaml exists at root
- [ ] status.md exists at root
- [ ] validation/ directory exists (may be empty)
- [ ] logs/ directory exists with rq_spec_context.md
- [ ] data/ directory exists (empty)
- [ ] code/ directory exists (empty)
- [ ] plots/ directory exists (empty)
- [ ] NO files at root except info.md, config.yaml, status.md
- [ ] NO misplaced .json files

### Phase 2-3: Validation Complete
- [ ] validation/scholar_report.md exists
- [ ] validation/statistics_report.md exists
- [ ] status.md shows validation scores
- [ ] docs/tools_inventory.md updated with RQ-tool mapping

### Phase 4: Finalization Complete
- [ ] info.md updated with validation feedback
- [ ] logs/rq_specification_report.md exists
- [ ] logs/rq_spec_context.md updated (finalization reasoning appended)
- [ ] status.md shows specification = "complete"

### Phase 6: Data Preparation Complete
- [ ] data/ has at least 1 input CSV (e.g., irt_input.csv)
- [ ] Every CSV has companion .md file
- [ ] code/data_prep_script.py exists
- [ ] logs/data_prep_report.md exists
- [ ] status.md shows data_prep = "success"
- [ ] NO theta_scores.csv or other derived data
- [ ] NO "mock", "placeholder", "temporary" keywords in any .md

### Phase 8: Analysis Complete
- [ ] data/ has output CSVs (theta_scores.csv, item_parameters.csv, lmm_results.csv)
- [ ] Every output CSV has companion .md file
- [ ] plots/ has visualization PNGs
- [ ] Every PNG has corresponding _data.csv
- [ ] code/analysis_script.py exists
- [ ] logs/analysis_executor_report.md exists
- [ ] status.md shows analysis_executor = "success"

---

## Migration Instructions

**For Existing RQs with Incorrect Structure:**

1. **Scan** current structure
2. **Identify** misplaced files:
   - rq_specification_report.md at root → Move to logs/
   - agent_data_prep.json → Rename to data_prep_report.md
   - prepare_irt_input.py or prepare_data.py → Rename to data_prep_script.py
   - scholar_input.json or other orphaned files → DELETE
3. **Create** missing companion .md files for any bare CSVs
4. **Delete** contaminated files (any with mock/placeholder/temporary keywords)
5. **Update** status.md to current schema
6. **Commit** structure fixes with message "Fix RQ X.Y file structure per ground truth"

---

## Version History

**v2.0 (2025-11-12):**
- Defined absolute ground truth structure (mandatory for all agents)
- Added stateful rq-spec agent with context dump (logs/rq_spec_context.md)
- Added companion .md requirement for all CSVs
- Added strict naming conventions (no variation allowed)
- Added file location rules (strict enforcement)
- Added phase-by-phase evolution
- Added structure validation checklist
- Added migration instructions for existing RQs

**v1.0 (2025-01-11):**
- Original results_schema.md (outdated, inconsistent with reality)

---

**End of Ground Truth Documentation**
