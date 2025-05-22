<template>
    <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
        <h2 class="text-center">Create Group</h2>

        <!-- Vista previa del avatar -->
        <div class="text-center mb-3" v-if="previewAvatarUrl">
            <img
                :src="previewAvatarUrl"
                alt="Avatar del grupo"
                class="rounded-circle border border-2"
                style="width: 100px; height: 100px; object-fit: cover"
            />
        </div>

        <!-- Nombre -->
        <input
            v-model="group.name"
            class="form-control mt-3 bg-primary-subtle"
            placeholder="Group's name"
            required
        />

        <!-- Selector de imagen -->
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

        <!-- Buscar usuarios -->
        <input
            v-model="search"
            class="form-control bg-primary-subtle mb-2"
            placeholder="Search users"
        />
        <ul v-if="searchResults.length" class="list-group mb-2">
            <li
                v-for="user in searchResults"
                :key="user.username"
                class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                @click="selectUser(user)"
            >
                <img :src="user.avatar" class="rounded-circle me-2" width="30" height="30" />
                <span>{{ user.username }}</span>
            </li>
        </ul>

        <!-- Lista de usuarios seleccionados -->
        <div class="mb-3">
            <span v-if="group.users.length === 0" class="text-light-dark">No users selected</span>
            <div
                v-for="user in group.users"
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

        <button type="submit" class="btn btn-purple-alt text-light w-100">Create</button>
    </form>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import { API_URL } from '@/globals'
import { useAuthStore } from '@/stores/auth.ts'
import { useUsers } from '@/composables/useUsers.ts'
import type { PublicUserDto } from '@/dtos/PublicUserDto.ts'



const emit = defineEmits<{
    (e: 'submit', data: { name: string; avatar: File | null; members: string[] }): void
}>()

const fileInput = ref<HTMLInputElement | null>(null)
const group = ref({
    name: '',
    avatar: null as File | null,
    users: [] as PublicUserDto[],
})
const previewAvatarUrl = ref<string | null>(null)

const search = ref('')
const searchResults = ref<PublicUserDto[]>([])
const users = useUsers()

watch(search, async (value) => {
    if (value.length < 1) return (searchResults.value = [])
    searchResults.value = (await users).value.filter(user => user.username.toLowerCase().includes(value.toLowerCase()))
})

const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement
    const files = target.files
    if (files && files[0]) {
        group.value.avatar = files[0]
        previewAvatarUrl.value = URL.createObjectURL(files[0])
    }
}

const removeFile = () => {
    group.value.avatar = null
    previewAvatarUrl.value = null
    if (fileInput.value) fileInput.value.value = ''
}

const selectUser = (user: PublicUserDto) => {
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
