import os
import sys
import argparse
import subprocess

from shlex import quote
from IPython.core.magic import (
    Magics, cell_magic, magics_class)
from IPython.core.magic_arguments import (
    argument, magic_arguments)
from IPython.utils.process import arg_split

from .errors import NVCCUnsupportedInputFile, NVCCUnspecifiedCompiler


DEFAULT_COMPILER_PATH = '/usr/local/cuda/bin/nvcc'
SUPPORTED_INPUT = ('.cu', '.c', '.cc', '.cxx', '.cpp', '.ptx', '.cubin', '.fatbin', '.o', '.obj', '.a', '.lib', '.res', '.so')


@magics_class
class NVCCPlugin(Magics):

    def __init__(self, shell):
        super(NVCCPlugin, self).__init__(shell)
        current_dir = os.getcwd()
        self.output_dir = os.path.join(current_dir, 'nvcc_src')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.out = os.path.join(current_dir, "compile.out")
        self.compiler = DEFAULT_COMPILER_PATH


    def compile(self, compiler_args, inputfile):
        options = (quote(arg) for arg in compiler_args)
        try:
            output = subprocess.check_output([
                self.compiler, '-I', quote(self.output_dir), '-o', quote(self.out), *options, inputfile],
                stderr=subprocess.STDOUT, shell=True
            )
        except FileNotFoundError:
            raise NVCCUnspecifiedCompiler(
                'The system cannot find the specified nvcc compiler')
        return output.decode('utf8')

    def run(self):
        output = subprocess.check_output(
            [self.out], stderr=subprocess.STDOUT, shell=True)
        return output.decode('utf8')

    @magic_arguments()
    @argument('-n', '--name', type=str, help='File name that will be produced by the cell.')
    @argument('-c', '--compile', action='store_true', help='Should be compiled?')
    @cell_magic
    def cuda(self, line, cell):
        argv = arg_split(line, posix=not sys.platform.startswith('win'))
        cell_args, compiler_args = self.cuda.parser.parse_known_args(argv)

        _, file_extension = os.path.splitext(cell_args.name)
        if file_extension not in SUPPORTED_INPUT:
            raise NVCCUnsupportedInputFile(
                f'{file_extension} unsupported input file suffixes')

        file_path = os.path.join(self.output_dir, cell_args.name)
        with open(file_path, 'w') as sourse_file:
            sourse_file.write(cell)

        if cell_args.compile:
            compile_output = self.compile(compiler_args, file_path)
            print(compile_output)
            return self.run()

        # if cell_args.compile:
        #     try:
        #         self.compile(self.output_dir, file_path, self.out)
        #         output = self.run()
        #     except subprocess.CalledProcessError as e:
        #         print(e.output.decode("utf8"))
        #         output = None
        # else:
        #     output = f'File written in {file_path}'

        # return output

    # @cell_magic
    # def cuda_run(self, line='', cell=None):
    #     try:
    #         args = self.argparser.parse_args(line.split())
    #     except SystemExit:
    #         self.argparser.print_help()
    #         return

    #     try:
    #         cuda_src = os.listdir(self.output_dir)
    #         cuda_src = [os.path.join(self.output_dir, x) for x in cuda_src if x[-3:] == '.cu']
    #         print(f'found sources: {cuda_src}')
    #         self.compile(self.output_dir, ' '.join(cuda_src), self.out)
    #         output = self.run(timeit=args.timeit)
    #     except subprocess.CalledProcessError as e:
    #         print(e.output.decode("utf8"))
    #         output = None

    #     return output
