#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient class.
Tests include:
- org property
- _public_repos_url property
- public_repos method
"""

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for GithubOrgClient."""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.

        The get_json function is patched to avoid real HTTP requests.
        """
        # Fake payload to simulate GitHub API response
        expected_payload = {"name": org_name}

        # Configure the mock to return the fake payload
        mock_get_json.return_value = expected_payload

        # Create a GithubOrgClient instance
        client = GithubOrgClient(org_name)

        # Access the .org property (uses mocked get_json)
        result = client.org

        # Assert get_json was called exactly once with the correct URL
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # Assert the property returns the expected payload
        self.assertEqual(result, expected_payload)

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct repos_url.

        The .org property is patched using PropertyMock to return a known payload.
        """
        # Fake payload for the org property
        test_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        # Patch the .org property to return the fake payload
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            # Create a GithubOrgClient instance
            client = GithubOrgClient("google")

            # Access the _public_repos_url property
            result = client._public_repos_url

            # Assert it returns the expected repos_url
            self.assertEqual(result, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the correct list of repository names.

        - get_json is patched to return a fake list of repos
        - _public_repos_url is patched to avoid real URLs
        """
        # Fake JSON payload from get_json
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"},
            {"name": "repo3"},
        ]

        # Patch the _public_repos_url property to return a fixed URL
        with patch("client.GithubOrgClient._public_repos_url",
                   new="http://example.com"):

            # Create a GithubOrgClient instance
            client = GithubOrgClient("google")

            # Call public_repos and store the result
            result = client.public_repos()

            # Assert the returned repo names are correct
            self.assertEqual(result, ["repo1", "repo2", "repo3"])

            # Assert get_json was called exactly once with the patched URL
            mock_get_json.assert_called_once_with("http://example.com")

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """
        Test that has_license correctly identifies if a repo has a license.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)

if __name__ == "__main__":
    unittest.main()
