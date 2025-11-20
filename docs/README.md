# REMEMVR Documentation

**Purpose:** Detailed reference guides for agents to load on-demand.

**Important:** These docs should NOT be kept in permanent context. Load only when needed for specific tasks.

---

## AVAILABLE DOCS

### 1. data_structure.md
**When to load:** When working with master.xlsx tags, understanding UID system, or extracting raw data.

**Used by:**
- Data-prep agent (always - CRITICAL for exact tag formatting)
- Any agent debugging data extraction issues
- User reviewing data structure

**Contents:**
- master.xlsx column structure
- UID format and age group mapping
- Complete tag schema (DEM, COG, RVR)
- **CRITICAL:** Exact tag formatting rules (dashes, not underscores)
- Examples of tag breakdown with correct formatting
- Data extraction workflow (NEW method using data.py directly)
- Handling different data sources:
  - Master.xlsx tags (most common)
  - Previous RQ outputs (e.g., theta estimates from IRT)
  - Computed scores (e.g., RAVLT_Total)
  - Mixed sources (combining multiple types)

---

### 2. variables_system.md ⚠️ LEGACY / DEPRECATED
**Status:** OLD METHOD - No longer used in new agent-based pipeline

**When to load:** Historical reference only OR when migrating old variables to NEW method

**Used by:**
- User reviewing legacy system
- Data-prep agent (only for migration/comparison purposes)

**Contents:**
- OLD variables.xlsx structure (Name, Label, Function, Type, Regex)
- Why this method was abandoned (480+ rows, unmaintainable, all-or-nothing)
- Migration notes for converting to NEW direct data.py interaction

**NEW METHOD (Active):**
- Data-prep agent reads RQ requirements from info.md or user instructions
- Agent calls data.py functions directly to extract needed tags
- Creates RQ-specific input.csv (not universal dfData)
- Each RQ gets only the data it needs
- Data can come from master.xlsx OR previous RQ outputs OR computed scores

---

### 3. irt_methodology.md
**When to load:** When running IRT analyses, interpreting theta scores, or validating IRT assumptions.

**Used by:**
- Analysis-executor agent (when running RQs using IRT)
- Results-inspector agent (validating IRT outputs)
- Statistics-expert agent (advising on IRT methodology)

**Contents:**
- Graded Response Model specification
- Multidimensional IRT (Q-matrix, correlated factors)
- deepirtools IWAVE parameters
- Composite_ID stacking rationale
- Iterative item filtering procedure
- Theta score interpretation
- Item parameters (difficulty, discrimination)
- IRT vs CTT comparison
- Model diagnostics and assumptions
- Output file formats

---

### 4. lmm_methodology.md
**When to load:** When running LMM trajectory analyses, comparing models, or interpreting longitudinal results.

**Used by:**
- Analysis-executor agent (when running RQs using LMM)
- Results-inspector agent (validating LMM outputs)
- Statistics-expert agent (advising on LMM methodology)

**Contents:**
- Linear Mixed Model specification
- Fixed effects (time coding, transformations)
- Random effects (intercepts, slopes)
- Model comparison (AIC, ΔAIC, Akaike weights, LRT)
- statsmodels syntax and parameters
- Extracting results (fixed effects, random effects, BLUPs, predictions)
- Assumptions and diagnostics
- Interaction effects
- Best practices and common pitfalls
- Output file formats

---

### 5. cognitive_tests.md
**When to load:** When analyzing Chapter 7 RQs involving RAVLT, BVMT, NART, RPM as predictors.

**Used by:**
- Data-prep agent (when extracting cognitive test scores)
- Analysis-executor agent (when running Chapter 7 analyses)
- Results-inspector agent (interpreting cognitive test relationships)

**Contents:**
- RAVLT (administration, scoring, interpretation)
- BVMT-R (administration, scoring, interpretation)
- NART (administration, scoring, limitations in REMEMVR)
- RPM (administration, scoring, interpretation)
- Hypothesized relationships to REMEMVR domains/paradigms
- Data extraction (tags in master.xlsx)
- Standardization procedures
- Analysis considerations (missing data, multicollinearity)

