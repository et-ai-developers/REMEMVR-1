# RQ 5.3: Do Free Recall, Cued Recall, and Recognition Exhibit Different Forgetting Trajectories?

**Chapter:** 5
**RQ Number:** 3
**Full ID:** 5.3

---

## Research Question

**Primary Question:**
Are there paradigm-specific differences in the rate and pattern of episodic forgetting over 6 days?

**Scope:**
This RQ examines forgetting rates for three retrieval paradigms (Item Free Recall, Item Cued Recall, Item Recognition) using IRT-derived ability estimates across four test sessions. Time variable uses TSVR (actual hours since encoding, 0 to ~200 hours), not nominal days. Focuses on Item-level questions only (IFR, ICR, IRE) - excludes Task Cued Recall (TCR) due to floor/ceiling effects and limited question types.

**Theoretical Framing:**
Transfer-appropriate processing theory (Morris et al., 1977) predicts that retrieval success depends on match between encoding and retrieval conditions. The retrieval support gradient hypothesis suggests paradigms lie on a continuum from self-initiated retrieval (Free Recall, most demanding) through partial support (Cued Recall) to recognition-based retrieval (Recognition, least demanding). Understanding paradigm-specific trajectories tests whether retrieval demands affect not just baseline performance but forgetting rate.

---

## Theoretical Background

**Relevant Theories:**
- **Transfer-Appropriate Processing (Morris et al., 1977):** Retrieval success depends on the match between encoding processes and retrieval demands. Different paradigms tap different retrieval processes.
- **Retrieval Support Continuum (Tulving, 1983):** Memory paradigms can be ordered by the amount of retrieval support provided - Free Recall provides minimal support, Cued Recall provides partial cues, Recognition provides complete target for matching.
- **Familiarity vs Recollection (Yonelinas, 2002):** Recognition can succeed via familiarity (fast, automatic), while Free Recall requires effortful recollection. This predicts Recognition will be most resistant to forgetting.

**Key Citations:**
- Morris, C. D., Bransford, J. D., & Franks, J. J. (1977): Transfer-appropriate processing framework
- Tulving, E. (1983): Elements of Episodic Memory - retrieval support gradients
- Bates, D. et al. (2015): LMM with random slopes methodology

**Theoretical Predictions:**
Transfer-appropriate processing and retrieval support theories predict an ordered effect: Free Recall (most demanding, self-initiated) will show steepest forgetting, Cued Recall (partial support) intermediate, and Recognition (familiarity-based, maximal support) slowest forgetting. The ordering should be monotonic, not just pairwise different.

**Literature Gaps:**
Most paradigm comparison studies examine baseline differences, not forgetting trajectories. Few studies test all three paradigms within the same participants using identical encoding (incidental) across longitudinal timepoints. REMEMVR's design allows isolation of retrieval support effects because encoding is identical (participants don't know which paradigm they'll face).

---

## Hypothesis

**Primary Hypothesis:**
Free Recall will show steepest forgetting (requires self-initiated retrieval), followed by Cued Recall (partial support), with Recognition showing most shallow decline (familiarity-based, least demanding). This reflects an ordered retrieval support gradient.

**Secondary Hypotheses:**
1. Divergence between paradigms will increase over time (trajectories fan out)
2. All paradigms will show significant forgetting (slopes < 0)
3. Non-linear models (Lin+Log or Quadratic) will fit better than simple linear

**Theoretical Rationale:**
The retrieval support gradient hypothesis predicts that as retrieval demands decrease (Free -> Cued -> Recognition), memory becomes more resilient to forgetting. Free Recall depends heavily on self-initiated retrieval processes that may decay faster than familiarity-based recognition. Cued Recall occupies an intermediate position - partial cues reduce but don't eliminate retrieval demands.

**Expected Effect Pattern:**
Significant Paradigm x Time interaction in LMM analysis. Post-hoc contrasts should show:
- Cued vs Free: Beta > 0 (Cued forgetting slower than Free)
- Recognition vs Free: Beta > 0 (Recognition slowest, largest difference from Free)
- Effect sizes at Day 6: Free vs Cued d ~ 0.3-0.4, Free vs Recognition d ~ 0.6-0.8

---

## Memory Domains

**Note:** This RQ is PARADIGM-based, not domain-based. It examines forgetting across retrieval paradigms rather than memory domains (What/Where/When). Items from ALL domains are included within each paradigm.

**Paradigms Examined:**

- [x] **Item Free Recall (IFR)**
  - Tag Pattern: `*IFR-*ANS`
  - Description: Self-initiated recall with minimal retrieval cues

- [x] **Item Cued Recall (ICR)**
  - Tag Pattern: `*ICR-*ANS`
  - Description: Recall with partial retrieval cues provided

- [x] **Item Recognition (IRE)**
  - Tag Pattern: `*IRE-*ANS`
  - Description: Recognition of previously seen items among distractors

**Paradigm Exclusions:**

- [ ] **Room Free Recall (RFR)** - Different response format, not directly comparable
- [ ] **Task Cued Recall (TCR)** - Only When questions, showed floor/ceiling effects

**Inclusion Rationale:**
Only Item-level paradigms (IFR, ICR, IRE) are included because they are directly comparable - same item types, same scoring, same response format. This provides clean paradigm comparison without confounds from different question types.

