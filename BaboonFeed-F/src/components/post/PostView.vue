<template>
    <div class="border border-dark-light rounded m-2 bg-secondary-alt w-75" role="article" :aria-labelledby="`post-title-${post.id}`">
        <div class="d-flex align-items-center justify-content-between px-3 p-2 border-bottom border-dark-light">
            <router-link :to="{ name: 'profile', params: { username: post.user.username } }" class="d-flex mt-2 align-items-center link-underline link-underline-opacity-0">
                <img class="me-2 rounded-circle border border-2 border-cyan"
                     :src="post.user.avatar" :alt="`Foto de perfil de ${post.user.username}`"
                     style="height: 35px; width: 35px;" />
                <h2 class="text-light-alt h5 mb-0" :id="`post-title-${post.id}`">
                    {{ post.user.username }}
                </h2>
            </router-link>

            <div class="p-2 border-start border-end border-3 border-purple rounded">
                <time :datetime="post.created_at">
                    <small>{{ formatDate(post.created_at) }}</small>
                </time>
            </div>
        </div>

        <div class="m-3 p-2 d-flex flex-column align-items-center">
            <p class="text-center">{{ post.content }}</p>
            <div :class="post.file.type === FileTypes.VIDEO ? `w-75 h-50 mb-3 me-5 me-md-0` : `w-75 h-50 mb-3`" v-if="post.file">
                <FileHandler :file="post.file" />
            </div>
            <div class="d-flex justify-content-end">
                <button class="btn btn-outline-primary-alt me-3" @click="handleLike(post)">
                    <font-awesome-icon :icon="['far', 'thumbs-up']" />
                    {{ post.likes.length }}
                </button>
                <button class="btn btn-outline-primary-alt me-3" @click="handleDislike(post)">
                    <font-awesome-icon :icon="['far', 'thumbs-down']" />
                    {{ post.dislikes.length }}
                </button>
                <router-link :to="{ name: 'replies', params: { id: post.id }}" class="btn btn-outline-primary-alt">
                    <font-awesome-icon :icon="['far', 'comment']" />
                </router-link>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import type { Post } from '@/types/Post.ts';
import FileHandler from '@/components/file/FileHandler.vue';

import axios from 'axios'
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts'
import { formatDate } from '@/plugins/daysjs/Daysjs.ts'
import { FileTypes } from '@/types/File.ts'

const authStore = useAuthStore();
const {post} = defineProps<{post: Post}>();

const handleLike = async (post: Post) => {
    if (!authStore.isAuthenticated) {
        alert('You need to login to like/dislike a post');
        return;
    }
    await axios.patch(`${API_URL}posts/${post.id}/like/`, {}, {
        headers: {
            'Authorization': `Bearer ${authStore.token}`
        }
    }).then(() => {
        const user = authStore.user;
        if (user && user.id) {
            if (post.likes.includes(user.id)) {
                post.likes = post.likes.filter((like) => like !== user.id);
            } else {
                post.likes.push(user.id);
                if (post.dislikes.includes(user.id)) {
                    post.dislikes = post.dislikes.filter((dislike) => dislike !== user.id);
                }
            }
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}

const handleDislike = async (post: Post) => {
    if (!authStore.isAuthenticated) {
        alert('You need to login to like/dislike a post');
        return;
    }
    await axios.patch(`${API_URL}posts/${post.id}/dislike/`, {}, {
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
    }).then(() => {
        const user = authStore.user;
        if (user && user.id) {
            if (post.dislikes.includes(user.id)) {
                post.dislikes = post.dislikes.filter((dislike) => dislike !== user.id);
            } else {
                post.dislikes.push(user.id);
                if (post.likes.includes(user.id)) {
                    post.likes = post.likes.filter((like) => like !== user.id);
                }
            }
        }
    }).catch(error => {
        console.error('Error:', error);
    });
}

</script>
