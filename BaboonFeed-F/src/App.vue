<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import ChatList from '@/components/Chat/ChatList.vue'

const route = useRoute();
const isAuthPage = computed(() => route.name === 'login' || route.name === 'register');

// Estado de la Navbar (contraída por defecto)
const isNavbarExpanded = ref(false);
</script>

<template>
    <div class="layout">
        <!-- Header de navegación -->
        <header v-if="!isAuthPage" aria-label="Navegación principal">
            <Navbar @update:expanded="isNavbarExpanded = $event" />
        </header>

        <!-- Contenido principal -->
        <main :class="['content', { 'content-expanded': isNavbarExpanded }]" id="main-content">
            <router-view />
        </main>

        <!-- Chat, fuera del contenido principal -->
        <aside v-if="!isAuthPage" class="d-none d-lg-block" aria-label="Lista de chats recientes" style="z-index: 2;">
            <ChatList />
        </aside>
    </div>
</template>

<style scoped>
/* Layout principal */
.layout {
    display: flex;
    flex-direction: row;
    width: 100%;
    height: 100vh;
}

/* Contenido cuando la navbar está contraída */
.content {
  width: 100%;
  flex-grow: 1;
  margin-left: 100px; /* Espacio de la navbar contraída */
  margin-right: 250px;
  transition: margin-left 0.3s ease-in-out, width 0.3s ease-in-out;
}

/* Contenido desplazado cuando la navbar está expandida */
.content-expanded {
  margin-left: 250px;
}

/* Ocultar scrollbar en navegadores WebKit */
.content::-webkit-scrollbar {
    display: none;
}

/* Ocultar scrollbar en Firefox */
.content {
    scrollbar-width: none;
}

/* Ocultar scrollbar en Edge */
.content {
    -ms-overflow-style: none;
}
</style>
