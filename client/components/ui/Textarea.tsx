import * as React from "react";
import { twMerge } from "tailwind-merge";

export type TextareaProps = React.TextareaHTMLAttributes<HTMLTextAreaElement>;

export const Textarea = React.forwardRef<HTMLTextAreaElement, TextareaProps>(
	({ className, ...props }, ref) => {
		return (
			<textarea
				ref={ref}
				className={twMerge(
					"w-full min-h-[120px] rounded-md bg-muted text-text placeholder:text-subtext border border-border px-3 py-2 outline-none focus:ring-2 focus:ring-primary/60 resize-y",
					className
				)}
				{...props}
			/>
		);
	}
);
Textarea.displayName = "Textarea";

export default Textarea;
