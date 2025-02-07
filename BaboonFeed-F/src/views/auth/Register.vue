<template>
    <div class="container d-flex justify-content-center align-items-center vh-100">
        <div class="card p-4 bg-warning-subtle" style="width: 22rem;">
            <h3 class="text-center">Registro</h3>
            <form @submit.prevent="handleRegister">
                <div class="mb-3">
                    <label for="name" class="form-label">Nombre</label>
                    <input type="text" id="name" class="form-control bg-primary-subtle" v-model="name" required />
                </div>
                <div class="mb-3">
                    <label for="email" class="form-label">Email</label>
                    <input type="email" id="email" class="form-control bg-primary-subtle" v-model="email" required />
                </div>
                <div class="mb-3">
                    <label for="password" class="form-label">Contraseña</label>
                    <input type="password" id="password" class="form-control bg-primary-subtle" v-model="password" required />
                </div>
                <button type="submit" class="btn btn-primary w-100">Registrarse</button>
            </form>
            <p v-if="error" class="text-danger mt-2">{{ error }}</p>
            <p v-if="success" class="text-success mt-2">{{ success }}</p>
        </div>
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    setup() {
        const name = ref('');
        const email = ref('');
        const password = ref('');
        const error = ref('');
        const success = ref('');

        const handleRegister = () => {
            if (name.value && email.value && password.value) {
                success.value = 'Registro exitoso';
                error.value = '';
            } else {
                error.value = 'Por favor, complete todos los campos';
                success.value = '';
            }
        };

        return {
            name,
            email,
            password,
            error,
            success,
            handleRegister
        };
    }
};
</script>
