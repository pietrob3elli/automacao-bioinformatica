import { AssemblyData } from '@/lib/data';

interface DataTableProps {
  data: AssemblyData[];
}

export default function DataTable({ data }: DataTableProps) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 shadow-lg overflow-hidden">
      <h3 className="text-xl font-semibold text-slate-100 mb-4">Assembly Metrics</h3>
      <div className="overflow-x-auto">
        <table className="w-full text-sm text-left">
          <thead className="text-xs text-slate-300 uppercase bg-slate-900">
            <tr>
              <th scope="col" className="px-6 py-3 font-medium">Sample</th>
              <th scope="col" className="px-6 py-3 font-medium text-right">Contigs</th>
              <th scope="col" className="px-6 py-3 font-medium text-right">Total Length</th>
              <th scope="col" className="px-6 py-3 font-medium text-right">N50</th>
              <th scope="col" className="px-6 py-3 font-medium text-right">GC Content (%)</th>
            </tr>
          </thead>
          <tbody>
            {data.map((row, idx) => (
              <tr 
                key={row.sample} 
                className={`${
                  idx % 2 === 0 ? 'bg-slate-800' : 'bg-slate-750'
                } border-b border-slate-700 hover:bg-slate-700 transition-colors`}
              >
                <td className="px-6 py-4 font-medium text-slate-100">{row.sample}</td>
                <td className="px-6 py-4 text-slate-300 text-right">{row.contigs}</td>
                <td className="px-6 py-4 text-slate-300 text-right">{row.total_length.toLocaleString()}</td>
                <td className="px-6 py-4 text-slate-300 text-right">{row.n50.toLocaleString()}</td>
                <td className="px-6 py-4 text-slate-300 text-right">{row.gc_content.toFixed(1)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
