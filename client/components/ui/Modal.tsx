"use client";
import * as React from "react";
import * as Dialog from "@radix-ui/react-dialog";
import { X } from "lucide-react";
import { twMerge } from "tailwind-merge";

type ModalProps = {
	open?: boolean;
	onOpenChange?: (open: boolean) => void;
	title?: string;
	description?: string;
	trigger?: React.ReactNode;
	children?: React.ReactNode;
	className?: string;
};

export function Modal({ open, onOpenChange, title, description, trigger, children, className }: ModalProps) {
	return (
		<Dialog.Root open={open} onOpenChange={onOpenChange}>
			{trigger && <Dialog.Trigger asChild>{trigger}</Dialog.Trigger>}
			<Dialog.Portal>
				<Dialog.Overlay className="fixed inset-0 bg-black/70 data-[state=open]:animate-in data-[state=open]:fade-in-0" />
				<Dialog.Content
					className={twMerge(
						"fixed left-1/2 top-1/2 w-[95vw] max-w-lg -translate-x-1/2 -translate-y-1/2 rounded-xl border border-border bg-surface p-4 shadow-subtle outline-none",
						className
					)}
				>
					<div className="flex items-start justify-between gap-4">
						<div>
							{title && (
								<Dialog.Title className="text-lg font-semibold text-text">
									{title}
								</Dialog.Title>
							)}
							{description && (
								<Dialog.Description className="mt-1 text-sm text-subtext">
									{description}
								</Dialog.Description>
							)}
						</div>
						<Dialog.Close asChild>
							<button
								aria-label="Close"
								className="rounded-md p-1 text-subtext hover:bg-muted hover:text-text"
							>
								<X className="h-5 w-5" />
							</button>
						</Dialog.Close>
					</div>
					<div className="mt-4">{children}</div>
				</Dialog.Content>
			</Dialog.Portal>
		</Dialog.Root>
	);
}

export default Modal;
