<template>
    <div>
        <h1 class="display-4">Home Page</h1>
        <div v-for="post in posts" :key="post.id">
            <h2>{{ post.user.username }}</h2>
            <div v-if="post.file">
                <img v-if="post.file.type == FileTypes.IMAGE" :src="post.file.name" alt="post" style="width: 100%; height: auto;">
                <media-player v-if="post.file.type == FileTypes.VIDEO" title="Sprite Fight" :src="post.file.name">
                    <media-provider></media-provider>
                    <media-video-layout thumbnails="https://files.vidstack.io/sprite-fight/thumbnails.vtt"></media-video-layout>
                </media-player>
            </div>
            <p>{{ post.content }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { reactive, onMounted } from 'vue';
    import type { Post } from '../types/Post';
    import { FileTypes } from '../types/File';
    import { API_URL } from '@/globals';
    import axios from 'axios';
    import 'vidstack/bundle';

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