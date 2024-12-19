import axios from 'axios'

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// Add token to requests if available
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

export const authAPI = {
  login: (credentials: { username: string; password: string }) =>
    api.post('/auth/login/', credentials),
    
  register: (userData: { username: string; password: string; email: string }) =>
    api.post('/auth/register/', userData),
    
  logout: () => api.post('/auth/logout/')
}

export const booksAPI = {
  getAll: () => api.get('/books/'),
  
  getOne: (id: number) => api.get(`/books/${id}/`),
  
  requestBook: (bookId: number, notes: string) =>
    api.post('/book-requests/', { book_id: bookId, notes }),
    
  getMyRequests: () => api.get('/book-requests/')
}

export const userAPI = {
  getProfile: () => api.get('/users/me/'),
  
  createLoan: (bookId: number) =>
    api.post('/loans/create/', { book_id: bookId })
}
