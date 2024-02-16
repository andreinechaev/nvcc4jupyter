# nvcc4jupyter: CUDA C++ plugin for Jupyter Notebook

| | |
| --- | --- |
| Testing | ![Python Versions][python-version] [![CI - Test][test-badge]][test-workflow] [![Coverage][coverage-badge]][coverage-results] |
| Code Quality | [![Code style: black][black-badge]][black-project] [![security: bandit][bandit-badge]][bandit-project]|
| Package | [![PyPI Latest Release][pypi-latest-version]][pypi-project-url] [![PyPI Downloads][pypi-downloads]][pypi-project-url] |

<!-- Testing badges -->
[python-version]: https://img.shields.io/pypi/pyversions/nvcc4jupyter
[test-badge]: https://github.com/andreinechaev/nvcc4jupyter/actions/workflows/test.yml/badge.svg
[test-workflow]: https://github.com/andreinechaev/nvcc4jupyter/actions/workflows/test.yml
[coverage-badge]: https://codecov.io/github/andreinechaev/nvcc4jupyter/coverage.svg?branch=master
[coverage-results]: https://codecov.io/gh/andreinechaev/nvcc4jupyter

<!-- Code Quality badges -->
[black-badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black-project]: https://github.com/ambv/black
[bandit-badge]: https://img.shields.io/badge/security-bandit-yellow.svg
[bandit-project]: https://github.com/PyCQA/bandit

<!-- Package badges -->
[pypi-project-url]: https://pypi.org/project/nvcc4jupyter/
[pypi-latest-version]: https://img.shields.io/pypi/v/nvcc4jupyter.svg
[pypi-downloads]: https://img.shields.io/pypi/dm/nvcc4jupyter.svg?label=PyPI%20downloads

**nvcc4jupyter** is a Jupyter Notebook plugin that provides cell and line
[magics](https://ipython.readthedocs.io/en/stable/interactive/magics.html)
to allow running CUDA C++ code from a notebook. This is especially
useful when combined with a hosted service such a Google's
[Colab](https://colab.research.google.com/) which provide CUDA capable GPUs
and you can start learning CUDA C++ without having to install anything or even
to own a GPU yourself.

## Table of Contents

- [Main Features](#main-features)
- [Install](#install)
- [Usage](#usage)
- [License](#license)
- [Documentation](#documentation)
- [Contributing](#contributing)

## Main Features
Here are just a few of the things that nvcc4jupyter does well:

  - [Easily run CUDA C++ code](https://nvcc4jupyter.readthedocs.io/en/latest/usage.html#hello-world)
  - [Profile your code with NVIDIA Nsight Compute or Nsight Systems](https://nvcc4jupyter.readthedocs.io/en/latest/usage.html#profiling)
  - [Compile your code with external libraries (e.g. OpenCV)](https://nvcc4jupyter.readthedocs.io/en/latest/notebooks.html#compiling-with-external-libraries)
  - [Share code between different programs in the same notebook / split your code into multiple files for improved readability](https://nvcc4jupyter.readthedocs.io/en/latest/usage.html#groups)

## Install
The installer for the latest released version is available at the [Python
Package Index (PyPI)](https://pypi.org/project/nvcc4jupyter).

```sh
pip install nvcc4jupyter
```

## Usage

First, load the extension to enable the magic commands:
```
%load_ext nvcc4jupyter
```

Running a quick CUDA Hello World program:
```c++
%%cuda
#include <stdio.h>

__global__ void hello(){
    printf("Hello from block: %u, thread: %u\n", blockIdx.x, threadIdx.x);
}

int main(){
    hello<<<2, 2>>>();
    cudaDeviceSynchronize();
}
```

For more advanced use cases, see [the documentation](https://nvcc4jupyter.readthedocs.io/en/latest/usage.html).

## Documentation
The official documentation is hosted on [readthedocs](https://nvcc4jupyter.readthedocs.io/).

## License
[MIT](LICENSE)

## Contributing

The recommended setup for development is using the devcontainer in GitHub
Codespaces or locally in VSCode.

If not using the devcontainer you need to install the package with the
development dependencies and install the pre-commit hook before commiting any
changes:
```bash
pip install -e .[dev]
pre-commit install
```

<hr>

[Go to Top](#table-of-contents)
