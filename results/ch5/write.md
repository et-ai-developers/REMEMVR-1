# Thesis Chapters 4 & 5 Writing System

**EXECUTION PARADIGM:** /clear → Read write.md → Execute → /clear (NO /save, NO /refresh, stateless sessions)

**OUTPUT:** Two polished PhD thesis chapters:
1. **Chapter 4 (chapter_4_analysis.md):** Statistical methods consolidated across all RQs
2. **Chapter 5 (chapter_5_empirical.md):** Empirical results organized by theoretical themes

**CONTEXT:** REMEMVR = VR episodic memory study. N=100, 4 test sessions over 6 days, What/Where/When domains, IRT-calibrated theta scores. 35 RQs total (5.1.1-5.5.7).

---

## Session Startup Protocol

```bash
# 1. Clear context window
/clear

# 2. Read these 3 files (load order matters):
Read: /home/etai/projects/REMEMVR/results/ch5/write.md          # This file (instructions)
Read: /home/etai/projects/REMEMVR/results/ch5/notepad.md        # Progress tracker
Read: /home/etai/projects/REMEMVR/thesis/methods.md             # Experimental context

# 3. Determine current task from notepad.md "Progress Tracker"
# 4. Execute task per instructions below
# 5. Update notepad.md with TERSE progress notes
# 6. User runs /clear when session complete
```

**Token budget per session:** Aim for 80-120k tokens. When approaching 140k, stop gracefully and update notepad.md.

---

## Chapter 4 Architecture (Analysis Methods)

**File:** `results/ch5/chapter_4_analysis.md`

**Purpose:** Consolidated statistical methodology. Avoid repetition across 35 RQs by describing general methods once.

**Structure:**

```markdown
# Chapter 4: Statistical Analysis

## 4.1 Overview of Analytic Strategy

[200-300 words: Multi-stage analysis pipeline, why IRT+LMM, dealing with repeated measures]

## 4.2 Item Response Theory (IRT) Calibration

### 4.2.1 Graded Response Model (GRM)
- Model specification (Samejima, 1969)
- Estimation method (marginal maximum likelihood)
- Convergence criteria
- Output: Theta scores + SE

### 4.2.2 Item Purification Protocol (Decision D039)
- Rationale: Exclude poor-quality items before analysis
- Criteria: a ≥ 0.4 (discrimination), |b| ≤ 3.0 (difficulty)
- Two-pass calibration:
  - Pass 1: All items → flag low quality
  - Pass 2: Purified items only → final theta estimates
- Retention rate expectations: 40-70% typical

### 4.2.3 Dimensionality Considerations
- Omnibus factor "All": Aggregates What/Where/When domains
- Domain-specific factors: Separate calibrations per domain
- Justification: Different RQs require different granularity

## 4.3 Linear Mixed Models (LMM)

### 4.3.1 Model Specification
- Fixed effects: Research-question specific (time, age, domain, etc.)
- Random effects: Random intercepts by participant (UID)
- Rationale: Accounts for within-subject correlation across test sessions
- Estimation: REML=True (parameter estimation), REML=False (model comparison via AIC)

### 4.3.2 Model Comparison Procedures
- Information criteria: AIC (penalized likelihood)
- Delta AIC interpretation: ΔAIC < 2 (competitive), 2-10 (weak support), >10 (essentially no support)
- Akaike weights: Relative probability of each model being best in candidate set
- Model averaging: Recommended when best model weight < 0.90

### 4.3.3 Assumption Checking
- Residual normality: Q-Q plots, Shapiro-Wilk test
- Homoscedasticity: Residual vs fitted plots, Levene's test
- Independence: Autocorrelation function (ACF) for temporal data
- Multicollinearity: VIF < 5 for predictors
- Convergence: Singular covariance matrices, gradient warnings

## 4.4 Effect Size Reporting

### 4.4.1 Standardized Effect Sizes
- Cohen's d: Mean difference / pooled SD (small=0.2, medium=0.5, large=0.8)
- Cohen's f²: R²/(1-R²) (small=0.02, medium=0.15, large=0.35)
- Partial η²: SS_effect / (SS_effect + SS_error)

### 4.4.2 LMM-Specific Effect Sizes
- Intraclass correlation (ICC): σ²_between / (σ²_between + σ²_within)
- Marginal R² (R²_m): Variance explained by fixed effects
- Conditional R² (R²_c): Variance explained by fixed + random effects

## 4.5 Multiple Comparisons Corrections

### 4.5.1 Bonferroni Correction (Decision D068)
- Applied when: Multiple pairwise comparisons within single RQ
- Adjusted α: α_adj = α / k (k = number of comparisons)
- Dual reporting: Report both uncorrected and Bonferroni-corrected p-values

### 4.5.2 False Discovery Rate (FDR)
- Applied when: Exploratory analyses with many tests
- Method: Benjamini-Hochberg procedure
- Threshold: q < 0.05 (expected 5% false discoveries)

## 4.6 Missing Data Handling

[Note: REMEMVR has 0% missing data post-IRT calibration. Section brief.]

- Participant-level exclusions: Insufficient effort (n=3 during data collection)
- Item-level exclusions: IRT purification (35% of items typical)
- No imputation needed: All retained participants completed all test sessions

## 4.7 Software and Reproducibility

- IRT calibration: mirt package (R 4.X) or PyIRT (Python 3.X) [specify from logs]
- LMM estimation: statsmodels (Python) or lme4 (R) [specify from logs]
- Visualization: matplotlib + seaborn (Python)
- Reproducibility: All analysis code available at github.com/rememvr/analysis

---
```

