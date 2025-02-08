import { describe, it, expect } from 'vitest';
import { mount } from '@vue/test-utils';
import UserProfile from '../../../views/user/UserProfile.vue';
import type { User } from '../../../types/User.ts';

const mockUser: User = {
    id: 1,
    email: 'john.doe@example.com',
    username: 'JohnDoe',
    created_at: '2025-02-07T10:00:00Z',
    bio: 'This is a bio',
    followers: 100,
    follows: 50,
    file: undefined,
};

describe('UserProfile.vue', () => {
    it('se monta correctamente', () => {
        const wrapper = mount(UserProfile, {
            props: {
                user: mockUser,
            },
        });
        expect(wrapper.exists()).toBe(true);
    });

    it('renderiza correctamente el username', () => {
        const wrapper = mount(UserProfile, {
            props: {
                user: mockUser,
            },
        });
        expect(wrapper.text()).toContain('Username: JohnDoe');
    });

    it('renderiza correctamente la bio', () => {
        const wrapper = mount(UserProfile, {
            props: {
                user: mockUser,
            },
        });
        expect(wrapper.text()).toContain('Bio: This is a bio');
    });

    it('renderiza correctamente el número de followers', () => {
        const wrapper = mount(UserProfile, {
            props: {
                user: mockUser,
            },
        });
        expect(wrapper.text()).toContain('Followers: 100');
    });

    it('renderiza correctamente el número de following', () => {
        const wrapper = mount(UserProfile, {
            props: {
                user: mockUser,
            },
        });
        expect(wrapper.text()).toContain('Following: 50');
    });

    it('renderiza la lista de posts', () => {
        const wrapper = mount(UserProfile, {
            props: {
                user: mockUser,
            },
        });
        const postItems = wrapper.findAll('.list-group-item');
        expect(postItems.length).toBe(5);
        expect(postItems[0].text()).toBe('A Post');
        expect(postItems[1].text()).toBe('A second Post');
        expect(postItems[2].text()).toBe('A third Post');
        expect(postItems[3].text()).toBe('A fourth Post');
        expect(postItems[4].text()).toBe('And a fifth Post');
    });
});
