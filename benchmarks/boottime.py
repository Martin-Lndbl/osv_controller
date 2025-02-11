import signal
import argparse
import subprocess
import os
import sys
import time

def run_benchmarks(file_path, format_string, use_stdout=False):
    output_dir = "out"
    if not use_stdout:
        os.makedirs(output_dir, exist_ok=True)

    t=time.time_ns()

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            benchmark, vcpus, threads, memsize, iterations, measurements, granularity, size = line.split()

            output_file_path = os.path.join(
                output_dir,
                format_string.format(
                    time=t,
                    benchmark=benchmark,
                    vcpus=int(vcpus),
                    threads=int(threads),
                    memsize=memsize,
                    iterations=iterations,
                    measurements=measurements,
                    granularity=granularity,
                    size=int(size)
                )
            )

            for iteration in range(int(iterations)):
                command = (
                    f"taskset -c 32-{32 + int(vcpus) - 1} "
                    f"../osv/scripts/run.py --novnc --nogdb "
                    f"--vcpus {vcpus} "
                    f"--memsize {memsize} "
                    f"-e \"{benchmark} -t {threads} -m {measurements} -g {granularity} -s {size}\""
                )

                print(f"Executing (iteration {iteration + 1}/{iterations}): {command}")

                try:
                    process = subprocess.Popen(
                        command,
                        shell=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=True,
                        preexec_fn=os.setsid
                    )

                    filtered_output = []

                    bootup = ""

                    for line in process.stdout:
                        line = line.strip()
                        if any(keyword in line for keyword in ["[backtrace]", "Out of memory", "page fault"]):
                            print(f"[ERROR] Detected error in output: {line}")
                            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                            sys.exit(1)
                        elif (line.startswith("OSv") and iteration == 0):
                            filtered_output.append(line)
                        elif (line.startswith("Booted")):
                            bootup = line.split(' ')[3]
                        elif line.startswith("out"):
                            filtered_output.append(f"iteration {iteration}:\n\n{bootup}")

                    process.wait()

                    if use_stdout:
                        if filtered_output:
                            print("\n".join(filtered_output))
                    else:
                        if iteration == 0:
                            with open(output_file_path, 'w') as out_file:
                                out_file.write("\n".join(filtered_output) + '\n\n')
                        else:
                            with open(output_file_path, 'a') as out_file:
                                out_file.write("\n".join(filtered_output) + '\n\n')


                except subprocess.CalledProcessError as e:
                    print(f"Error executing command: {command}")
                    print(e)
                    sys.exit(1)
    print(f"file regex: {output_dir}/{t}*")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run benchmarks from a file.")
    parser.add_argument("bench_file", help="Path to the bench file.")
    parser.add_argument("--stdout", action="store_true", help="Print output to stdout instead of files.")
    parser.add_argument("--format", type=str, help="Specify a custom format string for output filenames.")

    args = parser.parse_args()

    default_format = "{time}_{benchmark}_{vcpus:02}_{threads:02}_{memsize}_{iterations}_{measurements}_{granularity}_{size}"

    run_benchmarks(args.bench_file, args.format or default_format, args.stdout)

