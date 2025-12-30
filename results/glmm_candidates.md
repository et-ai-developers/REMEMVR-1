# GLMM Validation Candidates - Ch5 & Ch6 RQs

**Analysis Date:** 2025-12-24
**Based On:** results/glmm.md findings + RQ summary review

---

## Executive Summary

**Key Finding from glmm.md:** GLMM reveals **intercept effects** that IRT→LMM approach misses or underestimates, while **slope/interaction effects remain robust** across both methods.

**Pattern Discovered:**
- ✅ **Slopes/interactions:** IRT→LMM and GLMM always agree
- ⚠️ **Intercepts:** GLMM sometimes finds significant effects where IRT→LMM shows marginal/null

**Examples:**
- **RQ 5.1.3 Age intercept:** IRT→LMM p=.061 → GLMM p=.014 (marginal → significant)
- **RQ 5.4.1 Congruent intercept:** IRT→LMM p=.548 → GLMM p=.011 (null → significant)
- **RQ 6.1.3 Age intercept:** IRT→LMM p=.125 → GLMM p=.041 (null → marginal)

---

## Candidate RQs for GLMM Validation

### Priority 1: HIGH - Intercept-Only Hypotheses (Most Likely to Change)

These RQs test **baseline differences** (group means) without trajectory interactions. GLMM's higher power for intercepts could reveal hidden effects.

| RQ | Hypothesis | IRT→LMM Result | GLMM Prediction | Priority |
|----|-----------|---------------|-----------------|----------|
| **5.2.2** | Domain baseline differences (What vs Where) | Domain intercepts not reported separately | May find significant baseline differences | HIGH |
| **5.3.2** | Domain ranking (What/Where/When at Day 3) | Marginal means overlap (large CIs) | May find significant domain separation | HIGH |
| **5.5.2** | Source vs Destination baseline | Source > Destination at baseline (from 5.5.1) | May strengthen baseline effect | MEDIUM |
| **6.3.2** | Domain calibration baseline (What/Where/When at T1) | When overconfident (+0.377), What/Where underconfident (-0.25) | May find significant T1 domain differences | HIGH |
| **6.4.2** | Paradigm calibration baseline | ICR underconfident (-0.062), IFR/IRE overconfident | May find significant paradigm baseline differences | HIGH |

### Priority 2: MEDIUM - Age Effects on Intercepts

From glmm.md, age effects on **intercepts** (baseline ability) are consistently stronger in GLMM than IRT→LMM.

| RQ | Hypothesis | IRT→LMM Result | GLMM Finding | Status |
|----|-----------|---------------|--------------|--------|
| **5.1.3** | Age → Intercept (accuracy) | p=.061 (marginal) | **p=.014 (sig)** | ✅ VALIDATED |
| **6.1.3** | Age → Intercept (confidence) | p=.125 (null) | p=.041 (marginal) | ✅ VALIDATED |
| **5.2.3** | Age × Domain (intercepts) | NULL (p=0.412) | May find age differences in domain baselines | MEDIUM |
| **5.3.4** | Age × Paradigm (intercepts) | NULL (p=0.567) | May find age differences in paradigm baselines | MEDIUM |
| **5.4.3** | Age × Schema (intercepts) | NULL (p=0.389) | May find age effects on schema baseline | MEDIUM |
| **5.5.3** | Age × Source-Dest (intercepts) | NULL | May find age modulates source/destination baseline | MEDIUM |

### Priority 3: LOW - Schema Congruence "Quadruple NULL"

The "Quadruple NULL" pattern for schema effects is a **thesis centerpiece**. GLMM validation could confirm these are robust nulls vs underpowered tests.

| RQ | Measure | IRT→LMM Result | GLMM Value | Priority |
|----|---------|---------------|------------|----------|
| **5.4.1** | Schema → Accuracy intercept | NULL (p=.548) | **p=.011 (sig)** | ✅ VALIDATED |
| **6.5.1** | Schema → Confidence intercept | NULL (p_bonf=.634) | **p=.003 (sig)** - Congruent > Common > Incongruent | ✅ VALIDATED |
| **6.5.2** | Schema → Calibration intercept | NULL (p_bonf=.487) | Test if calibration baseline differs | MEDIUM |
| **6.5.3** | Schema → HCE intercept | NULL (p_bonf=.130, LPM + GEE) | **GEE validated (p_bonf=.169)** ✅ NULL CONFIRMED | ✅ DONE |

**CRITICAL UPDATE (2025-12-30):**
- **RQ 5.4.1 (Accuracy):** NULL → SIGNIFICANT (p=.548 → p=.011) ✅ VALIDATED
- **RQ 6.5.1 (Confidence):** NULL → SIGNIFICANT (p=.634 → p=.003) ✅ VALIDATED
- **RQ 6.5.2 (Calibration):** NULL (pending GLMM validation)
- **RQ 6.5.3 (HCE):** NULL CONFIRMED via GEE (p_bonf=.169) ✅ VALIDATED
- **Pattern:** Schema affects BASELINE (encoding strength), NOT TRAJECTORY (decline rates)
- **Narrative revision required:** "Quadruple NULL" → "Baseline effects, trajectory nulls (except HCE)"
- **Theoretical interpretation:** Schema affects acquisition (VR encoding), not retention (forgetting) or metacognitive dissociation (HCE)

