import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { CustomerDetail } from "@/components/customers/customer-detail";

describe("CustomerDetail", () => {
  it("renders customer fields", () => {
    render(
      <CustomerDetail
        customer={{
          id: "00000000-0000-4000-8000-000000000001",
          name: "Jamie",
          email: "jamie@example.com",
          phone: "5551111",
          request_details: "Need help",
          response_data: "Processed",
          created_at: "2025-06-01T12:00:00.000Z",
        }}
      />,
    );

    expect(screen.getByText("Jamie")).toBeInTheDocument();
    expect(screen.getByText("jamie@example.com")).toBeInTheDocument();
    expect(screen.getByText("Need help")).toBeInTheDocument();
    expect(screen.getByText("Processed")).toBeInTheDocument();
  });
});
