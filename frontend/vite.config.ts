/**
 * Vite dev/build: React plugin, `@` → `./src`, dev server on 5173.
 */
import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    host: true, // reachable from host when Vite runs in Docker
  },
});