### Priority 4: EXCLUDED - Slope/Interaction Tests (Already Robust)

These RQs test **trajectories** (Age × Time, Domain × Time). From glmm.md, these always agree between IRT→LMM and GLMM.

| RQ | Hypothesis | IRT→LMM Result | Likely GLMM Result | Validation Needed? |
|----|-----------|----------------|-------------------|-------------------|
| 5.1.3 | Age × Time (slope) | NULL (p=.76) | NULL (confirmed p=.46) | ✅ NO |
| 5.2.2 | Domain × Segment (piecewise slopes) | 3-way interaction NULL | Likely NULL | NO |
| 5.2.3 | Age × Domain × Time | NULL (p>0.26) | Likely NULL | NO |
| 5.4.3 | Age × Schema × Time | NULL (p=0.994) | Likely NULL | NO |
| 6.1.3 | Age × Time (confidence slope) | NULL (p=.32) | NULL (confirmed p=.27-.30) | ✅ NO |
| 6.3.2 | Domain × Time (calibration crossover) | Significant crossover | Likely significant | NO |
| 6.4.2 | Paradigm × Time (calibration parallel) | NULL (p=0.871) | Likely NULL | NO |

---

## Methodology: Why GLMM Reveals Intercepts

**From glmm.md interpretation:**

> "The discrepancies are in **intercepts, not slopes**. This likely reflects:
> - IRT aggregation smooths out baseline differences
> - GLMM with 28,800+ observations has more power for intercept detection
> - Slope effects require detecting *change over time*, which both methods capture similarly"

**Technical Explanation:**

1. **IRT→LMM Approach:**
   - Step 1: IRT calibration (aggregate items → theta scores per session)
   - Step 2: LMM on theta scores (N=400 observations for Ch5 RQs)
   - **Intercepts:** Based on aggregated theta (information loss from item-level averaging)

2. **GLMM Approach:**
   - Single-stage item-level model (N=28,800 raw responses)
   - **Intercepts:** Based on all item-level data (no aggregation step)
   - **Power advantage:** 72× more observations (28,800 vs 400)

3. **Why Slopes Agree:**
   - Both methods track *change over time* (trajectory shape)
   - IRT aggregation preserves slope structure (Day 0 → Day 6 change)
   - GLMM power advantage minimal for slope detection (within-person change robust to aggregation)

---

## Recommended Validation Strategy

### Phase 1: CRITICAL RQs (Run Immediately)

**Target:** RQs with **intercept-only hypotheses** where null findings are **thesis centerpieces**

1. **RQ 5.4.1 Schema Congruence (Accuracy)**
   - **Current:** NULL (p=.548)
   - **GLMM:** **p=.011 (SIGNIFICANT)**
   - **Impact:** Undermines "quadruple null" schema narrative if congruent items have higher baseline
   - **Action:** ✅ **ALREADY VALIDATED** - Need to integrate into thesis interpretation

2. **RQ 6.3.2 Domain Calibration (T1 Baseline)**
   - **Current:** When overconfident (+0.377), What/Where underconfident (-0.25) at T1
   - **GLMM Test:** Are T1 domain differences significant?
   - **Impact:** If significant, confirms domain-specific metacognitive failures at encoding

3. **RQ 6.4.2 Paradigm Calibration (Baseline)**
   - **Current:** ICR underconfident (-0.062), paradigm main effect p=.040 but NO pairwise contrasts significant
   - **GLMM Test:** Are paradigm baseline differences significant?
   - **Impact:** Resolves "significant LRT but null pairwise contrasts" paradox

### Phase 2: Age Effects Verification

**Target:** Age effects on **intercepts** (baseline ability differences across age)

4. **RQ 5.2.3 Age × Domain**
   - **Current:** NULL (p=0.412)
   - **GLMM Test:** Does age affect What vs Where baseline differently?
   - **Impact:** If significant, suggests VR spatial encoding compensates differently across domains

5. **RQ 5.3.4 Age × Paradigm**
   - **Current:** NULL (p=0.567)
   - **GLMM Test:** Does age affect Free/Cued/Recognition baseline differently?
   - **Impact:** If significant, suggests older adults benefit differently from retrieval support

### Phase 3: Secondary Validation

**Target:** NULL findings where **marginal effects** might become significant with GLMM power

6. **RQ 5.5.2 Source vs Destination (Consolidation)**
   - **Current:** NULL LocationType × Phase interaction (p=.610)
   - **GLMM Test:** Does source/destination baseline difference persist with item-level power?
   - **Impact:** Likely NULL (interaction test, not intercept), but verify

7. **RQ 6.5.1/6.5.2 Schema → Confidence/Calibration**
   - **Current:** NULL (p_bonf > .48)
   - **GLMM Test:** Are congruent items higher confidence/better calibrated at baseline?
   - **Impact:** Completes "quadruple null" GLMM validation

