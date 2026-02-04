'use client';

import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { AssemblyData } from '@/lib/data';

interface ScatterPlotProps {
  data: AssemblyData[];
}

export default function N50ScatterPlot({ data }: ScatterPlotProps) {
  // Transform data for scatter plot
  const scatterData = data.map(d => ({
    name: d.sample,
    x: d.contigs,
    y: d.n50,
  }));

  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 shadow-lg">
      <h3 className="text-xl font-semibold text-slate-100 mb-4">N50 vs Number of Contigs</h3>
      <ResponsiveContainer width="100%" height={400}>
        <ScatterChart margin={{ top: 20, right: 30, bottom: 20, left: 20 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#475569" />
          <XAxis 
            type="number" 
            dataKey="x" 
            name="Contigs" 
            label={{ value: 'Number of Contigs', position: 'insideBottom', offset: -10, fill: '#94a3b8' }}
            stroke="#94a3b8"
            tick={{ fill: '#94a3b8' }}
          />
          <YAxis 
            type="number" 
            dataKey="y" 
            name="N50" 
            label={{ value: 'N50', angle: -90, position: 'insideLeft', fill: '#94a3b8' }}
            stroke="#94a3b8"
            tick={{ fill: '#94a3b8' }}
          />
          <Tooltip 
            cursor={{ strokeDasharray: '3 3' }}
            contentStyle={{ 
              backgroundColor: '#1e293b', 
              border: '1px solid #475569',
              borderRadius: '8px',
              color: '#e2e8f0'
            }}
            formatter={(value: number | undefined, name: string | undefined) => {
              if (!value || !name) return ['', ''];
              if (name === 'N50') return [value.toLocaleString(), 'N50'];
              if (name === 'Contigs') return [value, 'Contigs'];
              return [value, name];
            }}
          />
          <Legend 
            wrapperStyle={{ color: '#94a3b8' }}
            formatter={() => 'Samples'}
          />
          <Scatter 
            name="Samples" 
            data={scatterData} 
            fill="#3b82f6" 
            fillOpacity={0.8}
          />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
}
