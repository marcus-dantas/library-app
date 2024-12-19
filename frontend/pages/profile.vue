<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card>
          <v-card-title class="text-h5">Profile</v-card-title>
          <v-card-text>
            <div v-if="user">
              <v-list>
                <v-list-item>
                  <v-list-item-title>Username</v-list-item-title>
                  <v-list-item-subtitle>{{ user.username }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item v-if="user.id">
                  <v-list-item-title>User ID</v-list-item-title>
                  <v-list-item-subtitle>{{ user.id }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>Role</v-list-item-title>
                  <v-list-item-subtitle>
                    {{ user.is_admin ? 'Admin' : 'User' }}
                  </v-list-item-subtitle>
                </v-list-item>
                <v-list-item v-if="user.email">
                  <v-list-item-title>Email</v-list-item-title>
                  <v-list-item-subtitle>{{ user.email }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
            <div v-else>
              <v-alert
                type="warning"
                variant="tonal"
              >
                Please login to view your profile
              </v-alert>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
const { user, checkAuth } = useAuth()

onMounted(async () => {
  try {
    await checkAuth()
  } catch (error) {
    console.error('Error checking authentication:', error)
  }
})
</script>
