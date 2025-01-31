import { File } from "@/types/File";
import { User } from "@/types/User";

export interface Message {
  id: number;
  content: string;
  created_at: string;
  author: User;
  file: File | null;
}
