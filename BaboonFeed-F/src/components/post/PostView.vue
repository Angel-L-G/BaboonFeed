<template>
    <div>
        <h2>{{ post.user.username }}</h2>
        <div v-if="post.file">
            <img v-if="post.file.type == FileTypes.IMAGE" :src="post.file.name" alt="post" style="width: 100%; height: auto;">
            <media-player v-if="post.file.type == FileTypes.VIDEO || post.file.type == FileTypes.AUDIO " title="Sprite Fight" :src="post.file.name">
                <media-provider></media-provider>
            </media-player>
        </div>
        <p>{{ post.content }}</p>
    </div>
</template>

<script setup lang="ts">
import { Post } from '../../types/Post';
import { FileTypes } from '../../types/File';
import 'vidstack/bundle';

const {post} = defineProps<{post: Post}>();

</script>