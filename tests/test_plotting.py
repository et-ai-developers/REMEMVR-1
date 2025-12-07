"""
Test suite for plotting.py functions.
TDD: Write tests FIRST, then implement functions.
"""
import pytest
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Add project root to path
PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))


class TestPlotComparisonBars:
    """Test plot_comparison_bars() function for grouped bar plots with CI."""

    def test_basic_grouped_bar_plot(self):
        """Test basic grouped bar plot creation with two groups."""
        from tools.plotting import plot_comparison_bars

        # Create test data (correlation comparison format)
        df = pd.DataFrame({
            'location_type': ['source', 'source', 'destination', 'destination'],
            'version': ['full', 'purified', 'full', 'purified'],
            'r': [0.93, 0.94, 0.80, 0.87],
            'CI_lower': [0.92, 0.93, 0.76, 0.85],
            'CI_upper': [0.95, 0.95, 0.83, 0.89]
        })

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='version',
            y_col='r',
            group_col='location_type',
            ci_lower_col='CI_lower',
            ci_upper_col='CI_upper'
        )

        # Check return types
        assert isinstance(fig, plt.Figure)
        assert isinstance(ax, plt.Axes)

        # Check that plot was created (has bars)
        assert len(ax.patches) > 0

        plt.close(fig)

    def test_no_ci_columns(self):
        """Test plot without confidence intervals."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'group': ['A', 'B', 'C'],
            'category': ['cat1', 'cat1', 'cat1'],
            'value': [10, 15, 20]
        })

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='category',
            y_col='value',
            group_col='group'
        )

        # Should still create plot without error bars
        assert isinstance(fig, plt.Figure)
        assert len(ax.patches) > 0

        plt.close(fig)

    def test_custom_colors(self):
        """Test custom color specification."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'location': ['source', 'destination'],
            'metric': ['correlation', 'correlation'],
            'value': [0.9, 0.8]
        })

        custom_colors = {'source': '#FF0000', 'destination': '#0000FF'}

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='metric',
            y_col='value',
            group_col='location',
            colors=custom_colors
        )

        assert isinstance(fig, plt.Figure)
        plt.close(fig)

    def test_single_facet(self):
        """Test single facet (no faceting)."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'model': ['IRT', 'Full_CTT', 'Purified_CTT'],
            'AIC': [1020, 974, 980]
        })

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='model',
            y_col='AIC',
            group_col=None  # No grouping
        )

        assert isinstance(fig, plt.Figure)
        assert len(ax.patches) == 3  # 3 bars

        plt.close(fig)

    def test_faceting_by_location_type(self):
        """Test faceting creates separate subplots."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'location_type': ['source', 'source', 'source',
                             'destination', 'destination', 'destination'],
            'model': ['IRT', 'Full_CTT', 'Purified_CTT'] * 2,
            'AIC': [1020, 974, 980, 1111, 1098, 1116]
        })

        fig, axes = plot_comparison_bars(
            df=df,
            x_col='model',
            y_col='AIC',
            facet_col='location_type'
        )

        # Should return figure and array of axes
        assert isinstance(fig, plt.Figure)
        assert isinstance(axes, np.ndarray)
        assert len(axes) == 2  # Two facets

        plt.close(fig)

    def test_annotations(self):
        """Test annotation parameter adds text to plot."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'model': ['A', 'B'],
            'value': [10, 20],
            'annotation': ['**', 'ns']
        })

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='model',
            y_col='value',
            annotation_col='annotation'
        )

        # Check that annotations were added (as text objects)
        assert len(ax.texts) >= 2  # Should have at least 2 annotations

        plt.close(fig)

    def test_save_to_file(self, tmp_path):
        """Test saving plot to file."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'x': ['A', 'B'],
            'y': [10, 20]
        })

        output_path = tmp_path / "test_plot.png"

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='x',
            y_col='y',
            output_path=output_path
        )

        # Check file was created
        assert output_path.exists()

        plt.close(fig)

    def test_labels_and_title(self):
        """Test custom labels and title."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'x': ['A', 'B'],
            'y': [10, 20]
        })

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='x',
            y_col='y',
            xlabel='Custom X',
            ylabel='Custom Y',
            title='Custom Title'
        )

        assert ax.get_xlabel() == 'Custom X'
        assert ax.get_ylabel() == 'Custom Y'
        assert ax.get_title() == 'Custom Title'

        plt.close(fig)

    def test_horizontal_bars(self):
        """Test horizontal bar orientation."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'category': ['A', 'B', 'C'],
            'value': [10, 20, 15]
        })

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='category',
            y_col='value',
            orientation='horizontal'
        )

        # In horizontal mode, patches should have width (not height)
        assert isinstance(fig, plt.Figure)
        assert len(ax.patches) == 3

        plt.close(fig)

    def test_error_bars_asymmetric(self):
        """Test asymmetric error bars (different CI_lower and CI_upper)."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'x': ['A', 'B'],
            'y': [10, 20],
            'CI_lower': [8, 18],
            'CI_upper': [13, 23]
        })

        fig, ax = plot_comparison_bars(
            df=df,
            x_col='x',
            y_col='y',
            ci_lower_col='CI_lower',
            ci_upper_col='CI_upper'
        )

        # Should have error bars
        # Check that error bar containers exist
        assert len(ax.containers) > 0

        plt.close(fig)

    def test_empty_dataframe_raises_error(self):
        """Test that empty DataFrame raises appropriate error."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame()

        with pytest.raises(ValueError, match="DataFrame is empty"):
            plot_comparison_bars(df=df, x_col='x', y_col='y')

    def test_missing_required_column_raises_error(self):
        """Test that missing required column raises KeyError."""
        from tools.plotting import plot_comparison_bars

        df = pd.DataFrame({
            'x': ['A', 'B'],
            # Missing 'y' column
        })

        with pytest.raises(KeyError):
            plot_comparison_bars(df=df, x_col='x', y_col='y')
