<script setup lang="ts">
import type { Group } from '@/types/Group.ts'
defineProps<{
    group: Group
}>()
</script>

<template>
    <div class="flex align-items-center justify-content-between gap-4 p-4 rounded shadow border">
        <img :src="group.avatar_url" alt="Avatar" class="w-12 h-12 rounded-full object-cover" />
        <h2 class="text-lg font-semibold"><slot></slot></h2>
    </div>
</template>
