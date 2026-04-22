import React, { useState } from 'react';
import { API_BASE_URL } from '../api/config';

const AuthPage: React.FC<{ onLogin: (token: string, role: string) => void }> = ({ onLogin }) => {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    const endpoint = isLogin ? '/login' : '/register';
    
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
      });
      
      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || 'Invalid credentials or account mismatch');
      
      if (isLogin) {
        onLogin(data.token, data.role);
      } else {
        setIsLogin(true);
        alert('Account created! Please enter your details to login.');
      }
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen w-full flex items-center justify-center bg-nebula-background relative overflow-hidden font-sans text-nebula-on_surface selection:bg-nebula-primary/30">
      
      {/* Background Ambience - Floating Nebula Nodes */}
      <div className="absolute top-[-15%] right-[-10%] w-[70vw] h-[70vw] bg-nebula-primary/5 blur-[120px] rounded-full pointer-events-none"></div>
      <div className="absolute bottom-[-10%] left-[-15%] w-[50vw] h-[50vw] bg-nebula-primary_container/5 blur-[100px] rounded-full pointer-events-none"></div>

      <div className="relative z-10 w-full max-w-lg p-6 animate-fade-in transition-all duration-700 ease-out">
        <div className="glass-panel p-12 nebula-glow border-none shadow-none">
          <div className="text-left mb-12">
            <h1 className="text-6xl font-display font-medium text-nebula-primary tracking-tighter mb-4 drop-shadow-[0_0_15px_rgba(195,245,255,0.3)]">
              MLSUITE
            </h1>
            <p className="text-nebula-on_surface_variant text-lg font-sans leading-relaxed max-w-[280px]">
              {isLogin ? 'Establish secure connection to neural assets' : 'Initialize operator access to machine learning modules'}
            </p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-8">
            <div className="space-y-6">
              <div className="space-y-2">
                <label className="data-label uppercase ml-1 opacity-60">Authentication Identifier</label>
                <input
                  type="email"
                  required
                  className="input-nebula"
                  placeholder="operator@mlsuite.io"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div className="space-y-2">
                <label className="data-label uppercase ml-1 opacity-60">Security Directive</label>
                <input
                  type="password"
                  required
                  className="input-nebula font-sans"
                  placeholder="••••••••••••"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </div>
            </div>

            {error && (
              <div className="bg-nebula-error_container/10 border-l-[3px] border-nebula-error text-nebula-error p-5 rounded-r-xl text-xs font-mono font-bold uppercase tracking-widest animate-pulse">
                {error}
              </div>
            )}

            <button type="submit" className="w-full btn-primary text-sm tracking-widest uppercase py-5">
              {isLogin ? 'Authenticate Operator' : 'Initialize Protocol'}
            </button>
          </form>

          <footer className="mt-12 text-left pt-8 border-t border-nebula-outline_variant/10">
            <button
              onClick={() => setIsLogin(!isLogin)}
              className="text-nebula-outline hover:text-nebula-primary text-xs font-mono font-bold uppercase tracking-widest transition-all duration-300"
            >
              {isLogin ? "[ PROTOCOL: INITIALIZE NEW ACCESS ]" : '[ PROTOCOL: RETURN TO AUTHENTICATION ]'}
            </button>
          </footer>
        </div>
      </div>
    </div>
  );
};

export default AuthPage;
