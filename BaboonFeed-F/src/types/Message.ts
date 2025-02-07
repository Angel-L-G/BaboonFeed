import type { File } from "@/types/File";
import type { User } from "@/types/User";

export interface Message {
  id: number;
  content: string;
  created_at: string;
  author: User;
  file: File | null;
}
