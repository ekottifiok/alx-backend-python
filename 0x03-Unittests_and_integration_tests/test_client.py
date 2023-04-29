#!/usr/bin/env python3
"""
Test Client module for testing
"""
from unittest import TestCase
from fixtures import TEST_PAYLOAD
from parameterized import parameterized, parameterized_class
from requests import HTTPError
from client import GithubOrgClient
from typing import Dict
from unittest.mock import (
    Mock,
    PropertyMock,
    patch,
    MagicMock
)


API = "https://api.github.com/"


class TestGithubOrgClient(TestCase):
    """runs test for TestGithubOrgClient

    Args:
        TestCase (class): _description_
    """

    @parameterized.expand([
        ("google", {"welcome": "google"}),
        ("abc", {"welcome": "abc"})
    ])
    @patch("client.get_json")
    def test_org(
        self,
        org: str,
        result: Dict[str, str],
        mock: MagicMock
    ) -> None:
        """test if the org function works well

        Args:
            org (str): _description_
            result (Dict[str, str]): _description_
            mock (MagicMock): _description_
        """
        mock.return_value = MagicMock(return_value=result)
        self.assertEqual(GithubOrgClient(org).org(), result)
        mock.assert_called_once_with(API + "orgs/" + org)

    def test_public_repos_url(self) -> None:
        """Test that the result of _public_repos_url
        is the expected one based on the mocked payload.
        """
        with patch(
                "client.GithubOrgClient.org",
                new_callable=PropertyMock,
        ) as mock:
            mock.return_value = {
                'repos_url': API,
            }
            self.assertEqual(
                GithubOrgClient("google")._public_repos_url,
                API
            )

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json: MagicMock) -> None:
        """Tests the `public_repos` method.

        Args:
            mock_get_json (MagicMock): the mocker
        """
        test_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [
                {
                    "id": 7697149,
                    "name": "episodes.dart",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/episodes.dart",
                    "created_at": "2013-01-19T00:31:37Z",
                    "updated_at": "2019-09-23T11:53:58Z",
                    "has_issues": True,
                    "forks": 22,
                    "default_branch": "master",
                },
                {
                    "id": 8566972,
                    "name": "kratu",
                    "private": False,
                    "owner": {
                        "login": "google",
                        "id": 1342004,
                    },
                    "fork": False,
                    "url": "https://api.github.com/repos/google/kratu",
                    "created_at": "2013-03-04T22:52:33Z",
                    "updated_at": "2019-11-15T22:22:16Z",
                    "has_issues": True,
                    "forks": 32,
                    "default_branch": "master",
                },
            ]
        }
        mock_get_json.return_value = test_payload["repos"]
        with patch(
                "client.GithubOrgClient._public_repos_url",
                new_callable=PropertyMock,
        ) as mock_public_repos_url:
            mock_public_repos_url.return_value = test_payload["repos_url"]
            self.assertEqual(
                GithubOrgClient("google").public_repos(),
                [
                    "episodes.dart",
                    "kratu",
                ],
            )
            mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once()

    @parameterized.expand([
        ({'license': {'key': "bsd-3-clause"}}, "bsd-3-clause", True),
        ({'license': {'key': "bsl-1.0"}}, "bsd-3-clause", False),
    ])
    def test_has_license(self, repo: Dict, key: str, expected: bool) -> None:
        """Tests the `has_license` method. to ensure it is expected"""
        self.assertEqual(
            GithubOrgClient("test").has_license(repo, key),
            expected
        )


@parameterized_class([
    {
        'org_payload': TEST_PAYLOAD[0][0],
        'repos_payload': TEST_PAYLOAD[0][1],
        'expected_repos': TEST_PAYLOAD[0][2],
        'apache2_repos': TEST_PAYLOAD[0][3],
    },
])
class TestIntegrationGithubOrgClient(TestCase):
    """Performs integration tests for the `GithubOrgClient` class.

    Args:
        TestCase (_type_): _description_

    Returns:
        _type_: _description_
    """    """"""

    @classmethod
    def setUpClass(cls) -> None:
        """
        Sets up class fixtures before running tests.
        and doesn't return anything

        """
        route_payload = {
            'https://api.github.com/orgs/google': cls.org_payload,
            'https://api.github.com/orgs/google/repos': cls.repos_payload,
        }

        def get_payload(url):
            if url in route_payload:
                return Mock(**{'json.return_value': route_payload[url]})
            return HTTPError

        cls.get_patcher = patch("requests.get", side_effect=get_payload)
        cls.get_patcher.start()

    def test_public_repos(self) -> None:
        """Tests the method."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(),
            self.expected_repos,
        )

    def test_public_repos_with_license(self) -> None:
        """Tests the method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls) -> None:
        """tears down the class after running all tests."""
        cls.get_patcher.stop()
