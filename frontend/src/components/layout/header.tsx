/**
 * Top navigation: brand and primary routes.
 */
import { Link, NavLink } from "react-router-dom";

import { cn } from "@/lib/utils";

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  cn(
    "rounded-md px-3 py-1.5 transition-colors hover:text-foreground",
    isActive ? "bg-muted font-medium text-foreground" : "text-muted-foreground",
  );

export function Header({ className }: { className?: string }) {
  return (
    <header className={cn("border-b bg-card", className)}>
      <div className="mx-auto flex max-w-5xl flex-wrap items-center justify-between gap-4 px-4 py-4">
        <Link to="/customers" className="text-lg font-semibold tracking-tight hover:opacity-90">
          Customer Information
        </Link>
        {/* `end`: "Customers" active only on /customers, not on /customers/:id */}
        <nav className="flex flex-wrap items-center gap-1 text-sm" aria-label="Main">
          <NavLink to="/customers" className={navLinkClass} end>
            Customers
          </NavLink>
          <NavLink to="/customers/new" className={navLinkClass}>
            New request
          </NavLink>
        </nav>
      </div>
    </header>
  );
}
