<script setup lang="ts">
import { formatDate } from '@/plugins/daysjs/Daysjs.ts'
import { useChatStore } from '@/stores/chatStore.ts'
import { useAuthStore } from '@/stores/auth.ts'

const chatStore = useChatStore()
const authStore = useAuthStore();
</script>

<template>
    <div class="right-panel bg-dark" role="complementary" aria-label="Panel de chats activos">
        <h2 class="text-center text-info-light p-3 fs-5">Active Chats</h2>

        <ul class="list-group list-group-flush px-3" role="list" v-if="authStore.isAuthenticated">
            <li v-show="chatStore.chatList.length === 0" class="list-group-item bg-dark border-bottom border-purple-light">
                <p class="fs-6 text-light">No active chats available.</p>
            </li>
            <li
                v-for="chatItem in chatStore.chatList"
                :key="chatItem.id"
                class="list-group-item bg-dark border-bottom border-purple-light"
                role="listitem"
            >
                <router-link
                    :to="`/chat/${chatItem.id}`"
                    class="nav-link text-purple-light d-flex pt-1 justify-content-between align-items-center"
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
                            <span
                                v-if="chatItem.newMessages > 0"
                                class="badge bg-danger ms-2"
                                aria-label="Mensajes sin leer"
                            >
                    {{ chatItem.newMessages }}
                </span>
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
        <div v-else class="text-center text-light-dark mt-3">
            <p class="fs-6">No active chats available.</p>
            <router-link :to="{name: 'login'}" class="btn btn-primary-alt" aria-label="Iniciar sesión">
                Login
            </router-link>
        </div>
    </div>
</template>

<style scoped>
/* Panel derecho fijo */
.right-panel {
  position: fixed;
  top: 0;
  right: 0;
  bottom: 0;
  width: 300px;
  height: 100vh;
  overflow-y: auto;
  padding-top: 1rem;
}

.chatImage{
    width: 45px;
    height: 45px;
}
</style>
