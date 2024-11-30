## Benchmarking tools for OSv's page frame allocator and NVMe driver 

The combination of python scripts currently supports plotting in 2 different ways:
* Over measurements. This means that one line in the plot is one input file
* Over threads. In case all input files have only one measurement, the measurements of all input files will be merged into one dataset, ordered the way they were specified as arguments.

### Benchmarking memory allocator in currently built kernel
* The following command will produce a `out` directory a file for each benchmark specified in `alloc.conf`
```bash
python3 measure_alloc.py alloc.conf
```

### Benchmarking NVMe driver in currently built kernel
* The following command will produce a `out` directory a file for each benchmark specified in `nvme.conf`
```bash
python3 measure_nvme.py nvme.conf
```

### Plot an output
* The following will produce a plot containing all specified benchmark outputs, if
    * Every input file contains a line starting with `granularity`
    * Every input file contains the x and y label for the plot separated by a `|` in the last line before the values begin
    * Every input file only has one measurement, or
        * The granularities of all files match
        * The x and y label of all files match
        * The amount of measurements of all files match
```bash
python4 plot.py <input files (benchmark output files, e.g. ./out/*)>
```
