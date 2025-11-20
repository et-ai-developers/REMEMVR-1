# Chapter 1: INTRODUCTION

Description:

This chapter establishes the theoretical and empirical foundation for why REMEMVR is needed. It reviews:
- Episodic memory definition using a functional/constructivist framework
- Neuroanatomical substrates (hippocampal network: CA1, CA3, dentate gyrus, entorhinal cortex, place cells, grid cells)
- Cognitive processes (encoding, consolidation via sleep, retrieval/reconstruction)
- Theoretical frameworks critically evaluated:
- Process-Based Memory Framework (PMAT)
- Multiple Trace Theory (MTT) vs Standard Consolidation Theory
- Scene Construction Theory (Hassabis & Maguire)
- Contextual Binding Theory
- Measurement paradox: Existing tools achieve ecological validity OR experimental control, but not both
- The REMEMVR solution: How VR resolves this historical forced choice

Questions:

1. Which theoretical framework do you ultimately argue for? Or do you propose a synthesis/new model?
-   Proving/disproving any specific model is beyond the scope of this thesis. Once we have our results, we will know which frameworks agree/disagree with the results which we can put into the discussion.
2. What's your position on the consolidation debate? (MTT vs SCT - do hippocampal traces fade or persist?)
-   No idea. Both make strong arguments that are hard to debunk without solid emirical evidence. It would be cool if our results could imply if one or the other looks more correct.
3. Do you introduce what/where/when as distinct cognitive systems here? Or just as a heuristic?
-   They are a heuristic. I prefer data driven understandings of the brain so I just picked simple labels we know are separate based on fMRI data, but I deliberately avoid trying to argue things like semantic and episodic memory are mutually exclusive mechanisms, or autobiographical memory is different to episodic memory. I find these arguments are more philosophical than scientific. It makes no sense to persist using cognitive topography that was developed 50+ years ago out of linguistic convenience rather than factual science.
4. What gaps in the literature does REMEMVR specifically address? (Beyond just "we need better tests")
-   It addresses the face/ecological validity issues inherent in standard episodic memory tests. We use these standard test results to make important clinical/research decisions and it is critical that we discover how reliable these results actually are. Furthermore it explores the role of confidence/strategy in episodic memory. I argue this in terms of utility. Standard tests don't care if a correct answer is a guess or if one person is completeing the task using a totally different strategy. Confidence is essential when we actually use our episodic memory for decision making. Also since I collected data across a stratefied range of ages, I can look at how different trends in ability change over the lifespan.
5. Do you review other VR memory studies? What makes REMEMVR different/better?
-   I plan on writing this up into the thesis but haven't yet. The main difference between REMEMVR and other VR memory tests is REMEMVR is specifically designed to measure multi-day EPISODIC memory accuracy and confidence, whereas other tests focus on 'every-day memory' or only measure single time-point accuracy, and none measure confidence or strategy.

---
# Chapter 2: METHOD

Description:

A concise but comprehensive protocol overview providing readers with the operational details needed to understand subsequent analyses:
- Participants: N=100, aged 20-70, stratified recruitment, exclusion criteria
- VR apparatus: Oculus Quest Pro, hand tracking, 1:1 locomotion, room design rules
- Encoding procedure: 4 rooms × 10 min, scripted interactions, 6 items + 7 observations per room
- Testing schedule: Day 0/1/3/6, Latin square counterbalancing
- Test structure: 8 sections per test (Sleep → RFR → IFR → TCR → ICR → RRE → IRE → Strategy)
- Scoring: Dichotomous (0/1) for object identity, partial credit (0.5) for adjacent spatial/temporal responses
- Cognitive battery: RAVLT, BVMT-R, NART, RPM administration and scoring
- Confidence ratings: 5-star Likert (1=Guess, 5=Certain), rescaled to 0-1, bias-corrected

Questions:

1. Do you include a participant flow diagram? (Consort-style: recruited → excluded → analyzed)
-   No. I could add one later on if it will help the reader understand the methodology.
2. What's your final position on partial credit? (You abandoned 3-category for temporal, but kept 0.5 for spatial?)
-   I originally assigned partial credit, but it's just too problematic and ripe for a reviewer to raise concerns. Unless I can find a simple, fair, valid, and reliable way to improve the resolution of the data by using partial credit, I will stick with dichotomous right/wrong scoring for accuracy.
3. Do you report inter-rater reliability for free-text scoring? (You + research assistant)
-   I have collected that data. I have over 1800 datapoints collected for each participant. One of those is who collected the data, me or the assistant.
4. What was the compliance rate for remote tests? (Day 1/3/6)
-   Some people didn't complete tests 3 and 6 actually ON days 3 and 6. Sometimes their tests were delayed by a day or two. During data collection, anyone who gave bad answers (i.e., I don't know) for a large portion of a test, was removed and replaced with a new candidate. Also if anyone didn't complete all 4 tests, they were removed as participants and their slot was re-recruited. So I have 100 participants that completed 4 tests each.

---
# Chapter 3: RATIONALE

Description:

