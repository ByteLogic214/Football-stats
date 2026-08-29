const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = {
  async getHealth() {
    const r = await fetch(`${API_BASE}/health`);
    return r.json();
  },
  async getCompetitions() {
    const r = await fetch(`${API_BASE}/competitions/`);
    return r.json();
  },
  async getMatches(params = '') {
    const r = await fetch(`${API_BASE}/matches/${params}`);
    return r.json();
  },
  async getAnalysis(matchId) {
    const r = await fetch(`${API_BASE}/analysis/${matchId}`);
    return r.json();
  }
};

export default api;
