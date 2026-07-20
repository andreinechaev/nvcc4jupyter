"""
Setup steps for platforms such as Kaggle, Colab, etc. to allow our extension
to work on them immediately after loading it.
"""

# pylint: disable=missing-function-docstring

import os
import traceback
from subprocess import DEVNULL, STDOUT, check_call
from typing import Optional

PATH_PRIORITY_DIR = "/usr/bin/priority"
KAGGLE_GCC_8_PATH = "/usr/bin/gcc-8"


def print_platform(platform: str) -> None:
    print(f'Detected platform "{platform}". Running its setup...')


def kaggle_setup() -> None:
    print("Updating the package lists...")
    check_call(["/usr/bin/apt-get", "update"], stdout=DEVNULL, stderr=STDOUT)

    print("Installing nvidia-cuda-toolkit, this may take a few minutes...")
    check_call(
        ["/usr/bin/apt-get", "install", "-y", "nvidia-cuda-toolkit"],
        stdout=DEVNULL,
        stderr=STDOUT,
    )
    os.makedirs(PATH_PRIORITY_DIR, exist_ok=True)

    gcc_symlink_path = os.path.join(PATH_PRIORITY_DIR, "gcc")
    if not os.path.exists(gcc_symlink_path):
        os.symlink(KAGGLE_GCC_8_PATH, gcc_symlink_path)

    if PATH_PRIORITY_DIR not in os.environ["PATH"].split(":"):
        os.environ["PATH"] = f"{PATH_PRIORITY_DIR}:" + os.environ["PATH"]


def colab_setup() -> None:
    pass


def setup_environment() -> None:
    """
    Detect the platform the extension was loaded on and run the necessary
    steps (install dependencies, add executables to PATH, etc.) for the
    extension to work.
    """

    if "NVCC4JUPYTER_NO_SETUP" in os.environ:
        return

    platform: Optional[str] = None
    try:
        if "KAGGLE_URL_BASE" in os.environ:
            platform = "Kaggle"
            print_platform(platform)
            kaggle_setup()
        elif "COLAB_RELEASE_TAG" in os.environ:
            platform = "Colab"
            print_platform(platform)
            colab_setup()
    except Exception:  # pylint: disable=broad-exception-caught
        print(
            f'Setup failed for detected platform "{platform}". Set the'
            ' "NVCC4JUPYTER_NO_SETUP" environment variable to disable running'
            " the setup on load. Please report the following error to"
            " https://github.com/andreinechaev/nvcc4jupyter/issues:"
            f" following error message:\n{traceback.format_exc()}"
        )
