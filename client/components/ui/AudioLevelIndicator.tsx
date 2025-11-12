"use client";
import * as React from "react";

export function AudioLevelIndicator({ level }: { level: number }) {
  const percentage = Math.min(100, Math.max(0, Math.round(level * 140)));
  return (
    <div className="h-2 w-full rounded-full bg-muted">
      <div
        className="h-2 rounded-full bg-linear-to-r from-primary to-secondary transition-[width]"
        style={{ width: `${percentage}%` }}
      />
    </div>
  );
}

export default AudioLevelIndicator;
