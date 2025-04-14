<template>
    <div class="border border-dark-light rounded m-2 bg-secondary-alt w-75">
        <div class="d-flex align-items-center justify-content-between px-3 p-2 border-bottom border-dark-light">
            <div class="d-flex mt-2">
                <img class="me-2 rounded-circle border border-2 border-cyan" :src="post.user.file?.name" :alt="post.user.username" style="height: 35px; width: 35px;">
                <h2 class="text-light-alt">{{ post.user.username }}</h2>
            </div>
            <div class="p-2 border-start border-end border-3 border-purple rounded">
                <small>{{ getTimeSince(post.created_at) }}</small>
            </div>
        </div>
        <div class="m-3 p-2 d-flex flex-column align-items-center">
            <p class="text-center ">{{ post.content }}</p>
            <div class="w-75 h-50" v-if="post.file">
                <FileHandler :file="post.file"/>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Post } from '@/types/Post.ts';
import FileHandler from '@/components/file/FileHandler.vue';

import { format, formatDistanceToNow, isToday, isYesterday } from "date-fns";
import { enUS } from "date-fns/locale";

const getTimeSince = (date: string) => {
    const postDate = new Date(date);

    if (isToday(postDate)) {
        return formatDistanceToNow(postDate, { addSuffix: true, locale: enUS });
    } else if (isYesterday(postDate)) {
        return "Yesterday";
    } else {
        return format(postDate, "EEEE do MMMM", { locale: enUS });
    }
};


const {post} = defineProps<{post: Post}>();

</script>
