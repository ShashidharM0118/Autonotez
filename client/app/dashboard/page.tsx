"use client";
import * as React from "react";
import { Card, Button } from "@/components/ui";

export default function DashboardPage() {
  const stats = [
    { label: "Notes", value: 12 },
    { label: "This week", value: 4 },
    { label: "Avg. length", value: "32m" },
  ];
  return (
    <div className="mx-auto max-w-6xl space-y-6 py-10">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold">Dashboard</h1>
        <Button>New recording</Button>
      </div>
      <div className="grid gap-4 md:grid-cols-3">
        {stats.map((s) => (
          <Card key={s.label}>
            <div className="text-2xl font-bold">{s.value}</div>
            <div className="text-subtext">{s.label}</div>
          </Card>
        ))}
      </div>
      <Card title="Recent notes">
        <div className="text-sm text-subtext">No recent notes yet.</div>
      </Card>
    </div>
  );
}
