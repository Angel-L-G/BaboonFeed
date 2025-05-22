import type { PublicUserDto } from '@/dtos/PublicUserDto.ts'

export interface Group {
    id: string
    name: string
    avatar_url: string
    leader: PublicUserDto
    members: PublicUserDto[]
}
