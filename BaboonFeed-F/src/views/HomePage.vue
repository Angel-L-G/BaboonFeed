<template>
    <div class="container-fluid text-center" role="region" aria-label="Página de inicio">
        <h1 class="display-4 m-3 text-primary-alt" tabindex="-1" id="home-heading">
            Baboon Feed
        </h1>

        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-9 me-2 content d-flex flex-column justify-content-center align-items-center"  role="list" aria-labelledby="home-heading">
                <PostView v-for="post in posts" :key="post.id" :post="post" role="listitem" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { reactive, onMounted } from 'vue';
    import type { Post } from '../types/Post';
    import { API_URL } from '@/globals';
    import PostView from '@/components/post/PostView.vue';
    import axios from 'axios'
    import type { Chat } from '@/types/Chat.ts'
    import { useAuthStore } from '@/stores/auth.ts'

    const authStore = useAuthStore();
    const posts = reactive<Post[]>([]);
    const chats = reactive<Chat[]>([]);

    onMounted( async () => {
        await axios.get(
            `${API_URL}posts/?limit=10&offset=0`
        ).then(async (response) => {
            const data = await response.data;
            data.results.forEach((post: Post) => {
                posts.push(post);
            });
        }).catch((error) => {
            console.log(error);
        });
        if (authStore.user) {
            await axios.get(
                `${API_URL}chats/?limit=10&offset=0`,
                {
                    headers: { 'Authorization': `Bearer ${authStore.token}` }
                }
            ).then(async (response) => {
                const data = await response.data;
                data.results.forEach((chat: Chat) => {
                    chats.push(chat);
                });
            }).catch((error) => {
                console.log(error);
            });
        }
    })
</script>

<style scoped>
.content {
    flex: 1;
    overflow: auto;
}
</style>
