# Chapter 5 Restructuring Plan

**Date:** 2025-12-10
**Current Status:** 37,000 words, 35 RQs, needs reduction to ~12,000 words
**Problem:** Linear presentation of 35 mini-papers creates encyclopedia, not thesis chapter
**Solution:** Restructure around narrative themes with integrated findings

---

## Current Structure Analysis

### Pattern Across Sections:
Each of §5.1-§5.5 follows identical template:
1. **Trajectory analysis** (functional form, domain/paradigm/schema/spatial comparison)
2. **Consolidation window** (two-phase forgetting, sleep effects)
3. **Age moderation** (does age affect the pattern?)
4. **Methodological validation** (IRT-CTT convergence, purification effects)
5. **Individual differences** (variance decomposition, clustering)

### Core Issue:
**RQ Matrix Structure:**

|                    | §5.1 General | §5.2 Domains | §5.3 Paradigms | §5.4 Schema | §5.5 Spatial |
|--------------------|--------------|--------------|----------------|-------------|--------------|
| Trajectory form    | 5.1.1        | 5.2.1        | 5.3.1          | 5.4.1       | 5.5.1        |
| Consolidation      | 5.1.2        | 5.2.2        | 5.3.2-5.3.3    | 5.4.2       | 5.5.2        |
| Age effects        | 5.1.3        | 5.2.3        | 5.3.4          | 5.4.3       | 5.5.3        |
| IRT-CTT validity   | —            | 5.2.4        | 5.3.5          | 5.4.4       | 5.5.4        |
| Purification       | —            | 5.2.5        | 5.3.6          | 5.4.5       | 5.5.5        |
| Variance decomp    | 5.1.4        | 5.2.6        | 5.3.7          | 5.4.6       | 5.5.6        |
| Clustering         | 5.1.5        | 5.2.7        | 5.3.8          | 5.4.7       | 5.5.7        |
| Other              | —            | —            | 5.3.9          | —           | —            |

**Total:** 35 RQs testing same 7 themes across 5 content facets

This creates **massive redundancy** when presented linearly:
- Reader encounters "Age shows no effect" **5 times** (5.1.3, 5.2.3, 5.3.4, 5.4.3, 5.5.3)
- Reader encounters "ICC_slope≈0 design limitation" **5 times** (5.1.4, 5.2.6, 5.3.7, 5.4.6, 5.5.6)
- Reader encounters "Power-law better than log" **4 times** (5.1.1, 5.2.1, 5.3.1, 5.4.1)

---

## Proposed Restructuring: Theme-Based Integration

### New Chapter Organization:

**§5.0 Introduction** (keep as is, ~500 words)

**§5.1 The Shape of VR Episodic Forgetting** (~3,000 words)
- **Core narrative:** What is the functional form? Power-law vs logarithmic paradigm shift
- **Flagship RQs:**
  - 5.1.1: General trajectory (FULL DETAIL, 800 words) ← Foundational finding
  - 5.1.2: Two-phase forgetting (FULL DETAIL, 600 words) ← Consolidation evidence
- **Integrated findings from:**
  - 5.2.1: Domain trajectories (200 words summary + Table 5.1 comparing What/Where/When)
  - 5.3.1: Paradigm trajectories (200 words summary + Table 5.2 comparing FR/CR/Recog)
  - 5.4.1: Schema effects on trajectories (200 words summary)
  - 5.5.1: Spatial trajectories (200 words summary)
- **Synthesis:** Power-law dominance is universal across content/paradigm (600 words)
- **Key takeaway:** Model averaging essential due to extreme functional form uncertainty

**§5.2 Age-Invariant VR Memory: A Scaffolding Effect** (~2,000 words)
- **Core narrative:** Why does age NOT predict forgetting in VR when it does in traditional tests?
- **Flagship RQ:**
  - 5.1.3: General age null effect (FULL DETAIL, 600 words) ← Environmental support hypothesis
- **Integrated findings from:**
  - 5.2.3: Domain age effects (NULL, 150 words)
  - 5.3.4: Paradigm age effects (NULL, 150 words)
  - 5.4.3: Schema age effects (NULL, 150 words)
  - 5.5.3: Spatial age effects (NULL, 150 words)
