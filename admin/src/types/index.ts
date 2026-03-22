export interface WordComparison {
  target: string | null
  recognized: string | null
  status: 'correct' | 'incorrect' | 'missing' | 'extra'
}

export interface Scores {
  accuracy: number
  completeness: number
  fluency: number
  overall: number
}

export interface EvaluationResult {
  target_text: string
  recognized_text: string
  scores: Scores
  word_comparison: WordComparison[]
}

export interface Practice {
  id: string
  text: string
  category: 'word' | 'phrase' | 'sentence'
  difficulty: 'beginner' | 'intermediate' | 'advanced'
  hint: string | null
  audio_url: string | null
}

export interface PracticeListResponse {
  items: Practice[]
  total: number
}

export interface HealthResponse {
  status: string
  model: {
    name: string
    status: 'not_loaded' | 'loading' | 'ready' | 'error'
  }
}

export type RecordingState = 'idle' | 'recording' | 'recorded' | 'playing'

export type ScoreLevel = 'Excellent' | 'Good' | 'Fair' | 'Poor'

export function getScoreLevel(score: number): ScoreLevel {
  if (score >= 90) return 'Excellent'
  if (score >= 70) return 'Good'
  if (score >= 50) return 'Fair'
  return 'Poor'
}

export function getScoreColor(score: number): string {
  if (score >= 80) return '#22c55e'
  if (score >= 60) return '#eab308'
  if (score >= 40) return '#f97316'
  return '#ef4444'
}

// ─── Auth Types ───

export interface LoginRequest {
  email: string
  password: string
}

export interface UserInfo {
  id: string
  email: string | null
  role: string
  nickname: string | null
  is_active: boolean
  created_at: string
}

export interface AuthResponse {
  user: UserInfo
  access_token: string
  token_type: string
}

// ─── Admin Types ───

export interface AdminUser {
  id: string
  email: string | null
  role: string
  openid: string | null
  nickname: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface PracticeForm {
  text: string
  category: string
  difficulty: string
  hint?: string | null
}

export interface AdminHistoryItem {
  id: string
  practice_id: string | null
  target_text: string
  recognized_text: string
  accuracy: number
  completeness: number
  fluency: number
  overall_score: number
  created_at: string
  user_email: string | null
}

export interface PaginatedResponse<T = unknown> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}