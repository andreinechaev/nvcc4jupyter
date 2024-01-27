"""
Parsers for the CUDA magic commands.
"""

import argparse
from typing import Callable, Optional

_default_profiler_args: str = ""
_default_compiler_args: str = ""


def set_defaults(
    compiler_args: Optional[str] = None, profiler_args: Optional[str] = None
) -> None:
    """
    Set the default values for various arguments of the magic commands. These
    values will be used if the user does not explicitly provide those arguments
    to override this behaviour on a cell by cell basis.

    Args:
        compiler_args: If not None, this value becomes the new default compiler
            config. Defaults to "".
        profiler_args: If not None, this value becomes the new default profiler
            config. Defaults to "".
    """

    # pylint: disable=global-statement
    global _default_compiler_args
    global _default_profiler_args
    if compiler_args is not None:
        _default_compiler_args = compiler_args
    if profiler_args is not None:
        _default_profiler_args = profiler_args


def str_to_lambda(arg: str) -> Callable[[], str]:
    """Convert argparse string to lambda"""
    return lambda: arg


def get_parser_cuda() -> argparse.ArgumentParser:
    """
    %%cuda magic command parser.
    """
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda magic that compiles and runs CUDA C++ code in this cell."
            " See https://nvcc4jupyter.readthedocs.io/en/latest/magics.html#cuda"  # noqa: E501
            " for usage details."
        )
    )
    parser.add_argument("-t", "--timeit", action="store_true")
    parser.add_argument("-p", "--profile", action="store_true")

    # --profiler-args and --compiler-args values are lambda functions to allow
    # changing the default value at runtime
    parser.add_argument(
        "-a",
        "--profiler-args",
        type=str_to_lambda,
        default=lambda: _default_profiler_args,
    )
    parser.add_argument(
        "-c",
        "--compiler-args",
        type=str_to_lambda,
        default=lambda: _default_compiler_args,
    )

    return parser


def get_parser_cuda_group_run() -> argparse.ArgumentParser:
    """
    %%cuda_group_run magic command parser.
    """
    parser = get_parser_cuda()
    parser.description = (
        "%%cuda_group_run magic that compiles and runs source files in a given"
        " group. See"
        " https://nvcc4jupyter.readthedocs.io/en/latest/magics.html#cuda-group-run"  # noqa: E501
        " for usage details."
    )
    parser.add_argument("-g", "--group", type=str, required=True)
    return parser


def get_parser_cuda_group_save() -> argparse.ArgumentParser:
    """
    %%cuda_group_save magic command parser.
    """
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda_group_save magic that saves CUDA C++ code in this cell for"
            " later compilation and execution with possibly more source files."
            " See https://nvcc4jupyter.readthedocs.io/en/latest/magics.html#cuda-group-save"  # noqa: E501
            " for usage details."
        )
    )
    parser.add_argument("-n", "--name", type=str, required=True)
    parser.add_argument("-g", "--group", type=str, required=True)
    return parser


def get_parser_cuda_group_delete() -> argparse.ArgumentParser:
    """
    %%cuda_group_delete magic command parser.
    """
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda_group_delete magic that deletes all files in a group. See"
            " https://nvcc4jupyter.readthedocs.io/en/latest/magics.html#cuda-group-delete"  # noqa: E501
            " for usage details."
        )
    )
    parser.add_argument("-g", "--group", type=str, required=True)
    return parser
