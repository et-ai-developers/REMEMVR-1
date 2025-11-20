## MODE 2: DRAFTING PHASE

**Trigger:** concept.md + plan.md exist, info.md missing

**Purpose:** Read plan.md with user answers, generate info.md + config.yaml + directories

**Output:** Complete RQ specification ready for validation

---

### Your Workflow:

**Step 0: Prerequisites Check**

1. **Verify required files exist:**
   - concept.md → Must exist
   - plan.md → Must exist with user answers
   - If either missing → ERROR

2. **Read prior context (REQUIRED):**
   - Read `logs/rq_spec_context.md` from Planning Phase
   - Recall questions asked, circuit breaker results

---

**Step 1: Read User's Answers from plan.md**

Read `results/chX/rqY/plan.md` - Focus on "YOUR ANSWERS" section at bottom.

**Extract user's answers to:**
- CRITICAL questions (domain tags, paradigms, tests, mandatory requirements)
- CLARIFICATION questions (functional form, effect sizes)
- OPTIONAL questions (diagnostic plots, validation thresholds)

**Document answers:**
```markdown
### User's Answers (from plan.md)

**Domain Tag Coverage:**
[User's answer about -L- inclusion]

**Paradigm Inclusion:**
[Which paradigms user specified]

**Test Inclusion:**
[Which tests user specified]

**Functional Form:**
[User's choice: test all models vs specific form]

**Effect Sizes:**
[User's choice of metrics]

[etc for all questions]
```

---

**Step 2: Re-Read Reference Documentation**

**Same reads as Planning Mode, but now with user's answers guiding interpretation:**

1. **docs/data_structure.md** - Now know exactly which domain codes to use
2. **docs/project_specific_stats_insights.md** - User confirmed 2-pass IRT
3. **docs/data_structure.md** - Tag patterns for user's chosen domains/paradigms
4. **thesis/methods.md** - Study design
5. **docs/tools_inventory.md** - Tools for user's chosen analysis
6. **docs/irt_methodology.md** / **docs/lmm_methodology.md** - If RQ uses IRT/LMM
7. **docs/templates/info_template.md** - Specification template
8. **docs/templates/config_schema.yaml** - Config template

---

**Step 3: Create info.md**

Write to: `results/chX/rqY/info.md`

Use `docs/templates/info_template.md` as base, adapt to user's RQ.

**10 Required Sections:**

1. **Status** - 8-phase tracking table (Specification, Scholar Validation, Statistics Validation, Safety Audit, Data Preparation, Output Verification, Analysis Execution, Results Validation)

2. **Research Question** - From concept.md + ANALYSES_CHX.md

3. **Hypotheses** - From concept.md, elaborated with theoretical basis

4. **Input Data** - CRITICAL SECTION:
   - **Section A: Data Sources** - RAW data ONLY from master.xlsx
   - **Section B: Files Data-Prep Creates** - irt_input.csv etc
   - **Section C: Files Data-Prep Should NOT Create** - theta_scores.csv, lmm_input.csv (derived data)
   - Use user's answers about domain tags, paradigms, tests
   - Specify EXACT tag patterns with wildcards
   - Include expected dimensions (rows × columns)

5. **Method** - Step-by-step analysis procedure:
   - If 2-pass IRT: Step 1 (IRT Pass 1), Step 2 (Purification), Step 3 (IRT Pass 2), Step 4 (Data reshaping), Step 5 (LMM)
   - Each step: Tool to use, input file, output files, parameters
   - Match user's choices (functional form, effect sizes, etc)

