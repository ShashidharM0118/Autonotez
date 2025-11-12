"use client";
import * as React from "react";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

export function AppLayout({ children }: { children: React.ReactNode }) {
	const [open, setOpen] = React.useState(false);
	return (
		<div className="min-h-screen bg-background text-text">
			<TopBar onMenuClick={() => setOpen((o) => !o)} />
			<div className="mx-auto flex w-full max-w-6xl">
				<Sidebar className={open ? "md:flex" : "md:flex hidden"} />
				<main className="flex-1 p-4 md:p-6">{children}</main>
			</div>
		</div>
	);
}

export default AppLayout;
