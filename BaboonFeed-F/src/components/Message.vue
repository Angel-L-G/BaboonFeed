<script setup lang="ts">
import type { MessageReceived } from '@/types/Message.ts'
import { computed, type PropType, toRaw, watch } from 'vue'
import { useAuthStore } from '@/stores/auth.ts'
import { formatDate } from '@/plugins/daysjs/Daysjs.ts'
import FileHandler from '@/components/file/FileHandler.vue'

const authStore = useAuthStore()
const props = defineProps({
    message: {
        type: Object as PropType<MessageReceived>,
        required: false, // Ya no es obligatorio
        default: () => ({ author: '', content: '', created_at: '' }),
    },
})

const author = computed(() => authStore.user!.username as string)

watch(
    () => props.message,
    (newMessage) => {
        console.log('Message changed:', toRaw(newMessage))
    },
    { deep: true, immediate: true },
)
</script>

<template>
    <div class="col" v-if="props.message">
        <div
            class="card"
            :class="{
                'bg-primary float-end ms-2 me-5': props.message.author == author,
                'bg-success float-start me-2 ms-5': props.message.author != author,
            }"
        >
            <div class="card-body">
                <div class="d-flex justify-content-between align-items-center mb-1">
                    <p
                        v-if="props.message.group && props.message.author != author"
                        class="mb-0 fw-bold me-1"
                    >
                        {{ props.message.author }}
                    </p>
                    <small class="text-muted mb-0">{{
                        formatDate(props.message.created_at)
                    }}</small>
                </div>
                <FileHandler v-if="message.file" :file="message.file" />
                <p class="card-text text-break">{{ props.message.content }}</p>
            </div>
        </div>
    </div>
    <div v-else>
        <p class="text-muted">Esperando mensaje...</p>
    </div>
</template>
