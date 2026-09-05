import { getStatusBadge, getSeverityBadge } from '../utils/helpers';

interface StatusBadgeProps {
  status: string;
  type?: 'status' | 'severity';
}

export default function StatusBadge({ status, type = 'status' }: StatusBadgeProps) {
  const badgeClass = type === 'severity' ? getSeverityBadge(status) : getStatusBadge(status);
  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium capitalize ${badgeClass}`}>
      {status}
    </span>
  );
}