A detailed justification for every design decision, demonstrating that REMEMVR's development was systematic and theory-driven:
- Why household rooms? (Familiarity, feasibility, cross-cultural applicability)
- Why 6 items not 8? (Pilot testing showed floor effects with 8)
- Why congruent/incongruent/common categories? (Tests schema theory predictions)
- Why 3 paradigms? (Different retrieval processes: generative vs familiarity-based)
- Why logarithmic delay spacing? (0, 1, 3, 6 days approximates Ebbinghaus curve)
- Why confidence ratings? (Metacognition, distinguishing lucky guesses from genuine recall)
- Why incidental encoding? (Prevents strategy confounds)
- Why this specific counterbalancing? (Controls for order/fatigue without cross-test contamination)
- Design constraints acknowledged: No tactile feedback, cultural generalizability limits, English-only

Questions:

1. Do you discuss why you DIDN'T include certain domains? (Affect, attention, source memory)
-   Affect is too subjective to include as a standardised metric. Attention WAS controlled by asking participants to describe each task they were doing out-loud. I don't know what you mean about source memory.
2. What's your justification for the specific discrimination thresholds (0.5-4.0)? Empirical or conventional?
-   That was based on several past papers that have used IRT for analysis. (To be referenced later)
3. Do you defend the Composite_ID stacking approach? (Assuming time-invariant item parameters)
-   Not specifically but I intend to. It is a necessary compromise that technically breaks the assumption of independence between participants, but allows for the model to be MUCH more stable. A proper longitudinal, multidimensional IRT requires thousands of participants and responses. So I believe this assumption violation is worth it.
4. Why NOT use adaptive testing? (CAT would be more efficient)
-   This was something I would have liked to have done, but since I am a team of one, with minimal computer experience, I didn't have the time or resources to write code that would create bespoke tests for individuals based on their ability. Computerised adaptive testing is definitely where future iterations of REMEMVR should go, but it wasn't realistically achievable for this PhD project.

---
# Chapter 4: ANALYSIS

Expanded Description:

This chapter explains the two-stage psychometric analysis pipeline and why it's superior to traditional approaches. Likely includes:
- Stage 1: Measurement Model (IRT)
- Why GRM over Rasch/2PL/3PL models
- Confirmatory factor analysis via Q-matrix
- deepirtools IWAVE (variational autoencoder) rationale
- Handling missingness (sparse matrices, MAR assumption)
- Iterative item purification procedure (discrimination filtering)
- IRT assumptions and diagnostic checks
- Stage 2: Longitudinal Model (LMM)
- Why LMM over repeated-measures ANOVA
- Random intercepts + random slopes specification
- Time coding (Days, Days², log(Days+1))
- Model selection via AIC vs BIC vs theory
- Assumption checking (residual normality, homoscedasticity)
- CTT vs IRT Comparison
- When conclusions differ
- Measurement precision advantages
- Handling Conditional Dependencies
- The what→where→when cuing problem
- Why frequentist methods are insufficient
- Preview of Bayesian approach (if used)

Questions:

1. Do you formalize the conditional dependency problem mathematically? P(Where|What, When)?
-   I originally wanted to create a bayseian conditional probability network using graph theory but this is FAR beyond my mathematical ability.
2. What IRT fit indices do you report? (RMSEA, CFI, TLI, test information curves?)
-   None. I don't know what those are. Should I include them? Which one should I pick?
3. Do you test for differential item functioning (DIF)? By age, sex, room?
-   No. Should I?
4. How do you justify the "correlated vs uncorrelated factors" comparison? Theory or data-driven?
-   This was theoretical. So far I have run analyses using both, but theoretically, remembering what something is must surely be correlated to remembering where it was. I would be uncomfortable stating those abilities are NOT correlated.
5. Do you discuss measurement invariance across time? (Are Day 0 and Day 6 on the same scale?)
-   All tests are on the same scale. All tests are basically identical except the room in questions and the contents of that room.
6. What's your Monte Carlo sample size (mc_samples)? How did you validate convergence?
-   In the IRT model_fit I used mc_samples = 1. I seem to recall that being because Monte Carlo is irrelevant at this step but I can't recall why. Then in the model_scores I used mc_samples = 100. This was an arbitary decision and I'm not sure how to properly explain it yet.
7. Do you use any shrinkage/regularization? Or full Bayesian priors?
-   I use the results from a standard IRT as priors that then get entered into the bayesian IRT. I'm not sure if this is the best approach.
8. How do you handle the multiple comparisons problem? (9 analysis sets × multiple models)
-   I haven't handled that at all yet. I guess I need some kind of bonferonni correction applied but I am yet to do that.

---
# Chapter 5: THE TRAJECTORY OF EPISODIC FORGETTING

Description:

The first empirical chapter establishes the basic forgetting patterns before introducing metacognition or individual differences. Systematically examines how accuracy (TQ scores) changes over time.

Research Questions:

Domain-Specific Forgetting:

1. Do What, Where, and When domains exhibit different forgetting trajectories?
- Hypothesis: Object identity (What) may be more resilient than spatial (Where) or temporal (When) memory
- Analysis: 3-factor LMM (What vs Where vs When) with Domain × Time interaction
2. Is there evidence for differential consolidation across domains?
- Hypothesis: Sleep-dependent consolidation (Day 0→1) may benefit spatial memory more than semantic
- Analysis: Compare Day 0→1 slope vs Day 1→6 slope by domain

