import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import CreatePost from '../../../components/post/CreatePost.vue';
//import type { File } from '../../../types/File.ts';

describe('CreatePost.vue', () => {

    it('se monta correctamente', () => {
        const wrapper = mount(CreatePost);
        expect(wrapper.exists()).toBe(true);
    });

    it('el valor de contenido se actualiza cuando se escribe en el input', async () => {
        const wrapper = mount(CreatePost);
        const input = wrapper.find('input[type="text"]');
        await input.setValue('Nuevo contenido para el post');
        expect(input.element.value).toBe('Nuevo contenido para el post');
    });

    /*it('el estado del archivo se actualiza al seleccionar un archivo', async () => {
        const wrapper = mount(CreatePost);
        const fileInput = wrapper.find('input[type="file"]');

        const file = new File(['dummy content'], 'image.png', { type: 'image/png' });
        await fileInput.trigger('change', {
            target: { files: [file] }
        });

        expect(wrapper.vm.file).toEqual(file);
    });

    it('el estado del archivo se elimina correctamente cuando se hace clic en "Remove File"', async () => {
        const wrapper = mount(CreatePost);
        const fileInput = wrapper.find('input[type="file"]');

        const file = new File(['dummy content'], 'image.png', { type: 'image/png' });
        await fileInput.trigger('change', {
            target: { files: [file] }
        });

        expect(wrapper.vm.file).toEqual(file);

        const removeButton = wrapper.find('button[type="button"]');
        await removeButton.trigger('click');

        expect(wrapper.vm.file).toBeNull();
    });

    it('llama a handleSubmit cuando se envía el formulario', async () => {
        const handleSubmitMock = vi.fn();
        const wrapper = mount(CreatePost);

        wrapper.vm.handleSubmit = handleSubmitMock;

        const submitButton = wrapper.find('button[type="submit"]');
        await submitButton.trigger('click');

        expect(handleSubmitMock).toHaveBeenCalled();
    });

    it('verifica el objeto de creación de post', async () => {
        const wrapper = mount(CreatePost);

        await wrapper.setData({ content: 'Contenido de prueba' });

        const file = new File(['dummy content'], 'test.jpg', { type: 'image/jpeg' });
        await wrapper.vm.handleFileChange({
            target: { files: [file] }
        } as Event);
        await wrapper.vm.handleSubmit();

        const createPost = {
            content: 'Contenido de prueba',
            file: {
                name: 'jpg',
                type: FileTypes.IMAGE,
            },
        };

        expect(wrapper.vm.createPost).toEqual(createPost);
    });*/
});
