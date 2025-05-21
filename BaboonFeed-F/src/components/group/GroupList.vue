<script setup lang="ts">
import type { Group } from '@/types/Group.ts'
import { onMounted, ref } from 'vue'
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts'
import axios from 'axios'
import type { GroupDto } from '@/dtos/GroupDto.ts'
import CreateGroupModal from '@/components/group/CreateGroupModal.vue'
import GroupCard from '@/components/group/GroupCard.vue'

const auth = useAuthStore()
const groups = ref<Group[]>([])
const errorMsg = ref<string>('')

onMounted(async () => {
    await axios
        .get(`${API_URL}groups/`, {
            headers: { Authorization: `Bearer ${auth.token}` },
        })
        .then((response) => {
            groups.value = response.data
        })
        .catch((error) => {
            console.log(error)
            errorMsg.value = error
        })
})

async function createGroup(data: GroupDto) {
    const formData = new FormData()
    formData.append('name', data.name)
    if (data.avatar) formData.append('avatar', data.avatar)
    data.members.forEach((member: string) => formData.append('members', member))
    console.log(JSON.stringify(formData))
    await axios
        .post(`${API_URL}groups/`, formData, {
            headers: {
                Authorization: `Bearer ${auth.token}`,
                'Content-Type': 'multipart/form-data',
            },
        })
        .then((response) => {
            groups.value.push(response.data)
        })
        .catch((error) => {
            console.log(error)
            errorMsg.value = error.message || 'Something went wrong'
        })
}
</script>

<template>
    <div class="p-4">
        <p v-if="errorMsg" class="text-red-500 mb-4">{{ errorMsg }}</p>

        <div class="flex justify-between items-center mb-4">
            <h2 class="text-2xl font-bold">Tus Grupos</h2>
            <button
                class="btn btn-warning"
                data-bs-toggle="modal"
                data-bs-target="#CreateGroupModal"
            >
                Crear Grupo
            </button>
        </div>

        <div class="grid gap-4">
            <GroupCard v-for="group in groups" :key="group.id" :group="group" >
                {{ group.name }}
            </GroupCard>
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
    </div>
</template>

<style scoped></style>
