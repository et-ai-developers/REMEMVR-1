# Chapter 5 Remaining RQ Execution Plan

**Created:** 2025-12-03
**Purpose:** Rigorous execution of remaining RQs with comprehensive validation
**Thesis Claim:** Laboratory dissociations dissolve in ecological memory encoding

---

## Critical Context

We are making a significant theoretical claim: that canonical What-Where-When dissociations from 100 years of laboratory research are artifacts of stimulus isolation. This claim MUST be supported by bulletproof methodology.

**Every RQ must pass ALL validation checks before results are trusted.**

---

## Pre-Execution Validation Checklist

### DATA SOURCING (Apply to EVERY RQ)

| # | Check | Verification Method | Pass Criteria |
|---|-------|---------------------|---------------|
| D1 | **Floor Effect Exclusion** | Verify step00 data excludes -O- domain for WWW analyses | No When domain items in domain-type RQs |
| D2 | **IRT Purification Applied** | Check item count in input data | 68 purified items (not 102 original) |
| D3 | **Correct Parent RQ** | Verify step00 data source path | Matches documented dependency chain |
| D4 | **Sample Size** | Check data dimensions | N=100 participants, expected row count |
| D5 | **No Missing Data** | Check for NaN/null values | Complete cases or documented handling |

### MODEL SPECIFICATION (Apply to EVERY LMM)

| # | Check | Verification Method | Pass Criteria |
|---|-------|---------------------|---------------|
| M1 | **Log Model Confirmed** | Check ROOT RQ AIC weights | Log or Lin+Log selected (weight > 40%) |
| M2 | **log_TSVR as Fixed Effect** | Grep code for time variable | Uses `log_TSVR`, NOT `TSVR_hours` or `Days` |
| M3 | **Random Slopes on log_TSVR** | Check `re_formula` parameter | `re_formula="~log_TSVR"` or equivalent |
| M4 | **Convergence Achieved** | Check model output | No convergence warnings |
| M5 | **Boundary Estimates Flagged** | Check variance components | Document if Var ≈ 0.000 |
| M6 | **Centering Applied** | Check continuous predictors | Age_c (centered), other covariates centered |

### SCALE TRANSFORMATION (Apply to trajectory analyses)

| # | Check | Verification Method | Pass Criteria |
|---|-------|---------------------|---------------|
| S1 | **Theta Scale Primary** | Verify DV in LMM | theta or ability estimate |
| S2 | **TCC Conversion Correct** | Check probability calculation | Proper IRT Test Characteristic Curve |
| S3 | **Dual-Scale Plots** | Check plot outputs | Both theta AND probability trajectories |
| S4 | **No Compression Artifacts** | Visual inspection | Probability curves not at floor/ceiling |

### STATISTICAL RIGOR (Apply to ALL analyses)

| # | Check | Verification Method | Pass Criteria |
|---|-------|---------------------|---------------|
| R1 | **Effect Sizes Reported** | Check results output | Cohen's d or standardized β for all effects |
| R2 | **Confidence Intervals** | Check parameter estimates | 95% CIs for key parameters |
| R3 | **Multiple Comparisons** | Document correction method | Bonferroni/FDR where >3 comparisons |
| R4 | **Residual Diagnostics** | Generate diagnostic plots | Normality, homoscedasticity acceptable |
| R5 | **Post-Hoc Power** | Calculate for null findings | Report detectable effect at 80% power |

---

## Post-Execution Validation Checklist

### RESULTS CONSISTENCY

| # | Check | Verification Method | Pass Criteria |
|---|-------|---------------------|---------------|
| C1 | **Direction Consistent** | Compare across related RQs | No sign flips between RQs |
| C2 | **Magnitude Plausible** | Compare to literature | Effect sizes in expected range |
| C3 | **Replication Pattern** | Check across Types | Similar patterns in Domains/Paradigms/Congruence |
| C4 | **IRT-CTT Static Convergence** | Calculate correlation | r > 0.85 at each timepoint |

### THESIS ALIGNMENT

| # | Check | Verification Method | Pass Criteria |
|---|-------|---------------------|---------------|
| T1 | **2024 Literature Match** | Compare to cited studies | Null age effects match SOTA |
| T2 | **Binding Hypothesis Fit** | Document consistency | Explain how result fits unitization theory |
| T3 | **Sensitivity Robust** | Alternative models tested | Conclusions stable across model variants |

---

## RQ Execution Order

### Phase 1: Verify Completed RQs (CRITICAL)

Before proceeding, re-validate all 15 completed RQs against the checklist above.

