# Chapter 7 RQ Execution Protocol

**Purpose:** Context window primer for executing any Ch7 RQ after /refresh
**Usage:** `read ch7/execute.md` then proceed with specified RQ

---

## EXECUTION FLOW

```
1. READ: docs/1_concept.md → docs/2_plan.md → docs/4_analysis.yaml (understand pipeline)
   NOTE: Specification files are in results/ch7/X.Y.Z/docs/ NOT the RQ root folder
2. TODOWRITE: Create step-by-step task list from 4_analysis.yaml
3. LOOP per step:
   a. Tell g_code to read ch7/gcode_lessons.md FIRST (contains all known bugs/fixes)
   b. g_code generates stepXX_*.py (informed by lessons learned)
   c. Run code, debug until output is statistically valid
   d. If new bug found: ADD TO gcode_lessons.md immediately
   e. Validate output makes theoretical sense
   f. Mark step complete, proceed to next
4. POST-EXECUTION: rq_inspect → rq_plots → rq_results → rq_validate
   ⚠️ CRITICAL: Run SEQUENTIALLY, not in parallel (rq_validate needs summary.md from rq_results)
5. UPDATE STATUS: Update ch7/rq_status.tsv with completion status
   ⚠️ MANDATORY: Do this IMMEDIATELY after validation completes, before reporting to user
6. ADD LESSONS: 
   - Add execution insights to "LESSONS LEARNED LOG" section below
   - Add g_code bugs/fixes to ch7/gcode_lessons.md
7. REPORT: Summary + thesis implications to user
```

**⚠️ MANDATORY END-OF-RQ UPDATES (DO NOT SKIP):**
- [ ] `ch7/rq_status.tsv` - Mark all validation columns TRUE, update Notes with key finding
      **This is the SINGLE SOURCE OF TRUTH for chapter progress. Update IMMEDIATELY after RQ completion.**
- [ ] `ch7/execute.md` - Add lessons learned (format: `[Date] [RQ] [Lesson]`)
- [ ] `ch7/gcode_lessons.md` - Add any new g_code bugs/fixes discovered during execution

---

## G_CODE LEARNING SYSTEM (NEW FOR CH7)

**Purpose:** Accumulate g_code lessons across RQs to prevent repeating bugs

### How It Works:
1. **Before each g_code invocation:** Tell g_code to read `ch7/gcode_lessons.md`
2. **After finding/fixing bugs:** Immediately update gcode_lessons.md with:
   - Bug description and symptoms
   - The fix that worked
   - Prevention strategy for future
3. **Benefits:** Each subsequent RQ benefits from all previous debugging

### Example g_code Invocation:
```
Task: g_code
Prompt: "Generate Step XX code.
CRITICAL: First read results/ch7/gcode_lessons.md for known bugs/fixes.
Then read specification from results/ch7/X.Y.Z/docs/4_analysis.yaml
[rest of prompt]"
```

### When to Update gcode_lessons.md:
- Function signature mismatches
- Column name case issues  
- Path calculation errors
- Validation logic bugs
- Data structure assumptions
- Any pattern that will recur

**The goal:** By RQ 7.8.x, g_code should produce nearly bug-free code on first attempt.

---

## TASK 1: UNDERSTAND THE OBJECTIVE

Before coding, answer these questions from 1_concept.md:
- What is the primary hypothesis?
- What would SUPPORT vs REFUTE the hypothesis look like?
- Expected effect sizes/directions?
- Sample size and structure (N × tests × conditions)?

**Sensible results checklist:**
- [ ] Effect directions match theoretical predictions (or explain divergence)
- [ ] Effect sizes are plausible (not |d| > 3.0, not r = 0.99)
- [ ] p-values align with effect magnitudes
- [ ] No impossible values (proportions outside [0,1], negative variances)
- [ ] Trajectories show expected patterns (decline, not random)

---

## CRITICAL LESSONS FROM CH5 & CH6

