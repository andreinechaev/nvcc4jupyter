#!/bin/bash

# install developer dependencies
pip install -e .[dev]

# make sure the developer uses pre-commit hooks
pre-commit install
