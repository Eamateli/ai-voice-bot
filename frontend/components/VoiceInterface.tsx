'use client'

import { useState, useRef, useEffect } from 'react'
import { Mic, MicOff, Volume2 } from 'lucide-react'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
const WS_URL = API_URL.replace(/^http/, 'ws')

interface VoiceInterfaceProps {
  isRecording: boolean
  setIsRecording: (value: boolean) => void
}

export default function VoiceInterface({ isRecording, setIsRecording }: VoiceInterfaceProps) {
  const [status, setStatus] = useState('Ready to start')
  const [transcription, setTranscription] = useState('')
  const [response, setResponse] = useState('')
  const [isConnected, setIsConnected] = useState(false)
  
  const wsRef = useRef<WebSocket | null>(null)
  const mediaRecorderRef = useRef<MediaRecorder | null>(null)

  // Connect to WebSocket on mount
  useEffect(() => {
    connectWebSocket()
    return () => {
      if (wsRef.current) {
        wsRef.current.close()
      }
    }
  }, [])

  const connectWebSocket = () => {
    const ws = new WebSocket(`${WS_URL}/ws/voice`)
    
    ws.onopen = () => {
      setIsConnected(true)
      setStatus('Connected')
    }

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data)
      
      if (data.type === 'transcription') {
        setTranscription(data.text)
        setStatus('Processing...')
      }
      
      if (data.type === 'audio_response') {
        setResponse(data.text)
        setStatus('Complete')
        playAudio(data.audio)
      }
    }

    ws.onclose = () => {
      setIsConnected(false)
      setStatus('Disconnected')
    }

    wsRef.current = ws
  }

  const playAudio = (audioData: number[]) => {
    const audioBytes = new Uint8Array(audioData)
    const audioBlob = new Blob([audioBytes], { type: 'audio/mp3' })
    const audioUrl = URL.createObjectURL(audioBlob)
    const audio = new Audio(audioUrl)
    audio.play()
  }

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const mediaRecorder = new MediaRecorder(stream)
      const chunks: BlobPart[] = []

      mediaRecorder.ondataavailable = (e) => chunks.push(e.data)
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(chunks, { type: 'audio/webm' })
        const arrayBuffer = await audioBlob.arrayBuffer()
        const audioArray = Array.from(new Uint8Array(arrayBuffer))
        
        wsRef.current?.send(JSON.stringify({
          type: 'audio',
          audio: audioArray,
          format: 'webm'
        }))
        
        stream.getTracks().forEach(track => track.stop())
      }

      mediaRecorder.start()
      mediaRecorderRef.current = mediaRecorder
      setIsRecording(true)
      setStatus('Recording...')
    } catch (error) {
      console.error('Microphone access denied:', error)
      setStatus('Microphone access denied')
    }
  }

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop()
      setIsRecording(false)
      setStatus('Processing...')
    }
  }

  return (
    <div className="glass-panel p-8">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-semibold">Voice Assistant</h2>
        <div className="flex items-center gap-2">
          <div className={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-sm text-gray-600">{isConnected ? 'Connected' : 'Disconnected'}</span>
        </div>
      </div>

      {/* Voice Button */}
      <div className="flex flex-col items-center justify-center py-12">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={!isConnected}
          className={`relative p-8 rounded-full transition-all ${
            isRecording 
              ? 'bg-red-500 hover:bg-red-600 scale-110' 
              : 'bg-blue-600 hover:bg-blue-700'
          } ${!isConnected ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          {isRecording ? (
            <MicOff className="w-12 h-12 text-white" />
          ) : (
            <Mic className="w-12 h-12 text-white" />
          )}
          
          {/* Pulse animation when recording */}
          {isRecording && (
            <div className="absolute inset-0 rounded-full bg-red-500 animate-ping" />
          )}
        </button>
        
        <p className="mt-4 text-sm text-gray-600">{status}</p>
      </div>

      {/* Transcription & Response */}
      <div className="space-y-4">
        {transcription && (
          <div className="p-4 bg-gray-100 dark:bg-gray-800 rounded-lg">
            <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">You said:</p>
            <p className="font-medium">{transcription}</p>
          </div>
        )}
        
        {response && (
          <div className="p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
            <div className="flex items-center gap-2 mb-1">
              <Volume2 className="w-4 h-4 text-blue-600" />
              <p className="text-sm text-blue-600 dark:text-blue-400">AI Response:</p>
            </div>
            <p className="font-medium">{response}</p>
          </div>
        )}
      </div>
    </div>
  )
}