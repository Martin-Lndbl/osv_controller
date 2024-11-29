## Benchmarking tools for OSv's page frame allocator and NVMe driver 

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
    * Every output contains a line starting with `granularity`
    * Every output contains the x and y label for the plot separated by a `|` in the last line before the values begin
```bash
python4 plot.py <benchmark-output>
```
