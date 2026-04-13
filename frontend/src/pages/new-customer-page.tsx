/**
 * Route `/customers/new`: dedicated create flow (deep-linkable, clear back navigation).
 */
import { useNavigate } from "react-router-dom";
import { useSWRConfig } from "swr";

import { CustomerForm } from "@/components/customers/customer-form";
import { PageLayout } from "@/components/layout/page-layout";

export function NewCustomerPage() {
  const navigate = useNavigate();
  const { mutate } = useSWRConfig();

  const handleCreated = async () => {
    // Revalidate every cached list page (any limit/offset) so the new row appears
    await mutate(
      (key) => Array.isArray(key) && key[0] === "customers",
      undefined,
      { revalidate: true },
    );
    navigate("/customers");
  };

  return (
    <PageLayout>
      <CustomerForm onCreated={handleCreated} />
    </PageLayout>
  );
}
