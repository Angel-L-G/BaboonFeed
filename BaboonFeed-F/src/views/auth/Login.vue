<template>
    <div class="container d-flex justify-content-center align-items-center vh-100 position-absolute top-50 start-50 translate-middle">
        <div class="card p-4 bg-primary" style="width: 22rem;"
             role="form" aria-label="Formulario de inicio de sesión">
            <h3 class="text-center">Login</h3>
            <form @submit.prevent="handleLogin">
                <div class="mb-3">
                    <label for="username" class="form-label text-secondary-alt">Username</label>
                    <input type="text" id="username" class="form-control bg-primary-subtle"
                           v-model="username" required autocomplete="username" aria-required="true"
                           :aria-invalid="!!error" :aria-describedby="error ? 'login-error' : null"
                           autofocus/>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label text-secondary-alt">Contraseña</label>
                    <input type="password" id="password" class="form-control bg-primary-subtle"
                           v-model="password" required autocomplete="current-password" aria-required="true"
                           :aria-invalid="!!error" :aria-describedby="error ? 'login-error' : null"/>
                </div>
                <button type="submit" class="btn btn-primary-alt w-100">Ingresar</button>
            </form>
            <p v-if="error" class="text-danger mt-2" role="alert" aria-live="assertive">
                {{ error }}
            </p>
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
const error = ref('');

const handleLogin = () => {
    if (username.value && password.value) {
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
                router.push("/home/");
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
    }
};
</script>