### IRT Settings (CRITICAL - 100× speed difference)
```python
# CORRECT:
model_fit.mc_samples = 1      # Point estimates for fitting (FAST)
model_scores.mc_samples = 100  # Monte Carlo for theta scores (ACCURATE)

# WRONG: mc_samples=100 for fitting → hours instead of minutes
```

### IRT Background Process Management (CRITICAL - context window)
```
# CORRECT: Run IRT as background process, wait for completion
1. Launch: poetry run python -u stepXX_*.py (as background process)
   → MUST use -u flag (unbuffered output) to see progress in log file
2. WAIT: Do NOT poll epoch status repeatedly
3. Check ONCE when process finishes (exit code 0)

# WRONG: Repeatedly checking BashOutput for epoch status
# → Blows up context window with thousands of epoch lines
# → Model will converge on its own; no intervention needed

# WRONG: Running without -u flag
# → Log file stays empty until process finishes (Python buffers stdout)

# REQUIRED: log() function must flush
def log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(f"{msg}\n")
        f.flush()  # ← CRITICAL
    print(msg, flush=True)  # ← CRITICAL
```

### LMM Coefficient Extraction (CRITICAL)
```python
# CORRECT: Extract fixed effects ONLY
n_fe = len(model.model.exog_names)
fixed_params = model.params[:n_fe]
fixed_pvalues = model.pvalues[:n_fe]

# WRONG: model.params includes random effects → wrong slice
```

### CSV Not Pickle for LMM Results
```python
# CORRECT: Export coefficients to CSV immediately
coef_df.to_csv('results/stepXX_lmm_coefficients.csv')

# WRONG: pickle.dump(model, ...) → patsy eval_env errors on reload
```

### UID Format Consistency
```python
# CORRECT: String UIDs throughout
df['UID'] = df['UID'].astype(str)  # "A010", "B023"

# WRONG: .astype(int) → fails on non-numeric prefixes
```

### Column Name Case Sensitivity
```python
# CORRECT: Uppercase for tool compatibility
df.columns = ['UID', 'TEST', 'TSVR', ...]

# WRONG: lowercase 'test' → tool lookup failures
```

---

## CH7-SPECIFIC CRITICAL SETTINGS

### Data Source (CRITICAL - Ch7 uses preprocessed CSVs)
```python
# CORRECT: Ch7 uses preprocessed participant data
df_participants = pd.read_csv('data/dfnonvr.csv')  # 101 columns, includes NART in column 2
df_tests = pd.read_csv('data/dfdata.csv')  # Test-level data (4 tests per participant)

# WRONG: Trying to extract from master.xlsx (Ch7 data is already prepared)
# WRONG: Looking for NART in column 34 (it's in column 2 after recreation)
```

### Cognitive Test Data Availability
```python
# All available in dfnonvr.csv:
# - NART Score: Column 2 (values 6-50, mean 31.9)
# - RAVLT scores: Columns with RAVLT prefix
# - BVMT scores: Columns with BVMT prefix
# - RPM scores: Columns with Raven/RPM prefix
# - STR (strategy questionnaire): Column 100
# - DASS scores: Columns with DASS prefix
# - Demographics: Age, Education, Gender columns
```

### Path Hierarchies (CRITICAL - Must use full paths)
```python
# CORRECT: Hierarchical paths for Ch7
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch7/7.X.Y
LOG_FILE = RQ_DIR / "logs" / "stepXX_*.log"
df.to_csv(RQ_DIR / "data" / "output.csv")
model_path = RQ_DIR / "results" / "step05_model.pkl"

# WRONG: Flat paths that were fixed in 4_analysis.yaml
# data/output.csv → results/ch7/7.X.Y/data/output.csv
# logs/step01.log → results/ch7/7.X.Y/logs/step01.log
```

### Cross-RQ Dependencies (Ch7 specific)
```python
# CORRECT: Load Ch5 models for comparison (many Ch7 RQs depend on Ch5)
ch5_model = pd.read_csv('results/ch5/5.2.1/results/step06_final_coefficients.csv')

# WRONG: Using .txt extension for model files (should be .pkl or .csv)
# WRONG: Using incorrect Ch5 RQ reference (e.g., 5.1.1 instead of 5.2.1)
```

