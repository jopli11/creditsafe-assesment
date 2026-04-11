import type { ReactNode } from "react";

import { Header } from "@/components/layout/header";

/**
 * Shared chrome: header + centered content column.
 * Keeps pages focused on domain UI instead of repeating layout markup.
 */
export function PageLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="mx-auto max-w-5xl space-y-8 px-4 py-8">{children}</main>
    </div>
  );
}
