/**
 * Read-only detail card — contact, request copy, processed `response_data`.
 *
 * **`response_data`**
 * Populated server-side by `_build_response_data` today (deterministic placeholder).
 * Interview narrative: in production this would aggregate scoring / verification APIs.
 *
 * **Dates**
 * `created_at` rendered with `toLocaleString()`; falls back to raw string if parse fails.
 *
 * **Skeleton**
 * `CustomerDetailSkeleton` avoids layout jump while SWR loads.
 */
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Skeleton } from "@/components/ui/skeleton";
import type { CustomerResponse } from "@/types/customer";

export function CustomerDetailSkeleton() {
  return (
    <div className="space-y-3">
      <Skeleton className="h-8 w-64" />
      <Skeleton className="h-24 w-full" />
      <Skeleton className="h-24 w-full" />
    </div>
  );
}

export function CustomerDetail({ customer }: { customer: CustomerResponse }) {
  const created = new Date(customer.created_at);

  return (
    <Card>
      <CardHeader>
        <CardTitle>{customer.name}</CardTitle>
        <CardDescription>
          Created {Number.isNaN(created.getTime()) ? customer.created_at : created.toLocaleString()}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4 text-sm">
        <div>
          <p className="font-medium text-foreground">Contact</p>
          <p className="text-muted-foreground">{customer.email}</p>
          <p className="text-muted-foreground">{customer.phone}</p>
        </div>
        <div>
          <p className="font-medium text-foreground">Request</p>
          <p className="whitespace-pre-wrap text-muted-foreground">{customer.request_details}</p>
        </div>
        <div>
          <p className="font-medium text-foreground">Processed response</p>
          <p className="whitespace-pre-wrap text-muted-foreground">{customer.response_data}</p>
        </div>
      </CardContent>
    </Card>
  );
}
