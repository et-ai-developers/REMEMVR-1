# Chapter 6 Execute.md Protocol Updates

Archive of runtime fixes and execution protocol updates for Chapter 6 RQ execution.

---

## Critical Runtime Fixes (2025-12-07 11:00)

**Context:** During RQ 6.3.1 execution (Steps 00-05), identified 3 critical runtime issues that required protocol updates in `results/ch6/execute.md`.

### Fix #1: IRT Background Process Management

**Problem:** Polling IRT epoch status repeatedly blows up context window
- Each status check adds 50-100 tokens
- 7000 epochs × repeated checks = 350k-700k tokens
- Causes API quota exhaustion and context overflow

**Solution:** DON'T poll epoch status during fitting
- Start process in background
- Let it run without interruption
- Check only ONCE at expected completion time
- Use log file timestamps to verify progress if needed

**Added to execute.md:** Warning about epoch polling antipattern

### Fix #2: Flush Pattern for log() Functions

**Problem:** Log messages buffer in memory, not visible in real-time
- Can't monitor progress of long-running processes
- Debugging requires waiting for full completion
- No feedback during multi-minute IRT fitting

**Solution:** Implement flush pattern in all logging
```python
def log(msg, f=None):
    print(msg, flush=True)  # Immediate stdout visibility
    if f:
        f.write(msg + '\n')
        f.flush()  # Immediate file visibility
```

**Added to execute.md:** Standard logging pattern for all generated code

### Fix #3: MINIMUM Settings for Code Validation

**Problem:** First runs with production settings (mc_samples=10000) take 30-60 minutes
- Too long to validate code correctness
- Wastes time if bugs exist
- Delays debugging cycle

**Solution:** Two-phase execution strategy
1. **Validation phase:** mc_samples=1, iw_samples=1 (completes in 2-7 min)
   - Validates code structure
   - Tests data flow
   - Confirms convergence
   - Catches bugs quickly
2. **Production phase:** mc_samples=10000, iw_samples=50 (run after validation)
   - Only run once code validated
   - Generate publication-quality parameters

**Added to execute.md:** MINIMUM settings specification for all IRT steps

**Archived from:** state.md Session 2025-12-07 11:00
**Original Date:** 2025-12-07 11:00
**Reason:** Session 3+ old, protocol updates documented in execute.md

**Note:** These patterns continue to be used in RQ 6.4.1 and future Chapter 6 RQs.

---
