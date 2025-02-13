import numpy as np
import matplotlib.pyplot as plt


def plot_bar_chart(*arrays, labels=None, categories=None, cap=0, title="Bar Chart", xlabel="Categories", ylabel="Values", output_file="bar_chart.pdf"):
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
    
    num_arrays = len(arrays)
    num_bars = len(arrays[0])
    
    # Ensure all arrays have the same length
    if not all(len(arr) == num_bars for arr in arrays):
        raise ValueError("All arrays must have the same length")
    
    x = np.arange(num_bars)  # X locations for the bars
    width = 0.8 / num_arrays  # Width of each bar

    if(cap > 0):
        capped_arrays = [np.minimum(arr, cap) for arr in arrays]
    else:
        capped_arrays = arrays
    
    plt.figure(figsize=(10, 6))  # Increased figure size for readability
    fig, ax = plt.subplots()
    
    for i, arr in enumerate(capped_arrays):
        ax.bar(x + i * width, arr, width, label=labels[i] if labels else f"Series {i+1}")
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    if(cap > 0):
        ax.set_title(f"{title} (Values > {cap} Capped)")  # Indicate capping
    else:
        ax.set_title(title)
    ax.set_xticks(x + width * (num_arrays - 1) / 2)
    ax.set_xticklabels(categories if categories else [f"Category {i+1}" for i in range(num_bars)], rotation=45, ha="right")
    ax.set_yscale("log")  # Logarithmic scale
    ax.legend()
    ax.grid(True, which="both", linestyle="--", alpha=0.5)  # Improve grid visibility

    plt.tight_layout()  # Prevents overlapping of labels
    plt.savefig(output_file, format='pdf')  # Save the plot as a PDF
    plt.close()


def leveldb_1():
    master = [1.1, 12.5, 1.8, 2.3, 3.4, 2.9, 0.2, 0.3, 268074, 2, 0.2, 0.3, 332.8, 2]
    llfree = [1.2, 12.8, 1.8, 2.2, 3.5, 3.1, 0.2, 0.4, 285949, 2.2, 0.2, 0.3, 305.4, 1.7]
    fastvirt = [1.2, 12.9, 2.4, 3.3, 8.2, 6.3, 0.3, 0.4, 353891, 4.7, 0.2, 0.4, 399.7, 1.9]
    labels = ["Master", "LLFree", "Superblock"]
    categories = [
          "fillseq",
          "fillsync",
          "fillrandom",
          "overwrite",
          "readrandom",
          "readrandom",
          "readseq",
          "readreverse",
          "compact",
          "readrandom",
          "readseq",
          "readreverse",
          "fill100K",
          "crc32c"
      ]

    plot_bar_chart(master, llfree, fastvirt,
                   labels=labels, 
                   categories=categories,
                   cap=450,
                   title="LevelDB Single Core", 
                   xlabel="Categories", 
                   ylabel="micros/op", 
                   output_file="leveldb1.pdf"
           )
def leveldb_64():
    master = [523.6, 9793.3, 524.8, 555.6, 556.7, 518.5, 323.6, 324.2, 3054729, 504, 283.7, 291, 20164.2, 69.2]
    llfree = [523.2, 267.1, 557.7, 559.8, 521.1, 532, 308.7, 322.6, 5278781, 510.5, 284.3, 292.5, 6641.3, 71]
    fastvirt = [551.5, 24255.6, 587.9, 584.9, 714.1, 698.1, 306.4, 307, 8804787, 721.8, 279.1, 285.9, 36154, 68.3]
    labels = ["Master", "LLFree", "Superblock"]
    categories = [
          "fillseq",
          "fillsync",
          "fillrandom",
          "overwrite",
          "readrandom",
          "readrandom",
          "readseq",
          "readreverse",
          "compact",
          "readrandom",
          "readseq",
          "readreverse",
          "fill100K",
          "crc32c"
      ]

    plot_bar_chart(master, llfree, fastvirt,
                   labels=labels, 
                   categories=categories,
                   cap=40000,
                   title="LevelDB 64 Cores",
                   xlabel="Categories",
                   ylabel="micros/op",
                   output_file="leveldb64.pdf"
           )

def leveldb_64_val2000():
    master = [527.6, 3124.6, 1137.4, 1168.7, 533.8, 413.1, 109.4, 129, 21797034, 407.3, 108.5, 124.5, 46421.3, 69]
    llfree = [550, 1090, 1183.9, 1210.9, 412, 399.6, 63.6, 72.4, 24438143, 404, 83.7, 73, 49832.9, 69.6]
    fastvirt = [1021.6, 2575.4, 2303.6, 2427.5, 2987.8, 1341.7, 252.5, 242.8, 46056587, 818, 253, 246.6, 101003.6, 72.6]
    labels = ["Master", "LLFree", "Superblock"]
    categories = [
          "fillseq",
          "fillsync",
          "fillrandom",
          "overwrite",
          "readrandom",
          "readrandom",
          "readseq",
          "readreverse",
          "compact",
          "readrandom",
          "readseq",
          "readreverse",
          "fill100K",
          "crc32c"
      ]

    plot_bar_chart(master, llfree, fastvirt,
                   labels=labels, 
                   categories=categories,
                   cap=3200,
                   title="LevelDB 64 Cores 2000B Values",
                   xlabel="Categories",
                   ylabel="micros/op",
                   output_file="leveldb64_val2000.pdf"
           )


