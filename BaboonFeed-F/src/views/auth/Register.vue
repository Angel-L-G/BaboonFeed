<template>
    <div class="container d-flex justify-content-center align-items-center vh-100 position-absolute top-50 start-50 translate-middle">
        <div class="card p-4 bg-primary" style="width: 22rem;" role="form"
             aria-label="Formulario de registro de usuario">
            <h1 class="text-center text-secondary-alt fs-3">Registro</h1>

            <form @submit.prevent="handleRegister" novalidate>
                <div class="mb-3">
                    <label for="name" class="form-label text-secondary-alt">Nombre</label>
                    <input type="text" id="name" class="form-control bg-primary-subtle"
                        v-model="name" required autocomplete="name" aria-required="true"
                        :aria-invalid="!!error" :aria-describedby="error ? 'register-error' : null"
                        autofocus/>
                </div>

                <div class="mb-3">
                    <label for="email" class="form-label text-secondary-alt">Email</label>
                    <input type="email" id="email" class="form-control bg-primary-subtle"
                        v-model="email" required autocomplete="email" aria-required="true"
                        :aria-invalid="!!error" :aria-describedby="error ? 'register-error' : null"/>
                </div>

                <div class="mb-3">
                    <label for="password" class="form-label text-secondary-alt">Contraseña</label>
                    <input type="password" id="password" class="form-control bg-primary-subtle"
                        v-model="password" required autocomplete="new-password" aria-required="true"
                        :aria-invalid="!!error" :aria-describedby="error ? 'register-error' : null"/>
                </div>

                <button type="submit" class="btn btn-primary-alt w-100">Registrarse</button>
            </form>

            <p v-if="error" id="register-error" class="text-danger mt-2" role="alert" aria-live="assertive">
                {{ error }}
            </p>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();

const name = ref('');
const email = ref('');
const password = ref('');
const error = ref('');

const handleRegister = () => {
    if (name.value && email.value && password.value) {
        error.value = '';
        router.push('/home/');
    } else {
        error.value = 'Por favor, complete todos los campos';
    }
};
</script>
