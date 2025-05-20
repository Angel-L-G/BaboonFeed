<template>
    <div
        class="container-fluid text-center overflow-hidden"
        role="region"
        aria-label="Página de inicio"
    >
        <div class="bg-secondary w-75 text-center position-fixed margin-right" style="z-index: 1;">
            <h1 class="display-4 m-3 text-primary-alt fw-bold" id="home-heading">Baboon Feed</h1>
        </div>

        <div class="row justify-content-center scroll-content">
            <div
                class="col-md-12 col-lg-9 me-2 content d-flex w-100 flex-column justify-content-center align-items-center overflow-hidden"
                role="list"
                aria-labelledby="home-heading"
            >
                <PostView v-for="post in posts" :key="post.id" :post="post" role="listitem" />
                <div ref="bottomSentinel" class="sentinel" />
            </div>
        </div>
    </div>
    <!-- Spinner de carga -->
    <div v-if="loading" class="spinner mt-3" role="status" aria-live="polite" aria-busy="true">
        <span class="visually-hidden">Cargando más publicaciones...</span>
    </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import type { Post } from '../types/Post'
import { API_URL } from '@/globals'
import PostView from '@/components/post/PostView.vue'
import axios from 'axios'
import type { Chat } from '@/types/Chat.ts'
import { useAuthStore } from '@/stores/auth.ts'

const authStore = useAuthStore();
const posts = reactive<Post[]>([]);
const chats = reactive<Chat[]>([]);
const bottomSentinel = ref<HTMLElement | null>(null);

const nextUrl = ref<string | null>(`${API_URL}posts/?limit=10`);
let loading = false;

const loadPosts = async () => {
    if (!nextUrl.value || loading) return;
    loading = true;

    try {
        const response = await axios.get(nextUrl.value);
        const data = response.data;
        data.results.forEach((post: Post) => posts.push(post));
        nextUrl.value = data.next; // actualiza con el siguiente enlace o null
    } catch (error) {
        console.error(error);
    } finally {
        loading = false;
    }
};

onMounted(async () => {
    await loadPosts();

    if (authStore.user) {
        try {
            const response = await axios.get(`${API_URL}chats/?limit=10&offset=0`, {
                headers: { Authorization: `Bearer ${authStore.token}` },
            });
            response.data.results.forEach((chat: Chat) => chats.push(chat));
        } catch (error) {
            console.error(error);
        }
    }

    // Scroll infinito con IntersectionObserver
    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry) => {
            if (entry.isIntersecting) {
                loadPosts();
            }
        });
    });

    if (bottomSentinel.value) {
        observer.observe(bottomSentinel.value);
    }
});
</script>

<style scoped>
.scroll-content {
    overflow-x: hidden;
    margin-top: 100px;
}

.margin-right {
    width: 100vh;
}

.spinner {
    border: 4px solid #f3f3f3; /* fondo claro */
    border-top: 4px solid #3498db; /* azul de carga */
    border-radius: 50%;
    width: 36px;
    height: 36px;
    animation: spin 1s linear infinite;
    margin: 1rem auto;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}
</style>
