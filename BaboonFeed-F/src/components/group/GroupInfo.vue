<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import axios from 'axios'
import { API_URL } from '@/globals.ts'
import type { Group } from '@/types/Group'
import { useAuthStore } from '@/stores/auth.ts'
import { useChatStore } from '@/stores/chatStore.ts'
import EditGroup from '@/components/group/EditGroup.vue'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const group = ref<Group | null>(null)
const isLoading = ref(true)
const showConfirmModal = ref(false)

onMounted(async () => {
    await fetchGroup()
})

async function fetchGroup() {
    try {
        const response = await axios.get(`${API_URL}groups/${route.params.id}/`, {
            headers: { Authorization: `Bearer ${authStore.token}` },
        })
        group.value = response.data
    } catch (err) {
        console.error('Error al cargar grupo:', err)
    } finally {
        isLoading.value = false
    }
}

const leaveGroup = async () => {
    try {
        await axios.delete(`${API_URL}groups/${group.value?.id}/leave/`, {
            headers: { Authorization: `Bearer ${authStore.token}` },
        })
        await useChatStore().removeGroup(group.value?.id as string)
        await router.push('/')
    } catch (err) {
        console.error('Error al salir del grupo:', err)
    }
}

const goToUserProfile = (username: string) => {
    router.push(`/users/profile/${username}`)
}
</script>

<template>
    <div class="container mt-4 text-white">
        <div v-if="isLoading" class="text-center">
            <div class="spinner-border" role="status">
                <span class="visually-hidden">Charging...</span>
            </div>
        </div>

        <div v-else-if="group" class="card bg-dark p-4">
            <div class="d-flex align-items-center gap-3 mb-4">
                <img
                    :src="group.avatar_url"
                    alt="avatar"
                    class="rounded-circle border border-2"
                    style="width: 60px; height: 60px; object-fit: cover"
                />
                <h2 class="mb-0 text-white">{{ group.name }}</h2>
                <button
                    v-if="authStore.user?.username === group.leader.username"
                    class="btn btn-purple-alt ms-auto"
                    data-bs-toggle="modal"
                    data-bs-target="#EditGroupModal"
                >
                    <font-awesome-icon :icon="['fas', 'pencil']" />
                </button>
            </div>

            <h4 class="text-primary">Leader</h4>
            <div
                class="d-flex align-items-center gap-2 mb-3 pointer"
                style="cursor: pointer"
                @click="goToUserProfile(group.leader.username)"
            >
                <img
                    :src="group.leader.avatar"
                    alt="avatar"
                    class="rounded-circle"
                    style="width: 40px; height: 40px; object-fit: cover"
                />
                <span class="text-white">{{ group.leader.username }}</span>
            </div>

            <h4 class="text-primary">Miembros</h4>
            <div class="d-flex flex-wrap gap-3">
                <div
                    v-for="member in group.members"
                    :key="member.username"
                    class="d-flex align-items-center gap-2 pointer"
                    style="cursor: pointer"
                    @click="goToUserProfile(member.username)"
                >
                    <img
                        :src="member.avatar"
                        alt="avatar"
                        class="rounded-circle"
                        style="width: 35px; height: 35px; object-fit: cover"
                    />
                    <span class="text-white">{{ member.username }}</span>
                </div>
            </div>

            <div class="mt-4">
                <button class="btn btn-danger" @click="showConfirmModal = true">
                    Salir del grupo
                </button>
            </div>
        </div>

        <div
            v-if="showConfirmModal"
            class="modal fade show d-block"
            tabindex="-1"
            role="dialog"
        >
            <div class="modal-dialog" role="document">
                <div class="modal-content bg-secondary text-light">
                    <div class="modal-header">
                        <h5 class="modal-title">¿Seguro que quieres salir del grupo?</h5>
                        <button type="button" class="btn-close" @click="showConfirmModal = false"></button>
                    </div>
                    <div class="modal-body">
                        <p>Ya no podrás enviar ni recibir mensajes en este grupo.</p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" @click="showConfirmModal = false">Cancelar</button>
                        <button class="btn btn-danger" @click="leaveGroup">Salir</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Modal para editar grupo -->
        <div
            class="modal fade"
            id="EditGroupModal"
            tabindex="-1"
            aria-labelledby="EditGroupModalLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content bg-secondary text-light">
                    <div class="modal-header">
                        <h5 class="modal-title">Editar grupo</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <EditGroup :groupId="Number(group?.id)" @updated="fetchGroup" v-if="group" />

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.pointer:hover span {
    text-decoration: underline;
}
</style>
