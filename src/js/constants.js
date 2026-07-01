// ===== CONSTANTS =====
const FACTORES = ['D', 'I', 'S', 'C'];
const CORES = { D: '#E74C3C', I: '#F39C12', S: '#27AE60', C: '#2980B9' };
const INSTRUMENT_VERSION = '2.0.0';
const API_BASE = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000' : '';
const DISCREPANCY_THRESHOLD = 4;
const ZONA_CINZENTA = 8;