**Building Chapter 4:**

When context_finder returns ANALYSIS section for an RQ:
1. **Extract method details** (GRM specs, LMM formula, purification criteria)
2. **Check notepad.md Analysis Method Catalog** - Is this method already documented?
   - **YES:** Note RQ uses this method (update catalog), skip writing to Ch4
   - **NO:** Add method description to appropriate Ch4 section, update catalog
3. **Avoid redundancy:** Don't repeat "2-pass GRM with a≥0.4" 20 times. Say once in Ch4, reference in Ch5.

---

## Chapter 5 Architecture (Empirical Results)

**File:** `results/ch5/chapter_5_empirical.md`

**Purpose:** Narrative thesis chapter. Organized by theoretical themes, not procedural order. Reader should understand story, not just statistics.

**Structure:**

```markdown
# Chapter 5: Empirical Results

## 5.0 Introduction

[300-500 words]
- REMEMVR goals: Characterize VR episodic memory forgetting across 6 days
- Three core questions:
  1. What is functional form of forgetting? (§5.1)
  2. Do What/Where/When domains differ? (§5.2)
  3. Do age and cognition predict memory? (§5.3)
  4. Do encoding factors matter? (§5.4)
  5. Does consolidation/sleep matter? (§5.5)
- Roadmap: 35 RQs organized into 5 thematic sections
- Methodological note: Statistical details in Chapter 4, empirical patterns here

## 5.1 Functional Form and Individual Differences in Forgetting Trajectories

[Section introduction: 150-200 words]
- Why functional form matters: Different forms imply different mechanisms
- Theoretical candidates: Linear (trace decay), Logarithmic (Ebbinghaus), Power-law (Wixted)
- Individual differences: Do all people forget the same way?

### 5.1.1 Functional Form of Forgetting Trajectories

**Research Question:** Which functional form best describes episodic forgetting across 6 days?

**Hypothesis:** Logarithmic model (Ebbinghaus, 1885).

**Analysis:** (§4.2.2, §4.3.2) [cross-reference to Chapter 4 methods]
- Sample: N=100, 400 obs
- IRT: 2-pass GRM, 68/105 items retained (see §4.2.2 for purification protocol)
- LMM: 5 candidate models compared via AIC (see §4.3.2 for model comparison procedures)

**Results:**
Logarithmic model best fit (AIC=873.71, weight=0.48), Lin+Log competitive (ΔAIC=0.84, weight=0.32). Memory declined 1.18 SD over 6 days (θ: 0.67→-0.51), with rapid early forgetting (Day 0-1: 0.55 SD) then asymptotic leveling (Day 3-6: 0.25 SD). Supports Ebbinghaus forgetting curve.

[Continue with interpretation, cross-references to related RQs, theoretical implications]

**Figure 5.1.1:** [path] [caption]

---

### 5.1.2 [Next RQ]

[Same structure: RQ → Hypothesis → Brief analysis note with Ch4 refs → Results → Figures]

---

## 5.2 Domain-Specific Forgetting Patterns

[Section intro explaining Why domains matter]

### 5.2.1 [First domain RQ]
### 5.2.2 [Second domain RQ]
...

---

## 5.3 Age and Cognitive Predictors of Memory Performance

[Section intro]

### 5.3.1 [First age RQ]
...

---

## 5.4 Encoding Factors and Schema Effects

[Section intro]

### 5.4.1 [First encoding RQ]
...

---

## 5.5 Consolidation and Sleep-Dependent Memory

[Section intro]

### 5.5.1 [First sleep RQ]
...

---

## 5.6 Chapter Summary

[500-800 words synthesizing across all 35 RQs]

- **Major findings:** Bullet list of 10-12 key results
- **Convergent evidence:** Where multiple RQs triangulate
- **Divergent evidence:** Contradictions or unexpected null results
- **Theoretical implications:** What does this mean for episodic memory theory?
- **Methodological insights:** What did VR paradigm reveal?
- **Limitations:** Cross-cutting issues (floor effects, short retention, omnibus IRT)
- **Bridge to discussion:** Preview Chapter 6 integration with literature

---
```

