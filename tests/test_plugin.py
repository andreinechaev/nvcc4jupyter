import math
import os
import re
import shutil
import subprocess
from argparse import ArgumentParser, Namespace
from copy import deepcopy
from typing import List

import pytest

from nvcc4jupyter.parsers import Profiler, get_parser_cuda, set_defaults
from nvcc4jupyter.plugin import NVCCPlugin


def check_profiler_output(output: str, profiler: str = "[NCU]"):
    # the output from the profiler will first be a line containing only
    # "[NCU]" or "[NSYS]" depending on what profiler was used and another
    # line containing the string "Hello World!"
    lines = output.strip().split("\n")
    assert len(lines) >= 2
    assert lines[0] == profiler
    assert lines[1] == "Hello World!"


def copy_source_to_group(
    source_fpath: str, group_name: str, workdir: str
) -> str:
    group_dirpath = os.path.join(workdir, group_name)
    os.makedirs(group_dirpath, exist_ok=True)
    destination_fpath = os.path.join(
        group_dirpath, os.path.basename(source_fpath)
    )
    shutil.copy(source_fpath, destination_fpath)
    return destination_fpath


@pytest.fixture(autouse=True, scope="session")
def before_all(scripts_path: str):
    os.environ["PATH"] = scripts_path + os.pathsep + os.environ["PATH"]


@pytest.fixture(autouse=True, scope="function")
def before_each(plugin: NVCCPlugin):
    # BEFORE TESTS
    set_defaults(profiler=Profiler.NCU, compiler_args="", profiler_args="")
    shutil.rmtree(plugin.workdir, ignore_errors=True)
    yield
    # AFTER TESTS
    pass


def test_save_source(plugin: NVCCPlugin, sample_cuda_code: str) -> None:
    gname = "test_save_source"
    sname = "sample.cu"
    plugin._save_source(sname, sample_cuda_code, gname)
    spath = os.path.join(plugin.workdir, gname, sname)
    assert os.path.exists(spath)
    with open(spath, "r", encoding="utf-8") as f:
        code = f.read()
    assert code == sample_cuda_code

    with pytest.raises(ValueError):
        plugin._save_source("wrong_extension.txt", sample_cuda_code, gname)


def test_delete_group(plugin: NVCCPlugin, sample_cuda_fpath: str) -> None:
    gname = "test_delete_group"
    source_fpath = copy_source_to_group(
        sample_cuda_fpath, gname, plugin.workdir
    )
    assert os.path.exists(source_fpath)
    plugin._delete_group(gname)
    assert not os.path.exists(source_fpath)


def test_compile(
    plugin: NVCCPlugin,
    sample_cuda_fpath: str,
):
    # we artificially create a source file group in the plugin workdir
    gname = "test_compile"
    source_fpath = copy_source_to_group(
        sample_cuda_fpath, gname, plugin.workdir
    )

    exec_fpath = plugin._compile(gname)
    assert os.path.exists(exec_fpath)

    with pytest.raises(RuntimeError):
        plugin._compile("inexistent_group")

    with pytest.raises(RuntimeError):
        os.remove(source_fpath)
        plugin._compile(gname)


def test_compile_args(
    plugin: NVCCPlugin,
    compiler_cpp_17_fpath: str,
    default_args: Namespace,
):
    gname = "test_compile_args"
    copy_source_to_group(compiler_cpp_17_fpath, gname, plugin.workdir)

    exec_fpath = plugin._compile(gname, compiler_args="--std c++17")
    assert os.path.exists(exec_fpath)

    # should fail due to the source file having c++ 17 features
    with pytest.raises(subprocess.CalledProcessError):
        exec_fpath = plugin._compile(gname, compiler_args="--std c++14")

    args = deepcopy(default_args)
    args.compiler_args = lambda: "--std c++14"
    output = plugin._compile_and_run(group_name=gname, args=args)
    assert "errors detected in the compilation of" in output


def test_compile_opencv(
    plugin: NVCCPlugin,
    compiler_opencv_fpath: str,
    default_args: Namespace,
):
    gname = "test_compile_opencv"
    copy_source_to_group(compiler_opencv_fpath, gname, plugin.workdir)

    # check that "pkg-config" exists
    assert subprocess.check_call(["which", "pkg-config"]) == 0

    pkg_config_args = ["pkg-config", "--cflags", "--libs", "opencv4"]
    opencv_compile_options = (
        subprocess.check_output(args=pkg_config_args).decode().strip()
    )

    args = deepcopy(default_args)
    args.compiler_args = lambda: opencv_compile_options
    output = plugin._compile_and_run(group_name=gname, args=args)
    assert "General configuration for OpenCV" in output


def test_run(
    plugin: NVCCPlugin,
    sample_cuda_fpath: str,
):
    gname = "test_run"
    copy_source_to_group(sample_cuda_fpath, gname, plugin.workdir)

    exec_fpath = plugin._compile(gname)
    output = plugin._run(exec_fpath)
    assert output == "Hello World!\n"


def test_run_timeit(
    plugin: NVCCPlugin, sample_cuda_fpath: str, timeit_regex: str
):
    gname = "test_run_timeit"
    copy_source_to_group(sample_cuda_fpath, gname, plugin.workdir)

    exec_fpath = plugin._compile(gname)
    output = plugin._run(exec_fpath, timeit=True)
    assert (
        re.match(timeit_regex, output) is not None
    ), f'Output "{output}" does not match the regex "{timeit_regex}".'


