"use client";
import * as React from "react";
import * as RT from "@radix-ui/react-toast";
import { twMerge } from "tailwind-merge";

export type ToastMessage = {
	id: string;
	title?: string;
	description?: string;
	variant?: "default" | "success" | "error";
};

const variantClasses: Record<string, string> = {
	default: "bg-surface border-border text-text",
	success: "bg-surface border-green-600 text-green-400",
	error: "bg-surface border-red-600 text-red-400",
};

export function ToastContainer({ messages, onRemove }: { messages: ToastMessage[]; onRemove: (id: string) => void }) {
	return (
		<RT.Provider swipeDirection="right" duration={4000}>
			{messages.map((m) => (
				<RT.Root
					key={m.id}
					className={twMerge(
						"data-[state=open]:animate-in data-[state=closed]:animate-out data-[swipe=end]:animate-out data-[state=open]:fade-in-0 data-[state=closed]:fade-out-0 data-[swipe=move]:translate-x-2 data-[swipe=end]:translate-x-full data-[state=open]:slide-in-from-right-full data-[state=closed]:slide-out-to-right-full rounded-md border px-4 py-3 shadow-subtle w-[320px]",
						variantClasses[m.variant || "default"]
					)}
					onOpenChange={(open) => {
						if (!open) onRemove(m.id);
					}}
				>
					{m.title && <RT.Title className="text-sm font-semibold">{m.title}</RT.Title>}
					{m.description && (
						<RT.Description className="mt-1 text-xs text-subtext">
							{m.description}
						</RT.Description>
					)}
				</RT.Root>
			))}
			<RT.Viewport className="fixed bottom-4 right-4 flex flex-col gap-2 z-50" />
		</RT.Provider>
	);
}

export default ToastContainer;
