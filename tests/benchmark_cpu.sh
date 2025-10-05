#!/bin/bash

# Benchmark script for matrix multiplication on GPU
# Usage: ./benchmark.sh

EXECUTABLE="./matrix_cpu"
OUTPUT_FILE="results/benchmark_cpu_results.csv"
RUNS_PER_SIZE=1

# Matrix sizes to test
MATRIX_SIZES=(128 256 512 768 1024 1536 2048)

# Create results directory if it doesn't exist
mkdir -p results

# Check if executable exists
if [ ! -f "$EXECUTABLE" ]; then
    echo "Error: $EXECUTABLE not found!"
    echo "Please compile it first with: gcc matrix_cpu.c -o matrix_cpu -lm"
    exit 1
fi

echo "Running benchmark with matrix sizes: ${MATRIX_SIZES[*]}"
echo "Runs per size: $RUNS_PER_SIZE"
echo "=================================================="

# Create CSV header
echo "matrix_size,runtime_ms,run_number" > "$OUTPUT_FILE"

# Run benchmarks
for N in "${MATRIX_SIZES[@]}"; do
    echo ""
    echo "Testing matrix size: ${N}x${N}"
    
    for run in $(seq 1 $RUNS_PER_SIZE); do
        output=$($EXECUTABLE $N 2>&1)
        
        if [ $? -eq 0 ]; then
            # Extract runtime from output (format: "CPU execution time (N=XXX): Y.YYYY seconds")
            # Parse the seconds value and convert to milliseconds
            seconds=$(echo "$output" | grep -oP '(?<=: )[0-9.]+(?= seconds)')
            if [ -n "$seconds" ]; then
                runtime_ms=$(echo "$seconds * 1000" | bc)
                echo "$N,$runtime_ms,$run" >> "$OUTPUT_FILE"
                echo "  Run $run: $runtime_ms ms"
            else
                echo "  Run $run: ERROR (could not parse output)"
                echo "$N,ERROR,$run" >> "$OUTPUT_FILE"
            fi
        else
            echo "  Run $run: ERROR"
            echo "$N,ERROR,$run" >> "$OUTPUT_FILE"
        fi
    done
done

echo ""
echo "=================================================="
echo "Benchmark complete! Results saved to: $OUTPUT_FILE"
echo "=================================================="

# Print summary statistics using awk
echo ""
echo "Summary Statistics:"
echo "--------------------------------------------------"

for N in "${MATRIX_SIZES[@]}"; do
    stats=$(awk -F',' -v n="$N" '
        $1 == n && $2 != "ERROR" {
            sum += $2; 
            if (min == "" || $2 < min) min = $2; 
            if (max == "" || $2 > max) max = $2;
            count++
        } 
        END {
            if (count > 0) 
                printf "N=%4d: avg=%10.6f ms, min=%10.6f ms, max=%10.6f ms\n", n, sum/count, min, max
        }
    ' "$OUTPUT_FILE")
    
    if [ -n "$stats" ]; then
        echo "$stats"
    fi
done
