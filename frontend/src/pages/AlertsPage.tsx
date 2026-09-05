import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import Layout from '../components/Layout';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import PaginationControls from '../components/PaginationControls';
import { alertsApi } from '../services/api';
import { formatDate } from '../utils/helpers';
import type { Alert } from '../types';

export default function AlertsPage() {
  const [page, setPage] = useState(1);
  const [statusFilter, setStatusFilter] = useState('');
  const [severityFilter, setSeverityFilter] = useState('');
  const queryClient = useQueryClient();

  const { data, isLoading } = useQuery({
    queryKey: ['alerts', page, statusFilter, severityFilter],
    queryFn: () =>
      alertsApi.list({
        page,
        page_size: 10,
        status: statusFilter || undefined,
        severity: severityFilter || undefined,
      }),
    refetchInterval: 5000,
  });

  const updateMutation = useMutation({
    mutationFn: ({ id, status }: { id: number; status: string }) =>
      alertsApi.update(id, { status }),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['alerts'] }),
  });

  return (
    <Layout title="Alerts" subtitle="Monitor and manage system alerts">
      <div className="flex flex-wrap gap-3 mb-4">
        <select
          value={statusFilter}
          onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
          className="input-field w-auto"
        >
          <option value="">All Statuses</option>
          <option value="active">Active</option>
          <option value="acknowledged">Acknowledged</option>
          <option value="resolved">Resolved</option>
        </select>
        <select
          value={severityFilter}
          onChange={(e) => { setSeverityFilter(e.target.value); setPage(1); }}
          className="input-field w-auto"
        >
          <option value="">All Severities</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
          <option value="critical">Critical</option>
        </select>
      </div>

      <DataTable<Alert>
        columns={[
          { key: 'title', header: 'Alert' },
          { key: 'machine_id', header: 'Machine', render: (a) => `#${a.machine_id}` },
          { key: 'severity', header: 'Severity', render: (a) => <StatusBadge status={a.severity} type="severity" /> },
          { key: 'status', header: 'Status', render: (a) => <StatusBadge status={a.status} /> },
          { key: 'is_auto_assigned', header: 'Auto-Assigned', render: (a) => (a.is_auto_assigned ? 'Yes' : 'No') },
          { key: 'created_at', header: 'Created', render: (a) => formatDate(a.created_at) },
          {
            key: 'actions',
            header: 'Actions',
            render: (a) =>
              a.status === 'active' ? (
                <div className="flex gap-1">
                  <button
                    onClick={() => updateMutation.mutate({ id: a.id, status: 'acknowledged' })}
                    className="btn-secondary text-xs py-1 px-2"
                  >
                    Ack
                  </button>
                  <button
                    onClick={() => updateMutation.mutate({ id: a.id, status: 'resolved' })}
                    className="btn-primary text-xs py-1 px-2"
                  >
                    Resolve
                  </button>
                </div>
              ) : null,
          },
        ]}
        data={data?.items ?? []}
        isLoading={isLoading}
      />
      <PaginationControls page={page} totalPages={data?.total_pages ?? 1} onPageChange={setPage} />
    </Layout>
  );
}
