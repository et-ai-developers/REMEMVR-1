# Chapter 5 Restructuring - Session Notepad

**Purpose:** Stateful tracking for multi-session Chapter 5 restructuring work
**Status:** INITIALIZED - Awaiting user approval to begin execution
**Last Updated:** 2025-12-10 (Session 1)

---

## QUICK RESUME PROMPT (Copy/paste after /clear)

```
I'm continuing work on Chapter 5 restructuring. Please read:
1. results/ch5/restructure_plan_v2_GOLD.md (master plan)
2. results/ch5/restructure_notepad.md (THIS FILE - session state)

Then continue from the current phase checkpoint.
```

---

## PROJECT OVERVIEW

**Goal:** Restructure chapter_5_empirical.md (37k words, 34 RQs) into gold-standard PhD thesis chapter

**Approach:**
- Main chapter: 14k words, 5 thematic narrative arcs, 8 flagship RQs + 26 integrated RQs
- Appendix A: 25k words, all 34 RQs in complete detail (zero information loss)

**Master Plan:** [restructure_plan_v2_GOLD.md](restructure_plan_v2_GOLD.md)

**Estimated Total Time:** 10-12 hours across multiple sessions

---

## CURRENT STATUS

**Phase:** PLANNING (awaiting user approval)

**Files:**
- ✅ `chapter_5_empirical.md` - Original (37k words, RESTORED from backup)
- ✅ `chapter_5_empirical_FULL.md` - Backup copy (identical to original)
- ✅ `restructure_plan_v2_GOLD.md` - Gold standard master plan (approved: PENDING)
- ✅ `appendix.md` - Template exists with A.1.1 populated
- ⏸️ `chapter_5_empirical_RESTRUCTURED.md` - Not yet created (Phase 1 task)

**User Decisions Needed:**
1. Approve gold-standard restructuring approach? (Y/N)
2. Approve 5-theme narrative organization? (Y/N)
3. Approve 8 flagship RQ selections? (Y/N)
4. Ready to begin Phase 1 execution? (Y/N)

---

## PHASE CHECKLIST (Track Progress Across Sessions)

### Phase 1: Create Structural Shell (1 hour)
- [ ] Copy chapter_5_empirical.md → chapter_5_empirical_OLD_v1.md
- [ ] Create chapter_5_empirical_RESTRUCTURED.md with 5-section shell
- [ ] Extract §5.0 Introduction (preserve verbatim)
- [ ] Extract §5.6 Summary (mark for rewrite)
- [ ] Verify shell structure renders correctly

**Deliverable:** Shell with placeholders (~1,500 words)
**Checkpoint saved:** `restructure_notepad.md` updated with Phase 1 COMPLETE

---

### Phase 2: Migrate Flagship RQs (3 hours)
**Target:** 8 flagship RQs (~5,600 words)

- [ ] **5.1.1** → §5.1.1 General trajectory form (900 words)
  - Location: OLD lines 23-52
  - Destination: RESTRUCTURED §5.1.1
  - Figures: 5.1, 5.2

- [ ] **5.1.2** → §5.1.2 Two-phase forgetting (700 words)
  - Location: OLD lines 54-68
  - Destination: RESTRUCTURED §5.1.2
  - Figures: 5.3

- [ ] **5.2.1** → §5.2.1 Domain trajectories (800 words)
  - Location: OLD lines 113-142
  - Destination: RESTRUCTURED §5.2.1
  - Figures: 5.7, 5.8

- [ ] **5.3.1 + 5.3.2** → §5.2.2 Paradigm trajectories (COMBINED, 800 words)
  - Location: OLD lines 143-174 (5.3.1), lines 175-202 (5.3.2)
  - Destination: RESTRUCTURED §5.2.2
  - Figures: 5.X, 5.Y (TBD)

- [ ] **5.1.3** → §5.3.1 General age effects (700 words)
  - Location: OLD lines 70-98
  - Destination: RESTRUCTURED §5.3.1
  - Figures: 5.4

- [ ] **5.1.4** → §5.4.1 Variance decomposition (800 words)
  - Location: OLD lines 100-127
  - Destination: RESTRUCTURED §5.4.1
  - Figures: 5.5

- [ ] **5.1.5** → §5.4.2 Latent profiles (700 words)
  - Location: OLD lines 129-158
  - Destination: RESTRUCTURED §5.4.2
  - Figures: 5.6

