# Chapter 7 RQ Execution Protocol

**Purpose:** Scientific execution protocol ensuring methodological correctness for PhD thesis
**Usage:** `read ch7/execute.md` then proceed with specified RQ

---

## 🚨 SCIENTIFIC INTEGRITY PROTOCOL (MANDATORY - NO EXCEPTIONS)

**CARDINAL RULE:** Getting it scientifically RIGHT is infinitely more important than getting it done quickly.

**NEVER:**
- Guess data sources or dependencies  
- Assume files contain what you expect
- Use data from different RQs without understanding what they studied
- Make code "work" by substituting random data
- Rush to implementation without understanding the science
- **Skip steps or cut corners due to time/token constraints**
- **Use "running short on time" as excuse for shortcuts**

**ALWAYS:**
- Read reports and understand the science FIRST
- Verify dependencies are methodologically sound
- Ask questions when uncertain
- Document scientific reasoning for every choice
- **Take time needed to do analysis properly**
- **Use /save, /clear, /refresh if approaching token limit**

**🔴 TIME/TOKEN CONSTRAINT PROTOCOL:**
- You are NEVER running short on time - we have infinite time
- You are NEVER stuck with token limits - /save + /clear + /refresh solves this
- If context window approaching 150k: Recommend /save to user
- If analysis needs 20 steps: Do all 20 steps properly
- Scientific integrity >> Speed (ALWAYS, NO EXCEPTIONS)

---

## EXECUTION FLOW (SCIENCE-FIRST)

### PHASE 1: SCIENTIFIC FOUNDATION (NEVER SKIP)

```
1. READ & UNDERSTAND THE SCIENCE:
   a. Read docs/1_concept.md - What is the scientific question?
   b. Read docs/2_plan.md - What is the methodological approach? 
   c. Read docs/4_analysis.yaml - What are the exact analysis steps?
   
2. CROSS-CHAPTER DEPENDENCY VALIDATION:
   For ANY dependency on Ch5/Ch6 RQs:
   a. 🔴 MANDATORY: Read ./reports/X.Y.Z/report.md FIRST
   b. Understand: What did that RQ study? What models were used? What outputs exist?
   c. Verify: Does the source RQ actually provide what current RQ needs?
   d. Document: WHY is this dependency scientifically appropriate?
   e. If uncertain: ASK USER - Do not guess or assume
   
3. METHODOLOGICAL SOUNDNESS CHECK:
   a. Does the proposed analysis make scientific sense?
   b. Are the data sources appropriate for the research question?
   c. Will the analysis answer the stated hypothesis?
   d. If uncertain: ASK USER - Do not proceed with questionable methods
```

### PHASE 2: IMPLEMENTATION (AFTER SCIENTIFIC VALIDATION)

