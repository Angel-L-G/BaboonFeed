import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import App from '../../App.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Mock de Vue Router para evitar errores
const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: '/', name: 'home', component: {} },
        { path: '/posts/add/', name: 'createPost', component: {} },
        { path: '/chat', name: 'chat', component: {} },
    ],
});

describe('App.vue', () => {
    it('debe montarse correctamente y contener contenido', async () => {
        router.push('/');
        await router.isReady();

        const wrapper = mount(App, {
            global: {
                plugins: [router],
                stubs: {
                    'font-awesome-icon': true, // Mock del componente para evitar el error
                },
            },
        });

        expect(wrapper.exists()).toBe(true);

        expect(wrapper.html()).not.toBe('');
    });
});
