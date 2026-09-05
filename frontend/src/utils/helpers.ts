export function getStatusColor(status: string): string {
  switch (status) {
    case 'healthy':
      return 'text-status-healthy';
    case 'warning':
      return 'text-status-warning';
    case 'critical':
      return 'text-status-critical';
    case 'maintenance':
      return 'text-industrial-accent';
    default:
      return 'text-status-offline';
  }
}

export function getStatusBadge(status: string): string {
  switch (status) {
    case 'healthy':
      return 'badge-healthy';
    case 'warning':
      return 'badge-warning';
    case 'critical':
      return 'badge-critical';
    default:
      return 'badge-offline';
  }
}

export function getSeverityBadge(severity: string): string {
  switch (severity) {
    case 'low':
      return 'badge-healthy';
    case 'medium':
      return 'badge-warning';
    case 'high':
    case 'critical':
      return 'badge-critical';
    default:
      return 'badge-offline';
  }
}

export function formatDate(dateStr: string): string {
  return new Date(dateStr).toLocaleString();
}

export function formatNumber(value: number, decimals = 2): string {
  return value.toFixed(decimals);
}

export function cn(...classes: (string | boolean | undefined)[]): string {
  return classes.filter(Boolean).join(' ');
}