- **Table 5.3:** Age effects summary across all 5 analyses (β estimates, p-values, effect sizes)
- **Synthesis:** Immersive VR provides cognitive scaffolding absent from neuropsych tests (800 words)
- **Key takeaway:** Context-supported memory compensates for age-related declines

**§5.3 Individual Differences: Baselines Dominate, Rates Are Parallel** (~2,500 words)
- **Core narrative:** People differ in WHAT they remember (baseline), not HOW they forget (rate)
- **Flagship RQs:**
  - 5.1.4: Variance decomposition (FULL DETAIL, 700 words) ← 432-fold ICC shift with model averaging
  - 5.1.5: Clustering on random effects (FULL DETAIL, 700 words) ← Three latent profiles
- **Integrated findings from:**
  - 5.2.6: Domain variance (ICC_slope≈0, 150 words)
  - 5.3.7: Paradigm variance (ICC_slope≈0, 150 words)
  - 5.4.6: Schema variance (ICC_slope≈0, 150 words)
  - 5.5.6: Spatial variance (ICC_slope≈0, 150 words)
- **Table 5.4:** ICC_intercept vs ICC_slope across all analyses (shows consistent 60%/0% pattern)
- **Synthesis:** Design limitation (4 timepoints insufficient) vs substantive finding (600 words)
- **Key takeaway:** Forgetting rate is trait-like (ICC=21%) but requires model averaging to detect

**§5.4 Content-Specific Memory Characteristics** (~2,500 words)
- **Core narrative:** What/Where/When domains, FR/CR/Recog paradigms, schema, spatial differ at BASELINE but forget similarly
- **Flagship RQs:**
  - 5.2.1: Domain trajectories (FULL DETAIL, 700 words) ← When floor effect, dual-scale reporting
  - 5.3.1-5.3.2: Paradigm trajectories + linear trend (FULL DETAIL, 800 words) ← Desirable difficulties
- **Integrated findings:**
  - 5.4.1: Schema congruence (400 words summary)
  - 5.5.1: Source vs destination (400 words summary)
- **Synthesis:** Encoding strength varies, decay rate doesn't (600 words)
- **Key takeaway:** Common forgetting mechanism operates uniformly across content types

**§5.5 Methodological Validation: IRT vs CTT Convergence** (~1,500 words)
- **Core narrative:** Does sophisticated IRT calibration yield different conclusions than simple CTT means?
- **Flagship RQ:**
  - 5.2.4: Domain IRT-CTT convergence (FULL DETAIL, 500 words) ← r=0.96 strong convergence
- **Integrated findings from:**
  - 5.3.5: Paradigm convergence (150 words)
  - 5.4.4: Schema convergence (150 words)
  - 5.5.4: Spatial convergence (150 words)
  - 5.2.5, 5.3.6, 5.4.5, 5.5.5: Purification effects (400 words integrated summary)
- **Table 5.5:** Correlation matrix (IRT theta vs CTT mean across all analyses)
- **Synthesis:** IRT calibration essential for scale linking but trajectory shapes robust (400 words)
- **Key takeaway:** CTT adequate for within-study comparisons, IRT critical for cross-study integration

**§5.6 Chapter Summary** (keep as is, ~800 words)

---

## Word Count Breakdown:

| Section | Word Target | Composition |
|---------|-------------|-------------|
| §5.0 Introduction | 500 | Current version (minimal edit) |
| §5.1 Shape of Forgetting | 3,000 | 2 flagship RQs (1,400) + 4 integrated summaries (1,000) + synthesis (600) |
| §5.2 Age-Invariant Memory | 2,000 | 1 flagship RQ (600) + 4 integrated summaries (600) + table + synthesis (800) |
| §5.3 Individual Differences | 2,500 | 2 flagship RQs (1,400) + 4 integrated summaries (600) + table + synthesis (500) |
| §5.4 Content-Specific Chars | 2,500 | 2 flagship RQs (1,500) + 2 integrated summaries (800) + synthesis (200) |
| §5.5 Methodological Valid | 1,500 | 1 flagship RQ (500) + 4 integrated summaries (700) + table + synthesis (300) |
| §5.6 Summary | 800 | Current version (minimal edit) |
| **TOTAL** | **12,800** | Within target range (12,000-13,000) |

---

