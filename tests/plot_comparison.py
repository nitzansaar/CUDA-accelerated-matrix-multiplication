#!/usr/bin/env python3
"""
Combined CPU vs GPU benchmark comparison plotter.
Generates a side-by-side comparison of CPU and GPU performance.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import os

def plot_comparison():
    """Plot CPU vs GPU benchmark comparison."""
    
    # File paths
    cpu_file = "results/benchmark_cpu_results.csv"
    gpu_file = "results/benchmark_results.csv"
    output_file = "results/comparison_plot.png"
    
    # Check if files exist
    if not os.path.exists(cpu_file):
        print(f"Error: CPU results file '{cpu_file}' not found.")
        sys.exit(1)
    
    if not os.path.exists(gpu_file):
        print(f"Error: GPU results file '{gpu_file}' not found.")
        sys.exit(1)
    
    # Read CPU data
    df_cpu = pd.read_csv(cpu_file)
    df_cpu = df_cpu[df_cpu['runtime_ms'] != 'ERROR']
    df_cpu['runtime_ms'] = pd.to_numeric(df_cpu['runtime_ms'])
    cpu_stats = df_cpu.groupby('matrix_size')['runtime_ms'].agg(['mean', 'std']).reset_index()
    
    # Read GPU data
    df_gpu = pd.read_csv(gpu_file)
    df_gpu = df_gpu[df_gpu['runtime_ms'] != 'ERROR']
    df_gpu['runtime_ms'] = pd.to_numeric(df_gpu['runtime_ms'])
    gpu_stats = df_gpu.groupby('matrix_size')['runtime_ms'].agg(['mean', 'std']).reset_index()
    
    # Create figure with subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    
    # Plot 1: CPU Performance
    ax1 = axes[0]
    ax1.errorbar(cpu_stats['matrix_size'], cpu_stats['mean'], yerr=cpu_stats['std'],
                 fmt='o-', capsize=5, capthick=2, linewidth=2, markersize=8,
                 color='#e74c3c', label='CPU')
    ax1.set_xlabel('Matrix Size (N)', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Runtime (ms)', fontsize=12, fontweight='bold')
    ax1.set_title('CPU Performance', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log', base=2)
    ax1.set_yscale('log')
    ax1.set_xticks(cpu_stats['matrix_size'])
    ax1.set_xticklabels([str(int(x)) for x in cpu_stats['matrix_size']], rotation=45)
    
    # Plot 2: GPU Performance
    ax2 = axes[1]
    ax2.errorbar(gpu_stats['matrix_size'], gpu_stats['mean'], yerr=gpu_stats['std'],
                 fmt='o-', capsize=5, capthick=2, linewidth=2, markersize=8,
                 color='#3498db', label='GPU')
    ax2.set_xlabel('Matrix Size (N)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Runtime (ms)', fontsize=12, fontweight='bold')
    ax2.set_title('GPU Performance', fontsize=14, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log', base=2)
    ax2.set_yscale('log')
    ax2.set_xticks(gpu_stats['matrix_size'])
    ax2.set_xticklabels([str(int(x)) for x in gpu_stats['matrix_size']], rotation=45)
    
    # Plot 3: Direct Comparison and Speedup
    ax3 = axes[2]
    
    # Merge data on common matrix sizes
    merged = pd.merge(cpu_stats, gpu_stats, on='matrix_size', suffixes=('_cpu', '_gpu'))
    
    # Plot both on the same axes
    ax3.errorbar(merged['matrix_size'], merged['mean_cpu'], yerr=merged['std_cpu'],
                 fmt='o-', capsize=5, capthick=2, linewidth=2, markersize=8,
                 color='#e74c3c', label='CPU', alpha=0.8)
    ax3.errorbar(merged['matrix_size'], merged['mean_gpu'], yerr=merged['std_gpu'],
                 fmt='s-', capsize=5, capthick=2, linewidth=2, markersize=8,
                 color='#3498db', label='GPU', alpha=0.8)
    
    ax3.set_xlabel('Matrix Size (N)', fontsize=12, fontweight='bold')
    ax3.set_ylabel('Runtime (ms)', fontsize=12, fontweight='bold')
    ax3.set_title('CPU vs GPU Comparison', fontsize=14, fontweight='bold')
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log', base=2)
    ax3.set_yscale('log')
    ax3.set_xticks(merged['matrix_size'])
    ax3.set_xticklabels([str(int(x)) for x in merged['matrix_size']], rotation=45)
    ax3.legend(fontsize=10, loc='upper left')
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=150, bbox_inches='tight')
    print(f"Comparison plot saved to: {output_file}")
    
    # Print comparison statistics
    print("\n" + "=" * 80)
    print("CPU vs GPU Performance Comparison")
    print("=" * 80)
    print(f"{'Matrix Size':<12} {'CPU (ms)':<15} {'GPU (ms)':<15} {'Speedup':<15}")
    print("-" * 80)
    
    for _, row in merged.iterrows():
        speedup = row['mean_cpu'] / row['mean_gpu']
        print(f"{int(row['matrix_size']):<12} {row['mean_cpu']:<15.6f} {row['mean_gpu']:<15.6f} {speedup:<15.2f}x")
    
    print("=" * 80)
    
    # Overall statistics
    avg_speedup = (merged['mean_cpu'] / merged['mean_gpu']).mean()
    max_speedup = (merged['mean_cpu'] / merged['mean_gpu']).max()
    max_speedup_size = merged.loc[(merged['mean_cpu'] / merged['mean_gpu']).idxmax(), 'matrix_size']
    
    print(f"\nAverage Speedup: {avg_speedup:.2f}x")
    print(f"Maximum Speedup: {max_speedup:.2f}x at matrix size {int(max_speedup_size)}x{int(max_speedup_size)}")
    print("")

if __name__ == "__main__":
    plot_comparison()

