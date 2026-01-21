"""Tests for utility functions."""

import pytest
from bundleup.utils import validate_non_empty_string, validate_dict, merge_headers


def test_validate_non_empty_string_with_valid_string():
    """Test validate_non_empty_string with valid string."""
    validate_non_empty_string("test", "param")  # Should not raise


def test_validate_non_empty_string_with_empty_string():
    """Test validate_non_empty_string with empty string."""
    with pytest.raises(ValueError, match="param cannot be empty"):
        validate_non_empty_string("", "param")


def test_validate_non_empty_string_with_whitespace_only():
    """Test validate_non_empty_string with whitespace only."""
    with pytest.raises(ValueError, match="param cannot be empty"):
        validate_non_empty_string("   ", "param")


def test_validate_non_empty_string_with_non_string():
    """Test validate_non_empty_string with non-string."""
    with pytest.raises(ValueError, match="param must be a string"):
        validate_non_empty_string(123, "param")


def test_validate_dict_with_valid_dict():
    """Test validate_dict with valid dictionary."""
    validate_dict({"key": "value"}, "param")  # Should not raise


def test_validate_dict_with_empty_dict():
    """Test validate_dict with empty dictionary."""
    validate_dict({}, "param")  # Should not raise


def test_validate_dict_with_non_dict():
    """Test validate_dict with non-dictionary."""
    with pytest.raises(ValueError, match="param must be a dictionary"):
        validate_dict("not a dict", "param")


def test_merge_headers_with_single_dict():
    """Test merge_headers with single dictionary."""
    result = merge_headers({"key": "value"})
    assert result == {"key": "value"}


def test_merge_headers_with_multiple_dicts():
    """Test merge_headers with multiple dictionaries."""
    result = merge_headers(
        {"key1": "value1"},
        {"key2": "value2"},
        {"key3": "value3"}
    )
    assert result == {"key1": "value1", "key2": "value2", "key3": "value3"}


def test_merge_headers_with_overlapping_keys():
    """Test merge_headers with overlapping keys (later values win)."""
    result = merge_headers(
        {"key": "value1"},
        {"key": "value2"}
    )
    assert result == {"key": "value2"}


def test_merge_headers_with_empty():
    """Test merge_headers with no arguments."""
    result = merge_headers()
    assert result == {}
