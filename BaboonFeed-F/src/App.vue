<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import ChatList from '@/components/ChatList.vue'

const route = useRoute();
const isAuthPage = computed(() => route.name === 'login' || route.name === 'register');

// Estado de la Navbar (contraída por defecto)
const isNavbarExpanded = ref(false);
</script>

<template>
    <div class="layout">
        <!-- Navbar solo si no es una página de autenticación -->
        <Navbar v-if="!isAuthPage" @update:expanded="isNavbarExpanded = $event" />

        <!-- Contenido ajustando su margen según la navbar -->
        <div :class="['content', { 'content-expanded': isNavbarExpanded }]">
            <router-view />
        </div>

        <ChatList v-if="!isAuthPage"/>
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
    overflow: auto;
    flex-grow: 1;
    margin-left: 100px; /* Espacio de la navbar contraída */
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

/* Panel derecho fijo */
.right-panel {
    width: 300px;
    height: 100vh;
    overflow-y: auto;
    position: fixed;
    right: 0;
    top: 0;
    padding-top: 1rem;
}

/* Ajuste del contenido para no solaparse con panel derecho */
.content {
    margin-right: 300px; /* Deja espacio al contenido para el panel */
}

/* Si navbar expandida */
.content-expanded {
    margin-left: 250px;
    margin-right: 300px;
}
</style>
