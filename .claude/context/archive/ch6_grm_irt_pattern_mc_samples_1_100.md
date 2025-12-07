# ch6_grm_irt_pattern_mc_samples_1_100

**Topic Description:** GRM IRT calibration pattern using mc_samples=1 for fitting (fast convergence) and mc_samples=100 for scoring (accurate theta estimates). Pattern originated in Ch5 RQ 5.5.1, applied successfully to Ch6 RQs. Prevents 7000+ epoch hangs.

---

## GRM mc_samples Pattern - Fast Fitting, Accurate Scoring (2025-12-06 22:00)

**Context:** During RQ 6.1.1 execution, initial mc_samples=10 caused convergence issues (7000+ epochs without completion). Switching to mc_samples=1 for fitting and mc_samples=100 for scoring resolved the issue.

**Archived from:** state.md (Session 2025-12-06 22:00)
**Original Date:** 2025-12-06 22:00
**Reason:** Pattern established, applies to all Ch6 GRM calibrations

---

### The Pattern

**For GRM IRT Calibration:**

1. **Fitting phase:** `mc_samples=1`
   - Fast convergence (~35k epochs in ~2 min)
   - Learns item parameters efficiently
   - Minimal Monte Carlo integration needed during optimization

2. **Scoring phase:** `mc_samples=100`
   - Accurate theta estimates
   - Higher precision for final scores
   - Used when generating theta.csv outputs

---

### Origin

**Pattern discovered in Ch5 RQ 5.5.1:**
- First encountered convergence issues with mc_samples=10
- Experimented with mc_samples=1 for fitting
- Confirmed accurate scoring requires mc_samples=100
- See archived topic: `rq_5.5.1_complete_production_execution.md`

---

### Why It Works

**Fitting (mc_samples=1):**
- Item parameters determined by gradient descent optimization
- Monte Carlo integration is auxiliary computation during optimization
- Lower mc_samples → faster per-epoch computation
- Optimizer still converges to correct parameters

**Scoring (mc_samples=100):**
- Theta estimation requires numerical integration over latent trait distribution
- Higher mc_samples → more accurate numerical approximation
- Only computed once (not per-epoch), so runtime acceptable

---

### Application to RQ 6.1.1

**Before fix:**
- mc_samples=10 (default)
- 7000+ epochs without convergence
- Session would have timed out

**After fix:**
- mc_samples=1 for fitting
- Converged at ~35k epochs in ~2 minutes
- mc_samples=100 for scoring
- All 72 items calibrated successfully

---

### Status

**Pattern confirmed for Ch6 GRM calibrations.**

This setting should be used for all future Ch6 RQs using GRM (6.1.1, 6.3.1, 6.4.1, etc.).

---
