<template>
    <div class="border border-dark-light rounded m-2 bg-secondary-alt w-75" role="article" :aria-labelledby="`post-title-${post.id}`">
        <div class="d-flex align-items-center justify-content-between px-3 p-2 border-bottom border-dark-light">
            <div class="d-flex mt-2 align-items-center">
                <img class="me-2 rounded-circle border border-2 border-cyan"
                     :src="post.user.file?.name" :alt="`Foto de perfil de ${post.user.username}`"
                     style="height: 35px; width: 35px;" />
                <h2 class="text-light-alt h5 mb-0" :id="`post-title-${post.id}`">
                    {{ post.user.username }}
                </h2>
            </div>

            <div class="p-2 border-start border-end border-3 border-purple rounded">
                <time :datetime="post.created_at">
                    <small>{{ formatDate(post.created_at) }}</small>
                </time>
            </div>
        </div>

        <div class="m-3 p-2 d-flex flex-column align-items-center">
            <p class="text-center">{{ post.content }}</p>
            <div class="w-75 h-50" v-if="post.file">
                <FileHandler :file="post.file" />
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Post } from '@/types/Post.ts';
import FileHandler from '@/components/file/FileHandler.vue';
import { formatDate } from '@/plugins/daysjs/Daysjs.ts'

const {post} = defineProps<{post: Post}>();

</script>
