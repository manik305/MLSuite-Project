import React, { useState } from 'react';
import AuthPage from './pages/AuthPage';
import UserDashboard from './pages/UserDashboard';
import AdminDashboard from './pages/AdminDashboard';

const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('mlsuite_token'));
  const [role, setRole] = useState<string | null>(localStorage.getItem('mlsuite_role'));

  const handleLogin = (newToken: string, newRole: string) => {
    localStorage.setItem('mlsuite_token', newToken);
    localStorage.setItem('mlsuite_role', newRole);
    setToken(newToken);
    setRole(newRole);
  };

  const handleLogout = () => {
    localStorage.removeItem('mlsuite_token');
    localStorage.removeItem('mlsuite_role');
    setToken(null);
    setRole(null);
  };

  return (
    <div className="min-h-screen bg-nebula-background text-nebula-on_surface font-sans selection:bg-nebula-primary/30">
      {!token ? (
        <AuthPage onLogin={handleLogin} />
      ) : role === 'admin' ? (
        <AdminDashboard token={token} onLogout={handleLogout} />
      ) : (
        <UserDashboard token={token} onLogout={handleLogout} />
      )}
    </div>
  );
};

export default App;
