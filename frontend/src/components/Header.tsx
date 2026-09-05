import { Bell, LogOut, User } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

interface HeaderProps {
  title: string;
  subtitle?: string;
}

export default function Header({ title, subtitle }: HeaderProps) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="h-16 bg-industrial-800/80 backdrop-blur-sm border-b border-industrial-600/30 flex items-center justify-between px-6 sticky top-0 z-40">
      <div>
        <h2 className="text-lg font-semibold text-white">{title}</h2>
        {subtitle && <p className="text-xs text-gray-500">{subtitle}</p>}
      </div>
      <div className="flex items-center gap-4">
        <button className="relative p-2 rounded-lg hover:bg-industrial-700/50 transition-colors">
          <Bell className="w-5 h-5 text-gray-400" />
        </button>
        <button
          onClick={() => navigate('/profile')}
          className="flex items-center gap-2 px-3 py-1.5 rounded-lg hover:bg-industrial-700/50 transition-colors"
        >
          <div className="w-8 h-8 rounded-full bg-industrial-accent/20 flex items-center justify-center">
            <User className="w-4 h-4 text-industrial-accent" />
          </div>
          <div className="text-left hidden sm:block">
            <p className="text-sm font-medium text-gray-200">{user?.full_name}</p>
            <p className="text-xs text-gray-500 capitalize">{user?.role?.replace('_', ' ')}</p>
          </div>
        </button>
        <button
          onClick={handleLogout}
          className="p-2 rounded-lg hover:bg-status-critical/10 text-gray-400 hover:text-status-critical transition-colors"
          title="Logout"
        >
          <LogOut className="w-5 h-5" />
        </button>
      </div>
    </header>
  );
}
