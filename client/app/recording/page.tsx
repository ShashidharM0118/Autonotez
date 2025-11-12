"use client";
import * as React from "react";
import { Button, AudioLevelIndicator, Card } from "@/components/ui";
import { getMicStream, createAudioLevelMonitor } from "@/lib/audio";

export default function RecordingPage() {
  const [stream, setStream] = React.useState<MediaStream | null>(null);
  const [level, setLevel] = React.useState(0);
  const [recording, setRecording] = React.useState(false);
  const mediaRecorderRef = React.useRef<MediaRecorder | null>(null);
  const chunksRef = React.useRef<Blob[]>([]);

  async function start() {
    if (recording) return;
    const mic = await getMicStream();
    setStream(mic);
    createAudioLevelMonitor(mic, setLevel);
    const mr = new MediaRecorder(mic);
    chunksRef.current = [];
    mr.ondataavailable = (e) => {
      if (e.data.size > 0) chunksRef.current.push(e.data);
    };
    mr.start();
    mediaRecorderRef.current = mr;
    setRecording(true);
  }

  function stop() {
    if (!recording) return;
    mediaRecorderRef.current?.stop();
    stream?.getTracks().forEach((t) => t.stop());
    setRecording(false);
  }

  return (
    <div className="mx-auto max-w-3xl space-y-6 py-10">
      <h1 className="text-2xl font-semibold">Record a meeting</h1>
      <Card title="Microphone">
        <div className="space-y-4">
          <AudioLevelIndicator level={level} />
          <div className="flex gap-3">
            {!recording && <Button onClick={start}>Start</Button>}
            {recording && (
              <Button variant="secondary" onClick={stop}>
                Stop
              </Button>
            )}
          </div>
          <p className="text-xs text-subtext">
            Levels update in real-time. When you stop, audio chunks would be processed and sent to backend (not yet wired).
          </p>
        </div>
      </Card>
    </div>
  );
}
