# PLATINUM CERTIFICATION WORKFLOW: RQ 5.2.6

**RQ:** 5.2.6 - Domain-Specific Variance Decomposition
**Date Started:** 2025-12-31
**Agent:** rq_platinum (v4.X)
**Criteria Version:** 2025-12-31

---

## PHASE 1: CONTEXT GATHERING (Steps 1-3)

### Step 1: Read RQ-Specific Context ✓

**Files Read:**
- ✓ docs/1_concept.md - Domain-specific variance decomposition, ICC > 0.40 hypothesis
- ✓ docs/2_plan.md - 7-step analysis plan, LMM with random slopes
- ✓ status.yaml - All agents completed successfully
- ✓ results/summary.md - ICC_slope_conditional: What=0.518, Where=0.531 (both SUBSTANTIAL)
- ✓ results/validation.md - 0 issues, VALIDATED FOR THESIS

**Key Findings:**
- **Hypothesis:** ICC_slope_conditional > 0.40 for each domain (trait-like forgetting)
- **Method:** Domain-stratified LMMs (separate per domain) with random intercepts + slopes
- **Current Status:** Primary hypothesis SUPPORTED (What=0.518, Where=0.531)
- **Critical Exclusion:** When domain excluded due to floor effect (77% item attrition)
- **Data:** 800 rows (100 UID × 4 tests × 2 domains)
- **Findings:**
  - Both domains substantial trait variance (~50% between-person)
  - Where domain: Significant Fan Effect (r=-0.32, p_bonf=0.003)
  - What domain: No significant intercept-slope correlation

**No Previous PLATINUM Certification Found**

---

### Step 2: Read Project-Level Requirements ✓

**Files Read:**
- ✓ results/glmm_candidates.md (MANDATORY)
- ✓ results/improvement_taxonomy.md (10 sections)

**🔴 GLMM COMPLIANCE CHECK (Step 2):**

**Searched glmm_candidates.md for "5.2.6":**
- ❌ **NOT LISTED in glmm_candidates.md**
- Need to determine if GLMM validation required via manual evaluation in Step 9A.1

**Extracted from glmm_candidates.md:**
- Pattern: GLMM reveals intercepts (baseline differences), slopes always agree
- Examples: RQ 5.1.3 Age intercept (p=.061→.014), RQ 5.4.1 Schema intercept (p=.548→.011)
- Slopes/interactions: Always agree between IRT→LMM and GLMM

**Extracted from improvement_taxonomy.md:**
- Section 1 (GLMM): Tests intercept effects, 28,800 vs 400-1,200 observations
- Section 3 (Power): Mandatory for NULL findings (TOST, post-hoc power)
- Section 4.4 (Random Slopes): 🔴 MANDATORY for modeling RQs
- Section 5 (Assumptions): LMM diagnostics mandatory
- Section 7 (Documentation): Dual p-values (D068), dual scales
- Section 8.3 (Confidence RQs): Response patterns mandatory

**Applicable Sections:**
- ⚠️ Section 1: GLMM (evaluate in Step 9A.1 - intercept comparisons across domains)
- ✅ Section 3: Power/Effect Sizes (ICC values ARE effect sizes, >0.50 adequate)
- ✅ Section 4.4: Random Slopes (MANDATORY - verify tested)
- ✅ Section 5: Assumptions (LMM diagnostics)
- ✅ Section 7: Documentation (dual p-values D068)
- ❌ Section 8.3: Response patterns (not a confidence RQ)

---

### Step 3: Inventory Current State ✓

**Folder Structure:**
```
results/ch5/5.2.6/
├── docs/           ✓ Complete (1_concept.md, 2_plan.md, 3_tools.yaml, 4_analysis.yaml)
├── data/           ✓ All outputs present (step00-step08)
├── code/           ✓ All scripts (step00-step08)
├── logs/           ✓ Execution logs exist
├── plots/          ✓ domain_icc_barplot.png exists
├── results/        ✓ summary.md, validation.md complete
└── status.yaml     ✓ All agents success
```

