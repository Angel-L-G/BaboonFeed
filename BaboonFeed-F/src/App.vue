<script setup lang="ts">
import { RouterView } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
</script>

<template class="h-100">
  <div class="bg-secondary">
    <Navbar />

    <router-view />

    <Footer />
  </div>
</template>
