<template>
  <v-container>
    <v-row class="mb-4">
      <v-col cols="12" md="6">
        <v-text-field
          v-model="searchQuery"
          label="Search books"
          prepend-inner-icon="mdi-magnify"
          clearable
          @input="handleSearch"
        />
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-center">
        <v-switch
          v-model="showOnlyAvailable"
          label="Show only available books"
          @change="filterBooks"
        />
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="filteredBooks"
      :loading="loading"
      :items-per-page="10"
      class="elevation-1"
    >
      <template v-slot:item.title="{ item }">
        <v-tooltip :text="item.title" location="top">
          <template v-slot:activator="{ props }">
            <span v-bind="props" class="text-truncate d-inline-block" style="max-width: 200px">
              {{ item.title }}
            </span>
          </template>
        </v-tooltip>
      </template>

      <template v-slot:item.available_copies="{ item }">
        <v-chip
          :color="item.available_copies > 0 ? 'success' : 'error'"
          size="small"
        >
          {{ item.available_copies }} / {{ item.total_copies }}
        </v-chip>
      </template>

      <template v-slot:item.actions="{ item }">
        <div class="d-flex gap-2">
          <v-btn
            size="small"
            color="primary"
            variant="outlined"
            @click="viewBookDetails(item)"
            :title="'View details for ' + item.title"
          >
            <v-icon start>mdi-book-open</v-icon>
            Details
          </v-btn>
        </div>
      </template>

      <template v-slot:no-data>
        <v-alert type="info" class="ma-2">
          No books available matching your criteria
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
import { useDebounceFn } from '@vueuse/core'
import type { Book } from '~/types'

const { user } = useAuth()
const { 
  books,
  loading,
  error: booksError,
  fetchBooks,
  filterBooks
} = useBooks()

const searchQuery = ref('')
const showOnlyAvailable = ref(false)
const showError = ref(false)
const errorMessage = ref('')

const headers = [
  { title: 'Title', key: 'title', sortable: true },
  { title: 'Author', key: 'author', sortable: true },
  { title: 'ISBN', key: 'isbn', sortable: false },
  { title: 'Availability', key: 'available_copies', sortable: true },
  { title: 'Actions', key: 'actions', sortable: false }
]

const filteredBooks = computed(() => 
  filterBooks(books.value, searchQuery.value, showOnlyAvailable.value)
)

const handleSearch = useDebounceFn(() => {
  // The filtering happens automatically through the computed property
}, 300)

function viewBookDetails(book: Book) {
  navigateTo(`/books/${book.id}/`)
}

function showErrorMessage(message: string) {
  errorMessage.value = message
  showError.value = true
}

function hideError() {
  showError.value = false
}

watch(() => booksError.value, (newError) => {
  if (newError) {
    showErrorMessage(newError)
  }
})

onMounted(() => {
  fetchBooks()
})
</script>

<style scoped>
.gap-2 {
  gap: 8px;
}

.text-truncate {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
</style>