**Data Files Inventory:**
- ✓ step00_lmm_input_filtered.csv (800 rows, When excluded)
- ✓ step01_model_metadata_what.yaml (Full random structure, converged)
- ✓ step01_model_metadata_where.yaml (Full random structure, converged)
- ✓ step01_fitted_models.pkl (2 MixedLM objects)
- ✓ step02_variance_components.csv (10 rows: 5 components × 2 domains)
- ✓ step03_icc_estimates.csv (6 rows: 3 ICC types × 2 domains)
- ✓ step04_random_effects.csv (200 rows: 100 UID × 2 domains)
- ✓ step05_intercept_slope_correlations.csv (2 rows, dual p-values D068)
- ✓ step06_domain_icc_comparison.csv (domain rankings)
- ✓ step07_domain_icc_barplot_data.csv (plot source)
- ✓ step08_*.csv (model-averaged variance, competitive models)

**Code Files:**
- ✓ step01_fit_domain_lmms.py (random slopes implemented: re_formula='~log_TSVR')
- ✓ All other scripts present

**Missing Files:** None

**Stale Outputs Check:**
- All files dated 2025-12-03 or 2025-12-09 (consistent, recent)
- No timestamp mismatches detected

**File Organization Issues:** None

---

## PHASE 2: GAP ANALYSIS (Steps 4-5)

### Step 4: Map RQ to Applicable Taxonomy Sections ✓

**Section 1 (GLMM Validation):**
- 🟡 **Evaluate in Step 9A.1** - RQ NOT in glmm_candidates.md
- Tests: Domain baseline differences (What vs Where at Day 0)
- Model formula: `theta ~ log_TSVR` (separate models per domain - NO domain predictor)
- **Key insight:** Domain-stratified models don't have domain main effect (separate fits)
- **Manual evaluation needed:** Does this RQ test intercepts? YES (baseline variance decomposition)
- Priority: MEDIUM (not testing group contrasts, but baseline variance)

**Section 2 (Statistical Robustness):**
- Not marginal findings (ICC ~0.52 clearly substantial)
- No binary outcomes
- Priority: LOW (not needed)

**Section 3 (Power & Effect Sizes):**
- ICC values ARE effect sizes (0.518, 0.531)
- No NULL findings (both domains substantial)
- CIs: Not standard for ICC (point estimates adequate)
- Priority: LOW (effect sizes already reported)

**Section 4 (Model Selection & Random Effects):**
- **4.4 Random Slopes Testing:** 🔴 MANDATORY
- Evidence needed: Intercepts-only vs intercepts+slopes comparison
- Current: Full random structure converged (re_formula='~log_TSVR')
- **Question:** Was intercepts-only tested via LRT? Need to verify in Step 12A
- Priority: 🔴 BLOCKER if not tested

**Section 5 (Assumption Validation):**
- LMM diagnostics needed: Q-Q, residuals vs fitted, homoscedasticity
- validation.md confirms convergence, variance positivity
- Need to verify assumption checks performed
- Priority: HIGH (mandatory for LMM)

**Section 6 (Sensitivity Analyses):**
- Not a calibration RQ (no difference scores)
- Not testing alternative breakpoints
- Priority: LOW (not applicable)

**Section 7 (Documentation):**
- Dual p-values: ✓ D068 compliant (step05_intercept_slope_correlations.csv)
- Dual scales: Not applicable (variance decomposition, not trajectories)
- Plots: ✓ domain_icc_barplot.png current
- Priority: MEDIUM (verify completeness)

**Section 8 (Data Quality):**
- Not confidence RQ (no response patterns needed)
- IRT purification documented (70 items from RQ 5.2.1)
- Priority: LOW (inherited from parent RQ)

**Section 9 (Theoretical Grounding):**
- summary.md Section 3 has extensive interpretation
- Literature cited (Koo & Li 2016, McGraw & Wong 1996, dual-process theory)
- Mechanisms explained (hippocampal consolidation, Fan Effect)
- Priority: MEDIUM (verify completeness)

**Section 10 (Critical Issues):**
- Convergence: ✓ Both domains converged (Full random structure)
- Missing analyses: Check random slopes testing (Step 12)
- Stale outputs: None detected
- Priority: VERIFY in subsequent steps

