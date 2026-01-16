'use client'

import { useState } from 'react'
import ResumeUpload from '@/components/ResumeUpload'
import JobDescriptionInput from '@/components/JobDescriptionInput'
import VariantComparison from '@/components/VariantComparison'

export default function Home() {
  const [resumeId, setResumeId] = useState<string | null>(null)
  const [jdId, setJdId] = useState<string | null>(null)
  const [variants, setVariants] = useState<any[]>([])

  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800">
      <div className="container mx-auto px-4 py-8 max-w-7xl">
        <header className="mb-8 text-center">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-2">
            ATS Resume Compiler
          </h1>
          <p className="text-gray-600 dark:text-gray-300">
            Translate your resume into ATS-optimized variants
          </p>
        </header>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-900 dark:text-white">
              Upload Resume
            </h2>
            <ResumeUpload onUploadSuccess={setResumeId} />
          </div>

          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-900 dark:text-white">
              Job Description
            </h2>
            <JobDescriptionInput onJdCreated={setJdId} />
          </div>
        </div>

        {resumeId && jdId && (
          <div className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-6">
            <h2 className="text-2xl font-semibold mb-4 text-gray-900 dark:text-white">
              Resume Variants
            </h2>
            <VariantComparison resumeId={resumeId} jdId={jdId} />
          </div>
        )}
      </div>
    </main>
  )
}
