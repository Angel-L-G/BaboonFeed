import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import HomePage from '@/components/HomePage.vue';

vi.hoisted(() => {
    Object.defineProperty(window, "matchMedia", {
        writable: true,
        enumerable: true,
        value: vi.fn().mockImplementation((query) => ({
            matches: false,
            media: query,
            onchange: null,
            addListener: vi.fn(), // deprecated
            removeListener: vi.fn(), // deprecated
            addEventListener: vi.fn(),
            removeEventListener: vi.fn(),
            dispatchEvent: vi.fn(),
        })),
    });
});

describe('HomePage.vue', () => {

    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('se monta correctamente', () => {
        const wrapper = mount(HomePage);
        expect(wrapper.exists()).toBe(true);
    });

    it('carga y renderiza los posts correctamente', async () => {
        // Datos simulados de la API
        const mockPosts = [
            { id: 1, content: 'Post 1', file: { name: 'post1.jpg' } },
            { id: 2, content: 'Post 2', file: { name: 'post2.jpg' } }
        ];

        // Mockea la función fetch
        vi.fn().mockResolvedValueOnce({
            json: async () => mockPosts, // Simula el método json() que devuelve mockPosts
            status: 200, // Código de estado HTTP
            statusText: 'OK', // Texto de estado HTTP
            headers: { 'Content-Type': 'application/json' }, // Cabecera de la respuesta
        });

        const wrapper = mount(HomePage);
        await new Promise(setImmediate);

        // Verifica que se renderizan los posts
        const postElements = wrapper.findAll('p');
        expect(postElements.length).toBeGreaterThan(1); // Debe haber contenido de post
    });


    it('carga y renderiza los usuarios correctamente', async () => {
        // Datos simulados de la API
        const mockUsers = [
            { id: 1, username: 'Usuario1', file: { name: 'user1.jpg' } },
            { id: 2, username: 'Usuario2', file: { name: 'user2.jpg' } }
        ];

        // Mockea la función fetch
        vi.fn().mockResolvedValueOnce({
            json: async () => mockUsers, // Simula el método json() que devuelve mockPosts
            status: 200, // Código de estado HTTP
            statusText: 'OK', // Texto de estado HTTP
            headers: { 'Content-Type': 'application/json' }, // Cabecera de la respuesta
        });

        const wrapper = mount(HomePage);
        await new Promise(setImmediate);

        // Verifica que se renderizan los usuarios
        const userElements = wrapper.findAll('h2');
        expect(userElements.length).toBeGreaterThan(1); // Debe haber nombres de usuario
    });
});