---

### Step 5: Generate Prioritized Action Plan ✓

**Priority: BLOCKER**
- None identified yet (pending Step 12 random slopes check)

**Priority: HIGH**
- [ ] Step 9: GLMM compliance evaluation (manual Step 9A.1 - domain-stratified models)
- [ ] Step 12: Random slopes testing verification (intercepts-only vs slopes comparison)
- [ ] Step 13: LMM assumption validation (Q-Q, residuals, homoscedasticity)

**Priority: MEDIUM**
- [ ] Step 17: Theoretical grounding completeness
- [ ] Step 19: Update summary.md with any new findings
- [ ] Step 20: Update validation.md with checks performed

**Priority: LOW**
- None currently

---

## PHASE 3: FILE ORGANIZATION (Steps 6-8)

### Step 6: Standardize File Naming ✓

**Check:**
- ✓ Code files: step00_*.py, step01_*.py, step02_*.py (consistent)
- ✓ Data files: step00_*.csv, step01_*.yaml, step02_*.csv (descriptive)
- ✓ Plot files: domain_icc_barplot.png (descriptive)

**No renaming needed - All files follow conventions**

---

### Step 7: Handle Stale Outputs ✓

**Timestamp Check:**
- Code files: 2025-12-03 14:04 - 14:11, step08: 2025-12-09 16:17
- Data files: 2025-12-03 (step00-07), 2025-12-09 (step08)
- Plots: 2025-12-03

**No stale outputs detected - All consistent**

---

### Step 8: Create Missing Mandatory Files ✓

**Check:**
- ✓ results/summary.md exists (comprehensive, 550 lines)
- ✓ results/validation.md exists (comprehensive validation report)
- ✓ status.yaml exists

**No missing mandatory files**

---

## PHASE 4: EXECUTE IMPROVEMENTS (Steps 9-18)

### Step 9: Section 1 - GLMM Validation

#### Step 9A.0: PRE-CHECK FAIL-SAFE ✓

**Question:** Did I read results/glmm_candidates.md in Step 2?
- ✅ **YES** - Read in Step 2, searched for "5.2.6"

**Proceeding to Step 9A**

---

#### Step 9A: Check If RQ in glmm_candidates.md ✓

**Cross-reference result:**
- ❌ **RQ 5.2.6 NOT LISTED** in glmm_candidates.md
- Not in HIGH priority, not in MEDIUM priority, not in LOW/EXCLUDED

**Proceed to Step 9A.1 (Manual Evaluation)**

---

#### Step 9A.1: Manual Evaluation ✓

**Does this RQ test ANY intercept effects?**

**Model specification analysis:**
```
For each domain (What, Where) SEPARATELY:
  Formula: theta ~ log_TSVR + (log_TSVR | UID)

  NO GROUP MAIN EFFECTS - domain-stratified models fit separately
```

**Key distinction:** This RQ does NOT test domain contrasts (What vs Where baseline comparison). It tests variance decomposition WITHIN each domain separately.

**Does RQ test intercepts?**
- **Intercept variance:** YES - var_intercept is primary output (baseline variance)
- **Group contrasts:** NO - no between-domain comparison (separate models)

**From glmm.md pattern:**
- GLMM reveals: Group baseline differences (intercept effects)
- GLMM agrees: Slope/interaction effects

**This RQ:**
- Tests: WITHIN-domain variance in baseline (var_intercept)
- Does NOT test: BETWEEN-domain baseline differences (no domain main effect)

**Conclusion: GLMM NOT NEEDED**

**Rationale:**
1. No group predictor in models (domain-stratified = separate fits)
2. No baseline group comparisons tested (What vs Where not compared)
3. Variance decomposition is meta-analysis of fitted models (not testing main effects)
4. Finding NOT null (ICC ~0.52 clearly substantial)

**GLMM would be needed IF:**
- Single model: `theta ~ Domain + log_TSVR + (log_TSVR | UID)` (tests Domain intercept)
- Testing: NULL finding for domain baseline differences
- But this RQ doesn't have that structure

