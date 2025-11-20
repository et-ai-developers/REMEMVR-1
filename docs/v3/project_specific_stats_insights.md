# Project-Specific Statistical Insights

**Purpose:** REMEMVR-specific statistical requirements discovered through analysis execution
**Audience:** rq-specification agent, statistics-expert agent
**Last Updated:** 2025-11-13
**Status:** Mandatory reading for all RQ specifications

---

## Critical Requirement: 2-Pass IRT with Item Purification

### **Decision D039 (2025-11-07): ALL RQs Use 2-Pass IRT**

**Mandatory for:** ALL 50 research questions in thesis (Chapters 5, 6, 7)

**Problem Solved:**
- REMEMVR temporal (When) items systematically too difficult for participants
- Extreme item parameters (|b| > 3.0) create noise that masks true domain effects
- Single-pass IRT with unpurified items produces uninterpretable results

**Evidence:**
- **RQ 5.1 MVP Execution (November 2024):**
  - Pass 1 (105 items): No clear domain effects, noisy theta estimates
  - Pass 2 (46 items, 43.8% retention): When domain effect revealed (26.5% slower forgetting, β=+0.136, p=0.007)
  - **Conclusion:** Purification was NECESSARY to detect true effect

---

## 2-Pass IRT Methodology Specification

### **Workflow:**

**Step 1: Pass 1 Calibration (All Items)**
- Calibrate multidimensional IRT model (GRM) on complete item set
- Estimate item parameters for all items across all factors (What, Where, When)
- Extract discrimination (a) and difficulty (b) parameters
- Do NOT use Pass 1 theta scores for downstream analysis

