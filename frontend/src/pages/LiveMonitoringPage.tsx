import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Layout from '../components/Layout';
import TrendChart from '../components/TrendChart';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import { machinesApi, sensorApi, analyticsApi } from '../services/api';
import { formatDate, formatNumber } from '../utils/helpers';
import type { SensorReading } from '../types';

export default function LiveMonitoringPage() {
  const [selectedMachine, setSelectedMachine] = useState<number | null>(null);

  const { data: machines } = useQuery({
    queryKey: ['machines-monitor'],
    queryFn: () => machinesApi.list({ page_size: 50 }),
    refetchInterval: 5000,
  });

  const activeMachineId = selectedMachine ?? machines?.items?.[0]?.id;

  const { data: readings } = useQuery({
    queryKey: ['live-readings', activeMachineId],
    queryFn: () => sensorApi.getLatest(activeMachineId!, 30),
    enabled: !!activeMachineId,
    refetchInterval: 5000,
  });

  const { data: trends } = useQuery({
    queryKey: ['live-trends', activeMachineId],
    queryFn: () => analyticsApi.getTrends(activeMachineId!, 1),
    enabled: !!activeMachineId,
    refetchInterval: 5000,
  });

  const latest = readings?.[0];

  return (
    <Layout title="Live Monitoring" subtitle="Real-time sensor data stream (updates every 5s)">
      <div className="flex flex-wrap gap-2 mb-6">
        {machines?.items?.map((m) => (
          <button
            key={m.id}
            onClick={() => setSelectedMachine(m.id)}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition-all border ${
              activeMachineId === m.id
                ? 'bg-industrial-accent/15 text-industrial-accent border-industrial-accent/30'
                : 'bg-industrial-800 text-gray-400 border-industrial-600/30 hover:border-industrial-accent/20'
            }`}
          >
            {m.machine_id} <StatusBadge status={m.status} />
          </button>
        ))}
      </div>

      {latest && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-3 mb-6">
          {[
            { label: 'Temperature', value: `${formatNumber(latest.temperature)}°C`, color: 'text-status-critical' },
            { label: 'Vibration', value: `${formatNumber(latest.vibration, 3)} mm/s`, color: 'text-status-warning' },
            { label: 'Current', value: `${formatNumber(latest.current)} A`, color: 'text-industrial-accent' },
            { label: 'Humidity', value: `${formatNumber(latest.humidity)}%`, color: 'text-gray-300' },
            { label: 'Pressure', value: `${formatNumber(latest.pressure)} PSI`, color: 'text-gray-300' },
            { label: 'RPM', value: formatNumber(latest.rpm, 0), color: 'text-gray-300' },
          ].map(({ label, value, color }) => (
            <div key={label} className="card text-center">
              <p className="text-xs text-gray-500 mb-1">{label}</p>
              <p className={`text-xl font-bold ${color}`}>{value}</p>
              {latest.anomaly_type && (
                <p className="text-xs text-status-critical mt-1 capitalize">{latest.anomaly_type.replace('_', ' ')}</p>
              )}
            </div>
          ))}
        </div>
      )}

      {trends && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
          <TrendChart title="Temperature" data={trends.temperature} color="#ef4444" unit="°C" />
          <TrendChart title="Vibration" data={trends.vibration} color="#f59e0b" />
          <TrendChart title="Current" data={trends.current} color="#06b6d4" unit="A" />
        </div>
      )}

      <DataTable<SensorReading>
        columns={[
          { key: 'temperature', header: 'Temp (°C)', render: (r) => formatNumber(r.temperature) },
          { key: 'vibration', header: 'Vibration', render: (r) => formatNumber(r.vibration, 3) },
          { key: 'current', header: 'Current (A)', render: (r) => formatNumber(r.current) },
          { key: 'humidity', header: 'Humidity (%)', render: (r) => formatNumber(r.humidity) },
          { key: 'pressure', header: 'Pressure', render: (r) => formatNumber(r.pressure) },
          { key: 'rpm', header: 'RPM', render: (r) => formatNumber(r.rpm, 0) },
          { key: 'anomaly_type', header: 'Anomaly', render: (r) => r.anomaly_type || '—' },
          { key: 'recorded_at', header: 'Timestamp', render: (r) => formatDate(r.recorded_at) },
        ]}
        data={readings ?? []}
        emptyMessage="Waiting for live sensor data..."
      />
    </Layout>
  );
}
