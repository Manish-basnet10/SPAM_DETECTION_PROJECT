import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiLogin, saveAuth } from "../services/api";
import "../App.css";

export default function Login() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setForm((p) => ({ ...p, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    if (!form.email || !form.password) {
      setError("Please fill in all fields");
      return;
    }
    setLoading(true);
    try {
      const data = await apiLogin(form);
      saveAuth(data.token, data.user);
      navigate("/dashboard");
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-bg">
      <div className="auth-card">
        <span className="auth-icon">🛡️</span>
        <h1 className="auth-title">Welcome Back</h1>
        <p className="auth-subtitle">Sign in to your SpamGuard account</p>

        {error && (
          <div className="alert alert-error">⚠️ {error}</div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input
              type="email"
              name="email"
              placeholder="you@example.com"
              value={form.email}
              onChange={handleChange}
              autoComplete="email"
            />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input
              type="password"
              name="password"
              placeholder="••••••••"
              value={form.password}
              onChange={handleChange}
              autoComplete="current-password"
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary"
            style={{ marginTop: 8 }}
            disabled={loading}
          >
            {loading ? "⏳ Signing in..." : "Sign In →"}
          </button>
        </form>

        <div className="auth-link">
          Don't have an account?{" "}
          <a href="/register">Create one free</a>
        </div>
      </div>
    </div>
  );
}
