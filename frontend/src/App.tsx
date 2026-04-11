import { Navigate, Route, Routes } from "react-router-dom";

import { CustomerDetailPage } from "@/pages/customer-detail-page";
import { CustomersPage } from "@/pages/customers-page";

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<Navigate to="/customers" replace />} />
      <Route path="/customers" element={<CustomersPage />} />
      <Route path="/customers/:id" element={<CustomerDetailPage />} />
      <Route path="*" element={<Navigate to="/customers" replace />} />
    </Routes>
  );
}
