import axios from "axios";

export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
export const ANALYTICS_KEY = __BANKAI_PUBLIC_ANALYTICS_KEY__;

const api = axios.create({
  baseURL: API_BASE_URL
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("bankai_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export async function login(email, password) {
  const response = await api.post("/api/users/login", { email, password });
  localStorage.setItem("bankai_token", response.data.access_token);
  localStorage.setItem("bankai_user", JSON.stringify(response.data.user));
  return response.data;
}

export async function fetchExpenses(status = "all") {
  const response = await api.get("/api/expenses", { params: { status } });
  return response.data;
}

export async function createExpense(payload) {
  const response = await api.post("/api/expenses", payload);
  return response.data;
}

export async function fetchAdminExpenses() {
  const response = await api.get("/api/admin/expenses");
  return response.data;
}

export async function approveExpense(id, status, note) {
  const response = await api.post(`/api/admin/expenses/${id}/approve`, { status, note });
  return response.data;
}

export async function uploadReceipt(expenseId, file) {
  const formData = new FormData();
  formData.append("receipt", file, file.name);
  const response = await api.post(`/api/expenses/${expenseId}/receipt`, formData);
  return response.data;
}

export default api;
