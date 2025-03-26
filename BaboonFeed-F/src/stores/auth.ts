import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const token = ref<string | null>(localStorage.getItem('token') || null)

    const isAuthenticated = computed(() => !!token.value)

    function logout() {
        token.value = null
        localStorage.removeItem('token')
    }

    return { token, isAuthenticated, logout }
})
