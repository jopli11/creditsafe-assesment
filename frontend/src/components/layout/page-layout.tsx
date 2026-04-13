/**
 * Shared layout wrapper — global chrome so pages only contain domain content.
 *
 * **Structure**
 * `min-h-screen` + `bg-background` for full-viewport app feel; `max-w-5xl` constrains
 * line length for readability; horizontal padding matches the header.
 */
import type { ReactNode } from "react";

import { Header } from "@/components/layout/header";

export function PageLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <Header />
      <main className="mx-auto max-w-5xl space-y-8 px-4 py-8">{children}</main>
    </div>
  );
}
