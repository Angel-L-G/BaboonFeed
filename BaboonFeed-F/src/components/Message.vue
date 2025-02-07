<script setup lang="ts">
import type {Message} from "@/types/Message.ts";
import type {PropType} from "vue";
defineProps(
    {
        message: {
            type: Object as PropType<Message>,
            required: true
        }
    }
);

const author = 1;
</script>

<template>
    <div class="col">
        <div class="card" :class="{ 'bg-success float-start ms-2 me-5': message.author === author, 'bg-info float-end me-2 ms-5': message.author !== author }">
            <div class="card-body">
                <small class="text-muted">{{ message.created_at }}</small>
                <p class="card-text text-break">{{ message.content }}</p>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
