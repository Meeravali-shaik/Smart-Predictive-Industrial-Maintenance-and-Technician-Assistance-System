import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Layout from '../components/Layout';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import PaginationControls from '../components/PaginationControls';
import { predictionsApi } from '../services/api';
import { formatDate, formatNumber } from '../utils/helpers';
import type { Prediction } from '../types';

export default function PredictionsPage() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['predictions', page],
    queryFn: () => predictionsApi.list({ page, page_size: 15 }),
    refetchInterval: 5000,
  });

  return (
    <Layout title="Predictions" subtitle="AI-powered failure predictions and health analysis">
      <div className="card mb-4 bg-industrial-accent/5 border-industrial-accent/20">
        <p className="text-sm text-gray-300">
          <span className="text-industrial-accent font-medium">Phase 1 Active:</span> Rule-based prediction engine
          analyzing temperature, vibration, and current patterns. ML models (Random Forest, Gradient Boosting,
          Logistic Regression) available via API for Phase 2 deployment.
        </p>
      </div>

      <DataTable<Prediction>
        columns={[
          { key: 'machine_id', header: 'Machine', render: (p) => `#${p.machine_id}` },
          { key: 'failure_type', header: 'Predicted Failure' },
          {
            key: 'failure_probability',
            header: 'Probability',
            render: (p) => (
              <span className={p.failure_probability > 0.7 ? 'text-status-critical font-medium' : ''}>
                {(p.failure_probability * 100).toFixed(1)}%
              </span>
            ),
          },
          { key: 'health_score', header: 'Health', render: (p) => `${formatNumber(p.health_score)}%` },
          { key: 'severity', header: 'Severity', render: (p) => <StatusBadge status={p.severity} type="severity" /> },
          { key: 'remaining_useful_life_hours', header: 'RUL (hrs)', render: (p) => formatNumber(p.remaining_useful_life_hours, 0) },
          { key: 'prediction_method', header: 'Method' },
          { key: 'created_at', header: 'Time', render: (p) => formatDate(p.created_at) },
        ]}
        data={data?.items ?? []}
        isLoading={isLoading}
        emptyMessage="Waiting for prediction data..."
      />
      <PaginationControls page={page} totalPages={data?.total_pages ?? 1} onPageChange={setPage} />
    </Layout>
  );
}
