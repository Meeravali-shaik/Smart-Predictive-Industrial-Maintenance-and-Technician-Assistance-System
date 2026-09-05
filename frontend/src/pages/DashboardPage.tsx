import { useQuery } from '@tanstack/react-query';
import { Factory, CheckCircle, AlertTriangle, XCircle, Bell, Users, HeartPulse, Activity } from 'lucide-react';
import Layout from '../components/Layout';
import StatCard from '../components/StatCard';
import TrendChart from '../components/TrendChart';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import HealthGauge from '../components/HealthGauge';
import { analyticsApi, machinesApi, notificationsApi } from '../services/api';
import { formatDate, formatNumber } from '../utils/helpers';
import type { SensorReading, Alert, MaintenanceRecord, Machine } from '../types';

export default function DashboardPage() {
  const { data: stats } = useQuery({
    queryKey: ['dashboard-stats'],
    queryFn: analyticsApi.getDashboard,
    refetchInterval: 5000,
  });

  const { data: machines } = useQuery({
    queryKey: ['machines-list'],
    queryFn: () => machinesApi.list({ page_size: 10 }),
    refetchInterval: 5000,
  });

  const firstMachine = machines?.items?.[0];

  const { data: trends } = useQuery({
    queryKey: ['dashboard-trends', firstMachine?.id],
    queryFn: () => analyticsApi.getTrends(firstMachine!.id, 1),
    enabled: !!firstMachine,
    refetchInterval: 5000,
  });

  const { data: readings } = useQuery({
    queryKey: ['dashboard-readings'],
    queryFn: () => analyticsApi.getDashboardReadings(10),
    refetchInterval: 5000,
  });

  const { data: alerts } = useQuery({
    queryKey: ['dashboard-alerts'],
    queryFn: () => analyticsApi.getDashboardAlerts(10),
    refetchInterval: 5000,
  });

  const { data: maintenance } = useQuery({
    queryKey: ['dashboard-maintenance'],
    queryFn: () => analyticsApi.getDashboardMaintenance(5),
    refetchInterval: 30000,
  });

  const { data: notifications } = useQuery({
    queryKey: ['dashboard-notifications'],
    queryFn: () => notificationsApi.list({ page_size: 5 }),
    refetchInterval: 30000,
  });

  return (
    <Layout title="Dashboard" subtitle="Real-time industrial monitoring overview">
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 mb-6">
        <StatCard title="Total Machines" value={stats?.total_machines ?? 0} icon={Factory} color="cyan" />
        <StatCard title="Healthy" value={stats?.healthy_machines ?? 0} icon={CheckCircle} color="green" />
        <StatCard title="Warning" value={stats?.warning_machines ?? 0} icon={AlertTriangle} color="yellow" />
        <StatCard title="Critical" value={stats?.critical_machines ?? 0} icon={XCircle} color="red" />
        <StatCard title="Active Alerts" value={stats?.active_alerts ?? 0} icon={Bell} color="red" />
        <StatCard title="Technicians" value={stats?.available_technicians ?? 0} icon={Users} color="green" subtitle="Available" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <div className="card">
          <div className="flex items-center gap-2 mb-3">
            <HeartPulse className="w-5 h-5 text-industrial-accent" />
            <h3 className="text-sm font-medium text-gray-300">Average Health</h3>
          </div>
          <HealthGauge score={stats?.average_health_score ?? 0} />
        </div>
        <div className="card">
          <div className="flex items-center gap-2 mb-3">
            <Activity className="w-5 h-5 text-status-warning" />
            <h3 className="text-sm font-medium text-gray-300">Predicted Failures</h3>
          </div>
          <p className="text-3xl font-semibold text-white">{stats?.predicted_failures ?? 0}</p>
          <p className="text-sm text-gray-400 mt-2">Risk alerts currently flagged</p>
        </div>
        <div className="card">
          <div className="flex items-center gap-2 mb-3">
            <Bell className="w-5 h-5 text-status-critical" />
            <h3 className="text-sm font-medium text-gray-300">Notifications</h3>
          </div>
          <ul className="space-y-2 text-sm text-gray-400">
            {(notifications?.items ?? []).slice(0, 3).map((item) => (
              <li key={item.id} className="truncate">• {item.title}</li>
            ))}
          </ul>
        </div>
      </div>

      {trends && (
        <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-4 mb-6">
          <TrendChart title="Temperature Trend (°C)" data={trends.temperature} color="#ef4444" unit="°C" />
          <TrendChart title="Vibration Trend (mm/s)" data={trends.vibration} color="#f59e0b" unit=" mm/s" />
          <TrendChart title="Current Trend (A)" data={trends.current} color="#06b6d4" unit="A" />
          <TrendChart title="Health Score Trend" data={trends.health_score} color="#10b981" unit="%" />
          <TrendChart title="Failure Probability (%)" data={trends.failure_probability} color="#a855f7" unit="%" />
        </div>
      )}

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 mb-6">
        <div>
          <h3 className="text-sm font-medium text-gray-300 mb-3">Latest Readings</h3>
          <DataTable<SensorReading>
            columns={[
              { key: 'machine_id', header: 'Machine', render: (r) => `#${r.machine_id}` },
              { key: 'temperature', header: 'Temp (°C)', render: (r) => formatNumber(r.temperature) },
              { key: 'vibration', header: 'Vib (mm/s)', render: (r) => formatNumber(r.vibration, 3) },
              { key: 'current', header: 'Current (A)', render: (r) => formatNumber(r.current) },
              { key: 'recorded_at', header: 'Time', render: (r) => formatDate(r.recorded_at) },
            ]}
            data={readings ?? []}
            emptyMessage="Waiting for sensor data..."
          />
        </div>
        <div>
          <h3 className="text-sm font-medium text-gray-300 mb-3">Recent Alerts</h3>
          <DataTable<Alert>
            columns={[
              { key: 'title', header: 'Alert' },
              { key: 'severity', header: 'Severity', render: (a) => <StatusBadge status={a.severity} type="severity" /> },
              { key: 'status', header: 'Status', render: (a) => <StatusBadge status={a.status} /> },
              { key: 'created_at', header: 'Time', render: (a) => formatDate(a.created_at) },
            ]}
            data={alerts ?? []}
            emptyMessage="No active alerts"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
        <div>
          <h3 className="text-sm font-medium text-gray-300 mb-3">Recent Maintenance</h3>
          <DataTable<MaintenanceRecord>
            columns={[
              { key: 'machine_id', header: 'Machine', render: (m) => `#${m.machine_id}` },
              { key: 'issue', header: 'Issue' },
              { key: 'downtime_hours', header: 'Downtime (h)', render: (m) => formatNumber(m.downtime_hours) },
              { key: 'repair_date', header: 'Date', render: (m) => formatDate(m.repair_date) },
            ]}
            data={maintenance ?? []}
          />
        </div>
        <div>
          <h3 className="text-sm font-medium text-gray-300 mb-3">Machine Status</h3>
          <DataTable<Machine>
            columns={[
              { key: 'machine_id', header: 'ID' },
              { key: 'name', header: 'Name' },
              { key: 'status', header: 'Status', render: (m) => <StatusBadge status={m.status} /> },
              { key: 'health_score', header: 'Health', render: (m) => `${formatNumber(m.health_score)}%` },
            ]}
            data={machines?.items ?? []}
          />
        </div>
      </div>
    </Layout>
  );
}
