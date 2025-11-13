#!/usr/bin/env python3
"""
This module contains unit tests for the utils.access_nested_map function,
verifying that it correctly retrieves values from nested dictionaries for
various paths.
"""

import unittest
from parameterized import parameterized
from utils import access_nested_map


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

        