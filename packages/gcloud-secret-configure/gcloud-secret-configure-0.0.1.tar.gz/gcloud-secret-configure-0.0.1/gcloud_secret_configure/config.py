import io
import os
import pathlib
from functools import lru_cache

from decouple import Config, RepositoryEmpty, RepositoryEnv

# from src.infra.std_logging import logging

BASE_DIR = pathlib.Path(__file__).parent
ENV_PATH = BASE_DIR / ".env"


class StringFileParser:
    def __init__(self, source):
        if not isinstance(source, io.StringIO):
            raise ValueError("source must be an instance of io.StringIO")
        self.source = source

    def parse(self):
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
    def __init__(self, source):
        parser = StringFileParser(source)
        self.data = parser.parse()

    def __contains__(self, key):
        return key in os.environ or key in self.data

    def __getitem__(self, key):
        return self.data[key]


@lru_cache()
def get_config(secret_fetcher=None, env_path=ENV_PATH):
    if env_path and env_path.exists():
        return Config(RepositoryEnv(str(env_path)))

    if secret_fetcher:
        payload = secret_fetcher.fetch_secret()
        if payload is not None:
            return Config(RepositoryString(payload))

    from decouple import config

    return config


# config = get_config(GoogleSecretFetcher())
