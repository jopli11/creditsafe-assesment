/**
 * SWR hooks for customer list and detail — stale-while-revalidate caching.
 *
 * **Why SWR (not TanStack Query here)?**
 * Small API surface, built-in deduping, and tuple cache keys fit this read-heavy UI
 * without extra boilerplate. For larger apps Query’s devtools and mutations API win.
 *
 * **Cache keys**
 * - List: `["customers", limit, offset]` — each pagination page is its own cache entry.
 * - Detail: `["customer", id]` — or `null` when `id` is undefined so **no request** fires
 *   (important for optional route params).
 *
 * **Revalidation after create**
 * `mutate` with `(key) => key[0] === "customers"` refreshes every list page key so
 * the new row appears after navigating back from `/customers/new`.
 *
 * **submitCustomer**
 * Thin wrapper around `createCustomer` for forms — keeps mutation call sites obvious.
 */

import useSWR from "swr";

import { createCustomer, fetchCustomer, fetchCustomerList } from "@/lib/api-client";
import type { CustomerCreatePayload, CustomerListResponse, CustomerResponse } from "@/types/customer";

export function useCustomersQuery(params: { limit: number; offset: number }) {
  const key: readonly [string, number, number] = ["customers", params.limit, params.offset];
  return useSWR<CustomerListResponse>(key, () =>
    fetchCustomerList({ limit: params.limit, offset: params.offset }),
  );
}

export function useCustomerQuery(id: string | undefined) {
  return useSWR<CustomerResponse>(id ? ["customer", id] : null, () => fetchCustomer(id as string));
}

export async function submitCustomer(payload: CustomerCreatePayload) {
  return createCustomer(payload);
}
