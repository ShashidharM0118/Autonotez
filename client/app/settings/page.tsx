"use client";
import * as React from "react";
import { Card, Button, Input } from "@/components/ui";

export default function SettingsPage() {
  return (
    <div className="mx-auto max-w-3xl space-y-6 py-10">
      <h1 className="text-2xl font-semibold">Settings</h1>
      <Card title="API">
        <div className="flex flex-col gap-3">
          <label className="text-sm text-subtext">Backend URL</label>
          <Input placeholder="http://localhost:5000/api" defaultValue={process.env.NEXT_PUBLIC_API_BASE} />
          <Button variant="outline">Save</Button>
        </div>
      </Card>
      <Card title="Preferences">
        <div className="text-sm text-subtext">More preferences coming soon.</div>
      </Card>
    </div>
  );
}
