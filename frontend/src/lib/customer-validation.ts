/**
 * Email + UK phone validators shared with `customer-form.tsx` (Zod `superRefine`).
 * Rules mirror `backend/app/schemas/customer.py`; the API always re-validates.
 */

// Character sets aligned with backend regex checks
const EMAIL_ALLOWED = /^[A-Za-z0-9.@_%+-]+$/;
const EMAIL_FULL = /^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$/;

export function validateEmailField(email: string): string | undefined {
  const v = email.trim();
  if (!v) return "Email is required";
  if (v.length > 320) return "Email is too long";

  if (!v.includes("@")) {
    return "Email must include an @ between the name and the domain (e.g. alex@company.com).";
  }

  const at = v.indexOf("@");
  if (v.includes("@", at + 1)) {
    return "Use a single @ symbol (e.g. name@domain.com).";
  }

  const local = v.slice(0, at);
  const domain = v.slice(at + 1);

  if (!local) {
    return "Add something before the @ (your mailbox name, e.g. alex.smith).";
  }
  if (!domain) {
    return "Add the domain after the @ (e.g. gmail.com or company.co.uk).";
  }
  if (!domain.includes(".")) {
    return "The domain after @ needs a dot (e.g. .com, .co.uk, or .org).";
  }
  if (domain.startsWith(".") || domain.endsWith(".")) {
    return "The domain cannot start or end with a dot.";
  }

  const tld = domain.split(".").pop() ?? "";
  if (!/^[A-Za-z]{2,}$/.test(tld)) {
    return "The part after the last dot (like .com or .uk) must be at least 2 letters.";
  }

  if (!EMAIL_ALLOWED.test(v)) {
    return "Email can only use letters, numbers, and . @ _ % + -.";
  }

  if (!EMAIL_FULL.test(v)) {
    return "That does not look like a complete email yet — check spelling around the name and domain.";
  }

  return undefined;
}

export function validateUkPhoneField(phone: string): string | undefined {
  const v = phone.trim();
  if (!v) return "Phone number is required";
  if (v.length > 50) return "Phone number is too long";

  if (!/^[\d\s\-+().]+$/.test(v)) {
    return "Use only digits, spaces, hyphens, brackets, and +. Letters and other symbols are not valid in a phone number.";
  }

  const digits = v.replace(/\D/g, "");
  if (!digits.length) {
    return "Enter at least one digit in your phone number.";
  }

  // Match backend: +44 / 44… → leading 0 for UK rules
  let d = digits;
  if (d.startsWith("44") && d.length >= 10) {
    d = `0${d.slice(2)}`;
  }

  if (!d.startsWith("0")) {
    return "Use a UK number starting with 0 (e.g. 020 7946 0958) or with +44 (e.g. +44 20 7946 0958).";
  }

  if (d.length < 10) {
    return "UK numbers need at least 10 digits including the leading 0. Add the rest of the number.";
  }
  if (d.length > 11) {
    return "UK numbers are at most 11 digits including the leading 0. Check for extra digits.";
  }

  if (d.startsWith("07")) {
    if (d.length !== 11) {
      return "UK mobile numbers are 11 digits long and start with 07 (e.g. 07700 900123).";
    }
    if (!/^07[1-9]\d{8}$/.test(d)) {
      return "After 07 the next digit should be 1–9 for a valid UK mobile.";
    }
    return undefined;
  }

  if (/^(01|02|03|05|08|09)/.test(d)) {
    if (d.length < 10 || d.length > 11) {
      return "That length does not match a typical UK landline or service number (expect 10–11 digits including the leading 0).";
    }
    return undefined;
  }

  return "Use a valid UK format: mobiles start with 07; many landlines start with 01, 02, or 03. Include the leading 0 or use +44.";
}
