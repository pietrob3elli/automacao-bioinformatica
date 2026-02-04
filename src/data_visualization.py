"""
Data Visualization Module
Provides functionality for visualizing bioinformatics data using Pandas and Matplotlib.
"""

import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Set style for better-looking plots
sns.set_style('whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)


class DataVisualizer:
    """
    Class for generating visualizations from bioinformatics data.
    
    Supports various plot types including bar charts, line plots, and histograms.
    Uses Pandas for data manipulation and Matplotlib/Seaborn for plotting.
    """
    
    def __init__(self, input_file, output_dir):
        """
        Initialize the DataVisualizer.
        
        Args:
            input_file (str): Path to input CSV file
            output_dir (str): Output directory for plots
        """
        self.input_file = Path(input_file)
        self.output_dir = Path(output_dir)
        self.data = None
        
        # Validate input
        self._validate_input()
        
        # Load data
        self._load_data()
    
    def _validate_input(self):
        """Validate that input file exists."""
        if not self.input_file.exists():
            raise FileNotFoundError(f"Input file not found: {self.input_file}")
        
        if not self.input_file.suffix == '.csv':
            logger.warning(f"Input file is not CSV, will attempt to read anyway")
    
    def _load_data(self):
        """Load data from CSV file using Pandas."""
        try:
            logger.info(f"Loading data from {self.input_file}")
            self.data = pd.read_csv(self.input_file)
            logger.info(f"Loaded {len(self.data)} rows and {len(self.data.columns)} columns")
            logger.info(f"Columns: {', '.join(self.data.columns)}")
            
            # Display basic statistics
            logger.info(f"\nData summary:\n{self.data.describe()}")
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def generate_plots(self, plot_type='all'):
        """
        Generate visualizations from the data.
        
        Args:
            plot_type (str): Type of plot to generate ('bar', 'line', 'histogram', 'all')
            
        Returns:
            bool: True if plots were generated successfully, False otherwise
        """
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        if self.data is None or self.data.empty:
            logger.error("No data loaded")
            return False
        
        try:
            if plot_type == 'all' or plot_type == 'bar':
                self._generate_bar_plot()
            
            if plot_type == 'all' or plot_type == 'line':
                self._generate_line_plot()
            
            if plot_type == 'all' or plot_type == 'histogram':
                self._generate_histogram()
            
            # Generate summary statistics
            self._generate_summary_report()
            
            logger.info(f"All plots saved to {self.output_dir}")
            return True
            
        except Exception as e:
            logger.error(f"Error generating plots: {e}")
            return False
    
    def _generate_bar_plot(self):
        """Generate bar plot for categorical data."""
        logger.info("Generating bar plot...")
        
        # Find categorical and numeric columns
        categorical_cols = self.data.select_dtypes(include=['object', 'category']).columns
        numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        
        if len(categorical_cols) > 0 and len(numeric_cols) > 0:
            cat_col = categorical_cols[0]
            num_col = numeric_cols[0]
            
            plt.figure(figsize=(12, 6))
            
            # Group by category and aggregate
            grouped = self.data.groupby(cat_col)[num_col].mean().sort_values(ascending=False)
            
            grouped.plot(kind='bar', color='steelblue')
            plt.title(f'Average {num_col} by {cat_col}')
            plt.xlabel(cat_col)
            plt.ylabel(f'Average {num_col}')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            output_file = self.output_dir / 'bar_plot.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Bar plot saved to {output_file}")
        else:
            logger.warning("No suitable columns for bar plot")
    
    def _generate_line_plot(self):
        """Generate line plot for time series or sequential data."""
        logger.info("Generating line plot...")
        
        numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        
        if len(numeric_cols) > 0:
            plt.figure(figsize=(12, 6))
            
            # Plot first numeric column
            col = numeric_cols[0]
            plt.plot(self.data.index, self.data[col], marker='o', linewidth=2, markersize=4)
            plt.title(f'{col} Over Samples')
            plt.xlabel('Sample Index')
            plt.ylabel(col)
            plt.grid(True, alpha=0.3)
            plt.tight_layout()
            
            output_file = self.output_dir / 'line_plot.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Line plot saved to {output_file}")
        else:
            logger.warning("No numeric columns for line plot")
    
    def _generate_histogram(self):
        """Generate histograms for all numeric columns."""
        logger.info("Generating histograms...")
        
        numeric_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        
        if len(numeric_cols) > 0:
            # Create subplot for each numeric column
            n_cols = min(len(numeric_cols), 3)
            n_rows = (len(numeric_cols) + n_cols - 1) // n_cols
            
            fig, axes = plt.subplots(n_rows, n_cols, figsize=(5*n_cols, 4*n_rows))
            
            if n_rows == 1 and n_cols == 1:
                axes = [axes]
            else:
                axes = axes.flatten() if len(numeric_cols) > 1 else [axes]
            
            for idx, col in enumerate(numeric_cols):
                if idx < len(axes):
                    axes[idx].hist(self.data[col].dropna(), bins=30, color='steelblue', edgecolor='black', alpha=0.7)
                    axes[idx].set_title(f'Distribution of {col}')
                    axes[idx].set_xlabel(col)
                    axes[idx].set_ylabel('Frequency')
            
            # Hide unused subplots
            for idx in range(len(numeric_cols), len(axes)):
                axes[idx].set_visible(False)
            
            plt.tight_layout()
            
            output_file = self.output_dir / 'histograms.png'
            plt.savefig(output_file, dpi=300, bbox_inches='tight')
            plt.close()
            
            logger.info(f"Histograms saved to {output_file}")
        else:
            logger.warning("No numeric columns for histogram")
    
    def _generate_summary_report(self):
        """Generate a summary statistics report."""
        logger.info("Generating summary report...")
        
        output_file = self.output_dir / 'summary_statistics.txt'
        
        with open(output_file, 'w') as f:
            f.write("=" * 80 + "\n")
            f.write("BIOINFORMATICS DATA SUMMARY REPORT\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(f"Input file: {self.input_file}\n")
            f.write(f"Number of rows: {len(self.data)}\n")
            f.write(f"Number of columns: {len(self.data.columns)}\n\n")
            
            f.write("Column Names:\n")
            for col in self.data.columns:
                f.write(f"  - {col} ({self.data[col].dtype})\n")
            
            f.write("\n" + "=" * 80 + "\n")
            f.write("DESCRIPTIVE STATISTICS\n")
            f.write("=" * 80 + "\n\n")
            
            f.write(str(self.data.describe()))
            
            f.write("\n\n" + "=" * 80 + "\n")
            f.write("MISSING VALUES\n")
            f.write("=" * 80 + "\n\n")
            
            missing = self.data.isnull().sum()
            f.write(str(missing[missing > 0]))
            
            if missing.sum() == 0:
                f.write("No missing values found.\n")
        
        logger.info(f"Summary report saved to {output_file}")


def main():
    """Example usage of DataVisualizer."""
    import argparse
    
    parser = argparse.ArgumentParser(description='Generate visualizations from data')
    parser.add_argument('-i', '--input', required=True, help='Input CSV file')
    parser.add_argument('-o', '--output', required=True, help='Output directory')
    parser.add_argument('--plot-type', choices=['bar', 'line', 'histogram', 'all'],
                       default='all', help='Type of plot to generate')
    
    args = parser.parse_args()
    
    visualizer = DataVisualizer(
        input_file=args.input,
        output_dir=args.output
    )
    
    success = visualizer.generate_plots(plot_type=args.plot_type)
    import sys
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