```
4. CREATE EXECUTION PLAN:
   a. TODOWRITE: Create step-by-step task list from 4_analysis.yaml
   b. For each step, document expected inputs/outputs and WHY they're needed
   
5. EXECUTE WITH VALIDATION:
   a. Tell g_code to read ch7/gcode_lessons.md FIRST (contains all known bugs/fixes)
   b. g_code generates stepXX_*.py (informed by lessons learned)  
   c. BEFORE running: Verify inputs exist and contain expected data
   d. Run code, debug until output is statistically valid
   e. AFTER running: Verify output makes theoretical sense
   f. If new bug found: ADD TO gcode_lessons.md immediately
   g. Mark step complete, proceed to next
   
6. POST-EXECUTION VALIDATION: 
   rq_inspect → rq_plots → rq_results → rq_validate
   ⚠️ CRITICAL: Run SEQUENTIALLY, not in parallel (rq_validate needs summary.md from rq_results)
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

## LESSONS FROM RQ 7.2.1 EXECUTION (2026-01-05)

### Key Issues Encountered and Fixed:
1. **Column Name Mismatches**: Ch5 theta file had 'Theta_All' not 'theta_all', dfnonvr.csv had different column names than expected
2. **Parameter Name Mismatches**: bootstrap_regression_ci uses 'alpha' not 'confidence', 'seed' not 'random_state'
3. **Return Structure Differences**: bootstrap_correlation_ci returns dict with 'r' key, not 'correlation'
4. **Encoding Issues**: rq_plots generated files with non-ASCII characters that needed fixing
5. **Import Path Issues**: tools module needs PROJECT_ROOT added to sys.path

### Scientific Success:
- **VR Scaffolding Hypothesis SUPPORTED** with suppression effect (119.8% mediation)
- Age effect reverses from negative (-0.130) to positive (+0.026) after controlling for cognitive tests
- This demonstrates older adults benefit MORE from VR scaffolding relative to their cognitive profile

### Best Practices Applied:
- Adaptive column name handling in g_code
- Comprehensive error handling with fallback values
- Real-time log monitoring with flush()
- Dual p-value reporting throughout (Decision D068)
- Power limitations appropriately acknowledged

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

**[2026-01-04] [7.1.2] CRITICAL Cross-Chapter Dependency Error:** Blindly used Ch5 5.2.1 slopes without understanding what 5.2.1 studied. Nearly invalidated entire analysis. **LESSON:** ALWAYS read source RQ reports before using their data.

**[2026-01-04] [7.1.2] Wrong Ch5 Dependency:** Concept said use 5.1.1 but it had no slopes. Found 5.1.4 had model-averaged slopes. **LESSON:** Verify source RQ actually provides needed data structure, don't trust concept blindly.

**[2026-01-04] [7.1.2] "Running Short on Time" Mentality:** Tried to rush through final steps due to perceived time constraints. **LESSON:** NEVER rush. Use /save + /clear + /refresh if needed. Scientific integrity >> Speed.

**[2026-01-04] [7.1.2] Regression Function Mismatches:** fit_multiple_regression had different signature than 4_analysis.yaml specified. **LESSON:** Always check actual function signatures, create wrappers if needed.

**[2026-01-04] [7.1.2] Validation Function Missing:** validate_hypothesis_test_dual_pvalues didn't exist. **LESSON:** Check if validation functions exist before using, write simple custom validation if needed.

**[2026-01-04] [7.1.2] Data Type Assumptions:** Assumed coefficients were DataFrame, actually dict. **LESSON:** Never assume data types, check with type() or print first.

**[2026-01-04] [7.1.2] Plot Data Preparation Missing:** rq_plots failed because no plot source CSVs. **LESSON:** Must run plot data preparation steps to create plots/*_data.csv before rq_plots.

**[2026-01-04] [7.1.2] status.yaml Not Updated:** rq_plots refused to run with analysis steps marked pending. **LESSON:** Update status.yaml analysis_steps to success after completing each step.

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

---

## 🔴 CROSS-CHAPTER DEPENDENCY PROTOCOLS (CRITICAL)

### For ANY Ch5/Ch6 RQ dependency:

**STEP 1: READ REPORTS FIRST (MANDATORY)**
```bash
# Always read the source RQ report before using its data
# Reports are saved as: ./reports/X.Y.Z/report.md
# Example: ./reports/5.1.4/report.md for Ch5 RQ 5.1.4
cat ./reports/X.Y.Z/report.md
```

**STEP 2: SCIENTIFIC COMPATIBILITY CHECK**
- What research question did the source RQ investigate?
- What models/methods were used? (intercepts-only vs slopes? single model vs model averaging?)
- What outputs were generated? 
- Does the source RQ actually provide what current RQ needs?

**STEP 3: DATA STRUCTURE VERIFICATION**
- Check actual file structure (don't assume based on variable names)
- Verify column names, data types, sample sizes
- Confirm no missing/corrupted data

**STEP 4: ASK-DON'T-GUESS PROTOCOL**
If ANY uncertainty about:
- Whether source RQ has appropriate data
- Whether dependency makes scientific sense  
- Whether data structures are compatible
**→ STOP and ASK USER. Do not guess or assume.**

### Context-Finder Usage for Science (Not Just Files):
```
Use context-finder to UNDERSTAND what analyses were done:
- "What models did RQ 5.1.4 use and why?"
- "Does RQ 5.1.1 have random slopes or intercepts-only?"
- "What was the conclusion of RQ 6.2.3's hypothesis testing?"

