#!/usr/bin/env python

from setuptools import find_packages, setup

setup(name='ai_embedder',
      version='1.0',
      description='This script takes .ai files and save them with linked files embedded.',
      author='mdobosz',
      author_email='doboszsite@gmail.com',
      packages=find_packages(),
      long_description="This script takes .ai files and save them with linked files embedded.",
      install_requires=[
            "altgraph==0.17.3",
           " pefile==2023.2.7",
            "pywin32==306",
            "pywin32-ctypes==0.2.1"
      ]
      )
