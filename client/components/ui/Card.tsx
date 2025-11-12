import * as React from "react";
import { twMerge } from "tailwind-merge";

type CardProps = React.HTMLAttributes<HTMLDivElement> & {
	title?: string;
	description?: string;
};

export function Card({ className, title, description, children, ...props }: CardProps) {
	return (
		<div
			className={twMerge(
				"rounded-xl border border-border bg-surface text-text shadow-subtle",
				className
			)}
			{...props}
		>
			{(title || description) && (
				<div className="p-4 border-b border-border/70">
					{title && <h3 className="text-base font-semibold">{title}</h3>}
					{description && (
						<p className="mt-1 text-sm text-subtext">{description}</p>
					)}
				</div>
			)}
			<div className="p-4">{children}</div>
		</div>
	);
}

export default Card;
