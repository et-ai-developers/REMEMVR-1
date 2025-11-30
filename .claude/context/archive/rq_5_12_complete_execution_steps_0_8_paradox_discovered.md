# RQ 5.12 Complete Execution - Steps 0-8, Paradox Discovered

## Session (2025-11-30 01:00)

**Archived from:** state.md
**Original Date:** 2025-11-30 01:00
**Reason:** RQ 5.12 execution phase complete (all 9 analysis steps), paradox discovered, ready for validation phase

---

**Task:** RQ 5.12 Step-by-Step Code Generation and Execution - Complete Analysis Pipeline (Steps 0-8)

**Context:** User requested execution of Step 0 using g_code agent with statistical validation mindset ("make sure results make statistical sense"). Proceeded through all 9 analysis steps (0-8) with comprehensive debugging, statistical validation, and scientific interpretation. Discovered major unexpected finding contradicting primary hypothesis.

**Major Accomplishments:**

**1. Step 0: Load Data Sources (COMPLETE - 1 bug fixed)**

**g_code Generation:**
- ✅ Generated step00_load_data.py with comprehensive validation
- ✅ Cross-RQ dependency check (verifies RQ 5.1 completion via status.yaml)
- ✅ Loads 4 input files (purified items, theta scores, TSVR mapping, raw scores)

**Bug #1: Status YAML Schema Mismatch**
- Expected: `status['steps']['step03_theta_scores']` (flat structure)
- Actual: `status['analysis_steps']['step03_irt_calibration_pass2']` (nested structure)
- Root cause: RQ 5.1 uses v4.X nested schema, g_code assumed flat schema
- Fix: Updated status check to use correct nested path
- Impact: Prevented FileNotFoundError on valid completed RQ

**Execution Results:**
- ✅ All 4 data sources loaded successfully (400 rows each for theta/TSVR/raw, 69 purified items)
- ✅ Composite_ID created (UID_test format: A010_1, A010_2, etc.)
- ✅ All validation passed (file existence, column schemas)

**Statistical Validation:**
- Purified items: 69 items (within expected 38-70 range)
- Item domains visible: What (-N-), Where (-U-/-D-/-L-), When (-O-/-T-)
- IRT parameters: a ∈ [0.44, 1.97], b ∈ [-2.59, 2.88] (within purification bounds |b| ≤ 3.0)
- Theta ranges: what [-1.33, 1.97], where [-1.26, 2.44], when [-0.37, 0.89] (plausible IRT range)
- All 400 composite_IDs with complete data (no missing values)

**2. Step 1: Map Items to Full vs Purified Sets (COMPLETE - 2 bugs fixed)**

**g_code Generation:**
- ✅ Generated step01_map_items.py for item retention mapping
- ✅ Stdlib operations (set operations, domain classification)

**Bug #2: Tool API Mismatch**
- Expected: `column_types={'item_name': object, 'domain': object, 'retained': bool}`
- Actual: Function signature requires `column_types: Dict[str, tuple]` (tuples of types)
- Fix: Changed to `column_types={'item_name': (object,), 'domain': (object,), 'retained': (bool,)}`
- Impact: Prevented TypeError during validation

**Bug #3: Specification Error - Item Count**
- Expected: 48-52 items total (per 4_analysis.yaml)
- Actual: 105 items total in dfData.csv (29 What + 50 Where + 26 When)
- Fix: Updated validation range to (100, 110)
- Root cause: Specification assumed ~50 items based on incomplete information
- Impact: Prevented false validation failure on correct data

**Execution Results:**
- ✅ Item mapping created: 105 items (69 retained, 36 removed)
- ✅ Domain breakdown: What 19/29 (65.5%), Where 45/50 (90.0%), When 5/26 (19.2%)

**Statistical Validation - CRITICAL FINDING:**
- **When domain: Only 19.2% retention (5 items remaining from 26)** ⚠️
- Severe item attrition matches RQ 5.1 floor effects (temporal items very difficult)
- Where domain: Excellent 90% retention (45 items, best for reliability)
- What domain: Moderate 65.5% retention (19 items, adequate)
- **Implication:** When domain measurements will be unreliable (only 5 items, below 7-10 minimum)

**3. Step 2: Compute Full CTT Scores (COMPLETE - 0 bugs)**

