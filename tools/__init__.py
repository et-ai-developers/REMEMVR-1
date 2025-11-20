"""
REMEMVR - Statistical Analysis Tools Package

A modular toolkit for analyzing episodic memory data from the REMEMVR study.

Modules:
- data_extraction: Extract tags from master.xlsx using data.py
- data_validation: Validate extracted data quality
- data_preprocessing: Preprocess and transform data
- analysis_irt: Item Response Theory analysis (GRM models)
- analysis_lmm: Linear Mixed Models for trajectory analysis
- analysis_ctt: Classical Test Theory scoring
- config: Configuration management (paths, plotting, models)
- plotting: Generic plotting functions (trajectories, diagnostics, histograms)
- validation: Statistical validation and lineage tracking
- utils: General utility functions
- cli: Command-line interface wrappers

Usage:
    from tools import data_extraction, analysis_irt, plot_trajectories

    # Extract data
    df = data_extraction.extract_tags(['TQ-IFR-i1-N', 'TQ-IFR-i2-N'])

    # Run IRT analysis
    results = analysis_irt.calibrate_grm(df)

    # Plot trajectories
    plot_trajectories.forgetting_curve(results)

Installation:
    pip install -e .

Development:
    pytest tests/ -v

Version: 1.0.0 (Refactored 2025-01-04)
"""

__version__ = "1.0.0"
__author__ = "REMEMVR Project"

# Import key functions
# from .data_extraction import extract_tags  # Phase 3
from .analysis_irt import (
    prepare_irt_data,
    configure_irt_model,
    fit_irt_model,
    extract_theta_scores,
    extract_item_parameters,
    calibrate_irt
)
# from .plot_trajectories import forgetting_curve  # Future

# LMM analysis exports
from .analysis_lmm import (
    prepare_lmm_data,
    configure_candidate_models,
    fit_lmm_model,
    compare_models,
    extract_fixed_effects,
    extract_random_effects,
    run_lmm_analysis
)

# Config management exports
from .config import (
    load_config,
    get_config,
    get_path
)

# Plotting exports
from .plotting import (
    setup_plot_style,
    plot_trajectory,
    plot_diagnostics,
    plot_histogram_by_group,
    theta_to_probability,
    save_plot_with_data
)

# Validation exports
from .validation import (
    create_lineage_metadata,
    save_lineage,
    load_lineage,
    validate_lineage,
    validate_irt_convergence,
    validate_irt_parameters,
    check_missing_data,
    validate_lmm_convergence,
    validate_lmm_residuals,
    validate_data_columns,
    validate_file_exists,
    validate_numeric_range,
    generate_validation_report,
    save_validation_report
)

__all__ = [
    # IRT Analysis (Phase 8 - MVP Phase 1)
    'prepare_irt_data',
    'configure_irt_model',
    'fit_irt_model',
    'extract_theta_scores',
    'extract_item_parameters',
    'calibrate_irt',
    # LMM Analysis (Phase 8 - MVP Phase 2)
    'prepare_lmm_data',
    'configure_candidate_models',
    'fit_lmm_model',
    'compare_models',
    'extract_fixed_effects',
    'extract_random_effects',
    'run_lmm_analysis',
    # Config Management (Automation Phase 1)
    'load_config',
    'get_config',
    'get_path',
    # Plotting (Automation Phase 1)
    'setup_plot_style',
    'plot_trajectory',
    'plot_diagnostics',
    'plot_histogram_by_group',
    'theta_to_probability',
    'save_plot_with_data',
    # Validation (Automation Phase 1)
    'create_lineage_metadata',
    'save_lineage',
    'load_lineage',
    'validate_lineage',
    'validate_irt_convergence',
    'validate_irt_parameters',
    'check_missing_data',
    'validate_lmm_convergence',
    'validate_lmm_residuals',
    'validate_data_columns',
    'validate_file_exists',
    'validate_numeric_range',
    'generate_validation_report',
    'save_validation_report',
]
