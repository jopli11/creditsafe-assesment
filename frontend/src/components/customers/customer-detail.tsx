/**
 * Read-only detail: contact, request text, and stored `response_data`.
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
          {/* Fallback keeps bad/legacy ISO strings readable */}
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
          {/* Populated server-side today; production might aggregate external APIs */}
          <p className="whitespace-pre-wrap text-muted-foreground">{customer.response_data}</p>
        </div>
      </CardContent>
    </Card>
  );
}
