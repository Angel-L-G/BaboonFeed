<script setup lang="ts">
import { RouterLink, RouterView } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import Navbar from '@/components/Navbar.vue'
import Footer from '@/components/Footer.vue'
import UserProfile from '@/views/User/UserProfile.vue'
</script>

<template class="h-100">
  <div class="bg-secondary">
    <Navbar />

    <UserProfile />

    <Footer />
  </div>
</template>
