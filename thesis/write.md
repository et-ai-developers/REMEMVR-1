# REMEMVR Thesis Writing System - General Instructions

**Last Updated:** 2026-01-02
**Purpose:** Stateless instructions for AI agents writing thesis chapters
**Principle:** Make it engaging, not exhausting - keep assessors interested!

---

## THE REMEMVR STORY (Overall Thesis Narrative)

**The Problem:**
Traditional episodic memory tests force a choice: ecological validity OR experimental control. You can't have both. Tests like RAVLT (word lists) have experimental rigor but don't capture real-world memory. Auto biographical interviews capture real memory but can't be standardized.

**The Solution:**
REMEMVR uses immersive VR to resolve this 140-year-old measurement paradox. Participants explore realistic household rooms, naturally encode episodic memories, then get tested over 6 days. It's ecological (real-world-like) AND standardized (everyone sees identical stimuli).

**The Discovery:**
Two years of data collection (N=100, ages 20-70) revealed surprising patterns. VR episodic memory follows power-law forgetting (challenging Ebbinghaus), shows age-invariant decay rates (contradicting aging literature), and demonstrates that confidence partially dissociates from accuracy. Model averaging proved essential - single-model approaches underestimate individual differences by 432-fold.

**The Contribution:**
This thesis establishes REMEMVR as a new assessment paradigm and reveals fundamental principles about how real-world episodic memory works, ages, and relates to metacognition.

---

## THESIS ARCHITECTURE (How Chapters Fit Together)

### Part I: Foundation
- **Ch1 (Introduction):** Why episodic memory matters, measurement paradox, VR solution
- **Ch2 (Methods):** How REMEMVR works (experimental protocol, N=100, 4 rooms, 6-day schedule)
- **Ch3 (Rationale):** Why every design decision was made (justifies the tool)
- **Ch4 (Analysis):** How we analyze REMEMVR data (IRT+LMM pipeline, model comparison)

### Part II: Empirical Findings
- **Ch5 (Forgetting Trajectories):** WHAT HAPPENS to memory over time (accuracy, functional form, age effects)
- **Ch6 (Metacognition):** Does confidence TRACK what happens? (calibration, high-confidence errors, dissociation)
- **Ch7 (Individual Differences):** What PREDICTS individual differences? (cognitive tests, age, sleep, strategy)

### Part III: Synthesis
- **Ch8 (Discussion):** What does this mean? (theory, clinical utility, future directions)

**The Narrative Arc:** Build the tool (Ch1-4) → Discover patterns (Ch5-7) → Interpret implications (Ch8)

---

## WRITING PHILOSOPHY: Engaging, Not Exhausting

### What Makes a Thesis Readable?

**✅ DO:**
- **Tell a story:** Each chapter has a narrative arc (problem → investigation → discovery → interpretation)
- **Build progressively:** Each section builds on the last (no abrupt jumps)
- **Use transitions:** Bridge between themes ("Having established X, we now examine whether Y...")
- **Synthesize:** Don't just report statistics - explain what patterns MEAN
- **Be concise:** Say it once well, not three times poorly
- **Vary sentence structure:** Short sentences for impact. Longer ones for nuance and context.
- **Use active voice:** "We found X" not "X was found"
- **Explain jargon:** First mention = full term, then abbreviation (e.g., "Free Recall (FR)")

**❌ DON'T:**
- **Data dump:** Listing 65 RQ abstracts with no integration
- **Repeat yourself:** "Age shows no effect" × 7 times (say it once with a table showing replication)
- **Hide in passive voice:** "It was observed that..." (Who observed? YOU did!)
- **Assume knowledge:** Define technical terms when first introduced
- **Overwhelm with statistics:** Integrate stats into narrative, don't bullet-list them
- **Create walls of text:** Break up long sections with subheadings, figures, tables

### The "Dinner Party Test"

Could you explain this chapter's main finding to a smart non-specialist at a dinner party? If yes, your writing is clear. If no, simplify.

**Example:**
- ❌ "Model averaging paradigm shift revealed ICC_slope heterogeneity sensitivity to functional form parameterization"
- ✅ "When we properly accounted for uncertainty in forgetting curve shape, individual differences in forgetting rate increased 432-fold - from essentially zero to a moderate trait"

### Keep Assessors Engaged

**Remember:** Thesis assessors read 5-10 theses per year. They're looking for:
1. **Competence:** Can you do rigorous science? (Show in flagship RQs)
2. **Judgment:** Can you integrate findings? (Show in synthesis sections)
3. **Communication:** Can you explain complex ideas clearly? (Show throughout)
4. **Contribution:** Did you advance the field? (Show in Discussion)

