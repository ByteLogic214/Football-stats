import React from 'react';

export default function OddsComparison({ odds }) {
  const markets = [...new Set(odds.map(o => o.market))];
  
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
      {markets.map(market => {
        const marketOdds = odds.filter(o => o.market === market);
        return (
          <div key={market} style={{ background: '#0f172a', padding: '15px', borderRadius: '8px' }}>
            <h4 style={{ color: '#38bdf8', marginBottom: '10px', fontSize: '14px' }}>{market}</h4>
            <table style={{ width: '100%', fontSize: '13px' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', color: '#94a3b8' }}>Casa</th>
                  <th style={{ textAlign: 'left', color: '#94a3b8' }}>Selección</th>
                  <th style={{ textAlign: 'center', color: '#94a3b8' }}>Apertura</th>
                  <th style={{ textAlign: 'center', color: '#94a3b8' }}>Actual</th>
                  <th style={{ textAlign: 'center', color: '#94a3b8' }}>Prob. Implícita</th>
                </tr>
              </thead>
              <tbody>
                {marketOdds.map((o, i) => (
                  <tr key={i}>
                    <td style={{ padding: '6px 0', color: '#cbd5e1' }}>{o.bookmaker}</td>
                    <td style={{ padding: '6px 0', color: '#e2e8f0' }}>{o.selection}</td>
                    <td style={{ padding: '6px 0', textAlign: 'center', color: '#94a3b8' }}>{o.opening ?? '-'}</td>
                    <td style={{ padding: '6px 0', textAlign: 'center', color: '#22c55e', fontWeight: 'bold' }}>
                      {o.current ?? '-'}
                    </td>
                    <td style={{ padding: '6px 0', textAlign: 'center', color: '#f59e0b' }}>
                      {o.implied_prob ? `${o.implied_prob}%` : '-'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        );
      })}
    </div>
  );
}
