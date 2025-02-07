// vitest.config.ts
import { defineConfig } from 'vitest/config';
import vue from '@vitejs/plugin-vue';

export default defineConfig({
    plugins: [vue()],
    test: {
        globals: true,
        environment: 'jsdom',
        setupFiles: './__tests__/setup.ts',
        coverage: {
            provider: 'istanbul',
            reporter: ['text', 'json', 'html'],
        },
    },
});
