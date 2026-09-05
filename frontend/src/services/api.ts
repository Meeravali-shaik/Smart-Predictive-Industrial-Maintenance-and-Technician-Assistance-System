import axios from 'axios';
import type {
  Alert,
  AnalyticsSummary,
  DashboardStats,
  LoginResponse,
  Machine,
  MachineTrends,
  MaintenanceRecord,
  Notification,
  PaginatedResponse,
  Prediction,
  SensorReading,
  Technician,
  User,
} from '../types';

const api = axios.create({
  baseURL: '/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      if (window.location.pathname !== '/login') {
        window.location.href = '/login';
      }
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: async (username: string, password: string): Promise<LoginResponse> => {
    const formData = new URLSearchParams();
    formData.append('username', username);
    formData.append('password', password);
    const { data } = await api.post<LoginResponse>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
    return data;
  },
  register: async (userData: object): Promise<User> => {
    const { data } = await api.post<User>('/auth/register', userData);
    return data;
  },
  getMe: async (): Promise<User> => {
    const { data } = await api.get<User>('/auth/me');
    return data;
  },
};

export const machinesApi = {
  list: async (params?: object): Promise<PaginatedResponse<Machine>> => {
    const { data } = await api.get<PaginatedResponse<Machine>>('/machines', { params });
    return data;
  },
  get: async (id: number): Promise<Machine> => {
    const { data } = await api.get<Machine>(`/machines/${id}`);
    return data;
  },
  create: async (machine: object): Promise<Machine> => {
    const { data } = await api.post<Machine>('/machines', machine);
    return data;
  },
  update: async (id: number, machine: object): Promise<Machine> => {
    const { data } = await api.put<Machine>(`/machines/${id}`, machine);
    return data;
  },
  delete: async (id: number): Promise<void> => {
    await api.delete(`/machines/${id}`);
  },
};

export const sensorApi = {
  list: async (params?: object): Promise<PaginatedResponse<SensorReading>> => {
    const { data } = await api.get<PaginatedResponse<SensorReading>>('/sensor-readings', { params });
    return data;
  },
  getLatest: async (machineId: number, limit = 50): Promise<SensorReading[]> => {
    const { data } = await api.get<SensorReading[]>(`/sensor-readings/latest/${machineId}`, {
      params: { limit },
    });
    return data;
  },
};

export const predictionsApi = {
  list: async (params?: object): Promise<PaginatedResponse<Prediction>> => {
    const { data } = await api.get<PaginatedResponse<Prediction>>('/predictions', { params });
    return data;
  },
  getLatest: async (machineId: number): Promise<Prediction> => {
    const { data } = await api.get<Prediction>(`/predictions/latest/${machineId}`);
    return data;
  },
};

export const alertsApi = {
  list: async (params?: object): Promise<PaginatedResponse<Alert>> => {
    const { data } = await api.get<PaginatedResponse<Alert>>('/alerts', { params });
    return data;
  },
  get: async (id: number): Promise<Alert> => {
    const { data } = await api.get<Alert>(`/alerts/${id}`);
    return data;
  },
  update: async (id: number, update: object): Promise<Alert> => {
    const { data } = await api.put<Alert>(`/alerts/${id}`, update);
    return data;
  },
};

export const techniciansApi = {
  list: async (params?: object): Promise<PaginatedResponse<Technician>> => {
    const { data } = await api.get<PaginatedResponse<Technician>>('/technicians', { params });
    return data;
  },
  create: async (tech: object): Promise<Technician> => {
    const { data } = await api.post<Technician>('/technicians', tech);
    return data;
  },
  update: async (id: number, tech: object): Promise<Technician> => {
    const { data } = await api.put<Technician>(`/technicians/${id}`, tech);
    return data;
  },
  delete: async (id: number): Promise<void> => {
    await api.delete(`/technicians/${id}`);
  },
};

export const maintenanceApi = {
  list: async (params?: object): Promise<PaginatedResponse<MaintenanceRecord>> => {
    const { data } = await api.get<PaginatedResponse<MaintenanceRecord>>('/maintenance', { params });
    return data;
  },
  create: async (record: object): Promise<MaintenanceRecord> => {
    const { data } = await api.post<MaintenanceRecord>('/maintenance', record);
    return data;
  },
};

export const notificationsApi = {
  list: async (params?: object): Promise<PaginatedResponse<Notification>> => {
    const { data } = await api.get<PaginatedResponse<Notification>>('/notifications', { params });
    return data;
  },
  markRead: async (id: number): Promise<Notification> => {
    const { data } = await api.put<Notification>(`/notifications/${id}/read`);
    return data;
  },
  archive: async (id: number): Promise<Notification> => {
    const { data } = await api.put<Notification>(`/notifications/${id}/archive`);
    return data;
  },
};

export const analyticsApi = {
  getDashboard: async (): Promise<DashboardStats> => {
    const { data } = await api.get<DashboardStats>('/analytics/dashboard');
    return data;
  },
  getTrends: async (machineId: number, hours = 24): Promise<MachineTrends> => {
    const { data } = await api.get<MachineTrends>(`/analytics/trends/${machineId}`, { params: { hours } });
    return data;
  },
  getSummary: async (): Promise<AnalyticsSummary> => {
    const { data } = await api.get<AnalyticsSummary>('/analytics/summary');
    return data;
  },
  getDashboardReadings: async (limit = 10): Promise<SensorReading[]> => {
    const { data } = await api.get<SensorReading[]>('/analytics/dashboard/readings', { params: { limit } });
    return data;
  },
  getDashboardAlerts: async (limit = 10): Promise<Alert[]> => {
    const { data } = await api.get<Alert[]>('/analytics/dashboard/alerts', { params: { limit } });
    return data;
  },
  getDashboardMaintenance: async (limit = 10): Promise<MaintenanceRecord[]> => {
    const { data } = await api.get<MaintenanceRecord[]>('/analytics/dashboard/maintenance', { params: { limit } });
    return data;
  },
  getReport: async (reportType = 'executive'): Promise<string> => {
    const { data } = await api.get<string>(`/analytics/reports/${reportType}`);
    return data;
  },
};

export default api;
