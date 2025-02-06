import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'home',
      component: () => import('@/views/Home.vue'),
    },
    {
      path: '/posts/add/',
      name: 'createPost',
      component: () => import('@/components/post/CreatePost.vue'),
    }
  ],
})

export default router
