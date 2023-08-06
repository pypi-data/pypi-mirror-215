import io

import pytest

from gcloud_secret_configure.config import RepositoryString


def test_init():
    # This test case tests the `__init__` method,
    # by providing a valid StringIO object.
    # It expects the data dictionary to be parsed correctly.
    source = io.StringIO("key1=value1\nkey2='value2'\nkey3='value3'")
    repo = RepositoryString(source)
    expected_data = {
        "key1": "value1",
        "key2": "value2",
        "key3": "value3",
    }
    assert repo.data == expected_data


def test_contains():
    # This test case tests the `__contains__` method,
    # by checking whether a key exists in the parsed data or not.
    # It expects True if the key exists and False otherwise.
    source = io.StringIO("key1=value1\nkey2='value2'\nkey3='value3'")
    repo = RepositoryString(source)
    assert "key1" in repo  # key exists
    assert "non_existent_key" not in repo  # key doesn't exist


def test_get_item():
    # This test case tests the `__getitem__` method,
    # by fetching the value of a specific key from the parsed data.
    # It expects the correct value of the key to be returned.
    source = io.StringIO("key1=value1\nkey2='value2'\nkey3='value3'")
    repo = RepositoryString(source)
    assert repo["key1"] == "value1"
    assert repo["key2"] == "value2"
    assert repo["key3"] == "value3"


def test_get_item_not_exists():
    # This test case tests the `__getitem__` method,
    # by fetching the value of a non-existent key from the parsed data.
    # It expects a KeyError to be raised.
    source = io.StringIO("key1=value1\nkey2='value2'\nkey3='value3'")
    repo = RepositoryString(source)
    with pytest.raises(KeyError):
        _ = repo["non_existent_key"]
