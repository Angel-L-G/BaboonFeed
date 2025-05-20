<template>
    <div class="container">
        <div class="row justify-content-center mt-5">
            <div class="col-12 col-md-6">
                <div class="mb-3">
                    <input type="text" class="form-control" placeholder="Buscar..." v-model="searchQuery"/>
                </div>

                <div v-if="searchQuery">
                    <p class="text-cyan">Searching for: "{{ searchQuery }}"</p>
                </div>

                <ul class="list-group">
                    <li class="list-group-item d-flex align-items-center gap-3" v-for="user in filteredUsers"
                        :key="user.username">
                        <img :src="user.avatar" alt="avatar" class="rounded-circle" width="40" height="40"/>
                        <span>{{ user.username }}</span>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { useUsers } from '@/composables/useUsers.ts'
import type { PublicUserDto } from '@/dtos/PublicUserDto.ts'

const searchQuery = ref('')
const users = useUsers();
const filteredUsers = ref<PublicUserDto[]>([]);

watch(searchQuery, async (newQuery) => {
    if (!newQuery) {
        filteredUsers.value = [];
        return;
    }

    const query = newQuery.toLowerCase();
    filteredUsers.value = (await users).value.filter((user) =>
        user.username.toLowerCase().includes(query)
    );
});
</script>

<style scoped>
img {
    object-fit: cover;
}
</style>
