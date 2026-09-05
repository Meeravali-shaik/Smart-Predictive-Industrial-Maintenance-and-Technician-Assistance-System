import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/Layout';
import { machinesApi } from '../services/api';
import { getStatusColor } from '../utils/helpers';

export default function FactoryTwinPage() {
  const navigate = useNavigate();
  const { data } = useQuery({
    queryKey: ['factory-twin-machines'],
    queryFn: () => machinesApi.list({ page_size: 50 }),
  });

  return (
    <Layout title="Digital Twin" subtitle="Live plant layout with machine health status">
      <div className="grid gap-4 lg:grid-cols-3">
        {(data?.items ?? []).map((machine) => (
          <button
            key={machine.id}
            onClick={() => navigate(`/machines/${machine.id}`)}
            className="card text-left hover:border-industrial-accent/50 transition-colors"
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="font-semibold text-white">{machine.name}</h3>
                <p className="text-sm text-gray-400">{machine.machine_id}</p>
              </div>
              <span className={`text-sm font-medium capitalize ${getStatusColor(machine.status)}`}>{machine.status}</span>
            </div>
            <div className="mt-4 h-2 rounded-full bg-industrial-700">
              <div className="h-2 rounded-full bg-industrial-accent" style={{ width: `${machine.health_score}%` }} />
            </div>
            <p className="mt-3 text-sm text-gray-400">{machine.location}</p>
          </button>
        ))}
      </div>
    </Layout>
  );
}
