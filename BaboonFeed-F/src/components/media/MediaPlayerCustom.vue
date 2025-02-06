<template>
    <div>
        <media-player title="Sprite Fight" :src="file.name">
            <media-provider></media-provider>
        </media-player>
    </div>
</template>

<script setup lang="ts">
import { File } from '../../types/File';
import 'vidstack/bundle';

const {file, width = 500, height = 500, border = 0} = defineProps<{
    file: File,
    width: number,
    height: number
    border: number
}>();


</script>