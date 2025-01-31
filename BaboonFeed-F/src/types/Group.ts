import { File } from "./File";
import { User } from "./User";

export interface Group {
  id: number;
  name: string;
  file: File | null;
  leader: User;
  members: User[];
}
