<script setup lang="ts">
import { formatDate } from '@/plugins/daysjs/Daysjs.ts'
import { useChatStore } from '@/stores/chatStore.ts'

const chatStore = useChatStore()
</script>

<template>
    <div class="right-panel bg-dark" role="complementary" aria-label="Panel de chats activos">
        <h2 class="text-center text-info-light p-3 fs-5">Chats activos</h2>

        <ul class="list-group list-group-flush px-3" role="list">
            <li
                v-for="chatItem in chatStore.chatList"
                :key="chatItem.id"
                class="list-group-item bg-dark border-bottom border-purple-light"
                role="listitem"
            >
                <router-link
                    :to="`/chat/${chatItem.id}`"
                    class="nav-link text-purple-light d-flex pt-1"
                    :aria-label="`Abrir chat con ${chatItem.name}`"
                >
                    <div class="d-flex flex-column w-100">
                        <div class="d-flex flex-row align-items-center w-100">
                            <img
                                :src="chatItem.avatar_url"
                                :alt="`Foto de perfil de ${chatItem.name}`"
                                class="rounded-circle chatImage"
                            />
                            <h3 class="ms-1 text-light-dark fw-bold fs-6 mb-0">
                                {{ chatItem.name }}
                            </h3>
                        </div>

                        <div class="d-flex flex-column" style="max-width: 100%">
                            <div
                                class="mt-1 text-light text-truncate overflow-hidden"
                                style="max-width: 220px"
                                :title="chatItem.last_message"
                                :aria-label="`Último mensaje: ${chatItem.last_message}`"
                            >
                                {{ chatItem.last_message }}
                            </div>
                            <div class="text-end text-danger-light">
                                <time :datetime="chatItem.last_modified">
                                    {{ formatDate(chatItem.last_modified) }}
                                </time>
                            </div>
                        </div>
                    </div>
                </router-link>
            </li>
        </ul>
    </div>
</template>

<style scoped>
.chatImage {
    width: 45px;
    height: 45px;
}
</style>
