<script setup lang="ts">
import { formatDate } from '@/plugins/daysjs/Daysjs.ts'

const chatList = [
    {
        id: 1,
        name: "Carlos Rodríguez",
        image: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        lastMessage: {
            text: "¿Nos vemos esta tarde?",
            date: "2025-03-12T17:30:00Z"
        }
    },
    {
        id: 2,
        name: "Ana Gómez",
        image: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        lastMessage: {
            text: "Te envié los documentos.",
            date: "2025-02-10T09:15:00Z"
        }
    },
    {
        id: 3,
        name: "Pedro Martínez",
        image: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        lastMessage: {
            text: "Gracias por la ayuda 🙏 de aquella vez",
            date: "2025-04-09T21:42:00Z"
        }
    },
    {
        id: 4,
        name: "Lucía Hernández",
        image: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        lastMessage: {
            text: "¿Ya viste el nuevo proyecto?",
            date: "2024-04-08T14:05:00Z"
        }
    },
    {
        id: 5,
        name: "Javier Torres",
        image: "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png",
        lastMessage: {
            text: "Hablamos mañana sin falta.",
            date: "2024-04-07T08:30:00Z"
        }
    }
]
</script>

<template>
    <div class="right-panel bg-dark">
        <h5 class="text-center text-info-light p-3">Active Chats</h5>
        <ul class="list-group list-group-flush px-3">
            <li v-for="chatItem in chatList" class="list-group-item bg-dark border-bottom border-purple-light">
                <router-link :to="`/chat/${chatItem.id}`" class="nav-link text-purple-light d-flex pt-1">
                    <div class="d-flex flex-column w-100">
                        <div class="d-flex flex-row align-items-center w-100">
                            <img :src="chatItem.image" alt="Profile" class="rounded-circle chatImage"/>
                            <h5 class="ms-1 text-light-dark fw-bold">{{ chatItem.name }}</h5>
                        </div>
                        <div class="d-flex flex-column" style="max-width: 100%;">
                            <div class="mt-1 text-light text-truncate overflow-hidden" style="max-width: 220px;">{{ chatItem.lastMessage.text }}</div>
                            <div class="text-end text-danger-light">{{ formatDate(chatItem.lastMessage.date )}}</div>
                        </div>
                    </div>
                </router-link>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.chatImage{
    width: 45px;
    height: 45px;
}
</style>