| RQ | Type | Status | Validation Priority |
|----|------|--------|---------------------|
| 5.1.1 | Functional Form | COMPLETE | HIGH - ROOT RQ |
| 5.1.2 | Two-Phase | COMPLETE | MEDIUM |
| 5.1.3 | Age Effects | COMPLETE | HIGH - Key null finding |
| 5.1.4 | Variance Decomp | COMPLETE | HIGH - ICC investigation |
| 5.1.5 | Clustering | COMPLETE | LOW |
| 5.2.1 | Domain Trajectories | COMPLETE | HIGH - ROOT RQ, When exclusion |
| 5.2.2 | Domain Consolidation | COMPLETE | MEDIUM |
| 5.2.3 | Domain Age | COMPLETE | HIGH - Key null finding |
| 5.2.4 | IRT-CTT | NEEDS VALIDATION | HIGH - Model correction applied |
| 5.3.1 | Paradigm Trajectories | COMPLETE | HIGH - ROOT RQ |
| 5.3.2 | Gradient Test | COMPLETE | MEDIUM |
| 5.3.3 | Paradigm Consolidation | COMPLETE | MEDIUM |
| 5.3.4 | Paradigm Age | COMPLETE | HIGH - Key null finding |
| 5.4.1 | Congruence Trajectories | COMPLETE | HIGH - ROOT RQ |
| 5.4.2 | Congruence Consolidation | COMPLETE | MEDIUM |
| 5.4.3 | Congruence Age | COMPLETE | HIGH - Key null finding |

### Phase 2: Execute Remaining Ready RQs

| RQ | Type | tools | analysis | Priority | Notes |
|----|------|-------|----------|----------|-------|
| 5.2.5 | Domains Purified CTT | TRUE | TRUE | MEDIUM | IRT-CTT on purified items |
| 5.2.6 | Domains Variance | TRUE | TRUE | LOW | ICC by domain |
| 5.2.7 | Domains Clustering | TRUE | TRUE | LOW | K-means by domain |
| 5.3.6 | Paradigms Purified CTT | TRUE | TRUE | MEDIUM | CTT by paradigm |
| 5.3.7 | Paradigms Variance | TRUE | TRUE | LOW | ICC by paradigm |
| 5.3.8 | Paradigms Clustering | TRUE | TRUE | LOW | K-means by paradigm |
| 5.3.9 | Paradigms Item LMM | TRUE | TRUE | MEDIUM | Cross-classified item analysis |
| 5.4.5 | Congruence Purified CTT | TRUE | TRUE | MEDIUM | CTT by schema |
| 5.4.6 | Congruence Variance | TRUE | TRUE | LOW | ICC by schema |
| 5.4.7 | Congruence Clustering | TRUE | TRUE | LOW | K-means by schema |
| 5.4.8 | Congruence Item LMM | TRUE | TRUE | MEDIUM | Item × schema analysis |

### Phase 3: Create and Execute New Type 5.5 (Source-Destination)

| RQ | Name | Question | Priority |
|----|------|----------|----------|
| 5.5.1 | Source-Destination Trajectories | -U- vs -D- forgetting rates | HIGH |
| 5.5.2 | Source-Destination Consolidation | Piecewise by source vs destination | MEDIUM |
| 5.5.3 | Source-Destination Age | Age × Source/Destination × Time | MEDIUM |

**Justification:**
- Expected POSITIVE finding (putdown harder than pickup)
- Demonstrates REMEMVR CAN detect meaningful dissociations
- Theoretically novel: source vs destination memory in VR
- Uses existing data (-U- and -D- flags)

### Phase 4: Assess Blocked RQs

| RQ | Type | Blocking Issue | Decision Criteria |
|----|------|----------------|-------------------|
| 5.1.6 | General Item GLMM | Missing GLMM tools | Build only if item analysis adds unique value |
| 5.2.8 | Domain Item GLMM | Missing GLMM tools | Build only if domain×item interaction important |
| 5.3.5 | Paradigm IRT-CTT | Missing CTT tools | Build only if paradigm-specific divergence expected |
| 5.4.4 | Congruence IRT-CTT | Missing CTT tools | Build only if schema-specific divergence expected |

---

## Sensitivity Analyses Required

### 1. Theta vs Probability Scale Comparison

**RQs to test:** 5.1.1, 5.2.1, 5.4.1 (ROOT RQs)

**Method:**
1. Run LMM on theta scale (primary)
2. Convert theta → probability via TCC
3. Run LMM on probability scale
4. Compare: Do conclusions match?

**If conclusions MATCH:** Report theta as primary, note probability confirms
**If conclusions DIVERGE:** Investigate scale-dependent effects, document both

### 2. Model Robustness

**For each key null finding (5.1.3, 5.2.3, 5.3.4, 5.4.3):**

1. Compare Log vs Lin+Log vs Quadratic model
2. Verify null holds across all well-fitting models
3. Document any model where effect becomes significant

