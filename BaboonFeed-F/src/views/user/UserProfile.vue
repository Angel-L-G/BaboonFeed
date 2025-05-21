<script setup lang="ts">
import { onMounted, ref } from "vue";
import { API_URL } from "@/globals";
import { useAuthStore } from '@/stores/auth.ts'
import axios from 'axios'
import type { User } from '@/types/User.ts'
import { useRoute } from 'vue-router'
import type { Post } from '@/types/Post.ts'
import PostView from '@/components/post/PostView.vue'
import EditUser from '@/components/EditUser.vue'

const authStore = useAuthStore();
const route = useRoute();
const username = route.params.username as string;

const loading = ref(true);
const errorMsg = ref<string | null>(null);
const user = ref<User | null>(null);
const posts = ref<Post[]>([]);

onMounted(async () => {
    if (authStore.user!.username === username) {
        user.value = authStore.user;
        loading.value = false;
    } else {
        try {
            const response = await axios.get(`${API_URL}users/${username}`, {
                headers: {
                    'Authorization': 'Bearer ' + authStore.token
                }
            });

            user.value = await response.data;
        } catch (err) {
            errorMsg.value = (err as Error).message;
        } finally {
            loading.value = false;
        }
    }
    if (user.value) {
        const response = await axios.get(`${API_URL}posts/?user_id=${user.value.id}`,
            {
                headers: {
                    'Authorization': 'Bearer ' + authStore.token
                }
            });
        posts.value = await response.data.results;
    }
});

const followUser = async () => {
    if (!authStore.isAuthenticated) {
        alert('You need to login to follow/unfollow a user');
        return;
    }
    try {
        await axios.patch(`${API_URL}users/${username}/follow/`, {}, {
            headers: {
                'Authorization': `Bearer ${authStore.token}`
            }
        });
        if (user.value!.followers.includes(authStore.user!.username)) {
            user.value!.followers = user.value!.followers.filter(follower => follower !== authStore.user!.username);
        } else {
            user.value!.followers.push(authStore.user!.username);
        }
    } catch (error) {
        console.error('Error:', error);
    }
};

const isFollowing = () => {
    return user.value?.followers.includes(authStore.user!.username);
};
</script>

