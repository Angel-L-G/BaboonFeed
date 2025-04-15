<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 bg-secondary-alt border-primary" style="width: 22rem">
            <h3 class="text-center text-primary">Login</h3>
            <form @submit.prevent="handleLogin">
                <div class="mb-3">
                    <label for="username" class="form-label text-primary">Username</label>
                    <input type="text" id="username" class="form-control bg-primary-subtle" v-model="username" required />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label text-primary">Password</label>
                    <input type="password" id="password" class="form-control bg-primary-subtle" v-model="password" required />
                </div>
                <button type="submit" class="btn btn-purple w-100 mb-3">Login</button>
                <router-link :to="{ name: 'register' }" class="btn btn-purple-alt w-100">Go to Register</router-link>
            </form>
            <p v-if="errorMsg" class="text-danger mt-2">{{ errorMsg }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth.ts';
import { useRouter } from 'vue-router'
import axios from 'axios'
import { API_URL } from '@/globals.ts'

const authStore = useAuthStore();
const router = useRouter();

const username = ref('');
const password = ref('');
const errorMsg = ref('');

const handleLogin = async () => {
    try {
        const responsePromise = await axios.post(
            `${API_URL}login/`,
            { username: username.value,  password: password.value }
        );
        const data = responsePromise.data;
        if (data.access) {
            authStore.token = data.access;
            authStore.user = data.user;
            localStorage.setItem('token', data.access);
            localStorage.setItem('user', JSON.stringify(data.user));
            errorMsg.value = '';
            await router.push("/home/");
        } else {
            console.log("No token received");
            errorMsg.value = 'Credenciales incorrectas';
            username.value = '';
            password.value = '';
        }
    } catch (error) {
        console.error('Error:', error);
        errorMsg.value = 'Credenciales incorrectas';
        username.value = '';
        password.value = '';
    }
};
</script>
