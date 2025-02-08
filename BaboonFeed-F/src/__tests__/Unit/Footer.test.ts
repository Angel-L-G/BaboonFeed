import { describe, it, expect, vi } from 'vitest';
import { mount } from '@vue/test-utils';
import Footer from '../../components/Footer.vue';

describe('Footer.vue', () => {
    it('se monta correctamente', () => {
        const wrapper = mount(Footer);
        expect(wrapper.exists()).toBe(true);
    });

    it('contiene las secciones Links, Creators y Documentation', () => {
        const wrapper = mount(Footer);

        expect(wrapper.text()).toContain('Links');
        expect(wrapper.text()).toContain('Creators');
        expect(wrapper.text()).toContain('Documentation');
    });
});
