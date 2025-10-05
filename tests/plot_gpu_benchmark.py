#!/usr/bin/env python3
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

def plot_benchmark_results(csv_file="results/benchmark_results.csv", output_file="results/benchmark_plot.png"):
    """
    Plot benchmark results from CSV file.
    
    Args:
        csv_file: Input CSV file with benchmark results
        output_file: Output image file for the plot
    """
    
    if not os.path.exists(csv_file):
        print(f"Error: Results file '{csv_file}' not found.")
        print("Please run the benchmark first with: ./benchmark.py or ./benchmark.sh")
        sys.exit(1)
    
    # Read the CSV file
    df = pd.read_csv(csv_file)
    
    # Check if there's any data
    if len(df) == 0:
        print(f"Error: No data found in '{csv_file}'")
        print("Please run the benchmark first with: ./benchmark.py or ./benchmark.sh")
        sys.exit(1)
    
    # Filter out error rows
    df = df[df['runtime_ms'] != 'ERROR']
    df['runtime_ms'] = pd.to_numeric(df['runtime_ms'])
    
    # Check again after filtering
    if len(df) == 0:
        print(f"Error: No valid data found in '{csv_file}' after filtering")
        print("All benchmark runs resulted in errors.")
        sys.exit(1)
    
    # Calculate statistics per matrix size
    stats = df.groupby('matrix_size')['runtime_ms'].agg(['mean', 'std', 'min', 'max']).reset_index()
    
    if len(stats) == 0:
        print(f"Error: Could not compute statistics from '{csv_file}'")
        sys.exit(1)
    
    # Create the plot
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    
    # Plot: Runtime vs Matrix Size (with error bars)
    ax.errorbar(stats['matrix_size'], stats['mean'], yerr=stats['std'], 
                 fmt='o-', capsize=5, capthick=2, linewidth=2, markersize=8)
    ax.set_xlabel('Matrix Size (N)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Runtime (ms)', fontsize=12, fontweight='bold')
    ax.set_title('GPU Matrix Multiplication Performance', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log', base=2)
    
    # Set x-axis ticks to show actual matrix sizes
    ax.set_xticks(stats['matrix_size'])
    ax.set_xticklabels([str(int(x)) for x in stats['matrix_size']], rotation=45)
    
    # Add data labels
    for _, row in stats.iterrows():
        ax.annotate(f"{row['mean']:.2f}", 
                    xy=(row['matrix_size'], row['mean']),
                    xytext=(0, 10), textcoords='offset points',
                    ha='center', fontsize=8)
    
    # Calculate GFLOPS for performance summary (not plotted)
    # For matrix multiplication: 2*N^3 operations
    stats['gflops'] = (2 * stats['matrix_size']**3) / (stats['mean'] * 1e6)  # Convert ms to seconds and ops to GFLOPS
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Plot saved to: {output_file}")
    
    # Print performance summary
    print("\nPerformance Summary:")
    print("=" * 70)
    print(f"{'Matrix Size':<15} {'Avg Time (ms)':<15} {'Performance (GFLOPS)':<20}")
    print("-" * 70)
    for _, row in stats.iterrows():
        print(f"{int(row['matrix_size']):<15} {row['mean']:<15.6f} {row['gflops']:<20.2f}")
    print("=" * 70)
    
    # Peak performance
    peak_gflops = stats['gflops'].max()
    peak_size = stats.loc[stats['gflops'].idxmax(), 'matrix_size']
    print(f"\nPeak Performance: {peak_gflops:.2f} GFLOPS at matrix size {int(peak_size)}x{int(peak_size)}")

if __name__ == "__main__":
    csv_file = "results/benchmark_results.csv"
    output_file = "results/benchmark_plot.png"
    
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    plot_benchmark_results(csv_file, output_file)

