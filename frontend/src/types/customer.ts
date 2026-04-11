/** Mirrors backend Pydantic models — keep in sync for interview walkthroughs. */

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
