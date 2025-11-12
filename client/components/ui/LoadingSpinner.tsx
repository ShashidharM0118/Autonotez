import * as React from "react";

export function LoadingSpinner({ size = 24 }: { size?: number }) {
	return (
		<div
			className="animate-spin"
			style={{ width: size, height: size }}
			aria-label="Loading"
		>
			<svg
				viewBox="0 0 24 24"
				className="text-primary"
				style={{ width: size, height: size }}
			>
				<circle
					className="opacity-25"
					cx="12"
					cy="12"
					r="10"
					stroke="currentColor"
					strokeWidth="4"
					fill="none"
				/>
				<path
					className="opacity-75"
					fill="currentColor"
					d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
				/>
			</svg>
		</div>
	);
}

export default LoadingSpinner;
