<template>
    <div class="container-fluid text-center overflow-hidden" role="region" aria-label="Página de inicio">
        <div class="bg-secondary w-75 text-center position-fixed margin-right">
            <h1 class="display-4 m-3 text-primary-alt fw-bold" id="home-heading">
                Baboon Feed
            </h1>
        </div>

        <div class="row justify-content-center scroll-content">
            <div class="col-md-12 col-lg-9 me-2 content d-flex w-100 flex-column justify-content-center align-items-center overflow-hidden"  role="list" aria-labelledby="home-heading">
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

    const posts = reactive<Post[]>([]);

    onMounted( async () => {
        await fetch(`${API_URL}api/posts/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(async (response) => {
            const data = await response.json();
            posts.push(...data);
            console.log(posts);

        }).catch((error) => {
            console.log(error);
        })
    })
</script>

<style scoped>
.scroll-content {
    overflow-x: hidden;
    margin-top: 100px;
}

.margin-right {
    width: 100vh;
}
</style>
