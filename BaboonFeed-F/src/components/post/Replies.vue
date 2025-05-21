<script setup lang="ts">
import ReplyView from '@/components/post/ReplyView.vue'

import { ref, onMounted } from 'vue'
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts'
import axios from 'axios';
import type { Post, Reply } from '@/types/Post.ts'
import { useRoute } from 'vue-router'
import PostView from '@/components/post/PostView.vue'

const authStore = useAuthStore()
const route = useRoute()
const replies = ref<Reply[]>([])
const postId = ref<string | null>(null)
const post = ref<Post | null>(null)
const replyContent = ref<string>('')

onMounted(async () => {
    postId.value = route.params.id as string
    await loadPost();
    await loadReplies()
})

async function loadPost() {
    if (!postId.value) {
        console.error('Post ID is null')
        return
    }
    try {
        const response = await axios.get(`${API_URL}posts/${postId.value}/`, {
            headers: {
                Authorization: `Bearer ${authStore.token}`,
            },
        })
        post.value = response.data
    } catch (error) {
        console.error('Error loading post:', error)
    }
}

async function loadReplies() {
    if (!postId.value) {
        console.error('Post ID is null')
        return
    }
    try {
        const response = await axios.get(`${API_URL}posts/${postId.value}/replies/`, {
            headers: {
                Authorization: `Bearer ${authStore.token}`,
            },
        })
        replies.value = await response.data
    } catch (error) {
        console.error('Error loading replies:', error)
    }
}

async function handleSubmit() {
    if (!replyContent.value) {
        alert('Reply content cannot be empty')
        return
    }
    try {
        const response = await axios.post(`${API_URL}posts/${postId.value}/replies/`, {
            content: replyContent.value,
        }, {
            headers: {
                Authorization: `Bearer ${authStore.token}`,
            },
        })
        replies.value.push(response.data)
        replyContent.value = ''
    } catch (error) {
        console.error('Error submitting reply:', error)
    }
}
</script>

<template>
    <div class="col-md-12 col-lg-9 me-2 content d-flex w-100 flex-column justify-content-center align-items-center overflow-hidden"
         role="list"
         aria-labelledby="home-heading"
         v-if="post"
    >
        <PostView :post="post" />
    </div>
    <form class="col-md-12 col-lg-9 me-2 content d-flex w-100 flex-column justify-content-center align-items-center overflow-hidden border-bottom border-purple-light"
          role="form"
          aria-labelledby="home-heading"
            @submit.prevent="handleSubmit"
    >
        <div class="d-flex justify-content-center align-items-center mb-3" style="width: 75%;">
            <textarea v-model="replyContent" class="form-control" placeholder="Write a reply..." rows="1"></textarea>
            <button type="submit" class="btn btn-primary ms-2">
                <font-awesome-icon :icon="['fas', 'paper-plane']" />
            </button>
        </div>
    </form>
    <div class="col-md-12 col-lg-9 me-2 content d-flex w-100 flex-column justify-content-center align-items-center overflow-hidden border-bottom border-purple-light"
         role="list"
         aria-labelledby="home-heading"
    >
        <div v-if="!replies || replies.length === 0" class="text-center mb-3">
            No replies for this post
        </div>
        <ReplyView v-for="reply in replies" :key="reply.id" :reply="reply" />
    </div>
</template>

<style scoped>

</style>
