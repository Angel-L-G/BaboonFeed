<template>
    <div class="container-fluid">
        <h1 class="display-4 m-3 text-white">Home Page</h1>
        <div class="row justify-content-center">
            <div class="col-md-12 col-lg-9 me-2">
                <PostView v-for="post in posts" :key="post.id" :post="post"/>
            </div>
            <div class="d-none d-lg-flex flex-column rounded col-lg-2 align-items-center bg-primary-subtle mt-1">
                <h2 class="bg-info-subtle w-100 text-center rounded-bottom border border-top-0 border-3 border-info">Groups</h2>
                <div v-for="user in users" :key="user.id" class="d-flex align-items-center justify-content-center rounded-top p-2">
                    <img class="me-3 rounded-circle border-3" :src="user.file?.name" :alt="user.username" style="height: 35px; width: 35px;">
                    <h2>{{ user.username }}</h2>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
    import { reactive, onMounted } from 'vue';
    import type { Post } from '../types/Post';
    import type { User } from '../types/User';
    import { API_URL } from '@/globals';
    import PostView from './post/PostView.vue';

    const posts = reactive<Post[]>([]);
    const users = reactive<User[]>([]);

    onMounted( async () => {
        await fetch(`${API_URL}posts`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(async (response) => {
            const data = await response.json();
            posts.push(...data);
            console.log(posts);

        }).catch((error) => {
            console.log(error);
        })

        await fetch(`${API_URL}users`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(async (response) => {
            const data = await response.json();
            users.push(...data);
            console.log(users);
        }).catch((error) => {
            console.log(error);
        })

    })

</script>
