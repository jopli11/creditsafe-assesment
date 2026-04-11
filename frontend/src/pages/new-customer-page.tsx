import { useNavigate } from "react-router-dom";
import { useSWRConfig } from "swr";

import { CustomerForm } from "@/components/customers/customer-form";
import { PageLayout } from "@/components/layout/page-layout";

/**
 * Dedicated route for creating a customer so the directory page stays read-focused.
 * After a successful POST, revalidate every cached customer list (any limit/offset)
 * so the new row appears without a full page refresh, then return to the directory.
 */
export function NewCustomerPage() {
  const navigate = useNavigate();
  const { mutate } = useSWRConfig();

  const handleCreated = async () => {
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
