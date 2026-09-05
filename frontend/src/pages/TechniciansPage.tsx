import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import Layout from '../components/Layout';
import DataTable from '../components/DataTable';
import StatusBadge from '../components/StatusBadge';
import PaginationControls from '../components/PaginationControls';
import { techniciansApi } from '../services/api';
import { formatDate } from '../utils/helpers';
import type { Technician } from '../types';

export default function TechniciansPage() {
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [availabilityFilter, setAvailabilityFilter] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['technicians', page, search, availabilityFilter],
    queryFn: () =>
      techniciansApi.list({
        page,
        page_size: 10,
        search: search || undefined,
        availability: availabilityFilter || undefined,
      }),
    refetchInterval: 15000,
  });

  return (
    <Layout title="Technicians" subtitle="Manage technician availability and skills">
      <div className="flex flex-wrap gap-3 mb-4">
        <select
          value={availabilityFilter}
          onChange={(e) => { setAvailabilityFilter(e.target.value); setPage(1); }}
          className="input-field w-auto"
        >
          <option value="">All Availability</option>
          <option value="available">Available</option>
          <option value="busy">Busy</option>
          <option value="off_duty">Off Duty</option>
        </select>
      </div>

      <DataTable<Technician>
        columns={[
          { key: 'name', header: 'Name' },
          { key: 'phone', header: 'Phone' },
          { key: 'email', header: 'Email', render: (t) => t.email || '—' },
          { key: 'skills', header: 'Skills' },
          { key: 'availability', header: 'Status', render: (t) => <StatusBadge status={t.availability} /> },
          { key: 'is_active', header: 'Active', render: (t) => (t.is_active ? 'Yes' : 'No') },
          { key: 'created_at', header: 'Joined', render: (t) => formatDate(t.created_at) },
        ]}
        data={data?.items ?? []}
        searchValue={search}
        onSearchChange={(v) => { setSearch(v); setPage(1); }}
        searchPlaceholder="Search technicians..."
        isLoading={isLoading}
      />
      <PaginationControls page={page} totalPages={data?.total_pages ?? 1} onPageChange={setPage} />
    </Layout>
  );
}
