# Results Schema

**Last Updated:** 2025-01-11
**Purpose:** Documents the standardized RQ folder structure and info.md template
**Audience:** Results-inspector agent, main claude
**Status:** Current

---

## NEW RESULTS SCHEMA

**Structure:**
```
results/
├── ch5/ (Chapter 5: Trajectory of Episodic Forgetting)
│   ├── rq1/ (RQ 5.1: Do domains show different forgetting trajectories?)
│   │   ├── info.md (Methodology, results summary, scholarly answer)
│   │   ├── data/
│   │   │   ├── input.csv (Data prepared by data-prep agent)
│   │   │   ├── output_1.csv (After step 1 of analysis)
│   │   │   ├── output_2.csv (After step 2 of analysis)
│   │   │   └── output.csv (Final results)
│   │   ├── code/
│   │   │   ├── run.py (Sequential analysis script)
│   │   │   └── terminal.log (Full execution log)
│   │   └── plots/
│   │       ├── trajectory_plot.png
│   │       └── trajectory_plot_data.csv (For regeneration)
│   ├── rq2/
│   └── ...
├── ch6/ (Chapter 6: Metacognition in Episodic Memory)
│   ├── rq1/
│   └── ...
└── ch7/ (Chapter 7: Individual Differences)
    ├── rq1/
    └── ...
```

### Enhanced RQ Folder Structure

Each RQ (e.g., `results/ch5/rq1/`) contains:

```
rq1/
├── config.yaml          # RQ-specific configuration (variables, models, parameters)
├── status.json          # Execution status tracking (pending/in_progress/completed/failed)
├── info.md              # Final report (methodology, results, interpretation)
├── data/
│   ├── input.csv
│   ├── intermediate_*.csv
│   └── output.csv
├── code/
│   └── run.py
├── plots/
│   ├── *.png
│   └── plot_data/
├── logs/                # SEPARATED: Agent logs vs analysis logs
│   ├── agent_data_prep.log
│   ├── agent_executor.log
│   ├── agent_inspector.log
│   └── analysis_terminal.log
└── validation/          # Validation outputs
    ├── report.md
    ├── diagnostics/
    └── checks/
```

---

## info.md Template

```markdown
# RQ [Number]: [Question Title]

## Research Question
[Full text of research question]

## Hypothesis
[Expected outcome]

## Methodology
[Statistical approach, models used, justification]

## Data Prepared
[Description of input.csv: variables, format, filters applied]

## Analysis Steps
[Sequential list of what was done]

## Raw Results
[Model outputs, coefficients, p-values, effect sizes]

## Validation Checks
[Assumptions tested, diagnostics, issues found/resolved]

## Interpretation
[Scholarly answer to the research question - draft thesis text]

## References
[Relevant citations for methodology]
```
