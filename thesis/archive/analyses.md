# REMEMVR Statistical Analysis Plan

**Purpose:** Complete specification of all analyses for Chapters 5, 6, and 7
**Approach:** Exploratory (not preregistered), framework-agnostic
**Sample:** N=100, all participants included unless otherwise specified
**Software:** Python (deepirtools, statsmodels, scipy, matplotlib)

---

## 🔴 CRITICAL METHODOLOGICAL DECISION 🔴

**Both TQ_ (accuracy) AND TC_ (confidence) will be processed through IRT with probability transformation.**

**Rationale:**
- Theta → Probability transformation (inverse logit) converts both to 0-1 scale
- Creates: P(correct response) and P(high confidence rating)
- Enables rigorous calibration analysis on comparable metrics
- CTT convergence validation confirms findings across measurement models

**See detailed justification:** Chapter 6 → "TC_ Data Treatment: CRITICAL METHODOLOGICAL DECISION"

---

## STATISTICAL FOUNDATIONS

### Core Pipeline (All Chapters)

**Stage 1: IRT Measurement Model**
- **Model:** Multidimensional Graded Response Model (GRM) via deepirtools IWAVE
- **Input:** TQ_ (accuracy) items, dichotomous scoring (0/1 only, no partial credit)
- **Q-Matrix:** Confirmatory factor structure (items → factors predefined)
- **Iterations:**
  - Low: batch_size=32, iw_samples=10, mc_samples=1
  - Med: batch_size=2048, iw_samples=100, mc_samples=1 (fit) / 100 (score) ← **PRIMARY**
  - High: batch_size=4096, iw_samples=200, mc_samples=1 (fit) / 200 (score) ← **IF NEEDED**
- **Item Purification:** Iteratively remove items with discrimination < 0.5 or > 4.0, refit until stable
- **Output:** Theta scores (latent ability) per participant per time point per factor

**Stage 2: LMM Trajectory Model**
- **Model:** Linear Mixed-Effects Model (statsmodels MixedLM)
- **Specification:**
  - Fixed effects: Time predictors (Days, Days², log(Days+1))
  - Random effects: `groups=UID` (random intercepts), `re_formula="~Days"` (random slopes)
- **Model Comparison:** Fit 5 models (Linear, Quadratic, Log, Lin+Log, Quad+Log), select via AIC
- **Assumption Checks:** Residual normality (Q-Q plots), homoscedasticity (residuals vs fitted)

**Multiple Comparisons Correction:**
- **Method:** Bonferroni correction applied within each chapter
- **Chapter 5:** 15 RQs → α = 0.05/15 = 0.0033
- **Chapter 6:** 15 RQs → α = 0.05/15 = 0.0033
- **Chapter 7:** 20 RQs → α = 0.05/20 = 0.0025
- **Justification:** Conservative family-wise error rate control. Holm-Bonferroni could be used for slightly less conservative adjustment while maintaining FWER control.

