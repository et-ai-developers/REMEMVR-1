# RQ X.Y Concept

**Author:** [Your name]
**Date:** YYYY-MM-DD
**RQ ID:** X.Y

---

## What I Want to Study (In My Words)

[Explain the research question in plain language, as if explaining to a colleague who knows your study design but not this specific analysis]

**Example:**
"I want to know if people forget object identity (What), spatial locations (Where), and temporal order (When) at different rates across the 6-day testing period. I expect What to be most resilient because it can rely on familiarity, while Where and When require more hippocampal binding."

---

## Key Variables

### Outcome Variable
**Variable:** [What you're measuring, e.g., "Episodic memory performance"]
**Operationalization:** [How it's measured, e.g., "IRT ability estimates (theta scores) from VR test items"]

### Predictor Variables
**Primary Predictor:** [Main variable of interest, e.g., "Memory domain (What/Where/When)"]
**Time Variable (if longitudinal):** [e.g., "Days since encoding (0, 0, 1, 6)"]
**Covariates (if any):** [e.g., "Age, RAVLT scores"]

---

## Memory Domains

**Which WWW domains does this RQ use?**

- [ ] **What** (object identity, -N- tags)
- [ ] **Where** (spatial location)
  - [ ] -L- tags (general location, legacy)
  - [ ] -U- tags (pick-up location)
  - [ ] -D- tags (put-down location)
- [ ] **When** (temporal order, -O- tags)

**Special considerations:**
[E.g., "Include ALL Where tags (-L-, -U-, -D-) because some items only have -L-"]
[E.g., "Exclude -L- because this RQ focuses on interactive items only (pick-up/put-down)"]

---

## Analysis Approach (High Level)

**Analysis Type:** [e.g., IRT + LMM, CTT only, Correlation, ANOVA, Descriptive statistics]

**Step 1:** [First analysis step, e.g., "IRT Pass 1 - Calibrate GRM on all VR items"]
**Step 2:** [Second step, e.g., "Purification - Remove items with |b|>3.0 or a<0.4"]
**Step 3:** [Third step, e.g., "IRT Pass 2 - Re-calibrate on purified items"]
**Step 4:** [Fourth step, e.g., "LMM - Model trajectories with Domain × Time interaction"]

**Special Methods:**
[Anything unusual? E.g., "Use quadratic + log time terms because forgetting is nonlinear"]

---

## Expected Pattern (Hypothesis)

**Hypothesis:** [What you expect to find]

**Example:**
"I expect a Domain × Time interaction where What shows slowest forgetting (shallow slope), Where intermediate, and When fastest forgetting (steep slope). Divergence should increase after Day 1 (consolidation period)."

**Theoretical Basis:** [Why do you expect this pattern?]

**Example:**
"Dual-process theory suggests What can rely on familiarity (perirhinal cortex), while Where and When require hippocampal binding. Consolidation theory predicts hippocampal-dependent memories are more vulnerable during consolidation."

---

## Data Inclusion/Exclusion

**Participants:**
- [ ] All 100 participants
- [ ] Subset: [Specify criteria, e.g., "Participants with ≥3 test sessions"]
- [ ] Exclude: [Specify criteria, e.g., "Participants with >30% missing VR data"]

**Items:**
- [ ] All VR items
- [ ] Subset: [Specify, e.g., "Only interactive items (IFR, ICR, IRE)"]
- [ ] Exclude: [Specify, e.g., "Room Free Recall (RFR) items"]

**Tests:**
- [ ] All 4 tests (T1, T2, T3, T4)
- [ ] Subset: [Specify, e.g., "Tests 1, 3, 4 only (exclude T2 - same day as T1)"]

---

## Special Considerations

**Anything unusual about this RQ?**

[Examples:]
- "This RQ uses 2-pass IRT purification (mandatory per Decision D039)"
- "This RQ compares recognition vs recall paradigms (need separate IRT models)"
- "This RQ includes age as covariate (need to extract DEM-X-Age)"
- "This RQ uses raw sum scores (CTT), not IRT"

---

## My Questions/Uncertainties

[List anything YOU'RE uncertain about before the rq-spec agent starts planning]

**Example:**
"Should I model time as linear, quadratic, or logarithmic? Or test all three and select via AIC?"

---

## References to Existing Documentation

**This RQ is based on:**
- [ ] ANALYSES_CH5.md (RQ 5.X)
- [ ] ANALYSES_CH6.md (RQ 6.X)
- [ ] ANALYSES_CH7.md (RQ 7.X)

**Relevant prior RQs (if any):**
[E.g., "Similar to RQ 5.3, but focuses on When domain only"]

---

**END OF CONCEPT TEMPLATE**

**Instructions for Use:**
1. Copy this template to `results/chX/rqY/concept.md`
2. Fill in all sections with your understanding of the RQ
3. Be specific about domain tags (Which -L-, -U-, -D- tags to include?)
4. Describe analysis steps in your own words (agent will formalize)
5. List any uncertainties you have (agent may address in plan.md questions)
6. Save and close - ready for rq-spec agent Planning Mode
