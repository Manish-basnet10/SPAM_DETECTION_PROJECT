import React, { useState, useEffect } from "react";
import { apiHistory } from "../services/api";
import "../App.css";

export default function History() {
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  useEffect(() => {
    apiHistory()
      .then((d) => setPredictions(d.predictions || []))
      .catch(() => setPredictions([]))
      .finally(() => setLoading(false));
  }, []);

  const filtered = predictions.filter((p) => {
    if (filter === "spam") return p.is_spam;
    if (filter === "safe") return !p.is_spam;
    return true;
  });

  const total = predictions.length;
  const spamCount = predictions.filter((p) => p.is_spam).length;
  const safeCount = total - spamCount;

  const formatDate = (iso) => {
    const d = new Date(iso);
    return d.toLocaleString([], { dateStyle: "medium", timeStyle: "short" });
  };

  return (
    <div className="page-bg">
      <div className="history-wrapper">
        {/* Header */}
        <h1 className="history-title">📋 Prediction History</h1>
        <p className="history-subtitle">All your past spam detection results, stored securely in MongoDB</p>

        {/* Stat Cards */}
        {!loading && (
          <div className="history-stat-cards">
            <div className="hstat red">
              <div className="hstat-num">{spamCount}</div>
              <div className="hstat-label">🚨 Spam Detected</div>
            </div>
            <div className="hstat green">
              <div className="hstat-num">{safeCount}</div>
              <div className="hstat-label">✅ Legitimate</div>
            </div>
            <div className="hstat blue">
              <div className="hstat-num">{total}</div>
              <div className="hstat-label">📊 Total Analyzed</div>
            </div>
          </div>
        )}

        {/* Filter Buttons */}
        {!loading && total > 0 && (
          <div className="filter-bar">
            <button
              className={`filter-btn ${filter === "all" ? "active" : ""}`}
              onClick={() => setFilter("all")}
            >
              All
            </button>
            <button
              className={`filter-btn ${filter === "spam" ? "active" : ""}`}
              onClick={() => setFilter("spam")}
            >
              🚨 Spam Only
            </button>
            <button
              className={`filter-btn ${filter === "safe" ? "active" : ""}`}
              onClick={() => setFilter("safe")}
            >
              ✅ Legitimate Only
            </button>
          </div>
        )}

        {/* Table */}
        {loading ? (
          <div className="spinner" />
        ) : filtered.length > 0 ? (
          <div className="table-wrap">
            <table>
              <thead>
                <tr>
                  <th>#</th>
                  <th>Message Preview</th>
                  <th>Result</th>
                  <th>Confidence</th>
                  <th>Date</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((item, idx) => (
                  <tr key={item.id}>
                    <td style={{ color: "var(--text-muted)", fontSize: 13 }}>{idx + 1}</td>
                    <td style={{ maxWidth: 360 }}>
                      <span
                        title={item.message}
                        style={{
                          display: "block",
                          overflow: "hidden",
                          textOverflow: "ellipsis",
                          whiteSpace: "nowrap",
                          maxWidth: 340,
                        }}
                      >
                        {item.message}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${item.is_spam ? "badge-spam" : "badge-safe"}`}>
                        {item.is_spam ? "🚨 Spam" : "✅ Legitimate"}
                      </span>
                    </td>
                    <td>
                      <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
                        <div
                          style={{
                            width: 60,
                            height: 6,
                            background: "#e2e8f0",
                            borderRadius: 4,
                            overflow: "hidden",
                          }}
                        >
                          <div
                            style={{
                              width: `${item.confidence}%`,
                              height: "100%",
                              background: item.is_spam ? "#ef4444" : "#10b981",
                              borderRadius: 4,
                            }}
                          />
                        </div>
                        <span style={{ color: "var(--text-muted)", fontSize: 13 }}>
                          {item.confidence}%
                        </span>
                      </div>
                    </td>
                    <td style={{ color: "var(--text-muted)", fontSize: 13, whiteSpace: "nowrap" }}>
                      {formatDate(item.created_at)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="table-wrap">
            <div className="empty-state">
              <div className="empty-state-icon">📭</div>
              <p>{total === 0 ? "No predictions yet" : "No results match your filter"}</p>
              <span>
                {total === 0
                  ? "Go to Spam Check and analyze your first email!"
                  : "Try a different filter above."}
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="site-footer">
        Developed by Aastha Gupta | CSE | AI Project
      </footer>
    </div>
  );
}
