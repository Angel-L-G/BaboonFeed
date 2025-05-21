<script setup lang="ts">

</script>

<template>
    <div class="container my-2">
        <h2 class="text-center">Login Required</h2>
        <p class="text-center">You need to login to access this</p>
        <router-link class="btn btn-purple-alt text-light w-100" :to="{ name: 'login' }">Go to Login</router-link>
    </div>
</template>
