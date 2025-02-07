import { config } from '@vue/test-utils';

// Mock global para Vue i18n (si lo usas)
config.global.mocks = {
    $t: (msg: string) => msg,
};
