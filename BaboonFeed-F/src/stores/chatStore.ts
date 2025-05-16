import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Chat } from '@/types/Chat.ts'
import { ChatType } from '@/types/Chat.ts'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth.ts'
import { API_URL } from '@/globals.ts'

const auth = useAuthStore()

export const useChatStore = defineStore('chat', () => {
    const chatList = ref<Chat[]>([])

    async function getPrivateChats() {
        await axios
            .get(`${API_URL}chats/`, {
                headers: { Authorization: `Bearer ${auth.token}` },
            })
            .then((res) => {
                chatList.value = res.data
                    .map((chat: Chat) => {
                        chat.type = ChatType.PRIVATE
                        chat.id = `${ChatType.PRIVATE}_${chat.id}`
                    })
                    .toArray()
            }).catch((err) => {
                console.error(err)
            })
    }

    async function getGroupChats() {
        await axios
            .get(`${API_URL}groups/`, {
                headers: { Authorization: `Bearer ${auth.token}` },
            })
            .then((res) => {
                chatList.value = res.data
                    .map((chat: Chat) => {
                        chat.type = ChatType.GROUP
                        chat.id = `${ChatType.GROUP}_${chat.id}`
                    })
                    .toArray()
            }).catch((err) => {
                console.error(err)
            })
    }

    async function getUserChats() {
        await getPrivateChats();
        await getGroupChats();
    }

    return { chatList, getUserChats }
})