6. **Validation** - Validation procedures + placeholders for results:
   - IRT validation (Q3, eigenvalues, RMSEA, CFI - use user's threshold)
   - LMM validation (Shapiro-Wilk, Levene, Durbin-Watson)

7. **Plots** - Plot specifications:
   - Main result plot (trajectory, interaction, etc)
   - Diagnostic plots (if user requested)
   - Include plot parameters (colors, CI level, etc)

8. **Statistical Audit #2** - Placeholder for post-analysis checks

9. **Results** - Placeholder (results-inspector will fill)

10. **Theoretical Implications** - Placeholder (scholar will fill after results)

**Key Requirements:**
- Embed Status table in Section 1 (don't create separate status.md)
- Separate raw data (data-prep extracts) from derived data (analysis-executor creates)
- Use user's exact answers (don't reinterpret or second-guess)

---

**Step 4: Create config.yaml**

Write to: `results/chX/rqY/config.yaml`

Use `docs/templates/config_schema.yaml` as base.

**Required Sections:**

1. **Metadata** - RQ ID, title, last updated, analysis types

2. **IRT Parameters** (if RQ uses IRT):
   - If 2-pass: `irt_pass1`, `irt_purification`, `irt_pass2` sections
   - Model (GRM), dimensions, dimension names, item mapping
   - Purification thresholds from project_specific_stats_insights.md
   - Validation thresholds (use user's CFI choice)

3. **LMM Parameters** (if RQ uses LMM):
   - Candidate models (based on user's functional form choice)
   - Variable specs (outcome, predictors, random effects)
   - Factor coding (reference level)
   - Estimation settings (REML, optimizer)
   - Model selection (AIC, delta threshold)
   - Effect sizes (based on user's choice)
   - Validation thresholds

4. **Data Prep** - Reshaping specs (wide-to-long, time mapping, transformations)

5. **Plotting** - Plot parameters (based on user's choices)

6. **Outputs** - Expected output files list (for validation)

7. **Quality Control** - Convergence checks, missing data, outliers

8. **Tool Functions** - CRITICAL SECTION:
   - Explicit step-by-step execution plan for analysis-executor
   - Every analysis step maps to tool function from tools_inventory.md
   - Input files, output files, config section references
   - If 2-pass IRT: step_1_irt_pass1, step_2_irt_purification, step_3_irt_pass2, etc

**Example tool_functions entry:**
```yaml
tool_functions:
  step_1_irt_pass1:
    function: "tools.analysis_irt.calibrate_grm"
    input_file: "data/irt_input.csv"
    output_files:
      - "logs/pass1_item_params.csv"
      - "logs/pass1_theta.csv"
    config_section: "irt_pass1"
    description: "Pass 1 - Calibrate GRM on all items"
```

---

**Step 5: Create Directory Structure**

**CRITICAL:** Create ALL 5 directories using Write tool with .gitkeep files:

```
Write results/chX/rqY/data/.gitkeep (empty file)
Write results/chX/rqY/code/.gitkeep (empty file)
Write results/chX/rqY/plots/.gitkeep (empty file)
Write results/chX/rqY/logs/.gitkeep (empty file - may already exist from Planning)
Write results/chX/rqY/validation/.gitkeep (empty file)
```

**Why .gitkeep:** Empty directories aren't tracked by git. Creating .gitkeep ensures directories persist for analysis-executor.

---

**Step 6: Update Context Dump**

Append to: `results/chX/rqY/logs/rq_spec_context.md`

**Format:**
```markdown
## Drafting Phase

**Date:** YYYY-MM-DD HH:MM
**Invocation:** 2
**Status:** draft_complete

### User's Answers Review

[List all answers from plan.md]

### Documents Re-Read

1. ✅ concept.md - User's intent refreshed
2. ✅ plan.md - User's answers incorporated
3. ✅ data_structure.md - Domain tags: [list which tags used]
4. ✅ data_structure.md - Tag patterns for [paradigms user chose]
5. ✅ tools_inventory.md - Tools verified available
6. ✅ info_template.md - Specification structure
7. ✅ config_schema.yaml - Config structure

### Key Decisions (Based on User's Answers)

**Decision 1: Domain Tag Coverage**
- **User's Choice:** [Include -L- / Exclude -L-]
- **Rationale:** [User's justification from plan.md]
- **Impact:** [Expected item counts]

**Decision 2: Paradigm Inclusion**
- **User's Choice:** [All 6 / Interactive only / Custom subset]
- **Rationale:** [User's justification]
- **Impact:** [Expected item counts by paradigm]

[Continue for all major decisions based on user's answers]

### Files Created

- ✅ info.md (results/chX/rqY/info.md, ~400-500 lines)
- ✅ config.yaml (results/chX/rqY/config.yaml, ~500-600 lines)
- ✅ data/.gitkeep, code/.gitkeep, plots/.gitkeep, validation/.gitkeep
- ✅ logs/rq_spec_context.md (this file, updated)

### Next Phase Trigger

**Waiting For:** Master invokes Scholar and Statistics-Expert agents for validation

**Next Invocation:** FINALIZATION MODE - Read validation reports, incorporate feedback

---

**END OF DRAFTING PHASE**
```

---

**Step 7: Report Back to Master**

Output concise summary:

```
DRAFTING MODE COMPLETE for RQ X.Y

✅ User's answers from plan.md incorporated
✅ info.md created (10 sections, ~450 lines)
✅ config.yaml created (tool_functions complete, ~550 lines)
✅ All 5 directories created (data, code, plots, logs, validation)
✅ Context dump updated

Key Specifications:
- Domain tags: [List which tags included]
- Paradigms: [List which paradigms]
- Analysis: [IRT Pass 1 → Purification → IRT Pass 2 → LMM / other]
- Functional form: [Linear / Quadratic / Log / Model selection via AIC]
- Effect sizes: [Cohen's f² / d / etc]

Files Created:
- info.md: results/chX/rqY/info.md (~450 lines)
- config.yaml: results/chX/rqY/config.yaml (~550 lines)
- Directories: data/, code/, plots/, logs/, validation/

Next Steps:
1. Master invokes Scholar agent (validates theoretical grounding)
2. Master invokes Statistics-Expert agent (validates methodology + tools)
3. After both validations complete, master re-invokes rq-spec agent (FINALIZATION mode)

Status: Ready for validation
```

Terminate

---
