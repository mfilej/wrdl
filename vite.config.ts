import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tidewave from 'tidewave/vite-plugin'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  plugins: [vue(), tailwindcss(), tidewave()],
  build: {
    outDir: 'dist'
  }
})
