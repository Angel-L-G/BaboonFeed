import { File } from "@/types/File";

export interface User {
  id: number;
  email: string;
  username: string;
  created_at: string;
  bio: string;
  file: File | null;
  followers: number;
  follows: number;
}
