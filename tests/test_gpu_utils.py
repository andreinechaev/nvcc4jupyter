import os
from typing import Callable, List

import pytest

from nvcc4jupyter.gpu_utils import get_architecture_args, get_gpu_architecture


@pytest.fixture(autouse=True)
def clear_architecture_cache():
    get_gpu_architecture.cache_clear()
    yield
    get_gpu_architecture.cache_clear()


@pytest.fixture
def mock_gpu(monkeypatch: pytest.MonkeyPatch, gpu_mocks_path: str):
    def setup(compute_cap: str, gpu_codes: str = "sm_75 sm_80 sm_90") -> None:
        monkeypatch.setenv(
            "PATH", gpu_mocks_path + os.pathsep + os.environ["PATH"]
        )
        monkeypatch.setenv("MOCK_COMPUTE_CAP", compute_cap)
        monkeypatch.setenv("MOCK_GPU_CODES", gpu_codes)

    return setup


def test_detect_architecture(mock_gpu: Callable[..., None]):
    mock_gpu("7.5")
    assert get_gpu_architecture() == "sm_75"
    assert get_architecture_args([]) == ["--gpu-architecture", "sm_75"]
    assert get_architecture_args(["--optimize", "3"]) == [
        "--gpu-architecture",
        "sm_75",
    ]


def test_architecture_newer_than_toolkit(mock_gpu: Callable[..., None]):
    mock_gpu("12.0", gpu_codes="sm_75 sm_80")
    assert get_gpu_architecture() is None
    assert get_architecture_args([]) == []


def test_compute_capability_not_reported(mock_gpu: Callable[..., None]):
    mock_gpu("")
    assert get_gpu_architecture() is None
    assert get_architecture_args([]) == []


def test_no_gpu(monkeypatch: pytest.MonkeyPatch, tmp_path):
    monkeypatch.setenv("PATH", str(tmp_path))
    assert get_gpu_architecture() is None
    assert get_architecture_args([]) == []


@pytest.mark.parametrize(
    "compiler_args",
    [
        ["-arch=sm_60"],
        ["-arch", "sm_60"],
        ["--gpu-architecture=sm_60"],
        ["--gpu-architecture", "sm_60"],
        ["-gencode", "arch=compute_60,code=sm_60"],
        ["--generate-code", "arch=compute_60,code=sm_60"],
        ["--optimize", "3", "-code=sm_60"],
    ],
)
def test_explicit_architecture_is_kept(
    mock_gpu: Callable[..., None], compiler_args: List[str]
):
    mock_gpu("7.5")
    assert get_architecture_args(compiler_args) == []
