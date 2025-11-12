import type { Variants } from "framer-motion";

export const fadeInUp: Variants = {
	hidden: { opacity: 0, y: 16 },
	show: {
		opacity: 1,
		y: 0,
		transition: { duration: 0.25 },
	},
};

export const staggerContainer = (stagger = 0.08) => ({
	hidden: {},
	show: {
		transition: { staggerChildren: stagger, delayChildren: 0.05 },
	},
});
