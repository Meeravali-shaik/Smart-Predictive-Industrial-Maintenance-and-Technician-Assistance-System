import { useNavigate } from 'react-router-dom';
import { Home } from 'lucide-react';

export default function NotFoundPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex items-center justify-center bg-industrial-900">
      <div className="text-center">
        <h1 className="text-8xl font-bold text-industrial-accent/30">404</h1>
        <p className="text-xl text-gray-300 mt-4">Page not found</p>
        <p className="text-gray-500 mt-2">The page you're looking for doesn't exist.</p>
        <button onClick={() => navigate('/dashboard')} className="btn-primary mt-6 inline-flex items-center gap-2">
          <Home className="w-4 h-4" /> Back to Dashboard
        </button>
      </div>
    </div>
  );
}
