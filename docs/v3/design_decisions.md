# Design Decisions & Rationale

**Last Updated:** 2025-01-11
**Purpose:** Documents key architectural and methodological design decisions
**Audience:** Main claude when questioning design choices
**Status:** Current

---

## KEY DESIGN DECISIONS & RATIONALE

### Why Composite_ID stacking?
**IRT Requirements:** Need large sample sizes (ideally 500+ responses per item)

**Solution:** Stack all 4 tests into one IRT model as if 400 different people took the same test once.

**Trade-off:** Assumes item parameters don't change over time (reasonable for VR stimuli).

### Why dichotomous scoring?
**Problem:** Temporal order questions with partial credit (0.5 for off-by-1) created uneven scoring.

**Solution:** Use dichotomous scoring (0 or 1 only) for most analyses. Some spatial questions may retain 0.5 for adjacent locations.

### Why agent-based architecture?
**Problems with old pipeline:**
1. Hard to verify correctness of individual analyses
2. Bulk processing makes debugging difficult
3. Results not organized by research question
4. No systematic validation

**Solution:** One RQ at a time, with validation at each step, full audit trail.
