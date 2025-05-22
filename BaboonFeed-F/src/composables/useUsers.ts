import { ref } from 'vue'
import type { PublicUserDto } from '@/dtos/PublicUserDto.ts'
import axios from 'axios'
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts'

const authStore = useAuthStore();

export async function useUsers() {

    const users = ref<PublicUserDto[]>([]);

    try {
        const response = await axios.get(`${API_URL}users/`,
            {
            headers: {"Authorization": `Bearer ${authStore.token}`},
            })
        users.value = await response.data || [];
        users.value = users.value.filter(user => user.username !== authStore.user!.username);
    } catch (error) {
        console.error("Error obteniendo usuarios:" + error);
    }

    return users;
}
