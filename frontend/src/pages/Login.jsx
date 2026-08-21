import React, { useState } from "react";
import { login } from "../api.js";

export default function Login({ onLogin, publicConfig }) {
  const [email, setEmail] = useState("employee@bankai.local");
  const [password, setPassword] = useState("password123");
  const [error, setError] = useState("");

  async function submit(event) {
    event.preventDefault();
    setError("");
    try {
      const result = await login(email, password);
      onLogin(result.user);
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
  }

  return (
    <main className="login-page">
      <section className="login-panel">
        <p className="eyebrow">Bankai Finance</p>
        <h1>Sign in</h1>
        <form onSubmit={submit}>
          <label>
            Email
            <input value={email} onChange={(event) => setEmail(event.target.value)} />
          </label>
          <label>
            Password
            <input
              type="password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
          </label>
          {error ? <p className="error">{error}</p> : null}
          <button type="submit">Continue</button>
        </form>
        <p className="small">Analytics: {publicConfig.analyticsKey}</p>
      </section>
    </main>
  );
}
