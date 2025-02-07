<template>
  <nav class="navbar navbar-expand-lg bg-primary">
    <div class="container-fluid">
      <router-link :to="{ name: '' }" class="navbar-brand text-light">Home</router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup"
        aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
            <!--<router-link :to="{ name: 'createPost' }" class="nav-link text-light" :class="{ active: route.path === '/posts/add/' }">Create Post</router-link>

            <router-link :to="{ name: '' }" class="nav-link" :class="{ active: route.path === '/' }">Example</router-link>
            <router-link :to="{ name: '' }" class="nav-link" :class="{ active: route.path === '/' }">Example</router-link>
            <router-link :to="{ name: '' }" class="nav-link" :class="{ active: route.path === '/' }">Example</router-link>
            <router-link :to="{ name: '' }" class="nav-link" :class="{ active: route.path === '/' }">Example</router-link>
            -->
        </div>
      </div>
    </div>
  </nav>
  <router-view />
</template>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';

const router = useRouter();
const route = useRoute();


</script>
