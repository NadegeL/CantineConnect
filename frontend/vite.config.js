import vue from '@vitejs/plugin-vue';

import { defineConfig } from 'vite';

import path from 'path';

import UnoCSS from 'unocss/vite';
import { presetUno, presetIcons } from 'unocss';

export default defineConfig({
  plugins: [
    vue(),
    UnoCSS({
      presets: [
        presetUno(),
        presetIcons({
          scale: 1.2,
          collections: {
            mdi: () => import('@iconify-json/mdi/icons.json').then(i => i.default),
          }
        }),
      ]
    }),

  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
