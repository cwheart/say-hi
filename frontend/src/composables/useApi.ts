import axios from 'axios'
import type {
  EvaluationResult,
  PracticeListResponse,
  Practice,
  HealthResponse,
  PaginatedResponse,
  HistoryDetail,
  HistoryItem,
} from '../types'
import { useAuth } from './useAuth'
import router from '../router'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

// Request interceptor: attach JWT token
api.interceptors.request.use((config) => {
  const { getToken } = useAuth()
  const token = getToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor: handle 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const { logout } = useAuth()
      logout()
      router.push('/login')
    }
    return Promise.reject(error)
  }
)

export function useApi() {
  async function evaluatePronunciation(
    audioBlob: Blob,
    targetText: string,
    practiceId?: string
  ): Promise<EvaluationResult> {
    const formData = new FormData()
    formData.append('audio', audioBlob, 'recording.webm')
    formData.append('target_text', targetText)
    if (practiceId) {
      formData.append('practice_id', practiceId)
    }

    const response = await api.post<EvaluationResult>('/evaluate', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return response.data
  }

  async function getPractices(
    category?: string,
    difficulty?: string
  ): Promise<PracticeListResponse> {
    const params: Record<string, string> = {}
    if (category) params.category = category
    if (difficulty) params.difficulty = difficulty

    const response = await api.get<PracticeListResponse>('/practices', { params })
    return response.data
  }

  async function getPracticeById(id: string): Promise<Practice> {
    const response = await api.get<Practice>(`/practices/${id}`)
    return response.data
  }

  async function getHealth(): Promise<HealthResponse> {
    const response = await api.get<HealthResponse>('/health')
    return response.data
  }

  async function getHistory(
    page: number = 1,
    pageSize: number = 10
  ): Promise<PaginatedResponse<HistoryItem>> {
    const response = await api.get<PaginatedResponse<HistoryItem>>('/history', {
      params: { page, page_size: pageSize },
    })
    return response.data
  }

  async function getHistoryById(id: string): Promise<HistoryDetail> {
    const response = await api.get<HistoryDetail>(`/history/${id}`)
    return response.data
  }

  async function getBestScore(practiceId: string): Promise<number | null> {
    try {
      const response = await api.get<PaginatedResponse<HistoryItem>>('/history', {
        params: { page: 1, page_size: 50 },
      })
      const matching = response.data.items.filter(
        (item) => item.practice_id === practiceId
      )
      if (matching.length === 0) return null
      return Math.max(...matching.map((item) => item.overall_score))
    } catch {
      return null
    }
  }

  return {
    evaluatePronunciation,
    getPractices,
    getPracticeById,
    getHealth,
    getHistory,
    getHistoryById,
    getBestScore,
  }
}