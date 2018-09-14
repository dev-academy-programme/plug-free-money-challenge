#!/usr/bin/env python
import setuptools


version = "0.0.1"

install_requires = (
)

setuptools.setup(
    name="free_money_challenge",
    version=version,
    author="Harrison Symes",
    author_email="symeshjb@gmail.com",
    url="https://github.com/free_money_challenge",
    packages=["free_money_challenge"],
    install_requires=install_requires,

    extras_require={
        "test": (
            "asynctest",
            "pytest > 3.3.2",
            "pytest-aiohttp",
            "pytest-asyncio",
        ),
        "dev": (
            "flake8",
            "flake8-commas",
            "flake8-isort",
            "flake8-mypy",
            "flake8-quotes",
            "pytest-cov",
        ),
    },
)
