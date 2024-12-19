<template>
  <v-app>
    <v-app-bar 
      elevation="1"
      color="white"
    >
      <v-container class="d-flex align-center px-2">
        <v-toolbar-title class="text-h5 font-weight-bold primary--text">
          Library App
        </v-toolbar-title>

        <template v-if="!isMobile">
          <v-spacer />
          <nav>
            <v-btn
              to="/"
              variant="text"
              class="mx-2"
              :active="route.path === '/'"
            >
              Home
            </v-btn>
            
            <v-btn
              v-if="isAuthenticated"
              to="/books"
              variant="text"
              class="mx-2"
              :active="route.path === '/books'"
            >
              <v-icon start>mdi-book-open-page-variant</v-icon>
              Books
            </v-btn>

            <template v-if="isAuthenticated">
              <v-btn
                to="/profile"
                variant="text"
                class="mx-2"
                :active="route.path === '/profile'"
              >
                <v-icon start>mdi-account</v-icon>
                Profile
              </v-btn>
              <v-btn
                @click="handleLogout"
                variant="text"
                class="mx-2"
                color="error"
              >
                <v-icon start>mdi-logout</v-icon>
                Logout
              </v-btn>
            </template>

            <template v-else>
              <v-btn
                to="/login"
                variant="text"
                class="mx-2"
                color="primary"
              >
                <v-icon start>mdi-login</v-icon>
                Login
              </v-btn>
              <v-btn
                to="/register"
                variant="outlined"
                color="primary"
                class="mx-2"
              >
                <v-icon start>mdi-account-plus</v-icon>
                Register
              </v-btn>
            </template>
          </nav>
        </template>

        <template v-else>
          <v-spacer />
          <v-btn
            icon
            @click="isDrawerOpen = !isDrawerOpen"
          >
            <v-icon>mdi-menu</v-icon>
          </v-btn>
        </template>
      </v-container>
    </v-app-bar>

    <v-navigation-drawer
      v-model="isDrawerOpen"
      temporary
      location="right"
    >
      <v-list>
        <v-list-item
          to="/"
          :active="route.path === '/'"
          @click="isDrawerOpen = false"
        >
          <template v-slot:prepend>
            <v-icon>mdi-home</v-icon>
          </template>
          Home
        </v-list-item>

        <v-list-item
          to="/books"
          :active="route.path === '/books'"
          @click="isDrawerOpen = false"
        >
          <template v-slot:prepend>
            <v-icon>mdi-book-open-page-variant</v-icon>
          </template>
          Books
        </v-list-item>

        <template v-if="isAuthenticated">
          <v-list-item
            to="/profile"
            :active="route.path === '/profile'"
            @click="isDrawerOpen = false"
          >
            <template v-slot:prepend>
              <v-icon>mdi-account</v-icon>
            </template>
            Profile
          </v-list-item>

          <v-list-item
            @click="handleLogoutMobile"
            color="error"
          >
            <template v-slot:prepend>
              <v-icon>mdi-logout</v-icon>
            </template>
            Logout
          </v-list-item>
        </template>

        <template v-else>
          <v-list-item
            to="/login"
            @click="isDrawerOpen = false"
            color="primary"
          >
            <template v-slot:prepend>
              <v-icon>mdi-login</v-icon>
            </template>
            Login
          </v-list-item>

          <v-list-item
            to="/register"
            @click="isDrawerOpen = false"
            color="primary"
          >
            <template v-slot:prepend>
              <v-icon>mdi-account-plus</v-icon>
            </template>
            Register
          </v-list-item>
        </template>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container class="py-4">
        <NuxtPage />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
const { isAuthenticated, checkAuth, logout } = useAuth()
const route = useRoute()

const isMobile = ref(false)
const isDrawerOpen = ref(false)

onMounted(async () => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
  try {
    await checkAuth()
  } catch (error) {
    console.error('Error checking authentication:', error)
  }
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
})

function checkMobile() {
  isMobile.value = window.innerWidth < 960
}

async function handleLogout() {
  await logout()
}

async function handleLogoutMobile() {
  isDrawerOpen.value = false
  await handleLogout()
}
</script>

<style scoped>
.v-btn {
  text-transform: none;
}
</style>
