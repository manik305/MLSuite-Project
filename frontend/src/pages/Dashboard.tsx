import React, { useState, useEffect } from 'react';

const Dashboard: React.FC<{ token: string; onLogout: () => void }> = ({ token, onLogout }) => {
  const [step, setStep] = useState(1);
  const [file, setFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');
  
  // Data Source State
  const [dataSource, setDataSource] = useState('file'); // 'file', 'sql', 'mongodb'
  const [sqlConfig, setSqlConfig] = useState({ connection_string: '', table_name: '' });
  const [mongoConfig, setMongoConfig] = useState({ connection_uri: '', db_name: '', collection_name: '' });

  // Data Analysis State
  const [analysis, setAnalysis] = useState<any>(null);
  const [availableColumns, setAvailableColumns] = useState<string[]>([]);
  
  // Configuration State
  const [taskType, setTaskType] = useState('classification');
  const [targetColumn, setTargetColumn] = useState('');
  const [availableModels, setAvailableModels] = useState<string[]>([]);
  const [selectedModel, setSelectedModel] = useState('');
  const [tune, setTune] = useState(false);
  
  // Results State
  const [results, setResults] = useState<any>(null);

  // Fetch models whenever taskType changes
  useEffect(() => {
    if (step >= 3) {
      fetchModels();
    }
  }, [taskType, step]);

  const fetchModels = async () => {
    try {
      const response = await fetch(`http://localhost:8001/models?task_type=${taskType}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await response.json();
      setAvailableModels(data.models);
      if (data.models.length > 0) setSelectedModel(data.models[0]);
    } catch (err) {
      console.error("Failed to fetch models", err);
    }
  };

  const handleAnalyze = async () => {
    setLoading(true);
    try {
      let queryParams = new URLSearchParams({ data_source: dataSource });

      if (dataSource === 'file') {
        if (!file) {
          setMessage('Please select a file first.');
          setLoading(false);
          return;
        }
        // First upload the file
        const formData = new FormData();
        formData.append('file', file);
        const uploadRes = await fetch('http://localhost:8001/upload', {
          method: 'POST',
          headers: { 'Authorization': `Bearer ${token}` },
          body: formData,
        });
        if (!uploadRes.ok) throw new Error("Upload failed");
        queryParams.append('filename', file.name);
      } else if (dataSource === 'sql') {
        queryParams.append('connection_string', sqlConfig.connection_string);
        queryParams.append('table_name', sqlConfig.table_name);
      } else if (dataSource === 'mongodb') {
        queryParams.append('connection_uri', mongoConfig.connection_uri);
        queryParams.append('db_name', mongoConfig.db_name);
        queryParams.append('collection_name', mongoConfig.collection_name);
      }
      
      // Immediate Analysis (EDI)
      const analyzeRes = await fetch(`http://localhost:8001/analyze?${queryParams.toString()}`, {
        headers: { 'Authorization': `Bearer ${token}` }
      });
      const data = await analyzeRes.json();
      if (!analyzeRes.ok) throw new Error(data.detail);
      
      setAnalysis(data);
      setAvailableColumns(data.columns);
      if (data.columns.length > 0) setTargetColumn(data.columns[data.columns.length - 1]);
      
      setStep(2); // Move to Discovery phase
      setMessage('Intelligence Discovery Complete');
    } catch (err: any) {
      setMessage('Error: ' + err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleTrain = async () => {
    if (!targetColumn) return;
    setLoading(true);
    try {
        let queryParams = new URLSearchParams({
            task_type: taskType,
            target_column: targetColumn,
            model_name: tune ? 'auto' : selectedModel,
            tune: tune.toString(),
            data_source: dataSource
        });

        if (dataSource === 'file') {
            queryParams.append('filename', file?.name || '');
        } else if (dataSource === 'sql') {
            queryParams.append('connection_string', sqlConfig.connection_string);
            queryParams.append('table_name', sqlConfig.table_name);
        } else if (dataSource === 'mongodb') {
            queryParams.append('connection_uri', mongoConfig.connection_uri);
            queryParams.append('db_name', mongoConfig.db_name);
            queryParams.append('collection_name', mongoConfig.collection_name);
        }

        const response = await fetch(`http://localhost:8001/train?${queryParams.toString()}`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}` }
        });
        const data = await response.json();
        if (!response.ok) throw new Error(data.detail);
        setResults(data);
        setStep(4); // Move to Results phase
    } catch (err: any) {
        alert('Training failed: ' + err.message);
    } finally {
        setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-nebula-background flex flex-col font-sans text-nebula-on_surface selection:bg-nebula-primary/30 overflow-hidden">
      
      {/* Absolute Background Elements */}
      <div className="absolute top-0 right-0 w-[60vw] h-[60vw] bg-nebula-primary/5 blur-[150px] rounded-full pointer-events-none z-0"></div>

      {/* Header */}
      <header className="bg-nebula-surface_container px-12 py-6 flex justify-between items-center z-50 relative shadow-2xl">
        <div className="flex items-center gap-6">
          <div className="w-12 h-12 bg-gradient-to-br from-nebula-primary to-nebula-primary_container rounded-lg flex items-center justify-center text-nebula-on_primary font-bold shadow-[0_0_20px_rgba(195,245,255,0.4)]">
            <span className="text-xl">M</span>
          </div>
          <div>
            <h1 className="text-2xl font-display font-medium text-nebula-on_surface tracking-tighter uppercase">MLSUITE / CORE</h1>
            <p className="text-[10px] font-mono text-nebula-primary tracking-[0.2em] font-bold mt-1 opacity-80 uppercase">Step {step}: {step === 1 ? 'Injection' : step === 2 ? 'Discovery' : step === 3 ? 'Refinement' : 'Intelligence'}</p>
          </div>
        </div>
        <div className="flex items-center gap-8">
          <button onClick={onLogout} className="btn-secondary text-[10px] uppercase font-bold tracking-[0.2em] px-4 py-2 border-nebula-outline/10 hover:text-nebula-error">
            Terminate Session
          </button>
        </div>
      </header>

      <main className="flex-1 flex flex-col items-center justify-start overflow-y-auto custom-scrollbar p-10 relative z-10">
        
        {/* Loading Overlay */}
        {loading && (
          <div className="fixed inset-0 bg-nebula-background/90 backdrop-blur-xl z-[100] flex flex-col items-center justify-center space-y-8">
            <div className="relative w-24 h-24">
              <div className="absolute inset-0 rounded-full border-[1.5px] border-nebula-primary/20"></div>
              <div className="absolute inset-0 rounded-full border-t-[1.5px] border-nebula-primary animate-spin shadow-[0_0_30px_rgba(195,245,255,0.4)]"></div>
            </div>
            <p className="text-sm font-mono font-bold text-nebula-primary uppercase tracking-[0.6em] animate-pulse">Synchronizing_Neural_Latencies</p>
          </div>
        )}

        {/* Step 1: Upload / Connect (Injection) */}
        {step === 1 && (
          <div className="w-full max-w-2xl space-y-12 py-10 animate-fade-in">
            <div className="text-center space-y-4">
              <h2 className="text-6xl font-display font-medium tracking-tightest leading-tight">Data <span className="italic opacity-40">Injection.</span></h2>
              <p className="text-nebula-on_surface_variant text-lg opacity-70">Initialize the intelligence cycle by selecting your data source.</p>
            </div>

            <div className="flex gap-4 justify-center">
                {['file', 'sql', 'mongodb'].map((type) => (
                    <button 
                        key={type} 
                        onClick={() => setDataSource(type)} 
                        className={`px-6 py-2 rounded-lg text-[10px] font-mono font-bold uppercase tracking-widest transition-all ${dataSource === type ? 'bg-nebula-primary text-nebula-on_primary shadow-lg' : 'bg-nebula-surface_container text-nebula-on_surface_variant border border-white/5'}`}
                    >
                        {type === 'mongodb' ? 'NoSQL (Mongo)' : type.toUpperCase()}
                    </button>
                ))}
            </div>

            <div className="bg-nebula-surface_container_lowest p-8 rounded-2xl border border-white/5 shadow-2xl space-y-8">
              {dataSource === 'file' && (
                <div className="bg-nebula-surface_container/30 rounded-xl p-12 text-center hover:bg-nebula-surface_container/50 transition-all cursor-pointer group relative overflow-hidden border-2 border-dashed border-nebula-outline/20">
                    <input type="file" onChange={(e) => setFile(e.target.files?.[0] || null)} className="hidden" id="file-upload" />
                    <label htmlFor="file-upload" className="cursor-pointer block space-y-6">
                    <div className="w-16 h-16 bg-nebula-surface_container_highest text-nebula-primary rounded-full flex items-center justify-center mx-auto group-hover:scale-110 transition-transform duration-500">
                        <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
                    </div>
                    <div>
                        <p className="text-lg font-bold text-nebula-on_surface tracking-tight">{file ? file.name : "Select Matrix File"}</p>
                        <p className="text-[9px] text-nebula-outline uppercase tracking-[0.3em] font-mono mt-2">CSV / EXCEL DATA SOURCES</p>
                    </div>
                    </label>
                </div>
              )}

              {dataSource === 'sql' && (
                <div className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest">Connection String (Path/URL)</label>
                        <input 
                            type="text" 
                            placeholder="e.g. data/my_db.sqlite" 
                            value={sqlConfig.connection_string}
                            onChange={(e) => setSqlConfig({...sqlConfig, connection_string: e.target.value})}
                            className="input-nebula w-full" 
                        />
                    </div>
                    <div className="space-y-2">
                        <label className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest">Table Name</label>
                        <input 
                            type="text" 
                            placeholder="e.g. predictions_table" 
                            value={sqlConfig.table_name}
                            onChange={(e) => setSqlConfig({...sqlConfig, table_name: e.target.value})}
                            className="input-nebula w-full" 
                        />
                    </div>
                </div>
              )}

              {dataSource === 'mongodb' && (
                <div className="space-y-6">
                    <div className="space-y-2">
                        <label className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest">Connection URI</label>
                        <input 
                            type="text" 
                            placeholder="mongodb://localhost:27017" 
                            value={mongoConfig.connection_uri}
                            onChange={(e) => setMongoConfig({...mongoConfig, connection_uri: e.target.value})}
                            className="input-nebula w-full" 
                        />
                    </div>
                    <div className="grid grid-cols-2 gap-4">
                        <div className="space-y-2">
                            <label className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest">Database</label>
                            <input 
                                type="text" 
                                placeholder="ml_db" 
                                value={mongoConfig.db_name}
                                onChange={(e) => setMongoConfig({...mongoConfig, db_name: e.target.value})}
                                className="input-nebula w-full" 
                            />
                        </div>
                        <div className="space-y-2">
                            <label className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest">Collection</label>
                            <input 
                                type="text" 
                                placeholder="users_data" 
                                value={mongoConfig.collection_name}
                                onChange={(e) => setMongoConfig({...mongoConfig, collection_name: e.target.value})}
                                className="input-nebula w-full" 
                            />
                        </div>
                    </div>
                </div>
              )}
            </div>

            <button onClick={handleAnalyze} className="w-full bg-nebula-primary text-nebula-on_primary rounded-xl font-mono font-bold text-[12px] tracking-[0.5em] py-6 hover:bg-nebula-primary_fixed transition-all duration-500 shadow-[0_20px_40px_rgba(195,245,255,0.2)] uppercase">
                Initialize Intelligence Discovery
            </button>
            
            {message && <p className="text-[10px] font-mono font-bold text-nebula-primary text-center uppercase tracking-widest">{message}</p>}
          </div>
        )}

        {/* Step 2: Discovery Phase (EDA & Stats) */}
        {step === 2 && analysis && (
          <div className="w-full max-w-7xl space-y-20 animate-fade-in py-10">
            <div className="flex justify-between items-end">
              <div className="space-y-2">
                <p className="text-[10px] font-mono font-bold text-nebula-primary uppercase tracking-[0.5em]">Phase 02 // Discovery</p>
                <h2 className="text-5xl font-display font-medium tracking-tight">Intelligence <span className="opacity-40 italic">Telemetry.</span></h2>
              </div>
              <button onClick={() => setStep(3)} className="px-10 py-4 bg-white/5 border border-white/10 rounded-lg text-[10px] font-mono font-bold uppercase tracking-[0.4em] hover:bg-nebula-primary hover:text-nebula-on_primary transition-all shadow-xl">
                Proceed to Refinement
              </button>
            </div>

            {/* Stats DNA Section */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
              <div className="bg-nebula-surface_container p-8 rounded-2xl border border-white/5 space-y-4 relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-24 h-24 bg-nebula-primary/10 blur-3xl -mr-12 -mt-12 group-hover:scale-150 transition-transform duration-1000"></div>
                <p className="text-[10px] font-mono text-nebula-outline uppercase tracking-widest">Numerical Entries</p>
                <p className="text-5xl font-display font-medium text-nebula-on_surface tracking-tighter">{analysis.stats.numerical_entries.toLocaleString()}</p>
                <div className="h-[2px] w-full bg-nebula-primary/20 relative rounded-full overflow-hidden">
                    <div className="absolute inset-0 bg-nebula-primary shadow-[0_0_10px_#c3f5ff] animate-pulse"></div>
                </div>
              </div>
              <div className="bg-nebula-surface_container p-8 rounded-2xl border border-white/5 space-y-4 relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-24 h-24 bg-nebula-primary/10 blur-3xl -mr-12 -mt-12 group-hover:scale-150 transition-transform duration-1000"></div>
                <p className="text-[10px] font-mono text-nebula-outline uppercase tracking-widest">Character Count</p>
                <p className="text-5xl font-display font-medium text-nebula-on_surface tracking-tighter">{analysis.stats.character_count.toLocaleString()}</p>
                <div className="h-[2px] w-full bg-nebula-primary/20 relative rounded-full"></div>
              </div>
              <div className="bg-nebula-surface_container p-8 rounded-2xl border border-white/5 space-y-4 relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-24 h-24 bg-nebula-primary/10 blur-3xl -mr-12 -mt-12 group-hover:scale-150 transition-transform duration-1000"></div>
                <p className="text-[10px] font-mono text-nebula-outline uppercase tracking-widest">Numerical Features</p>
                <p className="text-5xl font-display font-medium text-nebula-on_surface tracking-tighter">{analysis.stats.num_features}</p>
              </div>
              <div className="bg-nebula-surface_container p-8 rounded-2xl border border-white/5 space-y-4 relative overflow-hidden group">
                <div className="absolute top-0 right-0 w-24 h-24 bg-nebula-primary/10 blur-3xl -mr-12 -mt-12 group-hover:scale-150 transition-transform duration-1000"></div>
                <p className="text-[10px] font-mono text-nebula-outline uppercase tracking-widest">Categorical Features</p>
                <p className="text-5xl font-display font-medium text-nebula-on_surface tracking-tighter">{analysis.stats.cat_features}</p>
              </div>
            </div>

            {/* Graphs Display */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
              {analysis.plots.map((plot: string) => (
                <div key={plot} className="group relative overflow-hidden bg-nebula-surface_container rounded-xl transition-all duration-700 hover:-translate-y-2 border border-white/5">
                  <div className="p-5 flex justify-between items-center bg-nebula-surface_container_high bg-opacity-50">
                      <span className="text-[9px] font-mono font-bold text-nebula-outline uppercase tracking-[0.3em]">{plot.split('_')[0]} Spectral Plot</span>
                      <div onClick={() => window.open(`http://localhost:8001/static/plots/${plot}`, '_blank')} className="w-8 h-8 rounded-lg bg-nebula-surface_container_lowest flex items-center justify-center text-nebula-outline hover:text-nebula-primary transition-all">
                          <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" /></svg>
                      </div>
                  </div>
                  <div className="p-4 bg-[#0b1323]">
                    <img src={`http://localhost:8001/static/plots/${plot}?t=${Date.now()}`} alt="EDA" className="w-full h-auto rounded" />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Step 3: Configuration (Refinement) */}
        {step === 3 && (
          <div className="w-full max-w-4xl space-y-16 py-10 animate-fade-in">
            <div className="text-center space-y-4">
              <p className="text-[10px] font-mono font-bold text-nebula-primary uppercase tracking-[0.5em]">Phase 03 // Refinement</p>
              <h2 className="text-6xl font-display font-medium tracking-tight leading-tight">Neural <span className="opacity-40 italic">Mapping.</span></h2>
              <p className="text-nebula-on_surface_variant text-lg opacity-70">Define the architectural parameters for the prediction model.</p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
              <div className="bg-nebula-surface_container_lowest p-10 rounded-2xl border border-white/5 space-y-10 shadow-2xl">
                <div className="space-y-8">
                  <div>
                    <label className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest mb-4 block">Architectural Task</label>
                    <div className="flex gap-2 p-1 bg-nebula-surface_container_low rounded-lg">
                      {['classification', 'regression'].map((type) => (
                        <button key={type} onClick={() => setTaskType(type)} className={`flex-1 py-4 rounded text-[10px] font-mono font-bold uppercase tracking-widest transition-all ${taskType === type ? 'bg-nebula-primary text-nebula-on_primary shadow-lg' : 'text-nebula-on_surface_variant'}`}>{type}</button>
                      ))}
                    </div>
                  </div>

                  <div>
                    <label className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest mb-4 block">Target Dimension</label>
                    <select value={targetColumn} onChange={(e) => setTargetColumn(e.target.value)} className="input-nebula w-full font-mono text-xs">
                      {availableColumns.map(col => <option key={col} value={col}>{col}</option>)}
                    </select>
                  </div>

                  <div>
                    <label className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest mb-4 block">Cognitive Model</label>
                    <div className="relative">
                        <select 
                            disabled={tune}
                            value={selectedModel} 
                            onChange={(e) => setSelectedModel(e.target.value)} 
                            className={`input-nebula w-full font-mono text-xs text-nebula-primary font-bold ${tune ? 'opacity-30' : ''}`}
                        >
                            {availableModels.map(name => <option key={name} value={name}>{name}</option>)}
                        </select>
                        {tune && (
                            <div className="absolute inset-0 flex items-center justify-center bg-transparent pointer-events-none">
                                <span className="text-[9px] font-mono font-bold text-nebula-primary uppercase tracking-[0.3em] bg-nebula-surface_container px-3 py-1 rounded border border-nebula-primary/30">Auto-Selection Active</span>
                            </div>
                        )}
                    </div>
                    <p className="text-[9px] text-nebula-outline font-mono mt-3 uppercase tracking-widest italic font-bold">
                        {tune ? `Comparing all ${taskType} models...` : `Selected for ${taskType} task`}
                    </p>
                  </div>

                  <div className="flex items-center justify-between p-4 bg-nebula-surface_container rounded-xl border border-white/5">
                      <div className="space-y-1">
                          <p className="text-[10px] font-mono font-bold text-nebula-on_surface uppercase tracking-widest">Neural Optimization</p>
                          <p className="text-[8px] text-nebula-outline uppercase">Automated Model Selection & Tuning</p>
                      </div>
                      <button 
                        onClick={() => setTune(!tune)} 
                        className={`w-12 h-6 rounded-full relative transition-all duration-500 ${tune ? 'bg-nebula-primary shadow-[0_0_15px_rgba(195,245,255,0.4)]' : 'bg-nebula-surface_container_highest'}`}
                      >
                          <div className={`absolute top-1 w-4 h-4 rounded-full bg-white transition-all duration-500 shadow-xl ${tune ? 'left-7' : 'left-1'}`}></div>
                      </button>
                  </div>
                </div>

                <div className="pt-6 border-t border-white/5">
                    <button onClick={handleTrain} className="w-full py-6 bg-gradient-to-r from-nebula-primary to-nebula-primary_container text-nebula-on_primary rounded-xl font-mono font-bold text-xs tracking-[0.4em] uppercase shadow-2xl hover:scale-[1.02] transition-all">
                        Execute Neural Assembly
                    </button>
                    <button onClick={() => setStep(2)} className="w-full mt-4 py-3 text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-widest hover:text-nebula-on_surface transition-colors">
                        ← Back to Telemetry
                    </button>
                </div>
              </div>

              {/* Data Summary Card */}
              <div className="space-y-8">
                  <div className="bg-nebula-surface_container p-10 rounded-2xl space-y-6 border border-nebula-primary/10">
                      <h3 className="text-[10px] font-mono font-bold text-nebula-primary uppercase tracking-[0.4em]">Matrix Summary</h3>
                      <div className="space-y-6">
                            <div className="flex justify-between items-center">
                                <p className="text-[11px] text-nebula-outline uppercase tracking-widest">Source Type</p>
                                <p className="text-xs font-mono font-bold text-nebula-on_surface uppercase">{dataSource}</p>
                            </div>
                      </div>
                      <div className="pt-10">
                        <img 
                          src={`http://localhost:8001/static/plots/data_composition_pie.png?t=${Date.now()}`} 
                          alt="Composition" 
                          className="w-full h-auto rounded-lg shadow-inner scale-110 pointer-events-none" 
                        />
                      </div>
                  </div>
              </div>
            </div>
          </div>
        )}

        {/* Step 4: Results (Intelligence) */}
        {step === 4 && results && (
          <div className="w-full max-w-7xl animate-fade-in py-10 space-y-24">
             <div className="text-center space-y-4">
              <p className="text-[10px] font-mono font-bold text-nebula-primary uppercase tracking-[0.5em]">Phase 04 // Result</p>
              <h2 className="text-7xl font-display font-medium tracking-tightest leading-tight">Neural <span className="opacity-40 italic">Convergence.</span></h2>
              <button onClick={() => { setStep(1); setResults(null); }} className="px-6 py-2 bg-white/5 text-[9px] font-mono font-bold uppercase tracking-[0.3em] text-nebula-outline hover:text-nebula-on_surface border border-white/5 rounded mt-4">
                  Initialize New Sequence
              </button>
            </div>

            <div className="grid grid-cols-1 xl:grid-cols-3 gap-12 items-start">
                <div className="xl:col-span-2 space-y-12">
                    {/* Model Leaderboard (if auto-selected) */}
                    {results.is_auto_selected && results.tuning_result && (
                        <div className="bg-nebula-surface_container_lowest p-10 rounded-3xl border border-nebula-primary/10 space-y-8 shadow-2xl relative overflow-hidden">
                             <div className="absolute top-0 right-0 w-32 h-32 bg-nebula-primary/10 blur-[80px] -mr-16 -mt-16"></div>
                             <h4 className="text-[10px] font-mono font-bold text-nebula-primary uppercase tracking-[0.4em] relative z-10">Comparative Intelligence Leaderboard</h4>
                             
                             <div className="overflow-x-auto relative z-10">
                                <table className="w-full text-left border-collapse">
                                    <thead>
                                        <tr className="border-b border-white/5">
                                            <th className="py-4 text-[9px] font-mono text-nebula-outline uppercase tracking-widest">Model Candidate</th>
                                            <th className="py-4 text-[9px] font-mono text-nebula-outline uppercase tracking-widest text-center">Prediction Score</th>
                                            <th className="py-4 text-[9px] font-mono text-nebula-outline uppercase tracking-widest text-center">Error Rate</th>
                                            <th className="py-4 text-[9px] font-mono text-nebula-outline uppercase tracking-widest text-right">Status</th>
                                        </tr>
                                    </thead>
                                    <tbody className="divide-y divide-white/5">
                                        {results.tuning_result.leaderboard.map((item: any, idx: number) => (
                                            <tr key={item.model_name} className={`group ${item.is_winner ? 'bg-nebula-primary/5' : ''}`}>
                                                <td className="py-6">
                                                    <div className="flex items-center gap-4">
                                                        <span className="text-[10px] font-mono font-bold text-nebula-outline opacity-40">0{idx + 1}</span>
                                                        <p className={`text-sm font-display font-medium ${item.is_winner ? 'text-nebula-primary' : 'text-nebula-on_surface'}`}>{item.model_name}</p>
                                                    </div>
                                                </td>
                                                <td className="py-6 text-center">
                                                    <p className={`text-xl font-mono font-bold ${item.is_winner ? 'text-nebula-primary' : 'text-nebula-on_surface'}`}>{item.score}</p>
                                                    <p className="text-[8px] font-mono text-nebula-outline uppercase tracking-tighter">{item.metric_name}</p>
                                                </td>
                                                <td className="py-6 text-center">
                                                    <p className="text-xl font-mono text-nebula-outline/50">{item.error_rate}</p>
                                                </td>
                                                <td className="py-6 text-right">
                                                    {item.is_winner ? (
                                                        <span className="px-3 py-1 bg-nebula-primary text-nebula-on_primary text-[8px] font-mono font-bold uppercase tracking-widest rounded-full shadow-[0_0_15px_rgba(195,245,255,0.4)]">Winner / Best Fit</span>
                                                    ) : (
                                                        <span className="text-[8px] font-mono text-nebula-outline uppercase tracking-widest opacity-40">Defeated</span>
                                                    )}
                                                </td>
                                            </tr>
                                        ))}
                                    </tbody>
                                </table>
                             </div>
                        </div>
                    )}

                    <div className="bg-nebula-surface_container p-16 rounded-3xl relative overflow-hidden group border border-nebula-primary/10">
                        <div className="absolute top-0 right-0 w-full h-full bg-gradient-to-l from-nebula-primary/5 to-transparent blur-3xl pointer-events-none group-hover:from-nebula-primary/10 transition-all duration-1000"></div>
                        <div className="relative z-10 space-y-12">
                             <div>
                                <p className="text-[10px] font-mono font-bold text-nebula-primary uppercase tracking-[0.4em] mb-4">Dominant Neural Kernel</p>
                                <h4 className="text-8xl font-display font-medium text-nebula-on_surface tracking-tightest">
                                    {Object.keys(results.results)[0]}
                                </h4>
                            </div>
                            
                            <div className="grid grid-cols-2 lg:grid-cols-3 gap-10">
                                {Object.entries(results.results[Object.keys(results.results)[0]]).map(([k, v]: [string, any]) => (
                                    <div key={k} className="space-y-4 group/item">
                                        <p className="text-[10px] font-mono text-nebula-outline uppercase tracking-[0.3em] font-bold group-hover/item:text-nebula-primary transition-colors">{k}</p>
                                        <p className="text-5xl font-display font-medium text-nebula-on_surface tracking-tight">{(v as number).toFixed(4)}</p>
                                        <div className="h-[2px] w-full bg-nebula-surface_container_highest relative overflow-hidden rounded-full">
                                            <div className="absolute h-full bg-nebula-primary shadow-[0_0_10px_rgba(195,245,255,0.8)] transition-all duration-1000 ease-out" style={{ width: `${Math.min(100, (v as number) * 100)}%` }}></div>
                                        </div>
                                    </div>
                                ))}
                            </div>

                             {results.model_url && (
                                <div className="pt-12 flex justify-between items-center border-t border-white/5">
                                    <p className="text-[9px] font-mono text-nebula-outline uppercase tracking-widest italic opacity-50">Weights exported to kernel vault.</p>
                                    <a href={`http://localhost:8001${results.model_url}`} download className="px-8 py-4 bg-nebula-primary text-nebula-on_primary rounded-lg font-mono text-[10px] font-bold uppercase tracking-widest shadow-2xl transition-all hover:scale-105 active:scale-95">Download Model (.pkl)</a>
                                </div>
                            )}
                        </div>
                    </div>
                </div>

                <div className="space-y-8">
                     <h3 className="text-[10px] font-mono font-bold text-nebula-outline uppercase tracking-[0.4em]">Visual Performance DNA</h3>
                     <div className="grid grid-cols-1 gap-10">
                        {results.performance_plots.map((plot: string) => (
                           <div key={plot} className="bg-nebula-surface_container p-4 rounded-2xl border border-white/5 group overflow-hidden">
                              <p className="text-[9px] font-mono font-bold text-nebula-outline uppercase tracking-widest mb-4 opacity-70 group-hover:opacity-100 transition-opacity">Visual Metrics: {plot.split('model_')[1].replace('.png', '').replace('_', ' ')}</p>
                              <img src={`http://localhost:8001/static/plots/${plot}?t=${Date.now()}`} alt="Performance" className="w-full h-auto rounded-lg shadow-2xl group-hover:scale-110 transition-transform duration-1000" />
                           </div>
                        ))}
                     </div>
                </div>
            </div>
          </div>
        )}

      </main>
    </div>
  );
};

export default Dashboard;