**Domain Note:**
Within each paradigm, items span What (-N-), Where (-L-/-U-/-D-), and When (-O-) domains. Domain is not a factor in this analysis - theta scores aggregate across all domains within each paradigm.

---

## Analysis Approach

**Analysis Type:**
IRT (Item Response Theory) for ability estimation + LMM (Linear Mixed Models) for trajectory modeling

**High-Level Workflow:**

**Step 0:** Data Preparation
- Get raw scores from RQ 5.1 output: `./results/ch5/rq1/data/step00_irt_input.csv`
- Filter to keep only IFR, ICR, IRE columns (remove non-item paradigms)
- Get TSVR mapping from: `./results/ch5/rq1/data/step00_tsvr_mapping.csv`
- Create Q-matrix with paradigm factor structure:
  - free_recall = *IFR*
  - cued_recall = *ICR*
  - recognition = *IRE*

**Step 1:** IRT Analysis
- Execute IRT pipeline with correlated factors, 2-category GRM
- Extract theta scores (Theta_Free, Theta_Cued, Theta_Recognition) for each UID x Test

**Step 2:** Item Purification
- Remove items with extreme difficulty (|b| > 3.0) or low discrimination (a < 0.4)
- Within-paradigm filtering

**Step 3:** IRT Re-calibration
- Re-run IRT on purified item set
- Extract final theta scores

**Step 4:** Data Preparation for LMM
- Reshape theta scores from wide to long format (Paradigm as factor variable)
- Create time transformations: Days, Days^2, log(Days+1) using continuous TSVR variable
- Validate factor structure

**Step 5:** Model Fitting and Selection
- Fit 5 candidate LMMs with Paradigm x Time interactions:
  - Linear: Time x Paradigm
  - Quadratic: (Time + Time^2) x Paradigm
  - Logarithmic: log(Time+1) x Paradigm
  - Lin+Log: (Time + log(Time+1)) x Paradigm
  - Quad+Log: (Time + Time^2 + log(Time+1)) x Paradigm
- Treatment coding: Free Recall as reference
- Random intercepts and slopes by UID
- Fit with REML=False, select best via AIC

**Step 6:** Post-hoc Contrasts
- Extract Time x Paradigm interaction terms from best model
- Test differences in forgetting slopes: Cued-Free, Recognition-Free
- Report both with and without Bonferroni correction (alpha = 0.0033/3 = 0.0011)

**Step 7:** Effect Size Computation
- Calculate Cohen's d for paradigm differences at Day 6 (maximal divergence expected)
- Report: d_Free_Cued, d_Free_Recognition, d_Cued_Recognition

**Step 8:** Visualization
- Generate trajectory plot: 3 lines (Free/Cued/Recognition) over TSVR 0 -> 200 hours
- Include observed means with 95% CIs and model predictions

**Data Preprocessing (Per Solution Section 1.4):**
- **Accuracy Scores (-ANS tags):** Dichotomize before IRT: 1 = 1, all <1 = 0 (no partial credit)
- **IRT Model:** GRM (Graded Response Model) with 2 categories for dichotomized items
- **Correlated Factors:** Paradigm factors allowed to correlate in IRT model

**Special Methods:**
- **2-Pass IRT Purification:** Mandatory to remove psychometrically problematic items
- **TSVR Time Variable:** Use actual hours since encoding, not nominal days (0, 1, 3, 6)
- **Treatment Coding (Free as Reference):** Free Recall is most demanding, natural baseline for contrasts
- **Dual Reporting:** Report both corrected (Bonferroni) and uncorrected p-values

---

## Data Source

**Data Type:**
DERIVED (from RQ 5.1 outputs) + Subset/Regroup

### DERIVED Data Source:

**Source RQ:**
RQ 5.1 (Domain-Specific Forgetting Trajectories)

**File Paths:**
- `results/ch5/rq1/data/step00_irt_input.csv` (raw dichotomized VR item scores)
- `results/ch5/rq1/data/step00_tsvr_mapping.csv` (TSVR time variable mapping)

**Dependencies:**
RQ 5.1 must complete Step 0 (data preparation, TSVR mapping) before this RQ can begin. This RQ uses the same base data but creates new IRT factors (paradigm-based instead of domain-based).

**Usage:**
This RQ filters the RQ 5.1 input data to Item paradigms only (IFR, ICR, IRE), then creates a new Q-matrix that groups items by paradigm instead of domain. A fresh IRT calibration is run with paradigm factors.

### Tag Patterns (for filtering):

**Included Patterns:**
- Item Free Recall: `*IFR-*ANS`
- Item Cued Recall: `*ICR-*ANS`
- Item Recognition: `*IRE-*ANS`

**Excluded Patterns:**
- Room Free Recall: `*RFR-*` (different response format)
- Task Cued Recall: `*TCR-*` (only When questions, floor/ceiling effects)

### Inclusion/Exclusion Criteria:

**Participants:**
- [x] All 100 participants (inherited from RQ 5.1)

**Items:**
- [x] Item paradigms only (IFR, ICR, IRE)
- [ ] Room Free Recall (RFR) - EXCLUDED (different response format)
- [ ] Task Cued Recall (TCR) - EXCLUDED (floor/ceiling effects, only When questions)

**Tests:**
- [x] All 4 tests (T1, T2, T3, T4)
- Note: Time variable uses TSVR (actual hours since encoding), not nominal days

---
