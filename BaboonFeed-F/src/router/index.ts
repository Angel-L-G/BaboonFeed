import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/components/HomePage.vue'

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
    }
  ],
})

export default router
