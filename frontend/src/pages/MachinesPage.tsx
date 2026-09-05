import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { Eye } from 'lucide-react';
import Layout from '../components/Layout';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import PaginationControls from '../components/PaginationControls';
import { machinesApi } from '../services/api';
import { formatDate, formatNumber } from '../utils/helpers';
import type { Machine } from '../types';

export default function MachinesPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [statusFilter, setStatusFilter] = useState('');
  const navigate = useNavigate();

  const { data, isLoading } = useQuery({
    queryKey: ['machines', page, search, statusFilter],
    queryFn: () =>
      machinesApi.list({
        page,
        page_size: 10,
        search: search || undefined,
        status: statusFilter || undefined,
      }),
    refetchInterval: 10000,
  });

  return (
    <Layout title="Machines" subtitle="Manage and monitor industrial equipment">
      <div className="flex flex-wrap gap-3 mb-4">
        <select
          value={statusFilter}
          onChange={(e) => { setStatusFilter(e.target.value); setPage(1); }}
          className="input-field w-auto"
        >
          <option value="">All Statuses</option>
          <option value="healthy">Healthy</option>
          <option value="warning">Warning</option>
          <option value="critical">Critical</option>
          <option value="offline">Offline</option>
          <option value="maintenance">Maintenance</option>
        </select>
      </div>

      <DataTable<Machine>
        columns={[
          { key: 'machine_id', header: 'Machine ID' },
          { key: 'name', header: 'Name' },
          { key: 'factory', header: 'Factory' },
          { key: 'location', header: 'Location' },
          { key: 'machine_type', header: 'Type' },
          { key: 'status', header: 'Status', render: (m) => <StatusBadge status={m.status} /> },
          { key: 'health_score', header: 'Health', render: (m) => `${formatNumber(m.health_score)}%` },
          { key: 'installation_date', header: 'Installed', render: (m) => formatDate(m.installation_date) },
          {
            key: 'actions',
            header: 'Actions',
            render: (m) => (
              <button
                onClick={() => navigate(`/machines/${m.id}`)}
                className="btn-secondary text-xs py-1 px-2 flex items-center gap-1"
              >
                <Eye className="w-3 h-3" /> View
              </button>
            ),
          },
        ]}
        data={data?.items ?? []}
        searchValue={search}
        onSearchChange={(v) => { setSearch(v); setPage(1); }}
        searchPlaceholder="Search machines..."
        isLoading={isLoading}
      />
      <PaginationControls page={page} totalPages={data?.total_pages ?? 1} onPageChange={setPage} />
    </Layout>
  );
}
