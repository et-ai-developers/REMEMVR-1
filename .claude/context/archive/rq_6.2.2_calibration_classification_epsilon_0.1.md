# RQ 6.2.2 Calibration Classification (Epsilon 0.1)

## Classification Scheme for Over/Under/Calibrated Categories (2025-12-11 20:15)

**Context:** RQ 6.2.2 required classifying continuous calibration scores into discrete categories.

**Classification Rules (ε=0.1):**
- **Overconfident:** calibration > 0.1
- **Underconfident:** calibration < -0.1
- **Calibrated:** -0.1 ≤ calibration ≤ 0.1

---

### Overall Classification Distribution

**Total Observations:** 400 (100 participants × 4 tests)

| Category | Count | Percentage |
|----------|-------|------------|
| Overconfident | 187 | 46.8% |
| Underconfident | 177 | 44.2% |
| Calibrated | 36 | 9.0% |

**Key Finding:** Only 9% of observations are well-calibrated (within ±0.1 theta units).

---

### Classification by Timepoint

| Test | Overconfident | Underconfident | Calibrated |
|------|---------------|----------------|------------|
| T1 | 41 (41.0%) | 51 (51.0%) | 8 (8.0%) |
| T2 | 48 (48.0%) | 45 (45.0%) | 7 (7.0%) |
| T3 | 47 (47.0%) | 45 (45.0%) | 8 (8.0%) |
| T4 | 51 (51.0%) | 36 (36.0%) | 13 (13.0%) |

**Observations:**
- Overconfident proportion increases from 41% (T1) to 51% (T4)
- Underconfident proportion decreases from 51% (T1) to 36% (T4)
- Calibrated proportion remains stable (~7-13%)

---

### Statistical Method: Wilson Score Confidence Intervals

**Why Wilson CIs?**
- Proportions are binomial data
- Wilson score method is CORRECT for binomial proportions
- Avoids asymmetry issues of normal approximation
- Handles small sample sizes (N=100) appropriately

**Formula:** Wilson score interval for p with continuity correction

**Implementation:** `step02_proportion_overconfident.csv` contains Wilson CIs for each timepoint.

---

### Design Decision Rationale

**Choice of ε=0.1:**
- Corresponds to ~0.1 theta units = "noticeable miscalibration"
- Commonly used threshold in calibration literature
- Provides balance: Not too strict (ε=0.05) nor too lenient (ε=0.2)
- Allows majority of observations to be classified as over/under (90%), highlighting rare calibration

**Alternative Thresholds Considered:**
- **ε=0.05:** Too strict, only ~2-3% calibrated
- **ε=0.2:** Too lenient, ~20% calibrated (obscures miscalibration)
- **ε=0.1:** Goldilocks (chosen)

---

### Integration with Continuous Calibration Measure

**RQ 6.2.1:** Continuous calibration (theta_confidence - theta_accuracy)
**RQ 6.2.2:** Categorical classification (overconfident/underconfident/calibrated)

**Complementary Approaches:**
- Continuous: Detects MAGNITUDE of miscalibration
- Categorical: Detects DIRECTION and MEMBERSHIP
- Both needed for complete understanding

---

**Archived from:** state.md Session (2025-12-11 20:15)
**Original Date:** 2025-12-11 20:15
**Reason:** Session archived (3+ sessions old per context-manager protocol)

---