**Building Chapter 5:**

When context_finder returns RESULTS section for an RQ:
1. **Determine placement:** Which thematic section (5.1-5.5)?
2. **Write section intro** (if first RQ in that section): Explain why this theme matters
3. **Format RQ entry:**
   - Research question (1 sentence)
   - Hypothesis (1 sentence)
   - Analysis note: Brief specs + cross-ref to Ch4 (e.g., "§4.2.2, §4.3.1")
   - Results: Narrative paragraph(s), integrate statistics naturally
   - Figures: Path + publication-quality caption
4. **Cross-reference:** Link to related RQs (e.g., "These findings converge with RQ 5.2.2")
5. **Update notepad.md:** Log RQ complete, note cross-RQ patterns

---

## Workflow: Processing One RQ

**Standard sequence for each RQ (5.1.1 through 5.5.7):**

```
1. Invoke context_finder:
   Prompt: "Extract ALL statistical findings for RQ X.X.X from:
           - results/ch5/X.X.X/docs/1_concept.md (RQ, hypothesis, theory)
           - results/ch5/X.X.X/results/summary.md (statistics, model fit, effects)
           - results/ch5/X.X.X/plots/*.png (figure paths)

           Return 3 sections: ANALYSIS, RESULTS, PLOTS
           Preserve all numerical values exactly."

2. Process ANALYSIS section:
   - Extract method specs (GRM params, LMM formula, purification)
   - Check notepad.md Analysis Method Catalog
   - If NEW method → Add to chapter_4_analysis.md + update catalog
   - If EXISTING method → Just update catalog with RQ number, skip Ch4

3. Process RESULTS section:
   - Determine thematic placement (5.1, 5.2, 5.3, 5.4, or 5.5)
   - Write section intro if first RQ in section
   - Format RQ entry in chapter_5_empirical.md:
     * RQ + hypothesis (terse)
     * Analysis cross-ref to Ch4 (e.g., "§4.2.2")
     * Results narrative (integrate stats naturally)
     * Cross-refs to related RQs
   - Add figures with captions

4. Process PLOTS section:
   - Embed figure paths in Ch5
   - Write publication-quality captions
   - Connect plot to results interpretation

5. Update notepad.md:
   - Mark RQ complete in Progress Tracker
   - Log any cross-RQ patterns discovered
   - Note if method catalog updated

6. Check token budget:
   - If > 140k tokens → Stop, update notepad, tell user to /clear
   - Otherwise → Ask user: "RQ X.X.X complete. Continue to next RQ?"
```

---

## Cross-Session Continuity (Stateless Design)

**Problem:** After /clear, I forget everything.

**Solution:** notepad.md persistence

**What notepad.md tracks:**
- **Progress:** Which RQs completed, which in progress
- **Method catalog:** Which analysis methods documented in Ch4 (avoid duplication)
- **Patterns:** Cross-RQ themes discovered (e.g., "Temporal items consistently low discrimination")
- **Blockers:** Questions for user, missing data, ambiguities

**Session startup logic:**
```
IF notepad.md says "In Progress: 5.2.3":
  → Resume RQ 5.2.3 (re-invoke context_finder if needed)
ELSE IF notepad.md says "Completed: 5.1.1-5.1.7":
  → Start next RQ: 5.2.1
ELSE IF notepad.md says "Blocker: Missing summary.md for 5.3.2":
  → Ask user about blocker, resolve, continue
```

**Notepad discipline:**
- **TERSE:** "RQ 5.1.1 done. Log forgetting. GRM 2-pass." NOT "I have completed Research Question 5.1.1 which examined logarithmic forgetting trajectories..."
- **DELETE:** Once info incorporated into write.md or chapters, delete from notepad
- **PRUNE:** If notepad > 5k tokens, ruthlessly trim old session logs, keep only active info

---

## Quality Standards

**Chapter 4 (Analysis):**
- [ ] Every method used in ANY RQ is documented exactly once
- [ ] Cross-references from Ch5 to Ch4 work (§4.X.X format)
- [ ] No redundant repetition of "2-pass GRM" or "REML=False" across RQs
- [ ] Assumption checks, effect sizes, model comparison procedures all covered
- [ ] Reads like methods section of published meta-analysis (concise, authoritative)