## Flagship vs Integrated RQs:

### Flagship RQs (Full Detail, ~600-800 words each):
**Keep complete hypothesis, analysis, results, interpretation**

1. **5.1.1** - Functional form (power-law vs log paradigm shift) ← **FOUNDATIONAL**
2. **5.1.2** - Two-phase forgetting (consolidation evidence)
3. **5.1.3** - Age null effect (scaffolding hypothesis) ← **THEORETICALLY CRITICAL**
4. **5.1.4** - Variance decomposition (model averaging necessity)
5. **5.1.5** - Clustering (three profiles)
6. **5.2.1** - Domain trajectories (When floor effect, measurement lesson)
7. **5.3.1-5.3.2** - Paradigm trajectories (desirable difficulties)
8. **5.2.4** - IRT-CTT convergence (methodological validation)

**Total:** 8 flagship RQs (~5,600 words)

### Integrated RQs (Summary Form, ~150-400 words each):
**Report as: "Consistent with §5.1.1, [domain/paradigm/schema] showed power-law dominance..."**
**Include key statistics in integrated tables, cross-reference to Appendix A for full details**

- 5.2.2, 5.2.3, 5.2.5, 5.2.6, 5.2.7 (5 RQs, ~800 words total)
- 5.3.3, 5.3.4, 5.3.5, 5.3.6, 5.3.7, 5.3.8, 5.3.9 (7 RQs, ~1,200 words total)
- 5.4.2, 5.4.3, 5.4.4, 5.4.5, 5.4.6, 5.4.7 (6 RQs, ~1,000 words total)
- 5.5.2, 5.5.3, 5.5.4, 5.5.5, 5.5.6, 5.5.7 (6 RQs, ~1,000 words total)

**Total:** 24 integrated RQs (~4,000 words)

---

## New Summary Tables (Compact Presentation):

**Table 5.1: Functional Form Comparison Across Content Facets**
- Rows: General, What, Where, When, FR, CR, Recog, Schema, Spatial
- Cols: Best Model, AIC, Weight, N_eff, α_eff, θ decline (Day 0→6)

**Table 5.2: Age Effects Across All Analyses**
- Rows: 5 analyses (General, Domain, Paradigm, Schema, Spatial)
- Cols: Age β, SE, p, 95% CI, Cohen's d, Interpretation

**Table 5.3: ICC Decomposition Across All Analyses**
- Rows: 5 analyses
- Cols: ICC_intercept, ICC_slope, r_int_slope, Interpretation

**Table 5.4: IRT-CTT Convergence Across All Analyses**
- Rows: 4 analyses (Domain, Paradigm, Schema, Spatial)
- Cols: r_theta_CTT, Steiger's Z, p, RMSE, Interpretation

**Table 5.5: Consolidation Window Evidence Across Analyses**
- Rows: 5 analyses
- Cols: Early slope (0-48h), Late slope (48h+), Ratio, Segment×Time p

---

## Appendix A Strategy:

### Keep ALL 35 RQs in complete detail in Appendix A

**Structure mirrors old Chapter 5:**
- A.1.1 through A.1.5 (General trajectories)
- A.2.1 through A.2.7 (Domain-specific)
- A.3.1 through A.3.9 (Paradigm-specific)
- A.4.1 through A.4.7 (Schema effects)
- A.5.1 through A.5.7 (Spatial memory)

**Each appendix RQ includes:**
- Complete hypothesis, analysis description
- Full statistical tables (model comparison, AIC weights, variance components)
- Assumption diagnostics
- Extended interpretation
- Cross-references to main chapter sections

**Appendix word count:** ~25,000 words (current detail level preserved)

---

## Implementation Strategy:

### Phase 1: Create New Chapter Shell (~30 min)
1. Copy chapter_5_empirical.md → chapter_5_empirical_OLD.md (preserve original)
2. Create chapter_5_empirical_RESTRUCTURED.md with new §5.1-§5.6 headings
3. Extract §5.0 intro and §5.6 summary (keep verbatim)

### Phase 2: Migrate Flagship RQs (~1 hour)
1. Copy 8 flagship RQs into appropriate new sections
2. Light editing for narrative flow (remove redundant cross-refs)
3. Preserve figures, statistics, interpretation