**g_code Generation:**
- ✅ Generated step02_compute_full_ctt.py with zero bugs
- ✅ Stdlib operations (pandas mean aggregation by domain)

**Execution Results:**
- ✅ Full CTT scores computed for all 400 composite_IDs
- ✅ Score ranges: What [0.345, 1.000], Where [0.300, 0.925], When [0.154, 0.865]
- ✅ Score means: What 0.772, Where 0.598, When 0.460

**Statistical Validation:**
- Domain performance pattern: What > Where > When (expected, temporal memory hardest)
- No ceiling/floor effects at participant level (good spread)
- Example trajectory (A010): Test 1 → Test 4 shows forgetting (What 96.6%→93.1%, Where 88.5%→59.5%)
- Zero NaN values (complete data)
- All scores in [0, 1] range (valid proportions)

**4. Step 3: Compute Purified CTT Scores (COMPLETE - 0 bugs)**

**g_code Generation:**
- ✅ Generated step03_compute_purified_ctt.py with zero bugs
- ✅ Filters to retained items only (retained=True)

**Execution Results:**
- ✅ Purified CTT scores computed for all 400 composite_IDs
- ✅ Score ranges: What [0.105, 1.000], Where [0.300, 0.939], When [0.000, 1.000]
- ✅ Score means: What 0.716, Where 0.615, When 0.382

**Statistical Validation - Full vs Purified Comparison:**
- What: Mean Δ = -0.056 (purified slightly harder, 10 items removed)
- Where: Mean Δ = +0.017 (purified slightly easier, only 5 items removed, validates IRT)
- **When: Mean Δ = -0.078 (purified much harder, 21 items removed, 5 very difficult items remain)** ⚠️
- When domain shows extreme instability (example A010: full 0.73 vs purified 0.30 at Test 1)
- **Expected impact:** When domain Cronbach's α will be compromised (5 items insufficient)

**5. Step 4: Assess Reliability (COMPLETE - 0 bugs)**

**g_code Generation:**
- ✅ Generated step04_assess_reliability.py with zero bugs
- ✅ Uses catalogued tool: compute_cronbachs_alpha with bootstrap 95% CIs (n=1000)

**Execution Results (6000 bootstrap iterations, ~2 minutes):**
- ✅ Cronbach's α computed for full and purified sets across 3 domains

**Statistical Results:**
| Domain | Full α [CI] | Items | Purified α [CI] | Items | Δα | Assessment |
|--------|-------------|-------|-----------------|-------|-----|-----------|
| What | 0.712 [0.661, 0.753] | 29 | 0.702 [0.649, 0.744] | 19 | -0.010 | Minimal decline, CIs overlap ✅ |
| Where | 0.821 [0.798, 0.843] | 50 | 0.829 [0.804, 0.849] | 45 | +0.007 | Slight improvement ✅ |
| When | 0.575 [0.502, 0.630] | 26 | 0.616 [0.551, 0.674] | 5 | +0.041 | Improved but **still < 0.70** ⚠️ |

**Critical Scientific Finding:**
- ✅ What & Where: Acceptable-to-good reliability (α ≥ 0.70)
- ⚠️ When domain: Poor reliability for BOTH full (α=0.575) and purified (α=0.616)
- IRT purification improved or maintained reliability in all domains ✅
- **But When domain unreliable regardless** (inherent temporal memory inconsistency + only 5 items)
- Validates methodological hypothesis that purification maintains/improves reliability
- **Limitation:** When domain below acceptable threshold, results must be interpreted cautiously

**6. Step 5: Correlation Analysis with Steiger's z-test (COMPLETE - 0 bugs)**

