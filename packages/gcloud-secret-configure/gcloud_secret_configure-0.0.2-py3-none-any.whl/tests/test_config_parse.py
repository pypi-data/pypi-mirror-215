import io

import pytest

from gcloud_secret_configure.config import StringFileParser


def test_parse():
    # This test case tests the `parse` method,
    # by providing an StringIO object with valid and invalid lines.
    # It expects a dictionary of the valid lines parsed correctly.
    input_data = io.StringIO("key1=value1\n# This is a comment\nkey2='value2'\n\n")
    parser = StringFileParser(input_data)
    expected_result = {
        "key1": "value1",
        "key2": "value2",
    }
    assert parser.parse() == expected_result


def test_is_valid_line():
    # This test case tests the `_is_valid_line` method,
    # by providing valid and invalid lines.
    # It expects True for valid lines and False for invalid lines.
    parser = StringFileParser(io.StringIO(""))
    assert parser._is_valid_line("key1=value1")  # valid line
    assert not parser._is_valid_line(
        "# This is a comment"
    )  # invalid line: starts with "#"
    assert not parser._is_valid_line("   ")  # invalid line: only spaces
    assert not parser._is_valid_line("")  # invalid line: empty string


def test_parse_line():
    # This test case tests the `_parse_line` method,
    # by providing lines in different formats.
    # It expects tuples with the key and value parsed correctly.
    parser = StringFileParser(io.StringIO(""))
    assert parser._parse_line("key1=value1") == ("key1", "value1")  # without quotes
    assert parser._parse_line("key2='value2'") == (
        "key2",
        "value2",
    )  # with single quotes
    assert parser._parse_line('key3="value3"') == (
        "key3",
        "value3",
    )  # with double quotes


def test_init_with_wrong_type():
    # This test case tests the `__init__` method,
    # by providing an argument that is not an instance of StringIO.
    # It expects a ValueError.
    with pytest.raises(ValueError):
        StringFileParser("this is not a StringIO instance")
