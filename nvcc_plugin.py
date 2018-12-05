import os
import uuid
import timeit
import argparse
import tempfile
import subprocess
import IPython.core.magic as ipym
from IPython.core.magic_arguments import (argument, magic_arguments,
                                          parse_argstring)

compiler = '/usr/local/cuda/bin/nvcc'
ext = '.cu'


def get_argparser():
    parser = argparse.ArgumentParser(description='NVCCPlugin params')
    parser.add_argument("-t", "--timeit", action='store_true',
                        help='flag to return timeit result instead of stdout')
    return parser


@ipym.magics_class
class NVCCPlugin(ipym.Magics):

    def __init__(self, shell):
        super(NVCCPlugin, self).__init__(shell)
        self.argparser = get_argparser()

    @staticmethod
    def compile(file_path):
        subprocess.check_output([compiler, file_path + ext, "-o", file_path + ".out"], stderr=subprocess.STDOUT)

    def run(self, file_path, timeit=False):
        if timeit:
            stmt = f"subprocess.check_output(['{file_path}.out'], stderr=subprocess.STDOUT)"
            output = self.shell.run_cell_magic(magic_name="timeit", line="-q -o import subprocess", cell=stmt)
        else:
            output = subprocess.check_output([file_path + ".out"], stderr=subprocess.STDOUT)
            output = output.decode('utf8')
        return output

    @ipym.cell_magic
    def cu(self, line, cell):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit as e:
            self.argparser.print_help()
            return

        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = os.path.join(tmp_dir, str(uuid.uuid4()))
            with open(file_path + ext, "w") as f:
                f.write(cell)
            try:
                self.compile(file_path)
                output = self.run(file_path, timeit=args.timeit)
            except subprocess.CalledProcessError as e:
                print(e.output.decode("utf8"))
                output = None
        return output


out = "result.out"


@ipym.magics_class
class NVCCPluginV2(ipym.Magics):

    def __init__(self, shell):
        super(NVCCPluginV2, self).__init__(shell)
        with tempfile.TemporaryDirectory() as tmp:
            self.output_dir = os.path.join(tmp, str(uuid.uuid4()))

    @staticmethod
    def compile(file_path):
        subprocess.check_output([compiler, file_path, "-o", out], stderr=subprocess.STDOUT)

    def run(self, file_path, timeit=False):
        if timeit:
            stmt = f"subprocess.check_output(['{out}'], stderr=subprocess.STDOUT)"
            output = self.shell.run_cell_magic(magic_name="timeit", line="-q -o import subprocess", cell=stmt)
        else:
            output = subprocess.check_output([file_path + ".out"], stderr=subprocess.STDOUT)
            output = output.decode('utf8')
        return output

    @magic_arguments
    @argument('-n', '--name', type=str, help='file name that will be produced by the cell. must end with .cu extension')
    @argument('-c', '--compile', type=bool, help='Should be compiled?')
    @ipym.cell_magic
    def cuda(self, line='', cell=None):
        args = parse_argstring(self.cuda, line)
        if args.name[:-3] != '.cu':
            raise Exception('name must end with .cu')

        file_path = os.path.join(self.tmp_dir, args.name)
        with open(file_path, "w") as f:
            f.write(cell)

        if args.compile:
            try:
                self.compile(file_path)
                output = self.run(file_path, timeit=args.timeit)
            except subprocess.CalledProcessError as e:
                print(e.output.decode("utf8"))
                output = None
        else:
            output = f'File written in {file_path}'

        return output

    @ipym.cell_magic
    def cuda_run(self, line='', cell=None):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit:
            self.argparser.print_help()
            return

        try:
            self.compile('*.cu')
            output = self.run(out, timeit=args.timeit)
        except subprocess.CalledProcessError as e:
            print(e.output.decode("utf8"))
            output = None

        return output


def load_ipython_extension(ip):
    nvcc_plugin = NVCCPlugin(ip)
    ip.register_magics(nvcc_plugin)

    nvcc_plugin_v2 = NVCCPluginV2(ip)
    ip.register_magics(nvcc_plugin_v2)
