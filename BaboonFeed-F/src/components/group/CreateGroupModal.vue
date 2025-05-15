<script setup lang="ts">
import { ref, watch } from 'vue'
import axios from 'axios'
import { API_URL } from '@/globals.ts'

interface SelectedUser {
    username: string
    avatar_url: string
}

const emit = defineEmits<{
    (e: 'submit', data: { name: string; avatar: File | null; users: string[] }): void
    (e: 'close'): void
}>()

const groupData = ref({
    name: '',
    avatar: null as File | null,
    users: [] as SelectedUser[],
})

const search = ref('')
const searchResults = ref<SelectedUser[]>([])
const isSearching = ref(false)

watch(search, async (value) => {
    if (value.length < 2) {
        searchResults.value = []
        return
    }

    isSearching.value = true
    try {
        const response = await axios.get(`${API_URL}users/search/?q=${value}`)
        searchResults.value = response.data
    } catch (error) {
        console.error('Error buscando usuarios:', error)
    } finally {
        isSearching.value = false
    }
})

function handleFileChange(event: Event) {
    const target = event.target as HTMLInputElement
    if (target.files && target.files.length > 0) {
        groupData.value.avatar = target.files[0]
    }
}

function selectUser(user: SelectedUser) {
    const alreadySelected = groupData.value.users.some((u) => u.username === user.username)
    if (!alreadySelected) {
        groupData.value.users.push(user)
    }
    search.value = ''
    searchResults.value = []
}

function removeUser(username: string) {
    groupData.value.users = groupData.value.users.filter((u) => u.username !== username)
}

function handleSubmit() {
    emit('submit', {
        name: groupData.value.name,
        avatar: groupData.value.avatar,
        users: groupData.value.users.map((u) => u.username),
    })
}
</script>

<template>
    <div class="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50">
        <div class="bg-white p-6 rounded-lg w-full max-w-md shadow-lg">
            <h3 class="text-xl font-semibold mb-4">Crear Nuevo Grupo</h3>
            <form @submit.prevent="handleSubmit">
                <div class="mb-4">
                    <label class="block text-sm font-medium">Nombre del grupo</label>
                    <input v-model="groupData.name" type="text" class="w-full border rounded px-3 py-2" required />
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium">Avatar</label>
                    <input type="file" accept="image/*" @change="handleFileChange" />
                </div>

                <div class="mb-4">
                    <label class="block text-sm font-medium mb-1">Buscar usuarios</label>
                    <input
                        type="text"
                        v-model="search"
                        placeholder="Buscar por nombre"
                        class="w-full border rounded px-3 py-2 mb-2"
                    />
                    <ul v-if="searchResults.length" class="border rounded p-2 max-h-40 overflow-y-auto mb-2 bg-white shadow">
                        <li
                            v-for="user in searchResults"
                            :key="user.username"
                            class="flex items-center gap-2 py-1 cursor-pointer hover:bg-gray-100 px-2"
                            @click="selectUser(user)"
                        >
                            <img :src="user.avatar_url" class="w-6 h-6 rounded-full object-cover" />
                            <span>{{ user.username }}</span>
                        </li>
                    </ul>
                    <div class="flex flex-wrap gap-2 mt-2">
                        <div
                            v-for="user in groupData.users"
                            :key="user.username"
                            class="flex items-center gap-2 bg-gray-100 rounded-full px-3 py-1 text-sm"
                        >
                            <img :src="user.avatar_url" class="w-5 h-5 rounded-full" />
                            {{ user.username }}
                            <button @click.prevent="removeUser(user.username)" class="ml-1 text-red-600 font-bold">×</button>
                        </div>
                    </div>
                </div>

                <div class="flex justify-end gap-2 mt-4">
                    <button type="button" @click="$emit('close')" class="px-4 py-2 border rounded">
                        Cancelar
                    </button>
                    <button type="submit" class="bg-blue-600 text-white px-4 py-2 rounded">
                        Crear
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>
