"""
nvcc4jupyter: CUDA C++ plugin for Jupyter Notebook
"""

from .parsers import set_defaults  # noqa: F401
from .plugin import NVCCPlugin, load_ipython_extension  # noqa: F401

__version__ = "1.1.0"
