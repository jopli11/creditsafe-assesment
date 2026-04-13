/**
 * Vitest + jsdom: component tests under `tests/`, `@` alias matches Vite.
 * `setupFiles` loads Testing Library matchers; `globals` enables `describe`/`it` without imports.
 */
import path from "node:path";
import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
    setupFiles: ["./tests/setup.ts"],
    include: ["./tests/**/*.test.{ts,tsx}"],
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
