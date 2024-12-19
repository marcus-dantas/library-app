import { defineNuxtRouteMiddleware, navigateTo } from 'nuxt/app'

export default defineNuxtRouteMiddleware(async (to, from) => {
  const { checkAuth } = useAuth()
  const isAuthed = await checkAuth()

    if (to.path === '/login/') {
      if (isAuthed) {
        console.log('Already authenticated, redirecting to books')
        return navigateTo('/books/')
      }
      return
    }
  
    if (!isAuthed) {
      console.log('Not authenticated, redirecting to login')
      return navigateTo('/login/')
    }
})
