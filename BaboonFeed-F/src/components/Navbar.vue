<template>
    <div class="navigation">
        <h3 class="d-flex justify-content-center align-items-center mt-3">
            <router-link :to="{ name: 'home' }" class="navbar-brand text-primary mb-3 fs-3">
                BaboonFeed
            </router-link>
        </h3>
        <ul class="list-group list-group-flush primary gap-2 d-flex justify-content-center align-items-center">
            <li class="text-primary list-group-item bg-dark-alt">
                <router-link :to="{ name: 'chat' }" class="nav-link text-primary fs-4" :class="{ active: route.path === '/chat/' }">
                    Chat
                </router-link>
            </li>
            <li class="text-light list-group-item bg-dark-alt">
                <router-link :to="{ name: 'profile', params: { username: '1' } }" class="nav-link text-primary fs-4" :class="{ active: route.path === '/users/profile/' }">
                    Profile
                </router-link>
            </li>
            <li class="text-light list-group-item bg-dark-alt ">
                <div type="button" data-bs-toggle="modal" data-bs-target="#exampleModal" class="text-primary fs-4">
                    New Post
                </div>
            </li>
            <li class="text-light list-group-item bg-dark-alt">
            </li>
        </ul>
    </div>

    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content bg-secondary">
                <CreatePost></CreatePost>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
import CreatePost from "@/components/post/CreatePost.vue";
const route = useRoute();


</script>

<style scoped>
    .navigation{
        justify-content: center;
        align-items: center;
        margin: 0;
        top: 0;
        left: 0;
        bottom: 0;
        position: fixed;
        width: inherit;
        height: inherit;
    }
</style>
