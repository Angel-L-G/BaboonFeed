<template>
    <div :class="['sidebar', 'bg-dark', { 'expanded': isExpanded }]" role="navigation" aria-label="Menú lateral">
        <!-- Botón de colapsar -->
        <button class="btn btn-outline-primary toggle-btn" @click="toggleSidebar"
            :aria-expanded="isExpanded" aria-controls="sidebarMenu" aria-label="Alternar menú lateral">
            <font-awesome-icon :icon="['fas', 'bars']" />
        </button>

        <!-- Marca / logo -->
        <div class="ms-3 title-container">
            <p class="title-text my-4">
                <router-link :to="{ name: 'home' }" class="navbar-brand text-info-light py-3"
                    aria-label="Ir a la página de inicio">
                    <font-awesome-icon :icon="['fas', 'dove']" class="icon-fixed-large"/>
                    <span v-show="isExpanded" class="ms-3">BaboonFeed</span>
                </router-link>
            </p>
        </div>

        <!-- Menú -->
        <ul id="sidebarMenu" class="nav flex-column" role="menu" v-if="isAuthenticated">
            <li v-for="item in menuItems" :key="item.name" class="nav-item" role="none">
                <router-link :to="item.route" class="nav-link text-purple-light d-flex py-3 px-3"
                    role="menuitem" :aria-label="`Ir a ${item.name}`">
                    <font-awesome-icon :icon="item.icon" class="icon-fixed-large pt-1"/>
                    <span :class="['nav-text', 'ms-3', { 'visible': isExpanded }]">{{ item.name }}</span>
                </router-link>
            </li>

            <!-- Botón crear post -->
            <li class="nav-item" role="none">
                <button class="nav-link text-purple-light d-flex py-3 px-3 border-0 bg-transparent new-post-btn"
                    data-bs-toggle="modal" data-bs-target="#CreatePostModal" role="menuitem"
                    aria-label="Crear nueva publicación">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="icon-fixed-large pt-1"/>
                    <span :class="['nav-text', 'ms-3', { 'visible': isExpanded }]">New Post</span>
                </button>
            </li>
        </ul>

        <div class="nav-item d-flex h-100 justify-content-end align-items-end">
            <button class="nav-link text-danger d-flex py-3 px-3 border-0 bg-transparent"
                    @click="logout" v-if="isAuthenticated">
                <font-awesome-icon :icon="['fas', 'arrow-right-from-bracket']" class="icon-fixed-large pt-1" />
                <span :class="['nav-text', 'ms-3', { 'visible': isExpanded }]">Logout</span>
            </button>
            <router-link class="nav-link text-success d-flex py-3 px-3 border-0 bg-transparent"
                         v-if="!isAuthenticated" :to="{ name: 'login' }">
                <font-awesome-icon :icon="['fas', 'arrow-right-to-bracket']" class="icon-fixed-large pt-1" />
                <span :class="['nav-text', 'ms-3', { 'visible': isExpanded }]">Login/Register</span>
            </router-link>
        </div>
    </div>

    <!-- Modal para crear post -->
    <div class="modal fade" id="CreatePostModal" tabindex="-1"
         aria-labelledby="CreatePostModalLabel" aria-hidden="true" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content bg-secondary text-light">
                <header class="modal-header" data-bs-theme="dark">
                    <h2 id="CreatePostModalLabel" class="modal-title text-center">Create Post</h2>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                            aria-label="Cerrar modal"/>
                </header>
                <div class="modal-body">
                    <CreatePost />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import CreatePost from '@/components/post/CreatePost.vue';
import { computed, ref } from 'vue'
import { useAuthStore } from '@/stores/auth.ts'

const isExpanded = ref(false);
const emit = defineEmits(["update:expanded"]);
const authStore = useAuthStore();

const toggleSidebar = () => {
    isExpanded.value = !isExpanded.value;
    emit("update:expanded", isExpanded.value);
};

const username = computed(() => authStore.user?.username);

const menuItems = [
    { name: 'Chat', icon: ['fas', 'comment'], route: { name: 'chatFilter' } },
    { name: 'Profile', icon: ['fas', 'id-card'], route: { name: 'profile', params: { username: username.value } } }
];

const isAuthenticated = computed(() => authStore.isAuthenticated);

const logout = () => {
    authStore.logout();
};
</script>

<style scoped>
.sidebar {
    top: 0;
    left: 0;
    bottom: 0;
    width: 80px;
    transition: width 0.3s ease-in-out;
    padding: 20px;
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    overflow: hidden;
    background-color: #fff; /* O el color de fondo de tu sidebar */
    z-index: 1030; /* Asegura que esté por encima */
}

/* Sidebar expandida */
.sidebar.expanded {
    width: 250px;
}

@media (min-width: 992px) {
    .sidebar {
        position: fixed;
        transform: none !important;
        width: 80px;
    }

    .sidebar.expanded {
        width: 250px;
    }
}

@media (max-width: 991px) {
    .sidebar {
        position: fixed;
        top: 0;
        left: 0;
        width: 250px;
        height: 100vh;
        transform: translateX(-100%);
        transition: transform 0.3s ease-in-out;
        background-color: #111; /* Asegura que tenga fondo oscuro */
        z-index: 1050; /* Que esté por encima del contenido */
        box-shadow: 2px 0 8px rgba(0, 0, 0, 0.3); /* opcional */
    }

    .sidebar.expanded {
        transform: translateX(0);
    }
}

/* ANIMACIÓN FLUIDA AL DESAPARECER */
.nav-text {
    opacity: 0;
    width: 0;
    overflow: hidden;
    white-space: nowrap;
    transition:
        opacity 0.3s ease-in-out 0.2s, /* ⏳ Agregamos un pequeño delay al ocultar */
        width 0.5s ease-in-out;
}

/* Cuando la sidebar está expandida */
.nav-text.visible {
    opacity: 1;
    width: auto;
    transition:
        opacity 0.3s ease-in-out,  /* ⚡ Sin delay al aparecer */
        width 0.3s ease-in-out;
}

.toggle-btn {
    width: 60px;
    height: 60px;
    display: flex;
    justify-content: center;
    align-items: center;
    border: none;
    background: transparent;
    color: white;
}

.title-container {
    display: flex;
    align-items: center;
    justify-content: start;
    text-align: start;
    width: 100%;
    height: 95px;
}

.title-text {
    font-size: 1.5rem;
    margin: 0;
    text-align: start;
}

.nav-item {
    width: 100%;
    padding: 0 !important;
    height: 75px;
    min-width: 250px;
}

.nav-link {
    display: flex;
    align-items: start;
    justify-content: flex-start;
    width: 100%;
    font-size: 1.2rem;
}

.icon-fixed-large {
    width: 30px;
    min-width: 30px;
    text-align: center;
}
</style>
