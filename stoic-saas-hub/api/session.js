/**
 * /api/session — current user session info
 */
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const backendUrl = process.env.BACKEND_URL;
  if (backendUrl) {
    try {
      const upstream = await fetch(`${backendUrl}/api/session`);
      const data = await upstream.json();
      return res.status(200).json(data);
    } catch (e) {
      return res.status(502).json({ error: 'Backend unreachable', detail: e.message });
    }
  }

  return res.status(200).json({
    timestamp: new Date().toISOString(),
    session_id: `sess_${Date.now()}`,
    user: 'Benjamin',
    role: 'admin',
    permissions: ['read', 'write', 'admin'],
    expires_in_sec: 3600
  });
}
