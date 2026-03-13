/**
 * /api/wa_inbox — WhatsApp inbox messages
 */
export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');

  if (req.method === 'OPTIONS') return res.status(204).end();

  const backendUrl = process.env.BACKEND_URL;
  if (backendUrl) {
    try {
      const upstream = await fetch(`${backendUrl}/api/wa_inbox`);
      const data = await upstream.json();
      return res.status(200).json(data);
    } catch (e) {
      return res.status(502).json({ error: 'Backend unreachable', detail: e.message });
    }
  }

  return res.status(200).json({
    timestamp: new Date().toISOString(),
    messages: [
      { id: 1, contact: 'João Silva',     phone: '+5511987654321', message: 'Quando é a próxima live?',      status: 'unread'  },
      { id: 2, contact: 'Marcos Andrade', phone: '+5511912345678', message: 'Quero assinar o plano VIP',     status: 'pending' },
      { id: 3, contact: 'Amanda R.',      phone: '+5511976543210', message: 'O indicador deu sinal agora?',  status: 'replied' },
      { id: 4, contact: 'Carlos E.',      phone: '+5511965432109', message: 'Consigo parcelar a assinatura?', status: 'unread' },
      { id: 5, contact: 'Fernanda Lima',  phone: '+5511943210987', message: 'Qual é o WhatsApp do suporte?', status: 'pending' },
    ]
  });
}