def leveldb_1_ro():
    master = [10, 0.223, 4]
    llfree = [11, 0.225, 4]
    fastvirt = [11, 0.225, 4]
    labels = ["Master", "LLFree", "Superblock"]
    categories = [ "readseq", "readrandom", "readreverse" ]

    plot_bar_chart(master, llfree, fastvirt,
                   labels=labels, 
                   categories=categories,
                   cap=0,
                   title="LevelDB 1 Core",
                   xlabel="Categories",
                   ylabel="micros/op",
                   output_file="leveldb1_ro.pdf"
           )


def leveldb_64_ro():
    master = [24, 157.2, 22]
    llfree = [28, 161.587, 20]
    fastvirt = [27, 151.441, 22]
    labels = ["Master", "LLFree", "Superblock"]
    categories = [ "readseq", "readrandom", "readreverse" ]

    plot_bar_chart(master, llfree, fastvirt,
                   labels=labels, 
                   categories=categories,
                   cap=0,
                   title="LevelDB 64 Cores",
                   xlabel="Categories",
                   ylabel="micros/op",
                   output_file="leveldb64_ro.pdf"
           )



def fio():
    master = [5000, 5020, 21700, 4971, 17800, 7670, 26400, 13500, 8815, 7543, 26000, 10800]
    llfree = [5000, 4876, 21700, 4900, 17000, 7620, 27200, 11900, 6299, 7485, 27500, 10800]
    fastvirt = [5000, 4923, 22700, 4808, 5882, 7787, 26700, 12200, 5489, 7402, 25200, 11000]
    labels = ["Master", "LLFree", "Superblock"]
    categories = [
        "t=1 s=50M bs=4K ",
        "t=1 s=512M bs=4K ",
        "t=1 s=512M bs=1M ",
        "t=1 s=1G bs=4K ",
        "t=16 s=50M bs=4K ",
        "t=16 s=512M bs=4K ",
        "t=16 s=512M bs=1M ",
        "t=16 s=1G bs=4K ",
        "t=64 s=50M bs=4K ",
        "t=64 s=512M bs=4K ",
        "t=64 s=512M bs=1M ",
        "t=64 s=1G bs=4K ",
      ]

    plot_bar_chart(master, llfree, fastvirt,
                   labels=labels, 
                   categories=categories,
                   title="FIO read benchmark", 
                   xlabel="Params", 
                   ylabel="MB/s", 
                   output_file="fio.pdf"
           )

def myleveldb1():
    master = [ 1.995, 18.700, 5.522, 7.750, 6.998, 2.029, 0.394, 0.694, 166271.000, 1.935, 0.380, 0.656, 48.860, 0.565 ]
    llfree = [ 2.056, 18.630, 5.547, 7.910, 7.378, 2.082, 0.423, 0.729, 185273.000, 1.939, 0.400, 0.655, 49.730, 0.568 ]
    fastvirt = [ 2.791, 19.990, 8.028, 12.028, 11.065, 3.819, 0.862, 1.212, 303730.000, 3.421, 0.771, 1.063, 68.790, 0.567 ]
    labels = ["Master", "LLFree", "Superblock"]
    categories = [
          "fillseq",
          "fillsync",
          "fillrandom",
          "overwrite",
          "readrandom",
          "readrandom",
          "readseq",
          "readreverse",
          "compact",
          "readrandom",
          "readseq",
          "readreverse",
          "fill100K",
          "crc32c"
      ]

    plot_bar_chart(master, llfree, fastvirt,
                   labels=labels, 
                   categories=categories,
                   cap=70,
                   title="LevelDB 1 Core 2000B Values local",
                   xlabel="Categories",
                   ylabel="micros/op",
                   output_file="myleveldb1.pdf"
           )

def myleveldb32():
    master = [ 99.672, 18.982, 293.254, 294.756, 148.213, 110.178, 22.760, 27.413, 5708314.000, 98.706, 22.344, 27.389, 5199.124, 13.360 ]
    llfree = [ 119.723, 79.301, 301.264, 331.922, 111.208, 106.878, 11.684, 16.100, 7022524.000, 98.782, 11.703, 15.554, 5854.882, 12.732 ]
    fastvirt = [ 175.469, 21.008, 515.466, 533.631, 229.225, 125.186, 36.237, 36.690, 11486073.000, 138.776, 32.629, 37.120, 11211.324, 13.858 ]
    labels = ["Master", "LLFree", "Superblock"]
    categories = [
          "fillseq",
          "fillsync",
          "fillrandom",
          "overwrite",
          "readrandom",
          "readrandom",
          "readseq",
          "readreverse",
          "compact",
          "readrandom",
          "readseq",
          "readreverse",
          "fill100K",
          "crc32c"
      ]

    plot_bar_chart(master, llfree, fastvirt,
                   labels=labels, 
                   categories=categories,
                   cap=500,
                   title="LevelDB 32 Cores 2000B Values local",
                   xlabel="Categories",
                   ylabel="micros/op",
                   output_file="myleveldb32.pdf"
           )

leveldb_1()
leveldb_64()
# leveldb_64_val2000()

# leveldb_1_ro()
# leveldb_64_ro()

# myleveldb1()
# myleveldb32()

# fio()
