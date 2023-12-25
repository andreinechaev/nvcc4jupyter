## NVCC Plugin for Jupyter notebook

### V2 is available

V2 brings support of multiple source and header files.

##### Usage

- Install and load extension
```
!pip install git+https://github.com/andreinechaev/nvcc4jupyter.git
%load_ext nvcc_plugin
```

- Mark a cell to be treated as cuda cell
> `%%cuda --name example.cu --compile false`
>> NOTE: The cell must contain either code or comments to be run successfully. 
>> It accepts 2 arguments. `-n` | `--name`  - which is the name of either CUDA source or Header
>> The name parameter must have extension `.cu` or `.h`
>> Second argument `-c` | `--compile`; default value is `false`. The argument is a flag to specify
>> if the cell will be compiled and run right away or not. It might be usefull if you're playing in
>> the `main` function

- To compile and run all CUDA files you need to run
```
%%cuda_run
# This line just to bypass an exeption and can contain any text
```

- To profile your CUDA kernels using NVIDIA Nsight Compute CLI profiler you need to run
```
%%cu --profile
```
- You can add options to the profiler. Keep in mind that any argument after "--profiler-args" will be considered as a profiler argument. For example, to select which sections to collect metrics for you need to run
```
%%cu --profile --profiler-args --section SpeedOfLight --section MemoryWorkloadAnalysis --section Occupancy
```