### Module Path Corrections (CRITICAL - rq_analysis v5.1.0 issues)
```python
# CORRECT module paths (verified to exist):
from tools.data import load_participant_data, load_test_data
from tools.analysis_stats import extract_random_effects_from_lmm
from tools.validation import validate_data_columns

# WRONG (commonly generated incorrectly):
from tools.data_extraction import ...  # Module doesn't exist
from tools.analysis_extensions import validate_regression_assumptions  # Wrong module
```

---

## COMMON MISTAKES TO AVOID

### 1. Wrong Data Source
- **Ch7 NEVER uses master.xlsx** - All data is in dfnonvr.csv and dfdata.csv
- Column names are exact (case-sensitive)
- NART is in column 2, not column 34
- STR questionnaire is in column 100

### 2. Validator-Model Mismatches
- Use `validate_lmm_convergence` ONLY for LMM/GLMM models
- Use `validate_regression_assumptions` for regular regression
- Use `validate_clustering_quality` for clustering analyses
- Check actual model type before applying validators

### 3. File Format Errors
- Models: Always .pkl (not .txt)
- Data: Always .csv
- Coefficients: Export to CSV, not pickle
- Check file extensions match usage

### 4. Module Reference Errors
- `tools.data` NOT `tools.data_extraction`
- `tools.validation` for most validators
- `tools.analysis_extensions` for specialized validators
- Verify module exists before using

### 5. Path Hierarchy Issues
- ALWAYS use hierarchical paths: `results/ch7/7.X.Y/...`
- NEVER use flat paths: `data/`, `logs/`, `results/`
- Use RQ_DIR for dynamic resolution

---

## CODE-COPYING STRATEGY (75% Time Savings)

**When to use:** After first successful ROOT RQ in a chapter series (e.g., 7.1.1 → 7.1.2 → 7.1.3 → 7.1.4)

**Success rate:** Proven in Ch6 (3/3 applications)
**Time savings:** 45 min vs 4-5 hours with g_code (75-80% reduction)
**Bug rate:** 1-2 predictable bugs vs 5-6 systematic bugs per step

### Procedure:

```bash
# 1. Copy all code files from working source RQ
cp -r results/ch7/SOURCE_RQ/code/* results/ch7/TARGET_RQ/code/

# 2. Update RQ ID references (CRITICAL - prevents overwriting source RQ!)
cd results/ch7/TARGET_RQ/code
sed -i 's/SOURCE_ID/TARGET_ID/g' *.py  # e.g., 7.1.1 → 7.1.2
sed -i 's/ch7\/SOURCE_ID/ch7\/TARGET_ID/g' *.py

# 3. Update data source references if different
# Check if different columns or subsets needed

# 4. Fix module references based on 4_analysis.yaml
# Update any tools.data_extraction → tools.data
# Fix validator module paths

# 5. Run all steps sequentially, fix path bugs as they arise
```

### ⚠️ CRITICAL PATH VERIFICATION (MANDATORY)

**BEFORE running ANY copied code, verify these paths:**

```python
# ✅ CORRECT: Dynamic path resolution
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch7/TARGET_RQ
LOG_FILE = RQ_DIR / "logs" / "stepXX_*.log"
df = pd.read_csv(RQ_DIR / "data" / "input.csv")
df.to_csv(RQ_DIR / "data" / "output.csv")

# ❌ WRONG: Hardcoded source RQ paths
LOG_FILE = Path("/path/to/7.1.1/logs/stepXX.log")  # ← DANGER!
df = pd.read_csv("results/ch7/7.1.1/data/input.csv")  # ← Reads wrong RQ!
df.to_csv("../7.1.1/data/output.csv")  # ← Overwrites source RQ!
```

