export default defineNuxtConfig({
  ssr: false,
  app: {
    head: {
      title: 'Library App'
    }
  },
  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.API_BASE_URL || 'http://localhost:8000'
    }
  },
  nitro: {
    devProxy: {
      '/api': {
        target: 'http://localhost:8000/api',
        changeOrigin: true,
        prependPath: true,
      }
    }
  },
  typescript: {
    strict: true,
    typeCheck: true
  },
  css: [
    'vuetify/lib/styles/main.css',
    '@mdi/font/css/materialdesignicons.min.css'
  ],
  build: {
    transpile: ['vuetify']
  },
  imports: {
    dirs: ['stores']
  },
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true }
})
