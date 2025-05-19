<template>
    <div class="container my-2" role="form" aria-label="Create Post Form">
        <form @submit.prevent="handleSubmit" enctype="multipart/form-data" aria-labelledby="create-post-title">
            <div class="mt-3">
                <label for="postContent" class="form-label visually-hidden">Post Content</label>
                <textarea id="postContent" class="form-control bg-primary-subtle" v-model="content"
                    rows="4" required aria-required="true" placeholder="Write your post here"/>
            </div>

            <div class="input-group mb-3 mt-3">
                <label for="file" class="input-group-text bg-secondary text-light">File</label>
                <input id="file" class="form-control bg-primary-subtle" type="file" ref="fileInput"
                    @change="handleFileChange" aria-describedby="fileHelp"/>
                <button class="btn btn-purple-alt" type="button" @click="removeFile"
                    :aria-label="selectedFile ? 'Remove selected file' : 'No file to remove'">
                    <font-awesome-icon :icon="['far', 'trash-can']" />
                </button>
            </div>

            <div id="fileHelp" class="form-text text-light-dark">
                Hint: you can attach an image, video, or audio file.
            </div>

            <button class="btn btn-purple-alt text-light w-100 mt-2" type="submit">
                Create
            </button>

            <p v-if="error" class="text-danger mt-2" role="alert" aria-live="assertive">
                {{ error }}
            </p>
        </form>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type {PostCreate} from "@/types/Post.ts";
import { FileTypes } from "@/types/File.ts";
import axios from 'axios';
import { API_URL } from '@/globals.ts'
import { useAuthStore } from '@/stores/auth.ts';

const content = ref('');
const file = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);
const authStore = useAuthStore();

const handleFileChange = (e: Event) => {
    const target = e.target as HTMLInputElement;
    const files = target.files;
    if (files) {
        file.value = files[0];
    }
};

const removeFile = () => {
    file.value = null;
    if (fileInput.value) {
        fileInput.value.value = "";
    }
};

const handleSubmit = async () => {
    const createPost: PostCreate = {
        content: content.value,
        file: undefined
    };
    if (file.value) {
        createPost.file = {
            file: file.value.name.split(".").pop() || "",
            type: file.value.type.split("/").shift() as FileTypes || FileTypes.IMAGE
        };
    }
    console.log("AAAAAAAAAAAAAAAAAAAAAAA", createPost);
    try {
        const response = await axios.post(`${API_URL}posts/`, createPost, {
            headers: {
                'Content-Type': 'multipart/form-data',
                'Authorization': 'Bearer ' + authStore.token
            }
        });
        console.log(response.data);
    } catch (error) {
        console.error('Error creating post:', error);
    }
};
</script>
