import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { apiPredict, apiHealth } from "../services/api";
import "../App.css";

export default function SpamCheck() {
  const navigate = useNavigate();
  const [message, setMessage] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [apiOnline, setApiOnline] = useState(null);

  useEffect(() => {
    apiHealth()
      .then(() => setApiOnline(true))
      .catch(() => setApiOnline(false));
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) { setError("Please enter some text to analyze"); return; }
    setError(""); setResult(null); setLoading(true);
    try {
      const data = await apiPredict(message.trim());
      setResult(data);
    } catch (err) {
      setError(err.message || "Prediction failed. Make sure you are logged in.");
    } finally {
      setLoading(false);
    }
  };

  const isSpam = result?.result === "Spam";

  return (
    <div className="spamcheck-wrapper">
      <div className="spamcheck-card">
        {/* Title */}
        <h1 className="spamcheck-title">🔍 Analyze Your Email</h1>
        <p className="spamcheck-subtitle">Paste any email or message — our AI will classify it instantly</p>

        {/* API Status badge */}
        <div style={{ textAlign: "center", marginBottom: 20 }}>
          {apiOnline === null ? (
            <span className="api-badge offline">⏳ Checking API...</span>
          ) : apiOnline ? (
            <span className="api-badge online"><span className="dot" /> API Online — Ready</span>
          ) : (
            <span className="api-badge offline"><span className="dot" /> API Offline</span>
          )}
        </div>

        {/* Error */}
        {error && <div className="alert alert-error">⚠️ {error}</div>}

        {/* Input Form */}
        {!result && (
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Email / Message Content</label>
              <textarea
                placeholder={"Paste the email subject + body here...\n\nExample: Congratulations! You've won $1,000,000. Click here to claim your prize..."}
                value={message}
                onChange={(e) => setMessage(e.target.value)}
                disabled={loading}
              />
              <div className="char-count">{message.length} / 5000 characters</div>
            </div>
            <div className="btn-row">
              <button type="submit" className="btn btn-primary" disabled={loading || !apiOnline}>
                {loading ? "🤖 Analyzing..." : "🔍 Analyze Email"}
              </button>
              <button
                type="button"
                className="btn btn-secondary"
                onClick={() => navigate("/history")}
              >
                📋 View History
              </button>
            </div>
          </form>
        )}

        {/* Loading */}
        {loading && (
          <div style={{ textAlign: "center", paddingTop: 20 }}>
            <div className="spinner" />
            <p style={{ color: "var(--text-muted)", fontSize: 14 }}>AI is analyzing your message...</p>
          </div>
        )}

        {/* Result Card */}
        {result && !loading && (
          <div className={`result-card ${isSpam ? "spam" : "safe"}`}>
            <div className="result-icon-wrap">
              <span className="result-icon">{isSpam ? "⚠️" : "✅"}</span>
            </div>
            <div className="result-title">
              {isSpam ? "This is SPAM" : "This is NOT SPAM"}
            </div>
            <p className="result-hint">
              {isSpam
                ? "⚠️ This message exhibits spam patterns. Avoid clicking any links."
                : "🎉 This message appears legitimate. Stay cautious regardless."}
            </p>

            {/* Info Boxes */}
            <div className="result-info-boxes">
              <div className="result-info-box">
                <div className="info-label">Confidence</div>
                <div className="info-value">{result.confidence}%</div>
              </div>
              <div className="result-info-box">
                <div className="info-label">Classification</div>
                <div className="info-value" style={{ fontSize: 16, marginTop: 4 }}>{result.result}</div>
              </div>
            </div>

            {/* Confidence bar */}
            <div className="confidence-bar-wrap">
              <div className="confidence-bar-fill" style={{ width: `${result.confidence}%` }} />
            </div>

            {/* Email Preview */}
            <div style={{ marginTop: 20 }}>
              <div className="result-email-label">Original Email</div>
              <div className="result-email-preview">{message}</div>
            </div>

            {/* Buttons */}
            <div className="result-buttons">
              <button
                className="btn btn-primary"
                onClick={() => { setResult(null); setMessage(""); }}
              >
                🔍 Analyze Another Email
              </button>
              <button
                className="btn btn-secondary"
                onClick={() => navigate("/history")}
              >
                📋 View All Results
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="site-footer" style={{ width: "100%", marginTop: 40 }}>
        Developed by Aastha Gupta | CSE | AI Project
      </footer>
    </div>
  );
}
