# IRT Methodology Reference

**Purpose:** Technical explanation of Item Response Theory implementation in REMEMVR.

**Audience:** Analysis-executor agent, results-inspector agent, statistics-expert agent.

**Last Updated:** 2025-01-04

---

## OVERVIEW

REMEMVR uses **Multidimensional Graded Response Model (GRM)** implemented via **deepirtools IWAVE** (Importance-Weighted Amortized Variational Encoder).

**Why IRT over Classical Test Theory (CTT)?**
- CTT assumes all items equally difficult → masks differences
- IRT estimates latent ability (θ) accounting for item difficulty and discrimination
- IRT provides measurement precision per participant (standard errors)
- IRT allows adaptive testing and item analysis

---

## MODEL SPECIFICATION

### Graded Response Model (GRM)

**For dichotomous items (TQ accuracy: 0 or 1):**

P(X = 1 | θ, a, b) = 1 / (1 + exp(-a(θ - b)))

Where:
- X = Observed response (0 or 1)
- θ = Latent ability (higher = better memory)
- a = Discrimination parameter (how well item differentiates ability levels)
- b = Difficulty parameter (ability level at 50% probability of correct response)

**For polytomous items (TC confidence: 0, 0.25, 0.5, 0.75, 1.0):**

P(X ≥ k | θ, a, b_k) = 1 / (1 + exp(-a(θ - b_k)))

Where:
- b_k = Threshold parameter for category k
- Response has 5 categories, so 4 threshold parameters

---

## MULTIDIMENSIONAL IRT

### Confirmatory Factor Structure (Q-matrix)

Instead of estimating which items load on which factors (exploratory), we **specify** the factor structure based on theoretical domains.

**Example Q-matrix for "All by Domain" (3 factors):**

| Item | Factor 1 (What) | Factor 2 (Where) | Factor 3 (When) |
|------|-----------------|------------------|-----------------|
| TQ_IFR-N-i1 | 1 | 0 | 0 |
| TQ_IFR-U-i1 | 0 | 1 | 0 |
| TQ_IFR-O-i1 | 0 | 0 | 1 |

**Interpretation:** Items load on pre-specified factors based on memory domain.

### Correlated vs Uncorrelated Factors

**Uncorrelated (orthogonal):**
- Assumes memory domains are independent
- More constrained model
- Better for confirmatory analysis

**Correlated (oblique):**
- Allows factors to covary (e.g., people good at What also good at Where)
- More realistic but can have identification issues
- Estimates factor correlation matrix

**In REMEMVR:** We test both to see if conclusions change.

---

## DEEPIRTOOLS IWAVE

### Why Variational Autoencoder (VAE)?

Traditional IRT uses maximum likelihood estimation (slow for large datasets).

**IWAVE:**
- Uses neural networks to approximate posterior distributions
- Much faster for high-dimensional data
- Scales to hundreds of items and thousands of participants

### Key Parameters:

#### batch_size
**Definition:** Number of observations processed simultaneously during training.

**Values in REMEMVR:**
- low: 32
- med: 2048 (default)
- high: 4096

**Trade-off:** Larger batches = more stable gradients but more memory.

#### iw_samples
**Definition:** Importance-weighted samples for ELBO estimation.

**Values in REMEMVR:**
- low: 10
- med: 100 (default)
- high: 200

**Trade-off:** More samples = better approximation but slower.

#### mc_samples
**Definition:** Monte Carlo samples for posterior approximation.

**Values in REMEMVR:**
- Fitting: 1 (sufficient for training)
- Scoring: 100 (need more precision for theta estimates)

**Trade-off:** More samples = better theta estimates but slower scoring.

---

## COMPOSITE_ID STACKING

### Problem:
IRT needs large sample sizes (ideally 500+ responses per item).
- 100 participants × 50 items = 5,000 responses (good)
- But 4 separate time-point models = 1,250 responses each (marginal)

### Solution:
Stack all 4 tests into ONE IRT model as if 400 different people took the same test once.

**Composite ID format:** `{UID}_T{test_number}`
- Example: `A042_T3` = Participant A042's Test 3

