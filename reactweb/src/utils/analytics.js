// utils/analytics.js
import axios from "axios";
import { getUserId } from "./userId";

const API = "http://localhost:8000";

export function trackProductView(product_id) {
    logEvent("product_view", product_id);
}

export function trackAddToCart(product_id, quantity = 1) {
    logEvent("add_to_cart", product_id, { quantity });
}

function logEvent(event_type, product_id, metadata = {}) {
    axios.post(`${API}/analytics/track`, {
        event_type,
        product_id,
        user_id: getUserId(),
        metadata,
        timestamp: new Date().toISOString()
    }).catch(err => {
        console.warn("Analytics tracking failed:", err.message);
    });
}

export function track(eventType, productId) {
  fetch("http://localhost:8000/analytics/track", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      event_type: eventType,
      product_id: productId,
      user_id: "guest"
    })
  });
}