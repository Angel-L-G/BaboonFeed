// stores/layoutStore.ts
import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useLayoutStore = defineStore('layout', () => {
    const isNavbarExpanded = ref(false)

    const toggleNavbar = () => {
        isNavbarExpanded.value = !isNavbarExpanded.value
    }

    return {
        isNavbarExpanded,
        toggleNavbar,
    }
})
