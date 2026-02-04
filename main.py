#!/usr/bin/env python3
"""
Bioinformatics Automation Pipeline - Main CLI

Ponto de entrada principal para o pipeline de bioinformática.
Fornece interface CLI para tarefas de montagem de genomas e visualização de dados.
"""

import argparse
import sys
import logging
from pathlib import Path

# Importação dos módulos internos desenvolvidos
from src.genome_assembly import GenomeAssembler
from src.data_visualization import DataVisualizer

def main():
    """Ponto de entrada principal do CLI."""
    parser = argparse.ArgumentParser(
        description='SiaGel Bioinfo Automation: Pipeline de Genômica Procarionte',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Assemble genome from paired-end reads
  python main.py assemble -1 data/R1.fastq -2 data/R2.fastq -o output_dir

  # Visualize assembly statistics
  python main.py visualize -i data/assembly_stats.csv -o plots_dir
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # --- Subcomando para Montagem de Genoma ---
    assemble_parser = subparsers.add_parser(
        'assemble',
        help='Assemble genome using SPAdes assembler'
    )
    assemble_parser.add_argument('-1', '--forward', required=True, help='Forward reads file (FASTQ)')
    assemble_parser.add_argument('-2', '--reverse', required=True, help='Reverse reads file (FASTQ)')
    assemble_parser.add_argument('-o', '--output', required=True, help='Output directory for results')
    assemble_parser.add_argument('-t', '--threads', type=int, default=4, help='Number of threads (default: 4)')
    assemble_parser.add_argument('--careful', action='store_true', help='Run SPAdes in careful mode')
    
    # --- Subcomando para Visualização de Dados ---
    visualize_parser = subparsers.add_parser(
        'visualize',
        help='Generate visualizations from analysis results'
    )
    visualize_parser.add_argument('-i', '--input', required=True, help='Input CSV file with metrics')
    visualize_parser.add_argument('-o', '--output', required=True, help='Output directory for plots')
    visualize_parser.add_argument('--plot-type', choices=['bar', 'line', 'histogram', 'all'], default='all')

    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)

    # Configuração de Logs
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    try:
        if args.command == 'assemble':
            logging.info(f"🚀 Iniciando montagem de genoma para {args.forward}...")
            assembler = GenomeAssembler(
                forward_reads=args.forward,
                reverse_reads=args.reverse,
                output_dir=args.output,
                threads=args.threads,
                careful_mode=args.careful
            )
            success = assembler.run_assembly()
            
        elif args.command == 'visualize':
            logging.info(f"📊 Gerando visualizações de dados para {args.input}...")
            visualizer = DataVisualizer(
                input_file=args.input,
                output_dir=args.output
            )
            success = visualizer.generate_plots(plot_type=args.plot_type)

        if success:
            logging.info(f"✅ Comando '{args.command}' concluído com sucesso!")
        else:
            logging.error(f"❌ Comando '{args.command}' falhou.")
            sys.exit(1)
            
    except Exception as e:
        logging.error(f"❌ Erro crítico: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
