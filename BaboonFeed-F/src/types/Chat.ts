import type { User } from '@/types/User.ts'

export interface Chat {
    id: string;
    last_modified: string;
    last_message: string;
    users: User[];
    type: ChatType;
}

export enum ChatType{
    PRIVATE = 'private',
    GROUP = 'group'
}
