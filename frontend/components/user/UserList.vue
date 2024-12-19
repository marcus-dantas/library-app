<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchQuery"
          label="Search users"
          prepend-inner-icon="mdi-magnify"
          clearable
          @input="handleSearch"
        />
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="filteredUsers"
      :loading="loading"
      :items-per-page="10"
      class="elevation-1"
    >
      <template v-slot:item.username="{ item }">
        <v-btn
          variant="text"
          color="primary"
          :to="`/users/${item.id}`"
          class="text-none"
        >
          {{ item.username }}
        </v-btn>
      </template>

      <template v-slot:item.active_loans="{ item }">
        <v-chip
          :color="item.profile.active_loans?.length > 0 ? 'warning' : 'success'"
          size="small"
        >
          {{ item.profile.active_loans?.length || 0 }}
        </v-chip>
      </template>

      <template v-slot:item.actions="{ item }">
        <div class="d-flex gap-2">
          <v-btn
            size="small"
            color="primary"
            variant="outlined"
            :to="`/users/${item.id}`"
            :title="`View details for ${item.username}`"
          >
            <v-icon start>mdi-account-details</v-icon>
            Details
          </v-btn>
        </div>
      </template>

      <template v-slot:no-data>
        <v-alert type="info" class="ma-2">
          No users found matching your criteria
        </v-alert>
      </template>

      <template v-slot:loading>
        <v-progress-linear indeterminate color="primary" />
      </template>
    </v-data-table>

    <v-snackbar
      v-model="showError"
      color="error"
      timeout="3000"
    >
      {{ errorMessage }}
      <template v-slot:actions>
        <v-btn
          color="white"
          variant="text"
          @click="hideError"
        >
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-container>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useDebounceFn } from '@vueuse/core'
import type { User } from '~/types'

const { user: currentUser } = useAuth()
const { fetchApi } = useApi()

const users = ref<User[]>([])
const loading = ref(false)
const searchQuery = ref('')
const showOnlyActive = ref(false)
const showError = ref(false)
const errorMessage = ref('')

const headers = [
  { title: 'Username', key: 'username', sortable: true },
  { title: 'Active Loans', key: 'active_loans', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

const filteredUsers = computed(() => {
  let filtered = [...users.value]
  
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(user => 
      user.username.toLowerCase().includes(query) ||
      user.profile.full_name.toLowerCase().includes(query)
    )
  }
  
  if (showOnlyActive.value) {
    filtered = filtered.filter(user => 
      (user.profile.active_loans?.length || 0) > 0
    )
  }
  
  return filtered
})

async function fetchUsers() {
  loading.value = true
  try {
    const response = await fetchApi<User[]>('/api/users/')
    users.value = response
  } catch (err: any) {
    showErrorMessage(err.message || 'Failed to fetch users')
  } finally {
    loading.value = false
  }
}

const handleSearch = useDebounceFn(() => {
  // Filtering happens automatically through computed property
}, 300)

function showErrorMessage(message: string) {
  errorMessage.value = message
  showError.value = true
}

function hideError() {
  showError.value = false
}

onMounted(() => {
  fetchUsers()
})
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}
</style>
