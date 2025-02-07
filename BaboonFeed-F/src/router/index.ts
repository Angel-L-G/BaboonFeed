import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/components/HomePage.vue'),
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
    }],
})

export default router
