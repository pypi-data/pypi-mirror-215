from io import StringIO
from unittest.mock import patch

from google.auth.exceptions import DefaultCredentialsError

from gcloud_secret_configure.secret import GoogleSecretFetcher


@patch("google.cloud.secretmanager.SecretManagerServiceClient")
@patch("google.auth.default")
def test_fetch_secret(mock_auth_default, mock_secret_client):
    # Test for normal operation
    mock_auth_default.return_value = (None, "test_project")
    mock_secret_client.return_value.access_secret_version.return_value.payload.data.decode.return_value = (
        "test_secret"
    )
    fetcher = GoogleSecretFetcher()
    result = fetcher.fetch_secret()
    assert isinstance(result, StringIO)  # assert the return type
    assert result.getvalue() == "test_secret"  # assert the content

    # english: Test for authentication error
    mock_auth_default.side_effect = DefaultCredentialsError("Error")
    fetcher = GoogleSecretFetcher()
    assert fetcher.fetch_secret() is None
