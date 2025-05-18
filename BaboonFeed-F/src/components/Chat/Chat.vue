<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import ReconnectingWebSocket from 'reconnecting-websocket'
import type { MessageReceived, MessageSent } from '@/types/Message.ts'
import MessageComponent from '@/components/Message.vue'
import { useRoute } from 'vue-router'
import { useChatStore } from '@/stores/chatStore.ts'
import { useAuthStore } from '@/stores/auth.ts'
import { ChatType } from '@/types/Chat.ts'
import axios from 'axios'
import { API_URL } from '@/globals.ts'
import { watch } from 'vue'

const route = useRoute()
const chatId = computed(() => route.params.id as string)
const messages = ref<MessageReceived[]>([])
const isGroup = computed(() => chatId.value.startsWith(ChatType.GROUP))
const rawId = computed(() => chatId.value.split('_')[1])
const newMessage = ref<string>('')
const chatStore = useChatStore()
const authStore = useAuthStore()
const socket = ref<ReconnectingWebSocket>()
const nextQuery = ref<string>('')

watch(() => route.params.id, async () => {
    messages.value = []
    newMessage.value = ''
    await initializeChat()
})



onMounted(async () => {
    await initializeChat();
})

async function initializeChat(){
    socket.value = chatStore.getSocket(chatId.value)
    chatStore.setActiveChatId(chatId.value)
    await getMessages();
}

async function getMessages() {
    const url = `${API_URL}api/${isGroup.value ? 'groups' : 'chats'}/${rawId.value}/messages/`
    await axios
        .get(url, {
            headers: {
                Authorization: `Bearer ${authStore.token}`,
            },
        })
        .then((res) =>{
            (messages.value.unshift(...res.data.results))
            nextQuery.value = res.data.next
        })
        .catch((err) => console.log(err))
}

const sendMessage = () => {
    if (socket.value) {
        let messageData: MessageSent = {} as MessageSent
        if (isGroup.value) {
            messageData = { content: newMessage.value, group: Number(rawId.value) }
        } else {
            messageData = { content: newMessage.value, receiver: rawId.value }
        }
        socket.value.send(JSON.stringify(messageData))
    }
}

onUnmounted(() => {
    chatStore.setActiveChatId('')
})
</script>

<template>
    <div class="container d-flex flex-column justify-content-between my-3" style="height: 90vh">
        <div class="flex-grow-1 overflow-auto overflow-x-hidden" ref="chatContainer">
            <div v-for="message in messages" :key="message.id" class="row mt-3">
                <MessageComponent :message="message" />
            </div>
        </div>
        <div class="mt-4 flex">
            <div class="input-group mb-3">
                <input
                    v-model="newMessage"
                    type="text"
                    placeholder="Escribe un mensaje..."
                    class="form-control bg-primary-subtle"
                />
                <button @click="sendMessage" class="btn btn-primary text-light">Enviar</button>
            </div>
        </div>
    </div>
</template>
