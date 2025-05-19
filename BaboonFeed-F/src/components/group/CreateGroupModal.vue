<template>
    <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
        <h2 class="text-center">Crear Grupo</h2>
        <input
            v-model="group.name"
            class="form-control mt-3 bg-primary-subtle"
            placeholder="Nombre del grupo"
            required
        />

        <div class="input-group mt-3 mb-3">
            <input
                type="file"
                class="form-control bg-primary-subtle"
                @change="handleFileChange"
                ref="fileInput"
            />
            <button type="button" class="btn btn-purple-alt" @click="removeFile">
                <font-awesome-icon :icon="['far', 'trash-can']" />
            </button>
        </div>

        <input
            v-model="search"
            class="form-control bg-primary-subtle mb-2"
            placeholder="Buscar usuarios"
        />
        <ul v-if="searchResults.length" class="list-group mb-2">
            <li
                v-for="user in searchResults"
                :key="user.username"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                @click="selectUser(user)"
            >
                <img :src="user.avatar_url" class="rounded-circle me-2" width="30" height="30" />
                <span>{{ user.username }}</span>
            </li>
        </ul>

        <div class="mb-3">
            <span v-if="group.users.length === 0" class="text-muted"
                >No hay usuarios seleccionados</span
            >
            <div
                v-for="user in group.users"
                :key="user.username"
                class="badge bg-secondary me-2 d-inline-flex align-items-center"
            >
                <img :src="user.avatar_url" class="rounded-circle me-1" width="20" height="20" />
                {{ user.username }}
                <button
                    class="btn-close btn-close-white ms-2 btn-sm"
                    @click.prevent="removeUser(user.username)"
                ></button>
            </div>
        </div>

        <button type="submit" class="btn btn-purple-alt text-light w-100">Crear</button>
    </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import { API_URL } from '@/globals'
import { useAuthStore } from '@/stores/auth.ts'

const authStore = useAuthStore()

interface UserPreview {
    username: string
    avatar_url: string
}

const emit = defineEmits<{
    (e: 'submit', data: { name: string; avatar: File | null; members: string[] }): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const group = ref({
    name: '',
    avatar: null as File | null,
    users: [] as UserPreview[],
})

const search = ref('')
const searchResults = ref<UserPreview[]>([])

watch(search, async (value) => {
    if (value.length < 2) return (searchResults.value = [])
    const res = await axios.get(`${API_URL}users/?username=${value}`, {
        headers: {
            Authorization: `Bearer ${authStore.token}`,
        },
    })
    searchResults.value = res.data
})

const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    const files = target.files
    if (files) group.value.avatar = files[0]
}

const removeFile = () => {
    group.value.avatar = null
    if (fileInput.value) fileInput.value.value = ''
}

const selectUser = (user: UserPreview) => {
    if (!group.value.users.some((u) => u.username === user.username)) {
        group.value.users.push(user)
    }
    search.value = ''
    searchResults.value = []
}

const removeUser = (username: string) => {
    group.value.users = group.value.users.filter((u) => u.username !== username)
}

const handleSubmit = () => {
    const members = group.value.users.map((u) => u.username)
    emit('submit', {
        name: group.value.name,
        avatar: group.value.avatar,
        members: members,
    })
}
</script>
