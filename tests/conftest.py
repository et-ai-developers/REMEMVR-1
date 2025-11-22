"""
Pytest configuration and fixtures for tools tests.

Handles optional dependencies (torch, deepirtools) gracefully.
"""
import pytest
import sys

# Check for optional dependencies
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

try:
    import deepirtools
    HAS_DEEPIRTOOLS = True
except ImportError:
    HAS_DEEPIRTOOLS = False

try:
    import statsmodels
    HAS_STATSMODELS = True
except ImportError:
    HAS_STATSMODELS = False


# Markers for skipping tests based on dependencies
requires_torch = pytest.mark.skipif(
    not HAS_TORCH,
    reason="Requires torch (PyTorch) - not installed"
)

requires_deepirtools = pytest.mark.skipif(
    not HAS_DEEPIRTOOLS,
    reason="Requires deepirtools - not installed"
)

requires_statsmodels = pytest.mark.skipif(
    not HAS_STATSMODELS,
    reason="Requires statsmodels - not installed"
)
