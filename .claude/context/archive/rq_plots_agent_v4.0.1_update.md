# RQ Plots Agent v4.0.1 Update

**Topic:** rq_plots_agent_v4.0.1_update
**Created:** 2025-12-05 (context-manager archival)
**Description:** rq_plots agent enhancement adding critical multi-dimensional IRT probability conversion guidance.

---

## Critical Section Added After Multi-Dimensional IRT Bug Discovery (2025-12-05 12:30)

**Archived from:** state.md Session (2025-12-05 12:30)
**Original Date:** 2025-12-05 12:30
**Reason:** Agent update complete, version documented

### Agent Update

Added critical section to `.claude/agents/rq_plots.md`:

**"CRITICAL: Multi-Dimensional IRT Probability Conversion"**

Contents:
- Explains the problem (factor-specific difficulties create different theta scales)
- Shows the wrong approach (difficulty=0.0 for all)
- Shows the correct approach (loop through factors with factor-specific b values)
- Lists when this applies (2+ factor IRT models)
- Includes validation guidance (compare to raw accuracy)
- Documents lesson learned with RQ 5.5.1 example

**Version History Updated:** v4.0.1 (2025-12-05) with bug description and fix

### Code Example in Agent

```python
# CRITICAL: For multi-dimensional IRT (2+ factors)
# NEVER use difficulty=0.0 for all factors

# Extract factor-specific parameters from item_params
FACTOR_PARAMS = {}
for factor in df['FactorName'].unique():
    factor_items = item_params[item_params['Factor'] == factor]
    FACTOR_PARAMS[factor] = {
        'discrimination': factor_items['Discrimination'].mean(),
        'difficulty': factor_items['Difficulty'].mean()  # FACTOR-SPECIFIC!
    }

# Apply factor-specific conversion
for factor in df['FactorName'].unique():
    mask = df['FactorName'] == factor
    params = FACTOR_PARAMS[factor]
    df.loc[mask, 'probability'] = convert_theta_to_probability(
        df.loc[mask, 'theta'].values,
        discrimination=params['discrimination'],
        difficulty=params['difficulty']
    )
```

### Validation Check

Agent now includes guidance to compare probability-scale results to raw accuracy:
- If factor A has ~70% raw accuracy but plots show ~25%, conversion is wrong
- If factor B has ~25% raw accuracy, that should be reflected in plots
- Multi-factor IRT absorbs difficulty differences into item parameters (invisible in theta)

### Lesson Learned Documentation

RQ 5.5.1 example shows this error masked a 30-45 percentage point effect. User observed previous analyses showed significant intercept difference when scaled to probability, but RQ 5.5.1 showed null main effect. Investigation revealed the probability conversion bug.

**Key Principle:** Different theta scales (from different item difficulty distributions) require factor-specific parameters for probability conversion.

---
