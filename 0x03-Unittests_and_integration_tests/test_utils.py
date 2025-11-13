#!/usr/bin/env python3
"""
Unit tests for the utils module.
Tests access_nested_map for valid and invalid paths and get_json
for correct payloads using mocked HTTP calls.
"""

import unittest
from typing import Any
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import access_nested_map, get_json


class TestAccessNestedMap(unittest.TestCase):
    """
    Test class for the access_nested_map function.
    Checks that the function returns the correct value for different
    nested maps and paths, and raises KeyError for invalid paths.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map: dict, path: tuple, expected: Any) -> None:
        """
        Test that access_nested_map returns the expected value
        given a nested map and a sequence of keys representing the path.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ('a',)),
        ({'a': 1}, ('a', 'b')),
    ])
    def test_access_nested_map_exception(self, nested_map: dict, path: tuple) -> None:
        """
        Test that access_nested_map raises KeyError for invalid paths.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test class for the get_json function.
    Mocks HTTP calls to test that get_json returns the expected payload
    without making real network requests.
    """

    @patch("utils.requests.get")
    @parameterized.expand([
        ("example", "http://example.com", {"payload": True}),
        ("holberton", "http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, name, test_url, test_payload, mock_get):
        """
        Test that get_json returns the expected dictionary for a given URL
        by mocking requests.get so no real HTTP call is made.
        """
        mock_response = Mock()
        mock_response.json.return_value = test_payload
        mock_get.return_value = mock_response

        result = get_json(test_url)

        mock_get.assert_called_once_with(test_url)
        self.assertEqual(result, test_payload)
