<template>
    <div :class="['sidebar', 'bg-dark', { 'expanded': isExpanded }]">
        <button class="btn btn-outline-primary toggle-btn" @click="toggleSidebar">
            <font-awesome-icon :icon="['fas', 'bars']" />
        </button>

        <div class="ms-3 title-container">
            <p class="text-cyan text-center title-text">
                <router-link :to="{ name: 'home' }" class="navbar-brand text-cyan">
                    <font-awesome-icon :icon="['fas', 'dove']" class="icon-fixed-large" />
                    <span v-show="isExpanded" class="ms-3">BaboonFeed</span>
                </router-link>
            </p>
        </div>

        <ul class="nav flex-column">
            <li v-for="item in menuItems" :key="item.name" class="nav-item">
                <router-link :to="item.route" class="nav-link text-light d-flex py-3 px-3" v-if="isAuthenticated">
                    <font-awesome-icon :icon="item.icon" class="icon-fixed-large pt-1" />
                    <span :class="['nav-text', { 'visible': isExpanded }]">{{ item.name }}</span>
                </router-link>
                <button class="nav-link text-light d-flex py-3 px-3"
                        data-bs-toggle="modal" data-bs-target="#CreatePostModal" v-else-if="!isAuthenticated">
                    <font-awesome-icon :icon="item.icon" class="icon-fixed-large pt-1" />
                    <span :class="['nav-text', { 'visible': isExpanded }]">{{ item.name }}</span>
                </button>
            </li>

            <li class="nav-item">
                <button class="nav-link text-warning d-flex py-3 px-3 border-0 bg-transparent new-post-btn"
                        data-bs-toggle="modal" data-bs-target="#CreatePostModal">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="icon-fixed-large pt-1" />
                    <span :class="['nav-text', { 'visible': isExpanded }]">New Post</span>
                </button>
            </li>
        </ul>

        <!-- Logout -->
        <div class="nav-item d-flex h-100 justify-content-end align-items-end">
            <button class="nav-link text-danger d-flex py-3 px-3 border-0 bg-transparent"
                    @click="logout" v-if="isAuthenticated">
                <font-awesome-icon :icon="['fas', 'arrow-right-from-bracket']" class="icon-fixed-large pt-1" />
                <span :class="['nav-text', { 'visible': isExpanded }]">Logout</span>
            </button>
            <router-link class="nav-link text-success d-flex py-3 px-3 border-0 bg-transparent"
                         v-else-if="!isAuthenticated" :to="{ name: 'login' }">
                <font-awesome-icon :icon="['fas', 'arrow-right-to-bracket']" class="icon-fixed-large pt-1" />
                <span :class="['nav-text', { 'visible': isExpanded }]">Login/Register</span>
            </router-link>
        </div>
    </div>

    <div class="modal fade" id="CreatePostModal" tabindex="-1" aria-labelledby="CreatePostModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content bg-secondary text-light">
                <CreatePost v-if="isAuthenticated"/>
                <NeedToLogin v-else-if="!isAuthenticated" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import CreatePost from '@/components/post/CreatePost.vue';
import { ref, defineEmits, computed } from 'vue'
import { useAuthStore } from '@/stores/auth.ts'
import NeedToLogin from '@/components/NeedToLogin.vue'

const isExpanded = ref(false);
const emit = defineEmits(["update:expanded"]);
const authStore = useAuthStore();

const toggleSidebar = () => {
    isExpanded.value = !isExpanded.value;
    emit("update:expanded", isExpanded.value);
};

const isAuthenticated = computed(() => authStore.isAuthenticated);

const menuItems = [
    { name: 'Chat', icon: ['fas', 'comment'], route: { name: 'chat' } },
    //{ name: 'Group', icon: ['fas', 'people-group'], route: { name: 'group' } },
    { name: 'Profile', icon: ['fas', 'id-card'], route: { name: 'profile', params: { username: '1' } } },
];

const logout = () => {
    authStore.logout();
};
</script>

<style scoped>
.sidebar {
    position: fixed;
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
}

.sidebar.expanded {
    width: 250px;
}

/* 🎯 ANIMACIÓN FLUIDA AL DESAPARECER */
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
