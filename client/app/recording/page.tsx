"use client";
import * as React from "react";
import { Button, AudioLevelIndicator, Card } from "@/components/ui";
import { getMicStream, createAudioLevelMonitor } from "@/lib/audio";
import { Mic, MonitorSpeaker, Play, Pause, Download } from "lucide-react";

type AudioSource = "microphone" | "system" | "both";

export default function RecordingPage() {
  const [micStream, setMicStream] = React.useState<MediaStream | null>(null);
  const [systemStream, setSystemStream] = React.useState<MediaStream | null>(null);
  const [micLevel, setMicLevel] = React.useState(0);
  const [systemLevel, setSystemLevel] = React.useState(0);
  const [recording, setRecording] = React.useState(false);
  const [audioSource, setAudioSource] = React.useState<AudioSource>("microphone");
  const [recordedBlob, setRecordedBlob] = React.useState<Blob | null>(null);
  const [recordedUrl, setRecordedUrl] = React.useState<string | null>(null);
  const [playing, setPlaying] = React.useState(false);
  
  const mediaRecorderRef = React.useRef<MediaRecorder | null>(null);
  const chunksRef = React.useRef<Blob[]>([]);
  const audioRef = React.useRef<HTMLAudioElement | null>(null);
  const micMonitorCleanupRef = React.useRef<(() => void) | null>(null);
  const systemMonitorCleanupRef = React.useRef<(() => void) | null>(null);

  async function startRecording() {
    if (recording) return;
    
    try {
      let combinedStream: MediaStream | null = null;
      
      if (audioSource === "microphone" || audioSource === "both") {
        const mic = await getMicStream();
        setMicStream(mic);
        micMonitorCleanupRef.current = createAudioLevelMonitor(mic, setMicLevel);
        combinedStream = mic;
      }
      
      if (audioSource === "system" || audioSource === "both") {
        const system = await navigator.mediaDevices.getDisplayMedia({
          video: false,
          audio: {
            echoCancellation: false,
            noiseSuppression: false,
            autoGainControl: false,
          },
        });
        setSystemStream(system);
        systemMonitorCleanupRef.current = createAudioLevelMonitor(system, setSystemLevel);
        
        if (audioSource === "both" && combinedStream) {
          // Combine both streams
          const audioContext = new AudioContext();
          const micSource = audioContext.createMediaStreamSource(combinedStream);
          const systemSource = audioContext.createMediaStreamSource(system);
          const destination = audioContext.createMediaStreamDestination();
          
          micSource.connect(destination);
          systemSource.connect(destination);
          
          combinedStream = destination.stream;
        } else {
          combinedStream = system;
        }
      }
      
      if (!combinedStream) {
        throw new Error("No audio stream available");
      }
      
      const mr = new MediaRecorder(combinedStream, {
        mimeType: MediaRecorder.isTypeSupported("audio/webm")
          ? "audio/webm"
          : "audio/ogg",
      });
      
      chunksRef.current = [];
      
      mr.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data);
      };
      
      mr.onstop = () => {
        const blob = new Blob(chunksRef.current, { type: mr.mimeType });
        setRecordedBlob(blob);
        const url = URL.createObjectURL(blob);
        setRecordedUrl(url);
      };
      
      mr.start();
      mediaRecorderRef.current = mr;
      setRecording(true);
    } catch (error) {
      console.error("Error starting recording:", error);
      alert(`Failed to start recording: ${error instanceof Error ? error.message : "Unknown error"}`);
    }
  }

  function stopRecording() {
    if (!recording) return;
    
    mediaRecorderRef.current?.stop();
    
    if (micStream) {
      micStream.getTracks().forEach((t) => t.stop());
      setMicStream(null);
    }
    
    if (systemStream) {
      systemStream.getTracks().forEach((t) => t.stop());
      setSystemStream(null);
    }
    
    if (micMonitorCleanupRef.current) {
      micMonitorCleanupRef.current();
      micMonitorCleanupRef.current = null;
    }
    
    if (systemMonitorCleanupRef.current) {
      systemMonitorCleanupRef.current();
      systemMonitorCleanupRef.current = null;
    }
    
    setMicLevel(0);
    setSystemLevel(0);
    setRecording(false);
  }

  function togglePlayback() {
    if (!audioRef.current) return;
    
    if (playing) {
      audioRef.current.pause();
      setPlaying(false);
    } else {
      audioRef.current.play();
      setPlaying(true);
    }
  }

  function downloadRecording() {
    if (!recordedUrl || !recordedBlob) return;
    
    const a = document.createElement("a");
    a.href = recordedUrl;
    a.download = `recording-${Date.now()}.webm`;
    a.click();
  }

  React.useEffect(() => {
    // Cleanup on unmount
    return () => {
      if (micStream) micStream.getTracks().forEach((t) => t.stop());
      if (systemStream) systemStream.getTracks().forEach((t) => t.stop());
      if (recordedUrl) URL.revokeObjectURL(recordedUrl);
      if (micMonitorCleanupRef.current) micMonitorCleanupRef.current();
      if (systemMonitorCleanupRef.current) systemMonitorCleanupRef.current();
    };
  }, [micStream, systemStream, recordedUrl]);

  return (
    <div className="mx-auto max-w-3xl space-y-6 py-10">
      <h1 className="text-2xl font-semibold">Record Audio</h1>
      
      {/* Audio Source Selection */}
      <Card title="Audio Source">
        <div className="space-y-4">
          <div className="grid grid-cols-3 gap-3">
            <button
              onClick={() => !recording && setAudioSource("microphone")}
              disabled={recording}
              className={`flex flex-col items-center gap-2 rounded-lg border p-4 transition-all ${
                audioSource === "microphone"
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border bg-surface text-subtext hover:bg-muted"
              } ${recording ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
            >
              <Mic className="h-6 w-6" />
              <span className="text-sm font-medium">Microphone</span>
            </button>
            
            <button
              onClick={() => !recording && setAudioSource("system")}
              disabled={recording}
              className={`flex flex-col items-center gap-2 rounded-lg border p-4 transition-all ${
                audioSource === "system"
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border bg-surface text-subtext hover:bg-muted"
              } ${recording ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
            >
              <MonitorSpeaker className="h-6 w-6" />
              <span className="text-sm font-medium">System Audio</span>
            </button>
            
            <button
              onClick={() => !recording && setAudioSource("both")}
              disabled={recording}
              className={`flex flex-col items-center gap-2 rounded-lg border p-4 transition-all ${
                audioSource === "both"
                  ? "border-primary bg-primary/10 text-primary"
                  : "border-border bg-surface text-subtext hover:bg-muted"
              } ${recording ? "opacity-50 cursor-not-allowed" : "cursor-pointer"}`}
            >
              <div className="flex items-center gap-1">
                <Mic className="h-5 w-5" />
                <MonitorSpeaker className="h-5 w-5" />
              </div>
              <span className="text-sm font-medium">Both</span>
            </button>
          </div>
          
          <p className="text-xs text-subtext">
            Select audio source before starting recording. System audio requires screen sharing permission.
          </p>
        </div>
      </Card>

      {/* Recording Controls */}
      <Card title="Recording">
        <div className="space-y-4">
          {/* Microphone Level */}
          {(audioSource === "microphone" || audioSource === "both") && (
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-subtext">
                <Mic className="h-4 w-4" />
                <span>Microphone Level</span>
              </div>
              <AudioLevelIndicator level={micLevel} />
            </div>
          )}
          
          {/* System Audio Level */}
          {(audioSource === "system" || audioSource === "both") && (
            <div className="space-y-2">
              <div className="flex items-center gap-2 text-sm text-subtext">
                <MonitorSpeaker className="h-4 w-4" />
                <span>System Audio Level</span>
              </div>
              <AudioLevelIndicator level={systemLevel} />
            </div>
          )}
          
          {/* Control Buttons */}
          <div className="flex gap-3 pt-2">
            {!recording && (
              <Button onClick={startRecording}>
                Start Recording
              </Button>
            )}
            {recording && (
              <Button variant="secondary" onClick={stopRecording}>
                Stop Recording
              </Button>
            )}
          </div>
          
          {recording && (
            <div className="flex items-center gap-2 text-sm text-primary">
              <div className="h-2 w-2 animate-pulse rounded-full bg-primary" />
              <span>Recording in progress...</span>
            </div>
          )}
        </div>
      </Card>

      {/* Playback Section */}
      {recordedUrl && (
        <Card title="Recording Output">
          <div className="space-y-4">
            <audio
              ref={audioRef}
              src={recordedUrl}
              onEnded={() => setPlaying(false)}
              onPlay={() => setPlaying(true)}
              onPause={() => setPlaying(false)}
              className="hidden"
            />
            
            <div className="flex items-center gap-4">
              <Button
                variant="outline"
                onClick={togglePlayback}
                className="flex items-center gap-2"
              >
                {playing ? (
                  <>
                    <Pause className="h-4 w-4" />
                    Pause
                  </>
                ) : (
                  <>
                    <Play className="h-4 w-4" />
                    Play
                  </>
                )}
              </Button>
              
              <Button
                variant="ghost"
                onClick={downloadRecording}
                className="flex items-center gap-2"
              >
                <Download className="h-4 w-4" />
                Download
              </Button>
            </div>
            
            <div className="rounded-md bg-muted p-3">
              <div className="text-xs text-subtext">
                <div>Size: {(recordedBlob!.size / 1024).toFixed(2)} KB</div>
                <div>Format: {recordedBlob!.type}</div>
              </div>
            </div>
            
            <p className="text-xs text-subtext">
              You can play the recorded audio or download it. To process it for transcription, 
              you would send this to the backend API.
            </p>
          </div>
        </Card>
      )}
    </div>
  );
}
