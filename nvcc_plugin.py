from IPython.core.interactiveshell import InteractiveShell

from v1.v1 import NVCCPlugin as NVCC_V1


def load_ipython_extension(shell: InteractiveShell):
    nvcc_plugin = NVCC_V1(shell)
    shell.register_magics(nvcc_plugin)
