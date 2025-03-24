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
                <router-link :to="item.route" class="nav-link text-light d-flex py-3 px-3">
                    <font-awesome-icon :icon="item.icon" class="icon-fixed-large pt-1" />
                    <span v-show="isExpanded" class="ms-3 nav-text">{{ item.name }}</span>
                </router-link>
            </li>

            <li class="nav-item">
                <button class="nav-link text-warning d-flex py-3 px-3 border-0 bg-transparent new-post-btn"
                        data-bs-toggle="modal" data-bs-target="#CreatePostModal">
                    <font-awesome-icon :icon="['fas', 'circle-plus']" class="icon-fixed-large pt-1" />
                    <span v-show="isExpanded" class="ms-3 nav-text ellipsis-text text">New Post</span>
                </button>
            </li>
        </ul>
    </div>

    <div class="modal fade" id="CreatePostModal" tabindex="-1" aria-labelledby="CreatePostModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content bg-secondary text-light">
                <CreatePost></CreatePost>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, defineEmits } from 'vue';
import CreatePost from '@/components/post/CreatePost.vue';

const isExpanded = ref(false);
const emit = defineEmits(["update:expanded"]); // Emitir cambios al padre

const toggleSidebar = () => {
    isExpanded.value = !isExpanded.value;
    emit("update:expanded", isExpanded.value); // Notificar al padre
};

const menuItems = [
    { name: 'Chat', icon: ['fas', 'comment'], route: { name: 'chat' } },
    { name: 'Profile', icon: ['fas', 'id-card'], route: { name: 'profile', params: { username: '1' } } }
];
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
}

.sidebar.expanded {
    width: 250px;
}

span {
    white-space: nowrap;
    padding: 0;
    margin: 0;
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
    padding: 0 !IMPORTANT;
    height: 75px;
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

.nav-text {
    font-size: 1.2rem;
}
</style>
