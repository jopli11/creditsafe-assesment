/**
 * TypeScript types for API JSON — kept manual here; production might codegen from OpenAPI.
 */

// 201 POST body — UUID as string in JSON
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
  created_at: string; // ISO 8601 from API
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
