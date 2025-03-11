<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import ReconnectingWebSocket from 'reconnecting-websocket';
import type {MessageReceived, MessageSent} from "@/types/Message.ts";
import MessageComponent from "@/components/Message.vue";


const messages = ref<MessageReceived[]>([]);
const newMessage = ref<string>('');
const socket = ref<ReconnectingWebSocket | null>(null);
const token = localStorage.getItem('token');
const otherUserId = 2;/*TODO change the id to the receiver*/

onMounted(() => {
    socket.value = new ReconnectingWebSocket(`ws://localhost:8000/ws/chat/private/${otherUserId}/`);

    socket.value.onmessage = (event: MessageEvent) => {
        try {
            console.log('WebSocket message:', event.data);
            const message: MessageReceived = JSON.parse(event.data).message;
            messages.value.push(message);
        } catch (error) {
            console.error('Error parsing WebSocket message:', error);
        }
    }

    socket.value.onclose = () => {
        console.log('WebSocket cerrado');
    }

    // Cuando se abra la conexión, enviar el token como un primer mensaje
    socket.value.onopen = () => {
        // Enviar el token en el primer mensaje
        const authMessage = { type: 'auth', token: token };
        socket.value!.send(JSON.stringify(authMessage));

        console.log('Conexión WebSocket establecida y token enviado');
    };
});

const sendMessage = () => {
    if (socket.value) {
        const messageData: MessageSent = { content: newMessage.value, receiver: "Coso2" };
        socket.value.send(JSON.stringify(messageData));
    }
}

onUnmounted(() => {
    if (socket.value) {
        socket.value.close();
    }
});
</script>

<template>
    <div class="container d-flex flex-column justify-content-between my-3" style="height: 90vh;">
        <div class="flex-grow-1 overflow-auto overflow-x-hidden" ref="chatContainer">
            <div v-for="message in messages" :key="message.id" class="row mt-3">
                <MessageComponent :message="message" />
            </div>
        </div>
        <div class="mt-4 flex">
            <div class="input-group mb-3">
                <input v-model="newMessage" type="text" placeholder="Escribe un mensaje..."
                       class="form-control bg-primary-subtle"/>
                <button @click="sendMessage" class="btn btn-primary text-light">Enviar</button>
            </div>
        </div>
    </div>
</template>
