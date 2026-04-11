import { useCallback, useState } from "react";

import { CustomerForm } from "@/components/customers/customer-form";
import { CustomerList } from "@/components/customers/customer-list";
import { PageLayout } from "@/components/layout/page-layout";
import { useCustomersQuery } from "@/hooks/use-customers";

const PAGE_SIZE = 20;

export function CustomersPage() {
  const [offset, setOffset] = useState(0);
  const { data, error, isLoading, mutate } = useCustomersQuery({
    limit: PAGE_SIZE,
    offset,
  });

  const onCreated = useCallback(async () => {
    await mutate();
  }, [mutate]);

  return (
    <PageLayout>
      <CustomerForm onCreated={onCreated} />
      <section className="space-y-3">
        <div className="flex items-center justify-between gap-2">
          <h2 className="text-lg font-semibold tracking-tight">Customers</h2>
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