Paradigm-Specific Forgetting:

3. Do Free Recall, Cued Recall, and Recognition show different forgetting rates?
- Hypothesis: Recognition should be more resilient (familiarity-based) than free recall (generative)
- Analysis: 3-factor LMM with Paradigm × Time interaction
4. Does retrieval support buffer against forgetting?
- Hypothesis: Cued recall falls between free recall and recognition
- Analysis: Planned contrasts on slopes (FR > CR > RE)

Semantic Context Effects:

5. Does semantic congruence affect forgetting trajectories?
- Hypothesis: Incongruent items (schema-violating) may be more memorable initially but decay faster
- Analysis: 3-factor LMM (Common vs Congruent vs Incongruent) with Congruence × Time interaction
6. Do congruent items show consolidation benefits?
- Hypothesis: Schema-consistent items integrate better during sleep consolidation
- Analysis: Test for Congruence × Time-segment interaction (early vs late forgetting)

Functional Form of Forgetting:

7. What mathematical function best describes episodic forgetting curves?
- Hypothesis: Logarithmic (classic Ebbinghaus) vs power law vs exponential
- Analysis: AIC comparison across 5 LMM models (Linear, Quadratic, Log, Lin+Log, Quad+Log)
8. Is there evidence for two-phase forgetting? (Fast initial decay + stable plateau)
- Hypothesis: Quadratic or piecewise models may fit better than simple exponential
- Analysis: Compare linear vs quadratic time terms

Age Effects:

9. Do older adults show steeper forgetting trajectories than younger adults?
- Hypothesis: Age affects consolidation/storage, not just encoding
- Analysis: Age × Time interaction in LMM (continuous age or age groups)
10. Is there an age × domain interaction?
- Hypothesis: Older adults may show disproportionate spatial (Where) deficits
- Analysis: 3-way interaction (Age × Domain × Time)

IRT vs CTT:

11. Does using IRT theta scores change substantive conclusions about forgetting?
- Hypothesis: CTT sum-scores may mask domain differences due to measurement error
- Analysis: Compare LMM results using CTT means vs IRT thetas
12. Do poorly discriminating items drive CTT results?
- Hypothesis: After removing low-discrimination items, CTT and IRT should converge
- Analysis: Compare pre- vs post-purification CTT results

Individual Differences (Random Effects):

13. How much variance in forgetting rate is between-person vs within-person?
- Analysis: ICC from random slopes model
14. Are there distinct forgetting profiles? (Fast forgetters vs slow forgetters)
- Analysis: Growth mixture modeling or latent class analysis (if sample size permits)

Item-Level Predictors:

15. Do items with higher IRT difficulty forget faster?
- Hypothesis: Difficult items may be more fragile
- Analysis: Difficulty × Time interaction (cross-level in multilevel model)

Questions:

