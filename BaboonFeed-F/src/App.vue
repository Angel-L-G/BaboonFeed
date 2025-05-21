<script setup lang="ts">
import { computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from '@/components/Navbar.vue'
import ChatList from '@/components/Chat/ChatList.vue'
import { useAuthStore } from '@/stores/auth.ts'
import { useChatStore } from '@/stores/chatStore.ts'
import { useLayoutStore } from '@/stores/layoutStore.ts'

const route = useRoute()
const isAuthPage = computed(() => route.name === 'login' || route.name === 'register')
const auth = useAuthStore()
const layout = useLayoutStore();
const isNavbarExpanded = computed(() => layout.isNavbarExpanded);
const chat = useChatStore()

onMounted( async() => {
    if (auth.isAuthenticated && !isAuthPage.value) {
        await chat.getUserChats()
        await chat.connectToAllChats()
    }
})

onUnmounted( async () => {
    await chat.disconnectAllChats();
})
</script>

<template>
    <div class="layout">
        <!-- Header de navegación -->
        <header v-if="!isAuthPage" aria-label="Navegación principal">
            <Navbar />
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
    transition: margin-left 0.3s ease-in-out, width 0.3s ease-in-out;
}

/* Aplicar márgenes solo en pantallas grandes (≥ 992px) */
@media (min-width: 992px) {
    .content {
        margin-left: 100px;
        margin-right: 250px;
    }

    .content-expanded {
        margin-left: 250px;
    }
}

@media (max-width: 991px) {
    .content {
        margin: 0 !important;
    }

    .content-expanded {
        margin: 0 !important;
    }
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
