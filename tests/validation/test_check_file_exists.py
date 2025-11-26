"""Tests for check_file_exists validation function."""

import pytest
from pathlib import Path
import tempfile
from tools.validation import check_file_exists


class TestCheckFileExists:
    """Test check_file_exists validation function."""

    def test_file_exists_basic(self, tmp_path):
        """Test basic file existence check."""
        # Create temporary file
        test_file = tmp_path / "test.csv"
        test_file.write_text("some data")

        result = check_file_exists(str(test_file))

        assert result["valid"] is True
        assert "exists" in result["message"].lower()
        assert result["size_bytes"] > 0
        assert result["file_path"] == str(test_file)

    def test_file_does_not_exist(self, tmp_path):
        """Test file does not exist."""
        non_existent = tmp_path / "does_not_exist.csv"

        result = check_file_exists(str(non_existent))

        assert result["valid"] is False
        assert "not exist" in result["message"].lower() or "does not exist" in result["message"].lower()
        assert result["size_bytes"] == 0
        assert result["file_path"] == str(non_existent)

    def test_file_exists_with_minimum_size_pass(self, tmp_path):
        """Test file exists and meets minimum size requirement."""
        test_file = tmp_path / "large.csv"
        test_file.write_text("x" * 1000)  # 1000 bytes

        result = check_file_exists(str(test_file), min_size_bytes=500)

        assert result["valid"] is True
        assert result["size_bytes"] >= 500
        assert "meets minimum size" in result["message"].lower() or "exists" in result["message"].lower()

    def test_file_exists_with_minimum_size_fail(self, tmp_path):
        """Test file exists but does not meet minimum size requirement."""
        test_file = tmp_path / "small.csv"
        test_file.write_text("tiny")  # 4 bytes

        result = check_file_exists(str(test_file), min_size_bytes=100)

        assert result["valid"] is False
        assert "too small" in result["message"].lower() or "below minimum" in result["message"].lower()
        assert result["size_bytes"] == 4
        assert "100" in str(result["message"])  # Mentions minimum threshold

    def test_empty_file_with_zero_minimum(self, tmp_path):
        """Test empty file passes with min_size_bytes=0 (default)."""
        test_file = tmp_path / "empty.csv"
        test_file.write_text("")  # 0 bytes

        result = check_file_exists(str(test_file))

        assert result["valid"] is True
        assert result["size_bytes"] == 0

    def test_empty_file_with_minimum_size(self, tmp_path):
        """Test empty file fails with min_size_bytes > 0."""
        test_file = tmp_path / "empty.csv"
        test_file.write_text("")  # 0 bytes

        result = check_file_exists(str(test_file), min_size_bytes=1)

        assert result["valid"] is False
        assert result["size_bytes"] == 0
        assert "too small" in result["message"].lower() or "below minimum" in result["message"].lower()

    def test_accepts_path_object(self, tmp_path):
        """Test function accepts pathlib.Path object."""
        test_file = tmp_path / "test.csv"
        test_file.write_text("data")

        # Pass Path object instead of string
        result = check_file_exists(test_file)

        assert result["valid"] is True
        assert result["size_bytes"] > 0

    def test_directory_not_treated_as_file(self, tmp_path):
        """Test directory returns False (not a file)."""
        test_dir = tmp_path / "directory"
        test_dir.mkdir()

        result = check_file_exists(str(test_dir))

        # Should fail because it's a directory, not a file
        assert result["valid"] is False
        assert "not a file" in result["message"].lower() or "directory" in result["message"].lower()

    def test_relative_path(self, tmp_path):
        """Test function handles relative paths correctly."""
        # Create file in temp directory
        test_file = tmp_path / "relative_test.csv"
        test_file.write_text("data")

        # Test with string path
        result = check_file_exists(str(test_file))

        assert result["valid"] is True
        assert result["size_bytes"] > 0
        # File path should be preserved as provided
        assert "relative_test.csv" in result["file_path"]

    def test_large_file_size(self, tmp_path):
        """Test file size reported correctly for larger files."""
        test_file = tmp_path / "large.csv"
        size = 5 * 1024 * 1024  # 5 MB
        test_file.write_bytes(b"x" * size)

        result = check_file_exists(str(test_file))

        assert result["valid"] is True
        assert result["size_bytes"] == size
