#!/usr/bin/env python

"""
  Copyright (c) 2025, SunSpec Alliance
  All Rights Reserved
"""

from setuptools import setup

setup(
    name='pysunspec2',
    version='1.3.2',
    description='Python SunSpec Tools',
    license="Apache Software License, Version 2.0",
    author='SunSpec Alliance',
    author_email='support@sunspec.org',
    url='https://sunspec.org/',
    packages=['sunspec2', 'sunspec2.modbus', 'sunspec2.file', 'sunspec2.tests'],
    package_data={
      'sunspec2.tests': ['test_data/*', 'tls_data/*'],
      'sunspec2': ['models/json/*'],
    },
    scripts=['scripts/suns.py'],
    python_requires='>=3.5',
    extras_require={
      'serial': ['pyserial'],
      'excel': ['openpyxl'],
      'test': ['pytest'],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
