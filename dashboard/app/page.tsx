import SummaryCard from '@/components/SummaryCard';
import N50ScatterPlot from '@/components/N50ScatterPlot';
import DataTable from '@/components/DataTable';
import { loadAssemblyData, calculateSummaryStats } from '@/lib/data';

export default function Home() {
  const data = loadAssemblyData();
  const { totalReads, totalContigs, assemblyStatus } = calculateSummaryStats(data);

  return (
    <div className="min-h-screen bg-slate-900">
      {/* Header */}
      <header className="bg-slate-800 border-b border-slate-700 shadow-lg">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-3xl font-bold text-slate-100">🧬 Bioinformatics Pipeline Dashboard</h1>
          <p className="text-slate-400 mt-2">Prokaryotic Genome Assembly Analytics</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <SummaryCard 
            title="Total Reads" 
            value={totalReads.toLocaleString()} 
            icon="📊"
          />
          <SummaryCard 
            title="Assembly Status" 
            value={assemblyStatus} 
            icon="✅"
          />
          <SummaryCard 
            title="Contig Count" 
            value={totalContigs} 
            icon="🧬"
          />
        </div>

        {/* Scatter Plot */}
        <div className="mb-8">
          <N50ScatterPlot data={data} />
        </div>

        {/* Data Table */}
        <div>
          <DataTable data={data} />
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-slate-800 border-t border-slate-700 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-slate-400 text-center text-sm">
            Automated Bioinformatics Pipeline Analysis &copy; 2026
          </p>
        </div>
      </footer>
    </div>
  );
}
