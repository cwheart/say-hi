import { ref, computed } from 'vue'
import axios from 'axios'
import type { AuthResponse, UserInfo, LoginRequest, RegisterRequest } from '../types'
import router from '../router'

const TOKEN_KEY = 'sayhi_token'
const USER_KEY = 'sayhi_user'

const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
const user = ref<UserInfo | null>(
  localStorage.getItem(USER_KEY) ? JSON.parse(localStorage.getItem(USER_KEY)!) : null
)

const api = axios.create({ baseURL: '/api' })

export function useAuth() {
  const isAuthenticated = computed(() => !!token.value)

  function setAuth(authResponse: AuthResponse) {
    token.value = authResponse.access_token
    user.value = authResponse.user
    localStorage.setItem(TOKEN_KEY, authResponse.access_token)
    localStorage.setItem(USER_KEY, JSON.stringify(authResponse.user))
  }

  function clearAuth() {
    token.value = null
    user.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
  }

  async function login(data: LoginRequest): Promise<void> {
    const response = await api.post<AuthResponse>('/auth/login', data)
    setAuth(response.data)
  }

  async function register(data: RegisterRequest): Promise<void> {
    const response = await api.post<AuthResponse>('/auth/register', data)
    setAuth(response.data)
  }

  function logout() {
    clearAuth()
    router.push('/login')
  }

  function getToken(): string | null {
    return token.value
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    getToken,
  }
}
