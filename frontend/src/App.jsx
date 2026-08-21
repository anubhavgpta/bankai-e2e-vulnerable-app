import React, { useMemo, useState } from "react";
import Login from "./pages/Login.jsx";
import Expenses from "./pages/Expenses.jsx";
import Admin from "./pages/Admin.jsx";
import { ANALYTICS_KEY } from "./api.js";

export default function App() {
  const [user, setUser] = useState(() => {
    const raw = localStorage.getItem("bankai_user");
    return raw ? JSON.parse(raw) : null;
  });
  const [page, setPage] = useState("expenses");

  const publicConfig = useMemo(
    () => ({
      analyticsKey: ANALYTICS_KEY,
      supportEmail: "finance-help@bankai.local"
    }),
    []
  );

  function logout() {
    localStorage.removeItem("bankai_token");
    localStorage.removeItem("bankai_user");
    setUser(null);
  }

  if (!user) {
    return <Login onLogin={setUser} publicConfig={publicConfig} />;
  }

  return (
    <div className="shell">
      <header className="topbar">
        <div>
          <p className="eyebrow">Internal finance</p>
          <h1>Expense Approval Portal</h1>
        </div>
        <nav>
          <button onClick={() => setPage("expenses")}>Expenses</button>
          <button onClick={() => setPage("admin")}>Admin</button>
          <button onClick={logout}>Sign out</button>
        </nav>
      </header>

      <main>
        {page === "expenses" ? <Expenses user={user} /> : <Admin user={user} />}
      </main>
    </div>
  );
}