---

## Implementation Notes

### Code Template (Based on glmm.md)

```python
# Single-stage GLMM on item-level data
import statsmodels.formula.api as smf

# Load item-level data (NOT theta aggregated)
item_data = pd.read_csv('master.xlsx_item_level_responses.csv')

# Fit binomial GLMM (for binary accuracy)
model = smf.mixedlm(
    "Correct ~ Group * Time + (1 + Time | UID) + (1 | Item)",
    data=item_data,
    groups=item_data['UID'],
    family=sm.families.Binomial()
)
result = model.fit()

# Extract intercept contrasts
# E.g., for RQ 5.4.1: Congruent vs Incongruent at Day 0
```

### Expected Runtime

- **Per RQ:** ~5-10 minutes (GLMM fitting on 28,800 observations)
- **Phase 1 (3 RQs):** ~30 minutes
- **Phase 2 (2 RQs):** ~20 minutes
- **Phase 3 (2 RQs):** ~20 minutes
- **Total:** ~1.5 hours for all 7 RQs

### Tools Available

- **Existing GLMM code:** results/glmm.md shows validated approach for RQs 5.1.3, 5.4.1, 6.1.1, 6.1.3
- **Item-level data:** master.xlsx (raw responses for all RQs)
- **Validation script:** Can create automated script to run all 7 RQs in parallel

---

## Expected Outcomes

### Scenario A: NULL Findings Remain NULL (Best Case for Thesis)

- Age × Domain/Paradigm/Schema interactions remain NULL with GLMM
- "Age-invariant" and "Schema quadruple null" narratives **strengthened**
- Demonstrates findings robust to statistical approach

### Scenario B: Some Intercepts Become Significant (Thesis Refinement Required)

- **RQ 5.4.1 schema effect confirmed significant** (already known: p=.011)
- Other domain/paradigm baselines may differ
- **Action:** Revise "quadruple null" to "slope null, intercept significant"
- **Interpretation:** Schema affects **encoding strength** (baseline) but not **forgetting rate** (trajectory)

### Scenario C: Major Findings Change (Thesis Overhaul)

- Multiple age × group interactions become significant
- **Action:** Rewrite age-invariance claims
- **Likelihood:** LOW (glmm.md shows slopes always agree, intercepts partially differ)

---

## Recommended Next Steps

1. **Read results/glmm.md thoroughly** - Contains full GLMM methodology for 4 RQs already validated
2. **Run Phase 1 CRITICAL RQs** (6.3.2, 6.4.2) - ~20 minutes
3. **Review RQ 5.4.1 GLMM finding** - Already shows schema null → significant, integrate into thesis
4. **Run Phase 2 Age Effects** (5.2.3, 5.3.4) - ~20 minutes
5. **Compile validation report** - Summary of which findings changed, which remained robust

---

## Summary Table: GLMM Validation Priority

| RQ | Test Type | Current Result | GLMM Expected | Priority | Runtime |
|----|-----------|---------------|---------------|----------|---------|
| ✅ 5.1.3 | Age intercept | p=.061 (marginal) | **p=.014 (sig)** | DONE | - |
| ✅ 5.4.1 | Schema intercept | p=.548 (null) | **p=.011 (sig)** | DONE | - |
| ✅ 6.1.1 | Time effect | Sig | Sig | DONE | - |
| ✅ 6.1.3 | Age intercept | p=.125 (null) | p=.041 (marginal) | DONE | - |
| 🔴 6.3.2 | Domain calibration T1 | Descriptive only | Test sig? | **HIGH** | 10 min |
| 🔴 6.4.2 | Paradigm calibration baseline | LRT sig, pairwise null | Test pairwise? | **HIGH** | 10 min |
| 🟡 5.2.3 | Age × Domain intercept | NULL (p=.412) | Likely NULL | MEDIUM | 10 min |
| 🟡 5.3.4 | Age × Paradigm intercept | NULL (p=.567) | Likely NULL | MEDIUM | 10 min |
| 🟡 6.5.1 | Schema → Confidence | NULL (p_bonf=.634) | Likely NULL | MEDIUM | 10 min |
| 🟡 6.5.2 | Schema → Calibration | NULL (p_bonf=.487) | Likely NULL | MEDIUM | 10 min |
| 🟢 5.2.2 | Domain × Segment slopes | 3-way NULL | Likely NULL | LOW | - |
| 🟢 5.5.2 | Source-Dest × Phase | NULL (p=.610) | Likely NULL | LOW | - |

**Legend:**
- ✅ Already validated in results/glmm.md
- 🔴 HIGH priority - Critical for thesis interpretation
- 🟡 MEDIUM priority - Strengthens robustness claims
- 🟢 LOW priority - Slope/interaction tests (agree across methods)

---

**Total Recommended Validations:** 6 new RQs (~1 hour runtime)

**Critical Action:** Review RQ 5.4.1 GLMM finding (schema intercept effect significant) and integrate into thesis narrative before defense.