**Verification checklist (run BEFORE executing):**
```bash
# 1. Grep for source RQ ID in ALL files
grep -r "SOURCE_ID" results/ch7/TARGET_RQ/code/
# → Should return ZERO matches

# 2. Grep for hardcoded absolute paths
grep -r "/results/ch7/" results/ch7/TARGET_RQ/code/
# → Should return ZERO matches (except comments)

# 3. Check RQ_DIR is correctly defined
grep -n "RQ_DIR = " results/ch7/TARGET_RQ/code/*.py
# → Should use parents[1] or resolve() to target RQ

# 4. Verify log file paths
grep -n "LOG_FILE = " results/ch7/TARGET_RQ/code/*.py
# → Should use RQ_DIR / "logs" / ...

# 5. Check all read_csv/to_csv calls
grep -n "read_csv\|to_csv" results/ch7/TARGET_RQ/code/*.py
# → Should use RQ_DIR / "data" / ... or correct data source files
```

---

## STEP EXECUTION TEMPLATE

For each step in 4_analysis.yaml:

```
1. READ step specification (inputs, outputs, validation)
2. CHOOSE strategy:
   a. CODE-COPY: If working template exists (verify paths first!)
   b. G_CODE: If first RQ or new analysis type
3. RUN: poetry run python results/ch7/X.Y.Z/code/stepXX_*.py
4. VALIDATE output:
   - File exists at expected path?
   - Row/column counts match specification?
   - Values in expected ranges?
   - No NaN/Inf where unexpected?
5. THEORETICAL CHECK:
   - Does direction match hypothesis?
   - Are magnitudes plausible?
   - Any anomalies to flag?
6. DEBUG if needed (iterate until valid)
7. MARK step complete in TodoWrite
```

---

## VALIDATION AGENTS (Post-Execution)

**rq_inspect:** Validates all outputs exist and meet schema
**rq_plots:** Creates publication-quality visualizations (run plots.py BEFORE this agent)
**rq_results:** Generates summary.md with anomaly detection
**rq_validate:** Thesis-quality checklist validation (REQUIRES summary.md to exist)

### ⚠️ CRITICAL: Sequential Execution Required

```
# CORRECT: Run validation agents SEQUENTIALLY
1. rq_inspect (can run in background)
2. Generate plots: PYTHONPATH=/home/etai/projects/REMEMVR poetry run python plots/plots.py
3. rq_results (wait for completion - creates summary.md)
4. rq_validate (MUST run AFTER rq_results - reads summary.md)

# WRONG: Running all 4 agents in parallel
# → rq_validate will fail with "summary.md missing" because rq_results hasn't finished
```

**Why sequential matters:**
- rq_validate reads `results/summary.md` to check scientific plausibility
- rq_results creates `results/summary.md` (can take 1-2 minutes)
- If rq_validate starts before rq_results finishes → CIRCUIT BREAKER triggers

Run in sequence. Don't skip. Each catches different issues.

---

## THESIS CONTEXT

**Chapter 7 Theme:** Individual differences and cognitive predictors
**Key Questions:**
- Do cognitive abilities predict memory performance? (crystallized vs fluid)
- Does strategy use predict forgetting trajectories? (elaboration, organization)
- Are there distinct memory phenotypes? (clustering, profiles)
- Do demographics matter? (age, education, gender effects)

**Connect results to:**
- Ch5 memory findings (baseline comparisons)
- Ch6 confidence findings (metacognitive differences)
- Theoretical frameworks in 1_concept.md
- Clinical implications for personalized assessment

---

## LESSONS LEARNED LOG (Terse Format - Updated Session-by-Session)

**Purpose:** Capture critical insights discovered during Ch7 execution for cross-RQ learning. Add new lessons in terse format immediately after discovery. Format: `[Date] [RQ] [Lesson]`

### Data Source Lessons

**[2026-01-05] [7.1.x] Master.xlsx Reference Error:**
- Ch7 should NEVER reference master.xlsx - all data is preprocessed
- dfnonvr.csv has participant data (101 columns after fix)
- dfdata.csv has test-level data (4 tests per participant)
- 610 incorrect references fixed across 78 files
- rq_analysis v5.3.0 now enforces Ch7 data source rules

