import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import type { User } from '@/types/User.ts'
import { useChatStore } from '@/stores/chatStore.ts'

export const useAuthStore = defineStore('auth', () => {
    const token = ref<string | null>(localStorage.getItem('token') || null)
    const user = ref<User | null>(localStorage.getItem('user') ? JSON.parse(localStorage.getItem('user')!) : null)

    const isAuthenticated = computed(() => !!token.value)

    function logout() {
        token.value = null
        localStorage.removeItem('token')
        user.value = null
        localStorage.removeItem('user')
        useChatStore().disconnectAllChats()
    }

    return { token, user, isAuthenticated, logout }
})