**Chapter 5 (Empirical Results):**
- [ ] Organized by theory/theme, not procedural RQ order
- [ ] Section intros explain why each theme matters (150-200 words each)
- [ ] Statistics integrated into narrative prose, not dumped in bullet lists
- [ ] Cross-references connect related findings (e.g., "converges with RQ 5.2.2")
- [ ] Figures have publication-quality captions (describe axes, pattern, takeaway)
- [ ] Null results reported with same detail as significant results
- [ ] Reads like results chapter of published monograph (story-driven, cohesive)

**Statistical reporting:**
- [ ] Always: β, SE, z/t, p, 95% CI
- [ ] Always: Effect sizes (d, f², η²) with interpretation (small/medium/large)
- [ ] Always: Model fit (AIC, BIC, R²) when comparing models
- [ ] Bonferroni correction noted when applied (dual p-values per Decision D068)

**Writing style:**
- [ ] PhD thesis level (formal, precise, objective)
- [ ] Domain expertise assumed (reader knows IRT, LMM, episodic memory theory)
- [ ] No editorializing (report findings objectively)
- [ ] Transparent about limitations and unexpected patterns

---

## Token Budget Management

**Per RQ estimate:** ~4k tokens (context_finder 3k + formatting 1k)

**35 RQs total:** ~140k tokens across multiple sessions

**Session strategy:**
- Session 1: Process RQs until ~120k tokens → Update notepad → User /clear
- Session 2: Resume from notepad → Process more RQs → Update notepad → User /clear
- Session 3+: Repeat until all 35 RQs complete
- Final session: Write section intros + chapter summary (Ch5 §5.6)

**Graceful stopping:**
When approaching 140k tokens:
1. Finish current RQ (don't stop mid-RQ)
2. Update notepad.md with progress
3. Tell user: "Token budget approaching limit. Processed RQs X.X.X through Y.Y.Y. Please run /clear to start fresh session. Next session will resume at RQ Z.Z.Z per notepad.md."

---

## Troubleshooting

**Problem:** context_finder returns incomplete statistics (missing CIs or p-values)
**Solution:** Re-invoke with explicit request: "Extract COMPLETE statistics including ALL β, SE, z, p, 95% CI values."

**Problem:** RQ has no summary.md (analysis not run yet)
**Solution:** Log blocker in notepad.md, skip RQ, continue with next. Circle back later.

**Problem:** Can't determine which Ch4 section for a new method
**Solution:** Add to Ch4 with placeholder section number (§4.X.X TBD), note in notepad for future organization.

**Problem:** Chapter 5 section intro unclear (don't know what theme is)
**Solution:** Read 1_concept.md for first RQ in section, extract theoretical motivation, use as section intro seed.

**Problem:** Figures missing or wrong paths
**Solution:** Invoke context_finder again with explicit "List EXACT file paths for all plots in results/ch5/X.X.X/plots/"

---

## Final Integration Phase (After All 35 RQs Complete)

**Chapter 4 finalization:**
1. Read entire chapter_4_analysis.md
2. Fill in any placeholder section numbers (§4.X.X → §4.2.3)
3. Add chapter intro (§4.1) explaining overall analytic strategy
4. Check all Ch5 cross-references resolve correctly
5. Polish prose for consistency and clarity

**Chapter 5 finalization:**
1. Read entire chapter_5_empirical.md
2. Write §5.0 Introduction (300-500 words)
3. Write §5.6 Chapter Summary (500-800 words synthesizing 35 RQs)
4. Polish section intros (ensure 150-200 words each, cohesive flow)
5. Verify all cross-references work (both within Ch5 and to Ch4)
6. Check figure numbering is sequential and captions are publication-quality

---

## Success Criteria

**Deliverables:**
- [x] chapter_4_analysis.md: Polished methods chapter (consolidated, no redundancy)
- [x] chapter_5_empirical.md: Polished results chapter (narrative, thematic organization)
- [x] All 35 RQs documented with complete statistics
- [x] Cross-references from Ch5 to Ch4 functional
- [x] Figures embedded with publication-quality captions
- [x] Null results reported with equal detail as significant results
- [x] Writing quality: PhD thesis standard (formal, precise, cohesive)

**Verification:**
- User can read Ch4 and understand ALL methods used in thesis
- User can read Ch5 and understand empirical story WITHOUT needing to reference Ch4 constantly
- External reader (thesis examiner) would find chapters publication-ready
- No "TBD" or placeholder text remains
- No redundant repetition of methods across RQs
- Both chapters read like cohesive narratives, not stitched-together fragments

---

**END INSTRUCTIONS**
