import type { File } from "@/types/File";

export interface MessageReceived {
  id: number;
  content: string;
  created_at: string;
  author: string;
  receiver?: string;
  group?: number;
  file?: File;
}

export interface MessageSent {
    content: string;
    receiver?: string;
    group?: number;
    file?: File;
}
