/**
 * Shared layout: header + main content (pages stay domain-only).
 */
import type { ReactNode } from "react";

import { Header } from "@/components/layout/header";

export function PageLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      {/* max-w-5xl + px matches header; keeps line length readable */}
      <main className="mx-auto max-w-5xl space-y-8 px-4 py-8">{children}</main>
    </div>
  );
}
