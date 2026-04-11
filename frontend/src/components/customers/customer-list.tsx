import { Link } from "react-router-dom";

import { CustomerCard } from "@/components/customers/customer-card";
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table";
import type { CustomerResponse } from "@/types/customer";

export function CustomerListSkeleton() {
  return (
    <div className="space-y-2">
      <Skeleton className="h-10 w-full" />
      <Skeleton className="h-10 w-full" />
      <Skeleton className="h-10 w-full" />
    </div>
  );
}

export function CustomerList({
  items,
  isLoading,
  limit,
  offset,
  total,
  onPrev,
  onNext,
}: {
  items: CustomerResponse[];
  isLoading: boolean;
  limit: number;
  offset: number;
  total: number;
  onPrev: () => void;
  onNext: () => void;
}) {
  if (isLoading) {
    return <CustomerListSkeleton />;
  }

  if (items.length === 0) {
    return <p className="text-sm text-muted-foreground">No customers yet — submit the first request above.</p>;
  }

  const start = offset + 1;
  const end = offset + items.length;
  const canPrev = offset > 0;
  const canNext = offset + limit < total;

  return (
    <div className="space-y-4">
      <div className="md:hidden space-y-3">
        {items.map((c) => (
          <CustomerCard.Root key={c.id}>
            <CustomerCard.Header title={c.name} description={c.email} />
            <CustomerCard.Body>
              <p className="text-muted-foreground">{c.phone}</p>
            </CustomerCard.Body>
            <CustomerCard.Footer>
              <CustomerCard.TitleLink id={c.id} label="View details" />
            </CustomerCard.Footer>
          </CustomerCard.Root>
        ))}
      </div>

      <div className="hidden md:block">
        <Table>
          <TableHeader>
            <TableRow>
              <TableHead>Name</TableHead>
              <TableHead>Email</TableHead>
              <TableHead>Phone</TableHead>
              <TableHead className="text-right">Actions</TableHead>
            </TableRow>
          </TableHeader>
          <TableBody>
            {items.map((c) => (
              <TableRow key={c.id}>
                <TableCell className="font-medium">{c.name}</TableCell>
                <TableCell>{c.email}</TableCell>
                <TableCell>{c.phone}</TableCell>
                <TableCell className="text-right">
                  <Button variant="ghost" size="sm" asChild>
                    <Link to={`/customers/${c.id}`}>Details</Link>
                  </Button>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </div>

      <div className="flex flex-wrap items-center justify-between gap-3 text-sm text-muted-foreground">
        <span>
          Showing {start}–{end} of {total}
        </span>
        <div className="flex gap-2">
          <Button type="button" variant="outline" size="sm" onClick={onPrev} disabled={!canPrev}>
            Previous
          </Button>
          <Button type="button" variant="outline" size="sm" onClick={onNext} disabled={!canNext}>
            Next
          </Button>
        </div>
      </div>
    </div>
  );
}
