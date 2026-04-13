/**
 * Route `/customers`: paginated directory.
 */
import { useState } from "react";
import { Link } from "react-router-dom";

import { CustomerList } from "@/components/customers/customer-list";
import { PageLayout } from "@/components/layout/page-layout";
import { Button } from "@/components/ui/button";
import { useCustomersQuery } from "@/hooks/use-customers";

const PAGE_SIZE = 20;

export function CustomersPage() {
  const [offset, setOffset] = useState(0);
  // SWR key includes offset — changing page refetches the slice
  const { data, error, isLoading } = useCustomersQuery({
    limit: PAGE_SIZE,
    offset,
  });

  return (
    <PageLayout>
      <section className="space-y-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <h2 className="text-lg font-semibold tracking-tight">Customers</h2>
          {/* asChild: Radix slot — link semantics with button styling */}
          <Button size="sm" asChild>
            <Link to="/customers/new">New request</Link>
          </Button>
        </div>
        {error ? (
          <p className="text-sm text-destructive" role="alert">
            Failed to load customers. Is the API running?
          </p>
        ) : null}
        <CustomerList
          items={data?.items ?? []}
          isLoading={isLoading}
          limit={PAGE_SIZE}
          offset={offset}
          total={data?.total ?? 0}
          onPrev={() => setOffset((o) => Math.max(0, o - PAGE_SIZE))}
          onNext={() => setOffset((o) => o + PAGE_SIZE)}
        />
      </section>
    </PageLayout>
  );
}
