<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-12 col-md-6">
                <div class="mb-3">
                    <input
                        type="text"
                        class="form-control"
                        placeholder="Buscar..."
                        v-model="searchQuery"
                    />
                </div>

                <div v-if="searchQuery">
                    <p class="text-cyan">Searching for: "{{ searchQuery }}"</p>
                </div>

                <div class="d-grid gap-3">
                    <div
                        v-for="user in filteredUsers"
                        :key="user.username"
                        class="d-flex justify-content-between align-items-center p-3 bg-dark text-light rounded shadow-sm group-card"
                        role="button"
                    >
                        <div
                            class="d-flex align-items-center gap-3"
                            @click="goToProfile(user.username)"
                        >
                            <img :src="user.avatar" class="rounded-circle" width="48" height="48" />
                            <strong>{{ user.username }}</strong>
                        </div>
                        <button class="btn btn-primary btn-sm" @click="startChat(user)">
                            <font-awesome-icon :icon="['fas', 'comment']" />
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useUsers } from '@/composables/useUsers.ts'
import type { PublicUserDto } from '@/dtos/PublicUserDto.ts'
import { useChatStore } from '@/stores/chatStore.ts'
import { useRouter } from 'vue-router'
import { type Chat, ChatType } from '@/types/Chat.ts'
import axios from 'axios'
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts'

const searchQuery = ref('')
const users = useUsers()
const filteredUsers = ref<PublicUserDto[]>([])
const chatStore = useChatStore()
const defaultChats = computed(() =>
    chatStore.chatList
        .filter((chat: Chat) => chat.type == ChatType.PRIVATE)
        .map((chat: Chat) => ({ username: chat.name, avatar: chat.avatar_url } as PublicUserDto)),
)
const router = useRouter()
const auth = useAuthStore()

onMounted(() => {
    if (searchQuery.value === '') {
        const currentUsername = auth.user?.username || JSON.parse(localStorage.getItem('user') || '{}')?.username
        let initialized = false

        const stop = watch(
            () => chatStore.chatList.length,
            (length) => {
                if (length > 0) {
                    filteredUsers.value = chatStore.chatList
                        .filter((chat) => chat.type === ChatType.PRIVATE)
                        .map((chat) => ({
                            username: chat.name,
                            avatar: chat.avatar_url,
                        }))
                    if (initialized) stop()
                    initialized = true
                }
            },
            { immediate: true }
        )
    }
})


watch(searchQuery, async (newQuery) => {
    const currentUsername = auth.user?.username || JSON.parse(localStorage.getItem('user') || '{}')?.username

    if (!newQuery) {
        filteredUsers.value = defaultChats.value
        return
    }

    const query = newQuery.toLowerCase()
    filteredUsers.value = (await users).value.filter((user) =>
        user.username.toLowerCase().includes(query),
    ).filter(user => user.username !== currentUsername);
})

const goToProfile = (username: string) => {
    router.push(`/users/profile/${username}`)
}

const startChat = async (targetUser: PublicUserDto) => {
    console.log('startChat', targetUser)
    const existingChat = chatStore.chatList.find(
        (chat) =>
            chat.type === ChatType.PRIVATE &&
            chat.members.some((m) => m.username === targetUser.username),
    )

    if (existingChat) {
        console.log('existingChat', existingChat)
        router.push(`/chat/${existingChat.id}`)
        return
    }

    await axios.post(
        `${API_URL}chats/`,
        {
            members: [targetUser.username],
        },
        {
            headers: { Authorization: `Bearer ${auth.token}` },
        },
    ).then(async (response) => {
        const id = await chatStore.addPrivateChat(response.data, targetUser)
        await router.push(`/chat/${id}`)
    }).catch((error) => {
        console.error(error)
    })
}
</script>

<style scoped>
img {
    object-fit: cover;
}
</style>
