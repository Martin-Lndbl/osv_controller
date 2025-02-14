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

def plot_benchmark(data, granularity, title, xlabel, ylabel, stddev, log):
    # Configure font sizes for better readability
    plt.rcParams.update({
        'font.family': 'serif',          # Use serif font
        'font.serif': ['Times New Roman', 'Georgia', 'DejaVu Serif'],  # Palatino alternatives
        'font.size': 12,                 # General font size
        'axes.titlesize': 14,            # Title font size
        'axes.labelsize': 12,            # Axis label font size
        'xtick.labelsize': 10,           # X-axis tick font size
        'ytick.labelsize': 10,           # Y-axis tick font size
        'legend.fontsize': 10,           # Legend font size
    })

    # Create a plot with half a DIN A4 page width (4.13 inches) and height 3 inches
    plt.figure(figsize=(4.13, 3))
    # plt.figure(figsize=(12, 6))

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

        if(stddev):
            # Plot standard deviation first (in gray, no lines)
            plt.errorbar(
                measurements,
                cycles,
                yerr=std_devs,
                fmt='none',
                color='black',
                alpha=0.3,
                capsize=3,
            )

        plt.plot(
            measurements,
            cycles,
            ('o-' if stddev else '-'),  # 'o' for points and '-' for the line
            label=os.path.basename(file_name)
        )

    # Label the axes and add a legend
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)
    plt.grid(True)
    plt.legend()

    if(log):
        plt.yscale('log')

    # Adjust layout to ensure labels are not cut off
    plt.tight_layout()

    # Save and display the plot
    plt.savefig("benchmark_plot.pdf", format="pdf", dpi=300)  # High DPI for quality
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
            cpu_cycles[measurement].append(float(line))
            measurement += 1;

    return np.array(cpu_cycles), xlabel, ylabel, granularity

