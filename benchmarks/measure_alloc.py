import signal
import argparse
import subprocess
import os
import sys

def run_benchmarks(file_path, format_string, use_stdout=False):
    # Create the output directory if not using stdout
    output_dir = "out"
    if not use_stdout:
        os.makedirs(output_dir, exist_ok=True)

    with open(file_path, 'r') as file:
        for line in file:
            # Skip comments and empty lines
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Parse the line
            benchmark, vcpus, threads, memsize, iterations, measurements, granularity = line.split()

            # Use the provided format string or default one
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
           
            # Build the command
            command = (
                f"taskset -c 64-{64 + int(vcpus) - 1} "
                f"../osv/scripts/run.py --novnc "
                f"--vcpus {vcpus} "
                f"--memsize {memsize} "
                f"-e \"{benchmark} -t {threads} -i {iterations} -m {measurements} -g {granularity}\""
            )

            # Print the command to verify
            print(f"Executing: {command}")

            try:
                # Open the process in a new process group
                process = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    preexec_fn=os.setsid  # Start the process in a new session
                )

                filtered_output = []

                # Stream the output line-by-line
                for line in process.stdout:
                    line = line.strip()
                    if any(keyword in line for keyword in ["[backtrace]", "Out of memory", "page fault"]):
                        print(f"[ERROR] Detected error in output: {line}")
                        # Terminate the process group
                        os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                        sys.exit(1)
                    elif line.startswith("OSv") or len(filtered_output) > 0:
                        filtered_output.append(line)

                # Wait for process to terminate
                process.wait()

                # Write or print the output based on the flag
                if use_stdout:
                    if filtered_output:
                        print("\n".join(filtered_output))
                else:
                    if filtered_output:
                        with open(output_file_path, 'w') as out_file:
                            out_file.write("\n".join(filtered_output) + '\n')

            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {command}")
                print(e)
                sys.exit(1)  # Exit with an error code for the error

            except Exception as e:
                # Terminate the process group if an exception occurs
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                print(f"An error occurred: {e}")
                sys.exit(1)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run benchmarks from a file.")
    parser.add_argument("bench_file", help="Path to the bench file.")
    parser.add_argument("--stdout", action="store_true", help="Print output to stdout instead of files.")
    parser.add_argument("--format", type=str, help="Specify a custom format string for output filenames.")

    args = parser.parse_args()

    # Default format string if none provided
    default_format = "{benchmark}_{vcpus:02}_{threads:02}_{memsize}_{iterations}_{measurements}_{granularity}"

    # Run the benchmarks with the custom or default format
    run_benchmarks(args.bench_file, args.format or default_format, args.stdout)

