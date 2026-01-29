import React, { useEffect, useState } from "react";
import { getSummary } from "../api";

export default function AnalyticsPage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    getSummary()
      .then(res => setData(res))
      .catch(err => console.error("Analytics error:", err));
  }, []);

  if (!data) return <div style={{ padding: 20 }}>Loading analytics...</div>;

  const { global, per_user } = data;

  return (
    <div style={{ padding: 20 }}>
      <h2>Product Analytics</h2>

      {/* Global Summary */}
      <section style={{ marginTop: 30 }}>
        <h3>Global Counts</h3>
        <table border="1" cellPadding="6">
          <thead>
            <tr>
              <th>Product</th>
              <th>Views</th>
              <th>Add to Cart</th>
            </tr>
          </thead>
          <tbody>
            {Array.from(new Set([
              ...Object.keys(global.views || {}),
              ...Object.keys(global.add_to_cart || {})
            ])).map(pid => (
              <tr key={pid}>
                <td>{pid}</td>
                <td>{global.views?.[pid] || 0}</td>
                <td>{global.add_to_cart?.[pid] || 0}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* Per User Breakdown */}
      <section style={{ marginTop: 30 }}>
        <h3>Per User Breakdown</h3>

        {Object.keys(per_user.views || {}).map(pid => (
          <div key={pid} style={{ marginBottom: 20 }}>
            <h4>Product {pid}</h4>

            <table border="1" cellPadding="6">
              <thead>
                <tr>
                  <th>User</th>
                  <th>Views</th>
                  <th>Add to Cart</th>
                </tr>
              </thead>
              <tbody>
                {Array.from(new Set([
                  ...Object.keys(per_user.views[pid] || {}),
                  ...Object.keys(per_user.add_to_cart?.[pid] || {})
                ])).map(uid => (
                  <tr key={uid}>
                    <td>{uid}</td>
                    <td>{per_user.views?.[pid]?.[uid] || 0}</td>
                    <td>{per_user.add_to_cart?.[pid]?.[uid] || 0}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </section>
    </div>
  );
}
