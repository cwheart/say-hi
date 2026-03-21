import { getToken, setToken, setUser, clearAll } from './storage'
import { post } from './request'

interface LoginResponse {
  access_token: string
  token_type: string
  user: {
    id: string
    email?: string
    nickname?: string
    role: string
  }
}

/**
 * WeChat silent login (MP-WEIXIN only)
 * Calls uni.login() to get a code, sends to backend /api/wx/login
 */
export function wxLogin(): Promise<void> {
  return new Promise((resolve, reject) => {
    // #ifdef MP-WEIXIN
    uni.login({
      success: async (loginRes) => {
        if (!loginRes.code) {
          reject(new Error('wx.login failed: no code'))
          return
        }
        try {
          const data = await post<LoginResponse>('/wx/login', {
            code: loginRes.code,
          })
          setToken(data.access_token)
          setUser(data.user)
          resolve()
        } catch (e) {
          reject(e)
        }
      },
      fail: (err) => {
        reject(new Error(err.errMsg || 'wx.login failed'))
      },
    })
    // #endif

    // #ifdef H5
    reject(new Error('wxLogin is not available on H5'))
    // #endif
  })
}

/**
 * H5 email/password login
 */
export async function h5Login(email: string, password: string): Promise<void> {
  const data = await post<LoginResponse>('/auth/login', { email, password })
  setToken(data.access_token)
  setUser(data.user)
}

/**
 * Ensure the user is logged in.
 * - MP-WEIXIN: auto wx login if no token
 * - H5: redirect to login page if no token
 */
export async function ensureLogin(): Promise<void> {
  const token = getToken()
  if (token) return

  // #ifdef MP-WEIXIN
  await wxLogin()
  // #endif

  // #ifdef H5
  uni.reLaunch({ url: '/pages/login/login' })
  throw new Error('Not logged in, redirecting to login page')
  // #endif
}

/**
 * Logout: clear stored credentials and redirect
 */
export function logout(): void {
  clearAll()

  // #ifdef MP-WEIXIN
  // On MP-WEIXIN, just clear data. Next request will trigger re-login.
  // #endif

  // #ifdef H5
  uni.reLaunch({ url: '/pages/login/login' })
  // #endif
}

/**
 * Check if user is currently logged in (has token)
 */
export function isLoggedIn(): boolean {
  return !!getToken()
}