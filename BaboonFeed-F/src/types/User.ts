export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
  bio: string;
  avatar?: string;
  followers: string[];
  following: string[];
}
