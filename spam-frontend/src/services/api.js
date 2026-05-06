// =============================================
// Centralized API Service
// All backend calls go through here.
// =============================================

const API_BASE = process.env.REACT_APP_API_URL || "http://127.0.0.1:5001";


// Helper: get JWT from localStorage
const getToken = () => localStorage.getItem("token");

// Helper: build auth headers
const authHeaders = () => ({
  "Content-Type": "application/json",
  Authorization: `Bearer ${getToken()}`,
});

// Helper: handle response (throws on non-ok)
const handleResponse = async (res) => {
  const data = await res.json();
  if (!res.ok) {
    throw new Error(data.error || "Something went wrong");
  }
  return data;
};

// ─── Auth ───────────────────────────────────────────────
export const apiRegister = async ({ name, email, password }) => {
  const res = await fetch(`${API_BASE}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ name, email, password }),
  });
  return handleResponse(res);
};

export const apiLogin = async ({ email, password }) => {
  const res = await fetch(`${API_BASE}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  return handleResponse(res);
};

// ─── Health ─────────────────────────────────────────────
export const apiHealth = async () => {
  const res = await fetch(`${API_BASE}/health`);
  return handleResponse(res);
};

// ─── Predict ────────────────────────────────────────────
export const apiPredict = async (message) => {
  const res = await fetch(`${API_BASE}/predict`, {
    method: "POST",
    headers: authHeaders(),
    body: JSON.stringify({ message }),
  });
  return handleResponse(res);
};

// ─── History ────────────────────────────────────────────
export const apiHistory = async () => {
  const res = await fetch(`${API_BASE}/history`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
};

// ─── Dashboard Stats ────────────────────────────────────
export const apiStats = async () => {
  const res = await fetch(`${API_BASE}/dashboard/stats`, {
    headers: authHeaders(),
  });
  return handleResponse(res);
};

// ─── Local Auth Helpers ─────────────────────────────────
export const saveAuth = (token, user) => {
  localStorage.setItem("token", token);
  localStorage.setItem("user", JSON.stringify(user));
};

export const clearAuth = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
};

export const getUser = () => {
  try {
    return JSON.parse(localStorage.getItem("user"));
  } catch {
    return null;
  }
};

export const isLoggedIn = () => !!getToken() && !!getUser();
