import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Cpu, Eye, EyeOff } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

export default function LoginPage() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);
    try {
      await login(username, password);
      navigate('/dashboard');
    } catch {
      setError('Invalid username or password');
    } finally {
      setLoading(false);
    }
  };

  const quickLogin = (user: string, pass: string) => {
    setUsername(user);
    setPassword(pass);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-industrial-900 relative overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-industrial-accent/10 via-industrial-900 to-industrial-900" />
      <div className="relative w-full max-w-md mx-4">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-industrial-accent/20 mb-4">
            <Cpu className="w-8 h-8 text-industrial-accent" />
          </div>
          <h1 className="text-2xl font-bold text-white">IndustrialAI</h1>
          <p className="text-gray-400 mt-1">Smart Predictive Maintenance System</p>
        </div>

        <form onSubmit={handleSubmit} className="card space-y-4">
          {error && (
            <div className="bg-status-critical/10 border border-status-critical/30 text-status-critical text-sm px-4 py-2 rounded-lg">
              {error}
            </div>
          )}
          <div>
            <label className="block text-sm text-gray-400 mb-1.5">Username</label>
            <input
              type="text"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="input-field"
              placeholder="Enter username"
              required
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1.5">Password</label>
            <div className="relative">
              <input
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="input-field pr-10"
                placeholder="Enter password"
                required
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-gray-500"
              >
                {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
              </button>
            </div>
          </div>
          <button type="submit" disabled={loading} className="btn-primary w-full py-3 disabled:opacity-50">
            {loading ? 'Signing in...' : 'Sign In'}
          </button>
        </form>

        <div className="mt-6 card">
          <p className="text-xs text-gray-500 mb-3">Demo Accounts (click to fill):</p>
          <div className="space-y-2 text-xs">
            {[
              { user: 'admin', pass: 'admin123', role: 'Admin' },
              { user: 'manager', pass: 'manager123', role: 'Factory Manager' },
              { user: 'technician', pass: 'tech123', role: 'Technician' },
            ].map(({ user, pass, role }) => (
              <button
                key={user}
                onClick={() => quickLogin(user, pass)}
                className="w-full text-left px-3 py-2 rounded-lg bg-industrial-700/50 hover:bg-industrial-700 text-gray-300 transition-colors"
              >
                <span className="font-medium">{role}</span>
                <span className="text-gray-500 ml-2">{user} / {pass}</span>
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
