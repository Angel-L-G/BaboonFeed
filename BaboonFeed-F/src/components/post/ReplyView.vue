<script setup lang="ts">
import { formatDate } from '@/plugins/daysjs/Daysjs.ts'
import type { Reply } from '@/types/Post.ts'
import { useAuthStore } from '@/stores/auth.ts'
import { API_URL } from '@/globals.ts'
import axios from 'axios'

const authStore = useAuthStore()
const { reply } = defineProps<{ reply: Reply }>();
console.log(reply);

const handleLike = async (reply: Reply) => {
    if (!authStore.isAuthenticated) {
        alert('You need to login to like/dislike a reply')
        return
    }
    await axios.patch(`${API_URL}posts/${reply.post}/replies/${reply.id}/like/`, {}, {
        headers: {
            'Authorization': `Bearer ${authStore.token}`
        }
    }).then(() => {
        const user = authStore.user
        if (user && user.id) {
            if (reply.likes.includes(user.id)) {
                reply.likes = reply.likes.filter((like) => like !== user.id)
            } else {
                reply.likes.push(user.id)
                if (reply.dislikes.includes(user.id)) {
                    reply.dislikes = reply.dislikes.filter((dislike) => dislike !== user.id)
                }
            }
        }
    }).catch(error => {
        console.error('Error:', error)
    })
}

const handleDislike = async (reply: Reply) => {
    if (!authStore.isAuthenticated) {
        alert('You need to login to like/dislike a reply')
        return
    }
    await axios.patch(`${API_URL}posts/${reply.post}/replies/${reply.id}/dislike/`, {}, {
        headers: {
            'Authorization': `Bearer ${authStore.token}`
        }
    }).then(() => {
        const user = authStore.user
        if (user && user.id) {
            if (reply.dislikes.includes(user.id)) {
                reply.dislikes = reply.dislikes.filter((dislike) => dislike !== user.id)
            } else {
                reply.dislikes.push(user.id)
                if (reply.likes.includes(user.id)) {
                    reply.likes = reply.likes.filter((like) => like !== user.id)
                }
            }
        }
    }).catch(error => {
        console.error('Error:', error)
    })
}
</script>

<template>
    <div class="rounded m-2 w-75" role="article" :aria-labelledby="`post-title-${reply.id}`">
        <div class="d-flex align-items-center justify-content-between px-3 p-2 border-bottom border-dark-light">
            <div class="d-flex mt-2 align-items-center">
                <img class="me-2 rounded-circle border border-2 border-cyan"
                     :src="reply.user.avatar" :alt="`Foto de perfil de ${reply.user.username}`"
                     style="height: 35px; width: 35px;" />
                <h2 class="text-light-alt h5 mb-0" :id="`post-title-${reply.id}`">
                    {{ reply.user.username }}
                </h2>
            </div>

            <div class="p-2 border-start border-end border-3 border-purple rounded">
                <time :datetime="reply.created_at">
                    <small>{{ formatDate(reply.created_at) }}</small>
                </time>
            </div>
        </div>

        <div class="m-3 p-2 d-flex flex-column align-items-start">
            <p class="text-left">{{ reply.content }}</p>
            <div class="d-flex justify-content-end">
                <button class="btn btn-outline-primary-alt me-3" @click="handleLike(reply)">
                    <font-awesome-icon :icon="['far', 'thumbs-up']" />
                    {{ reply.likes.length }}
                </button>
                <button class="btn btn-outline-primary-alt" @click="handleDislike(reply)">
                    <font-awesome-icon :icon="['far', 'thumbs-down']" />
                    {{ reply.dislikes.length }}
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
