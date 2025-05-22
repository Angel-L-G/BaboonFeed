<script setup lang="ts">
import { ref, onMounted, watch, computed } from 'vue'
import axios from 'axios'
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts'
import type { PublicUserDto } from '@/dtos/PublicUserDto.ts'
import { useChatStore } from '@/stores/chatStore.ts'

const props = defineProps<{ groupId: number }>()
const emit = defineEmits<{ (e: 'updated'): void }>()

const auth = useAuthStore()
const name = ref('')
const avatar = ref<File | null>(null)
const originalAvatarUrl = ref<string>('')
const previewAvatarUrl = ref<string | null>(null)
const fileInput = ref<HTMLInputElement | null>(null)
const selectedUsers = ref<PublicUserDto[]>([])
const search = ref('')
const searchResults = ref<PublicUserDto[]>([])

onMounted(async () => {
    try {
        const res = await axios.get(`${API_URL}groups/${props.groupId}/`, {
            headers: { Authorization: `Bearer ${auth.token}` },
        })
        name.value = res.data.name
        selectedUsers.value = res.data.members
        originalAvatarUrl.value = res.data.avatar_url
    } catch (err) {
        console.error('Error loading group data', err)
    }
})

watch(search, async (value) => {
    if (value.length < 1) return (searchResults.value = [])
    try {
        const res = await axios.get(`${API_URL}users/?username=${value}`, {
            headers: { Authorization: `Bearer ${auth.token}` },
        })
        searchResults.value = res.data
    } catch (err) {
        console.error('Error fetching users', err)
    }
})

const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    const file = target.files?.[0]
    if (file) {
        avatar.value = file
        previewAvatarUrl.value = URL.createObjectURL(file)
    }
}

const removeFile = () => {
    avatar.value = null
    previewAvatarUrl.value = null
    if (fileInput.value) fileInput.value.value = ''
}

const selectUser = (user: PublicUserDto) => {
    if (!selectedUsers.value.some((u) => u.username === user.username)) {
        selectedUsers.value.push(user)
    }
    search.value = ''
    searchResults.value = []
}

const removeUser = (username: string) => {
    selectedUsers.value = selectedUsers.value.filter((u) => u.username !== username)
}

const handleSubmit = async () => {
    const formData = new FormData()
    formData.append('name', name.value)
    selectedUsers.value.forEach((u) => formData.append('members', u.username))
    if (avatar.value) formData.append('avatar', avatar.value)

    try {
        const response = await axios.put(`${API_URL}groups/${props.groupId}/`, formData, {
            headers: {
                Authorization: `Bearer ${auth.token}`,
                'Content-Type': 'multipart/form-data',
            },
        })
        await useChatStore().updateGroup(response.data)
        emit('updated')
    } catch (err) {
        console.error('Error updating group', err)
    }
}

const displayedAvatar = computed(() => previewAvatarUrl.value || originalAvatarUrl.value)
</script>

<template>
    <form @submit.prevent="handleSubmit">
        <div class="text-center mb-3">
            <img
                v-if="displayedAvatar"
                :src="displayedAvatar"
                alt="Avatar del grupo"
                class="rounded-circle border border-2"
                style="width: 100px; height: 100px; object-fit: cover"
            />
        </div>

        <div class="mb-3">
            <label class="form-label">Nombre del grupo</label>
            <input v-model="name" type="text" class="form-control bg-primary-subtle" required />
        </div>

        <div class="mb-3">
            <label class="form-label">Avatar</label>
            <input type="file" class="form-control bg-primary-subtle" @change="handleFileChange" ref="fileInput" />
            <button type="button" class="btn btn-sm btn-danger mt-1" @click="removeFile">Quitar archivo</button>
        </div>

        <div class="mb-3">
            <input
                v-model="search"
                type="text"
                class="form-control bg-primary-subtle"
                placeholder="Buscar usuarios por nombre"
            />
            <ul v-if="searchResults.length" class="list-group mt-2">
                <li
                    v-for="user in searchResults"
                    :key="user.username"
                    class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                    @click="selectUser(user)"
                    style="cursor: pointer"
                >
                    <img :src="user.avatar" class="rounded-circle me-2" width="30" height="30" />
                    <span>{{ user.username }}</span>
                </li>
            </ul>
        </div>

        <div class="mb-3">
            <span v-if="selectedUsers.length === 0" class="text-muted">No hay usuarios seleccionados</span>
            <div
                v-for="user in selectedUsers"
                :key="user.username"
                class="badge bg-secondary me-2 d-inline-flex align-items-center"
            >
                <img :src="user.avatar" class="rounded-circle me-1" width="20" height="20" />
                {{ user.username }}
                <button
                    class="btn-close btn-close-white ms-2 btn-sm"
                    @click.prevent="removeUser(user.username)"
                ></button>
            </div>
        </div>

        <button class="btn btn-purple-alt text-light w-100" type="submit" data-bs-dismiss="modal">
            Update
        </button>
    </form>
</template>
