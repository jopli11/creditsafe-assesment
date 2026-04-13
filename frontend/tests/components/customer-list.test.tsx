/**
 * List tests: render with `MemoryRouter`, assert pagination summary and Next callback.
 */
import { render, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { MemoryRouter } from "react-router-dom";
import { describe, expect, it, vi } from "vitest";

import { CustomerList } from "@/components/customers/customer-list";

const sample = [
  {
    id: "00000000-0000-4000-8000-000000000001",
    name: "Alex",
    email: "alex@example.com",
    phone: "5550000",
    request_details: "Hi",
    response_data: "OK",
    created_at: "2025-01-01T00:00:00Z",
  },
];

describe("CustomerList", () => {
  it("renders rows and pagination summary", () => {
    render(
      <MemoryRouter>
        <CustomerList
          items={sample}
          isLoading={false}
          limit={20}
          offset={0}
          total={1}
          onPrev={vi.fn()}
          onNext={vi.fn()}
        />
      </MemoryRouter>,
    );

    // Mobile cards and desktop table are both in the DOM (Tailwind breakpoints
    // do not hide nodes in jsdom), so the name appears more than once.
    expect(screen.getAllByText("Alex").length).toBeGreaterThanOrEqual(1);
    expect(screen.getByText(/showing\s*1\s*[–-]\s*1\s+of\s+1/i)).toBeInTheDocument();
  });

  it("invokes pagination callbacks", async () => {
    const user = userEvent.setup();
    const onNext = vi.fn();
    render(
      <MemoryRouter>
        <CustomerList
          items={sample}
          isLoading={false}
          limit={20}
          offset={0}
          total={40}
          onPrev={vi.fn()}
          onNext={onNext}
        />
      </MemoryRouter>,
    );

    await user.click(screen.getByRole("button", { name: /next/i }));
    expect(onNext).toHaveBeenCalled();
  });
});
