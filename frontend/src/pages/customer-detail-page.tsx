/**
 * Route: `/customers/:id` — single-customer view driven by URL param.
 *
 * **Data**
 * `useCustomerQuery(id)` — SWR key `null` when `id` missing (should not happen here).
 *
 * **Error UX**
 * - `ApiError` + status **404** → friendly “Customer not found” (bad bookmark / deleted row).
 * - Other errors → generic load failure (network, 500).
 * - **Loading:** skeleton until `data` exists.
 */
import { Link, useParams } from "react-router-dom";

import { CustomerDetail, CustomerDetailSkeleton } from "@/components/customers/customer-detail";
import { PageLayout } from "@/components/layout/page-layout";
import { Button } from "@/components/ui/button";
import { useCustomerQuery } from "@/hooks/use-customers";
import { ApiError } from "@/lib/api-client";

export function CustomerDetailPage() {
  const { id } = useParams();
  const { data, error, isLoading } = useCustomerQuery(id);

  const notFound = error instanceof ApiError && error.status === 404;

  return (
    <PageLayout>
      <div className="flex flex-wrap items-center justify-between gap-3">
        <Button variant="outline" size="sm" asChild>
          <Link to="/customers">Back to directory</Link>
        </Button>
      </div>

      {notFound ? (
        <p className="text-sm text-muted-foreground" role="alert">
          Customer not found.
        </p>
      ) : null}
      {!notFound && error ? (
        <p className="text-sm text-destructive" role="alert">
          Unable to load this customer.
        </p>
      ) : null}
      {isLoading && !data ? <CustomerDetailSkeleton /> : null}
      {data ? <CustomerDetail customer={data} /> : null}
    </PageLayout>
  );
}
