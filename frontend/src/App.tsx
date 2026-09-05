import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import MachinesPage from './pages/MachinesPage';
import MachineDetailPage from './pages/MachineDetailPage';
import LiveMonitoringPage from './pages/LiveMonitoringPage';
import AlertsPage from './pages/AlertsPage';
import PredictionsPage from './pages/PredictionsPage';
import MaintenancePage from './pages/MaintenancePage';
import TechniciansPage from './pages/TechniciansPage';
import AnalyticsPage from './pages/AnalyticsPage';
import ProfilePage from './pages/ProfilePage';
import SettingsPage from './pages/SettingsPage';
import FactoryTwinPage from './pages/FactoryTwinPage';
import NotFoundPage from './pages/NotFoundPage';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 3000,
    },
  },
});

export default function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route element={<ProtectedRoute />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/machines" element={<MachinesPage />} />
              <Route path="/machines/:id" element={<MachineDetailPage />} />
              <Route path="/monitoring" element={<LiveMonitoringPage />} />
              <Route path="/alerts" element={<AlertsPage />} />
              <Route path="/predictions" element={<PredictionsPage />} />
              <Route path="/maintenance" element={<MaintenancePage />} />
              <Route path="/technicians" element={<TechniciansPage />} />
              <Route path="/analytics" element={<AnalyticsPage />} />
              <Route path="/digital-twin" element={<FactoryTwinPage />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/settings" element={<SettingsPage />} />
            </Route>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </QueryClientProvider>
  );
}
