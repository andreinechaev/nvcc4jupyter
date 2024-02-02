"""
Helper functions relating to file paths.
"""

import os
from glob import glob
from typing import List, Optional

CUDA_SEARCH_PATHS: List[str] = [
    "/opt/nvidia/nsight-compute",
    "/usr/local/cuda",
    "/opt",
    "/usr",
]


def is_executable(fpath: str) -> bool:
    """Check if file exists and is executable"""
    return os.path.isfile(fpath) and os.access(fpath, os.X_OK)


def which(name: str) -> Optional[str]:
    """Find an executable by name by searching the PATH directories"""
    for path_dir in os.environ.get("PATH", "").split(os.pathsep):
        exec_path = os.path.join(path_dir, name)
        if is_executable(exec_path):
            return exec_path
    return None


def find_executable(
    name: str, search_paths: Optional[List[str]] = None
) -> Optional[str]:
    """
    Find an executable, either by searching in the directories of the PATH
    environment variable or, if that did not work, by searching recursively
    in directories a list given as parameter.

    Args:
        name: The name of the executable to be found.
        search_paths: If None, only executables that are available from PATH
            will be found. Otherwise, will recursively search these
            directories. Defaults to None.

    Returns:
        The path to the executable if it is found, and None otherwise.
    """
    if search_paths is None:
        search_paths = []

    which_path = which(name)
    if which_path is not None:
        return which_path

    for search_path in search_paths:
        search_path = os.path.abspath(search_path)
        search_path = os.path.join(search_path, f"**/{name}")
        for exec_path in glob(search_path, recursive=True):
            return exec_path

    return None
