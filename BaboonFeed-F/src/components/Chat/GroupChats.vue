<script setup lang="ts">
import {onMounted, reactive} from "vue";
import type {User} from "@/types/User.ts";
import {API_URL} from "@/globals.ts";

const users = reactive<User[]>([]);

onMounted( async () => {
    await fetch(`${API_URL}users`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    }).then(async (response) => {
        const data = await response.json();
        users.push(...data);
        console.log(users);
    }).catch((error) => {
        console.log(error);
    })
})
</script>

<template>
    <div id="groups">
        <h2 class="w-100 text-center text-primary">
            <font-awesome-icon :icon="['fas', 'people-group']" />
            <span class="m-2 d-md-none d-lg-inline">Groups</span>
        </h2>
        <div v-for="user in users" :key="user.id" class="d-flex align-items-center justify-content-center rounded-top text-primary p-2">
            <img class="me-3 rounded-circle border-3" :src="user.avatar" :alt="user.username" style="height: 35px; width: 35px;">
            <h2>
                {{ user.username }}
            </h2>
        </div>
    </div>
</template>

<style scoped>

</style>
