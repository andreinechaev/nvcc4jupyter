"""
nvcc4jupyter: CUDA C++ plugin for Jupyter Notebook
"""

import argparse
import glob
import os
import shutil
import subprocess
import tempfile
import uuid
from typing import Dict, List, Optional

# pylint: disable=import-error
from IPython.core.interactiveshell import InteractiveShell
from IPython.core.magic import Magics, cell_magic, line_magic, magics_class

from .parsers import (
    Profiler,
    get_parser_cuda,
    get_parser_cuda_group_delete,
    get_parser_cuda_group_run,
    get_parser_cuda_group_save,
)
from .path_utils import CUDA_SEARCH_PATHS, find_executable
from .setup_env import setup_environment

DEFAULT_EXEC_FNAME = "cuda_exec.out"
SHARED_GROUP_NAME = "shared"


def print_out(out: str):
    """Print string line by line."""
    for line in out.split("\n"):
        print(line)


@magics_class
class NVCCPlugin(Magics):
    """
    CUDA C++ plugin for Jupyter Notebook
    """

    def __init__(self, shell: InteractiveShell):
        super().__init__(shell)
        self.shell: InteractiveShell  # type hint not provided by parent class

        self.parser_cuda = get_parser_cuda()
        self.parser_cuda_group_save = get_parser_cuda_group_save()
        self.parser_cuda_group_delete = get_parser_cuda_group_delete()
        self.parser_cuda_group_run = get_parser_cuda_group_run()

        self.workdir = tempfile.mkdtemp()
        print(f'Source files will be saved in "{self.workdir}".')

        self.profiler_paths: Dict[Profiler, Optional[str]] = {
            Profiler.NCU: None,
            Profiler.NSYS: None,
        }

    def _save_source(
        self, source_name: str, source_code: str, group_name: str
    ) -> None:
        """
        Save source code as a .cu or .h file in the group directory where
        files can be compiled together. Saving a source file to the group
        named "shared" will make those source files available when compiling
        any group.

        Args:
            source_name: The name of the source file. Must end in ".cu" or
                ".h".
            source_code: The source code to be written to the source file.
            group_name: The name of the group directory where the file will be
                saved.

        Raises:
            ValueError: If the source name does not have a proper extension.
        """
        _, ext = os.path.splitext(source_name)
        if ext not in (".cu", ".h"):
            raise ValueError(
                f'Given source name "{source_name}" must end in ".h" or ".cu".'
            )
        group_dirpath = os.path.join(self.workdir, group_name)
        os.makedirs(group_dirpath, exist_ok=True)
        source_fpath = os.path.join(group_dirpath, source_name)
        with open(source_fpath, "w", encoding="utf-8") as f:
            f.write(source_code)

    def _delete_group(self, group_name: str) -> None:
        """
        Removes all source files from the given group.

        Args:
            group_name: The name of the source files group.
        """
        group_dirpath = os.path.join(self.workdir, group_name)
        if os.path.exists(group_dirpath):
            shutil.rmtree(group_dirpath)

    def _compile(
        self,
        group_name: str,
        executable_fname: str = DEFAULT_EXEC_FNAME,
        compiler_args: str = "",
    ) -> str:
        """
        Compiles all source files in a given group together with all source
        files from the group named "shared".

        Args:
            group_name: The name of the source file group to be compiled.
            executable_fname: The output executable file name. Defaults to
                "cuda_exec.out".
            compiler_args: The optional "nvcc" compiler arguments.

        Raises:
            RuntimeError: If the group does not exist or if does not have any
                source files associated with it.

        Returns:
            The file path of the resulted executable file.
        """
        shared_dirpath = os.path.join(self.workdir, SHARED_GROUP_NAME)
        group_dirpath = os.path.join(self.workdir, group_name)
        if not os.path.exists(group_dirpath):
            raise RuntimeError(f'Group "{group_name}" does not exist.')

        source_files = list(glob.glob(os.path.join(group_dirpath, "*.cu")))
        if len(source_files) == 0:
            raise RuntimeError(
                f'Group "{group_name}" does not have any source files.'
            )
        source_files.extend(
            list(glob.glob(os.path.join(shared_dirpath, "*.cu")))
        )

        executable_fpath = os.path.join(group_dirpath, executable_fname)

        args = ["nvcc"]
        args.extend(compiler_args.split())
        args.append("-I" + shared_dirpath + "," + group_dirpath)
        args.extend(source_files)
        args.extend(["-o", executable_fpath, "-Wno-deprecated-gpu-targets"])

        subprocess.check_output(args, stderr=subprocess.STDOUT)

        return executable_fpath

    def _get_profiler_path(self, profiler: Profiler) -> str:
        """
        Get the path of the executable of a given profiling tool. Searches
        the directories of the PATH environment variable and some extra
        directories where CUDA is usually installed.

        Args:
            profiler: The profiler whose executable should be found.

        Raises:
            RuntimeError: If the profiler executable could not be found.

        Returns:
            The file path of the executable.
        """
        profiler_path = self.profiler_paths[profiler]
        if profiler_path is not None:
            return profiler_path

        profiler_path = find_executable(profiler.value, CUDA_SEARCH_PATHS)
        if profiler_path is None:
            raise RuntimeError(
                f'Could not find the "{profiler.value}" profiling tool.'
                " Consider searching for where it is installed and adding its"
                " directory to the PATH environment variable."
            )

        self.profiler_paths[profiler] = profiler_path
        return profiler_path

    def _run(  # pylint: disable=too-many-arguments
        self,
        exec_fpath: str,
        timeit: bool = False,
        profile: bool = False,
        profiler: Profiler = Profiler.NCU,
        profiler_args: str = "",
    ) -> str:
        """
        Runs a CUDA executable.

        Args:
            exec_fpath: The file path of the executable.
            timeit: If True, returns the result of the "timeit" magic instead
                of the standard output of the CUDA process. Defaults to False.
            profile: If True, the executable is profiled with NVIDIA Nsight
                Compute or NVIDIA Nsight Systems and the profiling output is
                added to stdout. Defaults to False.
            profiler: The profiling tool to use.
            profiler_args: The profiler arguments used to customize the
                information gathered by it and its overall behaviour. Defaults
                to an empty string.

        Returns:
            The standard output of the CUDA process or the "timeit" magic
            output.
        """
        if timeit:
            stmt = (
                f"subprocess.check_output(['{exec_fpath}'],"
                " stderr=subprocess.STDOUT)"
            )
            output = self.shell.run_cell_magic(
                magic_name="timeit", line="-q -o import subprocess", cell=stmt
            )
            # convert TimeitResult object to human readable string
            output = str(output)
        else:
            run_args = []
            if profile:
                profiler_path = self._get_profiler_path(profiler)
                run_args.extend([profiler_path] + profiler_args.split())
            run_args.append(exec_fpath)
            output = subprocess.check_output(
                run_args, stderr=subprocess.STDOUT
            )
            output = output.decode("utf8")

        return output

    def _compile_and_run(
        self, group_name: str, args: argparse.Namespace
    ) -> str:
        try:
            exec_fpath = self._compile(
                group_name=group_name,
                compiler_args=args.compiler_args(),
            )
            output = self._run(
                exec_fpath=exec_fpath,
                timeit=args.timeit,
                profile=args.profile,
                profiler=args.profiler(),
                profiler_args=args.profiler_args(),
            )
        except subprocess.CalledProcessError as e:
            output = e.output.decode("utf8")
        return output

    def _read_args(
        self, line: str, parser: argparse.ArgumentParser
    ) -> Optional[argparse.Namespace]:
        """
        Read arguments from the magic line. Makes sure to keep arguments
        between double quotes together for use with profiler arguments or
        compiler arguments.

        Args:
            line: The arguments on the line of the magic call in the jupyter
                cell.
            parser: The parser which will process the arguments after they are
                correctly tokenized.

        Returns:
            The parsed arguments.
        """
        tokens = line.strip().split('"')
        args_tokenized: List[str] = []
        for index, tok in enumerate(tokens):
            if index % 2 == 0:
                # tokens found outside double quotes are split at whitespace
                args_tokenized.extend(tok.split(" "))
            else:
                # anything found between double quotes will not be split
                args_tokenized.append(tok)
        args_tokenized = [arg for arg in args_tokenized if len(arg) > 0]

        try:
            return parser.parse_args(args_tokenized)
        except SystemExit:
            parser.print_help()
            return None

    @cell_magic
    def cuda(self, line: str, cell: str) -> None:
        """Compile and run the CUDA code in the cell.

        Args:
            line: The arguments on the line of the magic call in the jupyter
                cell.
            cell: All of the lines in the jupyter cell besides the magic call
                itself. It should contain all of the source code to be
                compiled and run.
        """
        args = self._read_args(line, self.parser_cuda)
        if args is None:
            return

        group_name = str(uuid.uuid4())
        self._save_source(
            source_name="single_file.cu",
            source_code=cell,
            group_name=group_name,
        )

        output = self._compile_and_run(group_name, args)
        print_out(output)

    @cell_magic
    def cuda_group_save(self, line: str, cell: str) -> None:
        """
        Save the CUDA code in the cell in a group of source files to be later
        compiled and executed by the "cuda_group_run" line magic.

        Args:
            line: The arguments on the line of the magic call in the jupyter
                cell.
            cell: All of the lines in the jupyter cell besides the magic call
                itself. It should contain all of the source code to be
                saved.
        """
        args = self._read_args(line, self.parser_cuda_group_save)
        if args is None:
            return

        self._save_source(
            source_name=args.name,
            source_code=cell,
            group_name=args.group,
        )

    @line_magic
    def cuda_group_run(self, line: str) -> None:
        """
        Compile and run all source files inside a specific source file group.

        Args:
            line: The arguments on the line of the magic call in the jupyter
                cell.
        """
        args = self._read_args(line, self.parser_cuda_group_run)
        if args is None:
            return

        output = self._compile_and_run(args.group, args)
        print_out(output)

    @line_magic
    def cuda_group_delete(self, line: str) -> None:
        """
        Remove all source files inside a specific source file group.

        Args:
            line: The arguments on the line of the magic call in the jupyter
                cell.
        """
        args = self._read_args(line, self.parser_cuda_group_delete)
        if args is None:
            return

        self._delete_group(args.group)


def load_ipython_extension(shell: InteractiveShell):
    """
    Method used by IPython to load the extension.
    """
    setup_environment()
    nvcc_plugin = NVCCPlugin(shell)
    shell.register_magics(nvcc_plugin)
