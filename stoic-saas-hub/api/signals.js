/**
 * /api/signals — LW 9.x active trading signals
 */
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const backendUrl = process.env.BACKEND_URL;
  if (backendUrl) {
    try {
      const upstream = await fetch(`${backendUrl}/api/signals`);
      const data = await upstream.json();
      return res.status(200).json(data);
    } catch (e) {
      return res.status(502).json({ error: 'Backend unreachable', detail: e.message });
    }
  }

  return res.status(200).json({
    timestamp: new Date().toISOString(),
    active_signals: [
      {
        id: 1, symbol: 'HK50', timeframe: 'H1', direction: 'BUY',
        entry: 16580.0, sl: 16500.0, tp: 16740.0,
        checklist: { historico: true, hook: true, cross_ema: true, trend_ok: true },
        age_minutes: 240
      },
      {
        id: 2, symbol: 'BTCUSD', timeframe: 'H4', direction: 'SELL',
        entry: 62100.0, sl: 62900.0, tp: 60500.0,
        checklist: { historico: true, hook: true, cross_ema: false, trend_ok: true },
        age_minutes: 480
      }
    ]
  });
}
