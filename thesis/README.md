# THESIS FOLDER ORGANIZATION

**Last updated:** 2025-11-01

---

## 📁 FOLDER STRUCTURE

```
thesis/
├── README.md                  ← This file
│
├── THESIS CHAPTERS (Main folder)
│   ├── introduction.md        ← Chapter 1: Introduction
│   ├── methods.md             ← Chapter 2: Method
│   ├── rationale.md           ← Chapter 3: Rationale/Design Decisions
│   └── chapters.md            ← Chapter planning/Q&A reference
│
├── analyses/                  ← ACTIVE ANALYSIS DOCUMENTS
│   ├── ANALYSES_DEFINITIVE.md ← THE ANALYSIS BIBLE (Part 0 complete)
│   ├── ANALYSES_CH5.md        ← Chapter 5: 15 RQs (streamlined)
│   ├── CH5_CERTIFICATION.md   ← Chapter 5 final certification
│   └── CH5_REVIEW.md          ← Chapter 5 comprehensive review
│
└── archive/                   ← OLD/REFERENCE DOCUMENTS
    ├── analyses.md            ← Original analyses (superseded by DEFINITIVE)
    ├── ANALYSES_AUDIT.md      ← Historical audit of original analyses
    ├── refresher.md           ← Context document (post-memory-wipe)
    └── introduction-edits.md  ← Draft additions (pending integration)
```

---

## 🎯 ACTIVE WORKING FILES

**For analysis bible work:**
- **analyses/ANALYSES_DEFINITIVE.md** - Part 0 complete (global specifications)
- **analyses/ANALYSES_CH5.md** - Chapter 5 complete (15 RQs streamlined)

**Next to create:**
- **analyses/ANALYSES_CH6.md** - Chapter 6: Metacognition (15 RQs)
- **analyses/ANALYSES_CH7.md** - Chapter 7: Individual Differences (20 RQs)

**For code implementation:**
- Start with **analyses/ANALYSES_DEFINITIVE.md** Part 0 (pipeline specifications)
- Then **analyses/ANALYSES_CH5.md** for Chapter 5 RQs

---

## 📚 REFERENCE DOCUMENTS

**Thesis chapters (main folder):**
- **introduction.md** - Episodic memory theory, frameworks, VR rationale
- **methods.md** - N=100, 4 rooms, 4 tests, VR setup, cognitive battery
- **rationale.md** - Design decisions, why household rooms, why 6 items, etc.
- **chapters.md** - Planning notes, research questions lists, user Q&A

**Archive (historical):**
- **archive/analyses.md** - Original 800-line analysis document (pre-audit)
- **archive/ANALYSES_AUDIT.md** - Line-by-line audit identifying 13 critical issues
- **archive/refresher.md** - Context document created after memory compaction
- **archive/introduction-edits.md** - Draft theory sections (schema, aging, individual differences)

---

## 🔑 KEY DECISIONS DOCUMENTED

**In ANALYSES_DEFINITIVE.md Part 0:**
- ✅ NO partial credit (dichotomous 0/1 only)
- ✅ Correlated factors = primary model (oblique rotation)
- ✅ Factor-specific discrimination for theta → probability transform
- ✅ Bonferroni correction: α_chapter = 0.05/k_RQs
- ✅ Complete data pipeline: master.xlsx → IRT → LMM → results

**In CH5_CERTIFICATION.md:**
- ✅ All 15 RQs approved for implementation
- ✅ Statistical design: GOLD STANDARD
- ✅ Data pipeline: UNAMBIGUOUS
- ✅ Code-ready: YES

---

## 📝 WORKFLOW STATUS

**COMPLETED:**
- ✅ Part 0: Global Specifications (800 lines)
- ✅ Chapter 5: 15 RQs streamlined (1,520 lines)
- ✅ Chapter 5 review and certification

**NEXT:**
- ⏳ Chapter 6: Metacognition (15 RQs)
- ⏳ Chapter 7: Individual Differences (20 RQs)
- ⏳ Compile into final ANALYSES_DEFINITIVE.md
- ⏳ OR: Start code implementation for Chapter 5

---

## 🎓 THESIS CHAPTERS OVERVIEW

**Chapter 1: Introduction** (introduction.md)
- Episodic memory definitions, anatomy, frameworks
- PMAT, MTT, Scene Construction Theory
- VR rationale
- **TO ADD:** Schema theory, aging effects, individual differences (from archive/introduction-edits.md)

**Chapter 2: Method** (methods.md)
- N=100, ages 20-70 (stratified)
- 4 VR rooms, 6 items per room
- 4 test sessions (Days 0, 1, 3, 6)
- Cognitive battery: RAVLT, BVMT, NART, RPM

**Chapter 3: Rationale** (rationale.md)
- Design decisions explained
- Why household rooms, why congruence manipulation, etc.

**Chapter 4: Statistical Analysis** (TBD)
- Will draw from ANALYSES_DEFINITIVE.md Part 0

**Chapter 5: Forgetting Trajectories** (analyses/ANALYSES_CH5.md)
- 15 research questions
- Domain differences, paradigm effects, functional form, age, IRT vs CTT, profiles

**Chapter 6: Metacognition** (To be created)
- 15 research questions
- Confidence trajectories, calibration, high-confidence errors

**Chapter 7: Individual Differences** (To be created)
- 20 research questions
- Cognitive test predictions, age mediation, profiles, predictive models

**Chapter 8: Discussion** (TBD)

---

**END OF README**
