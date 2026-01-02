# Conflicts Analysis: write.md vs Existing Thesis Structure

**Date:** 2026-01-02
**Purpose:** Identify conflicts between thesis/write.md (execution plan) and existing thesis structure

---

## CONFLICT SUMMARY

### ✅ NO CONFLICTS (Aligned)

1. **Chapter numbering** - Both systems agree:
   - Ch1: Introduction (thesis/introduction.md exists, partial draft)
   - Ch2: Methods (thesis/methods.md exists, partial draft)
   - Ch3: Rationale (thesis/rationale.md exists, partial draft)
   - Ch4: Analysis (planned but not written)
   - Ch5: The Trajectory of Episodic Forgetting (write.md targets this)
   - Ch6: Metacognition in Episodic Memory (write.md targets this)
   - Ch7: Individual Differences (planned but not written)
   - Ch8: Discussion (planned but not written)

2. **Theoretical framework** - All documents agree:
   - Framework-agnostic/exploratory approach
   - Functional/constructivist perspective
   - PMAT acknowledged as most empirically robust existing framework
   - Not testing specific framework hypotheses

3. **Study design basics** - Consistent across all documents:
   - N=100 participants, ages 20-70
   - 4 test sessions (Day 0/1/3/6)
   - What/Where/When domains
   - Free Recall/Cued Recall/Recognition paradigms
   - 5-star Likert confidence ratings
   - IRT calibration using GRM

---

## ⚠️ MINOR CONFLICTS (Easy to Resolve)

### 1. RQ Numbering Scheme Evolution

**chapters.md (older):**
- Lists RQs by TYPE (e.g., "RQ 5.1-5.2: Domain trajectories")
- 15 RQ types for Ch5, 15 for Ch6, 20 for Ch7 = 50 RQ types total

**write.md (current):**
- References RQs by SPECIFIC NUMBER (e.g., "RQ 5.1.1, 5.1.2, 5.2.1")
- 35 RQs Ch5 + 30 RQs Ch6 = 65 RQs with reports

**Resolution:**
- RQ numbering evolved from TYPE-based (5.1 = all domain trajectory RQs) to SPECIFIC (5.1.1 = general trajectory, 5.2.1 = domain trajectory for What/Where/When)
- This is EXPANSION not conflict - each "RQ type" became multiple specific RQs
- Example: chapters.md "RQ 5.1-5.2: Domain trajectories" → write.md "5.2.1 (What/Where/When), 5.2.2 (consolidation), 5.2.3 (age), 5.2.4 (IRT-CTT), 5.2.5 (purification), 5.2.6 (ICC), 5.2.7 (clustering)"

**Action:** Update chapters.md to reflect current X.Y.Z numbering system

---

### 2. Partial Credit Scoring

**thesis/methods.md (§2.3.7):**
```
Scoring (manual free-text, automatic MC, partial credit 0.5/0.25)
```

**User statement (from chapters.md Q&A):**
```
"Partial credit too problematic, stick with dichotomous 0/1"
```

**Resolution:**
- Partial credit was PILOTED but ABANDONED
- Methods.md describes original design, needs update to reflect final decision

**Action:** Update thesis/methods.md §2.3.7 to state:
```
Scoring was dichotomous (0=incorrect, 1=correct). Partial credit (0.5 for
adjacent spatial/ordinal errors, 0.25 for twice-removed ordinal errors) was
piloted but abandoned due to scoring complexity and low inter-rater reliability.
```

---

### 3. Chapter 4 Content Ambiguity

**write.md:** Does not address Ch4 (focuses only on Ch5-Ch6)

**thesis structure:** Has Ch2 (Methods) but also mentions Ch4 (Analysis)

**old results/ch5/write.md:** Had extensive Ch4 structure (IRT methods, LMM methods, effect sizes, software)

**Resolution:**
- Ch2 (thesis/methods.md) = EXPERIMENTAL methods (participants, apparatus, procedure)
- Ch4 (not yet written) = ANALYTICAL methods (IRT specifications, LMM specifications, model comparison, assumptions)
- write.md execution plan should generate Ch5-Ch6 only
- Separate effort needed for Ch4 (can extract from RQ reports Section 4: Methodology)

**Action:**
1. Note in write.md that Ch4 is OUT OF SCOPE for current plan
2. Create separate plan for Ch4 if needed (can use rq_theme_writer to extract methodology sections from reports)

---

## 🔴 MAJOR GAPS (Not Conflicts, But Missing Work)

### 1. Chapter 7: Individual Differences

**Status:** ~20 RQs listed in chapters.md, but NO REPORTS GENERATED

