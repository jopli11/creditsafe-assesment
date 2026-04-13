/**
 * Mobile-only card tiles for the directory (`md:hidden` from `CustomerList`).
 * Compound components avoid boolean prop sprawl (Radix-style composition).
 */
import type { ReactNode } from "react";
import { Link } from "react-router-dom";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { cn } from "@/lib/utils";

function Root({ children, className }: { children: ReactNode; className?: string }) {
  return <Card className={cn(className)}>{children}</Card>;
}

function Header({ title, description }: { title: string; description?: string }) {
  return (
    <CardHeader>
      <CardTitle className="text-base">{title}</CardTitle>
      {description ? <CardDescription>{description}</CardDescription> : null}
    </CardHeader>
  );
}

function Body({ children }: { children: ReactNode }) {
  return <CardContent className="space-y-2 text-sm">{children}</CardContent>;
}

function Footer({ children }: { children: ReactNode }) {
  return <div className="flex items-center justify-end border-t px-6 py-3">{children}</div>;
}

function TitleLink({ id, label }: { id: string; label: string }) {
  return (
    <Link className="text-primary underline-offset-4 hover:underline" to={`/customers/${id}`}>
      {label}
    </Link>
  );
}

export const CustomerCard = {
  Root,
  Header,
  Body,
  Footer,
  TitleLink,
};
