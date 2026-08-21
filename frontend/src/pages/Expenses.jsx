import React, { useEffect, useState } from "react";
import { createExpense, fetchExpenses } from "../api.js";
import ExpenseCard from "../components/ExpenseCard.jsx";

export default function Expenses({ user }) {
  const [expenses, setExpenses] = useState([]);
  const [form, setForm] = useState({
    title: "",
    description: "",
    amount: "",
    category: "travel"
  });
  const [status, setStatus] = useState("all");

  async function refresh(nextStatus = status) {
    setExpenses(await fetchExpenses(nextStatus));
  }

  useEffect(() => {
    refresh();
  }, []);

  async function submit(event) {
    event.preventDefault();
    if (!form.title || Number(form.amount) <= 0) {
      alert("Title and positive amount are required");
      return;
    }
    await createExpense({ ...form, amount: Number(form.amount) });
    setForm({ title: "", description: "", amount: "", category: "travel" });
    refresh();
  }

  return (
    <section className="workspace">
      <div className="panel">
        <h2>Submit expense</h2>
        <form onSubmit={submit} className="expense-form">
          <input
            placeholder="Title"
            value={form.title}
            onChange={(event) => setForm({ ...form, title: event.target.value })}
          />
          <textarea
            placeholder="Description"
            value={form.description}
            onChange={(event) => setForm({ ...form, description: event.target.value })}
          />
          <input
            placeholder="Amount"
            value={form.amount}
            onChange={(event) => setForm({ ...form, amount: event.target.value })}
          />
          <select
            value={form.category}
            onChange={(event) => setForm({ ...form, category: event.target.value })}
          >
            <option value="travel">Travel</option>
            <option value="meals">Meals</option>
            <option value="software">Software</option>
            <option value="office">Office</option>
          </select>
          <button type="submit">Submit</button>
        </form>
      </div>

      <div className="panel">
        <div className="list-heading">
          <div>
            <h2>{user.display_name}'s expenses</h2>
            <p className="small">Safe display path: {user.email}</p>
          </div>
          <select
            value={status}
            onChange={(event) => {
              setStatus(event.target.value);
              refresh(event.target.value);
            }}
          >
            <option value="all">All</option>
            <option value="pending">Pending</option>
            <option value="approved">Approved</option>
            <option value="rejected">Rejected</option>
          </select>
        </div>
        <div className="expense-list">
          {expenses.map((expense) => (
            <ExpenseCard key={expense.id} expense={expense} onChanged={refresh} />
          ))}
        </div>
      </div>
    </section>
  );
}