def test_run_profile(plugin: NVCCPlugin, sample_cuda_fpath: str):
    gname = "test_run_profile"
    copy_source_to_group(sample_cuda_fpath, gname, plugin.workdir)

    exec_fpath = plugin._compile(gname)
    output = plugin._run(
        exec_fpath,
        profile=True,
        # because we are running without a kernel (in the test env we have no
        # GPU) it does not matter what arguments we pass to the profiler as its
        # output will always be just a few warnings; the reason we add them
        # here is to test that no error is produced when passing the arguments
        profiler_args=(
            "--metrics l1tex__t_sectors_pipe_lsu_mem_global_op_ld.sum"
        ),
    )
    check_profiler_output(output)


def test_compile_and_run_multiple_files(
    plugin: NVCCPlugin,
    multiple_source_fpaths: List[str],
    default_args: Namespace,
):
    """
    Compiles and executes 3 cuda source files from
    tests/fixtures/multiple_files.
    """
    gname = "test_compile_and_run_multiple_files"
    for fpath in multiple_source_fpaths:
        copy_source_to_group(fpath, gname, plugin.workdir)
    output = plugin._compile_and_run(group_name=gname, args=default_args)
    check_profiler_output(output)


def test_compile_and_run_multiple_files_shared(
    plugin: NVCCPlugin,
    multiple_source_fpaths: List[str],
    default_args: Namespace,
):
    """
    Compiles and executes 3 cuda source files from
    tests/fixtures/multiple_files. However, the hello.cu and hello.h files are
    added to the "shared" group which is compiled with all other groups. This
    allows sharing error handling code easily and other very common code.
    """
    gname = "test_compile_and_run_multiple_files_shared"
    for fpath in multiple_source_fpaths:
        fname = os.path.basename(fpath)
        if fname == "main.cu":
            copy_source_to_group(fpath, gname, plugin.workdir)
        else:
            copy_source_to_group(fpath, "shared", plugin.workdir)
    output = plugin._compile_and_run(group_name=gname, args=default_args)
    check_profiler_output(output)


def test_read_args(plugin: NVCCPlugin):
    parser = ArgumentParser()
    parser.add_argument("-a", type=str, required=True)
    parser.add_argument("-b", type=float, required=True)
    args = plugin._read_args(
        '-a "--this has --spaces and --dashes" -b 0.75', parser
    )
    assert args.a == "--this has --spaces and --dashes"
    assert math.isclose(args.b, 0.75)


def test_set_defaults():
    parser = get_parser_cuda()
    args = parser.parse_args([])
    assert args.profiler_args() == ""
    assert args.compiler_args() == ""
    set_defaults(profiler_args="123")
    args = parser.parse_args([])
    assert args.profiler_args() == "123"
    assert args.compiler_args() == ""
    set_defaults(compiler_args="456")
    args = parser.parse_args([])
    assert args.profiler_args() == "123"
    assert args.compiler_args() == "456"
    set_defaults(profiler_args="")
    args = parser.parse_args([])
    assert args.profiler_args() == ""
    assert args.compiler_args() == "456"
    set_defaults(profiler_args="123")
    args = parser.parse_args(["--profiler-args", "789"])
    assert args.profiler_args() == "789"
    assert args.compiler_args() == "456"


def test_magic_cuda(
    capsys,
    plugin: NVCCPlugin,
    sample_cuda_code: str,
    sample_magic_cu_line: str,
):
    plugin.cuda(sample_magic_cu_line, sample_cuda_code)
    check_profiler_output(capsys.readouterr().out)


def test_magic_cuda_set_default_profiler(
    capsys,
    plugin: NVCCPlugin,
    sample_cuda_code: str,
    sample_magic_cu_line: str,
):
    # set the default profiler to Nsight Systems
    set_defaults(profiler=Profiler.NSYS)
    plugin.cuda(sample_magic_cu_line, sample_cuda_code)
    check_profiler_output(capsys.readouterr().out, profiler="[NSYS]")


def test_magic_cuda_bad_args(
    capsys,
    plugin: NVCCPlugin,
    sample_cuda_code: str,
):
    plugin.cuda("--this-is-an-unrecognized-argument", sample_cuda_code)
    output = capsys.readouterr().out
    assert output.startswith("usage: ")


def test_magic_cuda_group_save(plugin: NVCCPlugin, sample_cuda_code: str):
    gname = "test_save_source"
    sname = "sample.cu"
    plugin.cuda_group_save(f"-g {gname} -n {sname}", sample_cuda_code)
    spath = os.path.join(plugin.workdir, gname, sname)
    assert os.path.exists(spath)
    with open(spath, "r", encoding="utf-8") as f:
        code = f.read()
    assert code == sample_cuda_code


def test_magic_cuda_group_run(
    capsys, plugin: NVCCPlugin, sample_cuda_fpath: str
):
    gname = "test_magic_cuda_group_run"
    copy_source_to_group(sample_cuda_fpath, gname, plugin.workdir)
    plugin.cuda_group_run(f"--group {gname} --profile")
    check_profiler_output(capsys.readouterr().out)


def test_magic_cuda_group_delete(plugin: NVCCPlugin, sample_cuda_fpath: str):
    gname = "test_magic_cuda_group_run"
    source_fpath = copy_source_to_group(
        sample_cuda_fpath, gname, plugin.workdir
    )
    assert os.path.exists(source_fpath)
    plugin.cuda_group_delete(f"--group {gname}")
    assert not os.path.exists(source_fpath)
