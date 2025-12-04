# RQ 5.5.6: Source-Destination Variance Decomposition

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** Variance Decomposition
**Full ID:** 5.5.6

---

## Research Question

**Primary Question:**
What proportion of variance in source (-U-) and destination (-D-) memory is attributable to stable between-person differences (intercepts vs slopes)?

**Scope:**
This RQ examines variance decomposition for pick-up locations (-U- tags, source memory) and put-down locations (-D- tags, destination memory) across N=100 participants × 4 test sessions (T1, T2, T3, T4) = 800 observations (400 per location type). Analysis focuses on decomposing variance into between-person stable traits (intercepts and slopes) versus within-person measurement error.

**Theoretical Framing:**
Variance decomposition quantifies the proportion of individual differences that are trait-like (stable across timepoints) versus state-like (transient measurement error). This addresses whether source and destination memory show stable individual differences, particularly in forgetting rates. The universal pattern across Chapter 5 (RQs 5.1.4, 5.2.6, 5.3.7, 5.4.6) shows ICC_slope ≈ 0, indicating 4-timepoint design limits reliable slope estimation.

---

## Theoretical Background

**Relevant Theories:**

- **Individual Differences in Episodic Memory:** Stable trait-like variance in memory ability reflects both genetic factors (Papassotiropoulos et al., 2006) and structural brain differences (Voss et al., 2010). Intercept variance reflects baseline memory ability, while slope variance reflects individual differences in forgetting rate.

- **Measurement Reliability Theory:** ICC (Intraclass Correlation Coefficient) quantifies the proportion of total variance attributable to between-person differences. ICC > 0.40 indicates substantial trait-like stability (Cicchetti, 1994). ICC_slope requires sufficient timepoints for reliable estimation.

- **Source-Destination Memory Dissociation:** If destination encoding is weaker than source (per RQ 5.5.1 hypothesis), destination memory may show lower ICC_intercept (more variable baseline) due to greater susceptibility to encoding variability.

**Key Citations:**

- **Hertzog, C., Kramer, A. F., Wilson, R. S., & Lindenberger, U. (2008).** Enrichment effects on adult cognitive development. Psychological Science in the Public Interest, 9(1), 1-65. [Cognitive reserve and individual differences in aging]
- **Stern, Y. (2009).** Cognitive reserve. Neuropsychologia, 47(10), 2015-2028. [Individual differences in cognitive decline trajectories]
- **Drouin, H., Bherer, L., & Bherer, J. (2014).** Improving memory with strategy training. Psychology and Aging, 29(3), 467-475. [Individual differences in episodic memory]
- **Barr, D. J., Levy, R., Scheepers, C., & Tily, H. J. (2013).** Random effects structure for confirmatory hypothesis testing. Journal of Memory and Language, 68(3), 255-278. [LMM random effects specification]
- **Reuter-Lorenz, P. A., & Park, D. C. (2014).** How does it STAC up? Revisiting the scaffolding theory of aging and cognition. Neuropsychology Review, 24(3), 355-370. [Individual differences in cognitive aging]
- **Oberpriller, Q., & Kay, K. (2022).** Intraclass correlation: Improved methods and tutorials. Methods in Ecology and Evolution, 13(5), 1085-1098. [ICC computation and interpretation]
- **Cicchetti, D. V. (1994).** Guidelines, criteria, and rules of thumb for evaluating normed and standardized assessment instruments in psychology. Psychological Assessment, 6(4), 284-290. [ICC interpretation thresholds: poor <0.40, fair 0.40-0.59, good 0.60-0.74, excellent ≥0.75]

**Source-Destination Hypothesis Contingency:**
The variance decomposition results depend on the source-destination dissociation established in RQ 5.5.1. If RQ 5.5.1 shows equivalent source and destination memory (null finding), the ICC comparison between location types becomes less theoretically meaningful. However, the design limitation pattern (ICC_slope ≈ 0) is expected to replicate regardless of the main effect direction.

**Theoretical Predictions:**

ICC_slope will be near zero for both location types (<0.02), consistent with the universal pattern across Chapter 5. This reflects design limitation (4 timepoints insufficient for reliable slope estimation), not absence of individual differences. ICC_intercept will be moderate (0.30-0.60), indicating stable baseline differences. If destination encoding is weaker (per RQ 5.5.1), -D- may show lower ICC_intercept (more variable baseline).

**Literature Gaps:**
To be identified by rq_scholar. No prior studies have examined variance decomposition for source-destination memory in VR episodic contexts.

---

## Hypothesis

**Primary Hypothesis:**
ICC_slope will be near zero for both location types (<0.02), consistent with the universal pattern across Chapter 5 (5.1.4, 5.2.6, 5.3.7, 5.4.6). ICC_intercept will be moderate (0.30-0.60), indicating stable baseline differences.

**Secondary Hypotheses:**
If destination encoding is weaker (per RQ 5.5.1), -D- may show lower ICC_intercept (more variable baseline) compared to -U-.

**Theoretical Rationale:**
The universal ICC_slope ≈ 0 pattern reflects design limitation: 4 timepoints are insufficient for reliable individual slope estimation, not absence of true individual differences in forgetting rate. ICC_intercept stability reflects trait-like memory ability. Weaker destination encoding may manifest as greater baseline variability (lower ICC_intercept) due to increased susceptibility to encoding context and interference.

**Expected Effect Pattern:**

