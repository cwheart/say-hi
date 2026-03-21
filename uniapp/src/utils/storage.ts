const TOKEN_KEY = 'say_hi_token'
const USER_KEY = 'say_hi_user'

export function getToken(): string {
  return uni.getStorageSync(TOKEN_KEY) || ''
}

export function setToken(token: string): void {
  uni.setStorageSync(TOKEN_KEY, token)
}

export function removeToken(): void {
  uni.removeStorageSync(TOKEN_KEY)
}

export interface StoredUser {
  id: string
  email?: string
  nickname?: string
  role: string
}

export function getUser(): StoredUser | null {
  const raw = uni.getStorageSync(USER_KEY)
  if (!raw) return null
  try {
    return typeof raw === 'string' ? JSON.parse(raw) : raw
  } catch {
    return null
  }
}

export function setUser(user: StoredUser): void {
  uni.setStorageSync(USER_KEY, JSON.stringify(user))
}

export function removeUser(): void {
  uni.removeStorageSync(USER_KEY)
}

export function clearAll(): void {
  removeToken()
  removeUser()
}