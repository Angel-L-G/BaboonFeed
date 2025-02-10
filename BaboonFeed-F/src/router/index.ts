import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            redirect: '/login/',
        },
        {
            path: '/home/',
            name: 'home',
            component: () => import('@/components/HomePage.vue'),
        },
        {
            path: '/login/',
            name: 'login',
            component: () => import('@/views/auth/Login.vue'),
        },
        {
            path: '/register/',
            name: 'register',
            component: () => import('@/views/auth/Register.vue'),
        },
        {
            path: '/posts/add/',
            name: 'createPost',
            component: () => import('@/components/post/CreatePost.vue'),
        },
        {
            path: '/chat/',
            name: 'chat',
            component: () => import('@/components/Chat.vue'),
        },
        {
            path: '/users/profile/:username',
            name: 'profile',
            component: () => import('@/views/user/UserProfile.vue'),
        },
    ],
})

export default router
