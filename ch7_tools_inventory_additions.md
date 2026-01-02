# Ch7 Tools Inventory Additions

## Summary
- **32 new tools** needed for Ch7 (29 RED, 2 ORANGE, 1 YELLOW)
- **5 new modules** to create/expand
- **Blocks 32 Ch7 RQs** from execution

## New Modules Required

### 1. `tools/analysis_regression.py` (NEW MODULE)
Core regression analysis functionality - **CRITICAL PRIORITY**

```python
def fit_multiple_regression(X: np.ndarray, y: np.ndarray, feature_names: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Fit multiple linear regression with comprehensive diagnostics.
    
    Args:
        X: Predictor matrix (n_samples, n_features)
        y: Target vector (n_samples,)
        feature_names: Optional names for predictors
        
    Returns:
        Dictionary containing:
        - coefficients: Beta coefficients
        - p_values: P-values for each coefficient
        - r_squared: R² value
        - adjusted_r_squared: Adjusted R²
        - residuals: Model residuals
        - fitted_values: Fitted y values
        - model: Fitted statsmodels OLS object
    """
    
def fit_hierarchical_regression(X_blocks: List[np.ndarray], y: np.ndarray, block_names: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Fit hierarchical/block regression with incremental validity testing.
    
    Args:
        X_blocks: List of predictor matrices for each block
        y: Target vector
        block_names: Optional names for blocks
        
    Returns:
        Dictionary containing:
        - models: List of fitted models for each block
        - delta_r2: R² change for each block
        - f_tests: F-tests for R² change significance
        - cumulative_r2: Cumulative R² at each block
    """

def compute_regression_diagnostics(model: Any, X: np.ndarray, y: np.ndarray) -> Dict[str, Any]:
    """
    Compute comprehensive regression diagnostics.
    
    Returns:
        Dictionary containing:
        - vif: Variance Inflation Factors
        - cooks_d: Cook's distance values
        - leverage: Leverage values
        - durbin_watson: Durbin-Watson statistic
        - shapiro_wilk: Normality test for residuals
        - breusch_pagan: Homoscedasticity test
    """

def cross_validate_regression(X: np.ndarray, y: np.ndarray, n_folds: int = 5, seed: int = 42) -> Dict[str, Any]:
    """5-fold cross-validation for regression."""

def bootstrap_regression_ci(X: np.ndarray, y: np.ndarray, n_bootstrap: int = 1000, seed: int = 42) -> Dict[str, Any]:
    """Bootstrap confidence intervals for regression coefficients."""

def compute_cohens_f2(r2_full: float, r2_reduced: float) -> float:
    """Cohen's f² effect size for hierarchical regression."""

def compute_post_hoc_power(n: int, k_predictors: int, r2: float, alpha: float = 0.05) -> float:
    """Post-hoc power analysis for regression."""
```

### 2. `tools/analysis_lpa.py` (NEW MODULE)
Latent Profile Analysis functionality

```python
def fit_lpa_models(X: np.ndarray, k_range: range = range(2, 6), seed: int = 42) -> Dict[str, Any]:
    """
    Fit Latent Profile Analysis models with multiple K values.
    
    Args:
        X: Data matrix for profiles
        k_range: Range of K (number of profiles) to test
        seed: Random seed for reproducibility
        
    Returns:
        Dictionary containing:
        - models: Dict of fitted GaussianMixture models by K
        - bic_scores: BIC for each K
        - aic_scores: AIC for each K
        - entropy_scores: Entropy for each K
        - best_k: Optimal K based on BIC
    """

def extract_profile_membership(model: Any) -> np.ndarray:
    """Extract profile assignments from fitted LPA model."""

def compute_entropy(model: Any, X: np.ndarray) -> float:
    """Compute entropy (0-1) for LPA model quality."""
```

### 3. `tools/data.py` (EXPAND EXISTING)
Add cognitive test and specialized extractors

