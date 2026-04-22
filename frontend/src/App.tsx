import React, { useState } from 'react';
import AuthPage from './pages/AuthPage';
import UserDashboard from './pages/UserDashboard';
import AdminDashboard from './pages/AdminDashboard';
import LandingPage from './pages/LandingPage';

const App: React.FC = () => {
  const [token, setToken] = useState<string | null>(localStorage.getItem('mlsuite_token'));
  const [role, setRole] = useState<string | null>(localStorage.getItem('mlsuite_role'));
  const [showAuth, setShowAuth] = useState(false);

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
    setShowAuth(false);
  };

  return (
    <div className="min-h-screen bg-nebula-background text-nebula-on_surface font-sans selection:bg-nebula-primary/30">
      {!token ? (
        showAuth ? (
          <AuthPage onLogin={handleLogin} />
        ) : (
          <LandingPage onGetStarted={() => setShowAuth(true)} />
        )
      ) : role === 'admin' ? (
        <AdminDashboard token={token} onLogout={handleLogout} />
      ) : (
        <UserDashboard token={token} onLogout={handleLogout} />
      )}
    </div>
  );
};

export default App;
