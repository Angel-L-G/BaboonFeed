import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import Navbar from '../../components/Navbar.vue';
import { createRouter, createWebHistory } from 'vue-router';

// Mock de Vue Router para evitar errores
const router = createRouter({
    history: createWebHistory(),
    routes: [{ path: '/', name: 'home', component: {} }],
});

describe('Navbar.vue', () => {
    it('se monta correctamente', async () => {
        router.push('/');
        await router.isReady();

        const wrapper = mount(Navbar, {
            global: {
                plugins: [router],
            },
        });

        expect(wrapper.exists()).toBe(true);
    });

    it('contiene un enlace a Home con router-link', async () => {
        router.push('/');
        await router.isReady();

        const wrapper = mount(Navbar, {
            global: {
                plugins: [router],
            },
        });

        const homeLink = wrapper.find('.navbar-brand');
        expect(homeLink.exists()).toBe(true);
        expect(homeLink.text()).toBe('Home');
    });

    it('contiene el botón de hamburguesa para colapsar el menú', () => {
        const wrapper = mount(Navbar);
        const toggler = wrapper.find('.navbar-toggler');
        expect(toggler.exists()).toBe(true);
    });

    it('contiene el contenedor de navegación', () => {
        const wrapper = mount(Navbar);
        const navbarCollapse = wrapper.find('.collapse.navbar-collapse');
        expect(navbarCollapse.exists()).toBe(true);
    });
});
