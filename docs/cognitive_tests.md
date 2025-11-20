# Cognitive Tests Reference

**Purpose:** Explanation of cognitive tests used in REMEMVR and their scoring procedures.

**Audience:** Data-prep agent, analysis-executor agent when analyzing Chapter 7 RQs.

**Last Updated:** 2025-01-04

---

## OVERVIEW

REMEMVR includes a cognitive battery to assess individual differences in memory and intelligence:

1. **RAVLT** (Rey Auditory Verbal Learning Test) - Verbal episodic memory
2. **BVMT-R** (Brief Visuospatial Memory Test - Revised) - Visual/spatial memory
3. **NART** (National Adult Reading Test) - Premorbid IQ estimate
4. **RPM** (Raven's Progressive Matrices) - Fluid intelligence

**Purpose:** Predict REMEMVR performance and understand individual differences.

**Chapter:** 7 (Individual Differences in Episodic Memory)

---

## RAVLT (REY AUDITORY VERBAL LEARNING TEST)

### Purpose:
Assess verbal episodic memory (encoding, storage, retrieval).

### Administration:

**List A (Target List):** 15 unrelated words read aloud

**Trial 1-5:** Immediate free recall after each presentation
- Participant recalls as many words as possible
- Repeat list and recall 5 times total

**List B (Distraction List):** 15 different words read aloud
- Single immediate free recall trial

**Trial 6 (Free Recall):** Recall List A without re-presentation
- Tests interference effects

**Trial 7 (Delayed Recall):** Recall List A after 20-30 minute delay
- Tests long-term retention

**Recognition Trial:** Presented with 50 words (15 List A, 15 List B, 20 distractors)
- Participant identifies which words were in List A

### Scoring:

**Primary Scores (Tags in master.xlsx):**
- `A010-COG-X-RAV-T1Sc` through `A010-COG-X-RAV-T5Sc` = Trials 1-5 scores (0-15 each)
- `A010-COG-X-RAV-TDSc` = List B recall (0-15)
- `A010-COG-X-RAV-FRSc` = Free recall of List A (0-15)
- `A010-COG-X-RAV-DRSc` = Delayed recall of List A (0-15)

**Timing Data:**
- `A010-COG-X-RAV-T1Ti` through `A010-COG-X-RAV-T5Ti` = Trial durations (seconds)
- `A010-COG-X-RAV-TDTi` = Distraction trial duration
- `A010-COG-X-RAV-FRTi` = Free recall duration
- `A010-COG-X-RAV-DRDe` = Delay period
- `A010-COG-X-RAV-DRTi` = Delayed recall duration

**Recognition Scores:**
- `A010-COG-X-RAV-RXXA` = Correctly identified List A words (0-15)
- `A010-COG-X-RAV-RXSA` = False alarms to semantically similar distractors
- `A010-COG-X-RAV-RXPA` = False alarms to phonetically similar distractors
- `A010-COG-X-RAV-RSPA` = False alarms to semantically + phonetically similar distractors
- `A010-COG-X-RAV-RXXB` = False alarms to List B words
- `A010-COG-X-RAV-RXSB` = False alarms to List B semantically similar
- `A010-COG-X-RAV-RXPB` = False alarms to List B phonetically similar
- `A010-COG-X-RAV-RSPB` = False alarms to List B semantically + phonetically similar

**Computed Scores (to be calculated during analysis):**
- **RAVLT_Total:** Sum of T1Sc-T5Sc (0-75)
- **Learning:** T5Sc - T1Sc (improvement across trials)
- **Forgetting:** T5Sc - DRSc (loss from final learning to delayed recall)
- **Proactive Interference:** T1Sc - TDSc (how much prior learning interferes)
- **Retroactive Interference:** FRSc - T5Sc (how much new learning interferes)

### Interpretation:
- **High RAVLT_Total:** Strong verbal learning capacity
- **High DRSc:** Good long-term retention
- **Low Learning:** Encoding deficit
- **High Forgetting:** Storage/consolidation deficit

### Normative Data:
**Location:** `cog/RAVLT/`

**Adjustment:** T-scores (M=50, SD=10) based on age and education.

---

## BVMT-R (BRIEF VISUOSPATIAL MEMORY TEST - REVISED)

### Purpose:
Assess visuospatial memory (encoding, storage, retrieval of visual information).

### Administration:

**Stimulus:** 6 geometric figures in 2×3 grid, shown for 10 seconds

**Trial 1-3:** Immediate recall drawing
- Participant draws figures in correct locations
- Repeat stimulus and recall 3 times total

**Delayed Recall:** Draw figures after 25-minute delay

**Recognition Trial:** Shown 12 figures (6 targets + 6 distractors)
- Participant identifies which 6 were in original display

### Scoring:

**Recall Scoring (per figure):**
- **2 points:** Correct figure in correct location
- **1 point:** Correct figure in wrong location OR recognizable figure in correct location
- **0 points:** Incorrect figure or missing

**Total possible per trial:** 12 points (6 figures × 2 points)

**Primary Scores (Tags in master.xlsx):**
- `A010-COG-X-BVM-T1Sc`, `A010-COG-X-BVM-T2Sc`, `A010-COG-X-BVM-T3Sc` = Trial scores (0-12)
- `A010-COG-X-BVM-TDSc` = Delayed recall score (0-12)

**Timing Data:**
- `A010-COG-X-BVM-T1Ti`, `A010-COG-X-BVM-T2Ti`, `A010-COG-X-BVM-T3Ti` = Trial durations
- `A010-COG-X-BVM-TDTD` = Delay period (seconds)
- `A010-COG-X-BVM-TDTi` = Delayed recall duration

**Computed Scores (stored in master.xlsx):**
- `A010-COG-X-BVM-TotR` = Total Recall (T1Sc + T2Sc + T3Sc, 0-36)
- `A010-COG-X-BVM-Lear` = Learning (T3Sc - T1Sc)
- `A010-COG-X-BVM-PerR` = Percent Retained ((TDSc / T3Sc) × 100)
- `A010-COG-X-BVM-ReHi` = Recognition Hits (0-6)
- `A010-COG-X-BVM-ReFA` = Recognition False Alarms (0-6)
- `A010-COG-X-BVM-ReDI` = Recognition Discrimination (Hits - FA)
- `A010-COG-X-BVM-ReRB` = Recognition Response Bias ((FA - (6 - Hits)) / 6)

### Interpretation:
- **High TotR:** Strong visuospatial learning
- **High PerR:** Good consolidation
- **Low Lear:** Visuospatial encoding deficit
- **High ReDI:** Good recognition memory

### Normative Data:
**Location:** `cog/BVMT/`

**Adjustment:** T-scores based on age and education.

---

## NART (NATIONAL ADULT READING TEST)

### Purpose:
Estimate premorbid IQ (crystallized intelligence).

**Rationale:** Reading ability is relatively resistant to cognitive decline, so provides estimate of peak cognitive function.

### Administration:

**Stimulus:** 50 irregular English words (e.g., "ache", "bouquet", "topiary")

**Task:** Participant reads each word aloud

**Scoring:** Number of correctly pronounced words (0-50)

### Scoring:

**Primary Score (Tag in master.xlsx):**
- `A010-COG-X-NAR-Scor` = Number correct (0-50)

**Note:** Tag is "Scor" not "Score" - exact spelling critical!

**Timing:**
- `A010-COG-X-NAR-Time` = Test duration (seconds)

**Estimated IQ (computed during analysis):**
- Various formulas exist to convert NART score to estimated FSIQ (Full Scale IQ)
- Typical: FSIQ = 130 - (0.7 × errors)

### Interpretation:
- **High NAR-Scor:** High premorbid IQ, crystallized knowledge
- **Low NAR-Scor:** Lower educational attainment or language difficulties

### Limitations in REMEMVR:
- **Many participants non-native English speakers** → NART may underestimate IQ
- **No record of primary language** → Cannot correct for language effects
- **Use with caution in Chapter 7 analyses**

### Normative Data:
**Location:** `cog/NART/`

---

## RPM (RAVEN'S PROGRESSIVE MATRICES)

### Purpose:
Assess fluid intelligence (abstract reasoning, pattern recognition).

**Advantage:** Non-verbal, less culturally biased than NART.

### Administration:

**Stimulus:** 12 visual pattern puzzles (from Advanced Progressive Matrices Set I)

**Task:** Identify missing piece from 8 options

**Time:** Untimed (self-paced)

### Scoring:

**Primary Score (Tag in master.xlsx):**
- `A010-COG-X-RPM-Scor` = Number correct (0-12)

**Note:** Tag is "Scor" not "Score" - exact spelling critical!

**Timing:**
- `A010-COG-X-RPM-Time` = Test duration (seconds)

**Item-Level Data (Tags in master.xlsx):**
- `A010-COG-X-RPM-Tr01` through `A010-COG-X-RPM-Tr12` = Chosen option (0-8) for each puzzle
  - 0 = Correct answer (usually)
  - 1-8 = Specific incorrect options

**Note:** "Tr01" through "Tr12" for trials 1-12 (zero-padded)

### Interpretation:
- **High RPM-Scor:** Strong abstract reasoning, pattern recognition
- **Predicts:** Problem-solving, relational binding in memory

### Normative Data:
**Location:** `cog/RPM/`

**Adjustment:** Percentile ranks based on age.

---

## HYPOTHESIZED RELATIONSHIPS TO REMEMVR

### RAVLT → REMEMVR:
**Hypothesis:** Predicts Free Recall performance (both generative retrieval).

**Domain specificity:** May predict "What" domain better than "Where"/"When".

**Research Questions:** 7.1, 7.2, 7.5, 7.9

### BVMT → REMEMVR:
**Hypothesis:** Predicts spatial memory (Where domain).

**Paradigm specificity:** May predict Recognition better (visual matching).

**Research Questions:** 7.1, 7.2, 7.6

### NART → REMEMVR:
**Hypothesis:** General predictor (cognitive reserve).

**Caveat:** Language confound limits interpretation.

**Research Questions:** 7.1, 7.4, 7.8

### RPM → REMEMVR:
**Hypothesis:** Predicts complex integration (What+Where+When binding).

**Rationale:** Fluid intelligence supports relational reasoning.

**Research Questions:** 7.1, 7.7

---

## DATA EXTRACTION (NEW METHOD)

### Data-Prep Agent Workflow:

**For Chapter 7 RQs requiring cognitive test scores:**

1. Read RQ info.md to identify which tests are needed
2. Call data.py to extract tags from master.xlsx:

```python
# Example: Extract NART and RPM scores for all participants
tags_needed = {
    'NART_Score': '{UID}-COG-X-NAR-Scor',
    'RPM_Score': '{UID}-COG-X-RPM-Scor',
    'RAVLT_T1': '{UID}-COG-X-RAV-T1Sc',
    'RAVLT_T2': '{UID}-COG-X-RAV-T2Sc',
    'RAVLT_T3': '{UID}-COG-X-RAV-T3Sc',
    'RAVLT_T4': '{UID}-COG-X-RAV-T4Sc',
    'RAVLT_T5': '{UID}-COG-X-RAV-T5Sc',
    'BVMT_T1': '{UID}-COG-X-BVM-T1Sc',
    'BVMT_T2': '{UID}-COG-X-BVM-T2Sc',
    'BVMT_T3': '{UID}-COG-X-BVM-T3Sc',
}

data = extract_tags_for_all_participants(tags_needed)
```

3. Compute derived scores (e.g., RAVLT_Total = sum of T1-T5)
4. Standardize to T-scores if needed
5. Validate extracted data
6. Save to input.csv

### Standardization:

**For analyses:** Convert raw scores to T-scores (M=50, SD=10) using sample norms or published norms.

**Rationale:** Different scales across tests (RAVLT 0-75, BVMT 0-36, etc.) → need common metric for regression.

**When to standardize:**
- Always for regression analyses with multiple cognitive tests
- Not needed if only using one test
- Not needed if only using as grouping variable (e.g., high/low RAVLT)

---

## ANALYSIS CONSIDERATIONS

### Missing Data:
Some participants may have incomplete cognitive test data.

**Handling:**
- Use pairwise deletion (analyze available data)
- Report N for each analysis
- Check if missingness is systematic (e.g., older adults more likely to skip)

### Multicollinearity:
Cognitive tests may be correlated.

**Check:** Compute VIF (Variance Inflation Factor)

**Action if VIF > 5:** Consider using factor analysis or PCA to reduce dimensionality.

### Standardization Method:
**Sample norms:** Use mean/SD from REMEMVR sample (N=100)
- Pro: Matches sample distribution
- Con: Not generalizable beyond sample

**Published norms:** Use age/education-adjusted T-scores from test manuals
- Pro: Generalizable, accounts for demographics
- Con: May not match sample characteristics

**Recommendation:** Use sample norms for within-study comparisons, published norms for external validity claims.

---

## SCORING CODE

### Location:
`cog/cogtests.py`

### Functions:

**scoreRAVLT(participant_data):**
- Extracts Trial 1-5 scores from tags
- Computes Total, Learning, Forgetting
- Returns dictionary

**scoreBVMT(participant_data):**
- Extracts Trial 1-3, Delayed scores from tags
- Computes Total Recall, Learning, Percent Retained
- Returns dictionary

**scoreNART(participant_data):**
- Extracts NAR-Scor from tags
- Optionally converts to estimated IQ
- Returns score

**scoreRPM(participant_data):**
- Extracts RPM-Scor from tags
- Returns score

### Validation Status:
Code was written by research assistant (Jayce). User is not 100% confident in correctness.

**Action for refactor:** Validate scoring procedures against published manuals before using in Chapter 7 analyses.

---

## REFERENCES

- Rey, A. (1964). *L'examen clinique en psychologie*. Presses Universitaires de France.
- Benedict, R. H. B. (1997). *Brief Visuospatial Memory Test - Revised*. Psychological Assessment Resources.
- Nelson, H. E., & Willison, J. (1991). *National Adult Reading Test (NART)*. NFER-Nelson.
- Raven, J., Raven, J. C., & Court, J. H. (1998). *Raven's Progressive Matrices*. Oxford Psychologists Press.

---

**End of Cognitive Tests Reference**