**Impact:** write.md can only handle Ch5-Ch6 (65 reports exist), Ch7 has 0 reports

**Resolution:** Ch7 is FUTURE WORK, not current scope

**Action:** Explicitly note in write.md that Ch7 is deferred

---

### 2. Chapter 4: Analysis Methods

**Status:** Planned but not written

**Impact:** Ch5-Ch6 will need cross-references to Ch4 (e.g., "§4.2.2 IRT purification"), but Ch4 doesn't exist yet

**Resolution:** Two options:
- **Option A:** Write Ch4 BEFORE Ch5-Ch6 (extract from RQ report Section 4 Methodology)
- **Option B:** Write Ch5-Ch6 with placeholders (§4.X.X), fill in Ch4 later

**Action:** Ask user preference - do we need Ch4 first, or can we write Ch5-Ch6 with methodology placeholders?

---

### 3. RQ Report Coverage Gap

**65 reports exist** (Ch5 35 + Ch6 30)

**chapters.md lists ~85 total RQs** (Ch5 15 types → became 35 RQs, Ch6 15 types → became 30 RQs, Ch7 20 types → ??? RQs)

**Resolution:** Not all conceptual RQs became actual executed RQs (strategic prioritization)

**Action:** Update chapters.md to reflect ACTUAL RQ execution status (65 PLATINUM certified, rest deferred/skipped)

---

## 📋 DOCUMENTATION INCONSISTENCIES (To Fix)

### 1. Unresolved Methods Questions (from chapters.md Q&A)

**User flagged these as unresolved:**
- Monte Carlo samples: mc_samples=1 for model_fit, mc_samples=100 for model_scores (rationale forgotten)
- Multiple comparisons: No Bonferroni correction applied yet (acknowledged needed)
- DIF testing: Not done (user asks "Should I?")
- IRT fit indices: None reported (user asks "Which should I pick?")
- Confidence bias correction: Not done (user concerned about interpretability)
- NART validity: "Results are a bit bunk" (non-English speakers tested)

**Action:** These need resolution before finalizing thesis, but don't block Ch5-Ch6 writing (can document as limitations)

---

### 2. Section 1.7 Thesis Aims (Placeholder)

**Status:** introduction.md has headers for 1.7.1-1.7.6 but NO CONTENT

**Impact:** Chapter 5-6 will have forward/backward references to "thesis aims" that don't exist yet

**Action:** Write §1.7 before or during Ch5-Ch6 execution (brief, ~500 words total)

---

## 🎯 RECOMMENDED ACTIONS (Priority Order)

### Priority 1: Update chapters.md (IMMEDIATE)
- Replace old RQ type listings with current X.Y.Z numbering
- Add execution status (65/85 RQs PLATINUM certified, 20 Ch7 RQs deferred)
- Add major findings from RQ reports (power-law, age-invariant, ICC paradigm shift, etc.)
- Update to reflect v4.X architecture (report generation complete)

### Priority 2: Clarify Ch4 Strategy (BEFORE Ch5-Ch6 execution)
- Ask user: Write Ch4 first, or use placeholders?
- If placeholders: Document what §4.X.X sections will contain
- If Ch4 first: Create separate plan (can reuse rq_theme_writer for methodology extraction)

### Priority 3: Write §1.7 Thesis Aims (DURING Ch5-Ch6 execution)
- 500 words total (6 subsections × 80 words each)
- Can write in parallel with Phase 1 of write.md execution

### Priority 4: Update methods.md (DURING Ch5-Ch6 execution)
- Fix partial credit description (§2.3.7)
- Add any other design decisions finalized during RQ execution

### Priority 5: Document Known Limitations (DURING Ch5-Ch6 execution)
- Monte Carlo sampling choices
- No Bonferroni correction (yet)
- No DIF testing
- No IRT fit indices
- No confidence bias correction
- NART validity concerns

---

## ✅ WRITE.MD EXECUTION PLAN VIABILITY

**Can write.md execute as written?** YES, with clarifications:

**Scope:** Ch5-Ch6 only (35 + 30 = 65 RQs)
**Inputs:** 65 RQ reports in ./reports/X.Y.Z/report.md ✅ EXIST
**Dependencies:** Ch4 cross-refs (can use placeholders or write Ch4 first)
**Conflicts:** NONE blocking (all resolvable)

**Recommendation:** PROCEED with write.md execution after:
1. Updating chapters.md (1 hour)
2. Clarifying Ch4 strategy with user (5 min decision)
3. Optionally writing §1.7 Thesis Aims (30 min)

---

**END CONFLICTS ANALYSIS**
