interface SummaryCardProps {
  title: string;
  value: string | number;
  icon?: string;
}

export default function SummaryCard({ title, value, icon }: SummaryCardProps) {
  return (
    <div className="bg-slate-800 border border-slate-700 rounded-lg p-6 shadow-lg hover:border-slate-600 transition-colors">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-slate-400 text-sm font-medium uppercase tracking-wide">{title}</p>
          <p className="text-3xl font-bold text-slate-100 mt-2">{value}</p>
        </div>
        {icon && (
          <div className="text-4xl opacity-20">
            {icon}
          </div>
        )}
      </div>
    </div>
  );
}
