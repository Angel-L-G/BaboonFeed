import type { User } from './User'

export interface Group {
    id: number
    name: string
    avatar_url: string
    leader: User
    members: User[]
}
