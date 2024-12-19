import { ref } from 'vue'
import type { Book } from '~/types'

export function useBooks() {
  const { fetchApi } = useApi()
  
  const books = ref<Book[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)
  
  function filterBooks(items: Book[], query: string, onlyAvailable: boolean) {
    let result = [...items]
    
    if (query) {
      const loweredQuery = query.toLowerCase()
      result = result.filter(book => 
        book.title.toLowerCase().includes(loweredQuery) ||
        book.author.toLowerCase().includes(loweredQuery) ||
        book.isbn.includes(loweredQuery) ||
        book.description?.toLowerCase().includes(loweredQuery) || false
      )
    }
    
    if (onlyAvailable) {
      result = result.filter(book => book.available_copies > 0)
    }
    
    return result
  }

  async function fetchBooks() {
    loading.value = true
    error.value = null
    
    try {
      const response = await fetchApi<Book[]>('/api/books/')
      books.value = response
    } catch (err: any) {
      error.value = 'Failed to fetch books: ' + (err.message || 'Unknown error')
      throw err
    } finally {
      loading.value = false
    }
  }

  async function loanBook(bookId: number) {
    try {
      await fetchApi('/api/loans/create/', {
        method: 'POST',
        body: { book_id: bookId }
      })
      await fetchBooks()
      return true
    } catch (err: any) {
      const errorMessage = err.response?.data?.message || 'Failed to loan book'
      throw new Error(errorMessage)
    }
  }

  return {
    books,
    loading,
    error,
    fetchBooks,
    loanBook,
    filterBooks
  }
}
