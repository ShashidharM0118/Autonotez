import { create } from "zustand";

type RecordingState = {
  isRecording: boolean;
  level: number;
  setLevel: (n: number) => void;
  setRecording: (b: boolean) => void;
};

export const useRecordingStore = create<RecordingState>((set) => ({
  isRecording: false,
  level: 0,
  setLevel: (n) => set({ level: n }),
  setRecording: (b) => set({ isRecording: b }),
}));
