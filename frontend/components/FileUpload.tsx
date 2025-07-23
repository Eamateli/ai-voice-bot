'use client'

import { useState, useCallback } from 'react'
import { Upload, File, CheckCircle, XCircle } from 'lucide-react'

export default function FileUpload() {
  const [isDragging, setIsDragging] = useState(false)
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle')
  const [fileName, setFileName] = useState('')

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(true)
  }, [])

  const handleDragLeave = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
  }, [])

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault()
    setIsDragging(false)
    
    const files = e.dataTransfer.files
    if (files.length > 0) {
      handleFileUpload(files[0])
    }
  }, [])

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (files && files.length > 0) {
      handleFileUpload(files[0])
    }
  }

  const handleFileUpload = async (file: File) => {
    // Validate file type
    if (!file.name.endsWith('.pdf') && !file.name.endsWith('.txt')) {
      alert('Please upload PDF or TXT files only')
      return
    }

    setFileName(file.name)
    setUploadStatus('uploading')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('http://localhost:8000/api/v1/upload', {
        method: 'POST',
        body: formData,
      })

      if (response.ok) {
        const data = await response.json()
        setUploadStatus('success')
        console.log('Upload successful:', data)
        
        // Reset after 3 seconds
        setTimeout(() => {
          setUploadStatus('idle')
          setFileName('')
        }, 3000)
      } else {
        setUploadStatus('error')
        console.error('Upload failed')
      }
    } catch (error) {
      setUploadStatus('error')
      console.error('Upload error:', error)
    }
  }

  return (
    <div className="glass-panel p-6">
      <h2 className="text-xl font-semibold mb-4">Knowledge Base</h2>
      
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`border-2 border-dashed rounded-xl p-8 text-center transition-all ${
          isDragging 
            ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20' 
            : 'border-gray-300 dark:border-gray-600'
        }`}
      >
        <input
          type="file"
          id="file-upload"
          className="hidden"
          accept=".pdf,.txt"
          onChange={handleFileSelect}
        />
        
        {uploadStatus === 'idle' && (
          <>
            <Upload className="w-12 h-12 mx-auto mb-4 text-gray-400" />
            <p className="text-gray-600 dark:text-gray-400 mb-2">
              Drag & drop files here or
            </p>
            <label
              htmlFor="file-upload"
              className="text-blue-600 hover:text-blue-700 cursor-pointer font-medium"
            >
              browse to upload
            </label>
            <p className="text-sm text-gray-500 mt-2">
              PDF or TXT files only
            </p>
          </>
        )}
        
        {uploadStatus === 'uploading' && (
          <div className="flex flex-col items-center">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4" />
            <p className="text-gray-600">Uploading {fileName}...</p>
          </div>
        )}
        
        {uploadStatus === 'success' && (
          <div className="flex flex-col items-center">
            <CheckCircle className="w-12 h-12 text-green-500 mb-4" />
            <p className="text-green-600 font-medium">Upload successful!</p>
            <p className="text-sm text-gray-600 mt-1">{fileName}</p>
          </div>
        )}
        
        {uploadStatus === 'error' && (
          <div className="flex flex-col items-center">
            <XCircle className="w-12 h-12 text-red-500 mb-4" />
            <p className="text-red-600 font-medium">Upload failed</p>
            <button
              onClick={() => setUploadStatus('idle')}
              className="text-sm text-blue-600 hover:text-blue-700 mt-2"
            >
              Try again
            </button>
          </div>
        )}
      </div>
      
      <div className="mt-4">
        <p className="text-xs text-gray-500">
          Files are processed and indexed for AI responses
        </p>
      </div>
    </div>
  )
}