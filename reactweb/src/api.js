// src/api.js
import axios from "axios";

const API = "http://localhost:8000";

export const getEvents = () => axios.get(`${API}/analytics/events`);
export const getSummary = () => axios.get(`${API}/analytics/summary`);
export const getTopProducts = () => axios.get(`${API}/analytics/top`);
export const getDaily = () => axios.get(`${API}/analytics/daily`);
export const getUserSummary = () => axios.get(`${API}/analytics/user-summary`);
