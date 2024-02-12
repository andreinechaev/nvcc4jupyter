*********
Notebooks
*********

This page provides a list of useful Jupyter notebooks written with the
**nvcc4jupyter** library.

.. note::
   These notebooks are written for Google's Colab, but you may run them in
   other environments by installing all expected dependencies. If running in
   Colab, make sure to set the runtime type to a GPU instance (at the time of
   writing this, T4 is the GPU offered for free by Colab).

------

.. _compiling_with_external_libraries:

Compiling with external libraries
=================================

[`NOTEBOOK <https://colab.research.google.com/drive/1iuY46DCwv4hy3SqDhJgFeO8kgpHnzjTh?usp=sharing>`_]

If you need to compile CUDA C++ code that uses external libraries in the host
code (e.g. OpenCV for reading and writing images to disk) then this section is
for you.

To achieve this, use the :ref:`compiler-args <compiler_args>` option of the
:ref:`cuda <cuda_magic>` magic command to pass the correct compiler options
of the OpenCV library to **nvcc** for it to link the OpenCV code with the
code in your Jupyter cell. Those compiler options can be provided by the
`pkg-config <https://www.freedesktop.org/wiki/Software/pkg-config/>`_ tool.

In the notebook we show how to use OpenCV to load an image, blur it with a CUDA
kernel, and then save it back to disk using OpenCV again.
