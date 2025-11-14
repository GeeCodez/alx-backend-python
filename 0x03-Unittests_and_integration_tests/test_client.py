#!/usr/bin/env python3

import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized

from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""

        # 1. Fake data to return instead of real GitHub API
        expected_payload = {"name": org_name}

        # 2. Configure the mock to return the fake value
        mock_get_json.return_value = expected_payload

        # 3. Create a client using the org name
        client = GithubOrgClient(org_name)

        # 4. Call the property (which should use the mocked get_json)
        result = client.org

        # 5. Assert get_json was called *exactly once*
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

        # 6. Assert the return value is what we mocked
        self.assertEqual(result, expected_payload)


    def test_public_repos_url(self):
        test_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            self.assertEqual(result, test_payload["repos_url"])

if __name__=="__main__":
    unittest.main()