# REMEMVR Tools - Statistical Analysis Toolkit

## Overview

The `tools/` package provides a modular suite of functions for analyzing REMEMVR episodic memory data. All tools are designed to be:
- **Testable** - Unit tested with pytest
- **Modular** - Import only what you need
- **Documented** - Clear docstrings and examples
- **CLI-accessible** - Can be called from command line or Python

## Module Organization

### Data Preparation
| Module | Purpose | Key Functions |
|--------|---------|---------------|
| **data_extraction.py** | Extract tags from master.xlsx | `extract_tags()`, `extract_participant_data()` |
| **data_validation.py** | Validate data quality | `check_missing()`, `detect_outliers()` |
| **data_preprocessing.py** | Transform and preprocess | `dichotomize()`, `compute_svr()`, `create_composite_id()` |

### Statistical Analysis
| Module | Purpose | Key Functions |
|--------|---------|---------------|
| **analysis_irt.py** | Item Response Theory (deepirtools) | `calibrate_grm()`, `score_theta()` |
| **analysis_lmm.py** | Linear Mixed Models (statsmodels) | `fit_trajectory()`, `compare_models()` |
| **analysis_ctt.py** | Classical Test Theory | `compute_sum_score()`, `fit_trajectory_ctt()` |

### Visualization
| Module | Purpose | Key Functions |
|--------|---------|---------------|
| **plot_trajectories.py** | Forgetting curves | `forgetting_curve()`, `domain_comparison()` |
| **plot_diagnostics.py** | Model diagnostics | `residual_plot()`, `qq_plot()` |
| **plot_distributions.py** | Data distributions | `item_difficulty()`, `theta_distribution()` |

### Utilities
| Module | Purpose | Key Functions |
|--------|---------|---------------|
| **utils.py** | General utilities | `load_config()`, `save_results()`, `format_pvalue()` |
| **cli.py** | Command-line interface | CLI wrappers for all tools |

## Installation

Install as editable package for development:
```bash
pip install -e .
```

Or install with dependencies:
```bash
pip install -e ".[dev]"
```

## Usage Examples

### Python API
```python
from tools import data_extraction, analysis_irt, plot_trajectories

# Extract item data
tags = ['TQ-IFR-i1-N', 'TQ-IFR-i2-N', 'TQ-IFR-i3-N']
df = data_extraction.extract_tags(tags)

# Calibrate IRT model
results = analysis_irt.calibrate_grm(
    data=df,
    model='GRM',
    dichotomous=True
)

# Plot forgetting curve
plot_trajectories.forgetting_curve(
    theta=results['theta'],
    time=df['SVR'],
    output='results/ch5/rq1/plots/trajectory.png'
)
```

### Command Line Interface
```bash
# Extract data
python tools/cli.py extract --tags "TQ-IFR-i1-N,TQ-IFR-i2-N" --output data.csv

# Run IRT analysis
python tools/cli.py irt --input data.csv --output results.csv

# Fit LMM trajectory
python tools/cli.py lmm --input theta.csv --formula "theta ~ SVR" --output lmm.csv

# Generate plots
python tools/cli.py plot --input results.csv --type trajectory --output plot.png
```

## Configuration

Tools load configuration from `config/` directory:
- `config/paths.yaml` - Data and output paths
- `config/models.yaml` - Default model parameters
- `config/plotting.yaml` - Plot styling
- `config/logging.yaml` - Logging configuration

Override defaults with RQ-specific configs:
```python
from tools import utils

config = utils.load_config('results/ch5/rq1/config.yaml')
results = analysis_irt.calibrate_grm(data, **config['irt'])
```

## Testing

Run all tests:
```bash
pytest tests/ -v
```

Run specific module tests:
```bash
pytest tests/test_data_extraction.py -v
```

Run with coverage:
```bash
pytest tests/ --cov=tools --cov-report=html
```

## Development Status

**Phase 1 (CURRENT):** Structure creation, placeholder files
**Phase 2:** Archive legacy code
**Phase 3:** Create MIGRATION.md with function mappings
**Phase 4:** Implement tools (TDD approach)
**Phase 5+:** Integration and RQ execution

## Function Extraction Map

Functions will be extracted from legacy code:
- `irt.py` → `analysis_irt.py`, `analysis_lmm.py`
- `analysis.py` → `analysis_ctt.py`, `utils.py`
- `plots.py` → `plot_trajectories.py`, `plot_diagnostics.py`, `plot_distributions.py`
- `tools.py` → `data_preprocessing.py`
- `data/data.py` → `data_extraction.py` (adapt/fix bugs)

See `MIGRATION.md` for detailed function-level tracking (to be created in Phase 3).

## Contributing

Follow TDD workflow:
1. **Write test first** (in `tests/test_[module].py`)
2. **Run test** (should fail)
3. **Implement function** (simplest solution)
4. **Run test** (should pass)
5. **Refactor** (beautify, integrate)

See `.claude/claude.md` for detailed development methodology.

## References

- **IRT Methodology:** `docs/irt_methodology.md`
- **LMM Methodology:** `docs/lmm_methodology.md`
- **Data Structure:** `docs/data_structure.md`
- **Cognitive Tests:** `docs/cognitive_tests.md`

## License

PhD Thesis Project - All Rights Reserved
