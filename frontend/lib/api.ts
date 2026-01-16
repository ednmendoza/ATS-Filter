import axios from 'axios'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export interface Resume {
  id: string
  user_id: string
  raw_text: string
  parsed_json: any
  created_at: string
}

export interface JobDescription {
  id: string
  platform: string
  raw_text: string
  extracted_signals: any
  created_at: string
}

export interface ResumeVariant {
  id: string
  resume_id: string
  jd_id: string
  persona: string
  platform: string
  compiled_text: string
  scores: {
    keyword_score: number
    title_score: number
    age_proxy_risk: number
    overqual_risk: number
    survivability: number
  }
  created_at: string
}

export const resumeApi = {
  upload: async (file: File, userId: string = 'default_user'): Promise<Resume> => {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('user_id', userId)
    
    // Don't set Content-Type header - axios will set it automatically with boundary
    const response = await api.post<Resume>('/resumes/upload', formData)
    return response.data
  },

  get: async (resumeId: string): Promise<Resume> => {
    const response = await api.get<Resume>(`/resumes/${resumeId}`)
    return response.data
  },

  list: async (userId: string = 'default_user'): Promise<Resume[]> => {
    const response = await api.get<Resume[]>('/resumes', {
      params: { user_id: userId },
    })
    return response.data
  },
}

export const jdApi = {
  create: async (platform: string, rawText: string): Promise<JobDescription> => {
    const response = await api.post<JobDescription>('/jds', {
      platform,
      raw_text: rawText,
    })
    return response.data
  },

  get: async (jdId: string): Promise<JobDescription> => {
    const response = await api.get<JobDescription>(`/jds/${jdId}`)
    return response.data
  },
}

export const variantApi = {
  compile: async (
    resumeId: string,
    jdId: string,
    persona: string,
    platform: string
  ): Promise<ResumeVariant> => {
    const response = await api.post<ResumeVariant>('/variants/compile', {
      resume_id: resumeId,
      jd_id: jdId,
      persona,
      platform,
    })
    return response.data
  },

  get: async (variantId: string): Promise<ResumeVariant> => {
    const response = await api.get<ResumeVariant>(`/variants/${variantId}`)
    return response.data
  },

  list: async (resumeId?: string, jdId?: string): Promise<ResumeVariant[]> => {
    const response = await api.get<ResumeVariant[]>('/variants', {
      params: { resume_id: resumeId, jd_id: jdId },
    })
    return response.data
  },
}

export default api
