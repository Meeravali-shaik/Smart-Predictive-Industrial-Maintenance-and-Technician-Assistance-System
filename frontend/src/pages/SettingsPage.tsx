import Layout from '../components/Layout';
import { useAuth } from '../contexts/AuthContext';

export default function SettingsPage() {
  const { user } = useAuth();

  return (
    <Layout title="Settings" subtitle="Application configuration">
      <div className="max-w-2xl space-y-6">
        <div className="card">
          <h3 className="text-sm font-medium text-gray-300 mb-4">Account Settings</h3>
          <div className="space-y-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Display Name</label>
              <input type="text" defaultValue={user?.full_name} className="input-field" readOnly />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Email</label>
              <input type="email" defaultValue={user?.email} className="input-field" readOnly />
            </div>
          </div>
        </div>

        <div className="card">
          <h3 className="text-sm font-medium text-gray-300 mb-4">System Information</h3>
          <dl className="space-y-3 text-sm">
            <div className="flex justify-between">
              <dt className="text-gray-500">Platform</dt>
              <dd className="text-gray-200">IndustrialAI v1.0.0</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Sensor Mode</dt>
              <dd className="text-status-healthy">Simulated (5s interval)</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">Prediction Engine</dt>
              <dd className="text-gray-200">Rule-Based (Phase 1)</dd>
            </div>
            <div className="flex justify-between">
              <dt className="text-gray-500">API Documentation</dt>
              <dd>
                <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer" className="text-industrial-accent hover:underline">
                  Swagger UI
                </a>
              </dd>
            </div>
          </dl>
        </div>
      </div>
    </Layout>
  );
}
