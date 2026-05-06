import React, { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { apiStats, getUser, clearAuth } from "../services/api";
import "../App.css";

export default function Dashboard() {
  const navigate = useNavigate();
  const user = getUser();
  const [stats, setStats] = useState(null);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showLogout, setShowLogout] = useState(false);

  useEffect(() => {
    apiStats()
      .then((d) => { setStats(d.stats); setRecent(d.recent || []); })
      .catch(() => setStats({ total: 0, spam: 0, safe: 0, spam_rate: 0 }))
      .finally(() => setLoading(false));
  }, []);

  const handleLogout = () => {
    clearAuth();
    navigate("/");
  };

  const statCards = stats
    ? [
        { cls: "total", icon: "📊", num: stats.total,          label: "Total Analyzed" },
        { cls: "spam",  icon: "🚨", num: stats.spam,           label: "Spam Detected" },
        { cls: "safe",  icon: "✅", num: stats.safe,           label: "Safe Emails" },
        { cls: "rate",  icon: "📈", num: `${stats.spam_rate}%`, label: "Spam Rate" },
      ]
    : [];

  const actions = [
    { icon: "🔍", title: "Check Email", desc: "Paste any message to instantly detect spam with AI", path: "/spam" },
    { icon: "📋", title: "View History", desc: "Browse all your past predictions with results", path: "/history" },
  ];

  const formatTime = (iso) => {
    const d = new Date(iso);
    return d.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  return (
    <div className="page-bg">
      {/* Header */}
      <div className="page-header">
        <div>
          <h1 className="page-title">👋 Hey, {user?.name?.split(" ")[0] || "there"}!</h1>
          <p className="page-subtitle">Here's your spam detection summary</p>
        </div>
        <button className="btn btn-danger-outline" onClick={() => setShowLogout(true)}>
          🚪 Logout
        </button>
      </div>

      {/* Stats */}
      {loading ? (
        <div className="spinner" />
      ) : (
        <div className="stats-grid">
          {statCards.map((s, i) => (
            <div className={`stat-card ${s.cls}`} key={i} style={{ animationDelay: `${i * 0.08}s` }}>
              <div className="stat-icon">{s.icon}</div>
              <div className="stat-number">{s.num}</div>
              <div className="stat-label">{s.label}</div>
            </div>
          ))}
        </div>
      )}

      {/* Action Cards */}
      <div className="action-grid">
        {actions.map((a, i) => (
          <Link to={a.path} className="action-card" key={i}>
            <span className="action-card-icon">{a.icon}</span>
            <h3>{a.title}</h3>
            <p>{a.desc}</p>
            <span className="btn btn-primary" style={{ display: "inline-flex", width: "auto", padding: "10px 24px" }}>
              Open →
            </span>
          </Link>
        ))}
      </div>

      {/* Recent Activity */}
      {recent.length > 0 && (
        <div style={{ maxWidth: 1100, margin: "0 auto" }}>
          <div className="glass-card">
            <h2 style={{ fontSize: 18, fontWeight: 700, marginBottom: 20, color: "var(--text)" }}>
              🕓 Recent Activity
            </h2>
            <ul className="recent-list">
              {recent.map((r, i) => (
                <li className="recent-item" key={i}>
                  <span className={`recent-dot ${r.is_spam ? "spam" : "safe"}`} />
                  <span className="recent-msg">{r.message || "—"}</span>
                  <span className={`badge ${r.is_spam ? "badge-spam" : "badge-safe"}`}>
                    {r.result}
                  </span>
                  <span className="recent-time">{formatTime(r.created_at)}</span>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}

      {/* Footer */}
      <footer className="site-footer">
        Developed by Aastha Gupta | CSE | AI Project
      </footer>

      {/* Logout Modal */}
      {showLogout && (
        <div className="modal-overlay">
          <div className="modal-card">
            <p style={{ fontSize: 40, marginBottom: 12 }}>🚪</p>
            <h3>Sign out?</h3>
            <p>You'll need to log in again to access your dashboard.</p>
            <div className="modal-btns">
              <button className="btn btn-secondary" onClick={() => setShowLogout(false)}>Cancel</button>
              <button className="btn btn-danger-outline" onClick={handleLogout}>Sign Out</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
