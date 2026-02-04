import fs from 'fs';
import path from 'path';

export interface AssemblyData {
  sample: string;
  contigs: number;
  total_length: number;
  n50: number;
  gc_content: number;
}

export function loadAssemblyData(): AssemblyData[] {
  const filePath = path.join(process.cwd(), '..', 'data', 'sample_assembly_stats.csv');
  const fileContent = fs.readFileSync(filePath, 'utf-8');
  const lines = fileContent.trim().split('\n');
  
  // Skip header
  const dataLines = lines.slice(1);
  
  return dataLines.map(line => {
    const [sample, contigs, total_length, n50, gc_content] = line.split(',');
    return {
      sample,
      contigs: parseInt(contigs),
      total_length: parseInt(total_length),
      n50: parseInt(n50),
      gc_content: parseFloat(gc_content),
    };
  });
}

export function calculateSummaryStats(data: AssemblyData[]) {
  const totalReads = data.reduce((sum, d) => sum + d.total_length, 0);
  const totalContigs = data.reduce((sum, d) => sum + d.contigs, 0);
  const assemblyStatus = data.length > 0 ? 'Complete' : 'Pending';
  
  return {
    totalReads,
    totalContigs,
    assemblyStatus,
  };
}
