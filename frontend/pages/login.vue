<template>
  <v-container fluid fill-height>
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-card-title class="text-center">
            Login
          </v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Username"
                name="username"
                prepend-icon="mdi-account"
                type="text"
                required
              />
              <v-text-field
                v-model="password"
                label="Password"
                name="password"
                type="password"
                prepend-icon="mdi-lock"
                required
              />
              <v-alert
                v-if="error"
                type="error"
                dismissible
                outlined
                class="mb-4"
              >
                {{ error }}
              </v-alert>
              <v-btn
                type="submit"
                color="primary"
                block
                class="mt-4"
                :loading="loading"
              >
                Login
              </v-btn>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-spacer />
            <v-btn
              to="/register"
              text-color="primary"
            >
              Don't have an account? Register
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const { login } = useAuth()
const router = useRouter()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  loading.value = true
  error.value = ''

  try {
    await login({
      username: username.value,
      password: password.value
    })
  } catch (e: any) {
    if (e.response?.status === 403) {
      error.value = 'Session expired. Please refresh the page and try again.'
    } else if (e.response?.status === 401) {
      error.value = 'Invalid username or password'
    } else if (e.response?.data?.message) {
      error.value = e.response.data.message
    } else {
      error.value = 'An unexpected error occurred. Please try again.'
    }
    console.error('Login failed:', e)
  } finally {
    loading.value = false
  }
}
</script>
