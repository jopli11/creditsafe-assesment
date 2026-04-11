/**
 * SWR hooks for customer list/detail (`client-swr-dedup` pattern).
 * Keys are full URLs so dedupe works across components mounting the same resource.
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
