import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

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
            component: () => import('@/views/HomePage.vue'),
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
            meta: { requiresAuth: true },
        },
        {
            path: '/chat/:id?',
            name: 'chat',
            component: () => import('@/components/Chat/Chat.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: '/users/profile/:username',
            name: 'profile',
            component: () => import('@/views/user/UserProfile.vue'),
            meta: { requiresAuth: true },
        },
        {
            path: '/groups/',
            name: 'groups',
            component: () => import('@/components/group/GroupList.vue'),
            meta: { requiresAuth: true },
        }
    ],
})

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore()
    if (to.meta.requiresAuth && !authStore.isAuthenticated) {
        next('/login/')
    } else {
        next()
    }
})

export default router
