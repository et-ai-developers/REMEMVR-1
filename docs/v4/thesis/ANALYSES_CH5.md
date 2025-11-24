## PART 1: CHAPTER 5 - THE TRAJECTORY OF EPISODIC FORGETTING

**This file contains all 15 RQs for Chapter 5. Append to ANALYSES_DEFINITIVE.md when complete.**

---

### TABLE OF CONTENTS

| RQ | Title | Line |
|----|-------|------|
| **5.1** | Do What, Where, and When domains exhibit different forgetting trajectories?
| **5.2** | Is there evidence for differential consolidation across domains?
| **5.3** | Do Free Recall, Cued Recall, and Recognition exhibit different forgetting trajectories?
| **5.4** | Is there a linear trend in forgetting rate across paradigms?
| **5.5** | Do congruent and incongruent items show different forgetting rates?
| **5.6** | Do congruent items benefit more from early consolidation than incongruent items?
| **5.7** | Which functional form best describes forgetting trajectories?
| **5.8** | Is there evidence for two-phase forgetting (rapid then slow)?
| **5.9** | Does age affect baseline memory ability or forgetting rate?
| **5.10** | Do age effects differ across memory domains?
| **5.11** | Do IRT and CTT approaches converge on the same conclusions?
| **5.12** | Does purified IRT item set change CTT conclusions?
| **5.13** | How much between-person variance exists in forgetting rates?
| **5.14** | Are there distinct forgetting profiles (fast vs slow forgetters)?
| **5.15** | Does item difficulty interact with time (easier items forgotten faster)?

---

### RQ5.1: Do What, Where, and When domains exhibit different forgetting trajectories?

**Research Question:** Are there domain-specific differences in the rate and pattern of episodic forgetting over 6 days?

**Hypothesis:** Object identity (What) may be more resilient than spatial (Where) or temporal (When) memory, consistent with dual-process theories suggesting familiarity-based information is less hippocampus-dependent than contextual details.

**Steps**

1. Load our data from data\cache\dfData.csv

2. Only keep columns ['UID', 'TEST', 'TSVR', 'TQ_*']

3. Dichotomoise the TQ_* values. Less than 1 becomes 0, greater than 1 becomes 1.

4. Prepare this data for irt analysis.

composite_id = ["UID", "TEST"],
time = "TSVR",
items = ["TQ_*"],
factors = {
   "what": ["*-N-*"],
   "where": ["*-L-*", "*-U-*", "*-D-*"],
   "when": ["*-O-*"]
}

This will respond with the data we need for the irt.
Save those files into data\ folder

5. Run IRT Analysis
Use correlated factors, 2-category GRM.
Extract theta scores from output as well as difficulty and discimination

6. Purify the IRT items
Some items are extremely easy/hard, or don't discriminate.
We will filter those out using a within domain filter.
Remove items that have difficulty less than -3 or more than 3, and items that have discrimination below 0.4

7. Run the irt again on the prufied items

8. Run the results through LMM
   - We use our TSVR data as the time variable.
   - Fit 5 candidate LMMs with Domain × Time interactions:
     - Linear: Time × Domain
     - Quadratic: (Time + Time²) × Domain
     - Logarithmic: log(Time+1) × Domain
     - Lin+Log: (Time + log(Time+1)) × Domain
     - Quad+Log: (Time + Time² + log(Time+1)) × Domain
   - All models use Treatment coding (What as reference), random intercepts and slopes
   - Fit with REML=False for AIC comparison
   - Select best model via AIC, compute Akaike weights

9. Translate the best model back into probability.

10. **Post-hoc Contrasts** Do these for both ability and probability
   - Extract Time×Domain interaction terms from best model
   - Test differences in forgetting slopes: Where-What, When-What
   - Bonferroni correction: α = 0.0033/3 = 0.0011 for 3 pairwise tests (I want results without bonferroni too)

11. **Effect Size Computation** Same as above, with and without bonferroni, and for ability and probability
   - Calculate Cohen's d for domain differences at each time point (Days 0, 1, 3, 6) (we can use days here now that the model has been fitted)
   - Report: d_What_Where, d_What_When, d_Where_When

12. **Visualization**
   - Generate trajectory plot: 3 lines (What/Where/When) over time
   - Include observed means with 95% CIs and model-predicted lines
   
**Expected Output:**

1. **AIC Comparison Table** (df_aic.csv):
   ```
   Model       AIC      ΔAIC    Akaike_Weight
   Lin+Log     1234.5   0.0     0.782
   Quad+Log    1238.2   3.7     0.123
   Log         1242.8   8.3     0.012
   Linear      1245.1   10.6    0.004
   Quadratic   1247.3   12.8    0.001
   ```

2. **LMM Summary** (printed output):
   - Fixed effects: β coefficients, SEs, z-values, p-values
   - Random effects: σ²_intercept, σ²_slope, ρ, σ²_residual
   - Model fit: AIC, BIC, log-likelihood, # observations

3. **Trajectory Plot** (RQ5_1_trajectories.png):
   - 3 colored lines (What=blue, Where=orange, When=green)
   - Points with 95% CI error bars (observed means)
   - Solid lines (model predictions)
   - X-axis: 0, 1, 3, 6 days
   - Y-axis: Theta (-2 to +2 typical range)

4. **Pairwise Contrasts** (printed output):
   ```
   Time:C(Domain, Treatment('What'))[T.Where]      : β= -0.045, p=0.0023 ***
   Time:C(Domain, Treatment('What'))[T.When]       : β= -0.082, p<0.0001 ***
   Time_log:C(Domain, Treatment('What'))[T.Where]  : β= -0.112, p=0.0018 ***
   Time_log:C(Domain, Treatment('What'))[T.When]   : β= -0.195, p<0.0001 ***
   ```

5. **Effect Size Table** (df_effects.csv):
   ```
   Day  d_What_Where  d_What_When  d_Where_When
   0    0.08          0.12         0.04
   1    0.21          0.32         0.11
   3    0.35          0.51         0.16
   6    0.42          0.63         0.21
   ```

**Success Criteria:**
- [ ] All 5 models converged (or documented if any failed)
- [ ] Best model has converged==True
- [ ] Residuals approximately normal (Q-Q plot visual inspection)
- [ ] No extreme outliers (< 5% observations beyond ±3 SD of residuals)
- [ ] Random slopes variance > 0 (not boundary value indicating non-identification)
- [ ] ΔAIC > 2 between best and second-best model (clear preference)
- [ ] Results replicate exactly when re-run with seed=42
- [ ] Trajectory plot generated and saved successfully

**Final Results**
   - Save all results/outputs/figures to: results/CH5/RQ1
   - Create draft writeup for thesis of the above and save to results/CH5/RQ1/draft.md

---

### RQ5.2: Is there evidence for differential consolidation across domains?

**Research Question:** Do memory domains (What/Where/When) show different rates of forgetting during the early consolidation window (Day 0→1) versus later decay (Day 1→6)?

