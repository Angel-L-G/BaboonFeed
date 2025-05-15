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

    const posts = reactive<Post[]>([]);

    onMounted( async () => {
        await fetch(`${API_URL}posts/`, {
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
.content {
    flex: 1;
    overflow: auto;
}
</style>
