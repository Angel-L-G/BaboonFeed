import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Chat } from '@/types/Chat.ts'
import type { User } from '@/types/User.ts'
import { ChatType } from '@/types/Chat.ts'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth.ts'
import ReconnectingWebSocket from 'reconnecting-websocket';
import { API_URL, API_WEBSOCKET_URL } from '@/globals.ts'

type Socket = {
    id: string,
    socket: ReconnectingWebSocket
}

const auth = useAuthStore()

export const useChatStore = defineStore('chat', () => {
    const chatList = ref<Chat[]>([])
    const sockets = ref<Socket[]>([])

    async function getPrivateChats() {
        await axios
            .get(`${API_URL}chats/`, {
                headers: { Authorization: `Bearer ${auth.token}` },
            })
            .then((res) => {
                chatList.value = res.data
                    .map((chat: Chat) => {
                        const otherUser = chat.members.filter((user: User) => user.username != auth.user?.username).pop();
                        chat.type = ChatType.PRIVATE;
                        chat.id = `${ChatType.PRIVATE}_${chat.id}`;
                        chat.avatar_url = <string>otherUser?.avatar;
                        chat.name = <string>otherUser?.username;
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
                        chat.type = ChatType.GROUP;
                        chat.id = `${ChatType.GROUP}_${chat.id}`;
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

    async function _initializeSocket(socket: ReconnectingWebSocket, chatInfo: { type: 'private' | 'group', id: number }, token: string) {
        socket.onopen = () => {
            // Enviar token JWT para autenticación en cuanto el socket se conecta
            const authMessage = { type: 'auth', token: token }
            socket.send(JSON.stringify(authMessage))
            console.log(`WebSocket ${chatInfo.type}#${chatInfo.id} conectado y autenticado`)
        }

        // Manejar mensajes entrantes:
        socket.onmessage = (event) => {
            const data = JSON.parse(event.data)
            this.handleIncomingMessage(data, chatInfo)
        }

        socket.onclose = (event) => {
            console.warn(`WebSocket ${chatInfo.type}#${chatInfo.id} cerrado:`, event.reason || 'conexión cerrada')
            // Opcional: reconectar lógica o limpieza de estado
        }

        socket.onerror = (err) => {
            console.error(`Error en WebSocket ${chatInfo.type}#${chatInfo.id}:`, err)
        }
    }

    async function connectToAllChats() {
        const authStore = useAuthStore()
        const token = authStore.token;
        const user = authStore.user;
        if (!token || !user) return

        // Conexión para chats privados (un solo socket para todos los privados)
        const privateUrl = `${API_WEBSOCKET_URL}ws/chat/private/${authStore.user?.username}/`
        const privateSocket = new ReconnectingWebSocket(privateUrl)
        await _initializeSocket(privateSocket, { type: 'private', id: user.id }, token)
        // Guardamos la referencia si deseamos manejarla después (p. ej., para cerrar al salir)
        const newSockets = sockets.value
        newSockets.push({'id': 'private', 'socket': privateSocket})
        sockets.value = { ...newSockets }

        const groups = chatList.value.filter((chat: Chat) => ChatType.GROUP == chat.type)
        for (const group in groups) {
            const groupUrl = `${API_WEBSOCKET_URL}ws/chat/group/${group}`
        }
    }

    return { chatList, getUserChats }
})
