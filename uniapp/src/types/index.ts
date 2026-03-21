export interface Practice {
  id: string
  text: string
  category: 'word' | 'phrase' | 'sentence'
  difficulty: 'easy' | 'medium' | 'hard'
  hint?: string
  created_at?: string
  updated_at?: string
}

export interface PracticeListResponse {
  items: Practice[]
  total: number
}

export interface PaginatedResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
  total_pages: number
}

export interface WordComparison {
  word: string
  status: 'correct' | 'incorrect' | 'missing' | 'extra'
}

export interface EvaluationResult {
  id?: string
  target_text: string
  recognized_text: string
  accuracy: number
  completeness: number
  fluency: number
  overall_score: number
  word_comparison: WordComparison[]
  practice_id?: string
  created_at?: string
}

export interface User {
  id: string
  email?: string
  nickname?: string
  role: 'admin' | 'user'
  openid?: string
  is_active?: boolean
  created_at?: string
}

export interface HistoryItem {
  id: string
  target_text: string
  recognized_text: string
  accuracy: number
  completeness: number
  fluency: number
  overall_score: number
  word_comparison: WordComparison[]
  practice_id?: string
  created_at: string
}