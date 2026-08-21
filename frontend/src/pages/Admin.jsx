import React, { useEffect, useState } from "react";
import { approveExpense, fetchAdminExpenses } from "../api.js";

export default function Admin({ user }) {
  const [expenses, setExpenses] = useState([]);
  const [error, setError] = useState("");

  async function refresh() {
    setError("");
    try {
      setExpenses(await fetchAdminExpenses());
    } catch (err) {
      setError(err.response?.data?.detail || err.message);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  async function decide(expense, status) {
    await approveExpense(expense.id, status, `Reviewed by ${user.email}`);
    refresh();
  }

  return (
    <section className="panel">
      <div className="list-heading">
        <div>
          <h2>Admin approvals</h2>
          <p className="small">Signed in as {user.email}</p>
        </div>
        <button onClick={refresh}>Refresh</button>
      </div>
      {error ? <p className="error">{error}</p> : null}
      <table>
        <thead>
          <tr>
            <th>Employee</th>
            <th>Expense</th>
            <th>Amount</th>
            <th>Status</th>
            <th>Decision</th>
          </tr>
        </thead>
        <tbody>
          {expenses.map((expense) => (
            <tr key={expense.id}>
              <td>{expense.display_name || expense.email}</td>
              <td>
                <strong>{expense.title}</strong>
                <span dangerouslySetInnerHTML={{ __html: expense.description }} />
              </td>
              <td>${Number(expense.amount).toFixed(2)}</td>
              <td>{expense.status}</td>
              <td>
                <button onClick={() => decide(expense, "approved")}>Approve</button>
                <button onClick={() => decide(expense, "rejected")}>Reject</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </section>
  );
}
