import React from 'react';

export default function StatsTable({ stats }) {
  return (
    <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '14px' }}>
      <thead>
        <tr style={{ background: '#0f172a' }}>
          <th style={{ padding: '10px', textAlign: 'left', color: '#94a3b8' }}>Estadística</th>
          <th style={{ padding: '10px', textAlign: 'center', color: '#94a3b8' }}>Local</th>
          <th style={{ padding: '10px', textAlign: 'center', color: '#94a3b8' }}>Visitante</th>
          <th style={{ padding: '10px', textAlign: 'center', color: '#94a3b8' }}>Total</th>
        </tr>
      </thead>
      <tbody>
        {stats.map((s, i) => (
          <tr key={i} style={{ borderBottom: '1px solid #334155' }}>
            <td style={{ padding: '10px', color: '#e2e8f0' }}>{s.label}</td>
            <td style={{ padding: '10px', textAlign: 'center', color: '#38bdf8', fontWeight: 'bold' }}>
              {s.home ?? '-'}
            </td>
            <td style={{ padding: '10px', textAlign: 'center', color: '#f472b6', fontWeight: 'bold' }}>
              {s.away ?? '-'}
            </td>
            <td style={{ padding: '10px', textAlign: 'center', color: '#22c55e' }}>
              {s.total ?? '-'}
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