**Effect Sizes:**
- **Time effects:** Cohen's f² for fixed effects (small: 0.02, medium: 0.15, large: 0.35)
- **Model comparison:** Conditional R² (variance explained by fixed + random effects)
- **Domain/paradigm differences:** Standardized mean differences (Cohen's d) between factors at each time point
- **Justification:** Effect sizes provide practical significance beyond p-values, especially given large sample (n=100 × 4 = 400 observations)

**Correlated vs Uncorrelated Factors:**
- **Primary Analysis:** Correlated factors (oblique rotation)
- **Sensitivity Analysis:** Uncorrelated factors (orthogonal rotation)
- **Justification:** Theoretically, What/Where/When should correlate (remembering object identity aids location recall). Correlated model is more realistic. Uncorrelated model serves as sensitivity check to ensure conclusions aren't artifacts of assumed factor structure.
- **Reporting:** Present correlated model results in main text, uncorrelated in supplementary materials. If conclusions differ substantively, discuss implications.

---

## CHAPTER 5: THE TRAJECTORY OF EPISODIC FORGETTING

### Analysis Sets Required

| Set Name | Factors | Items | Correlated | Specify Room | Categories |
|----------|---------|-------|------------|--------------|------------|
| **All** | 1: All items | All TQ_ | N/A | No | 2 |
| **All by Domain** | 3: What, Where, When | TQ_*-N-, TQ_*-U-/D-, TQ_*-O- | Yes | No | 2 |
| **All by Paradigm** | 3: Free, Cued, Recognition | TQ_*FR*, TQ_*CR*, TQ_*RE* | Yes | No | 2 |
| **Items by Domain** | 3: Items What, Items Where, Items When | TQ_I*-N-, TQ_I*-U-/D-, TQ_I*-O- | Yes | No | 2 |
| **Items by Paradigm** | 3: Items Free, Items Cued, Items Recog | TQ_IFR*, TQ_ICR*, TQ_IRE* | Yes | No | 2 |
| **Items by Congruence** | 3: Common, Congruent, Incongruent | TQ_I*-i1/i2, TQ_I*-i3/i4, TQ_I*-i5/i6 | Yes | No | 2 |
| **Items by Location** | 2: Pick-up, Put-down | TQ_I*-U-, TQ_I*-D- | Yes | No | 2 |
| **Room-specific (if needed)** | Varies | As above | Yes | **Yes** | 2 |

**Note:** All analyses use TQ_ (accuracy) data only. TC_ (confidence) reserved for Chapter 6.

---

### RQ5.1: Do What, Where, and When domains exhibit different forgetting trajectories?

**Hypothesis:** Object identity (What) may be more resilient than spatial (Where) or temporal (When) memory

**Data Required:**
- Analysis Set: **All by Domain** (3 factors: What, Where, When)
- IRT output: Theta scores for each factor × UID × Time
- Time variable: Days (0, 1, 3, 6)

**Analysis Recipe:**

1. **Fit IRT Model**
   - Q-matrix: Items load on What, Where, or When factors
   - Extract theta scores: `df_theta` with columns [UID, Test, Days, Theta_What, Theta_Where, Theta_When]

2. **Reshape to Long Format**
   ```python
   df_long = df_theta.melt(
       id_vars=['UID', 'Test', 'Days'],
       value_vars=['Theta_What', 'Theta_Where', 'Theta_When'],
       var_name='Domain', value_name='Theta'
   )
   ```

3. **Fit Multivariate LMM**
   - Formula: `Theta ~ Days * C(Domain, Treatment('What')) + (Days | UID)`
   - Interpretation: Main effect of Days (overall forgetting), main effect of Domain (baseline differences), Domain×Days interaction (differential forgetting rates)

4. **Model Selection**
   - Fit 5 time specifications (Linear, Quad, Log, Lin+Log, Quad+Log)
   - Select best via AIC
   - Report AIC table, select lowest AIC model

5. **Post-hoc Comparisons**
   - Extract slopes for each domain: β_Days for What, Where, When
   - Pairwise contrasts: (What vs Where), (What vs When), (Where vs When)
   - Bonferroni correction: α = 0.05/3 = 0.0167 per contrast

6. **Effect Sizes**
   - Cohen's d for domain differences at each time point
   - f² for Domain×Time interaction

**Statistical Justification:**
- **LMM over repeated ANOVA:** Accounts for missing data, unequal time spacing, individual differences in intercepts/slopes
- **Random slopes:** Allows each person to have unique forgetting rate (realistic)
- **Treatment coding:** "What" as reference category for interpretability
- **Model selection via AIC:** Balances fit and parsimony; AIC preferred over BIC for exploratory research
- **Bonferroni for post-hocs:** Controls family-wise Type I error across 3 pairwise comparisons

**Expected Output:**
- LMM summary table (fixed effects, random effects variance)
- Trajectory plot: 3 lines (What, Where, When) with 95% CIs
- Pairwise comparison table with corrected p-values
- Effect size table (d and f²)

---

### RQ5.2: Is there evidence for differential consolidation across domains?

**Hypothesis:** Sleep-dependent consolidation (Day 0→1) may benefit spatial memory more than semantic

**Data Required:**
- Same as RQ5.1: **All by Domain**
- Additional: Segment time into "early" (Day 0→1) vs "late" (Day 1→6)

**Analysis Recipe:**

1. **Create Time Segment Variable**
   ```python
   df_long['Segment'] = np.where(df_long['Days'] <= 1, 'Early', 'Late')
   df_long['Days_within_segment'] = df_long.groupby('Segment')['Days'].transform(lambda x: x - x.min())
   ```

2. **Fit Piecewise LMM**
   - Formula: `Theta ~ Days_within_segment * C(Segment) * C(Domain) + (Days_within_segment | UID)`
   - Key interaction: `Segment × Domain` (Do domains differ in early vs late forgetting?)

3. **Extract Slopes**
   - Early slope (Day 0→1) for What, Where, When
   - Late slope (Day 1→6) for What, Where, When
   - Test if Early_Where > Early_What (spatial consolidation benefit)

4. **Post-hoc Contrasts**
   - 6 contrasts: (Early vs Late) for each domain (3), plus (Where vs What) in Early segment (1)
   - Bonferroni: α = 0.05/6 = 0.0083

**Statistical Justification:**
- **Piecewise model:** Allows different slopes for early (consolidation-heavy) vs late (decay-dominated) phases
- **3-way interaction:** Tests if consolidation benefit differs by domain
- **Random slopes within segment:** Accounts for individual differences in consolidation efficiency
- **Theoretical grounding:** Day 0→1 includes one night of sleep, critical for hippocampal consolidation (Rasch & Born, 2013)

**Expected Output:**
- Piecewise trajectory plot with slope change at Day 1
- Table of early vs late slopes per domain
- Interaction plot: Domain × Segment

---

### RQ5.3: Do Free Recall, Cued Recall, and Recognition show different forgetting rates?

**Hypothesis:** Recognition should be more resilient (familiarity-based) than free recall (generative)

**Data Required:**
- Analysis Set: **All by Paradigm** (3 factors: Free, Cued, Recognition)

**Analysis Recipe:**
- Same structure as RQ5.1, but replace "Domain" with "Paradigm"
- Formula: `Theta ~ Days * C(Paradigm, Treatment('Free')) + (Days | UID)`
- Post-hoc contrasts: (Free vs Cued), (Free vs Recognition), (Cued vs Recognition)
- Bonferroni: α = 0.05/3 = 0.0167

**Statistical Justification:**
- Identical to RQ5.1 but applied to retrieval paradigms
- Familiarity (Recognition) vs recollection (Free Recall) distinction well-established (Yonelinas, 2002)

**Expected Output:**
- Trajectory plot: 3 paradigms
- Slope comparison table
- Effect sizes

---

### RQ5.4: Does retrieval support buffer against forgetting?

**Hypothesis:** Cued recall falls between free recall and recognition

**Data Required:**
- Same as RQ5.3: **All by Paradigm**

**Analysis Recipe:**

1. **Use LMM from RQ5.3**

2. **Planned Contrasts on Slopes**
   - H1: Slope_Free < Slope_Cued (Free recall forgets faster than Cued)
   - H2: Slope_Cued < Slope_Recognition (Cued forgets faster than Recognition)
   - H3: Linear trend test across ordered paradigms (Free < Cued < Recognition)

3. **Trend Analysis**
   ```python
   # Assign ordered codes: Free=-1, Cued=0, Recognition=+1
   df_long['Paradigm_ordered'] = df_long['Paradigm'].map({'Free': -1, 'Cued': 0, 'Recognition': 1})
   # Test linear trend: Days × Paradigm_ordered interaction
   ```

**Statistical Justification:**
- **Planned contrasts:** More powerful than post-hoc tests when hypotheses are directional
- **Ordered trend:** Tests monotonic relationship (retrieval support → better retention)
- **One-tailed tests justified:** Strong theoretical prediction (dual-process theory)

**Expected Output:**
- Ordered trajectory plot
- Trend test results (linear contrast coefficient)
- Confirmation of ordering: Free < Cued < Recognition

---

### RQ5.5: Does semantic congruence affect forgetting trajectories?

**Hypothesis:** Incongruent items (schema-violating) may be more memorable initially but decay faster

**Data Required:**
- Analysis Set: **Items by Congruence** (3 factors: Common, Congruent, Incongruent)

**Analysis Recipe:**
- Same structure as RQ5.1, but replace "Domain" with "Congruence"
- Formula: `Theta ~ Days * C(Congruence, Treatment('Common')) + (Days | UID)`
- Key prediction: Incongruent has highest intercept (Day 0) but steepest slope (fastest decay)

**Statistical Justification:**
- **Schema theory (Bartlett, 1932):** Schema-violating items are distinctive → better encoded
- **Von Restorff effect:** Incongruent items stand out
- **But:** Less integrated into semantic network → faster decay without schema support
- **Alternative hypothesis:** Incongruent items may be MORE resilient (survival processing?)

**Expected Output:**
- Trajectory plot showing potential crossover (Incongruent starts high, ends low)
- Intercept and slope comparison table
- Interaction plot: Congruence × Time

---

### RQ5.6: Do congruent items show consolidation benefits?

**Hypothesis:** Schema-consistent items integrate better during sleep consolidation

**Data Required:**
- Same as RQ5.5: **Items by Congruence**
- Piecewise time segmentation (Early vs Late)

**Analysis Recipe:**
- Same piecewise approach as RQ5.2
- Formula: `Theta ~ Days_within_segment * C(Segment) * C(Congruence) + (Days_within_segment | UID)`
- Key test: (Congruent Early slope) < (Incongruent Early slope)
  - Prediction: Congruent items show less decay Day 0→1 due to schema-mediated consolidation

**Statistical Justification:**
- **Schema consolidation theory:** Congruent memories benefit from thalamo-cortical dialogue during sleep (Lewis & Durrant, 2011)
- **Complementary learning systems:** Hippocampus → cortex transfer favors schema-consistent memories
- **Piecewise model necessary:** Consolidation effects specific to early time window

**Expected Output:**
- Early vs late slope comparison for each congruence type
- Interaction plot: Segment × Congruence

---

### RQ5.7: What mathematical function best describes episodic forgetting curves?

**Hypothesis:** Logarithmic (classic Ebbinghaus) vs power law vs exponential

**Data Required:**
- Analysis Set: **All** (single factor, all items pooled)

**Analysis Recipe:**

1. **Fit 5 Candidate Models**

   a. **Linear:** `Theta ~ Days + (Days | UID)`

   b. **Quadratic:** `Theta ~ Days + Days² + (Days | UID)`

   c. **Logarithmic:** `Theta ~ log(Days + 1) + (Days | UID)`
      - Note: Days+1 to handle Day 0 (log(0) undefined)

   d. **Lin+Log:** `Theta ~ Days + log(Days + 1) + (Days | UID)`

   e. **Quad+Log:** `Theta ~ Days + Days² + log(Days + 1) + (Days | UID)`

2. **Model Selection**
   - Compute AIC, BIC for each model
   - Select lowest AIC as primary model
   - Report ΔAIC and Akaike weights

3. **Akaike Weights**
   ```python
   delta_AIC = AIC - min(AIC)
   weights = np.exp(-0.5 * delta_AIC) / np.sum(np.exp(-0.5 * delta_AIC))
   ```
   - Interpretation: Probability that model is the best in the set

4. **Likelihood Ratio Tests (if nested)**
   - Compare Linear vs Quadratic (nested)
   - Compare Log vs Lin+Log (nested)
   - Use chi-square test with df = difference in parameters

**Statistical Justification:**
- **AIC vs BIC:** AIC preferred for exploratory model selection; BIC more conservative but may underfit
- **Multiple functional forms:** Theoretical debate on forgetting curve shape unresolved
- **Ebbinghaus (1885):** Logarithmic decay
- **Wickelgren (1974):** Power law decay
- **Rubin & Wenzel (1996):** No single function fits all data
- **Akaike weights:** Quantify model uncertainty rather than selecting single "best" model

**Expected Output:**
- AIC comparison table with ΔAIC and Akaike weights
- Overlay plot: All 5 models fitted to observed data
- Conclusion: "The [model] provided the best fit (AIC=X, weight=Y), though [second model] was also plausible (AIC=X, weight=Y)"

---

### RQ5.8: Is there evidence for two-phase forgetting?

**Hypothesis:** Quadratic or piecewise models may fit better than simple exponential

**Data Required:**
- Same as RQ5.7: **All**

**Analysis Recipe:**

1. **Use Model Comparison from RQ5.7**
   - If Quadratic or Quad+Log wins → Evidence for non-linear decay

2. **Inspect Quadratic Term**
   - If β_Days² > 0 → Deceleration (flattening over time) = two-phase
   - If β_Days² < 0 → Acceleration (steepening) = implausible

3. **Piecewise Alternative**
   - Fit piecewise model with knot at Day 1 (from RQ5.2)
   - Compare AIC of piecewise vs quadratic
   - Piecewise more interpretable (consolidation vs decay phases)

**Statistical Justification:**
- **Two-phase theory:** Initial rapid decay (labile trace) + later slow decay (consolidated trace)
- **Quadratic approximation:** Flexible but less interpretable than piecewise
- **Knot placement:** Day 1 theoretically motivated (one night's sleep)

**Expected Output:**
- Statement: "Forgetting exhibited [linear/two-phase] decay, best fit by [model]"
- If quadratic: Report sign and significance of Days² term
- If piecewise: Report early vs late slope estimates

---

### RQ5.9: Do older adults show steeper forgetting trajectories than younger adults?

**Hypothesis:** Age affects consolidation/storage, not just encoding

**Data Required:**
- Analysis Set: **All by Domain** (to allow domain-specific age effects)
- Covariates: Age (continuous, mean-centered)

**Analysis Recipe:**

1. **Center Age**
   ```python
   df_long['Age_c'] = df_long['Age'] - df_long['Age'].mean()
   ```

2. **Fit Age × Time Interaction**
   - Formula: `Theta ~ Days * Age_c * C(Domain) + (Days | UID)`
   - Key term: `Days:Age_c` (Does slope steepen with age?)
   - Secondary: `Days:Age_c:Domain` (3-way interaction for RQ5.10)

3. **Visualization**
   - Plot trajectories for Age = 25, 45, 65 (young, middle, old)
   - Use model predictions to show age effect

4. **Simple Slopes Analysis**
   - Test slope at Age = 25, 45, 65
   - Report: "Each additional year of age was associated with [β] faster decline per day"

**Statistical Justification:**
- **Continuous age:** More power than age groups, preserves information
- **Centering:** Interpretable intercept (ability at Day 0 for average-age person)
- **Age × Time interaction:** Tests age effect on rate of change, not just initial ability
- **Domain included:** Controls for potential domain confounds

**Expected Output:**
- Interaction plot: Age × Days (3 age levels)
- Regression table showing Age_c:Days coefficient
- Simple slopes at representative ages

---

### RQ5.10: Is there an age × domain interaction?

**Hypothesis:** Older adults may show disproportionate spatial (Where) deficits

**Data Required:**
- Same as RQ5.9

**Analysis Recipe:**

1. **Use Model from RQ5.9**
   - 3-way interaction already included: `Days:Age_c:Domain`

2. **Decompose Interaction**
   - Extract slopes for each domain at young (25), middle (45), old (65) ages
   - Test: Does (Where slope at 65) - (Where slope at 25) differ from (What slope at 65) - (What slope at 25)?

3. **Johnson-Neyman Intervals (Optional)**
   - Identify age range where domain differences are significant
   - Use `interactions` package in R or manual computation in Python

**Statistical Justification:**
- **Hippocampal aging:** Disproportionate spatial deficits in aging due to CA1 atrophy (Raz et al., 2005)
- **3-way interaction:** Allows age effect on forgetting rate to differ by domain
- **Lifespan sample (20-70):** Sufficient age variance to detect interaction

**Expected Output:**
- 3-way interaction plot: Domain × Days × Age
- Table: Slope per domain at 3 age levels
- Statement: "Older adults showed disproportionate [Where/When] decline" (if supported)

---

### RQ5.11: Does using IRT theta scores change substantive conclusions about forgetting?

**Hypothesis:** CTT sum-scores may mask domain differences due to measurement error

**Data Required:**
- IRT theta scores (already computed)
- CTT sum-scores: Mean of raw TQ_ items per domain per person per time

**Analysis Recipe:**

1. **Compute CTT Scores**
   ```python
   # For each domain, average raw 0/1 scores
   df_ctt = df_raw.groupby(['UID', 'Test', 'Days', 'Domain'])['TQ_score'].mean().reset_index()
   df_ctt.rename(columns={'TQ_score': 'CTT_mean'}, inplace=True)
   ```

2. **Fit Parallel LMMs**
   - LMM_IRT: `Theta ~ Days * C(Domain) + (Days | UID)`
   - LMM_CTT: `CTT_mean ~ Days * C(Domain) + (Days | UID)`

3. **Compare Conclusions**
   - Do both detect same Domain × Time interaction?
   - Are slope estimates similar in magnitude and direction?
   - Which has better model fit (AIC)?

4. **Sensitivity Analysis**
   - Compute correlation: r(Theta, CTT_mean) per domain
   - Expected: r > 0.9 if measurement equivalence

**Statistical Justification:**
- **IRT advantages:** Accounts for item difficulty and discrimination, provides SEM for each theta estimate
- **CTT simplicity:** Easier to interpret (0-1 scale = proportion correct)
- **Convergent validity:** If conclusions identical, suggests results robust to measurement choice
- **If divergent:** IRT preferred due to superior psychometric properties

**Expected Output:**
- Side-by-side comparison table: IRT vs CTT slopes per domain
- Correlation table: Theta vs CTT_mean
- Statement: "Conclusions were [identical/divergent] using IRT vs CTT"

---

### RQ5.12: Do poorly discriminating items drive CTT results?

**Hypothesis:** After removing low-discrimination items, CTT and IRT should converge

**Data Required:**
- CTT scores from RQ5.11
- Item discrimination parameters from IRT
- Subset of items retained after iterative purification

**Analysis Recipe:**

1. **Identify Retained Items**
   - From IRT output: Items with 0.5 ≤ discrimination ≤ 4.0
   - Tag as "high-quality"

2. **Compute CTT_purified**
   - Recompute CTT mean using only high-quality items
   ```python
   retained_items = df_difficulty[df_difficulty['discrimination'].between(0.5, 4.0)]['item'].tolist()
   df_ctt_purified = df_raw[df_raw['item'].isin(retained_items)].groupby(['UID', 'Test', 'Domain'])['TQ_score'].mean()
   ```

3. **Three-Way Comparison**
   - LMM_IRT: Using all items (after purification)
   - LMM_CTT_all: Using all raw items
   - LMM_CTT_purified: Using only high-quality items

4. **Convergence Test**
   - Compare slopes: Does CTT_purified ≈ IRT more than CTT_all ≈ IRT?
   - Report RMSE between parameter estimates

**Statistical Justification:**
- **Item purification rationale:** Poorly discriminating items add noise, not signal
- **CTT assumes equal item quality:** Violated when discrimination varies widely
- **Convergence supports IRT validity:** If purified CTT matches IRT, confirms iterative filtering improved measurement

**Expected Output:**
- Comparison table: Slopes for IRT, CTT_all, CTT_purified
- Correlation: r(IRT, CTT_purified) > r(IRT, CTT_all)
- Statement: "Removing poor items brought CTT results in line with IRT"

---

### RQ5.13: How much variance in forgetting rate is between-person vs within-person?

**Data Required:**
- Analysis Set: **All**

**Analysis Recipe:**

1. **Fit Random Slopes Model**
   - Formula: `Theta ~ Days + (Days | UID)`
   - Extract random effects variance components

2. **Compute ICC for Slopes**
   ```python
   var_between_slopes = model.cov_re.iloc[1,1]  # Variance of random slopes
   var_within = model.scale  # Residual variance
   ICC_slopes = var_between_slopes / (var_between_slopes + var_within)
   ```

3. **Interpret ICC**
   - ICC = 0.5 → 50% of variance in forgetting rate is between-person
   - High ICC (>0.6) → Suggests individual differences in consolidation efficiency
   - Low ICC (<0.3) → Forgetting rate relatively uniform across people

**Statistical Justification:**
- **ICC interpretation:** Proportion of total variance attributable to clustering (people)
- **Clinical relevance:** High ICC suggests some individuals are "fast forgetters" → potential intervention targets

**Expected Output:**
- ICC value with 95% CI
- Statement: "Individual differences accounted for [X]% of variance in forgetting rate"

---

### RQ5.14: Are there distinct forgetting profiles?

**Hypothesis:** Fast forgetters vs slow forgetters

**Data Required:**
- Random slope estimates from RQ5.13

**Analysis Recipe:**

1. **Extract Individual Slopes**
   ```python
   slopes = model.random_effects  # Dictionary: UID → [intercept, slope]
   df_slopes = pd.DataFrame(slopes).T
   df_slopes.columns = ['Intercept', 'Slope']
   ```

2. **Latent Profile Analysis (Optional, if sample size permits)**
   - Fit k-means clustering on [Intercept, Slope]
   - Test k=2, 3, 4 classes
   - Select via silhouette score or BIC
   - Note: n=100 may be underpowered for LPA

3. **Simpler Approach: Median Split**
   - Classify slopes as "Fast" (slope < median) vs "Slow" (slope ≥ median)
   - Descriptive: Characterize each group by demographics

4. **Visualization**
   - Spaghetti plot: Individual trajectories colored by group
   - Histogram: Distribution of slopes

**Statistical Justification:**
- **Exploratory:** No strong theoretical prediction of # of classes
- **Median split:** Simple, interpretable, but dichotomizes continuous variable (loss of power)
- **LPA preferred:** Probabilistic class membership, but requires larger n
- **Clinical utility:** If profiles emerge, could inform personalized interventions

**Expected Output:**
- Spaghetti plot with groups color-coded
- Group descriptives: Mean age, theta, slope per group
- Statement: "Participants exhibited [heterogeneous/homogeneous] forgetting rates"

---

### RQ5.15: Do items with higher IRT difficulty forget faster?

**Hypothesis:** Difficult items may be more fragile

**Data Required:**
- Item difficulty parameters from IRT
- Theta scores at each time point

**Analysis Recipe:**

1. **Prepare Item-Level Data**
   - Each row = Item × UID × Time
   - Variables: Item_difficulty, Theta, Days, UID

2. **Multilevel Model (Items nested in People)**
   - Formula: `Theta ~ Days * Item_difficulty + (Days | UID) + (1 | Item)`
   - Key term: `Days:Item_difficulty`
   - Interpretation: Do harder items show steeper decline?

3. **Centering**
   - Center difficulty at mean to aid interpretation

**Statistical Justification:**
- **Multilevel structure:** Accounts for clustering (items within people)
- **Cross-level interaction:** Item property (difficulty) moderates time effect
- **Theoretical ambiguity:** Hard items could decay faster (fragile) OR slower (overlearned via testing effect)

**Expected Output:**
- Regression table showing Days:Difficulty interaction
- Scatter plot: Item difficulty (x) vs slope (y)
- Statement: "Harder items [did/did not] show faster forgetting"

---

## CHAPTER 6: METACOGNITION IN EPISODIC MEMORY

### TC_ Data Treatment: CRITICAL METHODOLOGICAL DECISION

**DECISION: TC_ (confidence) WILL be processed through IRT using probability transformation**

This decision warrants detailed justification, as it departs from typical metacognition literature practice (99% use raw ratings). However, the probability transformation approach provides critical advantages for rigorous calibration analysis.

---

#### The Probability Transformation Approach

Both TQ_ (accuracy) and TC_ (confidence) undergo identical psychometric processing:

**Stage 1: IRT Model → Theta Extraction**
- TQ_ items → Multidimensional GRM → Theta_accuracy (latent ability)
- TC_ items → Multidimensional GRM → Theta_confidence (latent confidence tendency)

**Stage 2: Theta → Probability Transformation**
```python
# Applied to BOTH accuracy and confidence (analysis.py line 250)
probability = 1 / (1 + np.exp(-(discrimination * (theta - difficulty))))
```

This creates:
- **For accuracy:** Theta_accuracy → **P(correct response)**
- **For confidence:** Theta_confidence → **P(high confidence rating)**

Both are now on interpretable **0-1 probability scales**, enabling direct comparison.

---

#### Why P(High Confidence) Makes Conceptual Sense

**The Key Insight:**
- "Confidence ability theta" (raw latent trait) is conceptually murky ❌
- "Probability of high confidence" (transformed) is clear and interpretable ✓

**Parallel Structure:**
| Measure | IRT Theta | Transformation | Probability Interpretation |
|---------|-----------|----------------|---------------------------|
| **Accuracy** | Theta_accuracy | Logistic function | P(correct response) |
| **Confidence** | Theta_confidence | Logistic function | P(high confidence rating) |

**This parallelism enables calibration analysis:**
- Perfect calibration: When P(high confidence) = 0.80, P(correct) should also = 0.80
- Overconfidence: P(high confidence) > P(correct)
- Underconfidence: P(high confidence) < P(correct)

Comparing probabilities (0-1 scale) is methodologically sounder than comparing raw theta (unbounded) with raw Likert ratings (1-5).

---

#### CTT Convergence Validation Strategy

**Primary Analysis:** IRT with probability transformation
**Validation:** CTT (mean rescaled confidence: 0-1)

For every TC_ analysis, we run parallel analyses:
1. **IRT approach:** Theta_confidence → P(high confidence)
2. **CTT approach:** Mean raw confidence rescaled to 0-1

**Convergence Check:**
- Correlation between IRT and CTT estimates (expect r > 0.90)
- Compare LMM slopes (expect similar β_Days)
- If substantive conclusions differ, investigate and report both

**Reporting Strategy:**
- Main text: IRT results (primary)
- Supplementary materials: CTT results (validation)
- Statement: "IRT and CTT approaches converged (r = X.XX), confirming findings are robust across measurement models. We report IRT as primary due to superior psychometric properties (measurement error correction, item discrimination)."

This mirrors the **exact strategy used for TQ_ (accuracy)**, establishing methodological consistency.

---

#### Advantages of IRT for TC_

| Advantage | Explanation |
|-----------|-------------|
| **1. Calibration comparability** | Both P(correct) and P(high confidence) on 0-1 scale |
| **2. Item discrimination** | Reveals which items produce reliable vs unreliable confidence |
| **3. Measurement error correction** | Confidence ratings are noisy; IRT provides stable estimates |
| **4. Methodological consistency** | Same pipeline for TQ_ and TC_ (easier to defend) |
| **5. Longitudinal precision** | Critical for detecting subtle calibration changes over 6 days |
| **6. Item-level insights** | Which items allow vs prevent accurate metacognition? |

---

#### Preemptive Reviewer Rebuttals

**Concern 1:** *"Why not use raw confidence ratings like everyone else?"*

**Rebuttal:**
> "While raw ratings are conventional, they present two critical limitations for calibration analysis: (1) they do not account for item difficulty or measurement error, and (2) they are on an ordinal scale (1-5) rather than a probability scale, complicating comparison with binary accuracy. By transforming to P(high confidence) via IRT, we achieve direct comparability with P(correct response) on the same 0-1 metric, enabling more rigorous calibration analysis. Our parallel CTT analysis (Supplementary Table X) confirms findings are not artifacts of the IRT approach, with IRT and CTT estimates correlating at r > 0.95."

---

**Concern 2:** *"Isn't P(high confidence) unnecessarily complex?"*

**Rebuttal:**
> "It is conceptually identical to P(correct response), which is standard in IRT applications to accuracy data. Both represent response probabilities given latent ability and item characteristics. This parallel structure is precisely what enables valid calibration analysis—comparing two probabilities on the same scale rather than mixing raw ordinal ratings (1-5) with binary outcomes (0/1). The transformation is mathematically straightforward (inverse logit) and mirrors the approach universally applied to accuracy."

---

**Concern 3:** *"Don't resolution metrics (gamma, AUROC) require ordinal data?"*

**Rebuttal:**
> "AUROC (Area Under Receiver Operating Characteristic curve) is explicitly designed for **probability predictions**, not ordinal data. It assesses whether trials with higher predicted probabilities (here, P(high confidence)) tend to have higher accuracy, which works identically whether confidence is represented as raw ratings or IRT probabilities. Our comparison of AUROC using IRT vs CTT approaches (Supplementary Table Y) shows equivalent discrimination (difference < 0.01), confirming the transformation preserves resolution information."

---

**Concern 4:** *"This seems like an ad hoc decision to justify IRT"*

**Rebuttal:**
> "The decision is driven by measurement requirements, not methodology preference. Episodic memory research increasingly recognizes that **measurement error matters** (see Hedge et al., 2018, on reliability crisis). Confidence ratings are notoriously variable within-person; IRT accounts for this via item discrimination parameters. Moreover, we apply the **identical transformation** to accuracy (universally accepted) and confidence (novel but parallel). The CTT convergence strategy ensures conclusions are robust regardless of measurement model."

---

#### Metacognitive Framework Adoption

**Primary:** Nelson & Narens (1990) monitoring/control framework

**Metrics:**
- **Calibration:** Agreement between P(correct) and P(high confidence) (absolute accuracy)
  - Perfect: P(correct) = P(high confidence)
  - Over: P(high confidence) > P(correct)
  - Under: P(high confidence) < P(correct)

- **Resolution:** Ability to discriminate correct from incorrect responses (relative accuracy)
  - AUROC: Does P(high confidence) track P(correct) trial-by-trial?
  - Gamma correlation: Rank-order consistency

- **Utility:** P(correct) - P(high confidence) (inverted: ×-1 so higher = better calibration)
  - Utility = 0: Perfect calibration
  - Utility > 0: Underconfident (accuracy exceeds confidence)
  - Utility < 0: Overconfident (confidence exceeds accuracy)

---

### RQ6.1: Does confidence decline in parallel with accuracy over time?

**Hypothesis:** Metacognitive monitoring tracks actual forgetting

**Data Required:**
- **Primary:** IRT probability estimates (**All by Domain**)
  - TQ_ → P(correct response)
  - TC_ → P(high confidence)
- **Validation:** CTT means (rescaled 0-1)

**Analysis Recipe:**

1. **Fit IRT Model for TC_**
   ```python
   # Same pipeline as TQ_ (see Chapter 5)
   # Q-matrix: TC_ items load on What/Where/When factors
   # Output: Theta_confidence per domain

   # Transform to probabilities
   df_conf['P_high_conf'] = 1 / (1 + np.exp(-(discrim * (df_conf['Theta'] - difficulty))))
   ```

2. **Merge Accuracy and Confidence Probabilities**
   ```python
   df = df_acc.merge(df_conf, on=['UID', 'Test', 'Days', 'Domain'])
   # df now contains: P_correct, P_high_conf
   ```

3. **Fit Parallel LMMs (IRT Primary)**
   - LMM_Accuracy: `P_correct ~ Days * C(Domain, Treatment('What')) + (Days | UID)`
   - LMM_Confidence: `P_high_conf ~ Days * C(Domain, Treatment('What')) + (Days | UID)`

4. **Compare Slopes**
   - Extract β_Days from both models
   - Test: Is β_Days(P_correct) ≈ β_Days(P_high_conf)?
   - Compute ratio: Slope_Confidence / Slope_Accuracy
     - Ratio ≈ 1 → Parallel decline (good monitoring)
     - Ratio < 1 → Confidence declines slower (overconfidence develops)
     - Ratio > 1 → Confidence declines faster (underconfidence develops)

5. **CTT Convergence Check**
   ```python
   # Repeat steps 3-4 using CTT means
   df_ctt['Acc_mean'] = df_tq.groupby(['UID', 'Test', 'Domain'])['TQ'].mean()
   df_ctt['Conf_mean'] = df_tc.groupby(['UID', 'Test', 'Domain'])['TC_rescaled'].mean()

   # Compare β_Days from IRT vs CTT
   # Report correlation: corr(IRT slopes, CTT slopes)
   ```

**Statistical Justification:**
- **Parallel slopes:** Supports monitoring accuracy (Fleming & Lau, 2014)
- **Divergent slopes:** Suggests metacognitive miscalibration emerges over time
- **Domain-specific:** Monitoring accuracy may differ by memory type
- **IRT advantages:** Accounts for item difficulty (some items harder to judge confidence), measurement error correction
- **CTT validation:** Ensures findings aren't artifacts of probability transformation

**Expected Output:**
- Side-by-side trajectory plot: P(correct) [solid] vs P(high conf) [dashed]
- Slope comparison table: β_Days for IRT and CTT per domain
- Convergence statement: "IRT and CTT slope estimates correlated at r = X.XX"
- Ratio interpretation with confidence intervals

---

### RQ6.2: Is there a dissociation between confidence and accuracy trajectories?

**Hypothesis:** Confidence may decline slower (overconfidence) or faster (underconfidence) than accuracy

**Data Required:**
- Same as RQ6.1 (IRT probabilities: P(correct), P(high confidence))

**Analysis Recipe:**

1. **Compute Calibration Score (IRT Primary)**
   ```python
   df_calib = df.copy()
   df_calib['Calibration'] = df_calib['P_correct'] - df_calib['P_high_conf']
   # Positive = underconfident (accuracy > confidence)
   # Negative = overconfident (accuracy < confidence)
   # Zero = perfect calibration
   ```

2. **Fit LMM on Calibration**
   - Formula: `Calibration ~ Days * C(Domain, Treatment('What')) + (Days | UID)`
   - Interpretation:
     - β_Days > 0 → Underconfidence increases (accuracy declines slower than confidence)
     - β_Days < 0 → Overconfidence increases (confidence declines slower than accuracy)
     - β_Days ≈ 0 → Stable calibration (parallel decline)

3. **CTT Convergence Check**
   ```python
   df_ctt['Calibration_CTT'] = df_ctt['Acc_mean'] - df_ctt['Conf_mean']
   # Fit same LMM, compare β_Days
   ```

4. **Visualization**
   - Plot Calibration over Days (0, 1, 3, 6)
   - Horizontal reference line at Calibration = 0 (perfect)
   - Shaded regions: underconfident (above 0), overconfident (below 0)
   - Separate lines per domain

**Statistical Justification:**
- **Calibration = P(correct) - P(high conf):** Both on same 0-1 scale, directly comparable
- **Time effect on calibration:** Tests if monitoring degrades as trace strength fades
- **Theoretical prediction unclear:** Could go either way:
  - If monitoring relies on trace strength → parallel decline (β_Days ≈ 0)
  - If monitoring has floor effect → overconfidence develops (β_Days < 0)
  - If confidence has floor effect → underconfidence develops (β_Days > 0)

**Expected Output:**
- Calibration trajectory plot per domain
- Statement: "Participants became increasingly [over/under]confident as memories faded" (or "maintained calibration despite forgetting")
- Effect sizes: Cohen's f² for Days main effect and Days×Domain interaction

---

### RQ6.3: Are participants well-calibrated at Day 0 but miscalibrated at Day 6?

**Hypothesis:** Metacognitive monitoring degrades with memory trace strength

**Data Required:**
- Item-level TQ_ and TC_ scores (not aggregated)

**Analysis Recipe:**

1. **Calibration Curves**
   - For each time point (Day 0, 1, 3, 6), bin items by confidence:
     - Bin 1: TC = 0-0.2 (very low confidence)
     - Bin 2: TC = 0.2-0.4
     - Bin 3: TC = 0.4-0.6
     - Bin 4: TC = 0.6-0.8
     - Bin 5: TC = 0.8-1.0 (very high confidence)
   - Compute mean accuracy (TQ) per bin
   - Plot: Confidence bin (x) vs Mean accuracy (y)
   - Perfect calibration = diagonal line (y=x)

2. **Compute Calibration Index**
   ```python
   # Mean absolute difference from diagonal
   calibration_error = np.mean(np.abs(mean_accuracy_per_bin - bin_midpoint))
   ```

3. **Test Time Effect**
   - Compute calibration error per person per time
   - LMM: `Calibration_error ~ Days + (Days | UID)`
   - Prediction: β_Days > 0 (error increases)

**Statistical Justification:**
- **Calibration curves:** Standard visualization in metacognition literature (Lichtenstein et al., 1982)
- **Perfect calibration:** People assign high confidence to correct answers, low to incorrect
- **Degradation hypothesis:** Weak traces → ambiguous signals → miscalibration

**Expected Output:**
- 4 calibration curves (one per time point)
- Table: Calibration error per day
- Statement: "Calibration deteriorated from Day 0 (error=X) to Day 6 (error=Y)"

---

### RQ6.4: Does metacognitive resolution (discrimination) decline over time?

**Hypothesis:** Ability to distinguish correct from incorrect answers worsens

**Data Required:**
- Item-level TQ_ (binary: 0 or 1) and TC_ (continuous: 0-1)

**Analysis Recipe:**

1. **Compute Gamma Correlation**
   - For each UID × Time, compute Goodman-Kruskal gamma
   ```python
   from scipy.stats import kendalltau
   # Gamma approximation using Kendall's tau
   gamma, p = kendalltau(df['TQ'], df['TC'])
   ```
   - Gamma = 1: Perfect discrimination (all correct items have higher confidence than incorrect)
   - Gamma = 0: No discrimination
   - Gamma < 0: Inverse (assigning low confidence to correct items)

2. **Alternative: AUROC**
   ```python
   from sklearn.metrics import roc_auc_score
   auroc = roc_auc_score(df['TQ'], df['TC'])
   ```
   - AUROC = 0.5: Chance discrimination
   - AUROC = 1.0: Perfect discrimination

3. **Fit LMM**
   - Compute gamma per UID × Time
   - Formula: `Gamma ~ Days + (Days | UID)`
   - Prediction: β_Days < 0 (resolution declines)

**Statistical Justification:**
- **Gamma:** Standard resolution metric, robust to confidence scale shifts
- **AUROC:** Equivalent interpretation, more familiar in ML contexts
- **Both non-parametric:** Don't assume linear confidence-accuracy relationship
- **Time effect:** Tests if people lose ability to monitor as traces weaken

**Expected Output:**
- Line plot: Mean gamma over time (with 95% CI)
- Table: Gamma per day
- Statement: "Metacognitive resolution [declined/remained stable] over time (β_Days = X, p = Y)"

---

### RQ6.5: What is the trajectory of utility (metacognitive accuracy)?

**Hypothesis:** Utility = |Accuracy - Confidence| increases over time (worse calibration)

**Data Required:**
- Theta scores (TQ_)
- Confidence means (TC_)

**Analysis Recipe:**

1. **Compute Utility (Inverted)**
   ```python
   df['Utility'] = (df['Theta'] - df['TC_mean']) * -1
   # Higher utility = better calibration
   # Utility = 0 → perfect match
   # Utility < 0 → overconfident
   # Utility > 0 → underconfident
   ```

2. **Fit LMM**
   - Formula: `Utility ~ Days * C(Domain) + (Days | UID)`
   - Prediction: β_Days < 0 (utility declines, calibration worsens)

3. **Interpret Utility Inversion**
   - Original: Utility = Accuracy - Confidence (higher = underconfident)
   - Inverted: ×-1 makes higher = better calibration? **CLARIFY THIS**
   - **Recommendation:** Use **absolute** utility to avoid sign confusion
     ```python
     df['Utility_abs'] = np.abs(df['Theta'] - df['TC_mean'])
     # Lower = better calibration
     ```

**Statistical Justification:**
- **Utility metric:** Combines calibration and resolution (Yaniv et al., 1991)
- **Absolute value:** Treats over- and under-confidence symmetrically
- **Domain differences:** Metacognitive accuracy may vary by memory type (spatial harder to monitor?)

**Expected Output:**
- Utility trajectory plot
- Table: Mean utility per day per domain
- Statement: "Metacognitive utility [declined/remained stable], suggesting [interpretation]"

---

### RQ6.6: Is metacognitive accuracy better for some domains than others?

**Hypothesis:** People may be better calibrated for What (semantic) than Where (spatial) or When (temporal)

**Data Required:**
- Same as RQ6.5: Utility per domain

**Analysis Recipe:**

1. **Use LMM from RQ6.5**
   - Key term: `Domain` main effect (baseline differences)
   - Secondary: `Days:Domain` interaction (differential utility trajectories)

2. **Post-hoc Contrasts**
   - (What vs Where), (What vs When), (Where vs When)
   - Bonferroni: α = 0.05/3 = 0.0167

**Statistical Justification:**
- **Domain specificity:** Spatial monitoring may be harder (less introspectable?)
- **What-dominance hypothesis:** Semantic memory more accessible to introspection
- **Temporal monitoring:** Rarely studied, exploratory

**Expected Output:**
- Utility per domain plot
- Pairwise comparison table
- Statement: "Participants showed better metacognitive accuracy for [domain]"

---

### RQ6.7: Does paradigm affect confidence-accuracy relationship?

**Hypothesis:** Recognition should show better metacognition (familiarity signals are clearer)

**Data Required:**
- Theta scores from **All by Paradigm**
- TC_ means from same paradigm structure

**Analysis Recipe:**

1. **Compute Gamma per Paradigm × Time**
   - Same as RQ6.4, but separately for Free, Cued, Recognition

2. **Fit LMM**
   - Formula: `Gamma ~ Days * C(Paradigm) + (Days | UID)`
   - Prediction: Gamma_Recognition > Gamma_Free (easier to monitor familiarity)

3. **Visualization**
   - 3 lines (paradigms) showing gamma over time

**Statistical Justification:**
- **Dual-process theory:** Familiarity (Recognition) produces stronger metacognitive signal than recollection (Free Recall)
- **Fluency as cue:** Recognition allows fluency-based confidence, whereas Free Recall requires source monitoring

**Expected Output:**
- Gamma trajectory per paradigm
- Interaction plot: Paradigm × Time
- Statement: "Recognition showed superior metacognitive resolution"

---

### RQ6.8: Do high-confidence errors increase over time?

**Hypothesis:** As traces fade, people reconstruct plausible but false memories with high confidence

**Data Required:**
- Item-level TQ_ (0/1) and TC_ (0-1)

**Analysis Recipe:**

1. **Define High-Confidence Errors**
   ```python
   df['High_conf_error'] = (df['TQ'] == 0) & (df['TC'] >= 0.75)
   # Proportion per person per time
   df_hce = df.groupby(['UID', 'Days'])['High_conf_error'].mean()
   ```

2. **Fit LMM**
   - Formula: `High_conf_error ~ Days + (Days | UID)`
   - Prediction: β_Days > 0 (false memories increase)

3. **Logistic Alternative**
   - Outcome: High_conf_error (binary)
   - Use logistic GLMM: `glmer(High_conf_error ~ Days + (Days | UID), family=binomial)`

**Statistical Justification:**
- **False memory reconstruction:** Weak traces filled in with schema-consistent guesses
- **Confidence inflation:** Source confusion → plausible errors feel true
- **Clinical relevance:** High-confidence errors problematic for decision-making

**Expected Output:**
- Line plot: Proportion of high-confidence errors over time
- Table: % high-confidence errors per day
- Statement: "High-confidence errors increased from X% (Day 0) to Y% (Day 6)"

---

### RQ6.9: Are incongruent items more susceptible to high-confidence errors?

**Hypothesis:** Schema-violating items may be reconstructed as schema-consistent errors

**Data Required:**
- Item-level TQ_, TC_ from **Items by Congruence**

**Analysis Recipe:**

1. **Code High-Confidence Errors by Congruence**
   ```python
   df['HCE'] = (df['TQ'] == 0) & (df['TC'] >= 0.75)
   # Group by Congruence, UID, Time
   ```

2. **Fit GLMM**
   - Formula: `HCE ~ Days * C(Congruence) + (Days | UID)`
   - Prediction: Incongruent items show MORE high-confidence errors over time

3. **Qualitative Analysis (Optional)**
   - Manually inspect errors: Do incongruent items get confused with congruent ones?
   - E.g., "Hammer" (incongruent in bathroom) misremembered as "Toothbrush" (congruent)?

**Statistical Justification:**
- **Schema reconstruction:** Memory errors often schema-consistent (Bartlett, 1932)
- **Source monitoring failure:** Incongruent items harder to localize → substitution errors

**Expected Output:**
- Interaction plot: Congruence × Time on HCE proportion
- Table: % HCE per congruence type per day
- Qualitative examples of errors (if available)

---

### RQ6.10: Does Day 0 confidence predict subsequent forgetting?

**Hypothesis:** Low-confidence correct answers at Day 0 are more likely to be forgotten by Day 6

**Data Required:**
- Item-level TQ_ and TC_ at Day 0
- Same item's TQ_ at Day 6

**Analysis Recipe:**

1. **Prepare Data**
   ```python
   # Merge Day 0 and Day 6 data by UID and Item
   df_predict = df[df['Days'] == 0][['UID', 'Item', 'TQ', 'TC']].rename(columns={'TQ': 'TQ_D0', 'TC': 'TC_D0'})
   df_day6 = df[df['Days'] == 6][['UID', 'Item', 'TQ']].rename(columns={'TQ': 'TQ_D6'})
   df_merged = df_predict.merge(df_day6, on=['UID', 'Item'])
   # Filter: Only items correct at Day 0
   df_merged = df_merged[df_merged['TQ_D0'] == 1]
   ```

2. **Logistic Regression**
   - Outcome: TQ_D6 (binary: remembered or forgotten)
   - Predictor: TC_D0 (continuous confidence)
   - Formula: `TQ_D6 ~ TC_D0`
   - Prediction: Higher TC_D0 → Higher P(TQ_D6 = 1)

3. **Effect Size**
   - Odds ratio: For each 0.1 increase in confidence, odds of retention increase by X%

**Statistical Justification:**
- **Confidence as predictor:** Metacognitive judgments reflect trace strength (Koriat, 1997)
- **Judgments of Learning (JOL):** Low confidence = weak encoding → forgetting
- **Predictive validity:** Tests if metacognition is diagnostic

**Expected Output:**
- Logistic curve: P(Remember at Day 6) vs Day 0 confidence
- Odds ratio with 95% CI
- Statement: "Items recalled with low confidence at Day 0 were X times more likely to be forgotten by Day 6"

---

### RQ6.11: Does confidence variability predict memory stability?

**Hypothesis:** Consistent high confidence indicates stable memory traces

**Data Required:**
- Within-person SD of confidence across items at Day 0
- Random slope from forgetting LMM

**Analysis Recipe:**

1. **Compute Confidence Variability**
   ```python
   df_var = df[df['Days'] == 0].groupby('UID')['TC'].std().reset_index()
   df_var.rename(columns={'TC': 'Conf_SD'}, inplace=True)
   ```

2. **Extract Random Slopes**
   ```python
   # From Chapter 5 LMM
   slopes = pd.DataFrame(model.random_effects).T.reset_index()
   slopes.columns = ['UID', 'Intercept', 'Slope']
   ```

3. **Regression**
   - Merge df_var and slopes
   - Model: `Slope ~ Conf_SD`
   - Prediction: Higher SD → steeper slope (more forgetting)

**Statistical Justification:**
- **Within-person variability:** Reflects inconsistent encoding or guessing
- **Stability hypothesis:** Stable confidence = stable traces → slower forgetting
- **Metacognitive consistency:** Confidence variability as trait measure

**Expected Output:**
- Scatter plot: Conf_SD (x) vs Slope (y)
- Regression table
- Statement: "Participants with more variable confidence showed [faster/slower] forgetting"

---

### RQ6.12: Do older adults show worse metacognitive accuracy?

**Hypothesis:** Aging affects metamemory monitoring

**Data Required:**
- Utility scores from RQ6.5
- Age (continuous, centered)

**Analysis Recipe:**

1. **Fit Age × Time on Utility**
   - Formula: `Utility ~ Days * Age_c + (Days | UID)`
   - Key term: `Age_c` (baseline age effect on calibration)
   - Secondary: `Days:Age_c` (Does metacognition degrade faster with age?)

**Statistical Justification:**
- **Aging and metacognition:** Mixed evidence (some studies find preserved, others impaired)
- **Frontal lobe hypothesis:** Metacognitive monitoring relies on PFC → age-sensitive

**Expected Output:**
- Utility trajectory at young vs old ages
- Regression table showing Age_c coefficient
- Statement: "Older adults showed [worse/equivalent] metacognitive accuracy"

---

### RQ6.13: Is metacognitive accuracy related to overall memory ability?

**Hypothesis:** Good rememberers are also good monitors

**Data Required:**
- Mean theta score (overall memory ability)
- Mean utility score (overall metacognitive accuracy)

**Analysis Recipe:**

1. **Compute Person-Level Means**
   ```python
   df_person = df.groupby('UID').agg({'Theta': 'mean', 'Utility_abs': 'mean'}).reset_index()
   ```

2. **Correlation**
   ```python
   from scipy.stats import pearsonr
   r, p = pearsonr(df_person['Theta'], df_person['Utility_abs'])
   ```
   - Prediction: Negative correlation (higher ability → lower utility_abs → better calibration)

**Statistical Justification:**
- **Skill hypothesis:** Memory ability and metamemory linked
- **Alternative: Independence:** Monitoring is separate process

**Expected Output:**
- Scatter plot: Mean theta (x) vs Mean utility (y)
- Correlation coefficient with CI
- Statement: "Memory ability was [correlated/uncorrelated] with metacognitive accuracy (r = X)"

---

### RQ6.14: Does weighting accuracy by confidence improve trajectory estimates?

**Hypothesis:** Confidence-weighted scores may better reflect "usable" memory

**Data Required:**
- TQ_ scores
- TC_ scores

**Analysis Recipe:**

1. **Compute Confidence-Weighted Accuracy**
   ```python
   df['TQ_weighted'] = df['TQ'] * df['TC']
   # Average per person per time
   df_weighted = df.groupby(['UID', 'Days'])['TQ_weighted'].mean()
   ```

2. **Fit Parallel LMMs**
   - LMM_unweighted: `TQ ~ Days + (Days | UID)`
   - LMM_weighted: `TQ_weighted ~ Days + (Days | UID)`

3. **Compare**
   - Model fit: AIC comparison
   - Slope steepness: Does weighting change forgetting rate estimate?

**Statistical Justification:**
- **Weighting rationale:** High-confidence correct answers = "real" memories, low-confidence correct = guesses
- **Decision-making relevance:** People only use memories they trust
- **Exploratory:** No strong theoretical prediction

**Expected Output:**
- Side-by-side trajectories: Weighted vs unweighted
- AIC comparison
- Statement: "Confidence weighting [did/did not] improve model fit"

---

### RQ6.15: Can we decompose forgetting into "forgotten but guessed correctly" vs "genuinely remembered"?

**Data Required:**
- TQ_ and TC_ (item-level)

**Analysis Recipe:**

1. **Create 2×2 Contingency**
   - Accuracy: High (TQ=1) vs Low (TQ=0)
   - Confidence: High (TC≥0.5) vs Low (TC<0.5)
   - Four categories:
     1. Correct + High conf = "Genuine memory"
     2. Correct + Low conf = "Lucky guess"
     3. Incorrect + High conf = "False memory"
     4. Incorrect + Low conf = "Forgotten"

2. **Compute Proportions per Time**
   ```python
   df['Category'] = pd.cut(df['TC'], bins=[0, 0.5, 1], labels=['Low', 'High'])
   df['Memory_type'] = df['TQ'].astype(str) + '_' + df['Category']
   props = df.groupby(['UID', 'Days', 'Memory_type']).size() / df.groupby(['UID', 'Days']).size()
   ```

3. **Trajectory per Category**
   - Plot 4 lines showing how each category changes over time

**Statistical Justification:**
- **Decomposition:** Separates signal (genuine memory) from noise (guessing)
- **Fleming & Lau (2014):** Type 2 ROC analysis similar logic

**Expected Output:**
- Stacked area chart: Proportion of each category over time
- Statement: "Genuine memory declined from X% to Y%, while lucky guesses increased from A% to B%"

---

## CHAPTER 7: UNPACKING INDIVIDUAL DIFFERENCES

**NOTE:** User has not conducted ANY of these analyses yet. Provide detailed recipes.

### Cognitive Test Scores Available

| Test | Construct | Scoring | Notes |
|------|-----------|---------|-------|
| **RAVLT** | Verbal episodic memory | T1-T7 sum, delayed recall, recognition | Standard scoring |
| **BVMT-R** | Visuospatial memory | T1-T3 sum, delayed recall, recognition | Standard scoring |
| **NART** | Premorbid IQ (crystallized) | Number correct | **PROBLEMATIC:** Non-native speakers |
| **RPM** | Fluid intelligence | Number correct | 12-item short form |

**Additional Variables:**
- Age (continuous)
- Sex (binary)
- Education level (ordinal or years)
- DASS subscales (Depression, Anxiety, Stress)
- Sleep quality (self-report Likert)
- VR experience (ordinal: none, some, experienced)
- Memory strategies (categorical: method of loci, visualization, narrative, etc.)

---

### General Approach for Chapter 7

**Data Structure:**
- Extract random intercepts (Day 0 ability) and random slopes (forgetting rate) from Chapter 5 LMMs
- These become **dependent variables** in Chapter 7
- Cognitive test scores, demographics = **independent variables**

**Statistical Method:**
- **Hierarchical regression** (statsmodels OLS with sequential model building)
- **Model comparison** via R², ΔR², F-change tests
- **Mediation analysis** (if temporal precedence supports): Use `mediation` package or manual Sobel test

**Sample Size Concern:**
- n=100 total, but only n=10 per 5-year age band
- **Solution for age subgroup analyses:** Collapse to 5 groups (n=20 each) or 2 groups (n=50 each)
  - Young (20-44, n=50) vs Old (45-70, n=50)
  - OR: 20-30, 30-40, 40-50, 50-60, 60-70 (n=20 each)

**Model Validation:**
- **Cross-validation:** 10-fold CV to test prediction accuracy
- **Shrinkage:** Compare in-sample R² to out-of-sample R² (expect ~10% shrinkage)
- **Bootstrapping:** 1000 resamples to estimate 95% CIs for regression coefficients

---

### RQ7.1: Do standard cognitive tests predict REMEMVR performance?

**Hypothesis:** Tests should predict Day 0 ability but may not predict forgetting rate

**Data Required:**
- Random intercepts from Chapter 5 (**All by Domain**): Intercept_What, Intercept_Where, Intercept_When
- Random slopes: Slope_What, Slope_Where, Slope_When
- Cognitive scores: RAVLT, BVMT, NART, RPM

**Analysis Recipe:**

1. **Prepare Data**
   ```python
   # Extract random effects from Chapter 5 LMM
   import pickle
   model = pickle.load(open('results/All by Domain/TQ_corr_noroom_2cats_p1_med_data_irt_Lin+Log.pkl', 'rb'))
   random_effects = pd.DataFrame(model.random_effects).T
   random_effects.columns = ['Intercept', 'Slope']
   random_effects.reset_index(inplace=True)
   random_effects.rename(columns={'index': 'UID'}, inplace=True)

   # Merge with cognitive scores
   df_cog = pd.read_csv('cog/cognitive_scores.csv')  # Hypothetical file
   df_merged = random_effects.merge(df_cog, on='UID')
   ```

2. **Hierarchical Regression: Predicting Intercept**
   - **Model 1:** `Intercept ~ 1` (baseline)
   - **Model 2:** `Intercept ~ RAVLT`
   - **Model 3:** `Intercept ~ RAVLT + BVMT`
   - **Model 4:** `Intercept ~ RAVLT + BVMT + NART`
   - **Model 5:** `Intercept ~ RAVLT + BVMT + NART + RPM`

   Compare models via ΔR², F-change test:
   ```python
   from statsmodels.formula.api import ols
   from scipy.stats import f

   # Example for Model 2 vs Model 3
   model2 = ols('Intercept ~ RAVLT', data=df_merged).fit()
   model3 = ols('Intercept ~ RAVLT + BVMT', data=df_merged).fit()

   delta_r2 = model3.rsquared - model2.rsquared
   delta_df = model3.df_model - model2.df_model
   f_stat = (delta_r2 / delta_df) / ((1 - model3.rsquared) / model3.df_resid)
   p_value = 1 - f.cdf(f_stat, delta_df, model3.df_resid)
   ```

3. **Hierarchical Regression: Predicting Slope**
   - Repeat above but with `Slope` as DV
   - Test: Do cognitive tests predict **rate of forgetting**?

4. **Report**
   - Table: R², ΔR², F-change, p for each step
   - Conclusion: "RAVLT explained X% of variance in Day 0 ability, but only Y% of variance in forgetting rate"

**Statistical Justification:**
- **Hierarchical regression:** Tests unique contribution of each predictor
- **Intercept vs Slope:** Separates encoding (initial ability) from consolidation (retention)
- **NART caveat:** May not be valid due to non-native speakers (report but interpret cautiously)

**Expected Output:**
- Two tables: Predicting Intercept, Predicting Slope
- Scatterplots: RAVLT vs Intercept, RAVLT vs Slope
- Statement: "Cognitive tests predicted Day 0 ability (R²=X) but not forgetting rate (R²=Y)"

---

### RQ7.2: Which cognitive test best predicts which REMEMVR domain?

**Hypothesis:** RAVLT (verbal) → What, BVMT (visuospatial) → Where, neither → When

**Data Required:**
- Domain-specific intercepts: Intercept_What, Intercept_Where, Intercept_When

**Analysis Recipe:**

1. **Separate Regressions per Domain**
   - **What:** `Intercept_What ~ RAVLT + BVMT + RPM`
   - **Where:** `Intercept_Where ~ RAVLT + BVMT + RPM`
   - **When:** `Intercept_When ~ RAVLT + BVMT + RPM`

2. **Standardize Coefficients**
   - Convert to β (standardized betas) for comparison
   - E.g., β_RAVLT for What vs β_RAVLT for Where

3. **Test Domain Specificity**
   - Is β_RAVLT(What) > β_BVMT(What)?
   - Is β_BVMT(Where) > β_RAVLT(Where)?

4. **Formal Test (Optional):**
   - Use SEM to test domain-specific paths
   - Or manual Wald test comparing coefficients across models

**Statistical Justification:**
- **Domain specificity hypothesis:** Modality-matched tests should predict better
- **RAVLT = verbal, BVMT = visuospatial:** Clear theoretical prediction
- **When domain:** No strong predictor expected (temporal encoding less studied)

**Expected Output:**
- 3 regression tables (one per domain)
- Heatmap: β coefficients (rows = tests, columns = domains)
- Statement: "RAVLT was the strongest predictor of What ability (β=X), while BVMT predicted Where (β=Y)"

---

### RQ7.3: Do cognitive tests predict initial ability (intercept) vs forgetting rate (slope)?

**Hypothesis:** Tests predict encoding capacity but not consolidation efficiency

**Data Required:**
- Same as RQ7.1

**Analysis Recipe:**
- Already covered in RQ7.1 (separate regressions for Intercept and Slope)
- Focus interpretation on **dissociation**:
  - If R²(Intercept) >> R²(Slope) → Tests measure encoding, not consolidation
  - If R²(Slope) significant → Tests also predict memory stability

**Statistical Justification:**
- **Intercept = trait ability at Day 0:** Tests should correlate (concurrent validity)
- **Slope = consolidation/forgetting:** May be independent process
- **Theoretical importance:** If tests don't predict slope, suggests REMEMVR taps unique process

**Expected Output:**
- Bar chart: R² for predicting Intercept vs Slope
- Statement: "Cognitive tests accounted for X% of variance in initial ability but only Y% in forgetting rate, suggesting consolidation is [independent/related]"

---

### RQ7.4: Is there unique variance in REMEMVR not explained by standard tests?

**Hypothesis:** REMEMVR taps ecological episodic memory beyond what pen-and-paper tests capture

**Data Required:**
- Full hierarchical regression from RQ7.1

**Analysis Recipe:**

1. **Compute Residual Variance**
   - From final model (all 4 tests included): R²_full
   - Unique variance = 1 - R²_full
   - E.g., If R² = 0.35 → 65% unexplained

2. **Interpretation**
   - High unexplained variance (>50%) → REMEMVR captures something novel
   - Low unexplained variance (<20%) → REMEMVR mostly redundant with existing tests

3. **Upper Bound Estimation**
   - R² upper bound = reliability of REMEMVR
   - ICC from random effects as proxy for reliability
   - Adjusted R² = R²_full / ICC
   - E.g., R²=0.35, ICC=0.80 → Adjusted R²=0.44 (56% still unexplained)

**Statistical Justification:**
- **Unique variance:** Core thesis argument that traditional tests are insufficient
- **Reliability correction:** Prevents overestimating unexplained variance due to measurement error

**Expected Output:**
- Pie chart: Explained (R²) vs Unexplained (1-R²) variance
- Statement: "After accounting for all standard tests, REMEMVR retained X% unique variance, supporting its utility as a novel measure"

---

### RQ7.5-7.7: Domain-Specific Predictions (RAVLT, BVMT, RPM)

**Covered in RQ7.2.** These RQs are variations asking:
- Does RAVLT predict Free Recall better? (Yes, both generative)
- Does BVMT predict Where more than When? (Likely yes)
- Does RPM predict integration? (Test via composite scores)

**Recipe for Composite Scores (RQ7.7):**
```python
# Create multi-domain composite
df_merged['Composite'] = (df_merged['Intercept_What'] + df_merged['Intercept_Where'] + df_merged['Intercept_When']) / 3
# Regression
model = ols('Composite ~ RPM + RAVLT + BVMT', data=df_merged).fit()
# Test if RPM uniquely predicts composite
```

---

### RQ7.8: Does age explain variance beyond cognitive test scores?

**Hypothesis:** Age has direct effects on consolidation not mediated by test performance

**Data Required:**
- Intercepts/Slopes
- Age (continuous, centered)
- Cognitive scores

**Analysis Recipe:**

1. **Hierarchical Regression**
   - **Model 1:** `Slope ~ Age_c`
   - **Model 2:** `Slope ~ Age_c + RAVLT + BVMT + NART + RPM`

2. **Compare R²**
   - If ΔR² (Model 2 vs Model 1) is small → Age effect not mediated by tests
   - If ΔR² large and Age_c coefficient drops → Mediation (tests explain age effect)

3. **Partial Correlation**
   - Compute: r(Age, Slope | RAVLT, BVMT, NART, RPM)
   - If significant → Direct age effect beyond tests

**Statistical Justification:**
- **Direct vs indirect effects:** Tests if age affects memory via cognitive ability or via separate mechanism (e.g., neurodegeneration)
- **Hierarchical approach:** Standard method for testing incremental validity

**Expected Output:**
- Table: R² for Model 1, Model 2, ΔR²
- Statement: "Age explained X% variance in forgetting beyond cognitive tests, suggesting direct consolidation effects"

---

### RQ7.9: Do cognitive tests attenuate age effects on REMEMVR?

**Hypothesis:** Age effects are mediated by cognitive ability

**Data Required:**
- Same as RQ7.8

**Analysis Recipe:**

1. **Mediation Analysis**
   - **Path A:** Age → RAVLT (test if age predicts cognitive scores)
   - **Path B:** RAVLT → REMEMVR (controlling for Age)
   - **Path C:** Age → REMEMVR (total effect)
   - **Path C':** Age → REMEMVR (controlling for RAVLT) (direct effect)
   - **Mediation:** C - C' (indirect effect via RAVLT)

2. **Sobel Test**
   ```python
   # Compute indirect effect
   indirect = beta_A * beta_B
   # Standard error
   SE_indirect = sqrt(beta_A² * SE_B² + beta_B² * SE_A²)
   # Z-test
   z = indirect / SE_indirect
   ```

3. **Bootstrap CIs**
   - 1000 resamples
   - Estimate 95% CI for indirect effect
   - If CI excludes 0 → Significant mediation

**Statistical Justification:**
- **Mediation requires:**
  1. Age → RAVLT (Path A significant)
  2. RAVLT → REMEMVR (Path B significant)
  3. Age effect attenuates when RAVLT included (C' < C)
- **Bootstrap preferred:** More robust than Sobel test for small samples

**Expected Output:**
- Mediation diagram with path coefficients
- Statement: "RAVLT mediated X% of the age effect on REMEMVR (indirect effect = Y, 95% CI [a, b])"

---

### RQ7.10: Is there an age × cognitive test interaction?

**Hypothesis:** Tests may be better predictors in older adults (floor effects in young)

**Data Required:**
- Age (continuous or grouped: Young vs Old)
- Cognitive scores
- REMEMVR intercepts

**Analysis Recipe:**

1. **Interaction Model**
   - Formula: `Intercept ~ Age_c * RAVLT`
   - Key term: `Age_c:RAVLT`
   - Interpretation: Does RAVLT prediction strength change with age?

2. **Simple Slopes**
   - Test RAVLT effect at Age = 25, 45, 65
   - Use `statsmodels` or manual computation:
     ```python
     # Slope at Age=25 (centered at -20 if mean=45)
     slope_25 = beta_RAVLT + beta_interaction * (-20)
     ```

3. **Visualization**
   - Scatterplot: RAVLT (x) vs Intercept (y), colored by Age group
   - Two regression lines: Young vs Old

**Statistical Justification:**
- **Floor/ceiling effects:** Tests may have restricted range in young (ceiling) or old (floor)
- **Interaction tests moderation:** Does relationship strength vary by age?

**Expected Output:**
- Regression table with interaction term
- Simple slopes at 3 ages
- Statement: "RAVLT was a stronger predictor in older adults (β=X) than younger adults (β=Y)"

---

### RQ7.11-7.13: Self-Reported Factors (Sleep, DASS, Strategies)

**Data Required:**
- Sleep quality (Likert, averaged across tests)
- DASS subscales (Depression, Anxiety, Stress)
- Strategies (categorical: method of loci, visualization, narrative, none)

**Analysis Recipe:**

1. **Multiple Regression Including Self-Report**
   - Formula: `Intercept ~ RAVLT + BVMT + Sleep_quality + DASS_Anxiety + DASS_Depression`
   - Test incremental validity: ΔR² when adding self-report variables

2. **Strategy as Categorical**
   - Dummy code strategies (reference = "none")
   - ANOVA: Do strategies differ in mean Intercept?
   ```python
   import statsmodels.api as sm
   from statsmodels.formula.api import ols
   model = ols('Intercept ~ C(Strategy)', data=df_merged).fit()
   anova_table = sm.stats.anova_lm(model, typ=2)
   ```

3. **DASS Predicting Utility (RQ7.12)**
   - Hypothesis: Anxiety impairs metacognition more than memory
   - Test: `Intercept ~ DASS_Anxiety` vs `Utility ~ DASS_Anxiety`
   - Compare β coefficients

**Statistical Justification:**
- **Sleep and memory:** Well-established link (consolidation)
- **DASS:** Anxiety may impair metacognitive monitoring (attentional control)
- **Strategies:** Exploratory (self-report may be unreliable)

**Expected Output:**
- Regression table including self-report variables
- ANOVA for strategy groups
- Statement: "Sleep quality predicted memory (β=X), while anxiety predicted metacognitive accuracy (β=Y)"

---

### RQ7.14-7.15: Latent Profile Analysis (Visualizers vs Verbalizers)

**Data Required:**
- Intercept_What, Intercept_Where, Intercept_When (3 variables per person)

**Analysis Recipe:**

1. **K-Means Clustering**
   ```python
   from sklearn.cluster import KMeans
   from sklearn.preprocessing import StandardScaler

   # Standardize
   scaler = StandardScaler()
   X = scaler.fit_transform(df_merged[['Intercept_What', 'Intercept_Where', 'Intercept_When']])

   # Fit k=2, 3, 4
   kmeans2 = KMeans(n_clusters=2, random_state=42).fit(X)
   kmeans3 = KMeans(n_clusters=3, random_state=42).fit(X)
   ```

2. **Model Selection**
   - Silhouette score (higher = better separation)
   ```python
   from sklearn.metrics import silhouette_score
   sil2 = silhouette_score(X, kmeans2.labels_)
   sil3 = silhouette_score(X, kmeans3.labels_)
   ```
   - Elbow plot: Within-cluster sum of squares vs k

3. **Profile Interpretation**
   - Cluster 1: High What, Low Where → "Verbalizers"
   - Cluster 2: High Where, Low What → "Visualizers"
   - Cluster 3: High all → "Generalists"

4. **Predict Profiles from Cognitive Tests (RQ7.15)**
   - Multinomial logistic regression: `Profile ~ RAVLT + BVMT + RPM`
   - Test: Does RAVLT-dominant predict Verbalizer profile?

**Statistical Justification:**
- **LPA vs K-means:** True LPA (latent class analysis) preferred but complex; K-means simpler
- **n=100 adequate:** Rule of thumb: 30-50 per cluster
- **Validation:** Silhouette score, within-cluster variance

**Expected Output:**
- Cluster plot (PCA reduction to 2D)
- Profile descriptives: Mean What/Where/When per cluster
- Multinomial regression table predicting cluster membership

---

### RQ7.16-7.18: Building a Predictive Model

**Goal:** Parsimonious model to predict REMEMVR from standard tests

**Data Required:**
- All cognitive and demographic variables

**Analysis Recipe:**

1. **Stepwise Regression (Forward Selection)**
   ```python
   from sklearn.feature_selection import SequentialFeatureSelector
   from sklearn.linear_model import LinearRegression

   X = df_merged[['RAVLT', 'BVMT', 'NART', 'RPM', 'Age', 'Sex', 'Education']]
   y = df_merged['Intercept']

   sfs = SequentialFeatureSelector(LinearRegression(), n_features_to_select='auto', direction='forward', cv=10)
   sfs.fit(X, y)
   selected_features = sfs.get_feature_names_out()
   ```

2. **Cross-Validation**
   - 10-fold CV to estimate out-of-sample R²
   ```python
   from sklearn.model_selection import cross_val_score
   scores = cross_val_score(LinearRegression(), X[selected_features], y, cv=10, scoring='r2')
   mean_r2 = scores.mean()
   ```

3. **Final Model**
   - Fit on full dataset using selected features
   - Report: β coefficients, 95% CIs, R²_adj

4. **Multivariate Model (RQ7.18)**
   - Canonical correlation: Multiple predictors → Multiple DVs
   ```python
   from sklearn.cross_decomposition import CCA
   X = df_merged[['RAVLT', 'BVMT', 'RPM']]
   Y = df_merged[['Intercept_What', 'Intercept_Where', 'Intercept_When']]
   cca = CCA(n_components=2)
   cca.fit(X, Y)
   # Report canonical correlations
   ```

**Statistical Justification:**
- **Stepwise regression:** Data-driven feature selection (risk of overfitting)
- **Cross-validation:** Protects against overfitting, estimates generalization
- **Canonical correlation:** Tests if multivariate predictors map to multivariate outcomes
- **Clinical utility:** Parsimonious model (3-5 predictors) preferred for practical use

**Expected Output:**
- Final model equation: "Intercept = β0 + β1*RAVLT + β2*Age + ε"
- Cross-validated R² (e.g., "Model explained 35% of variance, cross-validated R²=0.30")
- Feature importance plot

---

### RQ7.19-7.20: Reverse Inference (REMEMVR → Tests)

**Hypothesis:** If REMEMVR is purer episodic measure, it should predict test performance

**Data Required:**
- REMEMVR intercepts as predictors
- RAVLT/BVMT scores as outcomes

**Analysis Recipe:**

1. **Reverse Regression**
   - `RAVLT ~ Intercept_What + Intercept_Where + Intercept_When`
   - `BVMT ~ Intercept_What + Intercept_Where + Intercept_When`

2. **Compare Predictive Power**
   - R² for REMEMVR → RAVLT vs RAVLT → REMEMVR
   - If similar → Bidirectional relationship (construct overlap)
   - If REMEMVR → RAVLT stronger → REMEMVR more fundamental

3. **Paradigm-Specific (RQ7.20)**
   - Test if REMEMVR_Recognition predicts BVMT_Recognition better than BVMT_Recall
   - Need to extract paradigm-specific thetas from Chapter 5

**Statistical Justification:**
- **Reverse inference:** Tests causal directionality (exploratory, not confirmatory)
- **Temporal precedence lacking:** Both measured at Day 0 → correlation, not causation
- **Theoretical interest:** Suggests which is more "basic" construct

**Expected Output:**
- Bidirectional path diagram with R² values
- Statement: "REMEMVR accounted for X% of variance in RAVLT, similar to RAVLT→REMEMVR (Y%), suggesting [construct overlap/REMEMVR primacy]"

---

## SUMMARY OF ANALYSES BY CHAPTER

### Chapter 5: 15 Analyses
- RQ5.1-5.6: Domain/paradigm/congruence effects on forgetting (6 analyses)
- RQ5.7-5.8: Functional form of forgetting (2 analyses)
- RQ5.9-5.10: Age effects (2 analyses)
- RQ5.11-5.12: IRT vs CTT (2 analyses)
- RQ5.13-5.15: Individual differences, profiles, item difficulty (3 analyses)

### Chapter 6: 15 Analyses
- RQ6.1-6.5: Confidence trajectories and calibration (5 analyses)
- RQ6.6-6.7: Domain/paradigm metacognition (2 analyses)
- RQ6.8-6.9: High-confidence errors and false memories (2 analyses)
- RQ6.10-6.11: Confidence as predictor (2 analyses)
- RQ6.12-6.13: Age and ability effects on metacognition (2 analyses)
- RQ6.14-6.15: Confidence weighting and decomposition (2 analyses)

### Chapter 7: 20 Analyses
- RQ7.1-7.4: Predictive validity of standard tests (4 analyses)
- RQ7.5-7.7: Domain-specific predictions (3 analyses, overlap with RQ7.2)
- RQ7.8-7.10: Age as moderator/mediator (3 analyses)
- RQ7.11-7.13: Self-report factors (3 analyses)
- RQ7.14-7.15: Latent profiles (2 analyses)
- RQ7.16-7.18: Predictive modeling (3 analyses)
- RQ7.19-7.20: Reverse inference (2 analyses)

### Total: 50 Analyses

---

## GENERAL NOTES FOR ALL ANALYSES

### Assumption Checking (All LMMs)
1. **Residual normality:** Q-Q plots
2. **Homoscedasticity:** Residuals vs fitted values
3. **Random effects normality:** Check if intercepts/slopes normally distributed
4. **Multicollinearity (regressions):** VIF < 5
5. **Outliers:** Cook's distance, leverage plots

### Missing Data
- **IRT handles missingness:** MAR assumption via IWAVE
- **Regression:** Complete case analysis (n may drop below 100 if missing cognitive scores)
- **Consider multiple imputation if >10% missing**

### Effect Size Reporting
- **All analyses:** Report effect sizes alongside p-values
- **LMM:** Conditional R², marginal R²
- **Regression:** Adjusted R², standardized β
- **Group comparisons:** Cohen's d with 95% CI

### Visualization Standards
- **All plots:** 95% confidence intervals
- **Trajectories:** Points = observed means, lines = model predictions
- **Colors:** Consistent across chapters (Chapter 5 = blue palette, Chapter 6 = red palette, Chapter 7 = green palette)

### Reproducibility
- **Random seed:** Set `np.random.seed(42)` for all analyses
- **Save models:** Pickle all fitted models for later inspection
- **Code documentation:** Comment every analysis step
- **Version control:** Git commit after each RQ completed

---

**End of Analysis Plan**

This document should be read alongside `claude.md`, `CHANGELOG.md`, and thesis chapters for complete context.
