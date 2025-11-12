export type Note = {
	note_id: string;
	title?: string;
	transcript?: string;
	summary?: string;
	action_items?: string[];
	decisions?: string[];
	keywords?: string[];
	created_at?: string;
};

export type CreateNotePayload = {
	transcript: string;
	title?: string;
	model?: string;
};

export type LLMModel = {
	id: string;
	name: string;
};

export type ApiResponse<T> = {
	success: boolean;
	data?: T;
	error?: string;
};
