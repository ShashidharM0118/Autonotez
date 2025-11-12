export async function getMicStream(): Promise<MediaStream> {
  return navigator.mediaDevices.getUserMedia({ audio: true });
}

export function createAudioLevelMonitor(stream: MediaStream, onLevel: (level: number) => void) {
  const ctx = new AudioContext();
  const source = ctx.createMediaStreamSource(stream);
  const analyser = ctx.createAnalyser();
  analyser.fftSize = 1024;
  source.connect(analyser);
  const data = new Uint8Array(analyser.fftSize);
  let active = true;

  function tick() {
    if (!active) return;
    analyser.getByteTimeDomainData(data);
    let sumSquares = 0;
    for (let i = 0; i < data.length; i++) {
      const v = (data[i] - 128) / 128; // normalize to [-1,1]
      sumSquares += v * v;
    }
    const rms = Math.sqrt(sumSquares / data.length);
    onLevel(rms);
    requestAnimationFrame(tick);
  }
  tick();

  return () => {
    active = false;
    ctx.close();
  };
}
