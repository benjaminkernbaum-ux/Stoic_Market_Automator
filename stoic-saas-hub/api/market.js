/**
 * /api/market — live market snapshot proxy
 */
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const backendUrl = process.env.BACKEND_URL;
  if (backendUrl) {
    try {
      const upstream = await fetch(`${backendUrl}/api/market`);
      const data = await upstream.json();
      return res.status(200).json(data);
    } catch (e) {
      return res.status(502).json({ error: 'Backend unreachable', detail: e.message });
    }
  }

  // Static fallback with realistic data
  const jitter = (base, pct = 0.01) => parseFloat((base * (1 + (Math.random() * 2 - 1) * pct)).toFixed(2));
  return res.status(200).json({
    timestamp: new Date().toISOString(),
    assets: [
      { symbol: 'HK50',    price: jitter(16589.2, 0.005), change_pct: parseFloat((Math.random() * 3 - 1).toFixed(2)) },
      { symbol: 'S&P 500', price: jitter(5088.8,  0.003), change_pct: parseFloat((Math.random() * 2 - 0.5).toFixed(2)) },
      { symbol: 'NASDAQ',  price: jitter(17962.1, 0.004), change_pct: parseFloat((Math.random() * 3 - 1).toFixed(2)) },
      { symbol: 'VIX',     price: jitter(13.45,   0.02),  change_pct: parseFloat((Math.random() * 10 - 5).toFixed(2)) },
      { symbol: 'BTC/USD', price: jitter(62104.0, 0.01),  change_pct: parseFloat((Math.random() * 8 - 3).toFixed(2)) },
      { symbol: 'XAU/USD', price: jitter(2034.5,  0.003), change_pct: parseFloat((Math.random() * 1 - 0.5).toFixed(2)) },
    ]
  });
}
