import React, { useState, useEffect } from 'react';
import api from './services/api.js';
import AnalysisDashboard from './components/AnalysisDashboard.jsx';

function App() {
  const [matches, setMatches] = useState([]);
  const [selectedMatch, setSelectedMatch] = useState(null);
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadMatches();
  }, []);

  const loadMatches = async () => {
    const data = await api.getMatches('?status=live,finished&per_page=20');
    setMatches(data.data || []);
  };

  const analyze = async (matchId) => {
    setLoading(true);
    setSelectedMatch(matchId);
    const data = await api.getAnalysis(matchId);
    setAnalysis(data);
    setLoading(false);
  };

  return (
    <div style={{ padding: '20px', maxWidth: '1200px', margin: '0 auto' }}>
      <h1 style={{ color: '#38bdf8', marginBottom: '20px' }}>⚽ Football Stats Analyzer</h1>
      <p style={{ color: '#94a3b8', marginBottom: '20px' }}>
        Datos reales de TheStatsAPI + Comparación de cuotas en tiempo real
      </p>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '20px' }}>
        <div>
          <h3 style={{ color: '#cbd5e1' }}>Partidos en vivo / Finalizados</h3>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginTop: '10px' }}>
            {matches.map(m => (
              <button
                key={m.id}
                onClick={() => analyze(m.id)}
                style={{
                  padding: '12px',
                  background: selectedMatch === m.id ? '#0ea5e9' : '#1e293b',
                  border: '1px solid #334155',
                  borderRadius: '8px',
                  color: 'white',
                  cursor: 'pointer',
                  textAlign: 'left'
                }}
              >
                <div style={{ fontWeight: 'bold' }}>{m.home_team.name} vs {m.away_team.name}</div>
                <div style={{ fontSize: '12px', color: '#94a3b8' }}>
                  {m.status === 'live' ? '🔴 EN VIVO' : '✅ Finalizado'} | 
                  {m.score?.home ?? '-'} - {m.score?.away ?? '-'}
                </div>
              </button>
            ))}
          </div>
        </div>

        <div>
          {loading && <p style={{ color: '#94a3b8' }}>Cargando análisis real...</p>}
          {analysis && <AnalysisDashboard analysis={analysis} />}
        </div>
      </div>
    </div>
  );
}

export default App;