**Make their job easy:**
- Clear roadmaps (tell them where you're going)
- Signposting (remind them where you are)
- Summary tables (compact cross-RQ comparisons)
- Figures that actually help (not decorative)
- Honest limitations (shows maturity, not weakness)

---

## STATISTICAL REPORTING STANDARDS

### Complete Reporting (5-Component Format)

**For ALL LMM results, report:**
```
β=X.XX, SE=X.XX, p=.XXX, 95% CI [X.XX, X.XX], d=X.XX
```

**Example:**
"Age predicted baseline performance (β=-0.011, SE=0.016, p=.48, 95% CI [-0.042, 0.020], d=0.01), but this effect was trivial and not statistically significant."

**Why 5 components?**
- **β (coefficient):** Effect size in original units
- **SE (standard error):** Precision of estimate
- **p-value:** Statistical significance (under α=.05)
- **95% CI:** Range of plausible values
- **d (Cohen's d):** Standardized effect size (small=0.2, medium=0.5, large=0.8)

### Null Results Get Equal Treatment

**Don't hide null findings.** Report them with same detail as significant results. Null results are scientifically interesting (e.g., age-invariant VR forgetting challenges aging literature).

**Bad:**
"Age effects were not significant (p>.05)."

**Good:**
"Age did not predict forgetting rate (Age×Time β=0.000022, SE=0.0004, p=.96, 95% CI [-0.0008, 0.0008], d<0.01), suggesting VR contextual richness may equalize decay rates across the adult lifespan (ages 20-70)."

---

## CROSS-REFERENCING SYSTEM

### Within Chapter
```markdown
As reported in §5.3, age shows null effects across all content types...
See Table 5.3 for complete age effect replication across 5 analyses.
```

### Across Chapters
```markdown
These confidence trajectories (Ch6 §6.1) closely parallel the accuracy
trajectories established in Ch5 §5.2, suggesting metacognitive monitoring
tracks objective memory decline.
```

### To Methodology (Ch4)
```markdown
We used 2-pass IRT purification (§4.2.2) to exclude items with low
discrimination (a<0.4) before LMM analysis (§4.3.1).
```

### To Reports (Full Details)
```markdown
For complete statistical details, model comparison tables, and assumption
diagnostics, see reports/5.1.1/report.md Section 5.
```

---

## FLAGSHIP vs INTEGRATED RQ STRATEGY

### Flagship RQs (Full Detail, 600-900 words each)

**Purpose:** Demonstrate thesis-level analytical competence (assessors verify your rigor here)

**Include:**
- Complete hypothesis with theoretical rationale
- Brief analysis specs (+ cross-ref to Ch4 for methods)
- Full results with all statistics (β, SE, p, CI, d)
- Interpretation (hypothesis supported/refuted? why?)
- Figures with publication-quality captions
- Connections to theory (what does this mean?)

**Example:** RQ 5.1.1 (Functional form) - shows paradigm shift from logarithmic to power-law

### Integrated RQs (Summary Table + Narrative, 400-600 words total)

**Purpose:** Demonstrate systematic replication without redundancy

**Include:**
- Brief narrative intro (200 words: "We replicated functional form analysis across 5 content facets...")
- Summary table (compact presentation of key statistics across all integrated RQs)
- Brief narrative summary (200-400 words: patterns, exceptions, cross-refs to reports)

**Example:** RQs 5.2.1, 5.3.1, 5.4.1, 5.5.1 (Functional form replication) - shows power-law dominates universally

**Why this strategy?**
- Eliminates redundancy (don't repeat same analysis 7 times)
- Preserves depth (flagship RQs show full competence)
- Shows integration (summary tables reveal cross-RQ patterns)
- Maintains verifiability (cross-refs to reports for full details)

---

## FIGURE & TABLE GUIDELINES

### Figures

**Purpose:** Figures should HELP understanding, not just decorate

**Good figures:**
- Have clear, self-contained captions (reader shouldn't need main text to understand)
- Show patterns mentioned in text (if you say "power-law dominates," figure shows power-law curve)
- Use consistent color schemes (What=blue, Where=green, When=red throughout thesis)
- Include error bars (95% CI or SE, state which in caption)
- Have readable axis labels (12pt+ font, no jargon in labels)

**Example caption:**
```markdown
**Figure 5.1.** Episodic memory forgetting trajectories across 6 days (N=100, 400
observations). Theta scores decline following power-law function (α_eff=0.41,
best model weight=5.6%). Shaded region: 95% confidence interval. Model-averaged
predictions (blue) dominate single-model fits (gray), demonstrating importance of
accounting for functional form uncertainty (Shannon entropy H'=2.71, effective
N=15 competitive models). Data points: empirical means ± SE at each test session.
```

### Tables

**Purpose:** Compact presentation of cross-RQ patterns

**Good tables:**
- Have clear column headers (with units)
- Include sample sizes (N)
- Mark significance levels (* p<.05, ** p<.01, *** p<.001)
- Include effect sizes (not just p-values)
- Have informative captions
- Reference appendix for full details

**Example table:**
```markdown
**Table 5.3.** Age effects across all analyses (null findings replication)

| Analysis  | Age β (baseline) | SE    | p    | 95% CI          | Age×Time β | SE     | p    | d    |
|-----------|------------------|-------|------|-----------------|------------|--------|------|------|
| General   | -0.011           | 0.016 | .48  | [-0.042, 0.020] | 0.000022   | 0.0004 | .96  | 0.01 |
| Domain    | -0.009           | 0.014 | .52  | [-0.037, 0.019] | 0.000019   | 0.0004 | .96  | 0.01 |
| Paradigm  | -0.013           | 0.017 | .44  | [-0.047, 0.021] | 0.000025   | 0.0005 | .96  | 0.01 |
| Schema    | -0.010           | 0.015 | .50  | [-0.040, 0.020] | 0.000021   | 0.0004 | .96  | 0.01 |
| Spatial   | -0.012           | 0.016 | .46  | [-0.044, 0.020] | 0.000023   | 0.0004 | .95  | 0.01 |

*Note:* Age×Time interactions consistently nonsignificant (all p>.44), Cohen's
d<0.01 (trivial). See reports/5.*.3/report.md for complete analyses.
```

---

## SYNTHESIS SECTIONS (The "So What?")

Every theme needs a synthesis section (200-300 words) that answers:

1. **What pattern emerged?** (Convergent findings across RQs)
2. **What does it mean theoretically?** (Which frameworks supported/challenged?)
3. **What are the limitations?** (Where is evidence weak/uncertain?)
4. **How does it connect forward?** (What does next chapter/theme build on this?)

**Example (Ch5 §5.3.3 Age Synthesis):**
```markdown
The consistent null findings for Age×Time interactions across all five analyses
(p>.40, d<0.01) challenge the dual-deficit hypothesis of cognitive aging, which
predicts age should affect both baseline performance AND forgetting rate. Our
results suggest a different pattern: VR contextual richness may equalize forgetting
rates across the adult lifespan (20-70 years) even as baseline encoding ability
declines marginally with age.

This age-invariant forgetting pattern aligns with Craik & Rose's (2012) environmental
support hypothesis - rich multimodal cues in immersive VR may scaffold retrieval
equally well for younger and older adults. However, three limitations temper this
interpretation: (1) our sample range (20-70) may not capture steepest age-related
declines (>75 years), (2) floor effects at Day 6 (~30% accuracy) limit age
discriminability, and (3) 4-timepoint design provides insufficient power for
detecting small interaction effects.

Critically, this VR-specific pattern contrasts sharply with traditional tests:
Chapter 7 will demonstrate that standard neuropsychological tests (RAVLT, BVMT)
show robust age effects in this same sample, confirming the dissociation reflects
paradigm differences (VR scaffolding), not measurement insensitivity.
```

---

## FILE STRUCTURE & NAMING

### Thesis Chapter Files
```
/home/etai/projects/REMEMVR/thesis/
├── introduction.md          # Ch1 (partial draft exists)
├── methods.md               # Ch2 (partial draft exists)
├── rationale.md             # Ch3 (partial draft exists)
├── chapter_4_analysis.md    # Ch4 (to be written)
├── chapter_5_empirical.md   # Ch5 (to be written from 35 RQ reports)
├── chapter_6_empirical.md   # Ch6 (to be written from 30 RQ reports)
├── chapter_7_individual_differences.md  # Ch7 (future work)
├── discussion.md            # Ch8 (future work)
├── chapters_UPDATED.md      # RQ catalog (current state)
├── write.md                 # THIS FILE (general instructions)
├── write4.md                # Ch4-specific instructions
├── write5.md                # Ch5-specific instructions
├── write6.md                # Ch6-specific instructions
└── write7.md                # Ch7-specific instructions (placeholder)
```

### RQ Report Files (Source Material)
```
/home/etai/projects/REMEMVR/reports/
├── 5.1.1/report.md          # RQ 5.1.1 comprehensive report (10 sections)
├── 5.1.2/report.md          # RQ 5.1.2 comprehensive report
├── ...                      # 35 Ch5 reports total
├── 6.1.1/report.md          # RQ 6.1.1 comprehensive report
├── ...                      # 30 Ch6 reports total
└── [No Ch7 reports yet]
```

---

## STATELESS AGENT EXECUTION PARADIGM

### What "Stateless" Means

Each agent invocation is independent. Agent must:
1. Read this file (write.md) for general instructions
2. Read chapter-specific file (writeX.md) for chapter context
3. Read theme_specification.md for specific RQ assignments
4. Read RQ reports (./reports/X.Y.Z/report.md)
5. Write output (theme_X_content.md)
6. Report success/anomalies to master

**NO state persists between invocations.** Agent can't remember what it wrote last time.

### Master's Responsibilities

- Read all RQ report Section 9 summaries (build mental map)
- Create theme specifications (assign RQs to themes)
- Invoke agents (one per theme)
- Integrate agent outputs (copy into chapter shells)
- Write transitions, intros, summaries (maintain narrative coherence)
- Polish for cohesion (g_conflict, redundancy elimination, terminology standardization)
- Final quality review

### Agent's Responsibilities

- Read assigned RQ reports (comprehensive understanding)
- Identify cross-RQ patterns (convergence, divergence, exceptions)
- Organize: Flagship RQs (full detail) + Integrated RQs (summary table)
- Write: Theme section following template (intro, flagship subsections, integrated subsection, synthesis)
- Validate: Check statistics against reports, flag anomalies
- Output: Single markdown file (2-5 pages), report success

---

## QUALITY CHECKLIST (Before Calling It Done)

### Narrative Coherence
- [ ] Progressive story (each section builds on previous)
- [ ] Smooth transitions (100-150 words between themes)
- [ ] Clear roadmap (intro tells reader what's coming)
- [ ] Synthesis sections (explain what patterns MEAN, not just WHAT)

### Analytical Rigor
- [ ] Complete statistics (β, SE, p, CI, d for ALL LMM results)
- [ ] Flagship RQs show full depth (600-900 words, complete methods, results, interpretation)
- [ ] Summary tables for integrated RQs (cross-RQ patterns visible)
- [ ] Null results get equal treatment (not hidden or dismissed)

### Clarity & Readability
- [ ] Active voice predominates ("We found X" not "X was found")
- [ ] Jargon defined at first mention
- [ ] Sentence variety (short for impact, longer for nuance)
- [ ] No data dumps (statistics integrated into narrative)
- [ ] Figures help understanding (not decorative)

### Cross-References
- [ ] Within-chapter refs work (§X.Y.Z format)
- [ ] Cross-chapter refs work (Ch5 ↔ Ch6 ↔ Ch7)
- [ ] Method refs work (§4.X.X for analytical methods)
- [ ] Report refs work (reports/X.Y.Z/report.md for full details)

### Terminology Consistency
- [ ] "Theta" not "IRT-calibrated ability"
- [ ] "Days" not "Time" or "Retention Interval"
- [ ] "Free Recall" first mention, "FR" thereafter
- [ ] "What/Where/When" not "Content/Location/Temporal"

### Style & Tone
- [ ] Formal but not stuffy (PhD thesis standard)
- [ ] Objective but not robotic (show scientific judgment)
- [ ] Precise but not obfuscatory (say things clearly)
- [ ] Engaging but not casual (keep assessors interested)

---

## REMEMBER THE GOAL

**You're writing a PhD thesis, not a 65-RQ technical report.**

The thesis should:
- Tell a coherent scientific story about VR episodic memory
- Demonstrate mastery (analytical competence, integrative thinking, communication skill)
- Advance the field (REMEMVR as new paradigm, power-law forgetting, age-invariant VR, metacognitive dissociation)
- Be readable by external examiners who haven't seen REMEMVR before
- Keep assessors engaged (they're evaluating 5-10 theses, make yours memorable for good reasons)

**When in doubt, ask:** "Would this be interesting to read at 10pm on a Thursday after the assessor has already read three other theses today?"

If yes → you're doing it right.
If no → simplify, clarify, synthesize.

---

## NEXT STEPS

After reading this file, proceed to chapter-specific instructions:
- **Writing Ch4?** Read `thesis/write4.md`
- **Writing Ch5?** Read `thesis/write5.md`
- **Writing Ch6?** Read `thesis/write6.md`
- **Writing Ch7?** Read `thesis/write7.md`

Each writeX.md contains:
- Chapter-specific narrative arc (why this chapter matters in the thesis story)
- Thematic organization (how RQs are grouped)
- Flagship vs integrated RQ assignments
- Key messages per theme
- Cross-chapter connections

**Good luck! Write something you'd want to read yourself.**

---

**END GENERAL INSTRUCTIONS**
