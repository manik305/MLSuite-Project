import React, { useEffect, useState } from 'react';

const LandingPage: React.FC<{ onGetStarted: () => void }> = ({ onGetStarted }) => {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => setScrollY(window.scrollY);
    window.addEventListener('scroll', handleScroll, { passive: true });
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <div className="min-h-screen w-full bg-nebula-background text-nebula-on_surface font-sans selection:bg-nebula-primary/30 overflow-x-hidden">
      {/* Background Ambience */}
      <div 
        className="fixed top-[-20%] left-[10%] w-[80vw] h-[80vw] rounded-full pointer-events-none transition-transform duration-1000"
        style={{
          background: 'radial-gradient(circle, rgba(0, 229, 255, 0.08) 0%, rgba(0, 54, 61, 0) 70%)',
          transform: `translateY(${scrollY * 0.2}px)`,
        }}
      />
      
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50 transition-all duration-300 backdrop-blur-xl bg-nebula-background/70 border-b border-nebula-outline_variant/10 px-6 py-4 flex justify-between items-center">
        <div className="text-xl font-display font-bold tracking-tight text-white flex items-center gap-2">
          <div className="w-6 h-6 rounded-full bg-gradient-to-tr from-nebula-primary to-blue-500 shadow-[0_0_15px_rgba(0,229,255,0.5)]"></div>
          MLSUITE<span className="text-nebula-primary">.</span>
        </div>
        <button onClick={onGetStarted} className="bg-white text-black px-5 py-2 rounded-full font-semibold text-sm hover:scale-105 transition-transform">
          Sign In
        </button>
      </nav>

      <main className="pt-32 pb-24 px-6 md:px-12 max-w-7xl mx-auto relative z-10 w-full">
        
        {/* Hero Section */}
        <section className="min-h-[80vh] flex flex-col items-center justify-center text-center">
          <h2 className="text-nebula-primary font-mono text-sm tracking-[0.3em] uppercase mb-6 animate-fade-in">
            Introducing the future of ML
          </h2>
          <h1 className="text-6xl md:text-8xl lg:text-[7rem] font-display font-medium tracking-tighter leading-[1.1] mb-8">
            <span className="block text-white pb-2">Intelligence,</span>
            <span className="block bg-gradient-to-r from-cyan-300 via-blue-400 to-indigo-400 text-transparent bg-clip-text">
              orchestrated.
            </span>
          </h1>
          <p className="text-xl md:text-2xl text-nebula-on_surface_variant max-w-3xl font-light leading-relaxed mb-12">
            A radically powerful end-to-end machine learning pipeline. Ingest data, automate preprocessing, and deploy the optimal model—all engineered into one beautifully seamless experience.
          </p>
          <div className="flex gap-6">
            <button onClick={onGetStarted} className="bg-nebula-primary text-black px-8 py-4 rounded-full font-semibold text-lg hover:bg-white hover:scale-105 transition-all shadow-[0_0_30px_rgba(0,229,255,0.3)]">
              Get Started
            </button>
            <button className="text-white px-8 py-4 rounded-full font-semibold text-lg hover:bg-nebula-surface_variant transition-all flex items-center gap-2">
              Watch the film <span className="text-nebula-primary text-xl">▸</span>
            </button>
          </div>
        </section>

        {/* Graphical Statistical Analysis Section */}
        <section className="py-24">
          <div className="glass-panel p-1 rounded-3xl border border-nebula-outline_variant/30 overflow-hidden relative group">
            <div className="p-8 md:p-16 bg-gradient-to-br from-[#0a1120] to-[#040812] rounded-[22px] relative overflow-hidden">
              <div className="absolute top-0 right-0 w-full h-[500px] bg-[url('data:image/svg+xml;base64,PHN2ZyB4bWxucz0naHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmcnIHdpZHRoPSc0MCcgaGVpZ2h0PSc0MCc+PGRpdiBzdHlsZT0nd2lkdGg6MTAwJTtoZWlnaHQ6MTAwJTtiYWNrZ3JvdW5kLWltYWdlOmxpbmVhci1ncmFkaWVudCgjMTMxYzJiIDFweCwgIzBiMTMyMyAxcHgpLCBsaW5lYXItZ3JhZGllbnQoOTBkZWcsICMxMzFjMmIgMXB4LCAjMGIxMzIzIDFweCk7YmFja2dyb3VuZC1zaXplOjUwcHggNTBweDsnLz48L3N2Zz4=')] opacity-20 mask-image:linear-gradient(to_bottom,white,transparent)"></div>
              
              <div className="relative z-10 flex flex-col md:flex-row items-center gap-16">
                <div className="flex-1 space-y-6">
                  <h3 className="text-4xl md:text-5xl font-display font-medium text-white leading-tight">
                    Stats that speak <br/><span className="text-nebula-primary">volumes.</span>
                  </h3>
                  <p className="text-xl text-nebula-on_surface_variant font-light">
                    Deep dive into your dataset with real-time analytics. Our dynamic graphical entry point maps out feature correlations, null distributions, and out-of-bounds metrics instantly.
                  </p>
                  
                  <div className="grid grid-cols-2 gap-8 pt-8">
                    <div>
                      <div className="text-5xl font-display font-bold text-white mb-2">99<span className="text-nebula-primary">%</span></div>
                      <div className="text-sm text-nebula-on_surface_variant tracking-wider uppercase font-mono">Accuracy Rate</div>
                    </div>
                    <div>
                      <div className="text-5xl font-display font-bold text-white mb-2">10<span className="text-nebula-primary">x</span></div>
                      <div className="text-sm text-nebula-on_surface_variant tracking-wider uppercase font-mono">Faster Training</div>
                    </div>
                  </div>
                </div>

                {/* Simulated Chart Graphic */}
                <div className="flex-1 w-full h-[400px] bg-nebula-surface_container_lowest rounded-2xl border border-nebula-outline_variant/30 flex items-end p-8 gap-4 relative">
                  <div className="absolute top-6 left-6 text-nebula-on_surface_variant font-mono text-sm">Model Convergence (Loss)</div>
                  {[40, 70, 55, 90, 65, 100, 85].map((height, i) => (
                    <div key={i} className="flex-1 bg-gradient-to-t from-blue-600 to-cyan-300 rounded-t-lg relative group overflow-hidden" style={{ height: `${height}%` }}>
                      <div className="absolute inset-0 bg-white/20 opacity-0 group-hover:opacity-100 transition-opacity"></div>
                    </div>
                  ))}
                  {/* Floating tooltip simulation */}
                  <div className="absolute top-1/4 right-1/4 bg-white text-black px-4 py-2 rounded-lg font-mono text-sm shadow-[0_10px_20px_rgba(0,0,0,0.5)] transform rotate-[-5deg] animate-pulse">
                    Epoch 42: Validated
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* B2B Feature Grid (Apple Style Tiles) */}
        <section className="py-24">
          <h2 className="text-center text-4xl md:text-6xl font-display font-medium text-white mb-16">
            Everything you need. <br/><span className="text-nebula-on_surface_variant">Nothing you don't.</span>
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            
            <div className="glass-panel p-10 rounded-3xl flex flex-col justify-between min-h-[400px] border border-nebula-outline_variant/20 hover:border-nebula-primary/40 transition-colors">
              <div>
                <h3 className="text-3xl font-display text-white mb-4">Painless Injection</h3>
                <p className="text-nebula-on_surface_variant text-lg leading-relaxed">
                  Upload CSVs seamlessly. Our engine automatically detects schemas and aligns data types so you can skip the boilerplate.
                </p>
              </div>
              <div className="w-full h-32 mt-8 rounded-xl bg-gradient-to-r from-nebula-surface_container to-nebula-background flex items-center justify-center border border-nebula-outline_variant/10">
                 <div className="w-16 h-16 rounded-full bg-nebula-surface_container_highest flex items-center justify-center animate-bounce">
                    <span className="text-nebula-primary text-2xl">↓</span>
                 </div>
              </div>
            </div>

            <div className="glass-panel p-10 rounded-3xl flex flex-col justify-between min-h-[400px] border border-nebula-outline_variant/20 hover:border-nebula-primary/40 transition-colors">
              <div>
                <h3 className="text-3xl font-display text-white mb-4">Auto Pre-Processing</h3>
                <p className="text-nebula-on_surface_variant text-lg leading-relaxed">
                  Missing values? Categorical strings? Outliers? Handled. MLSuite cleans and scales your data using enterprise-grade algorithms.
                </p>
              </div>
              <div className="flex gap-2 mt-8 flex-wrap">
                 {['Imputation', 'Scaling', 'Encoding', 'PCA', 'SMOTE'].map(tech => (
                   <span key={tech} className="px-4 py-2 rounded-full bg-nebula-surface_container_low text-nebula-primary font-mono text-sm border border-nebula-primary/20">
                     {tech}
                   </span>
                 ))}
              </div>
            </div>

            <div className="md:col-span-2 glass-panel p-10 md:p-16 rounded-3xl border border-nebula-outline_variant/20 relative overflow-hidden group">
              <div className="absolute top-[-50%] right-[-10%] w-[500px] h-[500px] bg-blue-500/10 blur-[100px] rounded-full group-hover:bg-blue-500/20 transition-colors"></div>
              <div className="max-w-xl relative z-10">
                <h3 className="text-4xl md:text-5xl font-display text-white mb-6">Dynamic Model Selection</h3>
                <p className="text-nebula-on_surface_variant text-xl leading-relaxed mb-8">
                  We pit the industry's best models against each other. XGBoost, Random Forest, Logistic Regression. You get the winner.
                </p>
                <div className="flex bg-nebula-surface_container_lowest rounded-full p-2 w-max border border-nebula-outline_variant/20">
                  <div className="px-6 py-2 rounded-full bg-nebula-surface_container text-white font-medium">Training...</div>
                  <div className="px-6 py-2 text-nebula-on_surface_variant font-medium">Validating</div>
                  <div className="px-6 py-2 flex items-center gap-2"><div className="w-2 h-2 rounded-full bg-nebula-primary animate-pulse"></div>Deploying</div>
                </div>
              </div>
            </div>

          </div>
        </section>

      </main>

      {/* Footer CTA */}
      <footer className="w-full border-t border-nebula-outline_variant/20 bg-nebula-surface_container_lowest pt-24 pb-12 text-center text-white relative overflow-hidden">
        <h2 className="text-5xl md:text-7xl font-display font-medium mb-8">Ready to evolve?</h2>
        <button onClick={onGetStarted} className="bg-white text-black px-12 py-5 rounded-full font-bold text-lg hover:scale-105 transition-transform shadow-[0_0_40px_rgba(255,255,255,0.2)] mb-20">
          Enter the Suite
        </button>
        <p className="text-nebula-on_surface_variant/50 text-sm font-mono">
          &copy; 2026 MLSuite Technologies. All neural pathways reserved.
        </p>
      </footer>
    </div>
  );
};

export default LandingPage;
