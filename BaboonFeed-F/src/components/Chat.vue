<script setup lang="ts">
/*
import { ref, onMounted } from 'vue'
import { db } from '@/firebase' // Asegúrate de configurar Firebase
import { collection, addDoc, query, orderBy, onSnapshot } from 'firebase/firestore'

const messages = ref([])
const newMessage = ref('')
const messagesRef = collection(db, 'messages')

onMounted(() => {
    const q = query(messagesRef, orderBy('createdAt'))
    onSnapshot(q, (snapshot) => {
        messages.value = snapshot.docs.map((doc) => ({ id: doc.id, ...doc.data() }))
    })
})

const sendMessage = async () => {
    if (newMessage.value.trim() === '') return
    await addDoc(messagesRef, {
        text: newMessage.value,
        createdAt: new Date(),
    })
    newMessage.value = ''
}
*/
import {onMounted, ref} from "vue";
import type {Message} from "@/types/Message.ts";
import MessageComponent from "@/components/Message.vue";

const messages = ref<Message[]>([]);
const newMessage = ref('');

onMounted(() => {
    fetch('http://localhost:3000/messages')
        .then(messagesFetch => {
            return messagesFetch.json();
        }).then(messagesData => {
            messages.value = messagesData;
        }).catch(error => {
            console.log(error);
        })
});

const sendMessage = () => {
    fetch('http://localhost:3000/messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            id: messages.value.length + 1,
            content: newMessage.value,
            created_at: new Date().toString(),
            author: 1
        })
    }).then(() => {
        newMessage.value = '';
    }).catch(error => {
        console.log(error);
    });
};
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
