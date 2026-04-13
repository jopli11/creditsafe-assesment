/**
 * SWR hooks for customer list/detail and a thin create wrapper for forms.
 */
import useSWR from "swr";

import { createCustomer, fetchCustomer, fetchCustomerList } from "@/lib/api-client";
import type { CustomerCreatePayload, CustomerListResponse, CustomerResponse } from "@/types/customer";

export function useCustomersQuery(params: { limit: number; offset: number }) {
  // Tuple key: each pagination window is its own cache entry
  const key: readonly [string, number, number] = ["customers", params.limit, params.offset];
  return useSWR<CustomerListResponse>(key, () =>
    fetchCustomerList({ limit: params.limit, offset: params.offset }),
  );
}

export function useCustomerQuery(id: string | undefined) {
  // null key skips the fetch when id is missing (optional route params)
  return useSWR<CustomerResponse>(id ? ["customer", id] : null, () => fetchCustomer(id as string));
}

export async function submitCustomer(payload: CustomerCreatePayload) {
  return createCustomer(payload);
}
