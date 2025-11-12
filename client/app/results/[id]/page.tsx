"use client";
import * as React from "react";
import { useParams } from "next/navigation";
import { getNote } from "@/lib/api";
import { SummaryCard, Skeleton, Card } from "@/components/ui";
import type { Note } from "@/lib/types";

export default function ResultPage() {
  const params = useParams<{ id: string }>();
  const id = params?.id;
  const [note, setNote] = React.useState<Note | null>(null);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState<string | null>(null);

  React.useEffect(() => {
    if (!id) return;
    getNote(id)
      .then((n) => setNote(n))
      .catch((e) => setError(e?.message || "Failed to load note"))
      .finally(() => setLoading(false));
  }, [id]);

  if (loading) {
    return (
      <div className="mx-auto max-w-4xl space-y-4 py-10">
        <Skeleton className="h-10 w-2/3" />
        <Skeleton className="h-24 w-full" />
      </div>
    );
  }

  if (error || !note) {
    return (
      <div className="mx-auto max-w-4xl py-10 text-subtext">{error || "Note not found."}</div>
    );
  }

  return (
    <div className="mx-auto max-w-4xl space-y-6 py-10">
      <h1 className="text-2xl font-semibold">{note.title || "Meeting"}</h1>
      {note.summary && (
        <Card title="Summary">
          <p className="text-sm text-subtext whitespace-pre-wrap">{note.summary}</p>
        </Card>
      )}
      <div className="grid gap-4 md:grid-cols-2">
        {note.action_items && note.action_items.length > 0 && (
          <SummaryCard title="Action items" items={note.action_items} />
        )}
        {note.decisions && note.decisions.length > 0 && (
          <SummaryCard title="Decisions" items={note.decisions} />
        )}
      </div>
      {note.transcript && (
        <Card title="Transcript">
          <pre className="whitespace-pre-wrap text-sm text-subtext">{note.transcript}</pre>
        </Card>
      )}
    </div>
  );
}
