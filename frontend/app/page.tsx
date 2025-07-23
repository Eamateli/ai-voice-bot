'use client'

import { useState } from 'react'
import VoiceInterface from '@/components/VoiceInterface'
import FileUpload from '@/components/FileUpload'
import Analytics from '@/components/Analytics'

export default function Dashboard() {
  const [isRecording, setIsRecording] = useState(false)

  return (
    <div className="min-h-screen p-4 md:p-8">
      {/* Header */}
      <header className="max-w-7xl mx-auto mb-8">
        <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
          AI Voice Assistant
        </h1>
        <p className="text-gray-600 dark:text-gray-400 mt-2">
          Intelligent customer service powered by your knowledge base
        </p>
      </header>

      {/* Main Grid */}
      <div className="max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Voice Interface - Takes 2 columns */}
        <div className="lg:col-span-2">
          <VoiceInterface isRecording={isRecording} setIsRecording={setIsRecording} />
        </div>

        {/* Right Column */}
        <div className="space-y-6">
          <FileUpload />
          <Analytics />
        </div>
      </div>
    </div>
  )
}