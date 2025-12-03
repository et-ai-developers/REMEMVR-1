# RQ 5.5.1: Source-Destination Trajectories

**Chapter:** 5
**Type:** Source-Destination
**Subtype:** Trajectories (ROOT RQ for Type 5.5)
**Full ID:** 5.5.1

---

## Research Question

**Primary Question:**
Do pick-up locations (source: -U-) and put-down locations (destination: -D-) show different forgetting trajectories in VR episodic memory?

**Scope:**
This RQ examines spatial memory for interactive object locations, comparing memory for WHERE an item was picked up (source) vs WHERE it was placed (destination). Data structure: N=100 participants × 4 test sessions × 36 items (6 interactive items × 3 paradigms × 2 location types). Time variable uses TSVR (actual hours since encoding). This is a ROOT RQ that establishes the baseline for all Type 5.5 analyses.

**Theoretical Framing:**
This analysis tests whether source and destination spatial memories show differential forgetting. Unlike static object locations (-L-), interactive items require encoding TWO spatial locations per object: where it was picked up (source) and where it was placed (destination). Goal-directed action theory and action-effect binding predict that destinations (the goal/effect of the action) should be encoded more strongly than sources (the starting point).

---

## Theoretical Background

**Relevant Theories:**

1. **Action-Effect Binding (Schreiner & Kunde, 2024; Elsner & Hommel, 2001):**
   Actions become bound to their sensory effects. The destination location represents the ACTION EFFECT (seeing the object in its new position), which is more salient than the action's starting point. This predicts destination > source memory.

2. **Goal-Directed Action (Peng et al., 2024; J Neurosci, 2023):**
   Goal-directed behavior prioritizes end-states over initial conditions. In VR object manipulation, the destination IS the goal—participants decide WHERE to place the object, directing attention and cognitive resources to that location. Sources are merely starting points with no goal relevance.

3. **Prospective vs Retrospective Memory (Gopie & Craik, 2020):**
   Destination memory (where I PUT something) is prospective—tied to future retrieval. Source memory (where I GOT something) is retrospective—tied to past events. Prospective encoding may be stronger due to goal-relevance.

4. **Temporal Order Effects:**
   Pick-up always precedes put-down for each item. Recency effects favor destination memory; primacy effects favor source memory. VR research suggests recency dominates in immersive spatial contexts (Plancher et al., 2018).

5. **Motor Planning Depth:**
   Put-down actions involve active DECISION-MAKING (where to place the object), requiring deeper encoding. Pick-up actions are reactive (object already in a fixed location), requiring less deliberate processing.

**Key Citations:**
- Schreiner, T., & Kunde, W. (2024). The role of compatibility in long-term action-effect binding. Memory & Cognition.
- Peng, Y., et al. (2024). Perceptual-cognitive integration for goal-directed action. J Neurosci, 43(45), 7511.
- Gopie, N., & Craik, F. I. (2020). Developmental trends in children's source and destination memory. J Exp Child Psychol.
- Plancher, G., et al. (2018). Use of immersive VR to assess episodic memory. Neuropsychological Rehabilitation.
- Elsner, B., & Hommel, B. (2001). Effect anticipation and action control. J Exp Psychol: HPP.

**Literature Gap:**
No prior VR studies have examined source vs destination spatial memory for interactive objects in a longitudinal forgetting design. Source-destination distinctions have been studied in developmental psychology (Gopie & Craik) but not in adult forgetting trajectories or VR contexts. This is theoretically novel.

---

## Hypothesis

**Primary Hypothesis:**
Destination memory (-D-) will show HIGHER accuracy than source memory (-U-) across all timepoints (main effect of location type).

**Predicted Direction:** -D- > -U- (destination BETTER than source)

**Effect Size Expectation:** Small-to-medium (d = 0.20-0.40), based on the subtle nature of the encoding manipulation.

**Secondary Hypotheses:**
1. The -D- vs -U- difference may NOT interact with time (parallel forgetting curves, just different intercepts)
2. Logarithmic model will provide best fit (consistent with all other Type X RQs)
3. If an interaction exists, -D- may show SLOWER forgetting (stronger initial encoding → more durable trace)

**Theoretical Rationale:**
Destination locations are encoded during goal-directed action with active decision-making (WHERE should I place this?). Source locations are encoded passively during object identification (the object happens to be HERE). Goal-directed encoding with decision-making produces stronger, more elaborated memory traces. This predicts destination > source memory.

---

## Analysis Approach

**Design:**
- Factor: Location Type (2 levels: -U- source, -D- destination)
- Time: TSVR (continuous, hours since encoding)
- Random effects: (1 + log_TSVR | UID) or (1 | UID) based on convergence

**Statistical Tests:**
1. Model selection (5 functional forms per ROOT RQ protocol)
2. Main effect of location type (Source vs Destination)
3. Location Type × Time interaction (differential forgetting)
4. AIC-based model comparison

