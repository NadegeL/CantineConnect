import vue from '@vitejs/plugin-vue';

import { defineConfig } from 'vite';

import path from 'path';

import UnoCSS from 'unocss/vite';
import { presetUno } from 'unocss';

export default defineConfig({
  plugins: [
    vue(),
    UnoCSS(),
    presetUno(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
});
