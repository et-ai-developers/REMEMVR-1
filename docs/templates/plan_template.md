# RQ X.Y Planning Report

**Agent:** rq_specification v3.0
**Date:** YYYY-MM-DD HH:MM
**Mode:** Planning
**Status:** awaiting_user_input

---

## My Understanding of Your Concept

**Research Question:** [Agent's interpretation of RQ from concept.md]

**Analysis Type:** [IRT + LMM / CTT / Correlation / etc.]

**Analysis Pipeline (As I Understand It):**
1. [Step 1 as agent understands it from concept.md]
2. [Step 2]
3. [Step 3]
...

**Key Variables Identified:**
- **Outcome Variable:** [What's being measured]
- **Predictor Variables:** [Primary predictor, time variable, covariates]
- **Time Structure (if longitudinal):** [Days 0, 0, 1, 6]

---

## Domain Tag Mapping

**Based on data_structure.md, I identified these domain codes for this RQ:**

| Domain | Codes from data_structure.md | concept.md mentions? | Status |
|--------|------------------------|----------------------|--------|
| What | -N- | ✅ Yes | Clear |
| Where (general) | -L- | ❓ Unclear | **Question 1** |
| Where (pick-up) | -U- | ✅ Yes | Clear |
| Where (put-down) | -D- | ✅ Yes | Clear |
| When | -O- | ✅ Yes | Clear |

**Expected Tag Patterns:**
- What items: `*-RVR-T{1,2,3,4}-*-N-*-ANS`
- Where items (if -L- included): `*-RVR-T{1,2,3,4}-*-L-*-ANS`
- Where items (pick-up): `*-RVR-T{1,2,3,4}-*-U-*-ANS`
- Where items (put-down): `*-RVR-T{1,2,3,4}-*-D-*-ANS`
- When items: `*-RVR-T{1,2,3,4}-*-O-*-ANS`

**Expected Item Counts (from data_structure.md):**
- What domain: ~18-29 items (varies by paradigm inclusion)
- Where domain: ~16-36 items (depends on -L- inclusion)
- When domain: ~16-26 items (varies by paradigm inclusion)

---

## Tools Required

**Based on tools_inventory.md, I identified these tools for your analysis steps:**

| Step | Tool Function | Available? | Notes |
|------|--------------|------------|-------|
| Step 1 | tools.analysis_irt.calibrate_grm | ✅ Yes | IRT Pass 1 |
| Step 2 | tools.analysis_irt.purify_items | ✅ Yes | Purification |
| Step 3 | tools.analysis_irt.calibrate_grm | ✅ Yes | IRT Pass 2 |
| Step 4 | pandas.DataFrame.melt | ✅ Yes | Data reshaping |
| Step 5 | tools.analysis_lmm.run_lmm_analysis | ✅ Yes | LMM fitting |
| Step 6 | tools.plotting.plot_trajectory | ✅ Yes | Trajectory plot |
| Step 7 | tools.plotting.plot_diagnostics | ✅ Yes | Diagnostic plots |

**Tool Reuse Rate:** 100% (all required tools exist)

**New Tools Required:** None ✅

---

## Questions for You (Please Answer Below)

### CRITICAL Questions (Must answer to proceed)

**Question 1: -L- Domain Tag Inclusion**

**Context:** data_structure.md lists -L- as "Spatial location of NON-interactive objects (furniture, fixtures, doors, windows)". Your concept.md mentions "Where domain" but doesn't explicitly state whether -L- tags should be included.

**The Question:** Should I include -L- tags in Where domain extraction?

**Options:**
- **Option A:** YES, include -L- tags (comprehensive Where domain coverage)
- **Option B:** NO, exclude -L- tags (focus on interactive items only: -U-, -D-)

**Your Answer:**
[Edit here - Type "A" or "B" and brief justification]

---

**Question 2: Paradigm Inclusion**

**Context:** Your concept.md mentions VR items across paradigms. data_structure.md lists 6 paradigms: RFR, IFR, TCR, ICR, RRE, IRE.

**The Question:** Which paradigms should be included in this RQ?

**Options:**
- **Option A:** All 6 paradigms (comprehensive)
- **Option B:** Interactive items only (IFR, ICR, IRE - excludes RFR, TCR, RRE)
- **Option C:** Custom subset (specify which paradigms)

**Your Answer:**
[Edit here - Type "A", "B", or "C" with paradigm list if C]

---

### CLARIFICATION Questions (Help me understand)

**Question 3: Time Transformation**

**Context:** concept.md mentions "forgetting trajectories" but doesn't specify functional form. LMM can model time as linear, quadratic, or logarithmic.

**The Question:** Should I prepare multiple time transformations and use AIC to select best model?

**Options:**
- **Option A:** Test all 5 candidate models (linear, quadratic, log, lin+log, quad+log) - select via AIC (RECOMMENDED)
- **Option B:** Linear only (simplest, assumes constant forgetting rate)
- **Option C:** Quadratic only (assumes two-phase forgetting)
- **Option D:** Logarithmic only (Ebbinghaus forgetting curve)

**Your Answer:**
[Edit here - Type "A", "B", "C", or "D"]

---

**Question 4: Effect Size Metrics**

**Context:** You expect Domain × Time interaction. For thesis writeup, effect sizes are critical.

**The Question:** Which effect size metrics should I compute?

**Options:**
- **Option A:** Cohen's f² for interaction + Cohen's d for pairwise domain differences at Day 6 (RECOMMENDED for interaction + specific comparisons)
- **Option B:** Cohen's f² only (interaction effect size)
- **Option C:** Partial η² (ANOVA-style effect size)

**Your Answer:**
[Edit here - Type "A", "B", or "C"]

---

### OPTIONAL Questions (I can make reasonable default, but confirm if important)

**Question 5: Diagnostic Plot Inclusion**

**Context:** IRT can produce Item Characteristic Curves (ICC) and Test Characteristic Curves (TCC) for model diagnostics.

**The Question:** Should I create ICC/TCC plots, or just the main trajectory plot?

**Options:**
- **Option A:** Create ICC and TCC plots (comprehensive diagnostics, ~5MB extra files)
- **Option B:** Skip ICC/TCC (focus on main result - trajectory plot only)

**Your Answer:**
[Edit here - Type "A" or "B", or leave blank for my default: B]

---

**Question 6: Validation Threshold for CFI**

**Context:** IRT model fit uses CFI (Comparative Fit Index). Traditional threshold is CFI > 0.95, but statistics_expert often recommends CFI > 0.90 for dichotomous IRT data.

**The Question:** Which CFI threshold should I use?

**Options:**
- **Option A:** CFI > 0.90 (relaxed, appropriate for dichotomous data - RECOMMENDED)
- **Option B:** CFI > 0.95 (traditional, stricter)

**Your Answer:**
[Edit here - Type "A" or "B", or leave blank for my default: A]

---

## Proposed File Structure

**I will create:**

### Core Specification Files
- `info.md` - RQ specification (10 sections, ~400-500 lines)
- `config.yaml` - Analysis parameters (IRT + LMM config, ~500-600 lines)
- `status.md` - 8-phase tracking table (embedded in info.md Section 1)

### Directory Structure
- `data/.gitkeep` - Data files (data-prep, analysis-executor)
- `code/.gitkeep` - Analysis scripts (analysis-executor)
- `plots/.gitkeep` - Visualization files (analysis-executor)
- `logs/.gitkeep` - Agent reports (all agents)
- `validation/.gitkeep` - Validation reports (scholar, statistics-expert)

### Context & Reports
- `logs/rq_spec_context.md` - My context dump (decisions, reasoning)
- `logs/rq_specification_report.md` - Final report (created after Finalization)

---

## Clarifications Needed from Reference Documents

**These points were unclear in the documents I read:**

[If agent finds ambiguities in data_structure.md, project_specific_stats_insights.md, etc., list them here as additional questions]

**Example:**
- data_structure.md shows tag pattern `{UID}-RVR-{Test}-{Section}-{Item}-{Measure}`, but some examples include room codes. Should I account for room code wildcarding?

---

## Next Steps

**Your Action:**
1. Review this plan carefully
2. Answer CRITICAL questions (Questions 1-2) - REQUIRED to proceed
3. Answer CLARIFICATION questions (Questions 3-4) - Recommended
4. Answer OPTIONAL questions (Questions 5-6) - If defaults don't work for you
5. Save this file (plan.md)
6. Tell master: "Ready for rq-spec agent Drafting mode"

**My Next Action (Drafting Mode):**
1. Read your answers in this file (plan.md)
2. Read concept.md again (refresh understanding)
3. Generate info.md with all 10 sections
4. Generate config.yaml with complete tool_functions mapping
5. Create all directories (.gitkeep files)
6. Append to logs/rq_spec_context.md (document Drafting phase decisions)
7. Report back to master

---

**Estimated Time:**
- Your review + answer: ~10-15 minutes
- My drafting: ~5 minutes
- Total: ~15-20 minutes for Planning + Drafting

---

**END OF PLANNING REPORT**

---

## YOUR ANSWERS (Edit Below)

**Answer to Question 1 (-L- inclusion):**
[Type A or B, and brief justification]

**Answer to Question 2 (Paradigms):**
[Type A, B, or C with list if C]

**Answer to Question 3 (Time transformation):**
[Type A, B, C, or D]

**Answer to Question 4 (Effect sizes):**
[Type A, B, or C]

**Answer to Question 5 (Diagnostic plots):**
[Type A or B, or leave blank for default]

**Answer to Question 6 (CFI threshold):**
[Type A or B, or leave blank for default]

---

**Additional Comments/Questions for Agent:**
[If you have clarifications or additional instructions, write them here]
