#!/usr/bin/env python3
"""Test Utils module for testing"""
from unittest import TestCase
from unittest.mock import Mock, patch
from parameterized import parameterized
from utils import (
    access_nested_map,
    get_json,
    memoize,
)
from typing import (
    Dict,
    List,
    Mapping,
    Sequence,
    TypeVar,
    Union,
)


def mocked_requests_get(*args, **kwargs):
    """_summary_

    Returns:
        _type_: _description_
    """
    class MockResponse:
        """the mock response
        """

        def __init__(self, json_data, status_code) -> None:
            """initializing the MockResponse

            Args:
                json_data (_type_): _description_
                status_code (_type_): _description_
            """
            self.json_data = json_data
            self.status_code = status_code

        def json(self):
            return self.json_data

    if args[0] == "http://example.com":
        return MockResponse({"url": "http://example.com"}, 200)
    elif args[0] == "http://holberton.io":
        return MockResponse({"url": "http://holberton.io"}, 200)

    return MockResponse(None, 404)


class TestAccessNestedMap(TestCase):

    @parameterized.expand([
        ({"a": 1}, ("a"), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping,
        path: Sequence,
        expected: Union[Dict, int]
    ) -> None:
        """tests the access_nested_map function

        Args:
            nested_map (Mapping): _description_
            path (Sequence): _description_
            expected (Union[Dict, int]): _description_
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a,"), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping,
        path: Sequence,
        exception: Exception
    ) -> None:
        """tests how the access_nested_map responds to exception

        Args:
            nested_map (Mapping): _description_
            path (Sequence): _description_
            expected (KeyError): _description_
        """
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(TestCase):

    @parameterized.expand([
        (("http://example.com"), {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(
        self,
        test_url: str,
        test_payload: Dict
    ) -> None:
        """tests the get_json

        Args:
            test_url (str): _description_
            test_payload (Dict[str, str]): _description_
        """
        with patch(
            "requests.get",
            return_value=Mock(**{"json.return_value": test_payload})
        ) as patched_req:
            self.assertEqual(get_json(test_url), test_payload)
            patched_req.assert_called_once_with(test_url)


class TestMemoize(TestCase):
    """tests the memoize function

    Args:
        TestCase (TestCase): _description_
    """

    def test_memoize(self) -> None:
        """Tests `memoize`'s output.

        Returns:
            _type_: _description_
        """        """"""

        class TestClass:
            """Test class to handle certain methods
            """

            def a_method(self) -> int:
                """returns a number

                Returns:
                    int: 42
                """
                return 42

            @memoize
            def a_property(self) -> a_method:
                return self.a_method()

        with patch.object(
                TestClass,
                "a_method",
                return_value=lambda: 42,
        ) as memo_fxn:
            test_class = TestClass()
            self.assertEqual(test_class.a_property(), 42)
            self.assertEqual(test_class.a_property(), 42)
            memo_fxn.assert_called_once()
