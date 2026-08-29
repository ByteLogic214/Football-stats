import React from 'react';
import StatsTable from './StatsTable.jsx';
import OddsComparison from './OddsComparison.jsx';

export default function AnalysisDashboard({ analysis }) {
  return (
    <div style={{ background: '#1e293b', padding: '20px', borderRadius: '12px', border: '1px solid #334155' }}>
      <h2 style={{ color: '#38bdf8', marginBottom: '15px' }}>
        {analysis.home_team} vs {analysis.away_team}
      </h2>
      
      {analysis.score && (
        <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#22c55e', marginBottom: '20px' }}>
          Resultado: {analysis.score.home} - {analysis.score.away}
        </div>
      )}

      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ color: '#cbd5e1', marginBottom: '10px' }}>📊 Estadísticas Clave</h3>
        <StatsTable stats={analysis.key_stats} />
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h3 style={{ color: '#cbd5e1', marginBottom: '10px' }}>🎯 Probabilidades Calculadas</h3>
        <div style={{ display: 'flex', gap: '15px' }}>
          {analysis.btts_probability && (
            <div style={{ background: '#0f172a', padding: '15px', borderRadius: '8px', flex: 1 }}>
              <div style={{ fontSize: '12px', color: '#94a3b8' }}>Ambos Anotan (BTTS)</div>
              <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#f59e0b' }}>
                {analysis.btts_probability}%
              </div>
            </div>
          )}
          {analysis.over_goals_probability && (
            <div style={{ background: '#0f172a', padding: '15px', borderRadius: '8px', flex: 1 }}>
              <div style={{ fontSize: '12px', color: '#94a3b8' }}>Over 2.5 Goles</div>
              <div style={{ fontSize: '20px', fontWeight: 'bold', color: '#f59e0b' }}>
                {analysis.over_goals_probability}%
              </div>
            </div>
          )}
        </div>
      </div>

      <div>
        <h3 style={{ color: '#cbd5e1', marginBottom: '10px' }}>💰 Comparación de Cuotas</h3>
        <OddsComparison odds={analysis.odds_comparison} />
      </div>
    </div>
  );
}
