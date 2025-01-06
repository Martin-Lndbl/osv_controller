import signal
import argparse
import subprocess
import os
import sys

def run_benchmarks(file_path, format_string, use_stdout=False, output_dir = "out"):
    if not use_stdout:
        os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            benchmark, vcpus, threads, memsize, iterations, measurements, granularity = line.split()

            output_file_path = os.path.join(
                output_dir,
                format_string.format(
                    benchmark=benchmark,
                    vcpus=int(vcpus),
                    threads=int(threads),
                    memsize=memsize,
                    iterations=iterations,
                    measurements=measurements,
                    granularity=granularity
                )
            )

            for iteration in range(int(iterations)):
                command = (
                    f"taskset -c 0-{0 + int(vcpus) - 1} "
                    f"../osv/benchmarks/micro/{benchmark} "
                    f"-t {threads} -m {measurements} -g {granularity}"
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

                    for line in process.stdout:
                        line = line.strip()
                        if line.startswith("out"):
                            filtered_output.append(f"iteration {iteration}:\n")
                        elif (iteration == 0):
                            filtered_output.append(line)
                        elif len(filtered_output) > 0:
                            filtered_output.append(line)

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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run benchmarks from a file.")
    parser.add_argument("bench_file", help="Path to the bench file.")
    parser.add_argument("--stdout", action="store_true", help="Print output to stdout instead of files.")
    parser.add_argument("--format", type=str, help="Specify a custom format string for output filenames.")
    parser.add_argument("--out", type=str, help="Specify a output directory.")

    args = parser.parse_args()

    default_format = "native_{benchmark}_{vcpus:02}_{threads:02}_{memsize}_{iterations}_{measurements}_{granularity}"

    run_benchmarks(args.bench_file, args.format or default_format, args.stdout, args.out)

