# Test and Benchmark Scripts

This directory contains scripts for benchmarking and visualizing the performance of matrix multiplication implementations on CPU and GPU.

## Quick Start

To run all benchmarks and generate all plots in one command:

```bash
./tests/run_all_benchmarks.sh
```

This script will:
1. Run CPU benchmarks (`benchmark_cpu.sh`)
2. Run GPU benchmarks (`benchmark_gpu.sh`)
3. Generate CPU performance plots (`plot_cpu_benchmark.py`)
4. Generate GPU performance plots (`plot_gpu_benchmark.py`)
5. Generate a combined comparison plot (`plot_comparison.py`)

## Individual Scripts

### Benchmarking

- **`benchmark_cpu.sh`** - Runs CPU matrix multiplication benchmarks
  ```bash
  ./tests/benchmark_cpu.sh
  ```
  Outputs: `results/benchmark_cpu_results.csv`

- **`benchmark_gpu.sh`** - Runs GPU matrix multiplication benchmarks
  ```bash
  ./tests/benchmark_gpu.sh
  ```
  Outputs: `results/benchmark_results.csv`

### Visualization

- **`plot_cpu_benchmark.py`** - Generates CPU performance plots
  ```bash
  python3 ./tests/plot_cpu_benchmark.py
  ```
  Outputs: `results/benchmark_cpu_plot.png`

- **`plot_gpu_benchmark.py`** - Generates GPU performance plots
  ```bash
  python3 ./tests/plot_gpu_benchmark.py
  ```
  Outputs: `results/benchmark_plot.png`

- **`plot_comparison.py`** - Generates CPU vs GPU comparison plots
  ```bash
  python3 ./tests/plot_comparison.py
  ```
  Outputs: `results/comparison_plot.png`

## Prerequisites

### For CPU Benchmarks:
- GCC compiler
- Compiled `matrix_cpu` executable

### For GPU Benchmarks:
- NVIDIA GPU with CUDA support
- NVCC compiler (CUDA toolkit)
- Compiled `matrix_gpu` executable

### For Plotting:
- Python 3
- Required packages: `pandas`, `matplotlib`, `numpy`

Install Python dependencies:
```bash
pip install pandas matplotlib numpy
```

## Output Files

All results and plots are saved in the `results/` directory:

- `benchmark_cpu_results.csv` - Raw CPU benchmark data
- `benchmark_results.csv` - Raw GPU benchmark data
- `benchmark_cpu_plot.png` - CPU performance visualization
- `benchmark_plot.png` - GPU performance visualization
- `comparison_plot.png` - Side-by-side CPU vs GPU comparison

## Matrix Sizes Tested

Default matrix sizes (NxN): 128, 256, 512, 768, 1024, 1536, 2048, 3072, 4096

Each size is tested 3 times, and statistics (mean, std, min, max) are computed.

