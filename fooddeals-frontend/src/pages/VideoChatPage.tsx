import { useEffect, useRef, useState } from 'react';
import { Card } from '../components/Card';
import { Button } from '../components/Button';
import { SectionHeader } from '../components/SectionHeader';
import { WS_BASE_URL } from '../lib/config';

export function VideoChatPage() {
  const [isStreaming, setIsStreaming] = useState(false);
  const [status, setStatus] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const wsRef = useRef<WebSocket | null>(null);
  const mediaStreamRef = useRef<MediaStream | null>(null);
  const recorderRef = useRef<MediaRecorder | null>(null);

  const startStream = async () => {
    try {
      setStatus(null);
      const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: false });
      mediaStreamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }

      const ws = new WebSocket(`${WS_BASE_URL}/ws/stream`);
      
      ws.onopen = () => {
        setStatus('Connected to server. Streaming...');
        setIsStreaming(true);
        
        // Setup MediaRecorder to send chunks
        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'video/webm; codecs=vp9' });
        mediaRecorder.ondataavailable = (event) => {
          if (event.data.size > 0 && ws.readyState === WebSocket.OPEN) {
             ws.send(event.data);
          }
        };
        mediaRecorder.start(100); // 100ms chunks
        recorderRef.current = mediaRecorder;
      };

      ws.onerror = (error) => {
         console.error('WebSocket Error:', error);
         setStatus('Connection error.');
         stopStream();
      };
      
      ws.onclose = () => {
         setStatus('Connection closed.');
         setIsStreaming(false);
      };

      wsRef.current = ws;

    } catch (err) {
      console.error(err);
      setStatus('Failed to access camera or connect.');
    }
  };

  const stopStream = () => {
    if (recorderRef.current && recorderRef.current.state !== 'inactive') {
       recorderRef.current.stop();
    }
    if (mediaStreamRef.current) {
      mediaStreamRef.current.getTracks().forEach((track) => track.stop());
      mediaStreamRef.current = null;
    }
    if (wsRef.current) {
      wsRef.current.close();
      wsRef.current = null;
    }
    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }
    setIsStreaming(false);
    setStatus('Stream stopped.');
  };

  useEffect(() => {
     return () => stopStream();
  }, []);

  return (
    <div className="space-y-8">
      <SectionHeader 
         title="Live Video Stream" 
         subtitle="Stream video to the server for processing via WebSocket."
      />
      
      <div className="grid gap-8 lg:grid-cols-2">
         <Card className="border-violet-500/30 bg-violet-500/5 space-y-4">
            <div className="relative aspect-video bg-black rounded-xl overflow-hidden border border-slate-700">
               <video 
                  ref={videoRef} 
                  autoPlay 
                  muted 
                  playsInline 
                  className="w-full h-full object-cover"
               />
               {!isStreaming && (
                  <div className="absolute inset-0 flex items-center justify-center text-slate-500">
                     Camera Off
                  </div>
               )}
               {isStreaming && (
                  <div className="absolute top-2 right-2 animate-pulse">
                     <div className="bg-red-500 text-white text-xs px-2 py-1 rounded-full font-bold">LIVE</div>
                  </div>
               )}
            </div>

            <div className="flex gap-4 items-center justify-center">
               {!isStreaming ? (
                  <Button onClick={startStream}>Start Streaming</Button>
               ) : (
                  <Button tone="secondary" onClick={stopStream} className="bg-red-500/20 text-red-200 border-red-500/30 hover:bg-red-500/30">
                     Stop Streaming
                  </Button>
               )}
            </div>

            {status && (
               <div className="text-center text-xs text-slate-400">
                  {status}
               </div>
            )}
         </Card>

         <div className="space-y-4">
             <Card className="bg-slate-800/50 border-slate-700">
                <h3 className="text-lg font-semibold text-white mb-2">How it works</h3>
                <ul className="list-disc list-inside text-sm text-slate-300 space-y-2">
                   <li>Browser captures video via MediaDevices API.</li>
                   <li>MediaRecorder compresses video (WebM/VP9).</li>
                   <li>Chunks are sent over WebSocket to <code>/ws/stream</code>.</li>
                   <li>Backend pipes the stream to <code>ffmpeg</code> to save it locally.</li>
                </ul>
             </Card>
         </div>
      </div>
    </div>
  );
}
