import signal
import argparse
import subprocess
import os
import sys
import time
import re
import statistics
import csv

def run_benchmarks(sf, use_stdout=False):
    t=time.time_ns()
    output_dir = f"out/osv"
    os.makedirs(output_dir, exist_ok=True)
    outfile = os.path.join(output_dir, f"{t}.csv")
    with open(outfile, mode="w", newline="") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["mean", "stddev"])
    for query in range(1, 23):
        command = (
            "taskset -c 0-63 "
            "../osv/scripts/run.py --novnc --nogdb "
            "--vcpus 64 "
            "--memsize 200G "
            f"-e \"/duckdb -f /tpch/{query}.sql {sf}.db\""
        )

        print(f"Executing: {command}")

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
            try:
                stdout, stderr = process.communicate(timeout=120)
            except subprocess.TimeoutExpired:
                print("[ERROR] Subprocess timed out", file=sys.stderr)
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                stdout, stderr = process.communicate()
                print(stdout)
                print(stderr)
                sys.exit(1)

            if stderr:
                print(f"[ERROR] Subprocess stderr: {stderr}", file=sys.stderr)

            if process.returncode != 0:
                print(f"[ERROR] Subprocess failed with exit code {process.returncode}", file=sys.stderr)
                os.killpg(os.getpgid(process.pid), signal.SIGTERM) 
                sys.exit(1)

            if use_stdout:
                print(stdout)
            first = False
            real_times = []
            filtered_output.append(f"query {query}:\n")
            for line in stdout.splitlines():
                match = re.search(r"Run Time \(s\): real ([\d.]+)", line)
                if match and first:
                    real_time = float(match.group(1))
                    real_times.append(real_time)
                elif match:
                    first=True
            print(real_times)

            mean_time = statistics.mean(real_times)
            std_dev_time = statistics.stdev(real_times) if len(real_times) > 1 else 0.0

            print(f"Mean real time: {mean_time:.4f} s")
            print(f"Standard deviation: {std_dev_time:.4f} s")


            with open(outfile, mode="a", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)
                csv_writer.writerow([mean_time, std_dev_time])

        except Exception as e:
            print(f"[ERROR] Exception occurred: {e}", file=sys.stderr)
            sys.exit(1)
    print(f"file regex: {output_dir}/*")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run benchmarks from a file.")
    parser.add_argument("sf", help="Path to the bench file.")
    parser.add_argument("--stdout", action="store_true", help="Print output to stdout instead of files.")

    args = parser.parse_args()

    run_benchmarks(args.sf, args.stdout)

