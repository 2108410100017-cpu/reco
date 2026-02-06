import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {
  const [userId, setUserId] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = () => {
    if (!userId.trim()) {
      alert("Enter user ID");
      return;
    }

    if (password !== "123") {
      alert("Password is 123 for demo users");
      return;
    }

    // Save logged user
    localStorage.setItem("logged_user", userId);

    alert(`Logged in as ${userId}`);
    navigate("/");
  };

  return (
    <div style={container}>
      <h2>Demo User Login</h2>

      <input
        placeholder="Enter user ID (e.g., user-001)"
        value={userId}
        onChange={(e) => setUserId(e.target.value)}
        style={input}
      />

      <input
        type="password"
        placeholder="Password (123)"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        style={input}
      />

      <button onClick={handleLogin} style={btn}>
        Login
      </button>

      <p style={{ marginTop: "10px", color: "#777" }}>
        Demo users: user-001 → user-200 | Password: 123
      </p>
    </div>
  );
};

export default LoginPage;

const container = {
  maxWidth: "400px",
  margin: "60px auto",
  padding: "20px",
  border: "1px solid #ddd",
  borderRadius: "8px",
  textAlign: "center"
};

const input = {
  width: "100%",
  padding: "10px",
  margin: "10px 0"
};

const btn = {
  background: "#4CAF50",
  color: "white",
  padding: "10px 20px",
  border: "none",
  cursor: "pointer"
};
