#!/usr/bin/env python
import os

from setuptools import find_packages, setup

with open("README.md", "r") as readme_file:
    README = readme_file.read()


def _get_version():
    version = os.getenv("RELEASE_VERSION", default="1.0")
    if version.startswith("v"):
        version = version[1:]
    return version


setup(name='ai_embedder',
      version=_get_version(),
      description='This script takes .ai files and save them with linked files embedded.',
      author='mdobosz',
      author_email='doboszsite@gmail.com',
      packages=find_packages(),
      long_description_content_type="text/markdown",
      long_description=README,
      install_requires=[
            "pywin32==306",
            "pywin32-ctypes==0.2.1"
      ]
      )
