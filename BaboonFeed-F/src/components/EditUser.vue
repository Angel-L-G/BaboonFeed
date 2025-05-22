<template>
    <div class="container my-2" role="form" aria-label="Edit User Form">
        <form @submit.prevent="handleSubmit" aria-labelledby="edit-user-title">
            <!-- Imagen del usuario -->
            <div class="text-center mb-3">
                <img
                    v-if="displayedAvatar"
                    :src="displayedAvatar"
                    alt="Avatar del usuario"
                    class="rounded-circle border border-2"
                    style="width: 100px; height: 100px; object-fit: cover"
                />
            </div>

            <!-- Bio -->
            <div class="mt-3">
                <label for="editBio" class="form-label visually-hidden">Edit Bio</label>
                <textarea
                    id="editBio"
                    class="form-control bg-primary-subtle"
                    v-model="bio"
                    rows="4"
                    required
                    aria-required="true"
                    placeholder="Write your bio here"
                />
            </div>

            <!-- Avatar input -->
            <div class="input-group mb-3 mt-3">
                <label for="file" class="input-group-text bg-secondary text-light">Avatar</label>
                <input
                    id="file"
                    class="form-control bg-primary-subtle"
                    type="file"
                    ref="fileInput"
                    @change="handleFileChange"
                    aria-describedby="fileHelp"
                />
                <button
                    class="btn btn-purple-alt"
                    type="button"
                    @click="removeFile"
                    aria-label="Remove file"
                >
                    <font-awesome-icon :icon="['far', 'trash-can']" />
                </button>
            </div>

            <div id="fileHelp" class="form-text text-light-dark">
                Formats allowed: jpeg, jpg, png.
            </div>

            <!-- Botón -->
            <button
                class="btn btn-purple-alt text-light w-100 mt-2"
                type="submit"
                data-bs-dismiss="modal"
            >
                Edit Profile
            </button>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue';
import axios from 'axios';
import { API_URL } from '@/globals.ts';
import { useAuthStore } from '@/stores/auth.ts';

const authStore = useAuthStore();
const file = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const bio = ref(authStore.user?.bio || '');
const originalBio = ref(authStore.user?.bio || '');
const originalAvatarUrl = ref<string>(authStore.user?.avatar || '');
const previewAvatarUrl = ref<string | null>(null);

const { username } = defineProps<{ username: string }>();

const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const selected = target.files?.[0];
    if (selected) {
        file.value = selected;
        previewAvatarUrl.value = URL.createObjectURL(selected);
    }
};

const removeFile = () => {
    file.value = null;
    previewAvatarUrl.value = null;
    if (fileInput.value) fileInput.value.value = '';
};

const displayedAvatar = computed(() => previewAvatarUrl.value || originalAvatarUrl.value);

const handleSubmit = async () => {
    const formData = new FormData();
    const changedBio = bio.value !== originalBio.value;
    const changedAvatar = !!file.value;

    if (!changedBio && !changedAvatar) {
        alert('No changes made to bio or avatar');
        return;
    }

    formData.append("bio", bio.value);
    if (changedAvatar && file.value) {
        formData.append("avatar", file.value);
    }

    try {
        const response = await axios.put(`${API_URL}users/${username}/`, formData, {
            headers: {
                Authorization: 'Bearer ' + authStore.token,
                'Content-Type': 'multipart/form-data'
            }
        });

        if (changedBio) authStore.user!.bio = response.data.bio;
        if (changedAvatar) authStore.user!.avatar = response.data.avatar;
        localStorage.setItem('user', JSON.stringify(authStore.user));

        if (changedAvatar) location.reload();
    } catch (error) {
        console.error('Error updating user:', error);
    }
};
</script>
