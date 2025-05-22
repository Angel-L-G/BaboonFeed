<script setup lang="ts">
import type { Group } from '@/types/Group.ts'
import { onMounted, ref } from 'vue'
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts'
import axios from 'axios'
import type { GroupDto } from '@/dtos/GroupDto.ts'
import CreateGroupModal from '@/components/group/CreateGroupModal.vue'
import { useRouter } from 'vue-router'
import { ChatType } from '@/types/Chat.ts'
import { useChatStore } from '@/stores/chatStore.ts'

const auth = useAuthStore()
const chatStore = useChatStore()
const groups = ref<Group[]>([])
const errorMsg = ref<string>('')
const showConfirmModal = ref(false)
const selectedGroup = ref<Group | null>(null)
const router = useRouter()

onMounted(async () => {
    await fetchGroups()
})

async function fetchGroups() {
    try {
        const response = await axios.get(`${API_URL}groups/`, {
            headers: { Authorization: `Bearer ${auth.token}` },
        })
        groups.value = response.data
    } catch (error) {
        console.log(error)
        errorMsg.value = 'Error fetching groups'
    }
}

async function createGroup(data: GroupDto) {
    const formData = new FormData()
    formData.append('name', data.name)
    if (data.avatar) formData.append('avatar', data.avatar)
    data.members.forEach((member: string) => formData.append('members', member))

    try {
        const response = await axios.post(`${API_URL}groups/`, formData, {
            headers: {
                Authorization: `Bearer ${auth.token}`,
                'Content-Type': 'multipart/form-data',
            },
        })
        groups.value.push(response.data)
        await chatStore.addGroup(response.data)
    } catch (error) {
        console.log(error)
        errorMsg.value = 'Error creating group'
    }
}

function goToChat(group: Group) {
    const chatId = `${ChatType.GROUP}_${group.id}`
    router.push(`/chat/${chatId}`)
}

function confirmLeave(group: Group) {
    selectedGroup.value = group
    showConfirmModal.value = true
}

async function leaveGroup() {
    if (!selectedGroup.value) return

    try {
        await axios.delete(`${API_URL}groups/${selectedGroup.value.id}/leave/`, {
            headers: { Authorization: `Bearer ${auth.token}` },
        })
        await chatStore.removeGroup(selectedGroup.value.id)
        groups.value = groups.value.filter(g => g.id !== selectedGroup.value?.id)
    } catch (error) {
        console.error('Error al salir del grupo:', error)
    } finally {
        showConfirmModal.value = false
        selectedGroup.value = null
    }
}
</script>

<template>
    <div class="p-4 group-container">
        <p v-if="errorMsg" class="text-danger mb-4">{{ errorMsg }}</p>

        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="fs-3 fw-bold">Your Groups</h2>
            <button
                class="btn btn-warning"
                data-bs-toggle="modal"
                data-bs-target="#CreateGroupModal"
            >
                Create Group
            </button>
        </div>

        <div class="d-grid gap-3">
            <div
                v-for="group in groups"
                :key="group.id"
                class="d-flex justify-content-between align-items-center p-3 bg-dark text-light rounded shadow-sm group-card"
                role="button"
                @click="goToChat(group)"
            >
                <div class="d-flex align-items-center gap-3">
                    <img :src="group.avatar_url" class="rounded-circle" width="48" height="48" />
                    <strong>{{ group.name }}</strong>
                </div>
                <button class="btn btn-danger btn-sm text-white" @click.stop="confirmLeave(group)">
                    Leave
                </button>
            </div>
        </div>

        <div
            class="modal fade"
            id="CreateGroupModal"
            tabindex="-1"
            aria-labelledby="CreateGroupModalLabel"
            aria-hidden="true"
        >
            <div class="modal-dialog">
                <div class="modal-content bg-secondary text-light p-3">
                    <CreateGroupModal @submit="createGroup" />
                </div>
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
                        <h5 class="modal-title">Are you sure you want to leave the group?</h5>
                        <button type="button" class="btn-close" @click="showConfirmModal = false"></button>
                    </div>
                    <div class="modal-body">
                        <p>You won't be able to send or receive messages from this group.</p>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-secondary" @click="showConfirmModal = false">Cancel</button>
                        <button class="btn btn-danger" @click="leaveGroup">Leave</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.group-container {
    max-width: 800px;
    margin-left: auto;
    margin-right: auto;
}

.group-card:hover {
    background-color: #1a1a1a;
    transition: background-color 0.2s;
    cursor: pointer;
}
</style>
