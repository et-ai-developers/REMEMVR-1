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
Computes ICC for intercepts and slopes by location type. Tests whether the ICC_slope ≈ 0 pattern (found in 5.2.6, 5.3.7, 5.4.6) replicates.

---

## Theoretical Background

The ICC_slope ≈ 0 pattern across Chapter 5 reflects a design limitation (4 timepoints insufficient for reliable slope estimation). This should replicate for source-destination.

**Expected Pattern:**
- ICC_intercept: Moderate (0.30-0.60) - stable baseline differences
- ICC_slope: Near zero (<0.02) - forgetting rate not trait-like

---

## Hypothesis

**Primary Hypothesis:**
ICC_slope will be near zero for both -U- and -D-, consistent with the universal pattern across Chapter 5.

**Secondary Hypothesis:**
-D- may show lower ICC_intercept than -U- (if destination encoding is more variable).

---

## Analysis Approach

**Design:**
- Fit LMM with (1 + Time | UID) for -U- and -D- separately
- Extract variance components
- Compute ICC_intercept and ICC_slope
- Extract random effects for RQ 5.5.7 (clustering)

**Dependencies:**
- RQ 5.5.1 MUST be complete (provides best-fit model)

---

## Notes

**Matches:** RQ 5.2.6 (Domain Variance), 5.3.7 (Paradigm Variance), 5.4.6 (Congruence Variance)
**Expected:** ICC_slope ≈ 0 (design limitation)

**Outputs for Downstream:**
- Random effects (intercept + slope per UID per location type) for RQ 5.5.7 clustering
