#!/bin/bash

# Comprehensive benchmark script that runs CPU and GPU benchmarks and plots results
# Usage: ./run_all_benchmarks.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Change to the project root directory (parent of tests)
cd "$(dirname "$0")/.."

echo -e "${BLUE}=================================================="
echo "  Matrix Multiplication Benchmark Suite"
echo "  Running CPU and GPU benchmarks"
echo -e "==================================================${NC}"
echo ""

# Create results directory if it doesn't exist
mkdir -p results

# Step 1: Run CPU Benchmark
echo -e "${YELLOW}[1/4] Running CPU Benchmark...${NC}"
echo "=================================================="
if [ -f "./tests/benchmark_cpu.sh" ]; then
    bash ./tests/benchmark_cpu.sh
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ CPU Benchmark completed successfully${NC}"
    else
        echo -e "${RED}✗ CPU Benchmark failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: benchmark_cpu.sh not found!${NC}"
    exit 1
fi
echo ""

# Step 2: Run GPU Benchmark
echo -e "${YELLOW}[2/4] Running GPU Benchmark...${NC}"
echo "=================================================="
if [ -f "./tests/benchmark_gpu.sh" ]; then
    bash ./tests/benchmark_gpu.sh
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ GPU Benchmark completed successfully${NC}"
    else
        echo -e "${RED}✗ GPU Benchmark failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: benchmark_gpu.sh not found!${NC}"
    exit 1
fi
echo ""

# Step 3: Plot CPU Results
echo -e "${YELLOW}[3/4] Generating CPU Benchmark Plots...${NC}"
echo "=================================================="
if [ -f "./tests/plot_cpu_benchmark.py" ]; then
    python3 ./tests/plot_cpu_benchmark.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ CPU plots generated successfully${NC}"
    else
        echo -e "${RED}✗ CPU plot generation failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: plot_cpu_benchmark.py not found!${NC}"
    exit 1
fi
echo ""

# Step 4: Plot GPU Results
echo -e "${YELLOW}[4/4] Generating GPU Benchmark Plots...${NC}"
echo "=================================================="
if [ -f "./tests/plot_gpu_benchmark.py" ]; then
    python3 ./tests/plot_gpu_benchmark.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ GPU plots generated successfully${NC}"
    else
        echo -e "${RED}✗ GPU plot generation failed${NC}"
        exit 1
    fi
else
    echo -e "${RED}Error: plot_gpu_benchmark.py not found!${NC}"
    exit 1
fi
echo ""

# Step 5: Generate Combined Comparison Plot
echo -e "${YELLOW}[BONUS] Generating Combined CPU vs GPU Comparison Plot...${NC}"
echo "=================================================="
if [ -f "./tests/plot_comparison.py" ]; then
    python3 ./tests/plot_comparison.py
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Comparison plot generated successfully${NC}"
    else
        echo -e "${YELLOW}⚠ Comparison plot generation failed (non-critical)${NC}"
    fi
else
    echo -e "${YELLOW}Note: plot_comparison.py not found (optional)${NC}"
fi
echo ""

# Summary
echo -e "${BLUE}=================================================="
echo "  Benchmark Suite Complete!"
echo -e "==================================================${NC}"
echo ""
echo "Results saved in the 'results/' directory:"
echo "  - results/benchmark_cpu_results.csv"
echo "  - results/benchmark_results.csv (GPU)"
echo "  - results/benchmark_cpu_plot.png"
echo "  - results/benchmark_plot.png (GPU)"
if [ -f "results/comparison_plot.png" ]; then
    echo "  - results/comparison_plot.png (CPU vs GPU)"
fi
echo ""
echo -e "${GREEN}All benchmarks completed successfully!${NC}"

