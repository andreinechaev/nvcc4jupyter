"""
Helper functions relating to the GPU architecture code is compiled for.
"""

import re
import subprocess
from functools import lru_cache
from typing import List, Optional

from .path_utils import find_executable

QUERY_TIMEOUT_SECONDS: int = 30

# "nvcc" rejects a redefined architecture option, so we must not add our own
# if the user already provided any of these
ARCH_OPTION_PREFIXES = (
    "-arch",
    "--gpu-architecture",
    "-code",
    "--gpu-code",
    "-gencode",
    "--generate-code",
)

COMPUTE_CAP_PATTERN = re.compile(r"^(\d+)\.(\d+)$")


def _query(args: List[str]) -> Optional[str]:
    """Run a CUDA setup query, returning None if it is unavailable or fails"""
    exec_path = find_executable(args[0])
    if exec_path is None:
        return None

    try:
        output = subprocess.check_output(
            [exec_path] + args[1:],
            stderr=subprocess.DEVNULL,
            timeout=QUERY_TIMEOUT_SECONDS,
        )
    except (subprocess.SubprocessError, OSError):
        return None

    return output.decode("utf8")


def _get_compute_capability() -> Optional[str]:
    """Read the compute capability of the first GPU as an "sm_XY" string"""
    output = _query(
        ["nvidia-smi", "--query-gpu=compute_cap", "--format=csv,noheader"]
    )
    if output is None:
        return None

    # drivers too old to know the query field print "[Not Supported]"
    for line in output.splitlines():
        match = COMPUTE_CAP_PATTERN.match(line.strip())
        if match is not None:
            return f"sm_{match.group(1)}{match.group(2)}"

    return None


def _is_supported_by_nvcc(architecture: str) -> bool:
    """Check whether "nvcc" can generate code for the given architecture"""
    output = _query(["nvcc", "--list-gpu-code"])
    if output is None:
        return False

    return architecture in output.split()


@lru_cache(maxsize=1)
def get_gpu_architecture() -> Optional[str]:
    """
    Detect the architecture of the GPU of this machine.

    Returns:
        The architecture in the "sm_XY" format, or None if it could not be
        detected or the CUDA toolkit is too old to generate code for it.
    """
    architecture = _get_compute_capability()
    if architecture is None or not _is_supported_by_nvcc(architecture):
        return None

    return architecture


def get_architecture_args(compiler_args: List[str]) -> List[str]:
    """
    Compute the "nvcc" arguments which make it generate code for the GPU of
    this machine instead of PTX code, which a CUDA driver older than the CUDA
    toolkit fails to compile at runtime.

    Args:
        compiler_args: The "nvcc" arguments provided by the user.

    Returns:
        The architecture arguments, or an empty list if the user already chose
        an architecture or if it could not be detected.
    """
    if any(arg.startswith(ARCH_OPTION_PREFIXES) for arg in compiler_args):
        return []

    architecture = get_gpu_architecture()
    if architecture is None:
        return []

    return ["--gpu-architecture", architecture]
