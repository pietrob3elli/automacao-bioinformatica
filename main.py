#!/usr/bin/env python3
"""
Main entry point for the bioinformatics pipeline.
Provides CLI interface for genome assembly and data visualization tasks.
"""

import argparse
import sys
from pathlib import Path
from src.genome_assembly import GenomeAssembler
from src.data_visualization import DataVisualizer


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Bioinformatics Pipeline - Genome Assembly and Data Visualization',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Assemble genome from paired-end reads
  python main.py assemble -1 reads_R1.fastq -2 reads_R2.fastq -o output_dir

  # Visualize assembly statistics
  python main.py visualize -i assembly_stats.csv -o plots_dir
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Genome assembly subcommand
    assemble_parser = subparsers.add_parser(
        'assemble',
        help='Assemble genome using SPAdes'
    )
    assemble_parser.add_argument(
        '-1', '--forward',
        required=True,
        help='Forward reads file (FASTQ)'
    )
    assemble_parser.add_argument(
        '-2', '--reverse',
        required=True,
        help='Reverse reads file (FASTQ)'
    )
    assemble_parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output directory for assembly results'
    )
    assemble_parser.add_argument(
        '-t', '--threads',
        type=int,
        default=4,
        help='Number of threads to use (default: 4)'
    )
    assemble_parser.add_argument(
        '--careful',
        action='store_true',
        help='Run SPAdes in careful mode (reduces mismatches and indels)'
    )
    
    # Data visualization subcommand
    visualize_parser = subparsers.add_parser(
        'visualize',
        help='Generate visualizations from data'
    )
    visualize_parser.add_argument(
        '-i', '--input',
        required=True,
        help='Input CSV file with data to visualize'
    )
    visualize_parser.add_argument(
        '-o', '--output',
        required=True,
        help='Output directory for plots and reports'
    )
    visualize_parser.add_argument(
        '--plot-type',
        choices=['bar', 'line', 'histogram', 'all'],
        default='all',
        help='Type of plot to generate (default: all)'
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        if args.command == 'assemble':
            print(f"Starting genome assembly...")
            print(f"  Forward reads: {args.forward}")
            print(f"  Reverse reads: {args.reverse}")
            print(f"  Output directory: {args.output}")
            print(f"  Threads: {args.threads}")
            
            assembler = GenomeAssembler(
                forward_reads=args.forward,
                reverse_reads=args.reverse,
                output_dir=args.output,
                threads=args.threads,
                careful_mode=args.careful
            )
            
            success = assembler.run_assembly()
            
            if success:
                print(f"\n✓ Assembly completed successfully!")
                print(f"  Results saved to: {args.output}")
            else:
                print(f"\n✗ Assembly failed. Check logs for details.")
                sys.exit(1)
                
        elif args.command == 'visualize':
            print(f"Generating visualizations...")
            print(f"  Input file: {args.input}")
            print(f"  Output directory: {args.output}")
            print(f"  Plot type: {args.plot_type}")
            
            visualizer = DataVisualizer(
                input_file=args.input,
                output_dir=args.output
            )
            
            success = visualizer.generate_plots(plot_type=args.plot_type)
            
            if success:
                print(f"\n✓ Visualizations generated successfully!")
                print(f"  Plots saved to: {args.output}")
            else:
                print(f"\n✗ Visualization failed. Check logs for details.")
                sys.exit(1)
    
    except Exception as e:
        print(f"\n✗ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