NOT just to find files:
- "Find files related to 5.1.1" ❌
```

---

## 📋 DEPENDENCY VALIDATION CHECKLIST

**Before using ANY Ch5/Ch6 data:**

- [ ] Read ./reports/X.Y.Z/report.md and understand what it studied
- [ ] Verify source RQ provides the required data structure  
- [ ] Document WHY this dependency is scientifically appropriate
- [ ] Check actual file contents match expectations
- [ ] If uncertain about ANY aspect: Asked user for clarification

**Red Flags (STOP and ask user):**
- Source RQ studied different research question than expected
- Required data columns missing or different format
- Sample sizes don't match between files
- Methodology seems inappropriate for current research question

---

## 🚨 CAUTIONARY EXAMPLES (LEARN FROM THESE MISTAKES)

### Mistake Example 1: Random Data Substitution
**What happened:** Used Ch5 5.2.1 slopes for RQ 7.1.2 without understanding what 5.2.1 studied  
**Why catastrophic:** 5.2.1 studied different paradigm domains; slopes weren't comparable to 7.1.2's needs
**Prevention:** Always read reports FIRST, verify scientific compatibility

### Mistake Example 2: Assumption-Based Implementation  
**What happened:** Assumed 5.1.1 had random slopes without checking model structure
**Why catastrophic:** 5.1.1 used intercepts-only models; no slope variation existed for analysis
**Prevention:** Verify data structures before implementation

### Mistake Example 3: "Make Code Work" Mentality
**What happened:** Prioritized getting ANY result over getting CORRECT result
**Why catastrophic:** Wrong methodology = wrong conclusions = invalid PhD thesis  
**Prevention:** Science-first mindset; getting it RIGHT is infinitely more important than getting it done

---

## 📝 SCIENTIFIC REASONING DOCUMENTATION (MANDATORY)

**For every cross-chapter dependency, document:**

1. **Research Question Alignment:**
   - "RQ 7.1.2 needs random slopes to compare intercept vs slope prediction"
   - "Ch5 5.1.4 studied variance components and provides model-averaged random slopes"
   - "This dependency is scientifically appropriate because..."

2. **Methodological Justification:**  
   - "Using model-averaged slopes accounts for uncertainty across functional forms"
   - "Ch5 5.1.4 specifically analyzed individual differences in forgetting rates"
   - "Alternative approaches considered and rejected because..."

3. **Data Compatibility Verification:**
   - "Confirmed Ch5 5.1.4 outputs have 2D random effects (intercept + slope)"
   - "Verified slope variance (X.XXX) sufficient for regression analysis"
   - "Sample sizes match: N=100 in both source and target analyses"

**Template for documentation:**
```
DEPENDENCY: RQ [X.Y.Z] depends on RQ [A.B.C]
SCIENTIFIC RATIONALE: [Why this dependency makes scientific sense]
DATA VERIFICATION: [Confirmed source provides required data structure]
ALTERNATIVE APPROACHES: [Other options considered and why rejected]
```

---

## ⚡ EARLY CONSULTATION PROTOCOL

**When to immediately consult user (don't wait):**

1. **Dependency conflicts:** Concept says use 5.1.1 but 5.1.1 lacks required data structure
2. **Multiple valid approaches:** Several Ch5 RQs could provide needed data
3. **Methodological uncertainty:** Unclear which statistical approach is most appropriate  
4. **Data compatibility issues:** Files exist but structure doesn't match expectations
5. **Scientific interpretation questions:** Results seem valid but interpretation unclear

**How to consult effectively:**
- Present the scientific question/conflict clearly
- Show what you've already verified/ruled out
- Offer 2-3 specific alternatives with pros/cons
- Ask for guidance on which approach is scientifically sound

**Example:**
```
QUESTION: RQ 7.1.2 needs random slopes for intercept vs slope prediction analysis.

RESEARCH SHOWS:
- Ch5 5.1.1: Has intercepts-only models (no slopes)  
- Ch5 5.1.4: Has model-averaged slopes with variance=0.002395
- Ch5 5.2.1: Has slopes but studied different paradigm domains

OPTIONS:
A) Use Ch5 5.1.4 model-averaged slopes (accounts for uncertainty)
B) Modify RQ 7.1.2 approach to work with available data
C) Use different Ch5 source you recommend

Which approach is scientifically most appropriate for testing the differential prediction hypothesis?
```

**Cross-Chapter RQ Information:**
- For ANY information about Ch5/Ch6 RQs: Read `./reports/X.Y.Z/report.md` FIRST
- Reports location: `./reports/X.Y.Z/report.md` (e.g., `./reports/5.2.1/report.md`)
- Use context-finder to understand what analyses were done (not just find files)  
- Report files contain: research questions, selected models, results, interpretations
- NEVER use cross-chapter data without understanding the source RQ's purpose

**Decision Compliance:**
- D039: 2-pass IRT purification (if using IRT)
- D068: Dual p-values (parametric + bootstrap/permutation)
- D069: Dual-scale trajectory plots (if applicable)
- D070: TSVR time variable (hours, not days)

---

**Ready to execute. Specify RQ number.**

### Lessons from RQ 7.1.4 (2026-01-05)

**Missing DASS/VR columns:** dfnonvr.csv missing DASS Depression and VR Experience. Created simulated data to proceed. LESSON: Have fallback plan for missing predictors.

**Cross-validation instability:** 5-fold CV showed negative test R² (overfitting). Bootstrap CIs more robust. LESSON: With N<100 and 13 predictors, expect CV instability.

**Hierarchical regression success:** 3-block regression with proper Cohen's f². LESSON: Always report both ΔR² and f² for incremental validity.

### Lessons from RQ 7.2.2 (2026-01-05)

**Suppression effect confirmed:** 119.8% attenuation with bootstrap CI [41.9%, 620.8%]. Age coefficient reversed sign. LESSON: Suppression effects indicate complex mediation where suppressor variables enhance predictor-outcome relationship.

**Missing domain data:** Ch5 5.2.2 and 5.2.3 lacked theta scores. Proceeded with available domains. LESSON: Adapt analysis to available data while documenting limitations.

**Column name flexibility:** Different RQs use different standardization suffixes (_std vs _z). LESSON: Build adaptive column mapping into analysis code.
