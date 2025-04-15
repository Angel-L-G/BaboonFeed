<template>
    <div>
        <img v-if="file.type == FileTypes.IMAGE" :src="file.file" alt="post">
        <Plyr v-else>
            <video v-if="file.type == FileTypes.VIDEO" controls>
                <source src="https://www.w3schools.com/html/mov_bbb.mp4" type="video/mp4" />
            </video>
            <div v-else-if="file.type == FileTypes.AUDIO" class="bg-dark">
                <audio controls class="audio-container">
                    <source src="https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3" type="audio/mp3"/>
                </audio>
            </div>
        </Plyr>
    </div>
</template>

<script setup lang="ts">
import type { File } from '../../types/File';
import { FileTypes } from '../../types/File';
import "vue-plyr/dist/vue-plyr.css";
import Plyr from "vue-plyr";

const { file } = defineProps<{file: File}>();

</script>
