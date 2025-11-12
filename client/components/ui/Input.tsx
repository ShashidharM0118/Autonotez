import * as React from "react";
import { twMerge } from "tailwind-merge";

export type InputProps = React.InputHTMLAttributes<HTMLInputElement>;

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
	({ className, ...props }, ref) => {
		return (
			<input
				ref={ref}
				className={twMerge(
					"w-full rounded-md bg-muted text-text placeholder:text-subtext border border-border px-3 py-2 outline-none focus:ring-2 focus:ring-primary/60",
					className
				)}
				{...props}
			/>
		);
	}
);
Input.displayName = "Input";

export default Input;
