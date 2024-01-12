# nvcc4jupyter: CUDA C++ plugin for Jupyter Notebook

| | |
| --- | --- |
| Testing | ![Python Versions][python-version] [![CI - Test][test-badge]][test-workflow] [![Coverage][coverage-badge]][coverage-results] |
| Package | [![PyPI Latest Release][pypi-latest-version]][pypi-project-url] [![PyPI Downloads][pypi-downloads]][pypi-project-url] |

[python-version]: https://img.shields.io/pypi/pyversions/nvcc4jupyter
[test-badge]: https://github.com/cosminc98/nvcc4jupyter/actions/workflows/test.yml/badge.svg
[test-workflow]: https://github.com/cosminc98/nvcc4jupyter/actions/workflows/test.yml
[coverage-badge]: https://codecov.io/github/cosminc98/nvcc4jupyter/coverage.svg?branch=master
[coverage-results]: https://codecov.io/gh/cosminc98/nvcc4jupyter
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

## Main Features
Here are just a few of the things that nvcc4jupyter does well:

  - [Easily run CUDA C++ code](https://nvcc4jupyter.readthedocs.io/en/latest/usage.html#hello-world)
  - [Profile your code with NVIDIA Nsight Compute](https://nvcc4jupyter.readthedocs.io/en/latest/usage.html#profiling)
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

<hr>

[Go to Top](#table-of-contents)