### 3. Outlier Sensitivity

**Method:**
1. Identify potential outliers (>3 SD on any measure)
2. Re-run key analyses with and without outliers
3. Document if conclusions change

---

## Documentation Requirements

### For EVERY completed RQ:

```
results/ch5/X.Y.Z/
├── docs/
│   ├── 1_concept.md       # Validated against template
│   ├── 2_plan.md          # Steps with validation checkpoints
│   ├── 3_tools.yaml       # Tool specifications
│   └── 4_analysis.yaml    # Analysis recipe
├── code/
│   └── step*.py           # Reproducible code
├── data/
│   └── step*.csv          # Intermediate data
├── results/
│   ├── summary.md         # Complete results summary
│   ├── validation.md      # NEW: Validation checklist results
│   └── *.png              # Dual-scale plots
└── tests/
    └── test_*.py          # Unit tests for code
```

### NEW: validation.md Template

```markdown
# RQ X.Y.Z Validation Report

## Pre-Execution Checks
- [ ] D1: Floor effect exclusion - PASS/FAIL
- [ ] D2: IRT purification - PASS/FAIL (N items = ___)
- [ ] D3: Correct parent RQ - PASS/FAIL (parent = ___)
- [ ] D4: Sample size - PASS/FAIL (N = ___, rows = ___)
- [ ] D5: No missing data - PASS/FAIL

- [ ] M1: Log model confirmed - PASS/FAIL (AIC weight = ___%)
- [ ] M2: log_TSVR fixed effect - PASS/FAIL
- [ ] M3: Random slopes on log_TSVR - PASS/FAIL
- [ ] M4: Convergence - PASS/FAIL
- [ ] M5: Boundary estimates - NONE/FLAGGED
- [ ] M6: Centering applied - PASS/NA

- [ ] S1: Theta scale primary - PASS/FAIL
- [ ] S2: TCC conversion - PASS/NA
- [ ] S3: Dual-scale plots - PASS/FAIL
- [ ] S4: No compression - PASS/FAIL

## Post-Execution Checks
- [ ] R1: Effect sizes - PASS/FAIL (d = ___)
- [ ] R2: Confidence intervals - PASS/FAIL
- [ ] R3: Multiple comparisons - PASS/NA (method = ___)
- [ ] R4: Residual diagnostics - PASS/FAIL
- [ ] R5: Post-hoc power - PASS/NA (detectable d = ___)

- [ ] C1: Direction consistent - PASS/FAIL
- [ ] C2: Magnitude plausible - PASS/FAIL
- [ ] C3: Replication pattern - PASS/FAIL
- [ ] C4: IRT-CTT convergence - PASS/NA (r = ___)

- [ ] T1: 2024 literature match - PASS/NA
- [ ] T2: Binding hypothesis fit - PASS/PARTIAL/FAIL
- [ ] T3: Sensitivity robust - PASS/FAIL

## Overall Status: VALIDATED / NEEDS REVIEW / FAILED
```

---

## Execution Timeline

### Immediate (This Session)
1. Review this plan
2. Re-validate 5.2.4 (model correction applied)
3. Begin Phase 1 spot-checks on completed RQs

### Short-term (Next 2-3 Sessions)
1. Execute Phase 2 RQs (11 remaining ready)
2. Create 5.5 specifications
3. Execute 5.5.1-5.5.3

### After Assessment
1. Decide on blocked RQs
2. Build tools if needed
3. Final chapter scope determination

---

## Red Flags to Watch For

### STOP and Investigate If:

1. **Direction flip:** Effect positive in one RQ, negative in related RQ
2. **Boundary estimate:** Var = 0.000 when we expect variance
3. **Convergence failure:** Model won't fit with specified random effects
4. **Floor/ceiling:** Probability trajectories compressed at 0 or 1
5. **Sample size mismatch:** Row counts don't match expectations
6. **Missing When exclusion:** -O- domain items appear in WWW analyses
7. **Wrong time variable:** Code uses TSVR_hours instead of log_TSVR
8. **Singular matrix:** Covariance matrix warnings in output

### Document But Continue If:

1. **Simplified random effects:** Had to remove random slopes for convergence
2. **Alternative model better:** Lin+Log beats pure Log
3. **Partial pattern:** Some categories show effect, others don't
4. **Marginal significance:** p = 0.05-0.10 (document, don't interpret as null)

---

## Final Validation Gate

Before any RQ results are included in thesis:

1. **All checklist items PASS or documented exception**
2. **At least ONE sensitivity analysis confirms robustness**
3. **Results consistent with theoretical framework OR divergence explained**
4. **Dual-scale reporting confirms no artifacts**
5. **Code is reproducible (can re-run from step00)**

---

**End of Execution Plan**
