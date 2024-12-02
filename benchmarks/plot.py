import matplotlib.pyplot as plt
import argparse
import os
import numpy as np

def parse_granularity(granularity_str):
    """
    Parse granularity string, which can contain ranges and individual numbers.
    Example formats: '1-24', '32,40,48', or '1-24,32,40,48'
    """
    granularity_list = []
    parts = granularity_str.split(',')

    for part in parts:
        if '-' in part:
            start, end = map(int, part.split('-'))
            granularity_list.extend(range(start, end + 1))
        else:
            granularity_list.append(int(part))

    return granularity_list

def plot_benchmark(data, granularity, xlabel, ylabel):
    plt.figure(figsize=(10, 6))

    for file_name, cpu_cycles in data.items():
        # Handle different types of granularity (number or list)
        if isinstance(granularity, list):
            # Use granularity as the measurement values directly
            measurements = granularity
        else:
            # Generate measurements based on the length of cpu_cycles and granularity
            measurements = list(range(1, len(cpu_cycles) * granularity + 1, granularity))

        # Calculate the mean and standard deviation
        cycles = cpu_cycles.mean(axis=1)
        std_devs = np.std(cpu_cycles, axis=1)

        # Plot standard deviation first (in gray, no lines)
        plt.errorbar(
            measurements,
            cycles,
            yerr=std_devs,
            fmt='o',
            color='black',
            alpha=0.3,
            capsize=3,
            # label=f'{os.path.basename(file_name)} (std dev)' if len(data) == 1 else None
        )

        plt.plot(
            measurements,
            cycles,
            'o-',  # 'o' for points and '-' for the line
            color='blue',
            label=os.path.basename(file_name)
        )

    # Label the axes and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(f"Benchmark: {ylabel} per {xlabel}")

    # Add grid and legend for better readability
    plt.grid(True)
    plt.legend()

    # Save and display the plot
    plt.savefig("benchmark_plot.png", format="png")
    plt.show()

def parse_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    xlabel = ""
    ylabel = ""
    granularity = None

    cpu_cycles = None
    measurements = 1
    measurement = 0
    iterations = 1
    iteration = -1

    for i, line in enumerate(lines):
        line = line.strip()
        if line == "":
            continue
        elif line.startswith("measurements"):
            measurements = int(line.split()[1])
        elif line.startswith("granularity"):
            granularity = int(line.split()[1])
        elif line.startswith("iteration 0:"):
            cpu_cycles = [[] for _ in range(measurements)]
            iteration = 0
        elif line.startswith("xlabel"):
            xlabel = " ".join(line.split()[1:])
        elif line.startswith("ylabel"):
            ylabel =  " ".join(line.split()[1:])
        elif line.startswith("iteration "):
            measurement = 0
            iteration += 1
        elif iteration >= 0:
            cpu_cycles[measurement].append(int(line))
            measurement += 1;

    return np.array(cpu_cycles), xlabel, ylabel, granularity

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Plot benchmark data from multiple files.")
    parser.add_argument('file_paths', type=str, nargs='+', help="Paths to the files containing benchmark data.")
    parser.add_argument('-g', '--granularity', type=str, default=None, help="Granularity (single number, list of numbers, or range)")

    # Parse arguments
    args = parser.parse_args()

    # Parse granularity argument: either single number, range, or list of numbers
    if args.granularity:
        try:
            granularity = parse_granularity(args.granularity)
        except ValueError:
            print("Invalid granularity format. Please provide a number, list of numbers, or range (e.g., '1-24,32,40').")
            return
    else:
        granularity = None

    data = {}
    xl, yl, gr, nm = None, None, None, None

    # Read data from files and validate consistency
    for file_path in args.file_paths:
        cpu_cycles, xlabel, ylabel, file_granularity = parse_file(file_path)

        num_measurements = len(cpu_cycles)

        if xl is None:
            xl, yl, gr, nm = xlabel, ylabel, file_granularity, num_measurements
        else:
            if (num_measurements > 1 and (xlabel != xl or ylabel != yl or file_granularity != gr or num_measurements != nm)):
                print(f"Inconsistent data in file: {file_path}")
                print(f"Expected: xlabel='{xl}', ylabel='{yl}', granularity={gr}, number of measurements={nm}")
                print(f"Found: xlabel='{xlabel}', ylabel='{ylabel}', granularity={file_granularity}, number of measurements={num_measurements}")

        data[file_path] = cpu_cycles

    if not data:
        print("No valid data found. Exiting.")
        return

    if all(len(iterations) == 1 for iterations in data.values()):
        merged_iterations = np.array([iterations[0] for iterations in data.values()])
        data = {"Allocations": (merged_iterations)}
        gr = 1

    # Plot the benchmark data with the specified granularity
    plot_benchmark(data, granularity or gr, xl, yl)

if __name__ == "__main__":
    main()

