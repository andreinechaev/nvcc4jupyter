from setuptools import setup

setup(
    name='nvcc4jupyter',
    version='0.1',
    description='Jupyter notebook plugin to run CUDA C/C++ code',
    url='https://github.com/fuckthegoose/nvcc4jupyter',
    author='Ivan Sushkov',
    license='MIT',
    packages=['nvcc_plugin'],
    zip_safe=True
)
