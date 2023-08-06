import io
from unittest.mock import Mock, patch

import pytest
from decouple import UndefinedValueError
from google.auth.exceptions import DefaultCredentialsError

from gcloud_secret_configure import GoogleSecretFetcher, get_config


@patch("gcloud_secret_configure.config.RepositoryString")
@patch("gcloud_secret_configure.secret.GoogleSecretFetcher.fetch_secret")
@patch("gcloud_secret_configure.secret.google.auth.default")
def test_get_config(mock_auth_default, mock_fetch_secret, mock_repository_string):
    # Test for normal operation
    mock_auth_default.return_value = (
        Mock(),
        "test_project",
    )  # I don't want to use the real credentials
    mock_fetch_secret.return_value = io.StringIO(
        "key=test_value"
    )  # I don't want to use the real secret
    mock_repository_string.return_value = {"key": "test_value"}
    config = get_config(GoogleSecretFetcher())
    assert config("key", default="default") == "test_value"

    # Test for authentication error
    mock_auth_default.side_effect = DefaultCredentialsError("Error")
    config = get_config(GoogleSecretFetcher())
    with pytest.raises(UndefinedValueError):
        config("non_existent_key")
