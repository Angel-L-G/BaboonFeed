import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import ChatComponent from '@/components/Chat.vue';
import MessageComponent from '@/components/Message.vue';

// Mock de fetch
global.fetch = vi.fn();

describe('ChatComponent.vue', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('se monta correctamente', async () => {
        fetch.mockResolvedValueOnce({
            json: async () => [
                { id: 1, content: 'Hola', created_at: '2024-02-08', author: 1 },
            ],
        });

        const wrapper = mount(ChatComponent);

        expect(wrapper.exists()).toBe(true);
    });

    it('carga y muestra mensajes correctamente', async () => {
        fetch.mockResolvedValueOnce({
            json: async () => [
                { id: 1, content: 'Hola', created_at: '2024-02-08', author: 1 },
                { id: 2, content: '¿Cómo estás?', created_at: '2024-02-08', author: 2 },
            ],
        });

        const wrapper = mount(ChatComponent);
        await new Promise((resolve) => setTimeout(resolve, 0)); // Espera a que se resuelva el fetch

        const messages = wrapper.findAllComponents(MessageComponent);
        expect(messages.length).toBe(2);
    });

    it('envía un mensaje correctamente', async () => {
        fetch.mockResolvedValueOnce({ json: async () => [] }); // Para la carga inicial
        fetch.mockResolvedValueOnce({}); // Para la petición de POST

        const wrapper = mount(ChatComponent);

        // Simula escribir un mensaje
        const input = wrapper.find('input');
        await input.setValue('Nuevo mensaje');

        // Simula hacer click en el botón de enviar
        const button = wrapper.find('button');
        await button.trigger('click');

        // Verifica que fetch se llamó con la petición de POST
        expect(fetch).toHaveBeenCalledWith('http://localhost:3000/messages', expect.objectContaining({
            method: 'POST',
        }));

        // Verifica que el input se limpió después de enviar
        expect(wrapper.vm.newMessage).toBe('');
    });
});
