<template>
    <div class="container mt-5">
        <div class="row">
            <h1 class="">Create Post</h1>
            <form @submit.prevent="handleSubmit" enctype="multipart/form-data">
                <input class="form-control mt-3 bg-primary-subtle" type="text" v-model="content" />
                <div class="input-group mb-3 mt-3">
                    <input class="form-control bg-primary-subtle" type="file" ref="fileInput" @change="handleFileChange" id="file">
                    <button class="btn btn-warning" type="button" @click="removeFile"><font-awesome-icon :icon="['far', 'trash-can']" /></button>
                </div>
                <button class="btn btn-primary text-light" type="submit">Create</button>
            </form>
        </div>
    </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import type {PostCreate} from "@/types/Post.ts";
import { FileTypes } from "@/types/File.ts";

const content = ref('');
const file = ref<File | null>(null);
const fileInput = ref<HTMLInputElement | null>(null);

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

const handleSubmit = () => {
    let createPost: PostCreate = {
        content: content.value,
        file: undefined
    };
    if (file.value) {
        createPost.file = {
            name: file.value.name.split(".").pop() || "",
            type: file.value.type.split("/").shift() as FileTypes || FileTypes.IMAGE
        };
    }
    console.log(createPost);
    /*
    Cuando el server funcione
    fetch('/api/posts/add/', { method: 'POST', body: createPost })
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error(error));
        */
};
</script>
