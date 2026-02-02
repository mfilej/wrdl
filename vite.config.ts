import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tidewave from 'tidewave/vite-plugin'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  base: '/wrdl/',
  plugins: [vue(), tailwindcss(), tidewave()],
  build: {
    outDir: 'dist'
  }
})
