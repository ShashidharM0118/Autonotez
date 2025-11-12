import axios from "axios";
import type { Note, CreateNotePayload, ApiResponse, LLMModel } from "./types";

const api = axios.create({
	baseURL: process.env.NEXT_PUBLIC_API_BASE || "http://localhost:5000/api",
	timeout: 15000,
});

export async function fetchModels(): Promise<LLMModel[]> {
	const res = await api.get<LLMModel[]>("/notes/models");
	return res.data;
}

export async function createNote(payload: CreateNotePayload): Promise<Note> {
	const res = await api.post<Note>("/notes", payload);
	return res.data;
}

export async function getNote(id: string): Promise<Note> {
	const res = await api.get<Note>(`/notes/${id}`);
	return res.data;
}

export async function listNotes(): Promise<Note[]> {
	const res = await api.get<Note[]>("/notes");
	return res.data;
}

export async function health(): Promise<ApiResponse<{ status: string }>> {
	const res = await api.get("/notes/health");
	return res.data;
}

export default api;
