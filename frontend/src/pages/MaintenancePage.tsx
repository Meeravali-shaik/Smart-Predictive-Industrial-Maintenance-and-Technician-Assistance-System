import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Layout from '../components/Layout';
import DataTable from '../components/DataTable';
import PaginationControls from '../components/PaginationControls';
import { maintenanceApi } from '../services/api';
import { formatDate, formatNumber } from '../utils/helpers';
import type { MaintenanceRecord } from '../types';

export default function MaintenancePage() {
  const [page, setPage] = useState(1);

  const { data, isLoading } = useQuery({
    queryKey: ['maintenance', page],
    queryFn: () => maintenanceApi.list({ page, page_size: 10 }),
    refetchInterval: 30000,
  });

  return (
    <Layout title="Maintenance" subtitle="Track repairs, downtime, and maintenance history">
      <DataTable<MaintenanceRecord>
        columns={[
          { key: 'machine_id', header: 'Machine', render: (m) => `#${m.machine_id}` },
          { key: 'issue', header: 'Issue' },
          { key: 'technician_id', header: 'Technician', render: (m) => (m.technician_id ? `#${m.technician_id}` : '—') },
          { key: 'parts_replaced', header: 'Parts', render: (m) => m.parts_replaced || '—' },
          { key: 'downtime_hours', header: 'Downtime (h)', render: (m) => formatNumber(m.downtime_hours) },
          { key: 'status', header: 'Status' },
          { key: 'repair_date', header: 'Repair Date', render: (m) => formatDate(m.repair_date) },
        ]}
        data={data?.items ?? []}
        isLoading={isLoading}
      />
      <PaginationControls page={page} totalPages={data?.total_pages ?? 1} onPageChange={setPage} />
    </Layout>
  );
}
