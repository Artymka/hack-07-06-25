import { defineConfig } from "vite";
import dotenv from "dotenv";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import path from "path";
dotenv.config();

const VITE_BASE_URL = process.env.VITE_BASE_URL;

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "src"),
    },
  },
  define: {
    VITE_BASE_URL: JSON.stringify(VITE_BASE_URL),
  },
});
