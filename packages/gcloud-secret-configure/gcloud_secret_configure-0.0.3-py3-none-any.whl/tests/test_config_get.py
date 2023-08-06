import io
import pathlib

from decouple import AutoConfig, Config

from gcloud_secret_configure.config import get_config


def test_get_config(monkeypatch):
    # Dummy repository class to mimic the behavior of decouple.RepositoryEnv
    class DummyRepository:
        def __init__(self, *args, **kwargs):
            pass

        def __getitem__(self, item):
            return "value"

        def __contains__(self, item):
            return True

    # Case 1: When .env file exists
    monkeypatch.setattr(
        pathlib.Path, "exists", lambda x: True
    )  # Simulating the existence of .env file
    monkeypatch.setattr(
        "gcloud_secret_configure.config.RepositoryEnv", DummyRepository
    )  # Using dummy repository in place of decouple.RepositoryEnv
    config = get_config()
    assert isinstance(config, Config) or isinstance(
        config, AutoConfig
    )  # The returned config should be an instance of decouple.Config or AutoConfig

    # Case 2: When .env file does not exist
    monkeypatch.setattr(
        pathlib.Path, "exists", lambda x: False
    )  # Simulating the absence of .env file
    config = get_config()
    assert isinstance(config, Config) or isinstance(
        config, AutoConfig
    )  # The returned config should be an instance of decouple.Config or AutoConfig

    # Case 3: When a secret fetcher is provided and it returns a valid configuration
    class MockSecretFetcher:
        def fetch_secret(self, secret_label="env_file", version="latest"):
            return io.StringIO(
                "KEY=value"
            )  # Simulating a secret fetcher that returns a valid configuration

    config = get_config(
        secret_fetcher=MockSecretFetcher(), secret_label="env_file"
    )  # actually, 'secret_label' is not needed here
    assert isinstance(config, Config) or isinstance(
        config, AutoConfig
    )  # The returned config should be an instance of decouple.Config or AutoConfig

    # Case 4: When a secret fetcher is provided and it returns None
    class MockSecretFetcher:
        def fetch_secret(self, secret_label="env_file", version="latest"):
            return None  # Simulating a secret fetcher that returns None

    config = get_config(secret_fetcher=MockSecretFetcher())
    assert isinstance(config, Config) or isinstance(
        config, AutoConfig
    )  # The returned config should be an instance of decouple.Config or AutoConfig
