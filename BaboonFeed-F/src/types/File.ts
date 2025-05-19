export interface File {
  id?: number;
  file: string;
  type: FileTypes;
}

export enum FileTypes {
  IMAGE = 'image',
  AUDIO = 'audio',
  VIDEO = 'video'
}