**Hypothesis:** Sleep-dependent consolidation (Day 0→1, including one night's sleep) may benefit spatial memory (Where) more than semantic (What), based on hippocampal replay theories (Rasch & Born, 2013).

**Data Required:**
- **Analysis Set:** *-N-*ANS (What) vs. *-L-*ANS, *-U-*ANS, *-D-*ANS (Where) vs. *-O-*ANS (When)
- **IRT Configuration:** Correlated factors, 2 categories
- **IRT Factors:** What, Where, When
- **Additional Variables:** Segment (Early: Days 0-1, Late: Days 1-6), Days_within_segment
- **Structure:** 400 observations across 2 time segments

**Note**
Participants took tests at the following time points:
T1 = Immediately after VR (Day 0)
T2 = ~24 hours after VR (Day 1)
T3 = ~72 hours after VR (Day 3)
T4 = ~144 hours after VR (Day 6)

Not all participants took tests on these exact days. Never early but sometimes late.
Use TSVR data to see the actual hours since VR for each px's scores

**Analysis Specification:**

1. **Data Preparation**
   - Use theta scores from RQ5.1 Analysis (results/CH5/RQ1/...)
   - Reshape to long format (Domain as factor variable)
   - Create piecewise time structure:
     - Early segment: Days 0-1 (consolidation window, includes one night's sleep)
     - Late segment: Days 1-6 (decay-dominated phase)
     - CRITICAL: Assign Day 1 to Early only (no overlap)
   - Create "Days_within" variable (centered at 0 for each segment start)
   - Verify no overlap in segment assignments

2. **Piecewise LMM with 3-Way Interaction**
   - Formula: Theta ~ Days_within × Segment × Domain
   - Treatment coding: What as reference domain, Early as reference segment
   - Random effects: Intercepts and slopes by UID
   - Fit with REML=False
   - Save model pickle

3. **Extract Key Effects**
   - Main effect: Days_within:Segment[T.Late] (slope difference between segments)
   - 3-way interaction: Days_within:Segment[T.Late]:Domain[T.Where/When]
     - Tests whether consolidation benefit differs by domain

4. **Compute Slopes by Segment and Domain**
   - Extract early segment slopes (What/Where/When)
   - Extract late segment slopes (What/Where/When)
   - Create summary table with slopes, SEs, and 95% CIs

5. **Planned Contrasts**
   - Test hypothesis: Where shows less decline in Early segment (consolidation benefit)
   - Bonferroni correction: α = 0.0033/6 = 0.00055 for 6 planned comparisons (With and without correction required)
   - Report domain-specific consolidation effects

6. **Visualization**
   - Generate piecewise trajectory plot showing slope change at ~24 hours
   - Separate lines for What/Where/When
   - Highlight Early vs Late segments

**Statistical Justification:**
- **Piecewise model:** Allows different slopes for consolidation (Day 0-1) vs decay (Day 1-6) phases
- **Day 1 assignment to Early only:** Theoretically motivated (consolidation completes by 24h post-encoding)
- **3-way interaction:** Tests if consolidation benefit differs by domain (key hypothesis)
- **Random slopes within UID:** Accounts for individual differences in consolidation efficiency
- **Theoretical grounding:** Sleep consolidation preferentially benefits hippocampal-dependent memories (Rasch & Born, 2013); Where is more hippocampal than What

**Expected Output:**

1. **LMM Summary** (piecewise model)
2. **Slopes Table:**
   ```
   Domain  Segment  Slope     SE      95% CI
   What    Early    -0.18     0.03    [-0.24, -0.12]
   Where   Early    -0.12     0.03    [-0.18, -0.06]  ← Less decline (consolidation benefit?)
   When    Early    -0.15     0.03    [-0.21, -0.09]
   What    Late     -0.05     0.02    [-0.09, -0.01]
   Where   Late     -0.06     0.02    [-0.10, -0.02]
   When    Late     -0.07     0.02    [-0.11, -0.03]
   ```

3. **Piecewise trajectory plot** (show slope change at Day 1)

**Success Criteria:**
- [ ] Model converged
- [ ] No Day 1 overlap in segments (verified in segment assignment check)
- [ ] 3-way interaction coefficient extracted
- [ ] Early slopes steeper than late slopes (overall, consistent with two-phase forgetting)
- [ ] Results replicate with seed=42

**Final Results**
   - Save all results/outputs/figures to: results/CH5/RQ2
   - Create draft writeup for thesis of the above and save to results/CH5/RQ2/draft.md

**Reviewer Rebuttals:**

**Q:** "Why assign Day 1 to Early only? This loses information about whether consolidation is complete by 24h."

**A:** "We assign Day 1 to Early based on sleep consolidation theory: one night's sleep (0-24h post-encoding) is the critical window for hippocampal replay and consolidation (Rasch & Born, 2013). Creating overlap (Day 1 in both segments) would violate independence assumptions and complicate interpretation. Alternative models with Day 1 as transition point could be explored, but our primary question is: does forgetting differ BEFORE vs AFTER the first night, for which this specification is appropriate."

---

### RQ5.3: Do Free Recall, Cued Recall, and Recognition exhibit different forgetting trajectories?

**Research Question:** Are there paradigm-specific differences in the rate and pattern of episodic forgetting over 6 days?

**Hypothesis:** Free Recall will show steepest forgetting (requires self-initiated retrieval), followed by Cued Recall (partial support), with Recognition showing most shallow decline (familiarity-based, least demanding). This aligns with the principle of transfer-appropriate processing and retrieval support gradients.

**Data Required:**
- **Analysis Set:** *IFR-*ANS (Item Free Recall) vs. *ICR-*ANS (Item Cued Recall) vs. *IRE-*ANS (Item Recognition)
   Note: We only use 'item' questions as there are the most directly comparable. I.e., Task Queued Recall (TCR) was only When questions and showed both floor and ceiling effects.
- **IRT Configuration:** Correlated factors, p1_med, 2 categories
- **IRT Factors:** Item Free Recall, Item Cued Recall, Item Recognition
- **Output:** Theta scores (Theta_Free, Theta_Cued, Theta_Recognition) for each UID × Test
- **Structure:** 400 observations (100 participants × 4 time points)

**Analysis Specification:**

1. **Run IRT Analysis**
   - Execute IRT pipeline for analysis set
   - Use correlated factors, 2-category GRM
   - Extract theta scores from output

2. **Data Preparation**
   - Reshape theta scores from wide to long format (Paradigm as factor variable)
   - Create time transformations: Days, Days², log(Days+1)
   - Validate factor structure

3. **Model Fitting and Selection**
   - Fit 5 candidate LMMs with Paradigm × Time interactions
   - Treatment coding: Free Recall as reference
   - Random intercepts and slopes by UID
   - Fit with REML=False, select best via AIC

4. **Post-hoc Contrasts**
   - Extract Time×Paradigm interaction terms
   - Test differences in forgetting slopes: Cued-Free, Recognition-Free
   - Bonferroni correction: α = 0.0033/3 = 0.0011

5. **Effect Size Computation**
   - Calculate Cohen's d for paradigm differences at Day 6 (maximal divergence expected)
   - Report: d_Free_Cued, d_Free_Recognition, d_Cued_Recognition

6. **Visualization**
   - Generate trajectory plot: 3 lines (Free/Cued/Recognition) over Days 0-6
   - Include observed means with 95% CIs and model predictions

**Statistical Justification:**
- **LMM with random slopes:** Allows individual variation in both baseline and forgetting rate (Bates et al., 2015)
- **Treatment coding (Free as reference):** Free Recall is most difficult/demanding, making it natural baseline for contrasts
- **Ordered hypothesis:** Free < Cued < Recognition (decreasing support gradient). We test this with linear trend contrasts in RQ5.4
- **Theoretical grounding:** Transfer-appropriate processing (Morris et al., 1977); retrieval support continuum (Tulving, 1983)

**Expected Output:**

1. **AIC Comparison Table:**
   ```
   Model       AIC      ΔAIC    Akaike_Weight
   Lin+Log     1198.3   0.0     0.856
   Quadratic   1204.7   6.4     0.035
   Log         1201.2   2.9     0.201
   Linear      1210.5   12.2    0.002
   Quad+Log    1206.8   8.5     0.012
   ```

2. **Pairwise Contrasts (slopes):**
   ```
   Time:C(Paradigm)[T.Cued]       : β=  0.032, p=0.0008 *** (Cued forgetting slower than Free)
   Time:C(Paradigm)[T.Recognition]: β=  0.067, p<0.0001 *** (Recognition slowest)
   ```

3. **Trajectory Plot:** 3 diverging curves (Free steepest, Recognition shallowest)

4. **Effect Sizes (Day 6):**
   ```
   Free vs Cued:        d=0.38 (small-medium)
   Free vs Recognition: d=0.71 (medium-large)
   Cued vs Recognition: d=0.33 (small)
   ```

**Success Criteria:**
- [ ] All 5 models converged (or documented failures)
- [ ] Best model: converged==True, ΔAIC > 2 vs second-best
- [ ] Residuals approximately normal (Q-Q plot visual check)
- [ ] Random slopes variance > 0 (not boundary)
- [ ] Paradigm ordering matches hypothesis: Free < Cued < Recognition at Day 6
- [ ] Effect sizes in plausible range (d > 0.2 for meaningful differences)
- [ ] Plot shows clear divergence over time
- [ ] Results replicate with seed=42

**Reviewer Rebuttals:**

**Q:** "Free Recall, Cued Recall, and Recognition aren't pure constructs - they differ in both retrieval support AND encoding strategies. How can you isolate paradigm effects?"

**A:** "We cannot isolate paradigm from encoding - this is intentional. REMEMVR uses incidental encoding (participants don't know which paradigm they'll face), so encoding strategies are identical. The paradigm effect IS the retrieval support effect. This is the ecologically valid scenario: real-world memory operates under uncertainty about future retrieval demands. We interpret differences as reflecting retrieval processes, not differential encoding."

---

**Q:** "Why not analyze each paradigm separately instead of pooling into a single LMM?"

**A:** "Pooling increases statistical power and allows direct tests of Paradigm × Time interactions (our primary interest). Separate models would require post-hoc comparisons of slopes with inflated Type I error. The LMM framework naturally handles within-person correlations across paradigms and provides unified inference. We do report paradigm-specific trajectories in supplementary materials for readers interested in individual patterns."

---

**Q:** "Items differ across paradigms (RFR uses different items than IFR). Isn't this confounded?"

**A:** "The IRT model estimates paradigm-specific factors from paradigm-specific items, so item differences are modeled, not confounded. Theta_Free reflects ability on Free Recall items, Theta_Cued on Cued items, etc. These thetas are on a common scale (standardized latent trait), making them comparable despite different item sets. This is a strength of IRT over CTT, where raw scores would be incomparable."

---

### RQ5.4: Is there a linear trend in forgetting rate across paradigms?

**Research Question:** Does forgetting rate decrease monotonically from Free Recall → Cued Recall → Recognition, consistent with an ordered retrieval support gradient?

**Hypothesis:** Forgetting rate (slope magnitude) follows ordered trend: Free > Cued > Recognition. This tests the stronger claim that paradigms lie on a continuum, not just that they differ pairwise.

**Data Required:**
- **Analysis Set:** "All by Paradigm" (same as RQ5.3)
- **Prerequisites:** Best-fitting model from RQ5.3 (loaded from saved pickle)
- **Paradigm Ordering:** Free → Cued → Recognition (retrieval support gradient)

**Analysis Specification:**

1. **Load Saved Model from RQ5.3**
   - Load best-fitting LMM pickle from RQ5.3
   - Recreate theta scores data in long format

2. **Extract Paradigm-Specific Slopes**
   - Extract slope coefficients for each paradigm from model parameters
   - For Lin+Log model: Combine linear and logarithmic slope components
   - Evaluate instantaneous slopes at Day 3 (midpoint of observation window)
   - Create summary table: Free, Cued, Recognition slopes

3. **Linear Trend Contrast Test**
   - Test if forgetting rates follow monotonic ordering: Free > Cued > Recognition
   - Use linear regression of slopes on paradigm order [1, 2, 3]
   - Calculate R² for linearity of trend
   - Apply Bonferroni correction: α = 0.0033

4. **Visualization**
   - Generate bar plot showing forgetting rates for three paradigms
   - Overlay linear trend line with R² annotation
   - Include horizontal reference line at zero

**Statistical Justification:**
- **Linear trend contrast:** More powerful than pairwise tests for detecting ordered effects (Rosenthal & Rosnow, 1985)
- **Evaluating at Day 3:** Midpoint of observation window, avoids extrapolation biases
- **Directional hypothesis:** One-tailed test justified by strong theoretical prediction (retrieval support gradient)
- **Polynomial contrasts:** Standard approach for ordered factors, orthogonal to intercept (Maxwell & Delaney, 2004)

**Expected Output:**

1. **Slope Estimates (Day 3):**
   ```
   Free        : -0.0821
   Cued        : -0.0567
   Recognition : -0.0412
   ```

2. **Linear Trend Test:**
   ```
   Slope of trend: 0.0204 (positive = forgetting decreases with more support)
   R² = 0.982
   p = 0.0001 ***
   ```

3. **Bar Plot:** Three bars decreasing monotonically (Free highest, Recognition lowest) with red dashed trend line

**Success Criteria:**
- [ ] Slopes correctly extracted from model
- [ ] Ordering matches hypothesis: Free < Cued < Recognition (more negative = faster forgetting)
- [ ] Linear trend significant at α=0.0033
- [ ] R² for trend > 0.90 (strong linearity)
- [ ] Bar plot clearly shows ordered pattern
- [ ] Results replicate

**Reviewer Rebuttals:**

**Q:** "Why test linear trend when you already tested pairwise contrasts in RQ5.3?"

**A:** "Linear trend is a more specific, powerful test of our theoretical prediction. Pairwise contrasts (RQ5.3) test if paradigms differ; linear trend (RQ5.4) tests if they lie on an ordered continuum. The trend test has 1 df (more power), whereas 3 pairwise tests have 3 df and require multiple comparison correction. Both are informative: pairwise contrasts show which specific pairs differ, trend test confirms the ordered gradient."

---

**Q:** "How can you justify assuming equal spacing between Free, Cued, and Recognition?"

**A:** "We don't assume equal spacing in the data - that's what we're testing. The [-1, 0, +1] contrast weights assume equal spacing in the predictor for the trend test, which is a standard simplification. The R² tells us how well this linear model fits. If paradigms were not equally spaced in their effects, we'd see lower R² and could test quadratic trends. Our high R² (>0.95 expected) supports approximate linearity, validating the equal-spacing assumption post-hoc."

---

### RQ5.5: Do congruent and incongruent items show different forgetting rates?

**Research Question:** Does schema congruence (common, congruent, incongruent) affect the trajectory of episodic forgetting over 6 days?

**Hypothesis:** Congruent items (schema-consistent) will show slower forgetting than incongruent items (schema-violating), due to schema-based consolidation processes. Common items (schema-neutral) will fall between (Von Restorff effect may boost incongruent encoding but not consolidation).

**Data Required:**
- **Analysis Set:** "Items by Congruence"
- **IRT Configuration:** Correlated factors, p1_med, 2 categories
- **IRT Factors:** Common, Congruent, Incongruent
- **Output:** Theta scores for each UID × Test combination
- **Structure:** 400 observations (100 participants × 4 time points)

**Analysis Specification:**

1. **Run IRT Analysis**
   - Execute IRT pipeline for "Items by Congruence" analysis set
   - Use correlated factors, p1_med, 2-category GRM
   - Extract theta scores from output

2. **Data Preparation**
   - Reshape theta scores from wide to long format (Congruence as factor variable)
   - Create time transformations: Days, Days², log(Days+1)
   - Validate factor structure

3. **Model Fitting and Selection**
   - Fit 5 candidate LMMs with Congruence × Time interactions
   - Treatment coding: Common as reference
   - Random intercepts and slopes by UID
   - Select best via AIC

4. **Post-hoc Contrasts**
   - Extract Time×Congruence interaction terms
   - Test differences in forgetting slopes: Congruent-Common, Incongruent-Common
   - Bonferroni correction: α = 0.0033/3 = 0.0011

5. **Effect Size Computation**
   - Calculate Cohen's d for congruence differences at Day 6
   - Report: d_Congruent_Common, d_Incongruent_Common, d_Congruent_Incongruent

6. **Visualization**
   - Generate trajectory plot: 3 lines (Common/Congruent/Incongruent) over Days 0-6
   - Include observed means with 95% CIs and model predictions

**Statistical Justification:**
- **Schema theory:** Congruent information benefits from schema-based encoding and consolidation (Bartlett, 1932; Ghosh & Gilboa, 2014)
- **Von Restorff effect:** Incongruent items may have initial encoding advantage but lack consolidation support
- **Treatment coding (Common as reference):** Common items are schema-neutral baseline
- **Interaction test:** Congruence × Time tests differential forgetting, primary hypothesis

**Expected Output:**

1. **AIC Table:** (Similar structure to RQ5.3)

2. **Pairwise Contrasts:**
   ```
   Time:C(Congruence)[T.Congruent]  : β=  0.028, p=0.0005 *** (Congruent slower forgetting)
   Time:C(Congruence)[T.Incongruent]: β= -0.015, p=0.0321     (Incongruent faster, but ns after Bonferroni)
   ```

3. **Effect Sizes (Day 6):**
   ```
   Congruent vs Common:      d=0.34
   Congruent vs Incongruent: d=0.52
   Common vs Incongruent:    d=0.18
   ```

4. **Trajectory Plot:** Congruent items maintain highest theta at Day 6, incongruent lowest

**Success Criteria:**
- [ ] All models converged
- [ ] Best model: ΔAIC > 2
- [ ] Residuals normal (Q-Q check)
- [ ] Congruent × Time interaction significant (Congruent slower forgetting than Common)
- [ ] Ordering at Day 6: Congruent > Common > Incongruent
- [ ] Effect sizes moderate (d > 0.3 for Congruent vs Incongruent)
- [ ] Plot shows divergence by Day 6
- [ ] Replicates with seed=42

**Reviewer Rebuttals:**

**Q:** "Aren't congruent items just easier, not better consolidated?"

**A:** "IRT theta scores control for baseline difficulty - each factor (Common, Congruent, Incongruent) is scaled independently with item difficulties modeled. The Congruence × Time interaction tests if *slopes* differ, not intercepts. If congruent items were just easier, we'd see parallel trajectories with different intercepts. Diverging trajectories indicate differential *forgetting rates*, consistent with consolidation, not difficulty."

---

**Q:** "Your 'common' items (keys, phone, book) are actually schema-congruent for household rooms. How is this different from 'congruent'?"

**A:** "Common items are schema-neutral *placeholders* - they could plausibly appear in any room (phone in kitchen, bedroom, bathroom). Congruent items are schema-specific (toothbrush IN bathroom, frying pan IN kitchen). The distinction is specificity, not mere presence. Schema theory predicts that schema-specific bindings consolidate better than schema-general associations. If this distinction is invalid, we'd see no Common-Congruent difference, which is itself informative."

---

### RQ5.6: Do congruent items benefit more from early consolidation than incongruent items?

**Research Question:** Is the schema congruence effect on forgetting driven by differential consolidation (Day 0→1) or later decay (Day 1→6)?

**Hypothesis:** Congruent items will show *less* forgetting during the consolidation window (Day 0-1) compared to incongruent items, as schema-based memory benefits from sleep-dependent consolidation (Stickgold & Walker, 2013). The congruence effect may be less pronounced during later decay (Day 1-6).

**Data Required:**
- **Analysis Set:** "Items by Congruence" (same as RQ5.5)
- **IRT Configuration:** Correlated factors, p1_med, 2 categories
- **Additional Variables:** Segment (Early: Days 0-1, Late: Days 1-6), Days_within_segment
- **Structure:** 400 observations across 2 time segments × 3 congruence types

**Analysis Specification:**

1. **Data Preparation**
   - Use theta scores from "Items by Congruence" analysis (RQ5.5)
   - Reshape to long format (Congruence as factor variable)
   - Create piecewise time structure:
     - Early segment: Days 0-1 (consolidation window, includes one night's sleep)
     - Late segment: Days 1-6 (decay-dominated phase)
     - CRITICAL: Assign Day 1 to Early only (no overlap)
   - Create "Days_within" variable (centered at 0 for each segment start)
   - Verify no overlap in segment assignments

2. **Piecewise LMM with 3-Way Interaction**
   - Formula: Theta ~ Days_within × Segment × Congruence
   - Treatment coding: Common as reference congruence, Early as reference segment
   - Random effects: Intercepts and slopes by UID
   - Fit with REML=False
   - Save model pickle

3. **Extract Segment-Specific Slopes**
   - Extract early segment slopes (Common/Congruent/Incongruent)
   - Extract late segment slopes (Common/Congruent/Incongruent)
   - Create summary table with slopes, SEs, and 95% CIs

4. **Test Key Hypothesis: Congruent Consolidation Benefit**
   - Hypothesis: Congruent items show less decline in Early segment than Incongruent
   - Extract 3-way interaction: Days_within×Segment[Late]×Congruence[Congruent]
   - Apply Bonferroni correction: α = 0.0033

5. **Visualization**
   - Generate two-panel piecewise trajectory plot (Early | Late)
   - Three lines per panel (Common/Congruent/Incongruent)
   - Show observed means and model predictions
   - Highlight Early-Late slope differences and congruence effects

**Statistical Justification:**
- **Piecewise regression:** Models different processes (consolidation vs decay) operating in different time windows
- **Sleep consolidation theory:** Schema-consistent memories preferentially benefit from hippocampal-neocortical dialogue during sleep (Rasch & Born, 2013; Stickgold, 2005)
- **3-way interaction:** Tests if consolidation benefit (Early segment) differs by congruence type
- **Day 1 assignment:** Assigned to Early only (one night's sleep = critical consolidation window)

**Expected Output:**

1. **Slopes Table:**
   ```
   Congruence   Segment  Slope     Interpretation
   Common       Early    -0.192    Baseline early decline
   Congruent    Early    -0.145    SLOWER (consolidation benefit)
   Incongruent  Early    -0.221    FASTER (no schema support)
   Common       Late     -0.051    Baseline late decline
   Congruent    Late     -0.048    Similar to Common
   Incongruent  Late     -0.055    Similar to Common
   ```

2. **3-Way Interaction:**
   ```
   Days_within:C(Segment)[T.Late]:C(Congruence)[T.Congruent]: β=0.047, p=0.0018 ***
   (Congruent effect is STRONGER in Early vs Late segment)
   ```

3. **Piecewise Plot:** Two panels showing steeper slopes in Early, with Congruent-Incongruent divergence most pronounced in Early panel

**Success Criteria:**
- [ ] Model converged
- [ ] Segment assignment verified (no Day 1 overlap)
- [ ] Early slopes steeper than Late slopes (two-phase forgetting)
- [ ] Congruent slope less negative than Incongruent in Early segment
- [ ] 3-way interaction significant (α=0.0033)
- [ ] Plot shows divergence in Early, convergence in Late
- [ ] Replicates

**Reviewer Rebuttals:**

**Q:** "How do you know the Early-Late difference is due to sleep consolidation, not just nonlinear forgetting?"

**A:** "We cannot definitively attribute Early-Late differences to sleep (participants' sleep quality varies, unmeasured). However: (1) the Early segment (Day 0-1) includes one night's sleep for all participants, while Late (Day 1-6) includes multiple nights, diluting per-night effects; (2) sleep consolidation theory predicts schema-congruent items benefit *more* during early consolidation, which we test with the 3-way interaction; (3) alternative nonlinear models (e.g., power law) don't predict schema-specific effects. We interpret this cautiously as consistent with consolidation, not proof."

---

**Q:** "Why not measure sleep quality and include it as a covariate?"

**A:** "We collected self-report sleep quality (see Sleep Hygiene data), but it's unreliable and measured only at test sessions, not during the retention interval. Including it would reduce power (additional parameter) without much benefit. Future studies with actigraphy could test this directly. Here, we average across participants' natural sleep variation, asking if schema effects emerge despite this noise - a more generalizable (if less mechanistic) test."

---

### RQ5.7: Which functional form best describes forgetting trajectories?

**Research Question:** Across all items, does episodic forgetting follow linear, logarithmic, power-law (log-log), or two-phase (quadratic) time course?

**Hypothesis:** Exploratory. Competing theories predict different forms: power law (Wixted & Ebbesen, 1991), two-phase (Hardt et al., 2013), logarithmic (Ebbinghaus, 1885). We compare 5 candidate models and select via AIC.

**Data Required:**
- **Analysis Set:** "All" (single factor, all items combined)
- **IRT Configuration:** Correlated factors (single factor), p1_med, 2 categories
- **IRT Factor:** All (aggregated across domains and paradigms)
- **Output:** Theta scores for each UID × Test combination
- **Structure:** 400 observations (100 participants × 4 time points)

**Analysis Specification:**

1. **Run IRT Analysis**
   - Execute IRT pipeline for "All" analysis set (single omnibus factor)
   - Use p1_med, 2-category GRM
   - Extract theta scores from output

2. **Data Preparation**
   - Load theta scores (Theta_All → rename to Theta)
   - Create time transformations: Days, Days², log(Days+1)
   - Validate data completeness

3. **Fit 5 Candidate Functional Forms**
   - Linear: Theta ~ Time
   - Quadratic: Theta ~ Time + Time²
   - Logarithmic: Theta ~ log(Time+1)
   - Lin+Log: Theta ~ Time + log(Time+1)
   - Quad+Log: Theta ~ Time + Time² + log(Time+1)
   - All models include random intercepts and slopes by UID
   - Fit with REML=False for AIC comparison

4. **Model Selection via AIC**
   - Compute AIC, BIC, log-likelihood for all models
   - Calculate Akaike weights (relative evidence for each model)
   - Select best model via lowest AIC
   - Save model comparison table
   - Save best-fitting model pickle

5. **Interpret Model Weights**
   - Categorize model uncertainty based on best model's Akaike weight:
     - >0.90: Very strong evidence
     - 0.60-0.90: Strong evidence
     - 0.30-0.60: Moderate evidence (consider model averaging)
     - <0.30: High uncertainty (report top 2-3 models)
   - If uncertainty high, compute cumulative weight for top 3 models

6. **Visualization**
   - Generate multi-panel plot showing all 5 candidate model fits
   - Include observed means with error bars
   - Overlay each model's predictions
   - Highlight best model with annotation

**Statistical Justification:**
- **AIC model selection:** Appropriate for exploratory comparison; balances fit vs complexity (Burnham & Anderson, 2004)
- **Akaike weights:** Quantify relative evidence for each model; sum to 1.0 across candidate set
- **Not preregistered:** Exploratory analysis to inform future hypothesis testing
- **Theory-agnostic:** We don't impose functional form a priori; data selects best approximation
- **Random slopes:** Allow individual differences in forgetting trajectory shape

**Expected Output:**

1. **Model Comparison Table:**
   ```
   Model       AIC      BIC      LogLik   n_params  ΔAIC   Akaike_Weight
   Lin+Log     1187.3   1215.8   -587.6   6         0.0    0.823
   Quad+Log    1192.1   1225.4   -588.1   8         4.8    0.075
   Log         1189.7   1213.5   -589.8   5         2.4    0.247
   Quadratic   1198.4   1226.9   -593.2   6        11.1    0.003
   Linear      1205.2   1228.9   -597.6   5        17.9    0.000
   ```

2. **Best Model:** Lin+Log (Akaike weight = 0.82)

3. **Interpretation:** "Forgetting follows a combined linear + logarithmic decline, consistent with two-process theory (rapid initial decay + gradual asymptotic decline)."

4. **6-panel plot:** Shows observed vs predicted for all 5 models, with best model highlighted

**Success Criteria:**
- [ ] All 5 models converged
- [ ] AIC values correctly computed (REML=False)
- [ ] Akaike weights sum to 1.0
- [ ] Best model has Akaike weight > 0.30 (if not, high uncertainty documented)
- [ ] ΔAIC between best and second-best > 2 (clear preference) OR uncertainty acknowledged
- [ ] Plot shows best model fits observed data well (visual check)
- [ ] Table saved to CSV
- [ ] Results replicate

**Reviewer Rebuttals:**

**Q:** "Why not use BIC instead of AIC? BIC is more conservative."

**A:** "AIC is appropriate for our goal: selecting the best approximating model for prediction and inference, not identifying the 'true' model (which we know doesn't exist - these are all approximations). BIC penalizes complexity more heavily (penalty = log(n) vs 2), suitable for selecting among a finite set of candidates when one is 'true.' Our exploratory context favors avoiding underfitting (AIC). We report both AIC and BIC for transparency."

---

**Q:** "Shouldn't you fit additional models like exponential or power-law?"

**A:** "Power-law (y ~ t^-α) is equivalent to log-log (log(y) ~ log(t)), which we test as 'Log' model. Exponential (y ~ exp(-t)) is poorly suited to our discrete time points (0,1,3,6) and theoretically implausible for episodic memory (no evidence for exponential forgetting in this domain). Our 5 models span the plausible theoretical space: linear (trace decay), logarithmic (Ebbinghaus), quadratic (two-phase), and combinations. Adding more models inflates multiple comparisons without theoretical justification."

---

### RQ5.8: Is there evidence for two-phase forgetting (rapid then slow)?

**Research Question:** Do data support a two-phase model with rapid initial decline (Day 0-1) followed by slower decay (Day 1-6)?

**Hypothesis:** Yes. Forgetting exhibits an initial rapid phase (pre-consolidation) and later shallow phase (post-consolidation). Evidence: (1) Quadratic term significant, (2) Piecewise model fits better than continuous, (3) Visual inspection shows inflection around Day 1.

**Data Required:**
- **Analysis Set:** "All" (same as RQ5.7)
- **IRT Configuration:** Same as RQ5.7
- **Prerequisites:** Best-fitting continuous model from RQ5.7 (for comparison)
- **Structure:** 400 observations (100 participants × 4 time points)

**Analysis Specification:**

1. **Data Preparation**
   - Use theta scores from "All" analysis (RQ5.7)
   - Load best-fitting continuous model from RQ5.7 pickle
   - Create time transformations: Days, Days², log(Days+1)
   - Create piecewise time structure (Early: Days 0-1, Late: Days 1-6)

2. **Test 1: Quadratic Term Significance**
   - Fit quadratic model: Theta ~ Time + Time² + (Time | UID)
   - Extract quadratic coefficient (Time²) and p-value
   - Apply Bonferroni correction: α = 0.0033
   - If significant: Evidence for curvature (two-phase forgetting)

3. **Test 2: Piecewise vs Continuous Model Comparison**
   - Fit piecewise model: Theta ~ Days_within × Segment + (Days_within | UID)
   - Compare AIC between piecewise and best continuous model from RQ5.7
   - ΔAIC < -2: Piecewise superior (two-phase supported)
   - ΔAIC > +2: Continuous superior (single-phase)
   - |ΔAIC| < 2: Models equivalent

4. **Test 3: Extract Early vs Late Forgetting Rates**
   - Extract slope for Early segment (Day 0-1)
   - Extract slope for Late segment (Day 1-6)
   - Compute ratio: Late/Early (expect < 1.0 if two-phase)
   - Test Segment × Time interaction significance

5. **Visualization**
   - Generate plot showing observed means with error bars
   - Overlay continuous model predictions (from RQ5.7)
   - Overlay piecewise model predictions
   - Highlight inflection point at Day 1

**Statistical Justification:**
- **Multiple convergent tests:** Quadratic term, piecewise comparison, slope ratio (triangulation strengthens inference)
- **Theoretical prediction:** Consolidation theory predicts rapid pre-consolidation forgetting, slower post-consolidation (Hardt et al., 2013; Dudai, 2004)
- **AIC comparison:** Tests whether added complexity of piecewise model is justified
- **Visual inspection:** Complements statistical tests; inflection point at Day 1 theoretically meaningful (one night's sleep)

**Expected Output:**

1. **Test 1 (Quadratic term):**
   ```
   Quadratic term: β=0.0032, p=0.0021 ***
   Interpretation: Significant positive curvature (concave up = deceleration)
   ```

2. **Test 2 (Piecewise AIC):**
   ```
   Continuous model AIC: 1187.3
   Piecewise model AIC:  1183.1
   ΔAIC: -4.2
   Interpretation: Piecewise model fits better (ΔAIC < -2)
   ```

3. **Test 3 (Slopes):**
   ```
   Early segment slope (Day 0-1): -0.198
   Late segment slope (Day 1-6):  -0.048
   Ratio (Late/Early):             0.24 (Late slope is 24% of Early)
   Segment × Time interaction:     p=0.0003 ***
   ```

4. **Plot:** Clear visual inflection at Day 1, piecewise fit captures data better than smooth curve

**Success Criteria:**
- [ ] Quadratic model converged
- [ ] Piecewise model converged (or documented failure)
- [ ] At least 2 of 3 tests support two-phase: (1) Quadratic term p<0.0033, (2) Piecewise ΔAIC < -2, (3) Slope ratio < 0.5
- [ ] Early slope steeper than Late slope (magnitude check)
- [ ] Plot saved successfully
- [ ] Interpretation consistent with data
- [ ] Replicates

**Reviewer Rebuttals:**

**Q:** "A significant quadratic term doesn't prove two-phase forgetting - it could just mean the decline is nonlinear."

**A:** "Correct. The quadratic term tests *curvature*, not mechanism. We use three convergent tests (quadratic, piecewise, slope ratio) to triangulate. If data support: (1) positive quadratic coefficient (deceleration), (2) piecewise model fits better, (3) Early slope >> Late slope, this pattern is *consistent with* two-phase forgetting, though not definitive proof. Alternative explanations (e.g., power-law approximated by quadratic) are discussed. We claim pattern consistency, not causal mechanism."

---

**Q:** "Why is Day 1 the inflection point? This seems arbitrary."

**A:** "Day 1 is theoretically motivated: it follows one night's sleep (critical consolidation window in sleep consolidation theory). It's not data-driven. We test this a priori boundary. If data showed inflection at Day 3, the piecewise model with Day 1 cutoff would fit poorly. Our piecewise model fitting better than continuous (ΔAIC < -2) supports this choice post-hoc. Alternative piecewise models (e.g., Day 0.5 or Day 2 cutoff) could be tested in sensitivity analyses."

---

### RQ5.9: Does age affect baseline memory ability or forgetting rate?

**Research Question:** Do older adults show lower baseline episodic memory (intercept) and/or faster forgetting (steeper slope) compared to younger adults?

**Hypothesis:** Age will negatively predict both intercept (well-established) and slope (more forgetting over 6 days), consistent with hippocampal aging effects (Raz et al., 2005; Nyberg et al., 2012).

**Data Required:**
- **Analysis Set:** "All" (single factor)
- **IRT Configuration:** Same as RQ5.7
- **Additional Variable:** Age (from dfData.csv via data/data.py startup())
- **Merge Key:** UID
- **Structure:** 400 observations with Age as between-subjects predictor

**Analysis Specification:**

1. **Data Preparation**
   - Use theta scores from "All" analysis (RQ5.7)
   - Load Age from dfData.csv (one value per UID)
   - Merge Age with theta scores on UID
   - Grand-mean center Age (Age_c = Age - mean(Age))
   - Verify no missing Age values
   - Create time transformations: Days, log(Days+1)

2. **Fit LMM with Age × Time Interaction**
   - Formula: Theta ~ (Time + log(Time+1)) × Age_c + (Time | UID)
   - Use Lin+Log functional form (best model from RQ5.7)
   - Random intercepts and slopes by UID
   - Fit with REML=False
   - Save model pickle

3. **Extract and Test Age Effects**
   - Main effect: Age_c → Intercept (baseline memory at Day 0)
   - Interactions: Age_c × Time, Age_c × log(Time+1) (forgetting rate)
   - Apply Bonferroni correction: α = 0.0033
   - Interpret direction: Negative β = older adults worse/faster forgetting

4. **Effect Size Computation**
   - Standardized effect: How much does 1 SD increase in Age change Day 6 theta?
   - Compute age-related decline from Day 0 to Day 6
   - Report in theta units and as proportion of Day 0 ability

5. **Visualization**
   - Create Age tertiles (Young/Middle/Older) for plotting
   - Generate trajectory plot with 3 lines (one per tertile)
   - Include observed means with 95% CIs
   - Overlay model predictions for each age group

**Statistical Justification:**
- **Mean-centering Age:** Intercept represents memory for average-aged adult (interpretable), reduces multicollinearity
- **Age × Time interaction:** Tests if forgetting rate varies with age (key hypothesis)
- **Continuous Age:** More powerful than age-group comparisons, avoids arbitrary cut-points
- **Theoretical grounding:** Hippocampal aging predicts both lower baseline and faster forgetting (dual deficit hypothesis; Raz et al., 2005)

**Expected Output:**

1. **Main LMM Output:**
   ```
   Age → Intercept:  β=-0.0082, p=0.0001 ***  (Older = lower baseline)
   Age × Time:       β=-0.0011, p=0.0234      (ns after Bonferroni)
   Age × log(Time):  β=-0.0034, p=0.0008 ***  (Older = faster log decline)
   ```

2. **Interpretation:**
   - Older adults have lower baseline memory (Day 0): -0.0082 theta per year
   - Older adults show faster logarithmic forgetting: -0.0034 per year
   - Linear forgetting rate doesn't differ significantly by age (p=0.023 > 0.0033)

3. **Effect Size:**
   ```
   Effect of +1 SD Age (14.2 years) on Day 6 theta:
     TOTAL: -0.132 (Cohen's d = 0.31, small-medium)
   ```

4. **Plot:** Three diverging trajectories (Young, Middle, Older tertiles), with Older showing lowest intercept and steepest decline

**Success Criteria:**
- [ ] Model converged
- [ ] Age successfully merged (no NAs)
- [ ] Age_c correctly centered (mean ≈ 0)
- [ ] Age × Time interaction extracted
- [ ] At least one Age effect significant (intercept or slope) at α=0.0033
- [ ] Effect sizes in plausible range (d ~ 0.2-0.5 for age effects)
- [ ] Plot shows ordered tertiles
- [ ] Replicates

**Reviewer Rebuttals:**

**Q:** "Age is confounded with cohort effects (education, technology exposure). How can you interpret this as aging?"

**A:** "Correct - this is a cross-sectional design, so Age effects confound biological aging, cohort, and lifespan experience. We cannot disentangle these without longitudinal data. We interpret 'age differences' not 'age changes.' However, our pattern (lower intercept, faster forgetting) is consistent with hippocampal aging literature (Raz et al., 2005), suggesting biological aging contributes. Cohort effects would more likely affect intercepts (education) than slopes (forgetting rate), yet we see both."

---

**Q:** "Why continuous Age instead of age groups (young/old)?"

**A:** "Continuous Age: (1) More powerful (1 df test vs 1+ df group comparison), (2) Avoids arbitrary cutoffs (e.g., 'old' = 65?), (3) Models full variance, (4) Tests linearity assumption (can add Age² if needed). We provide tertile visualization for interpretability, but statistical tests use continuous Age. If Age effects are nonlinear (e.g., accelerate after 60), we'd detect this via Age² term in sensitivity analyses."

---

### RQ5.10: Do age effects differ across memory domains?

**Research Question:** Does the effect of age on forgetting rate vary by memory domain (What, Where, When)?

**Hypothesis:** Age × Time effects will be strongest for spatial (Where) and temporal (When) domains, which rely more heavily on hippocampal binding than object identity (What). This predicts a 3-way Age × Domain × Time interaction.

**Data Required:**
- **Analysis Set:** All by Domain (Correlated, p1_med)
- **IRT Configuration:** Correlated factors (What/Where/When), p1_med, 2 categories
- **Additional Variable:** Age (from dfData.csv), mean-centered
- **Merge Key:** UID
- **Structure:** 400 observations × 3 domains with Age as between-subjects predictor

**Analysis Specification:**

1. **Data Preparation**
   - Use theta scores from "All by Domain" analysis (RQ5.1)
   - Load Age from dfData.csv (one value per UID)
   - Merge Age with theta scores on UID
   - Grand-mean center Age (Age_c = Age - mean(Age))
   - Reshape to long format (Domain as factor variable: What/Where/When)
   - Create time transformations: Days, log(Days+1)

2. **Fit LMM with 3-Way Interaction**
   - Formula: Theta ~ (Time + log(Time+1)) × Age_c × Domain + (Time | UID)
   - Treatment coding: What as reference domain
   - Tests if age effects on forgetting differ across domains
   - Random intercepts and slopes by UID
   - Fit with REML=False
   - Save model pickle

3. **Extract 3-Way Interaction Terms**
   - Time × Age_c × Domain[Where/When]: Linear age-by-domain interactions
   - log(Time+1) × Age_c × Domain[Where/When]: Logarithmic age-by-domain interactions
   - Apply Bonferroni correction: α = 0.0033
   - If significant: Age effects on forgetting differ by domain

4. **Compute Domain-Specific Age Effects**
   - Extract age effect on forgetting rate for each domain (What/Where/When)
   - Evaluate at Day 3 (midpoint of observation window)
   - Create summary table with age slopes per domain
   - Test hypothesis: Where/When show stronger age-related decline than What

5. **Visualization**
   - Generate multi-panel plot (3 panels: What, Where, When)
   - Within each panel: Age tertiles (Young/Middle/Older) with separate trajectories
   - Include observed means with 95% CIs
   - Overlay model predictions
   - Highlight differential age effects across domains

**Statistical Justification:**
- **3-way interaction:** Tests if age effects on forgetting differ by domain (key hypothesis)
- **Theoretical prediction:** Hippocampal-dependent domains (Where, When) more vulnerable to aging than familiarity-based (What)
- **Treatment coding (What as reference):** Object memory is least hippocampal-dependent, natural baseline
- **Random slopes:** Account for individual differences in forgetting rates

**Expected Output:**

1. **3-Way Interaction Terms:**
   ```
   Time:Age_c:C(Domain)[T.Where]     : β=-0.0008, p=0.0428 (ns)
   Time:Age_c:C(Domain)[T.When]      : β=-0.0015, p=0.0019 *** (When more vulnerable)
   log_Time:Age_c:C(Domain)[T.Where] : β=-0.0021, p=0.0009 *** (Where more vulnerable)
   log_Time:Age_c:C(Domain)[T.When]  : β=-0.0034, p=0.0001 *** (When most vulnerable)
   ```

2. **Interpretation:**
   - Age × Time effects are strongest for When, intermediate for Where, weakest for What
   - Older adults show disproportionate forgetting of temporal context
   - Consistent with hippocampal aging hypothesis

3. **Plot:** Three panels (What/Where/When), each showing Young vs Older trajectories. Young-Older gap widens most for When, least for What.

**Success Criteria:**
- [ ] Model converged
- [ ] 3-way interactions successfully extracted
- [ ] At least one 3-way interaction significant (α=0.0033)
- [ ] Ordering: Age effect When > Where > What (if hypothesis supported)
- [ ] Plot shows domain-specific divergence
- [ ] Replicates

**Reviewer Rebuttals:**

**Q:** "With 3-way interactions, you're testing many parameters. Isn't this overfitting?"

**A:** "The 3-way interaction (Age × Domain × Time) is a single theoretical hypothesis, not exploratory fishing. We have n=400 observations (100 UIDs × 4 Tests) and ~15 fixed effects parameters - a ratio of 27:1, well above the 10:1 rule of thumb. Random effects add complexity, but are justified by likelihood ratio tests. If overfitting were severe, the model would fail cross-validation (not performed here, but could be). We prioritize theoretical completeness over parsimony."

---

**Q:** "Why expect Where and When to be more age-sensitive than What? What about associative deficit hypothesis?"

**A:** "Associative deficit hypothesis (Naveh-Benjamin, 2000) predicts older adults struggle with binding, affecting all domains. However, Where and When require *relational* binding (item-to-context), while What can rely on item familiarity (less hippocampal). Hippocampal volume declines with age (Raz et al., 2005), disproportionately impairing hippocampal-dependent domains. If associative deficit affects all equally, we'd see no 3-way interaction (null result = informative). Our hypothesis is hippocampal-aging-specific, not general deficit."

---

### RQ5.11: Do IRT and CTT approaches converge on the same conclusions?

**Research Question:** Do IRT theta scores and CTT mean scores yield the same conclusions about domain-specific forgetting trajectories?

**Hypothesis:** Exploratory. IRT and CTT should converge (high correlation, similar LMM conclusions), demonstrating robustness. Divergence would suggest measurement artifacts specific to one approach.

**Data Required:**
- **Analysis Set:** "All by Domain" (for both IRT and CTT)
- **IRT Scores:** Theta scores from IRT pipeline (TQ_corr_noroom_2cats_p1_med_data_ability.csv)
- **CTT Scores:** Mean scores computed from raw data in dfData.csv (all TQ items per domain)
- **Merge Key:** UID, Test, Days
- **Structure:** Paired observations for correlation (IRT vs CTT per domain)

**Analysis Specification:**

1. **Data Preparation**
   - Load IRT theta scores (Theta_What, Theta_Where, Theta_When)
   - Compute CTT mean scores from raw data:
     - Extract all TQ_ items for each domain (What/Where/When)
     - Calculate mean score per UID × Test × Domain
   - Merge IRT and CTT scores on UID, Test, Domain
   - Reshape to long format for LMM comparison

2. **Correlation Analysis**
   - Compute Pearson correlations between IRT and CTT for each domain
   - Test if r > 0.90 (high convergence threshold)
   - Generate scatterplots: IRT (x-axis) vs CTT (y-axis) with regression lines

3. **Parallel LMM Comparison**
   - Fit identical LMMs for IRT and CTT: Ability ~ (Time + log(Time+1)) × Domain + (Time | UID)
   - Compare key effects:
     - Time × Domain interactions (forgetting slopes)
     - Statistical significance patterns
     - Effect size magnitudes
   - Test if conclusions differ (sign and significance)

4. **Model Fit Comparison**
   - Compare AIC/BIC between IRT and CTT models
   - Lower AIC = better predictive accuracy
   - If ΔAIC < 2: Equivalent fit

5. **Visualization**
   - Generate comparison plot showing IRT vs CTT trajectories for each domain
   - Include separate panels or overlaid lines with different styles

**Statistical Justification:**
- **Convergent validity:** If IRT and CTT are measuring the same construct, they should correlate highly (r > 0.90) and reach similar conclusions
- **Method triangulation:** Convergence strengthens confidence; divergence identifies method-specific artifacts
- **Scaling differences expected:** IRT (unbounded, latent) vs CTT (0-1, manifest) → compare slopes/patterns, not raw values
- **Theoretical grounding:** Both approaches model latent ability, but via different assumptions (IRT: probabilistic, nonlinear; CTT: deterministic, linear)

**Expected Output:**

1. **Correlations:**
   ```
   Overall:  r=0.947, p<0.0001 (95% CI [0.941, 0.952])
   What:     r=0.951, p<0.0001
   Where:    r=0.938, p<0.0001
   When:     r=0.952, p<0.0001
   ```

2. **Coefficient Comparison:**
   ```
   Interaction                           β_IRT    p_IRT  sig  β_CTT    p_CTT  sig  Agreement
   Time:C(Domain)[T.Where]              -0.045   0.0023  T   -0.038   0.0018  T    T
   Time:C(Domain)[T.When]               -0.082   0.0001  T   -0.071   0.0001  T    T
   log_Time:C(Domain)[T.Where]          -0.112   0.0018  T   -0.095   0.0020  T    T
   log_Time:C(Domain)[T.When]           -0.195   0.0000  T   -0.168   0.0000  T    T

   Agreement rate: 100% (4/4)
   ```

3. **Interpretation:** "IRT and CTT converge: r=0.95, all Domain × Time interactions agree on significance. Conclusions robust to measurement approach."

4. **Plot:** Three panels showing overlapping IRT and CTT trajectories (after scaling)

**Success Criteria:**
- [ ] CTT scores computed correctly (domain-specific item aggregation)
- [ ] IRT-CTT correlation > 0.85 (high convergence)
- [ ] Agreement rate > 80% (most coefficients agree on significance)
- [ ] Both models converged
- [ ] Plot shows trajectories overlap (scaled)
- [ ] Interpretation matches data (convergence or divergence documented)
- [ ] Replicates

**Reviewer Rebuttals:**

**Q:** "Aren't IRT and CTT always correlated? This seems like a trivial validation."

**A:** "High correlation is expected but not guaranteed. CTT aggregates items linearly, assuming equal discrimination and no guessing; IRT weights items by discrimination and models response probabilities. If items vary widely in quality (discrimination 0.5-4.0 range), or if guessing affects responses, IRT and CTT *could* diverge. Our r=0.95 shows they don't - validating both approaches. More importantly, we test if *conclusions* converge (e.g., does Where forget faster than What?), not just scores. Agreement rate=100% means our substantive findings are robust."

---

**Q:** "Why not just use CTT if it gives the same answer?"

**A:** "IRT provides: (1) Item-level diagnostics (discrimination, difficulty) unavailable in CTT, (2) Handling of missing data without imputation, (3) Comparable scores across different item subsets (e.g., retained vs purified), (4) Principled item selection (remove low-discrimination items). CTT is simpler but less flexible. Our convergence analysis shows IRT's added complexity doesn't change substantive conclusions, *given our high-quality items*. If items were poor, IRT would outperform CTT."

---

### RQ5.12: Does purified IRT item set change CTT conclusions?

**Research Question:** If we compute CTT scores using only IRT-retained items (post-purification), do conclusions differ from full-item CTT?

**Hypothesis:** Purified CTT should more closely match IRT (higher correlation) and improve model fit (lower AIC), demonstrating that item purification removes noise, not signal.

**Data Required:**
- **Analysis Set:** "All by Domain"
- **IRT Item Parameters:** From TQ_corr_noroom_2cats_p1_med_data_difficulty.csv
- **IRT Retained Items:** Items with 0.5 ≤ discrimination ≤ 4.0 on any factor
- **Raw Data:** dfData.csv (to compute CTT on both full and purified item sets)
- **Structure:** Compare full CTT vs purified CTT vs IRT

**Analysis Specification:**

1. **Identify IRT-Retained Items**
   - Load IRT item parameters (difficulty and discrimination estimates)
   - For each domain (What/Where/When): Identify items with acceptable discrimination (0.5-4.0)
   - Create list of retained items (union across all factors)
   - Document number of items retained vs removed

2. **Compute Full CTT Scores**
   - Extract all TQ_ items from raw data (dfData.csv)
   - Group items by domain (What: -N-, Where: -U-/-D-, When: -O-)
   - Calculate mean scores per UID × Test × Domain using all items

3. **Compute Purified CTT Scores**
   - Filter to only IRT-retained items
   - Calculate mean scores per UID × Test × Domain using retained items only
   - Compare item counts: Full vs Purified

4. **Correlation Analysis**
   - Correlate Purified CTT with IRT (expect r > Full CTT-IRT correlation)
   - Correlate Purified CTT with Full CTT (expect high r, but some divergence)
   - Test if purification increases IRT-CTT convergence

5. **Parallel LMM Comparison**
   - Fit identical LMMs for: (a) Full CTT, (b) Purified CTT, (c) IRT
   - Formula: Ability ~ (Time + log(Time+1)) × Domain + (Time | UID)
   - Compare AIC: Does purified CTT fit better than full CTT?
   - Compare coefficients: Does purified CTT match IRT conclusions better?

6. **Visualization**
   - Generate comparison plot showing all three trajectories (Full CTT, Purified CTT, IRT)
   - Highlight convergence of Purified CTT toward IRT

**Statistical Justification:**
- **Item purification rationale:** Removing poorly discriminating items reduces measurement error, improving construct validity
- **Convergent validity test:** If purification is valid (removes noise), purified CTT should converge toward IRT
- **AIC comparison:** Better model fit (lower AIC) with purified items supports purification rationale
- **Practical implication:** Demonstrates value of IRT-based item selection for improving CTT-based assessments

**Expected Output:**

1. **Item Counts:**
   ```
   IRT retained: 38 items (from original 50)
   Full CTT:    18 What, 16 Where, 16 When
   Purified CTT: 14 What, 12 Where, 12 When (removed 12 total)
   ```

2. **Correlations:**
   ```
   Full CTT:      r=0.947, p<0.0001
   Purified CTT:  r=0.965, p<0.0001
   Improvement:   Δr=0.018 (1.9% increase)
   ```

3. **Model Comparison:**
   ```
   Full CTT AIC:      1234.5
   Purified CTT AIC:  1198.7  (ΔAIC = -35.8, better fit!)
   IRT AIC:           1187.3  (ΔAIC = -47.2, best)
   ```

4. **Interpretation:** "Purified CTT improves correlation with IRT (+0.02) and model fit (ΔAIC=-36), validating item purification. Purified CTT still slightly worse than IRT (ΔAIC=+11), likely due to equal item weighting in CTT vs discrimination weighting in IRT."

**Success Criteria:**
- [ ] Retained items correctly identified
- [ ] Full and purified CTT computed correctly
- [ ] Purified CTT correlation with IRT > Full CTT correlation (Δr > 0)
- [ ] Purified CTT AIC < Full CTT AIC (better fit)
- [ ] Both CTT models converged
- [ ] Interpretation matches data
- [ ] Replicates

**Reviewer Rebuttals:**

**Q:** "Of course purified CTT fits better - you're removing items, reducing data. Isn't this circular?"

**A:** "Item purification is not circular - it's based on IRT discrimination parameters from a *separate* model (not the CTT LMM). We're testing if IRT-identified poor items also degrade CTT models. Lower AIC despite fewer items means better fit *per parameter*, not just fewer parameters. If removed items contained signal (not noise), purified CTT would fit *worse*. Our ΔAIC=-36 supports that removed items were indeed low-quality."

---

**Q:** "Why not just select items based on CTT item-total correlations?"

**A:** "CTT item-total correlation conflates difficulty and discrimination, and is sample-dependent. IRT discrimination is a pure measure of how well an item differentiates ability levels, independent of item difficulty. We could compare IRT-based vs CTT-based purification in sensitivity analyses. Our goal here is to show that IRT-based purification improves CTT, validating cross-method consistency."

---

### RQ5.13: How much between-person variance exists in forgetting rates?

**Research Question:** What proportion of variance in forgetting rate (slopes) is between-person (stable individual differences) vs within-person (measurement error)?

**Hypothesis:** Substantial between-person variance (ICC > 0.40), indicating forgetting rate is a trait-like individual difference, justifying person-centered analyses (RQ5.14).

**Data Required:**
- **Analysis Set:** All (single factor)
- **File:** `results/All/TQ_corr_noroom_2cats_p1_med_data_ability.csv`
- **Prerequisites:** LMM with random slopes from RQ5.7

**Analysis Specification:**

1. **Load Best Model from RQ5.7**
   - Load saved LMM with random slopes (from "All" analysis)
   - Extract fitted model object for variance decomposition

2. **Extract Variance Components**
   - Extract random effects covariance matrix
   - Compute variance components: var_intercept, var_slope, cov_int_slope
   - Extract residual variance (within-person)

3. **Compute Intraclass Correlation Coefficients (ICC)**
   - **ICC for intercepts:** var_intercept / (var_intercept + var_residual)
   - **ICC for slopes (Method 1):** var_slope / (var_slope + var_residual) [simple ratio]
   - **ICC for slopes (Method 2):** Conditional ICC at Day 6 [accounts for intercept-slope covariance]
   - Interpret magnitude: ICC > 0.40 = substantial, 0.20-0.40 = moderate, < 0.20 = low

4. **Extract Individual Random Effects**
   - Extract person-specific random intercepts and slopes
   - Compute total intercept and slope (fixed + random effects)
   - Generate descriptive statistics for random slopes distribution
   - Save random effects for use in RQ5.14 (clustering analysis)

5. **Visualize Random Slopes Distribution**
   - Generate histogram showing distribution of individual forgetting rates
   - Create Q-Q plot to assess normality assumption
   - Include population mean reference line

6. **Test Intercept-Slope Correlation**
   - Compute correlation between baseline ability and forgetting rate
   - Test significance using t-test
   - Apply Bonferroni correction (α = 0.0033)
   - Interpret direction: negative = high performers maintain advantage (slower forgetting)

**Statistical Justification:**
- **ICC for slopes:** Quantifies trait-like stability of individual differences in forgetting
- **Theoretical importance:** High ICC justifies person-centered clustering (RQ5.14), low ICC suggests forgetting is unstable/noisy
- **Random slopes model:** Necessary to estimate between-person variance in trajectories (not just baselines)
- **Intercept-slope correlation:** Tests if high performers maintain advantage over time (negative r) or regress to mean

**Expected Output:**

1. **Variance Components:**
   ```
   Intercept (baseline):       0.385
   Slope (forgetting rate):    0.052
   Intercept-Slope covariance: -0.018
   Residual (within-person):   0.241
   ```

2. **ICC:**
   ```
   ICC (intercept):               0.615  (62% of baseline variance is between-person)
   ICC (slope, simple):           0.177  (18% of slope variance is between-person)
   ICC (total variance at Day 6): 0.548  (55% of Day 6 variance is between-person)

   Interpretation: Moderate between-person variance in forgetting rate
   ```

3. **Random Slopes Summary:**
   ```
            count  mean      std      min       25%      50%      75%      max
   Total_Slope  100  -0.065   0.082   -0.234   -0.112   -0.061   -0.015   0.098
   ```

4. **Intercept-Slope Correlation:**
   ```
   Correlation: r=-0.234, p=0.0189 (ns after Bonferroni)
   Interpretation: Weak negative trend (higher baseline → slightly slower forgetting)
   ```

5. **Plots:** Histogram shows normal distribution of random slopes; Q-Q plot confirms approximate normality

**Success Criteria:**
- [ ] Variance components extracted successfully
- [ ] ICC values between 0-1 (if not, model misspecification)
- [ ] Random slopes approximately normally distributed (Q-Q check)
- [ ] Intercept-slope correlation computed
- [ ] Interpretation matches ICC magnitude
- [ ] Random effects saved for RQ5.14
- [ ] Replicates

**Reviewer Rebuttals:**

**Q:** "ICC=0.18 for slopes seems low. Does this mean individual differences in forgetting are trivial?"

**A:** "ICC=0.18 means 18% of slope variance is between-person (stable), 82% is within-person (error + true change). This is *moderate* for behavioral data - forgetting is influenced by many unmeasured factors (sleep, stress, interference) causing within-person variability. For comparison, personality trait ICCs are ~0.50-0.70 (more stable), while mood ICCs are ~0.10-0.30 (less stable). Our ICC=0.18 suggests forgetting rate has detectable individual differences, but is not a highly stable trait. This justifies clustering (RQ5.14) to identify subgroups with distinct patterns."

---

**Q:** "Shouldn't you use a different ICC formula for slopes?"

**A:** "There's no consensus ICC formula for random slopes in LMMs. We report: (1) Simple ratio (var_slope / [var_slope + var_residual]) = conservative, assumes residual variance affects slopes equally; (2) Conditional ICC at Day 6 (total between-person variance / total variance) = less conservative, accounts for intercept-slope covariance. Both are valid; we report both for transparency. The simple ICC=0.18 is our primary estimate; Day 6 ICC=0.55 shows that by study end, most variance (55%) is between-person, as slopes accumulate."

---

### RQ5.14: Are there distinct forgetting profiles (fast vs slow forgetters)?

**Research Question:** Can participants be grouped into latent classes based on their forgetting trajectories (intercepts and slopes)?

**Hypothesis:** Exploratory. We may identify 2-3 profiles: (1) High baseline, slow forgetting; (2) Average baseline, average forgetting; (3) Low baseline, fast forgetting. Number of profiles determined by model selection (BIC).

**Data Required:**
- **Analysis Set:** All (single factor)
- **Random effects:** From RQ5.13 (`results/All/RQ5_13_random_slopes.csv`)
- **Clustering variables:** Total_Intercept, Total_Slope

**Analysis Specification:**

1. **Load Random Effects from RQ5.13**
   - Load saved random effects (Total_Intercept, Total_Slope for each UID)
   - Inspect descriptive statistics for clustering variables

2. **Standardize Clustering Variables**
   - Standardize intercepts and slopes to z-scores (mean=0, SD=1)
   - Ensures both dimensions contribute equally to distance metric
   - Different scales otherwise (intercepts ~0.5 range, slopes ~0.1 range)

3. **Determine Optimal Number of Clusters**
   - Test K=1 to K=6 clusters using K-means
   - Compute inertia (within-cluster sum of squares) for each K
   - Compute BIC for model selection: BIC = n*log(RSS/n) + k*log(n)
   - Generate elbow plot (inertia vs K) and BIC plot
   - Select optimal K as BIC minimum (balances fit vs complexity)

4. **Fit Final K-means Model**
   - Fit K-means with optimal K (random_state=42, n_init=50)
   - Extract cluster assignments for each participant
   - Compute cluster centers (unstandardize to original scale for interpretation)
   - Report cluster sizes

5. **Characterize Clusters**
   - Compute summary statistics (mean, SD, min, max) for intercepts and slopes per cluster
   - Assign interpretive labels based on intercept (High/Average/Low baseline) and slope (Fast/Slow forgetting)
   - Example: "High Baseline, Slow Forgetting" vs "Low Baseline, Fast Forgetting"

6. **Visualize Clusters**
   - Generate scatter plot: x-axis = Total_Intercept, y-axis = Total_Slope
   - Color points by cluster membership
   - Overlay cluster centers (large markers)
   - Include reference lines at x=0, y=0
   - Save cluster assignments for potential downstream analyses

**Statistical Justification:**
- **K-means clustering:** Identifies latent profiles based on intercept-slope joint distribution
- **BIC model selection:** Balances fit (fewer clusters = higher inertia) vs complexity (more clusters = overfitting)
- **Standardization:** Ensures intercepts and slopes contribute equally (different scales otherwise)
- **Theoretical value:** Identifies subgroups for targeted interventions; tests if forgetting is categorical or continuous

**Expected Output:**

1. **Cluster Selection:**
   ```
   K=1: Inertia=200.00, BIC=432.1
   K=2: Inertia=134.2, BIC=389.5
   K=3: Inertia=98.7, BIC=375.2  ← Minimum
   K=4: Inertia=82.1, BIC=381.8
   K=5: Inertia=71.3, BIC=392.4
   K=6: Inertia=63.8, BIC=405.1

   *** Optimal K = 3 (BIC minimum) ***
   ```

2. **Cluster Centers:**
   ```
   Cluster 1: Intercept= 0.512, Slope=-0.048  (High Baseline, Slow Forgetting) - n=28
   Cluster 2: Intercept= 0.021, Slope=-0.067  (Average Baseline, Average Forgetting) - n=48
   Cluster 3: Intercept=-0.438, Slope=-0.089  (Low Baseline, Fast Forgetting) - n=24
   ```

3. **Interpretation:** "Three distinct profiles emerged: (1) High performers with resilient memory (n=28), (2) Average performers with typical forgetting (n=48), (3) Low performers with rapid decline (n=24). This supports heterogeneity in forgetting trajectories."

4. **Plot:** Scatter plot showing 3 clusters with distinct centroids, minimal overlap

**Success Criteria:**
- [ ] Elbow and BIC plots generated
- [ ] Optimal K identified (BIC minimum)
- [ ] Final model converged
- [ ] Cluster sizes reasonably balanced (no cluster <10% of sample)
- [ ] Cluster centers interpretable (distinct intercept-slope combinations)
- [ ] Visualization shows clear separation
- [ ] Cluster assignments saved
- [ ] Replicates (K-means uses random initialization, but seed=42 ensures replication)

**Reviewer Rebuttals:**

**Q:** "K-means assumes spherical clusters. Is this appropriate for behavioral data?"

**A:** "K-means is a starting point for exploratory clustering. We chose it for: (1) Simplicity and interpretability, (2) BIC model selection straightforward, (3) Two dimensions only (intercept, slope) - spherical assumption less problematic. Alternative approaches (Gaussian Mixture Models, hierarchical clustering) could be explored in sensitivity analyses. If clusters show clear separation in our plot, K-means is adequate. If overlap is substantial, we'd note limitations and suggest alternatives."

---

**Q:** "How do you know these clusters are real, not just artifacts of K-means forcing a partition?"

**A:** "We use BIC to select K, which penalizes overfitting. If K=1 had lowest BIC, we'd conclude no meaningful clusters exist. Our K=3 selection suggests data support 3 clusters over a single homogeneous group. We also inspect cluster separation visually - well-separated clusters suggest real subgroups, overlapping clusters suggest continuous variation. This is exploratory hypothesis-generation, not confirmatory - future studies could validate profiles in independent samples."

---

### RQ5.15: Does item difficulty interact with time (easier items forgotten faster)?

**Research Question:** Do easier items (lower difficulty) show faster forgetting than harder items, consistent with initial strength predicting decay rate?

**Hypothesis:** Exploratory. Competing predictions: (1) Easier items = weaker encoding → faster forgetting (positive interaction), (2) Easier items = ceiling effects → slower apparent forgetting (negative interaction), (3) No interaction (difficulty affects intercept only).

**Data Required:**
- **Analysis Set:** All by Domain
- **Item parameters:** `results/All by Domain/TQ_corr_noroom_2cats_p1_med_data_difficulty.csv`
- **Response data:** Long-format with item-level responses
- **Software:** pymer4 (for crossed random effects: UID × Item)

**Analysis Specification:**

1. **Load and Merge Data**
   - Load item parameters (difficulty estimates from IRT)
   - Load response data in long format (UID × Test × Days × Item)
   - Merge item difficulty into response-level data
   - Verify data structure (number of observations, unique UIDs, unique items)

2. **Center Predictors**
   - Grand-mean center Difficulty for interpretability (Difficulty_c = Difficulty - mean)
   - Create time variables: Days and log(Days+1)
   - Centered Difficulty allows intercept to represent average item at average difficulty

3. **Fit Cross-Classified LMM**
   - **Formula:** Response ~ Time × Difficulty_c + (Time | UID) + (1 | Item)
   - **Random effects:** Crossed UID (person-specific intercepts/slopes) and Item (item-specific intercepts)
   - **Software:** pymer4 (Python wrapper for R's lme4) - statsmodels doesn't support crossed random effects
   - **Alternative if pymer4 unavailable:** Treat Item as fixed effect (less ideal, loses generalizability)

4. **Extract and Interpret Cross-Level Interaction**
   - Extract Time × Difficulty_c interaction term
   - Test significance using Bonferroni-corrected α = 0.0033
   - **Interpretation:**
     - Positive β: Easier items (lower difficulty) forget slower (ceiling effect)
     - Negative β: Easier items forget faster (weak encoding)
     - Non-significant: Item difficulty affects intercept only, not forgetting rate

5. **Visualize Interaction**
   - Generate predicted trajectories for easy items (-1 SD difficulty) vs hard items (+1 SD difficulty)
   - Plot Days (0, 1, 3, 6) on x-axis, predicted response probability on y-axis
   - Include both trajectories on same plot
   - If interaction significant: trajectories diverge; if non-significant: parallel lines

**Statistical Justification:**
- **Cross-level interaction:** Item-level predictor (difficulty) moderating person-level trajectory (time)
- **Crossed random effects:** Accounts for non-independence (responses nested in both UID and Item)
- **pymer4 required:** statsmodels doesn't support fully crossed random effects; pymer4 wraps lme4 (R)
- **Theoretical relevance:** Tests if initial item strength predicts decay (Jost's law of forgetting)

**Expected Output:**

1. **Cross-Level Interaction:**
   ```
   Time × Difficulty: β=-0.0082, p=0.0421 (ns after Bonferroni α=0.0033)
   Interpretation: Weak trend for easier items to forget faster, but not significant
   ```

2. **Alternative outcome (if significant):**
   ```
   Time × Difficulty: β=0.0123, p=0.0008 ***
   Interpretation: Easier items forget SLOWER (ceiling effect dominates)
   ```

3. **Plot:** Two trajectories (easy vs hard) showing divergence (if interaction significant) or parallelism (if ns)

**Success Criteria:**
- [ ] pymer4 model converged (if not, document alternative approach)
- [ ] Item difficulty successfully merged
- [ ] Difficulty_c correctly centered
- [ ] Cross-level interaction extracted
- [ ] Interpretation matches coefficient sign
- [ ] Plot generated
- [ ] Replicates

**Reviewer Rebuttals:**

**Q:** "Why use pymer4 instead of native Python? This adds a dependency on R."

**A:** "statsmodels (native Python) doesn't support crossed random effects (UID × Item). Options: (1) Use pymer4 (Python wrapper for R's lme4) - cleanest solution, (2) Treat Item as fixed effect - inflates parameters and loses generalizability, (3) Use hierarchical Bayesian model (PyMC3/Stan) - overkill for exploratory analysis. pymer4 is lightweight and widely used. If R unavailable, we document alternative fixed-effects approach and note limitation."

---

**Q:** "Doesn't item difficulty confound encoding and retrieval? How can you isolate forgetting?"

**A:** "Item difficulty (from IRT) reflects *average* endorsement probability across the sample and time points. The Difficulty × Time interaction tests if difficulty *slope* (change over time) varies by difficulty level. If difficult items just have lower intercepts (encoding), we'd see a main effect of Difficulty, not an interaction. The interaction specifically tests if forgetting rate (slope) depends on initial difficulty - addressing the confound you raise. We acknowledge that 'difficulty' could reflect encoding, storage, or retrieval; our design can't isolate these."

---

**END OF CHAPTER 5**
