# Chapter 4: Analysis Methods - Writing Instructions

**Read First:** `thesis/write.md` (general instructions)
**Chapter Status:** Not written (to be extracted from 65 RQ reports Section 4: Methodology)
**Target Length:** ~8,000-10,000 words

---

## WHY THIS CHAPTER MATTERS (Narrative Context)

**Ch4's Role in the Thesis:**
This is the **methodological foundation** that validates everything in Ch5-Ch7. Assessors will check: "Did you do the statistics correctly?" Ch4 answers: "Yes, and here's exactly how."

**What Goes in Ch4 vs Ch2:**
- **Ch2 (Experimental Methods):** How we collected data (participants, VR apparatus, encoding procedure, test schedule)
- **Ch4 (Analytical Methods):** How we analyzed data (IRT calibration, LMM specifications, model comparison)

**Why Ch4 is Critical:**
- Ch5-Ch6 sections say "We used 2-pass IRT purification (§4.2.2)" - Ch4 must explain what that means
- External examiners need to verify statistical rigor - Ch4 is where they look
- Prevents redundancy (explain each method ONCE here, cross-ref from Ch5-Ch7)

---

## CHAPTER STRUCTURE

### §4.1 Overview of Analytic Strategy (~500 words)
**Purpose:** The "big picture" before technical details

**Include:**
- Two-stage pipeline: IRT (measurement model) → LMM (longitudinal model)
- Why this approach? (Addresses measurement error before testing hypotheses)
- Workflow diagram: Raw data → IRT calibration → Theta scores → LMM analysis → Inference

### §4.2 Item Response Theory (IRT) Calibration (~3,000 words)

**§4.2.1 Graded Response Model (GRM) Specification**
- Why GRM over Rasch/2PL/3PL? (Ordinal confidence ratings require GRM)
- Model equation: P(Y≥k|θ) = logistic function of (a(θ-b_k))
- Parameters: a (discrimination), b_k (difficulty thresholds)
- Estimation: Marginal maximum likelihood via EM algorithm (deepirtools IWAVE)

**§4.2.2 Item Purification Protocol (Decision D039)**
- Rationale: Exclude low-quality items before analysis
- Criteria: a≥0.4 (discrimination), |b|≤3.0 (difficulty within range)
- Two-pass calibration:
  - Pass 1: All items → flag items violating criteria
  - Pass 2: Purified items only → final theta estimates
- Retention rate: Typically 40-70% (varies by domain)
- **NOTE:** When domain measurement failure (77% exclusion, 6-item scale) = problematic

**§4.2.3 Multidimensional IRT Specifications**
- What/Where/When as separate dimensions (Q-matrix specification)
- Omnibus "All" factor (aggregates across domains)
- Correlated vs uncorrelated factors (theoretical choice: correlated is plausible)

**§4.2.4 Composite_ID Stacking Approach**
- Method: 100 participants × 4 tests = 400 pseudo-participants
- Assumption violation: Breaks independence (same person at T1, T2, T3, T4)
- Justification: Necessary compromise for model stability with N=100 (true longitudinal IRT requires thousands)
- Trade-off accepted: Violation worth it for stable parameter estimates

**§4.2.5 IRT Assumptions and Diagnostics**
- Local independence (within-dimension)
- Monotonicity (higher θ → higher probability correct)
- Unidimensionality (within each What/Where/When factor)
- **UNRESOLVED:** IRT fit indices not yet reported (user asks: RMSEA, CFI, TLI, test information curves?)
- **UNRESOLVED:** DIF testing not done (user asks: should we test by age, sex, room?)

**§4.2.6 Monte Carlo Sampling**
- **UNRESOLVED:** mc_samples=1 for model_fit, mc_samples=100 for model_scores
- User can't recall rationale - needs documentation or justification

### §4.3 Linear Mixed Models (LMM) (~3,000 words)

**§4.3.1 Model Specification**
- Why LMM over repeated-measures ANOVA? (Handles unbalanced data, continuous time, nested structure)
- Fixed effects: Research-question specific (Time, Age, Domain, etc.)
- Random effects: Random intercepts by participant (UID) + random slopes when warranted
- Estimation: REML=True (parameter estimation), REML=False (model comparison via AIC)

**§4.3.2 Time Coding and Transformations**
- Days (linear): Raw retention interval
- Days² (quadratic): Tests deceleration
- log(Days+1) (logarithmic): Tests Ebbinghaus forgetting
- Power-law variants: (Days+1)^(-α) for α=0.3, 0.5, 0.7 (Wixted forgetting)
- Fractional exponents: sqrt(Days), cbrt(Days)
- Combined models: Days + log(Days), Days + Days² + log(Days)

