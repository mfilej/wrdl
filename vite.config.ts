import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import tidewave from 'tidewave/vite-plugin'
import tailwindcss from '@tailwindcss/vite'
import { viteStaticCopy } from 'vite-plugin-static-copy'

export default defineConfig({
  base: '/wrdl/',
  plugins: [
    vue(),
    tailwindcss(),
    tidewave(),
    viteStaticCopy({
      targets: [
        { src: '*.txt', dest: '.' }
      ]
    })
  ],
  build: {
    outDir: 'dist'
  }
})
