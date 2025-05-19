<script setup lang="ts">
import type { MessageReceived } from '@/types/Message.ts'
import { computed, type PropType, ref, toRaw, watch } from 'vue'
import { useAuthStore} from '@/stores/auth.ts';
import { formatDate } from '@/plugins/daysjs/Daysjs.ts'

const authStore = useAuthStore();
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
                'bg-success float-start ms-2 me-5': props.message.author === author,
                'bg-info float-end me-2 ms-5': props.message.author !== author,
            }"
        >
            <div class="card-body">
                <small class="text-muted">{{ formatDate(props.message.created_at) }}</small>
                <p class="card-text text-break">{{ props.message.content }}</p>
            </div>
        </div>
    </div>
    <div v-else>
        <p class="text-muted">Esperando mensaje...</p>
    </div>
</template>
