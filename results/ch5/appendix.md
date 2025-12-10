# Appendix A: Complete Statistical Results for Chapter 5

This appendix provides complete statistical details for all 35 Research Questions in Chapter 5. Each RQ section includes:
- Full model specifications
- Complete statistical tables
- Model comparison details
- Assumption diagnostics
- Extended results interpretation

**Organization:** Sections mirror Chapter 5 structure (§A.1 through §A.5), with subsections for each RQ.

---

## A.1 Functional Form and Individual Differences

This section contains complete statistical results for RQs 5.1.1 through 5.1.5, examining functional form of forgetting trajectories and individual differences in baseline ability and forgetting rates.

---

### A.1.1 Functional Form of Forgetting Trajectories (RQ 5.1.1)

**Main Chapter Reference:** §5.1.1

**Sample and Design:**
- N=100 participants, 400 observations (4 test sessions per participant)
- IRT calibration: Two-pass GRM with omnibus factor "All"
  - Pass 1: 105 items calibrated
  - Item purification: Excluded 37 items (discrimination a < 0.4 or difficulty |b| > 3.0)
  - Pass 2: 68 items retained (64.8% retention rate)
  - Theta range: [-2.52, 2.73]
- LMM time variable: TSVR_hours (continuous, range 1-246 hours, 295 unique values)

**Extended Model Comparison (66 Models):**

Extended model comparison tested 66 candidate functional forms using continuous time variable (TSVR_hours) with random intercepts by participant. Models compared via AIC (REML=False).

**Top 20 Models (Ranked by AIC):**

| Rank | Model | AIC | ΔAIC | Weight | Cumulative Weight |
|------|-------|-----|------|--------|-------------------|
| 1 | PowerLaw_04 (α=0.4) | 866.61 | 0.00 | 0.056 | 0.056 |
| 2 | PowerLaw_05 (α=0.5) | 866.77 | 0.16 | 0.052 | 0.108 |
| 3 | PowerLaw_03 (α=0.3) | 866.85 | 0.24 | 0.049 | 0.157 |
| 4 | PowerLaw_06 (α=0.6) | 867.12 | 0.51 | 0.043 | 0.200 |
| 5 | PowerLaw_02 (α=0.2) | 867.45 | 0.84 | 0.037 | 0.237 |
| ... | ... | ... | ... | ... | ... |
| 16 | SquareRoot+Log | 868.52 | 1.91 | 0.021 | 0.571 |
| 33 | Logarithmic | 869.71 | 3.10 | 0.012 | 0.823 |

**Key Findings:**
- Best single model: PowerLaw_04 (α=0.4), but only 5.6% weight (94% probability another model better)
- Top 5 models: All power-law variants (α=0.2 to 0.7), collectively 24% weight
- Logarithmic model (original hypothesis): Ranked 33rd, ΔAIC=+3.10, weight=1.2%
- Evidence ratio: 4.7:1 against logarithmic in favor of best power-law
- Extreme model uncertainty: Shannon diversity H'=2.71 (equivalent to 15 equally plausible models)

**Model Averaging Results:**

Given best model weight < 0.30, model averaging applied across 16 competitive models (ΔAIC < 2), collectively accounting for 57.1% of Akaike weight.

**Model-Averaged Parameters:**
- Effective power-law exponent: α_eff = 0.410
- Prediction standard errors: 0.001 to 0.046 (reflecting between-model variance)
- Effective number of models: N_eff = 15 (Shannon diversity)

**Observed Trajectory (Raw Data):**
- Day 0 (T1): θ = 0.67, Probability = 76% correct
- Day 1 (T2): θ = 0.12, Probability = 55% correct (Δθ = -0.55 in first 24h)
- Day 3 (T3): θ = -0.18, Probability = 43% correct
- Day 6 (T4): θ = -0.51, Probability = 30% correct
- Total decline: Δθ = -1.18 SD, ΔProbability = -46 percentage points

**Functional Form Interpretation:**

Power-law form: θ(t) ∝ (t + 1)^(-α)

Where:
- α_eff = 0.410 (intermediate within typical range α = 0.2-0.8 for laboratory tasks)
- Forgetting rate decreases proportionally with elapsed time
- Consistent with temporal distinctiveness theory (Wixted & Ebbesen, 1991; Brown, Neath, & Chater, 2007)

