import type { User } from '@/types/User'
import type { File } from '@/types/File'

export interface Post {
    id: number
    content: string
    created_at: string
    user: User
    file?: File
    likes: number[]
    dislikes: number[]
}

export interface PostCreate {
    content: string
    file?: File
}

export interface Reply {
    id: number
    content: string
    created_at: string
    replies: Reply[]
    post: Post
    user: User
    likes_count: number[]
    dislikes_count: number[]
}
