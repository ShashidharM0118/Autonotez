"use client";
import * as React from "react";
import { Menu, Mic } from "lucide-react";

export function TopBar({ onMenuClick }: { onMenuClick?: () => void }) {
	return (
		<header className="sticky top-0 z-40 w-full border-b border-border bg-background/80 backdrop-blur">
			<div className="mx-auto flex h-14 max-w-6xl items-center justify-between px-4">
				<div className="flex items-center gap-3">
					<button
						className="rounded-md p-2 text-subtext hover:bg-muted hover:text-text md:hidden"
						onClick={onMenuClick}
						aria-label="Open menu"
					>
						<Menu className="h-5 w-5" />
					</button>
					<div className="flex items-center gap-2 text-text">
						<Mic className="h-5 w-5 text-primary" />
						<span className="text-sm font-semibold">AutoNotez</span>
					</div>
				</div>
				<nav className="hidden items-center gap-6 text-sm text-subtext md:flex">
					<a href="#features" className="hover:text-text">Features</a>
					<a href="#testimonials" className="hover:text-text">Testimonials</a>
					<a href="#cta" className="hover:text-text">Get Started</a>
				</nav>
				<a
					href="#cta"
					className="rounded-md bg-primary px-3 py-2 text-sm font-medium text-white hover:bg-primary/90"
				>
					Try it free
				</a>
			</div>
		</header>
	);
}

export default TopBar;
