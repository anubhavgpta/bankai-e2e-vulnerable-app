import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    proxy: {
      "/api": "http://localhost:8000"
    }
  },
  define: {
    __BANKAI_PUBLIC_ANALYTICS_KEY__: JSON.stringify(
      process.env.VITE_ANALYTICS_KEY || "pk_live_fake_frontend_public_analytics_000"
    )
  }
});
