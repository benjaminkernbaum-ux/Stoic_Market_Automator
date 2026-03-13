/**
 * /api/wa_reply_status — AI auto-reply engine status
 */
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const backendUrl = process.env.BACKEND_URL;
  if (backendUrl) {
    try {
      const upstream = await fetch(`${backendUrl}/api/wa_reply_status`);
      const data = await upstream.json();
      return res.status(200).json(data);
    } catch (e) {
      return res.status(502).json({ error: 'Backend unreachable', detail: e.message });
    }
  }

  return res.status(200).json({
    timestamp: new Date().toISOString(),
    queue_size: 3,
    auto_reply_active: true,
    last_sent: new Date().toISOString(),
    ai_model: 'GPT-4o',
    avg_response_time_sec: 7.4
  });
}
