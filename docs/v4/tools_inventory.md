# Tools Inventory (v4.X)

**Version:** 4.0
**Last Updated:** 2025-11-22
**Purpose:** Authoritative API reference for VALIDATED analysis tools (YELLOW/GREEN only)
**Source of Truth:** `/home/etai/projects/REMEMVR/docs/v4/tools_status.tsv`

---

## Module: tools.analysis_irt

### prepare_irt_input_from_long

| Field | Value |
|-------|-------|
| **Description** | Convert long-format DataFrame to IRT tensors for IWAVE model fitting |
| **Inputs** | `df_long: DataFrame` (long format with composite_ID, item, response), `groups: Dict[str, List[str]]` (factor -> item mapping) |
| **Outputs** | `Tuple[Tensor, Tensor, Tensor, List, List]` (response_matrix, missing_mask, Q_matrix, composite_ids, item_list) |

### configure_irt_model

| Field | Value |
|-------|-------|
| **Description** | Build IWAVE Graded Response Model with specified architecture |
| **Inputs** | `n_items: int`, `n_factors: int`, `n_cats: int`, `Q_matrix: Tensor`, `correlated_factors: bool`, `device: str`, `seed: int` |
| **Outputs** | `IWAVE` model object |

### fit_irt_grm

| Field | Value |
|-------|-------|
| **Description** | Fit IRT model via variational inference (IWAVE algorithm) |
| **Inputs** | `model: IWAVE`, `response_matrix: Tensor`, `missing_mask: Tensor`, `batch_size: int`, `iw_samples: int`, `mc_samples: int` |
| **Outputs** | `IWAVE` fitted model |

### extract_theta_from_irt

| Field | Value |
|-------|-------|
| **Description** | Extract participant ability estimates (theta scores) from fitted model |
| **Inputs** | `model: IWAVE`, `response_matrix: Tensor`, `missing_mask: Tensor`, `composite_ids: List`, `factor_names: List`, `scoring_batch_size: int`, `mc_samples: int`, `iw_samples: int`, `invert_scale: bool` |
| **Outputs** | `DataFrame` with columns: composite_ID, domain_name, theta |

### extract_parameters_from_irt

| Field | Value |
|-------|-------|
| **Description** | Extract item parameters (discrimination a, difficulty b) from fitted model |
| **Inputs** | `model: IWAVE`, `item_list: List`, `factor_names: List`, `n_cats: int` |
| **Outputs** | `DataFrame` with columns: item, domain, Discrimination, Difficulty_1...Difficulty_k |

### calibrate_irt

| Field | Value |
|-------|-------|
| **Description** | Full IRT pipeline: prepare -> configure -> fit -> extract (convenience wrapper) |
| **Inputs** | `df_long: DataFrame`, `groups: Dict[str, List[str]]`, `config: dict` (irt_config with model params) |
| **Outputs** | `Tuple[DataFrame, DataFrame]` (theta_scores, item_parameters) |

### filter_items_by_quality

| Field | Value |
|-------|-------|
| **Description** | D039: Purify items by quality thresholds for 2-pass IRT calibration |
| **Inputs** | `df_items: DataFrame` (item parameters), `a_threshold: float` (default 0.4), `b_threshold: float` (default 3.0) |
| **Outputs** | `Tuple[DataFrame, DataFrame]` (retained_items, removed_items) |

### calibrate_grm

| Field | Value |
|-------|-------|
| **Description** | Backwards-compatible wrapper for calibrate_irt() |
| **Inputs** | `df_long: DataFrame`, `groups: Dict[str, List[str]]`, `config: dict` |
| **Outputs** | `Tuple[DataFrame, DataFrame]` (theta_scores, item_parameters) |

---

## Module: tools.analysis_lmm

### prepare_lmm_input_from_theta

| Field | Value |
|-------|-------|
| **Description** | DEPRECATED: Convert theta scores from wide to long format with nominal days. Violates D070. |
| **Inputs** | `theta_scores: DataFrame` (wide format with UID, test, Theta_* columns), `factors: List[str]` (optional filter) |
| **Outputs** | `DataFrame` with columns: UID, test, Factor, Ability, Days, Days_sq, log_Days |
| **Warning** | Use `fit_lmm_trajectory_tsvr()` instead for REMEMVR analyses |

### configure_candidate_models

| Field | Value |
|-------|-------|
| **Description** | Generate formulas for 5 candidate LMM models |
| **Inputs** | `n_factors: int` (1=single domain, >1=multiple), `reference_group: str` (required if n_factors > 1) |
| **Outputs** | `Dict[str, Dict[str, str]]` with keys: Linear, Quadratic, Log, Lin+Log, Quad+Log; each containing formula and re_formula |

