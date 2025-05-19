<template>
    <div class="align-items-end" role="group" :aria-label="`Archivo multimedia del post`">
        <!-- Imagen -->
        <img v-if="file.type === FileTypes.IMAGE" :src="file.file"
             alt="Imagen del post" class="img-fluid rounded"/>

        <!-- Video -->
        <Plyr v-else-if="file.type === FileTypes.VIDEO">
            <video controls :title="`Video del post`">
                <source :src="file.file" type="video/mp4" />
                <track kind="captions" srclang="es" label="Subtítulos en español"
                       src="/subtitulos/video-subtitles.vtt" default/>
                Tu navegador no soporta el video.
            </video>
        </Plyr>

        <!-- Audio -->
        <Plyr v-else-if="file.type === FileTypes.AUDIO">
            <audio controls class="audio-container" :aria-label="`Audio del post`">
                <source :src="file.file" type="audio/mp3" />
                Tu navegador no soporta el audio.
            </audio>
        </Plyr>
    </div>
</template>

<script setup lang="ts">
import type { File } from '@/types/File.ts';
import { FileTypes } from '@/types/File.ts';
import "vue-plyr/dist/vue-plyr.css";
import Plyr from "vue-plyr";

const { file } = defineProps<{file: File}>();

</script>
