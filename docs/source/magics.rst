**********
Magics API
**********

.. note::
   Arguments for profilers and the nvcc compiler can be passed in double
   quotes so they can contain spaces and dashes.

------

.. _cuda_magic:

cuda
====

Magic command that compiles, runs, and profiles CUDA C++ code in the cell.

Usage
-----

   - ``%%cuda``: Compile and run this cell.
   - ``%%cuda -p``: Also runs the Nsight Compute profiler.
   - ``%%cuda -p -a "<SPACE SEPARATED PROFILER ARGS>"``: Also runs the Nsight Compute profiler.
   - ``%%cuda -c "<SPACE SEPARATED COMPILER ARGS"``: Passes additional arguments to "nvcc".
   - ``%%cuda -t``: Outputs the "timeit" built-in magic results.

Options
-------

.. _timeit:

-t, --timeit
   Boolean. If set, returns the output of the "timeit" built-in
   ipython magic instead of stdout.

.. _profile:

-p, --profile
   Boolean. If set, runs the NVIDIA Nsight Compute (or NVIDIA Nsight Systems
   if changed via the \-\-profiler option) profiler whose output is appended to
   standard output.

.. _profiler:

-l, --profiler
   String. Can either be "ncu" (the default) to use NVIDIA Nsight Compute
   profiling tool, or "nsys" to use NVIDIA Nsight Systems profiling tool.

.. _profiler_args:

.. _profiler_args:

-a, --profiler-args
   String. Optional profiler arguments that can be space separated
   by wrapping them in double quotes. Will be passed to the profiler selected
   by the \-\-profiler option.. See profiler options here:
   `Nsight Compute <https://docs.nvidia.com/nsight-compute/NsightComputeCli/index.html#command-line-options>`_
   or `Nsight Systems <https://docs.nvidia.com/nsight-systems/UserGuide/index.html#command-line-options>`_.

.. _compiler_args:

-c, --compiler-args
   String. Optional compiler arguments that can be space separated
   by wrapping them in double quotes. They will be passed to "nvcc".
   See all options here:
   `NVCC Options <https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#nvcc-command-options>`_


.. _compiler_args:

-c, --compiler-args
   String. Optional compiler arguments that can be space separated
   by wrapping them in double quotes. They will be passed to "nvcc".
   See all options here:
   `NVCC Options <https://docs.nvidia.com/cuda/cuda-compiler-driver-nvcc/index.html#nvcc-command-options>`_


.. note::
   If both "\-\-profile" and "\-\-timeit" are used then no profiling is
   done.

Examples
--------
::

   # compile, run, and profile the code in the cell with the Nsight compute
   # profiler while collecting only metrics from the "MemoryWorkloadAnalysis"
   # section; also provides the "--optimize 3" option to "nvcc" during
   # compilation to optimize host code
   %%cuda -p -a "--section MemoryWorkloadAnalysis" -c "--optimize 3"

------

.. _cuda_group_save_magic:

cuda_group_save
===============

Magic command that saves CUDA C++ code in the cell for later
compilation and execution with possibly more source files.

Usage
-----

   - ``%%cuda_group_save -n <FILENAME> -g <GROUPNAME>``: Save the code in the current cell to a group of source files.

Options
-------

-n, --name
   String. Required file name of the saved source file. Must have
   either the ".cu" or ".h" extension. In order to import a header
   file saved with this magic you can simply add '#include "<name>"'.

-g, --group
   String. Required group name to which to add the saved source file.
   Groups are source files that get compiled together and do not
   interact with other groups. This allows you to have multiple
   unrelated CUDA programs within the same jupyter notebook. Adding
   files to a group named "shared" will make them available to all
   other source file groups. One use case for the shared group is for
   sharing error handling code which should be present in all CUDA
   programs.

Examples
--------
::

   # jupyter cell 1
   %%cuda_group_save -n "error_handling.h" -g "shared"
   <ERROR HANDLING CODE>

   # jupyter cell 2
   %%cuda_group_save -n "main.cu" -g "example_group"
   #include "error_handling.h"
   <YOUR CODE HERE>

------

.. _cuda_group_run_magic:

cuda_group_run
==============

Line magic command that compiles, runs, and profiles all source files
in a group.

Usage
-----

   - ``%%cuda_group_run -g <GROUPNAME>``: Compiles, runs, and profiles the sources files in the given group.

Options
-------

-g, --group
   String. Required group name whose source files should be deleted.

.. note::
   All options from the "%%cuda" cell magic are inherited.

Examples
--------
::

   # jupyter cell 1
   %%cuda_group_save -n "error_handling.h" -g "shared"
   <ERROR HANDLING CODE>

   # jupyter cell 2
   %%cuda_group_save -n "main.cu" -g "example_group"
   #include "error_handling.h"
   <YOUR CODE HERE>

   # jupyter cell 3
   %cuda_group_run -g "example_group" --profile

-----

.. _cuda_group_delete_magic:

cuda_group_delete
=================

Line magic command that deletes all source files in a group.

Usage
-----

   - ``%%cuda_group_delete -g <GROUPNAME>``: Removes all source files in the given group.

Options
-------

-g, --group
   String. Required group name whose source files should be deleted.

Examples
--------
::

   # jupyter cell 1
   %%cuda_group_save -n "error_handling.h" -g "shared"
   <ERROR HANDLING CODE>

   # jupyter cell 2 - here we delete the error shared group; in
   # practice this would be helpful if you want to overwrite some
   # functionality that was defined earlier in the notebook
   %cuda_group_delete -g "shared"
