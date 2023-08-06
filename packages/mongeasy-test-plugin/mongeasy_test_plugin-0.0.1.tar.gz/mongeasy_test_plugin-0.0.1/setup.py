#!/usr/bin/env python

from setuptools import setup, find_packages

with open("README.md", encoding="utf8") as f:
    readme = f.read()


setup(
    name="mongeasy_test_plugin",
    version="0.0.1",
    author="Joakim Wassberg",
    author_email="joakim.wassberg@arthead.se",
    description="Small package to test mongeasy plugin system",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/artheadsweden/mongeasy_test_plugin",
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Database",
    ],
    packages=find_packages(),
    install_requires=["mongeasy>=0.2.0"],
)