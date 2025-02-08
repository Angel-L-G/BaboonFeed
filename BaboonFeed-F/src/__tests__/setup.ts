import { config } from '@vue/test-utils';
import { vi } from 'vitest'

config.global.mocks = {
    $t: (msg: string) => msg,
};

global.window.matchMedia = global.window.matchMedia || (() => {
    return {
        matches: false,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
    };
});