### Phase 3: Write Integrated Summaries (~2 hours)
1. For each integrated RQ:
   - Extract key finding (1-2 sentences)
   - Report primary statistic only
   - Cross-reference to Appendix A.X.Y
   - Add row to appropriate summary table
2. Group by theme (4-6 integrated RQs per paragraph)

### Phase 4: Write Syntheses (~1 hour)
1. §5.1 synthesis: Power-law universality across content/paradigm
2. §5.2 synthesis: VR scaffolding explains age-invariance
3. §5.3 synthesis: Design limitation vs substantive ICC findings
4. §5.4 synthesis: Encoding differences, not decay differences
5. §5.5 synthesis: IRT critical for cross-study, CTT adequate within-study

### Phase 5: Create Summary Tables (~30 min)
1. Extract key statistics from all 35 RQs
2. Format as Tables 5.1-5.5
3. Insert into appropriate sections

### Phase 6: Populate Appendix A (~1 hour)
1. Copy ALL 35 RQs from OLD version into Appendix A structure
2. Add "Main Chapter Reference: §5.X" cross-links
3. Verify all figures, tables, statistics preserved

### Phase 7: Verify Integrity (~30 min)
1. Check all cross-references resolve
2. Verify all 55 figures still referenced
3. Confirm word count ~12,800
4. Validate Appendix A completeness (~25k words)

**Total estimated time:** 6-7 hours (one full work session)

---

## Key Benefits of This Approach:

1. **Narrative Coherence:**
   - Reader follows thematic story, not 35 isolated mini-papers
   - Redundant findings reported once (with integrated evidence)
   - Clear "big picture" messages emerge

2. **Demonstrates Mastery:**
   - Flagship RQs show full analytical depth
   - Integrated summaries show systematic replication
   - Synthesis shows theoretical integration

3. **Preserves Rigor:**
   - NO information loss (Appendix A has everything)
   - Complete reproducibility maintained
   - Examiners can verify any finding

4. **Appropriate Length:**
   - Main chapter: 12,800 words (thesis-appropriate)
   - Appendix: 25,000 words (reference/verification)
   - Total: 37,800 words (slightly more than current due to synthesis sections)

5. **Tells a Story:**
   - §5.1: "Forgetting follows power-law, not Ebbinghaus log"
   - §5.2: "Age doesn't matter in VR (scaffolding effect)"
   - §5.3: "People differ in baseline, not rate (design limitation?)"
   - §5.4: "Content matters for encoding, not forgetting"
   - §5.5: "IRT calibration works (methodology validated)"

---

## Potential Challenges:

1. **Figure renumbering:** 55 figures will need new numbers (5.1-5.15 in main, A.1-A.40 in appendix)
2. **Cross-reference updates:** Extensive §X.Y.Z → §X.Y + "see Appendix A.X.Y" conversions
3. **Table creation:** 5 new summary tables need careful data extraction
4. **Synthesis writing:** Requires fresh prose integrating multiple RQs
5. **Appendix population:** Mechanical but time-consuming copy-paste

---

## Alternative: Two-Chapter Split

If restructuring feels too radical, consider:

**Chapter 5: Core Forgetting Mechanisms** (15,000 words)
- §5.1 General trajectories (5 RQs, full detail)
- §5.2 Domain-specific (7 RQs, full detail)
- Focus: WHAT is the forgetting pattern?

**Chapter 6: Moderators and Methodology** (15,000 words)
- §6.1 Paradigm effects (9 RQs, full detail)
- §6.2 Schema and spatial (14 RQs, full detail)
- Focus: WHAT modulates the pattern? Is methodology robust?

**Chapter 7: [Original Chapter 6 content]**
**Chapter 8: [Original Chapter 7 content]**

This preserves depth but spreads across more chapters (thesis total: 8 chapters instead of 7).

---

## Recommendation:

**Proceed with theme-based restructuring (not two-chapter split).**

Reasoning:
1. Maintains planned thesis structure (7 chapters)
2. Eliminates redundancy more effectively
3. Creates stronger narrative coherence
4. Demonstrates integration skill (valued by examiners)
5. Appendix ensures zero information loss

**Next step:** User approval of restructuring plan, then execute Phase 1-7 systematically.

---

**END RESTRUCTURING PLAN**
