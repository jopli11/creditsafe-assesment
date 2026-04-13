/**
 * Route: `/customers/new` — dedicated create flow (not a modal) for deep-linking
 * and clear back-button behaviour.
 *
 * **After successful POST**
 * 1. `mutate` with a key filter revalidates **all** `["customers", …]` caches (any
 *    limit/offset) so whichever list page you land on includes the new row.
 * 2. `navigate("/customers")` returns to the directory without a full document reload.
 */
import { useNavigate } from "react-router-dom";
import { useSWRConfig } from "swr";

import { CustomerForm } from "@/components/customers/customer-form";
import { PageLayout } from "@/components/layout/page-layout";

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