- [ ] **5.2.4** → §5.5.1 IRT-CTT convergence (600 words)
  - Location: OLD lines 234-268
  - Destination: RESTRUCTURED §5.5.1
  - Figures: TBD

**Checkpoint saved:** `restructure_notepad.md` updated with Phase 2 COMPLETE + line number mappings

---

### Phase 3: Write Integrated Summaries (2 hours)
**Target:** 5 integrated sections + 5 summary tables (~4,000 words)

- [ ] **§5.1.3** Functional form replication (600 words + Table 5.1)
  - Integrate: 5.2.1, 5.3.1, 5.4.1, 5.5.1 (trajectory analyses)
  - Table: 10 rows (facets) × 7 cols (model, AIC, weight, N_eff, α_eff, Δθ, Appendix ref)
  - Cross-refs: A.2.1, A.3.1, A.4.1, A.5.1

- [ ] **§5.3.2** Age replication (400 words + Table 5.3)
  - Integrate: 5.2.3, 5.3.4, 5.4.3, 5.5.3 (age effect analyses)
  - Table: 5 rows (analyses) × 9 cols (Age β, SE, p, CI, Age×Time, SE, p, d, Appendix ref)
  - Cross-refs: A.2.3, A.3.4, A.4.3, A.5.3

- [ ] **§5.4.3** ICC_slope≈0 replication (400 words + Table 5.4)
  - Integrate: 5.2.6, 5.3.7, 5.4.6, 5.5.6 (variance decomposition)
  - Table: 5 rows × 6 cols (ICC_int, ICC_slope, r_int_slope, Slope SD, Interpretation, Appendix ref)
  - Cross-refs: A.2.6, A.3.7, A.4.6, A.5.6

- [ ] **§5.2.3** Schema/spatial effects (500 words + Table 5.2)
  - Integrate: 5.4.1-5.4.7, 5.5.1-5.5.7 (subset)
  - Table: 11 rows (facets) × 9 cols (N_items, θ Day0, θ Day6, Decline, Slope β, SE, p, d, Appendix ref)
  - Cross-refs: A.4.1-A.4.7, A.5.1-A.5.7

- [ ] **§5.5.2** IRT-CTT/purification (400 words + Table 5.5)
  - Integrate: 5.2.4-5.2.5, 5.3.5-5.3.6, 5.4.4-5.4.5, 5.5.4-5.5.5
  - Table: 11 rows × 7 cols (r_theta_CTT, Steiger Z, p, RMSE, Slope Δ, Interpretation, Appendix ref)
  - Cross-refs: A.2.4-A.2.5, A.3.5-A.3.6, A.4.4-A.4.5, A.5.4-A.5.5

**Checkpoint saved:** `restructure_notepad.md` updated with Phase 3 COMPLETE + table data extracted

---

### Phase 4: Write Synthesis Sections (2 hours)
**Target:** 5 NEW synthesis sections (~3,000 words)

- [ ] **§5.1.4** Power-Law Synthesis (800 words)
  - Topics: Temporal distinctiveness, VR middle ground (α=0.41), two-phase interpretation, practice effects, model averaging imperative

- [ ] **§5.2.4** Content Synthesis (500 words)
  - Topics: Encoding strength ≠ decay rate, theta vs probability scale, dual-scale reporting, common mechanism

- [ ] **§5.3.3** Age Synthesis (600 words)
  - Topics: Context-supported memory (Craik & Rose), VR scaffolding, hippocampal aging hypothesis NOT supported, Ch7 forward reference

- [ ] **§5.4.4** Individual Differences Synthesis (600 words)
  - Topics: Model averaging paradigm shift (432-fold), functional form sensitivity, clustering instability, design limitation

- [ ] **§5.5.3** Methodological Synthesis (500 words)
  - Topics: When to use IRT vs CTT, within-study vs cross-study, Ch7 forward reference

**Checkpoint saved:** `restructure_notepad.md` updated with Phase 4 COMPLETE

---

### Phase 5: Rewrite Summary (§5.6) (30 min)

- [ ] Read current §5.6 summary
- [ ] Rewrite with 5 thematic takeaways (150 words each)
- [ ] Add forward references to Ch6 and Ch7 (200 words)
- [ ] Update cross-references (no orphaned §5.X.Y.Z)

**Target:** 1,000 words
**Checkpoint saved:** `restructure_notepad.md` updated with Phase 5 COMPLETE

