import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRegister, saveAuth } from "../services/api";
import "../App.css";

export default function Register() {
  const navigate = useNavigate();
  const [form, setForm] = useState({ name: "", email: "", password: "", confirmPassword: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) =>
    setForm((p) => ({ ...p, [e.target.name]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(""); setSuccess("");
    if (!form.name || !form.email || !form.password || !form.confirmPassword) {
      setError("Please fill in all fields"); return;
    }
    if (form.password !== form.confirmPassword) {
      setError("Passwords do not match"); return;
    }
    if (form.password.length < 6) {
      setError("Password must be at least 6 characters"); return;
    }
    setLoading(true);
    try {
      const data = await apiRegister({
        name: form.name, email: form.email, password: form.password,
      });
      saveAuth(data.token, data.user);
      setSuccess("Account created! Redirecting...");
      setTimeout(() => navigate("/dashboard"), 1200);
    } catch (err) {
      setError(err.message || "Registration failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-bg">
      <div className="auth-card">
        <span className="auth-icon">✨</span>
        <h1 className="auth-title">Create Account</h1>
        <p className="auth-subtitle">Join SpamGuard — protect your inbox with AI</p>

        {error && <div className="alert alert-error">⚠️ {error}</div>}
        {success && <div className="alert alert-success">✅ {success}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Full Name</label>
            <input type="text" name="name" placeholder="John Doe"
              value={form.name} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label className="form-label">Email Address</label>
            <input type="email" name="email" placeholder="you@example.com"
              value={form.email} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label className="form-label">Password</label>
            <input type="password" name="password" placeholder="Min. 6 characters"
              value={form.password} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label className="form-label">Confirm Password</label>
            <input type="password" name="confirmPassword" placeholder="Repeat password"
              value={form.confirmPassword} onChange={handleChange} />
          </div>
          <button type="submit" className="btn btn-primary" style={{ marginTop: 8 }} disabled={loading}>
            {loading ? "⏳ Creating..." : "Create Account →"}
          </button>
        </form>

        <div className="auth-link">
          Already have an account? <a href="/">Sign in</a>
        </div>
      </div>
    </div>
  );
}
