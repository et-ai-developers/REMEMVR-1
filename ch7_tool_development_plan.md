# Ch7 Tool Development Plan

## Overview
- **Total Tools Needed:** 32 unique tools
- **Current Status:** 29 RED, 2 ORANGE, 1 YELLOW
- **Critical Path:** Regression tools block 15+ RQs

## Tool Status Color Coding
- 🔴 **RED:** Not implemented
- 🟠 **ORANGE:** Basic implementation, not validated  
- 🟡 **YELLOW:** Tested and documented
- 🟢 **GREEN:** Production-validated through RQ execution

## Priority Levels
- **CRITICAL:** Blocks 5+ RQs, needed immediately
- **HIGH:** Blocks 2-4 RQs, needed soon
- **MEDIUM:** Blocks 1-2 RQs, can be deferred
- **LOW:** Nice to have, plotting/convenience

---

## Phase 1: Critical Regression Infrastructure (Week 1)
**Goal:** Unblock 15+ RQs that need regression analysis

### 🔴 → 🟢 Core Regression Module
```python
# tools/analysis_regression.py
def fit_multiple_regression(X, y, feature_names=None):
    """Statsmodels OLS wrapper with diagnostics"""
    # Implementation: statsmodels.api.OLS
    # Returns: coefficients, p-values, R², residuals
    
def fit_hierarchical_regression(X_blocks, y, block_names=None):
    """Sequential block regression with ΔR² tests"""
    # Implementation: Sequential OLS fits
    # Returns: models list, ΔR², F-tests
    
def compute_regression_diagnostics(model, X, y):
    """VIF, Cook's D, leverage, assumptions"""
    # Implementation: statsmodels.stats
    # Returns: diagnostic dictionary
```

**Test Requirements:**
- [ ] Test with N=100, k=4 predictors (typical Ch7 case)
- [ ] Test hierarchical with 3 blocks
- [ ] Test VIF calculation accuracy
- [ ] Test Cook's D threshold detection
- [ ] Edge cases: Perfect collinearity, singular matrix

### 🔴 → 🟢 Cross-Validation & Bootstrap
```python
# tools/analysis_regression.py (continued)
def cross_validate_regression(X, y, n_folds=5, seed=42):
    """K-fold CV with reproducible splits"""
    # Implementation: sklearn.model_selection.KFold
    # Returns: CV scores, mean R², std R²
    
def bootstrap_regression_ci(X, y, n_bootstrap=1000, seed=42):
    """Bootstrap CIs for coefficients"""
    # Implementation: scipy.stats.bootstrap
    # Returns: CI bounds, bootstrap samples
```

**Test Requirements:**
- [ ] Test CV reproducibility (same seed = same splits)
- [ ] Test bootstrap CI coverage (95% nominal = 95% actual)
- [ ] Test with small samples (N=20)
- [ ] Test with perfect prediction (R²=1.0)

---

## Phase 2: Data Extraction Tools (Week 1-2)
**Goal:** Enable loading of cognitive tests and theta scores

### 🔴 → 🟢 Master.xlsx Extractors
```python
# tools/data.py
def extract_cognitive_tests(master_path, uid_list=None):
    """Extract RAVLT, BVMT, NART, RPM scores"""
    # Tags: {UID}-COG-S1-RAV-*, {UID}-COG-S1-BVM-*, etc.
    # Returns: DataFrame with T-scores
    
def extract_dass_scores(master_path, uid_list=None):
    """Extract DASS-21 subscales"""
    # Tags: {UID}-DEM-S0-DAS-D, -A, -S
    # Returns: DataFrame with subscale scores
    
def extract_sleep_per_test(master_path, uid_list=None, test_num=1):
    """Extract per-test sleep hours"""
    # Tags: {UID}-RVR-T{test_num}-SLP-H
    # Returns: DataFrame with sleep hours
```

**Test Requirements:**
- [ ] Test with sample master.xlsx
- [ ] Test missing data handling
- [ ] Test T-score standardization (M=50, SD=10)
- [ ] Test UID filtering

