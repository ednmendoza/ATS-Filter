'use client'

import { useState } from 'react'
import { jdApi } from '@/lib/api'

interface JobDescriptionInputProps {
  onJdCreated: (jdId: string) => void
}

export default function JobDescriptionInput({ onJdCreated }: JobDescriptionInputProps) {
  const [platform, setPlatform] = useState('linkedin')
  const [rawText, setRawText] = useState('')
  const [creating, setCreating] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [success, setSuccess] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!rawText.trim()) {
      setError('Please enter a job description')
      return
    }

    setCreating(true)
    setError(null)

    try {
      const jd = await jdApi.create(platform, rawText)
      setSuccess(true)
      onJdCreated(jd.id)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create job description. Please try again.')
    } finally {
      setCreating(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Platform
        </label>
        <select
          value={platform}
          onChange={(e) => setPlatform(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
        >
          <option value="linkedin">LinkedIn</option>
          <option value="indeed">Indeed</option>
          <option value="dice">Dice</option>
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
          Job Description
        </label>
        <textarea
          value={rawText}
          onChange={(e) => setRawText(e.target.value)}
          rows={10}
          placeholder="Paste the job description here..."
          className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-400 resize-none"
        />
      </div>

      {error && (
        <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded text-red-700 dark:text-red-400 text-sm">
          {error}
        </div>
      )}

      {success && (
        <div className="p-3 bg-green-50 dark:bg-green-900/20 border border-green-200 dark:border-green-800 rounded text-green-700 dark:text-green-400 text-sm">
          Job description processed successfully!
        </div>
      )}

      <button
        type="submit"
        disabled={creating || !rawText.trim()}
        className="w-full px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
      >
        {creating ? 'Processing...' : 'Process Job Description'}
      </button>
    </form>
  )
}
