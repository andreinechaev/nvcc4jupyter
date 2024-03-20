import os

from nvcc4jupyter.path_utils import find_executable


def test_which():
    assert find_executable("ls") == "/usr/bin/ls"


def test_find_executable(fixtures_path: str):
    exec_path = find_executable("searchforme", [fixtures_path])
    assert exec_path is not None

    exec_dir, exec_fname = os.path.split(exec_path)
    assert exec_fname == "searchforme"
    assert os.path.basename(exec_dir) == "scripts"