boot = {
'master': np.array([[192.25, 190.  , 188.29, 188.12, 187.64, 191.48, 187.91, 184.97,
        193.04, 190.32, 191.43, 187.94, 192.33, 190.43, 193.64, 188.46,
        195.17, 193.73, 189.34, 190.08],
        [201.45, 201.99, 201.07, 201.06, 204.48, 205.12, 204.58, 204.86,
        200.63, 201.98, 202.42, 202.01, 202.8 , 203.41, 200.98, 201.75,
        202.63, 202.48, 203.74, 204.24],
        [222.82, 222.72, 219.08, 220.21, 221.52, 220.3 , 219.37, 224.9 ,
        218.78, 223.77, 220.53, 225.28, 223.94, 221.3 , 222.73, 224.18,
        221.98, 222.14, 223.83, 219.49],
        [240.13, 237.35, 241.28, 241.15, 243.44, 241.62, 240.8 , 241.02,
        285.6 , 240.12, 239.15, 239.4 , 241.23, 241.56, 244.13, 239.72,
        239.99, 242.25, 238.51, 241.7 ],
        [256.98, 258.74, 258.64, 261.99, 261.09, 260.27, 257.67, 258.43,
        261.43, 259.19, 259.26, 259.36, 258.67, 257.97, 257.21, 254.64,
        258.64, 260.37, 260.27, 258.58]]),
'llfree': np.array([[191.31, 190.54, 191.08, 190.86, 189.83, 191.6 , 191.88, 190.18,
        192.25, 188.22, 189.04, 191.36, 191.07, 193.56, 190.9 , 190.99,
        192.64, 194.46, 195.66, 190.95],
       [204.34, 203.09, 200.98, 205.7 , 205.13, 201.85, 200.92, 201.22,
        201.09, 206.  , 202.02, 202.55, 201.56, 205.62, 201.74, 202.86,
        202.65, 203.25, 201.  , 198.78],
       [216.58, 217.45, 218.5 , 217.76, 218.42, 220.21, 220.29, 219.88,
        219.85, 219.95, 217.08, 217.43, 220.61, 220.4 , 219.47, 218.92,
        219.14, 219.2 , 219.37, 220.1 ],
       [234.63, 233.39, 235.35, 234.1 , 236.99, 236.21, 235.  , 235.71,
        236.44, 237.52, 235.51, 234.1 , 237.52, 236.12, 235.36, 236.69,
        237.5 , 235.21, 234.15, 236.05],
       [250.76, 250.57, 250.73, 251.98, 251.08, 250.2 , 248.9 , 251.23,
        254.96, 248.58, 249.9 , 250.09, 251.4 , 251.15, 247.29, 250.06,
        250.64, 250.81, 250.36, 252.59]]),
'fastvirt': np.array([[187.64, 190.15, 189.42, 190.86, 191.36, 190.29, 192.79, 186.07,
        190.07, 188.21, 189.97, 190.37, 187.42, 189.84, 188.48, 187.27,
        187.75, 188.04, 184.19, 189.05],
       [206.5 , 204.02, 201.94, 202.91, 204.23, 203.77, 211.01, 207.25,
        206.04, 202.32, 201.83, 203.56, 201.04, 209.25, 207.92, 204.74,
        202.36, 208.05, 209.2 , 209.11],
       [227.4 , 227.83, 231.2 , 229.04, 226.33, 220.65, 227.95, 230.28,
        229.74, 228.52, 228.37, 226.7 , 228.8 , 225.38, 226.75, 228.09,
        228.09, 231.52, 228.57, 227.86],
       [248.44, 245.54, 246.85, 247.52, 247.29, 249.5 , 245.5 , 246.16,
        246.07, 246.11, 244.87, 245.8 , 243.37, 245.18, 248.91, 247.49,
        245.13, 247.3 , 243.91, 248.66],
       [263.37, 259.8 , 262.47, 259.31, 261.22, 263.98, 264.29, 259.39,
        258.44, 261.44, 261.41, 262.08, 257.21, 258.55, 258.92, 261.2 ,
        266.07, 260.66, 260.58, 260.59]])
}

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Plot benchmark data from multiple files.")
    parser.add_argument('file_paths', type=str, nargs='+', help="Paths to the files containing benchmark data.")
    parser.add_argument('-g', '--granularity', type=str, default=None, help="Granularity (single number, list of numbers, or range)")
    parser.add_argument('-x', '--xlabel', type=str, default=None, help="Override for X-axis label")
    parser.add_argument('-y', '--ylabel', type=str, default=None, help="Override for Y-axis label")
    parser.add_argument('-l', '--label', type=str, default="Page Allocation", help="Custom label for the plot")
    parser.add_argument('-t', '--title', type=str, default=None, help="Custom title for the plot")
    parser.add_argument('-s', '--stddev', action='store_true', help="Show standard deviation on the plot")
    parser.add_argument('-e', '--log', action='store_true', help="Show y axis with logarithmic scale")


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
            if (args.xlabel):
                xl = args.xlabel
            if (args.ylabel):
                yl = args.ylabel
        else:
            if (num_measurements > 1 and (xlabel != xl or ylabel != yl or file_granularity != gr or num_measurements != nm)):
                print(f"Inconsistent data in file: {file_path}")
                print(f"Expected: xlabel='{xl}', ylabel='{yl}', granularity={gr}, number of measurements={nm}")
                print(f"Found: xlabel='{xlabel}', ylabel='{ylabel}', granularity={file_granularity}, number of measurements={num_measurements}")

        if(len(args.file_paths) == 1):
            data[args.label] = cpu_cycles
        else:
            data[file_path] = cpu_cycles

    if not data:
        print("No valid data found. Exiting.")
        return

    if all(len(iterations) == 1 for iterations in data.values()):
        merged_iterations = np.array([iterations[0] for iterations in data.values()])
        data = {args.label: (merged_iterations)}
        gr = 1

    # Plot the benchmark data with the specified granularity
    plot_benchmark(data, granularity or gr, args.title, xl, yl, args.stddev, args.log)
    # plot_benchmark(boot, [1,16,32,48,64], "Boot Time", "Cores", "Time (ms)", args.stddev, args.log)


if __name__ == "__main__":
    main()

