import { useParams, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { ArrowLeft } from 'lucide-react';
import Layout from '../components/Layout';
import StatCard from '../components/StatCard';
import TrendChart from '../components/TrendChart';
import StatusBadge from '../components/StatusBadge';
import DataTable from '../components/DataTable';
import { machinesApi, sensorApi, predictionsApi, analyticsApi } from '../services/api';
import { formatDate, formatNumber } from '../utils/helpers';
import { Thermometer, Activity, Zap, Heart, Clock3, Wrench, AlertTriangle } from 'lucide-react';
import HealthGauge from '../components/HealthGauge';
import type { SensorReading } from '../types';

export default function MachineDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const machineId = Number(id);

  const { data: machine } = useQuery({
    queryKey: ['machine', machineId],
    queryFn: () => machinesApi.get(machineId),
    enabled: !!machineId,
    refetchInterval: 5000,
  });

  const { data: readings } = useQuery({
    queryKey: ['readings', machineId],
    queryFn: () => sensorApi.getLatest(machineId, 20),
    enabled: !!machineId,
    refetchInterval: 5000,
  });

  const { data: prediction } = useQuery({
    queryKey: ['prediction', machineId],
    queryFn: () => predictionsApi.getLatest(machineId),
    enabled: !!machineId,
    refetchInterval: 5000,
    retry: false,
  });

  const { data: trends } = useQuery({
    queryKey: ['trends', machineId],
    queryFn: () => analyticsApi.getTrends(machineId, 2),
    enabled: !!machineId,
    refetchInterval: 5000,
  });

  const latest = readings?.[0];

  if (!machine) {
    return (
      <Layout title="Machine Details">
        <div className="text-gray-500">Loading machine data...</div>
      </Layout>
    );
  }

  return (
    <Layout title={machine.name} subtitle={`${machine.machine_id} • ${machine.location}`}>
      <button onClick={() => navigate('/machines')} className="btn-secondary mb-4 flex items-center gap-2">
        <ArrowLeft className="w-4 h-4" /> Back to Machines
      </button>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard title="Temperature" value={latest ? `${formatNumber(latest.temperature)}°C` : '--'} icon={Thermometer} color="red" />
        <StatCard title="Vibration" value={latest ? `${formatNumber(latest.vibration, 3)} mm/s` : '--'} icon={Activity} color="yellow" />
        <StatCard title="Current" value={latest ? `${formatNumber(latest.current)} A` : '--'} icon={Zap} color="cyan" />
        <StatCard title="Health Score" value={`${formatNumber(machine.health_score)}%`} icon={Heart} color="green" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-300 mb-4">Health Overview</h3>
          <HealthGauge score={machine.health_score} />
        </div>
        {prediction && (
          <div className="card lg:col-span-2">
            <h3 className="text-sm font-medium text-gray-300 mb-4">Prediction Insight</h3>
            <div className="grid md:grid-cols-2 gap-4 text-sm text-gray-300">
              <div>
                <p className="text-xs text-gray-500">Predicted Fault</p>
                <p className="font-medium text-white">{prediction.failure_type}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Confidence</p>
                <p className="font-medium text-white">{((prediction.confidence ?? prediction.failure_probability) * 100).toFixed(0)}%</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">RUL</p>
                <p className="font-medium text-white">{formatNumber(prediction.remaining_useful_life_days, 1)} days</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Risk</p>
                <p className="font-medium text-white capitalize">{prediction.risk_level?.toLowerCase() ?? 'medium'}</p>
              </div>
            </div>
            <p className="mt-4 text-sm text-gray-400">{prediction.explanation}</p>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6">
        <div className="card lg:col-span-1">
          <h3 className="text-sm font-medium text-gray-300 mb-4">Machine Info</h3>
          <dl className="space-y-3 text-sm">
            {[
              ['Status', <StatusBadge status={machine.status} />],
              ['Factory', machine.factory],
              ['Type', machine.machine_type],
              ['Installed', formatDate(machine.installation_date)],
              ['RPM', latest ? formatNumber(latest.rpm, 0) : '--'],
              ['Humidity', latest ? `${formatNumber(latest.humidity)}%` : '--'],
              ['Pressure', latest ? `${formatNumber(latest.pressure)} PSI` : '--'],
            ].map(([label, value]) => (
              <div key={String(label)} className="flex justify-between">
                <dt className="text-gray-500">{label}</dt>
                <dd className="text-gray-200">{value}</dd>
              </div>
            ))}
          </dl>
        </div>

        {prediction && (
          <div className="card lg:col-span-2">
            <h3 className="text-sm font-medium text-gray-300 mb-4">Latest Prediction</h3>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              <div>
                <p className="text-xs text-gray-500">Failure Type</p>
                <p className="text-sm font-medium text-white">{prediction.failure_type}</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Probability</p>
                <p className="text-sm font-medium text-status-critical">{(prediction.failure_probability * 100).toFixed(1)}%</p>
              </div>
              <div>
                <p className="text-xs text-gray-500">Severity</p>
                <StatusBadge status={prediction.severity} type="severity" />
              </div>
              <div>
                <p className="text-xs text-gray-500">RUL (hours)</p>
                <p className="text-sm font-medium text-white">{formatNumber(prediction.remaining_useful_life_hours, 0)}</p>
              </div>
            </div>
            <div className="flex items-center gap-2 text-industrial-accent text-sm font-medium mb-2"><Wrench className="w-4 h-4" />{prediction.maintenance_recommendation}</div>
            <div className="flex items-center gap-2 text-gray-400 text-sm mb-2"><Clock3 className="w-4 h-4" />Estimated duration: {prediction.estimated_maintenance_duration_hours ?? '--'}h</div>
            <div className="flex items-center gap-2 text-gray-400 text-sm"><AlertTriangle className="w-4 h-4" />Downtime: {prediction.estimated_downtime_hours ?? '--'}h</div>
            <p className="mt-3 text-sm text-gray-400">{prediction.recommended_action}</p>
          </div>
        )}
      </div>

      {trends && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 mb-6">
          <TrendChart title="Temperature" data={trends.temperature} color="#ef4444" unit="°C" />
          <TrendChart title="Vibration" data={trends.vibration} color="#f59e0b" />
          <TrendChart title="Health Score" data={trends.health_score} color="#10b981" />
          <TrendChart title="Failure Probability" data={trends.failure_probability} color="#a855f7" unit="%" />
        </div>
      )}

      <h3 className="text-sm font-medium text-gray-300 mb-3">Recent Readings</h3>
      <DataTable<SensorReading>
        columns={[
          { key: 'temperature', header: 'Temp', render: (r) => `${formatNumber(r.temperature)}°C` },
          { key: 'vibration', header: 'Vibration', render: (r) => formatNumber(r.vibration, 3) },
          { key: 'current', header: 'Current', render: (r) => `${formatNumber(r.current)}A` },
          { key: 'rpm', header: 'RPM', render: (r) => formatNumber(r.rpm, 0) },
          { key: 'anomaly_type', header: 'Anomaly', render: (r) => r.anomaly_type || 'Normal' },
          { key: 'recorded_at', header: 'Time', render: (r) => formatDate(r.recorded_at) },
        ]}
        data={readings ?? []}
      />
    </Layout>
  );
}