**§4.3.3 Model Selection via AIC**
- AIC = -2log(L) + 2k (penalized likelihood)
- ΔAIC interpretation: <2 (competitive), 2-10 (weak support), >10 (essentially no support)
- Akaike weights: w_i = exp(-0.5 ΔAIC_i) / Σexp(-0.5 ΔAIC_j)
- Model averaging: Recommended when best model weight < 0.90 (extreme uncertainty)

**§4.3.4 Random Slopes Specification**
- When to include? Test via AIC comparison (random intercept only vs intercept + slopes)
- Convergence issues: Singular covariance matrices common with small N × J
- Decision: Include slopes when ΔAIC < -2 (improves fit) AND model converges

**§4.3.5 Assumption Diagnostics**
- Residual normality: Q-Q plots, Shapiro-Wilk test (tolerance: minor violations OK with large N)
- Homoscedasticity: Residual vs fitted plots, Levene's test
- Independence: Autocorrelation function (ACF) for temporal residuals
- Multicollinearity: VIF < 5 for predictors
- Outliers: Studentized residuals >±3 investigated (but rarely excluded)

### §4.4 Effect Sizes and Practical Significance (~1,500 words)

**§4.4.1 Standardized Effect Sizes**
- Cohen's d: (M1 - M2) / SD_pooled (small=0.2, medium=0.5, large=0.8)
- Cohen's f²: R²/(1-R²) (small=0.02, medium=0.15, large=0.35)
- Partial η²: SS_effect / (SS_effect + SS_error)

**§4.4.2 LMM-Specific Effect Sizes**
- Intraclass correlation (ICC): σ²_between / (σ²_between + σ²_within)
- Marginal R² (R²_m): Variance explained by fixed effects only
- Conditional R² (R²_c): Variance explained by fixed + random effects
- Interpretation: R²_c - R²_m = variance explained by random effects

### §4.5 Multiple Comparisons and Inference (~1,500 words)

**§4.5.1 Multiple Comparisons Problem**
- **UNRESOLVED:** No corrections yet applied (user acknowledges need for Bonferroni or FDR)
- When correction needed: Multiple pairwise tests within single RQ
- Bonferroni: α_adj = α / k (k = number of comparisons)
- FDR (Benjamini-Hochberg): Controls expected proportion of false discoveries

**§4.5.2 Dual p-value Reporting (Decision D068)**
- Report both: Uncorrected p + Bonferroni-corrected p
- Rationale: Transparency (reader sees both exploratory and conservative inference)

**§4.5.3 Confidence Intervals**
- Always report 95% CI for fixed effects
- Bootstrap CI for complex models (if standard errors unreliable)

### §4.6 IRT-CTT Convergence Analysis (~1,000 words)

**Purpose:** Validate that IRT theta scores aren't just noise

**§4.6.1 Convergent Validity**
- Correlation: r(theta, CTT_mean) for each domain/paradigm
- Steiger's Z-test: Does r significantly differ from 1.0?
- RMSE: Root mean squared error between theta and CTT (scaled)

**§4.6.2 When Conclusions Differ**
- Trajectory shape: Compare slope estimates (IRT vs CTT)
- Hypothesis testing: Do conclusions change? (p<.05 vs p>.05)
- Interpretation: When CTT adequate? When IRT essential?

### §4.7 Software and Reproducibility (~500 words)

**IRT Software:**
- deepirtools (Python) - IWAVE estimation (variational autoencoder)
- mirt (R) - Alternative estimation for validation
- Version control: Git repository with all analysis code

**LMM Software:**
- statsmodels (Python) - MixedLM class
- lme4 (R) - Alternative for complex random effects structures

**Visualization:**
- matplotlib + seaborn (Python)
- ggplot2 (R) for publication figures

**Reproducibility:**
- All code: github.com/rememvr/analysis (or similar)
- Data availability: De-identified data upon reasonable request (ethics approval required)
- Computational environment: pyproject.toml + poetry.lock (exact package versions)

---

## HOW TO WRITE CH4 (Extraction Strategy)

### Source Material: RQ Reports Section 4 (Methodology)

All 65 RQ reports have Section 4: Methodology. This contains:
- IRT specifications for that specific RQ
- LMM model formulas
- Time transformations used
- Model comparison results
- Purification criteria and results

### Extraction Process:

