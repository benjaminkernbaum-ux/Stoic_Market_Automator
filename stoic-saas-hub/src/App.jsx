import React, { useState } from 'react';
import {
  BarChart2,
  Tv,
  GraduationCap,
  BookOpen,
  HeartHandshake,
  Settings,
  Bell,
  Search,
  TrendingUp,
  PlayCircle,
  Check,
  Shield,
  Smartphone
} from 'lucide-react';
import './index.css';

// Mock Data
const MARKET_DATA = [
  { name: 'HK50', price: '16,589.2', change: '+1.2%', up: true },
  { name: 'S&P 500', price: '5,088.8', change: '+0.8%', up: true },
  { name: 'NASDAQ', price: '17,962.1', change: '+1.5%', up: true },
  { name: 'VIX', price: '13.45', change: '-4.2%', up: false },
  { name: 'BTC/USD', price: '62,104.0', change: '+5.1%', up: true },
  { name: 'XAU/USD', price: '2,034.5', change: '-0.1%', up: false },
];

const VIDEOS = [
  { id: 1, title: 'Fechamento HK50 - Oportunidades', author: 'Stoic Market', duration: '45:20', thumb: 'https://images.unsplash.com/photo-1611974789855-9c2a0a7236a3?auto=format&fit=crop&q=80&w=800' },
  { id: 2, title: 'Análise Institucional Bitcoin', author: 'Stoic Market', duration: '28:15', thumb: 'https://images.unsplash.com/photo-1518546305927-5a555bb7020d?auto=format&fit=crop&q=80&w=800' },
  { id: 3, title: 'Review Setup LW 9.x no S&P500', author: 'Benjamin', duration: '32:10', thumb: 'https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=800' },
];

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard />;
      case 'indicator':
        return <IndicatorView />;
      case 'tv':
        return <StoicTV />;
      case 'academy':
        return <Academy />;
      case 'social':
        return <SocialProject />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="container">
      {/* Sidebar Navigation */}
      <aside className="sidebar">
        <div className="logo-area">
          <span className="logo-icon">🗿</span>
          <span className="logo-text">
            STOIC<span className="text-gold">MARKET</span>
          </span>
        </div>

        <nav className="nav-menu">
          <NavItem icon={<BarChart2 />} label="Dashboard" active={activeTab === 'dashboard'} onClick={() => setActiveTab('dashboard')} />
          <NavItem icon={<TrendingUp />} label="Indicador LW 9.x" active={activeTab === 'indicator'} onClick={() => setActiveTab('indicator')} />
          <NavItem icon={<Tv />} label="Stoic TV" active={activeTab === 'tv'} onClick={() => setActiveTab('tv')} />
          <NavItem icon={<GraduationCap />} label="Academy" active={activeTab === 'academy'} onClick={() => setActiveTab('academy')} />
          <NavItem icon={<BookOpen />} label="E-Books" active={activeTab === 'ebooks'} onClick={() => setActiveTab('ebooks')} />
          <NavItem icon={<HeartHandshake />} label="Projeto Social" active={activeTab === 'social'} onClick={() => setActiveTab('social')} />

          <div style={{ flex: 1 }}></div>
          <NavItem icon={<Settings />} label="Configurações" active={false} onClick={() => { }} />
        </nav>
      </aside>

      {/* Main Content Area */}
      <main className="main-content">
        <Header />

        {/* Ticker Tape */}
        <div className="market-ticker glass-panel">
          {MARKET_DATA.map((item, idx) => (
            <div key={idx} className="ticker-item">
              <span className="ticker-name">{item.name}</span>
              <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
                <span className="ticker-price">{item.price}</span>
                <span className={`ticker-change ${item.up ? 'text-green' : 'text-red'}`}>
                  {item.change}
                </span>
              </div>
            </div>
          ))}
        </div>

        <div className="content-render">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}

// ---- Sub Components ----

const NavItem = ({ icon, label, active, onClick }) => (
  <a className={`nav-item ${active ? 'active' : ''}`} onClick={onClick}>
    {icon}
    <span>{label}</span>
  </a>
);

