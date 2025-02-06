export interface File {
  id: number;
  name: string;
  type: FileTypes;
}

export enum FileTypes {
  IMAGE = 'image',
  AUDIO = 'audio',
  VIDEO = 'video'
}
