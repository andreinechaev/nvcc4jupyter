import argparse
import glob
import os

import pytest
from IPython.core.interactiveshell import InteractiveShell

from nvcc4jupyter.parsers import Profiler
from nvcc4jupyter.plugin import NVCCPlugin


@pytest.fixture(scope="session")
def shell():
    return InteractiveShell()


@pytest.fixture(scope="session")
def plugin(shell: InteractiveShell):
    return NVCCPlugin(shell=shell)


@pytest.fixture(scope="session")
def tests_path():
    return "tests"


@pytest.fixture(scope="session")
def fixtures_path(tests_path):
    return os.path.join(tests_path, "fixtures")


@pytest.fixture(scope="session")
def scripts_path(fixtures_path: str):
    return os.path.join(fixtures_path, "scripts")


@pytest.fixture(scope="session")
def compiler_cpp_17_fpath(fixtures_path: str):
    return os.path.join(fixtures_path, "compiler", "cpp_17.cu")


@pytest.fixture(scope="session")
def compiler_opencv_fpath(fixtures_path: str):
    return os.path.join(fixtures_path, "compiler", "opencv.cu")


@pytest.fixture(scope="session")
def sample_magic_cu_line():
    # fmt: off
    return '--profile --profiler-args "--metrics l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum" --compiler-args "--optimize 3"'  # noqa: E501
    # fmt: on


@pytest.fixture(scope="session")
def sample_cuda_fpath(fixtures_path: str):
    return os.path.join(fixtures_path, "single_file", "hello.cu")


@pytest.fixture(scope="session")
def sample_cuda_code(sample_cuda_fpath: str):
    with open(sample_cuda_fpath, "r", encoding="utf-8") as f:
        return f.read()


@pytest.fixture(scope="session")
def timeit_regex():
    return r".+ ± .+ per loop \(mean ± std. dev. of .+ runs, .+ loops each\)"


@pytest.fixture(scope="session")
def multiple_source_fpaths(fixtures_path: str):
    pattern_h = os.path.join(fixtures_path, "multiple_files", "*.h")
    pattern_cu = os.path.join(fixtures_path, "multiple_files", "*.cu")
    return list(glob.glob(pattern_h)) + list(glob.glob(pattern_cu))


@pytest.fixture(scope="session")
def default_args():
    return argparse.Namespace(
        timeit=False,
        profile=True,
        profiler=lambda: Profiler.NCU,
        profiler_args=lambda: "",
        compiler_args=lambda: "",
    )
