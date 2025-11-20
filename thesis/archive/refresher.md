# ANALYSIS BIBLE TASK - CONTEXT REFRESHER

**Purpose:** Resume analysis bible creation after context compaction
**Date Created:** 2025-11-01
**Task Status:** ~30% complete - Part 0 done, Chapter 5 templates created, Chapters 6-7 pending

---

## TASK OBJECTIVE

Create **ANALYSES_DEFINITIVE.md** - a comprehensive, zero-ambiguity statistical analysis specification for PhD thesis Chapters 5, 6, and 7 (50 research questions total).

**Quality Standard:** "Analysis bible" - complete executable specifications with NO room for assumptions.

**User Quote:** *"This document will be the backbone of my thesis so any mistakes will be CATASTROPHIC! Take your time, think HARD, and make this document live up to the description of analysis bible."*

---

## CRITICAL DECISIONS MADE (User-Approved)

### ✅ DECISION 1: Calibration Nomenclature (NOT "Utility")
**Implementation:**
```python
# Primary metric (direction)
Calibration = P_correct - P_high_conf
# Positive = Underconfident, Negative = Overconfident, Zero = Perfect

# Secondary metric (magnitude)
Calibration_error = abs(Calibration)
# Lower = Better, symmetrically treats over/under confidence
```

**Rationale:** Intuitive interpretation, removes confusing ×-1 inversions, matches standard nomenclature.

**Action:** Remove ALL "Utility" references from Chapter 6, replace with Calibration/Calibration_error.

---

### ✅ DECISION 2: TC_ IRT Processing
**Implementation:** TC_ (confidence) undergoes **IDENTICAL** IRT pipeline as TQ_ (accuracy)
- Same Q-matrix structure
- Same discrimination thresholds (0.5 ≤ discrim ≤ 4.0)
- Same iterative purification
- Items may differ between TQ_ and TC_ (expected)
- For calibration analyses: Use **intersection** of retained items from both

**Rationale:** Enables direct P(correct) vs P(high_conf) comparison on same 0-1 scale.

---

### ✅ DECISION 3: Probability Transformation - Factor-Specific Discrimination
**Implementation:**
```python
# For each factor (What, Where, When)
avg_discrim_factor = retained_items[f'Discrim_{factor}'].mean()  # Factor-specific!
avg_difficulty = retained_items['Difficulty'].mean()

P_response = 1 / (1 + np.exp(-(avg_discrim_factor * (theta - avg_difficulty))))
```

**Theoretical Justification:** Factor-specific discrimination reflects dimension-specific differentiation. Using Overall_Discrimination averages across orthogonal factors → dilutes signal.

**Example:** Item loading on "What" uses Discrim_What (e.g., 2.3), not Overall (e.g., 1.4).

---

### ✅ DECISION 4: Data Source for Chapter 7
**Source:** All data in master.xlsx, extracted via variables.xlsx tag system
- dfData.csv already contains ALL variables (RAVLT, BVMT, NART, RPM, demographics)
- Use existing data pipeline (data/data.py startup())
- **NEVER edit master.xlsx directly**
- User will explain tag system after bible complete

---

### ✅ DECISION 5: Model Pickling Strategy
**Implementation:**
- RECOMPUTE=True → All LMMs re-run from scratch
- Save NEW pickles in irt.py for Chapter 7 random effects extraction
- File pattern: `results/{set}/pkl/{analysis_name}.pkl`
- Method: `fit.save(model_path)` (statsmodels MixedLMResults.save())

---

## DOCUMENT STRUCTURE

### ANALYSES_DEFINITIVE.md (Target: 5000+ lines)

**Part 0: Global Specifications** (800 lines) ✅ COMPLETE
- IRT pipeline (TQ_ and TC_ identical processing)
- Probability transformation (factor-specific discrimination)
- Calibration nomenclature (signed + magnitude)
- LMM specifications (5 candidate models, AIC selection)
- Multiple comparisons correction (Bonferroni)
- Effect size reporting (d, f², R²)
- Assumption checking (convergence, normality, homoscedasticity)
- Data validation functions
- Reproducibility requirements (seed=42)
- Standardized RQ schema (8 mandatory elements)

**Part 1: Chapter 5 - Forgetting Trajectories** (1500 lines target)
- 15 Research Questions
- Templates completed: RQ5.1, RQ5.2 (~250 lines total)
- Remaining: RQ5.3-5.15 (abbreviated placeholders)

