from setuptools import find_packages, setup

setup(
    name="gcloud-secret-configure",
    version="1.0.0",
    description="A package to configure environment variables from Google Cloud Secret Manager",
    packages=find_packages(),
    install_requires=[],
    classifiers=[  # https://pypi.org/classifiers/
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
    ],
    author="Masato Emata",
    url="https://github.com/masatoEmata/cloud_secret_configure",
    keywords="google cloud secret manager environment variables",
)
