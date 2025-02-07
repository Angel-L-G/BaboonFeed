<script setup lang="ts">
import Footer from '@/components/Footer.vue'
import Navbar from '@/components/Navbar.vue'
</script>

<template>
    <Navbar />
    <main>
        <router-view />
    </main>
    <Footer />
</template>