**Part 2: Chapter 6 - Metacognition** (1500 lines target)
- 15 Research Questions
- Status: Not started

**Part 3: Chapter 7 - Individual Differences** (2000 lines target)
- 20 Research Questions
- Status: Not started

---

## STANDARDIZED RQ SCHEMA (8 Mandatory Elements)

Every RQ MUST contain:

1. **Research Question** - Precise, answerable question
2. **Hypothesis** - Directional prediction OR "Exploratory" with rationale
3. **Data Required** - Exact files with full paths, columns, preprocessing
4. **Analysis Recipe** - Numbered steps with complete executable code
5. **Statistical Justification** - Why this method? Theoretical grounding, citations
6. **Expected Output** - Exact tables/plots with column specifications
7. **Success Criteria** - Diagnostics checklist for validation
8. **Reviewer Rebuttals** - Anticipated objections with preemptive responses

**Quality Standard:** RQ5.1 and RQ5.2 (see ANALYSES_CH5.md lines 1-250) are REFERENCE TEMPLATES showing required detail level.

---

## FILES CREATED

### 1. thesis/ANALYSES_AUDIT.md (1112 lines)
**Purpose:** Comprehensive line-by-line audit of original analyses.md
**Key Sections:**
- 13 CRITICAL issues identified (all resolved)
- User decisions documented (lines 1000-1112)
- Schema requirements defined
- 20+ HIGH/MEDIUM priority items for improvement

**Status:** Reference document, decisions migrated to DEFINITIVE.md

---

### 2. thesis/ANALYSES_DEFINITIVE.md (800 lines)
**Purpose:** THE analysis bible (target final version)
**Current Contents:**
- Part 0: Global Specifications (COMPLETE)
- Parts 1-3: To be added

**Next Steps:**
1. Append ANALYSES_CH5.md (after completing RQ5.3-5.15)
2. Create Chapter 6 (15 RQs)
3. Create Chapter 7 (20 RQs)
4. Final validation pass

---

### 3. thesis/ANALYSES_CH5.md (current: ~300 lines, target: ~1500)
**Purpose:** Working file for Chapter 5
**Current Contents:**
- RQ5.1: Domain differences (What/Where/When) - COMPLETE TEMPLATE
- RQ5.2: Differential consolidation (piecewise) - COMPLETE TEMPLATE
- RQ5.3-5.15: Abbreviated placeholders

