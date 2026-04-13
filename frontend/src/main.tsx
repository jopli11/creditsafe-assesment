/**
 * Application bootstrap — React 19 `createRoot`, client-side `BrowserRouter`.
 *
 * **StrictMode** — double-invokes render in dev to surface unsafe side effects.
 *
 * **Sonner** (`<Toaster />`) — global toast host for success/error after form submit;
 * `richColors` + top-right matches common dashboard UX. Toasts are declared here so
 * any route can fire `toast.*` without mounting a provider per page.
 *
 * **Styles** — `./index.css` pulls in Tailwind layers + design tokens (shadcn-style).
 */
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "sonner";

import App from "./App";
import "./index.css";

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Root element #root not found");
}

createRoot(rootElement).render(
  <StrictMode>
    <BrowserRouter>
      <App />
      <Toaster richColors closeButton position="top-right" />
    </BrowserRouter>
  </StrictMode>,
);
