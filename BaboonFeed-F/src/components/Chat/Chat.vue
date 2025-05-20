<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref, watch } from 'vue'
import ReconnectingWebSocket from 'reconnecting-websocket'
import type { MessageReceived, MessageSent } from '@/types/Message.ts'
import type { Chat } from '@/types/Chat'
import MessageComponent from '@/components/Message.vue'
import { useRoute } from 'vue-router'
import { useChatStore } from '@/stores/chatStore.ts'
import { useAuthStore } from '@/stores/auth.ts'
import type { File as FileCustom } from '@/types/File.ts'
import { ChatType } from '@/types/Chat.ts'
import axios from 'axios'
import { API_URL } from '@/globals.ts'

const route = useRoute()
const chatId = computed(() => route.params.id as string)
const messages = ref<MessageReceived[]>([])
const isGroup = computed(() => chatId.value.startsWith(ChatType.GROUP))
const rawId = computed(() => chatId.value.split('_')[1])
const newMessage = ref<string>('')
const selectedFile = ref<File | null>(null)
const chatStore = useChatStore()
const authStore = useAuthStore()
const socket = ref<ReconnectingWebSocket>({} as ReconnectingWebSocket)
const nextQuery = ref<string>('')
const chat = computed(() => chatStore.chatList.find((chat) => chat.id === chatId.value) as Chat)

watch(
    () => route.params.id,
    async () => {
        messages.value = []
        newMessage.value = ''
        selectedFile.value = null
        await initializeChat()
    },
)

onMounted(async () => {
    await initializeChat()
})

async function initializeChat() {
    chatStore.setActiveChatId(chatId.value)
    try {
        await waitForSocket(chatId.value)
        socket.value = chatStore.getSocket(chatId.value)
    } catch (e) {
        console.error('No se pudo obtener el socket:', e)
    }
    await getMessages()
    chatStore.registerMessageListener((message: MessageReceived) => {
        messages.value = [...messages.value, message]
    })
}

async function getMessages() {
    const url = `${API_URL}${isGroup.value ? 'groups' : 'chats'}/${rawId.value}/messages/`
    await axios
        .get(url, {
            headers: {
                Authorization: `Bearer ${authStore.token}`,
            },
        })
        .then((res) => {
            messages.value.push(...res.data.results)
            messages.value = messages.value.reverse()
            nextQuery.value = res.data.next
        })
        .catch((err) => console.log(err))
}

async function waitForSocket(chatId: string, interval = 100, maxAttempts = 50): Promise<void> {
    return new Promise((resolve, reject) => {
        let attempts = 0
        const timer = setInterval(() => {
            const s = chatStore.getSocket(chatId)
            if (s) {
                clearInterval(timer)
                resolve()
            } else if (++attempts >= maxAttempts) {
                clearInterval(timer)
                reject(new Error('Socket not available'))
            }
        }, interval)
    })
}

const allowedTypes = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'audio/mpeg',
    'audio/ogg',
    'audio/wav',
    'video/mp4',
    'video/webm',
    'video/ogg',
]

const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]
    if (!file) {
        selectedFile.value = null
        return
    }

    if (!allowedTypes.includes(file.type)) {
        alert('Tipo de archivo no permitido.')
        target.value = '' // Limpia el input
        selectedFile.value = null
        return
    }

    selectedFile.value = file
}

async function uploadFile(): Promise<FileCustom | undefined> {
    if (!selectedFile.value) return undefined

    const formData = new FormData()
    formData.append('file', selectedFile.value)

    try {
        const response = await axios.post(`${API_URL}files/`, formData, {
            headers: {
                Authorization: `Bearer ${authStore.token}`,
                'Content-Type': 'multipart/form-data',
            },
        })
        return response.data
    } catch (error) {
        console.error('Error subiendo archivo:', error)
        return undefined
    }
}

const sendMessage = async () => {
    if (!socket.value || socket.value.readyState !== WebSocket.OPEN) return

    let file: FileCustom | undefined = undefined
    if (selectedFile.value) {
        file = await uploadFile()
        if (!file) return
    }

    const messageData: MessageSent = {
        content: newMessage.value,
        ...(isGroup.value ? { group: Number(rawId.value) } : { receiver: chat.value.name }),
        file: file,
    }

    socket.value.send(JSON.stringify(messageData))

    newMessage.value = ''
    selectedFile.value = null
}

onUnmounted(() => {
    messages.value = []
    newMessage.value = ''
    selectedFile.value = null
    chatStore.setActiveChatId('')
    chatStore.unregisterMessageListener()
})
</script>

<template>
    <div class="container d-flex flex-column justify-content-between my-3" style="height: 90vh">
        <div class="flex-grow-1 overflow-auto overflow-x-hidden" ref="chatContainer">
            <div v-for="message in messages" :key="message.id" class="row mt-3">
                <MessageComponent :message="message" />
            </div>
        </div>
        <div class="mt-4">
            <div class="input-group mb-3 align-items-center">
                <input
                    v-model="newMessage"
                    type="text"
                    placeholder="Escribe un mensaje..."
                    class="form-control bg-primary-subtle"
                />

                <!-- Botón personalizado para adjuntar archivo -->
                <label class="btn mb-0 bg-primary">
                    <font-awesome-icon :icon="['fas', 'link']" />
                    <input type="file" hidden @change="handleFileChange" />
                </label>

                <button @click="sendMessage" class="btn btn-primary">
                    <font-awesome-icon :icon="['fas', 'paper-plane']" />
                </button>
            </div>

            <!-- Mostrar nombre del archivo si hay -->
            <div
                v-if="selectedFile"
                class="text-muted small mt-1 d-flex align-items-center bg-primary rounded"
            >
                <span class="me-2">Archivo: {{ selectedFile.name }}</span>
                <button
                    @click="selectedFile = null"
                    class="btn btn-sm btn-outline-danger py-0 px-2"
                >
                    ✖
                </button>
            </div>
        </div>
    </div>
</template>
