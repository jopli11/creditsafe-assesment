import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { describe, expect, it, vi } from "vitest";

import { CustomerForm } from "@/components/customers/customer-form";
import { submitCustomer } from "@/hooks/use-customers";

vi.mock("@/hooks/use-customers", async (importOriginal) => {
  const actual = await importOriginal<typeof import("@/hooks/use-customers")>();
  return {
    ...actual,
    submitCustomer: vi.fn().mockResolvedValue({
      id: "00000000-0000-4000-8000-000000000099",
      status: "success",
      message: "Customer data stored successfully",
    }),
  };
});

describe("CustomerForm", () => {
  it("shows validation messages for empty submit", async () => {
    const user = userEvent.setup();
    render(<CustomerForm />);

    await user.click(screen.getByRole("button", { name: /submit request/i }));

    expect(await screen.findByText(/name is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(await screen.findByText(/phone number is required/i)).toBeInTheDocument();
  });

  it("submits valid payload and resets fields", async () => {
    const user = userEvent.setup();
    const onCreated = vi.fn();

    render(<CustomerForm onCreated={onCreated} />);

    await user.type(screen.getByRole("textbox", { name: "Name" }), "Taylor Morgan");
    await user.type(screen.getByRole("textbox", { name: "Email" }), "taylor@example.com");
    await user.type(screen.getByRole("textbox", { name: "Phone" }), "07700900123");
    await user.type(screen.getByRole("textbox", { name: "Request details" }), "Please verify billing address.");

    await user.click(screen.getByRole("button", { name: /submit request/i }));

    await waitFor(() => {
      expect(submitCustomer).toHaveBeenCalledWith(
        expect.objectContaining({
          name: "Taylor Morgan",
          email: "taylor@example.com",
          phone: "07700900123",
        }),
      );
    });
    await waitFor(() => {
      expect(onCreated).toHaveBeenCalled();
    });
    await waitFor(() => {
      expect(screen.getByRole("textbox", { name: "Name" })).toHaveValue("");
    });
  });
});