const Header = () => (
  <header className="top-header">
    <div className="glass-panel" style={{ display: 'flex', alignItems: 'center', padding: '10px 16px', gap: '8px', borderRadius: '30px', width: '300px' }}>
      <Search size={18} className="text-muted" />
      <input
        type="text"
        placeholder="Buscar ativos, aulas, vídeos..."
        style={{ background: 'transparent', border: 'none', color: '#fff', outline: 'none', width: '100%' }}
      />
    </div>

    <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
      <div className="glass-panel" style={{ padding: '10px', borderRadius: '50%', cursor: 'pointer' }}>
        <Bell size={20} className="text-gold" />
      </div>
      <div className="user-profile">
        <div className="avatar">B</div>
        <div style={{ display: 'flex', flexDirection: 'column' }}>
          <span style={{ fontSize: '14px', fontWeight: 'bold' }}>Benjamin</span>
          <span style={{ fontSize: '12px', color: 'var(--text-muted)' }}>Membro VIP</span>
        </div>
      </div>
    </div>
  </header>
);

const Dashboard = () => (
  <div>
    <h1 className="page-title" style={{ marginBottom: '24px' }}>Visão Geral</h1>
    <div className="dashboard-grid">
      <div className="card glass-panel span-8">
        <div className="card-title"><TrendingUp size={20} className="text-gold" /> Panorama de Mercado (VIX & HK50)</div>
        <div style={{ height: '300px', width: '100%', background: 'rgba(0,0,0,0.3)', borderRadius: '8px', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
          <span className="text-muted">Gráfico Principal (TradingView Widget placeholder)</span>
        </div>
      </div>

      <div className="card glass-panel span-4">
        <div className="card-title">Setup LW 9.x - Últimos Sinais</div>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginTop: '16px' }}>
          <div className="glass-panel" style={{ padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontWeight: 'bold' }}>HK50 (H1)</div>
              <div className="text-muted" style={{ fontSize: '12px' }}>Há 2 horas</div>
            </div>
            <div className="text-green" style={{ fontWeight: 'bold', background: 'rgba(46, 204, 113, 0.1)', padding: '4px 12px', borderRadius: '20px' }}>BUY</div>
          </div>
          <div className="glass-panel" style={{ padding: '16px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <div>
              <div style={{ fontWeight: 'bold' }}>BTCUSD (H4)</div>
              <div className="text-muted" style={{ fontSize: '12px' }}>Há 5 horas</div>
            </div>
            <div className="text-red" style={{ fontWeight: 'bold', background: 'rgba(231, 76, 60, 0.1)', padding: '4px 12px', borderRadius: '20px' }}>SELL</div>
          </div>
        </div>
        <button className="btn-gold" style={{ marginTop: 'auto' }}>Ir para Terminal</button>
      </div>

      <div className="card glass-panel span-12">
        <div className="card-title">Últimos Conteúdos em Vídeo</div>
        <div className="video-grid" style={{ marginTop: '16px' }}>
          {VIDEOS.map(v => (
            <div key={v.id} className="video-card">
              <div className="video-thumb">
                <img src={v.thumb} alt={v.title} />
                <div className="play-icon"><PlayCircle size={24} /></div>
              </div>
              <div className="video-title">{v.title}</div>
              <div className="video-info">{v.author} • {v.duration}</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  </div>
);

const IndicatorView = () => (
  <div className="sales-container animate-fade-in" style={{ position: 'relative', overflow: 'hidden', paddingBottom: '40px' }}>

    {/* Dynamic Background Effects */}
    <div className="glow-orb" style={{ top: '-10%', left: '20%', background: 'var(--gold)' }}></div>
    <div className="glow-orb" style={{ bottom: '10%', right: '10%', background: 'var(--blue)' }}></div>

    <div style={{ textAlign: 'center', marginBottom: '64px', paddingTop: '40px', position: 'relative', zIndex: 2 }}>
      <div style={{ display: 'inline-flex', alignItems: 'center', gap: '8px', background: 'rgba(223, 177, 91, 0.1)', color: 'var(--gold)', padding: '8px 20px', borderRadius: '30px', fontWeight: 'bold', letterSpacing: '2px', fontSize: '12px', marginBottom: '24px', border: '1px solid rgba(223, 177, 91, 0.3)', boxShadow: '0 0 20px rgba(223, 177, 91, 0.2)' }}>
        <span className="pulse-dot"></span> ACESSO PREMIUM
      </div>
      <h1 className="hero-title" style={{ fontSize: '56px', fontWeight: '800', marginBottom: '24px', lineHeight: '1.2', background: 'linear-gradient(to right, #fff, #dfb15b)', WebkitBackgroundClip: 'text', WebkitTextFillColor: 'transparent' }}>
        O Fim do Ruído de Mercado.<br /> A Certeza Institucional.
      </h1>
      <p className="text-muted" style={{ fontSize: '20px', maxWidth: '750px', margin: '0 auto', lineHeight: '1.6' }}>
        Você já perdeu dinheiro tentando adivinhar onde a tendência muda? O <b className="text-gold">Stoic LW 9.x</b> não tenta adivinhar. Ele prova matematicamente o momento exato da exaustão institucional.
      </p>
      <div style={{ marginTop: '40px', display: 'flex', gap: '16px', justifyContent: 'center' }}>
        <button className="btn-gold" style={{ padding: '16px 32px', fontSize: '18px', display: 'flex', alignItems: 'center', gap: '12px' }}>
          <Shield size={24} /> Assinar Agora - R$ 97/mês
        </button>
        <button className="btn-outline" style={{ padding: '16px 32px', fontSize: '18px', display: 'flex', alignItems: 'center', gap: '12px', background: 'transparent', border: '1px solid var(--gold)', color: 'var(--gold)', borderRadius: '8px', cursor: 'pointer' }}>
          <PlayCircle size={24} /> Ver Demonstração
        </button>
      </div>
    </div>

    <div className="dashboard-grid relative" style={{ zIndex: 2 }}>
      <div className="card glass-panel span-6" style={{ display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <h2 style={{ fontSize: '28px', marginBottom: '32px', color: '#fff' }}>A Máquina de Checklist Intelectual</h2>
        <ul style={{ listStyle: 'none', padding: 0, display: 'flex', flexDirection: 'column', gap: '32px' }}>
          <li className="feature-item" style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
            <div className="icon-box green-box"><Check size={28} /></div>
            <div>
              <h3 style={{ fontSize: '20px', marginBottom: '8px', color: '#fff' }}>O Gatilho de Momentum (Hook)</h3>
              <p className="text-muted" style={{ lineHeight: '1.6', fontSize: '15px' }}>O robô não entra em "repiques" normais. Ele caça a verdadeira exaustão de 5 barras provando matematicamente quando a força institucional perde o fôlego.</p>
            </div>
          </li>
          <li className="feature-item" style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
            <div className="icon-box red-box"><Shield size={28} /></div>
            <div>
              <h3 style={{ fontSize: '20px', marginBottom: '8px', color: '#fff' }}>Escudo Anti-Armadilha (Trend Filter 50)</h3>
              <p className="text-muted" style={{ lineHeight: '1.6', fontSize: '15px' }}>Bloqueia instantaneamente sinais contra a macro tendência (EMA 50). O fim definitivo das temidas "Bull Traps".</p>
            </div>
          </li>
          <li className="feature-item" style={{ display: 'flex', gap: '20px', alignItems: 'flex-start' }}>
            <div className="icon-box gold-box"><Smartphone size={28} /></div>
            <div>
              <h3 style={{ fontSize: '20px', marginBottom: '8px', color: '#fff' }}>Decisões Limpas: "SIM" ou "NÃO"</h3>
              <p className="text-muted" style={{ lineHeight: '1.6', fontSize: '15px' }}>Tabela visual de Checklist dita as regras na tela. Integração "Plug and Play" no TradingView com alertas diretos pro seu App.</p>
            </div>
          </li>
        </ul>
      </div>

      <div className="card glass-panel span-6 indicator-mockup-wrapper" style={{ position: 'relative', overflow: 'hidden', padding: 0, border: '1px solid rgba(223, 177, 91, 0.3)', borderRadius: '16px', boxShadow: '0 20px 40px rgba(0,0,0,0.6)' }}>
        <div className="mockup-header" style={{ padding: '16px 24px', background: 'rgba(0,0,0,0.4)', borderBottom: '1px solid rgba(255,255,255,0.05)', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <span style={{ fontWeight: '600', fontSize: '16px' }}>BTCUSD • 15m • Stoic</span>
            <span className="live-badge text-green" style={{ fontSize: '12px', fontWeight: 'bold', display: 'flex', alignItems: 'center', gap: '6px', background: 'rgba(46, 204, 113, 0.1)', padding: '4px 10px', borderRadius: '12px' }}>
              <span className="live-dot"></span> LIVE
            </span>
          </div>
          <div style={{ display: 'flex', gap: '8px' }}>
            <div className="mockup-btn"></div>
            <div className="mockup-btn"></div>
            <div className="mockup-btn"></div>
          </div>
        </div>

        {/* Animated Chart Simulation */}
        <div className="chart-simulation" style={{ height: '400px', background: '#0a0b10', position: 'relative', overflow: 'hidden' }}>
          {/* Grid */}
          <div className="chart-grid"></div>

          {/* Animated EMA Lines */}
          <svg style={{ position: 'absolute', top: 0, left: 0, width: '100%', height: '100%' }}>
            <path d="M-50,250 Q100,200 150,280 T300,180 T500,250 T700,100" fill="none" stroke="var(--blue)" strokeWidth="3" className="animated-path" />
            <path d="M-50,280 Q100,250 180,240 T350,220 T550,150 T750,120" fill="none" stroke="var(--orange)" strokeWidth="2" className="animated-path-slow" opacity="0.6" />
          </svg>

          {/* Buy Signal Animation */}
          <div className="buy-signal-anim" style={{ position: 'absolute', top: '65%', left: '30%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ background: 'var(--green)', color: 'white', fontSize: '12px', fontWeight: 'bold', padding: '4px 8px', borderRadius: '4px', marginBottom: '4px' }}>BUY</div>
            <div style={{ width: '0', height: '0', borderLeft: '6px solid transparent', borderRight: '6px solid transparent', borderBottom: '8px solid var(--green)' }}></div>
          </div>

          {/* Sell Signal Animation */}
          <div className="sell-signal-anim" style={{ position: 'absolute', top: '30%', left: '60%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <div style={{ width: '0', height: '0', borderLeft: '6px solid transparent', borderRight: '6px solid transparent', borderTop: '8px solid var(--red)' }}></div>
            <div style={{ background: 'var(--red)', color: 'white', fontSize: '12px', fontWeight: 'bold', padding: '4px 8px', borderRadius: '4px', marginTop: '4px' }}>SELL</div>
          </div>

          {/* Animated Table HUD */}
          <div className="hud-table" style={{ position: 'absolute', right: '16px', top: '16px', background: 'rgba(13, 15, 17, 0.9)', border: '1px solid rgba(223,177,91,0.2)', borderRadius: '12px', padding: '16px', width: '220px', boxShadow: '0 10px 30px rgba(0,0,0,0.5)', zIndex: 10 }}>
            <div style={{ fontSize: '12px', fontWeight: 'bold', marginBottom: '16px', color: 'var(--gold)', textAlign: 'center', letterSpacing: '1px' }}>CHECKLIST LW 9.X</div>
            <div className="hud-row"><span className="text-muted">Histórico</span> <span>✅</span></div>
            <div className="hud-row"><span className="text-muted">Hook</span> <span>✅</span></div>
            <div className="hud-row"><span className="text-muted">Cross EMA</span> <span>✅</span></div>
            <div className="hud-row"><span className="text-muted">Trend OK</span> <span>✅</span></div>
            <div className="hud-result hud-pulse-green" style={{ marginTop: '16px', padding: '10px', background: 'rgba(46, 204, 113, 0.15)', color: 'var(--green)', textAlign: 'center', fontWeight: 'bold', fontSize: '14px', borderRadius: '6px', border: '1px solid rgba(46, 204, 113, 0.3)' }}>✅ BUY BTCUSD</div>
          </div>
        </div>
      </div>
    </div>

    {/* Proof container */}
    <div className="proof-section mt-5" style={{ marginTop: '80px', textAlign: 'center', position: 'relative', zIndex: 2 }}>
      <h2 style={{ fontSize: '32px', marginBottom: '16px', color: '#fff' }}>Junte-se a Centenas de Traders</h2>
      <p className="text-muted" style={{ marginBottom: '40px', fontSize: '18px' }}>O que dizem os membros da comunidade que utilizam o Stoic LW 9.x</p>
      <div className="dashboard-grid">
        <div className="card glass-panel span-4 testimonial-card" style={{ padding: '32px', textAlign: 'left' }}>
          <div className="stars text-gold" style={{ marginBottom: '16px', fontSize: '20px' }}>★★★★★</div>
          <p className="text-muted" style={{ lineHeight: '1.6', fontStyle: 'italic', marginBottom: '24px' }}>"A tabela de checklist mudou meu operacional. Antigamente eu hesitava nas entradas, agora o indicador me diz exatamente quando é a hora."</p>
          <div style={{ fontWeight: 'bold', color: '#fff' }}>Carlos E. <span className="text-muted" style={{ fontWeight: 'normal', fontSize: '14px' }}>- Day Trader</span></div>
        </div>
        <div className="card glass-panel span-4 testimonial-card" style={{ padding: '32px', textAlign: 'left' }}>
          <div className="stars text-gold" style={{ marginBottom: '16px', fontSize: '20px' }}>★★★★★</div>
          <p className="text-muted" style={{ lineHeight: '1.6', fontStyle: 'italic', marginBottom: '24px' }}>"Incrível como o filtro de tendência me salvou de tomar stop nos dias laterais. Vale cada centavo da assinatura mensal."</p>
          <div style={{ fontWeight: 'bold', color: '#fff' }}>Fernando M. <span className="text-muted" style={{ fontWeight: 'normal', fontSize: '14px' }}>- Analista</span></div>
        </div>
        <div className="card glass-panel span-4 testimonial-card" style={{ padding: '32px', textAlign: 'left' }}>
          <div className="stars text-gold" style={{ marginBottom: '16px', fontSize: '20px' }}>★★★★★</div>
          <p className="text-muted" style={{ lineHeight: '1.6', fontStyle: 'italic', marginBottom: '24px' }}>"Plug and play mesmo! Coloquei no TradingView, ativei os alertas pro celular e só entro nas operações quando o robô grita."</p>
          <div style={{ fontWeight: 'bold', color: '#fff' }}>Amanda R. <span className="text-muted" style={{ fontWeight: 'normal', fontSize: '14px' }}>- Investidora</span></div>
        </div>
      </div>
    </div>
  </div>
);

const StoicTV = () => (
  <div>
    <h1 className="page-title" style={{ marginBottom: '24px' }}>Stoic TV (Lives & Análises)</h1>
    <div className="dashboard-grid">
      <div className="card glass-panel span-8" style={{ height: '500px' }}>
        <div className="video-thumb" style={{ height: '100%', marginBottom: 0, borderRadius: '8px' }}>
          <img src="https://images.unsplash.com/photo-1590283603385-17ffb3a7f29f?auto=format&fit=crop&q=80&w=1200" alt="Live" style={{ opacity: 0.5 }} />
          <div style={{ position: 'absolute', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '16px' }}>
            <div style={{ background: '#e74c3c', color: 'white', padding: '4px 12px', borderRadius: '20px', fontWeight: 'bold', fontSize: '14px' }}>AO VIVO AGORA</div>
            <h2>Fechamento do Mercado Asiático (HK50)</h2>
            <button className="btn-gold border-none"><PlayCircle size={20} style={{ display: 'inline', marginRight: '8px' }} /> Assistir Live</button>
          </div>
        </div>
      </div>
      <div className="card glass-panel span-4">
        <div className="card-title">Chat da Live VIP</div>
        <div style={{ flex: 1, background: 'rgba(0,0,0,0.2)', borderRadius: '8px', padding: '16px', display: 'flex', flexDirection: 'column' }}>
          <div style={{ flex: 1 }}>
            <div style={{ marginBottom: '12px' }}><span className="text-gold" style={{ fontWeight: 'bold' }}>João Silva:</span> Alguém pegou essa compra no fundo?</div>
            <div style={{ marginBottom: '12px' }}><span className="text-gold" style={{ fontWeight: 'bold' }}>Marcos:</span> Setup ativou lindo no H1.</div>
          </div>
          <input type="text" placeholder="Digite no chat..." style={{ width: '100%', padding: '12px', borderRadius: '8px', border: '1px solid var(--panel-border)', background: 'transparent', color: 'white' }} />
        </div>
      </div>
    </div>
  </div>
);

const Academy = () => (
  <div>
    <h1 className="page-title" style={{ marginBottom: '24px' }}>Stoic Academy</h1>
    <div className="video-grid">
      <div className="glass-panel" style={{ padding: '24px', textAlign: 'center' }}>
        <GraduationCap size={48} className="text-gold" style={{ margin: '0 auto 16px auto' }} />
        <h3>Formação de Traders</h3>
        <p className="text-muted" style={{ margin: '12px 0' }}>Curso completo do zero à consistência.</p>
        <button className="btn-gold">Acessar Curso</button>
      </div>
      <div className="glass-panel" style={{ padding: '24px', textAlign: 'center' }}>
        <BookOpen size={48} className="text-gold" style={{ margin: '0 auto 16px auto' }} />
        <h3>Módulo Análise Fundamentalista</h3>
        <p className="text-muted" style={{ margin: '12px 0' }}>Como ler os indicadores globais.</p>
        <button className="btn-gold">Acessar Curso</button>
      </div>
    </div>
  </div>
);

const SocialProject = () => (
  <div>
    <h1 className="page-title" style={{ marginBottom: '24px' }}>Projeto Social: Traders Transformando Vidas</h1>
    <div className="card glass-panel span-12" style={{ display: 'flex', flexDirection: 'row', gap: '32px' }}>
      <div style={{ flex: 1 }}>
        <img src="https://images.unsplash.com/photo-1488521787991-ed7bbaae773c?auto=format&fit=crop&q=80&w=800" style={{ width: '100%', borderRadius: '12px', opacity: 0.8 }} alt="Social" />
      </div>
      <div style={{ flex: 1, display: 'flex', flexDirection: 'column', justifyContent: 'center' }}>
        <h2 className="text-gold" style={{ marginBottom: '16px' }}>Impacto Real através do Mercado</h2>
        <p className="text-muted" style={{ lineHeight: '1.6', marginBottom: '24px' }}>
          Nossa comunidade acredita que o mercado financeiro é um meio de enriquecimento não apenas pessoal, mas coletivo. Parte da arrecadação das assinaturas VIP da Stoic Market é destinada a projetos de educação financeira para jovens em áreas carentes.
        </p>
        <div style={{ display: 'flex', gap: '24px', marginBottom: '32px' }}>
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold' }}>R$ 15.420</div>
            <div className="text-muted">Doações Realizadas em 2026</div>
          </div>
          <div>
            <div style={{ fontSize: '32px', fontWeight: 'bold' }}>120+</div>
            <div className="text-muted">Jovens Impactados</div>
          </div>
        </div>
        <button className="btn-gold" style={{ width: 'fit-content' }}>Conheça Mais</button>
      </div>
    </div>
  </div>
);

export default App;