**Theoretical Implications:**
- VR episodic memories occupy middle ground between:
  - Highly distinctive autobiographical events (shallow decay, α ≈ 0.2)
  - Impoverished word lists (steep decay, α ≈ 0.6-0.8)
- Recent events compressed in memory and thus less discriminable than remote events

**Methodological Paradigm Shift (Original vs Extended Analysis):**

Original analysis limitations:
1. Discrete Days variable (4 unique values) → insufficient resolution for fractional exponents
2. Only 5 models tested, omitted power-law variants despite citing Wixted & Ebbesen (1991)
3. Single best model selection (logarithmic, 48% weight) → ignored 52% probability another model better

Extended analysis improvements:
1. Continuous TSVR_hours (295 unique values) → stable fractional exponent estimation
2. 66 models including 12 power-law specifications → comprehensive functional form space
3. Model averaging across 16 competitive models → acknowledges extreme uncertainty, robust predictions

**Assumption Diagnostics:**

[Complete assumption validation details to be added from §4.3.3 results]

---

### A.1.2 Two-Phase Forgetting (RQ 5.1.2)

**Main Chapter Reference:** §5.1.2

[PLACEHOLDER: Detailed piecewise model specifications, practice decomposition analysis]

---

### A.1.3 Age Effects (RQ 5.1.3)

**Main Chapter Reference:** §5.1.3

[PLACEHOLDER: Extended model comparison with age interactions, power analysis details]

---

### A.1.4 Individual Differences in Forgetting Rate (RQ 5.1.4)

**Main Chapter Reference:** §5.1.4

[PLACEHOLDER: Random slopes model comparison, ICC decomposition tables]

---

### A.1.5 Latent Trajectory Clustering (RQ 5.1.5)

**Main Chapter Reference:** §5.1.5

[PLACEHOLDER: Cluster validation metrics, bootstrap stability analysis, profile tables]

---

## A.2 Domain-Specific Forgetting

Complete results for RQs 5.2.1 through 5.2.7.

---

### A.2.1 Domain Trajectories (RQ 5.2.1)

**Main Chapter Reference:** §5.2.1

[PLACEHOLDER: Domain-specific model specifications, pairwise contrasts]

---

### A.2.2 Domain × Consolidation Window (RQ 5.2.2)

**Main Chapter Reference:** §5.2.2

[PLACEHOLDER: Three-way interaction tables, consolidation window analyses]

---

### A.2.3 Domain × Age (RQ 5.2.3)

**Main Chapter Reference:** §5.2.3

[PLACEHOLDER: Age interaction models, tertile comparisons]

---

### A.2.4 IRT-CTT Convergence for Domains (RQ 5.2.4)

**Main Chapter Reference:** §5.2.4

[PLACEHOLDER: Correlation matrices, trajectory comparison tables, Steiger's z-tests]

---

### A.2.5 Purification Effects on Domains (RQ 5.2.5)

**Main Chapter Reference:** §5.2.5

[PLACEHOLDER: Purification impact tables, AIC comparisons, convergence diagnostics]

---

### A.2.6 Domain Variance Decomposition (RQ 5.2.6)

**Main Chapter Reference:** §5.2.6

[PLACEHOLDER: ICC tables by domain, variance component analysis]

---

### A.2.7 Domain-Based Clustering (RQ 5.2.7)

**Main Chapter Reference:** §5.2.7

[PLACEHOLDER: Cluster profiles, silhouette analysis, bootstrap Jaccard]

---

## A.3 Retrieval Paradigm Effects

Complete results for RQs 5.3.1 through 5.3.9.

[PLACEHOLDER: Similar structure for all §5.3 RQs]

---

## A.4 Encoding Factors and Schema Effects

Complete results for RQs 5.4.1 through 5.4.7.

[PLACEHOLDER: Similar structure for all §5.4 RQs]

---

## A.5 Source vs Destination Spatial Memory

Complete results for RQs 5.5.1 through 5.5.7.

[PLACEHOLDER: Similar structure for all §5.5 RQs]

---

**END APPENDIX A**
