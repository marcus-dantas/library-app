// utils/csrf.ts
/**
 * Retrieves the CSRF token from cookies, handling both client and server-side contexts.
 * This function is designed to work with Django's CSRF protection system.
 * 
 * @returns {string} The CSRF token if found in cookies, empty string otherwise
 */
export function getCSRFToken(): string {
  if (import.meta.server) return ''
  
  const name = 'csrftoken'
  let cookieValue = ''
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (const rawCookie of cookies) {
      const cookie = rawCookie.trim()
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}