---

### Phase 6: Populate Appendix A (2 hours)

- [ ] **A.1** General (5 RQs: 5.1.1-5.1.5)
  - A.1.1 already populated ✅
  - A.1.2-A.1.5 copy from OLD

- [ ] **A.2** Domain (7 RQs: 5.2.1-5.2.7)
  - Copy all 7 from OLD
  - Add "Main Chapter Reference: §X.Y" headers

- [ ] **A.3** Paradigm (9 RQs: 5.3.1-5.3.9)
  - Copy all 9 from OLD
  - Add cross-references

- [ ] **A.4** Schema (7 RQs: 5.4.1-5.4.7)
  - Copy all 7 from OLD
  - Add cross-references

- [ ] **A.5** Spatial (6 RQs: 5.5.1-5.5.6)
  - Copy all 6 from OLD
  - Add cross-references

**Target:** 25,000+ words (complete preservation)
**Checkpoint saved:** `restructure_notepad.md` updated with Phase 6 COMPLETE

---

### Phase 7: Final Verification and Polish (1.5 hours)

#### Cross-Reference Validation
- [ ] Check all "See Appendix A.X.Y" references resolve
- [ ] Check all "Main Chapter: §X.Y" back-references resolve
- [ ] Update orphaned §5.X.Y.Z references

#### Figure Renumbering
- [ ] Main chapter figures: 5.1-5.15 (12-15 figures)
- [ ] Appendix figures: A.1-A.55 (all original figures)
- [ ] Update all captions and in-text references

#### Word Count Verification
- [ ] Main chapter: Target 14,000 words (range 12-16k acceptable)
- [ ] Appendix A: Target 25,000+ words
- [ ] Total should match or slightly exceed original 37k

#### Table Verification
- [ ] Table 5.1 (Functional form comparison) renders correctly
- [ ] Table 5.2 (Content facet comparison) renders correctly
- [ ] Table 5.3 (Age effects summary) renders correctly
- [ ] Table 5.4 (ICC decomposition) renders correctly
- [ ] Table 5.5 (IRT-CTT convergence) renders correctly

#### Quality Checks
- [ ] Read §5.1 end-to-end (narrative flow)
- [ ] Read §5.2 end-to-end (narrative flow)
- [ ] Read §5.3 end-to-end (narrative flow)
- [ ] Read §5.4 end-to-end (narrative flow)
- [ ] Read §5.5 end-to-end (narrative flow)
- [ ] Read §5.6 summary (captures all themes)
- [ ] Verify flagship RQs show depth
- [ ] Verify integrated sections adequate
- [ ] Check syntheses connect to theory
- [ ] Validate forward references to Ch6/Ch7

**Checkpoint saved:** `restructure_notepad.md` updated with Phase 7 COMPLETE → PROJECT COMPLETE

---

## SESSION LOG (Track Work Across Sessions)

### Session 1: 2025-12-10 (Planning Phase)
**Duration:** ~2 hours
**Work Completed:**
- Context-finder analysis of thesis structure (Ch5/Ch6/Ch7 boundaries)
- Created restructure_plan_v2_GOLD.md (comprehensive master plan)
- Created restructure_notepad.md (THIS FILE - stateful tracking)
- Restored chapter_5_empirical.md from backup (reverted condensing attempt)
- Awaiting user approval to begin Phase 1 execution

**Token Usage:** ~117k / 200k

**Next Session Start Point:**
- Read restructure_plan_v2_GOLD.md (master plan)
- Read restructure_notepad.md (THIS FILE)
- Check "CURRENT STATUS" section above
- Continue from current phase checkpoint

**Files Modified This Session:**
- Created: restructure_plan_v2_GOLD.md
- Created: restructure_notepad.md
- Modified: chapter_5_empirical.md (restored from backup)
- No changes to: appendix.md (A.1.1 already populated, preserved)

---

### Session 2: [DATE] (Phase X)
**Duration:** [TIME]
**Work Completed:**
- [Bullet list of accomplishments]

**Token Usage:** [X]k / 200k

**Next Session Start Point:**
- [Instructions for next session]

**Files Modified This Session:**
- [List files changed]

**Checkpoint:** [Phase X complete/in-progress]

---

### Session 3: [DATE] (Phase X)
[Same template as Session 2]

---

## DECISION LOG (Track User Approvals)

