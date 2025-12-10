# Chapter 6 RQ Execution Protocol

**Purpose:** Context window primer for executing any Ch6 RQ after /refresh
**Usage:** `read ch6/execute.md` then proceed with specified RQ

---

## EXECUTION FLOW

```
1. READ: 1_concept.md → 2_plan.md → 4_analysis.yaml (understand pipeline)
2. TODOWRITE: Create step-by-step task list from 4_analysis.yaml
3. LOOP per step:
   a. g_code generates stepXX_*.py
   b. Run code, debug until output is statistically valid
   c. Validate output makes theoretical sense
   d. Mark step complete, proceed to next
4. POST-EXECUTION: rq_inspect → rq_plots → rq_results → rq_validate
5. REPORT: Summary + thesis implications to user
```

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

## CRITICAL LESSONS FROM CH5

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

### Multi-Dimensional IRT Factor Difficulties
```python
# CORRECT: Factor-specific mean difficulties
source_b = item_params[item_params['factor']=='Source']['b'].mean()  # e.g., -0.45
dest_b = item_params[item_params['factor']=='Dest']['b'].mean()      # e.g., +1.37

# WRONG: difficulty=0.0 for all → masks 25-30 percentage point effects
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

## COMMON MISTAKES TO AVOID

### 1. Wrong LMM Model Selection
- **Check 1_concept.md** for exact model formula
- Random slopes `(Time | UID)` vs intercept-only `(1 | UID)`
- GLMM binomial for binary outcomes, LMM for continuous
- Verify REML vs ML setting matches specification

### 2. Inline Code vs Tool Function
**STOP AND ASK USER before:**
- Modifying any function in `tools/`
- Adding new helper functions
- Changing validation thresholds
- Creating workarounds for tool bugs

**DO inline:**
- One-off data transformations specific to this RQ
- Plot customizations
- Temporary debugging code

### 3. Plot Style Consistency
- Use existing `tools.plotting.*` functions
- Dual-scale plots for IRT (theta + probability)
- Decision D069 compliance for trajectories
- Don't create new plot types without asking

### 4. Validation Shortcuts
**NEVER skip:**
- rq_inspect output validation
- Assumption diagnostics (even if they fail)
- Documenting violations (don't hide them)

### 5. File Path Errors
- Always use `results/ch6/X.Y.Z/` prefix
- data/ for intermediate CSVs
- results/ for final outputs
- plots/ for plot source data
- logs/ for execution logs

---

## CODE-COPYING STRATEGY (75% Time Savings)

**When to use:** After first successful ROOT RQ in a chapter series (e.g., 6.3.1 → 6.4.1 → 6.5.1 → 6.8.1)

**Success rate:** 3/3 applications (RQs 6.4.1, 6.5.1, 6.8.1)
**Time savings:** 45 min vs 4-5 hours with g_code (75-80% reduction)
**Bug rate:** 1-2 predictable bugs vs 5-6 systematic bugs per step

### Procedure:

```bash
# 1. Copy all code files from working source RQ
cp -r results/ch6/SOURCE_RQ/code/* results/ch6/TARGET_RQ/code/

# 2. Update RQ ID references (CRITICAL - prevents overwriting source RQ!)
cd results/ch6/TARGET_RQ/code
sed -i 's/SOURCE_ID/TARGET_ID/g' *.py  # e.g., 6.5.1 → 6.8.1
sed -i 's/ch6\/SOURCE_ID/ch6\/TARGET_ID/g' *.py

# 3. Find/replace factor names (if different factor structure)
sed -i 's/OldFactor1/NewFactor1/g' *.py
sed -i 's/OldFactor2/NewFactor2/g' *.py
# ... for all factors

# 4. Update IRT_CONFIG['factors'] list (Steps 01 & 03)
# Manually edit step01*.py and step03*.py:
# OLD: 'factors': ['Common', 'Congruent', 'Incongruent']
# NEW: 'factors': ['Source', 'Destination']

# 5. Fix Q-matrix column naming (Bug #6/#7 pattern - PREDICTABLE)
# Check actual Q-matrix format from Step 00 output, then update:
# - Step 01: factor_col construction (lines ~245-255)
# - Step 03: factor_col construction (lines ~275-285)

# 6. Run all steps sequentially, fix path bugs as they arise
```

### ⚠️ CRITICAL PATH VERIFICATION (MANDATORY)

**BEFORE running ANY copied code, verify these paths:**

```python
# ✅ CORRECT: Dynamic path resolution
RQ_DIR = Path(__file__).resolve().parents[1]  # results/ch6/TARGET_RQ
LOG_FILE = RQ_DIR / "logs" / "stepXX_*.log"
df = pd.read_csv(RQ_DIR / "data" / "input.csv")
df.to_csv(RQ_DIR / "data" / "output.csv")

# ❌ WRONG: Hardcoded source RQ paths
LOG_FILE = Path("/path/to/6.5.1/logs/stepXX.log")  # ← DANGER!
df = pd.read_csv("results/ch6/6.5.1/data/input.csv")  # ← Reads wrong RQ!
df.to_csv("../6.5.1/data/output.csv")  # ← Overwrites source RQ!

# ❌ WRONG: Relative paths without RQ_DIR
df = pd.read_csv("data/input.csv")  # ← Depends on working directory
df.to_csv("results/output.csv")  # ← Wrong location

# ❌ WRONG: String literals with RQ ID
comment_path = "results/ch6/6.5.1/logs/step01.log"  # ← Check ALL comments too!
```

**Verification checklist (run BEFORE executing):**
```bash
# 1. Grep for source RQ ID in ALL files
grep -r "SOURCE_ID" results/ch6/TARGET_RQ/code/
# → Should return ZERO matches

# 2. Grep for hardcoded absolute paths
grep -r "/results/ch6/" results/ch6/TARGET_RQ/code/
# → Should return ZERO matches (except comments)

# 3. Check RQ_DIR is correctly defined
grep -n "RQ_DIR = " results/ch6/TARGET_RQ/code/*.py
# → Should use parents[1] or resolve() to target RQ

# 4. Verify log file paths
grep -n "LOG_FILE = " results/ch6/TARGET_RQ/code/*.py
# → Should use RQ_DIR / "logs" / ...

# 5. Check all read_csv/to_csv calls
grep -n "read_csv\|to_csv" results/ch6/TARGET_RQ/code/*.py
# → Should use RQ_DIR / "data" / ... or relative paths from RQ_DIR
```

**Common path bugs (from RQ 6.8.1):**
- ✅ Fixed: TEST vs test column name case sensitivity
- ✅ Fixed: expected_rows validation (3 factors → 2 factors)
- ✅ Fixed: melt() including UID column as location value
- ⚠️ Remaining: Steps 06-07 using relative 'data/' instead of RQ_DIR / 'data/'

### Predictable Bugs to Fix Proactively:

**Bug #6/#7 (Q-matrix column naming):**
```python
# Check Q-matrix format FIRST (from Step 00 output):
df_q = pd.read_csv("results/ch6/TARGET_RQ/data/step00_q_matrix.csv")
print(df_q.columns)  # e.g., ['item_name', 'Source', 'Destination']

# Then update factor_col construction in Steps 01 & 03:
# FORMAT 1 (domain-based): factor_col = f"factor_{factor.lower()}"
# FORMAT 2 (numbered uppercase): factor_col = f"factor{i}_{factor}"
# FORMAT 3 (descriptive lowercase): factor_col = f"factor_{factor.lower()}"
# FORMAT 4 (direct capitalized): factor_col = factor  # ← RQ 6.8.1
```

**Expected row counts (n_factors dependent):**
```python
# Step 04 validation - update for actual factor count:
expected_rows = len(df_theta) * N_FACTORS  # 2 for Source/Dest, 3 for What/Where/When
```

### Why Code-Copying Works:

1. **Bugs #1-7 already fixed** in source RQ (systematic IRT issues)
2. **IRT settings validated** (mc_samples=1/100 pattern proven)
3. **File structure identical** (data/, logs/, plots/, results/ folders)
4. **LMM formula patterns** reusable across RQs
5. **Validation logic** generalizes well

### When NOT to Code-Copy:

- ❌ First RQ in chapter (no working template)
- ❌ Different analysis type (IRT → CTT, LMM → correlation)
- ❌ Different data structure (wide → long format change)
- ❌ New tool functions required (not just parameter changes)

---

## STEP EXECUTION TEMPLATE

For each step in 4_analysis.yaml:

```
1. READ step specification (inputs, outputs, validation)
2. CHOOSE strategy:
   a. CODE-COPY: If working template exists (verify paths first!)
   b. G_CODE: If first RQ or new analysis type
3. RUN: poetry run python results/ch6/X.Y.Z/code/stepXX_*.py
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
**rq_plots:** Creates publication-quality visualizations
**rq_results:** Generates summary.md with anomaly detection
**rq_validate:** Thesis-quality checklist validation

Run in sequence. Don't skip. Each catches different issues.

---

## THESIS CONTEXT

**Chapter 6 Theme:** Metacognitive confidence and calibration
**Key Questions:**
- Does confidence track accuracy? (calibration)
- Do high-confidence errors reveal metacognitive failures? (HCE)
- Can initial confidence predict forgetting? (predictive validity)
- Do source/destination show confidence dissociation? (replication)

**Connect results to:**
- Ch5 accuracy findings (convergent evidence)
- Theoretical frameworks in 1_concept.md
- Clinical implications for memory assessment

---

## LESSONS LEARNED LOG (Terse Format - Updated Session-by-Session)

**Purpose:** Capture critical insights discovered during Ch6 execution for cross-RQ learning. Add new lessons in terse format immediately after discovery. Format: `[Date] [RQ] [Lesson]`

### Validation Workflow Lessons

**[2025-12-10] [6.3.1, 6.4.1, 6.5.1, 6.8.1] Validation Agent Sequence:**
- plots.py requires PYTHONPATH set: `PYTHONPATH=/path/to/project poetry run python plots/plots.py`
- Import error if run from plots/ directory (tools module not found)
- rq_results agents BLOCK until PNG files exist (visual inspection required)
- Execute plots.py BEFORE launching rq_results agents
- All 4 agents (inspect → plots → results → validate) can run in parallel across RQs
- status.yaml must reflect actual execution state (agents quit if mismatch)

**[2025-12-10] [6.3.1] Step 08 Documentation Steps:**
- Some RQs have step08 (Ch5 comparison documentation) in plan but no code generated
- If step08 exists in 4_analysis.yaml but not executed: mark as "deferred" in status.yaml
- rq_results agents will document comparison qualitatively in summary.md
- Formal statistical comparison can be completed post-validation if needed

**[2025-12-10] [6.4.1, 6.5.1] Status.yaml Staleness:**
- Code-copying strategy updates code files but NOT status.yaml
- Agents read status.yaml to determine workflow state
- ALWAYS update status.yaml after manual execution (code-copying, bug fixes)
- Pattern: g_code=success, rq_inspect=success, all analysis_steps=success before launching plots/results

**[2025-12-10] [All 4 RQs] 100% Item Retention Pattern:**
- All Ch6 confidence RQs showed 100% item retention after purification (unusual vs typical 30-70%)
- GRM 5-category ordinal data may have inherently better psychometric properties than binary accuracy
- Discrimination: 1.98-6.14 (well above a≥0.4 threshold)
- Difficulty: 0.05-1.18 (well within |b|≤3.0 threshold)
- Documented as "unusual pattern" in validation.md, not blocking for thesis
- May indicate purification thresholds need tightening for ordinal IRT (sensitivity analysis recommended)

### Common Validation Issues

**[2025-12-10] GRM-2PL Probability Transformation Mismatch:**
- plots.py may use 2PL approximation instead of GRM category averaging
- Can cause probability reversals (higher probability despite lower theta)
- Observed in RQ 6.3.1: When domain higher probability (20%) vs lower theta (-0.39)
- Theta scale remains valid regardless; probability scale interpretability reduced
- Document limitation in thesis methods if observed

**[2025-12-10] Day 6 Floor Effects in Confidence Data:**
- Confidence trajectories converge to 2-3% probability by Hour 151 (Day 6)
- Near measurement floor for 5-category Likert scale
- Limits Decision D069 dual-scale interpretability (designed for accuracy, questionable for confidence)
- May reflect genuine confidence collapse, response bias, or scale compression
- Document in limitations, recommend raw distribution analysis

---

## QUICK REFERENCE

| Analysis Type | Model | Key Validation |
|--------------|-------|----------------|
| IRT Trajectories | GRM 5-category | mc_samples=1/100, factor difficulties |
| LMM | statsmodels MixedLM | n_fe slicing, CSV export |
| GLMM | binomial family | Item-level data, overdispersion check |
| Correlation | Pearson/Spearman | Normality test, bootstrap CI |
| Calibration | theta_conf - theta_acc | Reliability check, Lord's paradox |

**Decision Compliance:**
- D039: 2-pass IRT purification
- D068: Dual p-values (parametric + bootstrap/permutation)
- D069: Dual-scale trajectory plots
- D070: TSVR time variable (hours, not days)

---

**Ready to execute. Specify RQ number.**