**Data Requirements:**
- IRT theta scores from Pass 2 calibration (must calibrate -U- and -D- separately)
- OR: Raw accuracy scores if IRT calibration unavailable for this subset
- 36 items total: 18 -U- items + 18 -D- items

**Critical Decisions:**
- **D065:** Use IRT theta if calibration succeeds; otherwise CTT with n=36 items
- **D070:** TSVR (actual hours) as time metric
- **D068:** Dual p-values (raw + Bonferroni)

---

## Expected Outcomes

**Primary expectation:** Significant main effect of location type, with -D- > -U- accuracy

**If destination > source (confirmed):**
- Validates action-effect binding and goal-directed action theories in VR
- Demonstrates REMEMVR CAN detect meaningful dissociations
- Balances null findings from domains/paradigms/schemas (shows sensitivity)
- Provides theoretical contribution on ecological memory encoding
- First VR study to demonstrate source-destination dissociation in forgetting

**If null (source = destination):**
- Adds to universal null pattern across all factor structures
- Strengthens "laboratory artifacts dissolve in ecological encoding" thesis narrative
- Suggests VR binding creates unified traces even for sequential actions
- Either outcome is interpretable and valuable

**If source > destination (opposite to prediction):**
- Would suggest primacy effects dominate over goal-relevance
- Would require theoretical reinterpretation
- Still demonstrates REMEMVR sensitivity (detecting a dissociation)

---

## Interpretation Guidelines

**Scenario 1: Destination > Source (main effect, no interaction)**
- Interpretation: Goal-directed encoding creates stronger baseline memory
- Forgetting rates equivalent, just different starting points
- Thesis contribution: VR detects action-effect binding dissociation

**Scenario 2: Destination > Source (main effect + interaction: -D- slower forgetting)**
- Interpretation: Stronger encoding leads to more durable consolidation
- Thesis contribution: Encoding depth affects both acquisition AND retention

**Scenario 3: Destination = Source (null)**
- Interpretation: VR binding unifies source-destination into single trace
- Consistent with Chapter 5 null pattern
- Thesis contribution: Extends "laboratory dissociations dissolve" narrative

**Scenario 4: Source > Destination**
- Interpretation: Primacy effects dominate; object identification context aids retention
- Would contradict goal-directed action predictions
- Requires careful examination of confounds (task demands, counterbalancing)

---

## Limitations

1. **Temporal Confound:** Pick-up ALWAYS precedes put-down. Cannot fully disentangle location type from temporal position. Primacy vs recency effects confounded with source vs destination.

2. **Task Structure:** The VR task may create unique encoding conditions not generalizable to real-world source-destination memory.

3. **Item Count:** Only 18 items per factor level. If IRT calibration fails, CTT reliability may be marginal (α potentially < 0.70).

4. **Practice Effects:** 4 test sessions may produce strategy changes that affect source vs destination differentially.

5. **VR-Specific Effects:** HMD vs desktop, embodiment, cybersickness could interact with spatial memory encoding.

---

## Dependencies

**Upstream:**
- IRT calibration of -U- and -D- items (or raw data from master.xlsx)
- Purified item list from parent calibration (if using IRT)

**Downstream (depends on 5.5.1):**
- 5.5.2 (Consolidation): Uses best-fit model from 5.5.1
- 5.5.3 (Age Effects): Uses best-fit model from 5.5.1
- 5.5.4 (IRT-CTT): Validates 5.5.1 findings
- 5.5.5 (Purified CTT): Uses purified items from 5.5.1
- 5.5.6 (Variance): Uses LMM from 5.5.1
- 5.5.7 (Clustering): Uses random effects from 5.5.6

---

## Notes

**Strategic Purpose:**
This analysis was specifically added to demonstrate that REMEMVR CAN detect meaningful memory dissociations when they exist. The null pattern across Chapter 5 (domains, paradigms, schemas) is theoretically important but could raise validity concerns. Finding a positive effect for source-destination would strengthen the thesis argument.

**Data Subsetting:**
- Must filter to interactive items only (i1-i6)
- Must filter to paradigms with -U-/-D- domains (IFR, ICR, IRE)
- Must exclude RFR, TCR, RRE (no interactive items)

**IRT Considerations:**
- May need separate calibration for -U- and -D- items
- With only 18 items per factor level, unidimensional IRT may be marginal
- Fallback: Use raw accuracy (CTT) if IRT doesn't converge

**Theoretical Contribution:**
This RQ bridges action-effect binding literature (Elsner & Hommel, 2001; Schreiner & Kunde, 2024) with episodic memory forgetting research. No prior study has examined whether action-effect binding advantages persist across multi-day retention intervals. If destination memory is more durable, this has implications for VR training design (emphasize placement decisions, not just object identification).
