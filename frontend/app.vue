<template>
  <NuxtLayout>
    <NuxtPage />
  </NuxtLayout>
</template>

<script setup>
const { checkAuth } = useAuth()

onMounted(() => {
  checkAuth()
})
</script>