**Template Quality (RQ5.1 example):**
- 140 lines
- 7 analysis steps with executable code
- Data validation functions
- Model selection (5 candidates)
- Post-hoc contrasts with Bonferroni
- Effect sizes (Cohen's d)
- Trajectory plotting code
- Assumption checks
- 3 reviewer rebuttals

**Next:** Expand RQ5.3-5.15 to same detail level

---

## KEY SPECIFICATIONS FROM PART 0

### IRT Pipeline (Section 0.1)
- Software: deepirtools IWAVE
- Model: Graded Response Model (GRM)
- TQ_: Dichotomous (0/1), 2 categories
- TC_: Graded (0, 0.25, 0.5, 0.75, 1.0), 5 categories
- Hyperparameters (p1_med): batch=2048, iw=100, mc_fit=1, mc_score=100
- Iterative purification: Remove items with 0.5 > discrim > 4.0, refit until stable
- Output files: `results/{set}/TQ_corr_noroom_2cats_p1_med_data_ability.csv` (thetas)
- Output files: `results/{set}/TQ_corr_noroom_2cats_p1_med_data_difficulty.csv` (params)

### Probability Transformation (Section 0.2)
```python
# Factor-specific implementation
retained_items = df_params[
    (df_params[f'Discrim_{factor}'] >= 0.5) &
    (df_params[f'Discrim_{factor}'] <= 4.0)
]

avg_discrim = retained_items[f'Discrim_{factor}'].mean()  # NOT Overall_Discrimination
avg_difficulty = retained_items['Difficulty'].mean()

P_factor = 1 / (1 + np.exp(-(avg_discrim * (theta_factor - avg_difficulty))))
```

### LMM Specification (Section 0.4)
```python
import statsmodels.formula.api as smf

# 5 candidate models, select via AIC
models = {
    'Linear': "Outcome ~ Time * Factors + (Time | UID)",
    'Quadratic': "Outcome ~ (Time + Time_sq) * Factors + (Time | UID)",
    'Log': "Outcome ~ log_Time * Factors + (Time | UID)",
    'Lin+Log': "Outcome ~ (Time + log_Time) * Factors + (Time | UID)",  # Often best
    'Quad+Log': "Outcome ~ (Time + Time_sq + log_Time) * Factors + (Time | UID)"
}

# REML=False for AIC comparison
fit = smf.mixedlm(formula, data=df, groups=df["UID"], re_formula="~Time").fit(method=['lbfgs'], reml=False)
```

### Bonferroni Correction (Section 0.5)
- **Chapter 5:** α = 0.05/15 = 0.0033
- **Chapter 6:** α = 0.05/15 = 0.0033
- **Chapter 7:** α = 0.05/20 = 0.0025
- **Nested post-hocs:** α_chapter / k_comparisons (e.g., 0.0033/3 = 0.0011 for 3 pairwise tests)

### Reproducibility (Section 0.9)
```python
SEED = 42
np.random.seed(SEED)
random.seed(SEED)
torch.manual_seed(SEED)
```

---

## CHAPTER 5 RQ SUMMARY

| RQ | Title | Analysis Set | Key Test |
|----|-------|--------------|----------|
| 5.1 | Domain differences | All by Domain | Domain × Time interaction |
| 5.2 | Differential consolidation | All by Domain | Segment × Domain 3-way |
| 5.3 | Paradigm differences | All by Paradigm | Paradigm × Time |
| 5.4 | Retrieval support buffer | All by Paradigm | Ordered trend test |
| 5.5 | Congruence effects | Items by Congruence | Congruence × Time |
| 5.6 | Schema consolidation | Items by Congruence | Piecewise × Congruence |
| 5.7 | Functional form | All (single factor) | 5-model AIC comparison |
| 5.8 | Two-phase evidence | All | Quadratic term significance |
| 5.9 | Age effects | All by Domain + Age | Age × Time |
| 5.10 | Age × Domain | All by Domain + Age | Age × Domain × Time 3-way |
| 5.11 | IRT vs CTT | All by Domain | Parallel LMMs, correlation |
| 5.12 | Purified CTT | All by Domain | Retained items only |
| 5.13 | Between-person variance | All | ICC for random slopes |
| 5.14 | Forgetting profiles | All | K-means on slopes |
| 5.15 | Item difficulty × Time | All (item-level) | Cross-level interaction (pymer4) |

---

## CHAPTER 6 RQ SUMMARY

**Focus:** Metacognition (confidence calibration, resolution, errors)

**Critical Change:** All "Utility" → "Calibration" and "Calibration_error"

| RQ | Title | Primary Metric |
|----|-------|----------------|
| 6.1 | Parallel decline? | Compare slopes (P_correct vs P_high_conf) |
| 6.2 | Calibration trajectory | Calibration = P_correct - P_high_conf |
| 6.3 | Day 0 vs Day 6 calibration | Calibration curves (binned) |
| 6.4 | Resolution decline | Gamma, AUROC over time |
| 6.5 | Calibration error magnitude | Calibration_error = abs(Calibration) |
| 6.6 | Domain differences | Calibration_error by domain |
| 6.7 | Paradigm effects | Gamma by paradigm |
| 6.8 | High-confidence errors | Proportion TQ=0 & TC≥0.75 |
| 6.9 | Congruence × HCE | HCE by congruence type |
| 6.10 | Day 0 confidence predicts forgetting | Logistic GLMM |
| 6.11 | Confidence variability | SD(TC) predicts slope |
| 6.12 | Age × Calibration | Age effects on calibration |
| 6.13 | Ability × Calibration | Theta correlation with calibration |
| 6.14 | Confidence weighting | TQ × TC weighted scores |
| 6.15 | 2×2 decomposition | Correct/Incorrect × High/Low confidence |

---

## CHAPTER 7 RQ SUMMARY

**Focus:** Individual differences (cognitive tests, demographics, profiles)

**Data Source:** dfData.csv (via data/data.py startup())
- Contains: RAVLT, BVMT, NART, RPM, Age, Sex, Education, DASS
- Random effects extracted from saved LMMs (Chapter 5)

| RQ | Title | Predictors | Outcome |
|----|-------|-----------|---------|
| 7.1 | Test validity | RAVLT, BVMT, NART, RPM | Intercept + Slope |
| 7.2 | Domain-specific | Tests × Domains | Intercept_What/Where/When |
| 7.3 | Encoding vs consolidation | Tests | Intercept vs Slope dissociation |
| 7.4 | Unique variance | Tests (full model) | 1 - R² |
| 7.5-7.7 | Domain predictions | RAVLT, BVMT, RPM | Domain-specific intercepts |
| 7.8 | Age beyond tests | Age + Tests | Slope (incremental R²) |
| 7.9 | Age mediation | Age → Tests → REMEMVR | Sobel test, bootstrap CIs |
| 7.10 | Age × Test interaction | Age × RAVLT | Intercept (moderation) |
| 7.11-7.13 | Self-report | Sleep, DASS, Strategies | Intercept + Slope |
| 7.14-7.15 | Latent profiles | Intercepts (What/Where/When) | K-means clusters |
| 7.16-7.18 | Predictive model | All variables | Stepwise, cross-validation |
| 7.19-7.20 | Reverse inference | REMEMVR → Tests | Bidirectional prediction |

---

## NEXT STEPS

### Immediate (Resume Point)

1. **Complete Chapter 5** (RQ5.3-5.15)
   - Expand each to RQ5.1/5.2 detail level (~100 lines each)
   - Follow standardized 8-element schema
   - Include all code, justifications, rebuttals

2. **Create Chapter 6** (15 RQs)
   - Apply Calibration nomenclature throughout
   - TC_ IRT processing details
   - Probability transformation for both TQ_ and TC_
   - CTT convergence checks for every RQ

3. **Create Chapter 7** (20 RQs)
   - Random effects extraction from saved LMMs
   - dfData.csv as source (not separate cognitive_scores.csv)
   - Hierarchical regression specifications
   - Cross-validation procedures

4. **Final Validation**
   - Every RQ has 8 elements
   - All code executable
   - Success criteria complete
   - Reviewer rebuttals present
   - Cross-references accurate

### Compilation

Combine into single ANALYSES_DEFINITIVE.md:
```
Part 0: Global Specifications (DONE)
Part 1: Chapter 5 (append ANALYSES_CH5.md when complete)
Part 2: Chapter 6 (create)
Part 3: Chapter 7 (create)
```

---

## QUALITY CHECKPOINTS

Before marking any RQ complete, verify:

- [ ] 8 schema elements present
- [ ] Code is executable (not pseudocode)
- [ ] File paths are exact (results/{set}/TQ_corr_noroom_2cats_p1_med_data_ability.csv)
- [ ] Variable names match actual dataframe columns
- [ ] Statistical justifications cite sources where appropriate
- [ ] Success criteria include diagnostic checks (Q-Q plot, convergence, etc.)
- [ ] At least 2 reviewer rebuttals with substantive responses
- [ ] Expected output specifies exact table columns
- [ ] Bonferroni corrections calculated correctly
- [ ] Matches detail level of RQ5.1/5.2 templates

---

## USER CONTEXT

- **Project:** PhD thesis on episodic memory forgetting using VR
- **Sample:** N=100 participants (aged 20-70), 4 test sessions (Day 0/1/3/6)
- **Data:** 1,854 data points per participant (accuracy + confidence)
- **Method:** IRT (deepirtools) + LMM (statsmodels)
- **Philosophy:** Exploratory, framework-agnostic, NOT preregistered
- **Thesis Status:** Data collected, IRT pipeline functional, analyses pending

**User Quote:** *"I just want a robust and defensible thesis that is based on rock solid statistical analysis."*

---

## FILES TO REFERENCE

1. **thesis/ANALYSES_AUDIT.md** - All issues identified + resolutions
2. **thesis/ANALYSES_DEFINITIVE.md** - Part 0 complete
3. **thesis/ANALYSES_CH5.md** - RQ5.1, 5.2 templates
4. **data/data.py** - Data loading pipeline (master.xlsx + variables.xlsx tag system)
5. **analysis.py** - Current analysis code (probability transformation line 250)
6. **CLAUDE.md** - Project overview, acronyms, methodology

---

## COMMAND TO RESUME

After memory clear, read this file and say:

**"I've read the refresher. I understand the task is to complete the ANALYSES_DEFINITIVE.md analysis bible. Part 0 (800 lines) is done. Chapter 5 has RQ5.1 and RQ5.2 as reference templates (~100 lines each). I need to expand RQ5.3-5.15 to the same detail level, then create Chapters 6 and 7. All 5 critical user decisions are documented. Ready to proceed - which RQ should I start with?"**

Then continue from current progress.

---

**END OF REFRESHER**
