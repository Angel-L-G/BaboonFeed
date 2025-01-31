export interface File {
  id: number;
  name: string;
  type: FileTypes;
}

enum FileTypes {
  IMAGE = 'image',
  AUDIO = 'audio',
  VIDEO = 'video'
}
