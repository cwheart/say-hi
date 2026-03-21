import axios from 'axios'
import type {
  Practice,
  HealthResponse,
  PaginatedResponse,
  AdminUser,
  PracticeForm,
  AdminHistoryItem,
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
  // ─── Health ───
  async function getHealth(): Promise<HealthResponse> {
    const response = await api.get<HealthResponse>('/health')
    return response.data
  }

  // ─── Admin Users ───
  async function getUsers(page = 1, pageSize = 20): Promise<PaginatedResponse<AdminUser>> {
    const response = await api.get<PaginatedResponse<AdminUser>>('/admin/users', {
      params: { page, page_size: pageSize },
    })
    return response.data
  }

  async function disableUser(userId: string): Promise<AdminUser> {
    const response = await api.patch<AdminUser>(`/admin/users/${userId}/disable`)
    return response.data
  }

  async function enableUser(userId: string): Promise<AdminUser> {
    const response = await api.patch<AdminUser>(`/admin/users/${userId}/enable`)
    return response.data
  }

  // ─── Admin Practices ───
  async function getPractices(): Promise<{ items: Practice[]; total: number }> {
    const response = await api.get<{ items: Practice[]; total: number }>('/admin/practices')
    return response.data
  }

  async function createPractice(data: PracticeForm): Promise<Practice> {
    const response = await api.post<Practice>('/admin/practices', data)
    return response.data
  }

  async function updatePractice(id: string, data: Partial<PracticeForm>): Promise<Practice> {
    const response = await api.put<Practice>(`/admin/practices/${id}`, data)
    return response.data
  }

  async function deletePractice(id: string): Promise<void> {
    await api.delete(`/admin/practices/${id}`)
  }

  // ─── Admin History ───
  async function getHistory(
    page = 1,
    pageSize = 20,
    userId?: string
  ): Promise<PaginatedResponse<AdminHistoryItem>> {
    const params: Record<string, string | number> = { page, page_size: pageSize }
    if (userId) params.user_id = userId
    const response = await api.get<PaginatedResponse<AdminHistoryItem>>('/admin/history', { params })
    return response.data
  }

  return {
    getHealth,
    getUsers,
    disableUser,
    enableUser,
    getPractices,
    createPractice,
    updatePractice,
    deletePractice,
    getHistory,
  }
}