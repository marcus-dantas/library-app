<template>
  <v-container>
    <v-row v-if="!isAuthenticated" class="mb-6">
      <v-col cols="12">
        <h1 class="text-h3 text-center">Welcome to Library App</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col sm="8" md="6" lg="4" class="mx-auto">
        <v-card class="h-100">
          <template v-if="loading">
            <v-card-text class="text-center">
              <v-progress-circular indeterminate />
            </v-card-text>
          </template>

          <template v-else-if="!isAuthenticated">
            <v-card-title class="text-h5 text-center">
              Get Started
            </v-card-title>
            <v-card-actions>
              <v-btn
                to="/login"
                color="primary"
                prepend-icon="mdi-login"
              >
                Login
              </v-btn>
            </v-card-actions>
          </template>

          <template v-else>
            <v-card-title class="text-h5 text-center">
              Welcome Back, {{ user?.username }}!
            </v-card-title>
            <v-card-text>
              <p class="text-body-1">
                Access your profile to view your current loans and manage your library
                activities. We're glad to have you back!
              </p>
            </v-card-text>
            <v-card-actions>
              <v-btn
                color="primary"
                to="/books"
                prepend-icon="mdi-book"
              >
                Books
              </v-btn>
              <v-btn
                color="teal"
                to="/profile"
                prepend-icon="mdi-account"
              >
                Profile
              </v-btn>
            </v-card-actions>
          </template>
        </v-card>

      </v-col>
    </v-row>
    <v-row>
      <template v-if="isAuthenticated">
        <v-container class="mx-6 px-6">
            <UserList />
        </v-container>
      </template>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue';
import UserList from '~/components/user/UserList.vue';

const { user, isAuthenticated, checkAuth } = useAuth()
const loading = ref(true)
const error = ref<string | null>(null)

onMounted(async () => {
  try {
    await checkAuth()
  } catch (error) {
    console.error('Error checking authentication:', error)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.h-100 {
  height: 100%;
}
</style>
