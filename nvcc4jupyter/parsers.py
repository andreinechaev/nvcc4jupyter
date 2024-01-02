import argparse


def get_parser_cuda() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda magic that compiles and runs CUDA C++ code in this cell."
        )
    )
    parser.add_argument(
        "-t",
        "--timeit",
        action="store_true",
        help=(
            'If set, returns the output of the "timeit" built-in ipython magic'
            " instead of stdout."
        ),
    )
    parser.add_argument(
        "-p",
        "--profile",
        action="store_true",
        help=(
            "If set, runs the nvidia nsight compute profiler. Has no effect if"
            " used with --timeit."
        ),
    )
    parser.add_argument(
        "-a",
        "--profiler-args",
        type=str,
        default="",
        help=(
            "Extra options that can be passed to the nvidia nsight compute"
            " profiler. Must be the last option given to the argument parser"
            " so you can pass arguments with dashes."
        ),
    )
    return parser


def get_parser_cuda_group_run() -> argparse.ArgumentParser:
    parser = get_parser_cuda()
    parser.description = (
        "%%cuda_group_run magic that compiles and runs source files in a"
        " given group."
    )
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        required=True,
        help="The group whose files should be compiled and executed.",
    )
    return parser


def get_parser_cuda_group_save() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda_group_save magic that saves CUDA C++ code in this cell for"
            " later compilation and execution with possibly more source files."
        )
    )
    parser.add_argument(
        "-n",
        "--name",
        type=str,
        required=True,
        help=(
            'The name of the saved source file. Must have either the ".cu" or'
            ' ".h" extension. In order to import a header file saved with this'
            " magic you can simply add '#include \"<name>\"'."
        ),
    )
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        required=True,
        help=(
            "The group to which to add the saved source file. Groups are"
            " source files that get compiled together and do not interact with"
            " other groups. This allows you to have multiple unrelated CUDA"
            " programs within the same jupyter notebook. Adding files to a"
            ' group named "shared" will make them available to all other'
            " source file groups. One use case for this is sharing error"
            " handling code."
        ),
    )
    return parser


def get_parser_cuda_group_delete() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "%%cuda_group_reset magic that deletes all files in a group."
        )
    )
    parser.add_argument(
        "-g",
        "--group",
        type=str,
        required=True,
        help="The group whose files should be deleted.",
    )
    return parser

