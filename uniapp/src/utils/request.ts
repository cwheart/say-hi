import { getToken, clearAll } from './storage'

const BASE_URL = '/api'

interface RequestOptions {
  url: string
  method?: 'GET' | 'POST' | 'PUT' | 'DELETE'
  data?: any
  header?: Record<string, string>
}

interface ApiResponse<T = any> {
  statusCode: number
  data: T
}

let isRefreshing = false
let pendingRequests: Array<() => void> = []

function getAuthHeader(): Record<string, string> {
  const token = getToken()
  return token ? { Authorization: `Bearer ${token}` } : {}
}

async function handle401(): Promise<void> {
  // #ifdef MP-WEIXIN
  if (isRefreshing) return
  isRefreshing = true
  try {
    const { wxLogin } = await import('./auth')
    await wxLogin()
    pendingRequests.forEach((cb) => cb())
    pendingRequests = []
  } catch (e) {
    clearAll()
  } finally {
    isRefreshing = false
  }
  // #endif

  // #ifdef H5
  clearAll()
  uni.reLaunch({ url: '/pages/login/login' })
  // #endif
}

export function request<T = any>(options: RequestOptions): Promise<T> {
  return new Promise((resolve, reject) => {
    const { url, method = 'GET', data, header = {} } = options

    uni.request({
      url: `${BASE_URL}${url}`,
      method,
      data,
      header: {
        'Content-Type': 'application/json',
        ...getAuthHeader(),
        ...header,
      },
      success: (res) => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data as T)
        } else if (res.statusCode === 401) {
          handle401()
          reject(new Error('Unauthorized'))
        } else {
          reject(new Error((res.data as any)?.detail || `HTTP ${res.statusCode}`))
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || 'Network error'))
      },
    })
  })
}

// Convenience methods
export function get<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({ url, method: 'GET', data })
}

export function post<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({ url, method: 'POST', data })
}

export function put<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({ url, method: 'PUT', data })
}

export function del<T = any>(url: string, data?: any): Promise<T> {
  return request<T>({ url, method: 'DELETE', data })
}