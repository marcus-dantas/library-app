<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn
          variant="outlined"
          prepend-icon="mdi-arrow-left"
          @click="router.back()"
        >
          Back to Users
        </v-btn>
      </v-col>
    </v-row>

    <template v-if="currentUserDetails">
      <v-row class="mb-4">
        <v-col cols="12">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center pa-4">
              <div>
                <h2 class="text-h4">{{ currentUserDetails.username }}</h2>
                <p class="text-subtitle-1 mt-2">{{ currentUserDetails.profile.full_name }}</p>
              </div>
              <v-chip
                :color="canUserBorrow ? 'success' : 'error'"
                class="ml-4"
              >
                {{ canUserBorrow ? 'Can Borrow' : 'Max Loans Reached' }}
              </v-chip>
            </v-card-title>

            <v-card-text>
              <v-list>
                <v-list-item>
                  <template v-slot:prepend>
                    <v-icon color="primary">mdi-email</v-icon>
                  </template>
                  <v-list-item-title>Email</v-list-item-title>
                  <v-list-item-subtitle>{{ currentUserDetails.email }}</v-list-item-subtitle>
                </v-list-item>

              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row class="mb-4">
        <v-col cols="12">
          <v-card>
            <v-card-title class="d-flex justify-space-between align-center">
              <span>Active Loans</span>
              <v-chip>{{ activeLoans.length }} Books</v-chip>
            </v-card-title>

            <v-card-text>
              <v-table v-if="activeLoans.length">
                <thead>
                  <tr>
                    <th scope="col">Book Title</th>
                    <th scope="col">Loan Date</th>
                    <th scope="col">Due Date</th>
                    <th scope="col">Status</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="loan in activeLoans" :key="loan.id">
                    <td>{{ loan.book.title }}</td>
                    <td>{{ loan.loan_date }}</td>
                    <td>
                      <v-chip
                        :color="getDueDateColor(loan.days_remaining)"
                        size="small"
                      >
                        {{ loan.due_date }}
                      </v-chip>
                    </td>
                    <td>
                      <v-chip
                        :color="getLoanStatusColor(loan.status)"
                        size="small"
                      >
                        {{ loan.status }}
                      </v-chip>
                    </td>
                    <td v-if="isAdmin">
                      <v-btn
                        size="small"
                        color="primary"
                        @click="handleReturnBook(loan.id)"
                        :loading="returningBook === loan.id"
                      >
                        Return Book
                      </v-btn>
                    </td>
                  </tr>
                </tbody>
              </v-table>
              <v-alert
                v-else
                type="info"
                variant="tonal"
                class="mt-2"
              >
                No active loans
              </v-alert>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <v-row v-else-if="loading">
      <v-col cols="12">
        <v-skeleton-loader type="article" />
      </v-col>
    </v-row>

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
import type { User } from '~/types'

const route = useRoute()
const router = useRouter()
const { user: authenticatedUser } = useAuth()
const { fetchApi } = useApi()

const loading = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const returningBook = ref<number | null>(null)
const currentUserDetails = ref<User | null>(null)

const isAdmin = computed(() => authenticatedUser.value?.is_admin || false)

const activeLoans = computed(() => {
  return currentUserDetails.value?.profile.active_loans || []
})

const canUserBorrow = computed(() => {
  const maxAllowedLoans = 5
  return (activeLoans.value.length || 0) < maxAllowedLoans
})

function getDueDateColor(daysRemaining: number): string {
  if (daysRemaining < 0) return 'error'
  if (daysRemaining < 3) return 'warning'
  return 'success'
}

function getLoanStatusColor(status: string): string {
  switch (status) {
    case 'OVERDUE': return 'error'
    case 'ACTIVE': return 'success'
    default: return 'default'
  }
}

async function fetchUserDetails() {
  loading.value = true
  try {
    const response = await fetchApi<User>(`/api/users/${route.params.id}/`)
    currentUserDetails.value = response
  } catch (error: any) {
    showErrorMessage(error.message || 'Failed to fetch user details')
  } finally {
    loading.value = false
  }
}

async function handleReturnBook(loanId: number) {
  if (!isAdmin.value) return
  
  returningBook.value = loanId
  try {
    await fetchApi(`/api/loans/${loanId}/return_book/`, {
      method: 'POST'
    })
    await fetchUserDetails()
  } catch (error: any) {
    showErrorMessage(error.message || 'Failed to return book')
  } finally {
    returningBook.value = null
  }
}

function showErrorMessage(message: string) {
  errorMessage.value = message
  showError.value = true
}

function hideError() {
  showError.value = false
}

onMounted(() => {
  fetchUserDetails()
})
</script>
