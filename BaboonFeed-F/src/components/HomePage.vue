<template>
    <div>
        <h1 class="display-4">Home Page</h1>
        <div v-for="post in posts" :key="post.id">
            <PostView :post="post"></PostView>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { reactive, onMounted } from 'vue';
    import type { Post } from '../types/Post';
    import { API_URL } from '@/globals';
    import axios from 'axios';
    import PostView from './post/PostView.vue';

    const posts = reactive<Post[]>([]);

    onMounted( async () => {
        await axios.get(`${API_URL}posts`)
        .then((response) => {
            posts.push(...response.data);
        }).catch((error) => {
            console.log(error);
        })
    })

</script>