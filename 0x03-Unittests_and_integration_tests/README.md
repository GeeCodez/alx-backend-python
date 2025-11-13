# Python Testing Project

## Overview

This project demonstrates how to write **unit tests** and **integration tests** in Python. It uses the `unittest` framework and the `parameterized` package to efficiently test multiple inputs.

## Unit Tests

Unit tests are small, isolated tests that verify the behavior of a single function or class.  
Example: Testing the `access_nested_map` function to ensure it correctly retrieves values from nested dictionaries.

## Integration Tests

Integration tests check how multiple components of a system work together.  
Example: Testing a function that retrieves data from an external API and processes it before returning a result.

## Requirements

- Python 3.7+
- `parameterized` package (`pip install parameterized`)
- All files must be executable and follow `pycodestyle` style.

## Usage

Run the unit tests using:

```bash
python -m unittest test_utils.py
