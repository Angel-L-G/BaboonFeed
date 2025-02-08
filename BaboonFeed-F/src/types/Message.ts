import type { File } from "@/types/File";

export interface Message {
  id: number;
  content: string;
  created_at: string;
  author: number; //string;
  receiver?: string;
  group?: string;
  file?: File;
}
