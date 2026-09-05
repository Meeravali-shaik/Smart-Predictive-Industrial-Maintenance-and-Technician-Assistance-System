import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Cpu,
  Activity,
  Bell,
  Brain,
  Wrench,
  Users,
  BarChart3,
  Settings,
  Factory,
  ScanSearch,
} from 'lucide-react';
import { cn } from '../utils/helpers';

const navItems = [
  { to: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
  { to: '/machines', icon: Factory, label: 'Machines' },
  { to: '/monitoring', icon: Activity, label: 'Live Monitoring' },
  { to: '/alerts', icon: Bell, label: 'Alerts' },
  { to: '/predictions', icon: Brain, label: 'Predictions' },
  { to: '/maintenance', icon: Wrench, label: 'Maintenance' },
  { to: '/technicians', icon: Users, label: 'Technicians' },
  { to: '/analytics', icon: BarChart3, label: 'Analytics' },
  { to: '/digital-twin', icon: ScanSearch, label: 'Digital Twin' },
  { to: '/settings', icon: Settings, label: 'Settings' },
];

export default function Sidebar() {
  return (
    <aside className="fixed left-0 top-0 h-full w-64 bg-industrial-800 border-r border-industrial-600/30 flex flex-col z-50">
      <div className="p-5 border-b border-industrial-600/30">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-industrial-accent/20 flex items-center justify-center">
            <Cpu className="w-6 h-6 text-industrial-accent" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white">IndustrialAI</h1>
            <p className="text-xs text-gray-500">Predictive Maintenance</p>
          </div>
        </div>
      </div>
      <nav className="flex-1 p-3 space-y-1 overflow-y-auto">
        {navItems.map(({ to, icon: Icon, label }) => (
          <NavLink
            key={to}
            to={to}
            className={({ isActive }) =>
              cn(
                'flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all',
                isActive
                  ? 'bg-industrial-accent/15 text-industrial-accent border border-industrial-accent/30'
                  : 'text-gray-400 hover:text-gray-200 hover:bg-industrial-700/50'
              )
            }
          >
            <Icon className="w-5 h-5" />
            {label}
          </NavLink>
        ))}
      </nav>
      <div className="p-4 border-t border-industrial-600/30">
        <div className="flex items-center gap-2 text-xs text-gray-500">
          <div className="w-2 h-2 rounded-full bg-status-healthy animate-pulse-glow" />
          Simulator Active
        </div>
      </div>
    </aside>
  );
}
