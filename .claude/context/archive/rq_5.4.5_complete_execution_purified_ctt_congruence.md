# RQ 5.4.5 Complete Execution - Purified CTT Effects for Schema Congruence

**Topic:** rq_5.4.5_complete_execution_purified_ctt_congruence
**Created:** 2025-12-04 20:00
**Last Updated:** 2025-12-04 20:00

---

## RQ 5.4.5 Complete Execution (2025-12-04 01:30)

**Task:** RQ 5.4.5 Complete Execution - Purified CTT Effects for Schema Congruence

**Context:** User requested execution of RQ 5.4.5 following the methodology in execution_plan.md. This tests whether IRT-based item purification yields CTT scores that converge more strongly with IRT theta estimates for schema congruence levels (Common, Congruent, Incongruent).

**Archived from:** state.md Session (2025-12-04 01:30)
**Original Date:** 2025-12-04 01:30
**Reason:** RQ completed and validated, detailed execution content archived to reduce state.md size

### Major Accomplishments

#### 1. Executed 9 Analysis Steps (step00-step08)

| Step | Name | Key Result |
|------|------|------------|
| 00 | Verify dependencies | RQ 5.4.1 complete, 72 items total, 50 retained (69.4%) |
| 01 | Map items | Common 79%, Congruent 75%, Incongruent 54% retention |
| 02 | Compute Full CTT | 400 observations × 3 congruence levels |
| 03 | Compute Purified CTT | 400 observations × 3 congruence levels |
| 04 | Reliability assessment | All α improved: Common +0.022, Congruent +0.022, Incongruent +0.063 |
| 05 | Correlation analysis | **r=0.85-0.91, 2/3 Bonferroni significant (Congruent, Incongruent)** |
| 06 | Z-standardize scores | 9 columns all mean~0, SD~1 verified |
| 07 | Fit parallel LMMs | 9 models converged, **PARADOX: Full CTT better AIC for 2/3** |
| 08 | Prepare plot data | 6 rows correlation, 6 rows AIC for visualization |

#### 2. Key Statistical Findings

**Item Retention by Congruence:**

| Dimension | N Total | N Retained | Retention Rate |
|-----------|---------|------------|----------------|
| Common | 24 | 19 | 79.2% |
| Congruent | 24 | 18 | 75.0% |
| Incongruent | 24 | 13 | **54.2%** (lowest) |

**Reliability Improvement (Cronbach's Alpha):**

| Dimension | α Full | α Purified | Δα |
|-----------|--------|------------|-----|
| Common | 0.696 | 0.718 | +0.022 |
| Congruent | 0.721 | 0.743 | +0.022 |
| Incongruent | 0.639 | 0.702 | **+0.063** (largest) |

**Correlation with IRT Theta (Steiger's z-test, Bonferroni α=0.0167):**

| Dimension | r Full | r Purified | Δr | p_bonf | Significant? |
|-----------|--------|------------|-----|--------|--------------|
| Common | 0.853 | 0.875 | +0.022 | 0.428 | ❌ No |
| Congruent | 0.786 | 0.882 | +0.096 | <0.001 | ✅ Yes |
| Incongruent | 0.799 | 0.907 | +0.108 | <0.001 | ✅ Yes |

**LMM Model Fit (AIC - lower is better):**

| Dimension | AIC Full | AIC Purified | ΔAIC | Better Model |
|-----------|----------|--------------|------|--------------|
| Common | 1058.0 | 1075.2 | +17.2 | **Full** |
| Congruent | 1047.4 | 1082.6 | +35.2 | **Full** |
| Incongruent | 1068.0 | 1066.0 | -2.0 | Purified (marginal) |

#### 3. Purification-Trajectory Paradox Confirmed

**Key Finding:** Purified CTT shows significantly HIGHER correlation with IRT theta (Δr = +0.096 to +0.108, p < 0.001) BUT WORSE LMM model fit for Common and Congruent (ΔAIC = +17 to +35).

**Explanation:** Item purification removes psychometrically poor items (low discrimination, extreme difficulty), which improves correlation with IRT theta. However, these removed items also contribute variance useful for trajectory modeling. Result: better convergence BUT worse fit.

**Implication:** For trajectory analysis, Full CTT may be preferable despite lower IRT convergence. For cross-sectional studies, Purified CTT offers better construct validity.

#### 4. Finisher Agents Completed

| Agent | Status | Key Result |
|-------|--------|------------|
| **rq_inspect** | ✅ PASS | All 9 steps validated, 4-layer protocol |
| **rq_plots** | ✅ PASS | 2 plots: correlation_comparison.png, aic_comparison.png |
| **rq_results** | ✅ PASS | summary.md created, 3 anomalies documented |

#### 5. Files Created

**Code (9 scripts):**
- `results/ch5/5.4.5/code/step00_verify_dependencies.py` through `step08_prepare_plot_data.py`

**Data (14 files):**
- step00: dependency_check.txt, full_item_list.csv
- step01: item_mapping.csv
- step02-03: ctt_full_scores.csv, ctt_purified_scores.csv
- step04: reliability_assessment.csv
- step05: correlation_analysis.csv
- step06: standardized_scores.csv
- step07: lmm_model_comparison.csv, 3 summary text files
- step08: correlation_comparison_data.csv, aic_comparison_data.csv

**Plots (2 PNG + script):**
- `plots/correlation_comparison.png` - Grouped bar chart with significance markers
- `plots/aic_comparison.png` - Grouped bar chart with delta annotations
- `plots/plots.py`

**Results:**
- `results/summary.md` (35k comprehensive report)

#### 6. Documentation Updated

| File | Changes |
|------|---------|
| `results/ch5/5.4.5/status.yaml` | All agents + all 9 analysis_steps = success |
| `results/ch5/rq_status.tsv` | 5.4.5 COMPLETE with paradox finding documented |

#### 7. Thesis Implication

The purification-trajectory paradox represents a methodologically important discovery:
- **Primary Hypothesis (CTT-IRT Convergence):** PARTIALLY SUPPORTED (2/3 dimensions significant)
- **Secondary Hypothesis (LMM Model Fit):** NOT SUPPORTED (2/3 dimensions show worse fit)

This finding generalizes across the thesis: we saw the same pattern in RQ 5.2.5 (Domains). The consistent paradox suggests a fundamental trade-off between psychometric purity and trajectory modeling power.

**Recommendation:** Use IRT theta for trajectory analysis (best of both worlds), Full CTT when IRT unavailable for trajectories, Purified CTT only for cross-sectional comparisons.

### Session Metrics

**Tokens:**
- Session start: ~5k (after /refresh)
- Session end: ~80k (at /save)
- Delta: ~75k consumed

**Code steps created:** 9 (via g_code agent)
**Code steps run:** 9 (all successful)
**Bugs fixed by g_code:** ~5 (dimension name mismatches, z-score column names)
**Finisher agents run:** 3 (all PASS)

### Cross-References

**Related RQs:**
- RQ 5.2.5 (Domains): Same paradox pattern discovered first
- RQ 5.3.6 (Paradigms): Third replication of paradox

**Related Archive Topics:**
- ctt_irt_convergence_validated.md (2025-12-03 20:45: Original paradox discovery in domains)
- rq_5.2.5_when_exclusion_complete.md (2025-12-03 20:45: Same 9-step pipeline precedent)
- tdd_irt_ctt_tools_creation.md (2025-12-03 23:30: Tools used for this analysis)

---

**End of Archive Entry**
