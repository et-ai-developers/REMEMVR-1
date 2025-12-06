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

## STEP EXECUTION TEMPLATE

For each step in 4_analysis.yaml:

```
1. READ step specification (inputs, outputs, validation)
2. INVOKE g_code: "Generate stepXX for results/ch6/X.Y.Z"
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