**Assumption:** Item parameters (difficulty, discrimination) don't change over time.

**Justification:** VR stimuli are identical across time points. Reasonable assumption.

**Trade-off:** Cannot model time-varying item parameters, but gain 4× sample size.

---

## ITERATIVE ITEM FILTERING

### Discrimination Thresholds

Items with extreme discrimination are problematic:
- **Too low (a < 0.5):** Item doesn't differentiate ability levels well
- **Too high (a > 4.0):** Item may be overfitting or have other issues

### Procedure:

**Step 1:** Fit IRT model at iteration level (low/med/high)

**Step 2:** Extract discrimination parameters for all items

**Step 3:** Remove items with discrimination < 0.5 or > 4.0 on ANY loaded factor

**Step 4:** Refit model on remaining items

**Step 5:** Repeat until convergence or max iterations reached

**Rationale:** Improves measurement quality by removing poorly performing items.

---

## THETA SCORES (ABILITY ESTIMATES)

### Interpretation:
- **θ = 0:** Average ability (by construction)
- **θ > 0:** Above-average ability
- **θ < 0:** Below-average ability
- **Standard deviation:** Typically around 1.0

**Direction in REMEMVR:** Higher θ = better episodic memory performance.

### Standard Errors:
IRT provides SE(θ) for each participant, indicating measurement precision.

**Smaller SE:** More confident in ability estimate
**Larger SE:** Less confident (e.g., participant answered few items or all items very easy/hard)

### Reliability:
Marginal reliability = 1 - (mean(SE²) / var(θ))

**Interpretation:** Proportion of variance in θ that is "true score" (not measurement error).

### Downstream Usage: Theta Scores for LMM Analysis

**CRITICAL:** In REMEMVR, theta scores from IRT are the OUTCOME VARIABLE for LMM trajectory analysis.

**Pipeline Flow:**
1. **IRT Phase:** Calibrate with composite_ID stacking (100 participants × 4 tests = 400 "pseudo-participants")
2. **Output:** Theta scores for each composite_ID (A010_T1, A010_T2, A010_T3, A010_T4)
3. **Reshaping Phase:** Parse composite_ID, merge with TSVR (actual delay period), reshape to long format
4. **LMM Phase:** Model theta ~ TSVR with domain/paradigm/congruence factors

**Time Variable for LMM:**
- ❌ **WRONG:** Use T1/T2/T3/T4 as categorical factor OR nominal days (0, 1, 3, 6)
- ✅ **CORRECT:** Use TSVR (Time Since VR) = actual hours since encoding, converted to days

**Why TSVR is mandatory:**
- Each composite_ID (A010_T1, A010_T2, etc.) represents a SPECIFIC test session with SPECIFIC delay period
- TSVR provides precise delay for each composite_ID (e.g., A010_T2 = 27.2 hours, not "Day 1" = 24 hours)
- Using nominal days introduces measurement error (ignores participant-level variance in test timing)

**Data Source:**
- Extract TSVR from master.xlsx: `{UID}-RVR-{Test}-STA-X-TSVR`
- Merge with theta scores on [UID, Test] after parsing composite_ID

**See Decision D070 in project_specific_stats_insights.md for complete IRT→LMM pipeline documentation.**

---

## ITEM PARAMETERS

### Difficulty (b):
**Definition:** Ability level at which participant has 50% probability of correct response.

**Interpretation:**
- **b = 0:** Item of average difficulty
- **b > 0:** Difficult item (need high ability to answer correctly)
- **b < 0:** Easy item (even low ability participants get correct)

**Example:** Item with b = 1.5 is difficult; only participants with θ > 1.5 have >50% chance of success.

### Discrimination (a):
**Definition:** How steeply probability of correct response increases with ability.

**Interpretation:**
- **a = 0:** Item doesn't discriminate at all (useless)
- **a = 1:** Moderate discrimination
- **a = 2+:** High discrimination (excellent item)

**Visual:** Steep item characteristic curve (ICC).

---

## IRT vs CTT COMPARISON

