export type UserRole = 'admin' | 'factory_manager' | 'technician';

export interface User {
  id: number;
  email: string;
  username: string;
  full_name: string;
  role: UserRole;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Machine {
  id: number;
  machine_id: string;
  name: string;
  factory: string;
  location: string;
  machine_type: string;
  installation_date: string;
  status: 'healthy' | 'warning' | 'critical' | 'offline' | 'maintenance';
  health_score: number;
  description?: string;
  created_at: string;
  updated_at: string;
}

export interface SensorReading {
  id: number;
  machine_id: number;
  temperature: number;
  vibration: number;
  current: number;
  humidity: number;
  pressure: number;
  rpm: number;
  anomaly_type?: string;
  recorded_at: string;
}

export interface Prediction {
  id: number;
  machine_id: number;
  failure_type: string;
  failure_probability: number;
  health_score: number;
  severity: 'low' | 'medium' | 'high' | 'critical';
  remaining_useful_life_hours: number;
  remaining_useful_life_days: number;
  confidence?: number;
  explanation?: string;
  risk_level?: string;
  maintenance_recommendation?: string;
  estimated_maintenance_duration_hours?: number;
  estimated_downtime_hours?: number;
  estimated_maintenance_cost_usd?: number;
  prediction_method: string;
  recommended_action?: string;
  created_at: string;
}

export interface Alert {
  id: number;
  machine_id: number;
  technician_id?: number;
  title: string;
  message: string;
  alert_type: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  status: 'active' | 'acknowledged' | 'resolved';
  threshold_value?: number;
  actual_value?: number;
  recommended_action?: string;
  is_auto_assigned: boolean;
  created_at: string;
  resolved_at?: string;
}

export interface Technician {
  id: number;
  user_id?: number;
  name: string;
  phone: string;
  email?: string;
  skills: string;
  specialization?: string;
  current_workload: number;
  assignment_count: number;
  availability: 'available' | 'busy' | 'off_duty';
  is_active: boolean;
  created_at: string;
}

export interface MaintenanceRecord {
  id: number;
  machine_id: number;
  technician_id?: number;
  issue: string;
  repair_date: string;
  repair_notes?: string;
  parts_replaced?: string;
  downtime_hours: number;
  status: string;
  created_at: string;
}

export interface Notification {
  id: number;
  user_id: number;
  title: string;
  message: string;
  notification_type: string;
  is_read: boolean;
  status: 'unread' | 'read' | 'archived';
  reference_id?: number;
  created_at: string;
}

export interface DashboardStats {
  total_machines: number;
  healthy_machines: number;
  warning_machines: number;
  critical_machines: number;
  active_alerts: number;
  available_technicians: number;
  offline_machines: number;
  maintenance_machines: number;
  average_health_score: number;
  predicted_failures: number;
  maintenance_cost_saved: number;
  downtime_prevented_hours: number;
}

export interface TrendPoint {
  timestamp: string;
  value: number;
}

export interface MachineTrends {
  temperature: TrendPoint[];
  vibration: TrendPoint[];
  current: TrendPoint[];
  health_score: TrendPoint[];
  failure_probability: TrendPoint[];
}

export interface AnalyticsSummary {
  machine_health_score: number;
  monthly_failures: number;
  total_downtime_hours: number;
  average_temperature: number;
  average_current: number;
  average_vibration: number;
  predictive_maintenance_savings: number;
  machine_reliability: number;
  downtime_prevented_hours: number;
  predicted_failures: number;
  maintenance_cost_saved: number;
  failure_distribution: Record<string, number>;
  critical_machines: Array<{ name: string; health_score: number; status: string }>;
  frequent_faults: Array<{ name: string; count: number }>;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
}
