import { describe, it, expect, vi, beforeEach } from 'vitest';
import { mount } from '@vue/test-utils';
import CreatePost from '@/components/post/CreatePost.vue';

describe('CreatePost.vue', () => {
    beforeEach(() => {
        vi.clearAllMocks();
    });

    it('se monta correctamente', () => {
        const wrapper = mount(CreatePost);
        expect(wrapper.exists()).toBe(true);
    });

    it('permite escribir contenido en el input', async () => {
        const wrapper = mount(CreatePost);
        const input = wrapper.find('input[type="text"]');

        await input.setValue('Este es un nuevo post');

        expect(wrapper.vm.content).toBe('Este es un nuevo post');
    });

    it('permite seleccionar un archivo', async () => {
        const wrapper = mount(CreatePost, {
            global: {
                stubs: {
                    'font-awesome-icon': true,
                },
            },
        });
        const testFile = new File(['contenido'], 'test.png', { type: 'image/png' });

        // Llamamos directamente a la función de manejo de archivos
        wrapper.vm.handleFileChange({
            target: { files: [testFile] }
        } as unknown as Event);

        // Verificamos que el archivo se guardó en la variable `file`
        expect(wrapper.vm.file).not.toBe(null);
        expect(wrapper.vm.file?.name).toBe('test.png');
    });

    it('permite eliminar un archivo seleccionado', async () => {
        const wrapper = mount(CreatePost, {
            global: {
                stubs: {
                    'font-awesome-icon': true,
                },
            },
        });
        const removeButton = wrapper.find('button.btn-warning');

        const testFile = new File(['contenido'], 'test.png', { type: 'image/png' });

        wrapper.vm.handleFileChange({
            target: { files: [testFile] }
        } as unknown as Event);

        expect(wrapper.vm.file).not.toBe(null);

        await removeButton.trigger('click');

        expect(wrapper.vm.file).toBe(null);
    });

    it('envía el formulario correctamente con datos estructurados', async () => {
        const wrapper = mount(CreatePost, {
            global: {
                stubs: {
                    'font-awesome-icon': true,
                },
            },
        });
        const input = wrapper.find('input[type="text"]');
        const form = wrapper.find('form');

        const testFile = new File(['contenido'], 'test.png', { type: 'image/png' });

        wrapper.vm.handleFileChange({
            target: { files: [testFile] }
        } as unknown as Event);

        await input.setValue('Este es un nuevo post');

        // Espía la función `console.log` para verificar la salida
        const consoleSpy = vi.spyOn(console, 'log');

        await form.trigger('submit');

        expect(consoleSpy).toHaveBeenCalledWith({
            content: 'Este es un nuevo post',
            file: {
                name: 'png',
                type: 'image',
            },
        });

        consoleSpy.mockRestore();
    });
});
