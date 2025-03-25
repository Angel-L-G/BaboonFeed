<script setup lang="ts">
import type { User } from "@/types/User.ts";
import { onMounted, ref } from "vue";
import { API_URL } from "@/globals";
import { useRoute } from "vue-router";

const route = useRoute();
const username = route.params.username as string;

const user = ref<User | null>(null);
const loading = ref(true);
const error = ref<string | null>(null);

onMounted(async () => {
    try {
        const response = await fetch(`${API_URL}users/${username}`);
        if (!response.ok) throw new Error("Error al cargar el perfil");

        user.value = await response.json();
    } catch (err) {
        error.value = (err as Error).message;
    } finally {
        loading.value = false;
    }
});
</script>

<template>
    <div class="container profile-container mt-4">
        <!-- Mensaje de carga -->
        <div v-if="loading" class="text-center">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
        </div>

        <!-- Mensaje de error -->
        <div v-else-if="error" class="alert alert-danger text-center">
            {{ error }}
        </div>

        <!-- Perfil de usuario -->
        <div v-else-if="user" class="card profile-card bg-dark text-light">
            <div class="row g-0">
                <!-- Imagen de perfil -->
                <div class="col-md-4 d-flex align-items-center justify-content-center p-3">
                    <img
                        :src="user.file?.name || '/default-profile.png'"
                        class="rounded-circle img-fluid profile-img border-2 border-cyan"
                        alt="Profile Picture"
                    />
                </div>

                <!-- Información del usuario -->
                <div class="col-md-8">
                    <div class="card-body d-flex align-items-center justify-content-between gap-4">
                        <!-- Nombre de usuario más grande -->
                        <h1 class="card-title mb-2 fw-bold fs-1 text-center">{{ user.username }}</h1>

                        <!-- Sección de seguidores mejorada -->
                        <div class="d-flex gap-2 align-items-end">
                            <!-- Badge de Followers -->
                            <div class="badge badge-hover text-center">
                                <div class="d-flex align-items-center gap-1 mb-2">
                                    <font-awesome-icon :icon="['fas', 'users']" class="fs-6" />
                                    <span class="fs-6 fw-bold">{{ user.followers }}</span>
                                </div>
                                <span class="badge-text ">Followers</span>
                            </div>

                            <!-- Badge de Following -->
                            <div class="badge badge-hover text-center">
                                <div class="d-flex align-items-center gap-1 mb-2">
                                    <font-awesome-icon :icon="['fas', 'user-plus']" class="fs-6" />
                                    <span class="fs-6 fw-bold">{{ user.follows }}</span>
                                </div>
                                <span class="badge-text">Following</span>
                            </div>
                        </div>
                    </div>

                    <p class="card-text bio-text mt-3 bg-dark-light border-3 border-start border-cyan rounded ps-1 pt-2 me-3 text-gold-light">
                        {{ user.bio || "Este usuario aún no tiene una biografía." }}
                    </p>
                </div>
            </div>

            <div>
                <!-- Add posts here -->
            </div>
        </div>
    </div>
</template>

<style scoped>
.profile-container {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 35px;
    max-width: 800px;
    width: 100%;
}

.profile-card {
    border-radius: 15px;
    overflow: hidden;
}

.profile-img {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border: 4px solid white;
}

.bio-text {
    max-height: 80px;
    min-height: 80px;
    overflow: auto;
    font-size: 1rem;
    line-height: 1.4;
    padding-right: 5px;
}

.bio-text::-webkit-scrollbar {
    display: none;
}

.bio-text {
    scrollbar-width: none;
}

.card-body {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 4rem;
    padding: 10px 10px 0 0;
}

.badge-text {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.8);
}

</style>
