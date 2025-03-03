<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import OpenChats from "@/components/Chat/OpenChats.vue";

const route = useRoute()
const isAuthPage = computed(() => {
    return route.name === 'login' || route.name === 'register'
})
</script>

<template>
    <div class="layout">
        <div v-if="!isAuthPage" class="col-2 col-lg-2 bg-dark-alt static">
            <Navbar />
        </div>
        <div class="content">
            <router-view />
        </div>
        <div class="col-2 col-lg-2 bg-dark-alt static">
            <OpenChats />
        </div>
    </div>
</template>

<style scoped>
.layout {
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 100vh;
}

.content {
    flex: 1;
    overflow: auto; /* Solo hace scroll si es necesario */
}

/* Ocultar scrollbar en navegadores WebKit (Chrome, Safari, Edge) */
.content::-webkit-scrollbar {
    display: none;
}

/* Ocultar scrollbar en Firefox */
.content {
    scrollbar-width: none;
}

/* Ocultar scrollbar en Edge y otros */
.content {
    -ms-overflow-style: none;
}
</style>
