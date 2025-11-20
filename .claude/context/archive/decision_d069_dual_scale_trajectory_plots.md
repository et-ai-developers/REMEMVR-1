# Decision D069: Dual-Scale Trajectory Plots - Historical Archive

**Topic:** Dual-scale trajectory plotting requirement (theta + probability scales) for interpretability
**Time Period:** 2025-11-14 evening
**Status:** Complete (validated with rq-spec agent testing)

---

## Decision D069: Dual-Scale Trajectory Plots (2025-11-14 Evening)

**User Request:** "I find LMM plots where ability is on y-axis kind of abstract to conceptualize. Any time we are plotting trajectories of ability, can we convert it back to probability and plot that as well."

**Problem Identified:**
- Theta scale (-3 to +3) is abstract for readers unfamiliar with IRT
- "theta = 0.5" is harder to grasp than "60% probability correct"
- Thesis has mixed audience (psychometricians prefer theta, neuroscientists prefer percentages)
- Clinical relevance requires accessible metrics

**Solution: Decision D069 (2025-11-14) - Dual-Scale Trajectory Plots**

**Implementation:**
1. **Primary plot:** Theta scale (y-axis: -3 to +3) for statistical rigor
2. **Companion plot:** Probability scale (y-axis: 0-100%) for interpretability
3. **Transformation formula:** `probability = 1 / (1 + np.exp(-(discrimination * (theta - difficulty))))`
   - Use mean discrimination from Pass 2 IRT items
   - Use b = 0 (typical difficulty reference)

**Archived from:** state.md
**Original Date:** 2025-11-14 evening
**Reason:** Decision documented, tested with rq-spec agent, ready for production use

---

### Documentation Added

**File 1: project_specific_stats_insights.md (+245 lines)**
- Complete Decision D069 section (lines 410-653)
- Problem statement (theta abstract vs probability intuitive)
- Solution (dual-scale plotting with IRT transformation)
- Implementation steps (4-step Python workflow)
- Example interpretation (theta 0.45→0.25 = 66%→57% probability)
- Implementation requirements for info.md and config.yaml
- Validation checklist (7 items)
- Why project-specific (clinical relevance, mixed audience)
- Common misunderstandings section
- Updated Updates Log (line 679)

**File 2: docs_index.md (1 entry updated)**
- Updated project_specific_stats_insights.md Purpose and Key Topics to include Decision D069

**File 3: results/ch5/rq1/concept.md (3 edits)**
- Added Step 8: Dual-scale trajectory plots with transformation formula
- Added Special Methods bullet: Dual-scale plotting rationale
- Added Question 6: Trajectory plot y-axis scale (RESOLVED with Decision D069)

---

### Testing Decision D069

**Method:**
- Deleted plan.md to force agent re-generation
- Invoked rq-specification agent Planning Mode (second invocation)

**Agent Detection:**
- Agent successfully detected Decision D069 from updated project_specific_stats_insights.md
- Agent incorporated D069 in 6 sections of plan.md:
  - Circuit Breaker Check 3 (D069 compliance verification)
  - Analysis Pipeline Step 8 (dual-scale plotting detailed)
  - Key Specification Decision 8 (resolved decision documented)
  - Tools Required Table (Step 8B added)
  - config.yaml Preview (trajectory_plots.probability_scale section)
  - Explicit Verification Section (test objective evidence)

**Test Result:** PASSED

---

### Impact

**Scope:** All 50 RQs with trajectory plots showing theta over time

**Benefits:**
- Enhances interpretability for mixed audiences
- Preserves statistical rigor (theta-scale primary)
- Increases clinical relevance (probability-scale companion)
- Transparent methodology (both scales reported)

**Implementation Requirements:**
- Mandatory for ALL RQs with trajectory plots
- rq-specification agent will read Decision D069 and include dual-scale plotting in info.md
- Analysis-executor agent will generate both plots
- Results will show both theta and probability trajectories side-by-side

---
