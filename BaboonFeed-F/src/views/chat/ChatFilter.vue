<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-12 col-md-6">
                <div class="mb-3">
                    <input type="text" class="form-control" placeholder="Buscar..." v-model="searchQuery"/>
                </div>

                <div v-if="searchQuery">
                    <p class="text-cyan">Searching for: "{{ searchQuery }}"</p>
                </div>

                <ul class="list-group">
                    <li class="list-group-item d-flex align-items-center gap-3" v-for="user in filteredUsers"
                        :key="user.username">
                        <div class="d-flex align-items-center" style="cursor: pointer" @click="goToProfile(user.username)">
                            <img :src="user.avatar" class="rounded-circle me-3" style="width: 40px; height: 40px; object-fit: cover;" />
                            <span>{{ user.username }}</span>
                        </div>
                        <button class="btn btn-sm btn-primary" @click="startChat(user)">
                            <font-awesome-icon :icon="['fas', 'comment']" />
                        </button>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useUsers } from '@/composables/useUsers.ts'
import type { PublicUserDto } from '@/dtos/PublicUserDto.ts'
import { useChatStore } from '@/stores/chatStore.ts'
import { useRouter } from 'vue-router'
import { type Chat, ChatType } from '@/types/Chat.ts'
import axios from 'axios'
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts'

const searchQuery = ref('')
const users = useUsers();
const filteredUsers = ref<PublicUserDto[]>([]);
const chatStore = useChatStore()
const router = useRouter();
const auth = useAuthStore();

watch(searchQuery, async (newQuery) => {
    if (!newQuery) {
        filteredUsers.value = [];
        return;
    }

    const query = newQuery.toLowerCase();
    filteredUsers.value = (await users).value.filter((user) =>
        user.username.toLowerCase().includes(query)
    );
});

const goToProfile = (username: string) => {
    router.push(`/users/profile/${username}`)
}

const startChat = async (targetUser: PublicUserDto) => {
    console.log('startChat', targetUser)
    const existingChat = chatStore.chatList.find(chat =>
        chat.type === ChatType.PRIVATE &&
        chat.members.some(m => m.username === targetUser.username)
    )

    if (existingChat) {
        console.log('existingChat', existingChat)
        router.push(`/chat/${existingChat.id}`)
        return
    }

    try {
        const response = await axios.post(`${API_URL}chats/`, {
            members: [targetUser.username]
        }, {
            headers: { Authorization: `Bearer ${auth.token}` }
        })

        const newChat: Chat = {
            ...response.data,
            id: `${ChatType.PRIVATE}_${response.data.id}`,
            type: ChatType.PRIVATE,
            name: targetUser.username,
            avatar_url: targetUser.avatar,
        }

        chatStore.chatList.unshift(newChat)
        console.log(newChat)
        router.push(`/chat/${newChat.id}`)
    } catch (err) {
        console.error('Error al crear el chat:', err)
    }
}

</script>

<style scoped>
img {
    object-fit: cover;
}
</style>
