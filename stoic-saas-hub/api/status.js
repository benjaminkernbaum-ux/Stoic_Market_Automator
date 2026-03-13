/**
 * /api/status — health check proxy
 * Forwards to BACKEND_URL if set, otherwise returns static response.
 */
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const backendUrl = process.env.BACKEND_URL;
  if (backendUrl) {
    try {
      const upstream = await fetch(`${backendUrl}/api/status`);
      const data = await upstream.json();
      return res.status(200).json(data);
    } catch (e) {
      return res.status(502).json({ error: 'Backend unreachable', detail: e.message });
    }
  }

  // Static fallback
  return res.status(200).json({
    status: 'ok',
    service: 'Stoic Market Dashboard (static mode)',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
}
