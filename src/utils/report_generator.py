"""
Report generation module for creating analysis summaries.

This module provides functionality to generate Markdown reports summarizing
the results of bioinformatics analyses.
"""

import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from datetime import datetime


logger = logging.getLogger(__name__)


class ReportGenerator:
    """
    Generate summary reports in Markdown format.
    
    This class provides methods to create professional reports from
    analysis results, including QC metrics, assembly statistics, and more.
    """
    
    def __init__(self, output_dir: Path = Path("reports")):
        """
        Initialize the ReportGenerator.
        
        Args:
            output_dir: Directory to store generated reports (default: 'reports').
        """
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"ReportGenerator initialized with output directory: {output_dir}")
    
    def create_report(
        self,
        title: str,
        sections: List[Dict[str, str]],
        output_file: str = "analysis_report.md"
    ) -> Path:
        """
        Create a Markdown report with multiple sections.
        
        Args:
            title: Report title.
            sections: List of dictionaries with 'title' and 'content' keys.
            output_file: Name of the output Markdown file.
        
        Returns:
            Path to the generated report file.
        
        Example:
            >>> reporter = ReportGenerator()
            >>> sections = [
            ...     {'title': 'Quality Control', 'content': 'All samples passed QC'},
            ...     {'title': 'Assembly', 'content': 'Assembly completed successfully'}
            ... ]
            >>> report_path = reporter.create_report("Analysis Report", sections)
        """
        logger.info(f"Creating report: {title}")
        
        report_path = self.output_dir / output_file
        
        try:
            with open(report_path, 'w', encoding='utf-8') as f:
                # Write header
                f.write(f"# {title}\n\n")
                f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write("---\n\n")
                
                # Write sections
                for section in sections:
                    section_title = section.get('title', 'Untitled Section')
                    section_content = section.get('content', '')
                    
                    f.write(f"## {section_title}\n\n")
                    f.write(f"{section_content}\n\n")
                    f.write("---\n\n")
            
            logger.info(f"Report successfully created: {report_path}")
            return report_path
            
        except Exception as e:
            logger.error(f"Error creating report: {str(e)}")
            raise
    
    def add_qc_section(
        self,
        sample_name: str,
        qc_metrics: Dict[str, str]
    ) -> Dict[str, str]:
        """
        Create a Quality Control section for the report.
        
        Args:
            sample_name: Name of the sample.
            qc_metrics: Dictionary of QC metrics.
        
        Returns:
            Dictionary with 'title' and 'content' for report section.
        
        Example:
            >>> reporter = ReportGenerator()
            >>> metrics = {
            ...     'total_sequences': '1000000',
            ...     'gc_content': '52.3',
            ...     'poor_quality': '0'
            ... }
            >>> section = reporter.add_qc_section("Sample1", metrics)
        """
        logger.info(f"Creating QC section for sample: {sample_name}")
        
        content = f"### Sample: {sample_name}\n\n"
        
        if not qc_metrics:
            content += "*No QC metrics available.*\n"
        else:
            content += "| Metric | Value |\n"
            content += "|--------|-------|\n"
            
            for key, value in qc_metrics.items():
                # Format key for display
                display_key = key.replace('_', ' ').title()
                content += f"| {display_key} | {value} |\n"
        
        return {
            'title': f'Quality Control - {sample_name}',
            'content': content
        }
    
    def add_assembly_section(
        self,
        sample_name: str,
        assembly_stats: Dict[str, Any]
    ) -> Dict[str, str]:
        """
        Create an Assembly Statistics section for the report.
        
        Args:
            sample_name: Name of the sample.
            assembly_stats: Dictionary of assembly statistics.
        
        Returns:
            Dictionary with 'title' and 'content' for report section.
        
        Example:
            >>> reporter = ReportGenerator()
            >>> stats = {
            ...     'num_contigs': 42,
            ...     'total_length': 4500000,
            ...     'n50': 125000
            ... }
            >>> section = reporter.add_assembly_section("Sample1", stats)
        """
        logger.info(f"Creating assembly section for sample: {sample_name}")
        
        content = f"### Sample: {sample_name}\n\n"
        
        if not assembly_stats:
            content += "*No assembly statistics available.*\n"
        else:
            content += "| Statistic | Value |\n"
            content += "|-----------|-------|\n"
            
            # Format specific statistics nicely
            for key, value in assembly_stats.items():
                display_key = key.replace('_', ' ').title()
                
                # Format large numbers with commas
                if isinstance(value, int) and value > 999:
                    display_value = f"{value:,}"
                else:
                    display_value = str(value)
                
                content += f"| {display_key} | {display_value} |\n"
        
        return {
            'title': f'Assembly Statistics - {sample_name}',
            'content': content
        }
    
    def add_summary_section(
        self,
        total_samples: int,
        successful: int,
        failed: int,
        notes: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Create a Summary section for the report.
        
        Args:
            total_samples: Total number of samples processed.
            successful: Number of successful samples.
            failed: Number of failed samples.
            notes: Optional additional notes.
        
        Returns:
            Dictionary with 'title' and 'content' for report section.
        
        Example:
            >>> reporter = ReportGenerator()
            >>> section = reporter.add_summary_section(10, 8, 2, "2 samples had low coverage")
        """
        logger.info("Creating summary section")
        
        content = "### Processing Summary\n\n"
        content += f"- **Total Samples:** {total_samples}\n"
        content += f"- **Successful:** {successful}\n"
        content += f"- **Failed:** {failed}\n"
        
        if total_samples > 0:
            success_rate = (successful / total_samples) * 100
            content += f"- **Success Rate:** {success_rate:.1f}%\n"
        
        if notes:
            content += f"\n**Notes:**\n\n{notes}\n"
        
        return {
            'title': 'Summary',
            'content': content
        }
    
    def add_table_from_csv(
        self,
        title: str,
        data: List[Dict[str, str]],
        columns: Optional[List[str]] = None
    ) -> Dict[str, str]:
        """
        Create a section with a table from CSV data.
        
        Args:
            title: Section title.
            data: List of dictionaries (from CSV reader).
            columns: Optional list of columns to include. If None, uses all.
        
        Returns:
            Dictionary with 'title' and 'content' for report section.
        
        Example:
            >>> reporter = ReportGenerator()
            >>> data = [
            ...     {'sample': 'S1', 'status': 'pass'},
            ...     {'sample': 'S2', 'status': 'fail'}
            ... ]
            >>> section = reporter.add_table_from_csv("Results", data)
        """
        logger.info(f"Creating table section: {title}")
        
        if not data:
            return {
                'title': title,
                'content': "*No data available.*\n"
            }
        
        # Get columns
        if columns is None:
            columns = list(data[0].keys())
        
        # Create table header
        content = "| " + " | ".join(columns) + " |\n"
        content += "|" + "|".join(["---"] * len(columns)) + "|\n"
        
        # Add rows
        for row in data:
            values = [str(row.get(col, '')) for col in columns]
            content += "| " + " | ".join(values) + " |\n"
        
        return {
            'title': title,
            'content': content
        }
