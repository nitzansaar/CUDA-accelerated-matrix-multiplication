#!/usr/bin/env python3

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

# Read the CSV file
csv_file = 'results/benchmark_cpu_results.csv'

if not os.path.exists(csv_file):
    print(f"Error: Results file '{csv_file}' not found.")
    print("Please run the benchmark first with: ./tests/benchmark_cpu.sh")
    sys.exit(1)

df = pd.read_csv(csv_file)

# Filter out error rows
df = df[df['runtime_ms'] != 'ERROR']
df['runtime_ms'] = pd.to_numeric(df['runtime_ms'])

# Calculate mean and std for each matrix size
stats = df.groupby('matrix_size')['runtime_ms'].agg(['mean', 'std']).reset_index()

# Create the plot
plt.figure(figsize=(12, 6))

# Plot: Runtime vs Matrix Size
plt.subplot(1, 2, 1)
plt.errorbar(stats['matrix_size'], stats['mean'], yerr=stats['std'],
             marker='o', capsize=5, capthick=2, linewidth=2, markersize=8, color='#e74c3c')
plt.xlabel('Matrix Size (N)', fontsize=12, fontweight='bold')
plt.ylabel('Time (ms)', fontsize=12, fontweight='bold')
plt.title('CPU Matrix Multiplication Runtime vs Size', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xscale('log', base=2)
plt.yscale('log')
plt.xticks(stats['matrix_size'], [str(int(x)) for x in stats['matrix_size']], rotation=45)

# Plot 2: Performance in GFLOPS
plt.subplot(1, 2, 2)
# Calculate GFLOPS: (2*N^3 operations) / (time in seconds)
stats['gflops'] = (2 * stats['matrix_size']**3) / (stats['mean'] * 1e6)
plt.plot(stats['matrix_size'], stats['gflops'], 'o-', linewidth=2, markersize=8, color='#27ae60')
plt.xlabel('Matrix Size (N)', fontsize=12, fontweight='bold')
plt.ylabel('Performance (GFLOPS)', fontsize=12, fontweight='bold')
plt.title('CPU Performance (GFLOPS)', fontsize=14, fontweight='bold')
plt.grid(True, alpha=0.3)
plt.xscale('log', base=2)
plt.xticks(stats['matrix_size'], [str(int(x)) for x in stats['matrix_size']], rotation=45)

plt.tight_layout()
plt.savefig('results/benchmark_cpu_plot.png', dpi=300, bbox_inches='tight')
print("Plot saved to: results/benchmark_cpu_plot.png")

# Print statistics table
print("\nBenchmark Statistics:")
print("=" * 70)
print(f"{'Matrix Size':<15} {'Mean (ms)':<15} {'Std Dev (ms)':<15} {'GFLOPS':<15}")
print("-" * 70)
for _, row in stats.iterrows():
    print(f"{int(row['matrix_size']):<15} {row['mean']:<15.6f} {row['std']:<15.6f} {row['gflops']:<15.2f}")
print("=" * 70)

# Peak performance
peak_gflops = stats['gflops'].max()
peak_size = stats.loc[stats['gflops'].idxmax(), 'matrix_size']
print(f"\nPeak Performance: {peak_gflops:.2f} GFLOPS at matrix size {int(peak_size)}x{int(peak_size)}")