#!/usr/bin/env python3
"""
This module contains unit tests for the utils.access_nested_map function,
verifying that it correctly retrieves values from nested dictionaries for
various paths.
"""

import unittest
from unittest.mock import patch, Mock
from utils import get_json,access_nested_map
from parameterized import parameterized


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    It checks that the function returns the correct value for different
    nested maps and paths.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: object) -> None:
        """
        Test that access_nested_map returns the expected value given a nested
        map and a sequence of keys representing the path to the value.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected, f"{nested_map} following a sequence {path} must return {expected}")

    #testing the exceptions using the same parameterized.expand method
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


#!/usr/bin/env python3
"""
Unit tests for the utils.get_json function.
It mocks HTTP calls to test that get_json returns the expected payload
without making real network requests.
"""


class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function.
    It checks that get_json returns the correct dictionary and that
    requests.get is called exactly once with the correct URL.
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
        # Configure the mock to return a response with .json() = test_payload
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        # Call the function (it uses the mocked requests.get)
        result = get_json(test_url)

        # Assert that requests.get was called exactly once with test_url
        mock_get.assert_called_once_with(test_url)

        # Assert that the returned result matches the expected payload
        self.assertEqual(result, test_payload)


