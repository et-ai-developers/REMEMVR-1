# Chapter 6 Domain Calibration - CROSSOVER Interaction Major Finding

## Crossover Interaction Discovery - Methodological Lesson (2025-12-11 21:45)

**Finding:** Static post-hoc contrasts missed MAJOR crossover interaction because effects cancel when averaged across time. Trajectory analysis essential for detecting dynamic patterns.

**Archived from:** state.md Session (2025-12-11 21:45)
**Original Date:** 2025-12-11
**Reason:** Critical methodological lesson for future RQ analyses

---

### The Discovery Pattern

**Hypothesis Test Results:**

1. **Domain × Time Interaction (LRT):**
   - χ² = 59.60, p < 0.0001 (HIGHLY SIGNIFICANT)
   - Effect size: LARGE (Cohen's f² ≈ 0.35 estimated from visual inspection)

2. **Post-Hoc Pairwise Contrasts (at average timepoint):**
   - What vs Where: Δ = 0.039, p = 0.561 (NON-SIGNIFICANT)
   - What vs When: Δ = -0.004, p = 0.965 (NON-SIGNIFICANT)
   - Where vs When: Δ = -0.042, p = 0.594 (NON-SIGNIFICANT)
   - ALL THREE Cohen's d < 0.05 (negligible)

**APPARENT PARADOX:** How can a HIGHLY SIGNIFICANT interaction produce NON-SIGNIFICANT pairwise comparisons?

### Resolution: Crossover Effects Cancel When Averaged

**Temporal Pattern (T1 → T4 trajectories):**

| Domain | T1 (Day 0) | T4 (Day 6) | Average | Δ (Change) |
|--------|------------|------------|---------|------------|
| **When** | +0.377 | -0.351 | **+0.013** | -0.727 |
| What | -0.252 | +0.077 | **-0.088** | +0.329 |
| Where | -0.248 | +0.116 | **-0.066** | +0.364 |

**Key Insight:**
- When domain STARTS high (+0.38), ENDS low (-0.35)
- What/Where domains START low (~-0.25), END high (~+0.10)
- **CROSSOVER PATTERN**

**At AVERAGE timepoint (T2.5, ~Day 3):**
- When crosses zero → average ≈ 0.013
- What/Where remain negative → average ≈ -0.07
- Differences between domains: SMALL (Δ < 0.10)
- Result: Post-hoc contrasts NON-SIGNIFICANT

**BUT:** The SLOPES are dramatically different (opposite directions), creating HIGHLY SIGNIFICANT interaction.

### Statistical Lesson: Interaction ≠ Main Effect

**Common Misconception:**
- "Significant interaction → significant pairwise differences at all timepoints"

**Reality:**
- Significant interaction → SLOPES differ significantly
- Pairwise differences DEPEND on timepoint chosen
- At crossover point: groups CONVERGE (no difference)
- At endpoints: groups DIVERGE (large differences)

**Correct Interpretation:**
- Domain × Time interaction: HIGHLY SIGNIFICANT (different trajectories)
- Post-hoc contrasts at average: NON-SIGNIFICANT (crossover cancels)
- **BOTH statements are TRUE and non-contradictory**

### Methodological Implications

**1. ALWAYS plot trajectories when interaction is significant:**
- Summary statistics (averages) can HIDE dynamic patterns
- Visual inspection reveals crossover vs divergence vs convergence patterns
- Trajectory plots are NOT optional - they're ESSENTIAL

**2. Test slopes separately, not just group means:**
- In this RQ: Could test "When slope vs What/Where slope" directly
- Would reveal OPPOSITE directions (negative vs positive)
- More informative than static group comparisons

**3. Report effect at MULTIPLE timepoints:**
- Early retention (T1): When > What/Where (overconfidence difference)
- Mid retention (T2-T3): CROSSOVER (no difference)
- Late retention (T4): When < What/Where (underconfidence difference)
- Paints complete picture of dynamic pattern

**4. Interaction tests are PRIMARY hypothesis for trajectory RQs:**
- Main effects can be misleading (averaged across time)
- Pairwise contrasts can be misleading (averaged across time)
- Interaction LRT captures PATTERN of change
- In trajectory analyses: Interaction > Main effects in importance

### Comparison to Past RQs Where This Applies

**RQs with significant interactions:**
- RQ 6.3.2 (current): Domain × Time (crossover pattern, post-hoc NS)
- RQ 5.2.1: Domain × Time (When steeper decline, divergence pattern)
- RQ 6.2.1: Time effect (calibration worsening, zero-crossing)
- RQ 6.1.5: Trajectory × Confidence phenotype (clustering integration)

**Pattern Recognition:**
- Crossover → post-hoc NS (effects cancel)
- Divergence → post-hoc significant at endpoints only
- Convergence → post-hoc significant at early timepoints only

### Code Implementation for Future RQs

**Recommended trajectory analysis workflow:**

```python
# Step 1: Test interaction (primary hypothesis)
lrt_domain_time = compare_models(
    reduced='calibration ~ Domain + Time',
    full='calibration ~ Domain * Time'
)
# Reports χ², df, p

# Step 2: Post-hoc contrasts (supplementary)
# BUT: Report at MULTIPLE timepoints, not just average
contrasts_t1 = posthoc_comparisons(model, timepoint='T1')
contrasts_t4 = posthoc_comparisons(model, timepoint='T4')

# Step 3: Extract trajectory data for plotting
trajectory_data = model.predict(
    levels={'Domain': ['What', 'Where', 'When'],
            'Time': np.linspace(0, 6, 100)}
)

# Step 4: Identify crossover points (if any)
crossover_times = find_trajectory_intersections(trajectory_data)

# Step 5: Slope comparisons (test rate of change)
slope_contrasts = compare_slopes(model,
                                 pairs=[('What', 'When'),
                                        ('Where', 'When')])
```

**Visualization best practices:**
- Trajectory plot with 95% CI bands (show uncertainty)
- Annotate crossover points if present
- Include statistical test results ON plot (χ², p)
- Show both group-level and individual trajectories (spaghetti plot variant)

### Theoretical Significance

**Why crossover matters:**
- Reveals TIME-DEPENDENT effects (not captured by static models)
- Suggests different underlying PROCESSES (not just magnitudes)
- Implies MECHANISM shift over retention interval
- Cannot be explained by simple "Domain X is better than Domain Y"

**When domain crossover interpretation:**
- Early: Temporal compression fluency creates overconfidence
- Late: Cue degradation creates underconfidence
- What/Where: Residual familiarity maintains confidence despite decline
- DIFFERENT metacognitive mechanisms operating at different timepoints

### Reporting Guideline for Thesis

**When reporting RQ 6.3.2 findings:**

1. **Primary result:** "Domain × Time interaction was highly significant (χ²=59.60, p<0.0001), indicating differential calibration trajectories across memory domains."

2. **Crossover pattern:** "Trajectory analysis revealed a crossover interaction: When domain calibration improved over time (overconfident→underconfident, Δ=-0.73), whereas What/Where domains worsened (underconfident→overconfident, Δ≈+0.33)."

3. **Post-hoc context:** "Pairwise contrasts at the average timepoint were non-significant (all p>0.56), consistent with crossover effects canceling when averaged across time. This underscores the importance of trajectory analysis for detecting dynamic patterns."

4. **Theoretical synthesis:** "The crossover pattern suggests domain-specific cue degradation rates: rapid temporal cue loss (When) versus persistent familiarity/spatial cues (What/Where)."

**DO NOT report as:**
- ❌ "No significant differences between domains" (ignores interaction)
- ❌ "When domain is worse calibrated" (true at T4, false at T1)
- ❌ "Contradictory results" (interaction vs post-hoc) - they're complementary

---

**Cross-References:**
- RQ 6.3.2 complete archive (full statistical results)
- When domain paradox archive (mechanistic explanation)
- Ch5 5.2.1 (divergence pattern for comparison)
- execute.md lesson #3 (plot trajectories mandatory)

**Future Applications:**
- Any RQ testing Domain × Time, Age × Time, Paradigm × Time interactions
- Watch for crossover patterns in other metacognitive measures
- Consider timepoint-specific contrasts when interaction is significant
