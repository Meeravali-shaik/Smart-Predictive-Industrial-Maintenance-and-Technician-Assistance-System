import type { LucideIcon } from 'lucide-react';
import { cn } from '../utils/helpers';

interface StatCardProps {
  title: string;
  value: number | string;
  icon: LucideIcon;
  color?: 'green' | 'yellow' | 'red' | 'cyan' | 'gray';
  subtitle?: string;
}

const colorMap = {
  green: 'text-status-healthy bg-status-healthy/10 border-status-healthy/20',
  yellow: 'text-status-warning bg-status-warning/10 border-status-warning/20',
  red: 'text-status-critical bg-status-critical/10 border-status-critical/20',
  cyan: 'text-industrial-accent bg-industrial-accent/10 border-industrial-accent/20',
  gray: 'text-gray-400 bg-gray-500/10 border-gray-500/20',
};

export default function StatCard({ title, value, icon: Icon, color = 'cyan', subtitle }: StatCardProps) {
  return (
    <div className="card hover:border-industrial-accent/30 transition-all duration-300">
      <div className="flex items-start justify-between">
        <div>
          <p className="text-sm text-gray-400 mb-1">{title}</p>
          <p className="text-3xl font-bold text-white">{value}</p>
          {subtitle && <p className="text-xs text-gray-500 mt-1">{subtitle}</p>}
        </div>
        <div className={cn('p-3 rounded-lg border', colorMap[color])}>
          <Icon className="w-6 h-6" />
        </div>
      </div>
    </div>
  );
}
