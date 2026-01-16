'use client'

import { useState } from 'react'
import { resumeApi } from '@/lib/api'

interface ResumeUploadProps {
  onUploadSuccess: (resumeId: string) => void
}

export default function ResumeUpload({ onUploadSuccess }: ResumeUploadProps) {
  const [file, setFile] = useState<File | null>(null)
  const [uploading, setUploading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const selectedFile = e.target.files[0]
      const validTypes = ['.pdf', '.docx', '.txt']
      const fileExtension = selectedFile.name.toLowerCase().substring(selectedFile.name.lastIndexOf('.'))
      
      if (!validTypes.includes(fileExtension)) {
        setError('Please upload a PDF, DOCX, or TXT file')
        return
      }
      
      setFile(selectedFile)
      setError(null)
      setSuccess(false)
    }
  }

  const handleUpload = async () => {
    if (!file) {
      setError('Please select a file')
      return
    }

    setUploading(true)
    setError(null)

    try {
      const resume = await resumeApi.upload(file)
      setSuccess(true)
      onUploadSuccess(resume.id)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    } finally {
      setUploading(false)
    }
  }

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Select Resume File
        </label>
        <input
          type="file"
          accept=".pdf,.docx,.txt"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-500
            file:mr-4 file:py-2 file:px-4
            file:rounded-full file:border-0
            file:text-sm file:font-semibold
            file:bg-blue-50 file:text-blue-700
            hover:file:bg-blue-100
            dark:file:bg-blue-900 dark:file:text-blue-300"
        />
      </div>

      {file && (
        <div className="text-sm text-gray-600 dark:text-gray-400">
          Selected: {file.name}
        </div>
      )}

      {error && (
        <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded text-red-700 dark:text-red-400 text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded text-green-700 dark:text-green-400 text-sm">
          Resume uploaded successfully!
        </div>
      )}

      <button
        onClick={handleUpload}
        disabled={!file || uploading}
        className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
      >
        {uploading ? 'Uploading...' : 'Upload Resume'}
      </button>
    </div>
  )
}
