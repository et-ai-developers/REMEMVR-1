"""
Test suite for piecewise LMM tools
TDD: Write tests FIRST, then implement functions
"""
import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


class TestAssignPiecewiseSegments:
    """Test assign_piecewise_segments() function."""
    
    def test_basic_segment_assignment(self):
        """Test that tests 1-2 assigned to Early, tests 3-4 to Late."""
        from tools.analysis_lmm import assign_piecewise_segments
        
        # Create test data
        df = pd.DataFrame({
            'UID': ['P001', 'P001', 'P001', 'P001'],
            'test': [1, 2, 3, 4],
            'TSVR_hours': [0.0, 24.0, 72.0, 144.0],
            'theta': [0.5, 0.3, 0.1, -0.2]
        })
        
        result = assign_piecewise_segments(df, tsvr_col='TSVR_hours', early_cutoff_hours=24.0)
        
        # Check Segment column created
        assert 'Segment' in result.columns
        assert 'Days_within' in result.columns
        
        # Check segment assignment
        assert result.loc[0, 'Segment'] == 'Early'  # test 1
        assert result.loc[1, 'Segment'] == 'Early'  # test 2
        assert result.loc[2, 'Segment'] == 'Late'   # test 3
        assert result.loc[3, 'Segment'] == 'Late'   # test 4
    
    def test_days_within_calculation(self):
        """Test Days_within computed correctly for each segment."""
        from tools.analysis_lmm import assign_piecewise_segments
        
        df = pd.DataFrame({
            'UID': ['P001'] * 4,
            'test': [1, 2, 3, 4],
            'TSVR_hours': [0.0, 24.0, 72.0, 144.0],
            'theta': [0.5, 0.3, 0.1, -0.2]
        })
        
        result = assign_piecewise_segments(df, tsvr_col='TSVR_hours', early_cutoff_hours=24.0)
        
        # Early segment: Days_within = TSVR_hours / 24
        assert result.loc[0, 'Days_within'] == pytest.approx(0.0)     # 0 / 24
        assert result.loc[1, 'Days_within'] == pytest.approx(1.0)     # 24 / 24
        
        # Late segment: Days_within = (TSVR_hours - 72) / 24 (reset at Day 3)
        assert result.loc[2, 'Days_within'] == pytest.approx(0.0)     # (72 - 72) / 24
        assert result.loc[3, 'Days_within'] == pytest.approx(3.0)     # (144 - 72) / 24
    
    def test_no_missing_values(self):
        """Test that no NaN values introduced."""
        from tools.analysis_lmm import assign_piecewise_segments
        
        df = pd.DataFrame({
            'UID': ['P001'] * 4,
            'test': [1, 2, 3, 4],
            'TSVR_hours': [0.0, 24.0, 72.0, 144.0],
            'theta': [0.5, 0.3, 0.1, -0.2]
        })
        
        result = assign_piecewise_segments(df, tsvr_col='TSVR_hours', early_cutoff_hours=24.0)
        
        assert result['Segment'].isna().sum() == 0
        assert result['Days_within'].isna().sum() == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])


class TestExtractSegmentSlopes:
    """Test extract_segment_slopes_from_lmm() function."""
    
    def test_extracts_6_slopes_for_piecewise_model(self):
        """Test that function extracts 6 slopes (2 segments x 3 factors)."""
        from tools.analysis_lmm import extract_segment_slopes_from_lmm
        import statsmodels.formula.api as smf
        
        # Create mock piecewise data (2 segments x 3 congruence levels)
        np.random.seed(42)
        n_participants = 20
        n_obs_per_participant = 4  # 2 Early + 2 Late
        
        data = []
        for uid in range(n_participants):
            for segment in ['Early', 'Early', 'Late', 'Late']:
                for congruence in ['Common', 'Congruent', 'Incongruent']:
                    days_within = np.random.uniform(0, 1) if segment == 'Early' else np.random.uniform(0, 3)
                    theta = 0.5 - 0.1 * days_within + np.random.normal(0, 0.1)
                    data.append({
                        'UID': f'P{uid:03d}',
                        'Segment': segment,
                        'Congruence': congruence,
                        'Days_within': days_within,
                        'theta': theta
                    })
        
        df = pd.DataFrame(data)
        
        # Fit piecewise LMM with 3-way interaction
        formula = "theta ~ Days_within * C(Segment, Treatment('Early')) * C(Congruence, Treatment('Common'))"
        model = smf.mixedlm(formula, df, groups=df['UID'], re_formula='~Days_within')
        result = model.fit(method='lbfgs', maxiter=100)
        
        # Extract slopes
        slopes = extract_segment_slopes_from_lmm(
            result, 
            segment_col='Segment',
            factor_col='Congruence',
            segment_ref='Early',
            factor_ref='Common'
        )
        
        # Check structure
        assert isinstance(slopes, pd.DataFrame)
        assert len(slopes) == 6  # 2 segments x 3 congruence levels
        assert list(slopes.columns) == ['segment', 'factor', 'slope', 'se', 'CI_lower', 'CI_upper']
        
        # Check all combinations present
        combinations = set(zip(slopes['segment'], slopes['factor']))
        expected = {
            ('Early', 'Common'), ('Early', 'Congruent'), ('Early', 'Incongruent'),
            ('Late', 'Common'), ('Late', 'Congruent'), ('Late', 'Incongruent')
        }
        assert combinations == expected
    
    def test_ci_bounds_correct(self):
        """Test that CI bounds are slope +/- 1.96*SE."""
        from tools.analysis_lmm import extract_segment_slopes_from_lmm
        import statsmodels.formula.api as smf
        
        # Create simple mock data
        np.random.seed(123)
        df = pd.DataFrame({
            'UID': ['P001'] * 12,
            'Segment': ['Early'] * 6 + ['Late'] * 6,
            'Congruence': ['Common', 'Congruent'] * 6,
            'Days_within': np.random.uniform(0, 2, 12),
            'theta': np.random.normal(0, 1, 12)
        })
        
        formula = "theta ~ Days_within * C(Segment, Treatment('Early')) * C(Congruence, Treatment('Common'))"
        model = smf.mixedlm(formula, df, groups=df['UID'], re_formula='~1')
        result = model.fit(method='lbfgs', maxiter=50)
        
        slopes = extract_segment_slopes_from_lmm(result, 'Segment', 'Congruence', 'Early', 'Common')
        
        # Check CI bounds
        for _, row in slopes.iterrows():
            expected_lower = row['slope'] - 1.96 * row['se']
            expected_upper = row['slope'] + 1.96 * row['se']
            assert row['CI_lower'] == pytest.approx(expected_lower, abs=1e-6)
            assert row['CI_upper'] == pytest.approx(expected_upper, abs=1e-6)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
