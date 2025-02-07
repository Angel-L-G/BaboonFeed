import type { File } from "./File";
import type { User } from "./User";

export interface Group {
  id: number;
  name: string;
  file: File | null;
  leader: User;
  members: User[];
}
