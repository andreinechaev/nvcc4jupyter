from v1.v1 import NVCCPlugin as NVCC_V1
from v2.v2 import NVCCPluginV2 as NVCC_V2


def load_ipython_extension(ip):
    nvcc_plugin = NVCC_V1(ip)
    ip.register_magics(nvcc_plugin)

    nvcc_plugin_v2 = NVCC_V2(ip)
    ip.register_magics(nvcc_plugin_v2)
