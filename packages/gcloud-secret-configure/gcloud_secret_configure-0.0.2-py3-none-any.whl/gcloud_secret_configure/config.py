import io
import os
import pathlib
from functools import lru_cache
from typing import Dict

from decouple import Config, RepositoryEmpty, RepositoryEnv

# from src.infra.std_logging import logging

BASE_DIR = pathlib.Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"


class StringFileParser:
    """
    Helper class to parse a string containing key-value pairs
    :param source: A string containing key-value pairs
    """

    def __init__(self, source: io.StringIO):
        if not isinstance(source, io.StringIO):
            raise ValueError("source must be an instance of io.StringIO")
        self.source = source

    def parse(self) -> Dict[str, str]:
        data = {}
        file_ = self.source.read().split("\n")
        for line in file_:
            line = line.strip()
            if self._is_valid_line(line):
                k, v = self._parse_line(line)
                data[k] = v
        return data

    @staticmethod
    def _is_valid_line(line):
        return line and not line.startswith("#") and "=" in line

    @staticmethod
    def _parse_line(line):
        k, v = line.split("=", 1)
        k = k.strip()
        v = v.strip()
        if len(v) >= 2 and (
            (v[0] == "'" and v[-1] == "'") or (v[0] == '"' and v[-1] == '"')
        ):
            v = v[1:-1]
        return k, v


class RepositoryString(RepositoryEmpty):
    """
    Repository class to parse a string containing key-value pairs

    :param source: A string containing key-value pairs
    """

    def __init__(self, source: io.StringIO):
        parser = StringFileParser(source)
        self.data = parser.parse()

    def __contains__(self, key):
        return key in os.environ or key in self.data

    def __getitem__(self, key):
        return self.data[key]


@lru_cache()
def get_config(
    secret_fetcher=None,
    env_path: pathlib.Path = ENV_PATH,
    secret_label: str = "env_file",
) -> Config:
    """
    Returns a decouple.Config or decouple.AutoConfig instance
    :param secret_fetcher: An instance of a secret fetcher class
        like 'GoogleSecretFetcher' class.
    :param env_path: Path to the .env file
    :param secret_label: Label of the secret to be fetched
    :return: decouple.Config or decouple.AutoConfig instance

    Usage:
    >>> from gcloud_secret_configure.config import get_config
    >>> config = get_config()
    >>> config("KEY")
    """
    if env_path and env_path.exists():
        return Config(RepositoryEnv(str(env_path)))

    if secret_fetcher:
        payload = secret_fetcher.fetch_secret(secret_label=secret_label)
        if payload is not None:
            return Config(RepositoryString(payload))

    from decouple import config

    return config


# config = get_config(GoogleSecretFetcher())
