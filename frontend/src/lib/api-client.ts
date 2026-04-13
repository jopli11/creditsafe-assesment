/**
 * Typed fetch wrapper for the FastAPI JSON API — central place for base URL, headers, errors.
 *
 * **Base URL**
 * `import.meta.env.VITE_API_BASE_URL` (Vite injects at build time). In Docker Compose
 * this is `http://localhost:8000` because the **browser** on the host calls the API;
 * it is not the internal Docker service name. Fallback `http://localhost:8000` when
 * unset matches local `uvicorn` defaults.
 *
 * **Errors**
 * FastAPI returns `detail` as a string, a list of validation objects `{ loc, msg }`,
 * or nested objects. `formatErrorDetail` normalises those into one message string
 * for toasts and inline UI. `ApiError` keeps `status` + raw `body` so detail pages
 * can treat 404 differently from 500.
 *
 * **Parsing**
 * `parseJsonSafe` reads text first — avoids throw on empty body or non-JSON errors.
 *
 * **Endpoints**
 * `GET /api/customers?limit&offset`, `GET /api/customers/:id`, `POST /api/customers`.
 */

import type { CustomerCreatePayload, CustomerListResponse, CustomerResponse, CustomerSubmitResponse } from "@/types/customer";

export class ApiError extends Error {
  readonly status: number;
  readonly body: unknown;

  constructor(message: string, status: number, body: unknown) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

export function getApiBaseUrl(): string {
  const raw = import.meta.env.VITE_API_BASE_URL;
  if (raw && raw.length > 0) {
    return raw.replace(/\/$/, "");
  }
  return "http://localhost:8000";
}

function formatErrorDetail(body: unknown): string | null {
  if (!body || typeof body !== "object") {
    return null;
  }
  if (!("detail" in body)) {
    return null;
  }
  const detail = (body as { detail: unknown }).detail;
  if (typeof detail === "string") {
    return detail;
  }
  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (item && typeof item === "object" && "msg" in item) {
          return String((item as { msg: unknown }).msg);
        }
        return JSON.stringify(item);
      })
      .join("; ");
  }
  if (detail && typeof detail === "object") {
    return JSON.stringify(detail);
  }
  return String(detail);
}

async function parseJsonSafe(response: Response): Promise<unknown> {
  const text = await response.text();
  if (!text) {
    return null;
  }
  try {
    return JSON.parse(text) as unknown;
  } catch {
    return text;
  }
}

export async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const url = `${getApiBaseUrl()}${path.startsWith("/") ? path : `/${path}`}`;
  const response = await fetch(url, {
    ...init,
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
      ...init?.headers,
    },
  });
  const body = await parseJsonSafe(response);
  if (!response.ok) {
    const message = formatErrorDetail(body) || response.statusText || "Request failed";
    throw new ApiError(message, response.status, body);
  }
  return body as T;
}

export async function fetchCustomerList(params: { limit: number; offset: number }): Promise<CustomerListResponse> {
  const search = new URLSearchParams({
    limit: String(params.limit),
    offset: String(params.offset),
  });
  return apiRequest<CustomerListResponse>(`/api/customers?${search.toString()}`);
}

export async function fetchCustomer(id: string): Promise<CustomerResponse> {
  return apiRequest<CustomerResponse>(`/api/customers/${encodeURIComponent(id)}`);
}

export async function createCustomer(payload: CustomerCreatePayload): Promise<CustomerSubmitResponse> {
  return apiRequest<CustomerSubmitResponse>("/api/customers", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
