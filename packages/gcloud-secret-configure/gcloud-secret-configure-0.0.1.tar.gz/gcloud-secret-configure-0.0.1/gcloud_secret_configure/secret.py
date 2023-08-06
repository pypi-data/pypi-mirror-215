from abc import ABC, abstractmethod

import google.auth
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import secretmanager


class SecretFetcher(ABC):
    """
    Abstract class to define interface for fetching secrets.
    """

    @abstractmethod
    def fetch_secret(self):
        pass


class GoogleSecretFetcher(SecretFetcher):
    """
    Concrete implementation for fetching secrets from Google Cloud.
    """

    def fetch_secret(self, secret_label="env_file", version="latest") -> str | None:
        try:
            _, project_id = google.auth.default()
        except DefaultCredentialsError:
            project_id = None

        if project_id is None:
            return None

        client = secretmanager.SecretManagerServiceClient()

        gcloud_secret_name = (
            f"projects/{project_id}/secrets/{secret_label}/versions/{version}"
        )

        payload = client.access_secret_version(
            name=gcloud_secret_name
        ).payload.data.decode("UTF-8")
        return payload
