/** useCustomers / useCustomerQuery: fetch mock + null key behaviour. */
import { renderHook, waitFor } from "@testing-library/react";
import type { ReactNode } from "react";
import { SWRConfig } from "swr";
import { afterEach, describe, expect, it, vi } from "vitest";

import { useCustomerQuery, useCustomersQuery } from "@/hooks/use-customers";

function SwrTestWrapper({ children }: { children: ReactNode }) {
  // No request dedupe delay — tests resolve on first revalidation
  return <SWRConfig value={{ dedupingInterval: 0 }}>{children}</SWRConfig>;
}

const originalFetch = globalThis.fetch;

afterEach(() => {
  globalThis.fetch = originalFetch;
});

describe("useCustomersQuery", () => {
  it("loads customer list", async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      text: async () =>
        JSON.stringify({
          items: [],
          total: 0,
          limit: 20,
          offset: 0,
        }),
    }) as unknown as typeof fetch;

    const { result } = renderHook(() => useCustomersQuery({ limit: 20, offset: 0 }), {
      wrapper: SwrTestWrapper,
    });

    await waitFor(() => {
      expect(result.current.data?.total).toBe(0);
    });
  });
});

describe("useCustomerQuery", () => {
  it("skips fetch when id is missing", () => {
    const { result } = renderHook(() => useCustomerQuery(undefined), { wrapper: SwrTestWrapper });
    expect(result.current.data).toBeUndefined();
    expect(result.current.isLoading).toBe(false);
  });
});