### CTT Approach:
**Score:** Sum or mean of item responses
**Assumption:** All items equally weighted

**Problems:**
- Ignores item difficulty
- No measurement precision per person
- Cannot compare across different item sets

### IRT Approach:
**Score:** Latent ability (θ) weighted by item parameters
**Advantage:** Accounts for item properties

**Benefits:**
- More accurate ability estimates
- Standard errors per person
- Can compare across forms (if items on same scale)

**In REMEMVR:** We run both CTT and IRT analyses to check if conclusions differ.

---

## MODEL DIAGNOSTICS

### Item Fit:
Check if item responses match model predictions.

**Methods:**
- Residual analysis (observed vs expected frequencies)
- Chi-square item fit statistics

**Action if poor fit:** Remove item or investigate why.

### Person Fit:
Check if individual response patterns are plausible.

**Methods:**
- Person-fit statistics (e.g., lz, infit, outfit)
- Flag aberrant response patterns

**Action if poor fit:** Investigate data quality for that participant.

### Dimensionality:
Check if factor structure is correct.

**Methods:**
- Factor loadings (should match Q-matrix)
- Residual correlations (should be near zero)

**Action if poor fit:** Revise factor structure.

---

## ASSUMPTIONS

### 1. Local Independence
**Definition:** Responses to items are independent conditional on θ.

**Implication:** No residual correlations between items after accounting for ability.

**Violation:** If items are correlated beyond their shared factor (e.g., "What" knowledge helps "Where" recall).

**In REMEMVR:** Potential issue for memory domains. Conditional dependencies exist (knowing object identity helps recall location).

**Future:** Use Bayesian hierarchical models to model dependencies explicitly.

### 2. Monotonicity
**Definition:** Higher ability → higher probability of correct response.

**Implication:** No "trick questions" where higher ability hurts performance.

**In REMEMVR:** Reasonable assumption for episodic memory.

### 3. Unidimensionality (per factor)
**Definition:** Each factor represents a single latent trait.

**Implication:** Items loading on "What" should all measure the same construct.

**In REMEMVR:** Reasonable within domains, but domains may not be perfectly unidimensional.

---

## OUTPUT FILES

### data_ability.csv
**Columns:**
- Composite_ID: Participant-test identifier (e.g., A042_T3)
- Theta_{factor}: Ability estimate per factor
- SE_Theta_{factor}: Standard error per factor
- Test: Test number (1-4)
- Days: Days since VR encoding

**Use:** Input for LMM trajectory modeling.

### data_difficulty.csv
**Columns:**
- Item: Item name (e.g., TQ_IFR-N-i1)
- Difficulty: b parameter
- Discrimination_{factor}: a parameter per loaded factor
- Factor: Which factor item loads on

**Use:** Item analysis, understanding which items are hard/easy.

### data.csv
**Long-format response matrix:**
- Composite_ID
- Item name
- Response (0, 1, or 0.25/0.5/0.75/1.0 for confidence)

**Use:** Input to IRT model.

---

## IMPLEMENTATION DETAILS (irt.py)

### DeepIrt Class:
Wraps deepirtools IWAVE model.

**Key methods:**
- `fit()`: Train model on response data
- `score()`: Generate theta scores for participants
- `extract_item_params()`: Get difficulty and discrimination

### Analysis Class:
Orchestrates full IRT pipeline for one analysis set.

**Steps:**
1. Filter participants by age/exclusions
2. Select items based on groups/tags
3. Remove invariant items (≥95% responses in one category)
4. For each iteration level:
   - Fit IRT model
   - Extract theta scores + item parameters
   - Remove poorly discriminating items
   - Refit model
   - Run LMM on theta scores
   - Generate plots

---

## REFERENCES

- Samejima, F. (1969). Estimation of latent ability using a response pattern of graded scores. *Psychometrika Monograph Supplement*.
- Urban, C. J., & Bauer, D. J. (2021). A deep learning algorithm for high-dimensional exploratory item factor analysis. *Psychometrika, 86*(1), 1-29.
- deepirtools documentation: [Link to be added]

---

**End of IRT Methodology Reference**
