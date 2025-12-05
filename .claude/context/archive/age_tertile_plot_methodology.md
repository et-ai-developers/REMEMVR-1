# Age Tertile Plot Methodology

**Topic:** age_tertile_plot_methodology
**Created:** 2025-12-05 (context-manager archival)
**Description:** Methodology for creating age tertile trajectory plots with factor-specific IRT probability conversion.

---

## pd.qcut 33rd/67th Percentiles, Young/Middle/Older Labels (2025-12-05 14:00)

**Archived from:** state.md Session (2025-12-05 14:00)
**Original Date:** 2025-12-05 14:00
**Reason:** Methodology documented, 24 rows complete factorial

### Age Tertile Creation

**Method:** pd.qcut(Age, q=3, labels=['Young', 'Middle', 'Older'])

- **Young:** Age ≤ 33rd percentile
- **Middle:** 33rd < Age ≤ 67th percentile
- **Older:** Age > 67th percentile

**Ensures equal group sizes:**
- Young: 33 participants
- Middle: 34 participants
- Older: 33 participants

**RQ 5.5.3 Cutoffs:**
- Young: ≤37 years (33 participants)
- Middle: 37-52 years (34 participants)
- Older: >52 years (33 participants)

### Plot Data Structure (24 Rows Complete Factorial)

**Dimensions:**
- 3 age tertiles (Young, Middle, Older)
- 2 locations (Source, Destination)
- 4 tests (0, 1, 3, 6 days)

**Total:** 3 × 2 × 4 = 24 rows

**Columns:**
- AgeTertile (categorical: Young/Middle/Older)
- LocationType (categorical: Source/Destination)
- Test (integer: 0, 1, 3, 6)
- TSVR_hours (continuous: actual hours since encoding)
- theta_mean (mean IRT theta for group)
- theta_se (standard error)
- theta_ci_lower (95% CI lower bound)
- theta_ci_upper (95% CI upper bound)
- probability_mean (mean probability, **FACTOR-SPECIFIC conversion**)
- probability_se (standard error on probability scale)
- probability_ci_lower (95% CI lower bound)
- probability_ci_upper (95% CI upper bound)

### Factor-Specific IRT Probability Conversion

**CRITICAL:** Must use location-specific item parameters

```python
# Extract factor-specific parameters
FACTOR_PARAMS = {
    'Source': {
        'discrimination': item_params[item_params['LocationType']=='Source']['Discrimination'].mean(),
        'difficulty': item_params[item_params['LocationType']=='Source']['Difficulty'].mean()
    },
    'Destination': {
        'discrimination': item_params[item_params['LocationType']=='Destination']['Discrimination'].mean(),
        'difficulty': item_params[item_params['LocationType']=='Destination']['Difficulty'].mean()
    }
}

# Apply conversion
for loc in ['Source', 'Destination']:
    mask = plot_data['LocationType'] == loc
    params = FACTOR_PARAMS[loc]

    plot_data.loc[mask, 'probability_mean'] = convert_theta_to_probability(
        plot_data.loc[mask, 'theta_mean'],
        discrimination=params['discrimination'],
        difficulty=params['difficulty']  # LOCATION-SPECIFIC!
    )
```

**Why this matters:**
- Source items easier (b = -0.453) → higher probability for same theta
- Destination items harder (b = +1.371) → lower probability for same theta
- Using difficulty=0.0 for all would mask 30-45 percentage point baseline difference

### Validation

Compare plot probabilities to raw accuracy:
- Source should show ~70% baseline (Day 0), declining to ~45% (Day 6)
- Destination should show ~40% baseline, declining to ~25%
- If both show similar probabilities, conversion is WRONG

### Cross-RQ Applications

This methodology applies to:
- RQ 5.5.3 (Source-Destination age tertiles)
- RQ 5.3.4 (Paradigm age tertiles)
- RQ 5.4.3 (Congruence age tertiles)
- Any plot showing Age × Factor × Time trajectories

### Files

**RQ 5.5.3:**
- results/ch5/5.5.3/data/step05_age_tertile_plot_data.csv (24 rows)
- results/ch5/5.5.3/plots/age_tertile_trajectory_theta.png
- results/ch5/5.5.3/plots/age_tertile_trajectory_probability.png
- results/ch5/5.5.3/plots/age_tertile_dual_scale.png

---
