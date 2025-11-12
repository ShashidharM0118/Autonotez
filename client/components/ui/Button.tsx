"use client";
import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";
import { twMerge } from "tailwind-merge";

const buttonVariants = cva(
	"inline-flex items-center justify-center rounded-md font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-primary/70 disabled:opacity-50 disabled:pointer-events-none",
	{
		variants: {
			variant: {
				primary:
					"bg-primary text-white hover:bg-primary/90 shadow-subtle",
				secondary:
					"bg-secondary text-white hover:bg-secondary/90 shadow-subtle",
				outline:
					"border border-border bg-transparent text-text hover:bg-muted",
				ghost:
					"bg-transparent text-text hover:bg-muted/60",
			},
			size: {
				sm: "h-9 px-3 text-sm",
				md: "h-10 px-4 text-sm",
				lg: "h-11 px-5 text-base",
			},
		},
		defaultVariants: {
			variant: "primary",
			size: "md",
		},
	}
);

export type ButtonProps = React.ButtonHTMLAttributes<HTMLButtonElement> &
	VariantProps<typeof buttonVariants> & {
		asChild?: boolean;
	};

export const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
	({ className, variant, size, ...props }, ref) => {
		return (
			<button
				ref={ref}
				className={twMerge(buttonVariants({ variant, size }), className)}
				{...props}
			/>
		);
	}
);
Button.displayName = "Button";

export default Button;
