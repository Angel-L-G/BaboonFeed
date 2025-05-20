export interface File {
  id?: number;
  file: string;
  type: string;
}

export enum FileTypes {
  IMAGE = 'image',
  AUDIO = 'audio',
  VIDEO = 'video'
}
