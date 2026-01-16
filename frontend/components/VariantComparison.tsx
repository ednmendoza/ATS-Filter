'use client'

import { useState, useEffect } from 'react'
import { variantApi, ResumeVariant } from '@/lib/api'

interface VariantComparisonProps {
  resumeId: string
  jdId: string
}

export default function VariantComparison({ resumeId, jdId }: VariantComparisonProps) {
  const [persona, setPersona] = useState('ic')
  const [platform, setPlatform] = useState('linkedin')
  const [variants, setVariants] = useState<ResumeVariant[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [selectedVariant, setSelectedVariant] = useState<ResumeVariant | null>(null)

  const compileVariant = async () => {
    setLoading(true)
    setError(null)

    try {
      const variant = await variantApi.compile(resumeId, jdId, persona, platform)
      setVariants([...variants, variant])
      setSelectedVariant(variant)
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to compile variant. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    // Load existing variants
    const loadVariants = async () => {
      try {
        const existing = await variantApi.list(resumeId, jdId)
        setVariants(existing)
        if (existing.length > 0) {
          setSelectedVariant(existing[0])
        }
      } catch (err) {
        console.error('Failed to load variants:', err)
      }
    }
    loadVariants()
  }, [resumeId, jdId])

  return (
    <div className="space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
            Persona
          </label>
          <select
            value={persona}
            onChange={(e) => setPersona(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
          >
            <option value="ic">Individual Contributor</option>
            <option value="architect">Architect</option>
            <option value="hybrid">Hybrid</option>
          </select>
        </div>

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
      </div>

      <button
        onClick={compileVariant}
        disabled={loading}
        className="w-full px-4 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed text-white rounded-lg font-medium transition-colors"
      >
        {loading ? 'Compiling...' : 'Compile Variant'}
      </button>

      {error && (
        <div className="p-3 bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded text-red-700 dark:text-red-400 text-sm">
          {error}
        </div>
      )}

      {variants.length > 0 && (
        <div className="space-y-4">
          <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
            Compiled Variants
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {variants.map((variant) => (
              <div
                key={variant.id}
                onClick={() => setSelectedVariant(variant)}
                className={`p-4 border rounded-lg cursor-pointer transition-colors ${
                  selectedVariant?.id === variant.id
                    ? 'border-blue-500 bg-blue-50 dark:bg-blue-900/20'
                    : 'border-gray-300 dark:border-gray-600 hover:border-gray-400'
                }`}
              >
                <div className="text-sm font-medium text-gray-900 dark:text-white mb-2">
                  {variant.persona.toUpperCase()} - {variant.platform.toUpperCase()}
                </div>
                {variant.scores && (
                  <div className="text-xs text-gray-600 dark:text-gray-400">
                    Survivability: {(variant.scores.survivability * 100).toFixed(0)}%
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      {selectedVariant && (
        <div className="mt-6 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
              Compiled Resume
            </h3>
            {selectedVariant.scores && (
              <div className="text-sm text-gray-600 dark:text-gray-400">
                <div>Keyword: {(selectedVariant.scores.keyword_score * 100).toFixed(0)}%</div>
                <div>Title: {(selectedVariant.scores.title_score * 100).toFixed(0)}%</div>
                <div className="font-semibold text-indigo-600 dark:text-indigo-400">
                  Overall: {(selectedVariant.scores.survivability * 100).toFixed(0)}%
                </div>
              </div>
            )}
          </div>
          
          <div className="p-4 bg-gray-50 dark:bg-gray-900 rounded-lg border border-gray-200 dark:border-gray-700">
            <pre className="whitespace-pre-wrap text-sm text-gray-800 dark:text-gray-200 font-mono">
              {selectedVariant.compiled_text}
            </pre>
          </div>

          <button
            onClick={() => {
              const blob = new Blob([selectedVariant.compiled_text], { type: 'text/plain' })
              const url = URL.createObjectURL(blob)
              const a = document.createElement('a')
              a.href = url
              a.download = `resume-${selectedVariant.persona}-${selectedVariant.platform}.txt`
              a.click()
              URL.revokeObjectURL(url)
            }}
            className="px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium transition-colors"
          >
            Download as TXT
          </button>
        </div>
      )}
    </div>
  )
}
