import argparse
import subprocess

def run_benchmarks(file_path, output_file=None):
    # Clear the output file if it is specified
    if output_file:
        with open(output_file, 'w') as out_file:
            pass  # Just open and close to empty the file

    with open(file_path, 'r') as file:
        for line in file:
            # Skip comments and empty lines
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Parse the line
            benchmark, vcpus, threads, memsize, iterations, measurements, granularity= line.split()
        
            # Build the command
            command = (
                f"taskset -c 64-{64+int(vcpus)-1} "
                f"./osv/scripts/run.py --novnc "
                f"--vcpus {vcpus} "
                f"--memsize {memsize} "
                f"-e \"{benchmark} -t {threads} -i {iterations} -m {measurements} -g {granularity}\""
            )

            # Print the command to verify
            print(f"Executing: {command}")

            # Execute the command
            try:
                result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Capture all output lines
                output_lines = result.stdout.splitlines()

                # Find the first line starting with "OSv"
                start_recording = False
                filtered_output = []

                for line in output_lines:
                    if start_recording:
                        filtered_output.append(line)
                    elif line.startswith("OSv"):
                        start_recording = True
                        filtered_output.append(line)

                # If output file is specified, append filtered output to the file
                if output_file and filtered_output:
                    with open(output_file, 'a') as out_file:
                        for filtered_line in filtered_output:
                            out_file.write(filtered_line + '\n')
                        out_file.write('\n')

                # Optionally print the filtered output to console
                if not output_file and filtered_output:
                    print("\n".join(filtered_output))

            except subprocess.CalledProcessError as e:
                print(f"Error executing command: {command}")
                print(e)

if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(description="Run benchmarks from a file.")
    parser.add_argument("bench_file", help="Path to the bench file.")
    parser.add_argument("-o", "--output", help="File to write filtered outputs (after 'OSv').", default=None)

    args = parser.parse_args()

    # Run the benchmarks
    run_benchmarks(args.bench_file, args.output)

