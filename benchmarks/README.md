## Benchmarking tools for OSv's page frame allocator and NVMe driver 

The combination of python scripts currently supports plotting in 2 different ways:
* Over measurements. This means that one line in the plot is one input file
* Over threads. In case all input files have only one measurement, the measurements of all input files will be merged into one dataset, ordered the way they were specified as arguments.

### Benchmarking memory allocator in currently built kernel
* The following command will produce a `out` directory a file for each benchmark specified in `alloc.conf`
```bash
python3 measure_alloc.py alloc.conf
```
* In case of merging multiple files into one graph, the ordering of files passed to the `plot.py` script will determine the order of measurements in the graph. To keep using wildcards in this scenario. `--format "<python format string>"` may be used to fix the file ordering for your use case.

### Benchmarking NVMe driver in currently built kernel
* The following command will produce a `out` directory a file for each benchmark specified in `nvme.conf`
```bash
python3 measure_nvme.py nvme.conf
```

### Plot an output
* The following will produce a plot containing all specified benchmark outputs
```bash
python4 plot.py <input files (benchmark output files, e.g. ./out/*)>
```
* The `--granularity` parameter may be used to specify a custom granularity, like `--granularity 1-24,32,40,48,56,64`