<template>
    <div class="container profile-container mt-4">
        <div v-if="loading" class="text-center" aria-live="polite" aria-busy="true">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Cargando...</span>
            </div>
        </div>

        <div v-else-if="errorMsg" class="alert alert-danger text-center" role="alert" aria-live="assertive">
            {{ errorMsg }}
        </div>

        <div v-else-if="user" class="card profile-card bg-dark text-light" role="region"
             :aria-label="`Perfil de ${user.username}`">
            <div class="row g-0">
                <div class="col-md-4 d-flex align-items-center justify-content-center p-3">
                    <img
                        :src="user.avatar"
                        class="rounded-circle img-fluid profile-img border-2 border-cyan"
                        alt="Profile Picture"
                    />
                </div>

                <div class="col-md-8">
                    <div class="card-body d-flex align-items-center justify-content-between gap-4">
                        <h1 class="card-title mb-2 fw-bold fs-1 text-center">{{ user.username }}</h1>

                        <div class="d-flex gap-2 align-items-end">
                            <button class="btn btn-purple-alt" v-if="authStore.user!.username !== username" @click="followUser()">
                                {{ isFollowing() ? 'Unfollow' : 'Follow' }}
                            </button>
                            <div class="badge badge-hover text-center" role="group" aria-label="Seguidores">
                                <div class="d-flex align-items-center gap-1 mb-2">
                                    <font-awesome-icon :icon="['fas', 'users']" class="fs-6" />
                                    <span class="fs-6 fw-bold">{{ user.followers?.length || 0 }}</span>
                                </div>
                                <span class="badge-text ">Followers</span>
                            </div>

                            <div class="badge badge-hover text-center">
                                <div class="d-flex align-items-center gap-1 mb-2">
                                    <font-awesome-icon :icon="['fas', 'user-plus']" class="fs-6" />
                                    <span class="fs-6 fw-bold">{{ user.following?.length || 0 }}</span>
                                </div>
                                <span class="badge-text">Following</span>
                            </div>
                            <button class="btn btn-purple-alt" data-bs-toggle="modal" v-if="authStore.user!.username === username" data-bs-target="#EditUserModal">
                                <font-awesome-icon :icon="['fas', 'pencil']" />
                            </button>
                        </div>
                    </div>

                    <p class="card-text bio-text mt-3 bg-dark-light border-3 border-start border-cyan rounded ps-1 pt-2 me-3 text-gold-light"
                       :aria-label="user.bio ? `Biografía: ${user.bio}` : 'This user doesn\'t have a bio'">
                        {{ user.bio || "This user doesn't have a bio." }}
                    </p>
                </div>
            </div>

            <div class="row justify-content-center scroll-content" v-if="posts.length > 0">
                <div
                    class="col-md-12 col-lg-9 me-2 content d-flex w-100 flex-column justify-content-center align-items-center overflow-hidden"
                    role="list"
                    aria-labelledby="home-heading"
                >
                    <PostView v-for="post in posts" :key="post.id" :post="post" role="listitem" />
                </div>
            </div>
            <div v-else class="text-center mt-3">
                <p class="text-primary-alt">{{ authStore.user!.username === username ? "You don't" : "This user doesn't"}} have any posts</p>
            </div>
        </div>
    </div>

    <div class="modal fade" id="EditUserModal" tabindex="-1"
         aria-labelledby="EditUserModalLabel" aria-hidden="true" role="dialog">
        <div class="modal-dialog" role="document">
            <div class="modal-content bg-secondary text-light">
                <header class="modal-header" data-bs-theme="dark">
                    <h2 id="EditUserModalLabel" class="modal-title text-center">Edit User</h2>
                    <button type="button" class="btn-close" data-bs-dismiss="modal"
                            aria-label="Cerrar modal"/>
                </header>
                <div class="modal-body">
                    <EditUser :username="username"/>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.profile-container {
    position: absolute;
    left: 50%;
    transform: translateX(-50%);
    top: 35px;
    max-width: 800px;
    width: 100%;
}

.profile-card {
    border-radius: 15px;
    overflow: hidden;
}

.profile-img {
    width: 150px;
    height: 150px;
    object-fit: cover;
    border: 4px solid white;
}

.bio-text {
    max-height: 80px;
    min-height: 80px;
    overflow: auto;
    font-size: 1rem;
    line-height: 1.4;
    padding-right: 5px;
}

.bio-text::-webkit-scrollbar {
    display: none;
}

.bio-text {
    scrollbar-width: none;
}

.card-body {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 4rem;
    padding: 10px 10px 0 0;
}

.badge-text {
    font-size: 0.8rem;
    color: rgba(255, 255, 255, 0.8);
}

@media (max-width: 991px) {
    .profile-container {
        position: relative;
        left: auto;
        transform: none;
        top: 35px;
        width: 100%;
        padding-right: 10px;
    }

    .profile-card {
        flex-direction: column;
    }

    .row.g-0 {
        flex-direction: column;
    }

    .col-md-4,
    .col-md-8 {
        width: 100%;
        text-align: center;
    }

    .profile-img {
        width: 120px;
        height: 120px;
        margin: 0 auto;
    }

    .card-body {
        flex-direction: column;
        align-items: center;
        gap: 1rem;
        padding: 10px;
    }

    .bio-text {
        font-size: 0.9rem;
        margin: 0 1rem;
        max-height: none;
        min-height: auto;
        padding: 10px;
    }

    .scroll-content {
        padding-left: 0;
        padding-right: 0;
    }

    .content {
        margin-left: 0 !important;
    }
}
</style>