**Step 2: Item Purification**
- Apply exclusion criteria to identify problematic items:
  - **Extreme difficulty:** |b| > 3.0 (item too easy or too hard for sample)
  - **Poor discrimination:** a < 0.4 (item doesn't differentiate ability levels)
- Flag items meeting EITHER criterion on ANY factor
- Remove flagged items from item set
- Document which items removed and why (save to logs/purification_report.csv)

**Step 3: Pass 2 Re-Calibration (Purified Items Only)**
- Re-calibrate IRT model using purified item set
- Estimate final item parameters and participant theta scores
- Use Pass 2 theta scores for ALL downstream analyses (LMM, plots, results)

---

## Exact Purification Thresholds

**Mandatory Thresholds (Decision D039):**

| Parameter | Threshold | Interpretation | Action |
|-----------|-----------|----------------|--------|
| **Difficulty (b)** | \|b\| > 3.0 | Item too easy (<-3.0) or too hard (>+3.0) for sample | EXCLUDE |
| **Discrimination (a)** | a < 0.4 | Item doesn't differentiate ability levels | EXCLUDE |

**Exclusion Rule:** Items flagged on **ANY factor** are excluded (applies to multidimensional models with What/Where/When).

**Post-Purification Validation:**
- Minimum 3 items per factor required (if <3, flag as critical error)
- Discrimination range: [0.4, 3.0] (acceptable after purification)
- Difficulty range: [-4.0, +4.0] (acceptable after purification, wider than exclusion threshold)

---

## Expected Purification Rates

**Based on RQ 5.1 MVP:**
- **Initial items:** ~105 items (18 What + 16 Where + 16 When × 3 difficulty levels)
- **Retained items:** ~46 items (43.8% retention rate)
- **Excluded items:** ~59 items (56.2% exclusion rate)

**Domain-Specific Patterns:**
- **What items:** Lower exclusion rate (~30-40%)
- **Where items:** Moderate exclusion rate (~40-50%)
- **When items:** **Higher exclusion rate (~60-70%)** ← Systematically too difficult

**Interpretation:**
- High exclusion rate is EXPECTED, not a problem
- Temporal memory items inherently more difficult (consistent with dual-process theory)
- Purification improves measurement quality, does not indicate test design flaw

---

## Implementation Requirements for RQ Specifications

### **Section 3: Input Data & Variables (info.md)**

**MUST include:**
```markdown
### IRT Calibration: 2-Pass Methodology (Decision D039)

**Pass 1: Initial Calibration**
- Calibrate GRM on ALL items (~105 total)
- Extract item parameters (a, b) across all factors
- Identify problematic items: |b| > 3.0 OR a < 0.4
- Save Pass 1 parameters to logs/pass1_item_params.csv

**Purification:**
- Remove items with |b| > 3.0 (extreme difficulty)
- Remove items with a < 0.4 (poor discrimination)
- Save purification report to logs/purification_report.csv
- Expected retention: ~40-50% of items (based on RQ 5.1 MVP)

**Pass 2: Re-Calibration**
- Re-calibrate GRM on purified item set (~40-50 items)
- Generate final theta scores (Theta_What, Theta_Where, Theta_When)
- Use Pass 2 theta scores for LMM analysis
- Save Pass 2 parameters to data/item_parameters.csv
- Save theta scores to data/theta_scores.csv
```

### **Section 4: Method (info.md)**

**MUST include IRT purification steps:**
```markdown
### Step 1: IRT Pass 1 (Initial Calibration)
- Calibrate GRM on all items
- Estimate item parameters
- Time: ~60 minutes

### Step 2: Item Purification
- Apply thresholds: |b| > 3.0 OR a < 0.4
- Remove flagged items
- Validate ≥3 items per factor remain
- Time: ~5 minutes

### Step 3: IRT Pass 2 (Purified Calibration)
- Re-calibrate GRM on purified items
- Generate final theta scores
- Time: ~20-30 minutes

### Step 4: LMM Analysis
- Use Pass 2 theta scores as dependent variables
- [Rest of LMM workflow...]
```

### **config.yaml: tool_functions Section**

**MUST include 2-pass workflow:**
```yaml
tool_functions:
  irt_pass1:
    tool: tools.analysis_irt.calibrate_grm
    inputs: [data/irt_input.csv]
    outputs: [logs/pass1_item_params.csv, logs/pass1_theta.csv]
    config:
      model: graded_response
      dimensions: 3
      purification: false  # Pass 1 uses all items

  irt_purification:
    tool: tools.analysis_irt.purify_items
    inputs: [logs/pass1_item_params.csv]
    outputs: [logs/purification_report.csv, data/purified_item_list.csv]
    config:
      max_difficulty: 3.0
      min_discrimination: 0.4

  irt_pass2:
    tool: tools.analysis_irt.calibrate_grm
    inputs: [data/irt_input.csv, data/purified_item_list.csv]
    outputs: [data/item_parameters.csv, data/theta_scores.csv]
    config:
      model: graded_response
      dimensions: 3
      purification: true  # Pass 2 uses purified items only
```

---

## Why This Is Project-Specific

**Standard Psychometric Practice:**
- 2-pass IRT with purification is common in scale development
- NOT a novel contribution, but standard quality control

**REMEMVR-Specific Necessity:**
- **Temporal items systematically difficult:** Many When items exceed |b| > 3.0
- **Composite_ID stacking:** 100 participants × 4 tests = 400 composite observations increases item parameter precision, making purification more effective
- **Small sample for IRT:** N=400 is modest for ~105 items; purification improves parameter stability

**Without 2-pass purification:**
- Domain effects masked by noisy theta estimates
- Extreme item parameters distort ability scores
- Results uninterpretable (as demonstrated in RQ 5.1 MVP Pass 1)

---

## Common Misunderstandings

### ❌ "High exclusion rate means test is flawed"
**✅ Correct:** High exclusion rate (50-60%) is EXPECTED given REMEMVR's episodic memory difficulty gradient. Temporal items are theoretically predicted to be harder (dual-process theory), and purification reflects this.

### ❌ "Purification is optional quality improvement"
**✅ Correct:** Purification is MANDATORY (Decision D039). Without it, domain effects remain undetectable (RQ 5.1 MVP evidence).

### ❌ "RQ 5.12 compares purified vs unpurified sets"
**✅ Correct:** RQ 5.12 runs **CTT analysis on Pass 2 (purified) IRT set**, NOT a comparison of purification strategies. ALL RQs use 2-pass IRT.

### ❌ "Single-pass IRT is sufficient if model converges"
**✅ Correct:** Convergence ≠ valid measurement. Extreme item parameters can converge but still distort theta scores. Purification is about interpretability, not just model fit.

---

## Related Research Questions

**RQ 5.12: CTT Analysis on Purified Set**
- Uses **Pass 2 (purified) item set** for Classical Test Theory analysis
- Compares IRT (Chapters 5-7) vs CTT scoring approaches
- NOT about comparing purified vs unpurified items

**RQ 5.1-5.11, 6.1-6.15, 7.1-7.20:**
- ALL use 2-pass IRT (Decision D039)
- ALL use Pass 2 theta scores for downstream analysis

---

## Validation Checklist for RQ Specifications

**When reviewing RQ specifications, check:**

- [ ] Section 3 includes "2-Pass IRT Methodology" subsection
- [ ] Pass 1 → Purification → Pass 2 workflow clearly specified
- [ ] Purification thresholds match Decision D039: |b| > 3.0, a < 0.4
- [ ] config.yaml tool_functions includes irt_pass1, irt_purification, irt_pass2
- [ ] Method section includes Steps 1-3 (IRT Pass 1, Purification, IRT Pass 2) before LMM
- [ ] Expected outputs include: logs/pass1_item_params.csv, logs/purification_report.csv, data/item_parameters.csv (Pass 2), data/theta_scores.csv (Pass 2)
- [ ] Validation checks include "≥3 items per factor after purification"
- [ ] NO statements like "no item-level exclusions" or "purification explored in later RQ"

**If any checklist item fails → REJECT specification, require revision**

---

## Multiple Comparison Correction: Exploratory Approach

### **Decision D068 (2025-11-14): Report Both Corrected and Uncorrected Results**

**Context:**
- Thesis has exploratory aims (50 RQs across 3 chapters)
- Strict Bonferroni correction may lead to excessive Type II errors (false negatives)
- Supervisor recommendation: Report both corrected and uncorrected results

**Mandatory for:** ALL 50 research questions with post-hoc comparisons

---

### **Rationale:**

**Exploratory Research Philosophy:**
- This is a novel assessment tool (REMEMVR) with limited prior research
- Strict FWER control prioritizes avoiding false positives, but may miss real effects
- Exploratory research balances Type I and Type II error risks differently than confirmatory studies

**Supervisor Guidance:**
- "We don't want all our results to be insignificant"
- Bonferroni may be overly conservative given exploratory context
- Transparency via dual reporting allows readers to make own judgments

**Statistical Justification:**
- Bonferroni controls family-wise error rate (FWER) at cost of reduced power
- Uncorrected tests maintain power but increase false positive risk
- Reporting both provides complete picture for informed interpretation

---

### **Implementation:**

**Step 1: Conduct Post-Hoc Tests Without Correction**
- Extract pairwise comparisons from LMM (e.g., Where-What, When-What)
- Report raw p-values without adjustment
- Use standard α = 0.05 threshold for interpretation

**Step 2: Apply Bonferroni Correction**
- Calculate adjusted α = 0.0033 / k (where k = number of comparisons in RQ)
- Re-evaluate same tests against corrected threshold
- Report which results survive correction

**Step 3: Dual Reporting in Results**
```markdown
### Post-Hoc Contrasts

**Uncorrected Results (α = 0.05):**
- Where-What: β = -0.045, p = 0.023 *
- When-What: β = -0.082, p < 0.001 ***

**Bonferroni-Corrected Results (α = 0.0011):**
- Where-What: β = -0.045, p = 0.023 (NS after correction)
- When-What: β = -0.082, p < 0.001 ***

**Interpretation:** When domain effect robust to correction; Where domain effect significant uncorrected but not corrected (marginal evidence).
```

---

### **Reporting Language:**

**For results significant with and without correction:**
> "The When-What difference was significant both uncorrected (p < 0.001) and after Bonferroni correction (p < 0.001, α_corrected = 0.0011), providing robust evidence for domain-specific forgetting."

**For results significant uncorrected but not corrected:**
> "The Where-What difference was significant uncorrected (p = 0.023) but did not survive Bonferroni correction (α_corrected = 0.0011), suggesting marginal evidence that should be interpreted cautiously pending replication."

**For results non-significant uncorrected:**
> "No significant difference between Where and What domains (p = 0.342), neither uncorrected nor corrected."

---

### **Thesis Discussion Framing:**

**Limitations Section:**
> "This thesis adopts an exploratory approach, reporting both uncorrected and Bonferroni-corrected p-values. While uncorrected tests increase Type I error risk (false positives), strict correction may inflate Type II errors (false negatives) in novel assessment contexts. We prioritize transparency, allowing readers to evaluate evidence strength using either criterion. Confirmatory studies should replicate findings using pre-registered hypotheses with strict FWER control."

**Interpretation Philosophy:**
- **Corrected p < α:** Strong evidence, robust to multiple testing
- **Uncorrected p < α, corrected p > α:** Marginal evidence, tentative conclusion
- **Uncorrected p > α:** Insufficient evidence, null result

---

### **config.yaml Specification:**

**MUST include both correction approaches:**
```yaml
post_hoc_contrasts:
  comparisons:
    - "Where-What"
    - "When-What"
    - "When-Where"

  bonferroni:
    apply: true
    family_alpha: 0.0033  # Chapter-level FWER
    num_comparisons: 3
    adjusted_alpha: 0.0011  # 0.0033 / 3

  uncorrected:
    apply: true
    alpha: 0.05

  report_both: true  # Output includes both corrected and uncorrected results
```

---

### **Implementation Requirements for RQ Specifications:**

**Section 4: Method (info.md)**

**MUST include:**
```markdown
### Step X: Post-Hoc Contrasts (Dual Reporting)

**Uncorrected Tests:**
- Extract pairwise contrasts from best LMM model
- Report raw p-values (α = 0.05)
- Identify significant effects without correction

**Bonferroni-Corrected Tests:**
- Apply family-wise correction: α_corrected = 0.0033 / k
- Re-evaluate same contrasts against corrected threshold
- Identify effects robust to multiple testing correction

**Output:** Comparison table with both uncorrected and corrected p-values, effect sizes, and interpretation guidance.
```

---

### **Validation Checklist:**

**When reviewing RQ specifications, check:**

- [ ] Post-hoc contrasts section includes BOTH uncorrected and corrected approaches
- [ ] Bonferroni correction calculation shown: α_corrected = 0.0033 / k
- [ ] Results template includes columns for both p-values
- [ ] Interpretation guidance distinguishes: robust (corrected p < α), marginal (uncorrected p < α), null (uncorrected p > α)
- [ ] config.yaml specifies both bonferroni.apply=true AND uncorrected.apply=true
- [ ] NO statements like "Bonferroni not applied" or "only uncorrected results reported"

**If uncorrected-only or corrected-only → REJECT specification, require dual reporting**

---

### **Why This Is Project-Specific:**

**Standard Practice:**
- Confirmatory research: Strict FWER control (Bonferroni, Holm-Bonferroni)
- Exploratory research: More flexible, but practices vary widely

**REMEMVR-Specific Rationale:**
- **Novel assessment tool:** Limited prior research to guide hypothesis refinement
- **50 RQs:** Strict correction across all RQs may obscure real patterns
- **Supervisor guidance:** Prioritize discovery over strict error control
- **Transparency:** Dual reporting allows community to evaluate evidence using either standard

**Without dual reporting:**
- May miss real effects (excessive Type II errors)
- OR may overstate findings (excessive Type I errors if uncorrected-only)
- Dual reporting provides balanced, transparent approach

---

## Trajectory Plotting: Dual-Scale Visualization (Theta + Probability)

### **Decision D069 (2025-11-14): Convert Theta to Probability for Trajectory Plots**

**Context:**
- LMM trajectory plots show theta (ability) on y-axis over time
- Theta is abstract standardized scale (typically -3 to +3)
- Readers unfamiliar with IRT may struggle to conceptualize theta trajectories

**Mandatory for:** ALL RQs with LMM trajectory plots showing theta over time

---

### **Problem:**

**Theta scale is abstract:**
- Theta = 0 means "average ability" (relative to sample)
- Theta = +1 means "1 SD above average"
- Hard to intuitively grasp: "What does theta = 0.5 mean in practical terms?"

**Probability scale is intuitive:**
- Probability = 60% means "60% chance of correctly recalling item"
- Direct interpretation: "Participant has 60% success rate on typical items"
- More accessible for clinical/practitioner audiences

---

### **Solution:**

**Dual-Scale Trajectory Plotting:**
1. **Primary plot:** Theta scale (y-axis: -3 to +3) - Statistical rigor, LMM operates on this scale
2. **Companion plot:** Probability scale (y-axis: 0% to 100%) - Interpretability, transforms theta using IRT formula

**Both plots show identical trajectory patterns, just different y-axis scaling**

---

### **IRT Transformation Formula:**

**2-Parameter Logistic (2PL) Model:**
```python
probability = 1 / (1 + np.exp(-(discrimination * (theta - difficulty))))
```

**Parameters:**
- `theta`: Ability score from IRT (y-axis value at each timepoint from LMM trajectory)
- `discrimination` (a): Use **mean discrimination across purified items** from Pass 2 IRT
- `difficulty` (b): Use **b = 0** (represents "typical difficulty item") OR mean difficulty across purified items

**Rationale for b = 0:**
- Setting b = 0 transforms theta to "probability of correctly answering a typical-difficulty item"
- Theta is already centered at 0, so this mapping is natural
- Alternative: Use mean b from Pass 2 items (shifts curve but preserves trajectory shape)

---

### **Implementation Steps:**

**Step 1: Extract Item Parameters from Pass 2 IRT**
```python
# After Pass 2 IRT calibration
item_params = pd.read_csv('data/item_parameters.csv')
mean_discrimination = item_params['discrimination'].mean()  # e.g., a = 1.2
mean_difficulty = 0  # OR item_params['difficulty'].mean()
```

**Step 2: Load LMM Trajectory Predictions**
```python
# LMM predicted theta at each timepoint for each domain
lmm_predictions = pd.DataFrame({
    'Time': [0, 1, 3, 6],
    'Theta_What': [0.45, 0.38, 0.30, 0.25],
    'Theta_Where': [0.30, 0.20, 0.15, 0.10],
    'Theta_When': [0.20, 0.05, -0.10, -0.15]
})
```

**Step 3: Transform Theta to Probability**
```python
def theta_to_probability(theta, a, b):
    """Convert theta to probability using 2PL IRT model"""
    return 1 / (1 + np.exp(-(a * (theta - b))))

# Apply transformation to each domain
for domain in ['What', 'Where', 'When']:
    theta_col = f'Theta_{domain}'
    prob_col = f'Prob_{domain}'
    lmm_predictions[prob_col] = theta_to_probability(
        lmm_predictions[theta_col],
        a=mean_discrimination,
        b=mean_difficulty
    )
```

**Step 4: Generate Dual-Scale Plots**
```python
# Plot A: Theta scale (original LMM output)
plt.figure(figsize=(10, 6))
plt.plot(lmm_predictions['Time'], lmm_predictions['Theta_What'], label='What')
plt.plot(lmm_predictions['Time'], lmm_predictions['Theta_Where'], label='Where')
plt.plot(lmm_predictions['Time'], lmm_predictions['Theta_When'], label='When')
plt.ylabel('Theta (Ability)')
plt.xlabel('Days Since Encoding')
plt.title('Memory Trajectory: Theta Scale')
plt.savefig('plots/trajectory_theta.png')

# Plot B: Probability scale (transformed)
plt.figure(figsize=(10, 6))
plt.plot(lmm_predictions['Time'], lmm_predictions['Prob_What'] * 100, label='What')
plt.plot(lmm_predictions['Time'], lmm_predictions['Prob_Where'] * 100, label='Where')
plt.plot(lmm_predictions['Time'], lmm_predictions['Prob_When'] * 100, label='When')
plt.ylabel('Probability Correct (%)')
plt.xlabel('Days Since Encoding')
plt.title('Memory Trajectory: Probability Scale')
plt.ylim(0, 100)
plt.savefig('plots/trajectory_probability.png')
```

---

### **Example Interpretation:**

**Theta Scale Plot:**
- What domain: theta = 0.45 at Day 0 → 0.25 at Day 6 (decline of 0.20 theta units)
- When domain: theta = 0.20 at Day 0 → -0.15 at Day 6 (decline of 0.35 theta units)

**Probability Scale Plot (with a=1.2, b=0):**
- What domain: 66% correct at Day 0 → 57% correct at Day 6 (9% decline)
- When domain: 56% correct at Day 0 → 46% correct at Day 6 (10% decline)

**Reader Takeaway:** "Participants remembered 66% of What items immediately but only 57% after 6 days, while When items dropped from 56% to 46%."

---

### **Reporting in Results:**

**Section: Trajectory Analysis**

```markdown
### Forgetting Trajectories by Domain

**Theta Scale (Figure X):**
LMM trajectories show differential forgetting across domains. What domain maintained highest ability (theta = 0.45 → 0.25), while When domain showed steeper decline (theta = 0.20 → -0.15).

**Probability Scale (Figure Y):**
Transforming theta to probability correct (using mean item discrimination a = 1.2), we observe:
- What items: 66% correct at Day 0, declining to 57% at Day 6 (9% loss)
- Where items: 59% correct at Day 0, declining to 53% at Day 6 (6% loss)
- When items: 56% correct at Day 0, declining to 46% at Day 6 (10% loss)

**Interpretation:** Probability-scale trajectories reveal practical significance - participants lose approximately 10% recall accuracy for temporal information over 6 days, compared to 6% for spatial information.
```

---

### **Implementation Requirements for RQ Specifications:**

**Section 4: Method (info.md)**

**MUST include transformation step:**
```markdown
### Step X: Generate Trajectory Plots

**Theta Scale Plot:**
- Extract LMM predicted trajectories for each domain
- Plot theta vs. time with 95% CIs
- Y-axis: Theta (ability), range: -3 to +3
- Save to plots/trajectory_theta.png

**Probability Scale Plot:**
- Transform theta to probability using 2PL formula: p = 1/(1 + exp(-(a*(theta - b))))
- Use mean discrimination from Pass 2 IRT (a = mean(item_params$discrimination))
- Use b = 0 (typical difficulty reference point)
- Plot probability vs. time with transformed CIs
- Y-axis: Probability Correct (%), range: 0% to 100%
- Save to plots/trajectory_probability.png

**Output:** Dual-scale plots showing same trajectories in both theta and probability metrics.
```

---

### **config.yaml Specification:**

**MUST include transformation parameters:**
```yaml
trajectory_plots:
  theta_scale:
    enabled: true
    y_label: "Theta (Ability)"
    y_limits: [-3, 3]
    output: "plots/trajectory_theta.png"

  probability_scale:
    enabled: true
    transformation:
      formula: "1 / (1 + exp(-(a * (theta - b))))"
      discrimination_source: "mean"  # Use mean(a) from Pass 2 items
      difficulty_reference: 0  # b = 0 for typical difficulty
    y_label: "Probability Correct (%)"
    y_limits: [0, 100]
    output: "plots/trajectory_probability.png"
```

---

### **Validation Checklist:**

**When reviewing RQ specifications, check:**

- [ ] Trajectory plots section includes BOTH theta-scale and probability-scale plots
- [ ] Probability transformation formula specified: `1 / (1 + exp(-(a * (theta - b))))`
- [ ] Discrimination parameter sourced from Pass 2 IRT item parameters (mean or median)
- [ ] Difficulty reference specified (b = 0 or mean from Pass 2)
- [ ] config.yaml includes trajectory_plots.probability_scale.enabled = true
- [ ] Results interpretation includes practical significance from probability scale
- [ ] NO statements like "theta-only plots" or "probability conversion not needed"

**If probability-scale plot missing → REJECT specification, require dual-scale plotting**

---

### **Why This Is Project-Specific:**

**Standard Practice:**
- IRT analyses typically report theta scale only (statistical convention)
- Probability transformations sometimes included for interpretability but not universal

**REMEMVR-Specific Rationale:**
- **Clinical relevance:** Thesis has clinical implications - probability scale more accessible to practitioners
- **Difficulty gradient:** REMEMVR temporal items systematically harder - probability scale reveals practical impact
- **Mixed audience:** Thesis will be read by psychometricians (prefer theta) AND cognitive neuroscientists (prefer percentages)
- **Interpretability priority:** 50 RQs with complex trajectories - dual-scale plots enhance clarity

**Benefits:**
- Theta scale preserves statistical rigor (LMM operates on theta)
- Probability scale enhances accessibility (readers unfamiliar with IRT)
- Both scales together provide complete picture

**Without probability transformation:**
- Readers may misinterpret theta units ("What does theta = 0.5 mean?")
- Practical significance obscured by abstract metric
- Harder to communicate findings to non-psychometric audiences

---

## IRT→LMM Pipeline: Composite_ID Stacking with TSVR

### **Decision D070 (2025-11-14): Use TSVR (Hours Since Encoding), Not Nominal Days**

**Context:**
- IRT uses composite_ID stacking: 100 participants × 4 tests = 400 "pseudo-participants"
- Each composite_ID (e.g., A010_T1, A010_T2, A010_T3, A010_T4) gets theta scores from IRT
- LMM models theta over time to detect forgetting trajectories
- **Critical question:** What is the TIME variable in the LMM?

**Mandatory for:** ALL RQs using IRT→LMM pipeline (chapters 5, 6, 7)

---

### **Problem:**

**Nominal days are INCORRECT:**
- T1 = "Day 0", T2 = "Day 1", T3 = "Day 3", T4 = "Day 6" are INSTRUCTED test schedules
- Participants often completed tests at different times (scheduling conflicts, late submissions)
- Using nominal days ignores actual delay period variance

**Example:**
- Participant A010: T2 completed 28 hours after VR (should be "Day 1" = 24 hours)
- Participant A053: T2 completed 20 hours after VR (early completion)
- Using nominal "Day 1" for both = measurement error

---

### **Solution:**

**Use TSVR (Time Since VR) tags for ACTUAL delay period:**
- `{UID}-RVR-T1-STA-X-TSVR` = Hours since VR encoding at Test 1
- `{UID}-RVR-T2-STA-X-TSVR` = Hours since VR encoding at Test 2
- `{UID}-RVR-T3-STA-X-TSVR` = Hours since VR encoding at Test 3
- `{UID}-RVR-T4-STA-X-TSVR` = Hours since VR encoding at Test 4

**Data source:** Master.xlsx demographic tags (DEM topic)

---

### **Complete IRT→LMM Pipeline:**

**Step 1: IRT Calibration (Composite_ID Stacking)**
```python
# Input: Item response data in LONG format
# One row per composite_ID × item combination
irt_input = pd.DataFrame({
    'composite_ID': ['A010_T1', 'A010_T1', 'A010_T2', 'A010_T2', ...],
    'item_id': ['item1', 'item2', 'item1', 'item2', ...],
    'response': [1, 0, 1, 1, ...]
})

# IRT treats each composite_ID as independent "person"
# 100 participants × 4 tests = 400 "pseudo-participants"
```

**Step 2: Extract Theta Scores**
```python
# Output: One theta per composite_ID per domain
theta_scores = pd.DataFrame({
    'composite_ID': ['A010_T1', 'A010_T2', 'A010_T3', 'A010_T4', ...],
    'Theta_What': [0.45, 0.38, 0.30, 0.25, ...],
    'Theta_Where': [0.30, 0.20, 0.15, 0.10, ...],
    'Theta_When': [0.20, 0.05, -0.10, -0.15, ...]
})
```

**Step 3: Extract TSVR Data from Master.xlsx**
```python
# Extract TSVR for each participant × test combination
tsvr_data = data.extract_tags(
    tag_pattern='{UID}-RVR-{Test}-STA-X-TSVR',
    participants='all',
    tests=['T1', 'T2', 'T3', 'T4']
)

# Output:
tsvr_long = pd.DataFrame({
    'UID': ['A010', 'A010', 'A010', 'A010', ...],
    'Test': ['T1', 'T2', 'T3', 'T4', ...],
    'TSVR_hours': [0.5, 27.2, 73.8, 145.3, ...]  # ACTUAL hours since VR
})
```

**Step 4: Create LMM Input Dataset**
```python
# Parse composite_ID to extract UID and Test
theta_scores['UID'] = theta_scores['composite_ID'].str.split('_').str[0]
theta_scores['Test'] = theta_scores['composite_ID'].str.split('_').str[1]

# Merge theta scores with TSVR
lmm_input = theta_scores.merge(
    tsvr_long,
    on=['UID', 'Test'],
    how='left'
)

# Reshape from WIDE (3 theta columns) to LONG (domain as factor)
lmm_long = pd.melt(
    lmm_input,
    id_vars=['composite_ID', 'UID', 'Test', 'TSVR_hours'],
    value_vars=['Theta_What', 'Theta_Where', 'Theta_When'],
    var_name='Domain',
    value_name='Theta'
)

# Clean domain labels (Theta_What → What)
lmm_long['Domain'] = lmm_long['Domain'].str.replace('Theta_', '')

# Final LMM input:
# - One row per composite_ID × domain combination
# - Time variable: TSVR_hours (ACTUAL delay period)
# - Outcome: Theta (ability score)
```

**Step 5: Fit LMM with TSVR as Time Variable**
```python
import statsmodels.formula.api as smf

# Convert hours to days for interpretable coefficients
lmm_long['TSVR_days'] = lmm_long['TSVR_hours'] / 24

# Fit LMM with Domain × Time interaction
formula = "Theta ~ (TSVR_days + np.log(TSVR_days + 1)) * C(Domain, Treatment('What'))"
model = smf.mixedlm(
    formula=formula,
    data=lmm_long,
    groups=lmm_long['UID'],
    re_formula="~TSVR_days"  # Random intercepts + slopes
)

results = model.fit(reml=False)
```

---

### **Why TSVR, Not Nominal Days?**

**Statistical Validity:**
- LMM assumes time variable accurately reflects delay period
- Using nominal days introduces measurement error (some participants tested early/late)
- TSVR provides precise delay period for each composite_ID

**Example Variance:**
- T1 (nominal "Day 0"): TSVR range 0.3 to 2.5 hours (most ~0.5 hours)
- T2 (nominal "Day 1"): TSVR range 20 to 32 hours (target 24 hours)
- T3 (nominal "Day 3"): TSVR range 68 to 80 hours (target 72 hours)
- T4 (nominal "Day 6"): TSVR range 140 to 156 hours (target 144 hours)

**Impact of Ignoring TSVR:**
- Variance in delay period treated as residual error (noise)
- Reduces power to detect time effects
- Biases slope estimates (some participants tested systematically early/late)

---

### **Implementation Requirements for RQ Specifications:**

**Section 3: Input Data & Variables (info.md)**

**MUST include:**
```markdown
### IRT Output: Theta Scores
- Source: data/theta_scores.csv (from Pass 2 IRT)
- Variables: composite_ID, Theta_What, Theta_Where, Theta_When
- Format: One row per composite_ID (A010_T1, A010_T2, A010_T3, A010_T4)

### TSVR Data: Actual Delay Period
- Source: master.xlsx, tags `{UID}-RVR-{Test}-STA-X-TSVR`
- Variables: UID, Test, TSVR_hours
- Format: Hours since VR encoding (precise delay period)
- **CRITICAL:** Use TSVR as time variable in LMM, NOT nominal days (0, 1, 3, 6)

### Data Reshaping for LMM
- Parse composite_ID → extract UID and Test
- Merge theta scores with TSVR on [UID, Test]
- Reshape from WIDE (3 domains) to LONG (domain as factor)
- Convert TSVR_hours to TSVR_days (divide by 24) for interpretable coefficients
- Final format: One row per composite_ID × domain (400 composites × 3 domains = 1200 rows)
```

**Section 4: Method (info.md)**

**MUST include reshaping step:**
```markdown
### Step X: Reshape IRT Output for LMM

**Parse composite_ID:**
- Extract UID (participant ID) from composite_ID
- Extract Test (T1/T2/T3/T4) from composite_ID

**Merge with TSVR:**
- Load TSVR data from master.xlsx: `{UID}-RVR-{Test}-STA-X-TSVR`
- Merge theta scores with TSVR on [UID, Test]
- Verify all composite_IDs have TSVR values (no missingness)

**Reshape to long format:**
- Melt Theta_What, Theta_Where, Theta_When → single Theta column with Domain factor
- Convert TSVR_hours to TSVR_days (divide by 24)
- Output: data/lmm_input.csv (one row per composite_ID × domain)

**Validation:**
- Check N rows: 400 composite_IDs × 3 domains = 1200 rows
- Check TSVR_days range: ~0 to ~6.5 days (expect variance around nominal 0, 1, 3, 6)
- Check no missing TSVR values
```

**Section 4: Method - LMM Step**

**MUST specify TSVR as time variable:**
```markdown
### Step Y: Fit LMM with TSVR as Time Variable

**Time variable:** TSVR_days (NOT nominal days 0, 1, 3, 6)
- Actual delay period from VR encoding to test completion
- Accounts for participant-level variance in test scheduling
- Measured in days (converted from TSVR_hours / 24)

**Formula:** `Theta ~ (TSVR_days + np.log(TSVR_days + 1)) * C(Domain, Treatment('What'))`

**Random effects:** Random intercepts and slopes for TSVR_days by UID
- Allows participant-specific forgetting rates

**Output:** LMM results with Domain × Time interaction using ACTUAL delay period
```

---

### **config.yaml Specification:**

**MUST include TSVR extraction and reshaping:**
```yaml
step_4_extract_tsvr:
  tool: tools.data.extract_tags
  inputs: [config/master.xlsx]
  outputs: [data/tsvr_data.csv]
  config:
    tag_pattern: "{UID}-RVR-{Test}-STA-X-TSVR"
    participants: "all"
    tests: ["T1", "T2", "T3", "T4"]
    output_format: "long"

step_5_reshape_for_lmm:
  tool: tools.data.reshape_irt_to_lmm
  inputs: [data/theta_scores.csv, data/tsvr_data.csv]
  outputs: [data/lmm_input.csv]
  config:
    parse_composite_id: true  # Extract UID and Test from composite_ID
    merge_on: ["UID", "Test"]
    melt_domains: ["Theta_What", "Theta_Where", "Theta_When"]
    time_variable: "TSVR_hours"
    convert_hours_to_days: true  # TSVR_days = TSVR_hours / 24
    validate_row_count: 1200  # 400 composite_IDs × 3 domains

step_6_lmm_analysis:
  tool: tools.analysis_lmm.fit_trajectory_models
  inputs: [data/lmm_input.csv]
  outputs: [logs/model_selection.csv, logs/best_model.rds]
  config:
    outcome: "Theta"
    time_variable: "TSVR_days"  # CRITICAL: Use TSVR_days, not nominal days
    domain_variable: "Domain"
    domain_reference: "What"
    random_effects: "~TSVR_days"
    group_variable: "UID"
```

---

### **Validation Checklist:**

**When reviewing RQ specifications, check:**

- [ ] Section 3 mentions TSVR extraction from master.xlsx tags
- [ ] Time variable specified as TSVR (hours or days), NOT nominal days (0, 1, 3, 6)
- [ ] Reshaping step includes: parse composite_ID, merge with TSVR, melt domains
- [ ] LMM formula uses TSVR_days as time variable
- [ ] config.yaml includes step for extracting `{UID}-RVR-{Test}-STA-X-TSVR` tags
- [ ] config.yaml includes reshape_irt_to_lmm tool with TSVR merge
- [ ] Validation checks row count: 400 composite_IDs × 3 domains = 1200 rows
- [ ] NO statements like "use Days 0, 1, 3, 6" or "nominal test days"

**If nominal days used → REJECT specification, require TSVR**

---

### **Why This Is Project-Specific:**

**Standard IRT→LMM Practice:**
- Many studies use categorical time (e.g., T1, T2, T3 as factors)
- OR assume tests completed exactly on schedule (use nominal days)

**REMEMVR-Specific Rationale:**
- **Scheduling variance:** Participants completed tests within windows, not exact days
- **Composite_ID stacking:** 400 "pseudo-participants" means we HAVE precise delay data for each
- **Master.xlsx design:** TSVR tags explicitly captured for this purpose
- **Statistical precision:** Using actual delay periods reduces measurement error

**Benefits:**
- Accurate delay period for each composite_ID (not nominal average)
- Reduces residual error in LMM (variance explained by true time, not noise)
- Allows detection of subtle trajectory differences

**Without TSVR:**
- Measurement error inflates residual variance
- Biased slope estimates if participants systematically early/late
- Reduced power to detect time effects

---

### **Common Misunderstandings:**

#### ❌ "T1=Day 0, T2=Day 1, T3=Day 3, T4=Day 6 is the time variable"
**✅ Correct:** T1/T2/T3/T4 are TEST LABELS. TSVR is the TIME VARIABLE (actual hours/days since encoding).

#### ❌ "Nominal days are close enough, TSVR adds complexity"
**✅ Correct:** TSVR is NECESSARY for valid LMM. Measurement error in time variable biases estimates and reduces power.

#### ❌ "TSVR only matters if participants missed tests"
**✅ Correct:** TSVR matters because participants completed tests within WINDOWS (e.g., "Day 1" = 20-32 hours), not exact times. Variance exists even for compliant participants.

#### ❌ "composite_ID stacking is just for IRT, doesn't affect LMM"
**✅ Correct:** Composite_ID stacking affects BOTH IRT and LMM. Each composite_ID (A010_T1, A010_T2, etc.) needs its own TSVR value for the LMM to have correct time data.

---

## References

**Decision D039 (2025-11-07):** "2-Pass IRT as Standard Methodology"
- Source: `.claude/context/archive/decisions_automation.md`
- Status: Active, mandatory for all RQs

**RQ 5.1 MVP Execution (November 2024):**
- 105 items → 46 retained (43.8%)
- When domain effect only detected after purification (β=+0.136, p=0.007)
- Evidence that purification is necessary, not optional

**IRT Methodology Documentation:**
- `docs/irt_methodology.md` - General IRT theory and validation procedures
- `config/irt.yaml` - Template purification configuration

---

## Updates Log

| Date | Update | Reason |
|------|--------|--------|
| 2025-11-13 | Initial creation | RQ 5.1 v3.0 specification missing 2-pass IRT; stats-expert didn't catch project-specific requirement |
| 2025-11-14 | Added Decision D068: Dual reporting (corrected + uncorrected results) | Supervisor guidance for exploratory thesis; balance Type I/II error risks |
| 2025-11-14 | Added Decision D069: Dual-scale trajectory plots (theta + probability) | User request: Theta scale abstract, probability scale more intuitive for readers/clinicians |
| 2025-11-14 | Added Decision D070: IRT→LMM pipeline with TSVR (actual hours since encoding) | Critical fix: Time variable should be TSVR (actual delay period), NOT nominal days (0, 1, 3, 6). Complete pipeline documentation added. |

---

**End of Project-Specific Statistical Insights**

**Mandatory Action:** rq-specification and statistics-expert agents MUST read this file before creating/validating any RQ specification.