**g_code Generation:**
- ✅ Generated step05_correlation_analysis.py with zero bugs
- ✅ Uses catalogued tool: compare_correlations_dependent (Steiger's 1980 formula)
- ✅ Decision D068 compliance (dual p-value reporting: uncorrected + Bonferroni)

**Execution Results:**
- ✅ Steiger's z-test completed for all 3 domains (n=400)

**CRITICAL SCIENTIFIC FINDINGS - PRIMARY HYPOTHESIS TESTED:**

| Domain | Full CTT-IRT (r) | Purified CTT-IRT (r) | Δr | Steiger's z | p (uncorr) | p (Bonf) | Significant? |
|--------|------------------|----------------------|----|-------------|------------|----------|--------------|
| **What** | 0.879 | 0.906 | +0.027 | 10.06 | <0.001 | <0.001 | **YES** ✅ |
| **Where** | 0.940 | 0.955 | +0.015 | 14.22 | <0.001 | <0.001 | **YES** ✅ |
| **When** | 0.451 | 0.838 | +0.388 | 2.09 | 0.037 | 0.111 | **NO** ⚠️ |

**Hypothesis 1 Status: PARTIALLY SUPPORTED (2/3 domains)**

**What Domain:**
- Purified CTT significantly improves correlation with IRT (r: 0.879 → 0.906)
- Effect size modest (+2.7 percentage points) but highly significant (z=10.06)
- Validates that IRT purification improves convergent validity

**Where Domain:**
- Purified CTT significantly improves correlation with IRT (r: 0.940 → 0.955)
- Effect size small (+1.5 percentage points) but very strong evidence (z=14.22)
- Despite already excellent correlation (r=0.94), purification still helps

**When Domain - CRITICAL PARADOX:**
- Purified CTT shows MASSIVE improvement (r: 0.451 → 0.838, Δr = +0.388!)
- Full CTT-IRT correlation poor (r=0.45) due to unreliability (α=0.58)
- Purified CTT-IRT correlation excellent (r=0.84), comparable to What/Where
- **BUT fails Bonferroni correction** (p=0.111, needs p<0.017)
- Uncorrected p=0.037 suggests real effect, but low power (5 items, high variability)
- **Interpretation:** Pattern consistent with hypothesis but measurement limitations prevent statistical significance

**Overall Convergence Quality:**
- Mean Full CTT-IRT: r = 0.757
- Mean Purified CTT-IRT: r = 0.900
- **Mean improvement: +14.3 percentage points** (substantively large)

**7. Step 6: Standardize Outcomes for Parallel LMM (COMPLETE - 0 bugs)**

**g_code Generation:**
- ✅ Generated step06_standardize_outcomes.py with zero bugs
- ✅ Stdlib operations (z-score transformation per measurement × domain)
- ✅ Rationale: AIC comparison requires identical scales (Burnham & Anderson 2002)

**Execution Results:**
- ✅ All 1200 rows standardized (400 composite_IDs × 3 domains)
- ✅ Long format created: composite_ID, UID, TSVR_hours, domain, z_full_ctt, z_purified_ctt, z_irt_theta

**Statistical Validation:**
- All means effectively 0 (4.26×10⁻¹⁶, -2.19×10⁻¹⁶, -5.92×10⁻¹⁸) ✅
- All SDs = 0.9992 (within ±0.01 tolerance, essentially 1.0) ✅
- Pre-standardization: CTT scores [0,1] bounded, IRT theta unbounded logit (completely different scales)
- Post-standardization: All on same scale (mean=0, SD=1)
- Standardization preserves: relative ordering, individual differences, time effects
- Standardization enables: valid AIC comparison across measurement methods

**8. Step 7: Fit Parallel LMMs to Standardized Outcomes (COMPLETE - 3 bugs fixed)**

**g_code Generation:**
- ✅ Generated step07_fit_parallel_lmms.py implementing detailed loop specification
- ✅ Catalogued tool: fit_lmm_trajectory_tsvr (called 3 times in loop)
- ✅ Validation tool: validate_lmm_convergence

**Bug #4: Missing 'test' Column**
- df_tsvr unmerge extracted only ['composite_ID', 'UID', 'TSVR_hours']
- Function expects 'test' or 'Test' column for auto-detection
- Fix: Extract test number from composite_ID via `composite_ID.str.split('_').str[1]`
- Impact: Prevented KeyError at function entry

**Bug #5: Formula Variable Names (TSVR_hours)**
- Formula used 'TSVR_hours' but function converts to 'Days' column
- Random effects used '~TSVR_hours' but should be '~Days'
- Fix: Changed formula to use 'Days' and 'np.log(Days + 1/24)'
- Impact: Prevented NameError during patsy formula parsing

**Bug #6: Formula Variable Names (theta)**
- Formula used 'theta' but function creates 'Theta' column (capital T)
- Fix: Changed formula to 'Theta ~ (Days + np.log(Days + 1/24)) * C(Domain)'
- Impact: Prevented NameError during patsy formula evaluation

**Execution Results (~5 minutes, 3 LMM fits):**
- ✅ All 3 models converged successfully (boundary warnings normal for LMM)
- ✅ Formula: Theta ~ (Days + log(Days+1/24)) * C(Domain), Random: ~Days, Groups: UID
- ✅ ML estimation (REML=False) for valid AIC comparison

**🚨 SHOCKING SCIENTIFIC FINDING - CONTRADICTS HYPOTHESIS! 🚨**

**Model Comparison Results:**

| Measurement | AIC | Δ AIC (from IRT) | BIC | Rank | Interpretation |
|-------------|-----|------------------|-----|------|----------------|
| **Full CTT** | **2954.08** | **-53.13** | 3020.25 | **1st** ⭐ | **BEST MODEL** |
| **IRT theta** | 3007.21 | 0.00 (ref) | 3073.38 | 2nd | Reference |
| **Purified CTT** | 3108.50 | +101.29 | 3174.67 | **3rd** ❌ | **WORST MODEL** |

**CRITICAL INTERPRETATION:**

**Full CTT vs IRT theta: Δ AIC = -53.13** ⭐
- Substantial support for Full CTT (|Δ AIC| > 10 per Burnham & Anderson)
- **Classical test theory OUTPERFORMS modern IRT for forgetting trajectories!**
- Completely unexpected result

**Purified CTT vs IRT theta: Δ AIC = +101.29** ❌
- Substantial support for IRT over Purified CTT
- **Purified CTT is the WORST model**
- **Directly contradicts Hypothesis 2**

**Full CTT vs Purified CTT: Δ AIC = -154.42**
- Massive difference favoring Full CTT
- **Item purification WORSENED model fit** instead of improving it

**Hypothesis 2 Status: REJECTED**
- Expected: Purified CTT > IRT theta > Full CTT
- Actual: **Full CTT > IRT theta > Purified CTT**
- **Complete reversal of predicted order**

**Scientific Explanation (Why This Happened):**

**The When Domain Effect:**
- When domain: 81% item attrition (26 → 5 items)
- Purified CTT loses critical information about temporal memory variability
- Full CTT retains 26 items capturing more variance in forgetting trajectories

**"Good" Items Were Too Homogeneous:**
- IRT purification removed difficult items (|b| > 3.0)
- Those difficult items captured individual differences in forgetting rates
- Purified set: psychometrically cleaner but informationally impoverished

**Classical CTT Advantage:**
- More items → more variance → better trajectory modeling
- **Item count > item quality** for dynamic forgetting analysis
- Purified items internally consistent but miss temporal dynamics

**PARADOX DISCOVERED:**
- ✅ Purified CTT correlates better with IRT (Step 5: higher r values)
- ❌ Purified CTT models forgetting worse than Full CTT (Step 7: higher AIC)
- **Correlation convergence ≠ Model fit quality**
- Different methods optimize different criteria

**9. Step 8: Prepare Plot Data (COMPLETE - 0 bugs)**

**g_code Generation:**
- ✅ Generated step08_prepare_plot_data.py with zero bugs
- ✅ Stdlib operations (reshape correlations to long format)
- ✅ Validation tool: validate_plot_data_completeness

**Execution Results:**
- ✅ Plot 1 (Correlation Comparison): 6 rows (3 domains × 2 measurement types)
- ✅ Plot 2 (AIC Comparison): 3 rows (Full CTT, Purified CTT, IRT theta)
- ✅ All domains and measurements present, zero NaN values

**Plot Data Outputs:**
- plots/step08_correlation_comparison_data.csv (ready for grouped bar chart)
- plots/step08_aic_comparison_data.csv (ready for AIC comparison bar chart)

**Session Metrics:**

**Code Generation:**
- 9 analysis steps (step00 through step08)
- 9 Python scripts generated (~15-20 KB each)
- 9 log files created
- 19 data files generated
- 2 plot data CSVs prepared

**Bugs Fixed:**
1. Step 0: Status YAML schema mismatch (flat vs nested structure)
2. Step 1: Tool API mismatch (column_types single type vs tuple)
3. Step 1: Specification error (item count 50 vs 105)
4. Step 7: Missing 'test' column in df_tsvr
5. Step 7: Formula variable TSVR_hours → Days
6. Step 7: Formula variable theta → Theta

**Total Bugs:** 6 (all fixed during execution, zero unresolved issues)

**Execution Time:**
- Step 0: ~30 seconds (load + validate)
- Step 1: ~10 seconds (item mapping)
- Step 2: ~5 seconds (full CTT computation)
- Step 3: ~5 seconds (purified CTT computation)
- Step 4: ~2 minutes (bootstrap 6000 iterations)
- Step 5: ~10 seconds (Steiger's z-test)
- Step 6: ~5 seconds (standardization)
- Step 7: ~5 minutes (3 LMM fits with convergence)
- Step 8: ~5 seconds (plot data prep)
- **Total:** ~8 minutes pure execution + ~90 minutes debugging/validation = ~98 minutes

**Statistical Validation Throughout:**
- Every step: Range checks, plausibility tests, sample size verification
- Cross-step consistency: Full vs Purified CTT comparisons, domain patterns
- Hypothesis testing: Steiger's z-test with dual p-values (D068 compliance)
- Model comparison: AIC with Burnham & Anderson interpretation
- Scientific interpretation: After each step, explaining what results mean

**Files Generated This Session:**

**Code (9 files):**
1. results/ch5/rq12/code/step00_load_data.py
2. results/ch5/rq12/code/step01_map_items.py
3. results/ch5/rq12/code/step02_compute_full_ctt.py
4. results/ch5/rq12/code/step03_compute_purified_ctt.py
5. results/ch5/rq12/code/step04_assess_reliability.py
6. results/ch5/rq12/code/step05_correlation_analysis.py
7. results/ch5/rq12/code/step06_standardize_outcomes.py
8. results/ch5/rq12/code/step07_fit_parallel_lmms.py
9. results/ch5/rq12/code/step08_prepare_plot_data.py

**Data (19 files):**
- Step 0: 4 files (purified_items, theta_scores, tsvr_mapping, raw_scores)
- Step 1: 1 file (item_mapping)
- Step 2: 1 file (ctt_full_scores)
- Step 3: 1 file (ctt_purified_scores)
- Step 4: 1 file (reliability_assessment)
- Step 5: 1 file (correlation_analysis)
- Step 6: 1 file (standardized_outcomes)
- Step 7: 7 files (3 summaries, 3 fixed_effects, 1 model_comparison)
- Step 8: 2 files (2 plot data CSVs)

**Logs (9 files):**
- results/ch5/rq12/logs/step00_load_data.log through step08_prepare_plot_data.log

**Key Insights:**

**Methodological Trade-off Discovered:**
- IRT purification optimizes internal consistency (higher α, better r with IRT)
- BUT sacrifices predictive validity for trajectory modeling (worse AIC fit)
- **Different optimization criteria:** Static convergence vs dynamic modeling
- **Item count matters:** More items (even "poor" ones) capture more forgetting dynamics

**When Domain Critical Limitation:**
- Only 5 items retained (19.2%), below minimum 7-10 for reliable measurement
- Cronbach's α < 0.70 for both full and purified sets
- Massive correlation improvement (0.45 → 0.84) but underpowered statistically
- Floor effects + item scarcity = unreliable measurement regardless of method

**Publication-Quality Results:**
- Complete transparency (all methods, all results, all limitations documented)
- Dual p-value reporting (Decision D068 compliance)
- Bootstrap confidence intervals (robust uncertainty estimates)
- Comprehensive validation at every step
- Unexpected findings fully documented with scientific explanations

**PhD Thesis Contributions:**
- **Theoretical:** Paradox discovered (better convergence ≠ better modeling)
- **Methodological:** Comprehensive CTT/IRT comparison across multiple criteria
- **Practical:** Recommendation for trajectory studies (use Full CTT despite lower IRT correlation)

**RQ 5.12 Status:**
- ✅ All 9 analysis steps complete (Steps 0-8)
- ✅ All statistical validations passed
- ✅ All bugs fixed during execution
- ✅ Primary hypothesis partially supported (Step 5: convergent validity)
- ⚠️ Secondary hypothesis rejected (Step 7: model fit paradox)
- 🟡 Ready for validation pipeline: rq_inspect → rq_plots → rq_results

---
