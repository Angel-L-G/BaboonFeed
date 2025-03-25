<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 bg-primary" style="width: 22rem;">
            <h3 class="text-center text-secondary-alt">Register</h3>
            <form @submit.prevent="handleRegister">
                <div class="mb-3">
                    <label for="username" class="form-label text-secondary-alt">Username</label>
                    <input type="text" id="username" class="form-control bg-primary-subtle" v-model="username" required />
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label text-secondary-alt">Email</label>
                    <input type="email" id="email" class="form-control bg-primary-subtle" v-model="email" required />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label text-secondary-alt">Password</label>
                    <input type="password" id="password" class="form-control bg-primary-subtle" v-model="password" required />
                </div>
                <div class="mb-3">
                    <label for="confPassword" class="form-label text-secondary-alt">Confirm Password</label>
                    <input type="password" id="confPassword" class="form-control bg-primary-subtle" v-model="confPassword" required />
                </div>
                <button type="submit" class="btn btn-primary-alt w-100 mb-3">Register</button>
                <router-link :to="{ name: 'login' }" class="btn btn-primary-alt w-100">Go to Login</router-link>
            </form>
            <p v-if="errorMsg" class="text-danger mt-2">{{ errorMsg }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useAuthStore } from '@/stores/auth.ts';
import { useRouter } from 'vue-router'
import axios from 'axios'
import { API_URL } from '@/globals.ts'

const authStore = useAuthStore();
const router = useRouter();

const username = ref('');
const email = ref('');
const password = ref('');
const confPassword = ref('');
const errorMsg = ref('');

const handleRegister = async () => {
    if (password.value !== confPassword.value) {
        errorMsg.value = 'Las contraseñas no coinciden';
        password.value = '';
        confPassword.value = '';
        return;
    }
    try {
        const responsePromise = await axios.post(
            `${API_URL}api/register/`,
            {
                username: username.value,
                email: email.value,
                password: password.value,
                confirmPassword: confPassword.value
            }
        );
        const data = responsePromise.data;
        if (data.access) {
            authStore.token = data.access;
            localStorage.setItem('token', data.access);
            errorMsg.value = '';
            await router.push("/home/");
        } else {
            console.log("No token received");
            errorMsg.value = 'Error al registrar';
            username.value = '';
            email.value = '';
            password.value = '';
            confPassword.value = '';
        }
    } catch (error) {
        console.error('Error:', error);
        errorMsg.value = 'Error al registrar';
        username.value = '';
        email.value = '';
        password.value = '';
        confPassword.value = '';
    }
};
</script>
