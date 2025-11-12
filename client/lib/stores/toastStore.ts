import { create } from "zustand";
import type { ToastMessage } from "@/components/ui/Toast";

type ToastStore = {
	messages: ToastMessage[];
	push: (msg: Omit<ToastMessage, "id">) => void;
	remove: (id: string) => void;
	clear: () => void;
};

export const useToastStore = create<ToastStore>((set) => ({
	messages: [],
	push: (msg) =>
		set((s) => ({ messages: [...s.messages, { id: crypto.randomUUID(), ...msg }] })),
	remove: (id) => set((s) => ({ messages: s.messages.filter((m) => m.id !== id) })),
	clear: () => set({ messages: [] }),
}));
