"use client";
import * as React from "react";
import { Mic, Home, Settings, Layers } from "lucide-react";
import { twMerge } from "tailwind-merge";

type NavItem = {
	label: string;
	icon: React.ReactNode;
	href: string;
};

const navItems: NavItem[] = [
	{ label: "Home", icon: <Home className="h-4 w-4" />, href: "/" },
		{ label: "Record", icon: <Mic className="h-4 w-4" />, href: "/recording" },
	{ label: "Notes", icon: <Layers className="h-4 w-4" />, href: "/notes" },
	{ label: "Settings", icon: <Settings className="h-4 w-4" />, href: "/settings" },
];

export function Sidebar({ className }: { className?: string }) {
	return (
		<aside
			className={twMerge(
				"hidden md:flex w-60 flex-col border-r border-border bg-background/60 backdrop-blur",
				className
			)}
		>
			<div className="p-4">
				<div className="flex items-center gap-2 text-text">
					<Mic className="h-5 w-5 text-primary" />
					<span className="text-sm font-semibold">AutoNotez</span>
				</div>
			</div>
			<nav className="flex-1 px-2">
				{navItems.map((item) => (
					<a
						key={item.href}
						href={item.href}
						className="group flex items-center gap-2 rounded-md px-3 py-2 text-sm text-subtext hover:bg-muted hover:text-text"
					>
						<span className="text-text/70 group-hover:text-text">{item.icon}</span>
						{item.label}
					</a>
				))}
			</nav>
			<div className="p-4 text-xs text-subtext">v0.1.0</div>
		</aside>
	);
}

export default Sidebar;
