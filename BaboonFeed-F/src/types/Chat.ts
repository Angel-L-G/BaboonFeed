import type { User } from '@/types/User.ts'

export interface Chat {
    id: number;
    last_modified: string;
    last_message: string;
    users: User[];
}
