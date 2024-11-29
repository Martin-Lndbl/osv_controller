import matplotlib.pyplot as plt
import argparse

def plot_benchmark(cycles, xlabel, ylabel, granularity):
    measurements = list(range(1, len(cycles) * granularity + 1, granularity))

    plt.figure(figsize=(10, 6))
    plt.plot(measurements, cycles, marker='o', linestyle='-', color='blue', label='Cycles per Allocation')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"Benchmark: {ylabel} per {xlabel}")
    plt.grid(True)
    plt.legend()

    plt.savefig("benchmark_plot.svg", format="svg")

def read_cycles_from_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    cycles = []
    xlabel, ylabel, granularity = "", "", None

    for i, line in enumerate(lines):
        if "granularity" in line:
            granularity = int(line.split()[1])
        elif line.startswith("threads"):
            labels_line = lines[i + 1].strip()
            if "|" in labels_line:
                xlabel, ylabel = labels_line.split("|")
                cycles = [int(line.strip()) for line in lines[i + 2:] if line.strip().isdigit()]
                break

    return cycles, xlabel, ylabel, granularity

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Plot benchmark data from a file.")
    parser.add_argument('file_path', type=str, help="Path to the file containing benchmark data.")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Read cycles, labels, and granularity from the file
    cycles, xlabel, ylabel, granularity = read_cycles_from_file(args.file_path)
    
    if granularity is None:
        print("Granularity not found in the file. Exiting.")
        return
    
    # Plot the benchmark data
    plot_benchmark(cycles, xlabel, ylabel, granularity)

if __name__ == "__main__":
    main()