### fit_lmm_trajectory_tsvr

| Field | Value |
|-------|-------|
| **Description** | D070: Fit LMM using TSVR (actual hours since encoding) as time variable |
| **Inputs** | `theta_scores: DataFrame` (composite_ID, domain_name, theta), `tsvr_data: DataFrame` (UID, Test, TSVR_hours), `formula: str`, `groups: str` (default 'UID'), `re_formula: str` (default '~Days'), `reml: bool` (default False) |
| **Outputs** | `MixedLMResults` object |

### compare_lmm_models_by_aic

| Field | Value |
|-------|-------|
| **Description** | Fit all 5 candidate models, compare by AIC, return best model |
| **Inputs** | `data: DataFrame`, `n_factors: int`, `reference_group: str`, `groups: str`, `save_dir: Path` |
| **Outputs** | `Dict` with keys: models (all fitted), aic_comparison (DataFrame), best_model (name), best_result (MixedLMResults) |

### extract_fixed_effects_from_lmm

| Field | Value |
|-------|-------|
| **Description** | Extract fixed effects table from fitted LMM |
| **Inputs** | `result: MixedLMResults` |
| **Outputs** | `DataFrame` with columns: effect, coefficient, std_error, z_value, p_value |

### extract_random_effects_from_lmm

| Field | Value |
|-------|-------|
| **Description** | Extract random effects variance components and ICC |
| **Inputs** | `result: MixedLMResults` |
| **Outputs** | `Dict` with keys: variance_components (Dict), icc (float) |

### compute_contrasts_pairwise

| Field | Value |
|-------|-------|
| **Description** | D068: Post-hoc pairwise contrasts with dual p-value reporting |
| **Inputs** | `lmm_result: MixedLMResults`, `comparisons: List[str]` (e.g., ["Where-What", "When-What"]), `family_alpha: float` (default 0.05) |
| **Outputs** | `DataFrame` with columns: comparison, beta, se, z, p_uncorrected, alpha_corrected, p_corrected, sig_uncorrected, sig_corrected |

### compute_effect_sizes_cohens

| Field | Value |
|-------|-------|
| **Description** | Compute Cohen's f-squared effect sizes for LMM fixed effects |
| **Inputs** | `lmm_result: MixedLMResults`, `include_interactions: bool` (default False) |
| **Outputs** | `DataFrame` with columns: effect, f_squared, interpretation (negligible/small/medium/large) |

---

## Module: tools.plotting

### convert_theta_to_probability

| Field | Value |
|-------|-------|
| **Description** | Transform theta scores to probability scale via IRT 2PL formula |
| **Inputs** | `theta: ndarray`, `discrimination: float` (default 1.0), `difficulty: float` (default 0.0) |
| **Outputs** | `ndarray` of probabilities in range [0, 1] |

---

## Module: tools.validation

### validate_irt_convergence

| Field | Value |
|-------|-------|
| **Description** | Check IRT model convergence based on loss stability and parameter bounds |
| **Inputs** | `results: Dict[str, Any]` (containing loss_history, model parameters) |
| **Outputs** | `Dict[str, Any]` with keys: converged (bool), checks (list of check results), message (str) |

### validate_irt_parameters

| Field | Value |
|-------|-------|
| **Description** | Validate item parameters against quality thresholds |
| **Inputs** | `df_items: DataFrame`, `a_min: float` (default 0.4), `b_max: float` (default 3.0), `a_col: str` (default 'Discrimination'), `b_col: str` (default 'Difficulty') |
| **Outputs** | `Dict[str, Any]` with keys: valid (bool), n_items, n_valid, n_invalid, invalid_items (list), message (str) |

### validate_lmm_convergence

| Field | Value |
|-------|-------|
| **Description** | Check LMM model convergence status and warnings |
| **Inputs** | `lmm_result: MixedLMResults` |
| **Outputs** | `Dict[str, Any]` with keys: converged (bool), message (str), warnings (list) |

### validate_lmm_residuals

| Field | Value |
|-------|-------|
| **Description** | Test LMM residuals for normality using Kolmogorov-Smirnov test |
| **Inputs** | `residuals: ndarray`, `alpha: float` (default 0.05) |
| **Outputs** | `Dict[str, Any]` with keys: normal (bool), ks_statistic (float), p_value (float), message (str) |

---

**End of Tools Inventory**
