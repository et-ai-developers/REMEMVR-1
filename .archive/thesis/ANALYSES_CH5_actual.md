# PART 1: CHAPTER 5 - THE TRAJECTORY OF EPISODIC FORGETTING
# AS-BUILT DOCUMENTATION (Generated 2025-11-30)

**Purpose:** This file documents what was ACTUALLY implemented in RQs 5.1-5.13, extracted from the results folders. This serves as an "as-built" specification to compare against the original ANALYSES_CH5.md planning document.

**Method:** 13 parallel context_finder agents extracted documentation from results/ch5/5.X.X/ folders (docs/, data/, results/). Agents were forbidden from reading the original ANALYSES_CH5.md to ensure independence.

**Note:** RQs 5.14-5.15 not yet executed, so not included here.

---

## TABLE OF CONTENTS

| RQ | Title | Status |
|---|---|---|
| 5.1 | Domain-Specific Forgetting Trajectories | Complete |
| 5.2 | Differential Consolidation Across Memory Domains | Complete |
| 5.3 | Paradigm-Specific Forgetting Trajectories | Complete |
| 5.4 | Linear Trend in Forgetting Rate Across Paradigms | Complete |
| 5.5 | Schema Congruence Effects on Forgetting | Complete |
| 5.6 | Congruent Items and Early Consolidation | Complete |
| 5.7 | Functional Form of Forgetting Trajectories | Complete |
| 5.8 | Evidence for Two-Phase Forgetting | Complete |
| 5.9 | Age Effects on Baseline and Forgetting Rate | Complete |
| 5.10 | Domain-Specific Age Effects on Forgetting | Complete |
| 5.11 | IRT-CTT Convergent Validity | Complete |
| 5.12 | Purified IRT Item Set Effects on CTT | Complete |
| 5.13 | Between-Person Variance in Forgetting Rates | Complete |

---

### RQ5.1: Domain-Specific Forgetting Trajectories (What/Where/When)

**Research Question:** Are there domain-specific differences in the rate and pattern of episodic forgetting over 6 days? (from 1_concept.md line 12)

**Hypothesis:** Object identity (What) may be more resilient than spatial (Where) or temporal (When) memory, consistent with dual-process theories suggesting familiarity-based information is less hippocampus-dependent than contextual details. (from 1_concept.md lines 42-43)

**Data Required:**
- Source: data/cache/dfData.csv (derived from master.xlsx)
- Columns: UID, TEST, TSVR (actual hours since encoding), TQ_* (all VR test items)
- Domains: What (tag pattern `*-N-*`), Where (patterns `*-L-*`, `*-U-*`, `*-D-*`), When (`*-O-*`)
- Dichotomization: TQ_* values < 1 → 0, ≥ 1 → 1
- Participants: All 100, all 4 test sessions (T1-T4; 400 composite observations)
(from 2_plan.md Step 0, lines 34-47)

**Analysis Specification:**
1. Extract VR data from dfData.csv, dichotomize TQ_* values, create Q-matrix for 3-dimensional IRT
2. Run Pass 1 IRT (3-factor Graded Response Model, correlated factors) on all 105 items
3. Apply item purification: retain items with discrimination a ≥ 0.4 AND difficulty |b| ≤ 3.0
4. Run Pass 2 IRT calibration on 70 purified items (Decision D039)
5. Fit 5 candidate LMM models: Linear, Quadratic, Logarithmic, Lin+Log, Quad+Log (all with Domain × Time interactions)
6. Use TSVR (actual hours) as time variable, not nominal days (Decision D070)
7. Select best model via AIC; compute Akaike weights
8. Post-hoc contrasts: Where-What, When-What comparisons with Bonferroni correction (α = 0.0167 for 3 tests)
(from 2_plan.md Steps 1-8, lines 101-113)

**Expected Output:**
- IRT parameters: theta ability scores, discrimination (a), difficulty (b) for 70 purified items
- LMM results: fixed effects for intercept, domain main effects, log(TSVR) main effect, and Domain × log(TSVR) interactions
- Post-hoc contrasts: pairwise p-values (uncorrected and Bonferroni-corrected) per Decision D068
- Trajectory plots: observed means + fitted curves for theta scale and probability scale per Decision D069
(from 4_analysis.yaml metadata, lines 11-20 and 3_tools.yaml structure)

**Success Criteria:**
- IRT convergence achieved for both Pass 1 and Pass 2
- Minimum item retention rate of 50% after purification
- All 100 participants present across all 4 test sessions (0% missing data)
- LMM model selection via AIC produces valid Akaike weights
- Post-hoc contrasts report both corrected and uncorrected p-values
(from 2_plan.md validation criteria lines 91-92 and summary.md quality metrics)

**Final Results:**
Best-fitting trajectory model: Logarithmic pattern (AIC weight 62%). Key findings: All three domains show monotonic decline consistent with forgetting curves. Significant Domain × log(Days) interaction: When memory declines significantly faster than What memory (β = -0.415, p < .001; Bonferroni-corrected). Where memory shows minimal difference from What (β = 0.037, p = .722). Memory ability (theta) ranges: What [0.69 to -0.34 SD], Where [0.67 to -0.48 SD], When [0.20 to -0.11 SD] from Day 0 to Day 6. (from summary.md lines 72-80, 136-138)

---

### RQ5.2: Differential Consolidation Across Memory Domains

**Research Question:** Do memory domains (What/Where/When) show different rates of forgetting during the early consolidation window (Day 0→1) versus later decay (Day 1→6)? (from 1_concept.md line 11-12)

