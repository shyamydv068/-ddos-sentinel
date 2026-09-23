const statCards = [
  { label: 'Total Traffic', value: '—', tone: 'neutral' },
  { label: 'Requests/sec', value: '—', tone: 'good' },
  { label: 'Active Connections', value: '—', tone: 'warning' },
  { label: 'Attacks Detected', value: '—', tone: 'danger' },
  { label: 'Blocked IPs', value: '—', tone: 'danger' },
  { label: 'ML Accuracy', value: '—', tone: 'good' },
  { label: 'Detection Latency', value: '—', tone: 'neutral' },
];

function App() {
  return (
    <div className="dashboard-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-badge">DS</div>
          <div>
            <h1>DDOS SENTINEL</h1>
            <p>Real-Time DDoS Detection & Prevention</p>
          </div>
        </div>

        <nav className="nav">
          <span>Overview</span>
          <span>Live Traffic</span>
          <span>Attack Detection</span>
          <span>ML Analytics</span>
          <span>Kafka Streaming</span>
          <span>Spark Processing</span>
          <span>Attack History</span>
          <span>Blocked IPs</span>
          <span>Alerts</span>
          <span>System Logs</span>
          <span>Settings</span>
        </nav>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <h2>Operations Overview</h2>
            <p>System Online · Kafka Connected · Spark Streaming · ML Model Active</p>
          </div>
          <div className="status-pill success">SYSTEM ONLINE</div>
        </header>

        <section className="stats-grid">
          {statCards.map((card) => (
            <div key={card.label} className={`stat-card ${card.tone}`}>
              <label>{card.label}</label>
              <strong>{card.value}</strong>
            </div>
          ))}
        </section>

        <section className="panel-grid">
          <div className="panel large">
            <h3>Real-Time Network Traffic</h3>
            <div className="chart-placeholder">Traffic chart will render here</div>
          </div>
          <div className="panel">
            <h3>Attack Distribution</h3>
            <div className="chart-placeholder">Attack chart will render here</div>
          </div>
          <div className="panel">
            <h3>ML Performance</h3>
            <div className="chart-placeholder">ML metrics chart</div>
          </div>
          <div className="panel">
            <h3>Kafka Throughput</h3>
            <div className="chart-placeholder">Kafka metrics</div>
          </div>
          <div className="panel">
            <h3>System Health</h3>
            <div className="chart-placeholder">Backend / DB / Kafka / Spark / ML</div>
          </div>
          <div className="panel">
            <h3>Recent Alerts</h3>
            <ul className="log-list">
              <li>Waiting for live events...</li>
              <li>Demo traffic pipeline is initializing.</li>
            </ul>
          </div>
        </section>
      </main>
    </div>
  );
}

export default App;
