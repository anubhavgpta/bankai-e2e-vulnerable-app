import React, { useState } from "react";
import { uploadReceipt } from "../api.js";

export default function ReceiptUpload({ expenseId, onUploaded }) {
  const [message, setMessage] = useState("");

  async function handleChange(event) {
    const file = event.target.files[0];
    if (!file) {
      return;
    }
    if (!file.name) {
      setMessage("Receipt name is required");
      return;
    }
    try {
      const result = await uploadReceipt(expenseId, file);
      setMessage(`Uploaded ${result.receipt_path}`);
      onUploaded();
    } catch (err) {
      setMessage(err.response?.data?.detail || err.message);
    }
  }

  return (
    <label className="upload">
      Receipt
      <input type="file" onChange={handleChange} />
      {message ? <span>{message}</span> : null}
    </label>
  );
}