**[2026-01-05] [7.1.x] NART Data Recovery:**
- NART was missing from dfnonvr.csv despite documentation claiming it was there
- Root cause: column_mapping.py excluded NART during extraction
- Fixed by recreating dfnonvr.csv with all data
- NART now in column 2 (was incorrectly documented as column 34)
- Lesson: ALWAYS verify actual file contents vs documentation

### Path and Module Lessons

**[2026-01-05] [7.1.x] Hierarchical Path Requirements:**
- All Ch7 RQs MUST use hierarchical paths: results/ch7/7.X.Y/...
- Never use flat paths: data/, logs/, results/
- Fixed 25+ path issues across 7.1.x analysis files
- Use RQ_DIR = Path(__file__).resolve().parents[1] for dynamic resolution

**[2026-01-05] [7.1.x] Module Reference Corrections:**
- tools.data NOT tools.data_extraction (module doesn't exist)
- tools.validation for most validators
- tools.analysis_extensions for specialized validators only
- validate_regression_assumptions in tools.validation, not analysis_extensions
- Always verify module exists before using

### rq_analysis Agent Lessons

**[2026-01-04] [7.1.x] rq_analysis v5.1.0 Deep Verification:**
- Original v4.1.0 was translation agent, not verification agent
- Propagated errors from upstream (wrong paths, modules, validators)
- v5.1.0 adds deep verification: module checks, path correction, format validation
- Must verify actual Python functions exist, not just trust documentation
- Testing on 7.1.1-7.1.3 revealed systematic issues requiring manual fixes

**[2026-01-05] [All Ch7] Tool Name Mismatch Resolution:**
- rq_planner was inventing function names instead of using actual tools
- Examples: "extract_episodic_memory_data" doesn't exist
- Solution: Re-run rq_planner with explicit instruction to use tools_inventory.md
- Fixed 5 RQs that initially failed rq_tools phase
- 100% success rate after re-planning with actual tool names

### File Format and Validation Lessons

**[2026-01-04] [7.1.x] File Format Requirements:**
- Models: Always .pkl format (not .txt)
- Data: Always .csv format
- Coefficients: Export to CSV, not pickle (avoids patsy eval_env errors)
- Ch5 dependencies: Reference correct RQ (5.2.x not 5.1.1 for many analyses)

**[2026-01-04] [7.1.x] Validator-Model Type Matching:**
- validate_lmm_convergence: ONLY for LMM/GLMM models
- validate_regression_assumptions: For regular regression
- validate_clustering_quality: For clustering analyses
- Using wrong validator causes immediate failure
- Check actual model type before applying validators

---

## QUICK REFERENCE

| Analysis Type | Data Source | Key Validation |
|--------------|-------------|----------------|
| Cognitive Predictors | dfnonvr.csv cols | NART col 2, RAVLT/BVMT/RPM cols |
| Strategy Analysis | dfnonvr.csv col 100 | STR questionnaire data |
| Demographics | dfnonvr.csv | Age, Education, Gender cols |
| Cross-Ch5 Comparison | Ch5 results CSVs | Use 5.2.x not 5.1.1 |
| LMM with Predictors | dfdata.csv + dfnonvr.csv | Merge on UID |
| Clustering | Random effects CSVs | Min cluster N >= 10 |

**Critical Data Columns:**
- NART Score: Column 2 (6-50 range)
- STR Questionnaire: Column 100
- Demographics: Check DATA_DICTIONARY.md for exact columns
- Cognitive scores: RAVLT_, BVMT_, RPM_ prefixes

**Decision Compliance:**
- D039: 2-pass IRT purification (if using IRT)
- D068: Dual p-values (parametric + bootstrap/permutation)
- D069: Dual-scale trajectory plots (if applicable)
- D070: TSVR time variable (hours, not days)

---

**Ready to execute. Specify RQ number.**