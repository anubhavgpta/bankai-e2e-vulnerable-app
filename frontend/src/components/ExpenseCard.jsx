import React from "react";
import ReceiptUpload from "./ReceiptUpload.jsx";

export default function ExpenseCard({ expense, onChanged }) {
  return (
    <article className="expense-card">
      <div>
        <h3>{expense.title}</h3>
        <p className="description" dangerouslySetInnerHTML={{ __html: expense.description }} />
        <p className="small">Category: {expense.category}</p>
      </div>
      <div className="expense-meta">
        <strong>${Number(expense.amount).toFixed(2)}</strong>
        <span className={`status ${expense.status}`}>{expense.status}</span>
      </div>
      <ReceiptUpload expenseId={expense.id} onUploaded={onChanged} />
    </article>
  );
}
