import { Link } from "react-router-dom";

import { cn } from "@/lib/utils";

export function Header({ className }: { className?: string }) {
  return (
    <header className={cn("border-b bg-card", className)}>
      <div className="mx-auto flex max-w-5xl items-center justify-between gap-4 px-4 py-4">
        <Link to="/customers" className="text-lg font-semibold tracking-tight">
          Customer Information
        </Link>
        <nav className="text-sm text-muted-foreground">
          <Link to="/customers" className="hover:text-foreground">
            Directory
          </Link>
        </nav>
      </div>
    </header>
  );
}
