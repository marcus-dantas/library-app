// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  ssr: true,
  runtimeConfig: {
    apiBaseUrl: process.env.API_BASE_URL ?? 'http://localhost:8000/api'
  },
  typescript: {
    strict: true,
    typeCheck: true
  },
  build: {
    transpile: ['vuetify']
  },
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true }
})
