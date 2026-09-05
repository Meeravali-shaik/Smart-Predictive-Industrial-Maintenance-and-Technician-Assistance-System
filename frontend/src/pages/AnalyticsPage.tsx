import { useQuery } from '@tanstack/react-query';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from 'recharts';
import Layout from '../components/Layout';
import StatCard from '../components/StatCard';
import { analyticsApi } from '../services/api';
import { formatNumber } from '../utils/helpers';
import { Heart, AlertTriangle, Clock, DollarSign, Thermometer, Activity, Zap, FileText } from 'lucide-react';

const COLORS = ['#10b981', '#f59e0b', '#ef4444', '#6b7280'];

export default function AnalyticsPage() {
  const { data: summary } = useQuery({
    queryKey: ['analytics-summary'],
    queryFn: analyticsApi.getSummary,
    refetchInterval: 30000,
  });

  const { data: stats } = useQuery({
    queryKey: ['analytics-stats'],
    queryFn: analyticsApi.getDashboard,
    refetchInterval: 30000,
  });

  const pieData = stats
    ? [
        { name: 'Healthy', value: stats.healthy_machines },
        { name: 'Warning', value: stats.warning_machines },
        { name: 'Critical', value: stats.critical_machines },
        { name: 'Other', value: stats.offline_machines + stats.maintenance_machines },
      ]
    : [];

  const barData = summary
    ? [
        { name: 'Temperature', value: summary.average_temperature },
        { name: 'Current', value: summary.average_current },
        { name: 'Vibration', value: summary.average_vibration },
      ]
    : [];

  const faultData = Object.entries(summary?.failure_distribution ?? {}).map(([name, count]) => ({ name, count }));

  return (
    <Layout title="Analytics" subtitle="Performance metrics and predictive maintenance insights">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard title="Avg Health Score" value={`${formatNumber(summary?.machine_health_score ?? 0)}%`} icon={Heart} color="green" />
        <StatCard title="Monthly Failures" value={summary?.monthly_failures ?? 0} icon={AlertTriangle} color="red" />
        <StatCard title="Total Downtime" value={`${formatNumber(summary?.total_downtime_hours ?? 0)}h`} icon={Clock} color="yellow" />
        <StatCard title="PM Savings" value={`$${formatNumber(summary?.predictive_maintenance_savings ?? 0, 0)}`} icon={DollarSign} color="cyan" />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <StatCard title="Avg Temperature" value={`${formatNumber(summary?.average_temperature ?? 0)}°C`} icon={Thermometer} color="red" />
        <StatCard title="Avg Vibration" value={formatNumber(summary?.average_vibration ?? 0, 3)} icon={Activity} color="yellow" />
        <StatCard title="Reliability" value={`${formatNumber(summary?.machine_reliability ?? 0)}%`} icon={Zap} color="green" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-300 mb-4">Executive KPIs</h3>
          <div className="space-y-3 text-sm text-gray-300">
            <div className="flex justify-between"><span>Predicted Failures</span><span className="text-white">{summary?.predicted_failures ?? 0}</span></div>
            <div className="flex justify-between"><span>Downtime Prevented</span><span className="text-white">{summary?.downtime_prevented_hours ?? 0}h</span></div>
            <div className="flex justify-between"><span>Maintenance Cost Saved</span><span className="text-white">${formatNumber(summary?.maintenance_cost_saved ?? 0, 0)}</span></div>
            <div className="flex justify-between"><span>Critical Machines</span><span className="text-white">{summary?.critical_machines?.length ?? 0}</span></div>
          </div>
        </div>
        <div className="card">
          <h3 className="text-sm font-medium text-gray-300 mb-4">Frequent Faults</h3>
          <div className="space-y-2 text-sm text-gray-300">
            {(summary?.frequent_faults ?? []).map((fault) => (
              <div key={fault.name} className="flex justify-between"><span>{fault.name}</span><span className="text-white">{fault.count}</span></div>
            ))}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-300 mb-4">Machine Status Distribution</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie data={pieData} cx="50%" cy="50%" innerRadius={60} outerRadius={100} dataKey="value" label>
                {pieData.map((_, index) => (
                  <Cell key={index} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
              />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="card">
          <h3 className="text-sm font-medium text-gray-300 mb-4">Average Sensor Readings</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={barData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip
                contentStyle={{ backgroundColor: '#1f2937', border: '1px solid #374151', borderRadius: '8px' }}
              />
              <Bar dataKey="value" fill="#06b6d4" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="mt-6 card">
        <div className="flex items-center gap-2 mb-4">
          <FileText className="w-5 h-5 text-industrial-accent" />
          <h3 className="text-sm font-medium text-gray-300">Fault Distribution</h3>
        </div>
        <div className="flex flex-wrap gap-3">
          {faultData.map((entry) => (
            <div key={entry.name} className="rounded-lg border border-industrial-600/30 bg-industrial-900 px-3 py-2 text-sm text-gray-300">
              <span className="font-medium text-white">{entry.name}</span>: {entry.count}
            </div>
          ))}
        </div>
      </div>
    </Layout>
  );
}