1. Do you analyze all 9 analysis sets or focus on a subset? (All, by Domain, by Paradigm, etc.)
-   So far I have analysed 10 subsets but I probably need to look at more subsets for specific research questions.
2. How do you present the results? One big table, separate sections per RQ, or analysis set-by-set?
-   These will be heading by heading with figures per RQ.
3. Do you use effect sizes? (Cohen's d for time effects, R² for variance explained)
-   Not yet but I should.
4. What's your α-level after corrections? Bonferroni, FDR, or no correction?
-   I haven't done corrections yet and I need to.
5. Do you report both correlated and uncorrelated factor models? Which is primary?
-   Unsure. What do you suggest?
6. Do you include room-specific analyses (specify_room=True)? Or just general?
-   I ran an initial room-specific analysis to check if rooms are equally difficult which I believe they are. But after that, I don't specify room. I should do more room-specific analyses when looking at interactive item memory so I can look at how memory for specific objects changes over time.
7. What do you do with the p2_high iteration results? (Currently missing files)
-   I don't recall.

---
# Chapter 6: METACOGNITION IN EPISODIC MEMORY

Description:

The second empirical chapter introduces confidence (TC scores) to examine the relationship between subjective and objective memory. Tests whether people know what they know, and whether metacognitive accuracy changes over time.

Research Questions:

Confidence Trajectories:

1. Does confidence decline in parallel with accuracy over time?
- Hypothesis: Metacognitive monitoring tracks actual forgetting
- Analysis: Compare slope(Confidence) vs slope(Accuracy) within-subjects
2. Is there a dissociation between confidence and accuracy trajectories?
- Hypothesis: Confidence may decline slower (overconfidence) or faster (underconfidence) than accuracy
- Analysis: Confidence ~ Time vs Accuracy ~ Time, test slope difference

Metacognitive Calibration:

3. Are participants well-calibrated at Day 0 but miscalibrated at Day 6?
- Hypothesis: Metacognitive monitoring degrades with memory trace strength
- Analysis: Calibration curves (confidence vs accuracy bins) at each time point
4. Does metacognitive resolution (discrimination) decline over time?
- Hypothesis: Ability to distinguish correct from incorrect answers worsens
- Analysis: Gamma correlation or AUROC at each time point
5. What is the trajectory of utility (metacognitive accuracy)?
- Hypothesis: Utility = |Accuracy - Confidence| increases over time (worse calibration)
- Analysis: LMM with Utility ~ Time (using your inverted utility metric)

Domain & Paradigm Differences:

6. Is metacognitive accuracy better for some domains than others?
- Hypothesis: People may be better calibrated for What (semantic) than Where (spatial) or When (temporal)
- Analysis: Domain × Time interaction on utility scores
7. Does paradigm affect confidence-accuracy relationship?
- Hypothesis: Recognition should show better metacognition (familiarity signals are clearer)
- Analysis: Paradigm × Time interaction on gamma correlation

High-Confidence Errors (False Memories):

8. Do high-confidence errors increase over time?
- Hypothesis: As traces fade, people reconstruct plausible but false memories with high confidence
- Analysis: Proportion of (Incorrect & Confidence≥4) responses across time
9. Are incongruent items more susceptible to high-confidence errors?
- Hypothesis: Schema-violating items may be reconstructed as schema-consistent errors
- Analysis: Congruence × Accuracy × Confidence interaction

Predictive Validity:

10. Does Day 0 confidence predict subsequent forgetting?
- Hypothesis: Low-confidence correct answers at Day 0 are more likely to be forgotten by Day 6
- Analysis: Logistic regression (Day 6 accuracy ~ Day 0 confidence | Day 0 correct)
11. Does confidence variability predict memory stability?
- Hypothesis: Consistent high confidence indicates stable memory traces
- Analysis: Within-person SD(confidence) predicts slope variance

Age & Individual Differences:

12. Do older adults show worse metacognitive accuracy?
- Hypothesis: Aging affects metamemory monitoring
- Analysis: Age × Time interaction on utility/calibration
13. Is metacognitive accuracy related to overall memory ability?
- Hypothesis: Good rememberers are also good monitors
- Analysis: Correlation between mean theta score and mean utility score

Confidence-Weighted Performance:

14. Does weighting accuracy by confidence improve trajectory estimates?
- Hypothesis: Confidence-weighted scores may better reflect "usable" memory
- Analysis: Compare LMM using raw accuracy vs confidence-weighted accuracy
15. Can we decompose forgetting into "forgotten but guessed correctly" vs "genuinely remembered"?
- Analysis: 2×2 contingency (Accuracy × Confidence dichotomized) across time

Questions:

1. Which metacognitive framework do you adopt? Nelson & Narens (1990)? Fleming & Lau?
-   None so-far. What do you suggest?
2. How do you operationalize "good" vs "bad" metacognition formally? Gamma, calibration, resolution?
-   I am just assuming that 1:1 accuracy:metacognition is good. But I have no formal operationalisation yet. Should I have one?
3. Do you model confidence and accuracy jointly (multivariate LMM) or separately?
-   I have modelled them jointly in some analyses.
4. How did you handle confidence bias correction? Z-scores within-person? Described in Chapter 4?
-   I haven't corrected any confidence ratings (likert response bias). I want to but I am concerned the more corrections I apply to it, the less interpretable the results become.
5. Do you analyze TC_ (confidence) data through IRT too? Or just as raw Likert?
-   I have computed TC_ as a 0-1 score just by re-ranging the values. So they are basically raw likert but now instead of 1, 2, 3, 4, 5 it is 0, 0.25, 0.5, 0.75, 1.0
6. What's the theoretical prediction for utility? Should it be 0 (perfect calibration)?
-   I guess so? But I have nothing from the literature that says that should be the case. For example, I am noticing that confidence drops lower than accuracy (contrary to some literature), and I interpret this as a possible 'hedging' or erring on the side of caution, which could be the ideal behaviour and so it shouldn't be 1:1. This is an exploratory concept that I just thought of adding recently.
7. Do you test whether metacognition mediates age effects on memory? Age → Metacognition → Performance?
-   I haven't tested for the effects of correlates like age, sex, education yet but I want to.

---
# Chapter 7: UNPACKING INDIVIDUAL DIFFERENCES IN EPISODIC MEMORY ABILITY

Description:

The third and final empirical chapter addresses the central thesis question: How well do standard neuropsychological tests predict real-world episodic memory performance as measured by REMEMVR? This chapter integrates the RAVLT, BVMT-R, NART, and RPM data with REMEMVR outcomes.

Research Questions:

Predictive Validity of Standard Tests:

1. Do standard cognitive tests predict REMEMVR performance?
- Hypothesis: Tests should predict Day 0 ability but may not predict forgetting rate
- Analysis: RAVLT/BVMT/NART/RPM predicting REMEMVR theta scores
2. Which cognitive test best predicts which REMEMVR domain?
- Hypothesis: RAVLT (verbal) → What, BVMT (visuospatial) → Where, neither → When
- Analysis: Domain-specific theta ~ RAVLT + BVMT + NART + RPM
3. Do cognitive tests predict initial ability (intercept) vs forgetting rate (slope)?
- Hypothesis: Tests predict encoding capacity but not consolidation efficiency
- Analysis: Extract random intercepts & slopes from LMM, regress on cognitive scores
4. Is there unique variance in REMEMVR not explained by standard tests?
- Hypothesis: REMEMVR taps ecological episodic memory beyond what pen-and-paper tests capture
- Analysis: R² comparison, residual variance analysis

Domain Specificity:

5. Does RAVLT predict Free Recall better than Recognition?
- Hypothesis: Both are generative retrieval tasks
- Analysis: RAVLT × Paradigm interaction
6. Does BVMT predict spatial (Where) more than temporal (When)?
- Hypothesis: BVMT is visuospatial, not temporal
- Analysis: BVMT × Domain interaction
7. Does RPM (fluid intelligence) predict complex integration (What+Where+When)?
- Hypothesis: Relational binding requires fluid reasoning
- Analysis: RPM predicting multi-domain composite scores

Age as Moderator:

8. Does age explain variance beyond cognitive test scores?
- Hypothesis: Age has direct effects on consolidation not mediated by test performance
- Analysis: Hierarchical regression (Step 1: Age, Step 2: +Cognitive tests)
9. Do cognitive tests attenuate age effects on REMEMVR?
- Hypothesis: Age effects are mediated by cognitive ability
- Analysis: Mediation model (Age → RAVLT/BVMT → REMEMVR)
10. Is there an age × cognitive test interaction?
- Hypothesis: Tests may be better predictors in older adults (floor effects in young)
- Analysis: Age × RAVLT interaction term

Self-Reported & Contextual Factors:

11. Do self-reported factors predict performance?
- Sleep quality, VR experience, education level, typical sleep duration
- Analysis: Multiple regression including self-report variables
12. Does DASS (depression/anxiety/stress) predict memory or metacognition?
- Hypothesis: Anxiety may impair metacognitive accuracy more than memory itself
- Analysis: DASS subscales predicting theta vs utility scores
13. Do memory strategies (self-reported) correlate with performance?
- From strategy questionnaire: method of loci, visualization, narrative
- Analysis: Strategy use predicting intercept/slope

Latent Profile Analysis:

14. Are there distinct memory profiles? ("Visualizers" vs "verbalizers", "generalists" vs "specialists")
- Hypothesis: People differ qualitatively in how they encode/retrieve
- Analysis: Latent profile analysis on What/Where/When theta scores
15. Do cognitive test profiles predict REMEMVR profiles?
- Hypothesis: RAVLT-dominant individuals → What-dominant REMEMVR
- Analysis: Profile correspondence analysis

Building a Predictive Model:

16. Can we build a parsimonious model to predict real-world episodic memory from standard tests?
- Analysis: Stepwise regression, cross-validation
- Output: Clinical prediction tool
17. What proportion of REMEMVR variance is "unexplained"?
- Hypothesis: Ecological memory has substantial unique variance
- Analysis: R² upper bound
18. Do multivariate models outperform univariate models?
- Hypothesis: REMEMVR is multidimensional, requiring multivariate predictors
- Analysis: Canonical correlation or PLS

Reverse Inference:

19. Can REMEMVR performance predict performance on standard tests?
- Hypothesis: If REMEMVR is a "purer" episodic measure, it should predict test performance
- Analysis: REMEMVR → RAVLT/BVMT regression (reverse model)
20. Do different REMEMVR paradigms predict different tests?
- Hypothesis: REMEMVR Recognition → BVMT Recognition (both familiarity-based)
- Analysis: Paradigm-specific cross-test correlations

Questions:

1. Do you use factor analysis/PCA to reduce cognitive test dimensionality? Or keep them separate?
-   I haven't done any of these analyses yet.
2. What's your plan for handling multiple DVs from REMEMVR? (Separate models for each factor? Multivariate? Composite?)
-   Unsure. What do you suggest?
3. Do you use structural equation modeling (SEM)? Or hierarchical regression?
-   No idea what SEM is. I guess I was thinking of using hierarchical regression but am yet to understand how to achieve this in Python.
4. How do you handle the NART? (It's premorbid IQ, not current ability - different construct)
-   The NART results are a bit bunk as many particiapnts didn't have english as their primary langauage and I (foolishly) didn't record what langauges participants predominantly spoke.
5. Do you test directionality? (Mediation requires temporal precedence - cognitive tests were Day 0)
-   No. I don't really understand this question.
6. Do you include VR-specific variables? (e.g., simulator sickness, hand tracking accuracy)
-   Not yet. Nobody got VR sickness. I asked participants how much previous experience they have with VR and recorded how many seconds it took them to complete each task in each room in VR
7. What's your sample size for subgroup analyses? (n=10 per age band - might be underpowered for interactions)
-   I haven't decided this but you're right that n=10 is underpowered. We could consolidate age groups to increase n. I.e., Split the sample into 5 groups. (Ages 20-30, 30-40 etc n=20) or in half (Ages 20-45, 45-70 n=50)
8. Do you validate your predictive model? Cross-validation, hold-out sample, or just in-sample R²?
-   Not sure. What do you suggest?

---
# Chapter 8: DISCUSSION

Description:

This chapter synthesizes findings across all empirical chapters, interprets them within the broader theoretical landscape, and discusses implications for episodic memory theory, clinical assessment, and translational neuroscience.

Likely includes:
- Summary of key findings from Chapters 5, 6, 7
- Theoretical implications: Which frameworks are supported? (Scene Construction Theory? Contextual Binding?)
- Methodological contributions: REMEMVR as a new gold-standard tool
- IRT + LMM advantages: What did this approach reveal that CTT couldn't?
- Clinical utility: Can REMEMVR detect early Alzheimer's? Differentiate memory disorders?
- Ecological validity achieved: Did we actually measure "real" episodic memory?
- Limitations acknowledged:
- Sample size (n=100 adequate for IRT but marginal for complex interactions)
- Cultural generalizability (Western household rooms)
- VR limitations (no tactile feedback, visual resolution)
- Single encoding session (no practice effects studied)
- Future directions:
- Normative data collection across lifespan
- Clinical validation (MCI, AD, frontal amnesia cohorts)
- Longitudinal follow-up (do forgetting slopes predict future decline?)
- Modular room packs for cross-cultural use
- Integration with neuroimaging (fMRI during VR encoding)
- Intervention studies (rTMS, cognitive training)
- Translational vision: REMEMVR as standard assessment in memory clinics

Questions:

1. Do you propose clinical cutoffs? (e.g., "2 SD below mean theta = impaired"?)
-   Unsure.
2. What's your position on whether REMEMVR should replace existing tests? Complement or supplant?
-   It is currently impractical to replace current tests. I think the results of REMEMVR should be used to see if there are better ways to score/interpret current tests. Maybe a future version of REMEMVR could be more appropriate for clinical use.
3. Do you discuss cost-benefit? (VR setup expensive vs pen-and-paper tests cheap)
-   The VR setup isn't expensive. Oculus headsets are cheap. Making the wrong clinical decision can be very costly, financially and healthwise.
4. How do you frame "null" results? (e.g., if congruence doesn't matter, is that interesting?)
-   It depends if we have the statistical power to say they probably really are null. Lets cross that bridge when we know our full results.
5. Do you propose a specific theoretical model? Or remain framework-agnostic?
-   I prefer to be framework agnostic. This thesis didn't set out to prove/disprove any specific theory. It's more of an exploratory work that I intend to expand upon as a post-doc.
6. What's the "so what" for non-academics? Clinical, educational, or policy implications?
-    Good question. Lets keep pondering that as we go along.
7. Do you discuss the replication crisis? Preregistration, open data, reproducibility?
-   No. Do you think it's relevant? The reason I used VR is so others could replicate this exact methodology. I loathe experiments that are extremely difficult to recreate in the lab.
8. What's your elevator pitch? If I had 30 seconds to explain REMEMVR's contribution, what is it?
-   Good question. Lets figure that out as we go.

---
# Overall Questions About the Thesis:

1. What's the binding narrative thread? Is it "REMEMVR as a tool" or "episodic memory findings enabled by REMEMVR"?
-   I initially developed it as a tool but for the purposes of getting a PhD, it needs to be the latter.
2. How long is each empirical chapter? Are they balanced or is one much larger?
-   They should be balanced. They are not written yet.
3. Do you use the same participants for all analyses? Or exclude some for certain chapters?
-   I include ALL participants in all analyses (except in cases where we are looking at specific age ranges)
4. What's your theory of episodic forgetting? Active decay, interference, retrieval failure, or trace transformation?
-   No idea. Lets see what the data tells us.
5. Do you have preregistered hypotheses? Or is this exploratory given the tool is new?
-   This is exploratory. I didn't pre-register anything.
6. What's your plan for publications? Chapter 5→Paper 1, Chapter 6→Paper 2, etc.?
-   Lets discuss publishing papers after I have submitted the thesis haha!
7. Is there a unifying finding you hope to demonstrate? (e.g., "ecological episodic memory is multi-dimensional and poorly captured by current tests")
-   Yes. Basically traditional pen-paper tests aren't actually measuring episodic memory as we understand/use it in everyday life. This doesn't render those tests as obselete, but we need tools like REMEMVR to better understand these traditinoal test results. Or maybe we can develop a VR test that is practical for the clinic and than can indeed render old tests obselete.




# REVISED LIST
Chapter 5: The Trajectory of Episodic Forgetting
    
    Domain-Specific Forgetting:
1. Do What, Where, and When domains show different forgetting trajectories? [DONE]
    - Hypothesis: What may be more resilient than Where or temporal When
    - Analysis: IRT > 3-factor LMM (What vs Where vs When) with Domain * Time interaction
2. Is there evidence for differential consolidation across domains? [AI]
    - Hypothesis: Sleep-dependent consolidation (Day 0 > 1) may benefit spatial memory more than semantic
    - Analysis: Compare Day 0 > 1 slope vs Day 1 > 6 slope by domain

Paradigm-Specific Forgetting:
3. Do Free Recall, Cued Recall, and Recognition show different forgetting rates? [DONE]
    - Hypothesis: Recognition should be more resilient (familiarity) than free recall (generative)
    - Analysis: IRT > 3-factor LMM with Paradigm * Time interaction
4. Does retrieval support buffer against forgetting? [DONE]
    - Hypothesis: Cued recall falls between free recall and recognition
    - Analysis: Contrast on slopes (FR > CR > RE)

Semantic Context Effects:
5. Does semantic congruence affect forgetting trajectories? [DONE]
    - Hypothesis: Incongruent items may be more memorable initially but decay faster
    - Analysis: IRT > 3-factor LMM (Common vs Congruent vs Incongruent) with Congruence * Time interaction
6. Do congruent items show consolidation benefits? [AI]
    - Hypothesis: Schema-consistent items integrate better during sleep consolidation
    - Analysis: Test for Congruence * Time-segment interaction (early vs late forgetting)

Functional Form of Forgetting:
7. What mathematical function best describes episodic forgetting curves? [DONE]
    - Hypothesis: Logarithmic (classic Ebbinghaus) vs power law vs exponential
    - Analysis: AIC comparison across 5 LMM models (Linear, Quadratic, Log, Lin+Log, Quad+Log)
8. Is there evidence for two-phase forgetting? (Fast initial decay + stable plateau) [AI]
    - Hypothesis: Quadratic or piecewise models may fit better than simple exponential
    - Analysis: Compare linear vs quadratic time terms

Age Effects:
9. Do older adults show steeper forgetting trajectories than younger adults? [TO DO]
    - Hypothesis: Age affects consolidation/storage, not just encoding
    - Analysis: Age * Time interaction in LMM (continuous age or age groups)
10. Is there an age * domain interaction? [TO DO]
    - Hypothesis: Older adults may show disproportionate spatial (Where) deficits
    - Analysis: 3-way interaction (Age * Domain * Time)

IRT vs CTT:
11. Does using IRT theta scores change substantive conclusions about forgetting? [DONE]
    - Hypothesis: CTT sum-scores may mask domain differences due to measurement error
    - Analysis: Compare LMM results using CTT means vs IRT thetas
12. Do poorly discriminating items drive CTT results? [AI]
    - Hypothesis: After removing low-discrimination items, CTT and IRT should converge
    - Analysis: Compare pre- vs post-purification CTT results

Individual Differences:
13. How much variance in forgetting rate is between-person vs within-person? [TO DO]
    - Analysis: ICC from random slopes model

Item-Level Predictors:
14. Do items with higher IRT difficulty forget faster? [AI]
    - Hypothesis: Difficult items may be more fragile
    - Analysis: Difficulty * Time interaction (cross-level in multilevel model)

Chapter 6: Metacognition in Episodic Memory

    Confidence Trajectories:
1. Does confidence decline in parallel with accuracy over time? [DONE]
    - Hypothesis: Metacognitive monitoring tracks actual forgetting
    - Analysis: Compare slope(Confidence) vs slope(Accuracy) within-subjects
2. Is there a dissociation between confidence and accuracy trajectories? [DONE]
    - Hypothesis: Confidence may decline slower (overconfidence) or faster (underconfidence) than accuracy
    - Analysis: Confidence ~ Time vs Accuracy ~ Time, test slope difference

Metacognitive Calibration:
3. Are participants well-calibrated at Day 0 but miscalibrated at Day 6? [TO DO]
- Hypothesis: Metacognitive monitoring degrades with memory trace strength
- Analysis: Calibration curves (confidence vs accuracy bins) at each time point
4. Does metacognitive resolution (discrimination) decline over time? [AI]
- Hypothesis: Ability to distinguish correct from incorrect answers worsens
- Analysis: Gamma correlation or AUROC at each time point
5. What is the trajectory of utility (metacognitive accuracy)? [DONE]
- Hypothesis: Utility = |Accuracy - Confidence| increases over time (worse calibration)
- Analysis: LMM with Utility ~ Time (using your inverted utility metric)

Domain & Paradigm Differences:
6. Is metacognitive accuracy better for some domains than others? [TO DO]
- Hypothesis: People may be better calibrated for What (semantic) than Where (spatial) or When (temporal)
- Analysis: Domain * Time interaction on utility scores
7. Does paradigm affect confidence-accuracy relationship? [TO DO]
- Hypothesis: Recognition should show better metacognition (familiarity signals are clearer)
- Analysis: Paradigm * Time interaction on gamma correlation

High-Confidence Errors (False Memories):
8. Do high-confidence errors increase over time? [AI]
- Hypothesis: As traces fade, people reconstruct plausible but false memories with high confidence
- Analysis: Proportion of (Incorrect & Confidence≥4) responses across time
9. Are incongruent items more susceptible to high-confidence errors? [AI]
- Hypothesis: Schema-violating items may be reconstructed as schema-consistent errors
- Analysis: Congruence * Accuracy * Confidence interaction

Predictive Validity:
10. Does Day 0 confidence predict subsequent forgetting? [TO DO]
- Hypothesis: Low-confidence correct answers at Day 0 are more likely to be forgotten by Day 6
- Analysis: Logistic regression (Day 6 accuracy ~ Day 0 confidence | Day 0 correct)
11. Does confidence variability predict memory stability? [AI]
- Hypothesis: Consistent high confidence indicates stable memory traces
- Analysis: Within-person SD(confidence) predicts slope variance

Age & Individual Differences:
12. Do older adults show worse metacognitive accuracy? [TO DO]
- Hypothesis: Aging affects metamemory monitoring
- Analysis: Age * Time interaction on utility/calibration
13. Is metacognitive accuracy related to overall memory ability? [TO DO]
- Hypothesis: Good rememberers are also good monitors
- Analysis: Correlation between mean theta score and mean utility score

Confidence-Weighted Performance:
14. Does weighting accuracy by confidence improve trajectory estimates? [AI]
- Hypothesis: Confidence-weighted scores may better reflect "usable" memory
- Analysis: Compare LMM using raw accuracy vs confidence-weighted accuracy
15. Can we decompose forgetting into "forgotten but guessed correctly" vs "genuinely remembered"? [TO DO]
- Analysis: 2*2 contingency (Accuracy * Confidence dichotomized) across time

Chapter 7: Individual Differences in Episodic Memory

Predictive Validity of Standard Tests:
1. Do standard cognitive tests predict REMEMVR performance? [DONE FOR CTT]
- Hypothesis: Tests should predict Day 0 ability but may not predict forgetting rate
- Analysis: RAVLT/BVMT/NART/RPM predicting REMEMVR theta scores
2. Which cognitive test best predicts which REMEMVR domain? [DONE FOR CTT]
- Hypothesis: RAVLT (verbal) → What, BVMT (visuospatial) → Where, neither → When
- Analysis: Domain-specific theta ~ RAVLT + BVMT + NART + RPM
3. Do cognitive tests predict initial ability (intercept) vs forgetting rate (slope)? [DONE FOR CTT]
- Hypothesis: Tests predict encoding capacity but not consolidation efficiency
- Analysis: Extract random intercepts & slopes from LMM, regress on cognitive scores
4. Is there unique variance in REMEMVR not explained by standard tests? [DONE FOR CTT]
- Hypothesis: REMEMVR taps ecological episodic memory beyond what pen-and-paper tests capture
- Analysis: R² comparison, residual variance analysis

Domain Specificity:
5. Does RAVLT predict Free Recall better than Recognition? [TO DO]
- Hypothesis: Both are generative retrieval tasks
- Analysis: RAVLT * Paradigm interaction
6. Does BVMT predict spatial (Where) more than temporal (When)? [TO DO]
- Hypothesis: BVMT is visuospatial, not temporal
- Analysis: BVMT * Domain interaction
7. Does RPM (fluid intelligence) predict complex integration (What+Where+When)? [TO DO]
- Hypothesis: Relational binding requires fluid reasoning
- Analysis: RPM predicting multi-domain composite scores

Age as Moderator:
8. Does age explain variance beyond cognitive test scores? [DONE FOR CTT]
- Hypothesis: Age has direct effects on consolidation not mediated by test performance
- Analysis: Hierarchical regression (Step 1: Age, Step 2: +Cognitive tests)
9. Do cognitive tests attenuate age effects on REMEMVR? [DONE FOR CTT]
- Hypothesis: Age effects are mediated by cognitive ability
- Analysis: Mediation model (Age > RAVLT/BVMT > REMEMVR)
10. Is there an age * cognitive test interaction? [TO DO]
- Hypothesis: Tests may be better predictors in older adults (floor effects in young)
- Analysis: Age * RAVLT interaction term

Self-Reported & Contextual Factors:
11. Do self-reported factors predict performance? [DONE FOR CTT]
- Sleep quality, VR experience, education level, typical sleep duration
- Analysis: Multiple regression including self-report variables
12. Does DASS (depression/anxiety/stress) predict memory or metacognition? [DONE FOR CTT]
- Hypothesis: Anxiety may impair metacognitive accuracy more than memory itself
- Analysis: DASS subscales predicting theta vs utility scores
13. Do memory strategies (self-reported) correlate with performance? [TO DO]
- From strategy questionnaire: method of loci, visualization, narrative
- Analysis: Strategy use predicting intercept/slope

Latent Profile Analysis:
14. Are there distinct memory profiles? ("Visualizers" vs "verbalizers", "generalists" vs "specialists") [AI]
- Hypothesis: People differ qualitatively in how they encode/retrieve
- Analysis: Latent profile analysis on What/Where/When theta scores
15. Do cognitive test profiles predict REMEMVR profiles? [AI]
- Hypothesis: RAVLT-dominant individuals > What-dominant REMEMVR
- Analysis: Profile correspondence analysis

Building a Predictive Model:
16. Can we build a parsimonious model to predict real-world episodic memory from standard tests? [AI]
- Analysis: Stepwise regression, cross-validation
- Output: Clinical prediction tool
17. What proportion of REMEMVR variance is "unexplained"? [DONE FOR CTT]
- Hypothesis: Ecological memory has substantial unique variance
- Analysis: R² upper bound
18. Do multivariate models outperform univariate models? [AI]
- Hypothesis: REMEMVR is multidimensional, requiring multivariate predictors
- Analysis: Canonical correlation or PLS

Reverse Inference:
19. Can REMEMVR performance predict performance on standard tests? [TO DO]
- Hypothesis: If REMEMVR is a "purer" episodic measure, it should predict test performance
- Analysis: REMEMVR > RAVLT/BVMT regression (reverse model)
20. Do different REMEMVR paradigms predict different tests? [TO DO]
- Hypothesis: REMEMVR Recognition > BVMT Recognition (both familiarity-based)
- Analysis: Paradigm-specific cross-test correlations
