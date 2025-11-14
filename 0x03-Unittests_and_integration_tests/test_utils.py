#!/usr/bin/env python3
"""
Unit tests for the utils module.
It tests access_nested_map for valid and invalid paths and get_json
for correct payloads using mocked HTTP calls.
"""

import unittest
from typing import Any
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json,memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    It checks that the function returns the correct value for different
    nested maps and paths and raises KeyError for invalid paths.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: Any) -> None:
        """
        Test that access_nested_map returns the expected value given a nested
        map and a sequence of keys representing the path to the value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ('a',)),
        ({'a': 1}, ('a', 'b')),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple) -> None:
        """
        Test that access_nested_map raises KeyError for invalid paths
        in nested maps.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function.
    It mocks HTTP calls to test that get_json returns the expected payload
    without making real network requests.
    """

    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": False}),
    ])
    @patch("utils.requests.get")
    def test_get_json(self, name: str, test_url: str, test_payload: dict, mock_get: Mock) -> None:
        """
        Test that get_json returns the expected dictionary for a given URL
        by mocking requests.get so no real HTTP call is made.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)
        self.assertEqual(result, test_payload)

class TestMemoize(unittest.TestCase):
    """Unit test for the memoize decorator."""

    def test_memoize(self):
        """Test that a memoized method is called only once."""

        class TestClass:
            """A simple test class for memoize."""

            def a_method(self):
                """Method to be memoized."""
                return 42

            @memoize
            def a_property(self):
                """Memoized property that calls a_method."""
                return self.a_method()

        test_obj = TestClass()

        with patch.object(TestClass, "a_method", return_value=42) as mock_method:
            # Call the memoized property twice
            result1 = test_obj.a_property
            result2 = test_obj.a_property

            # Check that the return values are correct
            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)

            # Ensure a_method was called only once
            mock_method.assert_called_once()