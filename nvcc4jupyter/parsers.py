import argparse


def get_parser_cuda() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda magic that compiles and runs CUDA C++ code in this cell."
            " See https://nvcc4jupyter.readthedocs.io/en/latest/magics.html#cuda"
            " for usage details."
        )
    )
    parser.add_argument("-t", "--timeit", action="store_true")
    parser.add_argument("-p", "--profile", action="store_true")
    parser.add_argument("-a", "--profiler-args", type=str, default="")
    return parser


def get_parser_cuda_group_run() -> argparse.ArgumentParser:
    parser = get_parser_cuda()
    parser.description = (
        "%%cuda_group_run magic that compiles and runs source files in a given"
        " group. See"
        " https://nvcc4jupyter.readthedocs.io/en/latest/magics.html#cuda-group-run"
        " for usage details."
    )
    parser.add_argument("-g", "--group", type=str, required=True)
    return parser


def get_parser_cuda_group_save() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda_group_save magic that saves CUDA C++ code in this cell for"
            " later compilation and execution with possibly more source files."
            " See https://nvcc4jupyter.readthedocs.io/en/latest/magics.html#cuda-group-save"
            " for usage details."
        )
    )
    parser.add_argument("-n", "--name", type=str, required=True)
    parser.add_argument("-g", "--group", type=str, required=True)
    return parser


def get_parser_cuda_group_delete() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda_group_delete magic that deletes all files in a group. See"
            " https://nvcc4jupyter.readthedocs.io/en/latest/magics.html#cuda-group-delete"
            " for usage details."
        )
    )
    parser.add_argument("-g", "--group", type=str, required=True)
    return parser
