import type { User } from '@/types/User.ts'

export interface Chat {
    id: string;
    name: string;
    avatar_url: string;
    last_modified: string;
    last_message: string;
    members: User[];
    type: ChatType;
}

export enum ChatType{
    PRIVATE = 'private',
    GROUP = 'group'
}
