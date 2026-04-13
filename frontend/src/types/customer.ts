/**
 * TypeScript types for API JSON — mirrors `backend/app/schemas/customer.py`.
 *
 * **Why manual types (not OpenAPI codegen)?**
 * Keeps the assessment self-contained; in production you’d generate from `/openapi.json`
 * or use `openapi-typescript` in CI to prevent drift.
 *
 * **Conventions**
 * - IDs are **strings** in JSON (UUID serialization).
 * - `created_at` is ISO 8601 string from the API.
 */

export type CustomerSubmitResponse = {
  id: string;
  status: string;
  message: string;
};

export type CustomerResponse = {
  id: string;
  name: string;
  email: string;
  phone: string;
  request_details: string;
  response_data: string;
  created_at: string;
};

export type CustomerListResponse = {
  items: CustomerResponse[];
  total: number;
  limit: number;
  offset: number;
};

export type CustomerCreatePayload = {
  name: string;
  email: string;
  phone: string;
  request_details: string;
};
