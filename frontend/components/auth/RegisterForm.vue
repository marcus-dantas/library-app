<template>
  <v-card class="pa-4">
    <v-card-title class="text-center">
      Create Your Library Account
    </v-card-title>
    
    <v-form @submit.prevent="submitRegistration" class="mt-4">
      <v-text-field
        v-model="form.username"
        label="Username"
        :error-messages="validationErrors.username"
        required
      />
      
      <v-text-field
        v-model="form.email"
        label="Email Address"
        type="email"
        :error-messages="validationErrors.email"
        required
      />
      
      <v-text-field
        v-model="form.password"
        label="Password"
        type="password"
        :error-messages="validationErrors.password"
        required
      />
      
      <v-text-field
        v-model="form.confirmPassword"
        label="Confirm Password"
        type="password"
        :error-messages="validationErrors.confirmPassword"
        required
      />
      
      <v-btn 
        type="submit" 
        color="primary" 
        block 
        size="large"
        :loading="isSubmitting"
      >
        Register
      </v-btn>
    </v-form>
    
    <v-card-text class="text-center mt-4">
      Already have an account? 
      <nuxt-link to="/login">
        Log in
      </nuxt-link>
    </v-card-text>
  </v-card>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from '~/stores/auth'

// Define form state
const form = ref({
  username: '',
  email: '',
  password: '',
  confirmPassword: ''
})

// Validation and submission state
const validationErrors = ref({})
const isSubmitting = ref(false)

// Get auth store for registration
const authStore = useAuthStore()

async function submitRegistration() {
  // Reset previous errors
  validationErrors.value = {}
  isSubmitting.value = true

  try {
    // Call registration method from auth store
    await authStore.register({
      username: form.value.username,
      email: form.value.email,
      password: form.value.password,
      confirmPassword: form.value.confirmPassword
    })

    // Redirect on successful registration
    navigateTo('/dashboard')
  } catch (error) {
    // Handle registration errors
    if (error.response && error.response.data.errors) {
      validationErrors.value = error.response.data.errors
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>
