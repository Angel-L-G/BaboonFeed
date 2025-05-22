import { defineStore } from 'pinia'
import { ref } from 'vue'
import { type Chat, ChatType } from '@/types/Chat.ts'
import type { User } from '@/types/User.ts'
import axios from 'axios'
import { useAuthStore } from '@/stores/auth.ts'
import ReconnectingWebSocket from 'reconnecting-websocket'
import { API_URL, API_WEBSOCKET_URL } from '@/globals.ts'
import type { MessageReceived } from '@/types/Message.ts'

type Socket = {
    id: string
    socket: ReconnectingWebSocket
}

export const useChatStore = defineStore('chat', () => {
    const authStore = useAuthStore()
    const chatList = ref<Chat[]>([])
    const sockets = ref<Socket[]>([])
    const activeChatId = ref<string>('')
    const onMessageReceived = ref<((message: MessageReceived) => void) | null>(null)


    async function getUserChats() {
        const privateChats = await axios
            .get(`${API_URL}chats/`, {
                headers: { Authorization: `Bearer ${authStore.token}` },
            })
            .then((res) =>
                res.data.map((chat: Chat) => {
                    const otherUser = chat.members
                        .filter((user: User) => user.username != authStore.user?.username)
                        .pop()
                    chat.type = ChatType.PRIVATE
                    chat.id = `${ChatType.PRIVATE}_${chat.id}`
                    chat.avatar_url = <string>otherUser?.avatar
                    chat.name = <string>otherUser?.username
                    chat.newMessages = 0;
                    return chat
                })
            )
            .catch((err) => {
                console.error(err)
                return []
            })

        const groupChats = await axios
            .get(`${API_URL}groups/`, {
                headers: { Authorization: `Bearer ${authStore.token}` },
            })
            .then((res) =>
                res.data.map((chat: Chat) => {
                    chat.type = ChatType.GROUP
                    chat.id = `${ChatType.GROUP}_${chat.id}`
                    chat.newMessages = 0;
                    return chat
                })
            )
            .catch((err) => {
                console.error(err)
                return []
            })

        chatList.value = [...privateChats, ...groupChats]
    }

    function registerMessageListener(fn: (message: MessageReceived) => void) {
        onMessageReceived.value = fn
    }

    function unregisterMessageListener() {
        onMessageReceived.value = null
    }


    async function _initializeSocket(
        socket: ReconnectingWebSocket,
        chatInfo: { type: ChatType; id: string },
        token: string,
    ) {
        socket.onopen = () => {
            const authMessage = { type: 'auth', token: token }
            socket.send(JSON.stringify(authMessage))
            console.log(`WebSocket ${chatInfo.type}#${chatInfo.id} conectado y autenticado`)
        }

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data)
            handleIncomingMessage(data.message, chatInfo)
        }

        socket.onclose = (event) => {
            console.warn(
                `WebSocket ${chatInfo.type}#${chatInfo.id} cerrado:`,
                event.reason || 'conexión cerrada',
            )
        }

        socket.onerror = (err) => {
            console.error(`Error en WebSocket ${chatInfo.type}#${chatInfo.id}:`, err)
        }
    }

    async function connectToAllChats() {
        const token = authStore.token
        const user = authStore.user
        if (!token || !user) return

        const privateUrl = `${API_WEBSOCKET_URL}ws/chat/private/${authStore.user?.username}/`
        const privateSocket = new ReconnectingWebSocket(privateUrl)
        await _initializeSocket(
            privateSocket,
            { type: ChatType.PRIVATE, id: String(user.id) },
            token,
        )
        sockets.value = [ ...sockets.value, { id: ChatType.PRIVATE, socket: privateSocket }]

        for (const group of chatList.value.filter((chat: Chat) => ChatType.GROUP == chat.type)) {
            const groupUrl = `${API_WEBSOCKET_URL}ws/chat/group/${group.id.split("_")[1]}/`
            const groupSocket = new ReconnectingWebSocket(groupUrl)
            await _initializeSocket(groupSocket, { type: ChatType.GROUP, id: group.id }, token)
            sockets.value = [ ...sockets.value, { id: group.id, socket: groupSocket }]
        }
    }

    async function handleIncomingMessage(
        message: MessageReceived,
        chatInfo: { type: ChatType; id: string },
    ) {
        let chatId: string | null = null

        if (chatInfo.type === ChatType.PRIVATE) {
            chatId = `${ChatType.PRIVATE}_${message.chat}`
        } else {
            chatId = chatInfo.id
        }

        if (chatId == null) {
            console.warn('Mensaje recibido sin identificar chat:', message)
            return
        }

        if (activeChatId.value === chatId && onMessageReceived.value) {
            onMessageReceived.value(message)
        }

        const chatIndex = chatList.value.findIndex((c: Chat) => c.id === chatId)
        if (chatIndex === -1) {
            console.warn('Mensaje para chat no encontrado en store:', chatId)
            return
        }

        const chat: Chat = chatList.value[chatIndex]
        chat.last_message = message.content
        chat.last_modified = message.created_at || new Date().toISOString()

        if (activeChatId.value !== chatId) {
            chat.newMessages++;
            console.log('its different')
        }

        chatList.value.splice(chatIndex, 1)
        chatList.value.unshift(chat)
    }

    async function disconnectAllChats(){
        sockets.value.forEach((socket) => socket.socket.close())
        chatList.value = [];
    }

    function setActiveChatId(chatId: string) {
        activeChatId.value = chatId
    }

    function getSocket(chatId: string): ReconnectingWebSocket {
        return <ReconnectingWebSocket>sockets.value.find((socket) => socket.id == (chatId.startsWith(ChatType.PRIVATE) ? ChatType.PRIVATE : chatId) )?.socket
    }

    async function removeGroup(groupId: string) {
        const id = `${ChatType.GROUP}_${groupId}`
        const chatIndex = chatList.value.findIndex((c: Chat) => c.id === id)
        if (chatIndex === -1) {
            console.warn('Group not found in store:', groupId)
            return
        }
        chatList.value.splice(chatIndex, 1)

        sockets.value.find((socket) => socket.id == groupId)?.socket.close()
        const socketIndex = sockets.value.findIndex((socket) => socket.id == id)
        if (socketIndex === -1) {
            console.warn('Socket not found in store:', groupId)
            return
        }
        sockets.value.splice(socketIndex, 1)
    }

    async function addGroup(groupData: Chat) {
        const group: Chat = {
            ...groupData,
            id: `${ChatType.GROUP}_${groupData.id}`,
            type: ChatType.GROUP,
            newMessages: 0,
        }

        chatList.value.push(group)
        const groupSocket = new ReconnectingWebSocket(`${API_WEBSOCKET_URL}ws/chat/group/${groupData.id}/`)
        await _initializeSocket(groupSocket, { type: ChatType.GROUP, id: group.id }, authStore.token || '')
        sockets.value.push({ id: group.id, socket: groupSocket })
    }


    async function updateGroup(updatedGroup: Chat) {
        const id = `${ChatType.GROUP}_${updatedGroup.id}`
        const index = chatList.value.findIndex(c => c.id === id)

        if (index !== -1) {
            updatedGroup.id = id
            updatedGroup.type = ChatType.GROUP
            updatedGroup.newMessages = chatList.value[index].newMessages
            chatList.value.splice(index, 1)
            chatList.value.unshift(updatedGroup)
        } else {
            console.warn('Grupo no encontrado en chatList para actualizar:', updatedGroup.id)
        }
    }


    return { chatList, getUserChats, connectToAllChats, disconnectAllChats, setActiveChatId, getSocket, registerMessageListener, unregisterMessageListener, removeGroup, updateGroup, addGroup }
})
