<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12">
        <v-btn
          variant="outlined"
          prepend-icon="mdi-arrow-left"
          @click="router.back()"
        >
          Back to Books
        </v-btn>
      </v-col>
    </v-row>

    <template v-if="currentBook">
      <v-row>
        <v-col cols="12">
          <v-card class="elevation-1">
            <v-card-title class="d-flex justify-space-between align-center pa-4">
              <div>
                <h2 class="text-h4">{{ currentBook.title }}</h2>
                <p class="text-subtitle-1 mt-2">by {{ currentBook.author }}</p>
              </div>
              <v-chip
                :color="currentBook.available_copies > 0 ? 'success' : 'error'"
                class="ml-4"
              >
                {{ currentBook.available_copies }} / {{ currentBook.total_copies }} Available
              </v-chip>
            </v-card-title>

            <v-divider />

            <v-card-text class="pa-4">
              <v-row>
                <v-col cols="12" md="8">
                  <v-list>
                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-book-open-variant</v-icon>
                      </template>
                      <v-list-item-title>ISBN</v-list-item-title>
                      <v-list-item-subtitle>{{ currentBook.isbn }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-calendar</v-icon>
                      </template>
                      <v-list-item-title>Publication Year</v-list-item-title>
                      <v-list-item-subtitle>{{ currentBook.publication_year }}</v-list-item-subtitle>
                    </v-list-item>

                    <v-list-item>
                      <template v-slot:prepend>
                        <v-icon color="primary">mdi-format-list-text</v-icon>
                      </template>
                      <v-list-item-title>Description</v-list-item-title>
                      <v-list-item-subtitle class="mt-2">{{ currentBook.description }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-col>

                <v-col cols="12" md="4">
                  <v-card variant="outlined">
                    <v-card-title class="text-h6">
                      <v-icon start color="primary">mdi-account-multiple</v-icon>
                      Current Loans
                    </v-card-title>
                    <v-divider />
                    <v-list v-if="currentBook.current_loans?.length">
                      <v-list-item
                        v-for="loan in currentBook.current_loans"
                        :key="loan.id"
                        :title="loan.user_name"
                        :subtitle="`Due: ${loan.due_date}`"
                      >
                        <template v-slot:prepend>
                          <v-icon>mdi-account</v-icon>
                        </template>
                      </v-list-item>
                    </v-list>
                    <v-card-text v-else>
                      <v-alert type="info" variant="tonal">
                        No current loans
                      </v-alert>
                    </v-card-text>
                  </v-card>
                </v-col>
              </v-row>
            </v-card-text>

            <v-card-actions class="pa-4">
              <template v-if="isAdmin">
                <v-btn
                  color="primary"
                  prepend-icon="mdi-account-plus"
                  @click="showAssignDialog = true"
                  :disabled="!currentBook.available_copies"
                >
                  Assign to User
                </v-btn>
              </template>
              <template v-else>
                <v-btn
                  color="primary"
                  :disabled="!currentBook.available_copies || isLoaning"
                  @click="handleLoanBook"
                  :loading="isLoaning"
                >
                  Borrow Book
                </v-btn>
              </template>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </template>

    <template v-else-if="loading">
      <v-skeleton-loader type="article" />
    </template>

    <v-dialog v-model="showAssignDialog" max-width="500px">
      <v-card>
        <v-card-title>Assign Book to User</v-card-title>
        <v-card-text>
          <v-select
            v-model="selectedUserId"
            :items="availableUsers"
            item-title="username"
            item-value="id"
            label="Select User"
            :loading="loadingUsers"
            :rules="[v => !!v || 'User is required']"
          />
        </v-card-text>
        <v-card-actions>
          <v-spacer />
          <v-btn
            color="primary"
            @click="handleAssignBook"
            :loading="isAssigning"
            :disabled="!selectedUserId || isAssigning"
          >
            Assign Book
          </v-btn>
          <v-btn
            color="grey"
            @click="closeAssignDialog"
          >
            Cancel
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

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
import type { Book, User } from '~/types'

const route = useRoute()
const router = useRouter()
const { user: authenticatedUser } = useAuth()
const { fetchApi } = useApi()

const loading = ref(false)
const loadingUsers = ref(false)
const isLoaning = ref(false)
const isAssigning = ref(false)
const showError = ref(false)
const errorMessage = ref('')
const showAssignDialog = ref(false)
const selectedUserId = ref<number | null>(null)
const currentBook = ref<Book | null>(null)
const availableUsers = ref<User[]>([])

const isAdmin = computed(() => authenticatedUser.value?.is_admin || false)

async function fetchBookDetails() {
  loading.value = true
  try {
    const response = await fetchApi<Book>(`/api/books/${route.params.id}/`)
    currentBook.value = response
  } catch (error: any) {
    showErrorMessage(error.message || 'Failed to fetch book details')
  } finally {
    loading.value = false
  }
}

async function fetchAvailableUsers() {
  loadingUsers.value = true
  try {
    const response = await fetchApi<User[]>('/api/users/')
    availableUsers.value = response.filter(user => 
      !currentBook.value?.current_loans?.some(
        loan => loan.user_name === user.username
      )
    )
  } catch (error: any) {
    showErrorMessage(error.message || 'Failed to fetch users')
  } finally {
    loadingUsers.value = false
  }
}

async function handleLoanBook() {
  if (!currentBook.value?.available_copies || isLoaning.value) return
  
  isLoaning.value = true
  try {
    await fetchApi('/api/loans/create/', {
      method: 'POST',
      body: { book_id: currentBook.value.id }
    })
    await fetchBookDetails()
  } catch (error: any) {
    showErrorMessage(error.message || 'Failed to loan book')
  } finally {
    isLoaning.value = false
  }
}

async function handleAssignBook() {
  if (!selectedUserId.value || !currentBook.value || isAssigning.value) return
  
  isAssigning.value = true
  try {
    await fetchApi('/api/loans/create/', {
      method: 'POST',
      body: {
        book_id: currentBook.value.id,
        user_id: selectedUserId.value
      }
    })
    await fetchBookDetails()
    closeAssignDialog()
  } catch (error: any) {
    showErrorMessage(error.message || 'Failed to assign book')
  } finally {
    isAssigning.value = false
  }
}

function closeAssignDialog() {
  showAssignDialog.value = false
  selectedUserId.value = null
}

function showErrorMessage(message: string) {
  errorMessage.value = message
  showError.value = true
}

function hideError() {
  showError.value = false
}

watch(showAssignDialog, async (newValue) => {
  if (newValue && isAdmin.value) {
    await fetchAvailableUsers()
  }
})

onMounted(() => {
  fetchBookDetails()
})
</script>
