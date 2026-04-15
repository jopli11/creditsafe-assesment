/**
 * Application bootstrap: mount the application, routing, global styles, and toast host.
 * Detail (StrictMode, BrowserRouter, Sonner, Tailwind entry) is noted inline below.
 */
import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { Toaster } from "sonner";

import App from "./App";
import "./index.css"; // Tailwind layers + design tokens (shadcn-style)

const rootElement = document.getElementById("root");
if (!rootElement) {
  throw new Error("Root element #root not found");
}

createRoot(rootElement).render(
  // Dev-only: double-invokes render to surface unsafe side effects
  <StrictMode>
    {/* Client-side routing only — no SSR */}
    <BrowserRouter>
      <App />
      {/* Global host: any route can call toast.* without a per-page provider */}
      <Toaster richColors closeButton position="top-right" />
    </BrowserRouter>
  </StrictMode>,
);