---

## USAGE GUIDELINES FOR AGENTS

### Data-Prep Agent:
**Always load:**
- data_structure.md (CRITICAL: exact tag formatting with dashes)

**Sometimes load:**
- cognitive_tests.md (if RQ involves cognitive predictors - contains exact tag names)

**NEVER load (unless for historical reference):**
- variables_system.md (LEGACY - use direct data.py interaction instead)

**CRITICAL REQUIREMENTS:**
- Tags MUST use exact spelling with DASHES throughout
- Example CORRECT: `A010-COG-X-RPM-Scor` (note: "Scor" not "Score")
- Example WRONG: `RPM_Score` or `A010_COG_X_RPM_Score`
- Verify exact tag names in data_structure.md or cognitive_tests.md
- Call data.py functions directly (NEW method)
- Data sources: master.xlsx tags, previous RQ outputs, computed scores, or mixed

### Analysis-Executor Agent:
**Load based on RQ:**
- irt_methodology.md (if RQ uses IRT)
- lmm_methodology.md (if RQ uses LMM)
- cognitive_tests.md (if Chapter 7 RQ)

**Don't load all at once** - only what's needed for current RQ.

### Results-Inspector Agent:
**Load based on analysis type:**
- irt_methodology.md (if validating IRT analysis)
- lmm_methodology.md (if validating LMM analysis)
- cognitive_tests.md (if interpreting cognitive test effects)

**Goal:** Understand methodology deeply enough to validate correctness.

### Statistics-Expert Agent:
**Load as needed for consultation:**
- irt_methodology.md (if advising on IRT approach)
- lmm_methodology.md (if advising on LMM approach)

**Goal:** Provide expert statistical advice on methodology choices.

### Debug Agent:
**Load based on error:**
- data_structure.md (if data extraction error)
- variables_system.md (if variable creation error)
- irt_methodology.md (if IRT convergence error)
- lmm_methodology.md (if LMM convergence error)

---

## MAINTENANCE

### Adding New Docs:
If you create a new reference doc (e.g., plotting_reference.md), update this README with:
- Doc name
- When to load
- Used by (which agents)
- Brief contents summary

### Updating Existing Docs:
When methodology changes or bugs are fixed, update relevant docs and change "Last Updated" date.

### User Review:
User should periodically review docs to ensure accuracy, especially after significant codebase changes.

---

## ⚠️ CRITICAL WARNINGS FOR AGENTS

### Tag Formatting (HIGHEST PRIORITY):
**Getting tags wrong will cause catastrophic bugs in data extraction.**

**CORRECT tag format:**
- Use DASHES throughout: `A010-COG-X-RPM-Scor`
- Exact spelling matters: "Scor" not "Score"
- UID format: `A{GROUP}{COUNTER}` (e.g., A053)

**WRONG tag formats:**
- ❌ Underscores: `RPM_Score` or `A010_COG_X_RPM_Score`
- ❌ Wrong spelling: `A010-COG-X-RPM-Score` (should be "Scor")
- ❌ Guessing: Always verify exact tag name in docs

**Verification sources:**
- data_structure.md (complete tag schema)
- cognitive_tests.md (cognitive test tags with exact spellings)

### Data Preparation Workflow (NEW METHOD):
**DEPRECATED (do not use):**
- ❌ Creating variables.xlsx entries
- ❌ Running data.py to generate universal dfData
- ❌ Assuming all variables come from master.xlsx

**ACTIVE (use this):**
- ✅ Data-prep agent reads RQ requirements
- ✅ Agent calls data.py functions directly to extract specific tags
- ✅ Creates RQ-specific input.csv (not universal)
- ✅ Data sources can be: master.xlsx tags, previous RQ outputs, computed scores, or mixed
- ✅ Validates data immediately after extraction
- ✅ Clear documentation of what was extracted and why

---

**End of Documentation README**