```python
def extract_cognitive_tests(master_path: str, uid_list: Optional[List[str]] = None) -> pd.DataFrame:
    """
    Extract RAVLT, BVMT, NART, RPM from master.xlsx.
    
    Returns:
        DataFrame with columns: uid, ravlt_total, bvmt_total, nart, rpm
        Scores converted to T-scores (M=50, SD=10)
    """

def extract_domain_theta_scores(rq_path: str, domain: str = 'All') -> pd.DataFrame:
    """Extract domain-specific theta scores from Ch5 results."""

def extract_dass_scores(master_path: str, uid_list: Optional[List[str]] = None) -> pd.DataFrame:
    """Extract DASS-21 subscale scores."""

def extract_sleep_per_test(master_path: str, uid_list: Optional[List[str]] = None, test_num: int = 1) -> pd.DataFrame:
    """Extract per-test sleep hours."""

def standardize_to_t_scores(scores: np.ndarray, population_mean: float = None, population_sd: float = None) -> np.ndarray:
    """Convert raw scores to T-scores (M=50, SD=10)."""
```

### 4. `tools/analysis_stats.py` (EXPAND EXISTING)
Add D068-compliant statistical tests

```python
def one_way_anova_d068(groups: List[np.ndarray], correction: str = 'bonferroni') -> Dict[str, Any]:
    """
    One-way ANOVA with dual p-value reporting (Decision D068).
    
    Returns:
        Dictionary containing:
        - f_statistic: F-statistic
        - p_uncorrected: Uncorrected p-value
        - p_corrected: Bonferroni-corrected p-value
        - eta_squared: Effect size
        - df_between: Degrees of freedom between
        - df_within: Degrees of freedom within
    """

def chi_square_test_d068(contingency_table: np.ndarray) -> Dict[str, Any]:
    """Chi-square test with dual p-value reporting."""

def compute_cramers_v(chi2: float, n: int, k: int) -> float:
    """Cramér's V effect size for contingency tables."""
```

### 5. `tools/bootstrap.py` (NEW MODULE)
Specialized bootstrap procedures

```python
def bootstrap_correlation_ci(x: np.ndarray, y: np.ndarray, n_bootstrap: int = 1000, seed: int = 42) -> Dict[str, Any]:
    """Bootstrap confidence intervals for correlations."""

def bootstrap_icc_ci(data: pd.DataFrame, n_bootstrap: int = 1000, seed: int = 42) -> Dict[str, Any]:
    """Bootstrap confidence intervals for ICC."""
```

## Integration with Existing Tools

### Tools that already exist (need verification):
- `tools.analysis_lmm.fit_lmm_trajectory_tsvr` ✅ (GREEN from Ch5)
- `tools.analysis_ctt.compute_pearson_correlations_with_correction` ✅ (GREEN from Ch5)
- `tools.validation.validate_lmm_assumptions_comprehensive` 🟡 (YELLOW from Ch5)

### Tools to import from standard libraries:
```python
# Can use directly without wrapper:
from scipy import stats
from statsmodels.api import OLS
from sklearn.model_selection import KFold
from sklearn.mixture import GaussianMixture
```

## Testing Requirements

Each new tool needs:
1. **Unit tests** (minimum 5 test cases)
2. **Edge case tests** (null data, perfect correlation, singularities)
3. **Integration test** (with real Ch7 data subset)
4. **Performance test** (N=100, typical Ch7 size)
5. **Reproducibility test** (seed consistency)

## Documentation Requirements

For each tool, add to:
1. `docs/v4/tools_inventory.md` - Full API documentation
2. `docs/v4/tools_catalog.md` - One-line description
3. `docs/v4/tools_status.tsv` - Status tracking (RED→ORANGE→YELLOW→GREEN)
4. `results/ch7/*/3_tools.yaml` - RQ-specific tool specifications

## Priority Implementation Order

### Week 1: Unblock majority of RQs
1. `fit_multiple_regression` - Blocks 7.1.1, 7.1.3, 7.1.4
2. `extract_cognitive_tests` - Blocks all 7.1.x, 7.2.x
3. `cross_validate_regression` - Required by 10+ RQs
4. `bootstrap_regression_ci` - Required by 15+ RQs

### Week 2: Complete specialized needs
5. `fit_hierarchical_regression` - Blocks 7.1.4, 7.3.x
6. `fit_lpa_models` - Blocks 7.8.x
7. `one_way_anova_d068` - Blocks 7.3.5, 7.7.x
8. Effect sizes and power calculations

### Week 3: Polish and validation
9. Remaining data extractors
10. Plotting tools (lower priority)
11. Clinical utility tools
12. Final validation with Ch7 RQ execution