### 🔴 → 🟢 Theta Score Extractors
```python
def extract_domain_theta_scores(rq_path, domain='All'):
    """Load domain-specific theta from Ch5 results"""
    # Path: results/ch5/{rq}/data/step03_theta_scores.csv
    # Returns: DataFrame[uid, test, theta]
    
def merge_theta_cognitive(theta_df, cognitive_df):
    """Merge by UID with validation"""
    # Implementation: pandas.merge with checks
    # Returns: Merged DataFrame
```

---

## Phase 3: LPA Tools (Week 2)
**Goal:** Enable latent profile analysis for RQ 7.8.x

### 🔴 → 🟢 Latent Profile Analysis
```python
# tools/analysis_lpa.py
def fit_lpa_models(X, k_range=range(2,6), seed=42):
    """Fit Gaussian Mixture Models for LPA"""
    # Implementation: sklearn.mixture.GaussianMixture
    # Returns: models, BIC scores, entropy values
    
def extract_profile_membership(model):
    """Get profile assignments"""
    # Implementation: model.predict()
    # Returns: Profile labels array
```

**Test Requirements:**
- [ ] Test with simulated 3-profile data
- [ ] Test BIC calculation accuracy
- [ ] Test entropy calculation (0-1 range)
- [ ] Test reproducibility with seed

---

## Phase 4: Statistical Tests with D068 (Week 2)
**Goal:** Implement dual p-value reporting per Decision D068

### 🔴 → 🟢 ANOVA & Chi-Square
```python
# tools/analysis_stats.py
def one_way_anova_d068(groups, dv, correction='bonferroni'):
    """ANOVA with dual p-value reporting"""
    # Implementation: scipy.stats.f_oneway
    # Returns: F, p_uncorrected, p_corrected, eta²
    
def chi_square_test_d068(contingency_table):
    """Chi-square with dual p-values"""
    # Implementation: scipy.stats.chi2_contingency
    # Returns: χ², p_uncorrected, p_corrected, Cramér's V
```

---

## Phase 5: Effect Sizes & Power (Week 3)
**Goal:** Complete effect size toolkit

### 🔴 → 🟢 Effect Size Calculations
```python
# tools/analysis_regression.py
def compute_cohens_f2(r2_full, r2_reduced):
    """Cohen's f² for hierarchical regression"""
    # Formula: (R²_full - R²_reduced)/(1 - R²_full)
    # Returns: f² value
    
def compute_post_hoc_power(n, k_predictors, r2, alpha=0.05):
    """Post-hoc power for regression"""
    # Implementation: statsmodels.stats.power
    # Returns: Power (0-1)
```

---

## Implementation Timeline

### Week 1: Core Infrastructure
- [ ] Day 1-2: Core regression module (fit, diagnostics)
- [ ] Day 3: Cross-validation & bootstrap
- [ ] Day 4: Data extractors (cognitive tests)
- [ ] Day 5: Testing & documentation

### Week 2: Specialized Tools  
- [ ] Day 6-7: LPA implementation
- [ ] Day 8: Statistical tests with D068
- [ ] Day 9: Effect sizes & power
- [ ] Day 10: Integration testing

### Week 3: Validation & Polish
- [ ] Day 11-12: Run Ch7 RQs with new tools
- [ ] Day 13: Fix bugs found in execution
- [ ] Day 14: Update documentation
- [ ] Day 15: Final validation

---

## Success Metrics
1. **Tool Coverage:** 32/32 tools GREEN
2. **RQ Enablement:** 32/32 Ch7 RQs executable
3. **Test Coverage:** 100% of tools have test suites
4. **Documentation:** All tools in inventory + catalog
5. **Validation:** Successfully execute 5+ Ch7 RQs

---

## TDD Workflow Reminder (9 Steps)
1. **context_finder** - Search existing code
2. **WebSearch** - Research best practices  
3. **AskUser** - Clarify requirements
4. **Test FIRST** - Write tests (RED phase)
5. **Implement** - Make tests pass (GREEN phase)
6. **Document (inventory)** - Full API spec
7. **Document (catalog)** - One-liner description
8. **Status YELLOW** - Update tools_status.tsv
9. **Track done** - Update tracking files

---

## Risk Mitigation
- **Dependency conflicts:** Use standard libraries (scipy, statsmodels, sklearn)
- **Performance issues:** Vectorize operations, use numpy
- **Numerical stability:** Check for singularities, use regularization
- **API consistency:** Follow existing tool signatures from Ch5/Ch6