1. **Read 5-10 representative RQ reports Section 4:**
   - RQ 5.1.1 (general trajectory - uses full model suite)
   - RQ 5.2.1 (domain analysis - multidimensional IRT)
   - RQ 5.1.3 (age effects - Age×Time interactions)
   - RQ 5.1.4 (variance decomposition - random slopes)
   - RQ 6.1.1 (confidence - ordinal IRT for TC_ variables)

2. **Identify common methodological elements:**
   - What IRT specs appear in ALL RQs? (those go in §4.2.1-4.2.4)
   - What LMM specs appear in ALL RQs? (those go in §4.3.1-4.3.3)
   - What varies by RQ? (briefly mention variation, don't re-explain each time)

3. **Extract method-specific details:**
   - Model comparison procedures (§4.3.3) - extract AIC tables from RQ 5.1.1
   - Purification results (§4.2.2) - extract retention rates across domains
   - Random slopes decisions (§4.3.4) - extract convergence issues examples

4. **Write Ch4 as GENERAL methodology:**
   - "We used 2-pass GRM purification..." (describe procedure)
   - NOT "For RQ 5.1.1 we did X, for RQ 5.2.1 we did Y..." (that's redundant)
   - IF variation exists, note it: "Most RQs used random intercepts only, but RQs 5.1.4-5.1.5 included random slopes when ΔAIC<-2"

### Cross-References FROM Ch5-Ch7 TO Ch4:

Ch5-Ch7 should say:
```markdown
We calibrated theta scores using 2-pass GRM purification (§4.2.2) and
tested functional form via AIC model comparison (§4.3.2-4.3.3). For
complete methodological details, see Chapter 4.
```

NOT:
```markdown
We used a graded response model with marginal maximum likelihood estimation
via the EM algorithm, with discrimination parameters constrained to a≥0.4...
[500 words of methods repeated in every RQ section]
```

---

## UNRESOLVED METHODOLOGICAL QUESTIONS (To Address or Flag as Limitations)

**From thesis/chapters.md Q&A:**

1. **IRT fit indices:** None reported yet. Should we include RMSEA, CFI, TLI, test information curves?
   - **ACTION:** Decide which indices matter for thesis, compute them, report in §4.2.5
   - **OR:** Flag as limitation ("Future work should include formal fit indices")

2. **DIF testing:** Not done. Should we test for differential item functioning by age, sex, room?
   - **ACTION:** Decide if DIF matters for thesis claims
   - **OR:** Flag as limitation ("Assumed measurement invariance across age/sex without formal testing")

3. **Monte Carlo sampling:** mc_samples=1 for model_fit, mc_samples=100 for model_scores - rationale unclear
   - **ACTION:** Research best practices, document justification
   - **OR:** Flag as decision made during analysis (rationale: computational efficiency)

4. **Multiple comparisons:** Not yet corrected (Bonferroni or FDR needed)
   - **ACTION:** Apply corrections to all pairwise tests, report dual p-values
   - **OR:** Acknowledge as limitation, report uncorrected with caveat

5. **Confidence bias correction:** Not done (user concerned about interpretability)
   - **ACTION:** Decide if within-person z-score correction needed for TC_ variables
   - **OR:** Use raw confidence ratings, acknowledge as limitation

---

## TONE & STYLE FOR CH4

**Remember:** This is methods documentation, not a tutorial.

**Do:**
- Be precise (exact model equations, parameter definitions)
- Be concise (one clear explanation per method)
- Be authoritative ("We used X because Y")
- Cross-reference decisions ("As justified in §3.4, we chose logarithmic spacing...")

**Don't:**
- Repeat yourself (say "2-pass GRM" once, not in every subsection)
- Apologize for choices ("Unfortunately we couldn't use CAT..." - just state what you DID)
- Overwhelm with math (equations for key models, prose for the rest)

**Example:**
❌ "We unfortunately were unable to implement computerized adaptive testing due to limited resources, so we had to use a fixed-form test design instead."

✅ "We used a fixed-form test design (identical items for all participants) to ensure standardization across the 4 test sessions."

---

## SUCCESS CRITERIA FOR CH4

- [ ] Every method mentioned in Ch5-Ch7 is documented in Ch4
- [ ] §4.X.X cross-references from Ch5-Ch7 all resolve
- [ ] IRT specifications clear (model, estimation, purification)
- [ ] LMM specifications clear (fixed/random effects, time coding, model selection)
- [ ] Effect sizes and inference procedures documented
- [ ] Software and reproducibility noted
- [ ] Unresolved questions flagged as limitations (if not resolved)
- [ ] External examiner could REPLICATE analyses from Ch4 description alone

**If assessors ask: "How exactly did you do the IRT calibration?" → Ch4 answers completely.**

---

**END CH4 INSTRUCTIONS**
