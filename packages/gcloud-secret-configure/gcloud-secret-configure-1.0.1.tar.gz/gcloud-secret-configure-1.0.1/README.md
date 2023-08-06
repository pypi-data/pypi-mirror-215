# irregular-chars
Configure environment variables from Google Cloud Secret Manager

inspired by: https://github.com/codingforentrepreneurs/Serverless-Container-Based-Python-App-on-Google-Cloud-Run

## Installation

You can install the package via pip:
```bash
pip install gcloud_secret_configure
```

## Usage
```py
from gcloud_secret_configure import get_config, GoogleSecretFetcher

# 'secret_label' must be the label of the uploaded secret
config = get_config(GoogleSecretFetcher(), secret_label="py_env_file")
MODE = config("MODE", cast=str, default="test")
```

## Prerequest
- Your environment is already authenticated to GoogleCloud
- Your secret has already been uploaded.
