<template>
  <AdminLayout v-if="isAuthenticated">
    <router-view />
  </AdminLayout>
  <router-view v-else />
</template>

<script setup lang="ts">
import AdminLayout from './components/AdminLayout.vue'
import { useAuth } from './composables/useAuth'

const { isAuthenticated } = useAuth()
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
</style>