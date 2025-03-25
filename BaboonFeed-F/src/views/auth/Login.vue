<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 bg-primary" style="width: 22rem;">
            <h3 class="text-center">Login</h3>
            <form @submit.prevent="handleLogin">
                <div class="mb-3">
                    <label for="username" class="form-label text-secondary-alt">Username</label>
                    <input type="text" id="username" class="form-control bg-primary-subtle" v-model="username" required />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label text-secondary-alt">Contraseña</label>
                    <input type="password" id="password" class="form-control bg-primary-subtle" v-model="password" required />
                </div>
                <button type="submit" class="btn btn-primary-alt w-100">Ingresar</button>
            </form>
            <p v-if="error" class="text-danger mt-2">{{ error }}</p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const username = ref('');
const password = ref('');
const error = ref('');

const handleLogin = () => {
    if (username.value && password.value) {
        fetch(
            'http://localhost:8000/api/login/',
            {
                method: 'POST',
                body: JSON.stringify({
                    username: username.value,
                    password: password.value
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        )
        .then(response => response.json())
        .then(data => {
            if (data.access) {
                localStorage.setItem('token', data.access);
                router.push('/home/');
            } else {
                error.value = 'Credenciales incorrectas';
            }
        });
    } else {
        error.value = 'Credenciales incorrectas';
    }
};
</script>
