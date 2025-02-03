import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  esbuild: {
    target: 'esnext',
    platform: 'linux'
  },
  server: {
    host: '0.0.0.0'
  }
})