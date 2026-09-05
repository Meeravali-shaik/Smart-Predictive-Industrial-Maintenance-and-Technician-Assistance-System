import Layout from '../components/Layout';
import { useAuth } from '../contexts/AuthContext';
import StatusBadge from '../components/StatusBadge';
import { formatDate } from '../utils/helpers';

export default function ProfilePage() {
  const { user } = useAuth();

  if (!user) return null;

  return (
    <Layout title="Profile" subtitle="Your account information">
      <div className="max-w-lg">
        <div className="card">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-16 h-16 rounded-full bg-industrial-accent/20 flex items-center justify-center text-2xl font-bold text-industrial-accent">
              {user.full_name.charAt(0)}
            </div>
            <div>
              <h3 className="text-lg font-semibold text-white">{user.full_name}</h3>
              <p className="text-gray-400">@{user.username}</p>
            </div>
          </div>
          <dl className="space-y-4">
            {[
              ['Email', user.email],
              ['Role', <StatusBadge status={user.role.replace('_', ' ')} />],
              ['Status', user.is_active ? 'Active' : 'Inactive'],
              ['Member Since', formatDate(user.created_at)],
            ].map(([label, value]) => (
              <div key={String(label)} className="flex justify-between py-2 border-b border-industrial-600/20">
                <dt className="text-gray-500 text-sm">{label}</dt>
                <dd className="text-gray-200 text-sm">{value}</dd>
              </div>
            ))}
          </dl>
        </div>
      </div>
    </Layout>
  );
}
