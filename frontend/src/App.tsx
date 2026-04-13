/**
 * Client-side route table for the customer SPA (no file-based routing).
 */
import { Navigate, Route, Routes } from "react-router-dom";

import { CustomerDetailPage } from "@/pages/customer-detail-page";
import { CustomersPage } from "@/pages/customers-page";
import { NewCustomerPage } from "@/pages/new-customer-page";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/customers" replace />} />
      {/* Register /new before /:id so "new" is not captured as a UUID param */}
      <Route path="/customers/new" element={<NewCustomerPage />} />
      <Route path="/customers" element={<CustomersPage />} />
      <Route path="/customers/:id" element={<CustomerDetailPage />} />
      <Route path="*" element={<Navigate to="/customers" replace />} />
    </Routes>
  );
}
