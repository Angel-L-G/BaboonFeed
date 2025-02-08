<template>
    <header>
        <nav class="navbar navbar-expand-lg bg-primary">
            <div class="container-fluid">
                <router-link :to="{ name: 'home' }" class="navbar-brand text-light">Home</router-link>
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
                        aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
                        <span class="navbar-toggler-icon"></span>
                    </button>
                    <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                        <div class="navbar-nav">
                            <router-link :to="{ name: 'createPost' }" class="nav-link text-light" :class="{ active: route.path === '/posts/add/' }">Create Post</router-link>
                            <router-link :to="{ name: 'chat' }" class="nav-link text-light" :class="{ active: route.path === '/chat/' }">Chat</router-link>
                            <router-link :to="{ name: 'profile' }" class="nav-link text-light" :class="{ active: route.path === '/users/profile/' }">Profile</router-link>
                            <router-link :to="{ name: 'login' }" class="nav-link text-light" :class="{ active: route.path === '/login/' }">Login</router-link>
                            <router-link :to="{ name: 'register' }" class="nav-link text-light" :class="{ active: route.path === '/register/' }">Register</router-link>
                            <!--
                            <router-link :to="{ name: '' }" class="nav-link" :class="{ active: route.path === '/' }">Example</router-link>
                            <router-link :to="{ name: '' }" class="nav-link" :class="{ active: route.path === '/' }">Example</router-link>
                            <router-link :to="{ name: '' }" class="nav-link" :class="{ active: route.path === '/' }">Example</router-link>
                            <router-link :to="{ name: '' }" class="nav-link" :class="{ active: route.path === '/' }">Example</router-link>
                            -->
                    </div>
                </div>
            </div>
        </nav>
    </header>
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router';
const route = useRoute();


</script>
