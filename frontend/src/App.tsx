/**
 * React Router route table (client-side only — no SSR).
 *
 * **Route order**
 * Register `/customers/new` **before** `/customers/:id`. Otherwise `:id` captures
 * the literal string `"new"` and the detail page tries to load a UUID named "new"
 * → confusing 404/validation errors.
 *
 * **Redirects**
 * `/` and `*` send users to `/customers` so the directory is the home surface.
 *
 * **Why React Router (not Next.js)?**
 * SPA + static hosting is enough for this CRUD UI; no need for SSR or file-based routes.
 */
import { Navigate, Route, Routes } from "react-router-dom";

import { CustomerDetailPage } from "@/pages/customer-detail-page";
import { CustomersPage } from "@/pages/customers-page";
import { NewCustomerPage } from "@/pages/new-customer-page";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/customers" replace />} />
      <Route path="/customers/new" element={<NewCustomerPage />} />
      <Route path="/customers" element={<CustomersPage />} />
      <Route path="/customers/:id" element={<CustomerDetailPage />} />
      <Route path="*" element={<Navigate to="/customers" replace />} />
    </Routes>
  );
}