**User Decision 1:** Restructuring Approach
- Date: PENDING
- Decision: [Approve / Modify / Reject]
- Notes: [Any modifications requested]

**User Decision 2:** Flagship RQ Selections
- Date: PENDING
- Decision: [Approve / Modify list]
- Modified list: [If changes requested]

**User Decision 3:** Word Count Target
- Date: PENDING
- Decision: [Accept 14k / Request lower target]
- Notes: [Acceptable range]

**User Decision 4:** Phase 1 Execution
- Date: PENDING
- Decision: [Proceed / Wait]

---

## ISSUE TRACKER (Problems Encountered)

No issues logged yet.

### Issue 1: [TITLE]
- Date: [YYYY-MM-DD]
- Description: [Problem encountered]
- Resolution: [How fixed, or OPEN if unresolved]
- Impact: [High / Medium / Low]

---

## QUICK REFERENCE (Key File Locations)

**Main Files:**
```
results/ch5/chapter_5_empirical.md          (ORIGINAL, 37k words)
results/ch5/chapter_5_empirical_FULL.md     (BACKUP, identical to original)
results/ch5/chapter_5_empirical_RESTRUCTURED.md  (TARGET, to be created Phase 1)
results/ch5/appendix.md                     (Appendix A, A.1.1 populated)
results/ch5/restructure_plan_v2_GOLD.md     (Master plan, 15k words)
results/ch5/restructure_notepad.md          (THIS FILE, session state)
```

**Reference Files:**
```
docs/v4/thesis/ANALYSES_CH6.md              (Ch6 metacognition context)
docs/v4/thesis/ANALYSES_CH7.md              (Ch7 external validity context)
docs/v3/irt_methodology.md                  (IRT technical details)
docs/v3/lmm_methodology.md                  (LMM technical details)
```

**Figure Directories:**
```
results/ch5/5.1.1/plots/                    (Figures 5.1-5.2)
results/ch5/5.1.2/plots/                    (Figure 5.3)
results/ch5/5.1.3/plots/                    (Figure 5.4)
[... continues for all 34 RQs ...]
```

---

## NOTES FOR FUTURE SESSIONS

**When resuming after /clear:**
1. Copy/paste the QUICK RESUME PROMPT (top of this file)
2. I will read restructure_plan_v2_GOLD.md and restructure_notepad.md
3. I will check "CURRENT STATUS" section for phase checkpoint
4. I will continue from the next unchecked [ ] task in Phase Checklist
5. I will update SESSION LOG with new session entry
6. I will save checkpoint after completing each phase

**Important Conventions:**
- Mark completed tasks with [x] in Phase Checklist
- Update CURRENT STATUS section when phase changes
- Log all file modifications in Session Log
- Log all user decisions in Decision Log
- Log any issues/blockers in Issue Tracker
- Commit to git after each phase completion (optional but recommended)

**Session Management:**
- Each session ~2-4 hours of focused work
- Complete full phase before stopping (don't stop mid-phase)
- Update notepad.md BEFORE ending session (checkpoint save)
- User can /clear between phases without losing state

---

## MASTER PLAN SUMMARY (Quick Reference)

**5 Thematic Narrative Arcs:**
1. §5.1 Power-Law Paradigm (3,500 words)
2. §5.2 Content Effects (3,000 words)
3. §5.3 Age-Invariant (2,000 words)
4. §5.4 Individual Differences (2,500 words)
5. §5.5 Methodological Validation (1,500 words)

**8 Flagship RQs (Full Detail):**
1. 5.1.1 - General trajectory form
2. 5.1.2 - Two-phase forgetting
3. 5.2.1 - Domain trajectories
4. 5.3.1+5.3.2 - Paradigm trajectories (combined)
5. 5.1.3 - General age effects
6. 5.1.4 - Variance decomposition
7. 5.1.5 - Latent profiles
8. 5.2.4 - IRT-CTT convergence

**26 Integrated RQs (Summarized with Tables)**

**5 Summary Tables:**
- Table 5.1: Functional form comparison (10 facets)
- Table 5.2: Content facet comparison (11 facets)
- Table 5.3: Age effects summary (5 analyses)
- Table 5.4: ICC decomposition (5 analyses)
- Table 5.5: IRT-CTT convergence (11 comparisons)

---

**END RESTRUCTURE NOTEPAD**

**Status:** READY FOR SESSION 2 (pending user approval to begin Phase 1)