**Decision: Skip GLMM validation - Not applicable to variance decomposition RQ**

**Documented rationale:** Domain-stratified models (separate per domain) do not test between-domain intercept contrasts. GLMM validation applies to RQs testing group main effects, not variance decomposition within groups.

**Proceed to Step 10**

---

### Step 10: Section 2 - Statistical Robustness ✓

**Not needed:**
- No marginal findings (ICC ~0.52 clearly substantial)
- No binary outcomes (continuous theta)

**Skip to Step 11**

---

### Step 11: Section 3 - Power & Effect Sizes ✓

**Check:**
- ✓ Effect sizes reported: ICC values (0.518, 0.531)
- ✓ Interpretations: "Substantial" threshold (>=0.40) applied
- ✓ No NULL findings requiring power analysis

**Already complete - no action needed**

---

### Step 12: Section 4 - Model Selection & Random Effects

#### Step 12A: Check If Random Slopes Already Tested 🔴 CRITICAL

**MANDATORY: Must verify random slopes comparison performed**

**Evidence search:**

**1. Check for comparison script:**
- step01_fit_domain_lmms.py exists
- Contains convergence fallbacks (Full → Uncorrelated → Intercept-only)
- **But no explicit intercepts-only vs slopes AIC comparison**

**2. Check validation.md:**
- M3 Detail: "Random Slopes on log_TSVR" - confirms slopes used
- M4 Detail: "Full random structure achieved" for both domains
- M5 Detail: var_slope positive (What=0.003, Where=0.004)
- **NO mention of "intercepts-only vs slopes comparison"**
- **NO mention of LRT test or ΔAIC**

**3. Check summary.md:**
- Line 99: "ICC_slope_simple is LOW (< 0.02) for both domains"
- Lines 220-228: Discusses ICC_slope_simple vs ICC_slope_conditional
- **NO documentation of random slopes testing procedure**

**4. Check code/step01_fit_domain_lmms.py:**
- Lines 94-201: Fit attempts (Full → Uncorrelated → Intercept-only)
- Fallback procedure implemented
- **But fallback is for CONVERGENCE failures, not model comparison**
- **No AIC-based model selection between structures**

**Result: 🔴 BLOCKER - Random slopes NOT tested via formal comparison**

**What exists:**
- ✓ Random slopes IMPLEMENTED (re_formula='~log_TSVR')
- ✓ Full structure CONVERGED for both domains
- ✓ Variance components positive (var_slope > 0)

**What's missing:**
- ❌ Intercepts-only model NOT fitted for comparison
- ❌ AIC comparison (intercepts-only vs slopes) NOT performed
- ❌ ΔAIC NOT documented
- ❌ No justification for using slopes (other than "it converged")

**Issue:** Cannot claim slopes improve fit without testing intercepts-only alternative

**Proceed to Step 12C: Create Random Slopes Comparison**

---

#### Step 12C: Create Random Slopes Comparison 🔴 BLOCKER RESOLUTION

**STATUS: Need to implement**

**Approach:**
- Fit intercepts-only models: `theta ~ log_TSVR + (1 | UID)` for each domain
- Compare AIC to existing Full models
- Compute ΔAIC
- Interpret: Option A/B/C (see rq_platinum protocol)

**This will be implemented in execution phase**

---

(Continue with remaining steps after random slopes testing completed...)

---

## PRIORITY ACTIONS IDENTIFIED

**BLOCKERS (Must fix before PLATINUM):**
1. 🔴 **Random slopes testing** (Step 12C) - No formal comparison documented
   - Action: Fit intercepts-only models for What and Where
   - Compare AIC to existing Full models
   - Document ΔAIC and interpret outcome

**HIGH (Mandatory):**
2. **LMM assumption validation** (Step 13) - Not documented
   - Action: Generate Q-Q plots, residuals vs fitted, homoscedasticity tests
   - Document in validation.md

**MEDIUM (Recommended):**
3. **GLMM evaluation documented** - Step 9A.1 reasoning captured
   - Action: Add to validation.md explaining why GLMM not needed

**Next: Execute Step 12C to resolve BLOCKER**
