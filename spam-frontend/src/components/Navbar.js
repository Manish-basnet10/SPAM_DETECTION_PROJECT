import React from "react";
import { useLocation, useNavigate, Link } from "react-router-dom";
import { getUser, clearAuth, isLoggedIn } from "../services/api";
import "../App.css";

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const user = getUser();
  const isAuth = location.pathname === "/" || location.pathname === "/register";

  const isActive = (path) => location.pathname === path;

  const handleLogout = () => {
    clearAuth();
    navigate("/");
  };

  return (
    <nav className="navbar">
      {/* Left: Shield + MailGuard */}
      <Link to={isLoggedIn() ? "/dashboard" : "/"} className="navbar-logo">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" style={{ color: "#fff" }}>
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" />
        </svg>
        MailGuard
      </Link>

      {/* Right: links or tagline */}
      {!isAuth && isLoggedIn() ? (
        <div className="navbar-links">
          <Link to="/dashboard" className={`nav-link ${isActive("/dashboard") ? "active" : ""}`}>
            📊 Dashboard
          </Link>
          <Link to="/spam" className={`nav-link ${isActive("/spam") ? "active" : ""}`}>
            🔍 Check Spam
          </Link>
          <Link to="/history" className={`nav-link ${isActive("/history") ? "active" : ""}`}>
            📋 History
          </Link>
          {user && <span className="nav-user">👤 {user.name}</span>}
          <button className="btn-logout-nav" onClick={handleLogout}>Sign Out</button>
        </div>
      ) : (
        <span className="navbar-tagline">AI-Powered Spam Detection</span>
      )}
    </nav>
  );
}
