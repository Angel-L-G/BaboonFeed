<script setup lang="ts">
import type { Group } from '@/types/Group.ts'
defineProps<{
    group: Group
}>()
</script>

<template>
    <div class="flex align-items-center gap-4 p-4 rounded shadow border group-card mb-2">
        <img :src="group.avatar_url" alt="Avatar" class="rounded-full img"/>
        <h2 class="text-lg font-semibold"><slot></slot></h2>
    </div>
</template>

<style scoped>
.img {
    width: 3rem;
    height: 3rem;
    object-fit: cover;
    border: 1px solid white;
}

.group-card {
    display: flex;
    flex-direction: row;
    gap: 10px;
}
</style>