- ICC_intercept: 0.30-0.60 for both location types (moderate stability)
- ICC_slope_simple: <0.02 for both location types (near zero)
- ICC_slope_conditional: similar to ICC_slope_simple
- Intercept-slope correlation: test with Bonferroni alpha=0.025, no strong directional prediction
- Potential location difference: ICC_intercept(-U-) > ICC_intercept(-D-)

---

## Memory Domains

**Domains Examined:**

- [ ] **What** (Object Identity)
  - Tag Code: `-N-`
  - Description: NOT examined in this RQ

- [x] **Where** (Spatial Location)
  - [ ] `-L-` tags (general location, legacy)
  - [x] `-U-` tags (pick-up location, SOURCE memory)
  - [x] `-D-` tags (put-down location, DESTINATION memory)
  - Disambiguation: This RQ examines ONLY -U- (source) and -D- (destination) tags, using variance decomposition from RQ 5.5.1 outputs. Legacy -L- tags are excluded.

- [ ] **When** (Temporal Order)
  - Tag Code: `-O-`
  - Description: NOT examined in this RQ

**Inclusion Rationale:**

Source (-U-) and destination (-D-) spatial memory are examined because RQ 5.5.1 establishes the foundational trajectory analysis and LMM fitting. This RQ decomposes variance from those fitted models to quantify stable individual differences in source vs destination memory.

**Exclusion Rationale:**

- **-L- tags:** Legacy spatial location tags excluded as RQ 5.5.1 focuses on source-destination dissociation.
- **What (-N-) and When (-O-) domains:** Not relevant to source-destination spatial memory.

---

## Analysis Approach

**Analysis Type:**
Variance decomposition using Linear Mixed Models (LMM) with random slopes. Computes Intraclass Correlation Coefficients (ICC) for intercepts and slopes per location type.

**High-Level Workflow:**

**Step 1:** Fit location-stratified LMMs with random slopes: theta ~ log_TSVR + (log_TSVR | UID) separately for Source and Destination. Use best-fit time transformation from RQ 5.5.1.

**Step 2:** Extract variance components per location: var_intercept, var_slope, cov_int_slope, var_residual from random effects covariance matrix.

**Step 3:** Compute ICC estimates per location:
- ICC_intercept = var_intercept / (var_intercept + var_residual)
- ICC_slope_simple = var_slope / (var_slope + var_residual)
- ICC_slope_conditional at Day 6 accounting for covariance

**Step 4:** Extract individual random effects per location for 100 participants (200 rows total: 100 UID × 2 locations). These random effects are REQUIRED outputs for RQ 5.5.7 (clustering analysis).

**Step 5:** Test intercept-slope correlations per location with Bonferroni alpha=0.025. Report dual p-values (Decision D068: both uncorrected and Bonferroni-corrected p-values).

**Step 6:** Compare ICC across location types (Source vs Destination). Test if ICC_intercept(-U-) > ICC_intercept(-D-).

**Expected Outputs:**

- `data/step01_model_metadata_source.yaml` (model convergence info for Source LMM)
- `data/step01_model_metadata_destination.yaml` (model convergence info for Destination LMM)
- `data/step01_source_lmm_model.pkl` (saved Source LMM model)
- `data/step01_destination_lmm_model.pkl` (saved Destination LMM model)
- `data/step02_variance_components.csv` (10 rows: 5 components × 2 locations)
- `data/step03_icc_estimates.csv` (6 rows: 3 ICC types × 2 locations)
- `data/step04_random_effects.csv` (200 rows: 100 UID × 2 locations, REQUIRED for RQ 5.5.7)
- `data/step05_intercept_slope_correlations.csv` (2 rows: Source, Destination)
- `plots/step06_location_icc_barplot.png` (visual comparison of ICC across locations)

**Success Criteria:**

- RQ 5.5.1 dependency verified (status.yaml: rq_concept, rq_scholar, rq_stats, rq_planner, rq_tools, rq_analysis, g_code, rq_inspect = success)
- Both location-stratified LMMs converge (model.converged=True)
- Variance components are positive (no negative variances or Heywood cases)
- ICC values are in [0,1] range
- 200 random effects extracted (100 UID × 2 locations)
- Dual p-values present for intercept-slope correlations (Decision D068)
- Location comparison interpretable (Source vs Destination ICC differences)

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.5.1 outputs)

### DERIVED Data Source:

**Source RQ:**
RQ 5.5.1 (Source-Destination Trajectories - ROOT)

**File Paths:**

- `results/ch5/5.5.1/data/step05_lmm_fitted_model.pkl` (best-fitting LMM model from RQ 5.5.1)
- `results/ch5/5.5.1/data/step04_lmm_input.csv` (800 rows: 100 UID × 4 tests × 2 location types)

**Dependencies:**

RQ 5.5.1 must complete all steps (IRT calibration, item purification, LMM fitting, model selection) before this RQ can run. Specifically, requires:
- IRT theta scores for Source (-U-) and Destination (-D-) items
- TSVR time mapping
- Best-fit time transformation (e.g., log_TSVR) identified via model selection

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.5.1, no exclusions)

**Items:**
- [x] Source items (-U- tags, pick-up locations)
- [x] Destination items (-D- tags, put-down locations)
- N/A: Theta scores already aggregated per location type

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4; nominal Days 0, 1, 3, 6)
- Inherited from RQ 5.5.1

**Time Variable:**
- TSVR (actual hours since encoding) from master.xlsx
- Best-fit transformation (e.g., log_TSVR) from RQ 5.5.1 model selection

---
