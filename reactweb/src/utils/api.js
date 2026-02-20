import axios from "axios";

const api = axios.create({
  // baseURL: "http://localhost:8000"
  baseURL: "https://reco-3-4mat.onrender.com"
  
});

api.interceptors.request.use((config) => {
  const userId = localStorage.getItem("user_id") || "guest_user";

  config.headers["X-User-ID"] = userId;

  return config;
});

export default api;
