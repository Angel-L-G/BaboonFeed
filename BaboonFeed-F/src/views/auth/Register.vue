<template>
    <div class="container d-flex justify-content-center align-items-center vh-100 position-absolute top-50 start-50 translate-middle">
        <div class="card p-4 bg-primary" style="width: 22rem;" role="form"
             aria-label="Formulario de registro de usuario">
            <h1 class="text-center text-secondary-alt fs-3">Register</h1>

            <form @submit.prevent="handleRegister" novalidate>
                <div class="mb-3">
                    <label for="username" class="form-label text-secondary-alt">Username</label>
                    <input type="text" id="username" class="form-control bg-primary-subtle"
                           v-model="username" required autocomplete="username" aria-required="true"
                           :aria-invalid="!!errorMsg" :aria-describedby="errorMsg ? 'register-error' : '' "
                           autofocus/>
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label text-secondary-alt">Email</label>
                    <input type="email" id="email" class="form-control bg-primary-subtle"
                           v-model="email" required autocomplete="email" aria-required="true"
                           :aria-invalid="!!errorMsg" :aria-describedby="errorMsg ? 'register-error' : '' "/>
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label text-secondary-alt">Password</label>
                    <input type="password" id="password" class="form-control bg-primary-subtle"
                           v-model="password" required autocomplete="new-password" aria-required="true"
                           :aria-invalid="!!errorMsg" :aria-describedby="errorMsg ? 'register-error' : '' "/>
                </div>

                <div class="mb-3">
                    <label for="confPassword" class="form-label text-secondary-alt">Confirm Password</label>
                    <input type="password" id="confPassword" class="form-control bg-primary-subtle"
                           v-model="confPassword" required autocomplete="confirm-new-password" aria-required="true"
                           :aria-invalid="!!errorMsg" :aria-describedby="errorMsg ? 'register-error' : '' "/>
                </div>

                <button type="submit" class="btn btn-primary-alt w-100">Register</button>
            </form>

            <!-- Enlace a registro -->
            <div class="text-center mt-3">
                <router-link to="/login" class="text-purple" aria-label="Go to registration page">
                    Already have an account? <strong>Login</strong>
                </router-link>
            </div>

            <!-- Parrafo para mostrar errores -->
            <p v-if="errorMsg" id="register-error" class="text-danger mt-2" role="alert" aria-live="assertive">
                {{ errorMsg }}
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import axios from 'axios'
import { API_URL } from '@/globals.ts'

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
            `${API_URL}register/`,
            {
                username: username.value,
                email: email.value,
                password: password.value,
                confirmPassword: confPassword.value
            }
        );
        const data = responsePromise.data;
        if (data) {
            errorMsg.value = 'Please check your email to confirm your account and then login';
        } else {
            console.log("No data received");
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
