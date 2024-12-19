import { ref, readonly } from 'vue'
import type { User, LoginCredentials, LoginResponse } from '~/types/index'
import { createCommonFetchOptions, mergeFetchOptions } from '~/utils/api'

export function useAuth() {
  const config = useRuntimeConfig()
  const router = useRouter()
  const baseOptions = createCommonFetchOptions(config)
  const user = ref<User | null>(null)
  const isAuthenticated = ref(false)
  const loading = ref(false)
  const { fetchApi } = useApi()

  async function checkAuth() {
    loading.value = true
    try {
      const fetchOptions = mergeFetchOptions(baseOptions, {
        method: 'GET'
      })

      const response = await fetchApi<User>('/api/users/me/', fetchOptions)
      
      if (response?.username) {
        user.value = {
          id: response.id,
          username: response.username,
          email: response.email,
          is_admin: response.is_admin,
          profile: response.profile
        }
        isAuthenticated.value = true
        return true
      }
    } catch (error: any) {
      user.value = null
      isAuthenticated.value = false
      if (error.response?.status !== 401 && error.response?.status !== 403) {
        throw new Error('Authentication check failed: ' + error.message)
      }
      return false
    } finally {
      loading.value = false
    }
  }

  async function login(credentials: LoginCredentials) {
    try {
      const loginOptions = mergeFetchOptions(baseOptions, {
        method: 'POST',
        body: JSON.stringify(credentials),
      })

      const response = await fetchApi<LoginResponse>('/api/auth/login/', loginOptions)

      if (response?.username) {
        user.value = {
          id: response.user_id,
          username: response.username,
          email: response.email,
          is_admin: response.is_admin,
          profile: response.profile
        }
        isAuthenticated.value = true
        await router.push('/books/')
        return true
      }
      return false
    } catch (error: any) {
      if (error.response?.status === 403) {
        throw new Error('Authentication failed: CSRF verication failed')
      } 
      console.error('Login failed:', error)
      throw error
    }
  }

  async function logout() {
    try {
      const logoutOptions = mergeFetchOptions(baseOptions, {
        method: 'POST'
      })

      await fetchApi('/api/auth/logout/', logoutOptions)
    } finally {
      user.value = null
      isAuthenticated.value = false
      await router.push('/login/')
    }
  }

  return {
    user: readonly(user),
    isAuthenticated: readonly(isAuthenticated),
    login,
    logout,
    checkAuth
  }
}
