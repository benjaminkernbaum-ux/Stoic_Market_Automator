/**
 * /api/whatsapp_stats — WhatsApp outreach statistics
 */
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const backendUrl = process.env.BACKEND_URL;
  if (backendUrl) {
    try {
      const upstream = await fetch(`${backendUrl}/api/whatsapp_stats`);
      const data = await upstream.json();
      return res.status(200).json(data);
    } catch (e) {
      return res.status(502).json({ error: 'Backend unreachable', detail: e.message });
    }
  }

  return res.status(200).json({
    timestamp: new Date().toISOString(),
    messages_sent_today: 218,
    messages_delivered: 210,
    messages_read: 168,
    replies_received: 84,
    conversion_rate_pct: 38.5,
    pipeline_value: 11200.0
  });
}
