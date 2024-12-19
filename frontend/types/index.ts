export interface User {
  id: number
  username: string
  email: string
  is_admin: boolean
  profile: UserProfile
}

export interface UserProfile {
  id: number
  username: string
  email: string
  full_name: string
  active_loans: BookLoan[]
  loan_history: BookLoan[]
  can_borrow: boolean
}

export interface BookLoan {
  id: number
  book: Book
  user_name: string
  loan_date: string
  due_date: string
  return_date: string | null
  status: 'ACTIVE' | 'OVERDUE' | 'RETURNED'
  days_remaining: number
}

export interface Book {
  id: number
  title: string
  author: string
  isbn: string
  description: string
  publication_year: number
  available_copies: number
  total_copies: number
  current_loans?: BookLoan[]
}

export interface LoginCredentials {
  username: string
  password: string
}

export interface LoginResponse {
  user_id: number
  username: string
  is_admin: boolean
  email: string
  profile: UserProfile
}
