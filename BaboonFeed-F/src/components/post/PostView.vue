<template>
    <div class="border border-secondary rounded m-2">
        <div class="d-flex align-items-center justify-content-center rounded-top bg-info-subtle p-2">
            <img class="me-2 rounded-circle border border-primary-subtle border-3" :src="post.user.file?.name" :alt="post.user.username" style="height: 35px; width: 35px;">
            <h2>{{ post.user.username }}</h2>
        </div>
        <div class="d-flex flex-column p-2 align-items-center justify-content-center">
            <div v-if="post.file">
                <FileHandler :file="post.file"/>
            </div>
            <p>{{ post.content }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Post } from '../../types/Post';
import FileHandler from '../file/FileHandler.vue';

const {post} = defineProps<{post: Post}>();

</script>