import { zodResolver } from "@hookform/resolvers/zod";
import { useState, useTransition } from "react";
import { useForm } from "react-hook-form";
import { toast } from "sonner";
import { z } from "zod";

import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { ApiError } from "@/lib/api-client";
import { submitCustomer } from "@/hooks/use-customers";

const phoneRegex = /^[\d\s\-+().]{7,50}$/;

const customerFormSchema = z.object({
  name: z.string().min(1, "Name is required").max(255),
  email: z.string().email("Enter a valid email"),
  phone: z
    .string()
    .min(7, "Phone is too short")
    .max(50)
    .regex(phoneRegex, "Use digits and common phone symbols only"),
  request_details: z.string().min(1, "Details are required").max(10_000),
});

export type CustomerFormValues = z.infer<typeof customerFormSchema>;

export function CustomerForm({ onCreated }: { onCreated?: () => void | Promise<void> }) {
  const [isPending, startTransition] = useTransition();
  const [serverError, setServerError] = useState<string | null>(null);

  const form = useForm<CustomerFormValues>({
    resolver: zodResolver(customerFormSchema),
    defaultValues: {
      name: "",
      email: "",
      phone: "",
      request_details: "",
    },
  });

  const onSubmit = (values: CustomerFormValues) => {
    setServerError(null);
    startTransition(async () => {
      try {
        const result = await submitCustomer(values);
        toast.success(result.message || "Customer saved");
        form.reset();
        await onCreated?.();
      } catch (err) {
        const message = err instanceof ApiError ? err.message : "Something went wrong";
        setServerError(message);
        toast.error(message);
      }
    });
  };

  return (
    <Card>
      <CardHeader>
        <CardTitle>New customer request</CardTitle>
        <CardDescription>Validated client-side (Zod) and again on the API (Pydantic).</CardDescription>
      </CardHeader>
      <CardContent>
        <form className="space-y-4" onSubmit={form.handleSubmit(onSubmit)} noValidate>
          <div className="grid gap-2">
            <Label htmlFor="name">Name</Label>
            <Input id="name" autoComplete="name" {...form.register("name")} />
            {form.formState.errors.name ? (
              <p className="text-sm text-destructive">{form.formState.errors.name.message}</p>
            ) : null}
          </div>
          <div className="grid gap-2">
            <Label htmlFor="email">Email</Label>
            <Input id="email" type="email" autoComplete="email" {...form.register("email")} />
            {form.formState.errors.email ? (
              <p className="text-sm text-destructive">{form.formState.errors.email.message}</p>
            ) : null}
          </div>
          <div className="grid gap-2">
            <Label htmlFor="phone">Phone</Label>
            <Input id="phone" autoComplete="tel" {...form.register("phone")} />
            {form.formState.errors.phone ? (
              <p className="text-sm text-destructive">{form.formState.errors.phone.message}</p>
            ) : null}
          </div>
          <div className="grid gap-2">
            <Label htmlFor="request_details">Request details</Label>
            <Textarea id="request_details" rows={4} {...form.register("request_details")} />
            {form.formState.errors.request_details ? (
              <p className="text-sm text-destructive">{form.formState.errors.request_details.message}</p>
            ) : null}
          </div>
          {serverError ? <p className="text-sm text-destructive">{serverError}</p> : null}
          <Button type="submit" disabled={isPending}>
            {isPending ? "Submitting…" : "Submit request"}
          </Button>
        </form>
      </CardContent>
    </Card>
  );
}
