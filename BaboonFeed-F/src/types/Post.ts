import { User } from "@/types/User";
import { File } from "@/types/File";

export interface Post {
  id: number;
  content: string;
  created_at: string;
  user: User;
  file: File | null;
  likes: number[];
  dislikes: number[];
}

export interface Reply {
  id: number;
  content: string;
  created_at: string;
  replies: Reply[];
  post: Post;
  user: User;
}