**Hypothesis:** Sleep-dependent consolidation (Day 0→1, including one night's sleep) may benefit spatial memory (Where) more than semantic (What), based on hippocampal replay theories. Secondary hypothesis: The 3-way interaction (Days_within × Segment × Domain) will be significant, indicating domain-specific consolidation effects. (from 1_concept.md lines 47-58)

**Data Required:** Theta scores from RQ 5.1 (results/ch5/rq1/data/step04_lmm_input.csv with columns: composite_ID, UID, test, TSVR_hours, domain, theta, se; ~1200 observations across 4 test sessions, 3 domains per 100 participants); item parameters from RQ 5.1 (step03_item_parameters.csv) for probability scale conversion. (from 2_plan.md lines 39-45, 414-417)

**Analysis Specification:**
1. Data preparation: Add Segment variable (Early: tests 0-1; Late: tests 3-6) and Days_within variable (time since segment start) to RQ 5.1 data
2. Piecewise LMM with 3-way interaction: `theta ~ Days_within × Segment × domain` with random intercepts and slopes by UID, REML=False
3. Extract 6 segment-domain slopes via linear combinations of fixed effects
4. Planned contrasts: 6 contrasts (3 domains × 2 segment comparisons) with Bonferroni correction (alpha=0.05/6=0.0083)
5. Consolidation benefit indices: Early slope - Late slope per domain
6. Dual-scale trajectory plot data preparation: theta scale + probability scale (Decision D069)
(from 2_plan.md Steps 0-5, lines 34-556)

**Expected Output:** Fitted piecewise LMM model (data/step01_piecewise_lmm_model.pkl); segment-domain slopes table (results/step02_segment_domain_slopes.csv); planned contrasts with dual p-values (results/step03_planned_contrasts.csv); consolidation benefit indices (results/step04_consolidation_benefit.csv); theta and probability-scale plot data (plots/step05_piecewise_theta_data.csv, plots/step05_piecewise_probability_data.csv). (from 4_analysis.yaml lines 114-543)

**Success Criteria:** Model convergence successful; all 6 segment-domain slopes computed with valid SEs and CIs; 6 planned contrasts with both uncorrected and Bonferroni-corrected p-values; consolidation benefit ranks assigned per domain; 12 rows in plot data (3 domains × 4 tests) with no NaN values. (from 2_plan.md lines 164-167, 241-271, 334-354, 516-547)

**Final Results:** Hypothesis NOT SUPPORTED. No planned contrasts significant after Bonferroni correction (alpha=0.0083). When domain showed least early forgetting (consolidation benefit rank 1, slope -0.208/day Early vs -0.013/day Late), contrary to prediction that Where would show greatest consolidation benefit. All domains show characteristic two-phase forgetting: steep early decline (What: -0.507/day, Where: -0.456/day, When: -0.208/day) followed by slower late decay. Domain-specific effects negligible (effect sizes f²<0.005). Probability scale shows practical impact: When remains at ~47% correct (above chance) while What and Where approach ~40-42% (near chance) by Day 6. (from results/summary.md lines 176-210)

---

### RQ5.3: Paradigm-Specific Forgetting Trajectories

**Research Question:** Are there paradigm-specific differences in the rate and pattern of episodic forgetting over 6 days? (from 1_concept.md line 12)

**Hypothesis:** Free Recall will show steepest forgetting (requires self-initiated retrieval), followed by Cued Recall (partial support), with Recognition showing most shallow decline (familiarity-based, least demanding). This reflects an ordered retrieval support gradient. (from 1_concept.md line 45)

**Data Required:**
- RQ 5.1 outputs: results/ch5/rq1/data/step00_irt_input.csv (dichotomized VR item scores)
- RQ 5.1 outputs: results/ch5/rq1/data/step00_tsvr_mapping.csv (TSVR time variable)
- Filter to Item paradigms only: IFR (Item Free Recall), ICR (Item Cued Recall), IRE (Item Recognition)
- Exclude RFR (Room Free Recall) and TCR (Task Cued Recall) due to response format differences
- 100 participants × 4 test sessions × 3 paradigms = 1200 observations
- Time variable: TSVR (actual hours since encoding, range 1-246 hours) NOT nominal days
(from 2_plan.md Step 0, lines 36-54)

**Analysis Specification:**
1. **Step 0:** Filter data to Item paradigms (IFR/ICR/IRE), create paradigm-based Q-matrix
2. **Step 1:** IRT Pass 1 calibration (Graded Response Model, 2 categories, correlated factors)
3. **Step 2:** Item purification per Decision D039 (discrimination a ≥ 0.4, difficulty |b| ≤ 3.0)
4. **Step 3:** IRT Pass 2 calibration (purified items only) - extract final theta scores
5. **Step 4:** Merge theta with TSVR, reshape to long format (paradigm as factor)
6. **Step 5:** Fit 5 candidate LMMs (Linear, Quadratic, Log, Lin+Log, Quad+Log), select best via AIC
7. **Step 6:** Post-hoc contrasts with dual p-values (uncorrected + Bonferroni alpha=0.0167)
8. **Step 7:** Compute effect sizes (Cohen's d at Day 6) and prepare trajectory plot data
(from 2_plan.md, lines 29-744)

**Expected Output:**
- data/step03_theta_scores.csv: 400 rows × 7 columns (composite_ID, theta/SE per paradigm)
- results/step05_model_comparison.csv: 5 models × 7 columns (AIC/BIC/likelihood comparisons)
- results/step05_lmm_model_summary.txt: Best model fixed effects + random effects
- results/step06_post_hoc_contrasts.csv: Pairwise contrasts with dual p-values
- results/step06_effect_sizes.csv: Cohen's d comparisons
- plots/step07_trajectory_theta_data.csv: Model predictions + observed means (theta scale)
- plots/step07_trajectory_probability_data.csv: Model predictions + observed means (probability scale)
(from 2_plan.md Step 5-7)

**Success Criteria:**
- IRT convergence successful (2-pass with item purification)
- 45/72 items retained post-purification (40-80 item range expected) - ACHIEVED: 62.5% retention
- All 5 LMM models converge with valid AIC comparisons
- Log model selected as best (Decision D070 TSVR time variable enables log detection)
- All validation tools pass (convergence, parameter ranges, residuals)
(from 2_plan.md lines 849-902)

**Final Results:**
Paradigm-specific forgetting trajectories analyzed across 100 participants (1200 observations). Log model decisively superior (AIC weight 0.9999) showing logarithmic forgetting for all paradigms. Recognition shows HIGHEST baseline ability (θ = 0.7, +0.210 vs Free Recall, p = .006 Bonferroni-corrected) BUT FASTEST forgetting trajectory (log_Days × Recognition β = -0.127, p = .013 uncorrected, n.s. Bonferroni). Hypothesis PARTIALLY REJECTED: Baseline retrieval support advantage confirmed, but forgetting rate advantage CONTRADICTED - Recognition declines steeper than Free Recall despite maximal retrieval support. Primary interpretation: Retrieval support affects baseline performance (encoding-retrieval match per Transfer-Appropriate Processing theory) but NOT consolidation durability; familiarity-based Recognition may decay faster than recollection-based Free Recall over 10-day interval. (from results/summary.md lines 1-123)

---

### RQ5.4: Linear Trend in Forgetting Rate Across Paradigms

**Research Question:** Does forgetting rate decrease monotonically from Free Recall → Cued Recall → Recognition, consistent with an ordered retrieval support gradient? (from 1_concept.md lines 11-12)

**Hypothesis:** Forgetting rate (slope magnitude) follows ordered trend: Free > Cued > Recognition. More negative slope = faster forgetting. Linear trend contrast will be significant at Bonferroni-corrected alpha = 0.0033. Expected effect pattern: Slope estimates (Day 3): Free ~ -0.08, Cued ~ -0.06, Recognition ~ -0.04. (from 1_concept.md lines 42-54)

**Data Required:** DERIVED from RQ 5.3 outputs: step05_lmm_fitted_model.pkl (Log model, best AIC=2346.60) and step04_lmm_input.csv (N=100 participants × 4 tests × 3 paradigms = 1200 observations, long format with TSVR_hours, TSVR_hours_log, paradigm, theta columns). (from 2_plan.md lines 32-72, 1_concept.md lines 128-143)

**Analysis Specification:**
1. Load RQ 5.3 LMM model and theta data (Step 0)
2. Extract paradigm-specific marginal means at Day 3 midpoint using model.predict() (Step 1)
3. Compute linear trend contrast within RQ 5.3 LMM using weights Free=-1, Cued=0, Recognition=+1; report dual p-values (uncorrected and Bonferroni-corrected α=0.0033) per Decision D068 (Step 2)
4. Prepare plot source CSV with paradigm means, confidence intervals, and fitted linear trend line (Step 3) (from 2_plan.md lines 29-357)

**Expected Output:** data/step01_marginal_means.csv (3 paradigms with marginal_mean, SE, CI), results/step02_linear_trend_contrast.csv (estimate, SE, z, dual p-values, CI), plots/step03_paradigm_forgetting_rates_data.csv (plot source with trend_line column), plots/step03_contrast_annotation.txt. (from 2_plan.md lines 136-392)

**Success Criteria:** All 4 steps produce outputs with correct structure; marginal means in [-3,3], SE>0, p-values in [0,1]; Bonferroni p ≥ uncorrected p; no NaN values; all 3 paradigms present; CI bounds logical. (from 2_plan.md lines 79-177, 4_analysis.yaml lines 111-334)

**Final Results:** HYPOTHESIS REJECTED. Observed forgetting slopes opposite to prediction: Free Recall slowest (-0.470) → Cued Recall intermediate (-0.520) → Recognition fastest (-0.597). Linear trend contrast = -0.127 (uncorrected p=0.013, Bonferroni p=0.200), indicating forgetting INCREASES with retrieval support, contradicting retrieval support gradient theory. Day 3 marginal means still show Recognition highest (θ=0.083), revealing disconnect between absolute performance level and forgetting rate. Pattern suggests encoding-retrieval trade-off rather than simple retrieval support effect. (from results/summary.md lines 49-137)

---

### RQ5.5: Schema Congruence Effects on Forgetting

**Research Question:** Does schema congruence (common, congruent, incongruent) affect the trajectory of episodic forgetting over 6 days? (from 1_concept.md line 12)

**Hypothesis:** Congruent items (schema-consistent) will show slower forgetting than incongruent items (schema-violating), due to schema-based consolidation processes. Common items (schema-neutral) will fall between congruent and incongruent in forgetting rate. (from 1_concept.md lines 46-52)

**Data Required:**
- RQ 5.1 outputs: `results/ch5/rq1/data/step00_irt_input.csv` (raw VR item responses, ~400 rows)
- RQ 5.1 TSVR mapping: `results/ch5/rq1/data/step00_tsvr_mapping.csv` (time variable, ~400 rows)
- Q-matrix recoding by congruence: items i1-i2 (common), i3-i4 (congruent), i5-i6 (incongruent) (from 2_plan.md lines 103-109)

**Analysis Specification:** 8-step pipeline per 2_plan.md:
1. **Step 00:** Extract interactive paradigm items (IFR, ICR, IRE only), create congruence Q-matrix with 3 dimensions
2. **Step 01:** IRT Pass 1 calibration (3-dimensional GRM, correlated factors on all items)
3. **Step 02:** Item purification (Decision D039: exclude items with |b| > 3.0 OR a < 0.4)
4. **Step 03:** IRT Pass 2 on purified items (final publication-quality theta scores)
5. **Step 04:** Merge theta scores with TSVR (Decision D070: actual hours, not days), reshape to long format
6. **Step 05:** Fit 5 candidate LMM models with Congruence × Time interactions, select by AIC
7. **Step 06:** Post-hoc pairwise contrasts with dual p-value reporting (Decision D068), effect sizes
8. **Step 07:** Prepare trajectory plot data, create theta-scale and probability-scale visualizations (Decision D069)

**Expected Output:**
- `data/step03_theta_scores.csv` - Final IRT ability estimates by congruence dimension (7 columns, ~400 rows)
- `results/step05_model_comparison.csv` - AIC/BIC comparison for 5 LMM candidates
- `results/step05_lmm_model_summary.txt` - Best model fixed/random effects
- `results/step06_post_hoc_contrasts.csv` - 3 pairwise slope contrasts with uncorrected + Bonferroni p-values
- `results/step06_effect_sizes.csv` - Cohen's f² effect sizes (3 rows)
- `plots/step07_trajectory_*.csv` - Aggregated plot data (12 rows × 3 congruence categories)

**Success Criteria:** (from 2_plan.md validation sections)
- All 8 steps complete with passing validation checks (IRT convergence, LMM convergence, no NaN values)
- 50-90 items retained after purification (40-70% retention expected)
- Best LMM model converges with AIC clear winner (log model predicted to dominate)
- Interaction terms extracted with both uncorrected and Bonferroni-corrected p-values
- 12 trajectory points created (3 congruence × 4 test sessions)

**Final Results:** Hypothesis NOT SUPPORTED. (from summary.md lines 198-206)
- NO significant Congruence × Time interactions (all p > .44, f² < 0.001)
- Schema congruence does NOT significantly affect episodic forgetting trajectories in VR
- All three categories showed similar baseline performance (60-62% correct, T1) and forgetting rates (decline to ~40% by T4)
- Logarithmic time model selected (AIC = 2652.57, 22-point advantage), confirming classic Ebbinghaus forgetting curve
- Strong main effect of Time (β = -0.193, p < .001), zero effect of Congruence factor

---

### RQ5.6: Congruent Items and Early Consolidation

**Research Question:** Is the schema congruence effect on forgetting driven by differential consolidation (Day 0-1) or later decay (Day 1-6)? (from 1_concept.md, line 12)

**Hypothesis:** Congruent items will show less forgetting during the consolidation window (Day 0-1) compared to incongruent items, as schema-based memory benefits from sleep-dependent consolidation. The congruence effect may be less pronounced during later decay (Day 1-6). (from 1_concept.md, lines 47-48)

**Data Required:**
- DERIVED: Theta scores from RQ 5.5 (results/ch5/rq5/data/step03_theta_scores.csv, 400 observations × 7 columns: composite_ID, theta_common, theta_congruent, theta_incongruent, se_common, se_congruent, se_incongruent)
- Input transformation: Reshape to long format with Congruence factor variable (Common/Congruent/Incongruent) and create piecewise time segments
- Early segment: Tests T1-T2 (Days 0-1, consolidation window with one night's sleep)
- Late segment: Tests T3-T4 (Days 1-6, post-consolidation decay)
(from 2_plan.md lines 36-56 and 3_tools.yaml lines 44-60)

**Analysis Specification:**
1. Extract theta scores from RQ 5.5 and validate structure (400 rows, no NaN in theta columns)
2. Reshape to long format with Congruence categories and Segment assignments
3. Create Days_within variable (time centered at 0 for each segment start)
4. Fit piecewise LMM: `theta ~ Days_within × Segment × Congruence + (1 + Days_within | UID)` with treatment coding (Common reference, Early reference)
5. Extract segment-specific slopes (Common/Congruent/Incongruent for each Early and Late segment)
6. Test primary hypothesis: 3-way interaction (Days_within × Segment[Late] × Congruence[Congruent]) significance with dual p-value reporting (uncorrected α=0.05, Bonferroni α=0.0033 with 15-test family)
7. Validate LMM assumptions: residual normality (Shapiro-Wilk), homoscedasticity (Levene test), random effects normality, multicollinearity (VIF)
(from 2_plan.md lines 35-140 and 4_analysis.yaml steps 1-6)

**Expected Output:**
- `data/step00_theta_scores_from_rq5.csv` (cached theta scores, 400 × 7)
- `results/step02_lmm_fit_piecewise.pickle` (fitted piecewise LMM object)
- `results/step03_slopes_by_segment.csv` (Early/Late slopes with 95% CIs for Common/Congruent/Incongruent)
- `results/step04_hypothesis_test_3way.csv` (primary 3-way interaction coefficient, SE, z-value, uncorrected p, Bonferroni p)
- `plots/piecewise_trajectory.png` (two-panel plot: Early segment | Late segment with observed means and model predictions)
- `plots/step05_residual_diagnostics.png` (four-panel: Q-Q plot, residuals vs fitted, random effects Q-Q, residuals histogram)
(from 4_analysis.yaml output_files sections and results/summary.md lines 133-135)

**Success Criteria:**
- LMM convergence successful (no singular fit warnings, gradient norm < 0.01)
- Primary 3-way interaction test interpretable (coefficient, SE, z-value calculated for Days_within × Segment[Late] × Congruence[Congruent] and Days_within × Segment[Late] × Congruence[Incongruent])
- Assumption validation: Shapiro-Wilk p > 0.05 (normality), Levene p > 0.05 (homoscedasticity acceptable if p < 0.05 still interpretable with homoscedasticity note)
- Sensitivity analyses completed: Compare piecewise AIC to continuous time models (Linear, Log, Linear+Log); document model fit ranking
(from 1_concept.md lines 184-232 and results/summary.md lines 30-80)

**Final Results:**
The piecewise LMM revealed no evidence for differential consolidation benefit (3-way interaction Days_within × Segment[Late] × Congruence[Congruent]: β = -0.018, p = .938). All congruence types showed similar forgetting rates within each segment. Sensitivity analysis found that continuous time models (Linear+Log) fit substantially better than piecewise (ΔAIC = -91 units), suggesting forgetting follows smooth trajectory rather than discrete consolidation/decay phases. Conclusion: Schema-based consolidation effects not detectable in this VR paradigm or consolidation window assumptions unjustified. (from results/summary.md lines 3, 176-177, 208-214)

---

### RQ5.7: Functional Form of Forgetting Trajectories

**Research Question:** Which functional form best describes episodic forgetting trajectories across a 6-day retention interval?

**Hypothesis:** Exploratory (no directional prediction). Compared 5 candidate models via AIC with Akaike weight interpretation.

**Data Required:**
- IRT input from RQ 5.1: step00_irt_input.csv (400 observations, all What/Where/When items)
- TSVR time variable: step00a_tsvr_data.csv (actual hours since encoding)

**Analysis Specification:** 7 steps - 2-pass IRT calibration (single omnibus "All" factor with purification), item purification (Decision D039: a ≥ 0.4, |b| ≤ 3.0), data preparation with time transformations, 5 candidate LMM models, AIC-based model selection, dual-scale plot preparation.

**Success Criteria:** IRT convergence (theta [-4,4], SE [0.1,1.5]), 30-70% item retention, all 5 LMM models converge, Akaike weights sum to 1.0±0.01, best model weight >0.30.

**Final Results:** **Logarithmic model best fit** (AIC = 873.71, weight = 0.482 = 48.2% probability). Lin+Log competitive (delta AIC = 0.84, weight = 0.317). Linear model rejected (delta AIC = 31.83). Results show Ebbinghaus-style forgetting: steep early decline (0.55 SD Day 0→1), asymptotic leveling (0.25 SD Day 3→6). Probability scale: recall 68% → 38% over 6 days. **Known issues:** Pass 1 IRT didn't converge (flagged "potentially unreliable"), temporal items disproportionately excluded (27/37 purified items were -O- items).

---

### RQ5.8: Evidence for Two-Phase Forgetting (Rapid then Slow)

**Research Question:** Do episodic memory data support a two-phase model with rapid initial decline (Day 0-1) followed by slower decay (Day 1-6)? (from 1_concept.md lines 11-12)

**Hypothesis:** Forgetting exhibits two distinct phases with rapid initial decline (Day 0-1, pre-consolidation) followed by slower decay (Day 1-6, post-consolidation), evidenced by convergence of three tests: (1) significant quadratic term (positive curvature = deceleration, p < 0.003333 Bonferroni-corrected), (2) piecewise vs continuous model AIC comparison (ΔAIC < -2 favors piecewise), (3) Late/Early slope ratio < 0.5 (from 1_concept.md lines 44-45)

**Data Required:** IRT-derived theta scores from RQ 5.7 (collapsed across What/Where/When domains), TSVR mapping (actual hours since encoding per Decision D070), and best continuous model from RQ 5.7 for AIC comparison (from 2_plan.md Step 0, lines 83-109)

**Analysis Specification:** Seven-step LMM-only analysis (from 2_plan.md):
0. Load theta scores and best continuous model from RQ 5.7, collapse across domains, merge with TSVR mapping
1. Create time transformations: quadratic variables (Time, Time²), log variable, piecewise segments (Early 0-48h / Late 48-240h), Days_within (recentered within segment)
2. Fit Theta ~ Time + Time² + (Time | UID); test if Time² coefficient significant (p < 0.003333)
3. Fit Theta ~ Days_within × Segment + (Days_within | UID); compare AIC to best continuous model (ΔAIC < -2 favors piecewise)
4. Validate LMM assumptions for both models (6 checks: residual normality, homoscedasticity, random effects normality, autocorrelation, linearity, outliers)
5. Extract Early and Late segment slopes from piecewise model, compute Late/Early ratio (expect < 0.5)
6. Prepare plot data: aggregate observed means + quadratic predictions + piecewise predictions for two-panel visualization (from 2_plan.md lines 74-108)

**Expected Output:** Quadratic model summary (Test 1), piecewise model summary (Test 2), assumption validation report (Test 3), slope comparison with ratio (Test 4), plot data CSV combining observed + two model predictions (from 3_tools.yaml and 4_analysis.yaml)

**Success Criteria:** Tests 1 and 3 support two-phase forgetting (Time² significant p < 0.001, slope ratio 0.161 << 0.5), convergence documented or fallback used transparently (from summary.md lines 30-31)

**Final Results:** PARTIALLY SUPPORTED hypothesis. Test 1: Quadratic term significant (Time² p < 0.001, coefficient = 0.000054), supporting deceleration. Test 2: AIC favors continuous model (ΔAIC = +5.03 > +2 threshold), contradicting piecewise prediction. Test 3: Slope ratio = 0.161 << 0.5 threshold with highly significant interaction (p < 0.000002), strongly supporting two-phase pattern. Conclusion: Forgetting exhibits two-phase dynamics (rapid early: -0.432/day vs slow late: -0.070/day, 6.2x difference), but transition is gradual (continuous deceleration) rather than sharp inflection at 48 hours (from summary.md lines 1-31, 54, 88, 105, 134-136).

---

### RQ5.9: Age Effects on Baseline and Forgetting Rate

**Research Question:** Do older adults show lower baseline episodic memory (intercept) and/or faster forgetting (steeper slope) compared to younger adults? (from 1_concept.md, line 12)

**Hypothesis:** Age will negatively predict both intercept (baseline memory at Day 0) and slope (forgetting rate across 6 days), consistent with hippocampal aging effects. Primary: Age_c on intercept significant (expected β < 0, p < 0.0167). Secondary: Age_c × log(Time+1) interaction significant; Age_c × Time interaction may be weaker after Bonferroni correction (from 1_concept.md, lines 50-64)

**Data Required:** IRT-derived theta scores from RQ 5.7 "All" factor analysis (composite What/Where/When domains); Age variable from data/cache/dfData.csv; TSVR mapping (actual hours since encoding) from RQ 5.7 Step 0. Input: 400 observations (100 participants × 4 test sessions) with columns: composite_ID, UID, TEST, TSVR_hours, theta, se_all, age (from 2_plan.md Steps 0-1, lines 37-90)

**Analysis Specification:**
1. Extract and merge theta scores (RQ 5.7) with Age and TSVR mapping (Step 0)
2. Grand-mean center Age (Age_c = age - mean(age)); create Time and Time_log transformations (Step 1)
3. Fit LMM: Theta ~ (Time + Time_log) × Age_c + (Time | UID) using Lin+Log functional form with REML=False (Step 2)
4. Extract age effects: Age_c main effect (baseline memory), Time:Age_c and Time_log:Age_c interactions (forgetting rates); apply Bonferroni correction α = 0.0167 for 3 tests (Step 3)
5. Compute effect size: Predict theta at Day 6 for average age vs. age+1SD scenarios; report decline in theta units and percentage (Step 4)
6. Create age tertiles (Young/Middle/Older) for visualization; aggregate observed means and model predictions per tertile × timepoint (Step 5)
(from 2_plan.md, lines 29-570)

**Expected Output:**
- data/step00_lmm_input_raw.csv (400 rows, 7 columns: composite_ID, UID, TEST, TSVR_hours, theta, se_all, age)
- data/step01_lmm_input_prepared.csv (400 rows, 10 columns: + Age_c, Time, Time_log)
- data/step02_lmm_model.pkl (fitted MixedLM model), results/step02_lmm_summary.txt (human-readable), data/step02_fixed_effects.csv (6 rows × 4 columns: term, coef, se, z, p)
- data/step03_age_effects.csv (3 rows: Age_c main effect + 2 interactions with dual p-values per Decision D068)
- data/step04_effect_size.csv (2 rows: predictions for average age vs. age+1SD at Day 6)
- plots/step05_age_tertile_plot_data.csv (12 rows: 3 tertiles × 4 timepoints with observed/predicted theta)
(from 2_plan.md, lines 78-91, 160-168, 249-269, 349-362, 435-442, 520-531)

**Success Criteria:**
- Model converges successfully; no NaN coefficients
- Fixed effects table includes all 6 terms (Intercept, Time, Time_log, Age_c, Time:Age_c, Time_log:Age_c)
- Random effects variances positive (intercept > 0, slope ≥ 0, residual > 0)
- All validation checks pass: no missing data post-merge, Age_c mean ≈ 0, LMM assumptions satisfied (normality, homoscedasticity), convergence diagnostics clean
- Plot data complete: all 3 tertiles at all 4 timepoints (12 rows total), ci_upper > ci_lower
(from 2_plan.md, lines 93-130, 170-204, 271-310, 365-399, 451-485, 533-569)

**Final Results:** Hypothesis NOT SUPPORTED. Age effects on forgetting rate were near-zero and in unexpected direction (positive, suggesting older adults forget slower - opposite to dual deficit hypothesis). Main effect: Age_c β = -0.012 (p = 0.182 Bonferroni), marginal baseline disadvantage for older adults but trivial effect size. Slope interactions: Time:Age_c β = 0.000015 (p = 1.000); Time_log:Age_c β = 0.001 (p = 1.000) - both non-significant. Effect size at Day 6: 1 SD age increase (~14.5 years) predicts only 0.10 theta unit decline (~20% relative). Practice effects confound identified as most plausible explanation for wrong-direction slope interactions. Null findings suggest VR's contextual richness may equalize forgetting trajectories across ages 20-70, or healthy older adults (selected sample) show comparable consolidation to younger adults. (from results/summary.md, lines 37-85, 146-156)

---

### RQ5.10: Domain-Specific Age Effects on Forgetting

**Research Question:** Does the effect of age on forgetting rate vary by memory domain (What, Where, When)? (from 1_concept.md line 12)

**Hypothesis:** Age x Time effects will be strongest for spatial (Where) and temporal (When) domains, which rely more heavily on hippocampal binding than object identity (What). This predicts a significant 3-way Age x Domain x Time interaction. (from 1_concept.md lines 45-46)

**Data Required:**
- IRT theta scores (1200 rows: 100 participants × 4 tests × 3 domains) from RQ 5.1 results/ch5/rq1/data/step03_theta_scores.csv
- TSVR mapping (400 rows: 100 participants × 4 tests) from RQ 5.1 results/ch5/rq1/data/step00_tsvr_mapping.csv
- Age variable (100 rows: one per participant) from data/cache/dfData.csv
(from 2_plan.md Step 0, lines 46-73)

**Analysis Specification:**
1. Merge theta, TSVR, and age data; grand-mean center age; reshape to long format (Step 1)
2. Fit LMM with formula: `theta ~ TSVR_hours + log_TSVR + Age_c + domain + TSVR_hours:Age_c + log_TSVR:Age_c + TSVR_hours:domain + log_TSVR:domain + Age_c:domain + TSVR_hours:Age_c:domain + log_TSVR:Age_c:domain + (TSVR_hours | UID)` (Step 2, line 108-109)
3. Validate LMM assumptions (7 diagnostics: residual normality, homoscedasticity, random effects normality, independence, linearity, outliers, convergence) (Step 2b, lines 117-151)
4. Model selection via LRT comparing: Full (random intercepts + slopes, correlated) vs Uncorrelated vs Intercept-only (Step 2c, lines 155-164)
5. Extract 3-way Age × Domain × Time interaction terms; apply Bonferroni correction α = 0.025 (Step 3, lines 166-172)
6. Compute domain-specific age effects (What/Where/When) and post-hoc Tukey HSD contrasts (Step 4, lines 173-183)

**Expected Output:**
- Fitted LMM model object with 3-way interaction terms and all fixed effects (results/step02_lmm_model.pkl)
- 3-way interaction terms CSV with dual p-values: Bonferroni-corrected and uncorrected (data/step03_interaction_terms.csv)
- Domain-specific age effects by memory domain (data/step04_age_effects_by_domain.csv)
- Post-hoc pairwise contrasts with Tukey HSD correction per Decision D068 (data/step04_post_hoc_contrasts.csv)
- Plot source CSV with observed means and model predictions aggregated by age tertiles (plots/step05_age_effects_plot_data.csv)
(from 4_analysis.yaml Steps 2-5, lines 150-556)

**Success Criteria:**
- All 1200 observations successfully merged with no NaN values
- LMM converges with all fixed effects estimable
- 3-way interaction terms present and correctly computed
- Age_c grand-mean centered: mean(Age_c) ≈ 0
- All 3 domains (What/Where/When) and 4 tests (T1/T2/T3/T4) present in output
(from 2_plan.md Step 0-1 validation, lines 99-262)

**Final Results:**
HYPOTHESIS NOT SUPPORTED. All 3-way Age × Domain × Time interaction terms non-significant (p > 0.4, far above Bonferroni α = 0.025). Domain-specific age effects virtually identical across What/Where/When (magnitude ≈ 0.00001 theta units/year, all p = 0.779). Visual patterns show minimal age tertile separation and uniform trajectories across all three domains. Null finding suggests either: (1) VR integrated What/Where/When encoding bypasses hippocampal age vulnerability, (2) insufficient power for small effects in N=100 sample, or (3) age range [20-70] too narrow to detect critical hippocampal aging threshold (post-70 decline). (from results/summary.md lines 81, 93, 296-323)

---

### RQ5.11: IRT-CTT Convergent Validity

**Research Question:** Do IRT theta scores and CTT mean scores yield the same conclusions about domain-specific forgetting trajectories? (from 1_concept.md, line 12)

**Hypothesis:** Exploratory. IRT theta scores and CTT mean scores should converge (r > 0.70 as strong convergence per psychometric standards, Cohen's kappa > 0.60 indicating substantial agreement on LMM coefficient significance patterns per Landis & Koch 1977), demonstrating robustness of domain-specific forgetting trajectory conclusions to measurement approach. (from 1_concept.md, lines 44-45)

**Data Required:**
- IRT theta scores from RQ 5.1 Step 3: results/ch5/rq1/data/step03_theta_scores.csv (composite_ID, theta_what, theta_where, theta_when)
- TSVR mapping from RQ 5.1 Step 0: results/ch5/rq1/data/step00_tsvr_mapping.csv (UID, test, TSVR_hours)
- Purified item list from RQ 5.1 Step 2: results/ch5/rq1/data/step02_purified_items.csv (40-60 items)
- Raw VR data: data/cache/dfData.csv (for CTT computation using same purified items)
(from 2_plan.md, lines 52-100)

**Analysis Specification:**
1. Load IRT theta scores, TSVR mapping, purified items, and raw data; filter raw data to purified items only (Step 0)
2. Compute CTT mean scores per UID x test x domain using purified item set (Step 1)
3. Compute Pearson correlations (IRT vs CTT) per domain with Holm-Bonferroni correction, dual p-value reporting (Decision D068), test r > 0.70 and r > 0.90 thresholds (Step 2)
4. Fit parallel LMMs: Score ~ (TSVR_hours + log(TSVR_hours+1)) × Domain + (TSVR_hours | UID) for both IRT and CTT with identical structure, implementing convergence-aware simplification (random slopes → intercepts if either fails) (Step 3)
5. Validate LMM assumptions for both models (normality, homoscedasticity, ACF) and apply same remediation to both (Step 4)
6. Extract and compare fixed effects, calculate Cohen's kappa (threshold κ > 0.60) for significance pattern agreement, flag discrepancies (Step 5)
7. Compare AIC/BIC (delta interpretation: |delta| < 2 equivalent, |delta| > 10 substantial) (Step 6)
8. Prepare scatterplot data: IRT vs CTT per domain with correlation annotations (Step 7)
9. Prepare trajectory data: IRT vs CTT mean scores per timepoint × domain with 95% CIs (Step 8)
(from 2_plan.md, lines 1-1423)

**Expected Output:**
Correlation results: results/step02_correlations.csv (r, 95% CI, p_uncorrected, p_holm, thresholds per domain)
LMM summaries: results/step03_irt_lmm_summary.txt and results/step03_ctt_lmm_summary.txt
Fixed effects comparison: results/step05_coefficient_comparison.csv (12 columns: term, estimate_irt, SE_irt, p_irt, sig_irt, estimate_ctt, SE_ctt, p_ctt, sig_ctt, agreement, beta_ratio, discrepancy_flag)
Model fit: results/step06_model_fit_comparison.csv (AIC/BIC deltas and interpretation)
Plot source data: data/step07_scatterplot_data.csv (1200 rows), data/step08_trajectory_data.csv (~24 rows)
(from 4_analysis.yaml and 2_plan.md)

**Success Criteria:**
- All correlations > 0.70 (strong convergence): PASS
- Cohen's kappa > 0.60 (substantial agreement): PASS
- Agreement ≥ 80% on coefficient significance patterns: PASS
- Both LMM models converged with identical random structure: PASS
- Assumption validation reports generated for both models: PASS
- All output files exist with expected row/column counts: PASS
(from 2_plan.md, lines 1197-1379 and results/summary.md)

**Final Results:** RQ 5.11 analysis COMPLETED 2025-11-29. Exceptional convergent validity confirmed across all three domains: What (r = 0.906, 95% CI [0.887, 0.922]), Where (r = 0.970, [0.963, 0.975]), When (r = 0.919, [0.903, 0.933]). All correlations exceed r > 0.90 threshold (exceeding r > 0.70 hypothesis). Cohen's kappa = 1.0 (perfect agreement on coefficient significance: 3/3 main effects agree on sig vs nonsig). Both IRT and CTT models converged with random slopes; 100% agreement on time effects direction (declining performance over time per TSVR_hours). Key finding: IRT and CTT reach identical statistical conclusions about domain-specific forgetting trajectories despite measurement approach differences, confirming methodological robustness of RQ 5.1 findings. Where domain shows highest convergence (r = 0.970, 45 items, most homogeneous psychometrics), While When domain achieves robust convergence (r = 0.919) despite severe item under-representation (only 5 items). (from results/summary.md, lines 1-551)

---

### RQ5.12: Purified IRT Item Set Effects on CTT

**Research Question:** If we compute CTT scores using only IRT-retained items (post-purification), do conclusions differ from full-item CTT? (from 1_concept.md lines 11-12)

**Hypothesis:** Purified CTT (using only IRT-retained items) will show higher correlation with IRT theta scores compared to full CTT, demonstrating that item purification removes noise rather than signal. (from 1_concept.md lines 44-45)

**Data Required:**
- IRT item parameters and theta scores from RQ 5.1 (results/ch5/rq1/data/step02_purified_items.csv, step03_theta_scores.csv)
- TSVR mapping from RQ 5.1 (results/ch5/rq1/data/step00_tsvr_mapping.csv)
- Raw dichotomized item responses from data/cache/dfData.csv for CTT computation (from 2_plan.md Step 0, lines 42-60)

**Analysis Specification:** 9-step pipeline (from 2_plan.md):
1. Load IRT items, theta, TSVR mapping, raw data
2. Map items to full vs purified sets, identify retained/excluded items
3. Compute full CTT scores (all items, mean per domain)
4. Compute purified CTT scores (retained items only, mean per domain)
5. CTT reliability assessment (Cronbach's alpha with bootstrap 95% CIs)
6. Correlation analysis using Steiger's z-test for dependent correlations (Decision D068 dual p-values)
7. Standardize outcomes to z-scores per domain for valid AIC comparison
8. Fit parallel LMMs with identical formula to three standardized measurements (Full CTT, Purified CTT, IRT theta)
9. Prepare plot data (correlation comparison + AIC comparison)

**Expected Output:** (from 2_plan.md/4_analysis.yaml)
- CTT full/purified scores per domain (data/step02_ctt_full_scores.csv, step03_ctt_purified_scores.csv)
- Cronbach's alpha assessment (data/step04_reliability_assessment.csv)
- Correlation analysis with dual p-values (data/step05_correlation_analysis.csv)
- Parallel LMM comparison (data/step07_lmm_model_comparison.csv + 6 additional files)
- Plot source CSVs (plots/step08_correlation_comparison_data.csv, step08_aic_comparison_data.csv)

**Success Criteria:** (from results/summary.md Section 1-2)
- Primary hypothesis SUPPORTED for What/Where domains: Purification significantly improved CTT-IRT convergence (What: r = 0.906 vs 0.879, delta_r = +0.027, p < .001; Where: r = 0.955 vs 0.940, delta_r = +0.015, p < .001)
- Reliability maintained: Cronbach's alpha stable or improved (What: delta = -0.01; Where: delta = +0.01)
- All 9 analysis steps validated per 4-layer substance criteria (existence, structure, substance, logs)

**Final Results:** (from results/summary.md)
What and Where domains show significantly higher CTT-IRT convergence after purification (both p < .001 Bonferroni-corrected), confirming that IRT item selection removes measurement noise. **Critical anomaly:** When domain shows catastrophic item loss (19% retention, 5 of 26 items), creating paradoxical LMM results (Full CTT AIC = 2954 vs IRT AIC = 3007 vs Purified CTT AIC = 3108) explained by severe domain imbalance in purified item pool.

---

### RQ5.13: Between-Person Variance in Forgetting Rates

**Research Question:** What proportion of variance in forgetting rate (slopes) is between-person (stable individual differences) vs within-person (measurement error)? (from 1_concept.md lines 11-12)

**Hypothesis:** Substantial between-person variance exists in forgetting rate (ICC for slopes > 0.40), indicating forgetting rate is a stable, trait-like individual difference rather than random noise. (from 1_concept.md lines 44-45)

**Data Required:** DERIVED from RQ 5.7 best-fitting Lin+Log LMM model. Requires three files: (1) `results/ch5/rq7/data/lmm_Lin+Log.pkl` (saved LMM model object with random slopes), (2) `results/ch5/rq7/data/step03_theta_scores.csv` (IRT ability estimates, columns: UID, test, Theta_All), (3) `results/ch5/rq7/data/step04_lmm_input.csv` (LMM input with TSVR_hours time variable) (from 2_plan.md lines 44-70)

**Analysis Specification:** 5 sequential steps per 2_plan.md:
1. Load RQ 5.7 dependencies (model, theta scores, TSVR mapping) with convergence validation (lines 36-146)
2. Extract variance components from random effects covariance matrix: var_intercept, var_slope, cov_int_slope, var_residual (lines 149-222)
3. Compute ICC estimates using dual methods: simple ratio [var_slope/(var_slope + var_residual)] and conditional ICC at Day 6 accounting for intercept-slope covariance (lines 225-308)
4. Extract individual random effects (random_intercepts, random_slopes, total_intercept, total_slope) for all 100 participants with descriptive statistics (lines 311-393)
5. Test intercept-slope correlation using Pearson r with dual p-value reporting per Decision D068 (uncorrected + Bonferroni α=0.0033), generate histogram and Q-Q plot of random slopes distribution (lines 396-508)

**Expected Output:** Data files: step01_model_metadata.yaml (model info), step02_variance_components.csv (5 components), step03_icc_estimates.csv (3 ICC types), step04_random_effects.csv (100 participants × 5 columns), step05_intercept_slope_correlation.csv (5 statistics). Results files: icc_summary.txt, random_slopes_descriptives.txt, correlation_interpretation.txt. Plots: histogram and Q-Q plot of random slopes. (from 2_plan.md section "Expected Data Formats")

**Success Criteria:** All 5 steps execute with validation passing (no missing files, variance components positive, ICC in [0,1], 100 participants extracted, correlation dual p-values reported). (from 2_plan.md validation sections lines 115-801)

**Final Results:** Hypothesis REJECTED. ICC_slope_simple = 0.0505% (0.000505), far below 0.40 threshold. Forgetting rate shows minimal between-person variance (99.95% within-person error). However, baseline ability shows high ICC (60.6%), and intercept-slope correlation is very strong (r = -0.973, p < 0.001), indicating high performers maintain advantage despite minimal forgetting rate variability. Analysis re-run with improved Lin+Log model (vs Log-only) yielded 42-fold improvement in slope variance but findings remain robust: forgetting rate NOT a stable cognitive trait in young healthy adults with 6-day retention. (from results/summary.md lines 54-110, 187-230)

---

## END OF ANALYSES_CH5_actual.md

**Generated:** 2025-11-30
**Source:** 13 parallel context_finder agents extracting from results/ch5/5.X.X/ folders
**Coverage:** RQs 5.1-5.13 (complete), RQs 5.14-5.15 (not yet executed)
**Purpose:** As-built documentation for comparison with original ANALYSES_CH5.md planning document
