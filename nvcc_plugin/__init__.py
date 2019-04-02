from .magics import NVCCPlugin


def load_ipython_extension(ip):
    nvcc_plugin = NVCCPlugin(ip)
    ip.register_magics(nvcc_plugin)
